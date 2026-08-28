#!/usr/bin/env python3
"""Estimate GPT-5.6 evidence tokens for local text and image files."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import cv2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", nargs="*", default=[])
    parser.add_argument("--texts", nargs="*", default=[])
    parser.add_argument("--chars-per-token", type=float, default=2.0)
    parser.add_argument("--overhead", type=int, default=2500)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    image_rows = []
    for item in args.images:
        path = Path(item)
        image = cv2.imread(str(path))
        if image is None:
            image_rows.append({"path": str(path), "error": "unreadable"})
            continue
        height, width = image.shape[:2]
        patches = math.ceil(width / 32) * math.ceil(height / 32)
        image_rows.append(
            {"path": str(path.resolve()), "width": width, "height": height, "original_detail_tokens": patches}
        )

    text_rows = []
    for item in args.texts:
        path = Path(item)
        content = path.read_text(encoding="utf-8")
        estimate = math.ceil(len(content) / args.chars_per_token)
        text_rows.append({"path": str(path.resolve()), "characters": len(content), "estimated_tokens": estimate})

    image_tokens = sum(row.get("original_detail_tokens", 0) for row in image_rows)
    text_tokens = sum(row.get("estimated_tokens", 0) for row in text_rows)
    payload = {
        "method": "images=ceil(width/32)*ceil(height/32); text=characters/chars_per_token",
        "images": image_rows,
        "texts": text_rows,
        "image_tokens": image_tokens,
        "text_tokens": text_tokens,
        "overhead_tokens": args.overhead,
        "estimated_total_input_tokens": image_tokens + text_tokens + args.overhead,
        "excludes": ["internal reasoning tokens", "tool metadata", "conversation history"],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
