#!/usr/bin/env python3
"""Export one AIC query, interval answer, and persistent YAML record."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml


FILE_PATTERN = re.compile(r"^(?:query|ans|result)-(\d+)-(?:kis|qa|trake)\.(?:txt|yaml)$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query-type", required=True, choices=["kis", "qa", "trake"])
    parser.add_argument("--query", required=True, help="Exactly one query, without a label")
    parser.add_argument("--video-id", required=True)
    parser.add_argument("--interval", nargs=2, type=int, metavar=("START", "END"))
    parser.add_argument(
        "--event-interval",
        nargs=2,
        type=int,
        action="append",
        default=[],
        metavar=("START", "END"),
    )
    parser.add_argument("--answer")
    parser.add_argument("--fps", type=float, required=True)
    parser.add_argument("--evidence", default="")
    parser.add_argument("--confidence", choices=["high", "medium", "low"], default="high")
    parser.add_argument("--root", default=r"D:\AIC\test")
    parser.add_argument("--index", type=int)
    return parser.parse_args()


def validate_interval(interval: list[int] | tuple[int, int], label: str) -> list[int]:
    start, end = interval
    if start < 0 or end < 0:
        raise ValueError(f"{label} cannot contain negative frame IDs")
    if start > end:
        raise ValueError(f"{label} start must be <= end")
    return [start, end]


def next_index(root: Path) -> int:
    found = []
    for directory in (root / "query", root / "answer", root / "yaml"):
        if not directory.exists():
            continue
        for path in directory.iterdir():
            match = FILE_PATTERN.match(path.name)
            if match:
                found.append(int(match.group(1)))
    return max(found, default=0) + 1


def write_new(path: Path, content: str) -> None:
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite existing result: {path}")
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8-sig")
    temporary.replace(path)


def main() -> int:
    args = parse_args()
    query = args.query.strip()
    if not query:
        raise ValueError("Query cannot be empty")
    if "\n\n" in query:
        raise ValueError("Query must be one query, not multiple paragraphs")
    if args.fps <= 0:
        raise ValueError("FPS must be positive")

    if args.query_type in {"kis", "qa"}:
        if args.interval is None:
            raise ValueError("KIS/Q&A requires --interval START END")
        if args.event_interval:
            raise ValueError("KIS/Q&A does not accept --event-interval")
        interval = validate_interval(args.interval, "interval")
        event_intervals: list[list[int]] = []
    else:
        if args.interval is not None:
            raise ValueError("TRAKE requires --event-interval, not --interval")
        if not args.event_interval:
            raise ValueError("TRAKE requires at least one --event-interval START END")
        interval = []
        event_intervals = [
            validate_interval(item, f"event interval {index + 1}")
            for index, item in enumerate(args.event_interval)
        ]

    if args.query_type == "qa" and not (args.answer or "").strip():
        raise ValueError("Q&A requires --answer")
    if args.query_type != "qa" and args.answer is not None:
        raise ValueError("--answer is only valid for Q&A")

    root = Path(args.root).resolve()
    query_dir = root / "query"
    answer_dir = root / "answer"
    yaml_dir = root / "yaml"
    for directory in (query_dir, answer_dir, yaml_dir):
        directory.mkdir(parents=True, exist_ok=True)

    sequence = args.index if args.index is not None else next_index(root)
    if sequence <= 0:
        raise ValueError("Sequence number must be positive")
    suffix = f"{sequence}-{args.query_type}"
    query_path = query_dir / f"query-{suffix}.txt"
    answer_path = answer_dir / f"ans-{suffix}.txt"
    yaml_path = yaml_dir / f"result-{suffix}.yaml"
    if any(path.exists() for path in (query_path, answer_path, yaml_path)):
        raise FileExistsError(f"Sequence {sequence} already exists for {args.query_type}")

    if args.query_type == "kis":
        submission = f"{args.video_id}, [{interval[0]}, {interval[1]}]"
        ground_truth = {"frame_interval": interval}
    elif args.query_type == "qa":
        clean_answer = args.answer.strip()
        submission = f"{args.video_id}, [{interval[0]}, {interval[1]}], {clean_answer}"
        ground_truth = {"frame_interval": interval, "answer": clean_answer}
    else:
        rendered = ", ".join(f"[{start}, {end}]" for start, end in event_intervals)
        submission = f"{args.video_id}, {rendered}"
        ground_truth = {"event_intervals": event_intervals}

    payload = {
        "sequence": sequence,
        "query_type": args.query_type,
        "query_vi": query,
        "video_id": args.video_id,
        "fps": args.fps,
        "ground_truth": ground_truth,
        "answer_submission": submission,
        "evidence": args.evidence.strip(),
        "confidence": args.confidence,
        "files": {
            "query": str(query_path),
            "answer": str(answer_path),
            "yaml": str(yaml_path),
        },
    }
    yaml_content = yaml.safe_dump(payload, allow_unicode=True, sort_keys=False, width=4096)
    write_new(query_path, query + "\n")
    write_new(answer_path, submission + "\n")
    write_new(yaml_path, yaml_content)

    print(
        json.dumps(
            {
                "sequence": sequence,
                "query": str(query_path),
                "answer": str(answer_path),
                "yaml": str(yaml_path),
                "yaml_content": yaml_content,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
