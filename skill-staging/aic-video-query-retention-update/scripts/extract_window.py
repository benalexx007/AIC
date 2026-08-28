#!/usr/bin/env python3
"""Extract exact indexed frames around a candidate event and make contact sheets."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import cv2
import numpy as np


SHEET_WIDTH = 1280
SHEET_HEIGHT = 720
SHEET_COLS = 4
SHEET_ROWS = 3


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--center-seconds", type=float)
    group.add_argument("--center-frame", type=int)
    parser.add_argument("--radius-frames", type=int, default=18)
    parser.add_argument("--step", type=int, default=1)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def fit_image(image: np.ndarray, width: int, height: int) -> np.ndarray:
    scale = min(width / image.shape[1], height / image.shape[0])
    resized = cv2.resize(image, (max(1, int(image.shape[1] * scale)), max(1, int(image.shape[0] * scale))))
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    y = (height - resized.shape[0]) // 2
    x = (width - resized.shape[1]) // 2
    canvas[y : y + resized.shape[0], x : x + resized.shape[1]] = resized
    return canvas


def create_sheets(frames: list[dict], output: Path) -> list[str]:
    sheets = []
    per_sheet = SHEET_COLS * SHEET_ROWS
    cell_w = SHEET_WIDTH // SHEET_COLS
    cell_h = SHEET_HEIGHT // SHEET_ROWS
    label_h = 28
    for sheet_index in range(math.ceil(len(frames) / per_sheet)):
        canvas = np.zeros((SHEET_HEIGHT, SHEET_WIDTH, 3), dtype=np.uint8)
        chunk = frames[sheet_index * per_sheet : (sheet_index + 1) * per_sheet]
        for slot, item in enumerate(chunk):
            row, col = divmod(slot, SHEET_COLS)
            x, y = col * cell_w, row * cell_h
            image = cv2.imread(item["path"])
            if image is None:
                continue
            fitted = fit_image(image, cell_w, cell_h - label_h)
            canvas[y + label_h : y + cell_h, x : x + cell_w] = fitted
            label = f"f={item['frame_id']}  t={item['seconds']:.3f}s"
            cv2.putText(canvas, label, (x + 5, y + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 255, 255), 1, cv2.LINE_AA)
        sheet_path = output / f"sheet-{sheet_index + 1:03d}.jpg"
        cv2.imwrite(str(sheet_path), canvas, [cv2.IMWRITE_JPEG_QUALITY, 88])
        sheets.append(str(sheet_path.resolve()))
    return sheets


def main() -> int:
    args = parse_args()
    video_path = Path(args.video).resolve()
    output = Path(args.output).resolve()
    frames_dir = output / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        raise SystemExit(f"Cannot open video: {video_path}")
    fps = capture.get(cv2.CAP_PROP_FPS)
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    if not fps or fps <= 0:
        raise SystemExit("Video FPS is unavailable")
    center = args.center_frame if args.center_frame is not None else round(args.center_seconds * fps)
    start = max(0, center - args.radius_frames)
    end = min(frame_count - 1, center + args.radius_frames)
    targets = list(range(start, end + 1, max(1, args.step)))

    rows = []
    for frame_id in targets:
        capture.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ok, frame = capture.read()
        if not ok:
            continue
        frame_path = frames_dir / f"f{frame_id:09d}_t{frame_id / fps:012.3f}.jpg"
        cv2.imwrite(str(frame_path), frame, [cv2.IMWRITE_JPEG_QUALITY, 94])
        rows.append({"frame_id": frame_id, "seconds": round(frame_id / fps, 6), "path": str(frame_path.resolve())})
    capture.release()

    sheets = create_sheets(rows, output)
    payload = {
        "video": str(video_path),
        "fps": fps,
        "center_frame": center,
        "start_frame": start,
        "end_frame": end,
        "frames": rows,
        "contact_sheets": sheets,
        "estimated_sheet_tokens_original_detail": len(sheets) * (math.ceil(SHEET_WIDTH / 32) * math.ceil(SHEET_HEIGHT / 32)),
    }
    manifest = output / "window.json"
    manifest.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"manifest": str(manifest), "frames": len(rows), "sheets": len(sheets)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
