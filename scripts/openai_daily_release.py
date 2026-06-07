#!/usr/bin/env python3
"""OpenAI-based arXiv Daily Summary release runner.

This runner intentionally does not depend on Claude Code. It uses the existing
stdlib arXiv parsers in this repository, calls the OpenAI API for editorial
judgment, writes HTML/JSON artifacts, and prepares a Slack message file for the
GitHub Actions workflow.
"""
from __future__ import annotations

import argparse
import calendar
import datetime as dt
import html
import json
import os
import re
import subprocess
import sys
import textwrap
import urllib.request
from pathlib import Path
from typing import Any

KST = dt.timezone(dt.timedelta(hours=9))
SITE_URL = os.environ.get("SITE_URL", "https://gisbi-kim.github.io/arxiv-daily-summary")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4.1")
REPO_ROOT = Path(__file__).resolve().parents[1]
OUT = REPO_ROOT / "out"

BUCKET_ORDER = [
    "3D/Scene",
    "Robot Learning",
    "Autonomous Driving",
    "Foundation Models",
    "Generation",
    "Efficiency/Systems",
    "Embodied AI",
    "Safety/Alignment",
]

CSS = """
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:#f6f8fa;color:#24292f;margin:0;padding:28px 12px;line-height:1.62}
.container{max-width:980px;margin:0 auto;background:#fff;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.06),0 1px 2px rgba(0,0,0,.04);padding:40px 48px}
h1{font-size:28px;margin:0 0 6px;color:#0d1117}h2{font-size:21px;margin:40px 0 14px;padding-bottom:8px;border-bottom:2px solid #e5e7eb}h3{font-size:16px;margin:14px 0 6px}h4.bucket{font-size:18px;margin:32px 0 10px;padding-top:14px;border-top:2px solid #e5e7eb;color:#0f172a}.count{font-size:13px;font-weight:400;color:#656d76}
a{color:#0969da;text-decoration:none}a:hover{text-decoration:underline}.home{display:inline-block;padding:6px 14px;font-size:13px;color:#0969da;background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;margin:0 0 18px}
.meta{font-size:13px;color:#3b434d;padding:14px 18px;background:#f6f8fa;border-left:3px solid #0969da;border-radius:6px;margin:14px 0 22px}.thesis{background:#0f172a;color:#f8fafc;border-radius:10px;padding:18px 22px;margin:16px 0 28px;font-size:16px}.thesis strong{color:#fef08a}
.cluster-table{width:100%;border-collapse:collapse;font-size:13px;margin:12px 0 18px}.cluster-table th,.cluster-table td{border:1px solid #d0d7de;padding:9px;vertical-align:top}.cluster-table th{background:#f6f8fa;color:#0d1117}
.card,.mini-paper{background:#fafbfc;border:1px solid #e5e7eb;border-radius:8px;padding:14px 18px;margin:12px 0}.mini-paper{background:#fff}.topic{border-left:4px solid #22c55e;background:#f0fdf4}.insight{border-left:4px solid #0969da;background:#f8fafc}
.bucket-line{font-family:ui-monospace,SFMono-Regular,Consolas,Menlo,monospace;background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;padding:10px 14px;font-size:13px;white-space:pre-wrap;overflow-x:auto}
.badge{display:inline-block;font-size:11px;font-weight:600;padding:1px 8px;border-radius:10px;margin-left:6px;vertical-align:middle;font-family:ui-monospace,monospace}.cv{background:#ddf4ff;color:#0550ae;border:1px solid #54aeff}.ro{background:#fff8c5;color:#7a4e00;border:1px solid #d4a72c}.cvro{background:#ffe5d9;color:#9a3412;border:1px solid #f59e0b}.x{background:#f3f4f6;color:#6b7280;border:1px solid #d1d5db}
.tag{display:inline-block;font-family:ui-monospace,SFMono-Regular,Consolas,Menlo,monospace;font-size:12px;color:#7c2d12;background:#fff7ed;border:1px solid #fed7aa;border-radius:6px;padding:1px 7px;margin:2px 3px 2px 0}.authors,.small{color:#475569;font-size:13.5px}footer{margin-top:40px;padding-top:16px;border-top:1px solid #eaeef2;font-size:12px;color:#656d76;text-align:center}
@media(max-width:760px){body{padding:16px 8px}.container{padding:24px 20px}.cluster-table{font-size:12.5px}}
""".strip()


def log(msg: str) -> None:
    print(f"[openai_daily_release] {msg}", flush=True)


