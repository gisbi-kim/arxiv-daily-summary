#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-09-16 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260916 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-16"


PROFILE = {
    "date": DATE,
    "weekday": "Wed",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching Wednesday 2026-09-16 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching Wednesday 2026-09-16 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "The 2026-09-16 batch says robot intelligence is becoming an authority-allocation problem. "
        "World-action and VLA papers no longer ask only whether a model can predict a plausible future; they ask whether depth, point tracks, BEV LiDAR, temporal context, object slots, or whole-body controller intents are the evidence allowed to change the next action. "
        "Geometry papers make the same move for maps: panoramic FoV, semantic place memory, LiDAR degeneracy, submap change detection, active-view benchmarks, and digital-twin structure diagnostics decide when a map update or localization estimate should be trusted. "
        "Contact-rich manipulation papers turn touch, proximity, embodiment, and geometric contracts into executable transfer conditions. "
        "Navigation, safety, and efficiency papers then supply revocation rules for episode-level uncertainty, traversability shift, rover slippage, cyber-physical attacks, body-rate-limited escape, sparse sensing, and active-parameter pruning. "
        "APRL should build evaluation assets where every representation declares what robot decision it can change and when that permission is withdrawn."
    ),
    "cluster_takeaway": (
        "Today's core is not better prediction or smaller models by itself; it is deciding when a representation has earned authority over an action, map update, safety intervention, or defer decision."
    ),
    "trend_note": (
        "Wednesday /new produced 187 deduplicated non-replacement papers and 156 ROI papers. "
        "The useful signal concentrates around WAM/VLA action interfaces, 3D geometry trust, contact-aware manipulation transfer, runtime uncertainty, and deployment compression."
    ),
    "cluster_specs": [
        {
            "title": "World-action models move from plausible futures to action-authority interfaces",
            "buckets": ["Robot Learning", "3D/Scene", "Generation"],
            "ids": ["2609.17524", "2609.16074", "2609.16697", "2609.16644", "2609.17021", "2609.17099", "2609.16864", "2609.17414"],
            "needles": [
                "world-action", "future modalities", "point tracks", "whole-body",
                "spatially-grounded", "latent actions", "temporal context", "slot",
                "actionable", "controllable",
            ],
            "why": (
                "기존 world model 평가는 미래 RGB나 rollout이 그럴듯한지에 기대기 쉬웠지만, 로봇에게 중요한 것은 어떤 미래 단서가 실제 행동 권한을 갖는지다. "
                "ModAR는 RGB보다 point track, DINO feature, depth가 더 일관된 행동 단서가 될 수 있음을 보이고, WAM survey와 actionable-world-model survey는 예측을 planning, recovery, verification으로 연결해야 한다고 정리한다. "
                "WholeBodyWAM, sensVLA, GeoLAM, TEMPO, SlotDiT는 각각 whole-body controller intent, BEV LiDAR grounding, geometry teacher, temporal context, object slot이 action head에 들어가는 경로를 분리한다. "
                "APRL은 world model을 영상 생성기로 보지 말고, 어떤 modality가 action delta와 failure recovery를 허가하는지 검증해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "WAM survey, multi-modal WAM, VLA grounding, temporal context, latent action, and object-centric generation papers all target the prediction-to-action interface.",
            "lab_action": (
                "LIBERO, dynamic handover, wheel-loader, and humanoid loco-manipulation tasks에서 RGB future, depth, point tracks, DINO feature, BEV LiDAR, temporal summary, object slot, and WBC intent를 ablation 축으로 두고 action delta, recovery success, latency, and contact failure를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Geometry evaluation shifts from visual fidelity to map-trust revocation",
            "buckets": ["3D/Scene", "Autonomous Driving", "Safety/Alignment"],
            "ids": ["2609.17387", "2609.17168", "2609.17145", "2609.17302", "2609.17106", "2609.16233", "2609.16443", "2609.16378", "2609.16662"],
            "needles": [
                "slam", "place recognition", "degeneracy", "change detection", "active vision",
                "3d scene", "parkour", "simulation fidelity", "point cloud tracking",
            ],
            "why": (
                "3D/SLAM/reconstruction 논문은 rendering 품질이나 평균 pose error만으로는 로봇 배포 실패를 설명하기 어렵다는 쪽으로 움직인다. "
                "PanoGS-SLAM은 FoV가 optimization conditioning을 바꾼다고 보고, HuMemSLAM은 semantic place memory와 latency를 함께 묻고, LiLi는 scan alignment가 관측 불가능한 transformation family를 드러낸다. "
                "CDSD, BRAVE-6D, Neverwhere, LiDAR simulation fidelity diagnostics는 map update, active view, visual locomotion, digital twin transfer가 실제로 믿을 수 있는지 따진다. "
                "따라서 APRL geometry 평가는 좋은 reconstruction이 아니라 언제 localization/map update/simulation evidence를 거부해야 하는지로 설계되어야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Panoramic SLAM, semantic VPR, LiDAR degeneracy, submap change detection, active vision, and simulation-fidelity papers repeat the same trust-gating decision.",
            "lab_action": (
                "Indoor/dynamic/corridor/outdoor scenes에서 FoV, semantic aliasing, LiDAR degeneracy, submap viewpoint mismatch, active-view distance, and simulated-structure deformation을 stress split으로 만들고 pose error, wrong loop closure, map-update rejection, grasp-pose quality, and navigation recovery를 함께 평가한다."
            ),
            "limit": 6,
        },
        {
            "title": "Dexterous manipulation turns contact and embodiment into transfer contracts",
            "buckets": ["Robot Learning", "3D/Scene"],
            "ids": ["2609.16319", "2609.16504", "2609.16586", "2609.16437", "2609.16683", "2609.17035", "2609.16040", "2609.16186", "2609.16331", "2609.16815"],
            "needles": [
                "dexterous", "tactile", "contact", "proximity", "whole-body",
                "soft", "bilateral", "occupancy", "geometric contracts", "embodiment",
            ],
            "why": (
                "로봇 조작은 human video나 language instruction을 그대로 행동으로 바꾸는 문제가 아니라, 접촉과 embodiment가 어떤 조건에서 transfer를 허가하는지 정하는 문제로 변하고 있다. "
                "ConGraspXL은 task-driven grasp constraint를 조합하고, UniDex-ViTac은 human video를 tactile contact가 붙은 robot rollout으로 바꾸며, ProxiDex는 hand-object proximity를 hardware-agnostic contact state로 삼는다. "
                "XRoboToolKit-T, Weave, SWIM, Bi-MoDe, ManiSkillFormer, Occupancy-guided nephrectomy, VED 논문은 tactile assistance, contact-aware retargeting, soft proprioception, force modifiers, geometric contracts, deformable anatomy, canonical embodiment가 실제 실행권을 나누는 단서임을 보인다. "
                "APRL은 contact-rich benchmark에서 tactile/proximity/embodiment cues가 언제 action을 바꿔야 하는지 직접 평가해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Dexterous grasping, visuo-tactile ACT, proximity dynamics, tactile teleoperation, humanoid interaction, soft robot VLA, and embodiment-transfer papers converge on contact authority.",
            "lab_action": (
                "Dexterous hand, soft robot, and dual-arm manipulation tasks에서 target constraint, fingertip contact, proximity token, tactile force assistance, canonical end-effector geometry, and deformable occupancy state를 ablation하고 slip, invalid contact, force overshoot, transfer success, and recovery action을 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Navigation and safety policies adopt episode-level revocation signals",
            "buckets": ["Embodied AI", "Safety/Alignment", "3D/Scene", "Efficiency/Systems"],
            "ids": ["2609.17499", "2609.17141", "2609.17187", "2609.17349", "2609.17292", "2609.17430", "2609.16852", "2609.17384", "2609.16958"],
            "needles": [
                "conformal", "traversability", "slippage", "resilience", "barrier",
                "reachability", "collaborative perception", "active inference", "uncertainty",
            ],
            "why": (
                "Embodied navigation과 safety 논문들은 한 step의 confidence나 nominal controller만으로는 실행을 허가하기 어렵다고 말한다. "
                "ENCP는 VLN uncertainty를 episode 단위로 정규화하고, traversability continual learning은 generated recall의 uncertainty를 adaptation에 포함하며, Fleet-to-Lab은 lunar rover slippage transfer를 model fusion 문제로 본다. "
                "RobResilience, escape-aware CBF, hybrid HJ reachability, CoAdapt, multi-robot active inference는 공격, body-rate limit, hybrid mode, bandwidth, team redundancy가 생길 때 언제 행동을 멈추거나 완화해야 하는지 묻는다. "
                "APRL은 navigation safety를 성공률이 아니라 defer timing, mitigation feasibility, reachable escape authority, and information redundancy로 평가해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "VLN, traversability, rover, cyber-physical resilience, CBF, HJ reachability, swarm perception, and active-inference papers all expose runtime revocation conditions.",
            "lab_action": (
                "R2R/REVERIE, rough-terrain, lunar-sim, UAV, and multi-robot monitoring episodes에서 episode-normalized uncertainty, terrain novelty, slippage domain gap, compromised-device predicates, body-rate escape margin, and expected evidence redundancy를 조절해 defer timing, mitigation success, collision proxy, and recovery cost를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Deployment compression is judged by preserved robot evidence, not parameter count",
            "buckets": ["Efficiency/Systems", "Robot Learning"],
            "ids": ["2609.16637", "2609.16503", "2609.17198", "2609.16722", "2609.16689", "2609.16810", "2609.17042", "2609.16656"],
            "needles": [
                "efficient", "compact", "latency", "quantization", "edge", "sparse",
                "ultra-lightweight", "parameter", "memory", "deployment",
            ],
            "why": (
                "Efficiency 논문들은 작아졌다는 사실보다, 압축 뒤에도 robot decision에 필요한 evidence가 남는지에 초점을 맞춘다. "
                "LePoKet은 compact optical-flow transfer를 구조적으로 학습하고, AdaDE는 VLA dense block을 MoE로 바꿔 active parameter를 줄이며, TIO-Former는 sparse ToF+IMU evidence로 nano-UAV odometry를 수행한다. "
                "VideoMM, EdgeVL, high-dimensional planning, adapter banks, VSSD quantization은 token, modality, planner move, motor option, activation precision을 줄여도 decisive cue가 보존되는지 묻는다. "
                "APRL은 latency/parameter 절감뿐 아니라 어떤 공간 단서, action expert, sensor memory, or option policy가 남아 downstream failure를 막는지 측정해야 한다."
            ),
            "confidence": "Medium",
            "confidence_note": "The papers share deployment-budget pressure, but their metrics span perception, VLA, odometry, planning, and motor options rather than one common benchmark.",
            "lab_action": (
                "Edge VLA, nano-UAV odometry, robot optical flow, long-video QA, and multi-robot planning tasks에서 active parameter ratio, token budget, ToF memory, quantization bit, sparse-move ratio, and adapter choice를 ablation하고 action error, odometry drift, decisive-cue recall, latency, and memory footprint를 함께 비교한다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Representation authority audit",
            "claim": (
                "For every modality or latent in a WAM/VLA stack, measure the action delta, recovery value, latency cost, and failure condition that grants or revokes execution authority."
            ),
        },
        {
            "title": "Geometry trust revocation suite",
            "claim": (
                "Stress panoramic SLAM, semantic place recognition, LiDAR degeneracy, submap change detection, and digital-twin fidelity with one shared map-update trust protocol."
            ),
        },
        {
            "title": "Contact-transfer contract for dexterous policies",
            "claim": (
                "Convert tactile, proximity, embodiment, and geometric-contract cues into explicit predictors of when human-video or language-derived skills transfer to new hands and objects."
            ),
        },
        {
            "title": "Episode-level uncertainty and mitigation benchmark",
            "claim": (
                "Evaluate navigation and safety policies by defer timing, reachable escape margin, mitigation feasibility, and information redundancy across dependent episodes."
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
        "meaning": "Included because it supports today's representation-authority thesis.",
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
