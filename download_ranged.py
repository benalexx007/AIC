#!/usr/bin/env python3
"""Download one HTTP file with validated parallel byte ranges."""

from __future__ import annotations

import argparse
import math
import os
import shutil
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--size", type=int)
    parser.add_argument("--workers", type=int, default=16)
    parser.add_argument("--retries", type=int, default=6)
    return parser.parse_args()


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
                speed = self.done / elapsed
                percent = 100.0 * self.done / self.total
                print(
                    f"progress={percent:6.2f}% bytes={self.done}/{self.total} speed={speed / 1024:.1f} KiB/s",
                    flush=True,
                )
                self.last_print = now


def probe_size(url: str) -> int:
    response = requests.get(
        url,
        headers={"Range": "bytes=0-0", "User-Agent": "Mozilla/5.0"},
        stream=True,
        timeout=(30, 120),
    )
    response.raise_for_status()
    content_range = response.headers.get("content-range", "")
    response.close()
    if "/" not in content_range:
        raise RuntimeError("Server did not provide total size in Content-Range")
    return int(content_range.rsplit("/", 1)[1])


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
        range_start = start + have
        try:
            with requests.get(
                url,
                headers={
                    "Range": f"bytes={range_start}-{end}",
                    "User-Agent": "Mozilla/5.0",
                },
                stream=True,
                timeout=(30, 180),
            ) as response:
                if response.status_code != 206:
                    raise RuntimeError(f"Part {index}: expected HTTP 206, got {response.status_code}")
                mode = "ab" if have else "wb"
                with partial_part.open(mode) as stream:
                    for chunk in response.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            stream.write(chunk)
                            progress.add(len(chunk))
            if partial_part.stat().st_size != expected:
                raise RuntimeError(
                    f"Part {index}: expected {expected} bytes, got {partial_part.stat().st_size}"
                )
            partial_part.replace(final_part)
            return final_part
        except Exception as error:
            if attempt >= retries:
                raise
            print(f"part={index} retry={attempt}/{retries} error={error}", flush=True)
            time.sleep(min(15, 2**attempt))
    raise RuntimeError(f"Part {index} failed")


def main() -> int:
    args = parse_args()
    if args.workers < 1 or args.workers > 64:
        raise ValueError("workers must be between 1 and 64")
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    total = args.size or probe_size(args.url)
    parts_dir = output.with_suffix(output.suffix + ".parts")
    parts_dir.mkdir(parents=True, exist_ok=True)
    part_size = math.ceil(total / args.workers)
    ranges = []
    for index in range(args.workers):
        start = index * part_size
        if start >= total:
            break
        end = min(total - 1, start + part_size - 1)
        ranges.append((index, start, end))

    print(f"total={total} workers={len(ranges)} part_size={part_size}", flush=True)
    progress = Progress(total)
    completed: dict[int, Path] = {}
    with ThreadPoolExecutor(max_workers=len(ranges)) as executor:
        futures = {
            executor.submit(
                download_part,
                index,
                args.url,
                start,
                end,
                parts_dir,
                args.retries,
                progress,
            ): index
            for index, start, end in ranges
        }
        for future in as_completed(futures):
            index = futures[future]
            completed[index] = future.result()

    merged = output.with_suffix(output.suffix + ".merge")
    with merged.open("wb") as destination:
        for index in range(len(ranges)):
            with completed[index].open("rb") as source:
                shutil.copyfileobj(source, destination, length=1024 * 1024)
    if merged.stat().st_size != total:
        raise RuntimeError(f"Merged size mismatch: {merged.stat().st_size} != {total}")
    os.replace(merged, output)
    for path in completed.values():
        path.unlink()
    parts_dir.rmdir()
    print(f"download=OK output={output} size={output.stat().st_size}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