def run(cmd: list[str], stdout_path: Path | None = None) -> None:
    log("$ " + " ".join(cmd))
    if stdout_path is None:
        subprocess.run(cmd, cwd=REPO_ROOT, check=True)
    else:
        stdout_path.parent.mkdir(parents=True, exist_ok=True)
        with stdout_path.open("w", encoding="utf-8", newline="\n") as f:
            subprocess.run(cmd, cwd=REPO_ROOT, check=True, stdout=f)


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "arxiv-daily-summary openai runner"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")


def strip_tags(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def parse_arxiv_listing_date() -> str:
    dates: list[dt.date] = []
    for cat in ["cs.CV", "cs.RO"]:
        raw = fetch_text(f"https://arxiv.org/list/{cat}/new")
        h3s = re.findall(r"<h3[^>]*>(.*?)</h3>", raw, re.S | re.I)
        if not h3s:
            raise RuntimeError(f"cannot find /new h3 listing date for {cat}")
        text = strip_tags(h3s[0])
        # Examples include dates like "Mon, 8 Jun 2026".
        m = re.search(r"(Mon|Tue|Wed|Thu|Fri|Sat|Sun),\s+(\d{1,2})\s+([A-Za-z]{3})\s+(\d{4})", text)
        if not m:
            raise RuntimeError(f"cannot parse listing date for {cat}: {text}")
        day = int(m.group(2))
        mon = list(calendar.month_abbr).index(m.group(3))
        year = int(m.group(4))
        dates.append(dt.date(year, mon, day))
    if dates[0] != dates[1]:
        raise RuntimeError(f"cs.CV and cs.RO listing dates differ: {dates}")
    return dates[0].isoformat()


def is_weekend(date_str: str) -> bool:
    return dt.date.fromisoformat(date_str).weekday() >= 5


def resolve_mode(requested_mode: str, target_date: str | None) -> tuple[str, str, str]:
    today = dt.datetime.now(tz=KST).date().isoformat()
    listing_date = parse_arxiv_listing_date()
    mode = requested_mode or "auto"
    if mode == "auto":
        post_date = target_date or listing_date
        if is_weekend(today) and not target_date:
            return "sunday", post_date, listing_date
        if post_date < listing_date:
            return "backfill", post_date, listing_date
        return "daily", post_date, listing_date
    if mode in {"daily", "backfill", "weekly", "sunday"}:
        return mode, target_date or listing_date, listing_date
    raise ValueError(f"unknown mode: {mode}")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def badge_class(badge: str) -> str:
    if badge == "CV/RO":
        return "cvro"
    if badge == "RO":
        return "ro"
    if badge == "CV":
        return "cv"
    return "x"


def paper_link(p: dict[str, Any]) -> str:
    title = html.escape(p.get("title") or p.get("arxiv_id", "paper"))
    arxiv_id = html.escape(p.get("arxiv_id", ""))
    badge = html.escape(p.get("badge", "?"))
    cls = badge_class(badge)
    return f'<a href="https://arxiv.org/abs/{arxiv_id}" target="_blank" rel="noopener">{title}</a> <span class="badge {cls}">{badge}</span>'


def compact_papers(classified: dict[str, Any], max_papers: int = 100) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for bucket in BUCKET_ORDER:
        for p in classified.get("buckets", {}).get(bucket, {}).get("papers", [])[:18]:
            rows.append({
                "arxiv_id": p.get("arxiv_id"),
                "title": p.get("title"),
                "abstract": (p.get("abstract") or "")[:1000],
                "subjects": p.get("subjects"),
                "bucket": bucket,
                "badge": p.get("badge"),
                "primary_cat": p.get("primary_cat"),
            })
            if len(rows) >= max_papers:
                return rows
    return rows


def fallback_brief(classified: dict[str, Any], date_str: str) -> dict[str, Any]:
    candidates = compact_papers(classified, 40)
    clusters = []
    for bucket in BUCKET_ORDER[:5]:
        papers = classified.get("buckets", {}).get(bucket, {}).get("papers", [])[:3]
        if papers:
            clusters.append({
                "cluster": f"{bucket} 쪽 신호",
                "representative_ids": [p["arxiv_id"] for p in papers],
                "why": f"{bucket} 버킷에서 관련 논문이 여러 편 잡혔습니다. 자동 fallback이라 세부 해석은 다음 실행에서 보강이 필요합니다.",
                "confidence": "Medium",
                "confidence_note": "keyword bucket 기반 fallback",
                "lab_action": "대표 논문 abstract를 확인하고 APRL 실험 축으로 재분류",
                "tags": ["[자동생성]", "[점검필요]"],
            })
    return {
        "thesis": f"{date_str} 배치는 자동 분류 기준으로 {classified.get('selected', 0)}편의 ROI 논문이 잡혔습니다. OpenAI 응답 파싱 실패로 fallback 리포트를 생성했습니다.",
        "clusters": clusters,
        "insights": ["OpenAI 응답 파싱 실패로 fallback 생성", "버킷 카운트와 대표 논문은 parser/classifier 결과를 사용"],
        "recommended_topics": ["OpenAI JSON 응답 안정화", "parser 결과 기반 cluster 재검토"],
        "slack_message": f"arXiv Daily Briefing - {date_str}\nFallback report generated. Full report: {SITE_URL}/posts/{date_str}.html",
    }


def call_openai(classified: dict[str, Any], date_str: str, source_mode: str, listing_date: str) -> dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing")
    payload = {
        "date": date_str,
        "source_mode": source_mode,
        "source_listing_date": listing_date,
        "counts": {
            "total": classified.get("total"),
            "selected": classified.get("selected"),
            "buckets": {b: classified.get("buckets", {}).get(b, {}).get("total", 0) for b in BUCKET_ORDER},
        },
        "papers": compact_papers(classified),
    }
    system = (
        "You are an APRL robotics research briefing editor. "
        "Write in Korean with a smart senior PhD-student briefing tone. "
        "Return valid JSON only. No markdown fences."
    )
    user = {
        "task": "Generate an arXiv daily briefing editorial JSON.",
        "requirements": [
            "Create a 1-2 sentence thesis.",
            "Create 4-6 clusters; each cluster needs 2-4 representative arxiv IDs when possible.",
            "At least one cluster should explicitly cover Geometry/SLAM/Reconstruction if there are relevant 3D/Scene papers.",
            "Use concrete lab actions, not generic follow-up wording.",
            "Return JSON keys: thesis, clusters, insights, recommended_topics, slack_message.",
            "Each cluster object keys: cluster, representative_ids, why, confidence, confidence_note, lab_action, tags.",
            "tags should be short Korean bracket labels such as [평가축], [방법전환], [실사용전환], [경고신호].",
        ],
        "data": payload,
    }
    req_body = json.dumps({
        "model": OPENAI_MODEL,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(user, ensure_ascii=False)},
        ],
    }, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=req_body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        raw = json.loads(r.read().decode("utf-8"))
    content = raw["choices"][0]["message"]["content"]
    return json.loads(content)


