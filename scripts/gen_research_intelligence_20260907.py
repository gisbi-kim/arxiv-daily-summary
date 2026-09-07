#!/usr/bin/env python3
"""Generate the 2026-09-07 Research Intelligence edition."""

from __future__ import annotations

import json
from pathlib import Path

from gen_research_intelligence_20260811 import build_html


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PROMPT = "prompts/instruction_v20260713.md"


RI_BY_DATE = {
    "2026-09-07": {
        "date": "2026-09-07",
        "edition": "Research Intelligence",
        "source_prompt": SOURCE_PROMPT,
        "source_mode": "new",
        "scope_note": (
            "Daily edition from matching Monday /new listings: 110 non-replacement cs.CV rows, "
            "41 cs.RO rows, 138 deduplicated papers, and 112 ROI papers. Tier A cards are conservative "
            "abstract-only autopsies from the repository parser output; no figure, table, full-text, code, "
            "or dataset-release claim is asserted unless the abstract itself states it."
        ),
        "executive_thesis": (
            "The September 7 batch moves the robotics question from whether a model can finish a benchmark "
            "episode to whether the system can identify the evidence that should change action before, during, "
            "and after failure. VLA papers expose timestamped failure detection, spatial-procedural difficulty, "
            "conditional visual grounding, failure recovery, tactile action correction, and paraphrase-stable "
            "reward modeling as separate release gates. Geometry papers make 3DGS, SfM, cross-view depth, open-set "
            "scene graphs, and radar-enhanced odometry useful only when they become navigation, localization, or "
            "field-robot benchmarks. World-model papers split imagination into physical exploration, trajectory "
            "planning, scenario generation, and remote-control resilience, while VLM and systems papers ask which "
            "latent concept, view, gaze feature, token, memory trace, or thermal budget may be trusted inside a "
            "deployed decision loop."
        ),
        "decision_cards": [
            {
                "label": "Decision",
                "title": "Failure needs a timestamp and a recovery contract",
                "body": (
                    "FailureSpot, RoboSPA, conditional visual grounding, LIBERO-Recover, TacPAC, and ROBORMBENCH "
                    "all reject terminal success as the only robotics signal."
                ),
            },
            {
                "label": "Decision",
                "title": "Geometry must become a task protocol",
                "body": (
                    "NavArena, FIRE-LIVWO, BLASt3R, HiSfM, CrossDepth, and open-set 3D scene graphs turn geometric "
                    "representations into navigation, localization, and observability tests."
                ),
            },
            {
                "label": "Decision",
                "title": "Efficient evidence must remain accountable",
                "body": (
                    "FailSAE, FAVE, LookThere, MCPO, gaze privacy, and DVFS papers ask which compressed or selected "
                    "signal still explains the decision, the failure, and the cost."
                ),
            },
        ],
        "papers": [
            {
                "rank": 1,
                "title": "FailureSpot: Label-Efficient Timestamp-Level Failure Detection for Vision-Language-Action Models",
                "arxiv_id": "2609.04277",
                "fit": "VLA deployment - timestamp-level failure localization - weak supervision from action chunks",
                "status": "Tier A - abstract-only",
                "status_quo": "VLA failure detection is often evaluated at the trajectory level, after the policy has already taken wrong actions.",
                "friction": "The abstract says trajectory-level labels turn normal pre-failure behavior into noisy failure supervision.",
                "hidden_premise": "Failure supervision should be aligned to the moment when the action stream becomes abnormal, not to the final episode label.",
                "conceptual_move": "Use unlabeled action chunks to generate weak timestamp signals, then spend dense labels only on uncertain trajectories.",
                "mechanism": "The method detects inconsistent consecutive chunks, frozen or idle actions, and aggressive random motions before fine-tuning with active timestamp labels.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper targets fine-grained timestamp-level VLA failure detection."},
                    {"trace": "[Abstract]", "claim": "It combines action-derived weak supervision with active learning for timestamp annotation."},
                    {"trace": "[Inference]", "claim": "APRL should ask how early a detector changes continuation, recovery, or stop decisions before terminal failure."},
                ],
                "falsification": "If action-derived weak labels mostly mark benign exploration or pause behavior, timestamp localization can become a style detector rather than a failure detector.",
                "adversarial": "Evaluate false alarms on slow cautious policies and missed alarms on smooth but wrong object-selection failures.",
                "thinking_tool": "Treat failure as a time-localized control variable, not a post-hoc episode attribute.",
                "transfer_boundary": "Direct for long-horizon VLA manipulation; less direct for short single-step actions where failure timing is ambiguous.",
            },
            {
                "rank": 2,
                "title": "RoboSPA: Can VLA Models Go Beyond Simple Scenes and Short-Horizon Tasks?",
                "arxiv_id": "2609.05324",
                "fit": "VLA diagnostics - spatial ambiguity - long-horizon procedural planning",
                "status": "Tier A - abstract-only",
                "status_quo": "Manipulation benchmarks often report completion under predefined settings and hide which reasoning burden caused failure.",
                "friction": "The abstract says current VLA systems struggle when spatial relations, low-level execution, and memory-intensive planning grow together.",
                "hidden_premise": "A deployable VLA should be evaluated on graded spatial and procedural difficulty, not only on a flat task list.",
                "conceptual_move": "Build a diagnostic benchmark whose tasks vary along fine-grained spatial reasoning and long-horizon procedural planning.",
                "mechanism": "RoboSPA instantiates 56 base tasks across five difficulty levels and reports diagnostic metrics beyond binary success.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "RoboSPA covers 10 task categories, 56 base tasks, and 280 variants."},
                    {"trace": "[Abstract]", "claim": "It uses 527K trajectories across multiple embodiments and diverse scenes."},
                    {"trace": "[Inference]", "claim": "APRL should separate spatial ambiguity, procedural memory, and execution precision before calling a VLA robust."},
                ],
                "falsification": "If difficulty levels correlate with dataset collection artifacts, the benchmark may measure distribution familiarity rather than reasoning complexity.",
                "adversarial": "Hold object identity and motor primitive constant while independently increasing spatial ambiguity and procedure length.",
                "thinking_tool": "Benchmark difficulty should name the cognitive variable that broke the action.",
                "transfer_boundary": "Strong for manipulation VLA evaluation; weaker for navigation unless spatial-procedural axes are adapted to route state.",
            },
            {
                "rank": 3,
                "title": "What Matters, When? Diagnosing and Improving Conditional Visual Grounding in Visuomotor Imitation Policies",
                "arxiv_id": "2609.05376",
                "fit": "visuomotor grounding - manipulation phase - distractor intervention",
                "status": "Tier A - abstract-only",
                "status_quo": "Visual robustness is often treated as one property of a policy across the whole rollout.",
                "friction": "The abstract says distractor sensitivity depends on both visual similarity and manipulation phase.",
                "hidden_premise": "The target evidence needed for control changes over time, so grounding should be diagnosed at phase and state level.",
                "conceptual_move": "Frame imitation-policy failure as conditional visual grounding instead of generic visual distribution shift.",
                "mechanism": "The study localizes failures to picking and placement, then tests distractor augmentation, phase-dependent attention regularization, and visual prompting.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The work systematically introduces distractor objects and receptacles with controlled color and shape similarity."},
                    {"trace": "[Abstract]", "claim": "Interventions improve robustness in simulation and on a physical UR3e."},
                    {"trace": "[Inference]", "claim": "APRL should label which visual cue must matter at each manipulation phase before evaluating grounding."},
                ],
                "falsification": "If phase labels are unavailable or intervention gains do not survive new task families, the diagnosis may be policy- and task-specific.",
                "adversarial": "Swap distractor relevance between pick and place phases while preserving the same final object set.",
                "thinking_tool": "Ask what visual evidence matters when, not whether the scene is generally harder.",
                "transfer_boundary": "Direct for imitation manipulation; less direct for policies whose state estimator already provides explicit object and goal states.",
            },
            {
                "rank": 4,
                "title": "LIBERO-RECOVER: Beyond Task Success Towards Failure Recovery in Robotic Manipulation Models",
                "arxiv_id": "2609.05178",
                "fit": "robot manipulation - failure recovery benchmark - post-failure reasoning",
                "status": "Tier A - abstract-only",
                "status_quo": "Near-perfect LIBERO success rates can be read as deployment readiness.",
                "friction": "The abstract says ideal initial-state success does not measure failed grasps, collisions, unintended object movement, or continuation after failure.",
                "hidden_premise": "A manipulation model is reliable only if it recognizes and repairs the state created by its own mistakes.",
                "conceptual_move": "Shift evaluation from task completion to four levels of recovery: retry, adaptation, object-state recovery, and environmental recovery.",
                "mechanism": "The benchmark collects real execution failures from strong embodied models and evaluates spatial, object-structure, interaction, and topological reasoning.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The benchmark contains 1,000+ recovery scenarios built on LIBERO."},
                    {"trace": "[Abstract]", "claim": "It changes the question from whether the robot succeeds to whether it can recover after failure."},
                    {"trace": "[Inference]", "claim": "APRL should score policies by recovery depth and residual state repair, not only first-pass success."},
                ],
                "falsification": "If recovery scenarios are too close to the source models' own failure distribution, benchmark performance may not transfer to new robots or tasks.",
                "adversarial": "Induce failures that preserve visual appearance but change contact, topology, or object affordance so recovery cannot rely on screenshots alone.",
                "thinking_tool": "Deployment readiness starts after the first failure, not before it.",
                "transfer_boundary": "Strong for manipulation; less direct for pure perception benchmarks without state-altering actions.",
            },
            {
                "rank": 5,
                "title": "NavArena: Automated Construction of Goal-Oriented Navigation Benchmarks from 3D Gaussian Splatting Reconstructions",
                "arxiv_id": "2609.04602",
                "fit": "3DGS - goal-oriented navigation - closed-loop benchmark generation",
                "status": "Tier A - abstract-only",
                "status_quo": "3DGS scenes are often treated as view-synthesis assets rather than navigation environments.",
                "friction": "The abstract says fixed 3DGS reconstructions lack traversability constraints, valid goals, and closed-loop protocols.",
                "hidden_premise": "A realistic scene representation is useful for navigation only if it can answer reachability, collision, and semantic-goal queries.",
                "conceptual_move": "Transform frozen 3DGS reconstructions into goal-oriented visual navigation benchmarks.",
                "mechanism": "NavArena derives occupancy costmaps from Gaussian density and height statistics, lifts semantic goals from open-vocabulary masks, and evaluates closed-loop episodes.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The framework generates 22.2 million expert trajectories across more than 2,000 scenes."},
                    {"trace": "[Abstract]", "claim": "It supports automatic generation and unified closed-loop evaluation of goal-oriented navigation episodes."},
                    {"trace": "[Inference]", "claim": "APRL should evaluate 3DGS maps by navigation success, collision queries, and semantic goal validity."},
                ],
                "falsification": "If Gaussian-derived occupancy misses transparent, movable, or robot-specific traversability constraints, the benchmark may overstate map usability.",
                "adversarial": "Compare 3DGS-derived occupancy against real robot traversability and dynamic obstacles under identical goal requests.",
                "thinking_tool": "A reconstruction becomes a robotics asset only after it defines valid actions and invalid collisions.",
                "transfer_boundary": "Strong for visual navigation and map evaluation; less direct for manipulation where contact geometry must be finer.",
            },
            {
                "rank": 6,
                "title": "FIRE-LIVWO: Robust LiDAR-Inertial-Visual-Wheel Odometry via Failure-Immune mmWave Radar Enhancement",
                "arxiv_id": "2609.05325",
                "fit": "field SLAM - underground degeneracy - adaptive multimodal observability",
                "status": "Tier A - abstract-only",
                "status_quo": "Multimodal odometry can still apply fixed trust in LiDAR, vision, wheel, and radar signals.",
                "friction": "The abstract describes smoke, dust, and self-similar corridors that remove visual information, weaken LiDAR features, and induce drift.",
                "hidden_premise": "Fusion weights should change when observability boundaries change in the field.",
                "conceptual_move": "Use failure-immune radar enhancement and online modality switching grounded in geometric and visual observability.",
                "mechanism": "FIRE-LIVWO fuses 4D mmWave radar, LiDAR, visual features, and wheel odometry in an IESKF with Doppler constraints and non-holonomic compensation.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The method identifies failure boundaries and switches modality weights under extreme underground conditions."},
                    {"trace": "[Abstract]", "claim": "Real-world underground coal mine experiments report average localization error of 5.677 m."},
                    {"trace": "[Inference]", "claim": "APRL should score odometry by when the system detects loss of observability and changes trust."},
                ],
                "falsification": "If switching thresholds are tuned to one mine geometry, robustness may not transfer to other corridors, tunnels, or sensor mountings.",
                "adversarial": "Create smoke, dust, repeated corridor, wheel-slip, and radar multipath splits that force different sensor failures.",
                "thinking_tool": "Pose estimates need observability-aware trust, not only lower average error.",
                "transfer_boundary": "Direct for field robots with radar, LiDAR, camera, and wheel sensing; less direct for indoor RGB-only navigation.",
            },
            {
                "rank": 7,
                "title": "TourPhysics: Bringing Physics to World Models for Exploration and Manipulation from a Single Image",
                "arxiv_id": "2609.04911",
                "fit": "visual world models - physical intervention - long-horizon exploration",
                "status": "Tier A - abstract-only",
                "status_quo": "Video world models can treat camera motion and physical intervention as similar appearance changes.",
                "friction": "The abstract says current models often lose physical or spatial consistency over long horizons.",
                "hidden_premise": "A world model should preserve a committed simulator state while using generation only for observations and appearance memory.",
                "conceptual_move": "Separate simulator state, geometric evidence, generator controls, and appearance memory during online exploration and manipulation.",
                "mechanism": "For each action, a simulator computes finite physical and camera trajectories; accepted observations update appearance memory while committed state remains fixed.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "TourPhysics distinguishes observation from physical intervention."},
                    {"trace": "[Abstract]", "claim": "It reports closer adherence to prescribed camera and object trajectories and reduced appearance drift during long-horizon revisits."},
                    {"trace": "[Inference]", "claim": "APRL should require world-model predictions to state which variables are simulated, generated, committed, or retryable."},
                ],
                "falsification": "If deterministic simulator assumptions dominate cases where contact or deformation is uncertain, the generated world may look consistent while missing real failure modes.",
                "adversarial": "Perturb hidden contact, object mass, and camera revisit loops to test where appearance memory masks physical state error.",
                "thinking_tool": "World-model observations should not be allowed to rewrite physical state without an explicit acceptance rule.",
                "transfer_boundary": "Strong for exploration and manipulation simulation; weaker for real-time control without a simulator state estimate.",
            },
            {
                "rank": 8,
                "title": "TacPAC: Tactile Prediction and Real-Time Action Correction in World-Action Models for Contact-Rich Manipulation",
                "arxiv_id": "2609.05266",
                "fit": "contact-rich manipulation - tactile feedback - action correction timing",
                "status": "Tier A - abstract-only",
                "status_quo": "World-action models commonly predict future observations before execution, with vision as the dominant future signal.",
                "friction": "The abstract says predicting future tactile observations naively recovers only a third of the achievable gain because feedback arrives during execution.",
                "hidden_premise": "Tactile evidence should be interpreted against the contact the plan expected, then used to correct the remaining action chunk.",
                "conceptual_move": "Turn tactile prediction from an added future view into a real-time correction mechanism.",
                "mechanism": "TacPAC caches the predicted contact and plan representation, then a tactile expert compares newly observed tactile images against that cache.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "One correction is reported as 20.7x cheaper than regenerating the action chunk."},
                    {"trace": "[Abstract]", "claim": "On five real-robot tasks, average success rises from 22 percent for the vision-only base model to 64 percent."},
                    {"trace": "[Inference]", "claim": "APRL should measure whether tactile prediction changes the remaining action before contact damage accumulates."},
                ],
                "falsification": "If tactile cache comparison only works for trained contact regimes, it may fail under new materials, compliance, or object geometry.",
                "adversarial": "Vary insertion clearance, fragile-object stiffness, and reorientation slip while holding visual observations nearly constant.",
                "thinking_tool": "Feedback is useful when it corrects an unexecuted action, not when it explains a completed failure.",
                "transfer_boundary": "Direct for tactile manipulation; weaker for tasks without contact sensing or chunked action execution.",
            },
            {
                "rank": 9,
                "title": "FailSAE: Towards Interpretable Failure Prediction for Vision-Language Models via Sparse Autoencoders",
                "arxiv_id": "2609.04276",
                "fit": "VLM failure prediction - interpretable sparse latents - runtime recovery",
                "status": "Tier A - abstract-only",
                "status_quo": "Failure predictors often use confidence scores or auxiliary classifiers that do not explain why the model is about to fail.",
                "friction": "The abstract says these methods can predict failures but provide limited interpretability.",
                "hidden_premise": "A failure warning is more useful when it names the latent concept drift behind the risk.",
                "conceptual_move": "Use sparse autoencoder latent activations as interpretable variables for VLM failure prediction.",
                "mechanism": "The pipeline trains sparse latent directions to remain interpretable while becoming informative for failure classification.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The framework outperforms evaluated baselines in failure prediction."},
                    {"trace": "[Abstract]", "claim": "Analysis suggests failures shift from class-specific concepts toward ambiguous or style-related concepts."},
                    {"trace": "[Inference]", "claim": "APRL should link failure warnings to interpretable state variables before handing authority to a VLM judge."},
                ],
                "falsification": "If sparse concepts do not align with robot-relevant causes, interpretability may be semantic while the action failure remains unexplained.",
                "adversarial": "Test cases where a visually plausible style cue and an action-critical object cue conflict.",
                "thinking_tool": "A warning should identify the concept that lost authority.",
                "transfer_boundary": "Strong for VLM classification and judging; needs adaptation before controlling robot action policies.",
            },
            {
                "rank": 10,
                "title": "Same Trajectory, Contradictory Rewards (ROBORMBENCH): Paraphrase Fragility in Vision Language Reward Models",
                "arxiv_id": "2609.05401",
                "fit": "robot reward models - paraphrase invariance - trajectory-grounded supervision",
                "status": "Tier A - abstract-only",
                "status_quo": "VLM reward models are often treated as semantic judges for robot progress.",
                "friction": "The abstract says paraphrasing the instruction alone can change predicted progress scores and flip the same behavior between failure and success.",
                "hidden_premise": "Reward functions must be invariant to task-preserving language before they can guide robot learning.",
                "conceptual_move": "Define paraphrase invariance as a core benchmark requirement for vision-language reward modeling.",
                "mechanism": "ROBORMBENCH pairs 2,390 real-robot trajectories with ground-truth progress labels and 21,673 verified paraphrases.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "Paraphrase-induced instability is reported as widespread and severe across proprietary and open-source VLMs."},
                    {"trace": "[Abstract]", "claim": "Dedicated reward models trained with trajectory-grounded supervision are substantially more stable."},
                    {"trace": "[Inference]", "claim": "APRL should reject VLM rewards that change under task-equivalent language rewrites."},
                ],
                "falsification": "If paraphrases are not truly task-equivalent under robot context, measured instability may mix language ambiguity with reward failure.",
                "adversarial": "Use task-preserving, constraint-changing, and action-goal rewrites on the same physical trajectory and require stable or intentionally changed rewards.",
                "thinking_tool": "A reward is not grounded unless semantically equivalent instructions produce the same action judgment.",
                "transfer_boundary": "Direct for robot reward learning and policy ranking; less direct for low-level controllers without language goals.",
            },
        ],
        "synthesis": [
            {
                "title": "VLA evaluation is becoming phase- and failure-aware",
                "links": "FailureSpot - RoboSPA - conditional visual grounding - LIBERO-Recover - TacPAC",
                "facts": "The abstracts separately expose timestamp labels, difficulty levels, phase-specific distractors, recovery levels, and tactile correction timing.",
                "inference": "The common decision is to locate when and why action should change before the final success label is trusted.",
            },
            {
                "title": "Geometry papers now ask for robot-facing protocols",
                "links": "NavArena - FIRE-LIVWO - BLASt3R - HiSfM - CrossDepth - 3D scene graphs",
                "facts": "The batch links 3DGS scenes, bundle adjustment, SfM disambiguation, surround depth, scene graphs, and radar-enhanced odometry to task evaluation.",
                "inference": "APRL should make geometry claims answer navigation, localization, observability, and closed-loop validity tests.",
            },
            {
                "title": "VLM and reward reliability moved below the answer layer",
                "links": "FailSAE - visual dominance - Think-Verify-Revise - ROBORMBENCH - MCPO",
                "facts": "The papers probe sparse concepts, deferral, dynamic logic verification, paraphrase-stable rewards, and cross-modal reasoning compression.",
                "inference": "The actionable variable is no longer only correctness; it is which latent, wording, view, or reasoning step controlled the decision.",
            },
        ],
        "frontier_memory": [
            {
                "label": "Strengthening",
                "history": "Late August and early September repeatedly framed robot intelligence as evidence budgeting before action authority.",
                "body": "September 7 strengthens that line by naming failure time, recovery state, visual grounding phase, tactile correction timing, and paraphrase-stable rewards.",
            },
            {
                "label": "New signal",
                "history": "Recent geometry notes emphasized robot-usable validity and drift-aware maps.",
                "body": "Today adds NavArena and open-set 3D scene graphs: 3D representations are becoming benchmark substrates that define goals, collisions, and semantic actions.",
            },
            {
                "label": "Commoditizing",
                "history": "Many world-model and generation papers now claim physical or controllable futures.",
                "body": "The differentiator is no longer saying world model; it is whether planning, stress generation, contact correction, or remote control has a falsifiable release gate.",
            },
            {
                "label": "Contradiction",
                "history": "Scaling VLA datasets and compact policy claims can make success rates look saturated.",
                "body": "RoboSPA, LIBERO-Recover, FailureSpot, and ROBORMBENCH argue that saturation disappears when spatial complexity, recovery, failure timing, and language invariance are tested.",
            },
            {
                "label": "Missing axis",
                "history": "Current corpora still split geometry, VLA failure, privacy, and efficient evidence into separate benchmarks.",
                "body": "APRL can own a closed-loop benchmark where geometry validity, sensor evidence, language invariance, tactile correction, and recovery outcome are evaluated in the same episode.",
            },
        ],
        "strategy": [
            {
                "priority": "Build moat",
                "portfolio": "Build moat",
                "title": "Timed failure and recovery benchmark",
                "opportunity": "Timed failure and recovery benchmark",
                "thesis": "Build robot episodes where failure onset, grounding error, recovery level, tactile correction, and reward-language invariance are labeled together.",
                "scores": {"strategic_fit": 5, "asymmetry": 5, "timing": 5, "tractability": 4, "defensibility": 5, "scientific_depth": 5},
                "one_week": "Instrument ten LIBERO/RoboCasa-style episodes with induced distractors, failed grasps, action pauses, and task-preserving paraphrases.",
                "one_week_probe": "Instrument ten LIBERO/RoboCasa-style episodes with induced distractors, failed grasps, action pauses, and task-preserving paraphrases.",
                "four_week": "Compare FailureSpot-style detectors, VLM judges, trajectory-grounded reward models, and recovery policies on the same timestamped episodes.",
                "four_week_build": "Compare FailureSpot-style detectors, VLM judges, trajectory-grounded reward models, and recovery policies on the same timestamped episodes.",
                "success": "A detector or reward gate predicts the needed recovery action at least one action chunk before terminal failure on three failure families.",
                "success_metric": "A detector or reward gate predicts the needed recovery action at least one action chunk before terminal failure on three failure families.",
                "stop": "Stop if timestamp labels do not improve recovery action choice beyond trajectory-level confidence and terminal success labels.",
                "stop_condition": "Stop if timestamp labels do not improve recovery action choice beyond trajectory-level confidence and terminal success labels.",
                "paper_path": "Failure-timed action admission and recovery evaluation for VLA manipulation.",
                "asset_path": "Timestamped manipulation episodes with distractors, recovery levels, tactile corrections, paraphrase sets, and action-change labels.",
                "asset": "Timestamped manipulation episodes with distractors, recovery levels, tactile corrections, paraphrase sets, and action-change labels.",
            },
            {
                "priority": "Exploit",
                "portfolio": "Exploit",
                "title": "Robot-usable 3DGS navigation arena",
                "opportunity": "Robot-usable 3DGS navigation arena",
                "thesis": "Turn local 3DGS and SfM reconstructions into goal, collision, observability, and localization tests for APRL navigation and field-robot work.",
                "scores": {"strategic_fit": 5, "asymmetry": 4, "timing": 5, "tractability": 4, "defensibility": 5, "scientific_depth": 4},
                "one_week": "Convert one lab corridor and one cluttered tabletop or outdoor route into 3DGS, occupancy, semantic-goal, and odometry-degeneracy probes.",
                "one_week_probe": "Convert one lab corridor and one cluttered tabletop or outdoor route into 3DGS, occupancy, semantic-goal, and odometry-degeneracy probes.",
                "four_week": "Benchmark NavArena-style goal generation, BLASt3R/HiSfM reconstruction, open-set scene graphs, CrossDepth, and radar-enhanced odometry against robot rollouts.",
                "four_week_build": "Benchmark NavArena-style goal generation, BLASt3R/HiSfM reconstruction, open-set scene graphs, CrossDepth, and radar-enhanced odometry against robot rollouts.",
                "success": "A geometry validity score predicts collision, relocalization, or semantic-goal failure better than view-synthesis or pose error alone.",
                "success_metric": "A geometry validity score predicts collision, relocalization, or semantic-goal failure better than view-synthesis or pose error alone.",
                "stop": "Stop if closed-loop failures are fully explained by conventional pose error and no representation-specific validity variable matters.",
                "stop_condition": "Stop if closed-loop failures are fully explained by conventional pose error and no representation-specific validity variable matters.",
                "paper_path": "Robot-usable validity of 3DGS, SfM, and multimodal odometry for navigation benchmarks.",
                "asset_path": "3DGS scenes, occupancy maps, semantic goals, odometry observability labels, and closed-loop navigation outcomes.",
                "asset": "3DGS scenes, occupancy maps, semantic goals, odometry observability labels, and closed-loop navigation outcomes.",
            },
            {
                "priority": "Explore",
                "portfolio": "Explore",
                "title": "Physical world-model stress loop",
                "opportunity": "Physical world-model stress loop",
                "thesis": "Use the same learned prior as a planner, a scenario generator, and a contact-time corrector, then reject it when physical obligations fail.",
                "scores": {"strategic_fit": 4, "asymmetry": 5, "timing": 5, "tractability": 3, "defensibility": 4, "scientific_depth": 5},
                "one_week": "Create two manipulation and two driving toy tasks with fixed physical obligations, perturbable trajectories, and a verifier for state consistency.",
                "one_week_probe": "Create two manipulation and two driving toy tasks with fixed physical obligations, perturbable trajectories, and a verifier for state consistency.",
                "four_week": "Compare TourPhysics-style state commitment, diffusion scenario guidance, TacPAC-style contact correction, and wireless-world-model remote control under shift.",
                "four_week_build": "Compare TourPhysics-style state commitment, diffusion scenario guidance, TacPAC-style contact correction, and wireless-world-model remote control under shift.",
                "success": "The stress loop exposes at least two planner failures that nominal benchmarks miss and improves recovery or safety margin after gating.",
                "success_metric": "The stress loop exposes at least two planner failures that nominal benchmarks miss and improves recovery or safety margin after gating.",
                "stop": "Stop if generated stresses do not transfer to real or independently simulated failures, or if verifier errors do not predict action risk.",
                "stop_condition": "Stop if generated stresses do not transfer to real or independently simulated failures, or if verifier errors do not predict action risk.",
                "paper_path": "World-model priors as coupled planners, stress generators, and physical release gates.",
                "asset_path": "Scenario seeds, physical-obligation labels, generated long-tail interactions, contact corrections, and remote-control recovery logs.",
                "asset": "Scenario seeds, physical-obligation labels, generated long-tail interactions, contact corrections, and remote-control recovery logs.",
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
