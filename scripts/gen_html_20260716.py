#!/usr/bin/env python3
"""Generate the 2026-07-16 daily briefing from matching arXiv /new listings."""
from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, phylogeny_for, week_start
from gen_research_intelligence_20260716 import DATA as RI_DATA


DATE = "2026-07-16"

PROFILE = {
    "date": DATE,
    "weekday": "Thu",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from the matching 2026-07-16 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-07-16 arXiv /new listings. "
        "Tier A claims are audited against official arXiv full text in the Research Intelligence edition."
    ),
    "thesis": (
        "7월 16일 배치의 핵심은 VLA와 embodied system이 커질수록 representation, state, simulator가 "
        "자동으로 좋아지는 것이 아니라는 점입니다. VLA 논문들은 fine-tuning 과정에서 semantic structure가 "
        "행동 표현 안에서 침식되는 문제를 드러내고, scene graph와 HRI benchmark 논문들은 완전한 상태를 "
        "한 번에 넣는 방식이 planner와 collaboration failure를 숨길 수 있음을 보입니다. APRL에는 더 큰 "
        "backbone보다 semantic retention, just-in-time state growth, simulator validity를 한 실험표에서 "
        "추적하는 harness가 더 즉시적인 연구 자산입니다."
    ),
    "cluster_takeaway": (
        "오늘의 논문들은 공통적으로 '더 많은 입력/더 큰 모델/더 빠른 simulator'가 아니라, 어떤 정보가 "
        "행동 결정에 실제로 남아야 하는지를 계측하라는 방향을 가리킵니다."
    ),
    "trend_note": (
        "Robot Learning, Efficiency/Systems, Generation, 3D/Scene이 동시에 두드러졌지만, robotics 관점의 "
        "공통 축은 semantic drift, runtime state saturation, simulator artifact, world-model controllability입니다. "
        "이는 최근 4주간 반복된 VLA runtime, geometry validity, benchmark audit 흐름과 이어집니다."
    ),
    "cluster_specs": [
        {
            "title": "VLA fine-tuning이 action skill보다 semantic retention 문제로 이동",
            "buckets": ["Robot Learning", "Foundation Models", "Efficiency/Systems"],
            "ids": ["2607.13429", "2607.13597", "2607.13605", "2607.13361", "2607.13455", "2607.13712"],
            "needles": ["vla", "language-action", "semantic", "fine-tuning", "instruction", "action representation"],
            "why": (
                "Anchor-Align과 Semantic Anchoring은 behavior cloning이 pretrained semantic structure를 지워 "
                "OOD object/instruction 실패를 만들 수 있음을 전면에 둡니다. stage-information VLA와 reverse-task "
                "policy learning까지 합치면, 오늘의 VLA 축은 더 많은 demo보다 fine-tuning 중 무엇을 보존할지 "
                "계측하는 문제로 이동했습니다."
            ),
            "confidence": "High",
            "confidence_note": "VLA, action representation, semantic alignment 신호가 CV/RO 양쪽에서 반복됩니다.",
            "lab_action": (
                "LIBERO/RoboCasa fine-tuning trajectory마다 instruction-action retrieval, OOD object swap, "
                "stage boundary error를 checkpoint별로 산출하고 success rate와 rank correlation을 비교합니다."
            ),
            "limit": 6,
        },
        {
            "title": "Embodied memory가 complete map에서 just-in-time state growth로 이동",
            "buckets": ["Embodied AI", "Robot Learning", "3D/Scene"],
            "ids": ["2607.13245", "2607.13653", "2607.13072", "2607.13461", "2607.13624", "2607.13067"],
            "needles": ["scene graph", "long-horizon", "navigation", "open-world", "semantic map", "teleoperation"],
            "why": (
                "JIT scene graph는 full graph가 planner를 포화시킬 수 있다고 보고, open-world mobile manipulation과 "
                "language-to-navigation 논문들은 필요한 state를 task intent에 맞게 열어야 한다고 봅니다. 이는 "
                "memory를 많이 저장하는 문제가 아니라, 언제 어떤 state를 성장시키고 버릴지 정하는 runtime protocol 문제입니다."
            ),
            "confidence": "High",
            "confidence_note": "scene graph, navigation, mobile manipulation, teleoperation이 모두 state-management 축으로 연결됩니다.",
            "lab_action": (
                "ObjectNav/mobile manipulation task에서 full graph, retrieved graph, just-in-time graph를 같은 "
                "planner와 latency budget으로 돌리고 graph token count, hidden dependency miss, recovery success를 잽니다."
            ),
            "limit": 6,
        },
        {
            "title": "World model과 simulator scale이 downstream validity 감사로 이동",
            "buckets": ["3D/Scene", "Autonomous Driving", "Generation", "Robot Learning"],
            "ids": ["2607.14005", "2607.13410", "2607.13059", "2607.13481", "2607.13451", "2607.13927"],
            "needles": ["world model", "simulator", "simulation", "driving", "occupancy", "dynamics", "long-horizon"],
            "why": (
                "M4World와 DynaDreamer는 driving world model을 long-horizon control과 ego-dynamics prior로 바꾸고, "
                "GPUSimBench는 GPU simulator를 physical consistency, scalability, determinism으로 나눕니다. "
                "공통 질문은 generated data의 양이 아니라 policy ranking과 failure distribution이 실제로 보존되는지입니다."
            ),
            "confidence": "High",
            "confidence_note": "driving world model, simulator benchmark, deformable dynamics가 같은 validity 축에 놓입니다.",
            "lab_action": (
                "동일 policy set을 simulator/world-model 조건별로 평가해 ranking inversion, determinism variance, "
                "closed-loop failure taxonomy를 조건별 metric bundle로 산출합니다."
            ),
            "limit": 6,
        },
        {
            "title": "Benchmark accuracy가 visual grounding과 interaction contract 감사로 이동",
            "buckets": ["Efficiency/Systems", "Robot Learning", "Safety/Alignment", "Generation"],
            "ids": ["2607.13305", "2607.13056", "2607.13527", "2607.13792", "2607.13931", "2607.10057"],
            "needles": ["benchmark", "grounding", "visual dependency", "interaction", "evaluation", "verifiable"],
            "why": (
                "Accuracy Without Grounding은 video LLM benchmark에서 정답률이 시각 의존성을 보장하지 않음을 묻고, "
                "HRIBench는 human role과 temporal coordination을 benchmark contract로 넣습니다. VGIF-Score와 "
                "egocentric procedural VQA까지 합치면, 오늘의 평가 축은 headline score가 아니라 어떤 evidence channel이 "
                "정답을 만들었는지 감사하는 방향입니다."
            ),
            "confidence": "High",
            "confidence_note": "benchmark, visual dependency, HRI, procedural reasoning 신호가 여러 bucket에서 반복됩니다.",
            "lab_action": (
                "기존 VLA/VLN evaluation에 black-frame or stale-observation control, evaluator threshold sweep, "
                "human-role perturbation을 넣고 score flip과 rollout failure를 같이 저장합니다."
            ),
            "limit": 6,
        },
        {
            "title": "Geometry와 sensing은 visual quality에서 robot-usable uncertainty로 이동",
            "buckets": ["3D/Scene", "Autonomous Driving", "Efficiency/Systems", "Safety/Alignment"],
            "ids": ["2607.13405", "2607.13682", "2607.13891", "2607.13674", "2607.13802", "2607.13925"],
            "needles": ["uncertainty", "lidar", "tracking", "stereo", "deraining", "low-light", "motion prior"],
            "why": (
                "WNOJ-LIO, sparse-view CT uncertainty, point-cloud clutter tracking, stereo matching, event deraining은 "
                "모두 보기 좋은 reconstruction보다 downstream state를 얼마나 믿을 수 있는지 묻습니다. "
                "3D/SLAM watch lens 관점에서는 map/rendering score보다 pose distortion, uncertainty calibration, "
                "tracking continuity가 더 직접적인 실험 축입니다."
            ),
            "confidence": "Medium-High",
            "confidence_note": "LIO, uncertainty, stereo, adverse-weather perception이 robot-usable reliability로 연결됩니다.",
            "lab_action": (
                "LiDAR-IMU, stereo, event/RGB adverse-weather stream에 동일 disturbance를 넣고 ATE, uncertainty ECE, "
                "tracking identity switch, downstream planner cost를 함께 산출합니다."
            ),
            "limit": 6,
        },
        {
            "title": "Human-facing robot deployment가 task skill에서 trust and coordination state로 이동",
            "buckets": ["Robot Learning", "Embodied AI", "Autonomous Driving", "Safety/Alignment"],
            "ids": ["2607.13056", "2607.13595", "2607.13497", "2607.13060", "2607.13653", "2607.13830"],
            "needles": ["human-robot", "trust", "collaboration", "patient", "humanoid", "landing", "deployable"],
            "why": (
                "HRIBench, active trust management, autonomous patient transport, humanoid uncanny-valley modeling은 "
                "robot deployment를 단순 task skill이 아니라 human constraint와 trust state를 포함한 system으로 봅니다. "
                "오늘의 human-facing 축은 policy success 뒤에 숨어 있는 coordination, safety recovery, acceptability를 "
                "명시적으로 계측하라는 신호입니다."
            ),
            "confidence": "Medium",
            "confidence_note": "HRI와 deployment 논문은 수가 적지만 APRL 실험 설계와 직접 연결됩니다.",
            "lab_action": (
                "협업/환자이송/landing task에서 human wait time, intervention timing, trust repair event, safety recovery를 "
                "policy success와 분리된 event taxonomy와 측정 항목으로 만듭니다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Semantic Retention Harness for VLA Fine-Tuning",
            "claim": "VLA checkpoint마다 semantic retrieval, language-action contradiction, OOD object relocation success를 함께 산출합니다.",
        },
        {
            "title": "Just-In-Time Robot State Protocol",
            "claim": "full scene graph, retrieved graph, just-in-time graph를 같은 task와 latency budget에서 비교합니다.",
        },
        {
            "title": "Simulator Validity Audit for Robot Learning",
            "claim": "GPU simulator와 driving world model이 policy ranking과 failure distribution을 바꾸는 조건을 찾습니다.",
        },
    ],
}


