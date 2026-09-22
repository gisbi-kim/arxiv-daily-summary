#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-09-22 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260922 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-22"


PROFILE = {
    "date": DATE,
    "weekday": "Tue",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching Tuesday 2026-09-22 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching Tuesday 2026-09-22 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "The 2026-09-22 batch says robot policies are no longer judged by whether they work once, "
        "but by whether their evidence contract survives counterfactual stress. VLA and driving papers "
        "turn visual perturbation regions, stale cameras, task-semantic swaps, offline compression metrics, "
        "and counterfactual pedestrian edits into closed-loop validation gates. Contact-rich manipulation "
        "papers make touch, wrench, force residuals, and imagined contact futures into authority signals "
        "that can refine or override a nominal action. Geometry and SLAM papers ask when registration, "
        "next-best-view, elevator transport state, predictive frontiers, uncertainty, and wide-view priors "
        "are trustworthy enough to move. Navigation, world-model, and safety papers then expose the hidden "
        "interfaces: phase progress, module dependence, action encoding, simulator queries, safety barriers, "
        "and recovery data must all be tested against the specific command they are allowed to change."
    ),
    "cluster_takeaway": (
        "Today's core is not better backbones or prettier maps; it is deciding which evidence source has the authority to keep, delay, refine, or veto the next robot command."
    ),
    "trend_note": (
        "Tuesday /new produced 455 deduplicated non-replacement papers and 382 ROI papers. "
        "The usable signal concentrates around closed-loop VLA validation, tactile/contact authority, uncertainty-aware geometry, evidence-gated navigation, world-model action contracts, and predictive safety."
    ),
    "cluster_specs": [
        {
            "title": "VLA validation moves from nominal score to counterfactual closed-loop evidence",
            "buckets": ["Robot Learning", "Autonomous Driving"],
            "ids": ["2609.22293", "2609.22582", "2609.24350", "2609.23565", "2609.23048", "2609.23650", "2609.24118"],
            "needles": [
                "robustness", "closed-loop", "trajectory", "counterfactual", "visual evidence",
                "camera", "task-semantic", "compressed", "failure", "vla", "domain shift",
            ],
            "why": (
                "기존 VLA/주행 평가는 clean benchmark score나 sampled corruption으로 안정성을 말했지만, 오늘 묶음은 어떤 counterfactual evidence가 실제 action을 바꾸는지 묻는다. "
                "Validating, Not Sampling은 연속 perturbation region을 검증하고, LIBERO-VPro는 stale camera와 task-relevant scene variation을 closed-loop로 넣으며, Beyond the Leaderboard는 pedestrian edit과 relighting으로 policy profile을 분해한다. "
                "MaskVLA, BAS-VLA, CARE, Closed-Loop Collapse 논문은 trajectory overfitting, semantic-preserving/breaking 변화, recovery state, offline compression gate가 서로 다른 실패 축임을 보여준다. "
                "APRL은 success rate 앞에 perturbation region, stale evidence, semantic swap, action-trace residual, recovery trigger를 독립 gate로 세워야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Region validation, visual robustness benchmark, counterfactual driving diagnosis, semantic calibration, compression collapse, and corrective execution repeat the closed-loop evidence contract.",
            "lab_action": (
                "LIBERO/RoboCasa/NAVSIM류 task에서 brightness/rotation region, camera staleness, local cue disruption, pedestrian counterfactual, task-semantic swap, compression residual, and post-failure correction을 stress split으로 만들고 action change, first failure cue, recovery success, false veto, and task success를 함께 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Contact-rich manipulation turns touch and force into command authority",
            "buckets": ["Robot Learning"],
            "ids": ["2609.24976", "2609.23888", "2609.24068", "2609.24511", "2609.23800", "2609.22840", "2609.23614", "2609.24507"],
            "needles": [
                "tactile", "contact", "force", "wrench", "insertion", "grasping",
                "dexterous", "touch", "residual", "compliance", "contact-rich",
            ],
            "why": (
                "Contact-rich manipulation은 RGB가 보는 상태와 물리적으로 중요한 상태가 다르기 때문에, touch와 force가 단순 보조 feature인지 command를 바꿀 authority인지가 핵심이다. "
                "DexTacWAM은 contact evolution을 predicted world state로 넣고, HapticWAM은 inference-time tactile 없이도 imagined contact package를 남기며, When Does Touch Matter?는 wrench와 taxel feedback이 비전-only grasp와 다른 조건을 분리한다. "
                "InsertAnything, ContactDP, ForceRFT, CompVLA, TACIT은 tight insertion, force residual, compliance, tactile attention supervision을 실제 action refinement로 연결한다. "
                "따라서 APRL manipulation 평가는 touch를 붙였는지가 아니라 어떤 contact signal이 action chunk를 언제 바꾸는지로 설계해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Visuo-tactile WAM, imagined touch, real-world tactile/wrench comparison, precision insertion, contact diffusion, force residual, compliance VLA, and tactile supervision share the contact-authority axis.",
            "lab_action": (
                "Dexterous cluttered grasping, tight peg insertion, deformable contact, and humanoid/contact-rich manipulation에서 vision-only, imagined touch, fingertip tactile, wrist wrench, force residual, compliance setting, and tactile attention을 ablation하고 slip lead time, jamming, peak force, regrasp timing, correction latency, and success를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Geometry systems shift from reconstruction fidelity to uncertainty-aware motion commitment",
            "buckets": ["3D/Scene", "Safety/Alignment"],
            "ids": ["2609.22716", "2609.23100", "2609.23491", "2609.23656", "2609.24140", "2609.24839", "2609.24846", "2609.24452"],
            "needles": [
                "registration", "slam", "gaussian", "uncertainty", "next-best-view", "lidar",
                "odometry", "mapping", "reconstruction", "view", "elevator", "frontier",
            ],
            "why": (
                "Geometry 논문들은 더 선명한 3D reconstruction보다 robot motion을 허용할 만큼 evidence가 믿을 만한지를 묻는다. "
                "ZIL은 image-to-LiDAR registration을 zero-shot/non-synchronized 조건으로 밀고, Splat-CBF는 Gaussian map의 uncertainty 안에서 next-best-view와 collision safety를 같은 QP에 넣으며, Elevator-VIGS는 elevator transport state를 robot motion과 분리한다. "
                "WOLF와 BayesianGS-SLAM은 predictive frontiers와 predictive surprise를 통해 어디를 볼지, 어떤 residual을 믿을지 결정하고, When Wider Views Fail과 LiDAR-language 논문은 foundation geometry prior가 넓은 view나 spatio-temporal 관계에서 깨지는 조건을 드러낸다. "
                "APRL map 평가는 PSNR/ATE만이 아니라 uncertainty가 실제 move/stop/view 선택을 바꿨는지를 봐야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Registration, safe NBV, visual-inertial GS-SLAM, LiDAR predictive exploration, uncertainty-aware SLAM, and wide-view stress testing all expose motion-commitment evidence.",
            "lab_action": (
                "LiDAR-camera registration, 3DGS map, visual-inertial elevator sequence, UAV LiDAR exploration, RGB-D neural SLAM, feed-forward reconstruction, and LiDAR-language relation tests에서 synchronization gap, view span, uncertainty threshold, transport-state model, predictive frontier, keyframe surprise, and downstream navigation success를 함께 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Embodied navigation separates evidence gathering, phase progress, and system-level calibration",
            "buckets": ["Embodied AI", "Foundation Models", "Autonomous Driving"],
            "ids": ["2609.22385", "2609.23423", "2609.23731", "2609.24189", "2609.23131", "2609.22813", "2609.23841"],
            "needles": [
                "navigation", "exploration", "partial observability", "phase", "calibration",
                "topological", "object retrieval", "planning", "belief", "evidence",
            ],
            "why": (
                "Navigation batch는 goal-reaching score를 하나로 보지 말고, evidence를 더 모을지, semantic phase를 넘길지, module uncertainty를 composition할지, graph commitment를 할지 분리하라고 말한다. "
                "Active Spatial Inspection은 cue sufficiency와 further inspection을 explicit하게 만들고, RiverVLN은 USV instruction을 visually verifiable semantic phases로 바꾸며, Marginal Calibration Does Not Compose는 component calibration이 downstream navigation uncertainty로 보존되지 않음을 보인다. "
                "Object-Path Graphs, Selective Commitment, Commonsense path planning, structured robotic search는 dense map 없이도 belief, graph, feasibility, abstention을 commitment rule로 삼는다. "
                "APRL navigation 평가는 final SPL보다 evidence-gathering cost, phase error, calibration dependence, false grasp/false defer, and graph-localization failure를 함께 기록해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Inspection, USV phase-grounded VLN, modular calibration, topological object navigation, selective commitment, and robotic search converge on evidence-gated commitment.",
            "lab_action": (
                "ObjectNav/VLN/USV/search tasks에서 cue sufficiency, re-observation action, semantic phase transition, covariance dependence, topological node localization, belief-space commitment, and abstention threshold를 ablation하고 wrong commitment, detour cost, social/physical safety, and recovery success를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "World models are being audited at the action interface, not by future-video quality alone",
            "buckets": ["Robot Learning", "Generation", "Safety/Alignment", "Efficiency/Systems"],
            "ids": ["2609.22332", "2609.24682", "2609.23252", "2609.24868", "2609.23753", "2609.24048", "2609.24749", "2609.23578"],
            "needles": [
                "world model", "world-action", "affordance", "action", "representation",
                "parameterization", "causal", "online", "dual", "latent", "wam",
            ],
            "why": (
                "World model 논문들은 미래 영상을 얼마나 잘 그리느냐보다, 그 representation이 어떤 action interface를 안정화하는지를 검증한다. "
                "AffordanceWAM은 human/robot video를 object-centric affordance로 연결하고, Think Like a World Model은 world-model feature를 compact VLA에 distill하며, Robot World Models Are Not Invariant는 action encoding이 latent future를 완전히 바꿀 수 있음을 보인다. "
                "DualWAM, OnlineWM, What Matters in Designing WAM, D-JEPA, AR-WAM은 global planning/local refinement, causal simulator query, representation choice, decision-aligned latent, visual-conditioned agent-ready WAM을 각각 action contract로 만든다. "
                "APRL은 generated future quality보다 action parameterization, causality, affordance target, and local feedback이 실제 command를 어떻게 바꾸는지 평가해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Affordance WAMs, WM-to-VLA distillation, action-encoding invariance, dual-system refinement, causal online learning, and design audits all target the action interface.",
            "lab_action": (
                "Manipulation WAM/VLA tasks에서 affordance heatmap, cached world-model feature, absolute-vs-delta action encoding, global-plan/local-refinement cadence, causal simulator query, and decision-aligned latent를 ablation하고 rollout error, action disagreement, closed-loop latency, contact recovery, and task success를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Safety and recovery move from current-step vetoes to predictive control authority",
            "buckets": ["Robot Learning", "Safety/Alignment", "Autonomous Driving"],
            "ids": ["2609.22462", "2609.22538", "2609.22591", "2609.23896", "2609.23280", "2609.23263", "2609.22762", "2609.24055"],
            "needles": [
                "safe", "safety", "barrier", "recovery", "failure", "uncertainty",
                "conformal", "mpc", "control", "referee", "collision", "human-in-the-loop",
            ],
            "why": (
                "Safety 논문들은 현재 action을 veto하는 필터에서 벗어나, 미래에 recovery authority가 남는지를 예측하고 그 근거를 control interface에 넣으려 한다. "
                "VLPSA는 perception-derived Poisson safety functions를 CBF-QP로 enforced full-body safety에 연결하고, FRAMES와 REBOOT는 humanoid/assembly failure를 monitoring과 phase-level recovery data로 만든다. "
                "BarrierFormer와 adaptive conformal quantile intervals는 predictive barrier와 calibrated uncertainty를 통해 future constraint violation을 줄이며, DriveReferee는 learned verdict 대신 predicted scene state 위에서 explicit geometric rule을 적용한다. "
                "APRL safety 평가는 collision avoided yes/no보다 warning latency, remaining control authority, uncertainty coverage, phase-specific recovery, and false conservatism을 같이 봐야 한다."
            ),
            "confidence": "High",
            "confidence_note": "CBF filtering, humanoid monitoring, recovery benchmark, predictive barrier transformer, conformal safety, MPC repair, analytic driving referee, and HRI recovery all make future authority explicit.",
            "lab_action": (
                "Manipulation, humanoid loco-manipulation, mobile navigation, driving WAM, and HRI recovery tasks에서 CBF activation, monitor decision, recovery phase, conformal interval width, predictive barrier horizon, analytic geometric verdict, and human help timing을 stress split으로 두고 unsafe execution, false stop, task delay, and recovery success를 비교한다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Counterfactual closed-loop VLA validation",
            "claim": (
                "One shared suite should combine region-level perturbation certificates, stale-camera execution, task-semantic swaps, compression residual traces, and recovery-trigger episodes."
            ),
        },
        {
            "title": "Contact authority ladder",
            "claim": (
                "Rank vision, imagined touch, tactile features, wrench estimates, force residuals, and compliance settings by when they should override the next action chunk."
            ),
        },
        {
            "title": "Evidence-budgeted map commitment",
            "claim": (
                "Evaluate SLAM/reconstruction methods by whether uncertainty, registration confidence, and next-best-view choices improve downstream move/stop/view decisions."
            ),
        },
        {
            "title": "Action-interface audit for world models",
            "claim": (
                "World models should be tested under action-encoding, affordance-target, causal-query, and local-refinement ablations before claiming robot-control transfer."
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
