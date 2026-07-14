#!/usr/bin/env python3
"""Generate the 2026-07-14 daily briefing from matching arXiv /new listings."""
from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, phylogeny_for, week_start
from gen_research_intelligence_20260714 import DATA as RI_DATA


DATE = "2026-07-14"

PROFILE = {
    "date": DATE,
    "weekday": "Tue",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from the matching 2026-07-14 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-07-14 arXiv /new listings. "
        "Tier A claims are separately audited against full PDFs in the Research Intelligence edition."
    ),
    "thesis": (
        "7월 14일 배치의 가장 강한 신호는 모델 용량보다 인터페이스 구조가 성패를 가른다는 점입니다. "
        "object slot, robot-frame pointmap, 이동식 sensor, visibility gate, stop-to-decide cadence, evaluator contract가 "
        "각각 관측·행동·안전·평가 사이의 불일치를 먼저 제거합니다. APRL에는 backbone 경쟁보다 어떤 불변량을 "
        "어느 층에서 강제할지와 그 선택이 깨지는 경계를 실험으로 소유하는 것이 더 방어력 있는 연구선입니다."
    ),
    "cluster_takeaway": (
        "오늘의 판세는 더 큰 모델을 붙이는 것이 아니라 object, robot frame, visibility, loop rate, answer contract처럼 "
        "실제 task가 요구하는 좌표와 시간척도를 representation과 evaluation에 직접 넣는 쪽으로 이동했습니다."
    ),
    "trend_note": (
        "Robot Learning, Efficiency/Systems, Safety/Alignment가 두껍고 Foundation Models와 3D/Scene이 평가·기하 축을 받칩니다. "
        "공통된 전환은 capacity scaling에서 interface alignment, 그리고 평균 성능에서 failure-boundary 측정으로의 이동입니다."
    ),
    "cluster_specs": [
        {
            "title": "VLA 경쟁이 backbone 용량에서 object·robot-frame·image-space 정렬로 이동",
            "buckets": ["Robot Learning"],
            "ids": ["2607.09825", "2607.11498", "2607.10706", "2607.11167", "2607.09818"],
            "needles": ["object-centric", "pointmap", "action map", "image-space", "vision-language-action"],
            "why": (
                "More Structure, See like a Robot, AMP, Pix2Act는 같은 병목을 서로 다른 좌표 정렬 문제로 봅니다. "
                "task-irrelevant patch를 object slot으로 압축하고, camera 관측을 robot frame으로 옮기거나, 3D action을 image plane에 투영합니다. "
                "따라서 encoder 크기보다 observation-action 사이에 보존해야 할 불변량을 먼저 고정하고 capacity를 나중에 늘려야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "object structure, robot frame, image-space action이라는 독립적인 정렬 신호가 여러 manipulation 논문에서 반복됩니다.",
            "lab_action": (
                "동일 π0.5/BC backbone에서 RGB, dense patch, object slot, robot-frame pointmap, image-space action을 교차하고 "
                "viewpoint shift, occlusion, calibration noise별 success와 failure family를 비교합니다."
            ),
            "limit": 6,
        },
        {
            "title": "Active perception이 정보량 최대화에서 보이는 동안 안전하게 행동하는 문제로 이동",
            "buckets": ["Efficiency/Systems", "Robot Learning"],
            "ids": ["2607.09959", "2607.10682", "2607.10553", "2607.11822", "2607.10180"],
            "needles": ["limited sensing", "sensor", "viewpoint", "visibility", "active"],
            "why": (
                "SEAMLiS는 정보가 많은 yaw가 이동 방향의 위험을 가릴 수 있음을 보이고, SensorPerch는 task에 맞는 관측점을 물리적으로 재배치합니다. "
                "SLIDER와 VoNI는 모든 공간·noise regime을 계속 관측하지 않고 필요한 정보만 갱신합니다. "
                "active perception의 목적함수는 coverage가 아니라 task utility, braking margin, 재관측 비용을 함께 포함해야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "finite FoV, task-specific viewpoint, sparse history, diagnostic probing이 관측 비용과 안전을 공동 최적화합니다.",
            "lab_action": (
                "동일 탐색 task에서 FoV, sensor placement, speed, braking margin을 조작하고 coverage time만이 아니라 hidden-obstacle exposure, "
                "collision, viewpoint construction latency, Joule/success를 공동 측정합니다."
            ),
            "limit": 6,
        },
        {
            "title": "실시간 로봇 제어가 고정-rate 가정에서 latency-aware hybrid execution으로 이동",
            "buckets": ["Robot Learning", "Foundation Models", "Safety/Alignment"],
            "ids": ["2607.11204", "2607.10625", "2607.10991", "2607.09713", "2607.10288"],
            "needles": ["latency", "real-time", "slow", "fast", "closed-loop"],
            "why": (
                "Stop to Decide, DASL, HUMA, rule-aligned SLM control은 느린 reasoning과 빠른 reactive control을 같은 주기로 돌리는 설계를 거부합니다. "
                "특히 control-loop rate가 물리적 이동량 v/f와 결합하면 알고리즘 정확도가 같아도 안전 경계가 바뀝니다. "
                "배포 연구는 평균 latency를 부록 수치가 아니라 state transition과 failure probability를 결정하는 독립 변수로 다뤄야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "quadruped, social navigation, skill learning, industrial control에서 slow/fast 분리와 validator gating이 반복됩니다.",
            "lab_action": (
                "Jetson 공유부하를 재현해 loop rate, jitter, action speed를 factorial sweep하고 continuous, pause-and-decide, conditional-reasoning 정책의 "
                "success, overshoot, reaction deadline miss, throughput을 비교합니다."
            ),
            "limit": 6,
        },
        {
            "title": "평가가 단일 점수에서 evaluator contract와 실패 계통 분해로 이동",
            "buckets": ["Foundation Models", "Safety/Alignment", "Robot Learning"],
            "ids": ["2607.10240", "2607.10826", "2607.11570", "2607.09866", "2607.11312"],
            "needles": ["evaluation", "benchmark", "reliability", "error", "judge"],
            "why": (
                "Short-Answer VQA와 3D-DefectBench는 모델 점수가 evaluator, view protocol, prompt schema, label regime의 함수임을 드러냅니다. "
                "ERR@HRI와 Robo-ValueRL도 error anticipation과 value reliability를 downstream 성능과 분리해 측정합니다. "
                "평균 accuracy를 그대로 최적화하면 semantic failure 대신 contract survival이나 label noise를 학습할 수 있으므로 score 생성 과정을 audit해야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "answer contract, judge pipeline, naturalistic error, value reliability가 측정 장치 자체를 연구 대상으로 만듭니다.",
            "lab_action": (
                "공식 metric 옆에 semantic audit, answer/failure type, evaluator perturbation, closed-loop consequence를 병기하고 "
                "error pool에서 model failure와 evaluation failure를 분리하는 자동 taxonomy를 구축합니다."
            ),
            "limit": 6,
        },
        {
            "title": "3D geometry가 clean-slate 모델보다 metric calibration과 기존 stack 호환성을 겨냥",
            "buckets": ["3D/Scene", "Safety/Alignment"],
            "ids": ["2607.11099", "2607.11588", "2607.11184", "2607.10690", "2607.11686"],
            "needles": ["slam", "metric", "geometry", "visual odometry", "reconstruction"],
            "why": (
                "Desc++는 mature SLAM의 descriptor interface를 유지하고, FoundationGeo는 relative geometry를 pixel-wise metric field로 보정합니다. "
                "GeoGS-SLAM과 incremental Gaussian triangulation은 foundation prior와 online map을 결합합니다. "
                "새 representation의 전략 가치는 rendering 품질보다 calibration shift를 견디고 기존 localization·meshing·recovery stack에 얼마나 낮은 비용으로 들어가는지에서 갈립니다."
            ),
            "confidence": "High",
            "confidence_note": "drop-in descriptor, focal coverage, online Gaussian map, explicit mesh, camera-only recovery가 배포 호환성 축으로 연결됩니다.",
            "lab_action": (
                "동일 trajectory에서 foundation geometry, descriptor enhancement, Gaussian SLAM을 focal shift·illumination·dropout 아래 비교하고 "
                "ATE, relocalization, map freshness, downstream recovery success, 추가 latency를 한 표에 둡니다."
            ),
            "limit": 6,
        },
        {
            "title": "자율주행 robustness가 수동 long-tail replay에서 editable·adversarial closed-loop world로 이동",
            "buckets": ["Autonomous Driving", "Safety/Alignment", "Generation"],
            "ids": ["2607.10630", "2607.09764", "2607.09772", "2607.10336", "2607.10975"],
            "needles": ["adversarial", "driving", "closed-loop", "risk", "world"],
            "why": (
                "AWM은 planner의 world model을 role-conditioned adversary로 전환하고, OmniSCS와 risk-field digital twin은 scene을 편집·진화시키며 폐루프 검증합니다. "
                "PrismAD는 interaction, geometry, intent expert를 분리합니다. 희귀 시나리오를 더 모으는 대신 어떤 agent coalition과 risk factor가 planner를 깨는지 생성하고 "
                "nominal 성능을 보존한 채 hard-case recovery를 학습하는 경쟁으로 이동했습니다."
            ),
            "confidence": "Medium-High",
            "confidence_note": "adversarial self-play, editable world, risk field, semantic planner routing이 long-tail failure generation을 중심으로 모입니다.",
            "lab_action": (
                "nuPlan/InterPlan 또는 CARLA에서 agent coalition, appearance/trajectory edit, risk-field 강도를 조작하고 nominal regression, tail CVaR, collision, "
                "counterfactual transfer를 같은 closed-loop protocol로 측정합니다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Coordinate-Aligned VLA Matrix",
            "claim": "object slot × robot-frame pointmap × image-space action을 동일 backbone에서 교차해 viewpoint·occlusion·calibration failure의 원인을 분리합니다.",
        },
        {
            "title": "Visibility–Latency Safety Envelope",
            "claim": "FoV, speed, braking distance, loop rate, jitter를 하나의 물리적 safety surface로 묶고 pause/gate/reposition의 전환 조건을 학습합니다.",
        },
        {
            "title": "Evaluator Contract Lab",
            "claim": "공식 점수, semantic correctness, failure taxonomy, closed-loop consequence를 분리해 benchmark 개선과 model 개선을 혼동하지 않게 합니다.",
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
        "contradiction": [item for item in RI_DATA["frontier_memory"] if item["signal"] == "긴장 관계"],
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
        "2607.10706", "2607.11167", "2607.10553", "2607.11822",
        "2607.10625", "2607.10991", "2607.10826", "2607.11570",
        "2607.11099", "2607.11588", "2607.10630", "2607.09764",
    }
    insights["tier_b"] = [abstract_card(p) for p in all_papers if p["arxiv_id"] in tier_b_ids]
    insights["tier_c"] = [abstract_card(p) for p in all_papers if p["arxiv_id"] not in tier_a_ids | tier_b_ids]
    insights["tiering_note"] = (
        "Tier A 6편은 official full text 기반입니다. Tier B 12편과 Tier C 246편은 parser-provided abstract만 사용했으며, "
        "problem/method/meaning 문장은 abstract 문장에서 보수적으로 추출했습니다."
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
    thesis_end = "</section>\n<h2>오늘의 클러스터 지도</h2>"
    ri_callout = (
        "</section>\n<section class=\"ri-callout\"><span><strong>오늘의 심층판:</strong> Tier A 6편의 주장·증거·숨은 전제·반증 조건을 원문 표까지 대조했습니다.</span>"
        f"<a href=\"{DATE}-research-intelligence.html\">Research Intelligence 열기 →</a></section>\n<h2>오늘의 클러스터 지도</h2>"
    )
    doc = doc.replace(thesis_end, ri_callout, 1)
    post_path.write_text(doc, encoding="utf-8")
