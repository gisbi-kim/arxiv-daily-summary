#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-08-24 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260824 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-24"


PROFILE = {
    "date": DATE,
    "weekday": "Mon",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching 2026-08-24 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-08-24 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "The 2026-08-24 batch is about action authorization rather than raw model capability. "
        "VLA papers ask whether certificates, temporal logic, future tokens, belief routing, and compression tolerance can decide when an action is safe to issue. "
        "Manipulation papers move evidence into tactile histories, physical properties, task-precedence graphs, and gripper/data co-design, while geometry and driving papers make map updates, state estimation, cooperative perception, and future rollout budgets auditable. "
        "The shared research move is to expose the hidden evidence variable before trusting a policy, planner, map, or VLM answer."
    ),
    "cluster_takeaway": (
        "Today's core is not another VLA, 3D, or world-model variant; it is deciding which certificate, contact state, map cue, evidence route, or rollout-risk signal is allowed to authorize action."
    ),
    "trend_note": (
        "Monday /new produced 133 deduplicated non-replacement papers and 110 ROI papers. "
        "Robot Learning, Foundation Models, Efficiency/Systems, and Safety/Alignment are all large enough to matter, but the strongest APRL signal is the repeated demand that actions, spatial answers, compressed tokens, and imagined futures carry an auditable evidence path."
    ),
    "cluster_specs": [
        {
            "title": "VLA control moves from plausible actions to certified and logic-conditioned authority",
            "buckets": ["Robot Learning", "Autonomous Driving", "Efficiency/Systems", "Foundation Models"],
            "ids": ["2608.20791", "2608.20556", "2608.20735", "2608.21247", "2608.20763", "2608.20890"],
            "needles": ["vla", "vision-language-action", "certified", "temporal logic", "future-token", "token compression", "belief", "routing"],
            "why": (
                "A VLA action is no longer treated as valid just because the model can produce it. "
                "CertVLA asks for rollout-level certificates against physical patches, Logic-VLA makes temporal logic an inference-time requirement, ForeTime-VLA distills future contact tokens without running the teacher online, JND compression defines token removal by downstream action deviation, CARD diagnoses whether belief states actually route into action, and collaborative driving VLA exposes multimodal interaction before planning. "
                "APRL should evaluate which explicit authorizer changed the action and which hidden condition invalidates it."
            ),
            "confidence": "High",
            "confidence_note": "Six papers independently expose action certificates, formal predicates, future tokens, action-compression tolerance, belief routing, and multimodal driving decisions.",
            "lab_action": (
                "Run closed-loop VLA tasks with physical patch masks, unseen STL predicates, moving-object phase shifts, belief-state partner changes, sensor disagreement, and token-compression levels; compare action delta, requirement violation, rollout certificate coverage, recovery timing, and terminal success."
            ),
            "limit": 6,
        },
        {
            "title": "Manipulation learning shifts from more demonstrations to contact-state and hardware evidence",
            "buckets": ["Robot Learning"],
            "ids": ["2608.21290", "2608.20546", "2608.21355", "2608.20962", "2608.21035", "2608.20784"],
            "needles": ["tactile", "gripper", "physical property", "friction", "stiffness", "precedence", "demonstration", "unlearning", "contact"],
            "why": (
                "The manipulation papers make dataset scale less separable from the sensing and hardware interface that produced the data. "
                "VT-MUSE treats tactile evolution as a sequential representation variable, Koala Gripper co-designs collection and execution hardware, ViTacPhys estimates mass, friction, and stiffness from human visual-tactile demonstrations, roller-jamming adds retention under pose uncertainty, TaPeR recovers sparse precedence graphs from few demos, and demonstration unlearning audits what behavior remains after deletion. "
                "The common decision is to measure whether contact, physics, task dependency, or data provenance survives into closed-loop behavior."
            ),
            "confidence": "High",
            "confidence_note": "Six Robot Learning papers share tactile, physical-property, hardware, task-graph, uncertainty, or demonstration-provenance evidence variables.",
            "lab_action": (
                "Build one contact-rich benchmark with visuotactile histories, mass/friction/stiffness labels, gripper pose uncertainty, partial task-order demonstrations, and removed-demonstration probes; compare contact prediction, grasp recovery, valid subtask reordering, action divergence to retrain, and final success."
            ),
            "limit": 6,
        },
        {
            "title": "Geometry validity moves from surface quality to observable state for robots",
            "buckets": ["3D/Scene", "Safety/Alignment"],
            "ids": ["2608.20687", "2608.20740", "2608.20788", "2608.21136", "2608.20891", "2608.21276"],
            "needles": ["surface reconstruction", "thin object", "monocular depth", "multi-view stereo", "streaming 3d", "state estimation", "localization", "coastline", "scene geometry"],
            "why": (
                "3D quality is being reframed as whether the representation exposes the state a robot can use. "
                "TopoSurfel links Gaussian surfels to meshes to reduce ambiguous floaters, VisTa3D shows thin-object failures and adds tactile geometry, M2Depth couples monocular priors with MVS instead of one-way fusion, Stream3Dv2 fuses geometric and semantic evidence over streaming RGB-D, IMU-free quadcopter estimation uses stationary scene points as implicit references, and coastline localization turns shoreline geometry into a GPS-denied constraint. "
                "APRL should judge geometry by observability, localizability, contact utility, and downstream control recovery."
            ),
            "confidence": "High",
            "confidence_note": "The geometry gate is triggered by 10 3D/Scene ROI papers plus reconstruction, depth, streaming 3D, state-estimation, and localization signals.",
            "lab_action": (
                "Evaluate Gaussian surface recon, thin-object tactile recon, DFM+MVS depth, streaming 3D segmentation, IMU-free stereo flow, and coastline localization on textureless, thin, occluded, streaming, GPS-denied, and dynamic scenes; score map floaters, depth scale error, localizability, contact-valid geometry, and route recovery."
            ),
            "limit": 6,
        },
        {
            "title": "VLM reasoning is audited by spatial state and structured evidence routes",
            "buckets": ["Foundation Models", "Efficiency/Systems"],
            "ids": ["2608.20414", "2608.20886", "2608.21140", "2608.21170", "2608.21244", "2608.20805"],
            "needles": ["spatial-state", "evidence", "auditable", "spatial relation", "visual scaffold", "anomaly score", "routing before looking", "video understanding"],
            "why": (
                "Final VLM answers are increasingly treated as unsafe unless the intermediate evidence path is inspectable. "
                "StateSight isolates latent spatial reconstruction, EviRank converts multimodal image re-ranking into typed evidence constraints, the CT agent decomposes spatial verification into parsing, localization, and geometry checks, visual scaffolds reveal grounding-related failures, VLM anomaly detection shows that answer readout is part of the detector, and Route2Look routes long-video queries through evidence acquisition tools. "
                "For robot agents, the question is not whether the answer sounds right, but whether the needed state was reconstructed and checked."
            ),
            "confidence": "High",
            "confidence_note": "Six VLM/video papers independently expose latent state, typed evidence packages, modular spatial verification, scaffolds, readout interfaces, or evidence-acquisition routes.",
            "lab_action": (
                "Create mobile-inspection and manipulation prompts with hidden spatial state, small labels, long-video evidence, anomaly intervals, and relation predicates; compare direct VLM answers, routed evidence acquisition, modular geometric verification, probability readouts, abstention, and downstream action errors."
            ),
            "limit": 6,
        },
        {
            "title": "Autonomy evaluation shifts to imagined, cooperative, and distributed stress conditions",
            "buckets": ["Autonomous Driving", "Robot Learning"],
            "ids": ["2608.20430", "2608.20974", "2608.20904", "2608.21032", "2608.21330", "2608.21055"],
            "needles": ["world action", "imagination", "driving", "simulation-based testing", "cooperative", "off-road", "soil", "collaborative perception", "misalignment"],
            "why": (
                "Autonomy papers are turning evaluation from one offline score into a family of explicit stress generators. "
                "RISE spends imagination only when rollout risk justifies cost, WA-JEPA changes video representation learning toward future-action prediction, distributed CARLA testing scales scenario execution, V2XBench and AURORA combine roadside sensing with VLM reasoning, NeSAM makes soil parameters part of kinodynamic prediction, and CoAnchor handles communication delay plus pose noise with object-level anchors. "
                "The shared decision is to publish the future, collaborator, terrain, or infrastructure condition under which the plan remains valid."
            ),
            "confidence": "High",
            "confidence_note": "Driving/autonomy papers repeat risk-conditioned rollout, action-coupled prediction, distributed scenario testing, V2X cooperation, terrain adaptation, and misalignment stress.",
            "lab_action": (
                "Run a distributed scenario suite with fixed versus adaptive WAM rollout, future-action JEPA, V2X occlusion, delayed collaborator messages, deformable soil, and pose noise; compare collision risk, rollout value, communication-induced action change, soil-parameter error, and closed-loop recovery."
            ),
            "limit": 6,
        },
        {
            "title": "Efficiency and generation are judged by preserved evidence, not smaller artifacts",
            "buckets": ["Efficiency/Systems", "Foundation Models", "Generation"],
            "ids": ["2608.20473", "2608.21134", "2608.21247", "2608.20770", "2608.20448", "2608.20936"],
            "needles": ["token compression", "quantization", "jnd", "physical consistency", "3d generation", "world models", "morphology", "evidence", "efficient"],
            "why": (
                "Compression and generation papers are becoming useful only when they state what evidence survives the cheaper representation. "
                "AVIOT transports video-token information under question and spatial constraints, Llama-Mobile quantizes VLMs for Arm deployment, JND-VLA ties compression to action deviation, MotionPhys rejects visually plausible videos with inconsistent trajectories, MultiCube gives part-level 3D semantic and spatial control, and GraphOp-WM factorizes morphology-independent dynamics from morphology-conditioned operators. "
                "The relevant metric is whether compressed or generated state still preserves the cue a planner or controller consumes."
            ),
            "confidence": "Medium",
            "confidence_note": "Six papers connect efficiency or generation to evidence preservation, but common embodied benchmarks are still weak.",
            "lab_action": (
                "Compare token transport, low-bit quantization, JND compression, generated-video physical consistency, part-level 3D control, and morphology-conditioned world models under matched planning tasks; measure latency, memory, action delta, physical-trajectory error, part constraint violation, and transfer to unseen morphology."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "VLA action-authority grid",
            "claim": (
                "Cross CertVLA-style patch masks, Logic-VLA temporal predicates, ForeTime future tokens, CARD belief routes, and JND compression levels in the same closed-loop tasks; measure which authorizer predicts action deviation before failure."
            ),
        },
        {
            "title": "Thin-contact robot geometry suite",
            "claim": (
                "Use thin objects, tactile maps, physical-property labels, and gripper pose uncertainty to test whether reconstruction quality changes grasp recovery, collision avoidance, or insertion success."
            ),
        },
        {
            "title": "Evidence-routing autonomy evaluator",
            "claim": (
                "Create scenes where adaptive imagination, V2X cooperation, long-video evidence routing, and soil-parameter updates should change deployment confidence only under named risk conditions."
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
        "meaning": "Included because it supports today's action-authorization and evidence-routing thesis.",
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
