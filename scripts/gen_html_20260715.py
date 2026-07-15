#!/usr/bin/env python3
"""Generate the 2026-07-15 daily briefing from matching arXiv /new listings."""
from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, phylogeny_for, week_start
from gen_research_intelligence_20260715 import DATA as RI_DATA


DATE = "2026-07-15"

PROFILE = {
    "date": DATE,
    "weekday": "Wed",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from the matching 2026-07-15 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-07-15 arXiv /new listings. "
        "Tier A claims are audited against official arXiv full text in the Research Intelligence edition."
    ),
    "thesis": (
        "7월 15일 배치의 가장 강한 신호는 모델 크기 경쟁보다 실패가 생기는 clock, coordinate, evaluator를 먼저 고정하는 쪽입니다. "
        "VLA 논문들은 token reuse, future latent, chunk boundary, backdoor evidence를 control loop와 연결하고, geometry 논문들은 "
        "radar physics, pixel loop closure, heterogeneous camera depth를 downstream map validity로 바꿉니다. APRL에는 새 backbone보다 "
        "실패가 시작되는 시간축과 공간축을 측정하는 harness가 더 큰 연구 자산입니다."
    ),
    "cluster_takeaway": (
        "오늘의 핵심은 더 빠른 VLA나 더 좋은 3D 모델이 아니라, runtime·geometry·evaluation의 숨은 계약을 실제 robot failure 안에서 어떻게 분리해 검증할 것인가입니다."
    ),
    "trend_note": (
        "Foundation Models, Generation, Efficiency/Systems가 두껍지만 robotics 관점의 실제 판세는 Robot Learning, 3D/Scene, Safety/Alignment가 잡습니다. "
        "공통 전환은 평균 성능에서 failure-family와 deployment-clock 측정으로, visual quality에서 downstream spatial validity로 이동하는 흐름입니다."
    ),
    "cluster_specs": [
        {
            "title": "VLA runtime이 token 절약에서 control-loop clock 정렬로 이동",
            "buckets": ["Robot Learning", "Safety/Alignment", "Efficiency/Systems"],
            "ids": ["2607.12659", "2607.12287", "2607.12992", "2607.12931", "2607.12892", "2607.13033", "2607.12571"],
            "needles": ["vla", "latency", "chunk", "real-time", "reward", "temporal redundancy", "inference"],
            "why": (
                "Reducing Temporal Redundancy와 Jetson-PI는 VLA 속도를 단순 pruning 문제가 아니라 action chunk가 실행될 미래 상태와 맞는지의 문제로 봅니다. "
                "ChunkFlow, ExToken, UR-VC, DenseReward도 success 뒤에 숨어 있는 chunk boundary, exploration cost, progress proxy, reward failure를 분리합니다. "
                "따라서 VLA 평가는 평균 success뿐 아니라 latency, jitter, boundary continuity, failure warning lead time을 함께 재야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "runtime, chunking, RL fine-tuning, reward/value correction 신호가 같은 execution-system 축으로 반복됩니다.",
            "lab_action": (
                "LIBERO/RoboCasa에서 latency, jitter, chunk overlap, token reuse ratio를 factorial sweep하고 success, SR@30s, boundary jitter, failure-warning lead time을 비교합니다."
            ),
            "limit": 6,
        },
        {
            "title": "3D representation 경쟁이 rendering fidelity에서 robot-usable geometry 계약으로 이동",
            "buckets": ["3D/Scene", "Robot Learning", "Generation", "Safety/Alignment"],
            "ids": ["2607.12265", "2607.12811", "2607.12356", "2607.12993", "2607.13017", "2607.12429", "2607.12398"],
            "needles": ["slam", "gaussian", "depth", "loop", "metric", "3d", "world action"],
            "why": (
                "DiffRadar와 PixelLoop는 map을 예쁘게 보이는 산출물이 아니라 pose drift, loop shortcut, planning cost를 바꾸는 representation으로 다룹니다. "
                "VistaVLA, X-Lens, FlowWAM은 3D Gaussian, calibrated heterogeneous depth, optical flow action처럼 policy가 소비할 수 있는 spatial interface를 만듭니다. "
                "APRL의 3D/SLAM 실험도 rendering score 옆에 localization, loop drift, dynamic-object failure, downstream task success를 기본 축으로 둬야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "radar SLAM, topological navigation, VLA manipulation, metric depth가 모두 downstream geometry validity를 요구합니다.",
            "lab_action": (
                "동일 trajectory에서 point-cloud map, Gaussian map, feature-field map을 focal shift, dynamic object, loop closure 조건별로 비교하고 ATE, costmap MAE, navigation success를 함께 평가합니다."
            ),
            "limit": 6,
        },
        {
            "title": "Benchmark 신뢰성이 headline score에서 evidence channel 감사로 이동",
            "buckets": ["Foundation Models", "Safety/Alignment"],
            "ids": ["2607.12278", "2607.12304", "2607.12818", "2607.12364", "2607.12375", "2607.12477", "2607.12503"],
            "needles": ["benchmark", "audit", "leakage", "temporal", "evidence", "evaluation", "reasoning"],
            "why": (
                "WSI leakage audit와 temporal benchmark audit는 같은 score라도 data provenance나 temporal channel이 다르면 의미가 달라진다는 점을 보입니다. "
                "DynTrace, Self in Space, IQA-T1, visual place recognition audit도 모델의 정답보다 어떤 evidence를 따라 판단했는지를 묻습니다. "
                "로봇 benchmark도 success score 전에 sensor timestamp, evaluator threshold, hidden-state evidence, provenance overlap을 분리해야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "pathology, video VLM, UAV cognition, visual place recognition에서 score contract 자체를 감사하는 논문이 반복됩니다.",
            "lab_action": (
                "기존 VLA/VLN evaluation에 timestamp shuffle, evaluator threshold sweep, instruction paraphrase, provenance split을 넣고 score flip과 rollout failure taxonomy를 함께 산출합니다."
            ),
            "limit": 6,
        },
        {
            "title": "Autonomous driving robustness가 logged long-tail 수집에서 procedural closed-loop generation으로 이동",
            "buckets": ["Autonomous Driving", "Generation", "Safety/Alignment", "3D/Scene"],
            "ids": ["2607.13028", "2607.12858", "2607.12959", "2607.12419", "2607.12214", "2607.12362"],
            "needles": ["driving", "closed-loop", "simulation", "anomaly", "lidar", "road", "4d"],
            "why": (
                "TerraZero는 rare driving case를 더 모으는 대신 real-world map에서 procedural scenario와 self-play로 long-tail interaction을 제조합니다. "
                "LARAD, ViCo3D, DeGuNet은 anomaly, V2X, LiDAR-camera detection에서 perception이 어떤 spatial logic과 geometry cue를 놓치는지 묻습니다. "
                "자율주행 평가는 static AP보다 agent coalition, map corruption, road-layout anomaly가 closed-loop safety를 어떻게 깨는지 재현해야 합니다."
            ),
            "confidence": "Medium-High",
            "confidence_note": "simulation, anomaly reasoning, V2X, efficient LiDAR-camera fusion이 모두 deployment failure generation으로 연결됩니다.",
            "lab_action": (
                "nuPlan/CARLA에서 lane topology, pedestrian conflict, map prior error, camera-LiDAR dropout을 stress split으로 만들고 tail CVaR, collision, recovery behavior를 함께 비교합니다."
            ),
            "limit": 6,
        },
        {
            "title": "Edge perception이 parameter 축소에서 task evidence 보존성 평가로 이동",
            "buckets": ["Efficiency/Systems", "Safety/Alignment", "Autonomous Driving"],
            "ids": ["2607.12297", "2607.12789", "2607.12544", "2607.12993", "2607.12419", "2607.12489", "2607.12275"],
            "needles": ["lightweight", "edge", "real-time", "efficient", "thermal", "depth", "low-power"],
            "why": (
                "MobileSAM2, AVQ-Attention, Edge-Aware Thermal UAV Tracking, X-Lens는 모두 계산량을 줄이되 task에 필요한 boundary, geometry, thermal cue, metric scale을 남겨야 합니다. "
                "DeGuNet과 Flatness-Preserving residual control은 perception/compute 축소가 downstream control이나 3D detection에 어떤 손실을 만드는지 봅니다. "
                "따라서 edge 연구는 FPS만이 아니라 압축 후에도 어떤 spatial evidence가 보존되는지 검증해야 합니다."
            ),
            "confidence": "Medium",
            "confidence_note": "segmentation, attention, UAV tracking, depth, control에서 효율성 신호가 많지만 공통 benchmark는 아직 약합니다.",
            "lab_action": (
                "latency, memory, bandwidth를 줄이는 조건별로 boundary error, geometry cue retention, tracking continuity, downstream action delta를 같은 Pareto curve에 둡니다."
            ),
            "limit": 6,
        },
        {
            "title": "Embodied agents가 semantic map과 lifelong memory를 runtime OS 자산으로 묶기 시작",
            "buckets": ["Embodied AI", "Foundation Models", "Robot Learning"],
            "ids": ["2607.12630", "2607.10350", "2607.12894", "2607.12965", "2607.12680", "2607.12625", "2607.11919"],
            "needles": ["memory", "semantic map", "embodied", "navigation", "agent", "lifelong"],
            "why": (
                "Instance-Enriched Semantic Maps, ABot-AgentOS, Hy-Embodied-VLM, MAMMOTH는 navigation과 manipulation을 단일 policy가 아니라 memory, semantic map, missing-modality handling, verification runtime으로 봅니다. "
                "ReflectVLN과 memory-centric MLLM 흐름도 long-horizon 실패가 planner 성능 이전에 state representation과 recovery loop에서 시작된다는 점을 강화합니다. "
                "APRL은 object-level map, episodic memory, failure verifier가 실제 navigation recovery를 얼마나 바꾸는지 하나의 runtime stack으로 실험해야 합니다."
            ),
            "confidence": "Medium",
            "confidence_note": "semantic map, lifelong memory, physical-world agent reports가 반복되지만 closed-loop robot evidence는 논문마다 강도가 다릅니다.",
            "lab_action": (
                "VLN/ObjectNav에서 semantic map richness, memory horizon, missing modality, verifier intervention을 ablation 축으로 두고 wrong-turn recovery와 subgoal completion을 평가합니다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Clock-Aligned VLA Deployment Harness",
            "claim": "latency, jitter, chunk overlap, token reuse, future latent correction이 execution failure를 언제 줄이거나 키우는지 closed-loop benchmark로 분리합니다.",
        },
        {
            "title": "Robot-Usable Geometry Validity Protocol",
            "claim": "Gaussian/radar/topological/depth map을 visual score가 아니라 ATE, loop drift, costmap MAE, navigation success로 비교합니다.",
        },
        {
            "title": "Evidence-Channel Audit for Robot Benchmarks",
            "claim": "success score를 timestamp, evaluator threshold, hidden-state evidence, provenance split으로 분해해 model failure와 benchmark artifact를 구별합니다.",
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
        "2607.12356", "2607.12811", "2607.13017", "2607.12278",
        "2607.12858", "2607.12993", "2607.12297", "2607.12630",
        "2607.10350", "2607.12429", "2607.12503", "2607.12992",
    }
    insights["tier_b"] = [abstract_card(p) for p in all_papers if p["arxiv_id"] in tier_b_ids]
    insights["tier_c"] = [abstract_card(p) for p in all_papers if p["arxiv_id"] not in tier_a_ids | tier_b_ids]
    insights["tiering_note"] = (
        "Tier A 6편은 official arXiv full text 기반입니다. Tier B 12편과 Tier C 나머지는 parser-provided abstract만 사용했으며, "
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
        "</section>\n<section class=\"ri-callout\"><span><strong>오늘의 심층판:</strong> Tier A 6편의 주장·증거·숨은 전제·반증 조건을 원문까지 대조했습니다.</span>"
        f"<a href=\"{DATE}-research-intelligence.html\">Research Intelligence 열기 →</a></section>\n<h2>오늘의 클러스터 지도</h2>"
    )
    doc = doc.replace(thesis_end, ri_callout, 1)
    post_path.write_text(doc, encoding="utf-8")
