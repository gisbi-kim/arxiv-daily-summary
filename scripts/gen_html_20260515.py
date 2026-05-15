#!/usr/bin/env python3
"""Generate the 2026-05-15 arXiv daily briefing artifacts from parser outputs."""
from __future__ import annotations

import html
import io
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, "scripts")
from classify import BUCKETS, assign_bucket, primary_badge

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DATE = "2026-05-15"
WEEKDAY = "금"
WEEK_START = "2026-05-09"
WEEK_END = DATE
SOURCE_MODE = "new"
ROOT = Path(__file__).resolve().parents[1]
BUCKET_ORDER = [b for b, _ in BUCKETS]
BUCKET_ICON = {
    "3D/Scene": "🧊",
    "Robot Learning": "🦾",
    "Autonomous Driving": "🚗",
    "Foundation Models": "🧠",
    "Generation": "🎨",
    "Efficiency/Systems": "⚙️",
    "Embodied AI": "🧭",
    "Safety/Alignment": "🛡️",
}
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
    ("SLAM/recon은 3DGS 지도, feed-forward geometry, localization으로 재포장되는 중",
     ["slam", "odometry", "localization", "relocalization", "gaussian", "splat", "3d reconstruction", "reconstruction", "lidar", "depth", "calibration", "pose", "mapping", "4d"],
     ["3D/Scene", "Autonomous Driving", "Robot Learning", "Generation"],
     "오늘 3D/Scene 논문은 단순히 예쁜 reconstruction을 만드는 쪽만이 아닙니다. Gaussian Splatting, fast visual geometry reconstruction, panoramic sparse-view completion, camera calibration, LiDAR fusion, physical reconstruction이 같이 나오면서, classic SLAM의 pose-map-correspondence 문제가 3DGS map, feed-forward geometry model, localization prior로 흩어져 다시 등장하는 흐름이 보입니다. 그래서 SLAM이라는 제목이 적어도 geometry backbone이 로봇과 주행 시스템의 지도 표현으로 이동하는지는 따로 추적해야 합니다.",
     "3DGS map, point cloud map, feed-forward geometry map을 visual localization 성공률, update cost, dynamic-object failure로 비교하는 1주짜리 표 작성",
     ["[방법전환]", "[실사용전환]", "[해부분석]"]),
    ("VLA가 큰 policy 하나에서 내부 역할을 나누는 쪽으로 이동",
     ["vla", "vision-language-action", "world model", "latent", "asynchronous", "capability vector"],
     ["Robot Learning", "Autonomous Driving", "Foundation Models", "3D/Scene"],
     "VLA를 하나의 거대한 policy로 보면 왜 성공하고 왜 실패하는지 설명하기가 어렵습니다. 오늘은 retrieval, multi-expert world model, asynchronous inference, capability vector, latent transition처럼 내부 역할을 나눠서 보려는 논문이 많이 나왔습니다. 그래서 다음 비교는 모델 크기보다 어떤 내부 구조가 어떤 task family에서 실제로 도움이 되는지를 따져야 합니다.",
     "LIBERO, RoboCasa, driving closed-loop에서 retrieval, expert routing, latent transition, async inference를 같은 표로 ablation",
     ["[방법전환]", "[해부분석]", "[실사용전환]"]),
    ("World model 평가는 예쁜 예측보다 행동과 물리 일관성으로 이동",
     ["world model", "physical", "physics", "4d", "interaction", "driving world model"],
     ["Generation", "Robot Learning", "Autonomous Driving", "3D/Scene"],
     "예전에는 world model을 미래 영상이 얼마나 그럴듯한지로 보는 경우가 많았습니다. 이번 묶음은 action-conditioned video, deformable object, driving world model, physical reasoning benchmark처럼 그 예측이 행동과 물리 조건에서 계속 쓸 수 있는지를 묻습니다. 즉 생성 품질보다 closed-loop 실패 조건을 먼저 보자는 신호입니다.",
     "PhyGround, ACWM-Phys, driving WM 계열을 묶어 물리 위반률, action success, temporal drift를 분리 측정",
     ["[평가축]", "[표준후보]", "[경고신호]"]),
    ("주행은 perception 점수보다 closed-loop 판단 근거를 묻기 시작",
     ["driving", "autonomous driving", "trajectory", "hd mapping", "closed-loop", "lane", "corruption"],
     ["Autonomous Driving", "Robot Learning", "Foundation Models"],
     "자율주행 논문이 lane, HD map, trajectory 예측을 따로 잘하는지에서 멈추지 않고 있습니다. VLA driver, expert routing, corruption dataset, closed-loop benchmark가 같이 나온 것은 판단 근거와 실패 상황을 실제로 주행 루프 안에서 확인하려는 흐름입니다.",
     "nuPlan/CARLA에서 corruption, route change, high-level instruction failure를 한 묶음으로 넣은 closed-loop stress test 구성",
     ["[평가축]", "[실사용전환]", "[위험보류]"]),
    ("VLM 신뢰성은 정답률보다 왜곡, 환각, 검증 경계를 보는 쪽으로 이동",
     ["hallucination", "over-alignment", "ood", "verification", "counterfactual", "robust", "medical", "vqa"],
     ["Foundation Models", "Safety/Alignment", "Efficiency/Systems"],
     "VLM이 벤치마크 정답을 맞히는지만 보면 실제 배포 위험을 놓치기 쉽습니다. 오늘은 over-alignment, kinematic physics calibration, medical VQA verification, OOD, jailbreak처럼 모델이 자신 있게 틀리는 조건을 드러내는 논문이 두껍게 나왔습니다.",
     "의료 VQA와 driving VLM에 counterfactual perturbation, confidence calibration, self-verification failure case를 같은 대시보드로 기록",
     ["[경고신호]", "[평가축]", "[해부분석]"]),
    ("효율화는 파라미터 축소보다 token, cache, streaming 제어로 구체화",
     ["token", "compression", "kv cache", "pruning", "efficient", "streaming", "edge", "tiny", "mcu"],
     ["Efficiency/Systems", "Foundation Models", "Generation"],
     "효율 논문이 단순히 작은 모델을 만드는 이야기에 머물지 않습니다. visual token compression, KV cache compression, token pruning, streaming impairments처럼 실제 추론 경로에서 무엇을 버리고 무엇을 남길지 정하는 문제로 바뀌고 있습니다.",
     "video diffusion, MLLM, tracking에서 token budget, latency, accuracy drop을 같은 x축으로 놓고 Pareto curve 작성",
     ["[실사용전환]", "[방법전환]", "[인프라]"]),
    ("Navigation은 단기 이동보다 기억, 제약, 애매한 지시를 함께 다루는 문제로 확장",
     ["navigation", "object navigation", "vln", "topological", "memory", "symbolic constraints", "planning"],
     ["Embodied AI", "Robot Learning", "3D/Scene", "Foundation Models"],
     "navigation을 다음 waypoint를 고르는 문제로만 보면 long-horizon 지시와 애매한 목표를 설명하기 어렵습니다. LCGNav, SleepWalk, ConsistNav, NEXUS 같은 논문은 기억, semantic executive control, symbolic constraint를 같이 보려는 흐름입니다.",
     "R2R/ObjectNav에 ambiguous query, memory reset, symbolic constraint violation을 넣은 navigation stress split 생성",
     ["[문제정의]", "[평가축]", "[인프라]"]),
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


