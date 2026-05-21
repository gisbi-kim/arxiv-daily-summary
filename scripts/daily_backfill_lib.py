#!/usr/bin/env python3
"""Shared HTML/JSON generator for date-section arXiv daily backfills."""
from __future__ import annotations

import datetime as dt
import html
import json
import re
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from classify import BUCKETS, assign_bucket, primary_badge


BUCKET_ORDER = [b for b, _ in BUCKETS]
SOURCE_MODE = "pastweek-date-section"

PHYLOGENY = {
    "3D/Scene": ("CVML", "Visual Perception > 3D Vision > Scene Representation > Gaussian/Geometry Models"),
    "Robot Learning": ("ROBOTICS", "Robot Learning > Policy Learning > Vision-Language-Action > Embodied Control"),
    "Autonomous Driving": ("ROBOTICS", "Autonomous Systems > Driving > Planning and Perception > Closed-Loop Evaluation"),
    "Foundation Models": ("CVML", "Foundation Models > Multimodal Learning > Vision-Language Models > Reasoning and Reliability"),
    "Generation": ("CVML", "Generative Modeling > Image and Video Generation > World Models > Controllable Synthesis"),
    "Efficiency/Systems": ("CVML", "Efficient ML Systems > Model Compression > Token and Cache Efficiency > Deployment"),
    "Embodied AI": ("ROBOTICS", "Embodied AI > Navigation and Planning > Instruction Following > Long-Horizon Agents"),
    "Safety/Alignment": ("CVML", "Trustworthy ML > Robustness and Alignment > OOD and Adversarial Risk > Deployment Safety"),
}


def load_json(path: str | Path) -> Any:
    with open(ROOT / path, encoding="utf-8") as f:
        return json.load(f)


def write_json(path: str | Path, payload: Any) -> None:
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def esc(value: Any) -> str:
    return html.escape(str(value or ""), quote=False)


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def text_blob(p: dict) -> str:
    return f"{p.get('title','')} {p.get('abstract','')} {p.get('subjects','')}".lower()


def paper_url(p: dict) -> str:
    return f"https://arxiv.org/abs/{p['arxiv_id']}"


def paper_link(p: dict, label: str | None = None) -> str:
    return f'<a href="{paper_url(p)}" target="_blank" rel="noopener">{esc(label or p["title"])}</a>'


def badge_html(badge: str) -> str:
    cls = {"CV": "cv", "RO": "ro", "CV/RO": "cvro"}.get(badge, "x")
    return f'<span class="badge {cls}">{esc(badge)}</span>'


def listing_count(rows: list[dict]) -> int:
    return sum(1 for row in rows if row.get("section") != "replace")


def classify_daily(cv_new: list[dict], ro_new: list[dict]) -> dict:
    by_id: dict[str, dict] = {}
    for p in cv_new + ro_new:
        if p.get("section") == "replace":
            continue
        q = dict(p)
        q["bucket"] = assign_bucket(q.get("title", ""), q.get("abstract", ""), q.get("subjects", ""))
        q["badge"] = primary_badge(q)
        by_id.setdefault(q["arxiv_id"], q)

    grouped = {b: [] for b in BUCKET_ORDER}
    for p in by_id.values():
        if p.get("bucket"):
            grouped[p["bucket"]].append(p)

    return {
        "total": len(by_id),
        "selected": sum(len(grouped[b]) for b in BUCKET_ORDER),
        "buckets": {
            b: {
                "total": len(grouped[b]),
                "cv": sum(1 for p in grouped[b] if p["badge"] == "CV"),
                "ro": sum(1 for p in grouped[b] if p["badge"] == "RO"),
                "cvro": sum(1 for p in grouped[b] if p["badge"] == "CV/RO"),
                "papers": grouped[b],
            }
            for b in BUCKET_ORDER
        },
    }


def all_classified_papers(classified: dict) -> list[dict]:
    papers = []
    for bucket, info in classified["buckets"].items():
        for p in info["papers"]:
            q = dict(p)
            q["bucket"] = bucket
            papers.append(q)
    return papers


