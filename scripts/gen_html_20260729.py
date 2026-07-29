#!/usr/bin/env python3
"""Generate the 2026-07-29 daily briefing from matching arXiv /new listings."""
from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, phylogeny_for, week_start
from gen_research_intelligence_20260729 import DATA as RI_DATA


DATE = "2026-07-29"

PROFILE = {
    "date": DATE,
    "weekday": "Wed",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from the matching 2026-07-29 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-07-29 arXiv /new listings. "
        "Tier A claims are checked against official arXiv HTML in the Research Intelligence edition."
    ),
    "thesis": (
        "The July 29 batch shifts the useful comparison from model scale to exposed evidence. "
        "CoTinyVLA, IDR, SAM3D-VLA, DC-WAM, and pi R2 all ask what intermediate state the robot "
        "policy can reveal before the next action is trusted: phase reasoning, causal modality effect, "
        "3D object prior, dynamic token, or fresh proprioceptive channel. HiFi-UMI and SONG make a "
        "parallel move at the data and simulator layer by tying scale to pose fidelity, synchronization, "
        "replay, photorealistic episodes, and social-safety labels. FIRMGrasp and track-leakage-free "
        "photogrammetry show the validation version of the same lesson: confidence is only useful when "
        "the adverse tail and blind spot are named. APRL should turn today's batch into evidence-bearing "
        "rollout ledgers before comparing larger VLA or world-model checkpoints."
    ),
    "cluster_takeaway": (
        "Today's useful signal is the repeated conversion of hidden policy, data, and metric assumptions "
        "into observable contracts that can be logged during a rollout."
    ),
    "trend_note": (
        "Foundation Models and Efficiency/Systems dominate raw volume, but the robotics-relevant thread is "
        "compact VLA reasoning, high-fidelity human demonstration capture, dynamic-centric world-action modeling, "
        "risk-aware grasping, social-navigation simulation, and leakage-aware geometry validation."
    ),
    "cluster_specs": [
        {
            "title": "VLA policies expose reasoning, modality effect, and 3D object state",
            "buckets": ["Robot Learning", "Generation", "Safety/Alignment", "3D/Scene"],
            "ids": ["2607.25487", "2607.25516", "2607.25912", "2607.25918", "2607.26055", "2607.25397"],
            "needles": ["vla", "vision-language-action", "action", "modality", "causal", "3d", "world-action", "dynamic"],
            "why": (
                "CoTinyVLA makes a compact VLA auditable through Plan and Think spans, IDR estimates causal visual importance at test time, "
                "SAM3D-VLA injects object-centric 3D priors during training, DC-WAM routes attention to interaction-induced dynamics, and pi R2 "
                "separates fast proprioception from slower vision-language context. The common decision is to expose a control-relevant state "
                "before treating the action as valid."
            ),
            "confidence": "High",
            "confidence_note": "Five robot-control papers independently target hidden evidence inside the action path.",
            "lab_action": (
                "Log one action rollout with Plan/Think text, visual-counterfactual action delta, target-object 3D-prior flag, dynamic-token salience, "
                "fresh proprioception age, and final action error; test which field predicts failure first."
            ),
            "limit": 6,
        },
        {
            "title": "Data scale becomes fidelity, replay, and episode-generation infrastructure",
            "buckets": ["Robot Learning", "3D/Scene", "Embodied AI", "Autonomous Driving"],
            "ids": ["2607.25895", "2607.25219", "2607.26005", "2607.25106", "2607.25448", "2607.25570"],
            "needles": ["data", "dataset", "benchmark", "simulation", "navigation", "demonstrations", "replay", "self-play"],
            "why": (
                "HiFi-UMI argues that robot-free manipulation data becomes deployable only after pose, synchronization, and field-of-view fidelity are controlled. "
                "SONG builds photorealistic 3DGS social-navigation episodes with safety and compliance labels, while Pictura trains driving self-play directly "
                "from perspective camera views. These papers make data scale conditional on whether the collection or simulator preserves the deployment evidence."
            ),
            "confidence": "High",
            "confidence_note": "Manipulation, social navigation, and driving all tie scale to preserved state variables.",
            "lab_action": (
                "Create a data-source ledger with pose accuracy, sync error, view coverage, replay pass rate, simulator observation gap, safety label, and real-world transfer result."
            ),
            "limit": 6,
        },
        {
            "title": "World models move from future pixels to deployable planning interfaces",
            "buckets": ["Generation", "Efficiency/Systems", "Robot Learning"],
            "ids": ["2607.26056", "2607.25236", "2607.25337", "2607.26037", "2607.25541", "2607.25053"],
            "needles": ["world model", "planning", "latent", "action", "trajectory", "reactive", "control", "jepa"],
            "why": (
                "INTACT turns latent intent into a direct action law without heavy search, VisualPatchWorld induces inspectable code dynamics for planning, "
                "TD-JEPA mines temporal-distance costs from offline logs, and Wonder keeps video-world-model quality in the systems discussion. "
                "The research decision is no longer whether a model predicts the future, but whether the future representation is usable by a planner under latency and contact."
            ),
            "confidence": "Medium-High",
            "confidence_note": "The papers span latent, code, diffusion/flow, and video world models but align on planning usability.",
            "lab_action": (
                "Benchmark world models with plan success, number of candidate rollouts, latency, contact failure, and inspectable state variable, not only image prediction loss."
            ),
            "limit": 6,
        },
        {
            "title": "Geometry and localization papers separate self-consistency from robot-usable truth",
            "buckets": ["3D/Scene", "Autonomous Driving", "Foundation Models", "Efficiency/Systems"],
            "ids": ["2607.24852", "2607.25389", "2607.25524", "2607.25215", "2607.25788", "2607.25784"],
            "needles": ["localization", "reconstruction", "geometry", "slam", "matching", "map", "pose", "geo"],
            "why": (
                "The photogrammetry protocol blocks track leakage while warning that internal consistency does not certify absolute accuracy. HOME targets robust matching in "
                "structured or textureless video, ReLATE and city-scale cross-view localization fuse geo-localization evidence, and IMU calibration keeps attitude estimation grounded. "
                "Together they argue that geometry metrics need a declared leakage path, pose substrate, and downstream task boundary."
            ),
            "confidence": "High",
            "confidence_note": "Reconstruction validation, matching, geo-localization, and calibration all expose map-validity conditions.",
            "lab_action": (
                "Run a map-validation card with blocked leakage path, absolute-anchor availability, localization survival under texture loss, and downstream navigation recovery."
            ),
            "limit": 6,
        },
        {
            "title": "Safety margins become adverse-tail and intent-disambiguation variables",
            "buckets": ["Safety/Alignment", "Autonomous Driving", "Robot Learning"],
            "ids": ["2607.25049", "2607.25989", "2607.25327", "2607.25388", "2607.25985", "2607.25056"],
            "needles": ["risk", "failure", "trust", "planning", "robust", "safety", "collision", "control"],
            "why": (
                "FIRMGrasp discounts grasp quality by adverse friction tails, self-driving networks track co-drift and root-cause ambiguity, BAIT models human belief shaping, "
                "and game-theoretic racing or AUV planning add multi-agent and spatio-temporal constraints. The shared signal is that a safety claim must carry the uncertain variable "
                "that makes the final score fragile."
            ),
            "confidence": "Medium-High",
            "confidence_note": "The mechanisms differ, but each paper turns a safety failure into an explicit latent variable.",
            "lab_action": (
                "For grasping and navigation, log nominal score, adverse-tail variable, intent or belief estimate, root-cause hypothesis, and terminal failure; audit false certifications."
            ),
            "limit": 6,
        },
        {
            "title": "VLM reliability is turning into atomic perception and evidence-preservation tests",
            "buckets": ["Foundation Models", "Safety/Alignment", "Efficiency/Systems"],
            "ids": ["2607.24957", "2607.25294", "2607.25589", "2607.25641", "2607.24794", "2607.25789"],
            "needles": ["benchmark", "perception", "evidence", "reasoning", "memory", "reproducibility", "physical", "context"],
            "why": (
                "PerceptionBench breaks multimodal perception into atomic visual tests, CLBench-V evaluates context learning, the radiology audit checks benchmark reproducibility, "
                "OmniPhys targets physical commonsense, and temporal-granularity memory asks what evidence survives long-video reasoning. For robot VLMs, the important extension is "
                "right answer, wrong evidence: the model must preserve the visual fact that justifies the action."
            ),
            "confidence": "Medium",
            "confidence_note": "Mostly CV/VLM papers, but they define reliability tests directly useful for robot perception-action audits.",
            "lab_action": (
                "Add atomic-perception and evidence-preservation labels to one robot VLM benchmark: object state, spatial relation, remembered frame, final answer, and action error."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Evidence-bearing VLA rollout ledger",
            "claim": (
                "Attach phase reasoning, causal visual-effect delta, 3D object-prior flag, dynamic-token salience, fresh-state age, and final action error to each step."
            ),
        },
        {
            "title": "High-fidelity data source and replay audit",
            "claim": (
                "Record pose accuracy, synchronization, field of view, replay pass rate, simulator observation gap, and real-world transfer before adding a data source."
            ),
        },
        {
            "title": "Adverse-tail metric card",
            "claim": (
                "For each grasp, map, or navigation metric, publish the adverse variable it measures and the blind spot it cannot certify."
            ),
        },
        {
            "title": "World-model planning usability test",
            "claim": (
                "Compare latent, code, and flow world models by plan success, search budget, latency, contact failure, and inspectable state variable."
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
        "2607.26005", "2607.26055", "2607.26056", "2607.25236", "2607.25337",
        "2607.25389", "2607.25524", "2607.25215", "2607.25989", "2607.25327",
        "2607.24957", "2607.25294", "2607.25589", "2607.25641", "2607.24794",
        "2607.25789", "2607.25448", "2607.25106",
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
