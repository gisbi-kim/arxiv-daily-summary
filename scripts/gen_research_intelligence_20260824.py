#!/usr/bin/env python3
"""Generate the 2026-08-24 Research Intelligence edition."""

from __future__ import annotations

import json
from pathlib import Path

from gen_research_intelligence_20260811 import build_html


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PROMPT = "prompts/instruction_v20260713.md"


RI_BY_DATE = {
    "2026-08-24": {
        "date": "2026-08-24",
        "edition": "Research Intelligence",
        "source_prompt": SOURCE_PROMPT,
        "source_mode": "new",
        "scope_note": (
            "Daily edition from matching Monday /new listings: 103 non-replacement cs.CV rows, "
            "37 cs.RO rows, 133 deduplicated papers, and 110 ROI papers. Tier A cards are "
            "conservative abstract-only autopsies from the repository parser output; no figure, "
            "table, full-text, code, or dataset-release claims are asserted."
        ),
        "executive_thesis": (
            "The August 24 batch turns robot intelligence into an authorization problem. VLA and "
            "robot-learning papers ask which temporal-logic rule, physical-attack certificate, "
            "future-token forecast, action-compression tolerance, tactile state, or task-precedence "
            "graph is allowed to change the next action. Geometry, VLM, and driving papers ask the "
            "same question for map updates, spatial-state reconstruction, video evidence routing, "
            "cooperative perception, and world-action rollouts. The useful APRL move is to build "
            "benchmarks where the hidden evidence variable must be named before the policy, planner, "
            "map, or compressed perception stack is trusted."
        ),
        "decision_cards": [
            {
                "label": "Decision",
                "title": "Action authority is being constrained before execution",
                "body": (
                    "CertVLA, Logic-VLA, ForeTime-VLA, JND compression for VLA, and CARD all make "
                    "the action interface visible: which attack mask, logic formula, future token, "
                    "token perturbation, or belief route changed the chosen action."
                ),
            },
            {
                "label": "Decision",
                "title": "Manipulation evidence is moving into hardware and contact state",
                "body": (
                    "VT-MUSE, Koala Gripper, ViTacPhys, hybrid roller-jamming, TaPeR, and "
                    "demonstration-unlearning audits ask whether contact, physical property, "
                    "gripper design, or task graph evidence survives into closed-loop behavior."
                ),
            },
            {
                "label": "Decision",
                "title": "Geometry and VLMs are evaluated by auditable state variables",
                "body": (
                    "TopoSurfel, VisTa3D, M2Depth, Stream3Dv2, IMU-free state estimation, "
                    "StateSight, EviRank, and spatial-verification agents all expose intermediate "
                    "state rather than accepting final visual quality or final answer accuracy."
                ),
            },
        ],
        "papers": [
            {
                "rank": 1,
                "title": "CertVLA: Certified Defense against Physical Visual Attacks for Vision-Language-Action Models",
                "arxiv_id": "2608.20791",
                "fit": "VLA safety - physical patch defense - closed-loop action certificate",
                "status": "Tier A - abstract-only",
                "status_quo": "Certified visual defenses usually certify discrete labels, while VLA policies output continuous temporally correlated actions.",
                "friction": "The abstract states that localized physical perturbations can attack VLA policies and that existing patch defenses do not directly certify closed-loop control.",
                "hidden_premise": "A safety claim for VLA deployment must certify behavior over a rollout, not only one visual query or one class label.",
                "conceptual_move": "Convert patch robustness into an action-consistency certificate with calibrated episode-level coverage.",
                "mechanism": "The abstract describes behaviorally consistent action regions, deterministic covering masks, and query-level decisions conjoined over a closed-loop rollout.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper identifies localized physical perturbations as a VLA vulnerability."},
                    {"trace": "[Abstract]", "claim": "It proposes calibrated behaviorally consistent actions and rollout-level certificates."},
                    {"trace": "[Inference]", "claim": "APRL should evaluate whether safety defenses preserve the action trajectory, not only visual classification."},
                ],
                "falsification": "If certified action coverage holds only for masks that do not affect contact-relevant pixels or if rollout success still fails under allowed patches, the certificate is too weak.",
                "adversarial": "Test adaptive patches on grippers, target objects, signs, and background regions while separating perception error from action deviation.",
                "thinking_tool": "Turn safety into an action-authority certificate with an explicit threat model and rollout boundary.",
                "transfer_boundary": "Strong for camera-conditioned VLA control; less direct for proprioception-only or map-based controllers.",
            },
            {
                "rank": 2,
                "title": "Logic-VLA: A Temporal Logic Conditioned Vision-Language-Action Model",
                "arxiv_id": "2608.20556",
                "fit": "VLA - temporal logic conditioning - safety-critical requirements",
                "status": "Tier A - abstract-only",
                "status_quo": "Natural-language robot instructions can be underspecified when the task has temporal or safety-critical constraints.",
                "friction": "The abstract argues that natural language may not precisely specify spatiotemporal requirements on resulting behavior.",
                "hidden_premise": "A VLA policy should accept formal requirements at inference time without sacrificing the nominal language task.",
                "conceptual_move": "Condition VLA behavior on Signal Temporal Logic specifications and optimize satisfying versus violating rollouts.",
                "mechanism": "The abstract names an STL syntax-graph encoder, STL-conditioned supervised finetuning, and trajectory-level preference optimization.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper frames temporal logic as an inference-time conditioning signal for VLA behavior."},
                    {"trace": "[Abstract]", "claim": "It evaluates closed-loop quadcopter navigation across randomized photorealistic environments."},
                    {"trace": "[Inference]", "claim": "APRL should require temporal predicates to be visible in the policy evaluation contract."},
                ],
                "falsification": "If unseen STL formulas raise requirement satisfaction but damage ordinary task completion, the logic interface is not yet robust.",
                "adversarial": "Use conflicting natural-language and STL constraints, unseen formulas, and perceptual ambiguity that hides a predicate boundary.",
                "thinking_tool": "Separate what the task asks from what the trajectory is forbidden or required to do over time.",
                "transfer_boundary": "Strong for navigation and sequential manipulation; weaker for one-shot static perception tasks.",
            },
            {
                "rank": 3,
                "title": "ForeTime-VLA: Causal Future-Token Distillation from a World Action Model for Conveyor-Belt Manipulation",
                "arxiv_id": "2608.20735",
                "fit": "VLA manipulation - future-token distillation - contact anticipation",
                "status": "Tier A - abstract-only",
                "status_quo": "Many VLA finetunes condition on the current observation even when moving-object manipulation requires future contact anticipation.",
                "friction": "The abstract states that running a video-scale world-action teacher or imagining future frames at deployment is costly.",
                "hidden_premise": "Future information can be compressed into causal tokens that preserve action-relevant transition timing.",
                "conceptual_move": "Distill a future-aware action-equivalent representation from a world-action model into a causal VLA policy.",
                "mechanism": "The abstract describes four future tokens, a phase token, manipulation phase, time-to-transition, and action-expert conditioning.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper names anticipation of contact events as central for moving-object manipulation."},
                    {"trace": "[Abstract]", "claim": "It predicts a whitened future-aware target and normalized time-to-transition from an eight-frame history."},
                    {"trace": "[Inference]", "claim": "APRL should score future-token usefulness by earlier action correction before contact."},
                ],
                "falsification": "If future tokens improve training loss but do not shift pre-contact actions or recovery timing, they are not action-equivalent.",
                "adversarial": "Vary belt speed, occlusion, object slip, and phase boundary labels to isolate future anticipation from memorized timing.",
                "thinking_tool": "Ask which minimal future variable must be causal at inference for contact timing to improve.",
                "transfer_boundary": "Strong for conveyor, catching, and moving-object manipulation; weaker for static pick-place tasks.",
            },
            {
                "rank": 4,
                "title": "VT-MUSE: Multimodal Unified Sequential Visuotactile Representation Learning for Manipulation",
                "arxiv_id": "2608.21290",
                "fit": "visuotactile manipulation - sequential contact dynamics - cross-modal representation",
                "status": "Tier A - abstract-only",
                "status_quo": "Visuotactile pipelines often encode modalities independently and fuse only current-step observations.",
                "friction": "The abstract says independent encoding limits fine-grained cross-modal dependencies and overlooks temporal contact evolution.",
                "hidden_premise": "A manipulation representation should retain global visual context and local tactile dynamics across time.",
                "conceptual_move": "Learn sequential visuotactile latents through cross-modal temporal alignment and masked-view consistency.",
                "mechanism": "The abstract describes a two-stage framework with modality-specific encoders, a conditional variational latent model, visual reconstruction, and tactile-depth prediction.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper identifies current-step fusion as insufficient for temporal contact dynamics."},
                    {"trace": "[Abstract]", "claim": "It predicts tactile depth changes while reconstructing masked recent visual observations."},
                    {"trace": "[Inference]", "claim": "APRL should measure contact-dynamics prediction against recovery and grasp-stability changes."},
                ],
                "falsification": "If temporal visuotactile latents do not improve failure prediction under slip, deformation, or occlusion, the representation is not control-relevant.",
                "adversarial": "Use visually stable but tactile-changing objects and tactile-stable but visually occluded grasps to separate modality dependence.",
                "thinking_tool": "Treat contact as a temporal state variable, not an auxiliary sensor feature.",
                "transfer_boundary": "Strong for contact-rich manipulation; weaker for tasks without tactile sensing or contact state labels.",
            },
            {
                "rank": 5,
                "title": "VisTa3D: A Dataset and Benchmark for Thin Object Reconstruction from Vision, Tactile, and 3D Point Clouds",
                "arxiv_id": "2608.20740",
                "fit": "thin-object reconstruction - tactile geometry - benchmark",
                "status": "Tier A - abstract-only",
                "status_quo": "3D reconstruction benchmarks often reward dense visible surfaces and under-test thin, deformable, or contact-inferred geometry.",
                "friction": "The abstract says current reconstruction models underperform on thin objects because such objects occupy little image and point-cloud volume.",
                "hidden_premise": "Tactile response maps can add local shape and deformation evidence unavailable to vision or range alone.",
                "conceptual_move": "Make thin-object reconstruction a multimodal benchmark with synchronized RGB, depth, tactile, IMU, pose, calibration, and laser-scan ground truth.",
                "mechanism": "The abstract introduces VisTa3D, 387 scenes, 70 thin objects, 17 environments, and a visuospatial-tactile fusion baseline.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper names thin-object low fidelity as a measurable failure of current 3D reconstruction models."},
                    {"trace": "[Abstract]", "claim": "It collects synchronized visual, depth, tactile, inertial, pose, calibration, segmentation, and laser-scanned ground truth data."},
                    {"trace": "[Inference]", "claim": "APRL should test robot maps on objects whose useful geometry is contact-revealed, not only visually visible."},
                ],
                "falsification": "If tactile fusion improves reconstruction metrics but not grasp, insertion, or collision avoidance, the geometry is not robot-usable.",
                "adversarial": "Use wires, straps, sheets, and transparent or deformable thin objects where vision is ambiguous but contact is informative.",
                "thinking_tool": "Benchmark reconstruction by the missing physical evidence a robot needs to act.",
                "transfer_boundary": "Strong for manipulation and inspection; less direct for open outdoor mapping.",
            },
            {
                "rank": 6,
                "title": "StateSight: Benchmarking Latent Spatial-State Reconstruction in Vision-Language Models",
                "arxiv_id": "2608.20414",
                "fit": "VLM spatial reasoning - latent state reconstruction - benchmark",
                "status": "Tier A - abstract-only",
                "status_quo": "Broad VLM benchmarks mix perception, OCR, prior knowledge, language, and reasoning, making spatial-state failure hard to isolate.",
                "friction": "The abstract reports that VLMs trail humans on cube-net, occluded tower, and connected-component spatial tasks.",
                "hidden_premise": "A useful spatial-reasoning benchmark should have deterministic oracle labels and isolate latent spatial structure from semantic priors.",
                "conceptual_move": "Turn VLM spatial evaluation into controlled latent-state reconstruction tasks with exact-match scoring and human baselines.",
                "mechanism": "The abstract describes procedurally generated cube-net, occluded cube-tower, and connected-component tasks, each with 300 prompts.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper isolates latent spatial structure from mixed broad benchmark factors."},
                    {"trace": "[Abstract]", "claim": "It reports human baselines exceeding tested VLMs on every task family."},
                    {"trace": "[Inference]", "claim": "APRL should test embodied VLM plans against hidden spatial-state reconstruction before action."},
                ],
                "falsification": "If spatial-state scores do not predict navigation, manipulation, or inspection failures, the benchmark remains cognitive rather than embodied.",
                "adversarial": "Add robot camera viewpoints, occluded supports, and distractor object priors so answer fluency cannot replace spatial state.",
                "thinking_tool": "Ask whether the model reconstructed the latent state that a planner would need.",
                "transfer_boundary": "Strong for VLM planning audits; weaker for low-level geometry pipelines that already expose metric state.",
            },
            {
                "rank": 7,
                "title": "RISE: Adaptive Imagination for World Action Models",
                "arxiv_id": "2608.20430",
                "fit": "driving world-action model - adaptive rollout budget - risk supervision",
                "status": "Tier A - abstract-only",
                "status_quo": "World-action models often spend a fixed future-rollout budget regardless of scene risk or planning benefit.",
                "friction": "The abstract says fixed imagination budgets are inefficient because factual logs expose only one realized future.",
                "hidden_premise": "A planner should continue imagining only when the current rollout prefix reveals risk and additional rollout is expected to improve planning.",
                "conceptual_move": "Make world-action imagination an adaptive Roll/Stop decision supervised by counterfactual driving futures.",
                "mechanism": "The abstract describes a latent evaluator, rollout gate, expected planning benefit, compute cost, and CounterDrive risk supervision.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper frames imagination budget as a scene-dependent planning decision."},
                    {"trace": "[Abstract]", "claim": "It constructs CounterDrive with diverse outcomes, risk levels, and expert verification."},
                    {"trace": "[Inference]", "claim": "APRL should score world models by whether extra rollout changes the decision in high-risk scenes."},
                ],
                "falsification": "If adaptive imagination does not change action or risk ranking in rare hazards, it is only a compute scheduler.",
                "adversarial": "Use counterfactual scenes where more imagination reveals a collision, but visually similar low-risk scenes should stop early.",
                "thinking_tool": "Allocate world-model rollout budget where the expected decision value is highest.",
                "transfer_boundary": "Strong for driving and long-horizon planning; less direct for short-horizon manipulation without future branching.",
            },
            {
                "rank": 8,
                "title": "Just Noticeable Difference Modeling for Token Compression in Vision-Language-Action Models",
                "arxiv_id": "2608.21247",
                "fit": "VLA efficiency - token compression - action tolerance",
                "status": "Tier A - abstract-only",
                "status_quo": "Token pruning and cache reuse often rely on visual similarity, attention, or saliency as indirect importance signals.",
                "friction": "The abstract argues that embodied tokens directly affect latency-sensitive closed-loop action prediction, so visual importance can miss action deviation.",
                "hidden_premise": "Safe compression should be defined by how much a token can change before downstream action deviates unacceptably.",
                "conceptual_move": "Borrow just noticeable difference as a receiver-dependent tolerance for VLA token compression.",
                "mechanism": "The abstract frames machine-oriented JND around downstream machine responses rather than human visual perception.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper says embodied-agent tokens affect closed-loop robot action prediction."},
                    {"trace": "[Abstract]", "claim": "It identifies action deviation tolerance as the key factor for safe compression."},
                    {"trace": "[Inference]", "claim": "APRL should compare compression by action delta, not only token count or latency."},
                ],
                "falsification": "If JND-guided compression preserves benchmark action deltas but fails under rare contact or safety states, tolerance was under-specified.",
                "adversarial": "Stress tokens that look redundant visually but encode grasp pose, obstacle boundary, small sign text, or temporal phase.",
                "thinking_tool": "Define efficiency by the smallest representation change that alters the robot action.",
                "transfer_boundary": "Strong for VLA deployment; weaker for offline captioning or retrieval without action consequences.",
            },
        ],
        "synthesis": [
            {
                "title": "VLA action interfaces now need explicit authorizers",
                "links": "CertVLA - Logic-VLA - ForeTime-VLA - JND-VLA - CARD",
                "facts": "The selected abstracts expose patch certificates, temporal-logic formulas, future contact tokens, token tolerance, and belief-to-action routing.",
                "inference": "A VLA benchmark should record which authorizer changed the action and which hidden condition would make that authorizer invalid.",
            },
            {
                "title": "Contact and geometry are becoming state-reconstruction problems",
                "links": "VT-MUSE - ViTacPhys - Koala Gripper - VisTa3D - Stream3Dv2 - ASV coastline localization",
                "facts": "The batch repeatedly uses tactile histories, physical-property estimates, gripper/data co-design, thin-object ground truth, streaming 3D fusion, and coastline constraints.",
                "inference": "APRL should link representation quality to the physical state the controller needs, not just to final visual fidelity.",
            },
            {
                "title": "World models and VLMs are moving toward evidence routing",
                "links": "RISE - WA-JEPA - Route2Look - EviRank - StateSight - spatial CT verification",
                "facts": "World-action and VLM papers expose rollout budget, future latents, query-adaptive evidence tools, structured relevance packages, and deterministic spatial checks.",
                "inference": "Evaluation should ask whether the system acquired the right evidence before answering or planning.",
            },
        ],
        "frontier_memory": [
            {
                "label": "Strengthening",
                "history": "August 18-21 emphasized runtime evidence gates, robot-facing geometry, and scenario-conditioned evaluation.",
                "body": "August 24 strengthens the same axis with certified VLA rollouts, temporal logic conditioning, future-token distillation, action-tolerance compression, and auditable spatial-state reconstruction.",
            },
            {
                "label": "New signal",
                "history": "Recent daily artifacts discussed VLA adaptation and world-action models mostly as policy or latent-interface problems.",
                "body": "Today adds a sharper certification/evidence layer: CertVLA and JND-VLA ask what perturbation can be allowed before closed-loop action changes.",
            },
            {
                "label": "Commoditizing",
                "history": "Video, generation, and VLM papers repeatedly offer new model variants.",
                "body": "The crowded axis is model naming; the defensible axis is whether the paper exposes a reusable benchmark variable such as spatial state, physical consistency, evidence package, or rollout-risk label.",
            },
            {
                "label": "Missing axis",
                "history": "The repo still lacks one shared suite joining VLA safety, tactile manipulation, geometry observability, and world-action rollout value.",
                "body": "APRL can own that gap by building episodes where the same hidden state controls safety authorization, tactile recovery, localization confidence, and future-rollout budget.",
            },
        ],
        "strategy": [
            {
                "priority": "Build moat",
                "title": "Action-authority audit for VLA deployment",
                "thesis": "Require VLA actions to declare whether they were authorized by a safety certificate, logic predicate, future token, tactile state, or action-tolerance rule.",
                "scores": {"fit": 5, "novelty": 5, "feasibility": 4, "moat": 5, "timing": 5, "evidence": 5},
                "one_week": "Create ten manipulation and drone-navigation tasks with physical patches, unseen STL predicates, moving-object phase shifts, and action-token compression variants.",
                "four_week": "Evaluate CertVLA-style masking, Logic-VLA-style predicates, ForeTime-style future tokens, and JND compression under matched closed-loop episodes.",
                "success": "The declared authorizer predicts action deviation, requirement violation, or recovery timing before terminal success changes.",
                "stop": "If authorizer labels do not change policy ranking or failure prediction, narrow the suite to the single strongest interface.",
                "asset": "Closed-loop episodes, patch masks, STL predicates, future-token labels, action-delta tolerances, and rollout authorization traces.",
            },
            {
                "priority": "Build moat",
                "title": "Thin-contact geometry benchmark",
                "thesis": "Connect thin-object reconstruction, tactile histories, physical-property estimates, and gripper co-design to manipulation outcomes.",
                "scores": {"fit": 5, "novelty": 4, "feasibility": 4, "moat": 5, "timing": 4, "evidence": 5},
                "one_week": "Select five thin or deformable objects and collect synchronized RGB-D, tactile response, gripper pose, and slip or deformation labels.",
                "four_week": "Compare visual-only reconstruction, tactile-augmented reconstruction, visuotactile policy latents, and physical-property-aware grasping on the same objects.",
                "success": "Tactile or physical-property evidence predicts grasp recovery, collision avoidance, or insertion success beyond visual reconstruction quality.",
                "stop": "If tactile evidence only improves offline reconstruction metrics, split the benchmark into perception and control tracks.",
                "asset": "Thin-object scenes, tactile maps, object physical-property labels, gripper interaction traces, and robot-usable geometry scores.",
            },
            {
                "priority": "Explore",
                "title": "Evidence-routing world-model evaluator",
                "thesis": "Measure whether extra imagination, video evidence routing, and cooperative perception change decisions only when risk or missing evidence justifies the cost.",
                "scores": {"fit": 4, "novelty": 4, "feasibility": 4, "moat": 4, "timing": 5, "evidence": 4},
                "one_week": "Define driving and mobile-robot scenes with low-risk stop cases, high-risk rollout-needed cases, occluded roadside evidence, and stale collaborator messages.",
                "four_week": "Compare fixed-rollout WAMs, RISE-style adaptive imagination, Route2Look-style evidence acquisition, and cooperative-perception anchors.",
                "success": "Adaptive evidence routing reduces compute on easy scenes and changes the action or confidence on high-risk scenes.",
                "stop": "If routing decisions correlate only with scene length or token count, remove the model and keep a cheaper heuristic baseline.",
                "asset": "Risk-labeled counterfactual scenes, evidence-acquisition logs, cooperative message perturbations, and rollout-value labels.",
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
