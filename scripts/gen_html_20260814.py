#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-08-14 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260814 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-14"


PROFILE = {
    "date": DATE,
    "weekday": "Fri",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching 2026-08-14 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-08-14 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "The 2026-08-14 batch shifts robotics value from after-the-fact scoring toward pre-commit evidence: "
        "latent futures that can abort contact, VLA activations that reveal stalled progress, active views that justify "
        "affordance grounding, and generated or reconstructed worlds that must prove embodiment and action validity."
    ),
    "cluster_takeaway": (
        "Today's common decision is whether evidence arrives early enough to change the next action: abort before contact, "
        "look again before grounding, route semantic and predictive dynamics before planning, or reject a generated world before it becomes training data."
    ),
    "trend_note": (
        "Friday /new produced 133 deduplicated non-replacement papers and 112 ROI papers. Generation and Foundation Models "
        "were the largest buckets, but the strongest robotics signal came from monitoring, active evidence acquisition, "
        "humanoid/embodied benchmarks, and human-to-robot world-model diagnostics."
    ),
    "cluster_specs": [
        {
            "title": "Robot execution monitors move before contact and completion",
            "buckets": ["Robot Learning", "Safety/Alignment", "Foundation Models"],
            "ids": ["2608.13438", "2608.13474", "2608.13284", "2608.13223", "2608.13167"],
            "needles": ["pre-contact", "progress", "failure", "teleoperation", "uncertainty", "abstain", "ood"],
            "why": (
                "ContactGuard, task-progress probing, predictive teleoperation safety, robustness uncertainty, and TRAPSBench all move the "
                "release question earlier than final success. They ask which latent future, activation signal, human-operator risk, "
                "or hidden answerability state can block the next action before the visible failure arrives."
            ),
            "confidence": "High",
            "confidence_note": "Five selected papers directly expose pre-contact, progress, uncertainty, or abstention signals.",
            "lab_action": (
                "Run contact-rich manipulation and navigation episodes with delayed failure labels, then measure monitor lead time, "
                "false abort rate, stalled-progress detection, and the exact action that each signal vetoes."
            ),
            "limit": 5,
        },
        {
            "title": "Synthetic manipulation data is judged by contact and embodiment transfer",
            "buckets": ["Robot Learning", "Generation", "3D/Scene"],
            "ids": ["2608.13049", "2608.13489", "2608.13028", "2608.12416", "2608.13555", "2608.13014"],
            "needles": ["human-to-robot", "handover", "world model", "embodiment", "contact", "dexterity", "tracking"],
            "why": (
                "H2R-Bench, DreamX-Phi, RGB-D handover generation, RoboSynChallenge, HumanTracker, and EgoPHI all reject a pure "
                "visual-realism test for synthetic manipulation data. The evidence has to survive embodiment constraints, functional "
                "contact, force or motion plausibility, and downstream execution."
            ),
            "confidence": "High",
            "confidence_note": "The selected papers share cross-embodiment manipulation, generated futures, or physical interaction diagnostics.",
            "lab_action": (
                "Convert human manipulation clips into robot-centric RGB-D or video futures, then score goal event, contact timing, "
                "force plausibility, embodiment correctness, and policy-imitation delta under identical tasks."
            ),
            "limit": 6,
        },
        {
            "title": "Embodied navigation must acquire evidence before deciding",
            "buckets": ["Embodied AI", "3D/Scene", "Autonomous Driving", "Foundation Models"],
            "ids": ["2608.12683", "2608.12707", "2608.12860", "2608.12835", "2608.13095", "2608.12917", "2608.12515"],
            "needles": ["navigation", "affordance", "viewpoint", "semantic", "free-space", "humanoid", "proxemic"],
            "why": (
                "FUSE, SAP-Nav, HumanoidVLN, AirForesight, Semantic Radiance Fields, and social navigation "
                "turn embodied reasoning into an evidence-acquisition problem. The agent must decide when another view, semantic query, "
                "physics constraint, or human-distance cue changes the route, target, or stop decision."
            ),
            "confidence": "High",
            "confidence_note": "Navigation and affordance papers independently converge on active observation and embodied evidence contracts.",
            "lab_action": (
                "Build paired scenes with hidden functional cues, ambiguous room-region targets, humanoid motion constraints, and human-proxemic hazards, "
                "then log which observation changed target grounding, route, or stop timing."
            ),
            "limit": 6,
        },
        {
            "title": "3D representations become metric interfaces, not render artifacts",
            "buckets": ["3D/Scene", "Autonomous Driving", "Embodied AI"],
            "ids": ["2608.12825", "2608.13147", "2608.13102", "2608.12442", "2608.12840", "2608.12866"],
            "needles": ["3d", "gaussian", "geometry", "metric", "radar", "depth", "pose", "vins"],
            "why": (
                "LocusGS, geometry-grounded driving perception, radar-camera depth completion, multi-view driving NVS, ASPIRE-VINS, "
                "and underwater relative pose estimation all make 3D work answerable to metric decisions. The useful artifact is not a prettier "
                "scene; it is a spatial token, depth anchor, pose estimate, or navigable view that changes a downstream system."
            ),
            "confidence": "Medium-High",
            "confidence_note": "The geometry set is smaller than generation, but multiple papers expose metric or control-facing interfaces.",
            "lab_action": (
                "Corrupt anchors, radar points, camera views, inertial residuals, and relative pose markers separately, then measure localization, "
                "depth, map, route, or perception degradation before image-quality metrics move."
            ),
            "limit": 6,
        },
        {
            "title": "VLM deployment shifts from answers to restraint and grounding",
            "buckets": ["Foundation Models", "Safety/Alignment", "Efficiency/Systems"],
            "ids": ["2608.13167", "2608.12911", "2608.12746", "2608.13267", "2608.13119", "2608.13463", "2608.13226"],
            "needles": ["abstain", "privacy", "hallucination", "visual evidence", "typographic", "router", "token pruning"],
            "why": (
                "Relational privacy leakage, object-anchor correction, blind-or-misled figure tests, typographic-attack defense, "
                "heterogeneous routing, and 3D VLM token pruning all separate fluent output from evidence-grounded output. For robots, a VLM "
                "needs visible restraint, anchor use, attack resistance, and budget-aware routing before approving an action."
            ),
            "confidence": "High",
            "confidence_note": "The VLM papers share reliability, grounding, privacy, and routing failure modes that transfer to robot-scene reasoning.",
            "lab_action": (
                "Run robot-scene questions with removed objects, typographic distractors, privacy-sensitive documents, and token-budget limits, "
                "then require abstention or route changes when visual evidence is insufficient."
            ),
            "limit": 6,
        },
        {
            "title": "Controllable generation is becoming a safety and budget interface",
            "buckets": ["Generation", "Efficiency/Systems", "Safety/Alignment"],
            "ids": ["2608.12829", "2608.13478", "2608.12780", "2608.13460", "2608.13541", "2608.13518"],
            "needles": ["controllable", "unlearning", "sparse", "video", "steering", "world model", "generation"],
            "why": (
                "Semantic steering, MapRoute++ concept unlearning, sparse video attention, motion-guided frame interpolation, SCULPT part generation, "
                "and intervention-aware clinical world modeling treat generation as an interface for control, deletion, budget, or intervention history. "
                "The robotics transfer is to publish which knob changed the synthetic evidence and what deployment risk it is meant to expose."
            ),
            "confidence": "Medium",
            "confidence_note": "This cluster is broader CV generation, but it defines controllability and budget knobs for simulation stress inputs.",
            "lab_action": (
                "Generate scene or video stress cases with one named control knob at a time, then test whether object scale, motion, deleted concept, "
                "part structure, or runtime budget changes robot perception or planning in the expected direction."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Pre-commit robot monitor audit",
            "claim": (
                "Compare latent-future aborts, VLA progress probes, teleoperation relative-velocity warnings, and VLM abstention gates on identical "
                "contact and navigation failures; score warning lead time, false vetoes, and action authority."
            ),
        },
        {
            "title": "Embodied evidence acquisition suite",
            "claim": (
                "Create hidden-affordance and open-vocabulary navigation scenes where each extra view, semantic query, or free-space query must "
                "be tied to a target, route, or stop-decision change."
            ),
        },
        {
            "title": "Human-to-robot generation transfer check",
            "claim": (
                "Evaluate generated robot manipulation videos by functional contact, embodiment correctness, force or object-response plausibility, "
                "and downstream policy-imitation delta before treating them as scalable robot data."
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
        "meaning": "Included because it supports today's pre-commit evidence thesis.",
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
