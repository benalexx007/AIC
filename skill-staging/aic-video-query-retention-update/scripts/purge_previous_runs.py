#!/usr/bin/env python3
"""Safely purge every prior per-video run while preserving final outputs."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs-root", default=r"D:\AIC\video-runs")
    parser.add_argument("--protected-root", default=r"D:\AIC\test")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Delete the listed children. Without this flag, perform a dry run.",
    )
    return parser.parse_args()


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def validate_roots(runs_root: Path, protected_root: Path) -> None:
    if runs_root == Path(runs_root.anchor):
        raise RuntimeError(f"Cleanup refused: runs root is a drive root: {runs_root}")
    if runs_root.name.casefold() != "video-runs":
        raise RuntimeError(f"Cleanup refused: expected a directory named video-runs: {runs_root}")
    if runs_root == protected_root:
        raise RuntimeError("Cleanup refused: runs root equals protected root")
    if is_relative_to(protected_root, runs_root) or is_relative_to(runs_root, protected_root):
        raise RuntimeError("Cleanup refused: runs root and protected root overlap")


def entry_size(path: Path) -> tuple[int, int]:
    if path.is_symlink() or path.is_file():
        try:
            return path.lstat().st_size, 1
        except FileNotFoundError:
            return 0, 0
    total_bytes = 0
    total_files = 0
    for child in path.rglob("*"):
        if child.is_file() or child.is_symlink():
            try:
                total_bytes += child.lstat().st_size
                total_files += 1
            except FileNotFoundError:
                continue
    return total_bytes, total_files


def main() -> int:
    args = parse_args()
    runs_root = Path(args.runs_root).resolve()
    protected_root = Path(args.protected_root).resolve()
    validate_roots(runs_root, protected_root)

    if not runs_root.exists():
        print(
            json.dumps(
                {
                    "executed": args.execute,
                    "runs_root": str(runs_root),
                    "protected_root": str(protected_root),
                    "targets": [],
                    "deleted_bytes": 0,
                    "deleted_files": 0,
                }
            )
        )
        return 0
    if not runs_root.is_dir():
        raise RuntimeError(f"Cleanup refused: runs root is not a directory: {runs_root}")

    targets = []
    total_bytes = 0
    total_files = 0
    for entry in sorted(runs_root.iterdir(), key=lambda item: item.name.casefold()):
        resolved = entry.resolve()
        if not is_relative_to(resolved, runs_root):
            raise RuntimeError(f"Cleanup refused: target resolves outside runs root: {entry}")
        if resolved == protected_root or is_relative_to(protected_root, resolved):
            raise RuntimeError(f"Cleanup refused: target could contain protected root: {entry}")
        size_bytes, file_count = entry_size(entry)
        targets.append(str(entry))
        total_bytes += size_bytes
        total_files += file_count

    if args.execute:
        for entry_text in targets:
            entry = Path(entry_text)
            if entry.is_symlink() or entry.is_file():
                entry.unlink()
            elif entry.is_dir():
                shutil.rmtree(entry)
            else:
                raise RuntimeError(f"Cleanup stopped: unsupported target type: {entry}")

    print(
        json.dumps(
            {
                "executed": args.execute,
                "runs_root": str(runs_root),
                "protected_root": str(protected_root),
                "targets": targets,
                "target_count": len(targets),
                "deleted_bytes": total_bytes if args.execute else 0,
                "deleted_files": total_files if args.execute else 0,
                "planned_bytes": total_bytes,
                "planned_files": total_files,
                "recoverable": False if args.execute and targets else None,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
