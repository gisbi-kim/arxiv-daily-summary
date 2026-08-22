#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-08-21 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260821 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-21"


PROFILE = {
    "date": DATE,
    "weekday": "Fri",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching 2026-08-21 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-08-21 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "The 2026-08-21 batch is about turning robot intelligence into auditable interfaces before deployment. "
        "VLA and manipulation papers expose embodiment mismatch, continual skill retention, latent-action choice, tactile world-action forecasts, and contact topology as separate variables that can change the next action. "
        "Autonomy and geometry papers do the same for scenario-conditioned evaluation, temporal-logic constraints, LiDAR degeneracy, metric registration, and sparse-view reconstruction. "
        "The shared research move is to make the evidence gate visible: what observation, contact state, map property, scenario condition, or generated process is allowed to authorize the policy."
    ),
    "cluster_takeaway": (
        "Today's core is not better average success; it is deciding which evidence interface authorizes adaptation, planning, mapping, and generated futures before a robot commits to an action."
    ),
    "trend_note": (
        "Friday /new produced 115 deduplicated non-replacement papers and 95 ROI papers. "
        "Robot Learning is the largest bucket, but the strongest APRL signal is the cross-bucket repetition of evidence-gated execution, scenario-conditioned evaluation, robot-facing geometry, and process-valid world generation."
    ),
    "cluster_specs": [
        {
            "title": "VLA adaptation moves from single finetunes to embodiment-safe action interfaces",
            "buckets": ["Robot Learning"],
            "ids": ["2608.19490", "2608.19589", "2608.19613", "2608.19574", "2608.20114", "2608.20208"],
            "needles": ["vla", "latent action", "world action", "tactile", "whole-body", "offline reinforcement", "finetuning", "continual"],
            "why": (
                "Existing robot adaptation often asks whether a single finetune raises task success on the new embodiment. "
                "This group instead exposes where adaptation can fail: self-demonstrated VLA data can overwrite old competence, skill-subspace updates can forget previous velocity mappings, latent-action design choices can hide inconsistent evaluation, tactile world-action models can miss contact hierarchy, and whole-body WAMs must split camera ego-motion from base and arm action. "
                "APRL should evaluate adaptation at the interface that changes the next action, not only at final task success."
            ),
            "confidence": "High",
            "confidence_note": "Six Robot Learning papers independently target VLA finetuning, continual skills, latent actions, tactile WAMs, whole-body WAMs, or offline action modeling.",
            "lab_action": (
                "Run equal-budget manipulation and mobile-manipulation tasks with new gripper geometry, old-skill probes, latent-action variants, tactile contact shifts, and base-arm coupling; compare next-action delta, forgetting rate, contact recovery, ego-motion error, and final success."
            ),
            "limit": 6,
        },
        {
            "title": "Manipulation evidence shifts from object success to contact topology and simulation-ready state",
            "buckets": ["Robot Learning"],
            "ids": ["2608.19372", "2608.19968", "2608.19759", "2608.19776", "2608.20251", "2608.20308"],
            "needles": ["tactile", "assembly", "grasp", "contact", "topology", "door", "egocentric", "hand", "teleoperation"],
            "why": (
                "A final grasp or traversal score hides the physical state that made the behavior reusable. "
                "Spatially distributed tactile feedback, assembly key-point voting, object-agnostic grasp generation, contact-topology-conditioned synthesis, simulated door twins, and egocentric hand-motion recovery all push the evidence toward contact, dependency, geometry, and real-to-sim state. "
                "The useful benchmark labels are not just success or failure; they are where the hand, object, door, tool, or operator feedback carried the decisive constraint."
            ),
            "confidence": "High",
            "confidence_note": "Six manipulation papers share contact, hand-state, grasp-topology, assembly-dependency, teleoperation, or door-twin evidence variables.",
            "lab_action": (
                "Build one contact-rich suite with tactile coverage, assembly dependency, object-agnostic grasp target, contact topology, door articulation, and occluded hand trajectory labels; compare final success against contact-state correctness, dependency satisfaction, recovery action, and sim-to-real traversal outcome."
            ),
            "limit": 6,
        },
        {
            "title": "Autonomy evaluation becomes scenario-conditioned before planning is trusted",
            "buckets": ["Autonomous Driving", "Robot Learning"],
            "ids": ["2608.19425", "2608.19453", "2608.19661", "2608.19671", "2608.20275", "2608.19380"],
            "needles": ["scenario", "temporal logic", "world model", "navigation", "inspection", "reachability", "accident", "planning"],
            "why": (
                "Average planner performance cannot tell whether a system is safe in the scenario family that matters. "
                "SCAPE conditions policy evaluation on scenarios, temporal-logic compilation makes stream-generated geometric parameters part of the TAMP contract, offshore AUV/ASV planning grounds LLM actions in a physics world model, SAGE prioritizes subsea inspection by changing risk state, DART-S audits reachable jump states before takeoff, and CAViAR asks for causal accident reasoning. "
                "The common decision is to publish the scenario, constraint, or reachable state that the plan actually covers."
            ),
            "confidence": "High",
            "confidence_note": "Autonomy papers repeatedly expose scenario, temporal-logic, world-state, inspection-risk, reachability, and causal-reasoning audit variables.",
            "lab_action": (
                "Create four deployment families with partial observability, generated geometric streams, offshore drift, risk-weighted inspection, and reachability boundary cases; compare aggregate success, temporal-logic violation, world-model correction, risk revisit timing, and reachable-state margin."
            ),
            "limit": 6,
        },
        {
            "title": "Geometry and SLAM validity is judged by degeneracy, registration transfer, and sparse-view use",
            "buckets": ["3D/Scene", "Safety/Alignment", "Generation"],
            "ids": ["2608.19536", "2608.19522", "2608.19693", "2608.20000", "2608.20056", "2608.19556"],
            "needles": ["lidar", "registration", "odometry", "degeneracy", "keypoint", "sparse view", "pose", "4d", "drift"],
            "why": (
                "The geometry papers make visual or metric structure accountable to robot-facing failure modes. "
                "Cross-modal semantic-prior distillation targets LiDAR registration under density and sensor shifts, LF-GICP exposes unobservable axes in degenerate LiDAR odometry, RIPE++ revisits sparse keypoints that support SLAM and registration, sparse-view point reconstruction asks whether known illumination can stabilize geometry, gravity-aware pose estimation uses IMU structure for faster localization, and Stream4D identifies geometric drift in streaming video generation. "
                "For APRL, map quality should be tested by registration transfer, localizability, pose validity, and downstream navigation or manipulation impact."
            ),
            "confidence": "High",
            "confidence_note": "The geometry watch lens is triggered by LiDAR registration, LiDAR odometry, keypoint learning, sparse-view reconstruction, pose estimation, and 4D drift signals.",
            "lab_action": (
                "Evaluate LiDAR registration, degeneracy-aware odometry, keypoint matching, sparse-view reconstruction, gravity-aided pose, and streaming 4D generation on tunnels, corridors, sparse views, sensor-density shifts, and dynamic objects; score drift axis detection, registration failure, pose validity, and route recovery."
            ),
            "limit": 6,
        },
        {
            "title": "VLM reliability shifts from confidence to evidence acquisition and authorization",
            "buckets": ["Foundation Models", "Safety/Alignment"],
            "ids": ["2608.19376", "2608.19739", "2608.20084", "2608.19208", "2608.19355", "2608.19729"],
            "needles": ["coverage", "evidence", "task and motion", "irrelevant text", "calibration", "safety", "branch", "grounded"],
            "why": (
                "One confidence number is not enough when the failure comes from missing observations, class-specific tails, irrelevant text priors, or unsafe branch choices. "
                "The conformal VLM audit shows marginal coverage can hide class-conditional collapse, question-guided evidence acquisition slows perception before answering, evidence-gated TAMP blocks unsupported subgoals, irrelevant-text interventions expose prediction bias, GRACE calibrates educational VQA around evidence, and SafeBranch aligns branch-pair safety for embodied agents. "
                "Robot VLMs should expose the observation or predicate that authorized an answer, subgoal, or branch."
            ),
            "confidence": "High",
            "confidence_note": "Six VLM/safety papers independently target class-tail risk, evidence acquisition, unsupported subgoals, text bias, calibration, and safe branching.",
            "lab_action": (
                "Test robot VLM and TAMP systems with hidden objects, small labels, irrelevant text, branch-pair safety conflicts, and class-tail visual shifts; compare answer accuracy, evidence-acquisition action, unsupported subgoal rate, branch violation, abstention, and downstream task failure."
            ),
            "limit": 6,
        },
        {
            "title": "Generative models are evaluated by process validity instead of local visual fidelity",
            "buckets": ["Generation", "3D/Scene", "Efficiency/Systems"],
            "ids": ["2608.19583", "2608.20107", "2608.19556", "2608.19723", "2608.19639", "2608.20336"],
            "needles": ["video generation", "causal", "physical", "streaming", "memory", "identity", "4d", "gaussian"],
            "why": (
                "Generation papers repeatedly reject local appearance as the only target. "
                "VGI-BENCH requires valid evolving processes, BeyondMasks treats object removal as a causal intervention with physical side effects, Stream4D targets geometric drift in streaming rollouts, StreamSoccer organizes bounded event memory, S2GS makes free-viewpoint video reconstruction sparse enough for edge deployment, and WithEveryone binds identities to distinct people and locations. "
                "For robotics, generated video or scene data should be kept only if it preserves the process, identity, geometry, and physical consequences that a planner would use."
            ),
            "confidence": "High",
            "confidence_note": "Six generation papers connect process validity, causal side effects, 4D drift, event memory, sparse FVV reconstruction, and identity grounding.",
            "lab_action": (
                "Create generated-scene probes where final appearance is plausible but process order, physical side effects, geometry drift, event memory, identity binding, or free-viewpoint consistency can fail; measure planner action error, object permanence, route consistency, and rejection rate."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Evidence-gated mobile manipulation",
            "claim": (
                "Build hidden-object and branch-pair tasks where VLM-TAMP subgoals, VLA actions, and safety predicates must cite observational evidence before execution; measure unsupported subgoal and unsafe-branch reduction."
            ),
        },
        {
            "title": "Contact-and-whole-body action interface suite",
            "claim": (
                "Compare self-demonstrated VLA adaptation, latent actions, tactile WAM, and decoupled whole-body WAM under the same door, grasp, and base-arm coordination tasks."
            ),
        },
        {
            "title": "Robot-facing geometry degeneracy benchmark",
            "claim": (
                "Use corridors, tunnels, sparse views, sensor-density shifts, and dynamic objects to test whether registration, odometry, pose, and 4D generation systems reveal the axis where downstream navigation will fail."
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
        "meaning": "Included because it supports today's evidence-gated execution thesis.",
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
