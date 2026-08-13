#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-08-13 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260813 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-13"


PROFILE = {
    "date": DATE,
    "weekday": "Thu",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching 2026-08-13 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-08-13 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "The 2026-08-13 batch shifts robotics value from bigger end-to-end policies toward execution contracts: "
        "what evidence is carried into adaptation, which slice or guard can veto a driving action, and when a map, "
        "memory, or generated world is trusted enough to change the robot's next move."
    ),
    "cluster_takeaway": (
        "Today's common decision is not whether a model can perceive or generate. It is whether the system can name "
        "the evidence that authorizes adaptation, command substitution, memory update, route choice, or stop decision."
    ),
    "trend_note": (
        "Thursday /new produced 152 deduplicated non-replacement papers and 121 ROI papers. Generation, "
        "Efficiency/Systems, Foundation Models, Safety/Alignment, Robot Learning, and Autonomous Driving were the "
        "largest buckets, but the strongest APRL signal came from papers that expose action-level evidence contracts."
    ),
    "cluster_specs": [
        {
            "title": "VLA adaptation moves from more data to structured execution evidence",
            "buckets": ["Robot Learning", "Foundation Models", "Safety/Alignment"],
            "ids": ["2608.11671", "2608.11739", "2608.11363", "2606.29699", "2608.12122", "2608.11769"],
            "needles": ["vision-language-action", "vla", "demonstration", "action token", "failure", "minimal data", "dexterous"],
            "why": (
                "StellaVLA, G0.5, MiDAS, OpenVLA failure monitoring, HandEdit, and hand-prior diagnosis all ask how a "
                "robot should reuse evidence when the scene, embodiment, or initial pose changes. The key shift is from "
                "collecting another trajectory to exposing which plan, reasoning token, residual update, warning signal, "
                "or embodiment prior actually changed the next action."
            ),
            "confidence": "High",
            "confidence_note": "Six selected papers touch VLA adaptation, action reasoning, warning signals, or embodiment-aware manipulation.",
            "lab_action": (
                "Run the same manipulation task under object, viewpoint, and initial-pose shifts while logging structured demo fields, "
                "reasoning/action tokens, residual updates, activation warning lead time, and final contact failure."
            ),
            "limit": 6,
        },
        {
            "title": "Driving safety turns average scores into slice, rule, and counterfactual contracts",
            "buckets": ["Autonomous Driving", "Generation", "Safety/Alignment"],
            "ids": ["2608.12051", "2608.11451", "2608.11601", "2608.12198", "2608.11407", "2608.11580"],
            "needles": ["risk", "safety", "counterfactual", "driving", "traffic", "hd map", "behavior planning"],
            "why": (
                "RISC, neuro-symbolic safety guards, counterfactual driving world models, TrafficDiffuser, RoadWeaver, "
                "and real-world behavior planning all reject a single aggregate driving score. They force the release "
                "question toward which risk slice was covered, which rule changed the command, and whether factual "
                "evidence was preserved before simulating an alternative action."
            ),
            "confidence": "High",
            "confidence_note": "Driving papers independently converge on coverage, guard intervention, counterfactual replay, and simulator-map evidence.",
            "lab_action": (
                "Pick three high-risk driving slices, define the rule or factual evidence expected to change the command, "
                "then compare learned planning, guard substitution, and world-model counterfactuals on identical episodes."
            ),
            "limit": 6,
        },
        {
            "title": "Embodied navigation needs causal memory and dynamic-world stress",
            "buckets": ["Embodied AI", "Robot Learning", "Generation"],
            "ids": ["2608.12308", "2608.11901", "2608.11876", "2608.11246", "2608.11350", "2608.12063"],
            "needles": ["navigation", "memory", "embodied", "dynamic", "world generation", "loco-manipulation", "skill"],
            "why": (
                "DreamFly, DaViNCi, D3D-GEN, embodied-agent harness work, skill-harness evolution, and sparse RL from "
                "SMPC demonstrations all treat long-horizon embodiment as a memory and stress-design problem. The useful "
                "question is whether historical evidence, dynamic elements, simulator domain grounding, or controller-generated "
                "demonstrations change route, stop, or recovery decisions before task success is reported."
            ),
            "confidence": "High",
            "confidence_note": "Navigation, simulator, harness, and loco-manipulation papers share the same dynamic closed-loop evaluation axis.",
            "lab_action": (
                "Create paired indoor/outdoor episodes with dynamic movers, missing views, and sparse reward recovery, then measure route change, "
                "stop timing, and recovery action under causal-memory or generated-world ablations."
            ),
            "limit": 6,
        },
        {
            "title": "3D scene assets become localization, grounding, and topology interfaces",
            "buckets": ["3D/Scene", "Efficiency/Systems", "Embodied AI"],
            "ids": ["2608.11263", "2608.11928", "2608.11699", "2608.11938", "2608.11697", "2608.11409"],
            "needles": ["3d", "gaussian", "place recognition", "topology", "point cloud", "surface", "metric"],
            "why": (
                "GeoUniPR, Seed2GS, STAR, sparse voxel reconstruction, point-cloud segmentation, and robotic ultrasound "
                "surface modeling all push 3D work beyond visual reconstruction. Their value appears when geometry "
                "decides cross-modal localization, object identity, expert routing, sparse reconstruction reliability, or real-time probe control."
            ),
            "confidence": "High",
            "confidence_note": "The geometry bucket is smaller than generation, but its representative papers are decision-facing.",
            "lab_action": (
                "Evaluate each 3D asset with corrupted or missing geometry and record whether place recognition, object extraction, "
                "routing, segmentation, or robot probe control changes before visual quality metrics move."
            ),
            "limit": 6,
        },
        {
            "title": "VLM reliability is becoming reference-use and router calibration",
            "buckets": ["Foundation Models", "Safety/Alignment", "Efficiency/Systems"],
            "ids": ["2608.11474", "2608.11847", "2608.12127", "2608.12158", "2608.11907", "2608.12220"],
            "needles": ["hallucination", "visual reference", "router", "calibration", "spatial reasoning", "closed-loop", "evaluation"],
            "why": (
                "TTH, LookBack, SCOPE-Router, Context-Calibrated DPO, semantic closed-loop evaluation, and SCOUT all "
                "separate fluent answers from evidence-grounded answers. For robotics this matters because a VLM should "
                "not route a task, justify a hazard, or approve an action unless its object token, visual reference, "
                "spatial reasoning step, and model-choice cost are visible."
            ),
            "confidence": "Medium-High",
            "confidence_note": "The VLM reliability papers are not all robotics papers, but they define directly portable evidence gates.",
            "lab_action": (
                "Run robot-scene questions through hallucination control, visual-reference scoring, and cost-aware routing, then remove the referenced object "
                "or spatial cue and measure whether the selected action or model route changes."
            ),
            "limit": 6,
        },
        {
            "title": "Generation pipelines are judged by controllability and deployment budget",
            "buckets": ["Generation", "Efficiency/Systems", "Autonomous Driving", "3D/Scene"],
            "ids": ["2608.12032", "2608.11618", "2608.12232", "2608.11537", "2608.11562", "2608.11452"],
            "needles": ["diffusion", "video", "generation", "compression", "scaling", "semantic", "benchmark"],
            "why": (
                "LoSA, generative video compression, ScaleVid, generative semantic segmentation, reflection simulation, and generation benchmarks "
                "show that generation is being evaluated by what can be controlled, accelerated, or audited. The robotics transfer is to stop "
                "grading generated scenes by appearance alone and require controllable object scale, reflection removal, semantic evidence, and runtime budget."
            ),
            "confidence": "Medium",
            "confidence_note": "This cluster is broader CV generation, but it defines simulation and perception stress knobs useful for robotics.",
            "lab_action": (
                "Use generated videos or scenes as stress inputs only after recording which control knob changed object scale, reflection, compression, "
                "semantic mask, or runtime, then test whether the robot decision changed in the expected direction."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Evidence-routed VLA adaptation grid",
            "claim": (
                "Compare raw demonstrations, structured demonstrations, reasoning/action tokens, residual online RL, and activation warnings under the "
                "same task-shift split; score the first action change and warning lead time before final success."
            ),
        },
        {
            "title": "Coverage-qualified driving replay",
            "claim": (
                "Publish driving results with risk slices, rule-triggered command substitutions, factual/counterfactual world-model pairs, and a clear "
                "statement of which slices remain uncovered."
            ),
        },
        {
            "title": "Executable 3D memory stress suite",
            "claim": (
                "Corrupt target masks, dynamic elements, topology, and metric scale in maps or generated worlds, then evaluate target choice, stop timing, "
                "route, base placement, and recovery action rather than render quality alone."
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
        "meaning": "Included because it supports today's execution-contract thesis.",
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
