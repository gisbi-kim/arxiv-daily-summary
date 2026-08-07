#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-08-07 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260807 import RI_BY_DATE


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-07"


PROFILE = {
    "date": DATE,
    "weekday": "Fri",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching 2026-08-07 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-08-07 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records official arXiv abstract/HTML evidence for Tier A."
    ),
    "thesis": (
        "The August 7 batch is a grounding audit for embodied models: language, future wrist state, world-model rollouts, "
        "LiDAR pose, and safety monitors all need to show which robot decision they change. In-Context VLA rejects "
        "free-form narration for low-level control, World-to-Wrist and Robust-WAM move future state into the action stream, "
        "XEWorld and GAUGE expose physical validity gaps in world models, and UQ-Loc makes geometry uncertainty operational."
    ),
    "cluster_takeaway": "Today's useful signal is not a new model family; it is the move from plausible evidence to action-changing evidence.",
    "trend_note": (
        "The Friday /new listing has 165 deduplicated papers and 137 ROI papers. Generation is the largest bucket, "
        "but the robotics signal is concentrated in VLA evidence consumption, future-state WAMs, cross-embodiment world-model audits, "
        "LiDAR/geometry uncertainty, and recoverable failure safety."
    ),
    "cluster_specs": [
        {
            "title": "VLA control shifts from narration to grounded evidence consumption",
            "buckets": ["Robot Learning", "Foundation Models", "Safety/Alignment"],
            "ids": ["2608.05738", "2608.05215", "2608.05369", "2608.05970", "2608.06374", "2608.05579", "2608.05715"],
            "needles": ["vla", "language", "affordance", "wrist", "memory", "grounded", "tool", "viewpoint", "prompt injection"],
            "why": (
                "In-Context VLA argues that low-level policies should consume grounded language rather than emit CoT; VLAff makes affordances executable through 3D scene information; "
                "World-to-Wrist turns wrist-local future state into an action interface; SkillMemo tests reusable skill memory; DyPES-VLA separates shared dynamics priors from embodiment-specific control; "
                "ARGUS reduces viewpoint burden with 3D alignment, and physical prompt-injection work warns that visual text can hijack the same grounding channel."
            ),
            "confidence": "High",
            "confidence_note": "Multiple papers directly target VLA grounding, action interfaces, affordances, memory, viewpoint alignment, and physical attacks.",
            "lab_action": "Run one manipulation suite with language-context ablation, visual text attack, viewpoint shift, wrist-future masking, and action-token delta logging.",
            "limit": 7,
        },
        {
            "title": "World models face embodiment-transfer and physical-fidelity audits",
            "buckets": ["Robot Learning", "Generation", "Safety/Alignment"],
            "ids": ["2608.05799", "2608.05948", "2608.05903", "2608.05706", "2608.06008", "2608.05523", "2608.06375"],
            "needles": ["world model", "wam", "action-conditioned", "physical", "future", "semantic", "latent", "embodiment", "fidelity"],
            "why": (
                "XEWorld asks whether action-conditioned models generalize to unseen robots or only match visual appearance; GAUGE scores simulators and video world models against calibrated physical measurements; "
                "Robust-WAM aligns semantic foresight into the action stream; LAWM-3D learns 3D-aware latent actions from human videos; Adaptive-WAM uses early-exit planning; HERA routes historical evidence for physical prediction; "
                "and humanoid WAM work moves the question to whole-body loco-manipulation."
            ),
            "confidence": "High",
            "confidence_note": "The cluster links WAM action prediction, physical fidelity, semantic foresight, 3D latent actions, and cross-embodiment tests.",
            "lab_action": "Compare simulator, video world model, and WAM rollouts on the same contact tasks using object displacement, contact timing, recovered physical parameters, and action success.",
            "limit": 7,
        },
        {
            "title": "Geometry becomes a reliability interface for localization and contact",
            "buckets": ["3D/Scene", "Robot Learning", "Autonomous Driving"],
            "ids": ["2608.06307", "2608.05647", "2608.05579", "2608.06014", "2608.06117", "2608.05539", "2608.05356"],
            "needles": ["lidar", "localization", "uncertainty", "geometry", "gaussian", "calibration", "viewpoint", "scene completion", "point cloud"],
            "why": (
                "UQ-Loc makes covariance part of LiDAR scene-coordinate registration; KILVO fuses kinematics, IMU, LiDAR, and vision for humanoid odometry under sensor degradation; "
                "ARGUS canonicalizes shifting robot camera views; controlled LiDAR scene completion tests when refinement helps; multi-view Gaussian reconstruction uses geometric confidence; "
                "OmniMech and LoDA add mechanical and multimodal change benchmarks. Geometry is useful when its confidence reaches planning."
            ),
            "confidence": "High",
            "confidence_note": "3D/Scene has 17 ROI papers, including LiDAR localization, odometry, Gaussian reconstruction, mechanical benchmarks, and multimodal change detection.",
            "lab_action": "Propagate per-voxel covariance, sensor-dropout labels, viewpoint shift, and map-change annotations into a single localization-to-action failure log.",
            "limit": 7,
        },
        {
            "title": "Long-video reasoning becomes evidence budgeting",
            "buckets": ["Foundation Models", "Efficiency/Systems", "Generation"],
            "ids": ["2608.05707", "2608.05780", "2608.05505", "2608.05631", "2608.05747", "2608.06060", "2608.05485"],
            "needles": ["evidence", "frame selection", "future", "temporal", "long-video", "uncertainty", "reasoning", "video"],
            "why": (
                "MEC frame selection builds one ranking that works across budgets; EviSelect allocates visual computation from internal attention evidence; "
                "DynaPix checks whether VLMs can identify the exact future rather than a plausible one; ChronoVision reconstructs latent temporal state; "
                "GST-Bench probes global spatial awareness from video, and retrieval-centric CoT uses hard negatives after failures. The common variable is evidence scheduling under limited context."
            ),
            "confidence": "High",
            "confidence_note": "The selected papers repeatedly separate evidence location, budget, temporal anchoring, and calibration.",
            "lab_action": "Evaluate long-video robot episodes with fixed-prefix frame ranking, dynamic selector, exact-future candidate tests, and downstream action error under equal token budgets.",
            "limit": 7,
        },
        {
            "title": "Robot safety moves from avoidance to recoverable failure contracts",
            "buckets": ["Safety/Alignment", "Autonomous Driving", "Foundation Models", "Embodied AI"],
            "ids": ["2608.05313", "2608.05715", "2608.05588", "2608.05594", "2608.05365", "2608.06088", "2608.05560"],
            "needles": ["failure", "safety", "attack", "prompt injection", "robust", "lifelong", "navigation", "validation", "fuzzing", "risk"],
            "why": (
                "Failing Gracefully scores impact severity when robot failures are inevitable; physical prompt injection creates a real VLM-planner attack surface; "
                "search-aided lifelong MAPF adds rotation and safety constraints; JTA targets scenario-based validation of safety-critical software; "
                "UUV navigation handles partial observability, IcFuzz mutates Isaac Sim, and proactive risk inference benchmarks test early warning. Safety becomes a replayable failure contract."
            ),
            "confidence": "Medium-High",
            "confidence_note": "The cluster spans real robot failure impact, physical attacks, constrained navigation, simulator fuzzing, and validation architecture.",
            "lab_action": "Build a safety replay set with signage attack, actuator degradation, simulator mutation, partial-observability navigation, and severity-weighted recovery labels.",
            "limit": 7,
        },
        {
            "title": "Weakly labeled human data needs executable alignment tests",
            "buckets": ["Robot Learning", "Generation", "Efficiency/Systems"],
            "ids": ["2608.05674", "2608.05215", "2608.05970", "2608.06221", "2608.06219", "2608.05725", "2608.06210"],
            "needles": ["human", "demonstration", "teleoperation", "tactile", "affordance", "action alignment", "skill", "manipulation"],
            "why": (
                "JoyAI-RA turns human egocentric video, simulation, and robot data into dual action alignment; VLAff extracts affordances from human videos; "
                "SkillMemo stores latent skill primitives; handwriting trajectory work and teleoperation interfaces expose human-likeness and operator-control measures; "
                "near-sensor visuotactile perception and variable-impedance diffusion policy test whether human or tactile evidence becomes executable robot control."
            ),
            "confidence": "Medium-High",
            "confidence_note": "The selected papers align human videos, demonstrations, teleoperation, tactile sensing, and compliant manipulation around executable action supervision.",
            "lab_action": "Audit one human-video-to-robot pipeline with latent action alignment, affordance heatmap transfer, skill-memory retrieval, and real-robot contact success.",
            "limit": 7,
        },
    ],
    "research_topics": [
        {
            "title": "Evidence-consuming VLA protocol",
            "claim": "Measure whether grounded language, affordance, wrist-future, and viewpoint-normalized evidence changes the next action under controlled perturbations.",
        },
        {
            "title": "Measurement-grounded WAM audit",
            "claim": "Compare physical-observable error, embodiment-transfer error, semantic-foresight quality, and final robot success on one shared task suite.",
        },
        {
            "title": "Recoverable failure replay set",
            "claim": "Combine physical prompt injection, inevitable hardware/software failures, navigation constraints, and simulator fuzzing into severity-weighted safety replays.",
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
        "meaning": "Included because it supports the day's action-grounding and physical-validity thesis.",
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
        "Research Intelligence uses official arXiv abstract pages and available official HTML structure for selected Tier A papers. "
        "Other daily cards are conservative abstract-based cards from repository parser text."
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