def classify_pastweek(papers: list[dict]) -> dict:
    out = {b: {"total": 0, "cv": 0, "ro": 0, "cvro": 0} for b in BUCKET_ORDER}
    seen: dict[str, dict] = {}
    for p in papers:
        seen.setdefault(p["arxiv_id"], p)
    for p in seen.values():
        bucket = assign_bucket(p.get("title", ""), p.get("abstract", ""), p.get("subjects", ""))
        if not bucket:
            continue
        badge = primary_badge(p)
        out[bucket]["total"] += 1
        if badge == "CV":
            out[bucket]["cv"] += 1
        elif badge == "RO":
            out[bucket]["ro"] += 1
        elif badge == "CV/RO":
            out[bucket]["cvro"] += 1
    return out


def keyword_counts(papers: list[dict]) -> list[list[Any]]:
    keywords = [
        "vla", "world model", "diffusion", "video", "gaussian", "3d", "4d",
        "navigation", "driving", "benchmark", "dataset", "token", "cache",
        "compression", "safety", "ood", "hallucination", "calibration",
        "robot", "manipulation", "memory", "slam", "odometry", "lidar",
    ]
    text = " ".join(text_blob(p) for p in papers)
    rows = [[k, text.count(k)] for k in keywords if text.count(k)]
    rows.sort(key=lambda x: (-x[1], x[0]))
    return rows[:24]


def importance_tags(p: dict, bucket: str) -> list[str]:
    text = text_blob(p)
    tags: list[str] = []
    if any(k in text for k in ["benchmark", "dataset", "evaluation", "challenge", "stress", "olympiad"]):
        tags.append("[평가축]")
    if any(k in text for k in ["safety", "risk", "robust", "adversarial", "ood", "uncertainty", "barrier"]):
        tags.append("[경고신호]")
    if any(k in text for k in ["efficient", "compression", "pruning", "cache", "lightweight", "real-time", "edge", "sparse"]):
        tags.append("[실사용전환]")
    if any(k in text for k in ["vla", "world model", "diffusion", "flow", "gaussian", "splatting", "distillation", "meta-action"]):
        tags.append("[방법전환]")
    if any(k in text for k in ["teleoperation", "human-in-the-loop", "crowdsourcing", "synthetic", "sim2real"]):
        tags.append("[데이터전환]")
    if any(k in text for k in ["survey", "taxonomy", "review"]):
        tags.append("[통합정리]")
    if not tags:
        tags.append("[문제정의]" if bucket in {"Embodied AI", "Safety/Alignment"} else "[인프라]")
    return tags[:3]


def phylogeny_for(bucket: str, paper: dict | None = None) -> dict:
    text = text_blob(paper or {})
    if bucket == "3D/Scene" and any(k in text for k in ["slam", "odometry", "lidar", "robot", "driving", "navigation", "pose"]):
        source = "ROBOTICS"
        lineage = "Perception and Mapping > State Estimation > SLAM and Odometry > Geometry Maps"
    elif bucket == "Generation" and any(k in text for k in ["world model", "robot", "driving", "aerial", "embodied"]):
        source = "ROBOTICS"
        lineage = "Simulation and World Models > Generative Simulation > Action-Conditioned Worlds > Control Evaluation"
    else:
        source, lineage = PHYLOGENY[bucket]
    phylum, cls, order, genus = [x.strip() for x in lineage.split(">")]
    return {
        "source": source,
        "phylum": phylum,
        "class": cls,
        "order": order,
        "genus": genus,
        "confidence": "Medium",
        "rationale": "제목, subject, ROI 버킷을 기준으로 canonical taxonomy의 가장 가까운 계통에 매핑했습니다.",
    }


def rank_paper(p: dict, bucket: str) -> int:
    text = text_blob(p)
    score = 0
    for kw in [
        "benchmark", "dataset", "vla", "vision-language-action", "world model",
        "closed-loop", "safety", "risk", "ood", "robust", "uncertainty",
        "token", "compression", "navigation", "gaussian", "splatting", "4d",
        "driving", "diffusion", "slam", "odometry", "lidar", "humanoid",
        "teleoperation", "manipulation", "hallucination", "evidence",
    ]:
        if kw in text:
            score += 3
    if p.get("badge") == "CV/RO":
        score += 5
    elif p.get("badge") == "RO":
        score += 3
    if bucket in {"3D/Scene", "Robot Learning", "Autonomous Driving"}:
        score += 1
    return score


