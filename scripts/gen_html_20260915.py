#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-09-15 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260915 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-15"


PROFILE = {
    "date": DATE,
    "weekday": "Tue",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching Tuesday 2026-09-15 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching Tuesday 2026-09-15 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "The 2026-09-15 batch says embodied AI is moving from broad capability claims to permissioned evidence. "
        "Affordance and grounding papers ask whether a model knows the target part, the causal image region, and the action-sensitive semantics before it is allowed to act. "
        "Robot-learning papers then turn that diagnosis into deployment contracts: compact outcome states, feasibility critics, action-head alignment, tactile transfer, and metrological evidence gates decide what can authorize execution. "
        "Geometry papers make the same move for maps by separating tracking uncertainty, self-correction timing, aerial-ground anchoring, and radar/LiDAR evidence from visual fidelity alone. "
        "Video, document, and world-model papers expose the runtime version of the problem: more samples, frames, tokens, or retrieved pages matter only if selection converts them into answer or action value. "
        "APRL should build benchmarks where every latent, map, memory, or safety signal must prove which robot decision it is allowed to change."
    ),
    "cluster_takeaway": (
        "Today's core is not larger VLAs, denser maps, or longer context; it is deciding which evidence is permitted to change the next action, map update, navigation commitment, or safety intervention."
    ),
    "trend_note": (
        "Tuesday /new produced 343 deduplicated non-replacement papers and 272 ROI papers. "
        "The volume spike is broad, but the useful signal is narrow: across manipulation, navigation, mapping, video reasoning, and driving, the strongest papers replace aggregate scores with evidence-specific permission tests."
    ),
    "cluster_specs": [
        {
            "title": "Affordance evaluation moves from answer accuracy to evidence-specific action permission",
            "buckets": ["Foundation Models", "Robot Learning", "Embodied AI"],
            "ids": ["2609.13225", "2609.13308", "2609.13228", "2609.13235", "2609.13458", "2609.14219"],
            "needles": [
                "part grounding", "counterfactual", "region labeling", "outcome bottleneck",
                "semantic transfer", "metrological evidence", "affordance", "action sensitivity",
            ],
            "why": (
                "기존 VLM/VLA 평가는 맞은 답이나 최종 행동만 보고 모델이 근거를 제대로 썼다고 읽기 쉬웠다. "
                "이번 묶음은 part identity, region intervention, semantic-action sensitivity, outcome-sufficient representation, and admissible inspection evidence를 따로 떼어 어느 증거가 실제 행동을 바꾸는지 묻는다. "
                "Part Grounding, GroundBench, CSGR, Outcome Bottlenecks, STAGE, and FRAME all turn grounding into a permission test rather than a score. "
                "APRL은 affordance benchmark에서 part, region, instruction semantics, compact state, and measurement provenance를 독립 변수로 두고 action flip과 invalid execution을 평가해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Six papers independently factorize part identity, visual region causality, semantic transfer, outcome state, and admissible evidence.",
            "lab_action": (
                "LIBERO/tabletop inspection tasks에서 target-part swap, causal-region mask, instruction-only semantic swap, outcome-bottleneck size, and evidence-admissibility gate를 ablation하고 action flip, invalid execution, false accept, recovery success, and inspection coverage를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "VLA deployment shifts from model scale to feasibility, latency, and physical-state gates",
            "buckets": ["Robot Learning", "Autonomous Driving"],
            "ids": ["2609.13231", "2609.13984", "2609.13244", "2609.13318", "2609.15726", "2609.15169"],
            "needles": [
                "shieldvla", "efficient vla", "dark manipulation", "3d diffusion policy",
                "visuo-tactile", "grounded reasoning-to-action", "latency", "feasibility",
            ],
            "why": (
                "Robot foundation model 논의는 더 큰 backbone이나 더 많은 demonstration으로 흐르기 쉽지만, 배포에서는 어떤 상태가 실행을 허가하는지가 더 중요하다. "
                "ShieldVLA는 안전 critic으로 feasible region을 나누고, EffVLA는 action-head alignment와 latency를 함께 재며, Physical Kernel과 Attention-DP3는 어둠·clutter에서 어떤 물리/기하 상태가 행동을 유지하는지 본다. "
                "Bench2Dex와 GRAVA는 tactile transfer와 grounded reasoning-to-action을 executable metric으로 끌어온다. "
                "APRL은 VLA를 평균 success 모델이 아니라 feasibility, latency, tactile, geometry, and reasoning evidence가 action authority를 나누는 실행 스택으로 평가해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Safety alignment, action-head scaling, dark manipulation, 3D diffusion policy, tactile benchmark, and driving VLA papers repeat the same deployment-contract decision.",
            "lab_action": (
                "Navigation/manipulation/driving suites에서 HJ-style safety score, copied-layer action head, write-time visual corruption, distractor geometry, tactile morphology, and grounded reasoning tokens를 stress split으로 만들고 constraint violation, action latency, recovery, contact failure, and trajectory compliance를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Robot geometry becomes self-correcting map evidence under uncertainty and sensor mismatch",
            "buckets": ["3D/Scene", "Autonomous Driving", "Efficiency/Systems"],
            "ids": ["2609.14634", "2609.15795", "2609.13903", "2609.14469", "2609.14619", "2609.13691", "2609.13733"],
            "needles": [
                "slam", "self-correcting", "aerial", "uav localization", "lidar", "radar",
                "bundle adjustment", "odometry", "uncertainty", "localization",
            ],
            "why": (
                "3D/SLAM 평가는 여전히 reconstruction fidelity나 pose error 하나로 끝나기 쉽지만, 로봇에게 필요한 것은 어느 불확실성을 믿고 언제 map을 고칠지다. "
                "SCOUT-SLAM은 tracking uncertainty가 reconstruction instability에 끌려가는 순환을 끊으려 하고, SURE-Map은 streaming geometry에 multi-timescale self-correction을 붙인다. "
                "SkyAnchor, PRI-Net, ESAFusion, MomentBA, and FFVO add aerial-ground anchoring, sparse LiDAR fusion, radar evidence selection, anisotropic correspondence uncertainty, and feed-forward odometry as trust interfaces. "
                "APRL은 map quality를 rendering이나 평균 pose error가 아니라 wrong-pose, wrong-map-update, dynamic-object damage, and downstream recovery로 평가해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Seven papers connect 3DGS SLAM, streaming geometry, aerial-ground registration, UAV localization, radar/LiDAR fusion, BA uncertainty, and visual odometry.",
            "lab_action": (
                "Indoor/dynamic/aerial/driving mapping episodes에서 dynamic clutter, weak texture, anchor sparsity, LiDAR degradation, radar clutter, correspondence anisotropy, and long-horizon scale drift를 조절해 relocalization error, map-update rejection, loop damage, detection AP under fog, and navigation recovery를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "World models are being priced by selection value rather than rollout abundance",
            "buckets": ["Generation", "Robot Learning", "Embodied AI"],
            "ids": ["2609.14973", "2609.14073", "2609.13257", "2609.14462", "2609.14561"],
            "needles": [
                "physical foundation", "counterfactual world", "compute-value", "streaming world",
                "latent world model", "world model", "sampling headroom", "physical",
            ],
            "why": (
                "World model 논문은 더 많은 rollout, 더 넓은 panorama state, 더 물리적인 latent를 제시하지만, 로봇 입장에서는 그것이 action 선택을 실제로 개선해야 한다. "
                "CVA는 sample pool의 oracle headroom이 selection gain이 아님을 보이고, LPA-CWM은 counterfactual world model을 motion reasoning adjudicator로 쓰며, PhysBrain과 GLAM은 physical or map-level latent가 행동/탐색에 연결되어야 함을 강조한다. "
                "AlayaVista는 global panoramic state와 local perspective rendering을 나누어 streaming context 문제를 드러낸다. "
                "APRL은 generated future를 action authority로 쓰기 전에 selection cost, verifier reliability, physical consistency, and downstream action change를 함께 계산해야 한다."
            ),
            "confidence": "Medium",
            "confidence_note": "Five papers share the decision-value framing, but common robot-control benchmarks are still thin.",
            "lab_action": (
                "Pushing/navigation/video-QA tasks에서 sample count, verifier score, panoramic state availability, physical adjudicator, and map-latent prediction을 독립 변수로 두고 selected-rollout action gain, compute cost, planning error, and failure-recovery timing을 비교한다."
            ),
            "limit": 5,
        },
        {
            "title": "Efficient multimodal systems shift from keeping content to preserving decisive evidence",
            "buckets": ["Efficiency/Systems", "Foundation Models"],
            "ids": ["2609.13804", "2609.13250", "2609.13293", "2609.13258", "2609.13267", "2609.13268", "2609.14258"],
            "needles": [
                "token selection", "keyframe selection", "temporal reliability", "eventgraph",
                "evidence-anchored", "evidence threading", "kv memory", "reliability",
            ],
            "why": (
                "Long-video, chart, document, and safety VLM systems all face token or evidence budgets, but retaining more content is not the same as preserving the decisive cue. "
                "StepPrune learns a STOP action for visual tokens, plug-and-play keyframe selection compares frame selectors, temporal reliability suppression removes corrupted egocentric evidence, and EventGraph/EventField gives temporal reasoning inspectable structure. "
                "STEER, CAVR/VET, and SPARK push the same rule into charts, documents, and safety KV memory: every retained token or thread should explain which answer or refusal it supports. "
                "APRL should treat compression for robot agents as decisive-cue preservation under latency, not visual reconstruction."
            ),
            "confidence": "High",
            "confidence_note": "Seven papers repeat evidence selection across visual tokens, keyframes, temporal events, structured charts, long documents, and safety KV memory.",
            "lab_action": (
                "Robot-video QA and edge VLA episodes에서 token STOP policy, query-aware keyframe selector, temporal reliability mask, event graph, evidence-thread path, and KV safety repair를 ablation하고 decisive-cue recall, hallucination, refusal correctness, prefill latency, and action error를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Navigation and driving agents move from absolute commands to revocable commitments",
            "buckets": ["Embodied AI", "Autonomous Driving"],
            "ids": ["2609.15098", "2609.15142", "2609.15195", "2609.14806", "2609.14058", "2609.14558", "2609.13941"],
            "needles": [
                "navigation", "compare before you commit", "harness", "belief-adaptive",
                "runtime uncertainty", "semantic target", "driver intent", "commit",
            ],
            "why": (
                "Embodied navigation and driving fail when an agent turns a plausible language answer or state estimate into an irreversible command too early. "
                "LG-VLN orchestrates parsing, mapping, planning, execution, and recovery as a state graph; C2Nav asks the VLM to compare physically vetted alternatives before committing; HarnessVLN validates planner proposals against spatial evidence and failures. "
                "Belief-adaptive UAV navigation, Koopman/NMPC multi-robot navigation, semantic target navigation, and BLInD all make trust or intent distributions explicit before action. "
                "APRL은 waypoint, stop, recovery, and intent outputs를 absolute answer로 받지 말고 compare, revoke, and trust-update interfaces로 바꾸어 failure lead time을 재야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Navigation, UAV, multi-robot, ASV, and driving papers all expose commitment authority under uncertainty.",
            "lab_action": (
                "R2R-CE/ObjectNav/UAV/driving scenarios에서 absolute waypoint, comparative gaze choice, route-sketch memory, GNSS trust belief, multi-robot uncertainty, and blind intent distribution을 바꿔 wrong-turn rate, stop error, recovery latency, collision proxy, and false-positive intervention을 비교한다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Permission-gated affordance benchmark",
            "claim": (
                "Separate target-part identity, causal visual region, semantic-action transfer, outcome state, and admissible measurement evidence before scoring robot action."
            ),
        },
        {
            "title": "Self-correcting map trust protocol",
            "claim": (
                "Compare 3DGS-SLAM, streaming geometry, aerial-ground anchoring, UAV localization, and radar/LiDAR fusion by map-update authority and downstream recovery."
            ),
        },
        {
            "title": "Selection-value audit for embodied world models",
            "claim": (
                "Charge sampling, verification, keyframe, token, and VLM-comparison costs against the actual action or navigation decision they improve."
            ),
        },
        {
            "title": "Revocable commitment interface for navigation",
            "claim": (
                "Replace absolute stop, waypoint, and intent outputs with comparative alternatives, trust updates, and walk-back tests under uncertainty."
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
        "meaning": "Included because it supports today's permissioned-evidence thesis.",
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
