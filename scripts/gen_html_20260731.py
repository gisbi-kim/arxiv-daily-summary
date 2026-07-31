#!/usr/bin/env python3
"""Generate the 2026-07-31 daily briefing from matching arXiv /new listings."""
from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, phylogeny_for, week_start
from gen_research_intelligence_20260731 import DATA as RI_DATA


DATE = "2026-07-31"

PROFILE = {
    "date": DATE,
    "weekday": "Fri",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from the matching 2026-07-31 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-07-31 arXiv /new listings. "
        "Tier A claims are checked against official arXiv HTML in the Research Intelligence edition."
    ),
    "thesis": (
        "The July 31 batch makes data, world models, and runtime repair converge on one question: which hidden state "
        "changes the robot action? Counterfactual Action Sensitivity Coverage and RedFlow turn demonstrations and failures "
        "into action-drift or corrective-target evidence. EgoGenesis, TacWAM, World Action Planner, ODEWorld, QQWorld, and "
        "PhiZero each ask which future state remains usable for planning: anchored 3D memory, tactile mechanics, pose-image "
        "rollout, physical-time flow, latent distribution shape, or physical language. ACE-Data-0 broadens the data side by "
        "capturing synchronized perception, body, object, audio, and contact streams, while LabEvolver shows how embodied "
        "agents can reuse experience only after safety and state are distilled. APRL should prioritize counterfactual data "
        "coverage and multi-channel WAM audits before running another generic VLA scaling comparison."
    ),
    "cluster_takeaway": (
        "Today's useful signal is not that world models are back; it is that papers are naming the state channel that makes a future actionable."
    ),
    "trend_note": (
        "Foundation Models, Generation, Efficiency/Systems, Robot Learning, and 3D/Scene all have high volume, but the robotics thread cuts across them: "
        "action-drift coverage, failed-action correction, tactile futures, anchored 3D memory, pose-image rollouts, physical-time flow, and evidence-routing under token limits."
    ),
    "cluster_specs": [
        {
            "title": "Robot data is ranked by counterfactual action sensitivity, not demo count",
            "buckets": ["Robot Learning", "Generation"],
            "ids": ["2607.27261", "2607.27782", "2607.27890", "2607.27549", "2607.28198", "2607.27784", "2607.28625"],
            "needles": ["counterfactual", "failure", "corrective", "data", "demonstration", "transfer", "action", "dexterous"],
            "why": (
                "Counterfactual Action Sensitivity Coverage selects examples by nuisance-induced action drift, RedFlow maps failed actions to successful corrective targets, "
                "Static In Dynamic Out augments moving-object manipulation, Cross-Embodiment Transfer and UniCross ask which behavior representation survives embodiment changes, "
                "and ACE-Data-0 provides synchronized ambient interaction state. The common decision is to score data by action information, not volume."
            ),
            "confidence": "High",
            "confidence_note": "Data selection, failure correction, cross-embodiment transfer, dexterous synthesis, and ambient capture all target action-relevant coverage.",
            "lab_action": (
                "For one imitation policy, log clean action, nuisance action, action drift, failed action, matched corrective target, preserved sensor channels, and post-repair success."
            ),
            "limit": 7,
        },
        {
            "title": "World-action models add missing physical channels to future prediction",
            "buckets": ["Robot Learning", "Generation", "Embodied AI"],
            "ids": ["2607.28243", "2607.28391", "2607.27599", "2607.27924", "2607.28415", "2607.28624", "2607.28362"],
            "needles": ["world", "action", "tactile", "physical", "latent", "planner", "memory", "dynamics"],
            "why": (
                "EgoGenesis adds anchored 3D memory and action geometry, TacWAM adds mechanics-aware tactile futures, World Action Planner searches over pose-image world-model rollouts, "
                "ODEWorld models physical-time flow, QQWorld regularizes latent tails, PhiZero reasons through physical language, and ShadowDancer learns unified action dynamics. "
                "The shared question is which channel makes the imagined future controllable."
            ),
            "confidence": "High",
            "confidence_note": "Multiple WAM papers independently expose channel-specific state variables rather than only future pixels.",
            "lab_action": (
                "Run equal-budget WAM ablations for visual-only, anchored 3D, tactile, pose-image, physical-time, and physical-language channels; report plan success and failure family."
            ),
            "limit": 7,
        },
        {
            "title": "Runtime correction turns failure traces into reusable policy gradients",
            "buckets": ["Robot Learning", "Autonomous Driving", "Safety/Alignment", "Embodied AI"],
            "ids": ["2607.27782", "2607.27511", "2607.28474", "2607.28623", "2607.27690", "2607.28451", "2607.27508"],
            "needles": ["failure", "safe", "alarm", "repair", "corrigible", "world", "aware", "aging"],
            "why": (
                "RedFlow localizes failed actions, surgical failure detection uses flow-matching world models, TEA-AgriVLN alarms on traversability mismatch, PAC-MAN adds perception-aware safety for humanoids, "
                "LabEvolver distills safe wet-lab experience, and hardware-aware aging asks how autonomous systems know their platform is degrading. "
                "The decision is to reuse failure traces while the safety boundary remains explicit."
            ),
            "confidence": "Medium-High",
            "confidence_note": "The papers span manipulation, surgery, agriculture, humanoid safety, wet labs, and hardware aging but align on runtime failure evidence.",
            "lab_action": (
                "Create a failure ledger with predicted failure, alarm state, corrective action, safety gate, hardware health, and whether the next attempt reused the experience safely."
            ),
            "limit": 7,
        },
        {
            "title": "Ambient and embodied data engines preserve synchronized state, not just video",
            "buckets": ["Robot Learning", "Generation", "Foundation Models"],
            "ids": ["2607.28625", "2607.28243", "2607.28394", "2607.28312", "2607.27549", "2607.28198", "2607.28624"],
            "needles": ["egocentric", "embodied", "hand-object", "memory", "capture", "world", "body", "transfer"],
            "why": (
                "ACE-Data-0 captures table-scale and room-scale human interaction with synchronized modalities, EgoGenesis synthesizes egocentric action video with anchored memory, "
                "hand-object interaction surveys and ObjectStream treat objects as memory anchors, and cross-embodiment/dexterous synthesis papers ask which behavior representation carries across bodies. "
                "The data asset is the synchronized state trace."
            ),
            "confidence": "High",
            "confidence_note": "Ambient capture, egocentric synthesis, object memory, and embodiment transfer all point to preserved state as the data moat.",
            "lab_action": (
                "Audit one candidate dataset for egocentric view, exocentric view, hand/body pose, object state, contact, audio, synchronization error, and downstream action probe."
            ),
            "limit": 7,
        },
        {
            "title": "3D geometry becomes an action prior that needs source and uncertainty tags",
            "buckets": ["3D/Scene", "Foundation Models", "Robot Learning"],
            "ids": ["2607.27749", "2607.28045", "2607.28300", "2607.27592", "2607.28442", "2607.28320", "2607.27825"],
            "needles": ["3d", "geometry", "reconstruction", "articulated", "odometry", "gaussian", "view", "depth"],
            "why": (
                "Rest-state articulated reconstruction infers joints before motion, RaDiVe targets robust 4D radar odometry, MonoVoc decouples geometry and semantics for lightweight 3D Gaussians, "
                "MeshFM and ViewMind3D push 3D understanding/QA, and dynamic surgical or UAV reconstruction papers bring uncertainty and camera motion into mapping. "
                "Geometry is now an action prior, so its source and uncertainty matter."
            ),
            "confidence": "High",
            "confidence_note": "The 3D/Scene count is large and includes articulated structure, odometry, open-vocabulary Gaussians, 3D QA, and dynamic reconstruction.",
            "lab_action": (
                "Tag each geometry field with source, confidence, expected failure mode, and action use: joint prior, pose update, object affordance, map query, or navigation recovery."
            ),
            "limit": 7,
        },
        {
            "title": "VLM reliability shifts toward evidence routing under token and grounding limits",
            "buckets": ["Foundation Models", "Efficiency/Systems", "Safety/Alignment"],
            "ids": ["2607.27667", "2607.27700", "2607.27823", "2607.27830", "2607.28463", "2607.28590", "2607.28225"],
            "needles": ["evidence", "token", "grounding", "hallucination", "routing", "verification", "risk", "visual"],
            "why": (
                "Witness evidence portfolios, token calibration before reasoning, verifier-guided object correction, intermediate-layer evidence routing, VisualRouter, VAD, and FaithEyes all ask "
                "which visual evidence survives compression, retrieval, or tool use. Robot VLM evaluation should treat right answer with wrong evidence as a failure."
            ),
            "confidence": "Medium-High",
            "confidence_note": "Foundation-model and systems papers repeat evidence preservation, routing, and grounding as the reliability axis.",
            "lab_action": (
                "For one robot VLM task, store evidence portfolio, kept tokens, routed frames, verifier correction, final answer, action, and wrong-evidence failure label."
            ),
            "limit": 7,
        },
    ],
    "research_topics": [
        {
            "title": "Counterfactual action-sensitivity coverage",
            "claim": (
                "Generate task-preserving nuisance pairs, measure policy action drift, then select examples that repair the largest causal action deviations."
            ),
        },
        {
            "title": "Multi-channel WAM failure audit",
            "claim": (
                "Compare visual, anchored 3D, tactile, pose-image, physical-time, and physical-language channels by the failure family each predicts or repairs."
            ),
        },
        {
            "title": "Ambient embodied data ledger",
            "claim": (
                "Before using a dataset, record synchronized modalities, spatial frame, contact coverage, object state, timing error, and downstream policy probe."
            ),
        },
        {
            "title": "Geometry-source action tags",
            "claim": (
                "Mark geometry priors used by a planner as observed, inferred, generated, or physically probed, with an uncertainty and stop condition."
            ),
        },
    ],
}


def abstract_card(paper: dict) -> dict:
    abstract = " ".join(str(paper.get("abstract", "")).split())
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", abstract) if s.strip()]
    problem = sentences[0] if sentences else "Abstract did not expose a clear problem statement."
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
        sentences[-1] if sentences else problem,
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
        "2607.28474", "2607.28415", "2607.28624", "2607.28312", "2607.28394",
        "2607.28045", "2607.28442", "2607.28300", "2607.27667", "2607.27700",
        "2607.27823", "2607.27830", "2607.28463", "2607.28590", "2607.28225",
        "2607.28623", "2607.27508", "2607.28451",
    }
    non_tier_c = tier_a_ids | tier_b_ids
    insights["tier_b"] = [abstract_card(p) for p in all_papers if p["arxiv_id"] in tier_b_ids and p["arxiv_id"] not in tier_a_ids]
    insights["tier_c"] = [abstract_card(p) for p in all_papers if p["arxiv_id"] not in non_tier_c]
    insights["tiering_note"] = (
        f"Tier A {len(tier_a_ids)} papers use official arXiv HTML evidence. "
        "Tier B and Tier C are conservative abstract-only cards from repository parser text and should not be read as full-text claims."
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
