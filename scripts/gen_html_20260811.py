#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-08-11 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260811 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-11"


PROFILE = {
    "date": DATE,
    "weekday": "Tue",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching 2026-08-11 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-08-11 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records official arXiv abstract and HTML availability checks for Tier A."
    ),
    "thesis": (
        "The August 11 batch shifts robotics from model scale toward evidence-controlled action interfaces. LIRA, GWM-VLA, "
        "SLIM, JEPA-WAM, World Tokens, VANE, and SC2-WM all ask where a representation becomes an executable correction, "
        "while CMU-Drive, FactorDrive, EMRD, Evidence-RL, consequence-sensitive token compression, and EndoMD-SLAM ask "
        "whether the measured evidence is causal, cooperative, or a shortcut. The practical APRL question is which state, "
        "token, message, or map update changes the downstream action under stress."
    ),
    "cluster_takeaway": (
        "Today's useful signal is that memory, world modeling, adaptation, cooperation, safety, and compression are all being "
        "reframed as action contracts: each must name the evidence it preserves and the failure condition that makes it stop."
    ),
    "trend_note": (
        "The Tuesday /new listing is large: 409 deduplicated papers and 336 ROI papers. The largest buckets are Generation, "
        "Foundation Models, Efficiency/Systems, Robot Learning, and Safety/Alignment, but the robotics-relevant signal is "
        "strongest where those buckets meet action routing, predictive latents, closed-loop correction, cooperative driving, "
        "evidence grounding, and map-update rejection."
    ),
    "cluster_specs": [
        {
            "title": "Action decoders expose the hidden VLM-to-control interface",
            "buckets": ["Robot Learning", "Foundation Models"],
            "ids": ["2608.07596", "2608.09771", "2608.09381", "2608.09730", "2608.08725", "2608.09176"],
            "needles": ["action decoder", "cross-layer", "predictive latent", "world tokens", "jepa-wam", "speculative decoding", "token compression"],
            "why": (
                "LIRA routes intermediate VLM layers into action fusion blocks, SLIM and JEPA-WAM turn predictive latents into action-grounded state, "
                "World Tokens uses world-model training while removing online video generation, WA-SpecDec cuts action-token latency, and consequence-sensitive compression asks which visual tokens are too costly to drop. "
                "The common research decision is to instrument the interface where representation depth, latent transition, and token budget actually change the action."
            ),
            "confidence": "High",
            "confidence_note": "Multiple VLA, latent world-model, and token-budget papers directly name action routing or action-grounded representation.",
            "lab_action": "Replay one manipulation task while logging selected VLM depth, latent transition error, world-token state, token budget, and action delta at every failure boundary.",
            "limit": 7,
        },
        {
            "title": "World models become closed-loop correction sensors",
            "buckets": ["Robot Learning", "Embodied AI", "Safety/Alignment", "Generation"],
            "ids": ["2608.07619", "2608.07548", "2608.09448", "2608.08023", "2608.09876", "2608.07981", "2608.09467"],
            "needles": ["world model", "future visual", "closed-loop", "test-time", "trajectory field", "physical", "failure-aware", "world-aware"],
            "why": (
                "GWM-VLA grounds latent dynamics in multi-view geometry and actions, SC2-WM uses world-model foresight to refine navigation before execution, VANE commits deployment updates only after future visual evidence, "
                "4D-WAM and energy-structured world models add spatiotemporal or physical consistency, and RecoverFly revisits unresolved UAV-VLA failures. "
                "A world model is becoming a sensor for when to correct, not only a generator of plausible futures."
            ),
            "confidence": "High",
            "confidence_note": "The cluster connects manipulation, VLN, aerial navigation, and world-action modeling around closed-loop correction.",
            "lab_action": "Add a correction-before-action table: predicted next observation, actual next observation, latent residual, update accepted/rejected, and resulting action change.",
            "limit": 7,
        },
        {
            "title": "Driving reasoning shifts from ego plans to cooperative evidence",
            "buckets": ["Autonomous Driving", "Foundation Models", "Safety/Alignment"],
            "ids": ["2608.07621", "2608.09591", "2608.09333", "2608.09098", "2608.08941", "2608.07577", "2608.09653"],
            "needles": ["cooperative", "driving", "planning-critical", "dual-horizon", "unstructured", "operational design", "safety filter", "out-of-vocabulary"],
            "why": (
                "CMU-Drive creates a cooperative closed-loop VLA driving benchmark, FactorDrive grounds reasoning in planning-critical spatial factors, DH-VLM adds dual-horizon cooperative latent reasoning, "
                "UnsDrive moves end-to-end control into unstructured mining scenes, ODD-to-action taxonomy asks what an ADS must demonstrate, and OOV road-object work prevents confident wrong labels. "
                "Driving VLA evaluation is moving toward which partner evidence, physical factor, or ODD condition changes the ego action."
            ),
            "confidence": "High",
            "confidence_note": "Several CV/RO and RO papers independently target cooperative, factor-grounded, unstructured, and safety-filtered driving decisions.",
            "lab_action": "Stress one driving scenario with missing V2V messages, occluded hazards, OOV objects, unstructured roads, and ODD boundaries while measuring action and waypoint changes.",
            "limit": 7,
        },
        {
            "title": "Safety is evidence causality under partial observability",
            "buckets": ["Safety/Alignment", "Foundation Models", "Embodied AI"],
            "ids": ["2608.08077", "2608.08021", "2608.09176", "2608.08167", "2608.07742", "2608.08622", "2608.08907"],
            "needles": ["evidence", "safety-critical", "memory", "hallucination", "consequence", "robustness", "visual tools", "grounding"],
            "why": (
                "EMRD splits embodied VLM safety into explore, map, remember, decide; Evidence-RL rewards answers that causally depend on object-centric evidence; "
                "Wiener filtering and VADER edit hallucination-prone representations, BRUCE escalates input corruption, ToolVision asks when a model should invoke visual tools, and SAIN grounds dialogue for mobile navigation. "
                "The safety decision is no longer just whether the model is correct, but whether the answer came from the evidence path that would survive a counterfactual stress test."
            ),
            "confidence": "High",
            "confidence_note": "The cluster has a large safety/foundation-model population and multiple papers explicitly centered on evidence grounding.",
            "lab_action": "Create paired counterfactual episodes with low light, removed evidence regions, high-consequence questions, and hallucination prompts, then measure action authority and answer changes.",
            "limit": 7,
        },
        {
            "title": "Geometry and SLAM decide when not to update the map",
            "buckets": ["3D/Scene", "Autonomous Driving", "Safety/Alignment", "Embodied AI"],
            "ids": ["2608.08949", "2608.09146", "2608.08016", "2608.07757", "2608.08476", "2608.07835", "2607.23755"],
            "needles": ["slam", "loop closure", "tracking", "lidar", "scene", "geometry", "pose", "semantic scene completion", "geo-localization"],
            "why": (
                "EndoMD-SLAM gates mapping under transient optical degradation, multi-submap implicit SLAM targets loop closure and drift, EgoTrack3D handles egocentric occlusion, "
                "incidence-aware LiDAR sampling attacks site-scan realism, RayLift represents depth uncertainty for scene completion, DAP-Pose fuses temporal physics for pose, and EvTrajGS reconstructs from unposed event streams. "
                "The shared robotics decision is when geometry should update memory, reject an observation, or change navigation/planning."
            ),
            "confidence": "Medium-High",
            "confidence_note": "3D/Scene has a strong SLAM/reconstruction signal and several adjacent driving/localization papers.",
            "lab_action": "Evaluate map systems with transient artifacts, loop closure drift, feature-sparse routes, depth uncertainty, and pose ambiguity; report update/reject decisions before ATE or reconstruction quality.",
            "limit": 7,
        },
        {
            "title": "Deployment budgets force selective correction rather than blanket scaling",
            "buckets": ["Efficiency/Systems", "Robot Learning", "Foundation Models", "Autonomous Driving"],
            "ids": ["2608.08630", "2608.09176", "2608.08725", "2608.09303", "2608.09467", "2608.07861", "2608.07835"],
            "needles": ["compression", "latency", "speculative", "uncertainty", "switching", "failure-aware", "cost", "budget", "cloud vlm"],
            "why": (
                "VLZip compresses interleaved long context, SAFE-CHEM switches policies under uncertainty, cloud VQA benchmarking exposes cost-latency tradeoffs, SeqLoc uses temporal evidence beyond one frame, "
                "RL-native distillation spends scored trajectories on few-step generation, Vid2WAM distills video priors into world-action models, and efficient radiology context reduction asks which visual context survives compression. "
                "The deployment pattern is selective preservation of the evidence that matters, not uniform scaling of every frame, token, or rollout."
            ),
            "confidence": "Medium",
            "confidence_note": "The cluster spans VLM systems and robot deployment papers; the unifying decision is resource allocation under risk.",
            "lab_action": "Run an equal-latency replay that removes tokens, context chunks, update candidates, and replay samples, then identify the first downstream decision that changes.",
            "limit": 7,
        },
    ],
    "research_topics": [
        {
            "title": "VLA interface failure microscope",
            "claim": "Measure layer routing, predictive-latent residuals, world-token state, and action deltas under camera shift, object swap, contact loss, and instruction ambiguity.",
        },
        {
            "title": "Future-evidence adaptation quarantine",
            "claim": "Hold VLA or world-model updates outside the live controller until future observations, uncertainty, and recovery labels justify committing them.",
        },
        {
            "title": "Shortcut-resistant robot evidence benchmark",
            "claim": "Stress embodied VLMs, driving VLAs, compression policies, and SLAM maps with low light, transient artifacts, OOV objects, delayed messages, and evidence-region counterfactuals.",
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
        "meaning": "Included because it supports the day's evidence-controlled action-interface thesis.",
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
        "Research Intelligence uses repository parser abstracts plus official arXiv HTML availability checks for selected Tier A papers. "
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
        f"Tier A {len(ri['papers'])} papers are checked against official arXiv parser abstracts and HTML availability, with evidence traces, "
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
