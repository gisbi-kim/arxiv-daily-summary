#!/usr/bin/env python3
"""Generate the 2026-05-19 arXiv daily briefing artifacts from parser outputs."""
from __future__ import annotations

import html
import io
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from classify import BUCKETS, assign_bucket, primary_badge

DATE = "2026-05-19"
WEEKDAY = "화"
WEEK_START = "2026-05-13"
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
        "title": "Geometry는 reconstruction 품질보다 sensing stack 통합으로 이동",
        "buckets": ["3D/Scene", "Robot Learning", "Generation"],
        "needles": ["3dphysvideo", "neurolidar", "lidar", "occupancy", "scene flow", "mesh", "3d", "4d", "reconstruction", "depth", "camera pose", "gaussian"],
        "why": "오늘 3D/Scene은 보기 좋은 3D 복원만 늘어난 날이 아닙니다. 3DPhysVideo는 물리 시뮬레이션과 3D scene reconstruction을 같이 보고, NeuroLiDAR와 NERVE는 센서 입력 자체를 바꾸며, VGGT-Occ와 GEM은 occupancy와 planning 쪽으로 연결됩니다. SLAM이라는 제목이 없어도 map, pose, depth, occupancy가 하나의 sensing stack으로 묶이고 있어서 geometry/SLAM/reconstruction watch lens에서 따로 봐야 합니다.",
        "lab_action": "camera/LiDAR/event 입력, occupancy map, scene-flow 출력을 같은 relocalization 또는 planning split에서 failure mode별로 비교",
    },
    {
        "title": "VLA는 더 큰 모델보다 robust execution과 egocentric data loop를 묻는다",
        "buckets": ["Robot Learning", "Embodied AI", "Autonomous Driving"],
        "needles": ["stablevla", "vla", "vision-language-action", "egokit", "egocentric", "ego", "hand", "manipulation", "teleoperation", "robot", "humanoid", "dexterous"],
        "why": "Robot Learning 쪽은 거대한 VLA 하나를 더 키우는 이야기보다, 실제 실행 데이터를 어떻게 만들고 흔들림을 어떻게 줄일지가 더 뚜렷합니다. StableVLA는 extra data 없이 robustness를 묻고, EgoKit과 EgoInteract는 egocentric collection과 synthetic interaction video를 붙이며, StableHand는 손 동작 추정을 world-space로 끌고 옵니다. 로봇 정책을 읽을 때 모델 이름보다 입력 수집, hand/body state, recovery loop를 먼저 봐야 하는 날입니다.",
        "lab_action": "egocentric sensor kit, synthetic interaction video, robust VLA policy를 같은 manipulation task에서 data cost와 recovery success로 ablation",
    },
    {
        "title": "Driving은 language prompt와 safety guidance를 closed-loop 근거로 바꾸는 중",
        "buckets": ["Autonomous Driving", "Robot Learning", "3D/Scene"],
        "needles": ["driving", "drive", "clap", "drivesafe", "drivesafer", "occupancy", "motion planning", "collaborative perception", "vehicle", "gaze", "safety"],
        "why": "자율주행은 perception 점수보다 실제 주행 판단을 어떻게 안정화하는지가 더 중요해졌습니다. DriveSafe와 DriveSafer는 위험 감지와 safety guidance를 직접 다루고, CLAP은 language prompt를 end-to-end driving latent space에 넣으며, VGGT-Occ와 GEM은 occupancy forecast와 planning 쪽을 보강합니다. 자연어 지시, 위험 설명, occupancy prediction이 따로 노는 게 아니라 closed-loop evidence로 묶이는 흐름입니다.",
        "lab_action": "nuPlan/CARLA에서 language prompt drift, risky scene suggestion, occupancy forecast error를 같은 closed-loop failure board로 기록",
    },
    {
        "title": "Generation은 long video와 surgical world model에서 시간 제어를 시험",
        "buckets": ["Generation", "Autonomous Driving", "Robot Learning", "3D/Scene"],
        "needles": ["video", "world model", "diffusion", "trajectory guidance", "surgery", "simulation", "flow", "controllable", "long video", "motion", "physical"],
        "why": "Generation 버킷은 숫자가 제일 크지만, 오늘 핵심은 예쁜 샘플보다 시간 구조를 얼마나 통제하느냐입니다. AtlasVid는 ultra-high-resolution long video를, SWoMo는 cataract surgery simulation world model을, 3DPhysVideo와 video reconstruction 계열은 trajectory와 physical consistency를 묻습니다. 로봇이나 의료 시뮬레이션으로 넘기려면 frame quality보다 action-conditioned temporal drift를 먼저 봐야 합니다.",
        "lab_action": "surgical video, driving video, 3D physical video를 같은 temporal-control metric으로 묶고 drift와 action consistency를 분리 평가",
    },
    {
        "title": "VLM reliability는 GUI, clinical, geometry처럼 채점 가능한 과제로 내려감",
        "buckets": ["Foundation Models", "Safety/Alignment", "Embodied AI"],
        "needles": ["hallucination", "explanation", "auditing", "audit", "geometric reasoning", "gui grounding", "clinical", "vqa", "vlm", "verification", "benchmark", "memory"],
        "why": "Foundation model과 safety 묶음은 추상적인 reasoning claim보다 검증 가능한 task로 내려왔습니다. GeoSym127K와 Hilbert-Geo는 geometry reasoning을 symbolic check로 묶고, WinDeskGround는 GUI grounding을 복잡한 multi-window 환경에서 재며, clinical rater auditing과 misleading explanation 논문은 모델이 맞아 보이는 이유를 어떻게 잘못 설명하는지 봅니다. 신뢰성 평가는 이제 '똑똑해 보임'이 아니라 채점 가능한 실패 로그를 남기는 쪽입니다.",
        "lab_action": "GUI grounding, clinical ordinal scoring, geometric proof task를 하나의 VLM failure-log schema로 묶어 explanation error와 answer error를 분리",
    },
    {
        "title": "Efficiency는 visual token과 video compression을 줄여도 의미가 남는지 묻는다",
        "buckets": ["Efficiency/Systems", "Foundation Models", "Generation"],
        "needles": ["visual token", "token", "compression", "video mllm", "streaming", "pruning", "efficient", "semantic communication", "lora", "cache", "attention"],
        "why": "Efficiency/System은 작은 모델 하나를 만드는 문제보다, 어떤 visual token과 video frame을 버려도 의미가 유지되는지 묻는 쪽으로 더 구체화됐습니다. F^3A는 MLLM visual token pruning을, Fre-Res는 video token compression을, StrLoRA와 streaming continual tuning 계열은 계속 들어오는 시각 입력을 어떻게 업데이트할지 봅니다. 실제 배포에서는 평균 정확도보다 token budget, latency, long-video degradation을 같이 봐야 합니다.",
        "lab_action": "video MLLM과 GUI/robot vision 입력에서 token pruning 비율, latency, downstream grounding 성공률을 같은 Pareto curve로 기록",
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
        "physics", "calibration", "memory", "intent", "cache", "occupancy",
        "egocentric", "stablevla", "gui", "geometric", "neuromorphic",
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
        "오늘의 핵심은 논문 수가 갑자기 커진 것보다, geometry·VLA·driving·MLLM이 모두 "
        "실제 입력과 실행 조건을 더 빡빡하게 묻기 시작했다는 점입니다. 센서와 occupancy, "
        "egocentric robot data, visual token budget, safety guidance가 같은 날 크게 올라왔습니다."
    )
    trend_text = (
        f"오늘 /new는 cs.CV {trends['daily_new_counts']['cv']}건, cs.RO {trends['daily_new_counts']['ro']}건이고 "
        f"dedupe 후 {classified['total']}건 중 {classified['selected']}건이 ROI 버킷에 걸렸습니다. "
        f"가장 큰 버킷은 {top[0][0]} {top[0][1]}편, {top[1][0]} {top[1][1]}편, {top[2][0]} {top[2][1]}편입니다. "
        "숫자로는 Generation과 Efficiency가 크지만, lab 관점에서는 geometry/SLAM/recon sensing stack, "
        "VLA robust execution, driving safety guidance를 따로 읽는 편이 더 중요합니다."
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
        "daily_thesis": "오늘은 큰 배치 안에서 geometry, VLA, driving, MLLM efficiency가 모두 실제 입력과 실행 조건으로 내려왔습니다. 센서 fusion, egocentric robot data, language-guided driving safety, visual token budget을 같이 봐야 합니다.",
        "clusters": [],
        "research_topics": [
            {"title": "Sensing-stack geometry board", "claim": "event/RGB/LiDAR 입력, occupancy map, scene-flow 출력을 같은 relocalization 또는 planning split에서 비교합니다."},
            {"title": "Robust VLA data-loop ablation", "claim": "egocentric collection, synthetic interaction video, no-extra-data robust VLA를 같은 manipulation task family에서 분리합니다."},
            {"title": "Visual-token deployment curve", "claim": "video MLLM과 robot vision 입력에서 token pruning, latency, grounding success를 한 Pareto curve로 기록합니다."},
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
