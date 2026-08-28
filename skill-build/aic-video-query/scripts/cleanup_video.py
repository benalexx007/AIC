#!/usr/bin/env python3
"""Safely delete only a completed run's downloaded Drive source video."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--result-yaml", required=True)
    parser.add_argument("--runs-root", default=r"D:\AIC\video-runs")
    return parser.parse_args()


def require_final_file(value: str, label: str) -> Path:
    path = Path(value).resolve()
    if not path.is_file() or path.stat().st_size <= 0:
        raise RuntimeError(f"Final {label} file is missing or empty: {path}")
    return path


def main() -> int:
    args = parse_args()
    manifest_path = Path(args.manifest).resolve()
    result_path = Path(args.result_yaml).resolve()
    runs_root = Path(args.runs_root).resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    payload = yaml.safe_load(result_path.read_text(encoding="utf-8-sig"))

    source_info = manifest.get("input", {})
    if source_info.get("origin") != "google_drive" or source_info.get("downloaded_source") is not True:
        raise RuntimeError("Cleanup refused: manifest does not identify a downloaded Google Drive source")

    files = payload.get("files", {})
    query_path = require_final_file(files.get("query", ""), "query")
    answer_path = require_final_file(files.get("answer", ""), "answer")
    yaml_recorded = require_final_file(files.get("yaml", ""), "YAML")
    if yaml_recorded != result_path:
        raise RuntimeError("Cleanup refused: --result-yaml does not match the YAML record")

    source = Path(manifest["video_path"]).resolve()
    if not source.is_relative_to(runs_root):
        raise RuntimeError(f"Cleanup refused: source is outside runs root: {source}")

    previous = payload.get("cleanup", {})
    if previous.get("deleted") is True and not source.exists():
        print(json.dumps({"deleted": False, "already_deleted": True, "source": str(source)}))
        return 0
    if not source.is_file():
        raise FileNotFoundError(f"Downloaded source video is missing: {source}")

    size = source.stat().st_size
    source.unlink()
    payload["cleanup"] = {
        "source_video": str(source),
        "deleted": True,
        "deleted_size_bytes": size,
        "deleted_at_utc": datetime.now(timezone.utc).isoformat(),
        "recoverable": False,
        "retained_outputs": [str(query_path), str(answer_path), str(result_path)],
    }
    temporary = result_path.with_suffix(result_path.suffix + ".tmp")
    temporary.write_text(
        yaml.safe_dump(payload, allow_unicode=True, sort_keys=False, width=4096),
        encoding="utf-8-sig",
    )
    temporary.replace(result_path)
    print(
        json.dumps(
            {
                "deleted": True,
                "source": str(source),
                "deleted_size_bytes": size,
                "recoverable": False,
                "result_yaml": str(result_path),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
