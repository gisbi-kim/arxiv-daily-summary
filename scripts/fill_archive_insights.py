#!/usr/bin/env python3
"""Backfill archive insight cards so the homepage can summarize old posts."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "posts"
INSIGHTS = ROOT / "insights"


def clean(text: str) -> str:
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    return re.sub(r"\s+", " ", text).strip()


def add_insight_class(source: str) -> tuple[str, int]:
    """Add class insight to cards inside the daily insight section."""
    marker = re.search(r"<h2[^>]*>.*?오늘의 인사이트.*?</h2>", source, re.S)
    if not marker:
        return source, 0
    start = marker.end()
    next_h2 = re.search(r"<h2[^>]*>", source[start:], re.S)
    end = start + next_h2.start() if next_h2 else len(source)
    block = source[start:end]
    new_block, count = re.subn(r"<div class='card'(?![^>]*\binsight\b)", "<div class='card insight'", block)
    if count == 0:
        new_block, count = re.subn(r'<div class="card"(?![^>]*\binsight\b)', '<div class="card insight"', block)
    if count:
        return source[:start] + new_block + source[end:], count
    return source, 0


def cluster_rows(source: str) -> list[dict[str, str]]:
    rows = []
    table_match = re.search(r"<table class='cluster-table'.*?</table>", source, re.S)
    if not table_match:
        return rows
    for row in re.findall(r"<tr>(.*?)</tr>", table_match.group(0), re.S):
        cells = re.findall(r"<td>(.*?)</td>", row, re.S)
        if len(cells) < 3:
            continue
        title = clean(cells[0])
        # Drop tag text from titles when present.
        title = re.split(r"\s*\[[^\]]+\]", title)[0].strip()
        why = clean(cells[2])
        links = re.findall(r'href="(https://arxiv\.org/abs/[0-9.]+)"', cells[1])
        if title and why:
            rows.append({"title": title, "claim": why, "papers": links[:4]})
    return rows


def insight_section(rows: list[dict[str, str]]) -> str:
    cards = ["\n<h2>💡 오늘의 인사이트</h2>"]
    for row in rows[:3]:
        refs = " · ".join(f'<a href="{p}" target="_blank" rel="noopener">{p.rsplit("/", 1)[-1]}</a>' for p in row["papers"])
        refs_html = f"<p class='small'>{refs}</p>" if refs else ""
        cards.append(
            "<div class='card insight'>"
            f"<h3>{html.escape(row['title'], quote=False)}</h3>"
            f"<p>{html.escape(row['claim'], quote=False)}</p>"
            f"{refs_html}</div>"
        )
    return "\n".join(cards) + "\n"


def insert_missing_section(source: str, rows: list[dict[str, str]]) -> tuple[str, bool]:
    if "오늘의 인사이트" in source or not rows:
        return source, False
    section = insight_section(rows)
    # Prefer inserting after the cluster table, before weekly trends.
    cluster = re.search(r"(<h2[^>]*>.*?오늘의 클러스터 지도.*?</h2>.*?</table>)", source, re.S)
    if cluster:
        return source[: cluster.end()] + section + source[cluster.end():], True
    thesis = re.search(r"</div>\s*(?=\n<h2)", source)
    if thesis:
        return source[: thesis.end()] + section + source[thesis.end():], True
    return source, False


def write_insights_json(date: str, rows: list[dict[str, str]]) -> bool:
    path = INSIGHTS / f"{date}.json"
    if path.exists() or not rows:
        return False
    payload = {
        "date": date,
        "insights": rows[:3],
        "research_topics": [
            {
                "title": f"{row['title']} 후속 확인",
                "claim": "원본 parser snapshot이 repo에 남아 있지 않은 초기 발행분이라, 대표 논문별 입력 조건, 평가셋, 실패 사례, ablation 유무를 먼저 비교표로 정리하는 것이 좋습니다.",
            }
            for row in rows[:3]
        ],
        "backfill_note": "Generated from the committed cluster table because the original insights JSON was not present in the repository.",
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return True


def main() -> int:
    changed_posts = 0
    changed_json = 0
    for path in sorted(POSTS.glob("2026-??-??.html")):
        source = path.read_text(encoding="utf-8", errors="replace")
        updated, class_count = add_insight_class(source)
        rows = cluster_rows(updated)
        updated, inserted = insert_missing_section(updated, rows)
        if updated != source:
            path.write_text(updated, encoding="utf-8", newline="\n")
            changed_posts += 1
            print(f"updated {path.relative_to(ROOT)} class_count={class_count} inserted={inserted}")
        if write_insights_json(path.stem, rows):
            changed_json += 1
            print(f"wrote insights/{path.stem}.json")
    print(f"changed_posts={changed_posts} changed_json={changed_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
