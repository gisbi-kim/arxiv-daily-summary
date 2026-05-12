#!/usr/bin/env python3
"""Build homepage daily /new counts from repo-local briefing metadata only.

This intentionally does not fetch arXiv.  The chart on index.html is a view of
the data that was already collected for this repository.  Counts are extracted
from saved daily trend notes and generation scripts that explicitly recorded
the daily /new batch as "cs.CV N + cs.RO M".

Weekend reports that reused a previous Friday batch are skipped so the date
chart does not pretend that a stale Friday listing was a Sunday submission
volume.  The homepage renders the `daily` rows as a date-by-date time series.
"""
from __future__ import annotations

import datetime as dt
import io
import json
import os
import re
import sys
from pathlib import Path


if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


DATE_RE = re.compile(r"(20\d{2}-\d{2}-\d{2}|20\d{6})")
COUNT_PATTERNS = [
    re.compile(r"cs\.CV\s+(\d+)\s*(?:편)?\s*(?:new\+cross)?\s*\+\s*cs\.RO\s+(\d+)", re.I),
    re.compile(r"cs\.CV/new\s+(\d+)\s*편\s*\+\s*cs\.RO/new\s+(\d+)", re.I),
]
STALE_MARKERS = (
    "same Friday",
    "Friday 5/1 listing",
    "금요일 배치",
)


def normalize_date(raw: str) -> str | None:
    raw = raw.strip()
    if re.fullmatch(r"20\d{6}", raw):
        return f"{raw[:4]}-{raw[4:6]}-{raw[6:]}"
    if re.fullmatch(r"20\d{2}-\d{2}-\d{2}", raw):
        return raw
    return None


def date_from_path(path: Path) -> str | None:
    match = DATE_RE.search(path.name)
    return normalize_date(match.group(1)) if match else None


def is_weekend(date: str) -> bool:
    return dt.date.fromisoformat(date).weekday() >= 5


def find_counts(text: str):
    for pattern in COUNT_PATTERNS:
        match = pattern.search(text)
        if match:
            return int(match.group(1)), int(match.group(2))
    return None


def is_stale_reused_batch(text: str) -> bool:
    return any(marker in text for marker in STALE_MARKERS)


def confidence_for(text: str) -> str:
    lowered = text.lower()
    if "new+cross" in lowered or "cross 포함" in text:
        return "new+cross"
    if "/new" in lowered:
        return "raw /new"
    return "saved metadata"


def collect_from_trends(root: Path):
    entries = {}
    for path in sorted((root / "trends").glob("20*.json")):
        date = date_from_path(path)
        if not date:
            continue
        if is_weekend(date):
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        structured = payload.get("daily_new_counts")
        if isinstance(structured, dict) and "cv" in structured and "ro" in structured:
            entries[date] = {
                "date": date,
                "cv": int(structured.get("cv") or 0),
                "ro": int(structured.get("ro") or 0),
                "scope": str(structured.get("scope") or "new+cross"),
                "source": path.relative_to(root).as_posix(),
            }
            continue
        note = str((payload.get("totals") or {}).get("note") or "")
        if not note or is_stale_reused_batch(note):
            continue
        counts = find_counts(note)
        if not counts:
            continue
        cv, ro = counts
        entries[date] = {
            "date": date,
            "cv": cv,
            "ro": ro,
            "scope": confidence_for(note),
            "source": path.relative_to(root).as_posix(),
        }
    return entries


def collect_from_scripts(root: Path):
    entries = {}
    for path in sorted((root / "scripts").glob("gen_html_20*.py")):
        date = date_from_path(path)
        if not date:
            continue
        if is_weekend(date):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if is_stale_reused_batch(text):
            continue
        # Prefer the explicit "오늘 /new" line when present.
        lines = [line for line in text.splitlines() if "오늘 /new" in line or "오늘 배치" in line]
        for line in lines:
            counts = find_counts(line)
            if not counts:
                continue
            cv, ro = counts
            entries[date] = {
                "date": date,
                "cv": cv,
                "ro": ro,
                "scope": confidence_for(line),
                "source": path.relative_to(root).as_posix(),
            }
            break
    return entries


def build(root: Path):
    # Trends are the committed daily snapshots, so they win over older scripts
    # when both have a count for the same date.
    entries = collect_from_scripts(root)
    entries.update(collect_from_trends(root))

    daily = []
    for date, row in sorted(entries.items()):
        weekday = dt.date.fromisoformat(date).strftime("%a")
        out = dict(row)
        out["weekday"] = weekday
        daily.append(out)

    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "source": "repo-local saved daily /new metadata only; no external arXiv fetch",
        "note": (
            "Counts include cross-listed /new entries when the saved report metadata "
            "recorded them as new+cross. Replacement/update-only entries are not used. "
            "Weekend reports that reused a prior Friday batch are skipped."
        ),
        "windows": [
            {"label": "1개월", "days": 31},
            {"label": "3개월", "days": 92},
            {"label": "6개월", "days": 183},
            {"label": "1년", "days": 366},
            {"label": "2년", "days": 731},
            {"label": "3년", "days": 1096},
        ],
        "daily": daily,
    }


def main() -> int:
    root = Path.cwd()
    output = root / "stats" / "weekday_counts.json"
    payload = build(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {output}: {len(payload['daily'])} repo-local daily count rows")
    for row in payload["daily"]:
        print(f"  {row['date']} {row['weekday']}  CV={row['cv']}  RO={row['ro']}  ({row['scope']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
