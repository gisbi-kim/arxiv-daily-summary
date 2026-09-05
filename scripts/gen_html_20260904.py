#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-09-04 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260904 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-04"


PROFILE = {
    "date": DATE,
    "weekday": "Fri",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching 2026-09-04 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-09-04 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "The 2026-09-04 batch is about evidence budgets before action authority. Geometry papers make reconstruction, odometry, "
        "wire segmentation, semantic maps, and industrial surface localization useful only when pose drift, contact consistency, "
        "sensor degeneracy, and downstream task error are measured together. VLA and manipulation papers reject raw scale as the "
        "default answer: web-video retrieval, evidence-gated modalities, real-to-sim evaluation, scheduled imagination, compact "
        "LIBERO policies, force-aware compensation, and action-sufficient intermediate features all ask which supervision or sensor "
        "signal may change the command. World-model papers similarly move from plausible futures to physically verified, action-consistent, "
        "and risk-aware feedback loops. VLM, safety, and efficiency papers then turn answers, pruned tokens, restored images, privacy exports, "
        "and uncertainty monitors into release gates that must preserve the evidence a robot needs to continue, stop, defer, or recover."
    ),
    "cluster_takeaway": (
        "Today's core is not adding more sensors, tokens, simulations, or demonstrations; it is deciding which evidence unit earns permission "
        "to change a robot action under cost, uncertainty, privacy risk, and physical contact."
    ),
    "trend_note": (
        "Friday /new produced 151 deduplicated non-replacement papers and 128 ROI papers. Generation, Efficiency/Systems, Foundation Models, "
        "and 3D/Scene are all substantial, but the APRL-relevant signal is the shared evidence-budget contract: modality gates, pose drift repair, "
        "behavior-quality evaluation, action-faithful world models, shortcut-resistant VLM tests, and risk-aware runtime monitors all ask what "
        "survives into the next action."
    ),
    "cluster_specs": [
        {
            "title": "Robot-usable geometry moves from reconstruction quality to drift and contact-aware action frames",
            "buckets": ["3D/Scene", "Robot Learning", "Safety/Alignment"],
            "ids": ["2609.03102", "2609.04201", "2609.03561", "2609.03891", "2609.03970", "2609.03720"],
            "needles": [
                "online 3d reconstruction", "pose query", "radar-imu-lidar", "odometry", "semantic mapping",
                "wire", "weld seam", "photogrammetry", "point clouds", "vibration", "depth", "gaussian",
            ],
            "why": (
                "기존 3D 평가는 reconstruction이나 segmentation 품질을 따로 보고 끝나기 쉽지만, 로봇은 pose drift, sensor degeneracy, wire contact, semantic freshness, and inspection geometry가 틀리면 바로 잘못된 행동을 낸다. "
                "Scal3R는 long video에서 local depth와 global pose failure를 분리하고, TRaIL-Odom은 LiDAR가 약한 방향에 radar Doppler를 더 믿게 하며, WireSeg-32K와 weld mapping은 물리적 접촉 형상과 작업 대상 geometry를 실제 robot pipeline에 넣는다. "
                "따라서 APRL geometry 평가는 visual fidelity가 아니라 relocalization, contact-safe manipulation, inspection pass, and route or grasp error가 바뀌는 조건으로 설계해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Six papers independently connect wire contact, pose drift, radar-LiDAR degeneracy, terrain vibration, semantic map updates, and weld-seam reconstruction.",
            "lab_action": (
                "Robot corridor, cable handling, rover terrain, and weld-inspection scenes에서 first-frame pose anchoring, Doppler weighting, wire self-occlusion, semantic-map update rate, photogrammetry viewpoint count를 독립 ablation 축으로 두고 relocalization success, slip or vibration risk, weld localization error, grasp-frame error를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "VLA learning shifts from demonstration volume to evidence-gated supervision and evaluation",
            "buckets": ["Robot Learning"],
            "ids": ["2609.03199", "2609.03142", "2609.03276", "2609.03681", "2609.03715", "2609.04193"],
            "needles": [
                "human demonstration retrieval", "evidence-gated", "real-to-sim", "imagination scheduling",
                "small can a manipulation policy", "action-oriented structural supervision", "world-model-guided",
            ],
            "why": (
                "Robot learning은 더 큰 VLA나 더 많은 demo만으로 설명하기 어려운 단계로 들어갔다. RoboTok은 web video가 robot supervision이 되려면 actor-centered hand trajectory retrieval이 필요하다고 보고, EGR은 sensor별 task relevance가 없는 fusion을 위험하게 본다. "
                "R2S-Eval은 success rate보다 behavior-quality ranking을 안정화하려 하고, WISE와 GIFT는 imagined future나 intermediate feature가 action에 충분한 구조를 남길 때만 supervision으로 인정한다. "
                "APRL은 demonstration source, sensor relevance, evaluation judge, imagination timing, feature supervision이 action permission과 recovery ranking을 실제로 바꾸는지 한 프로토콜에서 봐야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Six robot-learning papers expose data retrieval, modality evidence, evaluation calibration, imagination timing, compact policy capacity, and action-sufficient features.",
            "lab_action": (
                "LIBERO, RoboCasa, bimanual household, and visuotactile manipulation tasks에서 web-demo retrieval, modality gate, real-to-sim evaluator, imagination trigger, policy size, intermediate geometry-affordance supervision을 분리하고 action delta, failure lead time, human preference ranking, recovery success를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Contact-rich embodiment asks when physical interaction is allowed to continue",
            "buckets": ["Robot Learning", "Embodied AI", "3D/Scene", "Safety/Alignment"],
            "ids": ["2609.03889", "2609.03362", "2609.03761", "2609.03591", "2609.03758", "2609.03984"],
            "needles": [
                "contact-rich", "force-aware", "gripper", "bimanual", "on-policy corrections", "vine robot",
                "parkour", "tool manipulation", "passive grippers", "force", "manipulation",
            ],
            "why": (
                "Task completion만 보면 force, contact onset, gripper-object fit, body compensation, and recovery correction이 안전한지 알 수 없다. FWBC-VLA는 contact state를 token으로 넣어 semantic action과 whole-body compensation을 연결하고, ARTiS와 object-specific passive grippers는 tool or object geometry가 실제 force transfer를 좌우한다고 본다. "
                "Bimanual household manipulation and quadruped parkour work expand the same question to large-scale demonstrations, on-policy corrections, and autonomous terrain choices. "
                "APRL은 continue, reset, slow down, change grip, or fallback을 terminal success 이전에 판단하는 contact-state release gate를 가져야 한다."
            ),
            "confidence": "Medium-High",
            "confidence_note": "Contact, tool, gripper, bimanual, vine, and quadruped papers point to physical interaction variables, though shared benchmarks remain fragmented.",
            "lab_action": (
                "Door opening, whiteboard wiping, tool use, cable/wire handling, bimanual transfer, and rough-terrain locomotion에서 estimated force, local contact geometry, passive gripper compliance, correction timing, body compensation, terrain vibration을 ablation하고 continuation permission, force violation, recovery success, and task completion을 함께 평가한다."
            ),
            "limit": 6,
        },
        {
            "title": "World models move from plausible futures to action-consistent and risk-aware feedback loops",
            "buckets": ["Autonomous Driving", "Generation", "Foundation Models", "Robot Learning", "Efficiency/Systems"],
            "ids": ["2609.03572", "2609.03602", "2609.03225", "2609.03557", "2609.03952", "2609.03565", "2609.03774", "2609.04196"],
            "needles": [
                "world model", "world-action", "action-conditioned", "camera-conditioned", "physical",
                "reward", "jepa", "risk-informed", "native 3d world states", "driving", "feedback",
            ],
            "why": (
                "World model을 그럴듯한 video나 future representation으로만 평가하면 controller가 어떤 action을 바꿨는지 모른다. Drive-HWM, SV-WAM, and multi-style driving world models tie future prediction to driving action, while WorldReward and VeriPhy ask whether generated clips preserve action consistency and physical obligations. "
                "WISE, physically grounded JEPA, RIWM, and Puffin-World extend that logic to robot planning, intervention, uncertainty, recoverability, and native 3D world states. "
                "APRL은 imagined future가 action ranking, safety margin, recovery choice, and physical state estimate를 바꿀 때만 policy evidence로 인정해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Driving, manipulation, generative video, reward-model, JEPA, RIWM, and unified 3D world-state papers repeat action-consistency and feedback requirements.",
            "lab_action": (
                "Driving, manipulation, mobile navigation, and camera-control tasks에서 rollout horizon, action-conditioned data source, camera command, reward chunking, physical-verification failure, JEPA state alignment, risk memory를 독립 조건으로 두고 closed-loop action ranking, safety violation, recovery timing, and physical-state error를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "VLM reliability shifts from correct answers to shortcut-resistant evidence tests",
            "buckets": ["Foundation Models", "Safety/Alignment", "Efficiency/Systems"],
            "ids": ["2609.03611", "2609.03261", "2609.03429", "2609.03729", "2609.04200", "2609.03544", "2609.03675"],
            "needles": [
                "failbench", "shortcuts", "object-token", "answer-key-free", "spatial reasoning", "physical reasoning",
                "hallucination", "safety intervention", "evidence selection", "streaming video",
            ],
            "why": (
                "정답률이나 VLM judge agreement만 보면 모델이 실제 visual evidence를 썼는지 알 수 없다. FailBench는 robot task success judgment 자체가 cross-domain failure detection 문제라고 보고, MedQA-MM은 medical answer가 image finding이 아니라 shortcut으로 맞을 수 있음을 지적한다. "
                "object-token edits, 4D spatial reasoning, Principia, SafeRI, and CoFiE all test whether visual state, physics relation, safety token, or selected frame actually changes the answer. "
                "APRL robot VLM 평가는 final answer 대신 target absence, shortcut dependence, spatial relation, physical rule, and evidence-selection depth가 action permission을 바꾸는지 봐야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Robot judge, medical shortcut, object-token edit, 4D spatial, relational physics, safety-token, and streaming-evidence papers independently attack answer-only evaluation.",
            "lab_action": (
                "Robot outcome judging, tool-panel reading, spatial instruction QA, long-video task monitoring, and physical-rule prompts에서 target masking, answerable-task verification, object-token edit, relation inversion, safety-token intervention, coarse-to-fine frame selection을 ablation하고 answer change, refusal precision, unsafe action permission, and judge ranking stability를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Efficiency and safety gates move from lower cost to retained evidence and certified risk",
            "buckets": ["Efficiency/Systems", "Safety/Alignment", "Foundation Models"],
            "ids": ["2609.03158", "2609.03675", "2609.03820", "2609.03055", "2609.03699", "2609.03475", "2609.03516", "2609.03453"],
            "needles": [
                "token pruning", "coverage optimization", "evidence selection", "visual-token allocation",
                "privacy leakage", "runtime monitoring", "risk certificates", "missing-modality", "preprocessing failure",
            ],
            "why": (
                "Deployment cost와 safety를 평균 latency나 clean accuracy로만 보면 결정적 evidence를 버린 순간을 놓친다. CoverPruner asks who represents discarded tokens, CoFiE and long-video allocation test which frames deserve expensive processing, and robot privacy exports show that task utility can stay high while private structure leaks. "
                "PZR, SafeRestore, FlexibleFusion, and preprocessing-failure work add runtime uncertainty, detector-relative restoration risk, missing-modality fallback, and edge adversarial exposure. "
                "APRL은 cheaper, safer, or more private representation을 action-critical cue retention, residual risk, uncertainty precision, and downstream action delta로 인증해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Eight systems and safety papers connect token coverage, streaming evidence, privacy leakage, runtime monitoring, restoration certificates, modality fallback, and edge defenses.",
            "lab_action": (
                "Streaming robot video, domestic navigation export, industrial inspection, infrared-visible detection, and uncertainty-monitored arm control에서 token budget, frame selection, representation abstraction, zonotope reduction, restoration gate, missing-modality path를 ablation하고 decisive-cue recall, privacy leakage, false-positive monitor rate, detector evidence loss, and action delta를 비교한다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Evidence-budgeted action-admission benchmark",
            "claim": (
                "Use the same robot episodes to test whether modality gates, token pruning, real-to-sim evaluation, world-model imagination, and runtime monitors preserve the evidence that changes action."
            ),
        },
        {
            "title": "Robot-usable geometry drift protocol",
            "claim": (
                "Compare online reconstruction, Doppler-weighted odometry, semantic mapping, wire perception, and weld localization by downstream relocalization, grasp, inspection, and route errors."
            ),
        },
        {
            "title": "Scheduled imagination release gate",
            "claim": (
                "Evaluate world-model futures only at interaction-relevant states, with explicit horizon, physical obligation, feedback schedule, and policy-ranking impact."
            ),
        },
        {
            "title": "Shortcut-resistant robot evaluator",
            "claim": (
                "Validate VLM judges and efficient video selectors with target absence, visual shortcut, physical-rule, stale-state, and unsafe-action conditions before using them for robot policy ranking."
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
        "meaning": "Included because it supports today's evidence-budget and action-authority thesis.",
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
