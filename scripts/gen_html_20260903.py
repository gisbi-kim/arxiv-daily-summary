#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-09-03 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260903 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-03"


PROFILE = {
    "date": DATE,
    "weekday": "Thu",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching 2026-09-03 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-09-03 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "The 2026-09-03 batch is about action admission when evidence is multi-view, physical, delayed, or compressed. "
        "Geometry papers turn tracking, surgical reconstruction, weak map labels, panoramic UAV sensing, and humanoid odometry into questions about whether the metric frame is trustworthy enough for action. "
        "Manipulation and HRI papers ask whether contact geometry, map uncertainty, force safety, and stoppability should authorize continuation, intervention, or fallback. "
        "World-model papers challenge open-loop imagination scores by tying rollout quality to feedback schedules, sparse change, depth, and self-verification. "
        "Driving, VLM, and edge-system papers then widen the same contract: generated scenarios, trajectory scorers, hallucination detectors, streaming retrievers, and quantized models must prove that the retained evidence changes the decision before a robot acts."
    ),
    "cluster_takeaway": (
        "Today's core is not stronger perception or longer rollouts; it is whether independently counted, physically grounded, and feedback-checked evidence is sufficient to admit the next action."
    ),
    "trend_note": (
        "Thursday /new produced 168 deduplicated non-replacement papers and 139 ROI papers. "
        "Generation, Foundation Models, and Efficiency/Systems are large buckets, but the APRL-relevant signal is the shared demand for action gates: metric geometry must survive correspondence and viewpoint changes, contact policies must expose safety and disturbance, WAMs must match the feedback loop, and VLM/runtime systems must prove that their visual evidence was actually used."
    ),
    "cluster_specs": [
        {
            "title": "Geometry evaluation moves from plausible structure to metric frames that can release robot action",
            "buckets": ["3D/Scene", "Robot Learning"],
            "ids": ["2609.01899", "2609.02717", "2609.02798", "2609.02319", "2609.02222", "2609.02134"],
            "needles": [
                "multi-view", "3d point tracking", "surgical", "camera poses", "visual localization",
                "public maps", "fisheye", "panoramic", "odometry", "point cloud correspondence",
            ],
            "why": (
                "기존 geometry 평가는 reconstruction이나 localization이 그럴듯한지에 머무르기 쉽지만, 로봇은 correspondence, pose, view coverage, foot observation confidence가 잘못되면 바로 잘못된 행동을 낸다. "
                "TAPVid-MV는 3D point tracking에서 geometry recovery와 correspondence error를 분리해야 한다고 보여주고, MV-dVRK는 surgical surface를 scanner-validated tolerance로 재며, AutoCompass와 UAV panoramic sensing은 noisy pose labels와 parallax가 downstream place recognition을 흔드는 지점을 드러낸다. "
                "FOCUS와 humanoid retargeting은 contact or point-cloud evidence가 kinematic state를 얼마나 믿게 해 주는지 묻는다. "
                "APRL은 visual fidelity가 아니라 relocalization, route choice, footstep safety, surgical tool pose, and grasp frame이 바뀌는 조건으로 geometry를 평가해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Six papers independently connect multi-view tracks, surgical surface geometry, weak-map localization, panoramic UAV perception, foot-observation confidence, and point-cloud correspondence.",
            "lab_action": (
                "Multi-camera indoor, surgical workspace, public-map localization, UAV surround vision, and humanoid locomotion episodes에서 viewpoint count, correspondence ambiguity, weak pose labels, parallax depth, foot-contact reliability를 ablation하고 relocalization success, surgical surface tolerance, route deviation, footstep slip, action-frame error를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Contact-rich robot action shifts from task completion to continuation and fallback permission",
            "buckets": ["Robot Learning", "Embodied AI"],
            "ids": ["2609.01938", "2609.02020", "2609.02358", "2609.02402", "2609.02493", "2609.01662"],
            "needles": [
                "contact geometry", "force aware", "stoppability", "assistive care",
                "uncertainty-aware", "disturbance", "typed action admission", "provenance",
            ],
            "why": (
                "Task success 하나로 contact-rich robot을 평가하면 안전하지 않은 힘, 잘못된 접촉 위치, 과도한 scene disturbance, or duplicate evidence를 놓친다. "
                "DemoMimic은 local contact geometry가 object-generalization의 조건이라고 보고, torque-sampling MPPI와 MS-MEM은 force or uncertainty를 action selection에 넣으며, Safe-Stop은 stop 자체도 reachability agreement가 있어야 실행한다고 본다. "
                "Assistive-care benchmark와 PACT는 완료율 뒤의 force safety, observer leakage, provenance countability를 action admission 조건으로 분리한다. "
                "APRL은 manipulation과 HRI에서 continue, stop, confirm, fallback을 task-level result보다 먼저 판단하는 release gate를 가져야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Contact geometry, force-aware control, learned stoppability, assistive HRI scoring, disturbance-aware mapping, and provenance-conserving fusion all target action permission.",
            "lab_action": (
                "Dexterous manipulation, shelf retrieval, assistive-care wiping, humanoid stop, and multi-view collaboration tasks에서 local contact geometry, force threshold, map uncertainty, collateral disturbance, provenance partition, reach-avoid value를 독립 조건으로 두고 continuation permission, fallback timing, force violation, task recovery를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "World-model evaluation moves from imagined quality to feedback-matched action reliability",
            "buckets": ["Robot Learning", "3D/Scene", "Generation", "Efficiency/Systems"],
            "ids": ["2609.02811", "2609.02531", "2609.02046", "2609.02159", "2609.02886", "2609.02542"],
            "needles": [
                "world-model", "feedback", "world action model", "geometric latent", "sparse residual",
                "self-verifying", "long-horizon", "foothold", "imagined rollouts",
            ],
            "why": (
                "World model을 open-loop rollout이나 plausible video로만 보면 controller가 실제 feedback을 받는 순간 어떤 모델이 좋은지 바뀔 수 있다. "
                "imagined-rollout study는 measurement update schedule을 빼면 estimator ranking이 closed-loop optimum과 어긋날 수 있음을 보이고, SA-WAM은 depth-aware future를 action prediction과 함께 묶으며, sparse residual world models는 whole-scene prediction 대신 change gate를 둔다. "
                "World-Coherent Decoding, SolarWM, and humanoid visual locomotion은 future selection, long-horizon interaction data, and foothold anticipation이 feedback loop 안에서 평가되어야 한다고 말한다. "
                "APRL은 WAM benchmark에서 prediction horizon, correction interval, geometric state, change sparsity, and action success를 같은 closed-loop protocol로 묶어야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Six papers connect feedback schedule, geometric WAMs, sparse change models, self-verifying futures, open long-horizon data, and humanoid foothold anticipation.",
            "lab_action": (
                "Mobile path tracking, RoboCasa/LIBERO manipulation, tabletop pushing, humanoid foothold, and long-horizon video-control tasks에서 rollout horizon, measurement-update interval, depth encoding, residual change gate, future-candidate verifier, open-data mixture를 ablation하고 closed-loop ranking, recovery success, action delta, state drift를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Driving autonomy shifts from scenario generation to decision-transfer proof under risk",
            "buckets": ["Autonomous Driving", "Generation"],
            "ids": ["2609.01659", "2609.02462", "2609.01799", "2609.02252", "2609.02270", "2609.02688", "2609.02830", "2609.01609"],
            "needles": [
                "action-grounded", "cooperative planning", "trajectory scoring", "diffusion",
                "collision intent", "proxy", "driving decisions", "lidar semantic", "risk-aware",
            ],
            "why": (
                "Autonomous-driving evaluation이 scenario novelty나 proxy loss 개선에서 멈추면 실제 planner가 어떤 action을 바꾸는지 검증하지 못한다. "
                "VIPS는 V2I pseudo-simulation으로 error accumulation과 recovery를 보려 하고, designed trajectory samples and DiffuSearch는 candidate trajectory scoring and diffusion objectives를 decision boundary 가까이 밀어 넣는다. "
                "CrashDiffuser는 collision occurrence가 아니라 contact region intent를 조건으로 만들며, Proxy-to-Decision Transfer는 future-aware proxy improvement가 selected trajectory utility로 옮겨갔는지 분해한다. "
                "APRL은 driving and multi-robot safety에서 scenario generation, trajectory score, LiDAR robustness, and risk-aware diffusion이 feasible action set을 실제로 바꾸는지 확인해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Driving papers cover action-grounded survey evidence, V2I planning, scorer samples, diffusion planning, contact-region scenario generation, proxy-to-decision checks, LiDAR robustness, and risk-aware offline RL.",
            "lab_action": (
                "Urban intersections, V2I occlusions, highway risk, LiDAR adverse-weather, and collision-intent scenarios에서 trajectory perturbation axis, infrastructure message, diffusion objective alignment, contact-region target, proxy score margin, coarse-label robustness를 stress split으로 만들고 selected action change, safety violation, recovery timing, closed-loop utility를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "VLM reliability moves from confident answers to evidence provenance and state persistence",
            "buckets": ["Foundation Models", "Embodied AI"],
            "ids": ["2609.01888", "2609.02000", "2609.02028", "2609.02318", "2609.02359", "2609.02731", "2609.02486", "2609.01662"],
            "needles": [
                "hallucination", "causal drive", "attention drift", "mask-based", "yes/no verification",
                "streaming visual grounding", "retrieval", "adaptive", "provenance",
            ],
            "why": (
                "VLM이 자신 있게 대답하거나 hallucination score를 낮춘다고 해서 visual evidence를 제대로 썼다는 뜻은 아니다. "
                "faithfulness 재평가는 hallucination mitigation이 보수적 답변으로 object recall을 줄일 수 있다고 보고, Temporal Causal Drive는 decoding 단계에서 visual, question, prefix influence를 분리한다. "
                "CADMP, YesTrack, TempoGround, RVSD, ViSAR, and PACT는 attention drift, masked evidence, yes/no verification, object presence state, semantic retrieval, provenance countability를 통해 answer가 어떤 evidence에 의해 허가됐는지 묻는다. "
                "APRL robot VLM은 final answer보다 target absence, identity drift, duplicate-view agreement, retrieved crop, and visual-cue masking이 action permission을 바꾸는지 평가해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Seven VLM and embodied papers independently test hallucination trade-offs, causal source influence, attention drift, yes/no tracking, streaming state, sparse retrieval, and adaptive visual retrieval.",
            "lab_action": (
                "Robot instruction QA, multi-object tracking, streaming grounding, document/tool panels, and multi-camera action admission에서 target mask, duplicate provenance, old-frame retrieval, object enter/leave state, top-k page budget, and answer conservativeness를 ablation하고 refusal precision, identity drift, unsafe command rate, evidence-use sensitivity를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Deployment efficiency moves from lower cost to critical evidence retention under hardware limits",
            "buckets": ["Efficiency/Systems", "Generation", "Safety/Alignment"],
            "ids": ["2609.01683", "2609.01743", "2609.01778", "2609.02219", "2609.02780", "2609.02159", "2609.02291"],
            "needles": [
                "microcontrollers", "quantization", "adaptive visual input", "space robotics",
                "criticality", "streaming video", "shallow", "token", "compression", "self-verifying",
            ],
            "why": (
                "Edge deployment에서 latency, bitrate, or quantization loss만 줄이면 어떤 evidence가 사라졌는지 모른다. "
                "FORGE와 SCULPT는 integer-only or PTQ-ready models가 distribution shift and activation outliers under hardware constraints를 견뎌야 한다고 보고, AllocEmbed와 ShallowStream은 visual budget을 frame count, resolution, shallow index, and deep answer pass로 나눈다. "
                "space robotics segmentation은 low light, onboard compute, and radiation fault exposure를 함께 다루고, WCD and video compression work ask whether cheap futures or compressed streams retain action-relevant cues. "
                "APRL은 cost reduction을 decisive-cue retention, fault exposure, streaming miss, and downstream action delta로 검증해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Microcontroller TTA, PTQ readiness, adaptive video allocation, space-robotics acceleration, shallow streaming, WAM verification, and video compression all make cost a release-gate problem.",
            "lab_action": (
                "Microcontroller vision, lunar segmentation, streaming robot video, split VLM retrieval, and WAM planning tasks에서 integer-only adaptation, clipping bounds, frame-resolution allocation, DPU criticality mitigation, shallow-layer index depth, compression level을 ablation하고 decisive cue recall, fault-triggered error, latency-energy cost, downstream action delta를 비교한다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Provenance-aware action-admission benchmark",
            "claim": (
                "Build multi-camera robot episodes where duplicated agreement, independent views, target masks, and contact evidence decide hold, confirm, fallback, or execute."
            ),
        },
        {
            "title": "Feedback-faithful world-model metric",
            "claim": (
                "Evaluate WAMs and predictive estimators with explicit rollout horizon, measurement-update interval, sparse-change gate, and closed-loop action ranking."
            ),
        },
        {
            "title": "Contact-safe continuation protocol",
            "claim": (
                "Separate task success from force safety, local contact geometry, collateral disturbance, and learned recoverability in manipulation and assistive-care settings."
            ),
        },
        {
            "title": "Critical-evidence edge deployment test",
            "claim": (
                "Measure whether quantization, shallow streaming, adaptive frame allocation, and hardware fault mitigation preserve the cues that actually change robot action."
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
        "meaning": "Included because it supports today's action-admission thesis.",
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
