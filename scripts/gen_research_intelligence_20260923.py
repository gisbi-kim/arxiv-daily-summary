#!/usr/bin/env python3
"""Generate the 2026-09-23 Research Intelligence edition."""

from __future__ import annotations

import json
from pathlib import Path

from gen_research_intelligence_20260811 import build_html


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PROMPT = "prompts/instruction_v20260713.md"


RI_BY_DATE = {
    "2026-09-23": {
        "date": "2026-09-23",
        "edition": "Research Intelligence",
        "source_prompt": SOURCE_PROMPT,
        "source_mode": "new",
        "scope_note": (
            "Daily edition from matching Wednesday /new listings: 211 non-replacement cs.CV rows, "
            "151 cs.RO rows, 240 deduplicated papers, and 202 ROI papers. Tier A cards are "
            "conservative abstract-only autopsies from repository parser output; no figure, table, "
            "full-text, code, or dataset-release claim is asserted unless the abstract itself states it."
        ),
        "executive_thesis": (
            "The September 23 batch says robot intelligence is being tested less by average task score "
            "and more by whether the interface variable that authorizes action is the right one. "
            "IndustrialVLA-Bench, VLAQuantBench, action-tokenization work, RoboTwin-Phys, RoboFollow, "
            "and NavSafe-infinity all expose cases where clean success, reconstruction error, open-loop "
            "score, or low-entropy scenes hide deployment failure. Geometry papers including Dual "
            "Covariance 3DGS-SLAM, ArborSplat, PARTE, CODA, phi-RIE, and map-prior HD mapping push "
            "3D evidence toward registration, semantics, interaction, and online map use. PatchWAM, "
            "ForeDrive, DreamStream, GameDirector, CoDeR, and Fysiverse then make the same point for "
            "world models: a predicted future is useful only when it changes planning, simulation, or "
            "policy evaluation in a traceable way."
        ),
        "decision_cards": [
            {
                "label": "Decision",
                "title": "Robot-policy evaluation is moving from score comparison to evidence traceability",
                "body": (
                    "IndustrialVLA-Bench, VLAQuantBench, action-tokenization evaluation, RoboTwin-Phys, "
                    "and RoboFollow separate clean task success from robustness, language use, precision "
                    "assignment, physical-condition sensitivity, and closed-loop control."
                ),
            },
            {
                "label": "Decision",
                "title": "Geometry is becoming an action substrate",
                "body": (
                    "Dual Covariance 3DGS-SLAM, ArborSplat, CODA, PARTE, GRIP, and phi-RIE ask whether "
                    "a 3D representation supports tracking, semantic structures, scene completion, "
                    "registration, or physical interaction rather than photorealism alone."
                ),
            },
            {
                "label": "Decision",
                "title": "World models must prove their action interface",
                "body": (
                    "PatchWAM, ForeDrive, DreamStream, GameDirector, CoDeR, Fysiverse-3D, and Skytopia "
                    "all tie generated or latent futures to action patches, planning guidance, "
                    "policy-oriented simulation, executable code worlds, or navigation control."
                ),
            },
        ],
        "papers": [
            {
                "rank": 1,
                "title": "IndustrialVLA-Bench: A Traceable Multi-Axis Evaluation of Open Robot Policy Models",
                "arxiv_id": "2609.25562",
                "fit": "VLA/WAM evaluation - evidence tiers - robustness and deployment cost",
                "status": "Tier A - abstract-only",
                "status_quo": "Released VLA and WAM systems are often compared across incompatible protocols and single aggregate task scores.",
                "friction": "Clean LIBERO averages can be close while robustness, paraphrase sensitivity, latency, memory, and evidence status differ sharply.",
                "hidden_premise": "Robot-policy comparisons should be valid only when checkpoint, inference configuration, random seeds, and evidence tier are traceable.",
                "conceptual_move": "Evaluate released VLA and WAM systems under one reporting schema with separate clean capability, non-language robustness, instruction sensitivity, and execution-cost axes.",
                "mechanism": "The abstract reports six released systems, three complete seed evaluations, protocol-faithful tiers, and explicit latency, memory, runtime mode, and evidence status.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "Clean LIBERO averages differ by only 1.58 points while robustness and paraphrase summaries span 14.62 and 31.08 points."},
                    {"trace": "[Abstract]", "claim": "Strict comparisons are restricted to protocol-faithful systems, with weaker evidence tiers kept visible."},
                    {"trace": "[Inference]", "claim": "APRL should publish robot-policy leaderboards with protocol tier, cost, robustness, and instruction-sensitivity gates before ranking models."},
                ],
                "falsification": "If protocol-faithful systems keep the same ranking across clean, robustness, paraphrase, and deployment-cost axes, the multi-axis split is less decision-changing.",
                "adversarial": "The benchmark still depends on the chosen task families; contact-rich or navigation tasks may expose different VLA/WAM trade-offs.",
                "thinking_tool": "Do not compare released robot policies until the evidence tier and deployment cost are first-class columns.",
                "transfer_boundary": "Strong for released manipulation policies; needs new axes for mobile robots, surgical robots, and field navigation.",
            },
            {
                "rank": 2,
                "title": "VLAQuantBench: Closed-Loop Evaluation of Post-Training Quantization for Vision-Language-Action Models",
                "arxiv_id": "2609.25376",
                "fit": "VLA quantization - precision assignment - closed-loop robustness",
                "status": "Tier A - abstract-only",
                "status_quo": "Post-training quantization is often judged by memory savings and static numerical error.",
                "friction": "Small precision choices can make a VLA fail in closed loop even when offline replay or universal sensitivity heuristics look acceptable.",
                "hidden_premise": "Quantization policy is part of the controller, so layer scope, format, calibration, and protected projections must be evaluated through rollout success.",
                "conceptual_move": "Treat VLA quantization as a controlled closed-loop benchmark with recipe-dependent precision assignments instead of universal layer-sensitivity rules.",
                "mechanism": "The abstract reports 409 runs and 94,574 simulation episodes across four models, LIBERO, and additional simulation benchmark families.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "Under uncalibrated W4A4 round-to-nearest quantization, expanding a pi0.5 action-head subset from 126 to 167 layers raises success from 7.0% to 70.5%."},
                    {"trace": "[Abstract]", "claim": "For OpenVLA-OFT, protecting one 28,672-parameter output projection restores near-baseline success."},
                    {"trace": "[Inference]", "claim": "APRL should gate compressed robot policies by rollout families and action-head/projection protection, not only model-size savings."},
                ],
                "falsification": "If physical robot runs do not mirror simulation-sensitive precision assignments, the benchmark needs hardware-specific kernels and calibration axes.",
                "adversarial": "A recipe that rescues one policy can damage another; the abstraction should force model-specific assignment rather than a single compression rule.",
                "thinking_tool": "Compression is acceptable only after naming which action-critical projection or layer scope is protected.",
                "transfer_boundary": "Direct for VLA deployment; less direct for modular policies where quantized perception is separated from control.",
            },
            {
                "rank": 3,
                "title": "Beyond Reconstruction Error: Analytical and Data-Driven Action Tokenization for Autoregressive Vision-Language-Action Models",
                "arxiv_id": "2609.25820",
                "fit": "action tokenization - closed-loop criterion - decoder stability",
                "status": "Tier A - abstract-only",
                "status_quo": "Discrete action representations are commonly selected by reconstruction fidelity or rate-distortion alone.",
                "friction": "A tokenization that reconstructs actions well can be harder for a sequence model to predict and can reduce closed-loop control success.",
                "hidden_premise": "Action tokens should be judged by geometric fidelity, sequence predictability, decoder stability, and rollout behavior together.",
                "conceptual_move": "Compare analytical, linear data-driven, and nonlinear tokenizations under one interface and test how rankings change across diagnostics and LIBERO rollouts.",
                "mechanism": "The abstract contrasts PCA, Temporal-DCT, and autoencoder-style representations over rate-distortion, sequence modeling, token perturbation, and 3,500 rollouts.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "PCA has lower nominal reconstruction error than Temporal-DCT but lower mean seen-task success across three policy-training seeds."},
                    {"trace": "[Abstract]", "claim": "An autoencoder reduces reconstruction error further yet does not yield the strongest policy and is more sensitive to discrete token perturbations."},
                    {"trace": "[Inference]", "claim": "APRL should choose robot action tokens using rollout and perturbation diagnostics, not reconstruction error alone."},
                ],
                "falsification": "If token ranking becomes stable under larger model capacity and more data, the reported reversals may reflect underfitting rather than token semantics.",
                "adversarial": "Seed-level reversals imply evaluation must report uncertainty; otherwise a tokenization can look superior by chance.",
                "thinking_tool": "Treat action representation as a controllability contract, not a compression artifact.",
                "transfer_boundary": "Strong for autoregressive VLA control; needs adaptation for continuous diffusion policies.",
            },
            {
                "rank": 4,
                "title": "RoboTwin-Phys: Do WAMs and VLAs Understand the Physical World?",
                "arxiv_id": "2609.26292",
                "fit": "physical-condition diversity - WAM/VLA robustness - manipulation benchmark",
                "status": "Tier A - abstract-only",
                "status_quo": "Manipulation benchmarks vary appearance, layout, and visual observations while often keeping physical parameters fixed.",
                "friction": "Policies that survive visual randomization can degrade when mass, friction, or joint dynamics change.",
                "hidden_premise": "A robot policy has not learned a physical task unless it remains stable across plausible physical-condition changes.",
                "conceptual_move": "Make physical-condition diversity an explicit benchmark dimension with continuous variation of 13 physical attributes.",
                "mechanism": "The abstract releases more than 5,000 expert demonstrations with ground-truth physical parameters and evaluates representative WAMs and VLAs under those changes.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The benchmark varies mass, friction, joint dynamics, and other physical attributes within physically plausible ranges."},
                    {"trace": "[Abstract]", "claim": "Representative WAMs and VLAs can degrade markedly under physical-condition changes despite visual/layout randomization."},
                    {"trace": "[Inference]", "claim": "APRL should add physical-parameter sweeps to manipulation evaluation before claiming real-world robustness."},
                ],
                "falsification": "If physical-parameter estimates are unavailable or unidentifiable from robot observations, policy conditioning may not transfer beyond simulation.",
                "adversarial": "Mass and friction sweeps should be combined with sensor noise and contact geometry shifts; isolated physics axes can understate coupled failures.",
                "thinking_tool": "Ask whether a policy understands the physical variable that changes the outcome, not just the pixels.",
                "transfer_boundary": "Strong for simulation-to-real manipulation; weaker for tasks dominated by semantic planning rather than contact physics.",
            },
            {
                "rank": 5,
                "title": "Dual Covariance Gaussian Splatting SLAM: Decoupling Rendering and Registration for Robust Real-Time Tracking",
                "arxiv_id": "2609.25746",
                "fit": "3DGS SLAM - rendering versus tracking covariance - real-time registration",
                "status": "Tier A - abstract-only",
                "status_quo": "3DGS SLAM often uses one Gaussian covariance for both rendering quality and frame-to-map registration.",
                "friction": "Photometric optimization flattens covariances against surfaces, while robust registration needs uncertainty that reflects sensor geometry.",
                "hidden_premise": "A map primitive can serve rendering and tracking only if the two uncertainty contracts are separated.",
                "conceptual_move": "Keep one Gaussian mean but maintain separate rendering and tracking covariances, with tracking covariance derived from an RGB-D sensor noise model.",
                "mechanism": "The abstract also uses tracking covariances as Gaussian anchors for image corners to add constraints where depth geometry is weak.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper identifies conflicting demands between rendering covariance and registration covariance."},
                    {"trace": "[Abstract]", "claim": "It reports robust tracking across TUM RGB-D, ScanNet, Replica, and two RealSense D435i outdoor sequences at about 60 FPS."},
                    {"trace": "[Inference]", "claim": "APRL should evaluate 3DGS maps by whether their uncertainty supports tracking decisions, not only rendering quality."},
                ],
                "falsification": "If separate covariances do not improve downstream navigation or loop-closure recovery, the gain may remain a tracking-level improvement.",
                "adversarial": "Dynamic scenes, rolling shutter, and reflective surfaces can break the assumed sensor-noise covariance contract.",
                "thinking_tool": "Split visual fidelity and pose-estimation uncertainty into separate map responsibilities.",
                "transfer_boundary": "Direct for RGB-D 3DGS SLAM; needs separate treatment for LiDAR-only and monocular pipelines.",
            },
            {
                "rank": 6,
                "title": "ArborSplat: Online Semantic Gaussian Splatting SLAM for Orchards",
                "arxiv_id": "2609.26315",
                "fit": "semantic 3DGS SLAM - orchard structures - online map semantics",
                "status": "Tier A - abstract-only",
                "status_quo": "Appearance-driven 3DGS SLAM can preserve photometric detail while losing thin, task-critical structures.",
                "friction": "Orchard robots need trunks, trellises, and fruit in the map, but image-to-3D semantic transfer is unreliable for thin structures.",
                "hidden_premise": "Semantic capacity should be allocated according to robot-relevant structure, not only image reconstruction error.",
                "conceptual_move": "Optimize semantics directly on the Gaussian map using LiDAR odometry, class-specific height bands, ground-plane constraints, and online multi-view evidence fusion.",
                "mechanism": "The abstract rejects labels inconsistent with local ground surface or monocular depth and reserves Gaussian capacity for underrepresented structures.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The method targets apple and pear orchards across dormancy, flowering, and harvesting."},
                    {"trace": "[Abstract]", "claim": "It keeps ATE below 0.5 m on all 12 traversals and improves mIoU while running faster than compared semantic GS-SLAM systems."},
                    {"trace": "[Inference]", "claim": "APRL should score map semantics on structures that change robot behavior, especially thin or underrepresented classes."},
                ],
                "falsification": "If class-specific height bands do not transfer to other crop geometries or indoor clutter, the semantic prior may be domain-bound.",
                "adversarial": "A ground-plane prior can reject valid labels on sloped or occluded terrain; stress routes should include uneven rows and seasonal clutter.",
                "thinking_tool": "Preserve map capacity for action-relevant semantic structures, not just photometric fit.",
                "transfer_boundary": "Strong for agricultural and structured outdoor robots; less direct for unstructured indoor SLAM.",
            },
            {
                "rank": 7,
                "title": "An Action Is Worth One Patch: Unified World-Action Modeling with PatchWAM",
                "arxiv_id": "2609.25961",
                "fit": "world-action modeling - action-as-patch interface - shared generative backbone",
                "status": "Tier A - abstract-only",
                "status_quo": "World models usually add dedicated action heads or separate action experts to connect visual representations to control.",
                "friction": "Separate heads can hide whether the visual generative backbone itself contains the action-relevant dynamics.",
                "hidden_premise": "A continuous action can be written into a representation compatible with image patches and predicted by the same backbone.",
                "conceptual_move": "Treat continuous actions as another patch type through Action-as-Patch so one model predicts both robot motion and future scene state.",
                "mechanism": "The abstract says visual prediction and action generation become one generative process without a dedicated action head or separate expert.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "PatchWAM reports gains over a matched dual-expert control in subsampled training windows."},
                    {"trace": "[Abstract]", "claim": "Full-data evaluations report 91.8% success on LIBERO-Plus and 96.12% on RoboTwin 2.0 with augmented demonstrations."},
                    {"trace": "[Inference]", "claim": "APRL should test whether action-as-patch changes failure recovery and contact behavior, not only benchmark success."},
                ],
                "falsification": "If action-as-patch works only after heavy demonstration augmentation, the inherited capacity claim weakens under low-data deployment.",
                "adversarial": "Patch representation may obscure continuous control constraints; perturb action patches and evaluate physical feasibility.",
                "thinking_tool": "When adding a new robot signal, first ask whether the interface can inherit an existing generative backbone.",
                "transfer_boundary": "Strong for patch-tokenized visual policies; less direct for low-level torque controllers.",
            },
            {
                "rank": 8,
                "title": "ForeDrive: Foresight-Guided End-to-End Autonomous Driving with a Planning-Relevant Latent World Model",
                "arxiv_id": "2609.26299",
                "fit": "driving world model - planning-relevant latent - multi-horizon guidance",
                "status": "Tier A - abstract-only",
                "status_quo": "Latent world models are often optimized for future predictability and used as pretraining or auxiliary supervision.",
                "friction": "A predictable future representation may not be useful for trajectory generation, especially when horizon reliability varies.",
                "hidden_premise": "Future latents should guide planning without overriding the current observation when predicted futures are unreliable.",
                "conceptual_move": "Couple a JEPA-style multi-horizon latent future representation asymmetrically to a Diffusion Transformer planner.",
                "mechanism": "The abstract uses gated visual fusion, future-status injection, and Trajectory-Adaptive Bias to inject future latents as guidance.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "Planning gradients update the shared online encoder while stop-gradient routing trains the latent predictor with forecasting losses only."},
                    {"trace": "[Abstract]", "claim": "ForeDrive reports 89.9 PDMS on NAVSIM v1 and 90.0 one-stage EPDMS on NAVSIM v2 using only the current front-view image at inference."},
                    {"trace": "[Inference]", "claim": "APRL should evaluate whether predicted future latents change action ranking under uncertainty, not only future reconstruction."},
                ],
                "falsification": "If gated future latents do not improve closed-loop safety or recovery, the planning relevance may be open-loop benchmark-specific.",
                "adversarial": "Future-status gates can hide overconfidence; stress with occlusion, interaction-heavy scenes, and rare actor behavior.",
                "thinking_tool": "A world model should expose the reliability of each future horizon before the planner consumes it.",
                "transfer_boundary": "Strong for driving/planning; needs translation for manipulation where future visual tokens depend on contact state.",
            },
            {
                "rank": 9,
                "title": "NavSafe-infinity: Benchmarking Closed-Loop Driving Safety in Photorealistic Environments",
                "arxiv_id": "2609.26618",
                "fit": "closed-loop driving safety - traffic taxonomy - open-loop blind spot",
                "status": "Tier A - abstract-only",
                "status_quo": "End-to-end driving policies are commonly advanced on open-loop benchmarks.",
                "friction": "Open-loop gains can fail to predict compounding errors, recovery behavior, or safety interaction with other actors.",
                "hidden_premise": "Safety should be measured by scenario-level success and failure criteria under closed-loop feedback, not by imitation quality alone.",
                "conceptual_move": "Create a photorealistic closed-loop benchmark with 280 scenarios across 28 event types and category-level traffic-safety scores.",
                "mechanism": "The abstract defines failures through a structured taxonomy covering crashes, vulnerable road users, violations, and incidents.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "Evaluation of 20 E2E policies finds that open-loop gains do not reliably transfer to closed-loop safety."},
                    {"trace": "[Abstract]", "claim": "Open-loop RL fine-tuning can reward hack by trading safety margin for ego progress, which closed-loop feedback amplifies."},
                    {"trace": "[Inference]", "claim": "APRL should require closed-loop event taxonomies before accepting open-loop driving or navigation policy gains."},
                ],
                "falsification": "If closed-loop event categories do not predict real road or robot-route incidents, the taxonomy needs field calibration.",
                "adversarial": "Photorealistic simulation can still miss social or sensor failures; include domain randomization and real replay where possible.",
                "thinking_tool": "Open-loop improvement is not safety evidence until closed-loop recovery and actor interaction are tested.",
                "transfer_boundary": "Direct for autonomous driving; useful as a template for mobile-robot navigation safety suites.",
            },
            {
                "rank": 10,
                "title": "RoboFollow: Unveiling the Instruction Following Mirage in Embodied Agents",
                "arxiv_id": "2609.25636",
                "fit": "instruction following - low scene entropy - VLA/WAM diagnosis",
                "status": "Tier A - abstract-only",
                "status_quo": "Embodied agents can achieve high success when the scene visually implies the task, making language appear less necessary.",
                "friction": "A policy can score highly while barely using the instruction if the scene supports only one valid branch.",
                "hidden_premise": "Instruction-following benchmarks need high scene entropy and controlled perturbations that isolate comprehension from motor execution.",
                "conceptual_move": "Design a diagnostic benchmark with high scene entropy, a four-level perturbation protocol, and confound-controlled Intent and Execution scores.",
                "mechanism": "The abstract evaluates nine VLA and WAM policies and tests mitigations such as stronger VLM backbones, QA co-training, LangForce, and classifier-free guidance.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "Strong L0 performance does not reliably transfer to L1-L3 under the reported fine-tuning setup."},
                    {"trace": "[Abstract]", "claim": "Representative mitigations fail to close the instruction-following gap."},
                    {"trace": "[Inference]", "claim": "APRL should add high-entropy paired instructions before claiming language-conditioned manipulation or navigation."},
                ],
                "falsification": "If models trained with richer high-entropy data close L1-L3 without architectural changes, the failure is data coverage rather than instruction interface.",
                "adversarial": "The protocol restricts actions to the trained repertoire; open-world commands may reveal additional planning failures.",
                "thinking_tool": "Separate whether the robot followed language from whether the scene already made the action obvious.",
                "transfer_boundary": "Strong for VLA/WAM instruction benchmarks; needs task-specific entropy design for field robots.",
            },
        ],
        "synthesis": [
            {
                "title": "Evaluation axes are becoming more diagnostic than model families",
                "links": "IndustrialVLA-Bench - VLAQuantBench - action tokenization - RoboTwin-Phys - RoboFollow",
                "facts": "The batch separates clean score, robustness, paraphrase sensitivity, quantization assignment, token predictability, physical parameters, and instruction entropy.",
                "inference": "APRL should design benchmark tables around the failure variable being tested before grouping papers as VLA, WAM, or policy learning.",
            },
            {
                "title": "3D maps are judged by the operation they enable",
                "links": "Dual Covariance 3DGS-SLAM - ArborSplat - phi-RIE - CODA - PARTE - GRIP",
                "facts": "The geometry papers connect representations to tracking uncertainty, semantic thin structures, movable assets, scene completion, robust registration, and 2D-3D matching.",
                "inference": "Robot-usable geometry should report which downstream move, grasp, relocalization, or simulation edit changes because of the map.",
            },
            {
                "title": "World-model evidence must be consumed through an explicit action channel",
                "links": "PatchWAM - ForeDrive - DreamStream - GameDirector - CoDeR - Skytopia",
                "facts": "Action patches, planning-relevant latent futures, policy-oriented simulation, code worlds, and action-conditioned drone models all expose the channel between predicted future and command.",
                "inference": "Generated futures should be blocked from policy learning unless a reliability gate and action-consumption rule are visible.",
            },
        ],
        "frontier_memory": [
            {
                "label": "Strengthening",
                "history": "September 22 emphasized evidence contracts for VLA validation, contact authority, geometry uncertainty, and closed-loop safety.",
                "body": "September 23 strengthens the same axis but shifts it toward evaluation infrastructure: quantization, action tokens, physical parameters, instruction entropy, and closed-loop safety taxonomies.",
            },
            {
                "label": "New signal",
                "history": "Recent RI editions often treated 3DGS as a map or SLAM substrate.",
                "body": "Today adds interactive-environment conversion and semantic orchard mapping, making object-level editability and action-relevant semantic capacity part of the map contract.",
            },
            {
                "label": "Missing axis",
                "history": "The last four weeks have many VLA/WAM and driving benchmarks but fewer shared physical-contact datasets with measured force or material parameters.",
                "body": "RoboTwin-Phys and the force/tactile papers suggest APRL can own the gap between physics-diverse simulation and real contact instrumentation.",
            },
        ],
        "strategy": [
            {
                "priority": "Build moat",
                "title": "Evidence-tiered VLA/WAM evaluation ledger",
                "thesis": "Rank robot policies only after separating clean score, language entropy, physical parameters, quantization recipe, action-token stability, latency, memory, and evidence tier.",
                "scores": {"fit": 5, "novelty": 4, "feasibility": 5, "moat": 5, "timing": 5, "evidence": 5},
                "one_week": "Re-run two local VLA/WAM baselines on a small suite with paraphrase pairs, high-entropy scenes, physical-parameter sweeps, and latency/memory capture.",
                "four_week": "Build a public-style table that reports protocol tier, quantization setting, action-token diagnostics, physical robustness, instruction sensitivity, and rollout score.",
                "success": "At least one model ranking changes between clean success and the evidence-tiered evaluation.",
                "stop": "All diagnostic axes produce the same ranking and no actionable failure family is isolated.",
                "asset": "Protocol manifests, seed logs, quantization recipes, physical-condition labels, paraphrase sets, and latency/memory traces.",
            },
            {
                "priority": "Build moat",
                "title": "Robot-usable Gaussian map contract",
                "thesis": "Compare Gaussian maps by tracking uncertainty, semantic thin-structure preservation, object-level editability, and downstream navigation/manipulation success.",
                "scores": {"fit": 5, "novelty": 5, "feasibility": 4, "moat": 5, "timing": 5, "evidence": 5},
                "one_week": "Use one RGB-D route and one manipulation scene to compare single-covariance GS-SLAM, dual-covariance tracking, semantic map labels, and movable-object conversion.",
                "four_week": "Create repeated routes and object-edit scenes where map uncertainty, semantic capacity, and interactive assets are scored against relocalization, grasp planning, and collision checks.",
                "success": "A map that looks similar photometrically produces measurably different tracking, semantic recall, or task success under the contract.",
                "stop": "Task-level metrics are insensitive to covariance split, semantic capacity, or interactive conversion.",
                "asset": "RGB-D/LiDAR routes, Gaussian map states, semantic labels, object-edit masks, relocalization trials, and task-success logs.",
            },
            {
                "priority": "Explore",
                "title": "Action-interface audit for world models",
                "thesis": "Test whether a predicted future enters control through an action patch, planning-relevant latent, simulation replay, or safety gate that can be ablated.",
                "scores": {"fit": 5, "novelty": 4, "feasibility": 4, "moat": 4, "timing": 5, "evidence": 4},
                "one_week": "Instrument one manipulation and one navigation task with action-as-patch, latent-future guidance, and no-world-model baselines.",
                "four_week": "Add horizon reliability gates, action-encoding perturbations, and policy-oriented simulation rollouts across contact and driving-style tasks.",
                "success": "World-model signals improve one recovery or planning metric only when their action-consumption gate is active.",
                "stop": "Future predictions improve visual metrics but do not change action ranking, recovery, or safety margin.",
                "asset": "Action-interface ablations, latent reliability scores, generated rollout traces, policy decisions, and stop-condition labels.",
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
