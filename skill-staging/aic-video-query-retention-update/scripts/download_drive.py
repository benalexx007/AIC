#!/usr/bin/env python3
"""Resolve a public Google Drive filename, then download it with validation."""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from email.message import Message
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse

import requests


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AICVideoQuery/1.0"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="Public Google Drive file or folder URL")
    parser.add_argument("--filename", help="Target filename when url is a Google Drive folder")
    parser.add_argument("--output-dir", help="Destination directory; required unless --probe-only")
    parser.add_argument("--probe-only", action="store_true")
    parser.add_argument("--workers", type=int, default=24)
    parser.add_argument("--retries", type=int, default=6)
    return parser.parse_args()


def is_folder_url(url: str) -> bool:
    parsed = urlparse(url)
    return "/folders/" in parsed.path or "folders" in parsed.query


def resolve_file_id_from_folder(folder_url_or_id: str, target_filename: str) -> str:
    from gdown.download_folder import _get_session, _parse_embedded_folder_view, _extract_folder_id

    folder_id = folder_url_or_id if not folder_url_or_id.startswith("http") else _extract_folder_id(folder_url_or_id)
    sess, _ = _get_session(proxy=None, use_cookies=True, user_agent=USER_AGENT)
    
    target_clean = target_filename.strip()
    target_stem = Path(target_clean).stem.lower()
    prefix_match = re.match(r"^([a-zA-Z0-9]+)_", target_clean)
    target_prefix = prefix_match.group(1).lower() if prefix_match else ""
    
    queue = [folder_id]
    visited = set()
    
    while queue:
        current_id = queue.pop(0)
        if current_id in visited:
            continue
        visited.add(current_id)
        
        try:
            _, children = _parse_embedded_folder_view(sess, current_id)
        except Exception:
            continue
            
        child_dirs_priority = []
        child_dirs_other = []
        for cid, cname, ctype in children:
            if ctype == "application/vnd.google-apps.folder":
                name_lower = cname.lower()
                if "keyframe" in name_lower or "map-" in name_lower:
                    continue  # Explicitly skip keyframes per specification
                if target_prefix and target_prefix in name_lower:
                    child_dirs_priority.append(cid)
                else:
                    child_dirs_other.append(cid)
            else:
                c_stem = Path(cname).stem.lower()
                if cname.lower() == target_clean.lower() or c_stem == target_stem:
                    return cid
                    
        # Process prioritized folders first (e.g. matching batch L24)
        queue = child_dirs_priority + queue + child_dirs_other
        
    raise FileNotFoundError(f"File '{target_filename}' was not found in video folders of {folder_url_or_id}")


def extract_drive_id(url: str, filename: str | None = None) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Google Drive input must be an HTTP(S) URL")
    
    if is_folder_url(url):
        if not filename:
            raise ValueError("--filename is required when --url is a Google Drive folder")
        return resolve_file_id_from_folder(url, filename)

    match = re.search(r"/file/d/([^/]+)", parsed.path)
    file_id = match.group(1) if match else parse_qs(parsed.query).get("id", [""])[0]
    if not file_id or not re.fullmatch(r"[A-Za-z0-9_-]+", file_id):
        raise ValueError("Could not extract a valid Google Drive file ID")
    return file_id


def direct_url(file_id: str) -> str:
    return (
        "https://drive.usercontent.google.com/download"
        f"?id={quote(file_id)}&export=download&confirm=t"
    )


def filename_from_headers(headers: requests.structures.CaseInsensitiveDict) -> str:
    disposition = headers.get("content-disposition", "")
    message = Message()
    if disposition:
        message["content-disposition"] = disposition
    filename = message.get_filename() or ""
    filename = Path(filename.strip()).name
    if not filename or filename in {".", ".."}:
        raise RuntimeError(
            "Google Drive did not expose the original filename; stopping before download."
        )
    return filename


def probe(url: str) -> dict:
    with requests.get(
        url,
        headers={"Range": "bytes=0-0", "User-Agent": USER_AGENT},
        stream=True,
        timeout=(30, 120),
        allow_redirects=True,
    ) as response:
        response.raise_for_status()
        filename = filename_from_headers(response.headers)
        content_range = response.headers.get("content-range", "")
        if "/" in content_range:
            total = int(content_range.rsplit("/", 1)[1])
        else:
            total = int(response.headers.get("content-length") or 0)
        if total <= 0:
            raise RuntimeError("Google Drive did not provide a valid file size")
        return {
            "filename": filename,
            "size_bytes": total,
            "content_type": response.headers.get("content-type", ""),
            "range_supported": response.status_code == 206,
            "download_url": response.url,
        }


class Progress:
    def __init__(self, total: int) -> None:
        self.total = total
        self.done = 0
        self.started = time.monotonic()
        self.last_print = 0.0
        self.lock = threading.Lock()

    def add(self, amount: int) -> None:
        with self.lock:
            self.done += amount
            now = time.monotonic()
            if now - self.last_print >= 2.0 or self.done >= self.total:
                elapsed = max(0.001, now - self.started)
                speed = self.done / elapsed / (1024 * 1024)
                print(
                    f"download={100 * self.done / self.total:6.2f}% "
                    f"bytes={self.done}/{self.total} speed={speed:.2f} MiB/s",
                    flush=True,
                )
                self.last_print = now


