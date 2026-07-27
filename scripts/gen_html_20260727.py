#!/usr/bin/env python3
"""Generate the 2026-07-27 daily briefing from matching arXiv /new listings."""
from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, phylogeny_for, week_start
from gen_research_intelligence_20260727 import DATA as RI_DATA


DATE = "2026-07-27"

PROFILE = {
    "date": DATE,
    "weekday": "Mon",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from the matching 2026-07-27 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-07-27 arXiv /new listings. "
        "Tier A claims are checked against official arXiv HTML in the Research Intelligence edition."
    ),
    "thesis": (
        "7월 27일 배치의 결론은 robotics와 vision-language 연구가 더 큰 model score보다 action, scene, risk, "
        "and localization evidence를 시스템 계약으로 분리하는 방향으로 움직였다는 점입니다. Robot-Factored World Models와 "
        "GRACE는 action output을 바로 믿지 않고 rendered robot state와 gradient-free constraint guidance를 중간 표면으로 둡니다. "
        "SceneActBench와 SM4RT는 3D 능력을 텍스트 답변이 아니라 scene operation, motion basis, hidden geometry check로 묶습니다. "
        "JustDepth, CARA, Physical Agency, Mag4D-SLAM은 real-time depth, concept risk, tool-call verification, sensing substrate가 "
        "deployment failure를 설명하는 핵심 evidence임을 보여줍니다. APRL 관점에서는 policy 크기보다 action-to-state trace, scene-action benchmark, "
        "and sensing/risk evidence log를 먼저 소유하는 것이 더 방어적인 연구 자산입니다."
    ),
    "cluster_takeaway": (
        "오늘의 핵심은 VLA, 3D, depth, safety 논문을 따로 읽는 것이 아니라 robot episode가 어떤 evidence surface를 남겨야 "
        "실패를 복원할 수 있는지 묻는 것입니다."
    ),
    "trend_note": (
        "Robot Learning과 Generation이 각각 14편, 3D/Scene과 Foundation Models가 각각 12편으로 크지만, 공통 축은 bucket 크기가 아니라 "
        "action realization, scene operation, real-time sensing, interpretable risk, and verification trace입니다."
    ),
    "cluster_specs": [
        {
            "title": "Action-conditioned policy가 raw token에서 realized state contract로 이동",
            "buckets": ["Robot Learning", "Generation", "Efficiency/Systems"],
            "ids": ["2607.22535", "2607.21661", "2607.21670", "2607.21725", "2607.22534", "2607.22225"],
            "needles": ["world model", "action", "diffusion", "mppi", "policy", "robot", "tokens", "safe learning"],
            "why": (
                "Robot-Factored World Models는 action을 rendered robot geometry와 scene response의 계약으로 바꾸고, GRACE는 diffusion prior를 "
                "deployment-time cost로 재가중합니다. Ordered Action Tokens와 Physical Agency까지 묶으면 오늘의 action stack은 decoder competition이 아니라 "
                "action이 실제 state로 실현되는 경로를 어디에 기록하고 검증할지의 문제로 이동합니다."
            ),
            "confidence": "High",
            "confidence_note": "world model, diffusion guidance, action tokenization, orchestration papers가 같은 interface axis를 공유합니다.",
            "lab_action": (
                "LIBERO/RoboCasa 미니셋에서 raw action token, rendered nominal robot state, gradient-free cost guidance, verification wrapper를 비교하고 "
                "execution success, unsafe contact, recovery trigger, and state-prediction error를 같은 episode log에 저장합니다."
            ),
            "limit": 6,
        },
        {
            "title": "3D understanding이 static answer에서 executable scene operation으로 이동",
            "buckets": ["3D/Scene", "Foundation Models", "Generation"],
            "ids": ["2607.22393", "2607.22534", "2607.21848", "2607.21896", "2607.22147", "2607.22302"],
            "needles": ["3d", "scene", "reconstruction", "motion", "rendering", "view", "agent", "geometry"],
            "why": (
                "SceneActBench는 VLM이 Blender interface로 scene을 수정하고 hidden ground truth로 평가받게 만들며, SM4RT는 dynamic scene을 motion bases와 "
                "world-coordinate tracks로 구조화합니다. generative rendering, Gaussian allocation, sparse-view relocalization 신호와 함께 보면 3D 평가는 "
                "보기 좋은 reconstruction보다 scene operation이 성공하는지로 옮겨가고 있습니다."
            ),
            "confidence": "High",
            "confidence_note": "scene-agent benchmark, 4D motion geometry, rendering consistency, relocalization papers가 같은 executable 3D axis를 형성합니다.",
            "lab_action": (
                "내부 GLB scene 10개에 layout edit, camera pose, moving object reconstruction task를 만들고 VLM/tool agent가 만든 artifact를 hidden pose, topology, "
                "and motion-basis consistency로 채점합니다."
            ),
            "limit": 6,
        },
        {
            "title": "Autonomy risk가 final score에서 concept, constraint, and sensing evidence로 이동",
            "buckets": ["Autonomous Driving", "Safety/Alignment", "Efficiency/Systems"],
            "ids": ["2607.22494", "2607.22409", "2607.22172", "2607.22077", "2607.21673", "2607.22078"],
            "needles": ["risk", "collision", "constraint", "depth", "radar", "robust", "uncertainty", "driving"],
            "why": (
                "CARA는 collision anticipation을 concept-aware risk trajectory로 만들고, Conformal Constraint Tightening은 unknown dynamics 아래 chance constraint를 "
                "다룹니다. JustDepth는 radar-camera depth를 error-latency frontier로 놓고, OOD calibration과 robustness 논문들은 safety claim이 final accuracy가 아니라 "
                "어떤 evidence와 constraint를 release gate에 넣는지에 달려 있음을 보여줍니다."
            ),
            "confidence": "Medium-High",
            "confidence_note": "risk concept, constraint tightening, real-time depth, OOD calibration signals가 안전성 release axis로 연결됩니다.",
            "lab_action": (
                "driving/navigation clip마다 risk concept timeline, depth confidence, constraint slack, OOD score를 붙이고 collision/route-deviation 직전 몇 초에 "
                "어떤 evidence가 먼저 무너지는지 비교합니다."
            ),
            "limit": 6,
        },
        {
            "title": "Robot manipulation이 end-to-end success에서 orchestration and recovery trace로 이동",
            "buckets": ["Robot Learning"],
            "ids": ["2607.21725", "2607.22020", "2607.22119", "2607.22249", "2607.21648", "2607.22434"],
            "needles": ["manipulation", "bimanual", "tactile", "humanoid", "social robot", "orchestration", "recovery"],
            "why": (
                "Physical Agency는 frozen skills를 호출하고 verify/recover하는 closed loop를 강조하고, bimanual manipulation, tactile withdrawal, humanoid synthetic scenarios는 "
                "success demo만으로는 어떤 module이 실패했는지 설명하기 어렵다는 점을 반복합니다. manipulation 연구의 공통 축은 더 많은 demo보다 tool choice, contact reflex, "
                "and cooperative assignment가 episode trace에 남는지입니다."
            ),
            "confidence": "High",
            "confidence_note": "orchestration, bimanual cooperation, tactile reflex, humanoid synthetic scenario가 manipulation failure diagnosis로 묶입니다.",
            "lab_action": (
                "same tabletop assembly task에서 monolithic policy, explicit orchestrator, tactile reflex wrapper, bimanual assignment planner를 비교하고 "
                "subgoal verification, hand-off failure, reflex trigger, and second-attempt recovery를 계측합니다."
            ),
            "limit": 6,
        },
        {
            "title": "MLLM reliability가 answer confidence에서 evidence consistency and action readiness로 이동",
            "buckets": ["Foundation Models", "Safety/Alignment", "Embodied AI"],
            "ids": ["2607.22393", "2607.22034", "2607.22013", "2607.21722", "2607.22293", "2607.22014"],
            "needles": ["confidence", "reasoning", "visual", "multimodal", "agent", "mission", "reliable", "consistency"],
            "why": (
                "Small VLM confidence, saliency-steered chain-of-thought, robust visual reasoning, radiology reliability, and mission-level aerial agents all ask whether a model knows "
                "which visual evidence supports its decision. SceneActBench pushes that question further by requiring action on 3D scenes, so reliability is no longer self-reporting confidence "
                "but evidence consistency that survives tool use."
            ),
            "confidence": "Medium-High",
            "confidence_note": "confidence, CoT saliency, consistency constraints, action benchmark signals align despite different application domains.",
            "lab_action": (
                "robot VLM episodes에 answer confidence, saliency/evidence region, tool call, and final scene-state error를 함께 저장하고 right-answer-wrong-evidence cases를 별도 실패군으로 라벨링합니다."
            ),
            "limit": 6,
        },
        {
            "title": "Localization and mapping asset이 visual fidelity에서 failure-resilient substrate로 이동",
            "buckets": ["3D/Scene", "Embodied AI", "Autonomous Driving"],
            "ids": ["2607.21986", "2607.22145", "2607.22123", "2607.22226", "2607.22166", "2607.22325"],
            "needles": ["slam", "odometry", "localization", "mapping", "navigation", "path planning", "scene graph", "lidar"],
            "why": (
                "Mag4D-SLAM은 geomagnetic sensing을 GNSS-denied localization asset으로 만들고, Flight-Ready LIO와 DB-VIO는 embedded drone and visual-inertial continuity를 다룹니다. "
                "outdoor VLN, partial-observability planning, 2D scene graph generation까지 묶으면 mapping의 가치는 render quality가 아니라 robot이 실패할 때 남아 있는 localization substrate입니다."
            ),
            "confidence": "High",
            "confidence_note": "SLAM dataset, flight-ready LIO, VIO, outdoor navigation, path planning papers가 localization substrate axis를 공유합니다.",
            "lab_action": (
                "same outdoor route에서 LiDAR-inertial odometry, visual-inertial branch, geomagnetic cue, and language-goal localization을 ablation하고 "
                "relocalization time, drift, route recovery, and sensor dropout tolerance를 측정합니다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Action-to-state contract logger",
            "claim": (
                "Raw action, rendered nominal robot geometry, constraint cost, realized state, and verification outcome을 같은 rollout schema로 저장해 policy failure를 복원합니다."
            ),
        },
        {
            "title": "Scene-action hidden evaluator",
            "claim": (
                "VLM/tool agent가 수정한 GLB scene을 hidden pose, topology, motion-basis checks로 평가해 3D reasoning을 executable artifact로 바꿉니다."
            ),
        },
        {
            "title": "Risk concept and sensing evidence timeline",
            "claim": (
                "collision/navigation episode마다 risk concept, depth latency/confidence, localization substrate, constraint slack을 시간축으로 붙여 early failure signal을 찾습니다."
            ),
        },
        {
            "title": "Manipulation orchestration audit",
            "claim": (
                "TAMP, VLA, tactile reflex, bimanual assignment, recovery call을 explicit tool trace로 남겨 end-to-end success 뒤의 module failure를 분리합니다."
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
            "evidence_trace": paper["evidence"],
            "source": "official arXiv HTML",
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
        "2607.21670", "2607.22145", "2607.22014", "2607.22226", "2607.22166",
        "2607.22034", "2607.22013", "2607.21722", "2607.22249", "2607.22119",
        "2607.22020", "2607.22409", "2607.22325", "2607.22147", "2607.21848",
        "2607.21896", "2607.22123", "2607.22225",
    }
    non_tier_c = tier_a_ids | tier_b_ids
    insights["tier_b"] = [abstract_card(p) for p in all_papers if p["arxiv_id"] in tier_b_ids and p["arxiv_id"] not in tier_a_ids]
    insights["tier_c"] = [abstract_card(p) for p in all_papers if p["arxiv_id"] not in non_tier_c]
    insights["tiering_note"] = (
        f"Tier A {len(tier_a_ids)} papers use official arXiv HTML evidence. Tier B and Tier C are conservative abstract-only cards "
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
        f"Tier A {len(RI_DATA['papers'])} papers are checked against official arXiv HTML, with evidence traces, "
        f"adversarial reads, frontier memory, and APRL strategy board.</span>"
        f"<a href=\"{DATE}-research-intelligence.html\">Open Research Intelligence</a></section>"
    )
    doc = re.sub(r"</section>\n(<h2>.*?</h2>)", f"</section>\n{ri_callout}\n\\1", doc, count=1, flags=re.S)
    post_path.write_text(doc, encoding="utf-8")
