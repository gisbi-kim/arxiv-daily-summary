#!/usr/bin/env python3
"""Generate the 2026-07-21 daily briefing from matching arXiv /new listings."""
from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, phylogeny_for, week_start
from gen_research_intelligence_20260721 import DATA as RI_DATA


DATE = "2026-07-21"

PROFILE = {
    "date": DATE,
    "weekday": "Tue",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from the matching 2026-07-21 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-07-21 arXiv /new listings. "
        "Tier A claims are checked against official arXiv full text in the Research Intelligence edition."
    ),
    "thesis": (
        "7월 21일 배치의 핵심은 robot foundation policy가 더 큰 backbone보다 실행 상태를 어떻게 유지하고 검증하는가로 "
        "경쟁축이 옮겨졌다는 점입니다. Foresight Residual RL은 subtask success가 같아도 다음 phase가 쓸 terminal state quality가 "
        "다르다고 보고, FM-VLA는 image memory 대신 force event history를 VLA action expert에 넣습니다. PhyAgentOS와 POT-VLA는 "
        "task completion을 model output이 아니라 session evidence, persistent 3D object token, predicate verifier로 확인합니다. "
        "SPARK-VLN과 GeoBoN은 slow reasoning이나 WAM rollout을 실행 전에 언제 믿을지 selective compute 문제로 바꾸며, "
        "DROID-ANCHOR와 LiDAR/SLAM 논문들은 visual geometry를 odometry-anchored metric state와 relocalization evidence로 좁힙니다."
    ),
    "cluster_takeaway": (
        "오늘의 핵심은 더 큰 VLA가 아니라, terminal-state foresight, physical memory, verifier evidence, selective compute, metric geometry를 "
        "실제 closed-loop failure 안에서 어떻게 분리해 검증할 것인가입니다."
    ),
    "trend_note": (
        "Robot Learning 42편, Generation 40편, Foundation Models 39편, Efficiency/Systems 35편, 3D/Scene 32편이 동시에 두꺼웠지만, "
        "robotics 관점의 공통 연구 결정은 model scale이 아니라 execution-state accounting입니다. 오늘은 contact-rich handoff, force memory, "
        "persistent object state, session verifier, slow-fast planning, WAM future verification, odometry-anchored geometry가 서로 다른 구현으로 같은 질문을 던집니다."
    ),
    "cluster_specs": [
        {
            "title": "Long-horizon VLA가 subtask success에서 handoff state quality 평가로 이동",
            "buckets": ["Robot Learning"],
            "ids": ["2607.16506", "2607.18231", "2607.17651", "2607.16921", "2607.17257", "2607.17876"],
            "needles": ["vla", "force", "foresight", "contact", "failure", "assembly", "manipulation", "residual"],
            "why": (
                "기존 VLA fine-tuning은 각 subtask의 성공률을 올리면 chain도 좋아질 것처럼 다뤘지만, Foresight Residual RL은 successful terminal state 중에서도 "
                "다음 phase를 망치는 상태가 있음을 보입니다. FM-VLA와 PREFAIL까지 합치면 contact-rich manipulation의 핵심은 현재 image가 아니라 force event, "
                "handoff quality, failure precursor가 다음 skill에 어떻게 전달되는지입니다. 따라서 APRL manipulation 평가는 task success만 보지 말고 "
                "phase-boundary state, contact memory, downstream recovery를 함께 봐야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "VLA residual RL, force-memory VLA, hierarchical contact guidance, failure precursor, latency-aware policy composition이 같은 handoff-state 축으로 반복됩니다.",
            "lab_action": (
                "LIBERO/RoboCasa와 contact assembly task에서 phase terminal image, force trace, object pose, next-phase success predictor를 독립 ablation 축으로 두고 "
                "full-task success, false-success, recovery time, contact-event recall을 비교합니다."
            ),
            "limit": 6,
        },
        {
            "title": "Embodied agent 연구가 policy output에서 verifier-backed execution runtime으로 이동",
            "buckets": ["Robot Learning", "Foundation Models"],
            "ids": ["2607.16636", "2607.18016", "2607.18060", "2607.17861", "2607.17786", "2607.18236", "2607.16247"],
            "needles": ["verifiable", "verification", "runtime", "memory", "vla", "reasoning", "safety", "orchestration", "object tokens"],
            "why": (
                "PhyAgentOS는 task를 action call이 아니라 evidence와 verifier verdict가 남는 session으로 재정의하고, POT-VLA는 role-indexed 3D object records를 "
                "action generation과 predicate verification이 함께 쓰게 합니다. RoboHarness와 ConceptTree까지 보면 오늘의 agent/VLA 축은 더 똑똑한 planner보다 "
                "실패 evidence, recovery path, semantic transparency가 남는 runtime을 요구합니다."
            ),
            "confidence": "High",
            "confidence_note": "session verifier, persistent 3D object tokens, memory-driven orchestration, reasoning robustness, semantic transparency가 독립 논문군에서 반복됩니다.",
            "lab_action": (
                "같은 long-horizon task에 policy-only, retry-only, predicate verifier, persistent object-token, session-memory 조건을 적용하고 "
                "semantic completion, false-positive success, recovery count, human-debug time을 비교합니다."
            ),
            "limit": 7,
        },
        {
            "title": "Slow reasoning과 sampled futures가 always-on compute에서 selective trust gate로 이동",
            "buckets": ["Embodied AI", "Efficiency/Systems", "Generation", "Autonomous Driving"],
            "ids": ["2607.16806", "2607.17454", "2607.18042", "2607.16602", "2607.16314", "2607.17521", "2607.18080", "2607.17914"],
            "needles": ["world action", "test-time", "staleness", "future", "reasoner", "planner", "world model", "navigation", "evidence"],
            "why": (
                "SPARK-VLN은 slow VLM의 최종 answer를 기다리지 않고 intermediate hidden state를 fast planner에 streaming하고, GeoBoN은 WAM future의 cross-view geometry가 "
                "불안할 때만 additional sampling을 trigger합니다. Future-State-Conditioned VLN, PAVXploreRL, Depth-Regularized JEPA World Models까지 합치면 "
                "embodied world model의 질문은 더 많은 inference가 아니라 어떤 future evidence를 execution 전에 믿을지입니다."
            ),
            "confidence": "High",
            "confidence_note": "dynamic VLN staleness, WAM geometric verification, future-state supervision, action-conditioned world model이 같은 selective-trust 축을 만듭니다.",
            "lab_action": (
                "dynamic navigation과 RoboCasa-style WAM tasks에서 wait-then-act, token streaming, always-on Best-of-N, gated Best-of-N을 같은 latency budget에 두고 "
                "collision, route/task completion, trigger rate, false low-score selection, recovery success를 비교합니다."
            ),
            "limit": 8,
        },
        {
            "title": "3D/SLAM 평가가 visual fidelity에서 metric state와 relocalization 계약으로 이동",
            "buckets": ["3D/Scene", "Autonomous Driving", "Efficiency/Systems"],
            "ids": ["2607.17058", "2607.16862", "2607.16897", "2607.17171", "2607.17332", "2607.17852", "2607.17956", "2607.18078", "2607.16309"],
            "needles": ["slam", "odometry", "lidar", "place recognition", "metric", "relocalization", "occupancy", "gaussian", "3d language"],
            "why": (
                "3D/Scene만 32편이고, DROID-ANCHOR는 monocular depth를 odometry-anchored metric state로 바꾸며 InLiER는 heterogeneous LiDAR place recognition을 loop closure와 "
                "multi-agent map management 문제로 봅니다. GLidE-SLAM, VIDAR, VIO, VGOcc, SaaF까지 합치면 3D 결과물은 rendering/AbsRel 점수보다 "
                "scale drift, relocalization, loop closure, object retrieval ambiguity, downstream navigation recovery를 요구합니다."
            ),
            "confidence": "High",
            "confidence_note": "metric depth, LiDAR place recognition, embedded SLAM, VIO, dynamic localization, driving occupancy, 3D language fields가 geometry gate를 충족합니다.",
            "lab_action": (
                "same indoor/outdoor route에서 visual SLAM, odometry-anchored depth, LiDAR place recognition, Gaussian/occupancy map을 cross-sensor FoV, low-light, dynamic-object, wheel-slip split으로 비교하고 "
                "scale drift, relocalization success, loop-closure precision, navigation recovery delta를 평가합니다."
            ),
            "limit": 9,
        },
        {
            "title": "Open-vocabulary manipulation perception이 one-shot detection에서 ambiguity-aware assistance로 이동",
            "buckets": ["3D/Scene", "Robot Learning", "Embodied AI", "Foundation Models"],
            "ids": ["2607.16309", "2607.17323", "2607.16312", "2607.17754", "2607.17778", "2607.17938", "2607.16956", "2607.18062"],
            "needles": ["open-vocabulary", "retrieval", "ambiguity", "shared autonomy", "segmentation", "object", "task planning", "costmap"],
            "why": (
                "SaaF는 3D language field가 ambiguous query를 감지하고 clarification을 요청해야 한다고 보고, open-vocabulary shared autonomy는 teleoperation assistance를 "
                "perception-to-action loop로 연결합니다. xperception, DA-Fusion, CDIS, MuViSeg까지 보면 robot perception은 object를 한 번 찾는 문제가 아니라 "
                "unknown object, clutter, similar instances, ambiguous language를 operator/action policy가 쓸 수 있는 state로 바꾸는 문제입니다."
            ),
            "confidence": "Medium-High",
            "confidence_note": "3D object retrieval, shared autonomy, unseen instance segmentation, segment correspondence, social costmap이 assistance-state 축으로 연결됩니다.",
            "lab_action": (
                "cluttered bin/shelf/room scenes에서 open-vocabulary query ambiguity, RGB-D segmentation, 3D segment persistence, teleoperation assist를 같은 target set에 적용하고 "
                "clarification rate, wrong-object selection, operator correction time, grasp/navigation success를 비교합니다."
            ),
            "limit": 8,
        },
        {
            "title": "Robotics safety 평가가 average robustness에서 configurable failure-family search로 이동",
            "buckets": ["Safety/Alignment", "Robot Learning", "Autonomous Driving", "Foundation Models"],
            "ids": ["2607.17077", "2607.17786", "2607.18106", "2607.16943", "2607.17657", "2607.16311", "2607.18200", "2607.17326"],
            "needles": ["attack", "robustness", "failure", "risk", "safety", "benchmark", "reasoning", "chance constraints"],
            "why": (
                "ALLUDE는 physical adversarial attacks를 scene, weather, camera trajectory, optimizer, detector 조건으로 configurable하게 평가하고, VLA reasoning robustness 논문은 "
                "reasoning stage가 safety signal이 될 수 있다는 직관을 adaptive attack으로 깨뜨립니다. AV failure search와 SOTIF UAV risk annotations까지 합치면 "
                "안전성은 평균 robustness가 아니라 failure family를 설계하고 재현하는 능력입니다."
            ),
            "confidence": "Medium-High",
            "confidence_note": "differentiable attack evaluation, VLA cross-stage robustness, AV failure sampling, risk annotation, orientation shortcut mitigation이 같은 failure-family 축을 형성합니다.",
            "lab_action": (
                "robot/VLA perception stack에 weather, camera trajectory, visual perturbation, reasoning-stage attack, object-state shift를 factor로 둔 stress split을 만들고 "
                "defended success, false safety signal, recovery behavior, adaptive-attack degradation을 비교합니다."
            ),
            "limit": 8,
        },
    ],
    "research_topics": [
        {
            "title": "Execution-state ledger for contact-rich VLA",
            "claim": "terminal-state foresight, force memory, object-token verifier를 같은 episode schema로 저장하고 full-task failure attribution을 비교합니다.",
        },
        {
            "title": "Selective trust controller for slow/fast embodied inference",
            "claim": "token streaming, gated WAM sampling, future-state supervision을 같은 latency budget에서 collision, route completion, trigger quality로 평가합니다.",
        },
        {
            "title": "Metric geometry trust protocol",
            "claim": "odometry-anchored depth, LiDAR place recognition, VIO/SLAM, occupancy map을 relocalization, scale drift, navigation recovery 기준으로 비교합니다.",
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
        "2607.17651", "2607.16921", "2607.17257", "2607.18060", "2607.17861", "2607.17786",
        "2607.18236", "2607.18042", "2607.16602", "2607.16314", "2607.17521", "2607.16862",
        "2607.16897", "2607.17171", "2607.17332", "2607.17852", "2607.17956", "2607.18078",
        "2607.16309", "2607.17323", "2607.16312", "2607.17754", "2607.17778", "2607.17938",
        "2607.17077", "2607.18106", "2607.16943", "2607.17657", "2607.16311", "2607.18200",
    }
    insights["tier_b"] = [abstract_card(p) for p in all_papers if p["arxiv_id"] in tier_b_ids]
    insights["tier_c"] = [abstract_card(p) for p in all_papers if p["arxiv_id"] not in tier_a_ids | tier_b_ids]
    insights["tiering_note"] = (
        "Tier A 7편은 official arXiv full text 기반입니다. Tier B와 Tier C는 parser-provided abstract만 사용했으며 "
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
        f"Tier A 7편의 주장, 증거, 숨은 전제, 반증 조건을 원문 기준으로 대조했습니다.</span>"
        f"<a href=\"{DATE}-research-intelligence.html\">Research Intelligence 열기</a></section>"
    )
    doc = re.sub(r"</section>\n(<h2>.*?</h2>)", f"</section>\n{ri_callout}\n\\1", doc, count=1, flags=re.S)
    post_path.write_text(doc, encoding="utf-8")
