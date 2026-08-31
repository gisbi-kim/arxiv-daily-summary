#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-08-31 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260831 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-31"


PROFILE = {
    "date": DATE,
    "weekday": "Mon",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching 2026-08-31 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-08-31 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "The 2026-08-31 batch pushes robot and vision systems from plausible outputs toward action-release contracts. "
        "Geometry papers ask whether scale, coordinate frame, correspondence, sonar/LiDAR ambiguity, and onboard memory survive the path from reconstruction to action. "
        "VLA and manipulation papers make future dynamics, deictic reference, partial observability, contact, and bin-picking deadlock explicit execution variables. "
        "World-model and video papers convert memory from a generic cache into executable code, layer-routed retrieval, object-centric particles, and physics-aware dynamics. "
        "VLM and safety papers ask which cue, alarm, formal rule, ASR error, or QoS state should change the system decision before an answer or robot command is allowed."
    ),
    "cluster_takeaway": (
        "Today's core is not another larger VLA, prettier reconstruction, or cheaper token budget; it is whether metric geometry, future evidence, conditional cues, and runtime alarms can veto or revise the next action."
    ),
    "trend_note": (
        "Monday /new produced 120 deduplicated non-replacement papers and 104 ROI papers. "
        "Foundation Models are the largest bucket, but the APRL-relevant signal is the convergence of metric geometry, planning-horizon control, world-model memory, evidence-conditioned VLMs, and runtime safety gates."
    ),
    "cluster_specs": [
        {
            "title": "Robot policies move from current-frame action decoding to horizon-conditioned repair decisions",
            "buckets": ["Robot Learning", "Generation"],
            "ids": ["2608.27550", "2608.28108", "2608.27609", "2608.28075", "2608.28175", "2608.28140", "2608.28491"],
            "needles": [
                "vla", "vision-language-action", "planning horizon", "deictic", "partially observable",
                "event-triggered", "contact-guided", "bin-picking", "world modeling", "robot video",
            ],
            "why": (
                "기존 VLA 평가는 현재 관측과 명령에서 바로 action을 내는 능력에 초점을 맞췄다. "
                "VLAct는 고정된 robot-data 예산에서 representation quality를 묻고, PHR-VLA는 future dynamics를 training signal로 넣으며, DeicticVLA와 ROBUST TAMP는 사용자 pointing과 새로 발견한 물체가 plan을 바꿔야 하는 순간을 다룬다. "
                "따라서 APRL은 final success가 아니라 동일한 현재 프레임에서 미래 contact, deictic mask, hidden object, deadlock state가 action과 recovery timing을 어떻게 바꾸는지 비교해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Six robot papers independently expose data budget, future horizon, instruction mode, partial observation, contact, and grasp deadlock as execution variables.",
            "lab_action": (
                "LIBERO/RoboTwin과 bin-picking scenes에서 future contact label, deictic target mask, hidden object discovery, non-prehensile contact reward, occluded grasp deadlock을 독립 stress condition으로 두고 action delta, recovery trigger timing, contact error, terminal success를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Geometry evaluation moves from relative reconstruction quality to metric action validity",
            "buckets": ["3D/Scene", "Robot Learning", "Efficiency/Systems", "Autonomous Driving", "Embodied AI"],
            "ids": ["2608.27497", "2608.28288", "2608.27795", "2608.28033", "2608.28096", "2608.27971", "2608.27628"],
            "needles": [
                "metric-aware", "uav mapping", "underwater", "sonar", "compressed cost volumes",
                "correspondence pruning", "geometry-aware alignment", "forest", "lidar", "scale",
            ],
            "why": (
                "3D reconstruction이 시각적으로 그럴듯해도 robot이 거리, scale, pose, alignment를 틀리면 그 map은 action evidence가 아니다. "
                "MAGP는 arbitrary scale을 직접 문제로 삼고, GeoFF3D는 large-scale UAV mapping에서 coordinate anchoring을 요구하며, uScenes와 forest navigation은 optical degradation과 GNSS/cloud 제약 때문에 sensor ambiguity와 onboard processing을 드러낸다. "
                "APRL geometry 평가는 clean reconstruction score 대신 metric scale error, correspondence outlier, sensor sparsity, field drift가 grasp, route reuse, localization recovery를 얼마나 바꾸는지 봐야 한다."
            ),
            "confidence": "High",
            "confidence_note": "3D/Scene has 16 ROI papers, and multiple independent papers mention metric scale, UAV mapping, sonar, MVS memory, 2D-3D outliers, LiDAR, and field deployment.",
            "lab_action": (
                "Metric-object manipulation, UAV map reuse, underwater sensing, sparse LiDAR, and forest navigation cases에서 feed-forward reconstruction, MVS, 2D-3D pruning, multimodal alignment, RGB-sonar fusion을 scale error, pose drift, route deviation, grasp error, onboard latency로 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "World models shift from plausible sequences to executable state and memory contracts",
            "buckets": ["Foundation Models", "Generation", "Robot Learning", "3D/Scene"],
            "ids": ["2608.27549", "2608.27922", "2608.28460", "2608.28491", "2608.28549", "2608.28174", "2608.28069"],
            "needles": [
                "code as worlds", "kv cache", "layerrecall", "world model", "robot video",
                "geometry learner", "video re-shooting", "3d gaussian", "physics", "memory",
            ],
            "why": (
                "World model은 자연스러운 영상 roll-out을 만드는 것만으로 robot simulator가 되지 않는다. "
                "Code-as-World는 physical reasoning을 executable representation으로 바꾸고, DensityKV와 LayerRecall은 long video memory를 무엇을 남길지와 어느 layer에서 꺼낼지의 문제로 재정의하며, AcrossVAM은 robot video prediction을 object-centric motion과 appearance로 분리한다. "
                "APRL은 frame similarity보다 counterfactual code execution, memory revisit consistency, object-state prediction, action correction value가 downstream planning을 바꾸는지 평가해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Seven papers connect executable representations, KV memory, layer-selective recall, robot video particles, geometry-from-video, and physics-aware dynamics.",
            "lab_action": (
                "Leave-and-return manipulation videos, UAV camera paths, deformable-object interactions, and generated physical scenes에서 executable state edits, layer memory routing, object-particle rollout, point-cloud render conditioning을 future object pose, revisit memory gain, contact consistency, action correction value로 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "VLM reasoning moves from answer fluency to conditional evidence acquisition",
            "buckets": ["Foundation Models", "Efficiency/Systems", "Embodied AI"],
            "ids": ["2608.27871", "2608.27881", "2608.28316", "2608.28216", "2608.28406", "2608.27997", "2608.28266"],
            "needles": [
                "temporal tree", "streaming video", "conditional visual evidence", "one-shot exemplar",
                "mistake detection", "cross-view referring", "coordination benchmark", "cue",
            ],
            "why": (
                "VLM이 답을 자연스럽게 말해도 그 답을 허가한 visual cue가 맞는지는 별도 문제다. "
                "Temporal Tree of Thought는 long video에서 coarse-to-fine cue search를 만들고, StreamEMS는 memory 자체를 self-evolving representation으로 바꾸며, Conditional Visual Evidence Utility는 이미 관측한 cue에 따라 다음 cue의 가치가 뒤집힐 수 있음을 보인다. "
                "APRL은 answer accuracy만 보지 말고 target-present rejection, evidence hit rate, cue-order sensitivity, cross-view identity consistency, mistake-detection lead time이 action permission을 바꾸는지 평가해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Six papers share long-video cue search, streaming memory restructuring, conditional cue utility, exemplar grounding, mistake detection, and cross-view grounding.",
            "lab_action": (
                "Long-video QA, cluttered object detection, air-ground target referral, household coordination, and robot mistake videos에서 cue acquisition order, memory update rule, exemplar presence, cross-view distractors를 바꿔 evidence hit rate, false target acceptance, mistake lead time, downstream action error를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Runtime safety shifts from model self-report to external alarms and verifiable repair",
            "buckets": ["Safety/Alignment", "Embodied AI", "Efficiency/Systems", "Autonomous Driving"],
            "ids": ["2608.27808", "2608.28305", "2608.28437", "2608.28518", "2608.28409", "2608.27685"],
            "needles": [
                "runtime alarms", "closed-loop safe planning", "voice-controlled", "digital-twin",
                "risk-aware exploration", "bounded delay", "formal verification", "qos",
            ],
            "why": (
                "자율 에이전트와 robot이 스스로 성공했다고 말하는 것은 안전 evidence가 아니다. "
                "CURA는 computer-use agent의 false success self-report를 외부 telemetry alarm으로 감시하고, PanelShield는 manual evidence와 formal verification으로 industrial panel action을 repair하며, voice-controlled EAI와 LUCID는 ASR ambiguity와 QoS drift가 실행 risk로 이어지는 경로를 드러낸다. "
                "APRL은 policy confidence 대신 external alarm precision, violation localization, unsafe instruction acceptance, QoS-induced action delay, recovery cost를 실행 전 permission gate로 평가해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Six autonomy and safety papers independently expose false self-report, formal repair, ASR risk, QoS drift, risk allocation, and communication delay.",
            "lab_action": (
                "OSWorld-style agent tasks, industrial panel primitives, voice-command navigation, cloud-robot QoS, and heterogeneous multi-robot exploration에서 telemetry alarm, manual constraint, ASR confusion, bandwidth drop, hazard exposure를 stress split으로 만들고 violation-before-action, repair success, mission-value loss를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Deployment efficiency moves from compression ratio to preserving decision-changing evidence",
            "buckets": ["Efficiency/Systems", "Foundation Models", "3D/Scene", "Autonomous Driving", "Generation"],
            "ids": ["2608.28138", "2608.28008", "2608.28086", "2608.28429", "2608.28272", "2608.27735", "2608.27888"],
            "needles": [
                "token-budget", "visual token coding", "token communications", "event compression",
                "3dgs compression", "constant-vram", "thread-efficient", "bitrate", "memory",
            ],
            "why": (
                "배포 효율이 latency, bitrate, VRAM 숫자만 줄이는 경쟁이면 robot perception에서 어떤 evidence가 사라졌는지 보이지 않는다. "
                "Token-Budget Distillation과 Visual Token Coding은 compressed video VLM에서도 full-token semantics와 spatial coverage를 보존하려 하고, Ada-TokenCom과 Lossy Event Compression은 transmission이나 distortion metric이 task performance와 맞는지 묻는다. "
                "APRL은 압축 후 localization cue, object boundary, event timing, action-critical context, semantic safety class가 남아 있는지 downstream task 기준으로 비교해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Seven efficiency papers link video token compression, semantic communication, event compression, 3DGS quantization, constant-VRAM training, and runtime decoding.",
            "lab_action": (
                "Robot video QA, visual servoing, event-camera detection, 3DGS map streaming, texture-heavy simulation, and IoV perception에서 token budget, bitrate, VRAM partition, decoder sharing을 독립 변수로 두고 cue retention, boundary error, event timing loss, action-choice delta를 비교한다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Metric geometry action-release gate",
            "claim": (
                "Build a benchmark where reconstruction must preserve metric scale, coordinate frame, correspondence, and sensor ambiguity well enough to keep grasp, route, and localization decisions stable."
            ),
        },
        {
            "title": "Horizon-conditioned VLA recovery grid",
            "claim": (
                "Use paired manipulation states that look identical now but diverge in future contact, deictic reference, hidden object discovery, and deadlock risk to test when policies revise action."
            ),
        },
        {
            "title": "External alarm and repair protocol",
            "claim": (
                "Combine telemetry alarms, manual-derived formal constraints, ASR perturbations, and QoS shifts so robot or agent actions need independent permission before execution."
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
        "meaning": "Included because it supports today's action-release-contract thesis.",
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