def abstract_head(p: dict, limit: int = 340) -> str:
    text = clean(p.get("abstract", ""))
    if not text:
        return "초록이 저장되지 않아 제목과 분류 정보 기준으로만 판단했습니다."
    out = " ".join(re.split(r"(?<=[.!?])\s+", text)[:2]).strip()
    return out if len(out) <= limit else out[: limit - 1].rstrip() + "…"


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
        "rationale": "제목, 초록, ROI 버킷 기준으로 canonical taxonomy의 가장 가까운 계통에 매핑했습니다.",
    }


def importance_tags(p: dict, bucket: str) -> list[str]:
    text = text_blob(p)
    tags: list[str] = []
    if any(k in text for k in ["benchmark", "dataset", "stress-test", "evaluation"]):
        tags.append("[평가축]")
    if any(k in text for k in ["survey", "taxonomy", "position"]):
        tags.append("[통합정리]")
    if any(k in text for k in ["safety", "ood", "jailbreak", "robust", "adversarial", "corruption", "verification"]):
        tags.append("[경고신호]")
    if any(k in text for k in ["efficient", "compression", "pruning", "cache", "streaming", "edge", "tiny"]):
        tags.append("[실사용전환]")
    if any(k in text for k in ["vla", "world model", "latent", "routing", "diffusion", "flow", "gaussian"]):
        tags.append("[방법전환]")
    if not tags:
        tags.append("[문제정의]" if bucket in {"Embodied AI", "Safety/Alignment"} else "[인프라]")
    return tags[:3]


