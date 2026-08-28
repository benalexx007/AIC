#!/usr/bin/env python3
"""Search a semantic-index embedding store with one or more text prompts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", required=True, help="semantic-index.json")
    parser.add_argument("--prompt", action="append", required=True, help="Repeat for multiple search phrases")
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--min-gap-seconds", type=float, default=2.0)
    parser.add_argument("--output", help="Optional JSON output path")
    parser.add_argument("--frames-dir", help="Directory for full-resolution search matches")
    parser.add_argument("--no-extract-frames", action="store_true")
    parser.add_argument("--clip-model")
    parser.add_argument("--clip-pretrained")
    parser.add_argument("--clip-cache", default=r"D:\AIC\models\semantic\openclip")
    parser.add_argument("--device", default="auto", choices=["auto", "xpu", "cuda", "cpu"])
    return parser.parse_args()


def choose_device(requested: str) -> str:
    import torch

    if requested != "auto":
        if requested == "xpu" and not (hasattr(torch, "xpu") and torch.xpu.is_available()):
            raise RuntimeError("xpu was requested but torch.xpu is unavailable")
        if requested == "cuda" and not torch.cuda.is_available():
            raise RuntimeError("cuda was requested but CUDA is unavailable")
        return requested
    if hasattr(torch, "xpu") and torch.xpu.is_available():
        return "xpu"
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


def temporal_top_k(similarities: np.ndarray, seconds: np.ndarray, top_k: int, min_gap: float) -> list[int]:
    selected: list[int] = []
    for index in np.argsort(-similarities):
        item = int(index)
        if all(abs(float(seconds[item]) - float(seconds[prior])) >= min_gap for prior in selected):
            selected.append(item)
            if len(selected) >= top_k:
                break
    return selected


def extract_match_frames(video: Path, frame_ids: list[int], output: Path) -> dict[int, str]:
    import cv2

    output.mkdir(parents=True, exist_ok=True)
    targets = sorted(set(frame_ids))
    target_set = set(targets)
    paths: dict[int, str] = {}
    capture = cv2.VideoCapture(str(video))
    if not capture.isOpened():
        raise RuntimeError(f"Cannot open video: {video}")
    frame_id = 0
    last_target = targets[-1]
    while frame_id <= last_target:
        if frame_id in target_set:
            ok, frame = capture.read()
            if not ok:
                break
            path = output / f"f{frame_id:09d}.jpg"
            if not cv2.imwrite(str(path), frame, [cv2.IMWRITE_JPEG_QUALITY, 95]):
                raise RuntimeError(f"Failed to write search frame: {path}")
            paths[frame_id] = str(path.resolve())
        else:
            if not capture.grab():
                break
        frame_id += 1
    capture.release()
    return paths


def main() -> int:
    args = parse_args()
    if args.top_k < 1 or args.min_gap_seconds < 0:
        raise ValueError("--top-k must be positive and --min-gap-seconds cannot be negative")
    index_path = Path(args.index).resolve()
    payload = json.loads(index_path.read_text(encoding="utf-8"))
    embeddings_path = Path(payload["artifacts"]["embeddings"])
    samples_path = Path(payload["artifacts"]["samples"])
    samples = json.loads(samples_path.read_text(encoding="utf-8"))
    arrays = np.load(embeddings_path)
    embeddings = arrays["embeddings"].astype(np.float32)
    embeddings /= np.linalg.norm(embeddings, axis=1, keepdims=True).clip(min=1e-12)
    frame_ids = arrays["frame_ids"]
    seconds = arrays["seconds"]
    if len(samples) != len(embeddings):
        raise RuntimeError("semantic index and embedding rows do not match")

    import open_clip
    import torch

    stored_model = payload["models"]["openclip"]
    model_name = args.clip_model or stored_model["model"]
    pretrained = args.clip_pretrained or stored_model["pretrained"]
    device = choose_device(args.device)
    model, _, _ = open_clip.create_model_and_transforms(
        model_name,
        pretrained=pretrained,
        cache_dir=str(Path(args.clip_cache).resolve()),
    )
    model = model.eval().to(device)
    tokenizer = open_clip.get_tokenizer(model_name)
    tokens = tokenizer(args.prompt).to(device)
    with torch.inference_mode():
        text_features = model.encode_text(tokens).float()
        text_features = text_features / text_features.norm(dim=-1, keepdim=True).clamp_min(1e-12)
    query_embeddings = text_features.cpu().numpy().astype(np.float32)
    similarity_matrix = query_embeddings @ embeddings.T

    selected_by_prompt = [
        temporal_top_k(similarities, seconds, min(args.top_k, len(embeddings)), args.min_gap_seconds)
        for similarities in similarity_matrix
    ]
    extracted_paths: dict[int, str] = {}
    if not args.no_extract_frames:
        frame_output = Path(args.frames_dir).resolve() if args.frames_dir else index_path.parent / "search-frames"
        selected_frame_ids = [int(frame_ids[index]) for indices in selected_by_prompt for index in indices]
        extracted_paths = extract_match_frames(Path(payload["video"]["path"]), selected_frame_ids, frame_output)

    searches = []
    for prompt, similarities, selected_indices in zip(args.prompt, similarity_matrix, selected_by_prompt):
        matches = []
        for rank, index in enumerate(selected_indices, start=1):
            sample = samples[index]
            frame_id = int(frame_ids[index])
            matches.append(
                {
                    "rank": rank,
                    "frame_id": frame_id,
                    "seconds": round(float(seconds[index]), 6),
                    "similarity": round(float(similarities[index]), 6),
                    "frame_path": sample.get("candidate_frame") or extracted_paths.get(frame_id),
                    "object_counts": sample.get("object_counts", {}),
                    "cluster_id": sample.get("cluster_id"),
                }
            )
        searches.append({"prompt": prompt, "matches": matches})

    result = {
        "semantic_index": str(index_path),
        "model": {"name": model_name, "pretrained": pretrained, "device": device},
        "searches": searches,
    }
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        output = Path(args.output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
