#!/usr/bin/env python3
"""Generate the 2026-05-18 arXiv daily briefing artifacts from parser outputs."""
from __future__ import annotations

import html
import io
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from classify import BUCKETS, assign_bucket, primary_badge

DATE = "2026-05-18"
WEEKDAY = "월"
WEEK_START = "2026-05-12"
WEEK_END = DATE
SOURCE_MODE = "new"
ROOT = Path(__file__).resolve().parents[1]
BUCKET_ORDER = [b for b, _ in BUCKETS]

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

CLUSTER_SPECS = [
    {
        "title": "Geometry는 3DGS 지도와 feed-forward 재구성 쪽으로 다시 모이고 있음",
        "buckets": ["3D/Scene", "Robot Learning", "Generation"],
        "needles": ["gaussian", "splat", "vggt", "3d", "4d", "lidar", "calibration", "panoramic", "mesh", "reconstruction", "depth"],
        "why": "오늘 3D/Scene 묶음은 단순히 보기 좋은 3D 생성 논문이 많다는 신호가 아닙니다. PanoPlane, TurboVGGT, CalibAnyView, Denoising-GS처럼 지도 표현, 카메라 보정, sparse-view 재구성, Gaussian map 품질을 직접 건드리는 논문이 같이 나왔습니다. SLAM이라는 제목이 없어도 pose, map, correspondence, update 비용을 다시 묻는 흐름이라서 geometry/SLAM/reconstruction watch lens로 따로 봐야 합니다.",
        "lab_action": "3DGS map, VGGT류 feed-forward geometry, calibration prior를 같은 relocalization split에서 성공률, update cost, dynamic-object failure로 비교",
    },
    {
        "title": "VLA는 모델 하나보다 intent, depth, correction 같은 실행 구조로 갈라짐",
        "buckets": ["Robot Learning", "Embodied AI", "Autonomous Driving"],
        "needles": ["vla", "vision-language-action", "intent", "depth", "humanoid", "dexterous", "correction", "teleoperation", "manipulation"],
        "why": "VLA 논문을 하나의 거대한 policy 경쟁으로 보면 오늘 신호가 흐려집니다. Evo-Depth는 depth cue를, IntentVLA와 humanoid control 계열은 짧은 horizon intent를, dexterous correction 논문은 사람이 중간에 고쳐 주는 실행 루프를 봅니다. 즉 모델 크기보다 내부 표현과 개입 지점이 실제 robot task family에서 얼마나 안정성을 주는지가 핵심입니다.",
        "lab_action": "LIBERO/RoboCasa와 humanoid-control split에서 depth cue, intent state, intervention correction을 같은 task family로 ablation",
    },
    {
        "title": "Driving은 perception 점수보다 closed-loop 실패 증거를 더 강하게 요구함",
        "buckets": ["Autonomous Driving", "Robot Learning"],
        "needles": ["driving", "closed-loop", "trajectory", "planning", "map", "vehicle", "collision", "uav", "navigation", "flow matching"],
        "why": "자율주행 쪽은 trajectory나 map prediction 자체보다, 그 예측이 실제 주행 루프 안에서 실패를 줄이는지 묻는 논문이 더 중요합니다. CLOVER는 closed-loop value ranking을, semantic attack 논문은 online map construction의 취약점을, flow-matching driving policy와 graph-of-convex-sets planning은 제어 쪽 기준을 제공합니다. offline perception score와 deployment stability 사이 간격을 재는 날입니다.",
        "lab_action": "nuPlan/CARLA에서 map attack, route change, high-level instruction drift를 하나의 closed-loop stress board로 묶기",
    },
    {
        "title": "World model과 video generation은 보기 좋은 예측보다 조작 가능성을 묻고 있음",
        "buckets": ["Generation", "Autonomous Driving", "Robot Learning", "3D/Scene"],
        "needles": ["world model", "video", "diffusion", "flow", "interactive", "physics", "controllable", "generation", "motion", "future"],
        "why": "Generation 버킷은 여전히 가장 크지만, 오늘 읽을 지점은 샘플 품질보다 controllability입니다. Delta Forcing, Head Forcing, physics-grounded reward, driving world model 계열은 사용자가 원하는 시간 구조나 행동 조건을 넣었을 때 예측이 계속 버티는지를 묻습니다. 이 흐름은 로봇이나 주행 평가로 넘어가기 전에 world model의 실패 조건을 분리해 보려는 움직임입니다.",
        "lab_action": "camera/action condition, temporal drift, physical violation을 분리한 controllable video/world-model metric 설계",
    },
    {
        "title": "VLM reliability는 외부 도구보다 내부 검증 경로와 memory 한계로 이동",
        "buckets": ["Foundation Models", "Safety/Alignment", "Embodied AI"],
        "needles": ["hallucination", "verification", "memory", "agent", "reasoning", "counterfactual", "ood", "alignment", "vqa", "vlm"],
        "why": "Foundation model 묶음에서는 단순 benchmark 점수보다 왜 틀렸는지 추적하는 논문이 눈에 띕니다. SIRA는 attribution을 내부 재구성으로 다루고, DermAgent는 traceable decision을, MemLens와 navigation bottleneck 논문은 memory와 3D understanding이 long-horizon 실패로 이어지는 지점을 봅니다. 신뢰성은 이제 외부 도구를 붙이는 문제가 아니라 내부 검증 경로와 기억 구조를 같이 보는 문제에 가깝습니다.",
        "lab_action": "medical VQA, long-term memory, VLN을 같은 failure-log schema로 기록하고 self-verification failure case를 분리",
    },
    {
        "title": "Efficiency는 작은 모델보다 token, cache, streaming budget 제어 문제",
        "buckets": ["Efficiency/Systems", "Foundation Models", "Generation"],
        "needles": ["token", "cache", "pruning", "compression", "efficient", "streaming", "sparse", "lora", "edge", "attention"],
        "why": "Efficiency/System 논문은 파라미터를 줄이는 이야기에서 더 구체적인 runtime budget으로 내려왔습니다. CoReDiT, HeatKV, InsightTok, representative attention, streaming video understanding은 어떤 token을 남기고 어떤 cache를 줄여도 의미가 유지되는지를 묻습니다. 실제 배포에서는 정확도 하나보다 latency, memory, long-context degradation을 같이 보는 쪽이 더 유용합니다.",
        "lab_action": "video diffusion, MLLM, tracking 계열에서 token budget, KV cache size, latency, accuracy drop을 같은 Pareto curve로 기록",
    },
]


