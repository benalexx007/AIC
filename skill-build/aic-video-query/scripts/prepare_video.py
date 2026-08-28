#!/usr/bin/env python3
"""Prepare token-bounded evidence from a local or public Drive video."""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np


SHEET_WIDTH = 1280
SHEET_HEIGHT = 720
SHEET_COLS = 4
SHEET_ROWS = 3
FRAMES_PER_SHEET = SHEET_COLS * SHEET_ROWS
DEFAULT_FFMPEG_BIN = Path(r"D:\AIC\tools\ffmpeg\ffmpeg-master-latest-win64-gpl\bin")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Local video or public Google Drive URL")
    parser.add_argument("--query-type", required=True, choices=["kis", "qa", "trake"])
    parser.add_argument("--profile", default="high", choices=["high", "xhigh"])
    parser.add_argument("--output")
    parser.add_argument("--runs-root", default=r"D:\AIC\video-runs")
    parser.add_argument("--whisper-model", default="small")
    parser.add_argument("--whisper-root", default=r"D:\AIC\models\whisper")
    parser.add_argument("--language", default=None)
    parser.add_argument("--scene-threshold", type=float, default=27.0)
    parser.add_argument("--skip-scenes", action="store_true")
    parser.add_argument("--skip-transcript", action="store_true")
    return parser.parse_args()


def run(command: list[str]) -> None:
    print("RUN", subprocess.list2cmdline(command), flush=True)
    subprocess.run(command, check=True)


def find_binary(name: str) -> str:
    env_bin = os.environ.get("FFMPEG_BIN")
    candidates = []
    if env_bin:
        env_path = Path(env_bin)
        candidates.append(env_path / f"{name}.exe" if env_path.is_dir() else env_path)
    discovered = shutil.which(name)
    if discovered:
        candidates.append(Path(discovered))
    candidates.append(DEFAULT_FFMPEG_BIN / f"{name}.exe")
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate.resolve())
    raise FileNotFoundError(f"{name} was not found; set FFMPEG_BIN")


def rate(value: str | None) -> float:
    if not value or value in {"0/0", "N/A"}:
        return 0.0
    if "/" in value:
        numerator, denominator = value.split("/", 1)
        return float(numerator) / float(denominator) if float(denominator) else 0.0
    return float(value)


