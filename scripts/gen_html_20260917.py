#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-09-17 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260917 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-17"


PROFILE = {
    "date": DATE,
    "weekday": "Thu",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching Thursday 2026-09-17 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching Thursday 2026-09-17 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "The 2026-09-17 batch says robot learning is becoming an evidence-contract discipline. "
        "VLA papers no longer only ask whether a larger backbone performs better; they ask which context example, model layer, action token, future representation, cache, or local fallback is allowed to change the next command. "
        "Geometry papers make a parallel shift: feed-forward 3D, Gaussian splats, LiDAR submaps, sonar local SLAM, radar preprocessing, and physical-property maps now need reliability signals that say when a robot should trust or reject the state. "
        "Navigation papers turn hand gaze, semantic maps, grounded landmarks, geometric memory, and social response into evidence gathered before committing motion. "
        "Contact-rich manipulation papers split nominal task motion from force, tactile, energy, morphology, and generated physics corrections. "
        "Safety and deployment papers then define the revocation layer: anomaly lead time, omnidirectional trajectory risk, adversarial feature consistency, selective trajectory replacement, Lyapunov safety layers, cloud-local VLA handoff, and activation cache reuse. "
        "APRL should build evaluation assets where every representation declares what robot decision it can change, when that permission is revoked, and what failure evidence would falsify it."
    ),
    "cluster_takeaway": (
        "Today's core is not a bigger VLA, prettier 3D, or faster edge model; it is the contract that decides when context, geometry, force, risk, or local memory can change robot execution."
    ),
    "trend_note": (
        "Thursday /new produced 217 deduplicated non-replacement papers and 179 ROI papers. "
        "The usable signal concentrates around VLA action interfaces, geometry trust gates, active navigation evidence, contact correction, runtime safety, and edge deployment."
    ),
    "cluster_specs": [
        {
            "title": "VLA adaptation moves from larger backbones to measured action interfaces",
            "buckets": ["Robot Learning", "Autonomous Driving", "Efficiency/Systems", "Safety/Alignment"],
            "ids": ["2609.19138", "2609.18084", "2609.18259", "2609.18487", "2609.18623", "2609.17728", "2609.18462", "2609.18016", "2609.18663", "2609.19104"],
            "needles": [
                "vla", "vision-language-action", "action token", "in-context", "adaptation",
                "future", "recurrent action memory", "semantic", "local action", "cache",
            ],
            "why": (
                "기존 VLA 평가는 백본 크기나 평균 성공률을 먼저 보았지만, 오늘 논문들은 실제 명령을 바꾸는 인터페이스를 분리한다. "
                "GPT-Policy는 context compiler와 constrained controller를 연결하고, layer diagnostic 논문은 shift별로 어느 region을 조정해야 하는지 측정하며, M2Tok과 ActionPiece는 action vocabulary가 물리적 관계를 보존하는지 묻는다. "
                "FIVE-VLA, RAF-VLA, CSWAM, VLA-ULAP, rMuscle은 temporal memory, future representation, causal semantic history, local fallback, activation cache가 어떤 action authority를 갖는지 드러낸다. "
                "따라서 APRL VLA 평가는 모델 전체가 아니라 context, layer, token, memory, cache 중 무엇이 명령을 바꿨는지 분리해 평가해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "In-context robot learning, layer-wise adaptation, action tokenization, driving VLA memory, WAM semantics, local fallback, and inference cache papers all target the action interface.",
            "lab_action": (
                "LIBERO, RoboTwin, Bench2Drive, and one physical contact task에서 context examples, tuned layer groups, action-token vocabulary, recurrent action memory, future-aligned representation, semantic history, cloud-call interval, and activation cache를 ablation 축으로 두고 action delta, recovery success, latency, and failure family를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Geometry systems start exposing when maps and 3D predictions should be trusted",
            "buckets": ["3D/Scene", "Autonomous Driving", "Generation", "Efficiency/Systems"],
            "ids": ["2609.18465", "2609.17810", "2609.18473", "2609.18898", "2609.18920", "2609.18628", "2609.18819", "2609.18893", "2609.18088", "2609.18737"],
            "needles": [
                "3d", "gaussian", "slam", "lidar", "sonar", "reconstruction",
                "reliability", "conditioning", "odometry", "submap", "physical property",
            ],
            "why": (
                "3D/SLAM/reconstruction 논문은 좋은 모양을 만드는 데서 그치지 않고, 로봇이 그 geometry를 믿어도 되는 조건을 묻는다. "
                "GeoCond는 low overlap, low parallax, extreme rotation에서 feed-forward 3D confidence가 무너지는지를 gate로 바꾸고, Wind on Trees는 dynamic 4DGS가 photometric fit이 아니라 물리 파라미터와 extrapolation을 회복하는지 시험한다. "
                "CADSplat, NormLift, PhysVGGT는 CAD anchor, semantic feature norm, dense physical property를 robot decision에 연결하고, VIO stress benchmark, SEAM, SOL-SLAM은 sensor degradation, submap evidence, acoustic registration이 언제 local map authority를 가질지 묻는다. "
                "APRL geometry 평가는 pose error나 rendering score보다 map update, localization, grasp planning, navigation recovery를 허가하거나 거부하는 trust gate로 설계되어야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Feed-forward 3D reliability, dynamic 4DGS physical grounding, CAD-aided 3DGS, semantic reliability, physical properties, VIO degradation, lifelong LiDAR mapping, and sonar SLAM repeat the trust-gate decision.",
            "lab_action": (
                "Sparse-view, low-parallax, dynamic-object, subterranean, construction-site, and underwater sequences에서 geometry confidence, CAD anchor strength, semantic reliability, physical-property map, IMU/camera degradation, submap evidence, and sonar-only registration을 stress split으로 만들고 wrong pose, harmful map update, grasp-planning error, and navigation recovery를 함께 평가한다."
            ),
            "limit": 6,
        },
        {
            "title": "Embodied navigation is becoming evidence gathering before motion commitment",
            "buckets": ["Robot Learning", "Embodied AI", "Autonomous Driving", "Safety/Alignment"],
            "ids": ["2609.18548", "2609.17628", "2609.17910", "2609.18058", "2609.18581", "2609.18789", "2609.18776", "2609.18125", "2609.18451", "2609.17834"],
            "needles": [
                "navigation", "route", "grounding", "active perception", "head motion",
                "vln", "social navigation", "terrain", "trajectory", "map",
            ],
            "why": (
                "Navigation 논문들은 이제 policy가 바로 움직이는지보다, 움직이기 전에 어떤 증거를 더 모으고 어떤 공간 목표를 확정하는지를 본다. "
                "HAP와 LEAP는 hand motion과 gaze/active perception이 task evidence를 모으는 방식을 다루고, Map2Route와 Finder는 semantic map과 object-finding loop가 accept/continue/abort 결정을 가져야 한다고 본다. "
                "GroundingVLN과 AdaGeoVLN은 grounded landmark, pixel goal, geometry memory를 motion decision에 연결하고, TRACER와 PRISM은 사람 반응과 interaction trait를 persistent evidence로 유지한다. "
                "VLM-MPPI와 VCTP는 language-selected flight behavior와 vehicle heading/contact terrain이 route commitment를 바꾼다는 점을 보여준다."
            ),
            "confidence": "High",
            "confidence_note": "Egocentric active perception, quadruped gaze, route planning, object finding, grounded VLN, geometry memory, social response, UAV mode selection, and off-road terrain planning share pre-commitment evidence gathering.",
            "lab_action": (
                "Habitat/HM3D, R2R-CE, social-navigation, quadruped terrain, UAV indoor, and off-road route tasks에서 gaze target, semantic route constraint, evidence-gathering step, grounded pixel goal, GFM memory budget, human-response belief, MPPI behavior mode, and wheel-contact surface cost를 조절해 wrong commitment, detour, collision proxy, and recovery cost를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Contact-rich manipulation treats force and embodiment as correction signals",
            "buckets": ["Robot Learning", "Generation"],
            "ids": ["2609.18164", "2609.18174", "2609.18242", "2609.18497", "2609.18504", "2609.18620", "2609.19137", "2609.17540", "2609.18117", "2609.18232"],
            "needles": [
                "force", "tactile", "contact", "dexterous", "grasp", "embodiment",
                "deformable", "energy", "manipulation", "audio",
            ],
            "why": (
                "Contact-rich manipulation은 더 좋은 visual policy 하나로 해결되는 문제가 아니라, nominal action과 physical correction을 분리하는 문제로 읽힌다. "
                "Energy-regularized imitation은 mechanical work를 줄이는 regularizer를 만들고, TacBPM은 tactile-proprioceptive history를 behavior prior로 증류하며, ForceDelta-VLA와 TAO-Force는 force history가 reference action을 언제 어떻게 수정해야 하는지 분리한다. "
                "InterMASH, DeformSmith, Dreaming the Sound of Contact는 cross-embodiment geometry, deformable asset physics, audio-shaped force profile을 통해 contact transfer 조건을 명시한다. "
                "APRL은 force/tactile/morphology cue가 평균 성공률을 올렸는지보다, slip, invalid contact, excessive force, recovery timing 중 무엇을 예측하고 고치는지 평가해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Energy-aware imitation, tactile priors, force-conditioned corrections, force-aware VLA control, cross-embodiment grasp geometry, deformable assets, and audio-derived contact forces converge on correction authority.",
            "lab_action": (
                "Dexterous reorientation, bimanual contact, deformable object manipulation, and grasp transfer tasks에서 mechanical-work penalty, tactile history, force correction, fast-slow admittance branch, morphology token, deformable asset physics, and audio-shaped force profile을 ablation하고 peak force, slip, invalid contact, transfer success, and recovery timing을 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Robot safety shifts toward runtime risk, anomaly, and adversarial revocation",
            "buckets": ["Robot Learning", "3D/Scene", "Safety/Alignment", "Autonomous Driving", "Efficiency/Systems"],
            "ids": ["2609.17843", "2609.18191", "2609.17856", "2609.18451", "2609.18442", "2609.17758", "2609.17834", "2609.18752", "2609.18324"],
            "needles": [
                "anomaly", "risk", "adversarial", "safety", "trajectory", "robust",
                "obstacle", "barrier", "selective", "failure",
            ],
            "why": (
                "Safety 논문들은 정적인 confidence 숫자보다 실행 중 어떤 evidence가 행동 권한을 회수해야 하는지에 집중한다. "
                "RoboVAD는 unseen task와 unseen anomaly type에서 recovery trigger가 얼마나 어려운지 보이고, OmniRisk는 dynamic obstacle velocity에 맞춘 trajectory-level risk를 single pass로 예측한다. "
                "Heterogeneous cooperative perception 공격 논문은 sensor diversity가 자동 방어가 아님을 보이며, HetShield 같은 trust layer가 spatiotemporal consistency를 검증해야 한다고 주장한다. "
                "VLM-MPPI, RiskWorld, CALOS, VCTP는 language-selected UAV behavior, selective trajectory replacement, Lyapunov torque correction, vehicle-conditioned terrain cost처럼 실행 중 plan을 멈추거나 바꾸는 조건을 드러낸다."
            ),
            "confidence": "High",
            "confidence_note": "Manipulation anomaly, quadrotor risk, cooperative perception attacks, language-conditioned UAV planning, risk-aware driving world models, safety layers, and terrain planning all express revocation timing.",
            "lab_action": (
                "Robot-arm manipulation, cooperative driving, quadrotor, UAV indoor, and off-road navigation episodes에서 unseen anomaly type, dynamic obstacle approach velocity, malicious feature injection, language-mode mismatch, predicted collision correction, Lyapunov constraint activation, and wheel-contact cost shift를 별도 stress split으로 만들고 lead time, false stop, recovery success, collision proxy, and task completion을 함께 평가한다."
            ),
            "limit": 6,
        },
        {
            "title": "Edge deployment work asks what evidence survives pruning, caching, and local fallback",
            "buckets": ["Efficiency/Systems", "Robot Learning", "Autonomous Driving"],
            "ids": ["2609.18663", "2609.19104", "2609.18037", "2609.18239", "2609.18056", "2609.18363", "2609.18955", "2609.18139", "2609.18207"],
            "needles": [
                "lightweight", "edge", "pruning", "cache", "efficient", "sparse",
                "local", "latency", "tracking", "parameter",
            ],
            "why": (
                "Efficiency 논문들은 작아지는 것 자체가 아니라, 줄인 뒤에도 어떤 task evidence가 남는지를 묻는다. "
                "VLA-ULAP은 cloud VLA call을 local action predictor가 언제 대체할 수 있는지 측정하고, rMuscle은 반복 factory workload에서 visual-token output과 action activation pattern을 cache한다. "
                "SetPlanner, Unified Response Geometry, Position Anchor Tuning은 frozen SAM prompt, pruning subset, point-cloud token anchor가 downstream behavior를 보존하는지 확인하고, online multi-camera 3D tracking과 KDTwin은 lightweight system이 identity와 driving scene segmentation evidence를 잃지 않는지 본다. "
                "APRL deployment 평가는 latency와 parameter count만 보지 말고, local fallback이나 pruning이 action, tracking, geometry, segmentation decision을 언제 망가뜨리는지 함께 봐야 한다."
            ),
            "confidence": "Medium",
            "confidence_note": "The papers share deployment-budget pressure, but span VLA inference, segmentation prompting, pruning, point-cloud adaptation, tracking, and driving segmentation rather than one benchmark.",
            "lab_action": (
                "Edge VLA, point-cloud adaptation, frozen-SAM instrument segmentation, multi-camera tracking, and lightweight driving segmentation tasks에서 cloud-call interval, cache hit, token anchor count, pruned response subset, prompt-set candidate disagreement, recurrent query memory, and distillation target을 ablation하고 action error, ID switch, Dice/HOTA, latency, energy, and failure recovery를 비교한다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Robot evidence-contract benchmark",
            "claim": (
                "Context examples, action tokens, geometry confidence, force corrections, risk fields, and edge fallback should each declare the decision they can change and the condition that revokes that authority."
            ),
        },
        {
            "title": "Geometry trust gate for robot maps",
            "claim": (
                "Evaluate feed-forward 3D, 3DGS, LiDAR, sonar, and physical-property outputs by downstream map-update, localization, grasp-planning, and navigation recovery decisions."
            ),
        },
        {
            "title": "Contact-correction authority stack",
            "claim": (
                "Separate nominal task motion from force, tactile, energy, morphology, deformable-physics, and audio-shaped correction channels in contact-rich manipulation."
            ),
        },
        {
            "title": "Latency-aware VLA handoff protocol",
            "claim": (
                "Measure when a small local predictor, cache, or action-memory module can safely replace cloud VLA inference without hiding rare dynamic failures."
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
        "meaning": "Included because it supports today's evidence-contract thesis.",
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
