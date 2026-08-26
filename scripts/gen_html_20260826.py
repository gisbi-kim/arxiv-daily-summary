#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-08-26 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260826 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-26"


PROFILE = {
    "date": DATE,
    "weekday": "Wed",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching 2026-08-26 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-08-26 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "The 2026-08-26 batch is about permission to trust intermediate evidence. "
        "World-action papers ask whether imagined futures actually follow actions and whether prediction credit should be settled after execution. "
        "VLA and manipulation papers split adaptation into latency, skill hierarchy, gripper embodiment, contact events, and trajectory-level tokens instead of treating demonstrations as interchangeable. "
        "Geometry and simulation papers turn 3D assets into physically executable scenes, while driving and embodied-safety papers make recovery under sensor faults, emergency interactions, and temporal-logic constraints the main evaluation unit. "
        "The shared research decision is to expose the variable that can change behavior before the policy, planner, mapper, cache, or simulator is trusted."
    ),
    "cluster_takeaway": (
        "Today's core is not a larger robot model or a prettier generated world; it is whether the evidence variable that changes behavior is action-faithful, physically executable, recoverable, and cheap enough to use in deployment."
    ),
    "trend_note": (
        "Wednesday /new produced 149 deduplicated non-replacement papers and 124 ROI papers. "
        "Efficiency/Systems and Robot Learning are the largest buckets, but the strongest APRL signal is the convergence of WAM action-faithfulness, VLA interface adaptation, executable 3D scenes, and trajectory-level safety evidence."
    ),
    "cluster_specs": [
        {
            "title": "World-action models move from plausible futures to action-faithfulness contracts",
            "buckets": ["Robot Learning", "Generation", "3D/Scene"],
            "ids": ["2608.24885", "2608.23863", "2608.24101", "2608.24882", "2608.24714", "2608.23927", "2608.24855"],
            "needles": ["world-action", "world action", "action-conditioned", "future", "imagination", "latent action", "visual tracks", "credit", "gaussianwam", "planning"],
            "why": (
                "기존 WAM 평가는 미래 영상이 그럴듯한지에 기대기 쉬웠지만, 로봇은 그 미래가 실제 action을 따르는지를 먼저 물어야 한다. "
                "WorldEcho는 off-expert action following을 직접 찌르고, DreamLedger는 실행 후 prediction credit을 정산하며, TrAct와 LAWA는 visual track과 latent action으로 control-relevant state를 압축하고, GaussianWAM과 GlanceWAM은 geometry supervision과 비동기 imagination을 정책 루프에 넣는다. "
                "APRL은 video fidelity가 아니라 action delta, SE(3) trajectory, contact state, horizon별 settlement가 policy choice를 바꾸는지를 평가해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Seven WAM/planning papers independently name action following, prediction settlement, latent action, visual tracks, Gaussian geometry, or planning reuse.",
            "lab_action": (
                "Expert, recovery, off-expert, and contact-changing actions을 같은 상태에서 넣고 pixel WAM, latent-action WAM, visual-track WAM, Gaussian-supervised WAM, generative latent planner를 비교해 action-faithfulness error, contact-state mismatch, trajectory deviation, downstream policy change를 평가한다."
            ),
            "limit": 6,
        },
        {
            "title": "VLA adaptation moves from demo reuse to latency, gripper, contact, and trajectory interfaces",
            "buckets": ["Robot Learning"],
            "ids": ["2608.23831", "2608.24042", "2608.24603", "2608.24111", "2608.24741", "2608.23629", "2608.23994"],
            "needles": ["vla", "latency", "skill retrieval", "gripper", "contact", "trajectory-level", "tamp", "teacher", "demonstration"],
            "why": (
                "기존 robot adaptation은 demonstration을 더 잘 고르는 문제처럼 보였지만, 오늘 묶음은 어떤 interface가 transferable한지를 분리한다. "
                "Latency-aware RL은 기다리는 동안 dynamics가 바뀐다고 보고, hierarchical retrieval은 long-horizon subskill 구조를 찾고, gripper-aware VLA는 embodiment-specific grasping을 드러내며, CAT와 contact-rich LfD는 trajectory token과 contact transition을 action 표현의 단위로 삼는다. "
                "따라서 few-shot success만 비교하지 말고 latency, subskill order, gripper type, contact event, trajectory parameterization을 독립 ablation 축으로 둬야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Seven robot papers share the interface-adaptation question across latency, retrieval, gripper, contact, trajectory, symbolic operator, and human-teaching dynamics.",
            "lab_action": (
                "같은 manipulation task에서 inference latency, retrieved subskill, gripper type, contact transition, trajectory tokenization, symbolic macro-operator를 독립 변수로 바꾸고 action discontinuity, recovery timing, contact error, terminal success를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "3D scene generation shifts from surface recovery to physically executable simulation assets",
            "buckets": ["3D/Scene", "Foundation Models"],
            "ids": ["2608.24212", "2608.23869", "2608.23930", "2608.24109", "2608.23943", "2608.24093"],
            "needles": ["simulation", "interactive", "physics", "3d scene", "mesh", "pbr", "relightable", "point cloud", "asset"],
            "why": (
                "3D reconstruction이 보기 좋은 표면을 만드는 단계에 머물면 로봇 benchmark 자산으로 쓰기 어렵다. "
                "NeoWorld-Pro는 monocular image를 interactive scene program으로 바꾸고, Gen2Physics는 generated mesh를 physics-ready material decomposition으로 연결하며, SceneReGen, ExMesh++, Luce, 4D point-tube JEPA는 object assembly, topology, PBR material, spatiotemporal point representation을 별도 계약으로 만든다. "
                "APRL은 reconstructed asset을 support, collision, articulation, scale, relighting, robot task success로 검증해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Six 3D/physics papers connect scene reconstruction, interactive programming, material grounding, relightable assets, topology, and point-cloud temporal structure.",
            "lab_action": (
                "Monocular scene program, mesh-to-physics asset, relightable Gaussian, UV-PBR mesh, and 4D point representation을 support violation, collision validity, articulation success, viewpoint relighting, scale drift, downstream embodied-task success로 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Perception efficiency moves from token reduction to decision-relevant evidence preservation",
            "buckets": ["Efficiency/Systems", "Safety/Alignment"],
            "ids": ["2608.23921", "2608.24063", "2608.23923", "2608.24671", "2608.24544", "2608.24365", "2608.23574"],
            "needles": ["token", "cache", "pruning", "slicing", "reliability", "anchor", "sparse", "feature tracking", "patch selection", "evidence"],
            "why": (
                "경량화가 latency만 줄이면 배포에는 충분하지 않다. "
                "HAP와 VisCache는 visual token과 KV cache를 줄일 때 query-relevant evidence가 남아야 한다고 보고, ROI-Gated SAHI와 InfoDPP-PAC은 작은 객체나 slide patch에서 어디에 계산을 쓸지 선택하며, ReGround-Surg, KLTNet, MaST는 anchor, sparse feature, motion prior가 tracking이나 segmentation 실패를 좌우한다고 본다. "
                "압축 후에도 실제 결정에 필요한 crop, cache, feature track, anchor mask, patch set이 남는지 task-level metric으로 확인해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Seven efficiency and reliability papers share budgeted evidence selection across tokens, cache, slices, anchors, feature tracks, motion sparsity, and patch sets.",
            "lab_action": (
                "Visual-token pruning, KV-cache pruning, ROI slicing, reliability-guided anchor grounding, sparse VIO tracking, motion-aware tracking, and patch selection을 같은 inspection/navigation cases에서 evidence cost, missed-small-object rate, tracking drift, segmentation failure, downstream action error로 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Embodied autonomy safety moves from average success to recovery and constraint trajectories",
            "buckets": ["Embodied AI", "Autonomous Driving", "Safety/Alignment", "Robot Learning"],
            "ids": ["2608.23839", "2608.24094", "2608.24366", "2608.24282", "2608.23972", "2608.24525", "2608.24019"],
            "needles": ["resilience", "emergency", "sensor degradation", "lidar", "safety", "constraint", "stl", "rollout-guided", "planning", "recovery"],
            "why": (
                "자율시스템을 최종 success나 collision 하나로 판단하면 실패가 시작된 지점을 놓친다. "
                "Resilience metric은 recovery와 stabilization을 보고, SIREN-Bench는 emergency-vehicle interaction을 behavior-level scenario로 만들며, variance-guided fusion과 CARE는 sensor degradation과 first sighting에서 어떤 evidence를 남겨야 하는지 묻고, STL-MPPI와 RoG-DAgger는 temporal-logic constraints와 policy-induced state를 training/evaluation 안으로 끌어온다. "
                "APRL은 perturbation 이전, 중간, 이후의 recovery curve와 constraint violation을 같이 봐야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Seven autonomy papers connect recovery metrics, emergency scenarios, sensor-fault fusion, adaptive LiDAR reserves, formal constraints, post-training rollouts, and fast planning.",
            "lab_action": (
                "Emergency-vehicle scenes, asymmetric camera/LiDAR faults, unseen-object first sightings, STL mission constraints, policy-induced driving states, and underactuated short-horizon plans을 구성해 recovery time, constraint violation, near-miss, planner deviation, rollout correction value를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "VLM reasoning shifts from fluent answers to localized accountable evidence",
            "buckets": ["Foundation Models", "Safety/Alignment"],
            "ids": ["2608.23723", "2608.23853", "2608.23974", "2608.24134", "2608.24138", "2608.24430", "2608.24439", "2608.23978"],
            "needles": ["evidence", "graph", "feedback", "procedural", "repair", "explainable", "interactive", "reasoning", "grounding"],
            "why": (
                "VLM 결과가 자연스럽게 말이 되는지만 보면 국소 증거가 틀린 상태를 감출 수 있다. "
                "DriftAD와 LUX는 localized defect와 lesion graph를 쓰고, BooF와 explainable face recognition은 generalist-expert feedback과 auditable evidence를 요구하며, EgoErrorVQA, RubSE, DoublesEval, interactive grounding은 절차 오류, visual repair context, tactical moment, dialogue-acquired target evidence를 평가 단위로 만든다. "
                "APRL의 embodied VLM 평가는 답변 fluency가 아니라 어떤 local evidence가 action permission이나 repair decision을 바꿨는지를 물어야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Eight VLM papers independently require localized defects, graph evidence, expert feedback, procedural errors, visual repair rubrics, explainable decisions, tactical moments, or interactive grounding.",
            "lab_action": (
                "Defect inspection, lesion captioning, procedural error, UI repair, multi-agent tactic, and ambiguous grounding prompts에서 direct VLM answer와 evidence-localized answer를 비교해 local evidence hit rate, wrong-permission rate, repair regression, action-choice change를 평가한다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "World-model action-faithfulness harness",
            "claim": (
                "Probe expert, recovery, off-expert, and contact-changing actions in the same states; compare imagined future state, SE(3) trajectory, contact mismatch, and downstream policy choice."
            ),
        },
        {
            "title": "Latency and interface-aware VLA adaptation grid",
            "claim": (
                "Cross inference latency, subskill retrieval, gripper type, contact event, and trajectory tokenization to identify which interface predicts failure before terminal success changes."
            ),
        },
        {
            "title": "Executable scene and recovery benchmark",
            "claim": (
                "Grade generated scenes and autonomy stacks by support, collision, articulation, sensor-fault recovery, emergency interaction, temporal-logic satisfaction, and robot task success."
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
        "meaning": "Included because it supports today's action-faithfulness and deployable-evidence thesis.",
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