def safe_slug(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", value).strip("-").lower()
    return slug[:60] or "video"


def resolve_input(value: str, run_dir: Path) -> tuple[Path, dict]:
    local = Path(value)
    if local.is_file():
        resolved = local.resolve()
        return resolved, {
            "origin": "local",
            "downloaded_source": False,
            "original_filename": resolved.name,
        }
    if value.lower().startswith(("http://", "https://")):
        from download_drive import download_drive

        downloaded, drive_metadata = download_drive(value, run_dir)
        return downloaded.resolve(), {
            "origin": "google_drive",
            "downloaded_source": True,
            "original_filename": drive_metadata["filename"],
            "source_url": value,
            "size_bytes": drive_metadata["size_bytes"],
            "content_type": drive_metadata["content_type"],
            "reused_existing": drive_metadata["reused_existing"],
        }
    raise FileNotFoundError(f"Input is neither a file nor an HTTP URL: {value}")


def probe_video(video_path: Path, ffprobe: str) -> dict:
    command = [
        ffprobe,
        "-v",
        "error",
        "-show_streams",
        "-show_format",
        "-of",
        "json",
        str(video_path),
    ]
    payload = json.loads(subprocess.check_output(command, text=True, encoding="utf-8"))
    video_stream = next(stream for stream in payload["streams"] if stream.get("codec_type") == "video")
    fps = rate(video_stream.get("avg_frame_rate")) or rate(video_stream.get("r_frame_rate"))
    duration = float(video_stream.get("duration") or payload.get("format", {}).get("duration") or 0.0)
    frame_count = int(video_stream.get("nb_frames") or 0)
    if not frame_count and duration and fps:
        frame_count = round(duration * fps)
    return {
        "fps": fps,
        "duration_seconds": duration,
        "frame_count": frame_count,
        "width": int(video_stream.get("width") or 0),
        "height": int(video_stream.get("height") or 0),
        "video_codec": video_stream.get("codec_name"),
        "has_audio": any(stream.get("codec_type") == "audio" for stream in payload["streams"]),
    }


def evenly_limit(items: list, limit: int) -> list:
    if len(items) <= limit:
        return items
    if limit <= 1:
        return [items[0]]
    indices = [round(index * (len(items) - 1) / (limit - 1)) for index in range(limit)]
    return [items[index] for index in indices]


def detect_scenes(video_path: Path, threshold: float, profile: str) -> list[dict]:
    from scenedetect import SceneManager, open_video
    from scenedetect.detectors import ContentDetector

    video = open_video(str(video_path))
    manager = SceneManager()
    manager.add_detector(ContentDetector(threshold=threshold))
    manager.detect_scenes(video=video, show_progress=True, frame_skip=1 if profile == "high" else 0)
    scenes = manager.get_scene_list(start_in_scene=True)
    return [
        {
            "start_frame": start.frame_num,
            "end_frame": max(start.frame_num, end.frame_num - 1),
            "start_seconds": round(start.seconds, 6),
            "end_seconds": round(end.seconds, 6),
            "mid_frame": (start.frame_num + max(start.frame_num, end.frame_num - 1)) // 2,
        }
        for start, end in scenes
    ]


def fit_image(image: np.ndarray, width: int, height: int) -> np.ndarray:
    scale = min(width / image.shape[1], height / image.shape[0])
    resized = cv2.resize(image, (max(1, int(image.shape[1] * scale)), max(1, int(image.shape[0] * scale))))
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    y = (height - resized.shape[0]) // 2
    x = (width - resized.shape[1]) // 2
    canvas[y : y + resized.shape[0], x : x + resized.shape[1]] = resized
    return canvas


def extract_frames(video_path: Path, targets: list[dict], frames_dir: Path, fps: float) -> list[dict]:
    frames_dir.mkdir(parents=True, exist_ok=True)
    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        raise RuntimeError(f"Cannot open video with OpenCV: {video_path}")
    rows = []
    for target in sorted(targets, key=lambda item: item["frame_id"]):
        frame_id = target["frame_id"]
        capture.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ok, frame = capture.read()
        if not ok:
            continue
        seconds = frame_id / fps
        path = frames_dir / f"f{frame_id:09d}_t{seconds:012.3f}.jpg"
        cv2.imwrite(str(path), frame, [cv2.IMWRITE_JPEG_QUALITY, 92])
        rows.append(
            {
                "frame_id": frame_id,
                "seconds": round(seconds, 6),
                "sources": target["sources"],
                "path": str(path.resolve()),
            }
        )
    capture.release()
    return rows


def create_sheets(frames: list[dict], sheets_dir: Path) -> list[str]:
    sheets_dir.mkdir(parents=True, exist_ok=True)
    cell_w = SHEET_WIDTH // SHEET_COLS
    cell_h = SHEET_HEIGHT // SHEET_ROWS
    label_h = 28
    sheets = []
    for sheet_index in range(math.ceil(len(frames) / FRAMES_PER_SHEET)):
        canvas = np.zeros((SHEET_HEIGHT, SHEET_WIDTH, 3), dtype=np.uint8)
        chunk = frames[sheet_index * FRAMES_PER_SHEET : (sheet_index + 1) * FRAMES_PER_SHEET]
        for slot, item in enumerate(chunk):
            row, col = divmod(slot, SHEET_COLS)
            x, y = col * cell_w, row * cell_h
            image = cv2.imread(item["path"])
            if image is None:
                continue
            canvas[y + label_h : y + cell_h, x : x + cell_w] = fit_image(image, cell_w, cell_h - label_h)
            label = f"f={item['frame_id']} t={item['seconds']:.2f}s"
            cv2.putText(canvas, label, (x + 5, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 255, 255), 1, cv2.LINE_AA)
        path = sheets_dir / f"overview-{sheet_index + 1:03d}.jpg"
        cv2.imwrite(str(path), canvas, [cv2.IMWRITE_JPEG_QUALITY, 88])
        sheets.append(str(path.resolve()))
    return sheets


def main() -> int:
    args = parse_args()
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    input_stem = Path(args.input).stem if not args.input.lower().startswith(("http://", "https://")) else "drive-video"
    run_dir = Path(args.output).resolve() if args.output else (Path(args.runs_root) / f"{safe_slug(input_stem)}-{args.query_type}-{args.profile}-{timestamp}").resolve()
    run_dir.mkdir(parents=True, exist_ok=True)

    ffmpeg = find_binary("ffmpeg")
    ffprobe = find_binary("ffprobe")
    video_path, input_info = resolve_input(args.input, run_dir)
    metadata = probe_video(video_path, ffprobe)
    if metadata["fps"] <= 0 or metadata["frame_count"] <= 0:
        raise RuntimeError("Video FPS/frame count could not be determined")

    transcript_text = run_dir / "transcript.txt"
    transcript_json = run_dir / "transcript.json"
    if metadata["has_audio"] and not args.skip_transcript:
        audio_path = run_dir / "audio-16k-mono.wav"
        run([ffmpeg, "-y", "-v", "error", "-i", str(video_path), "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(audio_path)])
        transcriber = Path(__file__).with_name("transcribe_audio.py")
        command = [
            sys.executable,
            str(transcriber),
            "--audio",
            str(audio_path),
            "--output-json",
            str(transcript_json),
            "--output-text",
            str(transcript_text),
            "--model",
            args.whisper_model,
            "--model-root",
            args.whisper_root,
        ]
        if args.language:
            command.extend(["--language", args.language])
        run(command)
    else:
        transcript_text.write_text("", encoding="utf-8")
        transcript_json.write_text(json.dumps({"segments": []}, indent=2), encoding="utf-8")

    scenes = [] if args.skip_scenes else detect_scenes(video_path, args.scene_threshold, args.profile)
    scenes_path = run_dir / "scenes.json"
    scenes_path.write_text(json.dumps(scenes, ensure_ascii=False, indent=2), encoding="utf-8")

    interval = 30.0 if args.profile == "high" else 20.0
    coarse_limit = 41 if args.profile == "high" else 61
    scene_limit = 48 if args.profile == "high" else 84
    duration = metadata["duration_seconds"] or metadata["frame_count"] / metadata["fps"]
    coarse_seconds = []
    current = 0.0
    while current < duration:
        coarse_seconds.append(current)
        current += interval
    coarse_seconds.append(max(0.0, duration - 1.0 / metadata["fps"]))
    coarse_seconds = evenly_limit(coarse_seconds, coarse_limit)
    selected_scenes = evenly_limit(scenes, scene_limit)

    merged: dict[int, set[str]] = {}
    for seconds in coarse_seconds:
        frame_id = min(metadata["frame_count"] - 1, max(0, round(seconds * metadata["fps"])))
        merged.setdefault(frame_id, set()).add("coarse")
    for scene in selected_scenes:
        frame_id = min(metadata["frame_count"] - 1, max(0, scene["mid_frame"]))
        merged.setdefault(frame_id, set()).add("scene")
    targets = [{"frame_id": frame_id, "sources": sorted(sources)} for frame_id, sources in merged.items()]

    frames = extract_frames(video_path, targets, run_dir / "overview-frames", metadata["fps"])
    frame_index_path = run_dir / "frames-index.json"
    frame_index_path.write_text(json.dumps(frames, ensure_ascii=False, indent=2), encoding="utf-8")
    sheets = create_sheets(frames, run_dir / "contact-sheets")

    transcript_chars = len(transcript_text.read_text(encoding="utf-8"))
    sheet_tokens = math.ceil(SHEET_WIDTH / 32) * math.ceil(SHEET_HEIGHT / 32)
    manifest = {
        "query_type": args.query_type,
        "profile": args.profile,
        "video_id": video_path.stem,
        "video_path": str(video_path),
        "input": input_info,
        "metadata": metadata,
        "artifacts": {
            "transcript_text": str(transcript_text.resolve()),
            "transcript_json": str(transcript_json.resolve()),
            "scenes": str(scenes_path.resolve()),
            "frames_index": str(frame_index_path.resolve()),
            "contact_sheets": sheets,
        },
        "sampling": {
            "coarse_interval_seconds": interval,
            "coarse_samples": len(coarse_seconds),
            "detected_scenes": len(scenes),
            "selected_scene_representatives": len(selected_scenes),
            "extracted_overview_frames": len(frames),
            "contact_sheets": len(sheets),
        },
        "token_estimate": {
            "contact_sheet_tokens_original_detail": len(sheets) * sheet_tokens,
            "transcript_tokens_conservative": math.ceil(transcript_chars / 2.0),
            "method": "image=ceil(width/32)*ceil(height/32); Vietnamese text=characters/2",
            "excludes": ["dense verification", "OCR", "internal reasoning", "conversation/tool overhead"],
        },
        "next_step": (
            "Run semantic_index.py with the dedicated semantic Python environment. Then read transcript and semantic-index.json, "
            "inspect a bounded set of full-resolution candidates, and run extract_window.py for exact endpoints. "
            "Use contact sheets only to check coverage gaps and OCR only on shortlisted frames."
        ),
    }
    manifest_path = run_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"run_dir": str(run_dir), "manifest": str(manifest_path), "sheets": len(sheets)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
