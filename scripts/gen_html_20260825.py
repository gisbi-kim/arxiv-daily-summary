#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-08-25 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260825 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-25"


PROFILE = {
    "date": DATE,
    "weekday": "Tue",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching 2026-08-25 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-08-25 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "The 2026-08-25 batch is about evidence authority rather than larger model form. "
        "VLA papers expose prompt text, typed spatial heads, memory events, intent labels, modality masks, and counterfactual negatives as separate reasons an action may change. "
        "Geometry papers push 3DGS, SLAM, visual localization, and point-cloud privacy toward robot-usable state: the map must know when it is localizable, stale, private, compressed, or physically trustworthy. "
        "World-action and VLM papers make the same move for future state, risk objects, video chunks, crops, audio triage, and instruction-conditioned hazards. "
        "The shared research decision is to name the evidence variable before trusting the policy, planner, mapper, generated future, or final answer."
    ),
    "cluster_takeaway": (
        "Today's core is not VLA, SLAM, video generation, or VLM reasoning by itself; it is deciding which prompt, spatial state, memory event, map update, rollout, or evidence route has authority to change the next action."
    ),
    "trend_note": (
        "Tuesday /new produced 307 deduplicated non-replacement papers and 254 ROI papers. "
        "Foundation Models and Generation are the largest buckets, but the strongest APRL signal comes from Robot Learning, 3D/Scene, Autonomy, and Efficiency papers that turn evidence selection into a control or map-validity contract."
    ),
    "cluster_specs": [
        {
            "title": "VLA control moves from behavior cloning to authorized prompt, memory, and spatial interfaces",
            "buckets": ["Robot Learning"],
            "ids": ["2608.23224", "2608.23138", "2608.22869", "2608.23478", "2608.22419", "2608.21740"],
            "needles": ["vla", "vision-language-action", "prompt-authority", "spatial grounding", "memory", "intent", "modality masking", "counterfactual"],
            "why": (
                "A VLA action is no longer treated as trustworthy simply because it matches a demonstrated motor command. "
                "TOWN-VLA makes retrieved text an authorized control intervention, Pointing-VLA gives PICK and PLACE typed spatial readouts, UniMem asks which event should update memory, INDI distills behavior-level intent, modality masking tests which sensor stream is reliable, and CounterAlign adds negative supervision for instruction-inconsistent actions. "
                "APRL should evaluate the interface that changed the action and the stress condition under which that authority should be revoked."
            ),
            "confidence": "High",
            "confidence_note": "Six Robot Learning papers independently expose prompt, spatial, memory, intent, modality, or negative-action authority boundaries.",
            "lab_action": (
                "Run matched VLA episodes with prompt appends, typed point and heatmap targets, event-memory toggles, intent labels, camera or language masks, and counterfactual negative actions; compare action delta, discontinuity, instruction violation, recovery timing, and terminal success."
            ),
            "limit": 6,
        },
        {
            "title": "World-action models shift from video fidelity to action-relevant future state",
            "buckets": ["Generation", "Autonomous Driving", "Safety/Alignment", "Efficiency/Systems"],
            "ids": ["2608.22067", "2608.23486", "2608.21402", "2608.22364", "2608.21414", "2608.22187"],
            "needles": ["world action", "wam", "future state", "future latent", "risk", "viewpoint", "on-policy", "simulator", "behavior-aware"],
            "why": (
                "World-action papers are separating useful future state from visually plausible future frames. "
                "DELE-w0.5 argues that manipulation needs the compact future state reached after action, GeoWAM moves driving WAMs into point-cloud geometry, selective cross-view consistency constrains only view-invariant action coordinates, WAM-OPD repairs distillation on the student's own rollout distribution, RiskWorld identifies object-level risk through imagined ego-object evolution, and BehaviorWorldGen makes surrounding-agent behavior a controllable simulator variable. "
                "The evaluation unit should be whether the predicted future changes the action under the correct risk or viewpoint condition."
            ),
            "confidence": "High",
            "confidence_note": "Six WAM/driving papers share action-aligned state, viewpoint robustness, on-policy distillation, risk-object, or behavior-simulation evidence.",
            "lab_action": (
                "Compare pixel WAM, future-state WAM, geometry WAM, selective cross-view consistency, on-policy distillation, and behavior-aware simulation under matched driving and manipulation tasks; score future-state error, action delta, risk-object identity, view-change degradation, and closed-loop recovery."
            ),
            "limit": 6,
        },
        {
            "title": "Geometry and SLAM evaluation moves from surface quality to governed robot-usable maps",
            "buckets": ["3D/Scene", "Autonomous Driving", "Safety/Alignment"],
            "ids": ["2608.22906", "2608.22896", "2608.23290", "2608.22054", "2608.22465", "2608.21380"],
            "needles": ["slam", "localization", "pose", "structure-from-motion", "gaussian", "point cloud", "privacy", "visual-language navigation", "gps"],
            "why": (
                "The geometry signal is not just more 3D reconstruction. "
                "AquaFlow makes underwater optical degradation a mapping variable, SuperMap manages stale open-vocabulary semantics over time, Spotter uses facade landmarks when GPS degrades, robust global SfM prunes ambiguous view-graph edges, M3ISR isolates camera geometry and representation efficiency for 3D/4D Gaussian splats, and RoboShape treats point-cloud privacy as an embodied mapping constraint. "
                "APRL should treat map updates, map compression, semantic aging, and privacy leakage as decisions that affect robot behavior."
            ),
            "confidence": "High",
            "confidence_note": "The geometry gate is triggered by 32 3D/Scene ROI papers plus multiple SLAM, localization, SfM, 3DGS, and point-cloud privacy signals.",
            "lab_action": (
                "Evaluate 3DGS SLAM, semantic 4D mapping, facade localization, SfM pruning, Gaussian compression, and point-cloud privacy encoders on degraded-media, stale-object, GPS-denied, ambiguous-match, camera-sweep, and room-disclosure splits; compare localization recovery, map update error, task success, and privacy leakage."
            ),
            "limit": 6,
        },
        {
            "title": "Embodied safety shifts from reaching a target to proving permission under fixed scenes",
            "buckets": ["Foundation Models", "Embodied AI", "Robot Learning", "Safety/Alignment", "3D/Scene"],
            "ids": ["2608.21928", "2608.22678", "2608.22149", "2608.21572", "2608.21735", "2608.21416"],
            "needles": ["safety", "risk", "inspection", "guaranteed", "certificate", "teleoperation", "digital twin", "permission", "constraint"],
            "why": (
                "Several papers make embodied success conditional on whether the task was actually permitted. "
                "GuardianBench fixes the scene and changes the instruction to expose latent contextual risk, RACO separates reaching from valid inspection confirmation, Meta-Ctrl guarantees syntactic and semantic plan constraints, sim-to-real betting certificates attach confidence to expensive real trials, safety-critical aerial teleoperation adds hierarchical barrier constraints, and operational digital twin clinics test embodied agents in task-level clinical scenes. "
                "The common decision is to evaluate when the robot should stop, abstain, reject, or certify instead of merely reaching something plausible."
            ),
            "confidence": "High",
            "confidence_note": "Six papers share fixed-scene instruction risk, inspection validity, formal constraints, performance certificates, safety barriers, or task-based digital twins.",
            "lab_action": (
                "Build fixed-scene instruction pairs, hard inspection distractors, formal plan constraints, small-sample sim-to-real bets, aerial barrier cases, and digital-twin clinical tasks; compare unsafe approval, valid-stop rate, constraint violation, certificate width, barrier intervention, and operator recovery."
            ),
            "limit": 6,
        },
        {
            "title": "VLM reasoning moves from final answers to selective evidence acquisition",
            "buckets": ["Foundation Models", "Efficiency/Systems"],
            "ids": ["2608.21762", "2608.23011", "2608.22359", "2608.22883", "2608.21883", "2608.22217"],
            "needles": ["crop routing", "evidence", "triage", "speculative", "chain-of-thought compression", "revisit", "long-video", "budgeted"],
            "why": (
                "VLM papers increasingly ask whether the system bought the right evidence before answering. "
                "GapSight learns when to look again from crop loss gaps, long-video RAG separates coarse indexing from fine evidence, acoustic triage chooses egocentric windows before video decoding, FOVEA adapts visual evidence for cache-friendly speculative decoding, VIG compresses reasoning by visual information gain, and uncertainty-aware radiology revisits suspicious regions. "
                "For embodied agents, the useful metric is whether extra perception changes an action or abstention under the intended evidence cost."
            ),
            "confidence": "High",
            "confidence_note": "Six papers independently route crop, temporal, audio, visual-token, reasoning-token, or revisit evidence under budget constraints.",
            "lab_action": (
                "Create inspection, navigation, and manipulation prompts with small labels, hidden defects, long-video evidence, audio pre-cues, and suspicious regions; compare direct answers, crop routing, temporal graph expansion, audio triage, focused speculative decoding, and revisit reasoning by evidence cost, abstention, and downstream action error."
            ),
            "limit": 6,
        },
        {
            "title": "Generation and inspection are judged by release-time calibration, not plausible samples",
            "buckets": ["Generation", "Safety/Alignment", "Foundation Models"],
            "ids": ["2608.21748", "2608.21839", "2608.21784", "2608.23070", "2608.21967", "2608.21425"],
            "needles": ["calibrate", "reward", "verifier", "risk control", "default shift", "world model", "quality inspection", "human preference"],
            "why": (
                "Generation papers are adding release gates around the sample, not only better sampling. "
                "Calibrate What You SHIP separates candidate-level calibration from post-selection release risk, FIRM-Video checks evidence before reward scoring, DefaultShift audits accelerated model defaults, the simulator survey asks which world-model capabilities still lag physics engines, trustworthy manufacturing inspection couples automation with human review under data scarcity, and calibrated distributional reward learning accounts for noisy human preferences. "
                "APRL should use generation only after the release decision exposes what failure mode the sample is certified not to hide."
            ),
            "confidence": "Medium",
            "confidence_note": "Six generation/inspection papers share calibration, verifier, default-shift, simulator-gap, or human-review evidence, though embodied benchmarks are still scattered.",
            "lab_action": (
                "Run text-to-image, text-to-video, manufacturing inspection, and world-model candidates through candidate-level versus post-selection calibration, checklist reward scoring, accelerated-model default shifts, simulator capability tests, and human-review deferral; compare shipped-risk violation, missed defect rate, physical inconsistency, and review load."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "VLA authority-boundary stress grid",
            "claim": (
                "Cross prompt appends, typed spatial heads, event memory, intent distillation, modality masks, and counterfactual negatives in identical VLA episodes; measure which interface predicts action divergence before failure."
            ),
        },
        {
            "title": "Governed map validity benchmark",
            "claim": (
                "Use underwater degradation, stale object semantics, GPS-denied facades, ambiguous SfM edges, Gaussian compression, and point-cloud privacy probes to test whether map governance changes robot task success."
            ),
        },
        {
            "title": "Evidence-budgeted embodied VLM evaluator",
            "claim": (
                "Create prompts where a crop, temporal chunk, audio cue, focused visual evidence path, or same-scene risk contrast should change action permission only under named evidence costs."
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
        "meaning": "Included because it supports today's evidence-authority and map-governance thesis.",
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
