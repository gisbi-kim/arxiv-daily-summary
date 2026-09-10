#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-09-10 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260910 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-10"


PROFILE = {
    "date": DATE,
    "weekday": "Thu",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching 2026-09-10 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-09-10 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "The 2026-09-10 batch says robot intelligence is no longer judged by whether a model can produce a plausible command, "
        "but by whether the evidence channel behind that command is credible, calibrated, and still available when control changes. "
        "Robot-learning papers split VLA post-training into hallucination-aware imagined rollouts, verifier credibility, data-curation gradients, "
        "future-representation supervision, frequency-aware action chunks, semantic harnesses, and physical deformable-object benchmarks. "
        "Geometry papers turn 3DGS views, LiDAR degeneracy, monocular metric point clouds, sparse lane maps, and 2D-to-3D diffusion features into "
        "planner-facing uncertainty checks. Driving and field-robot papers make safety a relative-risk, policy-uncertainty, vulnerable-road-user, "
        "routing, and simulation-coverage question. VLM and systems papers then ask whether confidence, token pruning, video hallucination detectors, "
        "chain-of-thought checks, belief states, and privacy boundaries preserve the evidence that authorizes the next answer or action."
    ),
    "cluster_takeaway": (
        "Today's core is not more capable VLA, world-model, or VLM components; it is deciding which verifier, map, token, belief state, or simulation signal is allowed to change a robot action."
    ),
    "trend_note": (
        "Thursday /new produced 153 deduplicated non-replacement papers and 117 ROI papers. "
        "Robot Learning, Generation, Efficiency/Systems, Safety/Alignment, and 3D/Scene all have enough signal, but the APRL-relevant movement is the shared evidence-admission contract: "
        "imagined rollouts, verifier scores, map uncertainty, risk fields, and compressed visual histories must prove what action decision they are allowed to affect."
    ),
    "cluster_specs": [
        {
            "title": "VLA post-training moves from more rollouts to verifier-aware action authority",
            "buckets": ["Robot Learning", "Foundation Models", "Safety/Alignment"],
            "ids": ["2609.09941", "2609.09250", "2609.10021", "2609.09630", "2609.09925", "2609.10405", "2609.10522"],
            "needles": [
                "hallucination-aware", "verifier", "gradient compatibility", "future representation",
                "time-frequency", "frequency-conditioned", "semantic interface", "vision-language-action",
            ],
            "why": (
                "기존 VLA post-training은 더 많은 rollout이나 더 큰 action head가 성능을 올린다고 읽기 쉬웠지만, 이번 묶음은 무엇을 신뢰하고 학습 신호로 쓸지 먼저 묻는다. "
                "HaWMPO는 imagined rollout의 hallucination score를 정책 최적화에 넣고, No Free Checker는 verifier의 availability와 credibility가 trade-off임을 정리한다. "
                "RoboDrop은 post-training sample이 validation gradient와 맞는지 보고, JEPA Policy와 FreqFM/TFGCA는 future representation과 action frequency가 실제 action chunk를 어떻게 바꾸는지 드러낸다. "
                "APRL은 VLA fine-tuning을 success rate만으로 평가하지 말고 verifier source, sample trust, imagined-state reliability, action-frequency failure를 같은 episode에서 분리해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Seven papers independently target hallucinated rollouts, verifier credibility, data curation, future supervision, frequency conditioning, geometric chunk attention, and semantic action interfaces.",
            "lab_action": (
                "LIBERO/RoboCasa와 실제 tabletop task에서 hallucinated future, corrupted demonstration, ambiguous verifier score, high-frequency contact correction, and semantic-command grounding을 stress split으로 만들고 verifier gameability, recovery success, chunk-frequency error, sample-filter precision, final success를 함께 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "World models must separate physics, habit, and generated plans before control",
            "buckets": ["Generation", "Robot Learning", "3D/Scene"],
            "ids": ["2609.09210", "2609.10506", "2609.09597", "2609.10050", "2609.10540", "2609.10464", "2609.10531", "2609.09828"],
            "needles": [
                "world model", "physics", "habit", "latent planning", "tactile", "generated videos",
                "programmable world", "partial observations", "vision feedback",
            ],
            "why": (
                "World model이라는 이름만으로는 policy training, latent planning, simulation tracking, tactile correction, or programmable state 중 무엇을 책임지는지 알 수 없다. "
                "Identifying Habit, Physics, and Nuisance는 teleoperation data에서 operator habit과 shared physics를 분리하고, DUET-DINO는 cross-view latent prediction을 7-DoF planning에 연결한다. "
                "Compact Visuotactile World Models와 generated video plan grounding은 tactile/visual prediction이 실제 control decision으로 들어오는 시점을 묻고, Programmable World Model과 Semigroup-JEPA는 explicit state evolution과 physics parameter conditioning을 분리한다. "
                "APRL은 imagined future가 planner prior, verifier, tactile correction, physics simulator, or playable state machine 중 어느 권한을 갖는지 역할별 gate를 세워야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Eight papers share a world-model authority question across VLA planning, tactile lifting, video plans, programmable state, physics generalization, partial 3D observations, and real-to-sim adaptation.",
            "lab_action": (
                "Manipulation and navigation suites에서 habit-shuffled demonstrations, cross-view occlusion, tactile-force mismatch, generated HOI references, partial-geometry guidance, and programmable off-screen state를 ablation하고 planner success, force-budget violation, state-count accuracy, physical-parameter error, recovery improvement를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Geometry evaluation shifts from render quality to uncertainty and degeneracy contracts",
            "buckets": ["3D/Scene", "Autonomous Driving", "Efficiency/Systems"],
            "ids": ["2609.10307", "2509.06285", "2609.10336", "2609.10322", "2609.09394", "2609.09491", "2609.10095", "2609.10376"],
            "needles": [
                "conformal prediction", "degenerate lidar registration", "drift correction", "lane geometry",
                "metric pointcloud", "camera poses", "gaussian splatting", "sparse-view", "uncertainty",
            ],
            "why": (
                "3D/SLAM/reconstruction 평가는 visual fidelity나 평균 pose error만으로 robot deployment risk를 설명하기 어렵다. "
                "View-Structured Conformal Prediction은 pixel coverage와 view-event coverage의 차이를 드러내고, DCReg는 LiDAR registration에서 어느 physical motion direction이 unconstrained인지 해석한다. "
                "OSM lane geometry drift correction, OmniPoint, learned global camera poses, LinearMask-GS, and LiDAR diffusion feature bridge는 모두 sparse prior, camera model, pruning, diffusion feature가 planner가 먹을 수 있는 evidence인지 묻는다. "
                "APRL geometry 평가는 relocalization success, view-level uncertainty, degeneracy direction, map-prior failure, and downstream action change를 같은 protocol 안에서 검증해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Eight geometry papers connect 3DGS uncertainty, LiDAR degeneracy, lane-map priors, monocular point clouds, pose graphs, pruning, and LiDAR diffusion features to action-facing validity.",
            "lab_action": (
                "Corridor, sparse-view room, fisheye camera, lane-map route, and cluttered tabletop scenes에서 view coverage, LiDAR degeneracy axis, OSM prior alignment, ray-distance geometry, pose-graph noise, Gaussian pruning, and LiDAR diffusion features를 바꿔 relocalization failure, collision-query precision, wrong-turn rate, endpoint feasibility를 평가한다."
            ),
            "limit": 6,
        },
        {
            "title": "Autonomy safety moves into relative risk, uncertainty, and scenario-coverage tests",
            "buckets": ["Autonomous Driving", "Safety/Alignment", "Embodied AI"],
            "ids": ["2609.10377", "2609.09650", "2609.09881", "2609.10139", "2609.09752", "2609.10400", "2609.10484", "2609.10433"],
            "needles": [
                "risk", "uncertainty-aware", "camera-lidar fusion", "vulnerable road users", "driver gaze",
                "agv routing", "traffic management", "holoocean", "uav exploration",
            ],
            "why": (
                "Autonomous driving과 field robotics의 안전성은 offline perception score가 아니라 어떤 rare scenario에서 control이 어떻게 달라지는지로 판단해야 한다. "
                "DRiF는 handcrafted absolute risk 대신 pairwise relative risk를 end-to-end planning에 붙이고, RUDC는 policy uncertainty에 따라 safety correction strictness를 바꾼다. "
                "CLFTv2는 vulnerable road user recall을 real-time camera-LiDAR fusion으로 다루고, TransGaze-Object, AGV routing, narrow industrial traffic management, and HoloOcean은 gaze, fleet routing, mixed-vehicle coordination, marine simulation coverage를 safety evidence로 만든다. "
                "APRL field-robot 평가는 risk order, uncertainty-triggered intervention, sensor-fusion failure, route congestion, and simulation-to-field coverage를 closed-loop scenario 안에서 비교해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Eight papers connect driving risk, uncertainty-aware control, VRU fusion, driver gaze, AGV routing, industrial traffic, marine simulation, and UAV exploration to scenario-level safety.",
            "lab_action": (
                "CARLA/Bench2Drive-style scenes, warehouse AGV layouts, and HoloOcean/coastal robot scenarios에서 relative risk label, ensemble uncertainty, LiDAR return density, VRU class imbalance, gaze-object cue, routing congestion, and communication delay를 ablation하고 collision rate, intervention count, near-miss severity, throughput, mission coverage를 평가한다."
            ),
            "limit": 6,
        },
        {
            "title": "VLM reliability shifts from confidence to evidence order and belief-state consistency",
            "buckets": ["Foundation Models", "Safety/Alignment", "Efficiency/Systems"],
            "ids": ["2609.09184", "2609.09206", "2609.09895", "2609.09790", "2609.09692", "2609.10036", "2609.09417"],
            "needles": [
                "evidence-order", "hallucinate", "hallucination detectors", "hazard identification",
                "chain-of-thought", "belief-state", "rubric-grounded", "calibration",
            ],
            "why": (
                "VLM judge와 robot reasoning을 confidence 하나로 맡기면 어떤 visual evidence가 사라졌을 때 판단이 무너지는지 알 수 없다. "
                "Evidence-Order Calibration은 question-critical evidence가 사라질 때 confidence가 monotonic하게 떨어지는지 보고, HEAL은 hallucination을 synergy head의 information drift로 해석한다. "
                "VidHalLoc은 hallucination detector 자체의 신뢰도를 평가하고, LogiScope-VQA와 CT-SAFR는 warehouse hazard reasoning and robot CoT faithfulness를 deployment gate로 만든다. "
                "Belief-State Engine은 partial observability에서 raw history 대신 posterior를 LLM에 주는 구조를 제안하므로, APRL은 VLM reasoning을 evidence order, detector credibility, belief calibration, and unsafe-action refusal로 검증해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Seven papers target evidence monotonicity, hallucination mechanisms, detector reliability, logistics hazards, CoT verification, belief states, and rubric-grounded verification.",
            "lab_action": (
                "Robot video QA, warehouse hazard scenes, and partially observable planning tasks에서 critical-region masking, synergy-head calibration, hallucination-detector disagreement, CoT verifier failure, posterior/raw-history exposure, and rubric grounding을 intervention으로 두고 answer flip, belief calibration, unsafe-action refusal, detector precision을 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Efficiency becomes irreversible evidence admission under token, cache, and sensor budgets",
            "buckets": ["Efficiency/Systems", "Foundation Models", "Safety/Alignment", "Generation", "Robot Learning"],
            "ids": ["2609.10297", "2609.10346", "2609.10355", "2609.09188", "2609.10018", "2609.09234", "2609.09413"],
            "needles": [
                "token pruning", "cache", "inference-efficiency", "lensless gaze", "elastic model",
                "compact target-centric", "active learning", "visual tokens", "privacy",
            ],
            "why": (
                "Efficiency 논문은 latency와 FLOPs만 줄였다고 끝나지 않고, 줄인 정보가 나중 action에 필요한 evidence였는지 설명해야 한다. "
                "TRACE는 GUI trajectory에서 버린 token을 cache 때문에 되돌릴 수 없다고 보고 evidence admission order를 세우며, VIP-Router는 sample별 pruning strategy를 고른다. "
                "VideoLLM efficiency survey, lensless gaze privacy audit, Elastoformer, compact UAV servoing, and decision-focused active learning은 각각 frame/token cost, identity leakage, runtime mode switching, target-centric cue sufficiency, and scale-aware process decisions를 다룬다. "
                "APRL은 edge robot perception을 cost curve만으로 고르지 말고 decisive-cue retention, privacy leakage, thermal/runtime mode, and downstream control error를 함께 봐야 한다."
            ),
            "confidence": "Medium-High",
            "confidence_note": "Seven papers share evidence admission under runtime, cache, token, privacy, target-cue, and decision-cost constraints, though task domains are broad.",
            "lab_action": (
                "Streaming robot video, GUI-like control panels, UAV servoing, and wearable/XR sensing episodes에서 token budget, KV contraction, sample-adaptive pruning, gaze representation, elastic runtime mode, target-cue dimension, and active-learning query를 ablation하고 decisive-cue recall, latency, privacy attack success, control error, task utility를 비교한다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Verifier credibility grid for robot post-training",
            "claim": (
                "Evaluate imagined rollout scores, learned rewards, formal monitors, gradient-compatible samples, and human labels against the same failure and reward-hacking episodes."
            ),
        },
        {
            "title": "Planner-facing geometry uncertainty benchmark",
            "claim": (
                "Compare 3DGS uncertainty, LiDAR degeneracy directions, sparse lane-map correction, monocular metric point clouds, and LiDAR diffusion features by downstream navigation failures."
            ),
        },
        {
            "title": "World-model role separation harness",
            "claim": (
                "Force each world model to declare whether it is physics state, operator habit, tactile correction, generated plan, programmable state, or partial-observation guide."
            ),
        },
        {
            "title": "Irreversible evidence admission test",
            "claim": (
                "Measure token pruning, KV contraction, frame sampling, CoT verification, belief filtering, and privacy-preserving sensing by the action-critical evidence they keep or discard."
            ),
        },
    ],
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def all_papers(classified: dict) -> list[dict]:
    rows = []
    for bucket, info in classified.get("buckets", {}).items():
        for paper in info.get("papers", []):
            q = dict(paper)
            q["bucket"] = bucket
            rows.append(q)
    return rows


def abstract_card(paper: dict, ri_lookup: dict) -> dict:
    text = " ".join(str(paper.get("abstract", "")).split())
    return {
        "arxiv_id": paper.get("arxiv_id"),
        "title": paper.get("title"),
        "bucket": paper.get("bucket"),
        "reading_depth": ri_lookup.get(paper.get("arxiv_id"), "abstract-only"),
        "problem": text[:360],
        "method": "See Research Intelligence edition for abstract evidence trace and falsification note.",
        "meaning": "Included because it supports today's evidence-contract and action-authority thesis.",
    }


def enrich_insights() -> None:
    insights_path = ROOT / "insights" / f"{DATE}.json"
    trends = load_json(ROOT / "trends" / f"{DATE}.json")
    insights = load_json(insights_path)
    classified = load_json(ROOT / "out" / "classified.json")
    papers = all_papers(classified)
    by_id = {p["arxiv_id"]: p for p in papers}
    ri = RI_BY_DATE[DATE]
    ri_ids = [paper["arxiv_id"] for paper in ri["papers"]]
    ri_lookup = {paper["arxiv_id"]: paper["status"] for paper in ri["papers"]}

    insights["source_listing_date"] = trends["source_listing_date"]
    insights["source_mode"] = trends["source_mode"]
    insights["daily_new_counts"] = trends["daily_new_counts"]
    insights["paper_autopsies"] = [abstract_card(by_id[pid], ri_lookup) for pid in ri_ids if pid in by_id]
    insights["frontier_memory"] = ri["frontier_memory"]
    insights["strategy_board"] = ri["strategy"]
    insights["tiering_note"] = (
        "Research Intelligence uses repository parser abstracts for selected Tier A papers. "
        "No figure/table/full-text claims are asserted in this conservative automation run."
    )
    insights["research_intelligence"] = {
        "html": f"posts/{DATE}-research-intelligence.html",
        "json": f"intelligence/{DATE}.json",
        "source_prompt": ri["source_prompt"],
    }
    write_json(insights_path, insights)


def add_ri_callout() -> None:
    post_path = ROOT / "posts" / f"{DATE}.html"
    doc = post_path.read_text(encoding="utf-8")
    if "ri-callout" in doc:
        return
    doc = doc.replace(
        ".thesis strong{color:#fef08a}",
        ".thesis strong{color:#fef08a}.ri-callout{display:flex;justify-content:space-between;gap:16px;align-items:center;margin:-12px 0 28px;padding:14px 18px;border:1px solid #67e8f9;border-radius:10px;background:#ecfeff;color:#164e63}.ri-callout a{font-weight:750;white-space:nowrap}@media(max-width:760px){.ri-callout{align-items:flex-start;flex-direction:column}}",
    )
    ri = RI_BY_DATE[DATE]
    ri_callout = (
        f"<section class=\"ri-callout\"><span><strong>Today's Research Intelligence</strong> "
        f"Tier A {len(ri['papers'])} papers are conservative abstract-only cards with evidence traces, "
        f"adversarial reads, frontier memory, and APRL strategy board.</span>"
        f"<a href=\"{DATE}-research-intelligence.html\">Open Research Intelligence</a></section>"
    )
    doc = re.sub(r"</section>\n(<h2>.*?</h2>)", f"</section>\n{ri_callout}\n\\1", doc, count=1, flags=re.S)
    post_path.write_text(doc, encoding="utf-8", newline="\n")


def main() -> int:
    build(PROFILE, "out/cv_new.json", "out/ro_new.json")
    build_research_intelligence()
    enrich_insights()
    add_ri_callout()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
