#!/usr/bin/env python3
"""Transcribe one audio file with Faster-Whisper in an isolated process."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-text", required=True)
    parser.add_argument("--model", default="small")
    parser.add_argument("--model-root", default=r"D:\AIC\models\whisper")
    parser.add_argument("--language", default=None)
    parser.add_argument("--compute-type", default="int8")
    return parser.parse_args()


def timestamp(seconds: float) -> str:
    seconds = max(0.0, seconds)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"


def main() -> int:
    args = parse_args()
    from faster_whisper import WhisperModel

    model = WhisperModel(
        args.model,
        device="cpu",
        compute_type=args.compute_type,
        download_root=args.model_root,
    )
    segments_iter, info = model.transcribe(
        args.audio,
        language=args.language,
        beam_size=5,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 500},
        word_timestamps=False,
    )

    segments = []
    text_lines = []
    for segment in segments_iter:
        text = segment.text.strip()
        item = {
            "id": segment.id,
            "start": round(segment.start, 3),
            "end": round(segment.end, 3),
            "text": text,
            "avg_logprob": round(segment.avg_logprob, 4),
            "no_speech_prob": round(segment.no_speech_prob, 4),
        }
        segments.append(item)
        if text:
            text_lines.append(
                f"[{timestamp(segment.start)} --> {timestamp(segment.end)}] {text}"
            )

    payload = {
        "model": args.model,
        "device": "cpu",
        "compute_type": args.compute_type,
        "language": info.language,
        "language_probability": round(info.language_probability, 4),
        "duration": round(info.duration, 3),
        "duration_after_vad": round(info.duration_after_vad, 3),
        "segments": segments,
    }
    output_json = Path(args.output_json)
    output_text = Path(args.output_text)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_text.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    output_text.write_text("\n".join(text_lines) + ("\n" if text_lines else ""), encoding="utf-8")
    estimated_tokens = math.ceil(sum(len(line) for line in text_lines) / 2.0)
    print(json.dumps({"segments": len(segments), "estimated_text_tokens": estimated_tokens}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
