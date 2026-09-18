#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-09-18 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260918 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-18"


PROFILE = {
    "date": DATE,
    "weekday": "Fri",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching Friday 2026-09-18 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching Friday 2026-09-18 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "The 2026-09-18 batch says embodied systems are no longer competing only on better perception or stronger policies; "
        "they are competing on when a representation is allowed to control the robot. "
        "Geometry papers make maps answer for calibration, compute budget, lighting, cross-agent fusion, and query ambiguity before the map is trusted. "
        "Navigation papers separate evidence acquisition from route commitment: active viewpoints, onboard VLN stages, topology memories, target uncertainty, movable-obstacle relocation, and terrain-feeling forecasts all ask what must be known before moving. "
        "Manipulation papers split nominal motion from correction authority through tactile world models, future latents, obstacle-aware coding agents, transparent teleoperation, underwater bimanual data, and residual insertion control. "
        "Safety and deployment papers then define revocation: adversarial VLA states that persist after a patch, vehicle commands that must not execute, reach-avoid-stay filters, scenario generators, V2X validation, hidden-vehicle minimax search, and quantization gates that accept, reject, or defer deployment. "
        "APRL should build evaluation assets where map, language, touch, foresight, safety, and compression modules declare what decision they can change and what evidence removes that authority."
    ),
    "cluster_takeaway": (
        "Today's core is not more 3D, more VLM reasoning, or larger policies; it is the evidence gate that decides when map state, navigation intent, contact correction, safety filters, or compressed deployment models may control execution."
    ),
    "trend_note": (
        "Friday /new produced 232 deduplicated non-replacement papers and 191 ROI papers. "
        "The usable signal concentrates around robot-usable Gaussian maps, evidence-gathering navigation, contact and tactile correction, runtime safety revocation, world-action scenario generation, and deployment degradation gates."
    ),
    "cluster_specs": [
        {
            "title": "Robot maps move from reconstruction output to trust-gated decision state",
            "buckets": ["3D/Scene", "Foundation Models", "Robot Learning", "Efficiency/Systems"],
            "ids": ["2609.19518", "2609.19628", "2609.20348", "2609.20589", "2609.20586", "2609.20235", "2609.19911", "2609.20475", "2609.19876", "2609.20817"],
            "needles": [
                "slam", "gaussian", "mapping", "3d scene", "confidence", "query", "localization",
                "grounding", "rgb-d", "hdr", "calibration", "referring",
            ],
            "why": (
                "기존 3D/SLAM 평가는 pose error나 rendering 품질을 먼저 보았지만, 오늘 묶음은 로봇이 그 map을 언제 믿어도 되는지를 묻는다. "
                "AMB3R-SLAM과 VGGT-GS SLAM은 장거리 계층 consistency와 uncalibrated Gaussian refinement를 다루고, EliGSiR와 RawSLAM은 bounded compute와 HDR lighting에서 online map authority가 어떻게 유지되는지 본다. "
                "CoRef-GS, Scene-Q, CitySTAR, SenseFuse는 fused map과 open-vocabulary 3D query가 ambiguity, semantic mismatch, spatial relation을 만나면 빠른 retrieval을 믿을지 reasoning으로 넘길지 결정해야 함을 보여준다. "
                "따라서 APRL geometry 평가는 reconstruction score가 아니라 map update, localization, 3D query, manipulation planning을 허가하거나 보류하는 trust gate로 설계되어야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Kilometer-scale SLAM, uncalibrated Gaussian SLAM, continual RGB-D mapping, HDR Gaussian SLAM, cooperative referring maps, and confidence-aware 3D querying all repeat the map authority decision.",
            "lab_action": (
                "RGB-D/Gaussian indoor sequence, uncalibrated monocular video, HDR lighting, fused multi-agent map, and large-building floor-plan localization에서 hierarchy level, calibration residual, compute load, HDR exposure, semantic compatibility, and query confidence를 stress split으로 만들고 map-update error, wrong localization, wrong 3D query, and downstream navigation/manipulation failure를 함께 평가한다."
            ),
            "limit": 6,
        },
        {
            "title": "Navigation policies shift from acting immediately to gathering missing evidence",
            "buckets": ["Robot Learning", "Embodied AI", "Autonomous Driving", "Generation"],
            "ids": ["2609.19554", "2609.20191", "2609.20388", "2609.20443", "2609.19541", "2609.19863", "2609.20694", "2609.20277", "2609.20034", "2609.19315"],
            "needles": [
                "navigation", "active perception", "target search", "uncertainty", "route", "relocate",
                "world model", "instruction", "planning", "foresight", "trajectory",
            ],
            "why": (
                "Navigation 논문들은 policy가 바로 움직이는지보다, 움직이기 전에 어떤 증거를 더 모아야 하는지를 분리한다. "
                "VA-Bench는 visual demonstration, active camera, metric control, feedback revision을 한 loop로 묶고, VLN on the Fly는 grounding, 3D goal lifting, planning, control을 inspectable onboard stages로 둔다. "
                "Navi-Agent와 target-search uncertainty 논문은 coordinate-free topology와 spatial/semantic belief를 통해 progress verification과 disambiguation을 분리하고, NAMO와 Feel-WM은 relocation choice와 terrain feel prediction이 route commitment를 바꾼다. "
                "APRL navigation 평가는 최종 success뿐 아니라 어떤 viewpoint, candidate, relocation, proprioceptive forecast가 motion commitment를 정당화하고 실패 회복을 앞당기는지 비교해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Active perception, onboard aerial VLN, coordinate-free navigation, VLM target-search uncertainty, movable-obstacle planning, and off-road world models all target pre-commitment evidence.",
            "lab_action": (
                "VA-Bench style manipulation, aerial VLN, VLN-CE, target search, NAMO, and off-road driving tasks에서 camera viewpoint, 3D goal confidence, topology memory, spatial-semantic EIG, relocation sequence, and proprioceptive future risk를 ablation 축으로 두고 wrong commitment, detour cost, collision proxy, task progress, and recovery cost를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Contact-rich manipulation separates nominal motion from correction authority",
            "buckets": ["Robot Learning", "Safety/Alignment", "Generation"],
            "ids": ["2609.20649", "2609.20669", "2609.20822", "2609.19196", "2609.19200", "2609.20414", "2609.19962", "2609.19688", "2609.19194", "2609.19228"],
            "needles": [
                "tactile", "contact", "manipulation", "dexterous", "teleoperation", "underwater",
                "force", "foresight", "obstacle", "residual", "whole-body",
            ],
            "why": (
                "Manipulation 논문들은 좋은 nominal policy 하나보다, 어떤 correction channel이 언제 행동을 바꿔야 하는지를 묻는다. "
                "DexTouch-WM은 human touch와 robot tactile dynamics를 맞춰 future contact를 예측하고, foresight diffusion policy는 sparse future gripper state로 latent guidance를 만든다. "
                "Obstacle-aware coding agents는 안전 constraint가 trace에 있어도 route/contact planning priority가 되지 않으면 충돌한다는 점을 보이고, DITTO와 ULOHA는 force feedback, bimanual underwater disturbances, action chunking 같은 data-collection and deployment gaps를 드러낸다. "
                "Book insertion과 LYRIC 계열 signal까지 합치면 APRL은 nominal task motion, tactile forecast, obstacle veto, residual correction, embodiment gap을 별도 권한으로 평가해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Tactile world models, future latent guidance, coding-agent safety failures, transparent teleoperation, underwater bimanual learning, and residual insertion control all ask when corrections override nominal motion.",
            "lab_action": (
                "Dexterous manipulation, obstacle-constrained pick/place, book insertion, underwater bimanual transfer, and whole-body contact tasks에서 tactile history, future latent, obstacle veto, force-feedback teleoperation, medium disturbance, residual correction, and morphology gap을 ablation하고 slip, collision, jamming, peak force, recovery timing, and transfer success를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Safety research moves from static constraints to revocation timing",
            "buckets": ["Safety/Alignment", "Robot Learning", "Autonomous Driving", "Embodied AI"],
            "ids": ["2609.19669", "2609.19630", "2609.19449", "2609.20318", "2609.19681", "2609.20480", "2609.20435", "2609.19393", "2609.20103", "2609.20756"],
            "needles": [
                "safety", "adversarial", "risk", "critical", "barrier", "occlusion", "dynamic obstacle",
                "authorization", "recover", "validation", "scenario",
            ],
            "why": (
                "Safety 논문들은 안전 여부를 마지막 collision label로만 보지 않고, 언제 policy authority를 회수해야 하는지로 바꾼다. "
                "VLA adversarial persistence는 patch 제거 뒤에도 recoverability가 망가지는지 측정하고, vehicle voice authorization은 execute/refuse/clarify/confirm/defer/emergency/no-call taxonomy로 tool authority를 분리한다. "
                "Strict reach-avoid-stay CBF와 dynamic obstacle ILP는 runtime intervention 조건을 만들고, AR/VAST/AdvScene/hidden-vehicle search는 driving failure를 찾기 위해 scenario initialization, dynamic map availability, occlusion memory를 조작한다. "
                "APRL safety 평가는 사고 후 설명이 아니라 intervention lead time, false stop, recovery success, and authority revocation reason을 함께 봐야 한다."
            ),
            "confidence": "High",
            "confidence_note": "VLA attacks, LLM authorization, CBF safety filters, AR scenario generation, V2X validation, occlusion minimax search, and dynamic obstacle planning all express revocation timing.",
            "lab_action": (
                "LIBERO, vehicle voice-command, reach-avoid navigation, work-zone driving, V2X occluded intersections, hidden-vehicle scenarios, and dynamic obstacle courses에서 attack removal time, authorization class, CBF activation, generated criticality, dynamic-map availability, occlusion horizon, and planner intervention을 stress split으로 만들고 lead time, false execute, false stop, collision proxy, and recovery success를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "World-action models and scenario generators become closed-loop evaluation instruments",
            "buckets": ["Generation", "Autonomous Driving", "Robot Learning", "Efficiency/Systems"],
            "ids": ["2609.20034", "2609.20377", "2609.20277", "2609.19315", "2609.19347", "2609.20694", "2609.20318", "2609.20103", "2609.20756", "2609.19894"],
            "needles": [
                "world model", "scenario", "long-horizon", "action", "planning", "driving",
                "simulation", "verified", "closed-loop", "teacher", "offline reinforcement",
            ],
            "why": (
                "World model과 scenario generation 논문은 예쁜 미래를 만드는 데서 끝나지 않고, closed-loop failure를 만들어내는 실험 장치가 되고 있다. "
                "Astronex-World, MM-Future, JEPA-WAM, GAVEL, HOPHY는 visual instruction, world-action prediction, graph world models, hypergraph planning을 task execution과 연결하고, AR scene transformation과 AdvScene은 안전한 driving slice를 critical interaction으로 바꾼다. "
                "OPTED와 parking offline RL은 expensive sensor simulation 없이 closed-loop post-training or waypoint action tokens를 다루려 한다. "
                "APRL은 world-action model을 policy generator가 아니라 hypothesis generator로 쓰고, generated scenario가 어떤 failure mode를 실제 closed-loop metric으로 드러내는지 검증해야 한다."
            ),
            "confidence": "Medium",
            "confidence_note": "World-action, graph planning, AR/latent critical scenarios, on-policy driving teachers, and parking action tokens connect generation to closed-loop evaluation but span several benchmarks.",
            "lab_action": (
                "Driving, manipulation, additive manufacturing, off-road mission planning, and long-horizon task planning에서 generated visual instruction, world-action rollout, graph/hypergraph plan, AR-inserted actor, latent initial scene, privileged teacher, and waypoint action token을 비교하고 collision, task completion, plan validity, distribution shift, and sim-to-real transfer를 함께 평가한다."
            ),
            "limit": 6,
        },
        {
            "title": "Deployment efficiency work asks which evidence survives compression or routing",
            "buckets": ["Efficiency/Systems", "Foundation Models", "3D/Scene", "Robot Learning", "Autonomous Driving"],
            "ids": ["2609.19441", "2609.19990", "2609.20299", "2609.19683", "2609.20066", "2609.20160", "2609.20290", "2609.20441", "2609.19745", "2609.20150"],
            "needles": [
                "quantization", "pruning", "routing", "efficient", "low-bit", "sparse", "edge",
                "degradation", "token", "distillation", "transmission",
            ],
            "why": (
                "Efficiency 논문들은 latency나 parameter count를 줄이는 것보다, 어떤 evidence가 남아야 task decision이 유지되는지를 묻는다. "
                "PreDE는 WAM quantization을 closed-loop task degradation accept/reject/defer gate로 바꾸고, QCPruner는 query-relevant visual token evidence를 보존한다. "
                "Dynamic CLIP layer routing은 입력별로 어떤 layer를 신뢰할지 학습하고, MiX, PointEvent, ultra-sparse LiDAR, edge flood distillation은 memory bandwidth, event evidence, sparse occupancy, deployment-size 제약을 task signal 보존 문제로 바꾼다. "
                "APRL deployment 평가는 압축률 하나가 아니라 어떤 representation, token, layer, temporal evidence가 사라질 때 action, map, detection, and OOD decisions가 깨지는지 봐야 한다."
            ),
            "confidence": "Medium",
            "confidence_note": "WAM quantization, token pruning, layer routing, low-bit VLM acceleration, event evidence, and sparse LiDAR all share evidence preservation under budget pressure.",
            "lab_action": (
                "WAM policies, MLLM 3D queries, CLIP OOD detection, edge VLM inference, event-camera tiny-object detection, sparse LiDAR occupancy, and edge segmentation tasks에서 bit width, token budget, routed layer depth, low-bit format, event serialization, voxel sparsity, and distillation target을 ablation하고 task degradation, false confidence, latency, energy, and recovery decision을 비교한다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Robot decision-authority gate",
            "claim": (
                "Map state, VLM query, route choice, tactile forecast, safety filter, and compressed WAM configuration should each expose act/defer/revoke decisions tied to failure evidence."
            ),
        },
        {
            "title": "Gaussian map trust benchmark",
            "claim": (
                "Evaluate Gaussian SLAM and open-vocabulary 3D maps by map-update harm, localization reliability, query ambiguity, and downstream navigation/manipulation decisions."
            ),
        },
        {
            "title": "Evidence-gathering navigation suite",
            "claim": (
                "Separate active viewpoint, spatial-semantic uncertainty, topology memory, relocation sequence, and proprioceptive terrain foresight before scoring route commitment."
            ),
        },
        {
            "title": "Contact correction authority stack",
            "claim": (
                "Treat tactile prediction, future latent, force feedback, obstacle veto, residual correction, and embodiment gap as separate correction channels rather than policy decorations."
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
        "meaning": "Included because it supports today's decision-authority thesis.",
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
