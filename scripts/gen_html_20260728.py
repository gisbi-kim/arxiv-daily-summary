#!/usr/bin/env python3
"""Generate the 2026-07-28 daily briefing from matching arXiv /new listings."""
from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, phylogeny_for, week_start
from gen_research_intelligence_20260728 import DATA as RI_DATA


DATE = "2026-07-28"

PROFILE = {
    "date": DATE,
    "weekday": "Tue",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from the matching 2026-07-28 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-07-28 arXiv /new listings. "
        "Tier A claims are checked against official arXiv HTML in the Research Intelligence edition."
    ),
    "thesis": (
        "The July 28 batch is less about larger robot-policy backbones than about the evidence surfaces "
        "that make an action, map, or navigation decision trustworthy. DeVA, N0-VTLA, N0-TWAM, and FutureRTC "
        "all expose physical state before action execution: depth and affordance cues, latent tactile tokens, "
        "future touch, and execution-time observations. ArmnetBench and Data Pyramid turn embodied progress "
        "into data provenance plus repeatable real-world rollout infrastructure. The SLAM, off-road navigation, "
        "visual localization, driving, and risk-guided flight papers make the same point from another angle: "
        "intermediate state estimates need association confidence, freshness, and risk horizon. APRL should "
        "therefore treat physical-state logging and resettable evaluation cells as first-class research assets."
    ),
    "cluster_takeaway": (
        "Today's useful signal is not a single winning architecture. It is the repeated move of turning hidden "
        "robot state into a measurable contract before claiming generalization."
    ),
    "trend_note": (
        "Efficiency/Systems and Generation dominate raw volume, but the robotics-relevant thread is tactile "
        "world-action modeling, asynchronous execution, scalable real-world evaluation, semantic mapping, and "
        "risk-timed navigation."
    ),
    "cluster_specs": [
        {
            "title": "Robot action models expose physical state before trusting the next chunk",
            "buckets": ["Robot Learning", "Generation", "Efficiency/Systems"],
            "ids": ["2607.24159", "2607.23782", "2607.23783", "2607.24008", "2607.24267", "2607.24296"],
            "needles": ["tactile", "action", "robot", "future", "chunk", "policy", "physical", "world model"],
            "why": (
                "DeVA injects physical guidance into action prediction, N0-VTLA predicts latent tactile tokens, "
                "N0-TWAM makes touch a native world-action stream, and FutureRTC corrects stale observations before execution. "
                "Together they argue that the action tensor is not the right unit of comparison unless the rollout also records the "
                "physical state that made the action valid."
            ),
            "confidence": "High",
            "confidence_note": "Multiple robot-policy papers share the same action-to-physical-state interface move.",
            "lab_action": (
                "Run one tabletop task with four logs per action chunk: raw action, predicted depth or affordance, predicted tactile state, "
                "and execution-time observation age. Score failure prediction before score-based policy comparison."
            ),
            "limit": 6,
        },
        {
            "title": "Embodied data work shifts from more demonstrations to typed evaluation infrastructure",
            "buckets": ["Robot Learning", "Embodied AI", "Efficiency/Systems"],
            "ids": ["2607.24744", "2607.24481", "2607.23108", "2607.22997", "2607.23784", "2607.23515"],
            "needles": ["data", "benchmark", "evaluation", "real-world", "manipulation", "curriculum", "demonstrations", "pipeline"],
            "why": (
                "Data Pyramid separates robot, simulation, UMI-style, egocentric, and general data by fidelity and scalability, while ArmnetBench "
                "makes physical evaluation cells cheap and repeatable. The supporting manipulation papers reinforce the same concern: without a typed "
                "data source and a rollout-label protocol, more demonstrations can hide the failure family rather than fix it."
            ),
            "confidence": "High",
            "confidence_note": "Data taxonomy and real-world evaluation infrastructure appear as explicit papers, not as background assumptions.",
            "lab_action": (
                "Create a data ledger for one APRL manipulation line with source tier, robot alignment, reset cost, label fields, and expected blind spots; "
                "then run a small low-cost-cell replication with two policies."
            ),
            "limit": 6,
        },
        {
            "title": "Navigation safety becomes a future-risk and freshness problem",
            "buckets": ["Robot Learning", "Autonomous Driving", "Embodied AI", "3D/Scene"],
            "ids": ["2607.23565", "2607.23743", "2607.23511", "2607.23910", "2607.24431", "2607.24369"],
            "needles": ["risk", "navigation", "driving", "planner", "flight", "future", "collision", "traversability"],
            "why": (
                "Risk-guided flight predicts directional future collision risk, off-road navigation learns traversability-aware global routes, and MOJITO "
                "keeps dense sensor evidence connected to driving actions. The shared question is when a planning or perception estimate expires before "
                "the terminal safety metric notices."
            ),
            "confidence": "Medium-High",
            "confidence_note": "The papers span flight, off-road navigation, driving, and cooperative perception, but align on timed autonomy evidence.",
            "lab_action": (
                "For ten navigation episodes, log risk horizon, traversability confidence, localization source, action delay, and terminal route deviation; "
                "test which field changes earliest before failure."
            ),
            "limit": 6,
        },
        {
            "title": "Semantic maps are judged by association and localization survival",
            "buckets": ["3D/Scene", "Embodied AI", "Safety/Alignment", "Autonomous Driving"],
            "ids": ["2607.23384", "2607.23901", "2607.24409", "2607.23758", "2607.23962", "2607.23468"],
            "needles": ["slam", "localization", "mapping", "pose", "road", "gnss", "object", "recovery"],
            "why": (
                "Semantic Object SLAM targets data-association ambiguity, AR shared workspaces and high-end street imagery focus localization substrate, "
                "and road reconstruction or GNSS-spoofing detection extend the same concern to driving scenes. Map quality matters only if the robot can "
                "keep association and pose confidence alive during deployment."
            ),
            "confidence": "High",
            "confidence_note": "SLAM, visual localization, road reconstruction, and robust tracking form a coherent map-validity axis.",
            "lab_action": (
                "Build a semantic-map stress split with repeated objects, viewpoint change, and sensor dropout; score association flips, relocalization time, "
                "and downstream navigation recovery instead of only trajectory error."
            ),
            "limit": 6,
        },
        {
            "title": "MLLM reliability moves from confidence to compositional evidence execution",
            "buckets": ["Foundation Models", "Safety/Alignment", "Embodied AI", "Efficiency/Systems"],
            "ids": ["2607.22864", "2607.23052", "2607.24407", "2607.22716", "2607.23193", "2607.23504"],
            "needles": ["spatial", "logic", "reasoning", "evidence", "token", "memory", "navigation", "multimodal"],
            "why": (
                "Spatial-IQ decomposes spatial intelligence into hierarchical tests, Similarity Is Not Logic shows dual-encoder retrieval can violate boolean constraints, "
                "and token-compression or memory-navigation papers ask whether compressed context still preserves the evidence needed for action. Reliability is therefore "
                "not self-confidence; it is whether the representation executes the intended spatial or logical constraint."
            ),
            "confidence": "Medium-High",
            "confidence_note": "Different model families converge on evidence preservation under compression, memory, or compositional queries.",
            "lab_action": (
                "Add right-answer-wrong-evidence labels to a robot VLM benchmark: spatial decomposition, boolean constraint, retained visual token, and final action error."
            ),
            "limit": 6,
        },
        {
            "title": "Runtime compression becomes a control-loop variable",
            "buckets": ["Efficiency/Systems", "Generation", "Foundation Models"],
            "ids": ["2607.22708", "2607.23265", "2607.23844", "2607.24027", "2607.23046", "2607.23193"],
            "needles": ["edge", "token", "compression", "cache", "latency", "real-time", "pruning", "deployment"],
            "why": (
                "On-device UI VLMs, video token condensation, diffusion caching, attention sparsification, and omnichannel token compression all reduce compute, "
                "but robotics turns that saving into a control question: does the compressed representation still preserve the evidence needed before the next action cycle?"
            ),
            "confidence": "Medium",
            "confidence_note": "The systems papers are broad, but the control-loop implication is consistent with FutureRTC and edge VLM evidence.",
            "lab_action": (
                "Benchmark a robot VLM with retained-token maps, latency, action-cycle miss rate, and failure prediction under the same task, not only throughput."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Physical-state action contract benchmark",
            "claim": (
                "Store action chunk, predicted depth/affordance, predicted tactile state, observation age, and realized post-action state in one rollout schema."
            ),
        },
        {
            "title": "Embodied data ledger and low-cost cell replication",
            "claim": (
                "Tie each data source to fidelity, reset cost, label cost, and failure family, then validate two policies on a small resettable arm-cell setup."
            ),
        },
        {
            "title": "Timed navigation-state freshness test",
            "claim": (
                "Attach risk horizon, traversability confidence, localization source, and association confidence to each navigation step before the route fails."
            ),
        },
        {
            "title": "Evidence-preserving compression audit",
            "claim": (
                "Track which visual tokens, memory frames, or spatial relations survive compression and whether their loss predicts wrong robot actions."
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
        "2607.22864", "2607.23052", "2607.23504", "2607.23511", "2607.23743",
        "2607.23910", "2607.24409", "2607.24431", "2607.22708", "2607.22716",
        "2607.23193", "2607.23265", "2607.23844", "2607.24027", "2607.23901",
        "2607.23758", "2607.23962", "2607.23468",
    }
    non_tier_c = tier_a_ids | tier_b_ids
    insights["tier_b"] = [abstract_card(p) for p in all_papers if p["arxiv_id"] in tier_b_ids and p["arxiv_id"] not in tier_a_ids]
    insights["tier_c"] = [abstract_card(p) for p in all_papers if p["arxiv_id"] not in non_tier_c]
    insights["tiering_note"] = (
        f"Tier A {len(tier_a_ids)} papers use official arXiv HTML evidence. Tier B and Tier C are conservative abstract-only cards "
        "built from repository parser text and should not be read as full-text claims."
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
