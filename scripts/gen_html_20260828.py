#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-08-28 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260828 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-28"


PROFILE = {
    "date": DATE,
    "weekday": "Fri",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching 2026-08-28 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-08-28 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "The 2026-08-28 batch is about evidence arriving early enough to change a robot or visual reasoner's next move. "
        "VLA papers expose configured failure residuals, retry/reset recovery, ordered execution history, online reward grounding, safe termination, and streaming action decoding as control variables rather than after-the-fact explanations. "
        "World-model papers ask whether cross-embodiment dynamics, causal action-state sequences, revisit memory, probabilistic alignment, and dynamic scene generation preserve state that a controller can use. "
        "Geometry and localization papers make map validity depend on pose, calibration, LiDAR sparsity, contact, multi-agent alignment, and onboard compute budgets. "
        "VLM and deployment papers push evidence retrieval, grounding heads, confidence calibration, token pruning, and edge perception into auditable units so fluent answers or fast inference cannot hide lost visual evidence."
    ),
    "cluster_takeaway": (
        "Today's core is not bigger policies, prettier world models, or cheaper tokens; it is whether failure, memory, geometry, and visual evidence can be tested before the system commits to the next action."
    ),
    "trend_note": (
        "Friday /new produced 151 deduplicated non-replacement papers and 125 ROI papers. "
        "Generation and Foundation Models are numerically large, but the strongest APRL signal is the convergence of VLA recovery, world-model memory, robot-usable geometry, certified safety margins, and evidence-preserving inference."
    ),
    "cluster_specs": [
        {
            "title": "Robot policies move from final success to pre-failure recovery and streaming execution variables",
            "buckets": ["Robot Learning", "Safety/Alignment"],
            "ids": ["2608.26578", "2608.26645", "2608.26821", "2608.27384", "2608.27079", "2608.26571", "2608.26673"],
            "needles": [
                "vla", "failure", "retry", "reset", "temporal", "streaming", "action decoding",
                "online reinforcement", "safe goal-conditioned", "one-bit", "predictive-coding",
            ],
            "why": (
                "기존 robot policy 평가는 episode가 끝난 뒤 success/fail을 세는 데 머물기 쉬웠다. "
                "TrapVLA는 실패 자체를 설정 가능한 action residual로 만들고, FLARE는 retry와 reset을 online arbitration 문제로 분리하며, TemporalFlow-VLA와 FlashVLA는 과거 실행 순서와 streaming chunk가 다음 action을 바꿀 수 있음을 묻는다. "
                "APRL은 terminal success만 보지 말고 failure mode identity, recovery lead time, history-order dependence, asynchronous action discontinuity를 같은 rollout 안에서 비교해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Six robot papers independently expose failure shape, recovery branch, execution history, online reward, safe termination, and streaming latency as action variables.",
            "lab_action": (
                "LIBERO/RoboTwin contact tasks에서 configured trigger, missed grasp, dropped object, shuffled execution history, sparse reward, streaming chunk delay를 독립 stress condition으로 두고 action residual, recovery switch timing, contact error, terminal success를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "World models shift from plausible rollouts to memory, alignment, and embodiment contracts",
            "buckets": ["Generation", "Robot Learning", "Embodied AI", "Safety/Alignment"],
            "ids": ["2608.27406", "2608.27033", "2608.26239", "2608.27073", "2608.27328", "2608.27345", "2608.26200", "2608.26947"],
            "needles": [
                "world model", "world action", "cross-embodiment", "causal autoregressive",
                "revisit", "probabilistic", "spatialcrafter", "dynamic embodied", "gamewam", "wall-ss",
            ],
            "why": (
                "video world model은 자연스러운 frame을 만드는 것만으로 robot simulator가 되지 않는다. "
                "CLAP과 Riemann-1.0은 action representation과 embodiment를 causal state transition으로 맞추려 하고, R2M-Bench와 PAWBench는 revisit memory와 outcome distribution이 generic temporal stability와 구분되는지 묻는다. "
                "APRL은 rollout similarity 대신 object state, action-conditioned future, leave-and-return memory, stochastic outcome distribution이 downstream control 판단을 바꾸는지 평가해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Seven world-model papers connect cross-embodiment action spaces, causal WAMs, revisit controls, probabilistic alignment, and dynamic embodied scenes.",
            "lab_action": (
                "같은 manipulation/navigation scene에서 embodiment, action parameterization, return trajectory, stochastic outcome, 3D proxy quality를 바꿔 world-model rollout을 만들고 future object pose, memory gain, action correction value, failure prediction을 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "3D and localization papers turn clean reconstruction into robot-usable map release gates",
            "buckets": ["3D/Scene", "Embodied AI", "Safety/Alignment"],
            "ids": ["2608.26589", "2608.26868", "2608.26789", "2608.26383", "2608.26932", "2608.26737", "2608.26888", "2608.27365"],
            "needles": [
                "slam", "localization", "odometry", "calibration", "lidar", "point-cloud",
                "3d gaussian", "reconstruction", "contact-aided", "underwater", "compute-platform",
            ],
            "why": (
                "3D reconstruction이 예쁜 novel view를 만들더라도 robot이 그 map으로 localization, grasp, navigation을 못 하면 deployment evidence가 아니다. "
                "DPA-I2P, CGS-SLAM, LiDAR calibration, GSSC, contact-aided underwater localization, lab-robot 3D benchmark는 pose, LiDAR sparsity, calibration drift, multi-agent submap alignment, physical contact, compute budget을 release 조건으로 끌어온다. "
                "따라서 APRL의 geometry 평가는 PSNR이나 mIoU만 보지 말고 map을 믿었을 때 route deviation, grasp pose error, drift recovery, onboard latency가 어떻게 변하는지 봐야 한다."
            ),
            "confidence": "High",
            "confidence_note": "3D/Scene has 13 ROI papers and includes SLAM, LiDAR, calibration, contact localization, and laboratory robot compute signals.",
            "lab_action": (
                "3DGS map, point-cloud registration, semantic scene completion, contact-aided factor graph, calibration estimator, feed-forward reconstruction을 pose noise, sparse LiDAR, extrinsic drift, underwater feature scarcity, onboard compute limit에서 localization drift, route deviation, grasp error, recovery time으로 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "VLM reasoning moves from fluent answers to auditable evidence retrieval and calibration units",
            "buckets": ["Foundation Models", "Safety/Alignment", "Efficiency/Systems"],
            "ids": ["2608.26355", "2608.27417", "2608.26993", "2608.26856", "2608.27004", "2608.26382", "2608.27154", "2608.26716"],
            "needles": [
                "evidence", "retrieval heads", "visual retrieval", "grounded", "calibration",
                "benchmark", "visual text", "layout", "vqa", "rubric", "faithfully",
            ],
            "why": (
                "VLM이 그럴듯한 문장을 만들면 reasoning이 된 것처럼 보이지만, robot이나 의료·문서 workflow에서는 어떤 visual evidence가 답을 허가했는지 확인해야 한다. "
                "PACE는 option-discriminative cue를 찾고, Retrieval Heads Meet Vision은 grounding을 담당하는 attention heads를 causal하게 찾으며, Aphanta, MedREAL, MVC-Bench, ReViCo는 visual intermediate, pixel grounding, confidence calibration, visual text correction을 검증 단위로 만든다. "
                "APRL은 answer accuracy보다 evidence hit rate, unsupported-object rate, calibration error, action-permission error를 같이 봐야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Eight VLM papers share evidence retrieval, causal grounding heads, visual intermediates, pixel grounding, calibration, and visual-text benchmarks.",
            "lab_action": (
                "Long-video QA, referring expression, visual text, medical VQA, layout, robot grounding cases에서 direct answer와 evidence-unit answer를 비교하고 cue recall, referent hit rate, unsupported visual claim, confidence miscalibration, downstream action-permission error를 평가한다."
            ),
            "limit": 6,
        },
        {
            "title": "Autonomy certification shifts from closed-course pass/fail to public-road and clearance guarantees",
            "buckets": ["Autonomous Driving", "Safety/Alignment"],
            "ids": ["2608.26669", "2608.26533", "2608.26759", "2608.27085", "2608.27271", "2608.27151"],
            "needles": [
                "public-road", "assisted lane change", "safety clearance", "conformal",
                "multi-agent", "warehouse", "fleet", "scheduling", "fixture", "trajectory",
            ],
            "why": (
                "자율시스템 검증을 proving ground success나 평균 planner score로 끝내면 실제 운영에서 남는 legal, clearance, congestion, fleet-value risk를 놓친다. "
                "Assisted lane change public-road test는 승인 시나리오 밖의 regulatory distance violation을 보이고, conformal safety clearance는 plan-time margin과 realized clearance의 차이를 certificate로 다루며, MAPD haven, bucket brigade, MAV scheduling은 multi-robot operation에서 병목과 blocking을 별도 guarantee로 만든다. "
                "APRL은 closed-loop success와 함께 clearance certificate, reservation feasibility, local load balance, scientific-value objective를 trajectory-level로 비교해야 한다."
            ),
            "confidence": "Medium",
            "confidence_note": "Six autonomy papers share deployment certification and operations guarantees, though domains range from driving to warehouse and marine fleets.",
            "lab_action": (
                "Public-road lane-change, dense-warehouse pickup, fixture transition, and marine-fleet scenarios에서 plan-time margin, realized clearance, waiting blockage, local load transfer, mission-value loss를 stress split으로 만들고 guarantee violation과 recovery cost를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Deployment efficiency moves from cheaper tokens to preserving action-critical visual evidence",
            "buckets": ["Efficiency/Systems", "Foundation Models", "3D/Scene", "Generation"],
            "ids": ["2608.27206", "2608.26806", "2608.26965", "2608.26948", "2608.26720", "2608.26724", "2608.27198", "2608.26644", "2608.27181"],
            "needles": [
                "token pruning", "condense", "extract", "clusterattention", "compression",
                "low-latency", "edge", "event streams", "continual learning", "semantic communication",
            ],
            "why": (
                "edge deployment에서 inference가 빨라졌다는 사실만으로 perception이 믿을 만해진 것은 아니다. "
                "PACE와 multi-image token pruning은 visual token budget을 줄이면서 holistic context와 detail을 보존하려 하고, KISS-GS와 ClusterAttention은 어떤 compression component와 attention cluster가 실제 gain을 만드는지 분해하며, event-stream discovery, sparse continual transformers, semantic NOMA는 latency, memory, bandwidth 조건을 현장 perception과 연결한다. "
                "APRL은 speedup이나 file size 대신 pruning 뒤에도 localization cue, object boundary, anomaly region, action-relevant context가 남는지 비교해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Nine efficiency papers connect token pruning, attention clustering, 3DGS compression, event perception, continual learning, and semantic communication.",
            "lab_action": (
                "VLM token pruning, attention clustering, 3DGS compression, event-stream object discovery, sparse continual learning, semantic communication을 같은 robot perception cases에서 latency, bandwidth, memory, localization cue retention, object-boundary error, action-choice delta로 비교한다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Configured VLA failure recovery grid",
            "claim": (
                "Combine triggered action residuals, retry/reset skills, temporal-history corruption, online reward grounding, and streaming latency in one rollout-level failure benchmark."
            ),
        },
        {
            "title": "Robot map release-gate benchmark",
            "claim": (
                "Require 3DGS, point-cloud registration, LiDAR completion, factor-graph localization, and feed-forward reconstruction to pass pose, calibration, contact, sparsity, and compute stress."
            ),
        },
        {
            "title": "World-model memory control harness",
            "claim": (
                "Use revisit controls, stochastic outcome repeats, embodiment swaps, and object-state probes to test whether generated futures are actionable rather than merely smooth."
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
        "meaning": "Included because it supports today's evidence-before-commitment thesis.",
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
