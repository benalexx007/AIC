#!/usr/bin/env python3
"""Build a local CLIP + YOLO semantic index for a video.

Run this script with the dedicated semantic environment. It stores embeddings and
detector metadata locally so the language model only needs to inspect a small set
of full-resolution candidate frames.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from PIL import Image


DEFAULT_CLIP_CACHE = Path(r"D:\AIC\models\semantic\openclip")
DEFAULT_YOLO_MODEL = Path(r"D:\AIC\models\semantic\yolo26n.pt")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", help="Video path; optional when --manifest is supplied")
    parser.add_argument("--manifest", help="prepare_video.py manifest to read and update")
    parser.add_argument("--scenes", help="Optional scenes.json path")
    parser.add_argument("--output", help="Output directory; defaults to <run>/semantic")
    parser.add_argument("--profile", choices=["high", "xhigh"])
    parser.add_argument("--sample-fps", type=float)
    parser.add_argument("--candidate-limit", type=int)
    parser.add_argument("--summary-limit", type=int)
    parser.add_argument("--cluster-count", type=int)
    parser.add_argument("--max-samples", type=int)
    parser.add_argument("--min-gap-seconds", type=float, default=2.0)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--clip-model", default="ViT-B-32")
    parser.add_argument("--clip-pretrained", default="laion2b_s34b_b79k")
    parser.add_argument("--clip-cache", default=str(DEFAULT_CLIP_CACHE))
    parser.add_argument("--clip-device", default="auto", choices=["auto", "xpu", "cuda", "cpu"])
    parser.add_argument("--yolo-model", default=str(DEFAULT_YOLO_MODEL))
    parser.add_argument("--yolo-device", default="cpu")
    parser.add_argument("--yolo-imgsz", type=int, default=512)
    parser.add_argument("--yolo-conf", type=float, default=0.25)
    return parser.parse_args()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(temporary, path)


def package_version(name: str) -> str:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return "unknown"


def choose_clip_device(requested: str) -> str:
    import torch

    if requested != "auto":
        if requested == "xpu" and not (hasattr(torch, "xpu") and torch.xpu.is_available()):
            raise RuntimeError("CLIP device xpu was requested but torch.xpu is unavailable")
        if requested == "cuda" and not torch.cuda.is_available():
            raise RuntimeError("CLIP device cuda was requested but CUDA is unavailable")
        return requested
    if hasattr(torch, "xpu") and torch.xpu.is_available():
        return "xpu"
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


def video_metadata(path: Path) -> dict[str, Any]:
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise RuntimeError(f"Cannot open video: {path}")
    fps = float(capture.get(cv2.CAP_PROP_FPS))
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    capture.release()
    if fps <= 0 or frame_count <= 0:
        raise RuntimeError("Video FPS/frame count could not be determined")
    return {
        "fps": fps,
        "frame_count": frame_count,
        "duration_seconds": frame_count / fps,
        "width": width,
        "height": height,
    }


def evenly_limit(values: list[int], limit: int) -> list[int]:
    if len(values) <= limit:
        return values
    indices = np.linspace(0, len(values) - 1, num=limit, dtype=np.int64)
    return [values[int(index)] for index in indices]


def build_targets(
    metadata: dict[str, Any],
    scenes: list[dict[str, Any]],
    sample_fps: float,
    max_samples: int,
) -> tuple[list[int], dict[int, list[str]]]:
    if sample_fps <= 0:
        raise ValueError("--sample-fps must be positive")
    step = max(1, round(metadata["fps"] / sample_fps))
    periodic = list(range(0, metadata["frame_count"], step))
    periodic.append(metadata["frame_count"] - 1)
    periodic = evenly_limit(sorted(set(periodic)), max_samples)

    sources: dict[int, set[str]] = {}
    for frame_id in periodic:
        sources.setdefault(frame_id, set()).add("periodic")
    for scene in scenes:
        frame_id = int(scene.get("mid_frame", -1))
        if 0 <= frame_id < metadata["frame_count"]:
            sources.setdefault(frame_id, set()).add("scene_midpoint")
    targets = sorted(sources)
    if len(targets) > max_samples:
        scene_ids = [frame_id for frame_id in targets if "scene_midpoint" in sources[frame_id]]
        scene_ids = evenly_limit(scene_ids, min(len(scene_ids), max_samples))
        remaining = max(0, max_samples - len(scene_ids))
        periodic_ids = [frame_id for frame_id in targets if frame_id not in set(scene_ids)]
        targets = sorted(set(scene_ids + evenly_limit(periodic_ids, remaining)))
    return targets, {frame_id: sorted(sources[frame_id]) for frame_id in targets}


def iter_target_frames(video: Path, targets: list[int]):
    capture = cv2.VideoCapture(str(video))
    if not capture.isOpened():
        raise RuntimeError(f"Cannot open video: {video}")
    target_set = set(targets)
    last_target = targets[-1]
    frame_id = 0
    while frame_id <= last_target:
        if frame_id in target_set:
            ok, frame = capture.read()
            if not ok:
                break
            yield frame_id, frame
        else:
            if not capture.grab():
                break
        frame_id += 1
    capture.release()


def encode_clip(model, preprocess, device: str, frames: list[np.ndarray]) -> np.ndarray:
    import torch

    tensors = []
    for frame in frames:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        tensors.append(preprocess(Image.fromarray(rgb)))
    batch = torch.stack(tensors).to(device)
    with torch.inference_mode():
        features = model.encode_image(batch).float()
        features = features / features.norm(dim=-1, keepdim=True).clamp_min(1e-12)
    return features.cpu().numpy().astype(np.float32)


def detector_rows(results, names: dict[int, str] | list[str]) -> list[dict[str, Any]]:
    rows = []
    for result in results:
        detections = []
        counts: dict[str, int] = {}
        if result.boxes is not None and len(result.boxes):
            xyxy = result.boxes.xyxy.cpu().numpy()
            confidences = result.boxes.conf.cpu().numpy()
            classes = result.boxes.cls.cpu().numpy().astype(int)
            for box, confidence, class_id in zip(xyxy, confidences, classes):
                label = names[class_id] if isinstance(names, list) else names.get(class_id, str(class_id))
                counts[label] = counts.get(label, 0) + 1
                detections.append(
                    {
                        "label": label,
                        "confidence": round(float(confidence), 5),
                        "box_xyxy": [round(float(value), 2) for value in box],
                    }
                )
        rows.append({"object_counts": counts, "detections": detections})
    return rows


def object_change(previous: dict[str, int] | None, current: dict[str, int]) -> float:
    if previous is None:
        return 0.0
    labels = set(previous) | set(current)
    denominator = sum(previous.values()) + sum(current.values())
    if denominator == 0:
        return 0.0
    return sum(abs(previous.get(label, 0) - current.get(label, 0)) for label in labels) / denominator


def robust_normalize(values: list[float]) -> np.ndarray:
    array = np.asarray(values, dtype=np.float32)
    if len(array) < 2:
        return np.zeros_like(array)
    low, high = np.percentile(array, [5, 95])
    if high <= low + 1e-9:
        return np.zeros_like(array)
    return np.clip((array - low) / (high - low), 0.0, 1.0)


def cluster_representatives(embeddings: np.ndarray, cluster_count: int) -> tuple[np.ndarray, list[int]]:
    from sklearn.cluster import MiniBatchKMeans

    count = min(max(1, cluster_count), len(embeddings))
    if count == 1:
        return np.zeros(len(embeddings), dtype=np.int32), [0]
    estimator = MiniBatchKMeans(
        n_clusters=count,
        random_state=42,
        batch_size=min(256, max(count * 3, 32)),
        n_init="auto",
    )
    labels = estimator.fit_predict(embeddings.astype(np.float32))
    centers = estimator.cluster_centers_.astype(np.float32)
    centers /= np.linalg.norm(centers, axis=1, keepdims=True).clip(min=1e-12)
    representatives = []
    for cluster_id in range(count):
        indices = np.flatnonzero(labels == cluster_id)
        similarities = embeddings[indices] @ centers[cluster_id]
        representatives.append(int(indices[int(np.argmax(similarities))]))
    return labels.astype(np.int32), representatives


def select_candidates(
    records: list[dict[str, Any]],
    representative_indices: list[int],
    limit: int,
    min_gap_seconds: float,
) -> list[int]:
    selected: list[int] = []

    def add(index: int, enforce_gap: bool = True) -> None:
        if index in selected or len(selected) >= limit:
            return
        seconds = records[index]["seconds"]
        if enforce_gap and any(abs(seconds - records[item]["seconds"]) < min_gap_seconds for item in selected):
            return
        selected.append(index)

    for index in sorted(representative_indices, key=lambda item: records[item]["candidate_score"], reverse=True):
        add(index)
    for index in sorted(range(len(records)), key=lambda item: records[item]["candidate_score"], reverse=True):
        add(index)
    if len(selected) < limit:
        for index in sorted(range(len(records)), key=lambda item: records[item]["candidate_score"], reverse=True):
            add(index, enforce_gap=False)
    return selected


def compact_candidate(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "rank": row["rank"],
        "frame_id": row["frame_id"],
        "seconds": row["seconds"],
        "score": row["candidate_score"],
        "cluster_id": row["cluster_id"],
        "objects": row["object_counts"],
        "reasons": row["reasons"],
        "frame": row["candidate_frame"],
    }


def select_diverse_summary(
    candidate_rows: list[dict[str, Any]],
    limit: int,
    duration_seconds: float,
) -> list[dict[str, Any]]:
    """Mix score, temporal coverage, and CLIP-cluster diversity."""
    if len(candidate_rows) <= limit:
        return list(candidate_rows)
    selected: list[dict[str, Any]] = []
    selected_frames: set[int] = set()

    def add(row: dict[str, Any]) -> None:
        if len(selected) >= limit or row["frame_id"] in selected_frames:
            return
        selected.append(row)
        selected_frames.add(row["frame_id"])

    for row in candidate_rows[: max(2, limit // 3)]:
        add(row)

    bin_count = min(8, max(2, limit // 2))
    if duration_seconds > 0:
        for bin_id in range(bin_count):
            start = duration_seconds * bin_id / bin_count
            end = duration_seconds * (bin_id + 1) / bin_count
            rows = [
                row
                for row in candidate_rows
                if start <= row["seconds"] < end or (bin_id == bin_count - 1 and row["seconds"] <= end)
            ]
            if rows:
                add(max(rows, key=lambda row: row["candidate_score"]))

    seen_clusters = {row["cluster_id"] for row in selected}
    for row in sorted(
        candidate_rows,
        key=lambda item: (not item["cluster_representative"], -item["candidate_score"]),
    ):
        if row["cluster_id"] not in seen_clusters:
            add(row)
            seen_clusters.add(row["cluster_id"])

    for row in candidate_rows:
        add(row)
    return sorted(selected, key=lambda row: row["rank"])


def assess_adaptive_expansion(
    summary_rows: list[dict[str, Any]],
    candidate_rows: list[dict[str, Any]],
    duration_seconds: float,
    query_type: str,
) -> dict[str, Any]:
    if not summary_rows:
        return {
            "recommended": False,
            "reasons": ["no_candidates"],
            "metrics": {},
        }
    bin_count = 4 if duration_seconds >= 120 else 2
    represented_bins = {
        min(bin_count - 1, int(row["seconds"] / max(duration_seconds, 1e-9) * bin_count))
        for row in summary_rows
    }
    unique_clusters = len({row["cluster_id"] for row in summary_rows})
    strong_candidates = sum(row["candidate_score"] >= 0.35 for row in summary_rows)
    temporal_span = (
        (max(row["seconds"] for row in summary_rows) - min(row["seconds"] for row in summary_rows))
        / max(duration_seconds, 1e-9)
    )
    reasons = []
    can_expand = len(candidate_rows) > len(summary_rows)
    if can_expand and query_type == "trake":
        reasons.append("trake_requires_broader_ordered_event_coverage")
    if can_expand and duration_seconds >= 300 and (len(represented_bins) < 2 or temporal_span < 0.25):
        reasons.append("narrow_temporal_coverage")
    minimum_clusters = min(3, max(1, len(summary_rows) // 3))
    if can_expand and unique_clusters < minimum_clusters:
        reasons.append("low_clip_cluster_diversity")
    if can_expand and strong_candidates < min(2, len(summary_rows)):
        reasons.append("low_semantic_strength")
    return {
        "recommended": bool(reasons),
        "reasons": reasons,
        "metrics": {
            "represented_temporal_bins": len(represented_bins),
            "temporal_bins": bin_count,
            "temporal_span_ratio": round(temporal_span, 4),
            "unique_clip_clusters": unique_clusters,
            "strong_candidate_count": strong_candidates,
        },
    }


def save_full_resolution_frames(video: Path, records: list[dict[str, Any]], indices: list[int], output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    by_frame = {records[index]["frame_id"]: index for index in indices}
    for frame_id, frame in iter_target_frames(video, sorted(by_frame)):
        index = by_frame[frame_id]
        path = output / f"f{frame_id:09d}_t{records[index]['seconds']:012.3f}.jpg"
        if not cv2.imwrite(str(path), frame, [cv2.IMWRITE_JPEG_QUALITY, 95]):
            raise RuntimeError(f"Failed to write candidate frame: {path}")
        records[index]["candidate_frame"] = str(path.resolve())


def resolve_inputs(args: argparse.Namespace) -> tuple[Path, Path | None, Path, str, list[dict[str, Any]], dict[str, Any] | None]:
    manifest_path = Path(args.manifest).resolve() if args.manifest else None
    manifest = read_json(manifest_path) if manifest_path else None
    video_value = args.video or (manifest or {}).get("video_path")
    if not video_value:
        raise ValueError("Supply --video or a manifest containing video_path")
    video = Path(video_value).resolve()
    if not video.is_file():
        raise FileNotFoundError(video)
    profile = args.profile or (manifest or {}).get("profile") or "high"
    if profile not in {"high", "xhigh"}:
        raise ValueError(f"Unsupported profile: {profile}")
    scenes_value = args.scenes or ((manifest or {}).get("artifacts") or {}).get("scenes")
    scenes = read_json(Path(scenes_value)) if scenes_value and Path(scenes_value).is_file() else []
    if args.output:
        output = Path(args.output).resolve()
    elif manifest_path:
        output = manifest_path.parent / "semantic"
    else:
        output = video.parent / f"{video.stem}-semantic"
    return video, manifest_path, output.resolve(), profile, scenes, manifest


def main() -> int:
    args = parse_args()
    video, manifest_path, output, profile, scenes, manifest = resolve_inputs(args)
    output.mkdir(parents=True, exist_ok=True)
    metadata = video_metadata(video)

    defaults = {
        "high": {"sample_fps": 1.0, "candidate_limit": 24, "summary_limit": 8, "cluster_count": 16, "max_samples": 1500},
        "xhigh": {"sample_fps": 2.0, "candidate_limit": 40, "summary_limit": 12, "cluster_count": 24, "max_samples": 3000},
    }[profile]
    sample_fps = args.sample_fps if args.sample_fps is not None else defaults["sample_fps"]
    candidate_limit = args.candidate_limit if args.candidate_limit is not None else defaults["candidate_limit"]
    summary_limit = args.summary_limit if args.summary_limit is not None else defaults["summary_limit"]
    cluster_count = args.cluster_count if args.cluster_count is not None else defaults["cluster_count"]
    max_samples = args.max_samples if args.max_samples is not None else defaults["max_samples"]
    if args.batch_size < 1 or candidate_limit < 1 or summary_limit < 1 or cluster_count < 1 or max_samples < 1:
        raise ValueError("Batch size and count limits must be positive")

    targets, sources = build_targets(metadata, scenes, sample_fps, max_samples)
    if not targets:
        raise RuntimeError("No sample frames were selected")

    import open_clip
    import torch
    from ultralytics import YOLO

    clip_device = choose_clip_device(args.clip_device)
    print(f"Loading OpenCLIP {args.clip_model}/{args.clip_pretrained} on {clip_device}", flush=True)
    clip_model, _, preprocess = open_clip.create_model_and_transforms(
        args.clip_model,
        pretrained=args.clip_pretrained,
        cache_dir=str(Path(args.clip_cache).resolve()),
    )
    clip_model = clip_model.eval().to(clip_device)
    yolo_path = Path(args.yolo_model).resolve()
    if not yolo_path.is_file():
        raise FileNotFoundError(f"YOLO model not found: {yolo_path}")
    print(f"Loading YOLO {yolo_path.name} on {args.yolo_device}", flush=True)
    detector = YOLO(str(yolo_path))

    records: list[dict[str, Any]] = []
    embedding_batches: list[np.ndarray] = []
    previous_gray: np.ndarray | None = None
    batch_ids: list[int] = []
    batch_frames: list[np.ndarray] = []

    def process_batch() -> None:
        nonlocal previous_gray
        if not batch_frames:
            return
        clip_features = encode_clip(clip_model, preprocess, clip_device, batch_frames)
        yolo_results = detector.predict(
            source=batch_frames,
            imgsz=args.yolo_imgsz,
            conf=args.yolo_conf,
            device=args.yolo_device,
            verbose=False,
        )
        detections = detector_rows(yolo_results, detector.names)
        for frame_id, frame, detector_row in zip(batch_ids, batch_frames, detections):
            gray = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (160, 90), interpolation=cv2.INTER_AREA)
            motion = 0.0 if previous_gray is None else float(np.mean(cv2.absdiff(gray, previous_gray)) / 255.0)
            previous_gray = gray
            records.append(
                {
                    "frame_id": frame_id,
                    "seconds": round(frame_id / metadata["fps"], 6),
                    "sources": sources[frame_id],
                    "motion_raw": round(motion, 6),
                    **detector_row,
                }
            )
        embedding_batches.append(clip_features)
        print(f"Indexed {len(records)}/{len(targets)} frames", flush=True)
        batch_ids.clear()
        batch_frames.clear()

    for frame_id, frame in iter_target_frames(video, targets):
        batch_ids.append(frame_id)
        batch_frames.append(frame)
        if len(batch_frames) >= args.batch_size:
            process_batch()
    process_batch()
    if len(records) != len(targets):
        print(f"Warning: decoded {len(records)} of {len(targets)} target frames", flush=True)
    if not records:
        raise RuntimeError("No video frames could be decoded")

    embeddings = np.concatenate(embedding_batches, axis=0)[: len(records)]
    previous_counts: dict[str, int] | None = None
    for index, record in enumerate(records):
        record["clip_change_raw"] = 0.0 if index == 0 else round(max(0.0, float(1.0 - embeddings[index] @ embeddings[index - 1])), 6)
        record["object_change_raw"] = round(object_change(previous_counts, record["object_counts"]), 6)
        previous_counts = record["object_counts"]

    clip_norm = robust_normalize([record["clip_change_raw"] for record in records])
    object_norm = robust_normalize([record["object_change_raw"] for record in records])
    motion_norm = robust_normalize([record["motion_raw"] for record in records])
    scene_flags = np.asarray(["scene_midpoint" in record["sources"] for record in records], dtype=np.float32)
    scores = 0.45 * clip_norm + 0.25 * object_norm + 0.20 * motion_norm + 0.10 * scene_flags

    labels, representatives = cluster_representatives(embeddings, cluster_count)
    representative_set = set(representatives)
    for index, record in enumerate(records):
        record["clip_change"] = round(float(clip_norm[index]), 6)
        record["object_change"] = round(float(object_norm[index]), 6)
        record["motion"] = round(float(motion_norm[index]), 6)
        record["scene_midpoint"] = bool(scene_flags[index])
        record["cluster_id"] = int(labels[index])
        record["cluster_representative"] = index in representative_set
        record["candidate_score"] = round(float(scores[index]), 6)

    selected = select_candidates(records, representatives, min(candidate_limit, len(records)), args.min_gap_seconds)
    save_full_resolution_frames(video, records, selected, output / "candidate-frames")

    embeddings_path = output / "embeddings.npz"
    np.savez_compressed(
        embeddings_path,
        frame_ids=np.asarray([record["frame_id"] for record in records], dtype=np.int64),
        seconds=np.asarray([record["seconds"] for record in records], dtype=np.float32),
        embeddings=embeddings.astype(np.float16),
    )

    candidate_rows = []
    representative_frames = {records[index]["frame_id"] for index in representatives}
    for rank, index in enumerate(sorted(selected, key=lambda item: records[item]["candidate_score"], reverse=True), start=1):
        source = records[index]
        row = {
            key: source[key]
            for key in (
                "frame_id",
                "seconds",
                "sources",
                "object_counts",
                "clip_change",
                "object_change",
                "motion",
                "scene_midpoint",
                "cluster_id",
                "cluster_representative",
                "candidate_score",
                "candidate_frame",
            )
        }
        row["rank"] = rank
        reasons = []
        if row["frame_id"] in representative_frames:
            reasons.append("clip_cluster_representative")
        if row["candidate_score"] >= 0.5:
            reasons.append("semantic_or_object_change")
        if row["scene_midpoint"]:
            reasons.append("scene_midpoint")
        row["reasons"] = reasons or ["coverage"]
        candidate_rows.append(row)

    samples_path = output / "semantic-samples.json"
    atomic_write_json(samples_path, records)
    detected_object_totals: dict[str, int] = {}
    for record in records:
        for label, count in record["object_counts"].items():
            detected_object_totals[label] = detected_object_totals.get(label, 0) + count
    detected_object_totals = dict(
        sorted(detected_object_totals.items(), key=lambda item: (-item[1], item[0]))[:20]
    )

    index_path = output / "semantic-index.json"
    summary_path = output / "semantic-summary.json"
    expanded_summary_path = output / "semantic-summary-expanded.json"
    default_rows = candidate_rows[: min(summary_limit, len(candidate_rows))]
    expanded_limit = min(candidate_limit, max(summary_limit, summary_limit * 2), len(candidate_rows))
    expanded_rows = select_diverse_summary(candidate_rows, expanded_limit, metadata["duration_seconds"])
    summary_candidates = [compact_candidate(row) for row in default_rows]
    expanded_candidates = [compact_candidate(row) for row in expanded_rows]
    query_type = str((manifest or {}).get("query_type") or "unknown")
    adaptive = assess_adaptive_expansion(
        default_rows,
        candidate_rows,
        metadata["duration_seconds"],
        query_type,
    )
    adaptive["expanded_summary"] = str(expanded_summary_path.resolve())
    adaptive["expanded_candidate_count"] = len(expanded_candidates)
    summary_payload = {
        "schema_version": 2,
        "profile": profile,
        "video": {
            "id": video.stem,
            "duration_seconds": round(metadata["duration_seconds"], 3),
            "fps": metadata["fps"],
            "resolution": f"{metadata['width']}x{metadata['height']}",
        },
        "candidate_count_total": len(candidate_rows),
        "candidate_count_in_summary": len(summary_candidates),
        "detected_object_totals": dict(list(detected_object_totals.items())[:12]),
        "candidates": summary_candidates,
        "adaptive_expansion": adaptive,
        "full_index": str(index_path.resolve()),
    }
    summary_rendered = json.dumps(summary_payload, ensure_ascii=False, indent=2)
    summary_payload["estimated_text_tokens_conservative"] = math.ceil((len(summary_rendered) + 80) / 2.0)
    atomic_write_json(summary_path, summary_payload)
    expanded_payload = {
        "schema_version": 2,
        "profile": profile,
        "expansion_level": 1,
        "selection_strategy": "top_score + temporal_bins + unique_clip_clusters",
        "trigger_reasons": adaptive["reasons"],
        "video": summary_payload["video"],
        "candidate_count_total": len(candidate_rows),
        "candidate_count_in_summary": len(expanded_candidates),
        "detected_object_totals": summary_payload["detected_object_totals"],
        "candidates": expanded_candidates,
        "full_index": str(index_path.resolve()),
    }
    expanded_rendered = json.dumps(expanded_payload, ensure_ascii=False, indent=2)
    expanded_payload["estimated_text_tokens_conservative"] = math.ceil((len(expanded_rendered) + 80) / 2.0)
    atomic_write_json(expanded_summary_path, expanded_payload)

    index_payload = {
        "schema_version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "profile": profile,
        "video": {"path": str(video), **metadata},
        "models": {
            "openclip": {
                "model": args.clip_model,
                "pretrained": args.clip_pretrained,
                "device": clip_device,
                "package_version": package_version("open-clip-torch"),
                "torch_version": torch.__version__,
            },
            "yolo": {
                "model_path": str(yolo_path),
                "device": args.yolo_device,
                "imgsz": args.yolo_imgsz,
                "confidence": args.yolo_conf,
                "package_version": package_version("ultralytics"),
            },
            "clustering": {"package_version": package_version("scikit-learn")},
        },
        "sampling": {
            "sample_fps": sample_fps,
            "requested_targets": len(targets),
            "decoded_samples": len(records),
            "max_samples": max_samples,
            "cluster_count": len(representatives),
            "candidate_limit": candidate_limit,
            "summary_limit": summary_limit,
            "expanded_summary_limit": expanded_limit,
            "min_gap_seconds": args.min_gap_seconds,
        },
        "score": {
            "formula": "0.45*clip_change + 0.25*object_change + 0.20*motion + 0.10*scene_midpoint",
            "normalization": "5th-95th percentile clipping per video",
            "note": "Candidate ranking is a retrieval heuristic; verify facts and endpoints in source frames.",
        },
        "artifacts": {
            "embeddings": str(embeddings_path.resolve()),
            "samples": str(samples_path.resolve()),
            "summary": str(summary_path.resolve()),
            "expanded_summary": str(expanded_summary_path.resolve()),
            "candidate_frames_dir": str((output / "candidate-frames").resolve()),
        },
        "detected_object_totals": detected_object_totals,
        "cluster_representatives": [
            {
                "cluster_id": int(labels[index]),
                "frame_id": records[index]["frame_id"],
                "seconds": records[index]["seconds"],
                "candidate_frame": records[index].get("candidate_frame"),
            }
            for index in representatives
        ],
        "candidates": candidate_rows,
    }
    atomic_write_json(index_path, index_payload)

    if manifest_path and manifest is not None:
        manifest.setdefault("artifacts", {})["semantic_index"] = str(index_path.resolve())
        manifest["artifacts"]["semantic_summary"] = str(summary_path.resolve())
        manifest["artifacts"]["semantic_summary_expanded"] = str(expanded_summary_path.resolve())
        manifest["artifacts"]["semantic_embeddings"] = str(embeddings_path.resolve())
        manifest["artifacts"]["semantic_samples"] = str(samples_path.resolve())
        manifest["artifacts"]["semantic_candidate_frames"] = str((output / "candidate-frames").resolve())
        manifest.setdefault("sampling", {})["semantic"] = index_payload["sampling"]
        manifest["next_step"] = (
            "Read semantic-summary.json and inspect adaptive_expansion. Open semantic-summary-expanded.json when "
            "recommended or when initial evidence is repetitive/ambiguous. Use adaptive transcript_search.py around "
            "selected timestamps, clip_search.py for event-specific retrieval, and dense windows for exact endpoints."
        )
        atomic_write_json(manifest_path, manifest)

    print(
        json.dumps(
            {
                "semantic_index": str(index_path.resolve()),
                "semantic_summary": str(summary_path.resolve()),
                "semantic_summary_expanded": str(expanded_summary_path.resolve()),
                "adaptive_expansion_recommended": adaptive["recommended"],
                "embeddings": str(embeddings_path.resolve()),
                "samples_metadata": str(samples_path.resolve()),
                "samples": len(records),
                "candidates": len(candidate_rows),
                "clip_device": clip_device,
                "yolo_device": args.yolo_device,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
