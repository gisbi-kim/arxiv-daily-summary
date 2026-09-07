#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-09-07 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260907 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-07"


PROFILE = {
    "date": DATE,
    "weekday": "Mon",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching 2026-09-07 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-09-07 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "The 2026-09-07 batch is about action permission after evidence has been localized. VLA and robot-learning papers stop treating success as a scalar: "
        "FailureSpot, RoboSPA, conditional visual grounding, LIBERO-Recover, TacPAC, and ROBORMBENCH ask when a failure starts, which phase loses the target, "
        "what recovery level is required, whether tactile feedback can still correct the unexecuted action, and whether a reward survives task-equivalent language. "
        "Geometry papers then turn 3DGS, SfM, cross-view depth, scene graphs, and radar-enhanced odometry into robot-facing protocols with goals, collisions, observability, "
        "and localization failure. World-model papers split imagination into physical exploration, trajectory planning, safety-critical scenario generation, contact correction, "
        "and remote-control resilience. VLM and systems papers complete the same pattern by requiring interpretable failure concepts, influential views, foveated evidence, sparse selection, "
        "privacy-aware gaze features, and thermal or hardware budgets to prove that the evidence they keep is the evidence that changes the decision."
    ),
    "cluster_takeaway": (
        "Today's core is not that robots need more data or larger world models; it is that each visual, tactile, geometric, linguistic, and runtime signal must identify the action decision it is allowed to change."
    ),
    "trend_note": (
        "Monday /new produced 138 deduplicated non-replacement papers and 112 ROI papers. Generation and Efficiency/Systems are numerically large, but the APRL signal is the failure-localization contract: "
        "timestamp labels, recovery levels, geometry-derived navigation goals, radar observability switches, physical world-model obligations, and compressed evidence all become release gates."
    ),
    "cluster_specs": [
        {
            "title": "VLA evaluation moves from final success to timed failure and recovery contracts",
            "buckets": ["Robot Learning", "Foundation Models", "Embodied AI"],
            "ids": ["2609.04277", "2609.05324", "2609.05376", "2609.05178", "2609.05401", "2609.05260"],
            "needles": [
                "failure detection", "recover", "spatial-procedural", "conditional visual grounding",
                "paraphrase", "same trajectory", "different action", "timestamp-level",
            ],
            "why": (
                "기존 VLA 평가는 terminal success가 높으면 배포 가능성도 높다고 읽기 쉬웠지만, 이번 묶음은 실패가 어느 시점에 시작됐고 어떤 회복 행동이 필요한지 묻는다. "
                "FailureSpot은 trajectory label이 pre-failure 동작을 오염시킨다고 보고 timestamp supervision으로 옮기며, RoboSPA와 conditional visual grounding은 공간 난이도와 phase-specific distractor를 분리한다. "
                "LIBERO-Recover와 ROBORMBENCH는 성공률 포화 뒤에 recovery level과 paraphrase-stable reward가 비어 있음을 보여주므로, APRL VLA 평가는 task success와 별도로 failure onset, recovery depth, language invariance를 같은 episode에서 평가해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Six papers independently target failure timing, spatial-procedural difficulty, phase grounding, recovery, reward paraphrases, and executable language decisions.",
            "lab_action": (
                "LIBERO/RoboCasa와 실제 tabletop task에서 object distractor, state-changing failed grasp, action pause, task-preserving paraphrase, multi-constraint instruction을 stress split으로 만들고 timestamp-level failure AUC, recovery action accuracy, reward invariance, final success를 함께 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Geometry becomes a robot benchmark substrate instead of a reconstruction artifact",
            "buckets": ["3D/Scene", "Autonomous Driving", "Foundation Models", "Embodied AI"],
            "ids": ["2609.04602", "2609.05325", "2609.04381", "2609.05210", "2609.04718", "2609.05397", "2609.04607", "2609.04965"],
            "needles": [
                "3d gaussian splatting", "navigation", "odometry", "radar", "bundle adjustment",
                "structure-from-motion", "scene graph", "cross-view localization", "surround depth",
            ],
            "why": (
                "3D representation은 더 예쁜 novel view를 만드는 데서 끝나면 로봇 행동을 승인할 근거가 되지 못한다. "
                "NavArena는 3DGS를 goal, traversability, collision query가 있는 navigation benchmark로 바꾸고, FIRE-LIVWO는 smoke, dust, repeated corridor에서 observability를 보고 modality weight를 바꾼다. "
                "BLASt3R, HiSfM, CrossDepth, CAD-free 3D priors, open-set scene graph papers는 모두 geometry가 pose, goal, object identity, depth, and semantic action을 얼마나 안정적으로 지탱하는지 묻는다. "
                "따라서 APRL geometry 평가는 reconstruction loss보다 closed-loop navigation failure, relocalization, collision validity, and object-goal execution으로 설계해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Eight geometry papers connect 3DGS, SfM, BA, odometry, scene graphs, cross-view localization, and multi-view depth to robot-facing protocols.",
            "lab_action": (
                "Lab corridor, outdoor route, and cluttered tabletop scenes에서 3DGS-derived occupancy, BLASt3R/HiSfM reconstruction, CrossDepth surround estimates, radar-enhanced odometry, open-set scene graph goals를 비교하고 collision query precision, relocalization success, goal-reaching, pose drift, semantic-goal failure를 평가한다."
            ),
            "limit": 6,
        },
        {
            "title": "World models split into planning priors, stress generators, and contact-time correctors",
            "buckets": ["Generation", "Autonomous Driving", "Robot Learning"],
            "ids": ["2609.04911", "2609.04921", "2609.05266", "2609.04958", "2609.04851", "2609.05416"],
            "needles": [
                "world model", "physical", "trajectory planning", "scenario generation", "tactile",
                "action correction", "remote robotic control", "camera and hand motion",
            ],
            "why": (
                "World model을 단순 future video로 쓰면 계획, 검증, 회복 중 어떤 권한을 주는지 흐려진다. "
                "TourPhysics는 simulator state와 generated observation을 분리하고, driving diffusion prior는 planner와 long-tail scenario generator라는 두 역할을 동시에 맡긴다. "
                "TacPAC은 predicted tactile contact를 실행 중 correction으로 바꾸며, MINT와 wireless world-model work는 egocentric trajectory supervision과 remote-control resilience로 같은 질문을 넓힌다. "
                "APRL은 imagined future가 planner ranking, stress-test coverage, contact correction, or remote fallback 중 무엇을 바꿨는지 역할별로 검증해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Six papers define world models as physical exploration, driving priors, tactile correction, egocentric motion estimation, remote control, and compositional-world generation.",
            "lab_action": (
                "Manipulation, navigation, and driving toy suites에서 simulator-state commitment, diffusion guidance energy, tactile-cache correction, egocentric trajectory supervision, wireless link perturbation을 ablation하고 planner degradation, generated scenario transfer, contact recovery, trajectory error, communication fallback success를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "VLM reliability moves from confidence to mechanism-level failure explanation",
            "buckets": ["Foundation Models", "Safety/Alignment", "Efficiency/Systems"],
            "ids": ["2609.04276", "2609.04281", "2609.05388", "2609.05224", "2609.05149", "2609.05174"],
            "needles": [
                "failure prediction", "sparse autoencoders", "visual dominance", "deferral",
                "neuro-symbolic", "prioritize", "causal information flow", "self-explainable",
            ],
            "why": (
                "Confidence score 하나로 VLM을 맡기면 모델이 왜 틀리는지, 언제 사람이나 규칙으로 넘겨야 하는지 알 수 없다. "
                "FailSAE는 sparse latent concept으로 failure prediction을 설명하려 하고, visual dominance work는 개인화 safety에서 보는 정보가 아는 정보를 덮을 때 deferral을 넣는다. "
                "Think-Verify-Revise와 First Things First는 reasoning을 검증 가능한 must-have constraint로 나누며, causal information flow와 self-explainable bottleneck work는 판단 경로가 실제 evidence를 통과했는지 묻는다. "
                "APRL은 VLM judge나 reward를 쓸 때 answer confidence가 아니라 latent concept, deferral trigger, logical constraint, and evidence path가 action permission을 바꿨는지 봐야 한다."
            ),
            "confidence": "Medium-High",
            "confidence_note": "Six papers attack VLM failures through sparse concepts, visual dominance, dynamic verification, priority constraints, information flow, and explanatory bottlenecks.",
            "lab_action": (
                "Robot outcome judging, spatial QA, and safety instruction tasks에서 SAE concept shift, visual/text conflict, must-have constraint violation, causal path masking, explanation bottleneck을 intervention으로 두고 answer change, deferral precision, unsafe action refusal, reward ranking stability를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Efficient perception becomes selective evidence admission under privacy, memory, and thermal budgets",
            "buckets": ["Efficiency/Systems", "Foundation Models", "Safety/Alignment"],
            "ids": ["2609.04392", "2609.04698", "2609.04802", "2609.04947", "2609.04592", "2609.04705", "2609.05161"],
            "needles": [
                "foveated", "sparse vision", "long-horizon spatial memory", "chain-of-thought compression",
                "gaze", "privacy", "thermal throttling", "hardware-efficient", "token",
            ],
            "why": (
                "Efficiency는 적은 token이나 낮은 latency만으로는 충분하지 않고, 버린 정보가 robot decision에 필요한 evidence였는지 설명해야 한다. "
                "FAVE와 LookThere는 어디를 볼지 고르고, LTE는 장시간 object trajectory를 language-queryable memory로 압축하며, MCPO는 visual-independent reasoning step을 제거한다. "
                "Gaze privacy, DVFS, and robot-dynamics accelerator papers add privacy leakage, thermal stability, and hardware precision as deployment constraints. "
                "APRL은 sparse/foveated perception을 decisive-cue recall, long-horizon retrieval, identity leakage, thermal failure, and dynamics error와 함께 평가해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Seven papers connect view selection, sparse tokens, long-horizon memory, multimodal reasoning compression, gaze privacy, thermal DVFS, and robot accelerator budgets.",
            "lab_action": (
                "Streaming robot video and XR/HRI navigation episodes에서 foveation policy, sparse selector budget, language trajectory compression, multimodal CoT pruning, gaze representation, DVFS mode, mixed precision을 바꿔 decisive-cue recall, retrieval success, re-identification leakage, thermal throttling, control error를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Human-facing embodiment exposes language, gesture, gaze, and crowd state as action variables",
            "buckets": ["Embodied AI", "Robot Learning", "Efficiency/Systems", "Autonomous Driving"],
            "ids": ["2609.05300", "2609.05133", "2609.04545", "2609.04438", "2609.05282"],
            "needles": [
                "crowds", "schema bounded", "gesture", "identity reasoning", "handover", "human-robot",
                "social", "bimanual", "navigation",
            ],
            "why": (
                "Human-facing robot은 language plan, crowd interaction, gesture perception, long-term identity memory, and tactile handover가 서로 다른 속도로 action을 바꾸는 시스템이다. "
                "H2INT는 crowded navigation에서 human-human and human-robot interaction state를 모델링하고, schema-bounded policy refinement는 LLM reasoning을 local learning보다 느린 정책 수준에 묶는다. "
                "SocioGesture, ICM-Bench, and tactile bimanual handover papers show that social gesture, identity memory, and compliance cues cannot be reduced to final task completion. "
                "APRL은 사람 주변 task에서 semantic instruction, social signal, and tactile compliance가 언제 local controller 권한을 바꾸는지 단계별로 분리해야 한다."
            ),
            "confidence": "Medium",
            "confidence_note": "Five papers share human-facing action variables, though benchmarks span navigation, gesture, identity memory, and handover.",
            "lab_action": (
                "Crowded navigation, handover, and social-instruction episodes에서 language policy update rate, crowd-density state, gesture latency, identity-memory horizon, tactile compliance를 독립 조건으로 두고 near-miss, handover force violation, wrong-person action, recovery choice를 평가한다."
            ),
            "limit": 5,
        },
    ],
    "research_topics": [
        {
            "title": "Timestamped VLA failure-recovery grid",
            "claim": (
                "Use the same manipulation episodes to compare timestamp detectors, conditional grounding interventions, recovery policies, tactile correction, and paraphrase-stable rewards."
            ),
        },
        {
            "title": "3DGS-to-navigation validity suite",
            "claim": (
                "Convert reconstructed scenes into goal, collision, semantic map, cross-view depth, and odometry-observability tests that predict real navigation failure."
            ),
        },
        {
            "title": "World-model role separation harness",
            "claim": (
                "Evaluate one learned prior separately as planner, scenario generator, physical-state simulator, tactile correction oracle, and remote-control fallback."
            ),
        },
        {
            "title": "Evidence-accountable efficient perception",
            "claim": (
                "Benchmark foveated views, sparse selectors, memory compression, CoT pruning, gaze privacy, DVFS, and robot accelerator precision by the action evidence they preserve."
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
        "meaning": "Included because it supports today's failure-localization and action-permission thesis.",
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
