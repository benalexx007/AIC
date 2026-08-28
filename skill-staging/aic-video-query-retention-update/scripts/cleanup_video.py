#!/usr/bin/env python3
"""Deprecated compatibility shim; current policy retains the completed run."""

from __future__ import annotations

import json


def main() -> int:
    print(
        json.dumps(
            {
                "deleted": False,
                "deprecated": True,
                "reason": (
                    "Completed runs are retained. Use purge_previous_runs.py only before "
                    "processing a later, different video."
                ),
            }
        )
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
