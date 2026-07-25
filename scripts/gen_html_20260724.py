#!/usr/bin/env python3
"""Generate the 2026-07-24 daily briefing from matching arXiv /new listings."""
from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, phylogeny_for, week_start
from gen_research_intelligence_20260724 import DATA as RI_DATA


DATE = "2026-07-24"

PROFILE = {
    "date": DATE,
    "weekday": "Fri",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from the matching 2026-07-24 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-07-24 arXiv /new listings. "
        "Tier A claims are checked against official arXiv full text in the Research Intelligence edition."
    ),
    "thesis": (
        "7월 24일 배치의 핵심은 로봇 foundation model과 geometry 연구가 모델 용량 경쟁에서 검증 가능한 실행 계약으로 이동했다는 점입니다. "
        "HyWorldVLA, PhysCoRe, GS-Agent는 generated future를 action, material dynamics, physical world state가 소비할 수 있는 형태로 바꾸려 합니다. "
        "Scale Up Strategically, AXIS, TableVerse, TransBiolab은 robot data scaling을 demo volume이 아니라 bias factor, growable snapshot, transparent-object coverage의 문제로 재정의합니다. "
        "GLAM-SLAM, HGeo-TopoMap, DTIF, VoLN, Geo3R은 mapping, navigation, spatial reasoning에서 map/state/geometry evidence가 downstream failure를 어떻게 막는지 묻습니다. "
        "FORGE-plus와 GuidedAttention은 LLM/VLA가 action을 직접 지배하는 대신 force budget, attention correction, recovery decision처럼 좁은 authority boundary로 들어갈 때 더 검증 가능하다는 신호를 줍니다."
    ),
    "cluster_takeaway": (
        "오늘의 핵심은 더 큰 VLA나 더 그럴듯한 3D scene이 아니라, world state, data factor, force budget, map topology, spatial evidence가 실제 robot task에서 깨지는 조건을 얼마나 잘 드러내는가입니다."
    ),
    "trend_note": (
        "Generation 23편, Safety/Alignment 19편, 3D/Scene과 Robot Learning이 각각 16편으로 크지만, robotics 관점의 공통 축은 bucket 크기가 아니라 "
        "hybrid world-state contract, bias-aware data scaling, robot-usable geometry, bounded supervision입니다."
    ),
    "cluster_specs": [
        {
            "title": "World-action model 평가가 future image에서 hybrid state contract로 이동",
            "buckets": ["Robot Learning", "Generation", "Autonomous Driving", "3D/Scene"],
            "ids": ["2607.20988", "2607.20653", "2607.21522", "2607.20889", "2607.21471", "2607.20549"],
            "needles": ["world model", "world modeling", "physical world", "hybrid", "future", "trajectory", "dynamics", "simulation"],
            "why": (
                "기존 world model 평가는 generated frame이 얼마나 그럴듯한지에 끌려가기 쉬웠지만, 로봇은 future image보다 action이 소비할 수 있는 state contract를 필요로 합니다. "
                "HyWorldVLA는 pixel supervision과 latent prediction을 나누어 NAVSIM trajectory robustness를 보고, PhysCoRe와 GS-Agent는 material-aware dynamics와 generative simulation을 physical state로 묻습니다. "
                "따라서 APRL 평가는 frame score를 넘어서 generated state가 pose, material response, route feasibility, next action stability를 얼마나 설명하는지 비교해야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "driving VLA, deformable dynamics, generative simulation, dynamic reconstruction papers가 같은 state-contract 축으로 모입니다.",
            "lab_action": (
                "RoboCasa/ManiSkill와 driving mini-trace에서 generated frame, latent state, object displacement, material response, planned trajectory를 독립 변수로 두고 "
                "execution success, contact violation, route deviation, imagined-success false positive를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Manipulation scaling이 demo volume에서 factor bias와 growable data engine으로 이동",
            "buckets": ["Robot Learning"],
            "ids": ["2607.21582", "2607.21588", "2607.21017", "2607.21071", "2607.21049", "2607.20771"],
            "needles": ["bias", "data", "dataset", "compositional", "generalization", "tabletop", "transparent", "attention", "vla"],
            "why": (
                "robot manipulation에서 데이터를 더 모으는 것만으로는 policy가 언어를 이해했는지 shortcut factor를 썼는지 구분할 수 없습니다. "
                "Scale Up Strategically는 Factor Dominance Rate/Hierarchy로 shortcut을 드러내고, AXIS는 task generation, teleoperation, augmentation, validation을 growable data engine으로 묶습니다. "
                "TableVerse와 TransBiolab은 grounded layouts와 transparent biomedical objects처럼 data coverage가 평가축 자체가 되는 영역을 보여줍니다."
            ),
            "confidence": "High",
            "confidence_note": "bias diagnosis, growable dataset, transparent/cluttered object coverage, correctable attention이 모두 data-scaling contract를 직접 다룹니다.",
            "lab_action": (
                "verb/object/color/material/visibility factor를 바꾼 tabletop split을 만들고 random collection, bias-aware collection, AXIS-style snapshot growth를 비교해 "
                "OOD success, factor dominance reduction, valid rollout cost, attention-correction recovery를 평가한다."
            ),
            "limit": 6,
        },
        {
            "title": "VLA execution structure가 monolithic action head에서 expert routing과 bounded recovery로 이동",
            "buckets": ["Robot Learning"],
            "ids": ["2607.20771", "2607.21227", "2607.20912", "2607.21049", "2607.20683", "2607.21341"],
            "needles": ["mixture-of-experts", "recovery", "force", "contact", "attention", "tactile", "unified robot", "bimanual"],
            "why": (
                "VLA가 한 덩어리 policy로 성공률만 내는 단계에서는 failure가 어느 module에서 시작되는지 보이지 않습니다. "
                "MoE VLA는 action expert routing이 reusable primitive처럼 나타날 수 있음을 보이고, FORGE-plus는 frozen LLM을 force ceiling과 recovery menu로 제한합니다. "
                "URF, GuidedAttention, FELT, bimanual diffusion papers까지 보면 실행 구조의 핵심은 더 큰 decoder가 아니라 expert, force, tactile, attention boundary를 분리해 검증하는 것입니다."
            ),
            "confidence": "High",
            "confidence_note": "expert routing, force-bounded recovery, correctable attention, tactile signal, bimanual composition이 같은 execution-structure 축을 형성합니다.",
            "lab_action": (
                "LIBERO/tabletop assembly에서 monolithic VLA, MoE action head, force-budget wrapper, attention-correction wrapper를 비교하고 "
                "phase-level expert reuse, peak force violation, recovery success, instruction-action contradiction을 함께 평가한다."
            ),
            "limit": 6,
        },
        {
            "title": "Robot-usable geometry가 rendering 품질에서 map topology와 large-scale tracking contract로 이동",
            "buckets": ["3D/Scene", "Autonomous Driving", "Embodied AI"],
            "ids": ["2607.21416", "2607.21281", "2607.21138", "2607.21438", "2607.20748", "2607.21023"],
            "needles": ["slam", "mapping", "topological", "loop closure", "depth", "rgb-d", "pose", "reconstruction", "gaussian"],
            "why": (
                "3D/Scene 버킷은 16편이지만 상단 신호는 rendering quality가 아니라 map/state가 robot task에 남는 방식입니다. "
                "GLAM-SLAM은 ORB-SLAM2 tracking과 Gaussian mapping을 decoupled real-time system으로 묶고, HGeo-TopoMap은 BEV instance geometry와 relation topology를 driving map prior로 학습합니다. "
                "DTIF, DAPM, RGB-D mining pipeline, WAT3R까지 포함하면 geometry gate는 relocalization, depth robustness, large-scale map update, downstream pose generation을 검증해야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "SLAM, topological mapping, loop closure, UAV depth, RGB-D pose generation, underwater reconstruction signals가 2편 이상 조건을 충분히 넘습니다.",
            "lab_action": (
                "same navigation/mining/UAV traces에서 sparse SLAM, Gaussian map, BEV topology, monocular depth를 비교하고 "
                "metric drift, relocalization success, topology error, pose-generation success, downstream route recovery를 측정한다."
            ),
            "limit": 6,
        },
        {
            "title": "MLLM reliability가 answer accuracy에서 spatial evidence와 hallucination span diagnosis로 이동",
            "buckets": ["Foundation Models", "Safety/Alignment", "Efficiency/Systems"],
            "ids": ["2607.21085", "2607.21105", "2607.20868", "2607.21155", "2607.21072", "2607.21036", "2607.21401"],
            "needles": ["hallucination", "spatial", "reasoning", "diagnosis", "visual cues", "guard", "adversarial", "benchmark"],
            "why": (
                "vision-language model reliability는 final answer가 맞았는지보다 어떤 visual evidence와 spatial relation을 근거로 삼았는지까지 봐야 합니다. "
                "Geo3R은 geometry cards로 relation hallucination을 줄이고, HalluScope는 hallucinated span과 type을 fine-grained diagnosis로 바꿉니다. "
                "ViSTR-Bench, CRAG-MM-Diagnostics, Show-Don't-Tell, GeoThreat, ResponseGuard는 dynamic visual cues, staged VQA analysis, pixel-space cognition, targeted attack, real-time moderation을 같은 evidence-contract 문제로 밀어 올립니다."
            ),
            "confidence": "High",
            "confidence_note": "spatial hallucination, span diagnosis, dynamic cue reasoning, guardrail efficiency가 서로 다른 benchmark에서 반복됩니다.",
            "lab_action": (
                "robot VLM agent episode에 geometry card, visual-cue timeline, hallucinated-span label, guardrail latency를 붙이고 "
                "phantom object grounding, wrong spatial relation, right-answer wrong-evidence, unsafe moderation miss를 failure family별로 평가한다."
            ),
            "limit": 7,
        },
        {
            "title": "Navigation and autonomy benchmark가 route success에서 capability, body, and conflict constraints로 이동",
            "buckets": ["Embodied AI", "Robot Learning", "Autonomous Driving", "Safety/Alignment"],
            "ids": ["2607.21400", "2607.21025", "2607.20785", "2607.20679", "2607.20772", "2607.20665", "2607.20505"],
            "needles": ["navigation", "traversability", "object navigation", "multi-robot", "drone", "payload", "traffic conflict", "capability"],
            "why": (
                "navigation benchmark가 SR/SPL만 보면 실제 deployment에서 capability, body geometry, social conflict, payload constraint가 어떻게 실패로 이어지는지 놓칩니다. "
                "VoLN은 visual-goal navigation에서 policy input contract를 좁히고, capability-aware traversability와 ZONDA는 robot capability and dynamic avoidance를 봅니다. "
                "multi-robot navigation, drone payload CBF-RL, traffic conflict prediction까지 묶으면 autonomy 평가는 route success가 아니라 constraint violation과 recovery margin을 함께 봐야 합니다."
            ),
            "confidence": "Medium-High",
            "confidence_note": "navigation, traversability, social/multi-robot, drone payload, traffic conflict papers가 constraint-aware autonomy로 연결됩니다.",
            "lab_action": (
                "indoor/outdoor route와 intersection scenarios에서 visual-goal policy, capability-aware planner, CBF safety wrapper, conflict predictor를 비교하고 "
                "clearance violation, payload slack, social conflict, false stop, recovery latency를 평가한다."
            ),
            "limit": 7,
        },
    ],
    "research_topics": [
        {
            "title": "Hybrid world-state contract harness",
            "claim": (
                "generated future를 image score가 아니라 latent state, pose, material response, trajectory feasibility, failure family로 바꿔 real/sim execution success와 비교한다."
            ),
        },
        {
            "title": "Bias-aware robot data growth protocol",
            "claim": (
                "verb/object/color/material/visibility factor dominance를 먼저 측정하고, 그 dominance를 깨는 targeted demonstrations and task snapshots를 설계한다."
            ),
        },
        {
            "title": "Gaussian-topology map validity split",
            "claim": (
                "3DGS map, sparse SLAM, BEV topology, monocular depth를 같은 route에서 비교해 relocalization, topology error, downstream recovery를 평가한다."
            ),
        },
        {
            "title": "Bounded supervisor for force and geometry",
            "claim": (
                "LLM/MLLM을 free-form planner가 아니라 force ceiling, geometry card, recovery menu로 제한하고 safety gain과 success drop을 함께 검증한다."
            ),
        },
    ],
}


def abstract_card(paper: dict) -> dict:
    abstract = " ".join(str(paper.get("abstract", "")).split())
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", abstract) if s.strip()]
    problem = sentences[0] if sentences else "Abstract did not expose a clear problem statement."
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
        "new": [item for item in RI_DATA["frontier_memory"] if item["signal"] == "new"],
        "strengthening": [item for item in RI_DATA["frontier_memory"] if item["signal"] == "strengthening"],
        "commoditizing": [],
        "contradiction": [],
        "missing_axis": [item for item in RI_DATA["frontier_memory"] if item["signal"] == "missing_axis"],
    }
    portfolio = {"BUILD": "Build moat", "EXPLOIT": "Exploit", "EXPLORE": "Explore"}
    strategy_board = []
    for item in RI_DATA["strategy"]:
        paper_path = [a["url"] for a in item["assets"] if "arxiv.org" in a["url"]]
        asset_path = [a["url"] for a in item["assets"] if "arxiv.org" not in a["url"]]
        if not asset_path:
            asset_path = [f"APRL internal asset: {item['title']} protocol"]
        strategy_board.append({
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
            "paper_path": paper_path,
            "asset_path": asset_path,
        })
    insights["strategy_board"] = strategy_board

    all_papers = [p for bucket in classified["buckets"].values() for p in bucket["papers"]]
    tier_a_ids = {paper["arxiv_id"] for paper in RI_DATA["papers"]}
    tier_b_ids = {
        "2607.20771", "2607.20653", "2607.21522", "2607.21017", "2607.21071",
        "2607.21049", "2607.20912", "2607.20683", "2607.21341", "2607.21138",
        "2607.21438", "2607.20748", "2607.21023", "2607.21105", "2607.20868",
        "2607.21155", "2607.21072", "2607.21401", "2607.21025", "2607.20785",
        "2607.20679", "2607.20772", "2607.20665", "2607.20505",
    }
    non_tier_a_or_b = tier_a_ids | tier_b_ids
    insights["tier_b"] = [abstract_card(p) for p in all_papers if p["arxiv_id"] in tier_b_ids]
    insights["tier_c"] = [abstract_card(p) for p in all_papers if p["arxiv_id"] not in non_tier_a_or_b]
    insights["tiering_note"] = (
        "Tier A 8 papers use official arXiv full text. Tier B and Tier C are conservative abstract-only cards "
        "built from repository parser text and should not be read as full-text claims."
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
        f"<section class=\"ri-callout\"><span><strong>오늘의 Research Intelligence</strong> "
        f"Tier A 8 papers are checked against official arXiv full text, with evidence traces, "
        f"adversarial reads, frontier memory, and APRL strategy board.</span>"
        f"<a href=\"{DATE}-research-intelligence.html\">Open Research Intelligence</a></section>"
    )
    doc = re.sub(r"</section>\n(<h2>.*?</h2>)", f"</section>\n{ri_callout}\n\\1", doc, count=1, flags=re.S)
    post_path.write_text(doc, encoding="utf-8")