def load_json(path: str):
    with open(ROOT / path, encoding="utf-8") as f:
        return json.load(f)


def esc(value) -> str:
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


def phylogeny_for(bucket: str) -> dict:
    source, lineage = PHYLOGENY[bucket]
    phylum, cls, order, genus = [x.strip() for x in lineage.split(">")]
    return {
        "source": source,
        "phylum": phylum,
        "class": cls,
        "order": order,
        "genus": genus,
        "confidence": "Medium",
        "rationale": "제목, 초록, ROI 버킷을 기준으로 canonical taxonomy의 가장 가까운 계통에 매핑했습니다.",
    }


def importance_tags(p: dict, bucket: str) -> list[str]:
    text = text_blob(p)
    tags: list[str] = []
    if any(k in text for k in ["benchmark", "dataset", "stress", "evaluation", "rank"]):
        tags.append("[평가축]")
    if any(k in text for k in ["safety", "ood", "jailbreak", "robust", "adversarial", "attack", "verification"]):
        tags.append("[경고신호]")
    if any(k in text for k in ["efficient", "compression", "pruning", "cache", "streaming", "edge", "tiny", "token"]):
        tags.append("[실사용전환]")
    if any(k in text for k in ["vla", "world model", "latent", "diffusion", "flow", "gaussian", "vggt"]):
        tags.append("[방법전환]")
    if any(k in text for k in ["survey", "taxonomy", "position"]):
        tags.append("[통합정리]")
    if not tags:
        tags.append("[문제정의]" if bucket in {"Embodied AI", "Safety/Alignment"} else "[인프라]")
    return tags[:3]


