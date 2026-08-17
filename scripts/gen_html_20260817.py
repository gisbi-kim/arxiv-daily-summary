#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-08-17 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260817 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-17"


PROFILE = {
    "date": DATE,
    "weekday": "Mon",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching 2026-08-17 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-08-17 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "The 2026-08-17 batch shifts robotics evaluation from final scorekeeping to explicit commitment interfaces: "
        "VLAs expose tool calls, process judges, handoff states, and reaction latency; world models preserve belief, "
        "temporal-logic predicates, and failed repair arguments; and autonomous systems make failure discovery, "
        "barriers, and safety certificates part of the same deployment contract."
    ),
    "cluster_takeaway": (
        "Today's common decision is whether a system can name the evidence that should change, delay, repair, or block the next action before a rollout is reduced to success or failure."
    ),
    "trend_note": (
        "Monday /new produced 116 deduplicated non-replacement papers and 97 ROI papers. Generation and Foundation Models "
        "were large buckets, but the strongest robotics signal came from VLA process interfaces, predicate-preserving world models, "
        "geometry/mapping efficiency, and event-matched safety evaluation."
    ),
    "cluster_specs": [
        {
            "title": "VLA execution shifts from monolithic actions to tool, judge, and latency interfaces",
            "buckets": ["Robot Learning"],
            "ids": ["2608.14047", "2608.14284", "2608.13924", "2608.14379", "2608.14144"],
            "needles": ["tool-use", "process assessment", "preference", "reaction-critical", "on-policy", "vla"],
            "why": (
                "ART, PRM-as-a-Judge, BICPO-VLA, ReflexVLA, and self-supervised visual on-policy distillation all reject the idea that final rollout success is enough. "
                "They expose a tool call, dense progress curve, request-to-handoff state, reaction latency, or augmented-view teacher signal as the place where the next action should be judged."
            ),
            "confidence": "High",
            "confidence_note": "Five Robot Learning papers independently expose VLA/tool/process/latency interfaces.",
            "lab_action": (
                "Run identical manipulation episodes while varying tool availability, process-judge threshold, action-handoff delay, and inference latency, "
                "then measure which interface changes the next action before terminal success changes."
            ),
            "limit": 5,
        },
        {
            "title": "World models move from plausible futures to preserved beliefs and verifiable predicates",
            "buckets": ["Generation"],
            "ids": ["2608.13923", "2608.13678", "2608.13901", "2608.14022", "2608.14530"],
            "needles": ["belief", "world model", "temporal logic", "failure diagnosis", "predicate", "causal", "world state"],
            "why": (
                "OpenBelief-Nav, hint2, Onto-EV-WM, ForgeWM, and Marionette all make the future auditable rather than merely realistic. "
                "They preserve object-observation provenance, temporal-logic proposition progress, failed predicate arguments, low-latency action-conditioned rollout, or explicit geometry state."
            ),
            "confidence": "High",
            "confidence_note": "Five world-model papers share a predicate, belief, or structured-state commitment rather than generic video generation.",
            "lab_action": (
                "Create navigation and manipulation tasks with ambiguous objects, temporal-logic constraints, and repairable failures, then compare early-commit labels, "
                "belief-preserving memory, predicate-gated repair, and action-conditioned world-model rollout on target choice and stop decisions."
            ),
            "limit": 5,
        },
        {
            "title": "Geometry and mapping value moves from image fidelity to deployable spatial contracts",
            "buckets": ["3D/Scene", "Autonomous Driving"],
            "ids": ["2608.14266", "2608.14136", "2608.14027", "2608.14394", "2608.14428", "2608.14282"],
            "needles": ["bundle adjustment", "gaussian", "event", "radar", "lidar", "3d", "geometry"],
            "why": (
                "LiDAR bundle adjustment, octree Gaussian consistency, event-camera local features, radar graph detection, GhostPoint, and MAGneT-3D all ask whether a spatial representation survives deployment constraints. "
                "The relevant output is a faster map, a stable anchor, an invariant radar feature, an occluded LiDAR structure, or a domain-general 3D proposal."
            ),
            "confidence": "High",
            "confidence_note": "The geometry/SLAM/reconstruction watch lens is triggered by multiple LiDAR, pose, radar, Gaussian, and 3D detection signals.",
            "lab_action": (
                "Compare LiDAR BA maps, Gaussian anchors, event features, radar graphs, and monocular 3D proposals under sparse scans, domain shift, dynamic objects, and memory limits, "
                "then score localization, detection, update cost, and navigation-relevant degradation."
            ),
            "limit": 6,
        },
        {
            "title": "Safety testing shifts from average risk to matched events and certifiable failure coverage",
            "buckets": ["Robot Learning", "Safety/Alignment", "Autonomous Driving", "Generation"],
            "ids": ["2608.14024", "2608.13719", "2608.14239", "2608.14531", "2608.14481"],
            "needles": ["evaluation", "failure discovery", "barrier", "certificate", "hazard", "safety"],
            "why": (
                "SSP, coverage-aware active evaluation, a temporal barrier framework, tube-based certificates, and hazard-informed envelopes all make safety evaluation event-structured. "
                "Instead of comparing unmatched domains or average risk, they preserve the safety-critical interaction, correct proxy failures, and state what correction or envelope keeps the system deployable."
            ),
            "confidence": "High",
            "confidence_note": "Driving, manipulation, aerial, articulated-vehicle, and urban-mobility papers converge on matched event and certificate logic.",
            "lab_action": (
                "Define one long-tail event with preserved topology, participant roles, timing, response constraints, and permitted corrections across simulator, proxy, and target robot, "
                "then evaluate target failures found per real test and the certificate violations each proxy misses."
            ),
            "limit": 5,
        },
        {
            "title": "Embodied agents acquire physical evidence before resolving language goals",
            "buckets": ["Foundation Models", "Embodied AI", "Robot Learning", "Efficiency/Systems", "3D/Scene"],
            "ids": ["2608.13605", "2608.13723", "2608.14160", "2608.14466", "2608.14082"],
            "needles": ["active perception", "navigation", "occupancy", "expected free energy", "partial observability", "object-goal"],
            "why": (
                "Active embodied disambiguation, Graph-MambaNav, OccPlanner, expected-free-energy path planning, and PILOT all treat navigation as evidence acquisition under partial observability. "
                "A language goal or pixel goal is not resolved until extra views, object relations, occupancy, information gain, or temporal context changes the route."
            ),
            "confidence": "Medium-High",
            "confidence_note": "The papers span target disambiguation, object navigation, pixel-goal grounding, exploration, and UAV planning.",
            "lab_action": (
                "Build paired scenes where labels, depth, traversability, and target-relevant object relations are hidden from the first view, then measure which observation changes target grounding, route, or stop timing."
            ),
            "limit": 5,
        },
        {
            "title": "Benchmarks become domain-transfer audits, not isolated leaderboards",
            "buckets": ["3D/Scene", "Autonomous Driving", "Robot Learning"],
            "ids": ["2608.14049", "2608.14085", "2608.14207", "2608.14287", "2608.14028"],
            "needles": ["benchmark", "simulation", "collaborative", "domain shift", "human demonstrations", "dataset"],
            "why": (
                "FlatLab, CoDS, MMUSV-Sim, acoustic UAV detection, and AdvDex all make the evaluation domain itself part of the research claim. "
                "The key question is whether the benchmark preserves material behavior, multi-agent sensing, weather/noise/domain shift, or human-to-robot action alignment enough to predict real deployment."
            ),
            "confidence": "Medium",
            "confidence_note": "The cluster is methodologically broad, but all selected papers expose benchmark/domain-transfer assumptions.",
            "lab_action": (
                "For each new dataset or simulation benchmark, predeclare which physical variable must transfer, then test a held-out domain where material, wave, noise, pose, or embodiment mismatch should break the claim."
            ),
            "limit": 5,
        },
    ],
    "research_topics": [
        {
            "title": "Commitment-interface VLA audit",
            "claim": (
                "Compare tool calls, PRM progress curves, action-handoff correction, latent future prediction, and reaction latency on the same manipulation failures; "
                "score warning lead time, veto authority, false intervention rate, and terminal success."
            ),
        },
        {
            "title": "Predicate-preserving world memory",
            "claim": (
                "Evaluate object-belief provenance, temporal-logic proposition tracking, ontology-gated repair, and explicit world-state prediction in tasks where early label commitment causes a wrong route or wrong repair."
            ),
        },
        {
            "title": "Matched-event safety transfer harness",
            "claim": (
                "Build a synthetic-to-sim-to-physical safety event chain with transfer audits, proxy-corrected failure discovery, and temporal/tube certificate checks before reporting deployment risk."
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
        "meaning": "Included because it supports today's commitment-interface thesis.",
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
