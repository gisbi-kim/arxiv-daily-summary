#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-08-12 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260812 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-12"


PROFILE = {
    "date": DATE,
    "weekday": "Wed",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching 2026-08-12 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-08-12 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "8월 12일 배치는 로봇 시스템의 핵심 병목이 더 큰 모델이 아니라, 어떤 증거를 믿고 정책, 지도, 캐시, "
        "메모리, 안전 판단을 갱신할지 정하는 문제로 이동했음을 보여준다. Semantic 3DGS grounding, Surgical WAM, "
        "FACT, VIScore, Gated VLA-Cache, estimator spectral analysis, AD2-Bench는 모두 최종 점수보다 update/reject/cache/"
        "retrieve/intervene 결정을 먼저 드러내야 한다고 말한다."
    ),
    "cluster_takeaway": (
        "오늘의 핵심은 더 정확한 perception이나 더 큰 world model이 아니라, evidence가 부족할 때 어떤 subsystem이 "
        "멈추고, 다시 계산하고, 실패 rollout을 학습 신호로 전환하는지를 release gate로 만드는 것이다."
    ),
    "trend_note": (
        "수요일 /new는 180 dedup 중 151편이 ROI에 걸렸고, Foundation Models, Efficiency/Systems, Safety/Alignment, "
        "Robot Learning, Generation이 가장 컸다. 하지만 robotics-relevant signal은 semantic 3D map, world-action model, "
        "cache invalidation, estimator health, evidence-chain benchmark처럼 decision boundary를 명시하는 논문에서 강했다."
    ),
    "cluster_specs": [
        {
            "title": "World-action models shift from plausible futures to failure-conditioned control",
            "buckets": ["Robot Learning", "Autonomous Driving", "Foundation Models", "Generation"],
            "ids": ["2608.11204", "2608.10232", "2608.11174", "2608.10107", "2608.10413", "2608.10744"],
            "needles": ["world-action", "world model", "failure-aware", "planning-relevant", "4d consistent", "future prediction", "failure"],
            "why": (
                "기존 world model 평가는 그럴듯한 미래 영상을 만드는지에 머무르기 쉬웠지만, Surgical WAM과 FACT는 "
                "action-labeled budget, failure rollout, task progress가 실제 control decision을 바꾸는지 묻는다. "
                "VIScore와 4D-WAM은 latent quality와 4D consistency가 planning success와 연결되어야 한다고 압박한다. "
                "APRL 관점에서는 future prediction을 성능 proxy로 쓰기 전에 실패 action이 어떤 recovery decision을 바꿨는지 검증해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "WAM, driving WAM, planning latent metric, failure-aware memory papers가 같은 control-evidence 축에 모인다.",
            "lab_action": "동일 manipulation 또는 driving replay에서 success-only WAM, failure-conditioned WAM, 4D-consistent WAM을 비교하고, task progress 예측이 실제 action 선택을 바꾸는 첫 시점을 측정한다.",
            "limit": 6,
        },
        {
            "title": "VLA deployment needs attack-aware and uncertainty-gated action shortcuts",
            "buckets": ["Robot Learning", "Efficiency/Systems", "Foundation Models", "Safety/Alignment"],
            "ids": ["2608.10393", "2608.10824", "2608.10484", "2608.10835", "2608.10489", "2608.10513"],
            "needles": ["attack", "kv-cache", "action token", "hallucination", "safety", "token pruning", "confidence", "margin"],
            "why": (
                "VLA 배포는 latency를 줄이는 동시에 action decision이 공격이나 불확실성에 흔들리는 순간을 알아야 한다. "
                "DURA는 자연스러운 diffusion patch로 action을 조작하고, Gated VLA-Cache는 action-token margin으로 cache를 무효화하며, "
                "SALT는 action latent가 언어적 의미를 잃는 문제를 제기한다. UniProbe와 SafeCap까지 합치면 배포 최적화는 빠르게 실행하는 문제가 아니라 "
                "언제 재계산하고 언제 action authority를 낮출지 정하는 문제다."
            ),
            "confidence": "High",
            "confidence_note": "attack, cache, action tokenizer, hallucination detector, safety-caption papers가 모두 action-evidence boundary를 건드린다.",
            "lab_action": "VLA replay에서 자연스러운 distractor patch, object swap, motion blur, low-margin action token을 stress split으로 만들고 cache reuse, recompute, action drift, task failure를 함께 비교한다.",
            "limit": 6,
        },
        {
            "title": "Geometry becomes executable scene memory instead of visual reconstruction",
            "buckets": ["3D/Scene", "Embodied AI", "Autonomous Driving", "Generation"],
            "ids": ["2608.10756", "2608.10682", "2608.11077", "2608.10057", "2608.11150", "2608.10286", "2608.10938"],
            "needles": ["gaussian", "3dgs", "semantic", "pose", "driving reconstruction", "geometry", "surround-view", "trajectory"],
            "why": (
                "오늘의 3D/Scene 신호는 rendering 품질 경쟁보다 지도와 action 사이의 interface에 가깝다. "
                "Semantic 3DGS grounding은 object localization, reachability, base positioning, action conditioning을 같은 3D substrate로 묶고, "
                "VGGD와 LGS는 driving reconstruction에서 foundation geometry prior와 primitive intervention을 이용한다. "
                "따라서 3DGS는 보기 좋은 scene asset이 아니라 target choice, pose estimate, map update, downstream navigation을 바꾸는 executable memory로 평가해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "3DGS, pose estimation, feed-forward driving reconstruction, semantic grounding papers가 14편 3D/Scene 안에서 반복된다.",
            "lab_action": "Semantic 3DGS map, feed-forward Gaussian map, pose-estimation map을 target grounding, base-placement feasibility, pose bound, navigation success 기준으로 비교하고 map update를 거부해야 할 조건을 표시한다.",
            "limit": 7,
        },
        {
            "title": "Navigation safety shifts from geometric clearance to introspective risk signals",
            "buckets": ["Embodied AI", "Safety/Alignment", "3D/Scene", "Efficiency/Systems"],
            "ids": ["2608.10623", "2608.10023", "2608.10791", "2608.11175", "2608.10056", "2608.10872", "2608.10485"],
            "needles": ["state estimator", "protection levels", "safety monitoring", "risk-aware", "safety filter", "human following", "tracking"],
            "why": (
                "안전 navigation은 더 작은 clearance threshold를 고르는 문제가 아니라, estimator, pose solver, MPC, safety filter가 언제 자기 판단을 믿을 수 없는지 알려야 하는 문제다. "
                "spectral estimator health, vision-based pose protection level, MPC dual stress, planetary risk-aware planning은 서로 다른 subsystem에서 introspection signal을 만든다. "
                "이 흐름은 APRL이 success/failure만 보지 말고 warning lead time과 intervention trigger를 동시에 평가해야 함을 뜻한다."
            ),
            "confidence": "High",
            "confidence_note": "estimator, pose integrity, MPC monitor, risk planner, safety filter papers가 같은 runtime warning 축을 형성한다.",
            "lab_action": "동일 navigation route에서 estimator spectrum, pose protection level, MPC multiplier stress, safety-filter activation을 동기화하고 false alarm budget을 맞춘 뒤 warning lead time과 recovery success를 비교한다.",
            "limit": 7,
        },
        {
            "title": "Urban and embodied reasoning benchmarks grade evidence chains before final answers",
            "buckets": ["Foundation Models", "Embodied AI", "Safety/Alignment", "Autonomous Driving"],
            "ids": ["2608.10954", "2608.10317", "2608.10278", "2608.10817", "2608.10764", "2608.10618"],
            "needles": ["evidence", "reasoning", "spatial", "traffic anomaly", "object navigation", "counterfactual", "chain"],
            "why": (
                "AD2-Bench와 TAR/TAR-Bench는 final answer가 맞았는지보다 어떤 visual evidence chain으로 결론에 도달했는지를 묻는다. "
                "Chain of Spatial Thoughts와 AECNav는 spatial token, evidence consolidation, target confirmation을 통해 navigation과 embodied reasoning에도 같은 기준을 적용한다. "
                "APRL은 language explanation을 신뢰하기 전에 evidence region을 제거하거나 바꿨을 때 action, route, hazard response가 어떻게 변하는지 측정해야 한다."
            ),
            "confidence": "Medium-High",
            "confidence_note": "urban MLLM benchmark, traffic anomaly reasoning, spatial grounding, object navigation papers가 evidence-chain 평가를 공유한다.",
            "lab_action": "urban scene과 ObjectNav episode에서 evidence region removal, distractor object, adverse weather, spatial-token ablation을 만들고 answer accuracy보다 action/route 변화와 recovery를 먼저 평가한다.",
            "limit": 6,
        },
        {
            "title": "Long-horizon robots need revisable memory with explicit trust boundaries",
            "buckets": ["Generation", "Embodied AI", "Foundation Models", "Robot Learning", "Safety/Alignment"],
            "ids": ["2608.10449", "2608.10949", "2608.10439", "2608.10744", "2608.10817", "2608.11174"],
            "needles": ["persistent", "memory", "streaming", "4d worlds", "long-horizon", "active graph", "dynamic"],
            "why": (
                "long-horizon service robot과 streaming video/world model 논문은 과거 정보를 길게 붙잡는 것보다 무엇을 stable baseline으로 남기고 무엇을 delta event로 갱신할지 묻는다. "
                "PBD-AG는 stable fixture와 dynamic object event를 분리하고, StreamFlow와 Stream Forcing은 streaming memory가 시간에 따라 유지되어야 할 evidence를 다룬다. "
                "이 축은 APRL이 memory length를 늘리는 경쟁보다 map belief, object identity, support relation, temporal evidence의 trust boundary를 소유해야 함을 보여준다."
            ),
            "confidence": "Medium",
            "confidence_note": "service-robot active graph와 streaming/4D video papers가 장기 memory update 문제로 연결되지만 공통 benchmark는 아직 약하다.",
            "lab_action": "장기 household route에서 fixture baseline, moved-object delta, visibility support, object identity drift를 분리하고, memory update가 target finding과 manipulation success를 바꾸는지 평가한다.",
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Failure-conditioned WAM evaluation grid",
            "claim": "성공 demo만 학습한 WAM과 failure rollout을 포함한 WAM을 같은 action-label budget에서 비교하고, progress prediction이 recovery action을 얼마나 먼저 바꾸는지 측정한다.",
        },
        {
            "title": "Introspective shortcut release gate",
            "claim": "VLA cache, estimator, pose solver, MPC monitor가 내놓는 internal warning signal을 한 replay에 맞춰 latency 절감과 unsafe action lead time을 같이 평가한다.",
        },
        {
            "title": "Evidence-chain robot memory benchmark",
            "claim": "Semantic 3DGS map, ObjectNav belief, urban-scene reasoning trace에서 evidence를 제거하거나 왜곡해 target choice, base pose, route, hazard response가 바뀌는지 검증한다.",
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
        "meaning": "Included because it supports today's evidence-contract and introspective release-gate thesis.",
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