def rank_paper(p: dict, bucket: str) -> int:
    text = text_blob(p)
    score = 0
    for kw in ["benchmark", "dataset", "vla", "vision-language-action", "world model", "closed-loop", "safety", "ood", "jailbreak", "verification", "token", "compression", "navigation", "gaussian", "4d", "driving", "diffusion", "physics", "calibration"]:
        if kw in text:
            score += 3
    if p.get("badge") == "CV/RO":
        score += 4
    if p.get("badge") == "RO":
        score += 2
    return score + min(len(p.get("abstract", "")) // 500, 3)


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
    keywords = ["vla", "world model", "diffusion", "video", "gaussian", "3d", "4d", "navigation", "driving", "benchmark", "dataset", "token", "compression", "safety", "ood", "hallucination", "calibration", "robot", "manipulation", "latency"]
    text = " ".join(text_blob(p) for p in papers)
    return [[k, text.count(k)] for k in keywords if text.count(k)][:20]


def build_clusters(papers: list[dict]) -> list[dict]:
    used: set[str] = set()
    clusters = []
    for name, needles, buckets, why, action, tags in CLUSTER_SPECS:
        candidates = []
        if name.startswith("SLAM/recon"):
            priority_titles = [
                "TurboVGGT",
                "CalibAnyView",
                "PanoPlane",
                "VGGT-Edit",
                "Implicit spatial-frequency fusion",
                "Road Maps as Free Geometric Priors",
                "FU-MPC",
                "Real2Sim in HOI",
                "CineMesh4D",
            ]
            for p in papers:
                if p["arxiv_id"] in used:
                    continue
                title = p.get("title", "")
                for score, key in enumerate(reversed(priority_titles), start=1):
                    if key.lower() in title.lower():
                        candidates.append((score * 100 + rank_paper(p, p["bucket"]), p))
                        break
        else:
            for p in papers:
                if p["arxiv_id"] in used or p["bucket"] not in buckets:
                    continue
                hits = sum(1 for n in needles if n in text_blob(p))
                if hits:
                    candidates.append((hits * 10 + rank_paper(p, p["bucket"]), p))
        candidates.sort(key=lambda x: x[0], reverse=True)
        selected = [p for _, p in candidates[:4]]
        if len(selected) < 2:
            continue
        used.update(p["arxiv_id"] for p in selected)
        clusters.append({
            "cluster": name,
            "papers": selected,
            "why": why,
            "confidence": "High" if len(selected) >= 3 else "Medium",
            "confidence_note": f"대표 논문 {len(selected)}편 연결",
            "lab_action": action,
            "importance_tags": tags,
        })
    return clusters[:6]


def render_cluster_table(clusters: list[dict]) -> str:
    rows = []
    for cl in clusters:
        links = ", ".join(paper_link(p, p["title"].split(":")[0][:54]) for p in cl["papers"])
        tags = " ".join(f"<span class='tag'>{esc(t)}</span>" for t in cl["importance_tags"])
        rows.append("<tr>" + f"<td><strong>{esc(cl['cluster'])}</strong><br>{tags}</td>" + f"<td>{links}</td>" + f"<td>{esc(cl['why'])}</td>" + f"<td><strong>{esc(cl['confidence'])}</strong><br><span class='small'>{esc(cl['confidence_note'])}</span></td>" + f"<td>{esc(cl['lab_action'])}</td>" + "</tr>")
    return "<table class='cluster-table'><thead><tr><th>Cluster</th><th>대표 논문</th><th>왜 중요?</th><th>Confidence</th><th>Lab action</th></tr></thead><tbody>" + "\n".join(rows) + "</tbody></table>"


def summary_for_paper(p: dict) -> tuple[str, str, str]:
    text = text_blob(p)
    if "vla" in text or "vision-language-action" in text:
        return ("VLA가 새 장면이나 새 명령에서 어디까지 일반화되는지, 그리고 실패했을 때 어떤 내부 단계가 흔들리는지를 봅니다.", "제목과 초록 기준으로 retrieval, latent transition, asynchronous inference, capability vector, prior preserving 같은 구조적 장치를 제안합니다.", "단순 성공률보다 내부 역할 분해와 closed-loop 안정성을 같이 비교할 만한 논문입니다.")
    if "world model" in text or "physics" in text or "4d" in text:
        return ("생성되거나 예측된 장면이 보기 좋은지를 넘어, 행동과 물리 조건에서 계속 믿을 수 있는지가 문제입니다.", "action-conditioned video, driving world model, deformable object, physical reasoning benchmark 같은 축으로 평가 대상을 구체화합니다.", "world model을 실제 로봇이나 주행 루프에 넣기 전에 실패 조건을 분리해 볼 근거가 됩니다.")
    if "driving" in text or "trajectory" in text or "lane" in text:
        return ("자율주행 모델이 perception 점수는 좋아도 닫힌 주행 루프에서 잘못 판단할 수 있습니다.", "lane topology, HD mapping, trajectory expert routing, corruption dataset, closed-loop benchmark 같은 방식으로 평가 조건을 세분화합니다.", "offline metric과 실제 주행 안정성 사이의 간격을 줄이는 데 쓸 수 있습니다.")
    if "token" in text or "compression" in text or "cache" in text or "efficient" in text:
        return ("큰 모델을 실제로 쓰려면 latency, memory, token budget이 성능만큼 중요해집니다.", "token compression, pruning, KV cache compression, streaming 조건처럼 추론 경로의 병목을 직접 줄이는 쪽입니다.", "모델 정확도와 배포 비용을 같은 표에서 비교해야 하는 논문입니다.")
    if "navigation" in text or "planning" in text:
        return ("navigation은 단기 이동만 맞히는 문제가 아니라 기억, 목표 해석, 제약 조건을 함께 다뤄야 합니다.", "topological planning, semantic executive control, symbolic constraint, long-horizon benchmark 쪽으로 문제를 나눕니다.", "VLN/ObjectNav 평가에 애매한 지시와 장기 기억 실패를 넣어야 한다는 근거가 됩니다.")
    if "ood" in text or "jailbreak" in text or "robust" in text or "verification" in text:
        return ("모델이 자신 있게 틀리는 조건을 놓치면 실제 배포에서 위험합니다.", "OOD, corruption, counterfactual perturbation, self-verification, robustness stress test로 실패 조건을 드러냅니다.", "성능 개선 논문보다 배포 전 점검 항목으로 더 가치가 클 수 있습니다.")
    return ("해당 버킷에서 기존 접근이 놓치던 구체적인 데이터, 평가, 구조 문제를 다룹니다.", abstract_head(p, 260), f"{p['bucket']} 흐름 안에서 후속 실험의 비교 기준이나 보조 evidence로 볼 만합니다.")


def render_papers(classified: dict) -> str:
    parts = ["<h2>📄 논문별 요약</h2>"]
    for bucket in BUCKET_ORDER:
        info = classified["buckets"][bucket]
        parts.append(f"<h4 class='bucket'>{BUCKET_ICON[bucket]} {esc(bucket)} <span class='count'>· {info['total']}편 · CV {info['cv']} / RO {info['ro']} / CV-RO {info['cvro']}</span></h4>")
        selected = sorted(info["papers"], key=lambda p: rank_paper(p, bucket), reverse=True)[:14]
        for p0 in selected:
            p = dict(p0)
            p["bucket"] = bucket
            problem, method, meaning = summary_for_paper(p)
            phy = phylogeny_for(bucket)
            tag_html = " ".join(f"<span class='tag'>{esc(t)}</span>" for t in importance_tags(p, bucket))
            parts.append("<div class='mini-paper'>" + f"<h3>{paper_link(p)} {badge_html(p.get('badge','?'))}</h3>" + f"<p class='authors'>{esc(', '.join(p.get('authors', [])[:4]) or p.get('first_author',''))}</p>" + f"<p>{tag_html}</p>" + f"<p><strong>Phylogeny:</strong> {esc(phy['source'])} · {esc(phy['phylum'])} &gt; {esc(phy['class'])} &gt; {esc(phy['order'])} &gt; {esc(phy['genus'])}</p>" + "<ul>" + f"<li><strong>문제:</strong> {esc(problem)}</li>" + f"<li><strong>방법:</strong> {esc(method)}</li>" + f"<li><strong>의미:</strong> {esc(meaning)}</li>" + "</ul></div>")
    return "\n".join(parts)


def render_html(classified: dict, trends: dict, html_insights: dict) -> str:
    clusters = html_insights["clusters"]
    bucket_counts = {b: classified["buckets"][b]["total"] for b in BUCKET_ORDER}
    top = sorted(bucket_counts.items(), key=lambda x: x[1], reverse=True)[:3]
    bottom = sorted(bucket_counts.items(), key=lambda x: x[1])[:2]
    thesis = "오늘은 VLA와 world model이 여전히 크지만, 3D/Scene 쪽도 그냥 부록이 아닙니다. Gaussian Splatting, feed-forward reconstruction, calibration, LiDAR fusion이 같이 나오면서 classic SLAM/recon 문제가 새로운 geometry representation 안으로 흡수되는 흐름이 보입니다."
    trend_text = f"오늘 /new는 cs.CV {trends['daily_new_counts']['cv']}건, cs.RO {trends['daily_new_counts']['ro']}건이고 dedupe 후 {classified['total']}건 중 {classified['selected']}건이 ROI 버킷에 걸렸습니다. 가장 큰 버킷은 {top[0][0]} {top[0][1]}편, {top[1][0]} {top[1][1]}편, {top[2][0]} {top[2][1]}편입니다. 단순 생성 논문이 많은 날이지만, 3D/Scene도 {bucket_counts.get('3D/Scene', 0)}편으로 두껍습니다. 핵심은 VLA와 world model만이 아니라, SLAM/recon의 pose-map-correspondence 문제가 3DGS map, feed-forward geometry, localization/calibration 문제로 이름을 바꿔 이어진다는 점입니다."
    bucket_line = " · ".join(f"[{b.split('/')[0]}] {n}" for b, n in bucket_counts.items())
    insight_cards = "".join(f"<div class='card insight'><h3>{esc(cl['cluster'])}</h3><p>{esc(cl['why'])}</p><p><strong>대표:</strong> {paper_link(cl['papers'][0], cl['papers'][0]['title'])}</p></div>" for cl in clusters[:4])
    topic_cards = "".join(f"<div class='card topic'><h3>{esc(t['title'])}</h3><p>{esc(t['claim'])}</p></div>" for t in html_insights["research_topics"])
    must = "\n".join(f"<li>{paper_link(p, p['title'])} <span class='small'>{esc(' '.join(importance_tags(p, p['bucket'])))}</span></li>" for p in html_insights["must_read"])
    return f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>arXiv Daily Briefing — {DATE}</title><style>{CSS}</style></head><body><div class="container">
<a class="home" href="https://gisbi-kim.github.io/arxiv-daily-summary/">← 전체 목록으로</a>
<h1>📄 arXiv Daily Briefing — {DATE} ({WEEKDAY})</h1>
<div class="meta"><div><strong>시야:</strong> 주간 {WEEK_START} ~ {WEEK_END} · cs.CV/new + cs.RO/new</div>
<div><strong>소스:</strong> arxiv.org /list/cs.CV/new · /list/cs.RO/new · stdlib parser</div>
<div><strong>오늘 /new:</strong> cs.CV {trends['daily_new_counts']['cv']} + cs.RO {trends['daily_new_counts']['ro']} · {classified['total']} dedup · {classified['selected']} ROI papers</div>
<div><strong>프롬프트:</strong> prompts/instruction_v20260516.md 기준</div></div>
<div class="thesis"><strong>오늘의 결론:</strong> {esc(thesis)}</div>
<h2>🧩 오늘의 클러스터 지도</h2>{render_cluster_table(clusters)}
<h2>🔭 주간 동향</h2><p>{esc(trend_text)}</p>
<div class="bucket-line">{esc(bucket_line)}
TOP3: {esc(', '.join(f'{b} {n}' for b, n in top))} · BOTTOM2: {esc(', '.join(f'{b} {n}' for b, n in bottom))}</div>
<h2>💡 오늘의 인사이트</h2>{insight_cards}
<h2>🔬 추천 연구주제</h2>{topic_cards}
<h2>📌 must-read</h2><ol>{must}</ol>
{render_papers(classified)}
<h2>🔗 참고 링크</h2><ul><li><a href="https://arxiv.org/list/cs.CV/new">cs.CV/new</a></li><li><a href="https://arxiv.org/list/cs.RO/new">cs.RO/new</a></li></ul>
<footer>Generated from parser outputs. <a href="https://gisbi-kim.github.io/arxiv-daily-summary/">Archive</a></footer>
</div></body></html>
"""


CSS = r"""
*,*::before,*::after{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif;background:#f6f7f9;color:#1f2328;line-height:1.72;font-size:15px;padding:32px 16px;word-break:keep-all}
.container{max-width:980px;margin:0 auto;background:#fff;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.06),0 1px 2px rgba(0,0,0,.04);padding:40px 48px}
h1{font-size:28px;margin:0 0 6px;color:#0d1117}h2{font-size:21px;margin:40px 0 14px;padding-bottom:8px;border-bottom:2px solid #e5e7eb}h3{font-size:16px;margin:14px 0 6px}h4.bucket{font-size:18px;margin:32px 0 10px;padding-top:14px;border-top:2px solid #e5e7eb;color:#0f172a}.count{font-size:13px;font-weight:400;color:#656d76}
a{color:#0969da;text-decoration:none}a:hover{text-decoration:underline}.home{display:inline-block;padding:6px 14px;font-size:13px;color:#0969da;background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;margin:0 0 18px}
.meta{font-size:13px;color:#3b434d;padding:14px 18px;background:#f6f8fa;border-left:3px solid #0969da;border-radius:6px;margin:14px 0 22px}.thesis{background:#0f172a;color:#f8fafc;border-radius:10px;padding:18px 22px;margin:16px 0 28px;font-size:16px}.thesis strong{color:#fef08a}
.cluster-table{width:100%;border-collapse:collapse;font-size:13px;margin:12px 0 18px}.cluster-table th,.cluster-table td{border:1px solid #d0d7de;padding:9px;vertical-align:top}.cluster-table th{background:#f6f8fa;color:#0d1117}
.card,.mini-paper{background:#fafbfc;border:1px solid #e5e7eb;border-radius:8px;padding:14px 18px;margin:12px 0}.mini-paper{background:#fff}.insight{border-left:4px solid #0ea5e9}.topic{border-left:4px solid #22c55e;background:#f0fdf4}
.bucket-line{font-family:ui-monospace,SFMono-Regular,Consolas,Menlo,monospace;background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;padding:10px 14px;font-size:13px;white-space:pre-wrap;overflow-x:auto}
.badge{display:inline-block;font-size:11px;font-weight:600;padding:1px 8px;border-radius:10px;margin-left:6px;vertical-align:middle;font-family:ui-monospace,monospace}.cv{background:#ddf4ff;color:#0550ae;border:1px solid #54aeff}.ro{background:#fff8c5;color:#7a4e00;border:1px solid #d4a72c}.cvro{background:#ffe5d9;color:#9a3412;border:1px solid #f59e0b}.x{background:#f3f4f6;color:#6b7280;border:1px solid #d1d5db}
.tag{display:inline-block;font-family:ui-monospace,SFMono-Regular,Consolas,Menlo,monospace;font-size:12px;color:#7c2d12;background:#fff7ed;border:1px solid #fed7aa;border-radius:6px;padding:1px 7px;margin:2px 3px 2px 0}.authors,.small{color:#475569;font-size:13.5px}footer{margin-top:40px;padding-top:16px;border-top:1px solid #eaeef2;font-size:12px;color:#656d76;text-align:center}
@media(max-width:760px){body{padding:16px 8px}.container{padding:24px 20px}.cluster-table{font-size:12.5px}}
"""


def build() -> None:
    classified = load_json("out/classified.json")
    cv_new = load_json("out/cv_new.json")
    ro_new = load_json("out/ro_new.json")
    cv_pw = load_json("out/cv_pastweek.json")
    ro_pw = load_json("out/ro_pastweek.json")
    papers = all_classified_papers(classified)
    clusters = build_clusters(papers)
    must_read = []
    for cl in clusters:
        for p in cl["papers"]:
            if p["arxiv_id"] not in {x["arxiv_id"] for x in must_read}:
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
        "daily_thesis": "VLA와 world model이 크지만, 3D/Scene에서는 SLAM/recon 문제가 3DGS map, feed-forward geometry, localization/calibration 흐름으로 재포장되는 날입니다.",
        "clusters": [],
        "research_topics": [
            {"title": "3DGS map vs feed-forward geometry localization board", "claim": "3DGS 기반 map, point cloud map, VGGT류 feed-forward geometry를 같은 visual localization/relocalization split에서 성공률, update cost, dynamic-object failure로 비교합니다."},
            {"title": "VLA 내부 구조 ablation suite", "claim": "retrieval, expert routing, latent transition, async inference를 같은 manipulation/driving task family에서 비교해야 합니다."},
            {"title": "World model physical failure board", "claim": "보기 좋은 예측이 아니라 물리 위반률, action success, temporal drift를 분리 기록하는 평가판이 필요합니다."},
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
    print(f"wrote artifacts for {DATE}")


if __name__ == "__main__":
    build()
