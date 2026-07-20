#!/usr/bin/env python3
"""Generate the 2026-07-20 daily briefing from matching arXiv /new listings."""
from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, phylogeny_for, week_start
from gen_research_intelligence_20260720 import DATA as RI_DATA


DATE = "2026-07-20"

PROFILE = {
    "date": DATE,
    "weekday": "Mon",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from the matching 2026-07-20 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-07-20 arXiv /new listings. "
        "Tier A claims are checked against official arXiv full text in the Research Intelligence edition."
    ),
    "thesis": (
        "7월 20일 배치의 핵심은 로봇 foundation model을 크게 만들거나 3D representation을 빠르게 만드는 것만으로 "
        "실행 가능성이 보장되지 않는다는 점입니다. Xiaomi-Robotics-1은 100k 시간 real-world trajectory scale이 "
        "post-training 성능까지 이어질 수 있음을 보여주지만, AC-VLA와 IMBench는 familiar skill을 낯선 조합으로 "
        "다시 쓰는 순간 trajectory overfitting, wrist-view shortcut, reasoning-to-execution gap이 별도 실패로 나타난다고 "
        "말합니다. Think-at-5Hz/Act-at-20Hz와 Orbis 2는 driving stack에서 slow reasoning과 fast action, abstract dynamics와 "
        "detail rollout을 분리해야 함을 보이고, ImprovedVBGS와 VTLoc은 online geometry와 tactile contact를 실제 robot state로 "
        "쓰려면 latency, ambiguity, downstream recovery까지 함께 재야 한다는 신호를 줍니다."
    ),
    "cluster_takeaway": (
        "오늘의 핵심은 scale이나 fidelity가 아니라, scale이 만든 policy와 map state가 OOD composition, control freshness, "
        "contact ambiguity, online update 조건에서 실제 실패를 줄이는지 분리해 검증하는 것입니다."
    ),
    "trend_note": (
        "Foundation Models와 Robot Learning이 가장 두껍고 Efficiency/Systems, Safety/Alignment, 3D/Scene도 두드러졌지만, "
        "robotics 관점의 공통 축은 VLA composition, fast-slow control, world-model hierarchy, online geometry update, "
        "visual-tactile state alignment입니다. 이는 최근 4주간 반복된 action-facing interface, robot-usable geometry, "
        "closed-loop failure diagnosis 흐름이 더 구체적인 benchmark 계약으로 내려온 신호입니다."
    ),
    "cluster_specs": [
        {
            "title": "VLA scale이 average success에서 composition OOD 진단으로 이동",
            "buckets": ["Robot Learning", "Foundation Models", "3D/Scene"],
            "ids": ["2607.15330", "2607.15714", "2607.15641", "2607.15890", "2607.16193"],
            "needles": [
                "vla",
                "vision-language-action",
                "compositional",
                "intuitive manipulation",
                "out-of-distribution",
                "reasoning",
            ],
            "why": (
                "Xiaomi-Robotics-1은 data/model scale이 unseen-environment success를 올릴 수 있음을 보여주지만, "
                "AC-VLA는 familiar sub-task를 새 target으로 재조합하는 순간 trajectory overfitting과 wrist-view shortcut이 "
                "별도 병목으로 드러난다고 봅니다. IMBench와 UAV-DualCog까지 합치면, 오늘의 VLA/embodied benchmark 축은 "
                "평균 성공률보다 physical reasoning, sub-skill composition, self/environment state가 execution으로 이어지는지 묻는 방향입니다."
            ),
            "confidence": "High",
            "confidence_note": "large VLA, compositional VLA, intuitive manipulation, UAV reasoning benchmark가 같은 execution-diagnosis 축을 형성합니다.",
            "lab_action": (
                "LIBERO/RoboCasa와 IMBench-style tasks에서 ID success, object-target recombination, wrist-view masking, reasoning-to-action "
                "plan validity를 같은 policy checkpoint에 적용하고 OOD success, stage-boundary error, instruction-action contradiction을 비교합니다."
            ),
            "limit": 5,
        },
        {
            "title": "Contact-rich manipulation이 tactile data collection에서 3D contact-state alignment로 이동",
            "buckets": ["Robot Learning", "3D/Scene"],
            "ids": ["2607.16146", "2607.15448", "2607.15633", "2607.15641", "2607.15890", "2607.15395"],
            "needles": ["tactile", "contact", "visuo-tactile", "gripper", "force", "in-hand", "manipulation"],
            "why": (
                "VTLoc은 tactile image를 3D point cloud의 contact probability로 정렬하고, VTAP Gripper와 6-axis visuotactile sensor "
                "논문은 contact-rich manipulation에서 vision-only state가 충분하지 않다는 신호를 줍니다. 이 묶음은 tactile sensor를 "
                "단순 추가 modality가 아니라 contact ambiguity와 recovery action을 연결하는 state-estimation layer로 읽어야 한다는 뜻입니다."
            ),
            "confidence": "High",
            "confidence_note": "visual-tactile localization, active palm gripper, wrench estimation, manipulation benchmark가 같은 contact-state 축으로 반복됩니다.",
            "lab_action": (
                "peg-in-hole, folding, in-hand reorientation에서 tactile contact probability, force wrench estimate, vision-only pose를 "
                "독립 ablation 축으로 두고 contact entropy, failure-warning lead time, recovery success, unseen-object drop을 평가합니다."
            ),
            "limit": 6,
        },
        {
            "title": "Driving autonomy가 single forward pass에서 fast-slow state contract로 이동",
            "buckets": ["Autonomous Driving", "Generation"],
            "ids": ["2607.15621", "2607.15898", "2607.15969", "2607.15508", "2607.15863", "2607.15491", "2607.16181"],
            "needles": ["driving", "trajectory", "planning", "world model", "fast-slow", "localization", "risk"],
            "why": (
                "Think-at-5Hz/Act-at-20Hz는 slow VLA cache와 fast action expert를 나누고, Orbis 2는 abstract 2Hz world model과 "
                "detail 10Hz generator를 나눕니다. trajectory prediction, kinodynamic planning, cross-view geo-localization까지 합치면 "
                "driving stack의 핵심은 한 모델의 score가 아니라 cache age, action freshness, steering response, route failure가 어떻게 연결되는지입니다."
            ),
            "confidence": "High",
            "confidence_note": "closed-loop VLA driving, hierarchical world model, trajectory/planning/localization 논문이 같은 state-contract 축에 놓입니다.",
            "lab_action": (
                "CARLA/nuPlan-style routes에서 synchronous small model, stale replay, cached fast expert, hierarchical world model prior를 "
                "같은 route set에 두고 p95 latency, cache age, route completion, red-light/collision recovery를 함께 비교합니다."
            ),
            "limit": 7,
        },
        {
            "title": "3D reconstruction과 SLAM이 visual fidelity에서 online map update 계약으로 이동",
            "buckets": ["3D/Scene", "Efficiency/Systems", "Autonomous Driving"],
            "ids": ["2607.15542", "2607.15652", "2607.15727", "2607.16143", "2607.15536", "2607.16128", "2607.15889"],
            "needles": [
                "gaussian",
                "bundle adjustment",
                "reconstruction",
                "slam",
                "lidar",
                "real-time",
                "continual",
                "mobile 3d",
            ],
            "why": (
                "ImprovedVBGS는 continual Gaussian update latency를 robot navigation 요구로 끌어오고, CSS-BA는 weak geometry bundle adjustment의 "
                "stability를, Event3R은 asynchronous event stream의 global reconstruction을, NeoSLAM은 real-time throughput을 각각 묻습니다. "
                "따라서 3D/SLAM 평가는 rendering score보다 pose robustness, update cost, weak-parallax failure, downstream navigation success를 봐야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "3DGS, BA, event reconstruction, NeoSLAM, mobile 3D reconstruction 신호가 10편 이상에서 반복됩니다.",
            "lab_action": (
                "3DGS map, bundle-adjusted point map, event-based reconstruction, NeoSLAM map을 같은 weak-parallax/dynamic-object trajectory에 적용하고 "
                "ATE, update latency, memory footprint, relocalization success, downstream navigation cost를 비교합니다."
            ),
            "limit": 7,
        },
        {
            "title": "Embodied perception이 passive dataset selection에서 budgeted active world repair로 이동",
            "buckets": ["Embodied AI", "3D/Scene", "Robot Learning", "Foundation Models"],
            "ids": ["2607.15974", "2607.15828", "2607.16189", "2607.15642", "2607.15674"],
            "needles": ["active learning", "exploration", "navigation", "self-state", "world", "video", "object-goal"],
            "why": (
                "Embodied Active Learning은 robot navigation budget과 annotation budget을 동시에 묻고, SCAGE는 coverage frontier가 아니라 scene anomaly를 "
                "줄이는 exploration을 제안합니다. UAV-DualCog와 grounded long-video QA까지 합치면, embodied perception은 더 많은 frame을 보는 문제가 아니라 "
                "어떤 uncertainty를 이동·관측·라벨링 budget으로 고칠지 결정하는 문제로 바뀝니다."
            ),
            "confidence": "Medium-High",
            "confidence_note": "active learning, autonomous exploration, UAV dual cognition, grounded video QA가 같은 budgeted repair 축으로 연결됩니다.",
            "lab_action": (
                "AI2-THOR/Spot-style active detection과 unknown-scene exploration에서 coverage policy, anomaly policy, spatial-inconsistency policy를 "
                "같은 navigation/annotation budget으로 비교하고 mAP gain, reconstruction hole reduction, unnecessary travel, failed-query recovery를 평가합니다."
            ),
            "limit": 6,
        },
        {
            "title": "Efficient perception이 token 절감에서 task-relevant evidence 보존성 평가로 이동",
            "buckets": ["Efficiency/Systems", "Foundation Models", "Generation", "3D/Scene"],
            "ids": ["2607.15563", "2607.15689", "2607.16192", "2607.15650", "2607.16190", "2607.16012", "2607.15732"],
            "needles": ["token", "efficient", "frame selection", "scene-flow", "attention", "parallel", "sparse", "distillation"],
            "why": (
                "visual place recognition token reduction, long-video frame selection, MotionForesight, diffusion attention reuse는 모두 computation을 줄이지만 "
                "질문은 latency 자체가 아니라 어떤 spatial/temporal evidence가 보존되는지입니다. robot deployment에서는 token/frame을 줄인 뒤에도 place recognition, "
                "future scene-flow, dense prediction, video generation control에 필요한 evidence가 남아 있는지 봐야 합니다."
            ),
            "confidence": "Medium",
            "confidence_note": "VPR token reduction, MLLM frame selection, scene-flow prediction, sparse attention 논문이 연결되지만 공통 robot benchmark는 아직 약합니다.",
            "lab_action": (
                "VPR, long-video QA, future scene-flow task에서 token reduction, frame selector, sparse attention, distillation 조건을 같은 latency budget에 두고 "
                "localization recall, query evidence coverage, motion endpoint error, downstream action delta를 비교합니다."
            ),
            "limit": 7,
        },
    ],
    "research_topics": [
        {
            "title": "Composition-OOD VLA stress harness",
            "claim": "ID success와 object-target recombination, wrist-view shortcut, low-data adaptation을 같은 VLA checkpoint에서 함께 평가합니다.",
        },
        {
            "title": "Fast-slow control freshness audit",
            "claim": "slow backbone cache, fast action expert, hierarchical world model prior가 route completion과 safety recovery를 어떻게 바꾸는지 분리합니다.",
        },
        {
            "title": "Robot-usable geometry/contact state protocol",
            "claim": "online Gaussian map update와 tactile contact probability가 downstream localization, insertion, recovery에 미치는 영향을 계측합니다.",
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
            and re.search(r"\b(experiment|result|demonstrat|outperform|achiev|show|improv|validate|evaluate)\w*\b", s, re.I)
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
        "new": [item for item in RI_DATA["frontier_memory"] if item["signal"] in {"새로운 통합", "새로운 경고"}],
        "strengthening": [item for item in RI_DATA["frontier_memory"] if item["signal"] == "강화 중"],
        "commoditizing": [],
        "contradiction": [],
        "missing_axis": [item for item in RI_DATA["frontier_memory"] if item["signal"] in {"비어 있음", "새로운 공백"}],
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
        "2607.15641", "2607.15890", "2607.15448", "2607.15633", "2607.15652", "2607.15727",
        "2607.16143", "2607.15828", "2607.15974", "2607.16193", "2607.15689", "2607.16192",
        "2607.15563", "2607.15969", "2607.15508", "2607.15642", "2607.16189", "2607.16012",
    }
    insights["tier_b"] = [abstract_card(p) for p in all_papers if p["arxiv_id"] in tier_b_ids]
    insights["tier_c"] = [abstract_card(p) for p in all_papers if p["arxiv_id"] not in tier_a_ids | tier_b_ids]
    insights["tiering_note"] = (
        "Tier A 6편은 official arXiv full text 기반입니다. Tier B와 Tier C는 parser-provided abstract만 사용했으며 "
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
    ri_callout = (
        f"<section class=\"ri-callout\"><span><strong>오늘의 리서치 인텔리전스</strong> "
        f"Tier A 6편의 주장, 증거, 숨은 전제, 반증 조건을 원문 기준으로 대조했습니다.</span>"
        f"<a href=\"{DATE}-research-intelligence.html\">Research Intelligence 열기</a></section>"
    )
    doc = re.sub(r"</section>\n(<h2>.*?</h2>)", f"</section>\n{ri_callout}\n\\1", doc, count=1, flags=re.S)
    post_path.write_text(doc, encoding="utf-8")
