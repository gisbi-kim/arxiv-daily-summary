#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-08-20 backfill."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260820 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-20"


PROFILE = {
    "date": DATE,
    "weekday": "Thu",
    "week_start": week_start(DATE),
    "source_mode": "pastweek-date-section",
    "source_label": "arXiv cs.CV/pastweek + cs.RO/pastweek date section",
    "source_note": "Backfilled from the matching 2026-08-20 arXiv /pastweek date sections",
    "benchmark_note": (
        "Daily artifact generated from the 2026-08-20 /pastweek date sections. "
        "The date-section source has title/subject rows but no abstracts, so paper cards and Research Intelligence are conservative triage notes."
    ),
    "thesis": (
        "The August 20 backfill is not a fresh abstract-level deep dive; it is a source-audited recovery of the missing Thursday batch. "
        "Its strongest signal is that geometry, manipulation data, and world-model latents are being judged by whether they change a robot policy, route, or benchmark state. "
        "APRL should treat the day as a benchmark-design map: define the hidden state, material state, viewpoint state, or future latent that can falsify a deployment claim before scaling data collection."
    ),
    "cluster_takeaway": (
        "Today's core is not another robotics paper list; it is naming which geometry, material, coordination, or latent state must become an evaluated variable before a robot claim is trusted."
    ),
    "trend_note": (
        "The backfill parser recovered 125 deduplicated non-replacement papers and 50 ROI papers. "
        "3D/Scene and Robot Learning dominate the useful signal, with smaller but connected threads in decision-aligned world models, VLM evidence calibration, and embodied coordination."
    ),
    "cluster_specs": [
        {
            "title": "Geometry becomes a policy-facing intervention instead of a reconstruction side product",
            "buckets": ["3D/Scene"],
            "ids": ["2608.19066", "2608.19004", "2608.18388", "2608.18632", "2608.18624", "2608.18864"],
            "needles": ["vla", "gaussian", "slam", "odometry", "lidar", "4d", "navigation", "tractor", "scene flow"],
            "why": (
                "The date-section titles connect geometry to frozen VLA viewpoint handling, field LiDAR navigation, dynamic 4D reconstruction, UAV SLAM, visual odometry, and LiDAR scene flow. "
                "That means the useful question is not whether the map looks plausible; it is whether viewpoint, metric scale, odometry, or dynamic-flow evidence changes a route, manipulation policy, or downstream failure."
            ),
            "confidence": "High",
            "confidence_note": "Six 3D/Scene papers independently tie geometry to VLA policy use, field navigation, SLAM/VO evaluation, 4D reconstruction, or LiDAR flow.",
            "lab_action": (
                "Compare frozen-VLA viewpoint canonicalization, monocular SLAM, visual-odometry matching, 4D Gaussian reconstruction, and LiDAR scene-flow cues on camera-shift, scale-drift, crop-row navigation, dynamic-object, and route-recovery splits; score action delta, localization failure, and downstream navigation success."
            ),
            "limit": 6,
        },
        {
            "title": "Manipulation benchmarks move from final success to material, tool, and hidden-geometry state",
            "buckets": ["Robot Learning"],
            "ids": ["2608.18701", "2608.18618", "2608.18948", "2608.19188", "2608.18787", "2608.18258"],
            "needles": ["deformable", "dexterous", "benchmark", "human", "partial", "geometry", "reward", "granular", "manipulation"],
            "why": (
                "SoftVTBench, LabDex, RoboEdit, PartialBiGrasp, Dream2Reward, and granular-food imitation titles all point to states that final task success hides: deformation, lab-subtask hierarchy, human-video edit quality, hidden local geometry, reward transition alignment, and granular material behavior. "
                "For APRL, these are benchmark labels before they are policy improvements."
            ),
            "confidence": "High",
            "confidence_note": "Six robotics papers expose benchmark, data, reward, and hidden-state variables for manipulation.",
            "lab_action": (
                "Build one manipulation audit set where deformability, lab-tool subtask boundary, partial-view local geometry, human-video-derived experience, transition-aligned reward, and granular material state are independent labels; compare policy ranking under final success and each hidden-state label."
            ),
            "limit": 6,
        },
        {
            "title": "World models are being evaluated by decision alignment and control transfer",
            "buckets": ["Generation"],
            "ids": ["2608.19085", "2608.18746", "2608.18234", "2608.18647", "2608.18710", "2608.18484"],
            "needles": ["decision", "world model", "control", "navigation", "future latent", "mpc", "camera-controlled", "sparse attention"],
            "why": (
                "DA-WAM, Decision-Metric Alignment, GigaBrain-WBC, Progressive Experience Fusion, CamWorldQA, and sparse-attention video/world-model work share a research decision: a latent future or generated world matters only if it changes planning, navigation, control, or quality assessment under the task variable that matters. "
                "This is a better robotics test than visual plausibility alone."
            ),
            "confidence": "High",
            "confidence_note": "World-model titles repeatedly mention decision alignment, control, navigation, future latents, and quality assessment.",
            "lab_action": (
                "Create paired scenarios where the visual future is similar but braking, route choice, catheter motion, whole-body recovery, or camera-control quality should change; compare decision-aligned latent objectives against reconstruction or video-quality objectives by action error and recovery outcome."
            ),
            "limit": 6,
        },
        {
            "title": "VLM reliability shifts from answer confidence to calibrated evidence authority",
            "buckets": ["Foundation Models", "Safety/Alignment"],
            "ids": ["2608.19075", "2608.18628", "2608.18586", "2608.18984", "2608.18573", "2608.18399"],
            "needles": ["evidence", "calibrating", "hallucinations", "safety", "vision", "diagnostic", "uncertainty", "attention", "robustness"],
            "why": (
                "ReWEIGH, safety-overrides-vision, OmniHandwritingOCR, uncertainty-aware dating, PATE-Forensics, and attention-transfer robustness papers all make answer reliability depend on a specific evidence path, calibration state, or robustness structure. "
                "For robot VLMs, confidence is not enough; the visual cue or safety prior that authorized the answer must be visible."
            ),
            "confidence": "Medium-High",
            "confidence_note": "The signal spans evidence calibration, safety-vision conflict, diagnostic OCR, uncertainty, forensics, and attention robustness.",
            "lab_action": (
                "Evaluate robot VLM prompts under weak visual evidence, safety-prior conflict, handwriting or gauge ambiguity, domain-shifted visuals, and attention-transfer perturbations; score source-reliance shift, calibrated evidence strength, hallucinated action, and downstream task error."
            ),
            "limit": 6,
        },
        {
            "title": "Embodied autonomy turns coordination, navigation, and human-risk constraints into evaluated state",
            "buckets": ["Embodied AI", "Autonomous Driving", "3D/Scene"],
            "ids": ["2608.18292", "2608.18470", "2608.18840", "2608.18778", "2608.18140"],
            "needles": ["navigation", "retrieval", "collision", "code scenes", "psychological safety", "firefighting", "tractor", "assistive"],
            "why": (
                "GuideFetch, DevGRU, usage-driven code scenes, autonomous-vehicle psychological safety, and degradation-triggered firefighting routing all put the autonomy claim in a richer system context. "
                "The robot must coordinate retrieval with navigation, avoid collision, respect human risk, or handle event-triggered missions."
            ),
            "confidence": "Medium",
            "confidence_note": "The cluster is cross-bucket and title/subject based, but the evaluated-state theme is consistent across assistive, navigation, AV, and UAV settings.",
            "lab_action": (
                "Design navigation episodes where object retrieval, collision risk, user priority, degradation-triggered dispatch, and psychological-safety constraints can fail independently; compare route success, recovery behavior, constraint violation, and user-facing risk."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Policy-facing geometry audit",
            "claim": (
                "Run camera-shift, scale-drift, dynamic-object, and crop-row route tests where Gaussian canonicalization, SLAM/VO, and LiDAR cues can each change the robot's next action."
            ),
        },
        {
            "title": "Hidden-state manipulation labels",
            "claim": (
                "Annotate deformability, lab-subtask hierarchy, partial local geometry, human-video edit source, reward-transition alignment, and granular state before collecting more demonstrations."
            ),
        },
        {
            "title": "Decision-aligned world-model probe",
            "claim": (
                "Hold video plausibility roughly fixed while editing the scene variable that should change braking, route choice, catheter motion, or whole-body recovery; score latent usefulness by action change."
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


def source_card(paper: dict, ri_lookup: dict) -> dict:
    subjects = " ".join(str(paper.get("subjects", "")).split())
    return {
        "arxiv_id": paper.get("arxiv_id"),
        "title": paper.get("title"),
        "bucket": paper.get("bucket"),
        "reading_depth": ri_lookup.get(paper.get("arxiv_id"), "title/subject-only"),
        "problem": f"Backfill triage from title and subjects: {subjects}"[:360],
        "method": "No abstract/full-text evidence in the /pastweek date-section source; see Research Intelligence for conservative source notes.",
        "meaning": "Included because it supports the August 20 benchmark-design and evaluated-state thesis.",
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
    insights["paper_autopsies"] = [source_card(by_id[pid], ri_lookup) for pid in ri_ids if pid in by_id]
    insights["frontier_memory"] = ri["frontier_memory"]
    insights["strategy_board"] = ri["strategy"]
    insights["tiering_note"] = (
        "Backfill Research Intelligence is title/subject-only because arXiv /pastweek date sections do not include abstracts. "
        "No full-text, figure, table, code, or dataset claims are asserted."
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
        f"<section class=\"ri-callout\"><span><strong>Research Intelligence backfill</strong> "
        f"Tier A {len(ri['papers'])} papers are title/subject-only triage cards with source limits, "
        f"adversarial reads, frontier memory, and APRL strategy board.</span>"
        f"<a href=\"{DATE}-research-intelligence.html\">Open Research Intelligence</a></section>"
    )
    doc = re.sub(r"</section>\n(<h2>.*?</h2>)", f"</section>\n{ri_callout}\n\\1", doc, count=1, flags=re.S)
    post_path.write_text(doc, encoding="utf-8", newline="\n")


def main() -> int:
    build(PROFILE, "out/cv_20260820.json", "out/ro_20260820.json")
    build_research_intelligence()
    enrich_insights()
    add_ri_callout()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