def download_part(
    index: int,
    url: str,
    start: int,
    end: int,
    parts_dir: Path,
    retries: int,
    progress: Progress,
) -> Path:
    expected = end - start + 1
    final_part = parts_dir / f"part-{index:04d}.bin"
    partial_part = parts_dir / f"part-{index:04d}.tmp"
    if final_part.is_file() and final_part.stat().st_size == expected:
        progress.add(expected)
        return final_part
    if final_part.exists():
        final_part.unlink()

    for attempt in range(1, retries + 1):
        have = partial_part.stat().st_size if partial_part.exists() else 0
        if have > expected:
            partial_part.unlink()
            have = 0
        if have == expected:
            partial_part.replace(final_part)
            progress.add(expected)
            return final_part
        try:
            with requests.get(
                url,
                headers={
                    "Range": f"bytes={start + have}-{end}",
                    "User-Agent": USER_AGENT,
                },
                stream=True,
                timeout=(30, 180),
            ) as response:
                if response.status_code != 206:
                    raise RuntimeError(f"part {index}: expected HTTP 206, got {response.status_code}")
                mode = "ab" if have else "wb"
                with partial_part.open(mode) as stream:
                    for chunk in response.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            stream.write(chunk)
                            progress.add(len(chunk))
            actual = partial_part.stat().st_size
            if actual != expected:
                raise RuntimeError(f"part {index}: expected {expected} bytes, got {actual}")
            partial_part.replace(final_part)
            return final_part
        except Exception as error:
            if attempt >= retries:
                raise
            print(f"part={index} retry={attempt}/{retries} error={error}", flush=True)
            time.sleep(min(15, 2**attempt))
    raise RuntimeError(f"part {index} failed")


def download_single(url: str, output: Path, total: int) -> None:
    temporary = output.with_suffix(output.suffix + ".partial")
    progress = Progress(total)
    with requests.get(url, headers={"User-Agent": USER_AGENT}, stream=True, timeout=(30, 180)) as response:
        response.raise_for_status()
        with temporary.open("wb") as stream:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    stream.write(chunk)
                    progress.add(len(chunk))
    if temporary.stat().st_size != total:
        raise RuntimeError(f"Downloaded size mismatch: {temporary.stat().st_size} != {total}")
    os.replace(temporary, output)


def download_parallel(url: str, output: Path, total: int, workers: int, retries: int) -> None:
    workers = min(workers, max(1, total))
    parts_dir = output.with_suffix(output.suffix + ".parts")
    parts_dir.mkdir(parents=True, exist_ok=True)
    part_size = math.ceil(total / workers)
    ranges = [
        (index, index * part_size, min(total - 1, (index + 1) * part_size - 1))
        for index in range(workers)
        if index * part_size < total
    ]
    progress = Progress(total)
    completed: dict[int, Path] = {}
    with ThreadPoolExecutor(max_workers=len(ranges)) as executor:
        futures = {
            executor.submit(
                download_part, index, url, start, end, parts_dir, retries, progress
            ): index
            for index, start, end in ranges
        }
        for future in as_completed(futures):
            completed[futures[future]] = future.result()

    merged = output.with_suffix(output.suffix + ".merge")
    with merged.open("wb") as destination:
        for index in range(len(ranges)):
            with completed[index].open("rb") as source:
                shutil.copyfileobj(source, destination, length=1024 * 1024)
    if merged.stat().st_size != total:
        raise RuntimeError(f"Merged size mismatch: {merged.stat().st_size} != {total}")
    for attempt in range(10):
        try:
            os.replace(merged, output)
            break
        except PermissionError:
            if attempt == 9:
                raise
            time.sleep(0.3)
    for path in completed.values():
        try:
            path.unlink(missing_ok=True)
        except Exception:
            pass
    try:
        parts_dir.rmdir()
    except Exception:
        pass


def download_drive(
    url: str,
    output_dir: Path,
    filename: str | None = None,
    workers: int = 8,
    retries: int = 6,
) -> tuple[Path, dict]:
    if workers < 1 or workers > 64:
        raise ValueError("workers must be between 1 and 64")
    file_id = extract_drive_id(url, filename)
    resolved_url = direct_url(file_id)
    metadata = probe(resolved_url)
    output_dir.mkdir(parents=True, exist_ok=True)
    output = (output_dir / metadata["filename"]).resolve()
    if output.parent != output_dir.resolve():
        raise RuntimeError("Unsafe filename returned by Google Drive")
    if output.is_file() and output.stat().st_size == metadata["size_bytes"]:
        metadata["reused_existing"] = True
        return output, metadata
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite mismatched existing file: {output}")
    if metadata["range_supported"]:
        download_parallel(resolved_url, output, metadata["size_bytes"], workers, retries)
    else:
        download_single(resolved_url, output, metadata["size_bytes"])
    if output.stat().st_size != metadata["size_bytes"]:
        raise RuntimeError("Final file size validation failed")
    metadata["reused_existing"] = False
    return output, metadata


def main() -> int:
    args = parse_args()
    file_id = extract_drive_id(args.url, args.filename)
    metadata = probe(direct_url(file_id))
    if args.probe_only:
        print(json.dumps(metadata, ensure_ascii=False))
        return 0
    if not args.output_dir:
        raise ValueError("--output-dir is required unless --probe-only is used")
    output, metadata = download_drive(
        args.url,
        Path(args.output_dir).resolve(),
        filename=args.filename,
        workers=args.workers,
        retries=args.retries,
    )
    print(json.dumps({"output": str(output), **metadata}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
