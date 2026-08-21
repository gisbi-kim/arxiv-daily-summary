#!/usr/bin/env python3
"""Generate the 2026-08-20 Research Intelligence edition."""

from __future__ import annotations

import json
from pathlib import Path

from gen_research_intelligence_20260811 import build_html


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PROMPT = "prompts/instruction_v20260713.md"


RI_BY_DATE = {
    "2026-08-20": {
        "date": "2026-08-20",
        "edition": "Research Intelligence",
        "source_prompt": SOURCE_PROMPT,
        "source_mode": "pastweek-date-section",
        "scope_note": (
            "Backfill edition from arXiv /pastweek date sections: 94 cs.CV rows, "
            "38 cs.RO rows, 125 deduplicated papers, and 50 ROI papers. The /pastweek "
            "date-section source does not include abstracts, so Tier A cards are title/subject-only "
            "triage notes. No figure, table, method-section, code, dataset-release, or full-text claims "
            "are asserted."
        ),
        "executive_thesis": (
            "The August 20 backfill is a compact but useful bridge between robot-usable geometry and "
            "deployment-grade manipulation evidence. GS-VLA, the agricultural tractor paper, SLAM/UAV "
            "evaluation papers, and 4D Gaussian reconstruction work ask whether geometry changes a real "
            "policy, field route, or map validity decision. SoftVTBench, LabDex, RoboEdit, and hidden-geometry "
            "grasping papers ask whether manipulation benchmarks preserve deformability, dexterity, human "
            "experience, and partial-view state instead of reporting success alone. APRL should read this day "
            "as a source-audited backfill: enough signal to define benchmark axes, not enough source evidence "
            "to make full-text mechanism claims."
        ),
        "decision_cards": [
            {
                "label": "Decision",
                "title": "Geometry must affect a policy or field route",
                "body": (
                    "GS-VLA, agricultural tractor navigation, UAV SLAM, visual odometry, and 4D Gaussian "
                    "reconstruction titles all attach geometry to a policy, route, or validity test rather "
                    "than leaving it as visual output."
                ),
            },
            {
                "label": "Decision",
                "title": "Manipulation benchmarks need material and hidden-state labels",
                "body": (
                    "SoftVTBench, LabDex, PartialBiGrasp, and RoboEdit point toward benchmark assets that "
                    "name deformability, laboratory dexterity, partial local geometry, and human video edits "
                    "as separate evidence channels."
                ),
            },
            {
                "label": "Decision",
                "title": "World models are moving toward decision alignment",
                "body": (
                    "DA-WAM, Decision-Metric Alignment, GigaBrain-WBC, and endovascular world-model control "
                    "titles make future latent quality accountable to MPC, whole-body control, or navigation "
                    "rather than video plausibility alone."
                ),
            },
        ],
        "papers": [
            {
                "rank": 1,
                "title": "GS-VLA: Plug-and-Play Viewpoint Canonicalization for Frozen VLA Policies via Gaussian Splatting",
                "arxiv_id": "2608.19066",
                "fit": "Gaussian Splatting - frozen VLA - viewpoint canonicalization",
                "status": "Tier A - title/subject-only backfill triage",
                "status_quo": "Frozen VLA policies are often evaluated as if camera viewpoint is a nuisance handled by data diversity or augmentation.",
                "friction": "The title frames viewpoint canonicalization as a direct failure interface for frozen policies, which suggests that policy errors can begin before action decoding.",
                "hidden_premise": "A Gaussian scene representation can normalize viewpoint evidence without changing the policy backbone.",
                "conceptual_move": "Treat geometry as a plug-in policy-conditioning layer rather than a separate reconstruction artifact.",
                "mechanism": "Unknown from /pastweek title/subject rows; the safe claim is that Gaussian Splatting is positioned as the canonicalization tool.",
                "evidence": [
                    {"trace": "[Title]", "claim": "The title links frozen VLA policies, viewpoint canonicalization, and Gaussian Splatting."},
                    {"trace": "[Subjects]", "claim": "The row is listed under cs.CV with artificial intelligence cross-category context."},
                    {"trace": "[Source mode]", "claim": "Backfill source lacks abstracts, so mechanism and experiment details require later official abstract or PDF reading."},
                ],
                "falsification": "If viewpoint canonicalization improves image alignment but does not change robot action robustness under camera shifts, the policy-facing geometry claim is weak.",
                "adversarial": "Stress the method with calibration error, reflective objects, dynamic distractors, and wrist-camera views where Gaussian geometry may look stable but action evidence is wrong.",
                "thinking_tool": "Before scaling VLA data, ask whether the camera frame can be canonicalized as a separate intervention.",
                "transfer_boundary": "Most relevant to camera-sensitive manipulation; weaker for policies dominated by force, tactile, or proprioceptive state.",
            },
            {
                "rank": 2,
                "title": "SoftVTBench: A Deformation-Aware Visuo-Tactile Dataset and Benchmark for Deformable-Object Manipulation",
                "arxiv_id": "2608.18701",
                "fit": "deformable manipulation - visuo-tactile benchmark - material state",
                "status": "Tier A - title/subject-only backfill triage",
                "status_quo": "Manipulation success is often reported on rigid or lightly deformable objects where visual state is enough to rank a policy.",
                "friction": "Deformable objects can hide failure in material strain, contact distribution, or tactile state before final task failure appears.",
                "hidden_premise": "A useful deformable-object benchmark must expose tactile and deformation variables as first-class labels.",
                "conceptual_move": "Move deformable manipulation evaluation from final pose success to deformation-aware visuo-tactile evidence.",
                "mechanism": "Unknown from /pastweek source; the title safely indicates a dataset and benchmark centered on deformation-aware visuo-tactile signals.",
                "evidence": [
                    {"trace": "[Title]", "claim": "The title names a deformation-aware visuo-tactile dataset and benchmark."},
                    {"trace": "[Subjects]", "claim": "The paper is listed under cs.RO."},
                    {"trace": "[Inference]", "claim": "APRL can use this as a cue to separate visual success from tactile/material-state success."},
                ],
                "falsification": "If tactile and deformation labels do not change policy ranking beyond image-only metrics, the benchmark adds little diagnostic value.",
                "adversarial": "Include cases where the object reaches a target pose but deformation, tearing, or contact distribution is unacceptable.",
                "thinking_tool": "Score deformable manipulation by the hidden material state that would make reuse unsafe.",
                "transfer_boundary": "Direct for soft objects, cloth, food, and lab materials; less direct for rigid pick-place tasks.",
            },
            {
                "rank": 3,
                "title": "LabDex: A Hierarchical Benchmark for Dexterous Manipulation in Laboratories",
                "arxiv_id": "2608.18618",
                "fit": "dexterous manipulation - laboratory tasks - hierarchical benchmark",
                "status": "Tier A - title/subject-only backfill triage",
                "status_quo": "Dexterous manipulation benchmarks often emphasize isolated primitives without a lab workflow hierarchy.",
                "friction": "Laboratory manipulation fails through sequencing, tool handling, and local recovery, not only grasp success.",
                "hidden_premise": "A hierarchical benchmark can expose which subtask boundary, tool state, or local dexterity requirement causes failure.",
                "conceptual_move": "Make laboratory dexterity a benchmark hierarchy instead of a collection of independent manipulation tasks.",
                "mechanism": "Unknown from title/subject rows; the title safely supports only benchmark scope and hierarchy.",
                "evidence": [
                    {"trace": "[Title]", "claim": "The paper proposes a hierarchical benchmark for dexterous manipulation in laboratories."},
                    {"trace": "[Subjects]", "claim": "The paper is listed under cs.RO."},
                    {"trace": "[Inference]", "claim": "APRL should treat lab workflows as subtask-boundary diagnostics."},
                ],
                "falsification": "If the hierarchy does not identify different failure causes than flat success metrics, it is a packaging change rather than a diagnostic benchmark.",
                "adversarial": "Test tool handoff, liquid or granular transfer, occluded grip correction, and recovery after a wrong intermediate state.",
                "thinking_tool": "Decompose lab manipulation by the task boundary where dexterity becomes the bottleneck.",
                "transfer_boundary": "Strong for laboratory automation and bimanual manipulation; weaker for locomotion or pure navigation.",
            },
            {
                "rank": 4,
                "title": "DA-WAM: Decision-Aligned Future Latents for Driving World Models",
                "arxiv_id": "2608.19085",
                "fit": "driving world model - decision-aligned latent - future prediction",
                "status": "Tier A - title/subject-only backfill triage",
                "status_quo": "Driving world models can be judged by future-video or latent prediction quality without proving that the latent changes a maneuver.",
                "friction": "A future latent can be visually plausible while missing the variable that determines braking, lane choice, or avoidance.",
                "hidden_premise": "The future latent should be aligned to downstream decision variables, not only reconstruction or likelihood objectives.",
                "conceptual_move": "Make decision alignment the criterion for future latent usefulness in driving world models.",
                "mechanism": "Unknown from /pastweek source; the safe claim is that the title explicitly binds future latents to driving decisions.",
                "evidence": [
                    {"trace": "[Title]", "claim": "The title names decision-aligned future latents for driving world models."},
                    {"trace": "[Subjects]", "claim": "The paper is listed under cs.RO, cs.AI, and machine learning context."},
                    {"trace": "[Inference]", "claim": "APRL should test whether future latents predict action changes under hazardous scene variables."},
                ],
                "falsification": "If decision-aligned latents do not alter trajectory quality under OOD or near-miss cases, alignment is not operational.",
                "adversarial": "Hold visual quality constant while changing a traffic light, pedestrian intent, or route constraint that should alter the planned action.",
                "thinking_tool": "A world model latent is useful only if it preserves the variable that changes the next decision.",
                "transfer_boundary": "Direct for driving and mobile-robot planning; less direct for single-step perception tasks.",
            },
            {
                "rank": 5,
                "title": "ReWEIGH the Evidence: Calibrating Token-Level Ordinal Visual Evidence to Mitigate Hallucinations in Large Vision-Language Models",
                "arxiv_id": "2608.19075",
                "fit": "VLM hallucination - token-level evidence calibration - ordinal visual evidence",
                "status": "Tier A - title/subject-only backfill triage",
                "status_quo": "VLM reliability is often summarized by answer confidence or hallucination rate without exposing which visual tokens carried evidence.",
                "friction": "A model can sound confident while visual evidence is weak, ordinally misread, or overruled by a language prior.",
                "hidden_premise": "Token-level visual evidence can be calibrated so that answers reflect evidence strength more faithfully.",
                "conceptual_move": "Move hallucination mitigation from post-hoc answer filtering to evidence-weight calibration at the token level.",
                "mechanism": "Unknown from title/subject rows; the title safely supports the evidence-calibration framing.",
                "evidence": [
                    {"trace": "[Title]", "claim": "The title names token-level ordinal visual evidence calibration for hallucination mitigation."},
                    {"trace": "[Subjects]", "claim": "The paper is listed under cs.CV, cs.AI, and cs.CL."},
                    {"trace": "[Inference]", "claim": "Robot VLM evaluation should expose the visual evidence that authorized an answer or action."},
                ],
                "falsification": "If token-level calibration improves language metrics but not source-grounded action correctness, the transfer to robotics is limited.",
                "adversarial": "Use scenes with visually weak but task-critical cues, conflicting text labels, or ordinal measurements that can be confidently misread.",
                "thinking_tool": "Ask whether a VLM's answer is backed by calibrated visual evidence before using it for action.",
                "transfer_boundary": "Strong for VLM-heavy inspection, gauges, labels, and navigation prompts; weaker for low-level policies without language arbitration.",
            },
            {
                "rank": 6,
                "title": "GuideFetch: A Task Coordination Framework for Concurrent Navigation and Object Retrieval in Assistive Robot Dogs",
                "arxiv_id": "2608.18292",
                "fit": "assistive robot dogs - concurrent navigation and retrieval - task coordination",
                "status": "Tier A - title/subject-only backfill triage",
                "status_quo": "Assistive robots are often evaluated as separate navigation or object-retrieval systems.",
                "friction": "A real assistive robot dog must coordinate navigation and retrieval concurrently, where success can fail at the handoff between tasks.",
                "hidden_premise": "Coordination state is a separate control variable that should be measured apart from navigation or grasping alone.",
                "conceptual_move": "Frame assistive robot performance as concurrent task coordination.",
                "mechanism": "Unknown from title/subject rows; the title safely indicates a coordination framework for concurrent navigation and retrieval.",
                "evidence": [
                    {"trace": "[Title]", "claim": "The title names concurrent navigation and object retrieval in assistive robot dogs."},
                    {"trace": "[Subjects]", "claim": "The row is cross-listed in cs.RO and cs.CV."},
                    {"trace": "[Inference]", "claim": "APRL should score coordination-state failure separately from navigation or manipulation failure."},
                ],
                "falsification": "If concurrent evaluation reduces to independent navigation and retrieval scores, the coordination claim is weak.",
                "adversarial": "Test delayed object discovery, wrong-object retrieval, route blockage, and user-priority changes during execution.",
                "thinking_tool": "Make task coordination an explicit evaluated state in embodied systems.",
                "transfer_boundary": "Direct for mobile manipulation and assistive robots; less direct for fixed-base laboratory arms.",
            },
        ],
        "synthesis": [
            {
                "title": "Geometry is moving into the policy loop",
                "links": "GS-VLA - Agricultural Tractor - UAV SLAM - Visual Odometry - Depth Anything V4",
                "facts": "The selected titles attach geometry to frozen VLA viewpoint handling, field navigation, UAV SLAM or odometry evaluation, and dynamic 4D reconstruction.",
                "inference": "APRL should evaluate maps and reconstructions by action changes, localization recovery, and route stability.",
            },
            {
                "title": "Benchmarks are becoming state-label assets",
                "links": "SoftVTBench - LabDex - PartialBiGrasp - RoboEdit",
                "facts": "The robotics benchmark titles name deformation, lab dexterity, partial local geometry, and scalable human manipulation experience.",
                "inference": "The durable asset is a failure-state label set, not a larger collection of untyped demonstrations.",
            },
            {
                "title": "World-model quality is being tied to decisions",
                "links": "DA-WAM - Decision-Metric Alignment - GigaBrain-WBC - Progressive Experience Fusion",
                "facts": "World-model titles repeatedly mention decision alignment, control, navigation, or multi-task experience fusion.",
                "inference": "APRL should make future-state prediction answer which action would change, not just whether a video or latent looks plausible.",
            },
        ],
        "frontier_memory": [
            {
                "label": "Strengthening",
                "history": "August 18 and August 19 emphasized runtime evidence control and robot-usable geometry.",
                "body": "August 20 strengthens the same axis with VLA viewpoint canonicalization, field LiDAR navigation, UAV SLAM/VO evaluation, and manipulation benchmarks with tactile or partial-geometry state.",
            },
            {
                "label": "New signal",
                "history": "Recent RI notes had driving world models and safety shields, but less explicit decision-aligned latent wording.",
                "body": "DA-WAM and Decision-Metric Alignment make the latent-world-model objective directly accountable to the downstream decision metric.",
            },
            {
                "label": "Missing axis",
                "history": "Backfill source lacks abstracts and full text.",
                "body": "The current artifact should be treated as a triage map; full mechanism and experiment claims require official abstract/PDF follow-up before use in a proposal.",
            },
        ],
        "strategy": [
            {
                "priority": "Build moat",
                "title": "Policy-facing geometry stress suite",
                "thesis": "Test whether viewpoint canonicalization, metric SLAM, visual odometry, and field LiDAR cues change robot action robustness.",
                "scores": {"fit": 5, "novelty": 4, "feasibility": 4, "moat": 5, "timing": 5, "evidence": 3},
                "one_week": "Create camera-shift and field-route episodes with GS map, SLAM/VO, and LiDAR navigation variants around the same policy.",
                "four_week": "Build a reusable route/manipulation suite that exports viewpoint error, scale drift, route recovery, and action deltas.",
                "success": "A geometry intervention predicts or prevents a policy failure that success-only metrics hide.",
                "stop": "Geometry variants do not change policy ranking or failure prediction under controlled camera and route shifts.",
                "asset": "Camera-shift videos, route traces, scale checks, LiDAR navigation logs, and action-delta labels.",
            },
            {
                "priority": "Build moat",
                "title": "Manipulation state-label benchmark",
                "thesis": "Separate deformability, lab-tool hierarchy, partial-view geometry, human video edit quality, and reward transition labels.",
                "scores": {"fit": 5, "novelty": 4, "feasibility": 4, "moat": 5, "timing": 4, "evidence": 3},
                "one_week": "Annotate ten manipulation failures with material deformation, tool-subtask boundary, hidden local geometry, and recovery action labels.",
                "four_week": "Turn the labels into a small benchmark that compares human-video-derived experience, reward models, and partial-view grasping.",
                "success": "State labels explain a policy failure or recovery difference that final success does not.",
                "stop": "Labels collapse to the same ranking as final success or cannot be annotated reliably.",
                "asset": "Failure-state taxonomy, annotated clips, tactile/deformation notes, subtask hierarchy, and partial-view geometry labels.",
            },
            {
                "priority": "Explore",
                "title": "Decision-aligned world-model probe",
                "thesis": "Evaluate whether future latents preserve the variable that changes a driving, navigation, or whole-body control decision.",
                "scores": {"fit": 4, "novelty": 5, "feasibility": 3, "moat": 4, "timing": 5, "evidence": 3},
                "one_week": "Use three traffic or navigation scenes where one latent variable changes braking, route choice, or control recovery.",
                "four_week": "Compare decision-aligned latent objectives with video-quality or reconstruction objectives under matched scenarios.",
                "success": "Decision-aligned latents better predict action changes or near-miss avoidance than visual-quality scores.",
                "stop": "Latent alignment improves no downstream decision metric under controlled scenario edits.",
                "asset": "Edited scenarios, latent probes, decision deltas, near-miss labels, and control outcome traces.",
            },
        ],
    }
}


def main() -> int:
    (ROOT / "intelligence").mkdir(exist_ok=True)
    (ROOT / "posts").mkdir(exist_ok=True)
    for date, data in RI_BY_DATE.items():
        (ROOT / "intelligence" / f"{date}.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (ROOT / "posts" / f"{date}-research-intelligence.html").write_text(
            build_html(data),
            encoding="utf-8",
            newline="\n",
        )
        print(f"wrote intelligence/{date}.json and posts/{date}-research-intelligence.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
