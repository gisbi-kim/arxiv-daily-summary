#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-09-02 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260902 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-02"


PROFILE = {
    "date": DATE,
    "weekday": "Wed",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching 2026-09-02 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-09-02 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "The 2026-09-02 batch is about action permission under stale state and incomplete evidence. "
        "Geometry papers turn maps, scene graphs, and point-cloud registration into freshness contracts: VOIM delays semantic commitment, "
        "DSG and HitMem update dynamic 3D memory, On-the-Fly3R rejects inconsistent UAV views, and industrial bundle adjustment removes brittle correspondences before planning inherits the error. "
        "VLA and manipulation papers split action into typed motor programs, executable-skill preconditions, adaptive chunk stops, negation constraints, and future contact consequences. "
        "Driving and robot autonomy papers ask whether rare objects, partner communication, compression stages, and long-horizon risk should actually change the feasible action set. "
        "VLM and efficiency papers make the same demand at the evidence layer: verify the task, prove the visual cue was used, and spend extra tokens or bandwidth only when it changes the decision."
    ),
    "cluster_takeaway": (
        "Today's core is not a larger policy, denser map, or lower token count; it is whether state freshness, contact consequence, and visual evidence can veto or revise the next robot action."
    ),
    "trend_note": (
        "Wednesday /new produced 197 deduplicated non-replacement papers and 167 ROI papers. "
        "Foundation Models, Generation, and Efficiency/Systems are the largest buckets, but the APRL-relevant signal is the convergence of dynamic 3D memory, typed VLA execution, long-tail action affordance, visual evidence verification, and resource escalation gates."
    ),
    "cluster_specs": [
        {
            "title": "3D maps move from accumulated geometry to freshness-gated action state",
            "buckets": ["3D/Scene", "Embodied AI"],
            "ids": ["2609.00775", "2609.00619", "2609.00950", "2609.00923", "2609.01089", "2609.01276"],
            "needles": [
                "open-vocabulary 3d instance", "dynamic 3d scene graph", "temporal 3d memory",
                "online 3d reconstruction", "bundle adjustment", "correspondence-free",
                "egocentric video", "metric frame", "uav", "slam", "stale",
            ],
            "why": (
                "기존 mapping 평가는 더 많은 관측을 누적하면 map이 좋아진다는 가정에 기대기 쉽다. "
                "VOIM은 첫 detection에서 label을 확정하는 순간이 가장 약하다고 보고 voxel evidence가 쌓일 때까지 semantic commitment를 미루며, DSG와 HitMem은 object displacement가 scene graph와 3D memory를 낡게 만드는 문제를 직접 다룬다. "
                "On-the-Fly3R과 correspondence-free bundle adjustment는 UAV나 산업 workcell처럼 입력 순서와 correspondence가 불안정한 곳에서 잘못된 view를 받아들이지 않는 장치를 둔다. "
                "APRL geometry 평가는 map quality가 아니라 stale label, view rejection, memory decay, correspondence ambiguity가 route, grasp, relocalization을 얼마나 바꾸는지로 설계해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Six papers independently expose deferred labels, dynamic scene graphs, stale 3D memory, UAV consistency checks, correspondence-free registration, and egocentric metric frames.",
            "lab_action": (
                "Indoor ObjectNav, industrial scrap, UAV mapping, and egocentric manipulation scenes에서 label deferral, scene-graph update, memory decay, view rejection, and depth-map registration을 독립 ablation 축으로 두고 object relocation, route deviation, grasp-region error, relocalization success를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "VLA execution moves from raw action chunks to typed permission and stop contracts",
            "buckets": ["Robot Learning"],
            "ids": ["2609.01215", "2609.01281", "2609.00908", "2609.01596", "2609.00555", "2609.00641"],
            "needles": [
                "typed motor programs", "orchestrating", "deploying vla", "action chunking",
                "contact-rich", "negation-constrained", "aerial manipulation", "benchmark",
            ],
            "why": (
                "VLA를 raw action이나 고정 chunk를 내는 모델로만 보면 long-horizon failure가 어디서 시작됐는지 설명하기 어렵다. "
                "REFACTOR-VLA는 행동적으로 같은 motor program을 library로 인정하는 조건을 묻고, EmbodiedSkills는 skill decision을 실행 proposal로 보아 precondition과 outcome verification을 둔다. "
                "adaptive action chunking은 관측 grounding이 약해지는 순간 stop signal을 만들고, Facet-0과 negation-constrained grasping은 contact consequence와 forbidden region을 action 자체의 조건으로 끌어온다. "
                "따라서 APRL은 success rate 전에 skill type, precondition validity, attention stop timing, contact wrench, forbidden-region violation이 action permission을 바꾸는지 평가해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Six robot papers connect typed abstractions, execution proposals, adaptive stopping, contact prediction, negation constraints, and aerial manipulation benchmarks.",
            "lab_action": (
                "LIBERO, RoboTwin, peg/assembly, dexterous grasp, and aerial manipulation tasks에서 typed skill library, prerequisite check, action-attention entropy, action-wrench prediction, forbidden-part mask를 독립 변수로 두고 invalid-action rejection, contact failure lead time, recovery success, terminal task score를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Driving autonomy shifts from recognizing rare cases to deciding whether action affordance changed",
            "buckets": ["Autonomous Driving", "Efficiency/Systems"],
            "ids": ["2609.00242", "2609.00111", "2609.00192", "2609.00385", "2609.00718", "2609.00951"],
            "needles": [
                "counterfactual long-tail", "driving affordance", "qwen-drive", "pedestrian yielding",
                "risk-aware", "overtaking", "compressed driving", "collaborative perception",
            ],
            "why": (
                "자율주행 평가는 rare object를 맞혔는지나 planning score가 높은지에서 멈추면 실제 행동 변화를 놓친다. "
                "CoLT-Drive는 rare object가 ego vehicle의 feasible meta-action을 바꾸는지 묻고, Qwen-Drive는 BEV head와 planning expert를 inspectable 3D/action interface로 둔다. "
                "pedestrian-yielding bias benchmark와 risk-aware overtaking은 common-sense model과 implicit risk가 안전한 행동 근거가 되지 못할 수 있음을 보여주며, compressed driving policy 평가는 어떤 compression stage에서 stop-and-resume capability가 깨지는지 따라간다. "
                "APRL은 detection AP가 아니라 counterfactual object, social bias, long-horizon risk, communication payload, compression stage가 action set을 바꾸는지 평가해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Driving papers span counterfactual affordance, unified VLM-driving, bias tests, explicit risk rollouts, compression-stage loss, and collaborative perception.",
            "lab_action": (
                "Urban intersection, highway overtaking, collaborative perception, and compressed-policy scenarios에서 rare-object insertion, pedestrian attribute control, risk rollout horizon, V2V payload, pruning/distillation/quantization stage를 stress split으로 만들고 feasible action change, violation rate, recovery timing, closed-loop safety를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "VLM evaluation moves from answer accuracy to proving visual evidence changed the decision",
            "buckets": ["Foundation Models"],
            "ids": ["2609.00231", "2609.00232", "2609.00868", "2609.00658", "2609.00663", "2609.00830"],
            "needles": [
                "visual-origin hallucination", "task verification", "visual insensitivity",
                "metric physical reasoning", "render ceiling", "attention faithfulness",
            ],
            "why": (
                "VLM이 정답을 맞혀도 image evidence를 실제로 사용했는지는 별도 문제다. "
                "visual-origin hallucination은 hallucination 원인이 language prior만이 아니라 visual feature extraction과 image-text alignment일 수 있음을 보이고, VeriOCRBench는 애초에 answerable task인지 검증해야 한다고 말한다. "
                "Visual Insensitivity Gap, scale-equivariance training, render ceiling, attention-faithfulness 분석은 visual perturbation, metric scale, known rendering, attention causal effect로 모델이 어떤 cue를 썼는지 분리한다. "
                "APRL robot VLM 평가는 final answer accuracy보다 missing-target rejection, decisive-region sensitivity, scale use, and perception-reasoning split이 action permission을 바꾸는지 봐야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Six VLM papers independently test hallucination source, invalid-task verification, vision-ignoring samples, metric scale use, render ceilings, and attention faithfulness.",
            "lab_action": (
                "Robot instruction QA, text-rich tool panels, metric-video reasoning, and rendered 3D object queries에서 target absence, decisive-region blur, supplied-scale rescaling, camera inversion, attention perturbation을 독립 조건으로 두고 answer change, refusal precision, unsafe action permission, perception-vs-reasoning error를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Runtime efficiency moves from fewer tokens to query-specific evidence escalation",
            "buckets": ["Efficiency/Systems", "Foundation Models"],
            "ids": ["2609.00291", "2609.01200", "2609.01004", "2609.01224", "2609.00355", "2609.00659"],
            "needles": [
                "streaming video", "visual-token", "token pruning", "speculative decoding",
                "context plane", "cooperative perception", "token", "bandwidth", "memory",
            ],
            "why": (
                "효율을 token 수, bitrate, latency만 줄이는 문제로 보면 어떤 evidence를 버려도 되는지 판단할 수 없다. "
                "StreamScout는 query마다 timeline, recent frames, uniform look-back, salient retrieval 중 어디까지 봐야 하는지 결정하고, AI traffic coding은 split VLM의 visual-token payload를 rate-distortion이 아니라 rate-task 문제로 바꾼다. "
                "SinkPruner, S2Prune, GLANCE, drone fleet context plane은 high-norm sink token, spatial coverage, grounded speculative decoding, mission/bandwidth/context 조건이 evidence retention을 좌우한다고 본다. "
                "APRL은 compressed or pruned representation을 downstream action cue, old-event retrieval, spatial coverage, communication context가 남아 있는지로 비교해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Six systems papers connect adaptive video evidence, compressed AI traffic, sink token pruning, spatial coverage, vision-aware drafting, and fleet context routing.",
            "lab_action": (
                "Streaming robot video, split VLM inference, drone fleet perception, and grounded instruction tasks에서 token budget, retrieval depth, NNC quantization, sink-token removal, spatial region coverage, context-plane routing을 ablation하고 decisive-cue retention, old-event miss, action-choice delta, bandwidth-latency trade-off를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "World models move from plausible media to verifiable physical and spatial control loops",
            "buckets": ["Robot Learning", "Embodied AI", "Generation", "Foundation Models", "Efficiency/Systems", "Autonomous Driving"],
            "ids": ["2609.00188", "2609.00161", "2609.00610", "2609.00656", "2609.01582", "2609.01560", "2609.01252"],
            "needles": [
                "world action models", "interaction map", "4d world models", "physically plausible video",
                "spatialguard", "world control", "camera-controlled", "metric rotary",
            ],
            "why": (
                "World model과 generation은 그럴듯한 영상이나 장면을 만드는 단계에서 action과 검증 가능한 constraint를 다루는 단계로 이동하고 있다. "
                "ZimaBlue는 action-free egocentric video를 robot action model로 접지하고, IMPACT는 interaction region이 globally averaged loss에서 묻히는 문제를 attention-derived interaction map으로 보정한다. "
                "Streaming4D, chain-of-events video generation, SpatialGuard, H3-World, MeRoPE는 online 4D geometry, physical event chain, editable 3D layout harness, temporally routed language control, metric camera trajectory를 각각 검증 가능한 control variable로 만든다. "
                "APRL은 visual plausibility보다 action grounding, interaction fidelity, physical transition, spatial relation repair, camera-scale stability가 robot planning을 바꾸는지 평가해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Seven papers expose video-pretrained world action models, interaction-aware training, online 4D reconstruction, physical event conditioning, spatial harnesses, language control, and metric camera encodings.",
            "lab_action": (
                "Manipulation, navigation, camera-control, and interactive simulation tasks에서 egocentric video scale, interaction-map reweighting, block-wise 4D updates, event-chain conditioning, layout harness repair, temporal language routing, metric camera encoding을 비교해 contact consistency, spatial-relation violation, control leakage, planning success를 평가한다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Dynamic 3D memory freshness benchmark",
            "claim": (
                "Build paired scenes where maps, scene graphs, and 3D memory become stale, then evaluate whether update/retrieval policies preserve route, grasp, and relocalization decisions."
            ),
        },
        {
            "title": "Typed VLA action-permission protocol",
            "claim": (
                "Separate skill abstraction, precondition checks, adaptive chunk stopping, contact-wrench prediction, and forbidden-region constraints before a VLA command is executed."
            ),
        },
        {
            "title": "Counterfactual affordance test for autonomy",
            "claim": (
                "Use rare-object insertion, pedestrian-attribute controls, compression stages, and V2V payload changes to test whether perception changes feasible action rather than only labels."
            ),
        },
        {
            "title": "Evidence-use gate for robot VLMs",
            "claim": (
                "Measure target validity, visual sensitivity, metric-scale use, render ceilings, and adaptive evidence escalation before an answer can authorize a robot action."
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
        "meaning": "Included because it supports today's state-freshness and evidence-contract thesis.",
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
