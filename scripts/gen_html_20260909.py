#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-09-09 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260909 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-09"


PROFILE = {
    "date": DATE,
    "weekday": "Wed",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching 2026-09-09 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-09-09 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "The 2026-09-09 batch says a robot should not act just because a model produced a plausible next step; it should act only when the evidence that authorizes that step is still fresh, localized, and controller-relevant. "
        "VLA papers split reliability into force interruption, failure-boundary discovery, stage-aware recovery, process memory, native-video history, and reasoning-to-control consistency. "
        "Geometry papers turn 3DGS SLAM, spherical image-LiDAR, in-hand reconstruction, inertial odometry, occupancy completion, and BEV maps into planner-facing validity gates. "
        "World-model and navigation papers ask whether imagined physics, learned occupancy, target belief, and stale maps preserve the variables that make a future action safe. "
        "Safety and systems papers complete the same contract by testing whether token pruning, KV cache eviction, visual CoT, authority cues, cross-model pipelines, and observation-level attacks remove the evidence a deployed VLM or robot judge was supposed to use."
    ),
    "cluster_takeaway": (
        "Today's core is evidence permission: every memory, map, generated future, compressed token, and safety verdict has to name the action decision it is allowed to change."
    ),
    "trend_note": (
        "Wednesday /new produced 485 deduplicated non-replacement papers and 401 ROI papers, with Robot Learning and Foundation Models both above 70 ROI papers. "
        "The APRL signal is not volume; it is the convergence of VLA recovery, robot-usable geometry, closed-loop driving tests, and auditable efficient perception around explicit evidence gates."
    ),
    "cluster_specs": [
        {
            "title": "VLA reliability is shifting from success imitation to boundary and recovery control",
            "buckets": ["Robot Learning", "Foundation Models", "Embodied AI"],
            "ids": ["2609.05832", "2609.06114", "2609.06508", "2609.07047", "2609.05533", "2609.06251", "2609.06256"],
            "needles": [
                "vision-language-action", "failure-boundary", "closed-loop recovery", "force/torque",
                "process level memory", "native-video memory", "mobile robot control", "geometry move",
            ],
            "why": (
                "기존 VLA 평가는 expert demonstration을 더 잘 맞추면 robustness도 따라온다고 읽기 쉬웠지만, 이번 묶음은 성공 주변의 경계 변수를 직접 묻는다. "
                "CR-VLA-Force는 force evidence가 action chunk를 언제 끊어야 하는지 보며, Failure-Boundary Learning과 VLA-Corrector는 recoverable deviation과 semantic stage를 분리한다. "
                "MEMOBench와 SimpleMemVLA는 기억을 final success가 아니라 storage, update, compression, native-video retention 문제로 바꾸고, MobileVLA-R1 2.0은 reasoning과 executable control 사이의 접합부를 드러낸다. "
                "APRL VLA 평가는 final success와 별도로 failure boundary, recovery action, memory freshness, and force-interruption timing을 같은 episode 안에서 측정해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Seven papers independently target force timing, failure boundaries, stage recovery, process memory, native history, mobile reasoning, and geometry-to-local-VLA handoff.",
            "lab_action": (
                "LIBERO/RoboCasa와 실제 tabletop task에서 force spike, object displacement, stale-history cue, recoverable failed grasp, semantic stage error, and long-horizon mobile instruction을 stress split으로 만들고 boundary AUC, recovery action accuracy, memory operation accuracy, force-interruption latency, final success를 함께 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Geometry becomes useful only after it survives planner-facing validity checks",
            "buckets": ["3D/Scene", "Embodied AI", "Autonomous Driving", "Efficiency/Systems"],
            "ids": ["2609.07274", "2609.09012", "2609.08493", "2609.09069", "2609.06450", "2609.05783", "2609.08345"],
            "needles": [
                "3d gaussian slam", "spherical observations", "in-hand reconstruction", "learned occupancy",
                "inertial odometry", "bird's-eye-view", "multi-view 3d reasoning", "loop closure",
            ],
            "why": (
                "3D representation은 reconstruction score만 높아서는 robot asset이 되지 않는다. "
                "LightSplat은 3DGS SLAM을 loop closure와 online map consistency로 묶고, Spheriverse는 spherical image-LiDAR를 semantic occupancy and mapping benchmark로 만든다. "
                "AURORA는 under-observed surface를 줄이기 위해 in-hand reorientation을 닫힌 루프로 만들고, observation-gated occupancy는 learned completion이 planner를 잘못 움직일 수 있음을 보인다. "
                "Closed-loop BEV evaluation과 CoVeR는 각각 map error와 token coverage를 downstream control and 3D reasoning으로 검증하므로, APRL geometry 평가는 pose/rendering loss보다 relocalization, collision, endpoint feasibility, semantic-goal failure를 우선해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Seven geometry and planner-interface papers connect maps, occupancy, reconstruction, odometry, BEV, and token coverage to downstream action.",
            "lab_action": (
                "Lab corridor, cluttered tabletop, and CARLA-like driving scenes에서 3DGS loop closure, spherical occupancy, in-hand view selection, inertial preintegration, learned occupancy gate, BEV prediction, multi-view token coverage를 바꿔 relocalization success, collision query precision, endpoint feasibility, closed-loop control failure, semantic-goal error를 측정한다."
            ),
            "limit": 6,
        },
        {
            "title": "World models are being forced to expose which physical variable they commit to",
            "buckets": ["Generation", "Robot Learning", "Embodied AI", "Autonomous Driving"],
            "ids": ["2609.06207", "2609.06302", "2609.06009", "2609.06578", "2609.07126", "2609.09155", "2609.08230"],
            "needles": [
                "world model", "physical", "action-conditioned", "future utilization", "sensing degradation",
                "visual calibration", "action editing", "intervention-aware",
            ],
            "why": (
                "World model이라는 이름만으로는 planning, stress generation, recovery, and safety gating 중 무엇을 바꾸는지 알 수 없다. "
                "PhysWeep은 video generator가 요청한 physical parameter를 실제로 구현했는지 묻고, CST-WM은 embodied visual tracking에서 action-conditioned prediction이 causal hallucination을 만들 수 있음을 드러낸다. "
                "Intervention-aware world models, progress-conditioned future utilization, stage-wise reliability, SyncWorld, and ActionSplice 계열은 모두 미래 예측을 controller가 믿어도 되는 변수로 환원하려 한다. "
                "APRL은 generated future가 planner ranking, safety veto, contact correction, or observation recovery 중 어떤 권한을 갖는지 역할별 release gate를 세워야 한다."
            ),
            "confidence": "Medium-High",
            "confidence_note": "The papers share a world-model contract, though they span video generation, tracking, manipulation, mapping, and driving.",
            "lab_action": (
                "Manipulation, UAV tracking, and toy driving suites에서 generated future를 planner prior, physics verifier, intervention predictor, sensing-degradation monitor, and interactive edit oracle로 분리하고 realized physical parameter error, recovery improvement, unsafe action veto, trajectory drift, generated-stress transfer를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Driving and field robotics are moving safety tests into closed-loop scenario construction",
            "buckets": ["Autonomous Driving", "Foundation Models", "Safety/Alignment", "Embodied AI"],
            "ids": ["2609.05783", "2609.08965", "2609.07511", "2609.09073", "2609.05521", "2609.06368", "2609.08130"],
            "needles": [
                "closed-loop", "scenario-based testing", "beyond-view vectorized map", "reachability-aware",
                "connected vehicles", "cooperative driving", "driver alerting", "motion planner",
            ],
            "why": (
                "Driving perception과 planner 평가는 offline metric으로는 rare failure와 downstream risk를 놓치기 쉽다. "
                "Closed-loop BEV evaluation은 predicted map error가 behavior-cloning policy에 어떤 영향을 주는지 직접 보며, PlannerForge는 scenario generation부터 ADS assessment와 benchmarking까지 LLM-agent pipeline으로 묶는다. "
                "Beyond-view vectorized maps, reachability-aware MPC, connected-vehicle data distribution, cooperative-driving warnings, and adaptive driver alerting은 모두 safety evidence를 scenario, communication, and control loop 안에서 검증하려 한다. "
                "APRL field robotics에서는 perception score와 planning guarantee를 분리하지 말고 scenario construction, reachable set, communication relevance, and intervention timing을 같은 실험 로그에 넣어야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Seven papers connect driving maps, scenario agents, reachability, V2X relevance, cooperative warnings, and alert timing to closed-loop safety.",
            "lab_action": (
                "CARLA/nuPlan-style driving과 indoor field-robot navigation에서 predicted BEV, beyond-view map prior, reachability bound, V2X data relevance, cooperative warning latency, and driver/robot alert timing을 ablation하고 collision rate, planner violation, near-miss severity, intervention lead time, scenario coverage를 평가한다."
            ),
            "limit": 6,
        },
        {
            "title": "Compressed multimodal evidence now has to pass adversarial and localization audits",
            "buckets": ["Foundation Models", "Safety/Alignment", "Efficiency/Systems"],
            "ids": ["2609.08331", "2609.07499", "2609.05535", "2609.06058", "2609.06419", "2609.06704", "2609.08345", "2609.06663", "2609.05916"],
            "needles": [
                "observation-level attacks", "cross-model consistency", "evidence-aligned", "authority cues",
                "calibration", "chain-of-thought faithfulness", "token pruning", "kv cache", "token adaptive",
            ],
            "why": (
                "VLM과 VideoLLM은 답만 맞아도 내부 evidence pipeline이 잘못되면 robot judge나 guardrail로 쓰기 어렵다. "
                "DefTEval은 frame sampling, token compression, modality fusion을 공격 표면으로 보고, CrACK은 CLIP/SAM/DINO 같은 collaborative pipeline의 semantic-spatial alignment dependency를 공격한다. "
                "Evidence-aligned guardrails, GradeTrap, DualRead, visual CoT faithfulness, CoVeR, ECOKV, and STAR-Pro는 verdict, confidence, token salience, cache diversity가 action-critical evidence를 실제로 보존했는지 따진다. "
                "APRL은 efficient perception을 latency만으로 고르지 말고 localized evidence retention, authority-bias resistance, adversarial observation robustness, and action-permission stability를 같이 봐야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Nine papers directly target observation attacks, cross-model interfaces, evidence localization, calibration, CoT faithfulness, token pruning, and KV cache retention.",
            "lab_action": (
                "Robot video judging and multi-view spatial QA에서 hazardous frame, prompt-injection text, authority cue, missing object, one-view-only target, and cache-pruned history를 stress cases로 만들고 evidence localization, answer flip, unsafe action refusal, token coverage, KV retention diversity, latency를 함께 측정한다."
            ),
            "limit": 6,
        },
        {
            "title": "Embodied navigation is becoming a problem of stale beliefs and timed assistance",
            "buckets": ["Embodied AI", "Robot Learning", "Foundation Models", "Safety/Alignment", "Efficiency/Systems"],
            "ids": ["2609.08159", "2609.05841", "2609.05593", "2609.06326", "2609.05596", "2609.08886", "2609.06880", "2609.06424"],
            "needles": [
                "long-horizon target navigation", "spatial belief", "navigation failure prediction", "generalist robots",
                "time-aware assistive navigation", "scene memory", "situated spatial reasoning", "motion-aware navigation",
            ],
            "why": (
                "Embodied navigation은 goal을 찾는 문제가 아니라, 기억과 믿음이 언제 낡았고 언제 사람에게 말해야 하는지 결정하는 문제로 이동한다. "
                "OmniNav는 scene validity, target belief, interaction feasibility를 factorized posterior로 묶고, Spatial Belief Fields는 language-goal aerial navigation에서 하나의 waypoint로 uncertainty를 조기 붕괴시키지 않는다. "
                "Cost-sensitive failure prediction, generalist robot safety, Time-Aware Assistive Navigation, FRAME scene memory, contextual observer grounding, and OVMAN은 모두 stale state, timed assistance, attribute retrieval, social/spatial context를 action variables로 만든다. "
                "APRL navigation benchmark는 target success보다 belief freshness, warning timing, object-attribute recall, consequence severity, and interaction feasibility를 먼저 평가해야 한다."
            ),
            "confidence": "Medium-High",
            "confidence_note": "Eight papers share belief freshness and timed assistance, but task settings span aerial, mobile, assistive, and generalist robots.",
            "lab_action": (
                "ObjectNav/VLN and assistive-navigation episodes에서 moved-object goals, ambiguous language, stale scene memory, delayed warning, hidden obstacle, and attribute-only reference를 독립 조건으로 두고 belief update accuracy, warning lead time, wrong-target action, consequence-weighted failure, final success를 평가한다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Evidence-fresh VLA recovery grid",
            "claim": (
                "Compare native video history, process memory labels, force-aware interruption, failure-boundary detection, and stage-aware correction inside the same manipulation episodes."
            ),
        },
        {
            "title": "Planner-facing geometry validity protocol",
            "claim": (
                "Evaluate 3DGS, spherical occupancy, in-hand reconstruction, inertial odometry, learned occupancy, and BEV maps by the robot actions they permit or block."
            ),
        },
        {
            "title": "Physical world-model role audit",
            "claim": (
                "Force a generated future to declare whether it is a planner prior, physics verifier, intervention predictor, recovery oracle, or scenario generator before using it."
            ),
        },
        {
            "title": "Efficient evidence admission stress test",
            "claim": (
                "Measure token pruning, KV eviction, frame sampling, and VLM guardrails by localized evidence retention, adversarial robustness, and action-permission stability."
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
        "meaning": "Included because it supports today's evidence-permission thesis.",
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
