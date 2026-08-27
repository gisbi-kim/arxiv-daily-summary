#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-08-27 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260827 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-27"


PROFILE = {
    "date": DATE,
    "weekday": "Thu",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching 2026-08-27 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-08-27 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "The 2026-08-27 batch is about whether a robot or visual reasoner can name the evidence that gives it permission to act. "
        "VLA and WAM papers move beyond larger backbones by exposing geometry tokens, recovered visual features, streaming temporal memory, human-video context, 4D Gaussian state, and dense confidence as action interfaces. "
        "Manipulation papers split adaptation into retrieval authority, embodiment mapping, tactile feedback, contact attention, progress, events, and uncertainty rather than treating a demonstration as one homogeneous object. "
        "Mapping papers make pose, intrinsics, LiDAR labels, odometry degradation, orchard topology, and GPS spoofing explicit stress conditions. "
        "Driving and VLM papers push risk, grounding, rubric, and retrieval evidence upstream so wrong answers or maneuvers can be stopped before commitment."
    ),
    "cluster_takeaway": (
        "Today's core is not another large VLA, map, or VLM benchmark; it is whether geometry, contact, memory, risk, and visual evidence can grant or revoke permission before the next action is committed."
    ),
    "trend_note": (
        "Thursday /new produced 154 deduplicated non-replacement papers and 124 ROI papers. "
        "Foundation Models and Robot Learning are large, but the highest APRL signal is the convergence of geometry-aware VLA, object-centric WAM, resilient odometry, driving risk evidence, and visual faithfulness protocols."
    ),
    "cluster_specs": [
        {
            "title": "VLA and world-action models move from broad priors to geometry and temporal evidence contracts",
            "buckets": ["Robot Learning", "3D/Scene", "Generation"],
            "ids": ["2608.24959", "2608.25308", "2608.26067", "2608.26103", "2608.25956", "2608.25572", "2608.25659"],
            "needles": [
                "vla", "world-action", "world action", "world model", "gaussian", "4dgs",
                "temporal", "streaming", "visual representations", "confidence-guided", "in-context",
            ],
            "why": (
                "기존 robot foundation model은 큰 visual-language prior를 action head에 연결하면 충분하다고 보기 쉬웠다. "
                "이번 묶음은 그 prior가 실제 action을 바꾸는 근거를 geometry token, recovered visual representation, streaming temporal unit, human-video context, 4D Gaussian object state, dense confidence map으로 분리한다. "
                "APRL은 policy score만 비교하지 말고 각 interface를 지운 뒤 어떤 motor command, contact state, future object pose가 바뀌는지 평가해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Six VLA/WAM papers independently expose spatial, temporal, context, 4D object, and confidence evidence as action interfaces.",
            "lab_action": (
                "같은 manipulation episode에서 Gaussian geometry, recovered VL features, temporal memory, human-video context, object-centric 4D state, confidence map을 하나씩 교란하고 action deviation, contact mismatch, future-object pose error, terminal success 변화를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Manipulation adaptation shifts from offline demonstrations to execution-time embodiment and contact variables",
            "buckets": ["Robot Learning", "Foundation Models"],
            "ids": ["2608.25585", "2608.25864", "2608.26058", "2608.25798", "2608.25872", "2608.25757", "2608.25641"],
            "needles": [
                "retrieval-augmented", "multi-arm", "embodiment", "tactile", "contact",
                "uncertainty", "progress", "event", "affordance", "bimanual",
            ],
            "why": (
                "기존 adaptation은 demo를 얼마나 잘 고르는지나 final success로 끝나는 경우가 많았다. "
                "RA-VLA는 retrieved context가 action으로 번역되는지를 묻고, MA-VLA와 camera-centric action geometry는 arm과 embodiment의 공통 좌표계를 분리하며, TacForcing과 VISTA는 tactile/contact evidence가 action horizon 안에서 새로 들어와야 한다고 본다. "
                "따라서 APRL은 demonstration count가 아니라 retrieval, arm assignment, camera geometry, tactile refresh, contact event, progress와 uncertainty가 어느 시점에 행동을 바꾸는지 비교해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Seven robot papers share the same adaptation question across retrieval, multi-arm allocation, embodiment geometry, tactile feedback, contact attention, and online uncertainty.",
            "lab_action": (
                "LIBERO/RoboCasa와 bimanual contact tasks에서 retrieved example, arm-specific prompt, camera-centric action geometry, tactile refresh rate, visual contact deformation, progress signal, uncertainty signal을 독립 변수로 두고 recovery timing, contact error, action discontinuity, terminal success를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "3D and localization evaluation moves from clean reconstruction to robot-usable degradation contracts",
            "buckets": ["3D/Scene", "Embodied AI"],
            "ids": ["2608.25401", "2608.25418", "2608.25483", "2608.25135", "2608.25427", "2608.25799", "2608.25274", "2608.25642", "2608.26050"],
            "needles": [
                "pose", "intrinsics", "viewpoint", "lidar", "odometry", "calibration",
                "localization", "navigation", "underwater", "orchard", "degradation", "gnss",
            ],
            "why": (
                "3D/SLAM 성능을 깨끗한 novel-view 품질이나 평균 trajectory error로만 보면 배포 조건에서 어떤 가정이 무너지는지 놓친다. "
                "PIVOT은 pose와 intrinsics, 다른 camera path를 시험하고, LiDAR-SAM2는 4D LiDAR label을 video foundation model supervision으로 확장하며, underwater Gaussian study와 tilted-surface calibration, Super Odometry 2.0, AGRO-Nav, OpenCVL, EgoNav는 물, 경사, 악천후, orchard topology, cross-view localization, local control을 stress condition으로 만든다. "
                "로봇용 map 평가는 visual quality보다 calibration perturbation, sensor degradation, route following, recovery curve를 함께 봐야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Nine geometry/localization papers cover pose, intrinsics, LiDAR labels, underwater regimes, calibration, odometry resilience, orchard maps, CVL, and geometry-aware navigation.",
            "lab_action": (
                "3DGS map, point-cloud map, odometry fusion, orchard graph map, cross-view localization, learned waypoint navigation을 pose noise, calibration reuse, turbidity, low light, tilted ground, vegetation deformation 조건에서 localization drift, route deviation, collision risk, recovery time으로 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Driving and multi-robot safety shifts from outcome labels to pre-commitment risk trajectories",
            "buckets": ["Autonomous Driving", "Safety/Alignment"],
            "ids": ["2608.25344", "2608.25935", "2608.25142", "2608.26002", "2608.26074", "2608.25917", "2608.25690"],
            "needles": [
                "risk", "anomaly", "traffic", "driving", "interaction", "intent", "game",
                "topology", "trust", "rollout", "spoofing", "trajectory",
            ],
            "why": (
                "자율주행과 multi-robot planning을 collision이나 final success로만 평가하면 이미 회복 가능한 시간이 지나간 뒤에야 실패를 알게 된다. "
                "CoRE와 TAU-Agent는 temporal/entity evidence와 retrieval evidence를 뽑고, SkyDrive와 DESCENT는 새 도시와 airport topology에서 planner가 무엇을 배워야 하는지 묻고, Gating Before Commitment와 game-structure 측정은 intent divergence가 plan commitment 전에 드러나는지 본다. "
                "Trust-aware rollout planning까지 합치면 APRL의 safety 평가는 risk evidence lead time, repair window, constraint violation, assignment influence를 같은 trajectory 안에서 비교해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Seven autonomy papers independently move risk evidence into temporal regions, object tracks, aerial adaptation, topology, intent divergence, game structure, and trust monitors.",
            "lab_action": (
                "Ambiguous merges, emergency-like traffic, airport surface crossings, city-domain shifts, spoofed multi-robot assignments을 replay하고 temporal evidence onset, intent divergence, topology constraint violation, repair lead time, near-miss, planner correction value를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "VLM reliability moves from fluent answers to verifiable visual evidence units",
            "buckets": ["Foundation Models"],
            "ids": ["2608.24966", "2608.25299", "2608.25580", "2608.25529", "2608.26105", "2608.26091", "2608.25630", "2608.25375"],
            "needles": [
                "hallucination", "verifiable", "rubric", "instruction following", "visual reasoning",
                "rag", "grounding", "retrieval", "faithfulness", "evidence", "benchmark",
            ],
            "why": (
                "VLM이 자연스럽게 답한다고 해서 visual evidence가 맞는 것은 아니다. "
                "LLaVA hallucination-head 진단은 어떤 attention head가 없는 object를 부르는지 겨냥하고, PointRL은 point-level grounding을 검증 가능한 annotation evidence로 학습하며, V-Rubrics와 Video-IFBench는 answer quality를 atomic visual facts와 instruction constraint로 쪼갠다. "
                "VBVR-Pro, PlanSightRAG, SeVeR까지 보면 visual reasoning은 fluent answer보다 point, proposition, retrieved region, rubric, verifier가 실제로 맞는지로 평가해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Eight VLM papers share verifiable evidence units across hallucination heads, point grounding, rubrics, video instruction following, native visual reasoning, RAG, and 3D medical QA.",
            "lab_action": (
                "Object hallucination, point grounding, video instruction following, plan compliance, 3D medical QA, UI or robot grounding cases에서 direct answer와 evidence-unit answer를 비교해 unsupported-object rate, point coverage, rubric violation, retrieved-region hit rate, action-permission error를 평가한다."
            ),
            "limit": 6,
        },
        {
            "title": "Deployment efficiency shifts from compression score to auditable evidence preservation",
            "buckets": ["Efficiency/Systems", "Foundation Models"],
            "ids": ["2608.25332", "2608.25068", "2608.25495", "2608.25539", "2608.25622", "2608.26083", "2608.25940", "2608.24935", "2608.25178"],
            "needles": [
                "pruning", "lightweight", "low-latency", "quantised", "verifier", "auditable",
                "concept", "benchmark", "redundancy", "embedded", "runtime", "semantic communication",
            ],
            "why": (
                "압축 연구가 FLOPs나 latency만 줄이면 현장 모델이 어떤 evidence를 잃었는지 설명하지 못한다. "
                "Head-aware pruning과 SHIFT-LLM은 어떤 head나 residual correction이 필요한지 묻고, PoseOFF와 sidewalk extraction은 low-latency perception이 실제 HRI나 navigation decision에 충분한지 본다. "
                "CropCop, verifier-grounded video-editing planner, ICON decomposition, physical-AI benchmark redundancy는 runtime artifact, executable plan, concept shortcut, benchmark overlap까지 검증 대상으로 끌어온다."
            ),
            "confidence": "High",
            "confidence_note": "Nine deployment papers connect pruning, correction, low-latency HRI, quantized runtime artifacts, verifiers, concept explanations, benchmark redundancy, and embedded navigation.",
            "lab_action": (
                "Token/head pruning, depth-pruning correction, quantized plant model, low-latency HRI flow, embedded sidewalk navigation, verifier-grounded planner를 같은 deployment cases에서 evidence loss, shortcut exposure, verifier rejection, action anticipation delay, navigation error, benchmark-redundancy sensitivity로 비교한다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Permission-to-act interface ablation suite",
            "claim": (
                "Corrupt geometry tokens, temporal memory, retrieval context, tactile events, and uncertainty signals independently; measure which signal changes action choice before failure."
            ),
        },
        {
            "title": "Robot-usable map degradation protocol",
            "claim": (
                "Evaluate 3DGS, odometry fusion, graph navigation, and cross-view localization under pose, calibration, turbidity, low-light, tilted-ground, and vegetation deformation stress."
            ),
        },
        {
            "title": "Pre-commitment risk evidence benchmark",
            "claim": (
                "Replay driving and multi-robot interaction failures with annotated evidence onset, intent divergence, topology constraints, trust scores, repair lead time, and constraint violation."
            ),
        },
    ],
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def all_papers(classified: dict) -> list[dict]:
    rows = []
    for bucket, info in classified.get("buckets", {}).items():
        for paper in info.get("papers", []):
            q = dict(paper)
            q["bucket"] = bucket
            rows.append(q)
    return rows


def abstract_card(paper: dict, ri_lookup: dict) -> dict:
    text = " ".join(str(paper.get("abstract", "")).split())
    return {
        "arxiv_id": paper.get("arxiv_id"),
        "title": paper.get("title"),
        "bucket": paper.get("bucket"),
        "reading_depth": ri_lookup.get(paper.get("arxiv_id"), "abstract-only"),
        "problem": text[:360],
        "method": "See Research Intelligence edition for abstract evidence trace and falsification note.",
        "meaning": "Included because it supports today's permission-to-act and deployable-evidence thesis.",
    }


def enrich_insights() -> None:
    insights_path = ROOT / "insights" / f"{DATE}.json"
    trends = load_json(ROOT / "trends" / f"{DATE}.json")
    insights = load_json(insights_path)
    classified = load_json(ROOT / "out" / "classified.json")
    papers = all_papers(classified)
    by_id = {p["arxiv_id"]: p for p in papers}
    ri = RI_BY_DATE[DATE]
    ri_ids = [paper["arxiv_id"] for paper in ri["papers"]]
    ri_lookup = {paper["arxiv_id"]: paper["status"] for paper in ri["papers"]}

    insights["source_listing_date"] = trends["source_listing_date"]
    insights["source_mode"] = trends["source_mode"]
    insights["daily_new_counts"] = trends["daily_new_counts"]
    insights["paper_autopsies"] = [abstract_card(by_id[pid], ri_lookup) for pid in ri_ids if pid in by_id]
    insights["frontier_memory"] = ri["frontier_memory"]
    insights["strategy_board"] = ri["strategy"]
    insights["tiering_note"] = (
        "Research Intelligence uses repository parser abstracts for selected Tier A papers. "
        "No figure/table/full-text claims are asserted in this conservative automation run."
    )
    insights["research_intelligence"] = {
        "html": f"posts/{DATE}-research-intelligence.html",
        "json": f"intelligence/{DATE}.json",
        "source_prompt": ri["source_prompt"],
    }
    write_json(insights_path, insights)


def add_ri_callout() -> None:
    post_path = ROOT / "posts" / f"{DATE}.html"
    doc = post_path.read_text(encoding="utf-8")
    if "ri-callout" in doc:
        return
    doc = doc.replace(
        ".thesis strong{color:#fef08a}",
        ".thesis strong{color:#fef08a}.ri-callout{display:flex;justify-content:space-between;gap:16px;align-items:center;margin:-12px 0 28px;padding:14px 18px;border:1px solid #67e8f9;border-radius:10px;background:#ecfeff;color:#164e63}.ri-callout a{font-weight:750;white-space:nowrap}@media(max-width:760px){.ri-callout{align-items:flex-start;flex-direction:column}}",
    )
    ri = RI_BY_DATE[DATE]
    ri_callout = (
        f"<section class=\"ri-callout\"><span><strong>Today's Research Intelligence</strong> "
        f"Tier A {len(ri['papers'])} papers are conservative abstract-only cards with evidence traces, "
        f"adversarial reads, frontier memory, and APRL strategy board.</span>"
        f"<a href=\"{DATE}-research-intelligence.html\">Open Research Intelligence</a></section>"
    )
    doc = re.sub(r"</section>\n(<h2>.*?</h2>)", f"</section>\n{ri_callout}\n\\1", doc, count=1, flags=re.S)
    post_path.write_text(doc, encoding="utf-8", newline="\n")


def main() -> int:
    build(PROFILE, "out/cv_new.json", "out/ro_new.json")
    build_research_intelligence()
    enrich_insights()
    add_ri_callout()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
