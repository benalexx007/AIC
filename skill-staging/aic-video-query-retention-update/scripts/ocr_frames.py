#!/usr/bin/env python3
"""Run targeted PaddleOCR without importing Faster-Whisper/CTranslate2."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", nargs="*", default=[])
    parser.add_argument("--list", dest="list_file")
    parser.add_argument("--output", required=True)
    parser.add_argument("--lang", default="vi")
    parser.add_argument("--min-score", type=float, default=0.45)
    parser.add_argument("--cache", default=r"D:\AIC\.cache\paddlex")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    os.environ["PADDLE_PDX_CACHE_HOME"] = args.cache
    os.environ["PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK"] = "True"
    from paddleocr import PaddleOCR

    images = [Path(item) for item in args.images]
    if args.list_file:
        images.extend(
            Path(line.strip())
            for line in Path(args.list_file).read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    if not images:
        raise SystemExit("No images supplied")

    ocr = PaddleOCR(
        lang=args.lang,
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
        enable_mkldnn=False,
    )
    output = []
    for image_path in images:
        if not image_path.is_file():
            output.append({"image": str(image_path), "error": "not found"})
            continue
        predictions = ocr.predict(str(image_path))
        raw = predictions[0].json if predictions else {}
        result = raw.get("res", raw)
        texts = result.get("rec_texts", [])
        scores = result.get("rec_scores", [])
        polygons = result.get("rec_polys", result.get("dt_polys", []))
        lines = []
        for index, text in enumerate(texts):
            score = float(scores[index]) if index < len(scores) else 0.0
            if text.strip() and score >= args.min_score:
                polygon = polygons[index] if index < len(polygons) else None
                if hasattr(polygon, "tolist"):
                    polygon = polygon.tolist()
                lines.append({"text": text.strip(), "score": round(score, 4), "polygon": polygon})
        output.append({"image": str(image_path.resolve()), "lines": lines})

    destination = Path(args.output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"images": len(images), "output": str(destination.resolve())}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
