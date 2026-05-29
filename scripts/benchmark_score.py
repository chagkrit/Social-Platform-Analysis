#!/usr/bin/env python3
"""Deterministic healthcare social media benchmark scorer.

Input is a CSV with one row per platform/period summary. The script computes
standard KPIs, platform-level weighted scores, confidence grades, and JSON or
Markdown executive output. It uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from statistics import mean, pstdev
from typing import Any


DEFAULT_WEIGHTS = {
    "engagement_efficiency": 25.0,
    "engagement_quality": 20.0,
    "follower_growth_strength": 15.0,
    "growth_sustainability": 13.0,
    "reach_power": 10.0,
    "content_consistency": 10.0,
    "strategic_value": 5.0,
    "stability_control": 2.0,
}

NUMERIC_COLUMNS = {
    "posts",
    "followers_start",
    "followers_end",
    "reach",
    "impressions",
    "likes",
    "comments",
    "shares",
    "saves",
    "clicks",
    "video_views",
    "earned_mentions",
    "earned_reach",
    "paid_reach",
    "organic_reach",
    "strategic_value",
}


def to_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip().replace(",", "")
    if text.lower() in {"", "na", "n/a", "nan", "null", "none", "."}:
        return None
    try:
        parsed = float(text)
    except ValueError:
        return None
    if math.isnan(parsed) or math.isinf(parsed):
        return None
    return parsed


def safe_div(num: float | None, den: float | None) -> float | None:
    if num is None or den in {None, 0}:
        return None
    return num / den


def read_csv(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise SystemExit("CSV must have a header row.")
        rows = []
        for raw in reader:
            row: dict[str, Any] = {}
            for key, value in raw.items():
                normalized = key.strip()
                if normalized in NUMERIC_COLUMNS:
                    row[normalized] = to_float(value)
                else:
                    row[normalized] = "" if value is None else str(value).strip()
            rows.append(row)
    if not rows:
        raise SystemExit("CSV has no data rows.")
    if "platform" not in rows[0]:
        raise SystemExit("CSV must include a `platform` column.")
    return rows


def minmax_score(value: float | None, values: list[float]) -> float | None:
    if value is None or not values:
        return None
    lo, hi = min(values), max(values)
    if hi == lo:
        return 3.0
    return 1.0 + 4.0 * ((value - lo) / (hi - lo))


def clamp_score(value: float | None, default: float = 3.0) -> float:
    if value is None:
        return default
    return max(1.0, min(5.0, value))


def confidence(row: dict[str, Any]) -> tuple[str, list[str]]:
    missing = []
    if row.get("reach") is None and row.get("impressions") is None:
        missing.append("no reach/impressions denominator")
    if row.get("followers_start") is None or row.get("followers_end") is None:
        missing.append("missing follower start/end")
    if row.get("posts") in {None, 0}:
        missing.append("missing post count")
    if row.get("paid_reach") is None and row.get("organic_reach") is None:
        missing.append("no paid/organic split")
    if len(missing) <= 1:
        return "high", missing
    if len(missing) <= 3:
        return "medium", missing
    return "low", missing


def build_metrics(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for row in rows:
        likes = row.get("likes") or 0.0
        comments = row.get("comments") or 0.0
        shares = row.get("shares") or 0.0
        saves = row.get("saves") or 0.0
        clicks = row.get("clicks") or 0.0
        total_engagement = likes + comments + shares + saves + clicks
        reach = row.get("reach")
        followers_end = row.get("followers_end")
        followers_start = row.get("followers_start")
        earned_reach = row.get("earned_reach")
        posts = row.get("posts")
        conf, conf_notes = confidence(row)
        metrics = dict(row)
        metrics.update(
            {
                "total_engagement": total_engagement,
                "engagement_rate_by_reach": safe_div(total_engagement, reach),
                "engagement_rate_by_followers": safe_div(total_engagement, followers_end),
                "amplification_rate": safe_div(shares, reach),
                "save_share_quality_ratio": safe_div(saves + shares, total_engagement),
                "comment_depth_ratio": safe_div(comments, total_engagement),
                "follower_growth_rate": safe_div(
                    (followers_end - followers_start) if followers_end is not None and followers_start is not None else None,
                    followers_start,
                ),
                "engagement_per_post": safe_div(total_engagement, posts),
                "reach_per_post": safe_div(reach, posts),
                "earned_amplification_ratio": safe_div(earned_reach, reach),
                "earned_mention_rate": safe_div(row.get("earned_mentions"), posts),
                "confidence": conf,
                "confidence_notes": conf_notes,
            }
        )
        output.append(metrics)
    return output


def collect(metrics: list[dict[str, Any]], key: str) -> list[float]:
    return [float(row[key]) for row in metrics if row.get(key) is not None]


def score_rows(metrics: list[dict[str, Any]], weights: dict[str, float]) -> list[dict[str, Any]]:
    values = {
        "engagement_quality": collect(metrics, "save_share_quality_ratio"),
        "growth_sustainability": collect(metrics, "follower_growth_rate"),
        "engagement_efficiency": collect(metrics, "engagement_rate_by_reach")
        or collect(metrics, "engagement_rate_by_followers"),
        "follower_growth_strength": collect(metrics, "follower_growth_rate"),
        "reach_power": collect(metrics, "reach") or collect(metrics, "impressions"),
        "content_consistency": collect(metrics, "posts"),
        "stability_control": collect(metrics, "engagement_per_post"),
        "strategic_value": collect(metrics, "strategic_value"),
    }

    scored = []
    for row in metrics:
        dimension_scores = {
            "engagement_quality": minmax_score(row.get("save_share_quality_ratio"), values["engagement_quality"]),
            "growth_sustainability": minmax_score(row.get("follower_growth_rate"), values["growth_sustainability"]),
            "engagement_efficiency": minmax_score(
                row.get("engagement_rate_by_reach") if row.get("engagement_rate_by_reach") is not None else row.get("engagement_rate_by_followers"),
                values["engagement_efficiency"],
            ),
            "follower_growth_strength": minmax_score(row.get("follower_growth_rate"), values["follower_growth_strength"]),
            "reach_power": minmax_score(row.get("reach") if row.get("reach") is not None else row.get("impressions"), values["reach_power"]),
            "content_consistency": minmax_score(row.get("posts"), values["content_consistency"]),
            "stability_control": stability_score(row.get("engagement_per_post"), values["stability_control"]),
            "strategic_value": clamp_score(row.get("strategic_value"), 3.0),
        }
        weighted = 0.0
        weight_sum = 0.0
        for dimension, weight in weights.items():
            weighted += clamp_score(dimension_scores.get(dimension)) * weight
            weight_sum += weight
        final_score = weighted / weight_sum if weight_sum else None
        scored_row = dict(row)
        scored_row["dimension_scores"] = dimension_scores
        scored_row["weighted_score"] = final_score
        scored.append(scored_row)
    return sorted(scored, key=lambda item: (item.get("weighted_score") or 0), reverse=True)


def stability_score(value: float | None, values: list[float]) -> float | None:
    if value is None or len(values) < 2:
        return None
    avg = mean(values)
    sd = pstdev(values)
    if avg == 0:
        return 3.0
    z = abs((value - avg) / (sd or 1.0))
    return 5.0 if z <= 0.5 else 4.0 if z <= 1.0 else 3.0 if z <= 1.5 else 2.0 if z <= 2.0 else 1.0


def parse_weights(text: str | None) -> dict[str, float]:
    weights = dict(DEFAULT_WEIGHTS)
    if not text:
        return weights
    for part in text.split(","):
        if not part.strip():
            continue
        key, _, value = part.partition("=")
        if not key or not value:
            raise SystemExit(f"Invalid weight item: {part}")
        key = key.strip()
        if key not in weights:
            raise SystemExit(f"Unknown weight key: {key}")
        weights[key] = float(value)
    return weights


def round_value(value: Any, digits: int) -> Any:
    if isinstance(value, float):
        return None if math.isnan(value) or math.isinf(value) else round(value, digits)
    if isinstance(value, dict):
        return {key: round_value(val, digits) for key, val in value.items()}
    if isinstance(value, list):
        return [round_value(item, digits) for item in value]
    return value


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    rows = read_csv(Path(args.input))
    weights = parse_weights(args.weights)
    metrics = build_metrics(rows)
    scored = score_rows(metrics, weights)
    limitations = sorted({note for row in scored for note in row.get("confidence_notes", [])})
    return round_value(
        {
            "metadata": {
                "input": args.input,
                "organization": args.organization,
                "rows": len(rows),
                "weights": weights,
                "notes": [
                    "Scores are min-max normalized within the provided dataset.",
                    "Weighted scores are decision support and must be interpreted with data confidence.",
                    "Missing reach/impressions lowers confidence in engagement efficiency.",
                ],
            },
            "data_limitations": limitations,
            "platforms": scored,
            "top_platform": scored[0]["platform"] if scored else None,
        },
        args.digits,
    )


def markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Healthcare Social Benchmark Report",
        "",
        f"- Organization: {report['metadata'].get('organization') or ''}",
        f"- Input: `{report['metadata']['input']}`",
        f"- Rows analyzed: {report['metadata']['rows']}",
        f"- Top platform: {report.get('top_platform') or ''}",
        "",
        "## Data Limitations",
        "",
    ]
    if report["data_limitations"]:
        for item in report["data_limitations"]:
            lines.append(f"- {item}")
    else:
        lines.append("- No major denominator limitations detected from required fields.")
    lines.extend(
        [
            "",
            "## Weighted Scoring",
            "",
            "| Platform | Score | Confidence | Engagement by reach | Growth | Reach | Main limitation |",
            "|---|---:|---|---:|---:|---:|---|",
        ]
    )
    for row in report["platforms"]:
        notes = "; ".join(row.get("confidence_notes", []))
        lines.append(
            f"| {row.get('platform')} | {row.get('weighted_score')} | {row.get('confidence')} | "
            f"{row.get('engagement_rate_by_reach') or ''} | {row.get('follower_growth_rate') or ''} | "
            f"{row.get('reach') or row.get('impressions') or ''} | {notes} |"
        )
    lines.extend(["", "## Executive Interpretation Guardrails", ""])
    for note in report["metadata"]["notes"]:
        lines.append(f"- {note}")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Deterministic healthcare social benchmark scoring.")
    parser.add_argument("--input", required=True, help="Input CSV.")
    parser.add_argument("--organization", help="Organization name.")
    parser.add_argument("--weights", help="Comma-separated weight overrides, e.g. engagement_quality=25,reach_power=5")
    parser.add_argument("--json-out", help="Write JSON report.")
    parser.add_argument("--md-out", help="Write Markdown report.")
    parser.add_argument("--digits", type=int, default=5)
    args = parser.parse_args()

    report = build_report(args)
    json_text = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.json_out:
        Path(args.json_out).write_text(json_text, encoding="utf-8")
    if args.md_out:
        Path(args.md_out).write_text(markdown(report), encoding="utf-8")
    if not args.json_out and not args.md_out:
        print(json_text, end="")


if __name__ == "__main__":
    main()