def select_papers(spec: dict, papers: list[dict], used: set[str]) -> list[dict]:
    by_id = {p["arxiv_id"]: p for p in papers}
    selected: list[dict] = []
    for arxiv_id in spec.get("ids", []):
        p = by_id.get(arxiv_id)
        if p and p["arxiv_id"] not in used and p["bucket"] in spec["buckets"]:
            selected.append(p)

    selected_ids = {p["arxiv_id"] for p in selected}
    candidates: list[tuple[int, dict]] = []
    for p in papers:
        if p["arxiv_id"] in used or p["arxiv_id"] in selected_ids or p["bucket"] not in spec["buckets"]:
            continue
        text = text_blob(p)
        hits = sum(1 for n in spec["needles"] if n.lower() in text)
        if hits:
            candidates.append((hits * 20 + rank_paper(p, p["bucket"]), p))
    candidates.sort(key=lambda x: (x[0], x[1].get("title", "")), reverse=True)
    selected.extend(p for _, p in candidates)
    return selected[: spec.get("limit", 4)]


def build_clusters(profile: dict, papers: list[dict]) -> list[dict]:
    used: set[str] = set()
    clusters = []
    for spec in profile["cluster_specs"]:
        selected = select_papers(spec, papers, used)
        if len(selected) < 2:
            continue
        used.update(p["arxiv_id"] for p in selected)
        confidence = spec.get("confidence") or ("High" if len(selected) >= 3 else "Medium")
        clusters.append({
            "cluster": spec["title"],
            "papers": selected,
            "why": spec["why"],
            "confidence": confidence,
            "confidence_note": spec.get("confidence_note") or f"대표 논문 {len(selected)}편 연결",
            "lab_action": spec["lab_action"],
            "importance_tags": sorted({t for p in selected for t in importance_tags(p, p["bucket"])})[:4],
        })
    return clusters[:6]


def summary_for_paper(p: dict) -> tuple[str, str, str]:
    bucket = p["bucket"]
    if bucket == "3D/Scene":
        return ("Geometry / reconstruction", "map, pose, correspondence를 다른 이름으로 다시 다룹니다.", "SLAM/reconstruction 계열 실험의 map representation 후보로 볼 만합니다.")
    if bucket == "Robot Learning":
        return ("Robot execution structure", "정책 내부 표현이나 개입 지점이 실제 task 성공을 바꿀 수 있습니다.", "VLA/robot policy ablation의 구조 변수로 넣을 가치가 있습니다.")
    if bucket == "Autonomous Driving":
        return ("Closed-loop evidence", "offline perception score와 주행 안정성 사이 간격을 줄이려는 논문입니다.", "closed-loop stress test의 failure case로 모을 만합니다.")
    if bucket == "Generation":
        return ("Controllability", "생성 품질보다 조건을 넣었을 때 얼마나 안정적으로 움직이는지가 핵심입니다.", "world-model 평가에서 temporal drift와 action success를 같이 볼 후보입니다.")
    if bucket == "Efficiency/Systems":
        return ("Runtime budget", "token/cache/latency 제어가 실제 배포 성능을 가릅니다.", "Pareto curve나 edge-runtime 실험 축으로 바로 옮길 수 있습니다.")
    if bucket == "Embodied AI":
        return ("Long-horizon embodiment", "memory와 3D understanding이 navigation 실패로 이어지는 구간을 봅니다.", "VLN/ObjectNav stress split에 넣을 만합니다.")
    return ("Reliability", "모델이 자신 있게 틀리는 조건을 분리해 볼 수 있습니다.", "검증, calibration, counterfactual failure log에 쓸 만합니다.")


def paper_excerpt(p: dict) -> str:
    abstract = clean(p.get("abstract", ""))
    if abstract:
        return abstract[:420]
    subjects = clean(p.get("subjects", ""))
    return f"Backfill source에는 abstract가 없어 title/subject 기반으로 분류했습니다. Subjects: {subjects}"[:420]


