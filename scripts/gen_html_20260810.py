#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-08-10 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260810 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-10"


PROFILE = {
    "date": DATE,
    "weekday": "Mon",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching 2026-08-10 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-08-10 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records official arXiv abstract/HTML checks for Tier A."
    ),
    "thesis": (
        "The August 10 batch turns robotics evaluation toward state accountability: a VLA must remember what left view, "
        "a world model must expose physical state rather than only predict the next embedding, a controller must know when "
        "to yield authority, and a map must prove what action it enables. AtlasVLA, PSG-JEPA, AutoIntervene, WNM-3D, "
        "TEMPO, planning-token pruning, VPR distractors, and accessibility fields all point to the same audit: evidence is "
        "valuable only when it changes the robot decision under occlusion, viewpoint shift, physical drift, or deployment constraints."
    ),
    "cluster_takeaway": (
        "Today's useful signal is the migration from representation quality to decision accountability: memory, geometry, "
        "world models, compression, and safety are judged by the action or intervention they change."
    ),
    "trend_note": (
        "The Monday /new listing has 132 deduplicated papers and 112 ROI papers. Generation and Efficiency/Systems are large, "
        "but the robotics signal concentrates in persistent VLA state, physical-state world models, 3D-conditioned navigation, "
        "calibrated intervention, contact-preserving transfer, and shortcut-resistant localization."
    ),
    "cluster_specs": [
        {
            "title": "Persistent state turns VLA control into an audit trail",
            "buckets": ["Robot Learning", "Foundation Models", "Autonomous Driving"],
            "ids": ["2608.06729", "2608.07314", "2608.06965", "2608.07361", "2608.06434", "2608.06688", "2608.06994"],
            "needles": ["vla", "persistent", "world-ego", "semantic-action", "planning token", "cross-view", "trace residual", "action"],
            "why": (
                "AtlasVLA adds persistent world-ego memory, TEMPO separates semantic and action adaptation, cross-view action consistency asks whether a VLA can survive camera motion, "
                "planning-token pruning exposes when a driving VLA's intent becomes controller-usable, and CrossTracer/adaptive VLA work asks when reasoning or model selection should change control. "
                "The common research decision is to log the state variable that changes the action, not only the language or visual embedding that looks plausible."
            ),
            "confidence": "High",
            "confidence_note": "Multiple CV/RO and RO papers directly target VLA memory, adaptation, viewpoint robustness, planning-token readiness, and inference selection.",
            "lab_action": "Replay one manipulation and one driving/navigation task with object-exit, camera-shift, and phase-interruption splits while logging memory state, semantic drift, planning-token layer, and action delta.",
            "limit": 7,
        },
        {
            "title": "World models are judged by physical state, not future pixels",
            "buckets": ["Robot Learning", "Generation", "Autonomous Driving"],
            "ids": ["2608.06799", "2608.07468", "2608.06544", "2608.07408", "2608.07409", "2608.06770", "2608.07463"],
            "needles": ["world model", "physical state", "jepa", "world action", "latent", "task-relevant", "memory", "simwam"],
            "why": (
                "PSG-JEPA asks whether predictive latents identify robot state, SimWAM uses video dynamics only as a training signal for low-latency driving actions, TaskSense discards visual clutter before encoding, "
                "Addressable Memory and UniJEPA test long-horizon visual persistence, and surgical/reflective world-model papers stress control-conditioned generation. "
                "The batch is shifting from asking whether rollouts look right to whether the latent exposes the physical variable a planner needs."
            ),
            "confidence": "High",
            "confidence_note": "The cluster links physical grounding, WAM training, task-centric attention, long-horizon memory, and deployment latency.",
            "lab_action": "Add frozen-latent state probes, task-region masks, rollout-memory stress, and downstream action success to the same world-model evaluation table.",
            "limit": 7,
        },
        {
            "title": "Geometry becomes action budget rather than map decoration",
            "buckets": ["3D/Scene", "Robot Learning", "Embodied AI"],
            "ids": ["2608.07267", "2608.02304", "2608.07074", "2608.06412", "2608.06919", "2608.07012", "2608.07144"],
            "needles": ["3d", "scene", "navigation", "mapping", "accessibility", "lidar", "trajectory", "reconstruction", "gaussian"],
            "why": (
                "WNM-3D turns monocular history into a 3D scene prefix for future view/action generation, TRACE plans trajectories from map uncertainty and visibility, M2-SMap compresses semantic maps, "
                "Accessibility Fields label which surfaces a tool can physically reach, and LiDAR/Gaussian reconstruction papers expose representation handoffs. "
                "The actionable question is no longer map fidelity alone; it is whether geometry changes navigation, sensing, or contact choices under resource limits."
            ),
            "confidence": "High",
            "confidence_note": "3D/Scene has 11 ROI papers plus several RO map/navigation papers with direct robot-use claims.",
            "lab_action": "Evaluate map outputs by next-view information gain, reachable-contact labels, memory footprint, and closed-loop navigation/contact success rather than standalone reconstruction metrics.",
            "limit": 7,
        },
        {
            "title": "Intervention and safety become online control contracts",
            "buckets": ["Robot Learning", "Safety/Alignment", "Embodied AI", "Autonomous Driving"],
            "ids": ["2608.07065", "2608.06481", "2608.07328", "2608.06830", "2608.06885", "2608.06847", "2608.06648"],
            "needles": ["intervention", "safe", "robust", "fault", "attack", "spoofing", "distractor", "lyapunov", "coordination"],
            "why": (
                "AutoIntervene converts visual-action support into authority transfer, LyEvO and fault-tolerant locomotion handle robust policy execution, multi-robot communication attacks and GNSS spoofing expose adversarial coordination risk, "
                "and distractor-augmented VPR shows that a standard metric can reward condition matching instead of place identity. "
                "Safety is becoming a contract for when the system should switch, suppress, recover, or distrust a shortcut variable."
            ),
            "confidence": "Medium-High",
            "confidence_note": "The cluster spans deployment intervention, sim-to-real robustness, locomotion faults, multi-robot attacks, spoofing, and VPR shortcut evaluation.",
            "lab_action": "Build one replay set with action-support thresholds, condition distractors, communication attack, spoofing signal, and fault labels, then measure recovery quality and intervention timing.",
            "limit": 7,
        },
        {
            "title": "Contact-preserving transfer is the bottleneck for human data",
            "buckets": ["Robot Learning", "Autonomous Driving", "Efficiency/Systems"],
            "ids": ["2608.07045", "2608.06827", "2608.07002", "2608.07075", "2608.07140", "2608.07005", "2608.06488"],
            "needles": ["contact", "retargeting", "real-to-sim", "haptic", "tactile", "payload", "manipulation", "exoskeleton"],
            "why": (
                "C2Dex makes stable object-side contacts the shared representation for video-to-dexterous transfer, R2S-EGO refines sparse real capture into simulation, tactile/contact sensing papers expose transient external contacts, "
                "and payload/exoskeleton/force-actuation work asks whether embodiment details preserve the intended interaction. "
                "The batch says scalable human or sparse data only matters when local geometry, contact timing, and robot embodiment remain executable."
            ),
            "confidence": "Medium-High",
            "confidence_note": "Several RO papers connect transfer, contact sensing, haptics, real-to-sim refinement, and payload-constrained planning.",
            "lab_action": "Score human-video retargeting by stable object-side contact, transient contact detection, embodiment residual, and real-robot task success instead of visual trajectory similarity.",
            "limit": 7,
        },
        {
            "title": "Compression is acceptable only after preserving decision signals",
            "buckets": ["Efficiency/Systems", "Foundation Models", "Generation"],
            "ids": ["2608.07088", "2608.06411", "2608.07193", "2608.06942", "2608.06959", "2608.06794", "2608.06612"],
            "needles": ["token pruning", "compression", "onboard", "cache", "efficient", "distillation", "sampling termination", "bandwidth"],
            "why": (
                "RoRA, middle-layer attention prediction, AI4AI pruning, onboard satellite compression, onboard VLM summarization, diffusion sampling termination, and scalable location encoding all cut runtime or bandwidth budgets. "
                "The release-relevant distinction is whether pruning preserves the token, frame, or spatial cue that actually changes retrieval, planning, anomaly detection, or downlink decisions. "
                "Efficiency is a robotics asset only when the discarded evidence is shown not to affect the downstream decision."
            ),
            "confidence": "Medium",
            "confidence_note": "The cluster is mostly CV systems work, but many papers map cleanly to onboard perception and decision-budget constraints.",
            "lab_action": "Run equal-latency ablations that remove visual tokens, cache entries, frames, and downlink packets, then report the first robot or monitoring decision that changes.",
            "limit": 7,
        },
    ],
    "research_topics": [
        {
            "title": "Persistent-state VLA recoverability grid",
            "claim": "Measure memory state, planning-token readiness, semantic drift, and action-support score under occlusion, camera shift, phase interruption, and operator recovery.",
        },
        {
            "title": "Physical-state world-model probe",
            "claim": "Add frozen-latent proprioceptive probes, state-change probes, task-region masks, and downstream planning success to one WAM or JEPA pipeline.",
        },
        {
            "title": "Robot-usable geometry benchmark",
            "claim": "Evaluate VPR, semantic mapping, active reconstruction, and accessibility fields by condition distractors, reachable contact, next-view utility, and closed-loop success.",
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
        "meaning": "Included because it supports the day's state-accountability and action-facing evaluation thesis.",
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
        "Research Intelligence uses official arXiv abstract pages and available official HTML for selected Tier A papers. "
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
        f"Tier A {len(ri['papers'])} papers are checked against official arXiv pages, with evidence traces, "
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
