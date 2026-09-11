#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-09-11 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260911 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-11"


PROFILE = {
    "date": DATE,
    "weekday": "Fri",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching 2026-09-11 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-09-11 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "The 2026-09-11 batch says robot intelligence is becoming a transition-accountability problem: a model should act only "
        "when the evidence behind a memory, generated future, geometry map, or safeguard has survived the condition that will break deployment. "
        "VLA papers test robotized human video, single-step action generation, frozen predictive-state failure readouts, long-horizon memory plans, "
        "transition realizability, and differentiable safety constraints. Geometry papers ask whether 3DGS, radar, monocular SLAM, street language fields, "
        "and deformable registration still carry metric or semantic evidence under haze, occlusion, low-cost cameras, or sparse sensing. "
        "Generative and VLM papers then move evaluation from visual fluency toward ego-motion consistency, topological planning, hallucination verification, "
        "and query-conditioned evidence routing. APRL should therefore measure not only whether a component improves a benchmark score, but which transition it is authorized to change, "
        "under which failure mode, and when that authority must be revoked."
    ),
    "cluster_takeaway": (
        "Today's core is not bigger VLA, prettier generated worlds, or lighter caches; it is deciding which memory, map, generated frame, verifier, or sensor cue has enough evidence to change the next robot action."
    ),
    "trend_note": (
        "Friday /new produced 128 deduplicated non-replacement papers and 104 ROI papers. "
        "Generation and Robot Learning are the largest buckets, but the APRL-relevant movement is the shared permission test: "
        "transition memory, single-step actions, relocalization geometry, physical hazards, and routed visual evidence must prove their authority before deployment."
    ),
    "cluster_specs": [
        {
            "title": "VLA execution shifts from bigger action heads to evidence-grounded transition contracts",
            "buckets": ["Robot Learning", "Foundation Models", "Safety/Alignment"],
            "ids": ["2609.10706", "2609.10915", "2609.11445", "2609.11308", "2609.11561", "2609.11875"],
            "needles": [
                "vision-language-action", "vla", "robotized human videos", "single-step action",
                "failure signals", "predictive states", "memory-grounded", "transition realizability",
            ],
            "why": (
                "기존 VLA 평가는 더 큰 backbone이나 더 많은 demonstration을 넣으면 action quality가 오른다고 읽기 쉬웠지만, 이번 묶음은 action이 바뀌기 전에 어떤 transition evidence가 충분한지 묻는다. "
                "HuRo는 human video를 robot-aligned supervision으로 바꾸는 단계 자체를 검증하고, IMLE-VLA는 diffusion sampling을 single-step cIMLE action head로 대체해 latency와 jerk를 줄인다. "
                "FARM, 2AM, MaP-WAM, UniMPA는 failure readout, agent-side memory, segment plan, visual-action memory bank가 실제 transition을 허가하는지를 따진다. "
                "APRL은 final success만 보지 말고 transition ambiguity, memory retrieval, warning lead time, action throughput, OOD shift를 같은 episode에서 분리해 평가해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Six papers independently target robotized pretraining, single-step action generation, predictive failure states, agent memory, long-horizon plans, and action-grounded transition memory.",
            "lab_action": (
                "LIBERO/RoboCasa와 실제 tabletop task에서 robotized-human-video scale, action-head sampling step, predictive-state warning, memory-bank retrieval, transition-progress calibration을 ablation하고 OOD success, jerk, warning lead time, phase-transition error, recovery success를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Robot geometry moves from pretty maps to relocalization and sensor-survival evidence",
            "buckets": ["3D/Scene", "Autonomous Driving", "Generation", "Efficiency/Systems"],
            "ids": ["2609.11079", "2609.11766", "2609.10756", "2609.11616", "2609.11894", "2609.11223", "2609.11472"],
            "needles": [
                "relocalization", "3d gaussian splatting", "visual-slam", "radar depth",
                "language fields", "mmwave radar", "deformable registration", "haze",
            ],
            "why": (
                "3D/SLAM/reconstruction은 더 선명한 rendering을 만드는 문제로만 보면 robot deployment에서 언제 깨지는지 알기 어렵다. "
                "RIDE는 3DGS relocalization correspondence를 dense metric depth 보정에 쓰고, greenhouse Visual-SLAM은 monocular camera와 GLOMAP/HLoc로 가려진 tomato의 3D 위치를 복원한다. "
                "GRADE, LangStreet, radar point splatting, Tri-DehazeGS, BridgeMatch는 smoke, view-conditioned street splats, mmWave sensing, haze, deformable correspondence처럼 RGB가 약해지는 조건에서 geometry evidence가 살아남는지 묻는다. "
                "APRL geometry 평가는 photometric fidelity가 아니라 relocalization recovery, depth drift, semantic persistence, low-cost sensing, downstream action change로 판단해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Seven papers connect 3DGS, monocular SLAM, radar depth, street Gaussian semantics, mmWave view synthesis, haze-aware GS, and deformable registration to robot-usable geometry.",
            "lab_action": (
                "Corridor, greenhouse, smoke/low-light room, street-map, and deformable-object scenes에서 3DGS scale, PnP inlier density, monocular map quality, radar conditioning, semantic-anchor persistence, and correspondence pruning을 바꿔 relocalization failure, depth drift, semantic map decay, obstacle distance error, task success를 평가한다."
            ),
            "limit": 6,
        },
        {
            "title": "Embodied safety becomes a question of physical consequences before final task success",
            "buckets": ["Embodied AI", "Autonomous Driving", "Safety/Alignment", "Robot Learning", "Efficiency/Systems"],
            "ids": ["2609.10895", "2609.10951", "2609.11549", "2609.10726", "2609.11697", "2609.11225", "2609.11920"],
            "needles": [
                "hazard", "reactive decision", "formal verification", "operational data",
                "risk", "constraint enforcement", "closed-loop", "event-based",
            ],
            "why": (
                "Safety를 offline score나 마지막 성공 여부로만 보면, robot이 실제로 언제 위험한 행동을 선택했는지 놓친다. "
                "ReactHuman은 sudden household hazard에서 MLLM의 committed plan을 물리적으로 실행하고, steering verification은 주행하지 않은 disturbance 사이 조건을 bound propagation으로 본다. "
                "ADS operational-data 규정, hazardous exploration valuation, ActSafeGuard, Harness Robotic OS, EVPeriscope는 각각 field operation, information-risk, hard constraints, traceable runtime, degraded-sensor cooperation을 safety evidence로 만든다. "
                "APRL은 safety claim을 collision-free 평균이 아니라 reaction timing, constraint violation, risk-taking value, operational scenario reuse, and recovery authority로 분리해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Seven papers align around physical hazard reaction, formal between-test verification, operational safety data, hazardous exploration, action constraints, deployed inspection loops, and cross-robot perception.",
            "lab_action": (
                "Household hazard, CARLA steering, warehouse inspection, hazardous exploration, and ground-aerial navigation scenes에서 reaction deadline, disturbance intensity, information-risk objective, hard constraint layer, sensor occlusion, and runtime update gate를 ablation하고 physical harm proxy, lane departure, intervention count, mission survival, trace replayability를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Generative world models are being tested on physical rules instead of visual fluency",
            "buckets": ["Generation", "3D/Scene", "Foundation Models", "Efficiency/Systems"],
            "ids": ["2609.11172", "2609.11242", "2609.11900", "2609.11499", "2609.11265", "2609.11804"],
            "needles": [
                "physical consistency", "ego-motion", "think-with-video", "topological",
                "recursive scene", "uncertainty collapse", "visual autoregressive",
            ],
            "why": (
                "Video/image generation 평가는 더 보기 좋은 frame을 만드는지만으로 embodied planning에 충분하지 않다. "
                "EgoGenEval은 camera motion grounding과 scene state preservation을 분리하고, VWG-Bench는 video generator가 symbolic rule과 physical law를 따르는지 묻는다. "
                "MindTopo는 topology reasoning과 closed-loop planning을 나누고, RCWM은 recursive scene programs로 world construction을 명시하며, Uncertainty DMD와 Logit Refiner는 rollout root의 다양성 붕괴와 same-scale dependency 손실을 드러낸다. "
                "APRL은 generated observation을 reward, planner prior, or simulator로 쓰기 전에 topology, ego-motion, contact-relevant state, and temporal diversity가 유지되는지 검증해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Six papers separately test ego-motion consistency, video reasoning, topological planning, recursive scene construction, AR-video diversity, and token dependency in generated worlds.",
            "lab_action": (
                "Generated robot-view rollouts에서 camera-motion path, object identity, topology relation, contact state, first-chunk stochasticity, and intra-scale spatial dependency를 intervention으로 두고 planner action flip, scene-state preservation, rule violation, temporal diversity, downstream recovery를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Efficient multimodal agents turn memory and cache budgets into evidence-routing policies",
            "buckets": ["Efficiency/Systems", "Foundation Models", "Safety/Alignment", "Generation"],
            "ids": ["2609.11899", "2609.11582", "2609.10798", "2609.11081", "2609.11516", "2609.11244"],
            "needles": [
                "frames-on-demand", "kv cache", "modality uncertainty", "propagation",
                "visual token", "hallucination detection", "routing", "cache memory",
            ],
            "why": (
                "효율화는 이제 token, cache, summary를 줄이는 기술이 아니라 어떤 evidence를 미래 decision까지 남길지 고르는 정책이다. "
                "Caption-once Frames-on-Demand는 query가 pixel을 실제로 필요로 할 때만 keyframe을 부르고, OmniKVQuant는 omni-modal cache에서 temporal key drift와 modality-specific value geometry를 분리한다. "
                "RiVaT-Fuse는 scalar confidence 대신 matrix-valued trust geometry를 쓰고, TailProp, LoopVAE, OmniHallu는 propagation regime, recurrent tokenization, cross-modal claim verification을 evidence 보존 문제로 바꾼다. "
                "APRL은 edge robot perception에서 latency만 줄이지 말고 decisive cue recall, modality trust, cache drift, hallucination detector precision, and action error를 함께 봐야 한다."
            ),
            "confidence": "Medium-High",
            "confidence_note": "Six papers share evidence routing under frame, cache, modality, token, propagation, and hallucination-verifier budgets, although task domains vary.",
            "lab_action": (
                "Long video inspection, multimodal robot QA, and streaming control episodes에서 frame retrieval gate, KV bit-width, modality trust matrix, recurrent visual token depth, propagation regime, and hallucination verifier를 ablation하고 decisive-cue recall, cache drift, answer flip, latency, privacy/risk error, action success를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Dexterous and morphable robots move from data scale to reusable contact structure",
            "buckets": ["Robot Learning", "Embodied AI", "Safety/Alignment"],
            "ids": ["2609.11753", "2609.11775", "2609.11361", "2609.11553", "2609.11043", "2609.11357"],
            "needles": [
                "dexterous", "contact", "humanoid", "morphology", "locomotion",
                "temporal logic", "underactuated", "exoskeleton",
            ],
            "why": (
                "Contact-rich robotics는 더 큰 policy나 더 많은 demonstration으로만 풀기 어렵고, 어떤 physical structure를 재사용할 수 있는지 밝혀야 한다. "
                "SEED-UMI는 human과 robot이 같은 exoskeleton을 공유해 contact-rich demonstration의 measurement frame을 맞추고, pen-writing controller는 real-time Jacobian estimation으로 simulation이나 precollected demonstration 없이 in-hand writing을 시작한다. "
                "GeoTrussRover, CAP, LTLDiff, morphology-aware retargeting은 morphology, corrupted depth, temporal logic, wheeled-humanoid embodiment가 policy보다 먼저 구조화해야 할 제약임을 보여준다. "
                "APRL은 dexterity와 locomotion을 data volume 경쟁으로만 보지 말고 contact topology, shared measurement, perception corruption, action-order logic, embodiment-invariant subgoal을 실험 축으로 삼아야 한다."
            ),
            "confidence": "Medium-High",
            "confidence_note": "Six robot papers connect shared exoskeleton sensing, online Jacobian control, variable morphology, depth-denoising locomotion, temporal-logic manipulation, and humanoid retargeting.",
            "lab_action": (
                "Dexterous hand, wheeled-humanoid, quadruped, and multi-agent manipulation tasks에서 shared exoskeleton frame, online Jacobian update, contact topology, depth corruption level, LTL action ordering, and morphology parameter를 바꿔 contact stability, transfer success, recovery cost, safety violation, embodiment generalization을 비교한다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Transition-accountability grid for VLA control",
            "claim": (
                "Compare robotized human-video scale, single-step action heads, predictive-state failure readouts, memory banks, and hard constraints on the same transition failure families."
            ),
        },
        {
            "title": "Sensor-survival geometry protocol",
            "claim": (
                "Evaluate 3DGS, radar depth, monocular SLAM, street language fields, and event-based localization by relocalization, depth drift, semantic persistence, and downstream action success."
            ),
        },
        {
            "title": "Physical-consequence permission tests",
            "claim": (
                "Use executable hazard scenes, between-test formal bounds, ego-motion rollouts, and topological tasks to decide when model evidence may change action."
            ),
        },
        {
            "title": "Evidence-routing benchmark for efficient robot agents",
            "claim": (
                "Measure whether frame retrieval, KV quantization, modality fusion, recurrent tokenization, and hallucination verification preserve decisive cues under compute budgets."
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
        "meaning": "Included because it supports today's transition-accountability and evidence-permission thesis.",
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
