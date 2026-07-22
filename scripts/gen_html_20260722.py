#!/usr/bin/env python3
"""Generate the 2026-07-22 daily briefing from matching arXiv /new listings."""
from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, phylogeny_for, week_start
from gen_research_intelligence_20260722 import DATA as RI_DATA


DATE = "2026-07-22"

PROFILE = {
    "date": DATE,
    "weekday": "Wed",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from the matching 2026-07-22 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-07-22 arXiv /new listings. "
        "Tier A claims are checked against official arXiv full text in the Research Intelligence edition."
    ),
    "thesis": (
        "7월 22일 배치의 핵심은 robot foundation model과 autonomous system 연구가 더 큰 model output보다 "
        "실행 가능한 state contract를 어떻게 만들고 검증할지로 옮겨졌다는 점입니다. Masked Visual Actions, "
        "WorldScape Policy 2.0, Agentic Real2Sim은 video/world model을 action trajectory, event memory, simulator "
        "episode twin과 연결합니다. OREN-Bubble*, STeP, STL-GCS, reachability 논문들은 geometry와 language plan을 "
        "planner가 소비할 SDF, temporal logic, safety certificate로 바꾸려 합니다. Cognitive Dual-Process Planning과 "
        "No Training Better Flights는 slow reasoning을 always-on으로 쓰지 않고 routing, self-refinement, scoring gate로 제한합니다. "
        "Recti-Q, Hazard-or-Anomaly, MissingBench, PathAgentBench는 배포 안전성이 clean score가 아니라 OOD shift, "
        "evidence seeking, anomaly/hazard confusion에서 깨진다는 신호를 줍니다."
    ),
    "cluster_takeaway": (
        "오늘의 핵심은 더 큰 VLA나 더 긴 video model이 아니라, action, map, specification, reasoning, edge perception을 "
        "실제 failure condition 안에서 어떤 검증 가능한 state로 바꿀 것인가입니다."
    ),
    "trend_note": (
        "Generation 23편, Efficiency/Systems 20편, Foundation Models 19편, Robot Learning 15편, 3D/Scene 13편이 두꺼웠지만, "
        "robotics 관점의 공통 연구 결정은 model capacity보다 execution-state interface입니다. 오늘은 visual action masks, event memory, "
        "episode twins, SDF corridors, STL violation traces, fast/slow reasoning gates, quantization robustness patches가 서로 다른 형태로 같은 질문을 던집니다."
    ),
    "cluster_specs": [
        {
            "title": "World model이 video prior에서 executable action-state contract로 이동",
            "buckets": ["Robot Learning", "Generation", "Efficiency/Systems"],
            "ids": ["2607.19343", "2607.18840", "2607.19190", "2607.18703", "2607.18924", "2607.19191", "2607.18787"],
            "needles": ["world model", "world action", "masked visual", "real2sim", "action-conditioned", "physical parameter", "simulation", "video generation"],
            "why": (
                "기존 world model 평가는 video가 그럴듯한지 또는 action token을 넣을 수 있는지에 머무르기 쉬웠습니다. 이번 묶음은 action을 pixel trajectory로 보이게 하거나, "
                "event memory로 subgoal progress를 보존하거나, real episode를 simulator twin으로 바꿔 generated future가 실제 contact와 downstream success를 설명하는지 묻습니다. "
                "APRL은 WAM을 policy baseline이 아니라 visual action, event state, simulator replay가 같은 episode schema에서 비교되는 execution evaluator로 봐야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "Masked Visual Actions, WorldScape Policy 2.0, Agentic Real2Sim, AlayaRenderer, physical video-control 논문이 실행 가능한 world state 축을 반복합니다.",
            "lab_action": (
                "RoboCasa/DROID manipulation task에서 action-vector WAM, masked-visual-action rollout, event-memory policy, simulator-twin replay를 같은 episode schema로 비교하고 "
                "contact realism, object displacement, next-skill readiness, real execution success correlation을 평가합니다."
            ),
            "limit": 7,
        },
        {
            "title": "Language-conditioned planning이 prompt output에서 formal violation feedback runtime으로 이동",
            "buckets": ["Robot Learning", "Safety/Alignment", "Autonomous Driving"],
            "ids": ["2607.18580", "2607.18731", "2607.19196", "2607.18606", "2607.18362", "2607.19284", "2607.18855"],
            "needles": ["signal temporal logic", "stl", "behavior tree", "reachability", "feasibility", "kinodynamic", "motion planning", "constraints"],
            "why": (
                "VLM plan이나 sampling planner가 plausible action을 내는 것만으로는 constraint satisfaction을 보장할 수 없습니다. STeP는 instruction을 STL specification과 robustness trace로 바꾸고, "
                "correct-by-construction BT/STL-GCS/reachability/FARO 계열은 plan이 어떤 조건에서 실패하는지 수학적으로 드러내려 합니다. 따라서 APRL robot planning 평가는 task success뿐 아니라 "
                "violation margin, recovery attempt, unsafe contact, feasibility rejection을 함께 봐야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "STL specification, behavior tree synthesis, graph-of-convex-sets planning, reachability limits, feasibility-aware optimization이 같은 formal feedback 축으로 묶입니다.",
            "lab_action": (
                "UR5/Franka tabletop과 mobile manipulation tasks에서 plain VLM retry, scalar-cost MPC, STL violation trace, feasibility-aware optimizer를 비교하고 "
                "second-attempt recovery, constraint violation margin, unsafe contact count, plan rejection precision을 평가합니다."
            ),
            "limit": 7,
        },
        {
            "title": "3D/SLAM 평가가 visual geometry에서 planner가 소비하는 metric state로 이동",
            "buckets": ["3D/Scene", "Generation", "Efficiency/Systems"],
            "ids": ["2607.19306", "2607.19228", "2607.18801", "2607.18630", "2607.19120", "2607.19111", "2607.19171", "2607.18578"],
            "needles": ["sdf", "mapping", "planning", "3d gaussian", "geometry", "reconstruction", "point cloud", "lidar", "retrieval"],
            "why": (
                "오늘 3D/Scene은 avatar와 rendering도 많지만, robotics 관점의 강한 축은 map이나 3D field가 downstream planner/agent에게 무엇을 보장하는지입니다. "
                "OREN-Bubble*은 SDF gradient와 safe corridor를 묶고, IGGT4D와 ZeroSplat은 streaming object persistence와 ambiguous 3D language query를 다룹니다. "
                "APRL의 geometry 평가는 mesh score가 아니라 scale drift, relocalization, object persistence, clearance, navigation/manipulation recovery로 연결되어야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "SDF mapping/planning, streaming 4D geometry, referring 3DGS, object perception 3D recon, geometry-aware retrieval이 geometry gate를 충족합니다.",
            "lab_action": (
                "indoor route와 tabletop scene에서 SDF map, Gaussian/feature field, feed-forward 3D model, 3D language field를 same sensor split에 두고 "
                "scale drift, relocalization success, object persistence, clearance violation, downstream task recovery를 비교합니다."
            ),
            "limit": 8,
        },
        {
            "title": "VLM safety 평가가 answer accuracy에서 evidence-seeking failure family 진단으로 이동",
            "buckets": ["Foundation Models", "Safety/Alignment", "Efficiency/Systems"],
            "ids": ["2607.18325", "2607.18673", "2607.19261", "2607.18577", "2607.19061", "2607.18850", "2607.19077", "2607.18508"],
            "needles": ["hazard", "anomaly", "missing", "evidence", "pathology", "grounding", "anomaly detection", "safety", "faithfulness"],
            "why": (
                "VLM benchmark는 정답률이 높아도 model이 어떤 evidence를 보고 판단했는지, 그리고 어떤 failure family에서 confident mistake를 내는지 모르면 robot safety에 바로 쓰기 어렵습니다. "
                "Hazard-or-Anomaly는 unusualness와 physical danger를 분리하고, MissingBench/PathAgentBench/attention faithfulness 논문은 evidence seeking과 visual grounding을 따집니다. "
                "APRL은 emergency scene, manipulation safety, inspection task에서 false alarm, missed hazard, evidence region, intervention cost를 함께 평가해야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "hazard/anomaly confusion, missing-object-part detection, evidence-seeking pathology, causal attention audit, hidden hateful illusion이 같은 evidence reliability 축입니다.",
            "lab_action": (
                "robot inspection images에서 hazard, anomaly, missing part, deceptive visual cue를 orthogonal labels로 만들고 image-only, dense-caption, evidence-seeking VLM을 비교해 "
                "false alarm, missed hazard, evidence localization, operator correction time을 평가합니다."
            ),
            "limit": 8,
        },
        {
            "title": "Autonomous navigation reasoning이 always-on CoT에서 trust-gated compute로 이동",
            "buckets": ["Foundation Models", "Autonomous Driving", "Embodied AI"],
            "ids": ["2607.19288", "2607.19194", "2607.18604", "2607.18565", "2607.18637", "2607.18663", "2607.18768"],
            "needles": ["test-time", "dual-process", "uav navigation", "driving", "arbiter", "routing", "intersection", "scenario generation", "POMDP"],
            "why": (
                "UAV와 driving VLM은 slow reasoning을 더 많이 쓰면 좋아질 수 있지만, latency와 false-negative routing이 곧 safety cost가 됩니다. No Training Better Flights는 parallel exploration과 serial refinement를 scoring gate로 묶고, "
                "Cognitive Dual-Process Planning은 visual Arbiter와 rule validator로 slow path를 제한합니다. Integrity-gated Eco-CACC와 online POMDP interception까지 합치면 autonomous navigation은 "
                "언제 reasoning/communication/future sampling을 믿을지의 gate 문제로 이동하고 있습니다."
            ),
            "confidence": "Medium-High",
            "confidence_note": "UAV test-time scaling, driving fast/slow arbiter, LLM multi-UAV hierarchy, integrity-gated CACC, online POMDP planning이 trust gate 축을 공유합니다.",
            "lab_action": (
                "AirSim/CARLA-lite route에서 single-pass VLM, parallel-refine-select, visual-Arbiter slow path, integrity-gated controller를 같은 latency budget에 두고 "
                "collision, route completion, false slow-path skip, unnecessary conservative action, recovery trajectory를 비교합니다."
            ),
            "limit": 7,
        },
        {
            "title": "Edge robotics reliability가 compression Pareto에서 shift-conditioned patch and gate로 이동",
            "buckets": ["Efficiency/Systems", "3D/Scene", "Autonomous Driving"],
            "ids": ["2607.18540", "2607.18713", "2607.19146", "2607.19036", "2607.18747", "2607.18875", "2607.19284"],
            "needles": ["quantized", "edge robotics", "confidence-gated", "privacy", "fusion", "uav", "mmwave", "adversaries", "cooperative"],
            "why": (
                "edge deployment은 FPS와 model size만으로 충분하지 않습니다. Recti-Q는 4-bit PTQ가 clean accuracy를 보존해도 OOD robustness를 잃을 수 있음을 보이고, "
                "Confidence-Gated Heading과 Sarus는 perception output을 그대로 control/fusion에 넣지 말고 confidence, privacy, vendor boundary를 고려해야 한다고 봅니다. "
                "APRL은 edge perception을 latency Pareto가 아니라 shift family별 patchability와 command gate reliability로 평가해야 합니다."
            ),
            "confidence": "Medium-High",
            "confidence_note": "quantization robustness, UAV-UGV confidence gating, privacy-preserving cooperative fusion, RGB-event UAV tracking, radar-to-body translation이 deployment reliability 축으로 연결됩니다.",
            "lab_action": (
                "low-light/fog/motion-blur robot clips에서 quantized backbone, Recti-Q adapter, confidence-gated command, cooperative fusion baseline을 비교하고 "
                "OOD recovery, temporal consistency, command false-positive, payload size, edge latency를 함께 평가합니다."
            ),
            "limit": 7,
        },
    ],
    "research_topics": [
        {
            "title": "Execution-state contract harness",
            "claim": (
                "visual action rollout, event memory, simulator twin, real execution을 같은 episode schema로 맞추고 contact realism, object displacement, next-skill readiness를 함께 평가합니다."
            ),
        },
        {
            "title": "Formal failure feedback runtime",
            "claim": (
                "VLM-generated task plan을 STL predicate, violation margin, correction action으로 변환해 plain retry보다 recovery가 빨라지는지 tabletop and mobile manipulation에서 검증합니다."
            ),
        },
        {
            "title": "Robot-usable geometry protocol",
            "claim": (
                "SDF, Gaussian/feature field, feed-forward 3D geometry를 scale drift, relocalization, clearance violation, downstream recovery 기준으로 비교합니다."
            ),
        },
        {
            "title": "Edge robustness patch benchmark",
            "claim": (
                "4-bit quantized perception, tiny adapter patch, confidence-gated control을 low-light/fog/motion-blur split에서 비교해 OOD recovery and command stability를 평가합니다."
            ),
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
        "2607.19288", "2607.18604", "2607.18565", "2607.18637", "2607.18663", "2607.18768",
        "2607.18731", "2607.19196", "2607.18606", "2607.18362", "2607.19284", "2607.18855",
        "2607.19228", "2607.18801", "2607.18630", "2607.19120", "2607.19111", "2607.19171",
        "2607.18703", "2607.18924", "2607.19191", "2607.18787", "2607.18673", "2607.19261",
        "2607.18577", "2607.19061", "2607.18850", "2607.19077", "2607.18508", "2607.18713",
        "2607.19146", "2607.19036", "2607.18747", "2607.18875",
    }
    insights["tier_b"] = [abstract_card(p) for p in all_papers if p["arxiv_id"] in tier_b_ids]
    insights["tier_c"] = [abstract_card(p) for p in all_papers if p["arxiv_id"] not in tier_a_ids | tier_b_ids]
    insights["tiering_note"] = (
        "Tier A 8편은 official arXiv full text 기반입니다. Tier B와 Tier C는 parser-provided abstract만 사용했으며 "
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
        f"Tier A 8편의 주장, 증거, 숨은 전제, 반증 조건을 원문 기준으로 대조했습니다.</span>"
        f"<a href=\"{DATE}-research-intelligence.html\">Research Intelligence 열기</a></section>"
    )
    doc = re.sub(r"</section>\n(<h2>.*?</h2>)", f"</section>\n{ri_callout}\n\\1", doc, count=1, flags=re.S)
    post_path.write_text(doc, encoding="utf-8")
