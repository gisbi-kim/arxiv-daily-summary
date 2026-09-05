#!/usr/bin/env python3
"""Generate the 2026-09-04 Research Intelligence edition."""

from __future__ import annotations

import json
from pathlib import Path

from gen_research_intelligence_20260811 import build_html


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PROMPT = "prompts/instruction_v20260713.md"


RI_BY_DATE = {
    "2026-09-04": {
        "date": "2026-09-04",
        "edition": "Research Intelligence",
        "source_prompt": SOURCE_PROMPT,
        "source_mode": "new",
        "scope_note": (
            "Daily edition from matching Friday /new listings: 112 non-replacement cs.CV rows, "
            "48 cs.RO rows, 151 deduplicated papers, and 128 ROI papers. Tier A cards are conservative "
            "abstract-only autopsies from the repository parser output; no figure, table, full-text, code, "
            "or dataset-release claim is asserted unless the abstract itself states it."
        ),
        "executive_thesis": (
            "The September 4 batch turns evidence budgeting into the center of robot intelligence. Geometry "
            "papers ask which pose, Doppler, wire, semantic-map, or reconstruction signal remains reliable enough "
            "to define an action frame. Robot learning papers reject raw demonstration volume and instead gate "
            "training through modality relevance, web-video retrieval, real-to-sim evaluation, world-model "
            "imagination schedules, and action-sufficient intermediate features. World-model papers make the same "
            "move at the future-state layer: imagined futures, camera actions, and physical events matter only when "
            "they preserve consequences that change control. VLM, safety, and systems papers then attack the output "
            "layer by asking whether the answer, compressed token set, privacy-preserving export, restored image, or "
            "runtime monitor kept the evidence needed for a safe decision."
        ),
        "decision_cards": [
            {
                "label": "Decision",
                "title": "Evidence has to earn action authority",
                "body": (
                    "EGR, GIFT, FailBench, CoverPruner, and PZR all convert a score into a question about which "
                    "sensor, feature, token, or uncertainty set is allowed to affect the next decision."
                ),
            },
            {
                "label": "Decision",
                "title": "Geometry is becoming a failure contract",
                "body": (
                    "Scal3R, TRaIL-Odom, WireSeg-32K, and robotic weld mapping all judge geometry by drift, "
                    "contact consistency, sensor degeneracy, and downstream robot use rather than appearance alone."
                ),
            },
            {
                "label": "Decision",
                "title": "World models need bounded intervention",
                "body": (
                    "WISE, WorldReward, VeriPhy, physically grounded JEPA, and RIWM treat imagination as a "
                    "scheduled, audited, and risk-qualified intervention instead of an always-trusted simulator."
                ),
            },
        ],
        "papers": [
            {
                "rank": 1,
                "title": "Sensing Which Modality Matters: Evidence-Gated Regularization for Robust VLA Policies",
                "arxiv_id": "2609.03142",
                "fit": "VLA robustness - modality relevance - real-robot occlusion and distractor tests",
                "status": "Tier A - abstract-only",
                "status_quo": "Multimodal VLA policies often fuse every available sensor and hope training will ignore nuisance correlations.",
                "friction": "The abstract names modality entanglement: low-evidence sensors can still dominate under occlusion or distractors, while one informative sensor may not be sufficient.",
                "hidden_premise": "A policy should become invariant to low-evidence sensors and sufficient on high-evidence sensors before multimodal fusion is trusted.",
                "conceptual_move": "Turn sensor fusion into a per-frame, per-sensor evidence gate that regularizes the training objective without inference-time overhead.",
                "mechanism": "EGR derives task-relevance signals and applies state-conditional consistency objectives for low-evidence invariance and high-evidence sufficiency.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper introduces a BEHAVIOR-1K diagnostic suite and 47 rollout-based skills for modality entanglement."},
                    {"trace": "[Abstract]", "claim": "It reports gains under uninformative-sensor corruption, single-sensor fallback, and physical-object distractors on two real robot embodiments."},
                    {"trace": "[Inference]", "claim": "APRL should evaluate whether each sensor actually changes action safety before treating more modalities as stronger evidence."},
                ],
                "falsification": "If evidence gates collapse under unseen tasks or new sensor layouts, the method may be regularizing benchmark-specific correlations.",
                "adversarial": "Create scenes where tactile, wrist, and external camera cues alternate between helpful, irrelevant, and misleading while task success is held constant.",
                "thinking_tool": "Multimodal evidence is useful only after low-evidence invariance and high-evidence sufficiency are separated.",
                "transfer_boundary": "Strong for multi-camera and visuotactile robot policies; weaker for single-sensor settings without an evidence partition.",
            },
            {
                "rank": 2,
                "title": "Scal3R: Learning Efficient Multi-Relative Pose Query for Scalable Online 3D Reconstruction",
                "arxiv_id": "2609.04201",
                "fit": "online 3D reconstruction - long-video pose drift - multi-reference pose graph",
                "status": "Tier A - abstract-only",
                "status_quo": "Online reconstruction often anchors pose regression to the first frame, forcing long videos into extrapolation beyond training distribution.",
                "friction": "The abstract says depth stays locally stable while the global pose head collapses, so pose and local geometry fail differently.",
                "hidden_premise": "A reconstruction can be robot-usable only if global pose drift is repaired without discarding stable local depth evidence.",
                "conceptual_move": "Reformulate online reconstruction as multi-reference relative pose querying with lightweight tokens and pose-graph loop closure.",
                "mechanism": "Scal3R injects learnable pose-query tokens into a frozen backbone and queries poses relative to multiple past keyframes.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper reports more than 60 percent average ATE reduction on KITTI over the online baseline."},
                    {"trace": "[Abstract]", "claim": "It uses online pose-graph optimization with loop closure to suppress long-range drift."},
                    {"trace": "[Inference]", "claim": "APRL should score feed-forward reconstruction by relocalization and route or grasp changes under accumulated pose error."},
                ],
                "falsification": "If drift reduction does not improve downstream localization or manipulation frames, Scal3R remains a reconstruction metric win rather than a robot-validity win.",
                "adversarial": "Stress repeated corridors, moving objects, and loop-closure aliases where local depth appears stable but global action frames flip.",
                "thinking_tool": "Separate local geometry evidence from global pose authority before releasing a map for robot action.",
                "transfer_boundary": "Strong for long-video mapping and navigation; less direct for short tabletop clips where first-frame anchoring is not the bottleneck.",
            },
            {
                "rank": 3,
                "title": "TRaIL-Odom: Tightly Coupled Continuous Time Radar-IMU-LiDAR Odometry with Adaptive Doppler Weighting",
                "arxiv_id": "2609.03561",
                "fit": "radar-IMU-LiDAR odometry - directional degeneracy - adaptive Doppler weighting",
                "status": "Tier A - abstract-only",
                "status_quo": "Radar-LiDAR fusion often applies fixed residual weights even when LiDAR geometry and radar Doppler are directionally informative in different ways.",
                "friction": "The abstract says fixed radar weighting misallocates Doppler information across translational directions under geometric degeneracy.",
                "hidden_premise": "Sensor fusion should allocate trust by the currently weak motion subspace, not by a global sensor prior.",
                "conceptual_move": "Treat Doppler constraints as direction- and scan-dependent evidence that is reweighted against LiDAR geometric anisotropy.",
                "mechanism": "TRaIL-Odom combines per-point Doppler reweighting with scan-wise radar gain scheduling in a tightly coupled continuous-time odometry framework.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "Across 13 sequences the method reports state-of-the-art overall performance and clear advantages in degenerate scenes."},
                    {"trace": "[Abstract]", "claim": "In three degenerate ablations, both adaptive modules reduce RMSE ATE and RTE by 86.0 percent and 78.5 percent relative to fixed weighting."},
                    {"trace": "[Inference]", "claim": "APRL should condition odometry fusion weights on which direction is currently unobservable before planning trusts the pose."},
                ],
                "falsification": "If adaptive weights do not improve recovery in robot navigation decisions, the odometry gain may not translate beyond trajectory metrics.",
                "adversarial": "Use tunnels, flat walls, wet surfaces, and lateral motion where radar and LiDAR disagree about the weak direction.",
                "thinking_tool": "A sensor's evidence value is directional and state-dependent.",
                "transfer_boundary": "Direct for field robots with radar, LiDAR, and IMU; less direct for pure vision SLAM without Doppler constraints.",
            },
            {
                "rank": 4,
                "title": "R2S-Eval: Robot Evaluation with Real-to-Sim Calibration via Vision-Language Models",
                "arxiv_id": "2609.03276",
                "fit": "robot evaluation - real-to-sim calibration - VLM preference ranking",
                "status": "Tier A - abstract-only",
                "status_quo": "Robot policy evaluation is often treated as repeated hardware trials with binary success rates.",
                "friction": "The abstract says real-world evaluation is labor-intensive, unstable, and can produce different policy rankings across repeated runs.",
                "hidden_premise": "A calibrated simulator and behavior-level preference evaluator can expose execution quality differences hidden by final success labels.",
                "conceptual_move": "Move robot evaluation from manual success counting to calibrated rollout videos and aggregated pairwise preference conclusions.",
                "mechanism": "R2S-Eval generates real-to-sim calibrated rollout videos and asks a VLM evaluator to rank execution quality before aggregating policy preferences.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The pipeline is reported to achieve agreement with human preferences and reduce repeated hardware-operation effort."},
                    {"trace": "[Abstract]", "claim": "It reveals behavior-quality differences not captured by binary success labels."},
                    {"trace": "[Inference]", "claim": "APRL should publish policy rankings with calibration uncertainty and behavior-quality axes, not only success rate."},
                ],
                "falsification": "If VLM preferences are biased by simulator visuals or fail on new domains, real-to-sim calibration may stabilize the wrong ranking.",
                "adversarial": "Hold final success fixed while changing collision margin, hesitation, contact force, and recovery quality in calibrated rollout videos.",
                "thinking_tool": "Evaluation is a conclusion protocol, not a counter of terminal successes.",
                "transfer_boundary": "Strong for manipulation policy comparison; weaker for tasks where simulated videos cannot preserve critical tactile or force evidence.",
            },
            {
                "rank": 5,
                "title": "WISE: World-model-guided Imagination Scheduling for Efficient Post-training of Vision-Language-Action Models",
                "arxiv_id": "2609.03681",
                "fit": "VLA post-training - imagination scheduling - bounded future evidence",
                "status": "Tier A - abstract-only",
                "status_quo": "World models are often used as always-on imagined rollout engines for policy refinement.",
                "friction": "The abstract says imagination value varies by execution stage, while long rollouts can accumulate errors and introduce unreliable supervision.",
                "hidden_premise": "Imagined futures should refine policy actions only at interaction-relevant states and inside a trusted horizon.",
                "conceptual_move": "Schedule when and how world-model imagination is invoked during VLA post-training instead of using full imagination everywhere.",
                "mechanism": "WISE selectively invokes bounded multi-view rollouts, evaluates candidate futures with progress and completion signals, and uses relative outcomes for action refinement.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The method reports consistent improvements across manipulation tasks while reducing GPU computation time by about 80 percent compared with full imagination."},
                    {"trace": "[Abstract]", "claim": "Real-world evaluations show gains in robustness and generalization under distribution shifts."},
                    {"trace": "[Inference]", "claim": "APRL should record where imagination changes action ranking and where it becomes unreliable supervision."},
                ],
                "falsification": "If scheduling mostly removes hard cases, it may improve efficiency while leaving rare failure recovery unsolved.",
                "adversarial": "Force imagination at contact transitions, ambiguous object states, and recovery branches to find the horizon where supervision turns harmful.",
                "thinking_tool": "World-model imagination is an intervention with timing and stop conditions.",
                "transfer_boundary": "Strong for manipulation VLA post-training; weaker for policies whose world model cannot represent contact or hidden state.",
            },
            {
                "rank": 6,
                "title": "GIFT: Guided Intermediate Feature Training via Action-Oriented Structural Supervision for Robotic Manipulation",
                "arxiv_id": "2609.04193",
                "fit": "robot manipulation - action-sufficiency gap - intermediate feature supervision",
                "status": "Tier A - abstract-only",
                "status_quo": "Vision-language pretraining and world modeling can preserve rich visual information that is not useful for control.",
                "friction": "The abstract names an action-sufficiency gap: semantic and predictive features may omit geometry, affordance, or goal structure that actions need.",
                "hidden_premise": "Intermediate features should be supervised by control-relevant structure without forcing every model into the same action formulation.",
                "conceptual_move": "Guide intermediate robot features through geometry alignment, affordance prediction, and goal-region reconstruction.",
                "mechanism": "GIFT is instantiated in VLA, direct-action WAM, and inverse-dynamics WAM variants while retaining each model's action formulation.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "GIFT variants outperform corresponding baselines on LIBERO-Plus and RoboCasa."},
                    {"trace": "[Abstract]", "claim": "The gains are highlighted for articulated-object tasks and unseen visual and spatial perturbations."},
                    {"trace": "[Inference]", "claim": "APRL should evaluate whether intermediate structure predicts action errors before final success changes."},
                ],
                "falsification": "If structural supervision helps only when benchmark labels mirror the auxiliary tasks, the action-sufficiency claim is over-broad.",
                "adversarial": "Hide affordance cues, perturb geometry, and change goal regions independently to test which structure actually controls action.",
                "thinking_tool": "A feature is useful only if it is sufficient for the next action, not if it is visually rich.",
                "transfer_boundary": "Strong for manipulation and WAM/VLA comparisons; weaker for language-only planning or tasks without structural labels.",
            },
            {
                "rank": 7,
                "title": "FailBench: How Reliable are VLMs at Judging Robot Task Success?",
                "arxiv_id": "2609.03611",
                "fit": "robot outcome evaluation - VLM judge reliability - failure detection",
                "status": "Tier A - abstract-only",
                "status_quo": "Robot pipelines increasingly use VLMs as inexpensive judges for manipulation outcomes.",
                "friction": "The abstract says existing benchmarks offer limited evidence of cross-domain generalization for robot failure detection.",
                "hidden_premise": "A judge can authorize evaluation conclusions only if it detects failure modes across tasks, domains, and visual conditions.",
                "conceptual_move": "Make robot-success judging itself a benchmarked perception problem rather than an assumed service.",
                "mechanism": "FailBench supplies manipulation outcome examples for testing whether VLMs can reliably judge task success and failure.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The benchmark comprises 2,197 manipulation examples."},
                    {"trace": "[Abstract]", "claim": "It targets cross-domain robot failure detection rather than ordinary VQA accuracy."},
                    {"trace": "[Inference]", "claim": "APRL should validate every VLM evaluator before using it to rank robot policies."},
                ],
                "falsification": "If the benchmark lacks force, tactile, or invisible-state failures, a VLM may pass while missing robot-relevant failures.",
                "adversarial": "Create visually successful but physically invalid trials, and physically successful but visually ambiguous trials, then compare judge rankings.",
                "thinking_tool": "Evaluation agents need their own deployment benchmark.",
                "transfer_boundary": "Strong for vision-observable manipulation outcomes; incomplete for hidden contact, force, or proprioceptive failures.",
            },
            {
                "rank": 8,
                "title": "VeriPhy: Agentic Physical Reasoning for World Model Evaluation and Refinement",
                "arxiv_id": "2609.03153",
                "fit": "world-model evaluation - physical verification - auditable refinement",
                "status": "Tier A - abstract-only",
                "status_quo": "Generated videos can look fluent while violating physical obligations at specific moments.",
                "friction": "The abstract says visual fluency and scalar quality scores cannot identify the obligation a clip violates or the moment of failure.",
                "hidden_premise": "A world-model clip should be audited through named physical obligations that can localize and repair failures.",
                "conceptual_move": "Turn world-model evaluation into an agentic physical-verification workflow with explicit violation traces.",
                "mechanism": "VeriPhy uses a tool-using agent to check physical constraints and refine generated clips based on discovered failures.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper presents an auditable physical-verification system for generated video."},
                    {"trace": "[Abstract]", "claim": "It targets the obligation and moment where a clip fails, not only a scalar quality score."},
                    {"trace": "[Inference]", "claim": "APRL should define world-model failures as actionable physical obligations before using generated futures for planning."},
                ],
                "falsification": "If verifier obligations are incomplete or tuned to visible violations only, the system may miss control-relevant hidden state errors.",
                "adversarial": "Test contact persistence, support, collision, gravity, and camera-motion obligations independently under visually plausible clips.",
                "thinking_tool": "A generated future should carry a falsifiable physical obligation trace.",
                "transfer_boundary": "Strong for visual world-model auditing; weaker for tactile or force dynamics unless the verifier can observe them.",
            },
            {
                "rank": 9,
                "title": "Who Speaks for the Pruned? Visual Token Pruning as Coverage Optimization",
                "arxiv_id": "2609.03158",
                "fit": "VLM efficiency - visual token pruning - coverage of discarded evidence",
                "status": "Tier A - abstract-only",
                "status_quo": "Token pruning usually asks which visual tokens to keep and ignores what evidence the discarded tokens represented.",
                "friction": "The abstract says retained-token selection can preserve redundant high-scoring tokens while leaving discarded evidence uncovered.",
                "hidden_premise": "A compressed visual representation is trustworthy only if every removed token has a surviving representative for the target query and model.",
                "conceptual_move": "Formulate visual token pruning as representational coverage maximization rather than top-token retention.",
                "mechanism": "CoverPruner covers the full projected visual-token set with query-weighted demand using projector-space coverage and first-layer attention probes.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The method is training-free and reports the best average accuracy among compared methods across architectures and compression rates."},
                    {"trace": "[Abstract]", "claim": "The largest gains usually appear under aggressive compression."},
                    {"trace": "[Inference]", "claim": "APRL should measure whether pruned robot vision still covers the evidence that could change an action."},
                ],
                "falsification": "If coverage preserves semantics but misses geometry, grasp contact, or safety cues, it may still fail robot action admission.",
                "adversarial": "Prune scenes with small hazards, thin wires, transparent objects, and distant navigation cues while measuring action changes.",
                "thinking_tool": "Ask who represents the discarded evidence before accepting a cheaper visual context.",
                "transfer_boundary": "Strong for VLM visual context budgets; less direct for dense control policies that do not expose token-level evidence.",
            },
            {
                "rank": 10,
                "title": "Seeing Less Is Not Seeing Safely: Privacy Leakage from Task-Scoped Robot Perception Exports",
                "arxiv_id": "2609.03055",
                "fit": "robot privacy - task-scoped perception export - utility and leakage trade-off",
                "status": "Tier A - abstract-only",
                "status_quo": "A robot perception export can be treated as safe once raw sensor data stay local and only task-scoped structure leaves the device.",
                "friction": "The abstract says structured exports still leak household information through semantics, geometry, spatial structure, and task targets.",
                "hidden_premise": "A perception export should be released only after task utility and multiple residual inference risks are evaluated together.",
                "conceptual_move": "Profile downstream robot representations by utility, direct exposure, and held-out representation-aware privacy attacks.",
                "mechanism": "TFPD keeps rich perception local and evaluates navigation, collision checking, and object-goal exports on AI2-THOR and ProcTHOR splits.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "Three navigation exports achieve identical success and path ratio while linkability ranges from 0.532 to 0.970."},
                    {"trace": "[Abstract]", "claim": "Replacing explicit target labels with target regions reduces target-category macro-F1 while preserving near-identical task success."},
                    {"trace": "[Inference]", "claim": "APRL should evaluate robot representation exports as safety and privacy release decisions, not logging details."},
                ],
                "falsification": "If held-out attackers are weak or scene distributions are too narrow, leakage ordering may not transfer to real homes.",
                "adversarial": "Test target, geometry, topological, and semantic exports against attackers trained on disjoint houses and tasks.",
                "thinking_tool": "Seeing less is not a safety proof unless task utility and residual inference risk are jointly bounded.",
                "transfer_boundary": "Strong for domestic robots and cloud planner interfaces; less direct for fully local deployments with no representation export.",
            },
        ],
        "synthesis": [
            {
                "title": "Robot learning papers now name the evidence variable",
                "links": "EGR - RoboTok - R2S-Eval - WISE - GIFT",
                "facts": "The abstracts separate modality relevance, web-video motion retrieval, calibrated evaluation, imagination timing, and action-sufficient structure.",
                "inference": "The common decision is to let data, sensors, simulated futures, or features influence policy only after their action relevance is tested.",
            },
            {
                "title": "Geometry papers are release gates for downstream action",
                "links": "Scal3R - TRaIL-Odom - WireSeg-32K - semantic mapping - robotic weld mapping",
                "facts": "The batch covers pose drift, radar-LiDAR degeneracy, physically grounded wire deformation, dynamic semantic maps, and weld-seam localization.",
                "inference": "APRL should treat maps and reconstructions as candidates for action authority, with drift, contact, semantic freshness, and task error measured together.",
            },
            {
                "title": "Safety and efficiency papers reject average-score comfort",
                "links": "FailBench - CoverPruner - SafeRestore - PZR - privacy exports",
                "facts": "The papers test judge reliability, coverage of pruned evidence, detector-relative restoration risk, uncertainty monitor precision, and privacy leakage.",
                "inference": "Cheaper or safer-looking systems still need evidence-retention, risk, and failure-family tests before they can be trusted in a robot loop.",
            },
        ],
        "frontier_memory": [
            {
                "label": "Strengthening",
                "history": "August 31 through September 3 repeatedly framed robot intelligence as an action-release contract.",
                "body": "September 4 strengthens that contract with modality evidence gates, real-to-sim evaluation, world-model scheduling, robot judge benchmarks, and uncertainty monitors.",
            },
            {
                "label": "New signal",
                "history": "Earlier notes focused on provenance, geometry validity, and feedback-matched world models.",
                "body": "Today adds a stronger budget axis: visual tokens, sensor exports, imagination steps, and frame selections should be spent only when they preserve decision-changing evidence.",
            },
            {
                "label": "Contradiction",
                "history": "Robot learning often treats more modalities, more web demonstrations, or more imagined futures as better supervision.",
                "body": "EGR, WISE, CoverPruner, and privacy export work all show that extra evidence can be harmful, redundant, or leaky unless it is gated by relevance and risk.",
            },
            {
                "label": "Missing axis",
                "history": "Geometry, VLA evaluation, privacy, and runtime monitoring are still largely separate artifacts.",
                "body": "APRL can own a shared evidence-budget benchmark that ties sensor trust, geometry drift, privacy leakage, uncertainty precision, and action changes in one robot episode.",
            },
        ],
        "strategy": [
            {
                "priority": "Build moat",
                "portfolio": "Build moat",
                "title": "Evidence-budgeted robot action benchmark",
                "opportunity": "Evidence-budgeted robot action benchmark",
                "thesis": "Build robot episodes where every camera, tactile stream, map update, compressed token set, and imagined future must prove that it changes action safely.",
                "scores": {"strategic_fit": 5, "asymmetry": 5, "timing": 5, "tractability": 4, "defensibility": 5, "scientific_depth": 5},
                "one_week": "Create five manipulation and navigation episodes with informative, irrelevant, corrupted, duplicated, and missing sensor evidence.",
                "one_week_probe": "Create five manipulation and navigation episodes with informative, irrelevant, corrupted, duplicated, and missing sensor evidence.",
                "four_week": "Compare EGR-style gates, ordinary fusion, token pruning, real-to-sim evaluation, and uncertainty monitors under the same action-admission labels.",
                "four_week_build": "Compare EGR-style gates, ordinary fusion, token pruning, real-to-sim evaluation, and uncertainty monitors under the same action-admission labels.",
                "success": "An evidence gate changes unsafe action permission or recovery timing before final task success diverges on at least three failure families.",
                "success_metric": "An evidence gate changes unsafe action permission or recovery timing before final task success diverges on at least three failure families.",
                "stop": "Stop if evidence partitions do not change decisions beyond ordinary confidence or success-rate thresholds.",
                "stop_condition": "Stop if evidence partitions do not change decisions beyond ordinary confidence or success-rate thresholds.",
                "paper_path": "Evidence-budgeted action admission for multimodal robot policies.",
                "asset_path": "Robot episodes with sensor relevance labels, token budgets, action deltas, uncertainty sets, privacy exports, and fallback outcomes.",
                "asset": "Robot episodes with sensor relevance labels, token budgets, action deltas, uncertainty sets, privacy exports, and fallback outcomes.",
            },
            {
                "priority": "Exploit",
                "portfolio": "Exploit",
                "title": "Robot-usable geometry drift suite",
                "opportunity": "Robot-usable geometry drift suite",
                "thesis": "Evaluate maps and reconstructions by the pose, correspondence, contact, and semantic freshness failures that change downstream robot action.",
                "scores": {"strategic_fit": 5, "asymmetry": 4, "timing": 5, "tractability": 4, "defensibility": 5, "scientific_depth": 4},
                "one_week": "Record one corridor route and one tabletop cable or weld-like object with repeated views, weak labels, and sensor degeneracy.",
                "one_week_probe": "Record one corridor route and one tabletop cable or weld-like object with repeated views, weak labels, and sensor degeneracy.",
                "four_week": "Benchmark Scal3R-like reconstruction, radar/LiDAR odometry, semantic mapping, and task-specific segmentation against route and manipulation outcomes.",
                "four_week_build": "Benchmark Scal3R-like reconstruction, radar/LiDAR odometry, semantic mapping, and task-specific segmentation against route and manipulation outcomes.",
                "success": "A robot-validity metric predicts relocalization, grasp, or inspection failure better than reconstruction or trajectory metrics alone.",
                "success_metric": "A robot-validity metric predicts relocalization, grasp, or inspection failure better than reconstruction or trajectory metrics alone.",
                "stop": "Stop if downstream failures are fully explained by standard pose error and no representation-specific variable matters.",
                "stop_condition": "Stop if downstream failures are fully explained by standard pose error and no representation-specific variable matters.",
                "paper_path": "Robot-usable validity tests for online reconstruction, semantic maps, and sensor-degenerate odometry.",
                "asset_path": "Robot trajectories, wire or weld geometry, semantic update logs, odometry degeneracy labels, and downstream action outcomes.",
                "asset": "Robot trajectories, wire or weld geometry, semantic update logs, odometry degeneracy labels, and downstream action outcomes.",
            },
            {
                "priority": "Explore",
                "portfolio": "Explore",
                "title": "Scheduled imagination release gate",
                "opportunity": "Scheduled imagination release gate",
                "thesis": "Treat robot world-model imagination as a bounded intervention whose timing, horizon, and verifier must be released before it can train or guide a policy.",
                "scores": {"strategic_fit": 4, "asymmetry": 5, "timing": 5, "tractability": 3, "defensibility": 4, "scientific_depth": 5},
                "one_week": "Replay two manipulation tasks with imagined rollouts injected at contact approach, contact transition, recovery, and terminal phases.",
                "one_week_probe": "Replay two manipulation tasks with imagined rollouts injected at contact approach, contact transition, recovery, and terminal phases.",
                "four_week": "Compare full imagination, WISE-style scheduling, physical-verification rejection, and JEPA state-alignment gates under controlled distribution shifts.",
                "four_week_build": "Compare full imagination, WISE-style scheduling, physical-verification rejection, and JEPA state-alignment gates under controlled distribution shifts.",
                "success": "A scheduled or verified imagination policy beats full imagination under at least two shift families while using less compute.",
                "success_metric": "A scheduled or verified imagination policy beats full imagination under at least two shift families while using less compute.",
                "stop": "Stop if imagination timing does not alter policy ranking or if verifier errors correlate poorly with action failure.",
                "stop_condition": "Stop if imagination timing does not alter policy ranking or if verifier errors correlate poorly with action failure.",
                "paper_path": "Timed and verified imagination as a release gate for VLA post-training.",
                "asset_path": "Imagined-future traces, injection timings, physical-obligation labels, action rankings, and compute profiles.",
                "asset": "Imagined-future traces, injection timings, physical-obligation labels, action rankings, and compute profiles.",
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
