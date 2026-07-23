#!/usr/bin/env python3
"""Generate the 2026-07-23 daily briefing from matching arXiv /new listings."""
from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, phylogeny_for, week_start
from gen_research_intelligence_20260723 import DATA as RI_DATA


DATE = "2026-07-23"

PROFILE = {
    "date": DATE,
    "weekday": "Thu",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from the matching 2026-07-23 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-07-23 arXiv /new listings. "
        "Tier A claims are checked against official arXiv full text in the Research Intelligence edition."
    ),
    "thesis": (
        "7월 23일 배치의 핵심은 robot foundation model 연구가 더 큰 backbone 경쟁에서 실행 가능한 상태 계약을 "
        "소유하는 방향으로 이동했다는 점입니다. KineBench와 PerceptDrive는 world/video model을 visual realism이 아니라 "
        "kinematic grounding, trajectory execution, perception-prior routing으로 검증합니다. EgoRecovery와 LENS는 성공 demo를 "
        "더 모으는 대신 failure state, corrective intent, scene abstraction을 회복 가능한 robot data asset으로 바꿉니다. "
        "NavVerse, EA-Nav, DINS-IO, Silent Failures는 각각 navigation boundary, embodiment geometry, inertial state, evidence trace를 "
        "새로운 release gate로 밀어 올립니다."
    ),
    "cluster_takeaway": (
        "오늘의 질문은 어떤 모델이 가장 큰가가 아니라, generated state, recovery action, navigation route, agent evidence가 "
        "로봇이 소비할 수 있는 검증 가능한 계약으로 남는가입니다."
    ),
    "trend_note": (
        "Generation 20편, Foundation Models 16편, Robot Learning 15편, Efficiency/Systems 14편, Autonomous Driving 13편이 "
        "크지만, robotics 관점의 공통 축은 model family가 아니라 state contract, recovery data, embodiment-aware safety, "
        "and trajectory-level evidence audit입니다."
    ),
    "cluster_specs": [
        {
            "title": "World-action model 평가가 video prior에서 executable kinematic contract로 이동",
            "buckets": ["Generation", "Autonomous Driving", "3D/Scene", "Efficiency/Systems"],
            "ids": ["2607.19876", "2607.20175", "2607.19971", "2607.19919", "2607.19719", "2607.19701", "2607.19528"],
            "needles": ["world model", "world-action", "kinematic", "trajectory", "planning", "diffusion", "prediction", "driving"],
            "why": (
                "KineBench는 generated video를 6D pose와 simulator execution으로 바꾸고, PerceptDrive는 frozen perception prior를 "
                "expert-routed world-action model로 보존합니다. Diffusion ReRoll, Koopman Dreamer, conflict-aware prediction/planning도 "
                "generated future가 downstream action에서 어떤 failure를 만드는지를 묻습니다. APRL은 video score보다 contact realism, "
                "object displacement, trajectory feasibility, real execution correlation을 같은 episode schema로 묶어야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "KineBench와 PerceptDrive는 full-text에서 execution and trajectory metrics를 명시하고, 관련 papers가 같은 state-contract 축으로 모입니다.",
            "lab_action": (
                "RoboCasa/ManiSkill task 3개에서 generated frames, 6D end-effector pose, object displacement, contact event, "
                "next-skill readiness를 같은 episode schema로 저장하고 real/sim execution ranking과 correlation을 측정합니다."
            ),
            "limit": 7,
        },
        {
            "title": "Recovery 학습이 성공 demo 확장에서 failure-state data economy로 이동",
            "buckets": ["Robot Learning"],
            "ids": ["2607.19745", "2607.19633", "2607.19479", "2607.20033", "2607.20345", "2607.20293", "2607.20110", "2607.19804"],
            "needles": ["recovery", "failure", "teleoperation", "clutter", "planning", "single human video", "humanoid", "diffusion policy"],
            "why": (
                "EgoRecovery는 사람이 만드는 egocentric recovery segment가 robot teleoperation보다 failure coverage를 훨씬 싸게 늘릴 수 있음을 보이고, "
                "LENS는 cluttered planning state를 task-relevant abstraction으로 줄입니다. ModPack, single-video skill, retail humanoid "
                "post-training papers까지 묶으면 병목은 policy head가 아니라 어떤 failure를 staging하고 어떤 corrective intent를 기록할지입니다."
            ),
            "confidence": "High",
            "confidence_note": "대표 논문들이 모두 recovery data, task abstraction, teleoperation/post-training interface를 직접 다룹니다.",
            "lab_action": (
                "tabletop 4개 failure family를 정의하고 human egocentric recovery, robot teleop recovery, LENS-style scene abstraction을 "
                "동일 task에서 비교해 valid recovery segments/hour, second-attempt success, unsafe corrective contact를 기록합니다."
            ),
            "limit": 8,
        },
        {
            "title": "Embodied navigation benchmark가 scene split에서 body-aware safety episode로 이동",
            "buckets": ["Embodied AI", "Foundation Models", "Robot Learning", "Autonomous Driving"],
            "ids": ["2607.19695", "2607.19880", "2607.19530", "2607.19827", "2607.19850", "2607.20061", "2607.20116"],
            "needles": ["navigation", "embodiment", "safe", "social navigation", "tracking", "localization", "hospital", "guide dog"],
            "why": (
                "NavVerse는 indoor-to-outdoor transition을 continuous robot execution과 safety metric으로 묶고, EA-Nav는 same observation도 "
                "embodiment geometry에 따라 다른 risky trajectory가 된다고 봅니다. guide dog, hospital physical AI, social navigation, "
                "embodied visual tracking papers를 함께 보면 navigation benchmark의 핵심은 route success가 아니라 body-conditioned risk, "
                "boundary traversal, recovery latency입니다."
            ),
            "confidence": "High",
            "confidence_note": "NavVerse와 EA-Nav의 full text가 embodiment/safety/evaluation contract를 직접 제시합니다.",
            "lab_action": (
                "indoor-to-outdoor route 20개에서 body width/height/token을 바꾼 agent를 평가하고, SR/SPL 외에 clearance violation, "
                "boundary hesitation, unsafe correction, human intervention time을 기록합니다."
            ),
            "limit": 7,
        },
        {
            "title": "Robot-usable geometry가 3D rendering에서 metric state estimator로 이동",
            "buckets": ["3D/Scene", "Autonomous Driving", "Efficiency/Systems", "Safety/Alignment"],
            "ids": ["2607.20232", "2607.20071", "2607.20116", "2607.20417", "2607.19777", "2607.19517", "2607.19711", "2607.20326"],
            "needles": ["odometry", "imu", "3d", "gaussian", "occupancy", "localization", "point cloud", "missing modalities", "segmentation"],
            "why": (
                "DINS-IO는 labeled position 없이 INS consistency로 velocity direction을 회복하고, GaussianSeed/RIM/ATSplat/point-cloud papers는 "
                "3D representation을 planning이나 localization이 소비할 수 있는 state로 바꾸려 합니다. 오늘의 geometry gate는 mesh나 render fidelity가 아니라 "
                "metric drift, relocalization, occupancy, missing-modality recovery, downstream navigation success에 있습니다."
            ),
            "confidence": "Medium-High",
            "confidence_note": "DINS-IO는 full-text metric evidence가 있고, 나머지 3D/AD papers는 parser abstract 기준으로 robot-usable state 축에 연결됩니다.",
            "lab_action": (
                "same indoor/outdoor robot episode traces에서 IMU-only DINS-IO, visual localization, Gaussian/occupancy field를 비교하고 "
                "metric drift, relocalization success, clearance violation, downstream route recovery를 함께 측정합니다."
            ),
            "limit": 8,
        },
        {
            "title": "Multimodal agent reliability가 answer accuracy에서 evidence trajectory audit으로 이동",
            "buckets": ["Foundation Models", "Safety/Alignment", "Efficiency/Systems"],
            "ids": ["2607.19793", "2607.19790", "2607.20092", "2607.20357", "2607.19547", "2607.19515", "2607.19811", "2607.20351"],
            "needles": ["silent failure", "taxonomy", "reasoning", "evidence", "agentic", "token", "compute", "memory", "modality"],
            "why": (
                "Silent Failures는 final answer가 맞아도 retrieval/evidence trajectory가 틀릴 수 있음을 보여주고, Trace, ENTRAP-VL, "
                "Look Less Think Faster, ChronoStitch, BLUE/Lean-SAM2는 reasoning taxonomy, compute budget, visual memory, deployment analytics를 "
                "각각 건드립니다. 로봇 agent로 옮기면 이는 phantom object grounding, stale localization, right-action-wrong-evidence를 잡는 audit layer입니다."
            ),
            "confidence": "High",
            "confidence_note": "Silent Failures full text가 taxonomy, TCR, blank-image stress test를 제시하며 관련 VLM papers가 evidence/compute axis를 보강합니다.",
            "lab_action": (
                "robot agent episode에 sensor evidence, state estimator output, planner rationale, action result를 붙이고 phantom grounding, "
                "stale state, wrong evidence-right action, over-retrieval labels를 100 episodes에 적용합니다."
            ),
            "limit": 8,
        },
        {
            "title": "Safety-critical planning이 single planner output에서 gated conflict and constraint feedback으로 이동",
            "buckets": ["Autonomous Driving", "Efficiency/Systems", "Safety/Alignment", "Robot Learning"],
            "ids": ["2607.19774", "2607.20352", "2607.19971", "2607.19484", "2607.19708", "2607.19599", "2607.19633"],
            "needles": ["safety", "conflict", "planning", "guarantee", "collision", "friction", "actuation", "defer"],
            "why": (
                "Defer to Plan, distributed motion planning with guarantees, conflict-aware prediction/planning, autonomous drifting, contact-persistent actuation, "
                "Coulomb friction splitting은 모두 planner output 자체보다 언제 defer하고, 어떤 constraint가 깨지고, 어떤 conflict가 control로 전파되는지를 봅니다. "
                "LENS까지 포함하면 safety-critical planning은 model capacity보다 feedback surface 설계입니다."
            ),
            "confidence": "Medium",
            "confidence_note": "대표 논문들이 safety guarantees, conflict-aware planning, contact/friction dynamics를 공유하지만 subdomains are heterogeneous.",
            "lab_action": (
                "CARLA-lite/V2X and tabletop-control tasks에서 planner-only, defer-to-plan, conflict-aware planning, constraint-feedback wrappers를 비교해 "
                "collision, false defer, recovery trajectory, constraint violation margin을 측정합니다."
            ),
            "limit": 7,
        },
    ],
    "research_topics": [
        {
            "title": "Action-state contract harness",
            "claim": (
                "generated future를 6D pose, contact, object displacement, route feasibility, next-skill readiness로 정규화해 "
                "real execution success와 correlation을 측정합니다."
            ),
        },
        {
            "title": "Failure-recovery data protocol",
            "claim": (
                "human egocentric recovery와 robot teleop recovery를 같은 failure family에서 수집하고, corrective intent bottleneck과 "
                "planner abstraction의 기여를 분리합니다."
            ),
        },
        {
            "title": "Embodiment-aware navigation safety split",
            "claim": (
                "same route를 body geometry and transition context별로 반복해 clearance violation, boundary hesitation, unsafe correction, "
                "intervention cost를 평가합니다."
            ),
        },
        {
            "title": "Robot silent-failure audit",
            "claim": (
                "final success와 별도로 sensor evidence, state estimate, planner rationale, action trace를 taxonomy label로 점검해 "
                "right-action-wrong-evidence와 phantom grounding을 잡습니다."
            ),
        },
    ],
}


def abstract_card(paper: dict) -> dict:
    """Build a conservative Tier B/C card using only parser-provided abstract text."""
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
        "new": [item for item in RI_DATA["frontier_memory"] if item["signal"] == "new"],
        "strengthening": [item for item in RI_DATA["frontier_memory"] if item["signal"] == "strengthening"],
        "commoditizing": [],
        "contradiction": [],
        "missing_axis": [item for item in RI_DATA["frontier_memory"] if item["signal"] == "missing_axis"],
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
        "2607.19719", "2607.19971", "2607.19919", "2607.19701", "2607.19528",
        "2607.19479", "2607.20033", "2607.20345", "2607.20293", "2607.20110",
        "2607.19530", "2607.19827", "2607.19850", "2607.20061", "2607.20116",
        "2607.20071", "2607.20417", "2607.19777", "2607.19517", "2607.19711",
        "2607.19790", "2607.20092", "2607.20357", "2607.19547", "2607.19515", "2607.19811",
        "2607.19774", "2607.20352", "2607.19484", "2607.19708", "2607.19599",
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
