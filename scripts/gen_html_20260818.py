#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-08-18 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260818 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-18"


PROFILE = {
    "date": DATE,
    "weekday": "Tue",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching 2026-08-18 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-08-18 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "The 2026-08-18 batch makes robot intelligence less about bigger backbones and more about runtime evidence control: "
        "VLAs expose process rewards, tactile residuals, counterfactual recovery, stop-aware chunking, and test-time search; "
        "Gaussian and LiDAR maps become task-conditioned memories that decide what to update, relight, ignore, or discard; "
        "and benchmarks increasingly ask whether the physical evidence path behind a score survives real deployment constraints."
    ),
    "cluster_takeaway": (
        "Today's common decision is to expose the variable that can change the next robot action: contact residual, process reward, map update, view authority, or failure event, before final success is trusted."
    ),
    "trend_note": (
        "Tuesday /new produced 355 deduplicated non-replacement papers and 291 ROI papers. Robot Learning and Generation were the largest buckets, "
        "but the highest APRL signal came from VLA runtime authority, 3DGS/LiDAR map governance, embodied benchmark provenance, and efficiency methods that preserve action-relevant evidence."
    ),
    "cluster_specs": [
        {
            "title": "VLA control shifts from policy output to runtime repair, residuals, and stop authority",
            "buckets": ["Robot Learning"],
            "ids": ["2608.14822", "2608.15816", "2608.15680", "2608.16172", "2608.16885", "2608.15139"],
            "needles": ["vla", "recovery", "tactile", "process reward", "stop-aware", "test-time computation", "structured action"],
            "why": (
                "Existing VLA evaluation often waits for terminal success, but this group exposes the intermediate authority that should alter execution. "
                "CoRe imagines recovery before physical trial, ViTaR bounds tactile correction as a residual, Robo-Dopamine 2.0 scores process history, "
                "SparkVLA ranks stop versus action prefixes, tau0-VLA allocates extra computation to hard subtask choices, and StructRL preserves structured exploration through denoising."
            ),
            "confidence": "High",
            "confidence_note": "Six Robot Learning papers independently target VLA recovery, contact, reward, stopping, search, and exploration interfaces.",
            "lab_action": (
                "Run the same LIBERO/RoboCasa-style perturbation tasks with mid-episode goal changes, object displacement, and contact loss, then compare counterfactual recovery, tactile residual authority, process-reward ranking, stop-prefix choice, and test-time search by warning lead time, action delta, and final success."
            ),
            "limit": 6,
        },
        {
            "title": "Gaussian and LiDAR maps move from passive reconstruction to task-conditioned update decisions",
            "buckets": ["3D/Scene"],
            "ids": ["2608.14713", "2608.15024", "2608.14902", "2608.14986", "2608.14996", "2608.15317"],
            "needles": ["gaussian", "slam", "lidar", "localization", "relight", "mapping", "memory"],
            "why": (
                "The geometry signal is not another rendering-quality race. SpotlessGS treats lighting as a robotics perception variable, MotionGS-SLAM models blur with event timing, "
                "geometry-aware 3DGS mapping decides where scarce online density should go, GaussMemory learns what task objects deserve memory, HP2-SLAM keeps LiDAR ICP interpretable under degeneracy, and LightLoc++ attacks sensor-configuration transfer."
            ),
            "confidence": "High",
            "confidence_note": "The geometry/SLAM/reconstruction watch lens is triggered by 26 3D/Scene ROI papers and multiple SLAM, LiDAR, localization, Gaussian, and memory signals.",
            "lab_action": (
                "Compare Gaussian maps, LiDAR ICP maps, and learned localization heads under lighting changes, camera blur, sensor-configuration shift, dynamic objects, and task-relevant occlusion, then score localization, manipulation recovery, update cost, and false stable memories."
            ),
            "limit": 6,
        },
        {
            "title": "Embodied benchmarks shift from scene labels to physical evidence and long-tail coverage",
            "buckets": ["Foundation Models", "Embodied AI"],
            "ids": ["2608.15410", "2608.16476", "2608.15284", "2608.16590", "2608.16843"],
            "needles": ["flood", "long-tail", "navigation", "trajectory", "embodied", "security", "harness"],
            "why": (
                "FloodReasonBench, in-the-wild urban navigation, VTInstructor, Zetta, and embodied-agent security all ask whether a benchmark preserves the physical evidence that matters for action. "
                "The shared shift is from generic scene understanding to coverage of flood hazards, urban long tails, trajectory geometry, closed-loop runtime critics, and attack entry points."
            ),
            "confidence": "High",
            "confidence_note": "Five embodied or foundation-model papers frame evaluation around domain evidence, navigation coverage, physical execution, or trust boundaries.",
            "lab_action": (
                "Build a navigation-response suite where low light, flood water, occlusion, long-tail urban scenes, and prompt or perception attacks are separate stress conditions, then measure which evidence source changes route choice, stop timing, recovery action, and edge latency."
            ),
            "limit": 5,
        },
        {
            "title": "Driving and multi-camera evaluation moves toward evidence that changes immediate safety action",
            "buckets": ["Autonomous Driving", "Foundation Models", "Safety/Alignment"],
            "ids": ["2608.14767", "2608.16041", "2608.14603", "2608.15539", "2608.15437", "2608.16614"],
            "needles": ["driving", "cooperative", "multi-camera", "bev", "scenario", "calibration", "safety"],
            "why": (
                "NARRATE grounds driving explanations in synchronized road data, ScenarioCharacterization makes safety features portable across trajectory datasets, semantic-aware cooperative perception balances bandwidth and safety horizon, "
                "CrossView asks which camera carries decisive evidence, MM-BEV computes only where timing affects the planner, and geospatial calibration work shows that clean accuracy rankings can change under distribution shift."
            ),
            "confidence": "High",
            "confidence_note": "Driving, multi-camera, BEV, scenario, and calibration papers share an evidence-to-action evaluation contract.",
            "lab_action": (
                "Define occlusion, bandwidth, camera-drop, distribution-shift, and braking-distance stress splits, then compare whether explanations, scenario features, cooperative perception, cross-view selection, and timely BEV computation change near-miss rate and required intervention."
            ),
            "limit": 6,
        },
        {
            "title": "World models become risk and benchmark reasoners instead of plausible video generators",
            "buckets": ["Generation", "3D/Scene"],
            "ids": ["2608.14952", "2608.16651", "2608.16859", "2608.16234", "2608.15452"],
            "needles": ["world model", "risk", "latent", "benchmark", "gaussian driving", "structured"],
            "why": (
                "Evidence of Absence sustains world state when vision fails, Orbit-Planner rolls out latent physical risk for satellites, HarnessEval-W demands a reasoning chain for visual-world scores, "
                "GaussianDWM++ adds language-grounded 3D scene understanding to driving generation, and structured flow matching treats generation sources as controllable spatial evidence. The question is no longer whether the future looks plausible, but whether it carries the risk variable a robot or evaluator needs."
            ),
            "confidence": "Medium-High",
            "confidence_note": "Five Generation/3D papers connect world modeling to risk, physical state, benchmark reasoning, or language-grounded 3D control.",
            "lab_action": (
                "Create tasks where vision is occluded, physical state is latent, or scene edits change collision risk, then compare world-model rollouts by hidden-risk detection, action-conditioned state recovery, benchmark explanation correctness, and downstream planner choice."
            ),
            "limit": 5,
        },
        {
            "title": "Efficiency work shifts from cheaper inference to preserving sparse control evidence",
            "buckets": ["Efficiency/Systems", "Foundation Models", "Robot Learning", "Autonomous Driving"],
            "ids": ["2608.16320", "2608.15075", "2608.16523", "2608.15962", "2608.15636", "2608.15437"],
            "needles": ["streaming", "token", "pruning", "event camera", "compression", "efficient", "timeliness"],
            "why": (
                "StreamOPD, SA-GEM, FLEET, SEER, efficient VLA speculative verification, and MM-BEV all resist a simple latency-only story. "
                "Each method decides which recent video cue, geospatial token, event feature, text region, action chunk, or BEV object deserves compute because it may change an answer or control decision."
            ),
            "confidence": "Medium-High",
            "confidence_note": "The papers span video, remote sensing, event control, long-context reasoning, VLA inference, and BEV perception, with a common sparse-evidence budget.",
            "lab_action": (
                "Sweep compute, token, memory, and latency budgets while holding task difficulty fixed, then measure retained event timing, geospatial evidence, streaming answer correctness, action-chunk validity, and planner-relevant BEV errors rather than reporting speed alone."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Runtime-authority VLA audit",
            "claim": (
                "Compare counterfactual recovery, tactile residual adaptation, process rewards, stop-aware chunking, structured exploration, and world-model-guided test-time search on identical perturbation episodes; score which interface changes the next action before terminal success changes."
            ),
        },
        {
            "title": "Task-driven map update protocol",
            "claim": (
                "Evaluate Gaussian and LiDAR maps under relighting, motion blur, dynamic objects, sensor-configuration shift, and task-object occlusion; require every map update policy to report localization, manipulation recovery, update cost, and false stable memory."
            ),
        },
        {
            "title": "Physical-evidence provenance benchmark",
            "claim": (
                "Build a flood, driving, or urban navigation benchmark where each score is tied to the decisive view, modality, scenario variable, trust boundary, and edge budget that changed the physical action."
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
        "meaning": "Included because it supports today's runtime-evidence-control thesis.",
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
