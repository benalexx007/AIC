#!/usr/bin/env python3
"""Propose alternate temporal clusters that may satisfy a provisional video query.

This is a retrieval gate, not an automatic semantic verdict. It combines full-video
text-to-frame CLIP search with near-duplicate image-embedding search, excludes the
verified target interval, groups remaining hits in time, and saves one review frame
per cluster when the source video is still available.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", required=True, help="semantic-index.json")
    parser.add_argument("--target-start-frame", required=True, type=int)
    parser.add_argument("--target-end-frame", required=True, type=int)
    parser.add_argument(
        "--prompt",
        action="append",
        required=True,
        help="Repeat for complete event/question-answer paraphrases, not isolated objects",
    )
    parser.add_argument("--top-k-per-prompt", type=int, default=40)
    parser.add_argument("--cluster-gap-seconds", type=float, default=10.0)
    parser.add_argument("--exclude-margin-seconds", type=float, default=5.0)
    parser.add_argument("--relative-text-threshold", type=float, default=0.88)
    parser.add_argument("--visual-duplicate-threshold", type=float, default=0.92)
    parser.add_argument("--max-review-clusters", type=int, default=4)
    parser.add_argument("--output", required=True)
    parser.add_argument("--frames-dir")
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


def existing_frame_path(index_dir: Path, sample: dict, frame_id: int) -> str | None:
    candidates = []
    if sample.get("candidate_frame"):
        candidates.append(Path(sample["candidate_frame"]))
    candidates.append(index_dir / "search-frames" / f"f{frame_id:09d}.jpg")
    candidates.extend((index_dir / "candidate-frames").glob(f"f{frame_id:09d}_*.jpg"))
    for path in candidates:
        if path.is_file():
            return str(path.resolve())
    return None


def extract_frames(video: Path, targets: dict[int, Path]) -> dict[int, str]:
    if not targets or not video.is_file():
        return {}
    import cv2

    capture = cv2.VideoCapture(str(video))
    if not capture.isOpened():
        return {}
    written: dict[int, str] = {}
    for frame_id, path in sorted(targets.items()):
        path.parent.mkdir(parents=True, exist_ok=True)
        capture.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
        ok, frame = capture.read()
        if ok and cv2.imwrite(str(path), frame, [cv2.IMWRITE_JPEG_QUALITY, 95]):
            written[frame_id] = str(path.resolve())
    capture.release()
    return written


def group_hits(hits: list[dict], gap_seconds: float) -> list[list[dict]]:
    if not hits:
        return []
    ordered = sorted(hits, key=lambda item: (item["seconds"], item["sample_index"]))
    groups: list[list[dict]] = [[ordered[0]]]
    for hit in ordered[1:]:
        if hit["seconds"] - groups[-1][-1]["seconds"] <= gap_seconds:
            groups[-1].append(hit)
        else:
            groups.append([hit])
    return groups


def main() -> int:
    args = parse_args()
    if args.target_start_frame < 0 or args.target_end_frame < args.target_start_frame:
        raise ValueError("target frame interval is invalid")
    if args.top_k_per_prompt < 1 or args.max_review_clusters < 1:
        raise ValueError("top-k and max-review-clusters must be positive")
    if args.cluster_gap_seconds < 0 or args.exclude_margin_seconds < 0:
        raise ValueError("time gaps cannot be negative")
    if not 0 < args.relative_text_threshold <= 1:
        raise ValueError("relative text threshold must be in (0, 1]")
    if not 0 < args.visual_duplicate_threshold <= 1:
        raise ValueError("visual duplicate threshold must be in (0, 1]")

    index_path = Path(args.index).resolve()
    payload = json.loads(index_path.read_text(encoding="utf-8"))
    arrays = np.load(Path(payload["artifacts"]["embeddings"]))
    embeddings = arrays["embeddings"].astype(np.float32)
    embeddings /= np.linalg.norm(embeddings, axis=1, keepdims=True).clip(min=1e-12)
    frame_ids = arrays["frame_ids"].astype(np.int64)
    seconds = arrays["seconds"].astype(np.float64)
    samples = json.loads(Path(payload["artifacts"]["samples"]).read_text(encoding="utf-8"))
    if len(samples) != len(embeddings):
        raise RuntimeError("semantic index and embedding rows do not match")

    fps = float(payload["video"]["fps"])
    target_start_seconds = args.target_start_frame / fps
    target_end_seconds = args.target_end_frame / fps
    target_mask = (frame_ids >= args.target_start_frame) & (frame_ids <= args.target_end_frame)
    if not np.any(target_mask):
        nearest = int(np.argmin(np.abs(seconds - ((target_start_seconds + target_end_seconds) / 2))))
        target_mask[nearest] = True
    outside_mask = (seconds < target_start_seconds - args.exclude_margin_seconds) | (
        seconds > target_end_seconds + args.exclude_margin_seconds
    )

    import open_clip
    import torch

    stored_model = payload["models"]["openclip"]
    model_name = args.clip_model or stored_model["model"]
    pretrained = args.clip_pretrained or stored_model["pretrained"]
    device = choose_device(args.device)
    model, _, _ = open_clip.create_model_and_transforms(
        model_name, pretrained=pretrained, cache_dir=str(Path(args.clip_cache).resolve())
    )
    model = model.eval().to(device)
    tokenizer = open_clip.get_tokenizer(model_name)
    tokens = tokenizer(args.prompt).to(device)
    with torch.inference_mode():
        text_features = model.encode_text(tokens).float()
        text_features /= text_features.norm(dim=-1, keepdim=True).clamp_min(1e-12)
    similarity_matrix = text_features.cpu().numpy().astype(np.float32) @ embeddings.T

    hits_by_index: dict[int, dict] = {}
    prompt_summaries = []
    outside_indices = np.flatnonzero(outside_mask)
    for prompt_index, (prompt, similarities) in enumerate(zip(args.prompt, similarity_matrix)):
        target_best = float(np.max(similarities[target_mask]))
        threshold = target_best * args.relative_text_threshold
        ranked_outside = outside_indices[np.argsort(-similarities[outside_indices])]
        accepted = [int(i) for i in ranked_outside[: args.top_k_per_prompt] if similarities[i] >= threshold]
        prompt_summaries.append(
            {
                "prompt": prompt,
                "target_best_similarity": round(target_best, 6),
                "relative_threshold": round(float(threshold), 6),
                "outside_hits": len(accepted),
            }
        )
        for sample_index in accepted:
            hit = hits_by_index.setdefault(
                sample_index,
                {
                    "sample_index": sample_index,
                    "frame_id": int(frame_ids[sample_index]),
                    "seconds": float(seconds[sample_index]),
                    "text_scores": {},
                    "visual_similarity": None,
                },
            )
            hit["text_scores"][str(prompt_index)] = round(float(similarities[sample_index]), 6)

    target_embeddings = embeddings[target_mask]
    visual_scores = np.max(embeddings @ target_embeddings.T, axis=1)
    visual_indices = np.flatnonzero(outside_mask & (visual_scores >= args.visual_duplicate_threshold))
    for sample_index in visual_indices:
        item = int(sample_index)
        hit = hits_by_index.setdefault(
            item,
            {
                "sample_index": item,
                "frame_id": int(frame_ids[item]),
                "seconds": float(seconds[item]),
                "text_scores": {},
                "visual_similarity": None,
            },
        )
        hit["visual_similarity"] = round(float(visual_scores[item]), 6)

    clusters = []
    for group in group_hits(list(hits_by_index.values()), args.cluster_gap_seconds):
        for hit in group:
            ratios = []
            for prompt_index, score in hit["text_scores"].items():
                baseline = prompt_summaries[int(prompt_index)]["target_best_similarity"]
                if baseline > 0:
                    ratios.append(score / baseline)
            hit["max_text_relative_to_target"] = round(max(ratios), 6) if ratios else None
        representative = max(
            group,
            key=lambda hit: max(hit.get("max_text_relative_to_target") or 0, hit.get("visual_similarity") or 0),
        )
        matched_prompt_ids = sorted({int(key) for hit in group for key in hit["text_scores"]})
        clusters.append(
            {
                "sampled_start_seconds": round(group[0]["seconds"], 6),
                "sampled_end_seconds": round(group[-1]["seconds"], 6),
                "hit_count": len(group),
                "matched_prompts": [args.prompt[i] for i in matched_prompt_ids],
                "max_text_relative_to_target": max(
                    (hit.get("max_text_relative_to_target") or 0 for hit in group), default=0
                ),
                "max_visual_similarity": max((hit.get("visual_similarity") or 0 for hit in group), default=0),
                "representative": representative,
            }
        )
    clusters.sort(
        key=lambda cluster: max(cluster["max_text_relative_to_target"], cluster["max_visual_similarity"]),
        reverse=True,
    )
    candidate_cluster_count = len(clusters)
    clusters = clusters[: args.max_review_clusters]

    output_path = Path(args.output).resolve()
    frames_dir = Path(args.frames_dir).resolve() if args.frames_dir else output_path.parent / "uniqueness-frames"
    extraction_targets: dict[int, Path] = {}
    for cluster in clusters:
        rep = cluster["representative"]
        frame_id = int(rep["frame_id"])
        path = existing_frame_path(index_path.parent, samples[rep["sample_index"]], frame_id)
        if path:
            rep["frame_path"] = path
        elif not args.no_extract_frames:
            extraction_targets[frame_id] = frames_dir / f"f{frame_id:09d}.jpg"
    extracted = extract_frames(Path(payload["video"]["path"]), extraction_targets)
    for cluster in clusters:
        rep = cluster["representative"]
        rep["frame_path"] = rep.get("frame_path") or extracted.get(int(rep["frame_id"]))
        rep.pop("sample_index", None)

    result = {
        "semantic_index": str(index_path),
        "target": {
            "start_frame": args.target_start_frame,
            "end_frame": args.target_end_frame,
            "start_seconds": round(target_start_seconds, 6),
            "end_seconds": round(target_end_seconds, 6),
            "excluded_margin_seconds": args.exclude_margin_seconds,
        },
        "model": {"name": model_name, "pretrained": pretrained, "device": device},
        "prompts": prompt_summaries,
        "retrieval_decision": (
            "review_required" if clusters else "no_alternate_cluster_detected"
        ),
        "candidate_cluster_count": candidate_cluster_count,
        "review_clusters_truncated": candidate_cluster_count > args.max_review_clusters,
        "important": "Clusters are retrieval proposals. Inspect each representative and verify the complete query predicates before accepting or rejecting the query.",
        "alternate_clusters": clusters,
    }
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
