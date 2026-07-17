#!/usr/bin/env python3
"""Generate the 2026-07-17 daily briefing from matching arXiv /new listings."""
from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, phylogeny_for, week_start
from gen_research_intelligence_20260717 import DATA as RI_DATA


DATE = "2026-07-17"

PROFILE = {
    "date": DATE,
    "weekday": "Fri",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from the matching 2026-07-17 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-07-17 arXiv /new listings. "
        "Tier A claims are checked against official arXiv full text in the Research Intelligence edition."
    ),
    "thesis": (
        "7월 17일 배치의 핵심은 로봇 foundation model이 더 큰 입력과 더 긴 context를 받는 순간 자동으로 안전해지는 것이 "
        "아니라, action-facing interface, contact state, world-action alignment, robot-usable geometry를 각각 분리해 "
        "검증해야 한다는 점입니다. VLA 논문들은 action supervision이 multimodal representation을 어떻게 바꾸는지 묻고, "
        "force/tactile 논문들은 vision-only action chunk가 접촉 상태를 놓치는 지점을 드러냅니다. 동시에 BadWAM과 3DGS/SLAM "
        "논문들은 imagined future와 visual fidelity가 실제 executable action이나 map validity를 보장하지 않는다는 경고를 줍니다."
    ),
    "cluster_takeaway": (
        "오늘의 핵심은 더 큰 VLA나 더 빠른 3D reconstruction이 아니라, 행동 직전의 representation, contact signal, geometry state가 "
        "어떤 closed-loop 실패를 실제로 줄이는지 비교하는 것입니다."
    ),
    "trend_note": (
        "Robot Learning이 가장 두껍고 Generation, Foundation Models, Safety/Alignment가 뒤따르지만, robotics 관점의 공통 축은 "
        "action-facing representation, contact observability, world-action safety, online geometry validity입니다. 이는 최근 4주간 "
        "반복된 VLA runtime, geometry validity, benchmark 검증 흐름이 더 구체적인 실험 계약으로 내려온 신호입니다."
    ),
    "cluster_specs": [
        {
            "title": "VLA 제어가 action head 경쟁에서 action-facing interface 진단으로 이동",
            "buckets": ["Robot Learning", "Foundation Models", "Efficiency/Systems"],
            "ids": ["2607.14635", "2607.14739", "2607.14280", "2607.14695", "2607.15275", "2607.14698"],
            "needles": ["vla", "vision-language-action", "action supervision", "streaming inference", "representation", "foresight"],
            "why": (
                "Action QFormer, FoMoVLA, DiMaS, Reflex, RoboTTT는 모두 VLA 성능을 action head 하나로 보지 않고, "
                "instruction-conditioned visual extraction, representation steering, streaming latency, long-context update가 "
                "행동 실패를 어떻게 바꾸는지 묻습니다. 따라서 VLA 평가는 backbone 크기보다 action-facing state가 실제로 어떤 "
                "visual evidence와 history를 통과시키는지부터 분리해야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "VLA representation, steering, streaming, long-context 신호가 CV/RO 양쪽에서 반복됩니다.",
            "lab_action": (
                "LIBERO/RoboCasa와 UAV tracking에서 query interface, steering vector, streaming inference, long-context policy를 "
                "같은 OOD object, target occlusion, latency perturbation 조건에 두고 success, recovery, instruction-action contradiction을 비교합니다."
            ),
            "limit": 6,
        },
        {
            "title": "Contact-rich manipulation이 vision-only chunk에서 force and tactile state 평가로 이동",
            "buckets": ["Robot Learning"],
            "ids": ["2607.14236", "2607.14578", "2607.14609", "2607.14842", "2607.14487", "2607.14730"],
            "needles": ["force", "tactile", "contact", "haptic", "in-hand", "gripper"],
            "why": (
                "LIFT, force-torque proxy, tactile grounding, KineFuse, sensing hand 논문은 접촉 상태가 vision과 kinematics만으로는 "
                "약하게 관측된다고 봅니다. 이번 묶음은 action chunk를 한 번 내는 policy보다, force memory와 tactile prediction이 "
                "실제 insertion, folding, in-hand tracking 실패를 얼마나 앞서 바꾸는지를 평가해야 한다는 흐름입니다."
            ),
            "confidence": "High",
            "confidence_note": "force, tactile, haptic, gripper 논문이 모두 contact observability 축으로 연결됩니다.",
            "lab_action": (
                "folding, insertion, in-hand pose tracking task에서 force memory length, tactile prediction target, haptic fusion encoder를 "
                "독립 ablation 축으로 두고 contact failure, recovery success, failure-warning lead time을 평가합니다."
            ),
            "limit": 6,
        },
        {
            "title": "World-action safety가 imagined future 품질에서 executable action alignment로 이동",
            "buckets": ["Safety/Alignment", "Robot Learning", "Foundation Models", "Autonomous Driving"],
            "ids": ["2607.15207", "2607.14943", "2607.14698", "2607.14543", "2607.14727", "2607.15016"],
            "needles": ["world-action", "safety", "adversarial", "barrier", "roadwork", "failure", "vla"],
            "why": (
                "BadWAM은 predicted future가 깨끗해 보여도 action channel이 공격될 수 있음을 보이고, WAM steering, illumination attack, "
                "SafeRelBench, WorkDrive는 embodied/spatial reasoning의 process-level failure를 묻습니다. 이는 safety 평가를 confidence나 "
                "future image fidelity가 아니라 action shift, relation violation, closed-loop recovery로 나누어야 한다는 신호입니다."
            ),
            "confidence": "High",
            "confidence_note": "WAM, VLA attack, embodied safety benchmark, driving roadwork reasoning이 같은 closed-loop safety 축을 형성합니다.",
            "lab_action": (
                "LIBERO/RoboTwin과 roadwork driving scenario에서 visual perturbation, relation violation, work-zone cue removal을 별도 stress split으로 "
                "구성하고 imagined future drift, action shift, task success, recovery behavior를 함께 비교합니다."
            ),
            "limit": 6,
        },
        {
            "title": "3DGS와 reconstruction이 visual fidelity에서 online geometry contract로 이동",
            "buckets": ["3D/Scene", "Efficiency/Systems", "Autonomous Driving"],
            "ids": ["2607.14470", "2607.14203", "2607.14481", "2607.15211", "2607.14639", "2607.15048", "2607.14228"],
            "needles": ["3d gaussian", "gaussian", "reconstruction", "lidar", "registration", "road surface", "se3"],
            "why": (
                "G2SR, Instant NuRec, unordered 3DGS, MAGiSt3R, image-to-point cloud registration은 reconstruction을 보기 좋은 novel view가 "
                "아니라 online map이 감당할 memory, throughput, pose robustness, camera-LiDAR alignment 문제로 바꿉니다. "
                "3D/SLAM 관점에서는 rendering score보다 localization, update cost, dynamic-object failure가 더 직접적인 평가 축입니다."
            ),
            "confidence": "High",
            "confidence_note": "3DGS, feed-forward reconstruction, LiDAR registration, road mapping 논문이 같은 robot-usable geometry 축으로 묶입니다.",
            "lab_action": (
                "3DGS map, point-cloud registration, feed-forward reconstruction을 같은 driving/robot camera trajectory에 적용하고 localization success, "
                "update cost, memory footprint, dynamic-object failure, downstream navigation cost를 비교합니다."
            ),
            "limit": 7,
        },
        {
            "title": "Embodied memory가 episode reset에서 persistent scene and action memory로 이동",
            "buckets": ["Embodied AI", "Foundation Models", "Autonomous Driving", "Robot Learning"],
            "ids": ["2607.14514", "2607.14252", "2607.14586", "2607.15182", "2607.14853", "2607.15163", "2607.14548"],
            "needles": ["memory", "navigation", "object-goal", "scene tokens", "embodied", "topological", "multi-agent"],
            "why": (
                "VTM-Nav와 MEMORA는 embodied agent가 episode가 끝날 때마다 scene knowledge를 버리는 protocol을 문제 삼고, SoftNav와 "
                "stigmertic graph memory는 3D scene token과 environment-aware memory를 planner 입력으로 다룹니다. 이번 축은 memory 용량보다 "
                "어떤 room/object/action evidence를 다음 episode에서 다시 쓸지의 retrieval 계약으로 읽어야 합니다."
            ),
            "confidence": "Medium-High",
            "confidence_note": "ObjectNav, embodied action memory, 3D scene token, collaborative navigation 신호가 반복됩니다.",
            "lab_action": (
                "반복 방문 ObjectNav와 mobile manipulation에서 no-memory, transcript memory, visual-topological memory, action memory를 비교하고 "
                "SPL, stale-memory failure, hidden-dependency miss, recovery success를 평가합니다."
            ),
            "limit": 6,
        },
        {
            "title": "Planning과 simulation이 single trajectory에서 constraint and scenario validity로 이동",
            "buckets": ["Autonomous Driving", "Generation", "Robot Learning", "3D/Scene"],
            "ids": ["2607.14455", "2607.14507", "2607.14387", "2607.14688", "2607.15111", "2607.15065", "2607.14997", "2607.14643"],
            "needles": ["planning", "scenario", "diffusion", "world model", "constraint", "coordination", "trajectory", "navigation"],
            "why": (
                "model-based diffusion planning, DRIFT, Chat2Scenic, MIND-CAVs, DriftWorld, AeroAct는 planning을 단일 best trajectory 산출이 아니라 "
                "constraint, intent communication, scenario generation, dynamics feasibility가 policy conclusion을 어떻게 바꾸는지 묻는 문제로 "
                "확장합니다. 이는 simulator와 planner를 따로 평가하지 말고 scenario validity와 executable control을 함께 보라는 신호입니다."
            ),
            "confidence": "Medium",
            "confidence_note": "planning, scenario generation, communication, world model 신호는 강하지만 공통 benchmark는 아직 분산되어 있습니다.",
            "lab_action": (
                "driving, UAV, quadruped navigation에서 scenario script, dynamic constraint, intent communication을 factorial split으로 만들고 "
                "planner feasibility, collision margin, ranking inversion, closed-loop task success를 비교합니다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Action-facing interface stress bench",
            "claim": "VLA의 query interface, steering, streaming inference, long-context update가 OOD object와 latency perturbation에서 어떤 실패를 줄이는지 분리합니다.",
        },
        {
            "title": "Contact-state VLA probe",
            "claim": "force memory, tactile prediction, haptic fusion을 contact-rich manipulation의 독립 변수로 두고 failure-warning lead time과 recovery success를 평가합니다.",
        },
        {
            "title": "Robot-usable geometry memory protocol",
            "claim": "3DGS reconstruction과 visual-topological memory를 반복 방문 navigation/localization task에 연결해 stale memory와 pose drift를 함께 봅니다.",
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
        "2607.14739", "2607.14280", "2607.14695", "2607.14698",
        "2607.14578", "2607.14609", "2607.14842", "2607.14203",
        "2607.14481", "2607.15211", "2607.14639", "2607.14252",
        "2607.14586", "2607.15065", "2607.14997", "2607.14387",
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
