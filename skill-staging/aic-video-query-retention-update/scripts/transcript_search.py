#!/usr/bin/env python3
"""Select token-bounded Whisper transcript segments by time and keywords."""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--transcript", help="Faster-Whisper transcript.json")
    source.add_argument("--manifest", help="prepare_video.py manifest containing transcript_json")
    parser.add_argument("--around-seconds", action="append", type=float, default=[])
    parser.add_argument("--query", action="append", default=[], help="Repeat for multiple local keyword searches")
    parser.add_argument("--radius-seconds", type=float, default=20.0)
    parser.add_argument("--max-radius-seconds", type=float, default=60.0)
    parser.add_argument("--no-adaptive", action="store_true", help="Disable sparse-window expansion")
    parser.add_argument("--min-chars-per-center", type=int, default=200)
    parser.add_argument("--min-segments-per-center", type=int, default=2)
    parser.add_argument("--profile", choices=["high", "xhigh"], default="high")
    parser.add_argument("--max-segments", type=int)
    parser.add_argument("--max-chars", type=int)
    parser.add_argument("--query-matches", type=int, default=3)
    parser.add_argument("--context-segments", type=int, default=1)
    parser.add_argument("--output", help="Optional compact JSON output path")
    return parser.parse_args()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    os.replace(temporary, path)


def resolve_transcript(args: argparse.Namespace) -> Path:
    if args.transcript:
        path = Path(args.transcript).resolve()
    else:
        manifest = read_json(Path(args.manifest).resolve())
        value = (manifest.get("artifacts") or {}).get("transcript_json")
        if not value:
            raise ValueError("Manifest does not contain artifacts.transcript_json")
        path = Path(value).resolve()
    if not path.is_file():
        raise FileNotFoundError(path)
    return path


def terms(value: str) -> list[str]:
    return [item for item in re.findall(r"\w+", value.casefold(), flags=re.UNICODE) if item]