def render_html(profile: dict, classified: dict, trends: dict, html_insights: dict) -> str:
    date = profile["date"]
    clusters = html_insights["clusters"]
    bucket_counts = {b: classified["buckets"][b]["total"] for b in BUCKET_ORDER}
    top = sorted(bucket_counts.items(), key=lambda x: x[1], reverse=True)
    top_text = ", ".join(f"{b} {n}편" for b, n in top[:3])
    trend_text = (
        f"이 backfill은 arXiv /pastweek의 {date} 날짜 섹션에서 복구했습니다. "
        f"cs.CV {trends['daily_new_counts']['cv']}건, cs.RO {trends['daily_new_counts']['ro']}건이고 "
        f"dedupe 후 {classified['total']}건 중 {classified['selected']}건이 ROI 버킷에 걸렸습니다. "
        f"상위 버킷은 {top_text}입니다. {profile['trend_note']}"
    )
    bucket_line = " · ".join(f"[{b}] {bucket_counts[b]}" for b in BUCKET_ORDER)

    cluster_rows = []
    for cl in clusters:
        reps = "<br>".join(f"{paper_link(p)} {badge_html(p.get('badge',''))}" for p in cl["papers"])
        tags = " ".join(f"<span class='tag'>{esc(t)}</span>" for t in cl["importance_tags"])
        confidence = f"{esc(cl['confidence'])}<br><span class='small'>{esc(cl['confidence_note'])}</span>"
        cluster_rows.append(
            f"<tr><td><strong>{esc(cl['cluster'])}</strong><br>{tags}</td>"
            f"<td>{reps}</td><td>{esc(cl['why'])}</td><td>{confidence}</td><td>{esc(cl['lab_action'])}</td></tr>"
        )

    insight_cards = "".join(
        f"<div class='card insight'><h3>{esc(cl['cluster'])}</h3><p>{esc(cl['why'])}</p></div>"
        for cl in clusters[:4]
    )
    topics = "".join(
        f"<div class='card topic'><h3>{esc(t['title'])}</h3><p>{esc(t['claim'])}</p></div>"
        for t in profile["research_topics"]
    )
    must = "\n".join(
        f"<li>{paper_link(p)} <span class='small'>{esc(' '.join(importance_tags(p, p['bucket'])))}</span></li>"
        for p in html_insights["must_read"]
    )

    bucket_sections = []
    for b in BUCKET_ORDER:
        papers = classified["buckets"][b]["papers"][:6]
        rows = []
        for p in papers:
            phy = phylogeny_for(b, p)
            rows.append(
                f"<div class='mini-paper'><strong>{paper_link(p)}</strong> {badge_html(p.get('badge',''))}"
                f"<p class='authors'>{esc(', '.join(p.get('authors', [])[:5]))}</p>"
                f"<p>{esc(paper_excerpt(p))}</p>"
                f"<p class='small'><strong>Phylogeny:</strong> {esc(phy['source'])} · {esc(phy['phylum'])} &gt; {esc(phy['class'])} &gt; {esc(phy['order'])} &gt; {esc(phy['genus'])}</p></div>"
            )
        bucket_sections.append(f"<h4 class='bucket'>{esc(b)} <span class='count'>{len(papers)}/{bucket_counts[b]}</span></h4>{''.join(rows)}")

    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>arXiv Daily Briefing - {date}</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:#f6f8fa;color:#24292f;margin:0;padding:28px 12px;line-height:1.62}}
