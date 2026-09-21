#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-09-21 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260921 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-21"


PROFILE = {
    "date": DATE,
    "weekday": "Mon",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching Monday 2026-09-21 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching Monday 2026-09-21 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "The 2026-09-21 batch says robot intelligence is moving from final success labels to early evidence timing. "
        "VLA reliability papers turn distribution shift, safety stage, proprioceptive deviation, and semantic commitment into signals that must appear before a rollout is unrecoverable. "
        "Contact-rich manipulation papers make tactile, force, deformation, and hidden physical properties into predicted state variables rather than passive feedback. "
        "Geometry and mapping papers ask what visual, geometric, semantic, or low-light evidence is worth collecting before pose, map, view, or navigation commitments are trusted. "
        "Social navigation and recovery papers then make the intervention decision explicit: a robot must know when to ask, slow down, recover, preserve control authority, or change evidence sources. "
        "APRL should build assets where every module reports the first observable cue that should change the robot's decision, not only whether the final task succeeded."
    ),
    "cluster_takeaway": (
        "Today's core is not bigger VLAs, richer tactile sensors, or prettier maps; it is deciding which early evidence is strong enough to change, defer, recover, or explain robot action."
    ),
    "trend_note": (
        "Monday /new produced 197 deduplicated non-replacement papers and 166 ROI papers. "
        "The usable signal concentrates around failure-timed VLA evaluation, contact-state forecasting, evidence-budgeted mapping, dynamic social navigation, world-model repair, and recovery authority."
    ),
    "cluster_specs": [
        {
            "title": "VLA evaluation moves from success rate to when failure becomes predictable",
            "buckets": ["Robot Learning", "Foundation Models"],
            "ids": ["2609.21246", "2609.21223", "2609.21369", "2609.21908", "2609.21659", "2609.21942", "2609.21358"],
            "needles": [
                "failure", "safe", "stage", "proprioception", "commitment", "semantic",
                "shift", "ask", "dialogue", "vla", "onset", "diagnosis",
            ],
            "why": (
                "기존 VLA 평가는 성공률이나 OOD 탐지를 끝점처럼 다뤘지만, 오늘 묶음은 실패가 언제 관측 가능해지는지를 묻는다. "
                "VLA-Scope는 shift 자체가 아니라 실행 실패 예측을 목표로 하고, SafeStage는 안전 실패를 rollout 단계별로 나누며, ProTracer는 proprioception으로 가장 이른 deviation 순간을 찾는다. "
                "CommitFlow와 Outcome-Conditioned End-Effector Geometry는 task stage가 물리 조건을 실제로 만족했는지 확인하고, When Should a Failing Robot Ask?는 어떤 sensor evidence가 사람 호출을 정당화하는지 따진다. "
                "따라서 APRL VLA 평가는 최종 success/fail이 아니라 onset, warning, intervention, ask-human timing을 같은 episode trace 안에서 비교해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Shift-aware failure prediction, staged safety, proprioceptive onset, semantic commitment, end-effector geometry, and corrective dialogue all repeat the failure-timing decision.",
            "lab_action": (
                "LIBERO/SimplerEnv와 실제 manipulation episode에서 visual shift, proprioceptive residual, semantic commitment, stage-level safety, end-effector geometry, and sensor-evidence value를 독립 축으로 두고 first-warning time, remaining recovery authority, false stop, false ask, and final task success를 함께 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Contact-rich manipulation makes hidden physical state a prediction target",
            "buckets": ["Robot Learning", "Generation", "Efficiency/Systems"],
            "ids": ["2609.21449", "2609.20980", "2609.21726", "2609.21753", "2609.21751", "2609.21448", "2609.21609", "2609.21803"],
            "needles": [
                "tactile", "contact", "force", "physics", "world model", "deformation",
                "multiphase", "residual", "manipulation", "forecast", "sensorimotor",
            ],
            "why": (
                "Contact-rich 작업은 RGB 관측만으로는 slip, compression, jamming, liquid redistribution 같은 핵심 상태를 늦게 본다. "
                "ME-Dex와 ForeTac-VLA는 tactile을 world/action model의 미래 상태로 예측하려 하고, ZeroTouch와 PSR은 deployment tactile hardware 없이도 contact deformation이나 force-history 표현을 예측하려 한다. "
                "ForceTwin, RMI, Potential-Field Action Representation, contact-mode planning 논문은 물체 속성, liquid-solid coupling, action representation, contact mode가 명목 policy를 언제 수정해야 하는지 드러낸다. "
                "APRL은 tactile sensor를 붙였는지가 아니라 어떤 hidden physical state가 action chunk를 바꾸는지를 평가해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Heterogeneous tactile WAM, tactile VLA forecasting, visual contact estimation, predictive sensorimotor state, physics-informed twins, and multiphase world models share the hidden-state forecasting axis.",
            "lab_action": (
                "Dexterous grasp, insertion, pushing, fabric/object comparison, and liquid-solid manipulation에서 tactile forecast, visual contact deformation, force-property estimate, potential-field action, and contact-mode sequence를 ablation하고 slip lead time, peak force, jamming, recovery timing, and task success를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Geometry systems move from offline reconstruction to evidence-budgeted robot state",
            "buckets": ["3D/Scene", "Generation", "Safety/Alignment"],
            "ids": ["2609.21347", "2609.21516", "2609.21754", "2609.21804", "2609.21114", "2609.21502", "2609.21226", "2609.21219", "2609.21186"],
            "needles": [
                "slam", "reconstruction", "gaussian", "odometry", "relocalization", "active",
                "localization", "view", "confidence", "map", "low-light", "semantic",
            ],
            "why": (
                "Geometry 논문들은 더 좋은 reconstruction 하나보다 로봇이 어떤 evidence를 더 모아야 pose와 map을 믿을 수 있는지로 이동한다. "
                "Cube-Splat은 360도 cubemap 관측을 하나의 pose optimization 계약으로 묶고, 2D GauSS-MI는 active view를 visual/geometric quality와 onboard compute 사이에서 선택한다. "
                "SFVO, VideoReloc, Noctif3R, event geo-localization, SLIM-init은 confidence-guided correspondence, adaptive clip length, photon-limited real-time SLAM, viewpoint variance, degenerate initialization을 실제 배포 조건으로 끌어낸다. "
                "APRL geometry 평가는 rendering score보다 evidence gained per compute, wrong pose lead time, and downstream navigation/manipulation failure를 함께 봐야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Panoramic GS-SLAM, active 2DGS reconstruction, confidence-guided VO, semantic relocalization, low-light SLAM, and event/VIO localization all repeat the evidence-budget problem.",
            "lab_action": (
                "RGB-D/Gaussian, panoramic, stereo-flow, low-light monocular, event-camera, and semantic-scene-graph sequences에서 next-view choice, confidence threshold, clip length, illumination level, viewpoint gap, and initialization degeneracy를 stress split으로 만들고 localization failure, map-update harm, query ambiguity, and navigation success를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Navigation benchmarks expose social response, map-language grounding, and evidence acquisition as separate variables",
            "buckets": ["Embodied AI", "Foundation Models", "Generation", "Robot Learning", "3D/Scene"],
            "ids": ["2609.21316", "2609.21504", "2609.21838", "2609.20983", "2609.21008", "2609.21792", "2609.21212"],
            "needles": [
                "navigation", "vln", "pedestrian", "social", "population", "map", "route",
                "traversability", "belief", "audio", "search", "pose", "memory",
            ],
            "why": (
                "Navigation 논문들은 goal reaching 하나로는 부족하고, 지도-언어 grounding, pedestrian response, traversability physics, temporary obstacle belief, audio distress cue를 따로 봐야 한다고 말한다. "
                "NaViRRator는 human-readable map의 route scaffold와 egocentric VLN instruction을 분리하고, DPed-VLN과 PopNavShift는 dynamic pedestrian과 population shift가 social compliance를 바꾸는지 본다. "
                "PIVOT, SPARROW, AcousticDiffusion, VNT-PA는 terrain semantics, waiting/rerouting/observing, audio-guided search, pose-attention memory가 route commitment 전에 어떤 evidence를 제공하는지 묻는다. "
                "APRL navigation 평가는 route success뿐 아니라 어떤 evidence source가 잘못된 commitment를 막았는지 기록해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Map-image route grounding, dynamic pedestrian VLN, behavioral population shift, off-road traversability, temporary obstacle POMDPs, audio-guided rescue, and pose-attention navigation converge on evidence acquisition.",
            "lab_action": (
                "Human-readable-map VLN, Habitat pedestrian VLN, off-road traversability, temporary-obstacle graph routing, search-and-rescue audio navigation, and repeated-depth-keyframe navigation에서 route scaffold error, pedestrian population, terrain physics label, wait/reroute observation, audio semantic prior, and pose-memory retrieval을 ablation하고 wrong commitment, social violation, detour cost, and recovery success를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "World models become controllable evaluation instruments rather than passive future predictors",
            "buckets": ["Generation", "Efficiency/Systems", "Robot Learning"],
            "ids": ["2609.20892", "2609.21474", "2609.21712", "2609.21155", "2609.21787", "2609.22055", "2609.21482", "2609.21740"],
            "needles": [
                "world model", "wam", "closed-loop", "servo", "action", "simulation",
                "repair", "audit", "continual", "rollout", "intervention", "recurrent",
            ],
            "why": (
                "World model 논문들은 미래를 그럴듯하게 맞히는 것보다, 어떤 rollout이 실제 control이나 repair decision을 바꾸는지 묻는다. "
                "WM-VS는 prediction-control mismatch를 closed-loop visual servoing 좌표로 바꾸고, MT-WAM은 one-pass predictive representation을 action generation 쪽으로 재지향한다. "
                "ZYT-World는 real-time controllable driving simulation을 production constraint로 걸고, Same World Different Knowledge와 Compact but Moving은 isolated repair와 intervention geometry가 shared-module deployment에서 어떻게 달라지는지 본다. "
                "APRL은 world model을 policy generator가 아니라 failure hypothesis generator로 쓰고, generated rollout이 어떤 action correction을 정당화하는지 검증해야 한다."
            ),
            "confidence": "Medium",
            "confidence_note": "Servo-aligned WMs, WAM action representation, controllable driving simulation, repair audits, recurrent intervention geometry, continual-learning WMs, and uncertainty rollout truncation share control-facing evaluation but span several settings.",
            "lab_action": (
                "Visual servoing, manipulation WAM, autonomous-driving simulation, recurrent world-model repair, and continual compositional tasks에서 progress coordinate, action-oriented representation, scene revisit identity, shared faulty information, intervention rank, and rollout uncertainty를 ablation하고 closed-loop error reduction, repair transfer, latency, and task success를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Recovery and safety shift from post-hoc vetoes to preserving control authority",
            "buckets": ["Autonomous Driving", "Safety/Alignment", "Robot Learning"],
            "ids": ["2609.21690", "2609.22075", "2609.21220", "2609.21130", "2609.20982", "2609.21580", "2609.21211"],
            "needles": [
                "recovery", "safe", "safety", "barrier", "intervene", "authority", "attack",
                "action-space", "trajectory", "chance", "constraint", "readiness",
            ],
            "why": (
                "Safety papers are moving from a final veto to whether the controller still has authority to recover. "
                "RAYA states that predicting failure is insufficient if the nominal plan has already spent recovery authority, and LIMBO internalizes barrier objectives into whole-body control rather than leaving safety as an external certificate. "
                "Noise-space steering, SAGE, ASGARD, Tilt as a Certified Resource, and stochastic swept-volume planning all separate nominal command, residual/gradient correction, action-space attacks, wrench-rate readiness, and chance-constrained collision models. "
                "APRL safety tests should measure remaining intervention authority and false-conservatism, not only collision avoidance."
            ),
            "confidence": "High",
            "confidence_note": "Recovery timing, learned barrier objectives, deployment-time steering, CBF-filtered collaboration, UAV action-space defense, multirotor readiness, and chance-constrained planning all make control authority explicit.",
            "lab_action": (
                "Mobile navigation, UAV, humanoid/whole-body control, HRC, and manipulation planners에서 warning latency, barrier activation, residual steering budget, attack overwrite severity, wrench-rate readiness, and collision-model uncertainty를 stress split으로 만들고 recovery success, false stop, task delay, and unsafe execution을 비교한다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Early-evidence failure timing benchmark",
            "claim": (
                "One manipulation and one navigation suite should log visual shift, proprioceptive onset, tactile forecast, map confidence, social response, and human-query value before final failure."
            ),
        },
        {
            "title": "Contact-state correction authority",
            "claim": (
                "Treat tactile, force, deformation, and hidden physical property forecasts as separate channels that can override or delay nominal VLA action chunks."
            ),
        },
        {
            "title": "Evidence-budgeted mapping for robot decisions",
            "claim": (
                "Active view, confidence-guided odometry, semantic relocalization, and low-light SLAM should be evaluated by decision evidence gained per compute and time."
            ),
        },
        {
            "title": "Social navigation population-shift stress test",
            "claim": (
                "Combine DPed-VLN and PopNavShift-style pedestrian populations with map-language route scaffolds to test whether social compliance survives behavioral shifts."
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
        "meaning": "Included because it supports today's early-evidence timing thesis.",
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
