#!/usr/bin/env python3
"""Validate the semantic-video Python environment and optionally prefetch models."""

from __future__ import annotations

import argparse
import json
import os
import platform
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models-dir", required=True)
    parser.add_argument("--yolo-model", default="yolo26n.pt")
    parser.add_argument("--clip-model", default="ViT-B-32")
    parser.add_argument("--clip-pretrained", default="laion2b_s34b_b79k")
    parser.add_argument("--report", required=True)
    parser.add_argument("--download-models", action="store_true")
    return parser.parse_args()


def package_version(name: str) -> str:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return "not-installed"


def main() -> int:
    args = parse_args()
    models_dir = Path(args.models_dir).resolve()
    report_path = Path(args.report).resolve()
    models_dir.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    import numpy as np
    import open_clip
    import sklearn
    import torch
    import torchvision
    import ultralytics
    from PIL import Image
    from ultralytics import YOLO

    xpu_available = bool(hasattr(torch, "xpu") and torch.xpu.is_available())
    xpu_name = None
    xpu_tensor_test = False
    if xpu_available:
        xpu_name = torch.xpu.get_device_name(0)
        value = torch.tensor([1.0, 2.0], device="xpu").sum().cpu().item()
        xpu_tensor_test = value == 3.0

    result: dict = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "packages": {
            "torch": torch.__version__,
            "torchvision": torchvision.__version__,
            "open_clip_torch": package_version("open_clip_torch"),
            "ultralytics": ultralytics.__version__,
            "scikit_learn": sklearn.__version__,
        },
        "xpu": {
            "available": xpu_available,
            "device_name": xpu_name,
            "tensor_test": xpu_tensor_test,
        },
        "models_dir": str(models_dir),
        "models_downloaded": bool(args.download_models),
    }

    if args.download_models:
        original_directory = Path.cwd()
        try:
            os.chdir(models_dir)
            yolo = YOLO(args.yolo_model)
            yolo_results = yolo.predict(
                source=np.zeros((640, 640, 3), dtype=np.uint8),
                device="cpu",
                verbose=False,
            )
            yolo_path = (models_dir / args.yolo_model).resolve()
            if not yolo_path.is_file():
                raise FileNotFoundError(f"YOLO checkpoint was not saved at {yolo_path}")
        finally:
            os.chdir(original_directory)

        clip_cache = models_dir / "openclip"
        clip_cache.mkdir(parents=True, exist_ok=True)
        clip_model, _, preprocess = open_clip.create_model_and_transforms(
            args.clip_model,
            pretrained=args.clip_pretrained,
            cache_dir=str(clip_cache),
        )
        clip_model.eval()
        clip_device = "xpu" if xpu_available else "cpu"
        clip_model = clip_model.to(clip_device)
        sample = preprocess(Image.new("RGB", (224, 224), color=(127, 127, 127))).unsqueeze(0)
        with torch.inference_mode():
            embedding = clip_model.encode_image(sample.to(clip_device))
            embedding = embedding / embedding.norm(dim=-1, keepdim=True)
        if embedding.ndim != 2 or embedding.shape[0] != 1:
            raise RuntimeError(f"Unexpected OpenCLIP embedding shape: {tuple(embedding.shape)}")

        result["model_checks"] = {
            "yolo": {
                "model": args.yolo_model,
                "checkpoint": str(yolo_path),
                "dummy_inference_results": len(yolo_results),
                "device": "cpu",
            },
            "openclip": {
                "model": args.clip_model,
                "pretrained": args.clip_pretrained,
                "cache": str(clip_cache),
                "embedding_shape": list(embedding.shape),
                "device": clip_device,
            },
        }

    report_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
