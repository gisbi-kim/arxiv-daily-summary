#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-08-19 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260819 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-19"


PROFILE = {
    "date": DATE,
    "weekday": "Wed",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching 2026-08-19 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-08-19 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "The 2026-08-19 batch is less about adding another foundation model and more about deciding which evidence gets authority over the next action. "
        "Robot papers expose skill libraries, code rewriting, force reflexes, action-flow world models, safety shields, and cue-following tests as separable execution interfaces; "
        "geometry papers ask whether scale, instance structure, bundle-adjustment validity, and edge SLAM fidelity survive robot use; "
        "and VLM/benchmark papers turn modality conflict, conditional branching, and safety specifications into variables that can falsify a deployment claim."
    ),
    "cluster_takeaway": (
        "Today's core is not a larger VLA or a prettier 3D scene; it is deciding which cue, map variable, safety predicate, or runtime interface is allowed to change the robot's next action."
    ),
    "trend_note": (
        "Wednesday /new produced 141 deduplicated non-replacement papers and 114 ROI papers. Robot Learning is the largest bucket, "
        "but the highest APRL signal comes from runtime authority allocation, robot-usable geometry validity, evidence-provenance benchmarks, and efficiency work that preserves sparse control evidence."
    ),
    "cluster_specs": [
        {
            "title": "VLA control moves from one action decoder to runtime authority allocation",
            "buckets": ["Robot Learning"],
            "ids": ["2608.17209", "2608.16978", "2608.17432", "2608.17453", "2608.17717", "2608.18077"],
            "needles": ["vla", "skill", "code", "force", "stereo", "intent", "action flow", "world model", "general robot learning"],
            "why": (
                "Existing VLA evaluation often treats the action decoder as the single place where a policy succeeds or fails. "
                "Teach-and-Grow externalizes reusable skill blocks, VLCP rewrites failed control code during an episode, UniReflex gives contact a fast force-reflex channel, "
                "EATR-Stereo routes auxiliary camera evidence through embodiment state, CompCPZ preserves disjunctive intent, and Hydra-0 turns action flow into a shared world-model interface. "
                "The shared research decision is to expose who has authority to change the next action before final success is trusted."
            ),
            "confidence": "High",
            "confidence_note": "Six Robot Learning papers independently expose skill, code, contact, stereo, intent, or action-flow authority interfaces.",
            "lab_action": (
                "Run identical tabletop perturbation episodes with object displacement, language ambiguity, stereo occlusion, and contact loss, then compare skill-block routing, code replanning, force-reflex gating, stereo-token routing, disjunctive intent preservation, and action-flow prediction by next-action delta, warning lead time, and final success."
            ),
            "limit": 6,
        },
        {
            "title": "Robot safety evaluation splits task success from authorized cues and physical specifications",
            "buckets": ["Robot Learning", "Embodied AI", "Foundation Models"],
            "ids": ["2608.17386", "2608.17600", "2608.17496", "2608.17318", "2608.17129"],
            "needles": ["safety", "specification", "cue", "authorized", "branch", "vqa", "manipulation-grounded", "risk", "shield"],
            "why": (
                "A robot can reach the goal while following an unauthorized visual cue, violating a safety predicate, or answering a hidden-object question without doing the needed manipulation. "
                "ManiGuard separates task success from LTL-grounded safety specifications, LIBERO-VIFO tests authorized versus unauthorized cue following, calibrated predictive safety rolls action chunks forward before shielding them, CondVLN isolates if-then branch execution, and PROBE forces VLM agents to manipulate clutter before answering. "
                "The evaluation unit shifts from final success to the evidence and constraint that authorized the action."
            ),
            "confidence": "High",
            "confidence_note": "Five papers share a specification, cue-authority, branch-choice, or manipulation-grounding evaluation contract.",
            "lab_action": (
                "Create manipulation and navigation episodes where the goal is achievable but one safety predicate, visual cue authorization, branch condition, or hidden-object evidence path can fail independently; compare policy rankings under task success, predicate violation, cue-following error, branch-choice error, and shield intervention."
            ),
            "limit": 5,
        },
        {
            "title": "Geometry and SLAM shift from reconstruction output to metric validity and queryable maps",
            "buckets": ["3D/Scene"],
            "ids": ["2608.17553", "2608.18028", "2608.17535", "2608.17832", "2608.17874", "2608.17283"],
            "needles": ["slam", "bundle adjustment", "gaussian", "3d", "4d", "scale", "uncertainty", "query", "reconstruct", "edge"],
            "why": (
                "The geometry signal is not another visual-quality race. Scalix asks learned depth to carry uncertainty into metric-scale SLAM, InitFree BA shows that a low optimization objective can hide invalid Euclidean reconstruction, GroupForward makes feed-forward Gaussians instance-queryable, GenRec separates pixels that must be reconstructed from pixels that may be generated, Jetson-ORB-SLAM3 preserves feature fidelity on edge hardware, and UniQuery4R turns 4D reconstruction into reusable query-conditioned geometry. "
                "For robots, a map is useful only if scale, instance identity, uncertainty, and edge latency survive downstream localization or manipulation."
            ),
            "confidence": "High",
            "confidence_note": "The geometry/SLAM/reconstruction watch lens is triggered by 17 3D/Scene ROI papers and multiple SLAM, BA, Gaussian, 4D, scale, and edge signals.",
            "lab_action": (
                "Compare monocular SLAM, InitFree BA, feed-forward Gaussian maps, reconstruction-generation split models, edge ORB-SLAM, and query-conditioned 4D reconstruction on sparse-view, scale-drift, lighting, dynamic-object, and small-instance retrieval conditions; score localization, manipulation recovery, query accuracy, update cost, and invalid metric reconstructions."
            ),
            "limit": 6,
        },
        {
            "title": "Driving robustness asks which evidence should change the trajectory immediately",
            "buckets": ["Autonomous Driving", "Robot Learning"],
            "ids": ["2608.17095", "2608.17882", "2608.18035", "2608.17178", "2608.17044", "2608.16966"],
            "needles": ["driving", "trajectory", "traffic", "saliency", "city", "vehicle", "localization", "attention", "robustness"],
            "why": (
                "Driving papers are less interested in another offline perception number and more interested in the evidence that changes a trajectory. "
                "Attention steering perturbs safety-critical actor tokens at inference time, ControlledShifts standardizes which trajectory-distribution tail is withheld, traffic-element awareness tests signs and lights across planners and VLAs, saliency-guided self-supervision preserves safety-critical video regions, AI City expands multi-camera and traffic-anomaly evaluation, and roadside-radar localization connects infrastructure sensing with vehicle state. "
                "The common decision is to name the scene variable that should alter the immediate maneuver."
            ),
            "confidence": "High",
            "confidence_note": "Driving, trajectory prediction, traffic-element, saliency, challenge, and localization papers share an evidence-to-action evaluation axis.",
            "lab_action": (
                "Build lane-change, intersection, traffic-light, cross-city, and sensor-drop stress splits, then compare attention steering, controlled OOD splitting, traffic-element injection, saliency masking, challenge-style multi-camera reasoning, and connected localization by trajectory displacement, near-miss rate, rule violation, and recovery action."
            ),
            "limit": 6,
        },
        {
            "title": "VLM reliability becomes source provenance instead of one confidence score",
            "buckets": ["Foundation Models", "Safety/Alignment"],
            "ids": ["2608.17205", "2608.17490", "2608.17607", "2608.17723", "2608.17427", "2608.18009"],
            "needles": ["source", "evidence", "reliance", "fusion", "reasoning", "gauge", "hallucination", "memory", "3d question"],
            "why": (
                "Reliability papers make the model reveal which evidence source actually won. Which Source Wins shows modality reliance can reverse by task, KAGES diagnoses when adding more foundation-model views hurts fusion, PathoArgus evaluates whether whole-slide answers use the supplied tissue evidence, gauge reading studies reliability under specialization and transfer, CAST counterfactually chooses anatomy regions during decoding, and Memory Tree querying asks which 3D key frames deserve context. "
                "For robotics, confidence is not enough; the decisive modality, view, region, or memory node must be visible."
            ),
            "confidence": "High",
            "confidence_note": "Six VLM papers independently target modality conflict, view-set selection, evidence chains, gauge reliability, hallucination mitigation, and 3D memory querying.",
            "lab_action": (
                "Evaluate robot inspection and navigation questions under image-text conflict, redundant camera views, missing tissue or object evidence, gauge-range ambiguity, counterfactual occlusion, and long-video memory limits; compare source-reliance shifts, selected-view authority, evidence-chain completeness, and action error."
            ),
            "limit": 6,
        },
        {
            "title": "Efficiency work shifts from raw latency to preserving sparse spatial or temporal evidence",
            "buckets": ["Efficiency/Systems", "Generation"],
            "ids": ["2608.17425", "2608.17787", "2608.17995", "2608.17402", "2608.17657", "2608.17700"],
            "needles": ["token", "latency", "edge", "event", "pruning", "efficient", "moe", "cache", "dynamic", "sparse"],
            "why": (
                "The efficiency signal is not simply cheaper inference. GSToken gives compact tokens explicit 3D geometric support, ETHEREAL builds hardware for sparse event streams, AViTS chooses which diffusion tokens deserve high-resolution refinement, MoE-ViE studies sparse expert capacity for vision encoders, pruning work decides which weights can be removed without biasing the model, and environment-invariant deepfake detection targets spurious shortcut removal. "
                "The research decision is to preserve the sparse spatial or temporal evidence that can still change a downstream judgment."
            ),
            "confidence": "Medium-High",
            "confidence_note": "Efficiency papers span 3D tokens, event hardware, adaptive generation tokens, MoE vision encoders, pruning, and invariant representations.",
            "lab_action": (
                "Sweep token, expert, pruning, event-cache, and resolution budgets while holding task difficulty fixed, then measure retained geometry support, event timing, semantic detail, shortcut suppression, edge latency, and downstream robot or inspection decision error rather than speed alone."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Runtime-authority robot policy grid",
            "claim": (
                "Put skill-block composition, code replanning, force reflexes, stereo evidence routing, action-flow prediction, and safety-shield vetoes around identical manipulation perturbations; measure which interface changes the next action before final success changes."
            ),
        },
        {
            "title": "Robot-usable geometry validity suite",
            "claim": (
                "Evaluate SLAM, bundle adjustment, Gaussian maps, feed-forward 4D reconstruction, and edge ORB pipelines under scale drift, sparse views, dynamic objects, small-instance retrieval, and lighting shifts; score metric validity and downstream task impact together."
            ),
        },
        {
            "title": "Evidence-provenance embodied benchmark",
            "claim": (
                "Build episodes where image/text conflict, conditional branch predicates, unauthorized cues, hidden-object manipulation, and safety specifications can fail independently; require every action or answer to identify the evidence path that authorized it."
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
        "meaning": "Included because it supports today's evidence-authority thesis.",
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
