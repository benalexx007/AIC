#!/usr/bin/env python3
"""Evaluate a sample query, record 2D metrics, and manage learning decisions."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate sample test case and manage learning gate")
    parser.add_argument("--query-file", required=True, help="Path to sample query txt file")
    parser.add_argument("--answer-file", required=True, help="Path to sample answer csv file")
    parser.add_argument("--difficulty-tier", type=int, required=True, choices=[1, 2, 3, 4, 5], help="Assessed difficulty tier (1-5)")
    parser.add_argument("--accuracy-score", type=float, required=True, help="Assessed accuracy percentage (0.0 to 100.0)")
    parser.add_argument("--intervals-json", required=True, help="JSON string representing list of extracted intervals, e.g. '[{\"start_frame\": 450, \"end_frame\": 520, \"event_desc\": \"E1\"}]'")
    parser.add_argument("--mod-vis", default="None", help="Visual reasoning difficulty analysis")
    parser.add_argument("--mod-aud", default="None", help="Acoustic/audio depth analysis")
    parser.add_argument("--mod-ocr", default="None", help="OCR/Text difficulty analysis")
    parser.add_argument("--mod-word", default="None", help="Wording / adversarial phrasing analysis")
    parser.add_argument("--mod-flow", default="None", help="Narrative flow / puzzle structure analysis")
    parser.add_argument("--accuracy-analysis", required=True, help="Detailed justification for the accuracy score")
    parser.add_argument("--distilled-insights", default="", help="Extracted insights/patterns to update 5 modules if learned")
    parser.add_argument("--log-file", default=r"D:\AIC\test\sample\evaluation_log.json", help="Path to evaluation log JSON")
    parser.add_argument("--report-file", default=r"D:\AIC\test\sample\evaluation_report.md", help="Path to evaluation report Markdown")
    return parser.parse_args()


def read_line_1_only(csv_path: Path) -> tuple[str, int | None]:
    """Strictly read only the first line of the answer CSV file."""
    if not csv_path.is_file():
        raise FileNotFoundError(f"Answer CSV file not found: {csv_path}")
    with csv_path.open("r", encoding="utf-8-sig", errors="replace") as f:
        line1 = f.readline().strip()
    if not line1:
        raise ValueError(f"First line of CSV is empty: {csv_path}")
    parts = [p.strip() for p in line1.split(",")]
    video_id = parts[0]
    seed_frame = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else None
    return video_id, seed_frame


def update_markdown_report(report_path: Path, records: list[dict]) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    learned_count = sum(1 for r in records if r["learning_decision"] == "LEARNED")
    rejected_count = len(records) - learned_count
    
    lines = [
        "# Báo Cáo Đánh Giá & Học Hỏi Từ Query Mẫu (Sample Evaluation Report)",
        "",
        f"> **Cập nhật lần cuối:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}  ",
        f"> **Tổng số mẫu đã đánh giá:** {len(records)} | **Đã học (Learned):** {learned_count} | **Từ chối (Rejected):** {rejected_count}",
        "",
        "## 📊 Bảng Tổng Hợp Đánh Giá",
        "",
        "| Sample ID | Video ID | Seed (Line 1) | Extracted Intervals | Tier | Accuracy | Decision | Key Insights |",
        "|---|---|---|---|:---:|:---:|:---:|---|",
    ]
    
    for r in records:
        intervals_str = ", ".join(f"[{item.get('start_frame')}, {item.get('end_frame')}]" for item in r["extracted_intervals"])
        decision_badge = "✅ **LEARNED**" if r["learning_decision"] == "LEARNED" else "❌ REJECTED"
        insights_short = (r.get("distilled_insights") or r.get("evaluation", {}).get("accuracy_analysis", ""))[:80].replace("|", "-")
        lines.append(
            f"| `{r['sample_id']}` | `{r['target_video_id']}` | `{r['seed_frame_csv_line1']}` | `{intervals_str}` | Tier {r['evaluation']['difficulty_tier']} | {r['evaluation']['accuracy_score']:.1f}% | {decision_badge} | {insights_short}... |"
        )
        
    lines.append("")
    lines.append("---")
    lines.append("## 📝 Chi Tiết Từng Mẫu Kiểm Thử")
    lines.append("")
    
    for r in records:
        lines.append(f"### Mẫu `{r['sample_id']}` ({r['target_video_id']})")
        lines.append(f"- **Query:** {r['query_text']}")
        lines.append(f"- **Dòng 1 CSV:** Video `{r['target_video_id']}`, Seed Frame `{r['seed_frame_csv_line1']}`")
        lines.append(f"- **Intervals:** {json.dumps(r['extracted_intervals'], ensure_ascii=False)}")
        lines.append(f"- **Đánh giá:** Tier {r['evaluation']['difficulty_tier']} / 5 | Độ chính xác: {r['evaluation']['accuracy_score']:.1f}% | Quyết định: **{r['learning_decision']}**")
        lines.append(f"- **Phân tích Vị từ / Độ chính xác:** {r['evaluation']['accuracy_analysis']}")
        lines.append(f"- **Phân tích Module:**")
        lines.append(f"  - `MOD-VIS`: {r['evaluation']['difficulty_breakdown']['MOD-VIS']}")
        lines.append(f"  - `MOD-AUD`: {r['evaluation']['difficulty_breakdown']['MOD-AUD']}")
        lines.append(f"  - `MOD-OCR`: {r['evaluation']['difficulty_breakdown']['MOD-OCR']}")
        lines.append(f"  - `MOD-WORD`: {r['evaluation']['difficulty_breakdown']['MOD-WORD']}")
        lines.append(f"  - `MOD-FLOW`: {r['evaluation']['difficulty_breakdown']['MOD-FLOW']}")
        if r.get("distilled_insights"):
            lines.append(f"- **Bài học chắt lọc:** {r['distilled_insights']}")
        lines.append("")
        
    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    args = parse_args()
    query_path = Path(args.query_file).resolve()
    answer_path = Path(args.answer_file).resolve()
    log_path = Path(args.log_file).resolve()
    report_path = Path(args.report_file).resolve()
    
    query_text = query_path.read_text(encoding="utf-8").strip()
    video_id, seed_frame = read_line_1_only(answer_path)
    intervals = json.loads(args.intervals_json)
    
    is_learned = (args.difficulty_tier >= 3) and (args.accuracy_score >= 85.0)
    learning_decision = "LEARNED" if is_learned else "REJECTED"
    
    sample_id = query_path.stem
    record = {
        "sample_id": sample_id,
        "evaluated_at_utc": datetime.now(timezone.utc).isoformat(),
        "query_file": str(query_path),
        "answer_file": str(answer_path),
        "query_text": query_text,
        "target_video_id": video_id,
        "seed_frame_csv_line1": seed_frame,
        "extracted_intervals": intervals,
        "evaluation": {
            "difficulty_tier": args.difficulty_tier,
            "difficulty_breakdown": {
                "MOD-VIS": args.mod_vis,
                "MOD-AUD": args.mod_aud,
                "MOD-OCR": args.mod_ocr,
                "MOD-WORD": args.mod_word,
                "MOD-FLOW": args.mod_flow,
            },
            "accuracy_score": args.accuracy_score,
            "accuracy_analysis": args.accuracy_analysis,
        },
        "learning_decision": learning_decision,
        "distilled_insights": args.distilled_insights if is_learned else "Rejected due to Tier < 3 or Accuracy < 85%",
    }
    
    log_path.parent.mkdir(parents=True, exist_ok=True)
    all_records: list[dict] = []
    if log_path.is_file():
        try:
            all_records = json.loads(log_path.read_text(encoding="utf-8"))
            if not isinstance(all_records, list):
                all_records = []
        except Exception:
            all_records = []
            
    # Update existing record or append new
    all_records = [r for r in all_records if r.get("sample_id") != sample_id]
    all_records.append(record)
    
    log_path.write_text(json.dumps(all_records, ensure_ascii=False, indent=2), encoding="utf-8")
    update_markdown_report(report_path, all_records)
    
    print(json.dumps({
        "sample_id": sample_id,
        "target_video_id": video_id,
        "seed_frame_line1": seed_frame,
        "difficulty_tier": args.difficulty_tier,
        "accuracy_score": args.accuracy_score,
        "learning_decision": learning_decision,
        "log_path": str(log_path),
        "report_path": str(report_path),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
