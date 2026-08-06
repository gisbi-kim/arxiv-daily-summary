#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-08-06 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260806 import RI_BY_DATE


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-06"


PROFILE = {
    "date": DATE,
    "weekday": "Thu",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching 2026-08-06 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-08-06 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records official arXiv abstract/HTML evidence for Tier A."
    ),
    "thesis": (
        "The August 6 batch is less about larger VLAs and more about deciding which evidence channel should control the next action. "
        "CofactVLA isolates visual confounders, SAFECAST and GUARD turn failure warnings into calibrated evidence tests, "
        "Faster-WAM and DreamWAM preserve action-relevant future state under compute limits, and Talk2Sensors makes outdoor grounding depend on named sensor cues. "
        "APRL should evaluate instruction, vision, future state, geometry, and risk probes as separable control interfaces."
    ),
    "cluster_takeaway": "Today's useful signal is evidence-channel validity across VLA control, WAM future state, multi-sensor grounding, and safety.",
    "trend_note": (
        "The Thursday /new listing has 160 deduplicated papers and 136 ROI papers. Foundation Models and Generation are the largest buckets, "
        "but the robotics signal is concentrated: VLA deconfounding, failure detection, long-horizon memory, WAM future conditioning, and sensor-aware geometry."
    ),
    "cluster_specs": [
        {
            "title": "VLA control becomes an evidence-channel deconfounding problem",
            "buckets": ["Robot Learning"],
            "ids": ["2608.04396", "2608.04510", "2608.04246", "2608.04633", "2608.04692", "2608.04196"],
            "needles": ["vla", "deconfounding", "grounding", "uncertainty", "failure", "instruction", "contrast", "risk"],
            "why": (
                "CofactVLA treats vision override as causal confusion, GUARD measures grounding through KV-cache ablations, SAFECAST calibrates hidden-state probes under contrast shifts, "
                "Mind-VLA aligns instruction-specific 3D target state, task-vector audits test closed-loop locality, and SiMDex asks which human videos actually help. "
                "The common decision is which evidence channel is allowed to steer a robot action."
            ),
            "confidence": "High",
            "confidence_note": "Multiple VLA papers directly target instruction grounding, risk detection, spatial alignment, and data selection.",
            "lab_action": "Run one manipulation suite with language masking, visual distractors, target-object occlusion, KV-cache ablation, and contrast-set calibration logged per failure.",
            "limit": 6,
        },
        {
            "title": "World-action models shift from RGB futures to useful future state",
            "buckets": ["Robot Learning", "Generation"],
            "ids": ["2608.04404", "2608.04657", "2608.04996", "2608.04653", "2608.04866", "2608.05084"],
            "needles": ["wam", "world", "future", "action", "controllable", "diffusion", "state", "memory"],
            "why": (
                "Faster-WAM keeps future conditioning at inference time, MobileWAM expands WAMs to mobile manipulation, DreamWAM predicts appearance, motion, geometry, and semantics beyond RGB, "
                "CoCo attacks statistical shortcuts in action-controllable world models, SlotNarrative preserves object state through compact narratives, and dynamic diffusion policies learn when to stop. "
                "The useful question is which future representation changes action success under shift."
            ),
            "confidence": "High",
            "confidence_note": "The selected papers repeatedly separate future state, action controllability, memory, and inference budget.",
            "lab_action": "Ablate future-cache age, RGB-only versus structured future state, action counterfactual consistency, and latency budget on the same manipulation/mobile task.",
            "limit": 6,
        },
        {
            "title": "Outdoor geometry needs sensor-cue and calibration accountability",
            "buckets": ["3D/Scene", "Robot Learning", "Autonomous Driving"],
            "ids": ["2608.04568", "2608.04673", "2608.04560", "2608.05066", "2608.04842", "2608.04420", "2608.04453"],
            "needles": ["3d", "sensor", "calibration", "pose", "uav", "lidar", "radar", "gaussian", "map"],
            "why": (
                "Talk2Sensors binds language grounding to camera, LiDAR, and radar cues; differential pose estimation and 3D-target calibration expose calibration error as a robot variable; "
                "OutLangSplat and RORA make outdoor or articulated reconstruction operational; SCOPE and TwinIR add safety-volume and HD-map attack stress. "
                "Geometry is useful only when the sensor cue and calibration assumption are named."
            ),
            "confidence": "High",
            "confidence_note": "3D grounding, pose, calibration, reconstruction, navigation certification, and map attacks all appear in the same daily batch.",
            "lab_action": "Test grounding and navigation under camera dropout, LiDAR/radar cue removal, extrinsic perturbation, sparse outdoor views, and map-boundary attack points.",
            "limit": 7,
        },
        {
            "title": "VLM reasoning moves from bigger context to evidence construction",
            "buckets": ["Foundation Models", "Efficiency/Systems", "Generation"],
            "ids": ["2608.04385", "2608.04452", "2608.04496", "2608.04483", "2608.04132", "2608.04759", "2608.04866"],
            "needles": ["evidence", "token", "grounding", "reasoning", "visual", "pruning", "re-examination", "allocation"],
            "why": (
                "ReGround diagnoses when reasoning drifts from image evidence, Q-CueGraph chooses query-conditioned crops, DIVE constructs residual-conditioned visual evidence, "
                "token-role pruning shows not all redundant tokens are equivalent, RUTA allocates visual tokens by utility, Trace/Verify/Correct repairs spatial reasoning, and SlotNarrative preserves object evidence across time. "
                "The hidden axis is evidence scheduling, not context length alone."
            ),
            "confidence": "High",
            "confidence_note": "Several independent VLM papers target evidence routing, visual re-examination, token allocation, and spatial verification.",
            "lab_action": "Compare full image context, query-crop evidence, iterative token retention, role-protected pruning, and spatial correction by downstream robot action error.",
            "limit": 7,
        },
        {
            "title": "Operational safety shifts to calibrated, physical, and constrained failures",
            "buckets": ["Safety/Alignment", "Autonomous Driving", "Robot Learning", "Embodied AI"],
            "ids": ["2608.04244", "2608.04453", "2608.04559", "2608.04190", "2608.04732", "2608.05021", "2608.04721"],
            "needles": ["safety", "adversarial", "attack", "uncertainty", "constraint", "planning", "failure", "conflict"],
            "why": (
                "SIGNPOST-Bench probes text-vision conflict, TwinIR and ColorFD make physical attacks operational, abductive fusion handles adversarial perception-model failures, "
                "safe actor-critic work integrates uncertainty with control, sc-LTL planning preserves constraints, and urgency-aware swarms add deadline pressure. "
                "Safety becomes a structured failure contract rather than a post-hoc warning."
            ),
            "confidence": "Medium-High",
            "confidence_note": "The cluster spans multimodal conflict, physical attacks, uncertainty-aware control, temporal-logic constraints, and swarm logistics.",
            "lab_action": "Create a safety replay set with text-vision conflict, HD-map perturbation, black-box physical attack, uncertainty update, and sc-LTL constraint violation labels.",
            "limit": 7,
        },
        {
            "title": "Embodied memory becomes explicit world-task binding",
            "buckets": ["Embodied AI", "Robot Learning", "Efficiency/Systems"],
            "ids": ["2608.04933", "2608.04765", "2608.05042", "2608.04825", "2608.04530", "2608.04905", "2608.05078"],
            "needles": ["memory", "long-horizon", "planning", "navigation", "embodied", "grounding", "task", "replay"],
            "why": (
                "Mimir separates world memory from task memory, explicit language memory helps long-horizon VLAs, BridgeVLA++ adds spatio-temporal memory for 3D manipulation, "
                "DBFly makes UAV navigation deliberate before action, FocusMem factors content/readout/trust, PRIMAL3 scales multi-agent pathfinding, and SpikingNav tests efficient navigation policies. "
                "The common variable is whether memory is bound to the active goal before control."
            ),
            "confidence": "Medium-High",
            "confidence_note": "Embodied papers are fewer, but they align tightly with VLA memory, navigation, and trust-factorized memory.",
            "lab_action": "Evaluate one long-horizon task with separate world-memory age, task-progress state, language-memory compression, and replan trigger ablations.",
            "limit": 7,
        },
    ],
    "research_topics": [
        {
            "title": "Evidence-channel VLA audit",
            "claim": "Cross language masking, visual distractors, KV-cache ablation, target-object occlusion, and contrast-set calibration in one manipulation benchmark.",
        },
        {
            "title": "Budgeted future-state WAM test",
            "claim": "Measure whether sparse future conditioning, structured non-RGB future state, and action counterfactual consistency improve rollout recovery under shift.",
        },
        {
            "title": "Sensor-cue grounding and calibration grid",
            "claim": "Evaluate 3D grounding with explicit camera, LiDAR, radar, extrinsic calibration, and map-boundary perturbations tied to action success.",
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
        "method": "See Research Intelligence edition for evidence trace and falsification note.",
        "meaning": "Included because it supports the day's evidence-channel thesis and APRL strategy board.",
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
        "Research Intelligence uses official arXiv abstract pages and available official HTML headings for selected Tier A papers. "
        "Other daily cards are conservative abstract-only cards from repository parser text."
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
        f"Tier A {len(ri['papers'])} papers are checked against official arXiv HTML, with evidence traces, "
        f"adversarial reads, frontier memory, and APRL strategy board.</span>"
        f"<a href=\"{DATE}-research-intelligence.html\">Open Research Intelligence</a></section>"
    )
    doc = re.sub(r"</section>\n(<h2>.*?</h2>)", f"</section>\n{ri_callout}\n\\1", doc, count=1, flags=re.S)
    post_path.write_text(doc, encoding="utf-8", newline="\n")


def main() -> int:
    build(PROFILE, "out/cv_new.json", "out/ro_new.json")
    enrich_insights()
    add_ri_callout()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