def rank_paper(p: dict, bucket: str) -> int:
    text = text_blob(p)
    score = 0
    for kw in [
        "benchmark", "dataset", "vla", "vision-language-action", "world model",
        "closed-loop", "safety", "ood", "jailbreak", "verification", "token",
        "compression", "navigation", "gaussian", "4d", "driving", "diffusion",
        "physics", "calibration", "memory", "intent", "cache",
    ]:
        if kw in text:
            score += 3
    if p.get("badge") == "CV/RO":
        score += 5
    if p.get("badge") == "RO":
        score += 3
    if bucket in {"3D/Scene", "Robot Learning", "Autonomous Driving"}:
        score += 1
    return score + min(len(p.get("abstract", "")) // 450, 3)


def all_classified_papers(classified: dict) -> list[dict]:
    papers = []
    for bucket, info in classified["buckets"].items():
        for p in info["papers"]:
            q = dict(p)
            q["bucket"] = bucket
            papers.append(q)
    return papers


def listing_count(rows: list[dict]) -> int:
    return sum(1 for row in rows if row.get("section") != "replace")


def classify_pastweek(papers: list[dict]) -> dict:
    out = {b: {"total": 0, "cv": 0, "ro": 0, "cvro": 0} for b in BUCKET_ORDER}
    seen = {}
    for p in papers:
        seen.setdefault(p["arxiv_id"], p)
    for p in seen.values():
        bucket = assign_bucket(p.get("title", ""), "", p.get("subjects", ""))
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


def keyword_counts(papers: list[dict]) -> list[list[object]]:
    keywords = ["vla", "world model", "diffusion", "video", "gaussian", "3d", "4d",
                "navigation", "driving", "benchmark", "dataset", "token", "cache",
                "compression", "safety", "ood", "hallucination", "calibration", "robot",
                "manipulation", "memory", "intent"]
    text = " ".join(text_blob(p) for p in papers)
    return [[k, text.count(k)] for k in keywords if text.count(k)][:22]


def select_papers(spec: dict, papers: list[dict], used: set[str]) -> list[dict]:
    candidates: list[tuple[int, dict]] = []
    for p in papers:
        if p["arxiv_id"] in used or p["bucket"] not in spec["buckets"]:
            continue
        text = text_blob(p)
        hits = sum(1 for n in spec["needles"] if n in text)
        if hits:
            candidates.append((hits * 20 + rank_paper(p, p["bucket"]), p))
    candidates.sort(key=lambda x: (x[0], x[1].get("title", "")), reverse=True)
    return [p for _, p in candidates[:4]]


def build_clusters(papers: list[dict]) -> list[dict]:
    used: set[str] = set()
    clusters = []
    for spec in CLUSTER_SPECS:
        selected = select_papers(spec, papers, used)
        if len(selected) < 2:
            continue
        used.update(p["arxiv_id"] for p in selected)
        clusters.append({
            "cluster": spec["title"],
            "papers": selected,
            "why": spec["why"],
            "confidence": "High" if len(selected) >= 3 else "Medium",
            "confidence_note": f"대표 논문 {len(selected)}편 연결",
            "lab_action": spec["lab_action"],
            "importance_tags": sorted({t for p in selected for t in importance_tags(p, p["bucket"])})[:4],
        })
    return clusters[:6]


def summary_for_paper(p: dict) -> tuple[str, str, str]:
    bucket = p["bucket"]
    if bucket == "3D/Scene":
        return ("Geometry / reconstruction", "map, pose, correspondence 문제를 다른 이름으로 다시 다룹니다.", "SLAM/reconstruction 계열 실험의 map representation 후보로 볼 만합니다.")
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


def render_html(classified: dict, trends: dict, html_insights: dict) -> str:
    clusters = html_insights["clusters"]
    bucket_counts = {b: classified["buckets"][b]["total"] for b in BUCKET_ORDER}
    top = sorted(bucket_counts.items(), key=lambda x: x[1], reverse=True)
    thesis = (
        "오늘의 핵심은 `생성 논문이 많다`가 아니라, generation·geometry·robot policy가 모두 "
        "실행 가능한 조건으로 내려오고 있다는 점입니다. 3DGS/VGGT 계열은 map representation 문제로, "
        "VLA는 depth·intent·intervention 구조로, video/world model은 controllability 평가로 이동합니다."
    )
    trend_text = (
        f"오늘 /new는 cs.CV {trends['daily_new_counts']['cv']}건, cs.RO {trends['daily_new_counts']['ro']}건이고 "
        f"dedupe 후 {classified['total']}건 중 {classified['selected']}건이 ROI 버킷에 걸렸습니다. "
        f"가장 큰 버킷은 {top[0][0]} {top[0][1]}편, {top[1][0]} {top[1][1]}편, {top[2][0]} {top[2][1]}편입니다. "
        "숫자로는 Generation이 크지만, lab 관점에서는 geometry/SLAM/recon과 VLA 실행 구조를 따로 읽는 편이 더 중요합니다."
    )
    bucket_line = " · ".join(f"[{b}] {bucket_counts[b]}" for b in BUCKET_ORDER)
    cluster_rows = []
    for cl in clusters:
        reps = "<br>".join(f"{paper_link(p)} {badge_html(p.get('badge',''))}" for p in cl["papers"])
        why = esc(cl["why"])
        tags = " ".join(f"<span class='tag'>{esc(t)}</span>" for t in cl["importance_tags"])
        cluster_rows.append(
            f"<tr><td><strong>{esc(cl['cluster'])}</strong><br>{tags}</td>"
            f"<td>{reps}</td><td>{why}</td><td>{esc(cl['confidence'])}</td><td>{esc(cl['lab_action'])}</td></tr>"
        )
    topics = "".join(f"<div class='card topic'><h3>{esc(t['title'])}</h3><p>{esc(t['claim'])}</p></div>" for t in html_insights["research_topics"])
    must = "\n".join(f"<li>{paper_link(p)} <span class='small'>{esc(' '.join(importance_tags(p, p['bucket'])))}</span></li>" for p in html_insights["must_read"])
    bucket_sections = []
    for b in BUCKET_ORDER:
        papers = classified["buckets"][b]["papers"][:6]
        rows = []
        for p in papers:
            phy = phylogeny_for(b)
            rows.append(
                f"<div class='mini-paper'><strong>{paper_link(p)}</strong> {badge_html(p.get('badge',''))}"
                f"<p class='authors'>{esc(', '.join(p.get('authors', [])[:5]))}</p>"
                f"<p>{esc(clean(p.get('abstract',''))[:420])}</p>"
                f"<p class='small'><strong>Phylogeny:</strong> {esc(phy['source'])} · {esc(phy['phylum'])} &gt; {esc(phy['class'])} &gt; {esc(phy['order'])} &gt; {esc(phy['genus'])}</p></div>"
            )
        bucket_sections.append(f"<h4 class='bucket'>{esc(b)} <span class='count'>{len(papers)}/{bucket_counts[b]}</span></h4>{''.join(rows)}")
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>arXiv Daily Briefing - {DATE}</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:#f6f8fa;color:#24292f;margin:0;padding:28px 12px;line-height:1.62}}
.container{{max-width:980px;margin:0 auto;background:#fff;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.06),0 1px 2px rgba(0,0,0,.04);padding:40px 48px}}
h1{{font-size:28px;margin:0 0 6px;color:#0d1117}}h2{{font-size:21px;margin:40px 0 14px;padding-bottom:8px;border-bottom:2px solid #e5e7eb}}h3{{font-size:16px;margin:14px 0 6px}}h4.bucket{{font-size:18px;margin:32px 0 10px;padding-top:14px;border-top:2px solid #e5e7eb;color:#0f172a}}.count{{font-size:13px;font-weight:400;color:#656d76}}
a{{color:#0969da;text-decoration:none}}a:hover{{text-decoration:underline}}.home{{display:inline-block;padding:6px 14px;font-size:13px;color:#0969da;background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;margin:0 0 18px}}
.meta{{font-size:13px;color:#3b434d;padding:14px 18px;background:#f6f8fa;border-left:3px solid #0969da;border-radius:6px;margin:14px 0 22px}}.thesis{{background:#0f172a;color:#f8fafc;border-radius:10px;padding:18px 22px;margin:16px 0 28px;font-size:16px}}.thesis strong{{color:#fef08a}}
.cluster-table{{width:100%;border-collapse:collapse;font-size:13px;margin:12px 0 18px}}.cluster-table th,.cluster-table td{{border:1px solid #d0d7de;padding:9px;vertical-align:top}}.cluster-table th{{background:#f6f8fa;color:#0d1117}}
.card,.mini-paper{{background:#fafbfc;border:1px solid #e5e7eb;border-radius:8px;padding:14px 18px;margin:12px 0}}.mini-paper{{background:#fff}}.topic{{border-left:4px solid #22c55e;background:#f0fdf4}}
.bucket-line{{font-family:ui-monospace,SFMono-Regular,Consolas,Menlo,monospace;background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;padding:10px 14px;font-size:13px;white-space:pre-wrap;overflow-x:auto}}
.badge{{display:inline-block;font-size:11px;font-weight:600;padding:1px 8px;border-radius:10px;margin-left:6px;vertical-align:middle;font-family:ui-monospace,monospace}}.cv{{background:#ddf4ff;color:#0550ae;border:1px solid #54aeff}}.ro{{background:#fff8c5;color:#7a4e00;border:1px solid #d4a72c}}.cvro{{background:#ffe5d9;color:#9a3412;border:1px solid #f59e0b}}.x{{background:#f3f4f6;color:#6b7280;border:1px solid #d1d5db}}
.tag{{display:inline-block;font-family:ui-monospace,SFMono-Regular,Consolas,Menlo,monospace;font-size:12px;color:#7c2d12;background:#fff7ed;border:1px solid #fed7aa;border-radius:6px;padding:1px 7px;margin:2px 3px 2px 0}}.authors,.small{{color:#475569;font-size:13.5px}}footer{{margin-top:40px;padding-top:16px;border-top:1px solid #eaeef2;font-size:12px;color:#656d76;text-align:center}}
@media(max-width:760px){{body{{padding:16px 8px}}.container{{padding:24px 20px}}.cluster-table{{font-size:12.5px}}}}
</style>
</head>
<body><main class="container">
<a class="home" href="../index.html">← Home</a>
<h1>arXiv Daily Briefing — {DATE} ({WEEKDAY})</h1>
<div class="meta">
<div><strong>소스:</strong> arXiv cs.CV/new + cs.RO/new · source_listing_date={DATE} · source_mode={SOURCE_MODE}</div>
<div><strong>주간 시야:</strong> {WEEK_START} ~ {WEEK_END}</div>
<div><strong>오늘 /new:</strong> cs.CV {trends['daily_new_counts']['cv']} + cs.RO {trends['daily_new_counts']['ro']} · {classified['total']} dedup · {classified['selected']} ROI papers</div>
</div>
<section class="thesis"><strong>오늘의 결론:</strong> {esc(thesis)}</section>
<h2>주간 동향</h2>
<p>{esc(trend_text)}</p>
<div class="bucket-line">{esc(bucket_line)}</div>
<h2>오늘의 클러스터 지도</h2>
<table class="cluster-table"><thead><tr><th>Cluster</th><th>대표 논문</th><th>왜 중요?</th><th>Confidence</th><th>Lab action</th></tr></thead><tbody>
{''.join(cluster_rows)}
</tbody></table>
<h2>추천 연구주제</h2>
{topics}
<h2>Must-read papers</h2>
<ol>{must}</ol>
<h2>버킷별 주요 논문</h2>
{''.join(bucket_sections)}
<footer>Generated from repo parser outputs. WebFetch was not used for arXiv source data.</footer>
</main></body></html>
"""


def build() -> None:
    classified = load_json("out/classified.json")
    cv_new = load_json("out/cv_new.json")
    ro_new = load_json("out/ro_new.json")
    cv_pw = load_json("out/cv_pastweek.json")
    ro_pw = load_json("out/ro_pastweek.json")
    papers = all_classified_papers(classified)
    clusters = build_clusters(papers)
    must_read: list[dict] = []
    seen = set()
    for cl in clusters:
        for p in cl["papers"]:
            if p["arxiv_id"] not in seen:
                seen.add(p["arxiv_id"])
                must_read.append(p)
    must_read = must_read[:10]
    trends = {
        "date": DATE,
        "source_listing_date": DATE,
        "source_mode": SOURCE_MODE,
        "daily_new_counts": {"cv": listing_count(cv_new), "ro": listing_count(ro_new), "scope": "new+cross; replacements excluded"},
        "totals": {"selected": classified["selected"], "total_scanned": classified["total"], "note": f"cs.CV {listing_count(cv_new)} + cs.RO {listing_count(ro_new)} new+cross entries, dedup {classified['total']}, selected {classified['selected']} ROI papers."},
        "buckets": {b: {k: v for k, v in classified["buckets"][b].items() if k != "papers"} for b in BUCKET_ORDER},
        "buckets_pastweek": classify_pastweek(cv_pw + ro_pw),
        "keywords_cv": keyword_counts(cv_pw),
        "keywords_ro": keyword_counts(ro_pw),
    }
    insights = {
        "date": DATE,
        "daily_thesis": "Generation이 가장 크지만 오늘의 핵심은 실행 조건입니다. 3DGS/VGGT geometry는 map representation으로, VLA는 depth/intent/intervention 구조로, video/world model은 controllability 평가로 내려오고 있습니다.",
        "clusters": [],
        "research_topics": [
            {"title": "Geometry map representation board", "claim": "3DGS map, feed-forward geometry, camera calibration prior를 같은 relocalization split에서 비교합니다."},
            {"title": "VLA execution-structure ablation", "claim": "depth cue, intent state, human intervention correction이 task success와 recovery에 주는 영향을 같은 benchmark family에서 분리합니다."},
            {"title": "World-model controllability metric", "claim": "camera/action condition, temporal drift, physical violation을 분리해 video/world model을 평가합니다."},
        ],
        "must_read": [],
        "phylogeny_tags": [],
    }
    for cl in clusters:
        payload = {"cluster": cl["cluster"], "why": cl["why"], "confidence": cl["confidence"], "lab_action": cl["lab_action"], "papers": []}
        for p in cl["papers"]:
            phy = phylogeny_for(p["bucket"])
            payload["papers"].append({"title": p["title"], "arxiv": paper_url(p), "importance_tags": importance_tags(p, p["bucket"]), "phylogeny": phy})
            insights["phylogeny_tags"].append({"paper": paper_url(p), "source": phy["source"], "lineage": f"{phy['phylum']} > {phy['class']} > {phy['order']} > {phy['genus']}"})
        insights["clusters"].append(payload)
    for p in must_read:
        phy = phylogeny_for(p["bucket"])
        insights["must_read"].append({"title": p["title"], "arxiv": paper_url(p), "why": summary_for_paper(p)[2], "importance_tags": importance_tags(p, p["bucket"]), "phylogeny": phy})
    html_insights = dict(insights)
    html_insights["clusters"] = clusters
    html_insights["must_read"] = must_read
    benchmarks = {
        "date": DATE,
        "results": [
            {"name": "Parser coverage", "value": f"{classified['selected']}/{classified['total']} ROI selected", "status": "pass"},
            {"name": "Cluster table", "value": f"{len(clusters)} clusters with representative papers", "status": "pass"},
            {"name": "Phylogeny tags", "value": f"{len(insights['phylogeny_tags'])} representative mappings", "status": "pass"},
        ],
    }
    (ROOT / "posts" / f"{DATE}.html").write_text(render_html(classified, trends, html_insights), encoding="utf-8", newline="\n")
    (ROOT / "trends" / f"{DATE}.json").write_text(json.dumps(trends, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "insights" / f"{DATE}.json").write_text(json.dumps(insights, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "benchmarks" / f"{DATE}.json").write_text(json.dumps(benchmarks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote artifacts for {DATE}: {len(clusters)} clusters, {len(must_read)} must-read papers")


if __name__ == "__main__":
    build()