def main() -> int:
    args = parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if not args.around_seconds and not args.query:
        raise ValueError("Supply at least one --around-seconds or --query selector")
    if (
        args.radius_seconds < 0
        or args.max_radius_seconds < args.radius_seconds
        or args.query_matches < 1
        or args.context_segments < 0
        or args.min_chars_per_center < 0
        or args.min_segments_per_center < 0
    ):
        raise ValueError("Radius/context must be non-negative and --query-matches must be positive")

    defaults = {
        "high": {"max_segments": 18, "max_chars": 4500},
        "xhigh": {"max_segments": 30, "max_chars": 8000},
    }[args.profile]
    max_segments = args.max_segments if args.max_segments is not None else defaults["max_segments"]
    max_chars = args.max_chars if args.max_chars is not None else defaults["max_chars"]
    if max_segments < 1 or max_chars < 1:
        raise ValueError("--max-segments and --max-chars must be positive")

    transcript_path = resolve_transcript(args)
    transcript = read_json(transcript_path)
    segments = transcript.get("segments") or []
    priorities: dict[int, float] = {}
    reasons: dict[int, set[str]] = {}
    adaptive_reasons: list[str] = []
    expanded_centers: list[float] = []
    unmatched_queries: list[str] = []

    def include(index: int, priority: float, reason: str) -> None:
        if not 0 <= index < len(segments):
            return
        priorities[index] = max(priorities.get(index, float("-inf")), priority)
        reasons.setdefault(index, set()).add(reason)

    for center in args.around_seconds:
        window_start = center - args.radius_seconds
        window_end = center + args.radius_seconds
        base_matches = []
        for index, segment in enumerate(segments):
            start = float(segment.get("start", 0.0))
            end = float(segment.get("end", start))
            if end >= window_start and start <= window_end:
                base_matches.append(index)
                midpoint = (start + end) / 2.0
                include(index, 1000.0 - abs(midpoint - center), f"time:{center:.3f}")
        base_chars = sum(len(str(segments[index].get("text", "")).strip()) for index in base_matches)
        sparse = len(base_matches) < args.min_segments_per_center or base_chars < args.min_chars_per_center
        if sparse and not args.no_adaptive and args.max_radius_seconds > args.radius_seconds:
            expanded_centers.append(center)
            adaptive_reasons.append(f"sparse_transcript_near:{center:.3f}")
            expanded_start = center - args.max_radius_seconds
            expanded_end = center + args.max_radius_seconds
            for index, segment in enumerate(segments):
                start = float(segment.get("start", 0.0))
                end = float(segment.get("end", start))
                if end >= expanded_start and start <= expanded_end:
                    midpoint = (start + end) / 2.0
                    include(index, 800.0 - abs(midpoint - center), f"adaptive-time:{center:.3f}")

    normalized_segment_terms = [terms(str(segment.get("text", ""))) for segment in segments]
    for query in args.query:
        query_terms = terms(query)
        if not query_terms:
            continue
        scored = []
        for index, segment_terms in enumerate(normalized_segment_terms):
            term_set = set(segment_terms)
            hits = sum(1 for item in query_terms if item in term_set)
            if hits:
                phrase_bonus = 1 if " ".join(query_terms) in " ".join(segment_terms) else 0
                scored.append((hits, phrase_bonus, index))
        if not scored:
            unmatched_queries.append(query)
        for hits, phrase_bonus, index in sorted(scored, key=lambda item: (-item[0], -item[1], item[2]))[: args.query_matches]:
            include(index, 2000.0 + hits * 100.0 + phrase_bonus * 25.0, f"query:{query}")
            for offset in range(1, args.context_segments + 1):
                include(index - offset, 500.0 - offset, f"context:{query}")
                include(index + offset, 500.0 - offset, f"context:{query}")

    selected_priority_order = sorted(priorities, key=lambda index: (-priorities[index], index))
    kept: list[int] = []
    used_chars = 0
    for index in selected_priority_order:
        if len(kept) >= max_segments:
            break
        text = str(segments[index].get("text", "")).strip()
        if not text:
            continue
        if kept and used_chars + len(text) > max_chars:
            continue
        if not kept and len(text) > max_chars:
            text = text[: max(1, max_chars - 1)].rstrip() + "…"
            segments[index] = {**segments[index], "text": text}
        kept.append(index)
        used_chars += len(text)
    kept.sort(key=lambda index: (float(segments[index].get("start", 0.0)), index))

    rows = [
        {
            "start": round(float(segments[index].get("start", 0.0)), 3),
            "end": round(float(segments[index].get("end", segments[index].get("start", 0.0))), 3),
            "text": str(segments[index].get("text", "")).strip(),
            "matched_by": sorted(reasons[index]),
        }
        for index in kept
    ]
    result = {
        "source": str(transcript_path),
        "profile": args.profile,
        "selectors": {
            "around_seconds": args.around_seconds,
            "radius_seconds": args.radius_seconds,
            "effective_radius_seconds": args.max_radius_seconds if expanded_centers else args.radius_seconds,
            "queries": args.query,
        },
        "limits": {"max_segments": max_segments, "max_transcript_chars": max_chars},
        "selected_segments": len(rows),
        "selected_transcript_chars": sum(len(row["text"]) for row in rows),
        "adaptive_expansion": {
            "enabled": not args.no_adaptive,
            "expanded": bool(expanded_centers),
            "expanded_centers": expanded_centers,
            "reasons": adaptive_reasons,
            "unmatched_queries": unmatched_queries,
            "further_fallback_recommended": not rows or bool(unmatched_queries),
        },
        "segments": rows,
    }
    initial = json.dumps(result, ensure_ascii=False, indent=2)
    result["estimated_output_tokens_conservative"] = math.ceil((len(initial) + 80) / 2.0)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        atomic_write(Path(args.output).resolve(), rendered)
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
