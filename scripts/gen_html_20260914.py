#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-09-14 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260914 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-14"


PROFILE = {
    "date": DATE,
    "weekday": "Mon",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching 2026-09-14 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-09-14 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "The 2026-09-14 batch says robotics and embodied AI are shifting from model-size claims to evidence-interface claims. "
        "Robot policies ask which latent interface, perception stream, planner-generated trajectory, tactile token, material estimate, or world model is allowed to condition the next action. "
        "Geometry papers ask whether scans, chained loop closures, room-object graphs, and low-altitude LIO settings can govern relocalization and retrieval after the environment changes. "
        "Driving, aerial, and search-and-rescue papers expose risk through criticality, battery, weather, comfort, communication, and feasibility constraints instead of treating safety as a final score. "
        "World-model, video-memory, and visual-cache papers then challenge the easy proxies: self-consistency, pixel retention, and visually fluent generation are not enough unless intervention tests show decision-level use. "
        "APRL should therefore build benchmarks where evidence is admitted only after it survives the action, map, memory, or safety interface it is supposed to control."
    ),
    "cluster_takeaway": (
        "Today's core is not more robot data, larger world models, or prettier geometry; it is deciding which evidence interface is authorized to change action, map reuse, risk intervention, or memory retrieval."
    ),
    "trend_note": (
        "Monday /new produced 142 deduplicated non-replacement papers and 115 ROI papers. "
        "Robot Learning dominates the batch, but the more useful signal is cross-bucket: actions, maps, memories, and multimodal caches are being judged by causal or physical permission tests rather than static quality."
    ),
    "cluster_specs": [
        {
            "title": "Robot policies move from shared visual features to auditable action-conditioning interfaces",
            "buckets": ["Robot Learning", "Efficiency/Systems", "Generation"],
            "ids": ["2609.12641", "2609.12081", "2609.12316", "2609.13053", "2609.12075", "2609.12278"],
            "needles": [
                "vision-action shortcut", "latent interface", "subsystem-specific", "distribution-aligned",
                "vision-language-action", "serving", "world-action", "model-based reinforcement",
            ],
            "why": (
                "기존 robot foundation model 평가는 큰 visual backbone이나 더 많은 demonstration이 action quality를 자연스럽게 올린다고 읽기 쉬웠다. "
                "이번 묶음은 그 가정을 쪼개어, 어떤 시각 정보가 latent interface를 통해 action head로 들어가고, base와 arm이 어떤 다른 perceptual stream을 쓰며, planner-generated data가 pretraining distribution과 맞는지 묻는다. "
                "LIT, MoPA, DATAFARM, Dynin-Robotics, VLA serving, and model-based adaptation papers all treat the evidence path into action as the object to test. "
                "APRL은 terminal success만 보지 말고 camera shift, subsystem conflict, planner-style mismatch, serving latency, and world-model adaptation이 action choice를 어디서 바꾸는지 분리해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Six papers independently expose visual latent interfaces, subsystem perception alignment, distribution-aligned planner data, omnimodal VLA generation, VLA serving, and world-model adaptation.",
            "lab_action": (
                "LIBERO/RoboCasa와 mobile-manipulation tasks에서 camera/distractor shifts, base-arm conflict, raw-versus-aligned TAMP trajectories, VLA serving queue pressure, and world-model adaptation을 ablation하고 OOD success, action flip, latency violation, recovery rate, and coordination failure를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Contact-rich manipulation shifts from demonstration volume to material, tactile, and force state",
            "buckets": ["Robot Learning", "3D/Scene"],
            "ids": ["2609.12549", "2609.12103", "2609.12634", "2609.12498", "2609.12894", "2609.12737", "2609.12677"],
            "needles": [
                "tactile", "rod insertion", "material", "center of mass", "fragile",
                "articulated", "deformable", "soil", "force",
            ],
            "why": (
                "Contact-rich manipulation is not solved by adding generic demonstrations if the policy cannot represent the physical state that controls failure. "
                "STAR makes sparse tactile signals predictive, RodForesight selects insertion actions after a world model predicts rod-hole alignment, material-conditioned diffusion estimates stiffness online, and force-guided CoM estimation stays below the tipping point. "
                "ArtManip, safe fragile grasping, and soil manipulation add articulated degrees of freedom, force thresholds, and material state as variables that decide whether an action is safe. "
                "APRL should evaluate manipulation data by whether it names the contact, material, force, and geometry variables that change recovery, not only by final task completion."
            ),
            "confidence": "High",
            "confidence_note": "Seven manipulation papers share the same decision: expose hidden physical state before selecting or trusting an action.",
            "lab_action": (
                "Dexterous, rod-insertion, deformable-object, fragile-grasp, and soil tasks에서 tactile masking, material-label error, force threshold, CoM margin, articulated-joint state, and world-model precheck을 독립 변수로 두고 slip, bend error, toppling risk, damage proxy, and recovery success를 평가한다."
            ),
            "limit": 6,
        },
        {
            "title": "Robot geometry becomes governed map evidence rather than passive reconstruction",
            "buckets": ["3D/Scene", "Embodied AI", "Safety/Alignment"],
            "ids": ["2609.12557", "2609.12221", "2609.12614", "2609.12417", "2609.12837", "2609.12285", "2609.12723"],
            "needles": [
                "relocalizing", "slam", "room-object", "point cloud registration", "lidar-inertial",
                "geometry-anchored", "floorplan", "monocular video",
            ],
            "why": (
                "3D/SLAM output is useful to a robot only when it can decide whether a map, scan, or room-object relation should constrain the next action. "
                "DRS-VPT unifies image-to-scan registration, Chain-SLAM propagates multi-session loop closures, ProClosure assigns objects to rooms from monocular video, and low-overlap registration plus LIO sensitivity papers expose when geometry is fragile. "
                "AnchorVLN adds the cleanest interface rule: the VLM proposes semantics, but geometry decides metric quantities. "
                "APRL should treat map reuse as an evidence-governed decision with explicit wrong-room, wrong-pose, and wrong-loop-closure failure modes."
            ),
            "confidence": "High",
            "confidence_note": "Seven papers connect relocalization, multi-session SLAM, room-object assignment, point-cloud registration, aerial LIO, geometry-anchored VLN, and floorplan encoding.",
            "lab_action": (
                "Indoor scan, corridor, aerial low-altitude, and room-object retrieval suites에서 scan overlap, loop-closure confidence, room boundary closure, LIO parameters, geometry-anchor availability, and floorplan modality를 바꿔 relocalization error, wrong-room retrieval, loop-closure damage, navigation recovery, and query success를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Autonomy safety moves from final pass rates to explicit risk envelopes and intervention bounds",
            "buckets": ["Autonomous Driving", "Robot Learning", "Safety/Alignment", "Efficiency/Systems"],
            "ids": ["2609.11947", "2609.12371", "2609.12095", "2609.12188", "2609.13011", "2609.12660", "2609.13083", "2609.12831"],
            "needles": [
                "criticality", "risk-informed", "weather hazards", "battery-aware", "comfort-bounded",
                "autonomous racing", "control barrier", "language-guided",
            ],
            "why": (
                "Autonomous systems can pass average planning metrics while still failing at the moment a risk envelope should constrain action. "
                "VRU criticality, READ's learned risk fields, operator-conditioned weather hazards, battery-aware multirotor planning, comfort-bounded action spaces, racing-at-the-limit control, VertexCBF, and ASTRIL-MPC all make the intervention boundary explicit. "
                "The shared move is to represent what condition should change the controller before a crash, discomfort event, collision, or mission loss occurs. "
                "APRL should compare safety methods by whether their risk signal changes action early enough and remains inspectable under disturbance."
            ),
            "confidence": "High",
            "confidence_note": "Eight control papers expose object criticality, spatial risk fields, weather uncertainty, battery propagation, comfort bounds, racing dynamics, barrier constraints, and language-bounded MPC.",
            "lab_action": (
                "Driving, UAV, racing, and rescue-robot scenarios에서 VRU motion, weather hazard uncertainty, battery state, comfort bounds, CBF vertex search, and LLM-retuned MPC limits를 stress split으로 만들고 intervention lead time, constraint violation, mission survival, passenger comfort, and collision proxy를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "World models are being judged by causal physical use rather than fluent rollouts",
            "buckets": ["Generation", "Foundation Models", "Efficiency/Systems"],
            "ids": ["2609.12441", "2609.12090", "2609.12874", "2609.13006", "2609.12036", "2609.13146"],
            "needles": [
                "physically anchored", "memory specificity", "4d-aware", "physics-aware",
                "world model simulator", "physically grounded", "rollout", "tokenizer",
            ],
            "why": (
                "Generated futures and memories can look coherent while carrying the wrong physical object, wrong episodic content, or wrong causal token. "
                "IMPLY shows self-consistency can bless the wrong object unless rollouts are anchored to calibration pushes, and the video-memory audit shows memory gains can come from generic representation repair rather than retrieved content. "
                "VideoTok4D, PhysPlan, Pelican-Sim, and SNAP3D all push toward compact or generated worlds that must preserve 4D structure, physical dynamics, action controllability, or assembly validity. "
                "APRL should make generated futures earn control authority through substitution, anchoring, and action-change tests."
            ),
            "confidence": "High",
            "confidence_note": "Six papers connect causal memory substitution, physics-anchored rollout checks, 4D tokenization, physics-aware generation, embodied simulators, and physical assembly constraints.",
            "lab_action": (
                "Robot-view rollout and long-video memory tasks에서 same-object calibration, wrong-memory substitution, 4D token perturbation, physics-guided generation, simulator action injection, and assembly validity를 ablation하고 action-choice flip, rollout error, object-state persistence, and downstream policy success를 평가한다."
            ),
            "limit": 6,
        },
        {
            "title": "Efficient multimodal agents shift from retaining content to routing decisive evidence",
            "buckets": ["Efficiency/Systems", "Foundation Models"],
            "ids": ["2609.13012", "2609.12517", "2609.12818", "2609.12622", "2609.12798", "2609.12408", "2609.12168", "2609.12663"],
            "needles": [
                "kv-cache", "frame-selection", "video agent", "modality degradation",
                "reliability-aware", "visual state machines", "split learning", "grounding",
            ],
            "why": (
                "Efficiency is no longer just fewer frames, tokens, or sensor streams; it is choosing which evidence must survive for the current query or safety decision. "
                "Pixel-decoding fails as a cache-importance proxy in one careful causal test, AutoSkill routes frame-selection skills by question taxonomy, VideoXAgent invokes tools on demand, and RA-SOD/LGFN model modality reliability under degraded RGB, thermal, or polarization cues. "
                "GSO-Net and split-learning VQA then tie evidence routing to deployed compliance and distributed inference constraints. "
                "APRL should evaluate compression and routing by decisive-cue recall and action error, not by retained visual detail or average context size."
            ),
            "confidence": "High",
            "confidence_note": "Eight papers share budget-aware evidence selection across KV cache, long-video frames, online tools, modality degradation, compliance state machines, and split inference.",
            "lab_action": (
                "Long-video robot QA, RGB-T inspection, camouflaged-object detection, and edge VLA episodes에서 KV eviction proxy, frame-selection skill, online tool budget, modality reliability, and split-learning aggregation을 바꿔 decisive-cue recall, hallucination rate, latency, compliance miss, and action error를 비교한다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Evidence-interface audit for robot policies",
            "claim": (
                "Compare latent interfaces, subsystem perception streams, planner-aligned data, tactile tokens, and material estimates under the same OOD action shifts."
            ),
        },
        {
            "title": "Governed map reuse benchmark",
            "claim": (
                "Measure when a scan, loop closure, room-object graph, or LIO parameter choice should be trusted enough to constrain navigation or retrieval."
            ),
        },
        {
            "title": "Causal rollout and memory permission test",
            "claim": (
                "Use calibration pushes, memory substitutions, 4D token interventions, and generated-rollout action flips to decide when world evidence may guide control."
            ),
        },
        {
            "title": "Decisive-evidence routing under runtime budgets",
            "claim": (
                "Evaluate KV eviction, frame selection, online video tools, and modality fusion by whether they preserve cues that change safety or action decisions."
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
        "meaning": "Included because it supports today's evidence-interface and permission-test thesis.",
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