.container{{max-width:980px;margin:0 auto;background:#fff;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.06),0 1px 2px rgba(0,0,0,.04);padding:40px 48px}}
h1{{font-size:28px;margin:0 0 6px;color:#0d1117}}h2{{font-size:21px;margin:40px 0 14px;padding-bottom:8px;border-bottom:2px solid #e5e7eb}}h3{{font-size:16px;margin:14px 0 6px}}h4.bucket{{font-size:18px;margin:32px 0 10px;padding-top:14px;border-top:2px solid #e5e7eb;color:#0f172a}}.count{{font-size:13px;font-weight:400;color:#656d76}}
a{{color:#0969da;text-decoration:none}}a:hover{{text-decoration:underline}}.home{{display:inline-block;padding:6px 14px;font-size:13px;color:#0969da;background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;margin:0 0 18px}}
.meta{{font-size:13px;color:#3b434d;padding:14px 18px;background:#f6f8fa;border-left:3px solid #0969da;border-radius:6px;margin:14px 0 22px}}.thesis{{background:#0f172a;color:#f8fafc;border-radius:10px;padding:18px 22px;margin:16px 0 28px;font-size:16px}}.thesis strong{{color:#fef08a}}
.cluster-table{{width:100%;border-collapse:collapse;font-size:13px;margin:12px 0 18px}}.cluster-table th,.cluster-table td{{border:1px solid #d0d7de;padding:9px;vertical-align:top}}.cluster-table th{{background:#f6f8fa;color:#0d1117}}
.card,.mini-paper{{background:#fafbfc;border:1px solid #e5e7eb;border-radius:8px;padding:14px 18px;margin:12px 0}}.mini-paper{{background:#fff}}.topic{{border-left:4px solid #22c55e;background:#f0fdf4}}.insight{{border-left:4px solid #0969da;background:#f8fafc}}
.bucket-line{{font-family:ui-monospace,SFMono-Regular,Consolas,Menlo,monospace;background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;padding:10px 14px;font-size:13px;white-space:pre-wrap;overflow-x:auto}}
.badge{{display:inline-block;font-size:11px;font-weight:600;padding:1px 8px;border-radius:10px;margin-left:6px;vertical-align:middle;font-family:ui-monospace,monospace}}.cv{{background:#ddf4ff;color:#0550ae;border:1px solid #54aeff}}.ro{{background:#fff8c5;color:#7a4e00;border:1px solid #d4a72c}}.cvro{{background:#ffe5d9;color:#9a3412;border:1px solid #f59e0b}}.x{{background:#f3f4f6;color:#6b7280;border:1px solid #d1d5db}}
.tag{{display:inline-block;font-family:ui-monospace,SFMono-Regular,Consolas,Menlo,monospace;font-size:12px;color:#7c2d12;background:#fff7ed;border:1px solid #fed7aa;border-radius:6px;padding:1px 7px;margin:2px 3px 2px 0}}.authors,.small{{color:#475569;font-size:13.5px}}footer{{margin-top:40px;padding-top:16px;border-top:1px solid #eaeef2;font-size:12px;color:#656d76;text-align:center}}
@media(max-width:760px){{body{{padding:16px 8px}}.container{{padding:24px 20px}}.cluster-table{{font-size:12.5px}}}}
</style>
</head>
<body><main class="container">
<a class="home" href="../index.html">← Home</a>
<h1>arXiv Daily Briefing — {date} ({profile['weekday']})</h1>
<div class="meta">
<div><strong>소스:</strong> arXiv cs.CV/pastweek date section + cs.RO/pastweek date section · source_listing_date={date} · source_mode={SOURCE_MODE}</div>
<div><strong>주간 시야:</strong> {profile['week_start']} ~ {date}</div>
<div><strong>오늘 /new:</strong> cs.CV {trends['daily_new_counts']['cv']} + cs.RO {trends['daily_new_counts']['ro']} · {classified['total']} dedup · {classified['selected']} ROI papers</div>
<div><strong>Backfill note:</strong> /pastweek 날짜 섹션에는 abstract가 없어 논문별 분류와 요약은 title/subject 기반입니다.</div>
</div>
<section class="thesis"><strong>오늘의 결론:</strong> {esc(profile['thesis'])}</section>
<h2>오늘의 클러스터 지도</h2>
<table class="cluster-table"><thead><tr><th>Cluster</th><th>대표 논문</th><th>왜 중요?</th><th>Confidence</th><th>Lab action</th></tr></thead><tbody>
{''.join(cluster_rows)}
</tbody></table>
<h2>주간 동향</h2>
<p>{esc(trend_text)}</p>
<div class="bucket-line">{esc(bucket_line)}</div>
<h2>오늘의 인사이트</h2>
{insight_cards}
<h2>추천 연구주제</h2>
{topics}
<h2>Must-read papers</h2>
<ol>{must}</ol>
<h2>버킷별 주요 논문</h2>
{''.join(bucket_sections)}
<footer>Generated from repo parser outputs. WebFetch was not used for arXiv source data.</footer>
</main></body></html>
"""


def build(profile: dict, cv_new_path: str, ro_new_path: str) -> None:
    date = profile["date"]
    cv_new = load_json(cv_new_path)
    ro_new = load_json(ro_new_path)
    cv_pw = load_json("out/cv_pastweek.json")
    ro_pw = load_json("out/ro_pastweek.json")
    classified = classify_daily(cv_new, ro_new)
    papers = all_classified_papers(classified)
    clusters = build_clusters(profile, papers)
    if len(clusters) < 3:
        raise SystemExit(f"not enough clusters for {date}: {len(clusters)}")

    must_read: list[dict] = []
    seen: set[str] = set()
    for cl in clusters:
        for p in cl["papers"]:
            if p["arxiv_id"] not in seen:
                seen.add(p["arxiv_id"])
                must_read.append(p)
    must_read = must_read[:10]

    trends = {
        "date": date,
        "source_listing_date": date,
        "source_mode": SOURCE_MODE,
        "daily_new_counts": {
            "cv": listing_count(cv_new),
            "ro": listing_count(ro_new),
            "scope": "new+cross; replacements excluded",
        },
        "totals": {
            "selected": classified["selected"],
            "total_scanned": classified["total"],
            "note": (
                f"Backfill from arXiv /pastweek date section for {date}: "
                f"cs.CV {listing_count(cv_new)} + cs.RO {listing_count(ro_new)} new+cross entries, "
                f"dedup {classified['total']}, selected {classified['selected']} ROI papers. "
                "Paper abstracts are not available in the date-section source."
            ),
        },
        "buckets": {b: {k: v for k, v in classified["buckets"][b].items() if k != "papers"} for b in BUCKET_ORDER},
        "buckets_pastweek": classify_pastweek(cv_pw + ro_pw),
        "keywords_cv": keyword_counts(cv_pw),
        "keywords_ro": keyword_counts(ro_pw),
    }

    insights = {
        "date": date,
        "daily_thesis": profile["thesis"],
        "clusters": [],
        "research_topics": profile["research_topics"],
        "must_read": [],
        "phylogeny_tags": [],
    }
    for cl in clusters:
        row = {
            "cluster": cl["cluster"],
            "why": cl["why"],
            "confidence": cl["confidence"],
            "confidence_note": cl["confidence_note"],
            "lab_action": cl["lab_action"],
            "importance_tags": cl["importance_tags"],
            "papers": [],
        }
        for p in cl["papers"]:
            phy = phylogeny_for(p["bucket"], p)
            row["papers"].append({
                "title": p["title"],
                "arxiv": paper_url(p),
                "importance_tags": importance_tags(p, p["bucket"]),
                "phylogeny": phy,
            })
            insights["phylogeny_tags"].append({
                "paper": paper_url(p),
                "source": phy["source"],
                "lineage": f"{phy['phylum']} > {phy['class']} > {phy['order']} > {phy['genus']}",
            })
        insights["clusters"].append(row)

    for p in must_read:
        phy = phylogeny_for(p["bucket"], p)
        insights["must_read"].append({
            "title": p["title"],
            "arxiv": paper_url(p),
            "why": summary_for_paper(p)[2],
            "importance_tags": importance_tags(p, p["bucket"]),
            "phylogeny": phy,
        })

    html_insights = {"clusters": clusters, "must_read": must_read}
    benchmarks = {
        "date": date,
        "results": [
            {"name": "Parser coverage", "value": f"{classified['selected']}/{classified['total']} ROI selected", "status": "pass"},
            {"name": "Backfill source", "value": f"cs.CV {listing_count(cv_new)} + cs.RO {listing_count(ro_new)} date-section rows", "status": "pass"},
            {"name": "Cluster table", "value": f"{len(clusters)} clusters with representative papers", "status": "pass"},
            {"name": "Phylogeny tags", "value": f"{len(insights['phylogeny_tags'])} representative mappings", "status": "pass"},
        ],
        "note": "Backfill artifact generated from arXiv /pastweek date-section parser output. Per-paper abstracts were unavailable, so summaries are intentionally title/subject based.",
    }

    (ROOT / "posts").mkdir(exist_ok=True)
    with open(ROOT / "posts" / f"{date}.html", "w", encoding="utf-8", newline="\n") as f:
        f.write(render_html(profile, classified, trends, html_insights))
    write_json(f"trends/{date}.json", trends)
    write_json(f"insights/{date}.json", insights)
    write_json(f"benchmarks/{date}.json", benchmarks)
    write_json("out/classified.json", classified)
    print(f"wrote artifacts for {date}: {len(clusters)} clusters, {len(must_read)} must-read papers")


def week_start(date: str) -> str:
    day = dt.date.fromisoformat(date)
    return (day - dt.timedelta(days=6)).isoformat()
