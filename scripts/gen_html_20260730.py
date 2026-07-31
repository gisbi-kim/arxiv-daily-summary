#!/usr/bin/env python3
"""Generate the 2026-07-30 daily briefing from arXiv /pastweek date sections."""
from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, phylogeny_for, week_start
from gen_research_intelligence_20260730 import DATA as RI_DATA


DATE = "2026-07-30"

PROFILE = {
    "date": DATE,
    "weekday": "Thu",
    "week_start": week_start(DATE),
    "source_mode": "pastweek-date-section",
    "source_label": "arXiv cs.CV/pastweek + cs.RO/pastweek date section",
    "source_note": "Backfilled from the matching 2026-07-30 arXiv /pastweek date sections",
    "benchmark_note": (
        "Daily artifact generated from the 2026-07-30 arXiv /pastweek date sections. "
        "The daily paper cards are title/subject based because /pastweek does not expose abstracts; "
        "Tier A claims are checked against official arXiv HTML in the Research Intelligence edition."
    ),
    "thesis": (
        "The July 30 backfill batch turns robotics progress into an execution-contract problem. "
        "TurboVLA asks whether a language-conditioned policy can run locally at control-loop speed without "
        "centering an LLM. RL2-VLA, CheckVLA, Route-by-Kinematics, and explicit kinematic guidance show that "
        "a policy also needs adaptive steering, action-conditioned verification, expert routing, and analytic "
        "constraints during the episode. CG-World and ActSWM define the world-model version of the same question: "
        "state fields, branch lineage, and action-sensitive futures matter more than plausible videos. BioVLN "
        "and HumanCLAW make embodiment measurable through operational face, clearance, body skill, and failure "
        "attribution. APRL should use this batch to build per-step ledgers for latency, action consequence, "
        "repair trigger, world-state field, and body constraint."
    ),
    "cluster_takeaway": (
        "The common signal is that policies, world models, and benchmarks are being judged by what they expose "
        "while the robot still has time to recover."
    ),
    "trend_note": (
        "Robot Learning and Generation dominate the ROI set, but the robotics-relevant axis is not bucket size. "
        "It is the repeated attempt to type the hidden state behind an action: latency, latent steering, verifier risk, "
        "world-state branch, operational face, and body-level decision quality."
    ),
    "cluster_specs": [
        {
            "title": "Real-time VLA control moves from LLM interface to execution contract",
            "buckets": ["Robot Learning", "Foundation Models"],
            "ids": ["2607.27205", "2607.26991", "2607.26807", "2607.26513", "2607.26315", "2607.27180"],
            "needles": ["vla", "vision-language-action", "action", "real-time", "kinematic", "expert", "body"],
            "why": (
                "TurboVLA removes the LLM bottleneck from the action pathway, RL2-VLA adapts latent steering only when failure is likely, "
                "Route by Kinematics and analytic guidance split routing from observation, and HumanCLAW asks whether a VLM can choose actions through a body. "
                "The shared decision is to define what execution state is visible before the next chunk is trusted."
            ),
            "confidence": "High",
            "confidence_note": "Six VLA or embodied-action papers expose different execution interfaces rather than only reporting final success.",
            "lab_action": (
                "Run one manipulation trace with fields for policy latency, instruction state, latent steering magnitude, expert route, kinematic constraint, body command, and terminal failure."
            ),
            "limit": 6,
        },
        {
            "title": "Execution-time verification and adaptive repair become policy modules",
            "buckets": ["Robot Learning", "Autonomous Driving", "Safety/Alignment"],
            "ids": ["2607.26789", "2607.26991", "2607.26802", "2607.26460", "2607.26434", "2607.26809"],
            "needles": ["verification", "risk", "repair", "failure", "planning", "reinforcement", "adaptive", "constrained"],
            "why": (
                "CheckVLA predicts action-conditioned consequences and rewrites the repairable suffix, RL2-VLA gates latent steering with failure prediction, "
                "risk-aware planning names probabilistic safety, and hardware-constrained RL keeps cost in the control loop. "
                "The research decision is to intervene based on a typed risk signal, not a generic confidence score."
            ),
            "confidence": "High",
            "confidence_note": "Verification, steering, safety assessment, and constrained hardware RL align around recovery while acting.",
            "lab_action": (
                "For each chunked episode, log predicted consequence, observed consequence, risk threshold, intervention time, suffix rewrite, hardware constraint, and recovery result."
            ),
            "limit": 6,
        },
        {
            "title": "World models are judged by action-sensitive state instead of plausible futures",
            "buckets": ["Generation", "Robot Learning", "Embodied AI"],
            "ids": ["2607.26452", "2607.26712", "2607.27017", "2607.26657", "2607.26754", "2607.26903"],
            "needles": ["world", "state", "action", "latent", "planning", "predictive", "experience", "physical"],
            "why": (
                "CG-World records typed state and branch lineage, ActSWM tests whether futures remain distinguishable under different actions, "
                "latent-identifiability work asks what physical parameters can be known, and Enfold/experience-synthesis papers fold world-generator computation into control. "
                "The common gate is action sensitivity, not visual plausibility."
            ),
            "confidence": "High",
            "confidence_note": "Dataset protocol, latent world model, identifiability, and embodied-control papers all target state/action observability.",
            "lab_action": (
                "Create a world-model sample schema with state fields, action, observation, branch id, action-recovery probe, and downstream planning success."
            ),
            "limit": 6,
        },
        {
            "title": "Embodied benchmarks type the body, usable face, and trust boundary",
            "buckets": ["Embodied AI", "Foundation Models", "Robot Learning"],
            "ids": ["2607.26914", "2607.27180", "2607.26121", "2607.26148", "2607.26567", "2607.26232"],
            "needles": ["navigation", "body", "trustworthy", "humanoid", "grasp", "speech", "benchmark", "embodied"],
            "why": (
                "BioVLN replaces point-goal navigation with operational-face and clearance zones, HumanCLAW decouples VLM decision from motor failure, "
                "trustworthy embodied intelligence frames graded system levels, and speech-to-grasp plus background manipulation work show the input and scene conditions that make action claims fragile."
            ),
            "confidence": "Medium-High",
            "confidence_note": "Navigation, body action, trust framework, speech-conditioned grasp, and manipulation detection papers all refine the embodied task contract.",
            "lab_action": (
                "Annotate one lab-navigation or tabletop task with target body, clearance, operational face, commanded skill, speech/text input, and failure attribution."
            ),
            "limit": 6,
        },
        {
            "title": "3D and Gaussian reconstruction shift toward structure-usable maps",
            "buckets": ["3D/Scene", "Generation", "Efficiency/Systems"],
            "ids": ["2607.26889", "2607.26595", "2607.26763", "2607.26645", "2607.26578", "2607.26234"],
            "needles": ["gaussian", "3d", "point cloud", "structure", "reconstruction", "scene", "sparse", "simulation"],
            "why": (
                "StructureGS targets articulated-object structure, SpatialQ judges 3DGS scene quality through an MLLM lens, point-cloud distillation and generation compress 3D datasets, "
                "and spline boundary representations tie reconstruction to simulation. The geometry signal is whether the map preserves part, quality, and simulation constraints, not just rendering."
            ),
            "confidence": "Medium-High",
            "confidence_note": "The 3D/Scene count is small but coherent around structured Gaussian or point-cloud artifacts.",
            "lab_action": (
                "Evaluate reconstructed objects with part-boundary consistency, quality explanation, compactness, simulation boundary fit, and downstream manipulation pose success."
            ),
            "limit": 6,
        },
        {
            "title": "VLM reliability papers test evidence preservation under domain risk",
            "buckets": ["Foundation Models", "Safety/Alignment", "Efficiency/Systems"],
            "ids": ["2607.27145", "2607.26554", "2607.26536", "2607.27066", "2607.26565", "2607.26885"],
            "needles": ["reasoning", "evidence", "alignment", "token", "ood", "compression", "contrastive", "decision"],
            "why": (
                "Spatial reasoning, medical token compression, tone-pressure decoding, scientific-figure alignment, OOD representation trajectories, and medical cross-modal alignment all ask "
                "whether a model keeps the evidence that justifies a decision under domain pressure. For robot VLMs this becomes right-action, wrong-evidence auditing."
            ),
            "confidence": "Medium",
            "confidence_note": "Mostly CV/VLM papers, but they define compact tests for evidence, compression, and OOD reliability.",
            "lab_action": (
                "Add evidence-preservation labels to one robot VLM task: visual fact, compressed token set, reasoning output, action, OOD cue, and failure family."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Execution-time VLA ledger",
            "claim": (
                "Record latency, latent steering, action-conditioned predicted consequence, calibrated risk, expert route, and suffix repair for each action chunk."
            ),
        },
        {
            "title": "Action-sensitive world-state schema",
            "claim": (
                "Store state fields, action, observation, branch lineage, action-recovery probe, and plan success before comparing world-model losses."
            ),
        },
        {
            "title": "Operational-face embodiment split",
            "claim": (
                "Replace point-goal success with body zone, clearance, usable side, commanded body skill, and decision-versus-execution failure attribution."
            ),
        },
        {
            "title": "Structure-usable Gaussian validation",
            "claim": (
                "Score 3DGS and point-cloud assets by part boundary, quality explanation, compactness, simulation compatibility, and downstream robot pose success."
            ),
        },
    ],
}


def abstract_card(paper: dict) -> dict:
    abstract = " ".join(str(paper.get("abstract", "")).split())
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", abstract) if s.strip()]
    problem = sentences[0] if sentences else "The /pastweek source exposes title and subject metadata but not an abstract."
    method = next(
        (
            s
            for s in sentences[1:]
            if re.search(r"\b(we propose|we present|we introduce|we develop|our method|our framework|our approach)\b", s, re.I)
        ),
        sentences[1] if len(sentences) > 1 else problem,
    )
    meaning = next(
        (
            s
            for s in reversed(sentences)
            if s not in {problem, method}
            and re.search(r"\b(experiment|result|demonstrat|outperform|achiev|show|improv|validate|evaluate)\w*\b", s, re.I)
        ),
        sentences[-1] if sentences else "Treat this as a conservative title/subject card, not a full-text claim.",
    )
    phy = phylogeny_for(paper["bucket"], paper)
    return {
        "arxiv_id": paper["arxiv_id"],
        "title": paper["title"],
        "bucket": paper["bucket"],
        "badge": paper.get("badge", ""),
        "reading_depth": "abstract-only",
        "problem": problem,
        "method": method,
        "meaning": meaning,
        "phylogeny": phy,
    }


def enrich_insights() -> None:
    root = Path(__file__).resolve().parents[1]
    insights_path = root / "insights" / f"{DATE}.json"
    trends = json.loads((root / "trends" / f"{DATE}.json").read_text(encoding="utf-8"))
    insights = json.loads(insights_path.read_text(encoding="utf-8"))
    classified = json.loads((root / "out" / "classified.json").read_text(encoding="utf-8"))

    insights["source_listing_date"] = trends["source_listing_date"]
    insights["source_mode"] = trends["source_mode"]
    insights["daily_new_counts"] = trends["daily_new_counts"]
    insights["paper_autopsies"] = [
        {
            "arxiv_id": paper["arxiv_id"],
            "title": paper["title"],
            "reading_depth": "full-text",
            "status_quo_belief": paper["status_quo"],
            "friction": paper["friction"],
            "hidden_premise": paper["hidden_premise"],
            "conceptual_move": paper["conceptual_move"],
            "mechanism": paper["mechanism"],
            "decisive_evidence": paper["evidence"],
            "falsification_frontier": paper["falsification"],
            "adversarial_read": paper["adversarial"],
            "transferable_thinking_tool": paper["thinking_tool"],
            "transfer_boundary": paper["transfer_boundary"],
            "evidence_trace": paper["evidence"],
            "source": "official arXiv HTML",
        }
        for paper in RI_DATA["papers"]
    ]
    insights["cross_paper_decisions"] = RI_DATA["synthesis"]
    insights["frontier_memory"] = {
        "new": [item for item in RI_DATA["frontier_memory"] if item["signal"] == "new"],
        "strengthening": [item for item in RI_DATA["frontier_memory"] if item["signal"] == "strengthening"],
        "commoditizing": [],
        "contradiction": [],
        "missing_axis": [item for item in RI_DATA["frontier_memory"] if item["signal"] == "missing_axis"],
    }
    portfolio = {"BUILD": "Build moat", "EXPLOIT": "Exploit", "EXPLORE": "Explore"}
    strategy_board = []
    for item in RI_DATA["strategy"]:
        paper_path = [a["url"] for a in item["assets"] if "arxiv.org" in a["url"]]
        asset_path = [a["url"] for a in item["assets"] if "arxiv.org" not in a["url"]]
        if not asset_path:
            asset_path = [f"APRL internal asset: {item['title']} protocol"]
        strategy_board.append({
            "opportunity": item["title"],
            "portfolio": portfolio[item["priority"]],
            "thesis": item["thesis"],
            "scores": {
                "strategic_fit": item["scores"]["fit"],
                "asymmetry": item["scores"]["novelty"],
                "timing": item["scores"]["timing"],
                "tractability": item["scores"]["feasibility"],
                "defensibility": item["scores"]["moat"],
                "scientific_depth": item["scores"]["evidence"],
            },
            "one_week_probe": item["one_week"],
            "four_week_build": item["four_week"],
            "success_metric": item["metric"],
            "stop_condition": item["stop"],
            "paper_path": paper_path,
            "asset_path": asset_path,
        })
    insights["strategy_board"] = strategy_board

    all_papers = [p for bucket in classified["buckets"].values() for p in bucket["papers"]]
    tier_a_ids = {paper["arxiv_id"] for paper in RI_DATA["papers"]}
    tier_b_ids = {
        "2607.26889", "2607.27017", "2607.26657", "2607.26807", "2607.26513",
        "2607.26802", "2607.26121", "2607.26595", "2607.27145", "2607.26554",
        "2607.26536", "2607.27066", "2607.26985", "2607.26809",
    }
    non_tier_c = tier_a_ids | tier_b_ids
    insights["tier_b"] = [abstract_card(p) for p in all_papers if p["arxiv_id"] in tier_b_ids and p["arxiv_id"] not in tier_a_ids]
    insights["tier_c"] = [abstract_card(p) for p in all_papers if p["arxiv_id"] not in non_tier_c]
    insights["tiering_note"] = (
        f"Tier A {len(tier_a_ids)} papers use official arXiv HTML evidence. "
        "Tier B and Tier C are conservative title/subject cards for this backfill because /pastweek does not expose abstracts."
    )
    insights["research_intelligence"] = {
        "html": f"posts/{DATE}-research-intelligence.html",
        "json": f"intelligence/{DATE}.json",
        "source_prompt": RI_DATA["source_prompt"],
    }
    insights_path.write_text(json.dumps(insights, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build(PROFILE, "out/cv_new.json", "out/ro_new.json")
    enrich_insights()

    post_path = Path(__file__).resolve().parents[1] / "posts" / f"{DATE}.html"
    doc = post_path.read_text(encoding="utf-8")
    doc = doc.replace(
        ".thesis strong{color:#fef08a}",
        ".thesis strong{color:#fef08a}.ri-callout{display:flex;justify-content:space-between;gap:16px;align-items:center;margin:-12px 0 28px;padding:14px 18px;border:1px solid #67e8f9;border-radius:10px;background:#ecfeff;color:#164e63}.ri-callout a{font-weight:750;white-space:nowrap}@media(max-width:760px){.ri-callout{align-items:flex-start;flex-direction:column}}",
    )
    ri_callout = (
        f"<section class=\"ri-callout\"><span><strong>Today's Research Intelligence</strong> "
        f"Tier A {len(RI_DATA['papers'])} papers are checked against official arXiv HTML, with evidence traces, "
        f"adversarial reads, frontier memory, and APRL strategy board.</span>"
        f"<a href=\"{DATE}-research-intelligence.html\">Open Research Intelligence</a></section>"
    )
    doc = re.sub(r"</section>\n(<h2>.*?</h2>)", f"</section>\n{ri_callout}\n\\1", doc, count=1, flags=re.S)
    post_path.write_text(doc, encoding="utf-8")