def build_lookup(classified: dict[str, Any]) -> dict[str, dict[str, Any]]:
    lookup = {}
    for bucket in BUCKET_ORDER:
        for p in classified.get("buckets", {}).get(bucket, {}).get("papers", []):
            lookup[p["arxiv_id"]] = p
    return lookup


def bucket_counts_text(classified: dict[str, Any]) -> str:
    labels = {
        "3D/Scene": "[3D]",
        "Robot Learning": "[RL]",
        "Autonomous Driving": "[AD]",
        "Foundation Models": "[FM]",
        "Generation": "[Gen]",
        "Efficiency/Systems": "[Eff]",
        "Embodied AI": "[Emb]",
        "Safety/Alignment": "[Safety]",
    }
    return " · ".join(f"{labels[b]} {classified.get('buckets', {}).get(b, {}).get('total', 0)}" for b in BUCKET_ORDER)


def build_html(date_str: str, classified: dict[str, Any], brief: dict[str, Any], source_mode: str, listing_date: str) -> str:
    lookup = build_lookup(classified)
    ymd = dt.date.fromisoformat(date_str)
    dow = ["월", "화", "수", "목", "금", "토", "일"][ymd.weekday()]
    cv_count = len(load_json(OUT / "cv_new.json")) if (OUT / "cv_new.json").exists() else 0
    ro_count = len(load_json(OUT / "ro_new.json")) if (OUT / "ro_new.json").exists() else 0
    rows = []
    for c in brief.get("clusters", [])[:6]:
        ids = c.get("representative_ids", [])[:4]
        reps = "<br>".join(paper_link(lookup[i]) for i in ids if i in lookup) or html.escape(", ".join(ids))
        tags = " ".join(f"<span class='tag'>{html.escape(t)}</span>" for t in c.get("tags", [])[:4])
        rows.append(
            "<tr>"
            f"<td><strong>{html.escape(c.get('cluster',''))}</strong><br>{tags}</td>"
            f"<td>{reps}</td>"
            f"<td>{html.escape(c.get('why',''))}</td>"
            f"<td>{html.escape(c.get('confidence','Medium'))}<br><span class='small'>{html.escape(c.get('confidence_note',''))}</span></td>"
            f"<td>{html.escape(c.get('lab_action',''))}</td>"
            "</tr>"
        )
    insights = "\n".join(f"<li>{html.escape(x)}</li>" for x in brief.get("insights", [])[:6])
    topics = "\n".join(f"<li>{html.escape(x)}</li>" for x in brief.get("recommended_topics", [])[:6])
    papers_by_bucket = []
    for bucket in BUCKET_ORDER:
        papers = classified.get("buckets", {}).get(bucket, {}).get("papers", [])[:12]
        if not papers:
            continue
        items = []
        for p in papers:
            authors = ", ".join(p.get("authors", [])[:4])
            if len(p.get("authors", [])) > 4:
                authors += ", et al."
            abstract = p.get("abstract", "")
            items.append(
                "<div class='mini-paper'>"
                f"<h3>{paper_link(p)}</h3>"
                f"<div class='authors'>{html.escape(authors)}</div>"
                f"<p>{html.escape(abstract[:500])}{'…' if len(abstract) > 500 else ''}</p>"
                f"<div class='small'>{html.escape(p.get('subjects',''))}</div>"
                "</div>"
            )
        papers_by_bucket.append(f"<h4 class='bucket'>{html.escape(bucket)} <span class='count'>{len(papers)} shown</span></h4>" + "\n".join(items))
    now = dt.datetime.now(tz=KST).strftime("%Y-%m-%d %H:%M:%S KST")
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>arXiv Daily Briefing - {date_str}</title>
<style>{CSS}</style>
</head>
<body><main class="container">
<a class="home" href="../index.html">← Home</a>
<h1>arXiv Daily Briefing — {date_str} ({dow})</h1>
<div class="meta">
<div><strong>소스:</strong> arXiv cs.CV + cs.RO · source_listing_date={listing_date} · source_mode={source_mode}</div>
<div><strong>오늘 /new:</strong> cs.CV {cv_count} + cs.RO {ro_count} · {classified.get('total', 0)} dedup · {classified.get('selected', 0)} ROI papers</div>
</div>
<section class="thesis"><strong>오늘의 결론:</strong> {html.escape(brief.get('thesis',''))}</section>
<h2>오늘의 클러스터 지도</h2>
<table class="cluster-table"><thead><tr><th>Cluster</th><th>대표 논문</th><th>왜 중요?</th><th>Confidence</th><th>Lab action</th></tr></thead><tbody>
{''.join(rows)}
</tbody></table>
<h2>주간 동향</h2>
<div class="card insight"><ul>{insights}</ul></div>
<h2>추천 연구주제</h2>
<div class="card topic"><ol>{topics}</ol></div>
<h2>Bucket counts</h2>
<div class="bucket-line">{html.escape(bucket_counts_text(classified))}</div>
<h2>논문 목록</h2>
{''.join(papers_by_bucket)}
<footer>Generated by OpenAI-based GitHub Actions runner · {now}</footer>
</main></body></html>
"""


def update_weekday_stats(date_str: str, cv_count: int, ro_count: int) -> None:
    path = REPO_ROOT / "stats" / "weekday_counts.json"
    payload: dict[str, Any]
    if path.exists():
        try:
            payload = load_json(path)
        except Exception:
            payload = {"items": []}
    else:
        payload = {"items": []}
    items = payload.get("items", [])
    items = [x for x in items if x.get("date") != date_str]
    items.append({"date": date_str, "cv": cv_count, "ro": ro_count})
    items.sort(key=lambda x: x.get("date", ""))
    payload = {"updated_at": dt.datetime.now(tz=KST).isoformat(), "items": items}
    write_json(path, payload)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default=os.environ.get("MODE", "auto"))
    parser.add_argument("--target-date", default=os.environ.get("TARGET_DATE", ""))
    args = parser.parse_args()

    OUT.mkdir(exist_ok=True)
    mode, post_date, listing_date = resolve_mode(args.mode, args.target_date or None)
    log(f"mode={mode} post_date={post_date} listing_date={listing_date}")

    if mode == "sunday":
        msg = f"arXiv Daily Summary: intentional no-op for Sunday/auto mode. Current /new listing date: {listing_date}."
        (OUT / "no_release.txt").write_text(msg + "\n", encoding="utf-8")
        (OUT / "slack_message.txt").write_text(msg + "\n", encoding="utf-8")
        return 0

    post_path = REPO_ROOT / "posts" / f"{post_date}.html"
    if post_path.exists() and mode == "auto":
        msg = f"arXiv Daily Summary: no release needed; posts/{post_date}.html already exists."
        (OUT / "no_release.txt").write_text(msg + "\n", encoding="utf-8")
        (OUT / "slack_message.txt").write_text(msg + "\n", encoding="utf-8")
        return 0

    if mode == "backfill" or post_date < listing_date:
        source_mode = "pastweek-date-section"
        run([sys.executable, "scripts/fetch_arxiv_pastweek_date.py", "cs.CV", post_date], OUT / "cv_new.json")
        run([sys.executable, "scripts/fetch_arxiv_pastweek_date.py", "cs.RO", post_date], OUT / "ro_new.json")
    else:
        source_mode = "new"
        if post_date != listing_date:
            raise RuntimeError(f"daily post_date must match listing_date: {post_date} != {listing_date}")
        run([sys.executable, "scripts/fetch_arxiv.py", "new", "cs.CV"], OUT / "cv_new.json")
        run([sys.executable, "scripts/fetch_arxiv.py", "new", "cs.RO"], OUT / "ro_new.json")

    run([sys.executable, "scripts/fetch_arxiv.py", "pastweek", "cs.CV"], OUT / "cv_pastweek.json")
    run([sys.executable, "scripts/fetch_arxiv.py", "pastweek", "cs.RO"], OUT / "ro_pastweek.json")
    run([sys.executable, "scripts/classify.py"], OUT / "classified.json")

    classified = load_json(OUT / "classified.json")
    cv_count = len(load_json(OUT / "cv_new.json"))
    ro_count = len(load_json(OUT / "ro_new.json"))
    if classified.get("total", 0) < 20:
        raise RuntimeError(f"too few parsed papers: total={classified.get('total')}")

    try:
        brief = call_openai(classified, post_date, source_mode, post_date)
    except Exception as exc:
        log(f"OpenAI generation failed, using fallback: {exc}")
        brief = fallback_brief(classified, post_date)

    trends = {
        "date": post_date,
        "source_listing_date": post_date,
        "source_mode": source_mode,
        "daily_new_counts": {"cv": cv_count, "ro": ro_count, "scope": "new+cross; replacements excluded"},
        "bucket_counts": {b: classified.get("buckets", {}).get(b, {}).get("total", 0) for b in BUCKET_ORDER},
    }
    benchmarks = {
        "date": post_date,
        "total_scanned": classified.get("total", 0),
        "selected": classified.get("selected", 0),
        "selected_ratio": round(classified.get("selected", 0) / max(1, classified.get("total", 0)), 4),
        "model": OPENAI_MODEL,
        "runner": "scripts/openai_daily_release.py",
    }
    insights = {
        "date": post_date,
        "thesis": brief.get("thesis", ""),
        "clusters": brief.get("clusters", []),
        "insights": brief.get("insights", []),
        "recommended_topics": brief.get("recommended_topics", []),
    }
    write_json(REPO_ROOT / "trends" / f"{post_date}.json", trends)
    write_json(REPO_ROOT / "benchmarks" / f"{post_date}.json", benchmarks)
    write_json(REPO_ROOT / "insights" / f"{post_date}.json", insights)
    post_path.parent.mkdir(exist_ok=True)
    post_path.write_text(build_html(post_date, classified, brief, source_mode, post_date), encoding="utf-8", newline="\n")
    update_weekday_stats(post_date, cv_count, ro_count)

    run([sys.executable, "scripts/build_feed.py"])
    run([sys.executable, "scripts/build_feed.py", "--check"])

    slack = brief.get("slack_message") or f"arXiv Daily Briefing - {post_date}\nFull report: {SITE_URL}/posts/{post_date}.html"
    if "Full report" not in slack:
        slack += f"\nFull report: {SITE_URL}/posts/{post_date}.html"
    (OUT / "slack_message.txt").write_text(slack + "\n", encoding="utf-8")
    (OUT / "release_ok.txt").write_text(f"released {post_date}\n", encoding="utf-8")
    log(f"release artifacts written for {post_date}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