def abstract_card(paper: dict) -> dict:
    """Build a conservative Tier B/C card using only parser-provided abstract text."""
    abstract = " ".join(str(paper.get("abstract", "")).split())
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", abstract) if s.strip()]
    problem = sentences[0] if sentences else "Abstract에서 구체적인 문제 설명을 확인하지 못했습니다."
    method = next(
        (
            s
            for s in sentences[1:]
            if re.search(r"\b(we propose|we present|we introduce|we develop|our method|our framework|our approach)\b", s, re.I)
        ),
        sentences[1] if len(sentences) > 1 else problem,
    )
    meaning = next(
        (
            s
            for s in reversed(sentences)
            if s not in {problem, method}
            and re.search(r"\b(experiment|result|demonstrat|outperform|achiev|show|improv|validate)\w*\b", s, re.I)
        ),
        sentences[-1] if sentences else problem,
    )
    phy = phylogeny_for(paper["bucket"], paper)
    return {
        "arxiv_id": paper["arxiv_id"],
        "title": paper["title"],
        "bucket": paper["bucket"],
        "badge": paper.get("badge", ""),
        "reading_depth": "abstract-only",
        "problem": problem,
        "method": method,
        "meaning": meaning,
        "phylogeny": phy,
    }


def enrich_insights() -> None:
    """Attach prompt-v20260713 research-intelligence and exhaustive tier data."""
    root = Path(__file__).resolve().parents[1]
    insights_path = root / "insights" / f"{DATE}.json"
    trends = json.loads((root / "trends" / f"{DATE}.json").read_text(encoding="utf-8"))
    insights = json.loads(insights_path.read_text(encoding="utf-8"))
    classified = json.loads((root / "out" / "classified.json").read_text(encoding="utf-8"))

    insights["source_listing_date"] = trends["source_listing_date"]
    insights["source_mode"] = trends["source_mode"]
    insights["daily_new_counts"] = trends["daily_new_counts"]
    for cluster in insights["clusters"]:
        cluster["representative_papers"] = [p["arxiv"] for p in cluster["papers"]]
        cluster["why_it_matters"] = cluster["why"]
        cluster["confidence_rationale"] = cluster["confidence_note"]

    insights["paper_autopsies"] = [
        {
            "arxiv_id": paper["arxiv_id"],
            "title": paper["title"],
            "reading_depth": "full-text",
            "status_quo_belief": paper["status_quo"],
            "friction": paper["friction"],
            "hidden_premise": paper["hidden_premise"],
            "conceptual_move": paper["conceptual_move"],
            "mechanism": paper["mechanism"],
            "decisive_evidence": paper["evidence"],
            "falsification_frontier": paper["falsification"],
            "adversarial_read": paper["adversarial"],
            "transferable_thinking_tool": paper["thinking_tool"],
            "transfer_boundary": paper["transfer_boundary"],
        }
        for paper in RI_DATA["papers"]
    ]
    insights["cross_paper_decisions"] = RI_DATA["synthesis"]

    insights["frontier_memory"] = {
        "new": [item for item in RI_DATA["frontier_memory"] if item["signal"] == "새로운 통합"],
        "strengthening": [item for item in RI_DATA["frontier_memory"] if item["signal"] == "강화 중"],
        "commoditizing": [],
        "contradiction": [],
        "missing_axis": [item for item in RI_DATA["frontier_memory"] if item["signal"] == "비어 있음"],
    }
    portfolio = {"BUILD": "Build moat", "EXPLOIT": "Exploit", "EXPLORE": "Explore"}
    insights["strategy_board"] = [
        {
            "opportunity": item["title"],
            "portfolio": portfolio[item["priority"]],
            "thesis": item["thesis"],
            "scores": {
                "strategic_fit": item["scores"]["fit"],
                "asymmetry": item["scores"]["novelty"],
                "timing": item["scores"]["timing"],
                "tractability": item["scores"]["feasibility"],
                "defensibility": item["scores"]["moat"],
                "scientific_depth": item["scores"]["evidence"],
            },
            "one_week_probe": item["one_week"],
            "four_week_build": item["four_week"],
            "success_metric": item["metric"],
            "stop_condition": item["stop"],
            "paper_path": [a["url"] for a in item["assets"] if "arxiv.org" in a["url"]],
            "asset_path": [a["url"] for a in item["assets"] if "arxiv.org" not in a["url"]],
        }
        for item in RI_DATA["strategy"]
    ]

    all_papers = [p for bucket in classified["buckets"].values() for p in bucket["papers"]]
    tier_a_ids = {paper["arxiv_id"] for paper in RI_DATA["papers"]}
    tier_b_ids = {
        "2607.13605", "2607.13361", "2607.13653", "2607.13072",
        "2607.13410", "2607.13481", "2607.13305", "2607.13527",
        "2607.13405", "2607.13682", "2607.13595", "2607.13497",
    }
    insights["tier_b"] = [abstract_card(p) for p in all_papers if p["arxiv_id"] in tier_b_ids]
    insights["tier_c"] = [abstract_card(p) for p in all_papers if p["arxiv_id"] not in tier_a_ids | tier_b_ids]
    insights["tiering_note"] = (
        "Tier A 6편은 official arXiv full text 기반입니다. Tier B 12편과 Tier C 나머지는 parser-provided abstract만 "
        "사용했으며 problem/method/meaning 문장은 abstract 문장에서 보수적으로 추출했습니다."
    )
    insights["research_intelligence"] = {
        "html": f"posts/{DATE}-research-intelligence.html",
        "json": f"intelligence/{DATE}.json",
        "source_prompt": RI_DATA["source_prompt"],
    }
    insights_path.write_text(json.dumps(insights, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build(PROFILE, "out/cv_new.json", "out/ro_new.json")
    enrich_insights()

    post_path = Path(__file__).resolve().parents[1] / "posts" / f"{DATE}.html"
    doc = post_path.read_text(encoding="utf-8")
    doc = doc.replace(
        ".thesis strong{color:#fef08a}",
        ".thesis strong{color:#fef08a}.ri-callout{display:flex;justify-content:space-between;gap:16px;align-items:center;margin:-12px 0 28px;padding:14px 18px;border:1px solid #67e8f9;border-radius:10px;background:#ecfeff;color:#164e63}.ri-callout a{font-weight:750;white-space:nowrap}@media(max-width:760px){.ri-callout{align-items:flex-start;flex-direction:column}}",
    )
    ri_callout = (
        f"<section class=\"ri-callout\"><span><strong>오늘의 리서치 인텔리전스</strong> "
        f"Tier A 6편의 주장, 증거, 숨은 전제, 반증 조건을 원문 기준으로 대조했습니다.</span>"
        f"<a href=\"{DATE}-research-intelligence.html\">Research Intelligence 열기</a></section>"
    )
    doc = re.sub(r"</section>\n(<h2>.*?</h2>)", f"</section>\n{ri_callout}\n\\1", doc, count=1, flags=re.S)
    post_path.write_text(doc, encoding="utf-8")
