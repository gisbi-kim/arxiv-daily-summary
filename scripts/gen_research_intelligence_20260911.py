#!/usr/bin/env python3
"""Generate the 2026-09-11 Research Intelligence edition."""

from __future__ import annotations

import json
from pathlib import Path

from gen_research_intelligence_20260811 import build_html


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PROMPT = "prompts/instruction_v20260713.md"


RI_BY_DATE = {
    "2026-09-11": {
        "date": "2026-09-11",
        "edition": "Research Intelligence",
        "source_prompt": SOURCE_PROMPT,
        "source_mode": "new",
        "scope_note": (
            "Daily edition from matching Friday /new listings: 89 non-replacement cs.CV rows, "
            "44 cs.RO rows, 128 deduplicated papers, and 104 ROI papers. Tier A cards are conservative "
            "abstract-only autopsies from the repository parser output; no figure, table, full-text, code, "
            "or dataset-release claim is asserted unless the abstract itself states it."
        ),
        "executive_thesis": (
            "The September 11 batch asks when a robot or multimodal agent is allowed to trust a transition. "
            "VLA papers move from bigger action heads toward robotized video supervision, single-step action "
            "sampling, memory-grounded planning, predictive-state failure readouts, and hard action constraints. "
            "Geometry papers turn 3DGS, monocular greenhouse SLAM, radar depth, street language fields, and "
            "deformable registration into evidence that must survive relocalization, occlusion, haze, low-cost "
            "sensors, and planner use. Generative and VLM papers stop rewarding visual fluency alone and ask "
            "whether ego-motion, topological structure, hallucination claims, and cached video evidence remain "
            "faithful. The common research decision is to treat memory, geometry, and generated futures as "
            "permission systems whose authority must be tested before they change an action."
        ),
        "decision_cards": [
            {
                "label": "Decision",
                "title": "VLA transitions need executable evidence",
                "body": (
                    "HuRo, IMLE-VLA, FARM, MaP-WAM, UniMPA, and ActSafeGuard each move a different link in the "
                    "observation-to-action chain from implicit trust to measurable transition evidence."
                ),
            },
            {
                "label": "Decision",
                "title": "Maps must prove sensor-survival value",
                "body": (
                    "RIDE, greenhouse Visual-SLAM, GRADE, LangStreet, and radar/GS papers judge geometry by "
                    "whether it still supports metric depth, semantics, or localization under degraded sensing."
                ),
            },
            {
                "label": "Decision",
                "title": "Efficiency is now evidence routing",
                "body": (
                    "Caption-once Frames-on-Demand, OmniKVQuant, RiVaT-Fuse, LoopVAE, and Uncertainty DMD show "
                    "that memory, cache, and fusion budgets must preserve the cue needed by a later decision."
                ),
            },
        ],
        "papers": [
            {
                "rank": 1,
                "title": "HuRo: Robotizing Human Videos for Scalable VLA Pretraining",
                "arxiv_id": "2609.10706",
                "fit": "VLA pretraining - human video robotization - embodiment transfer",
                "status": "Tier A - abstract-only",
                "status_quo": "Large human video corpora look attractive for robot policy learning, but embodiment mismatch can make visual imitation non-executable.",
                "friction": "The abstract says existing approaches either robotize task-matched videos or separately align observation and action at scale.",
                "hidden_premise": "Human videos become useful robot supervision only if missing intermediate signals and robot-aligned actions are reconstructed well enough for execution.",
                "conceptual_move": "Convert heterogeneous human videos into robot-aligned observations and action trajectories, then test whether scale helps VLA pretraining.",
                "mechanism": "HuRo infers missing intermediate signals across annotation levels and builds robotized episodes before downstream manipulation pretraining.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper constructs about 630K robotized episodes and 142M processed frames from five human-video sources."},
                    {"trace": "[Abstract]", "claim": "Increasing robotized pretraining scale improves real-world task completion from 51.5 percent to 80.3 percent and OOD completion from 34.9 percent to 72.2 percent."},
                    {"trace": "[Inference]", "claim": "APRL should judge human-video pretraining by execution transfer under spatial and visual shifts, not by clip count alone."},
                ],
                "falsification": "If gains disappear when action retargeting or visual robotization is stress-tested separately, scale is not the causal explanation.",
                "adversarial": "Hold video scale fixed and ablate visual robotization, action retargeting, missing-signal inference, and OOD object placement.",
                "thinking_tool": "Treat robotized video as executable supervision only after testing which alignment step changes the robot action.",
                "transfer_boundary": "Strong for manipulation pretraining; weaker for tasks whose human motions lack robot-actuator or contact analogues.",
            },
            {
                "rank": 2,
                "title": "IMLE-VLA: Fast Single-Step Action Generation for Vision-Language-Action Policies",
                "arxiv_id": "2609.10915",
                "fit": "VLA action generation - single-step sampling - deployment smoothness",
                "status": "Tier A - abstract-only",
                "status_quo": "Continuous VLA action heads often use iterative diffusion or flow-matching sampling and accept latency as the price of multimodality.",
                "friction": "The abstract links multi-step sampling to stop-and-go robot movement and slower task completion.",
                "hidden_premise": "A single-step generator can preserve multimodal action coverage if its objective prevents the collapse of naive regression.",
                "conceptual_move": "Replace iterative action sampling with conditional implicit maximum likelihood estimation for one-shot action generation.",
                "mechanism": "The cIMLE objective keeps multimodal action coverage while removing the repeated Euler-style sampling loop.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "Applied to pi_0.5, IMLE-VLA raises inference frequency from 15 Hz to 55 Hz and enables up to 11x higher action throughput."},
                    {"trace": "[Abstract]", "claim": "It reports 98.0 percent average success on the 40-task LIBERO benchmark and lower jerk in real Franka tasks."},
                    {"trace": "[Inference]", "claim": "APRL should test whether action-head speed changes contact stability before treating success rate as the whole story."},
                ],
                "falsification": "If single-step actions smooth easy motions but fail rare multimodal contact choices, latency gains may hide lost policy diversity.",
                "adversarial": "Evaluate perturbation, contact-rich, and multi-modal grasp choices while measuring jerk, action throughput, and failure recovery.",
                "thinking_tool": "A faster action head is only a robotics gain if the removed sampling steps were not carrying decisive uncertainty.",
                "transfer_boundary": "Direct for VLA manipulation; less direct for planners where action generation is not the runtime bottleneck.",
            },
            {
                "rank": 3,
                "title": "FARM: Reading Failure Signals from the Internal Predictive States of a Frozen Robotic World Model",
                "arxiv_id": "2609.11445",
                "fit": "robot failure monitoring - frozen world-model states - causal trajectory risk",
                "status": "Tier A - abstract-only",
                "status_quo": "Online robot failure monitors usually rely on proxy signals or separately trained monitoring models.",
                "friction": "The abstract asks whether a frozen pretrained robotic world model already contains decodable failure information.",
                "hidden_premise": "A predictive state is useful for deployment only if it exposes failure risk without updating the policy backbone.",
                "conceptual_move": "Train a tiny supervised readout over frozen VLA-JEPA predictive states for step-wise failure scores and causal trajectory risk.",
                "mechanism": "FARM keeps the predictive backbone frozen and learns a 33,985-parameter readout, then tests transfer and readout-only adaptation.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "Five-fold out-of-fold evaluation reports 85.68 pooled AUROC and 88.59 pooled AUPRC."},
                    {"trace": "[Abstract]", "claim": "The study tests real-robot populations on PIPER X, SO-101, and Franka and adds 0.2256 ms mean CUDA latency once the frozen state is available."},
                    {"trace": "[Inference]", "claim": "APRL should measure whether predictive-state warning lead time precedes recoverable execution failures."},
                ],
                "falsification": "If the readout only detects already-visible terminal mistakes, it is a post-hoc classifier rather than a control-useful monitor.",
                "adversarial": "Compare partial causal histories, hidden object shifts, and cross-robot transfer while measuring warning lead time and recovery success.",
                "thinking_tool": "Do not ask only what the world model predicts; ask when its hidden state knows an action is becoming unsafe.",
                "transfer_boundary": "Strong for VLA-JEPA-like manipulation systems; weaker for policies without comparable predictive states.",
            },
            {
                "rank": 4,
                "title": "UniMPA: A Unified Memory-Prediction-Action Model via Action-Grounded Transition Modeling",
                "arxiv_id": "2609.11875",
                "fit": "VLA memory - future prediction - action-grounded transitions",
                "status": "Tier A - abstract-only",
                "status_quo": "Observation-to-action policies can treat future prediction, memory retrieval, and action generation as loosely coupled modules.",
                "friction": "The abstract names transition ambiguity, prediction-execution mismatch, and experience-realization mismatch as coupled failures.",
                "hidden_premise": "A predicted future should be trusted only if it is grounded in historically executable visual-action evidence for the current scene.",
                "conceptual_move": "Use a shared action-grounded transition interface that connects persistent future prediction, visual-action memory, and prototype-biased flow.",
                "mechanism": "UniMPA tracks task progress with persistent/selective future streams and queries temporal and action-visual memory banks before refining actions.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper frames the limitation as a transition realizability gap with three named subproblems."},
                    {"trace": "[Abstract]", "claim": "It retrieves historically realized visual-action experience to judge whether a predicted transition is physically executable."},
                    {"trace": "[Inference]", "claim": "APRL should score future predictions by whether they can be realized by the robot in the current contact state."},
                ],
                "falsification": "If memory retrieval improves visual plausibility but not action feasibility under scene changes, the interface is not action-grounded.",
                "adversarial": "Construct visually similar phases requiring different transitions, then perturb contact state and historical action prototypes independently.",
                "thinking_tool": "A future frame is not evidence until a robot action can realize it.",
                "transfer_boundary": "Strong for long-horizon manipulation; weaker for open-world navigation where transition prototypes are less repeatable.",
            },
            {
                "rank": 5,
                "title": "RIDE: Relocalization-Informed Depth Estimation with 3D Gaussian Splatting",
                "arxiv_id": "2609.11079",
                "fit": "3DGS maps - relocalization geometry - robot RGB depth",
                "status": "Tier A - abstract-only",
                "status_quo": "Render-match-PnP relocalization is often treated as a pose-recovery tool, while dense depth is learned by a separate model.",
                "friction": "The abstract says relocalization correspondences carry metric geometry that is usually overlooked for depth estimation.",
                "hidden_premise": "A 3DGS map is robot-useful if sparse pose correspondences can correct dense perception through observation gaps.",
                "conceptual_move": "Fuse PnP-RANSAC inlier depth from a metrically scaled 3DGS model with pretrained video-depth priors for robot RGB streams.",
                "mechanism": "RIDE combines sparse metric depth, global/local correction, and temporal memory to support dense depth through intermittent observations.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The method estimates dense metric depth from a robot RGB stream using a metrically scaled 3DGS model."},
                    {"trace": "[Abstract]", "claim": "It is evaluated on robot sequences without fine tuning and reports improved depth accuracy and temporal consistency over scale-only calibration."},
                    {"trace": "[Inference]", "claim": "APRL should evaluate 3DGS maps by depth and relocalization recovery under observation gaps."},
                ],
                "falsification": "If improvement vanishes when PnP inliers are sparse or dynamic objects dominate, the map is not robust enough for deployment.",
                "adversarial": "Sweep occlusion length, map scale error, dynamic clutter, and view angle while measuring depth drift and pose recovery.",
                "thinking_tool": "Use relocalization geometry as a correction signal, not just a success/failure pose output.",
                "transfer_boundary": "Direct for mapped robot environments; weaker for unstructured scenes without a maintained metric 3DGS model.",
            },
            {
                "rank": 6,
                "title": "ReactHuman: A Physics-Grounded Benchmark for Human-Like Reactive Decision-Making in Embodied Multimodal LLMs",
                "arxiv_id": "2609.10895",
                "fit": "embodied MLLM safety - physical hazard reaction - executable evaluation",
                "status": "Tier A - abstract-only",
                "status_quo": "Embodied MLLM evaluation often measures passive video understanding or deliberate long-horizon planning.",
                "friction": "The abstract says no prior benchmark measures whether a model can turn physical understanding into immediate safety-critical action.",
                "hidden_premise": "A household robot decision core must be judged by the physical consequences of committed reactions, not by plausible explanations.",
                "conceptual_move": "Put the evaluated MLLM inside simulated humanoid hazard scenes and execute every committed plan.",
                "mechanism": "ReactHuman uses 17 event families, reproducible rigid-body scenes, adversarial object appearances, and a five-metric reaction suite.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The benchmark contains over 1,000 bit-for-bit reproducible scenes with 240 Hz rigid-body simulation ground truth."},
                    {"trace": "[Abstract]", "claim": "Seven evaluated MLLMs mishandle roughly one hazard in three, and the failures do not shrink with model scale in the reported study."},
                    {"trace": "[Inference]", "claim": "APRL should evaluate embodied reasoning by executed reaction safety under misleading appearance and motion cues."},
                ],
                "falsification": "If improved controllers solve reaction timing while the language model still chooses unsafe goals, the benchmark conflates policy and motor layers.",
                "adversarial": "Hold the hazard physics fixed while swapping appearance, reaction deadline, embodiment reach, and available evasive actions.",
                "thinking_tool": "Physical understanding earns authority only when the chosen action survives execution.",
                "transfer_boundary": "Strong for household and humanoid safety; less direct for slow inspection tasks where reaction timing is not dominant.",
            },
            {
                "rank": 7,
                "title": "Beyond Visual Quality: Evaluating Physical Consistency under Ego-Motion with EgoGenEval",
                "arxiv_id": "2609.11172",
                "fit": "generative world models - ego-motion consistency - embodied planning evidence",
                "status": "Tier A - abstract-only",
                "status_quo": "Visual generators are often benchmarked by single-image fidelity or short-step perceptual quality.",
                "friction": "The abstract says physical consistency under ego-motion remains underexplored and current models struggle to preserve scene state while moving the camera.",
                "hidden_premise": "A generated observation is useful for planning only if camera motion and scene-state preservation are both reliable.",
                "conceptual_move": "Build a pose-free benchmark that separates camera motion grounding from scene state preservation across single and multi-step ego-motion.",
                "mechanism": "EgoGenEval evaluates generators with geometry-grounded target views and validates CMG and SSP metrics against blinded human judgments.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The benchmark has 1,400 cases and 2,360 target views spanning single-step and multi-step ego-motion."},
                    {"trace": "[Abstract]", "claim": "Across 16 pose-free generators and two pose-conditioned references, no system performs well on both camera motion and scene-state preservation."},
                    {"trace": "[Inference]", "claim": "APRL should reject generated rollouts that improve appearance while breaking navigation-relevant state."},
                ],
                "falsification": "If pose-conditioned supervision fixes both axes in closed-loop robot scenes, the bottleneck may be the training objective rather than generation.",
                "adversarial": "Test self-conditioned rollouts with occluded obstacles, repeated turns, and contact-relevant objects that must persist across camera motion.",
                "thinking_tool": "Separate moving the camera from preserving the world.",
                "transfer_boundary": "Strong for vision-based world models; weaker for non-visual planners with explicit state simulators.",
            },
            {
                "rank": 8,
                "title": "Caption-once, Frames-on-Demand: Visual-Need Routing for Budget-Aware Agentic Long Video Understanding",
                "arxiv_id": "2609.11899",
                "fit": "long-video agents - visual evidence routing - edge-cloud compute budget",
                "status": "Tier A - abstract-only",
                "status_quo": "Long-video systems often choose between dense visual tokens that are expensive and text summaries that lose fine visual attributes.",
                "friction": "The abstract states that language memories preserve temporal structure better, while pixels remain decisive for attribute-level perception.",
                "hidden_premise": "The system should retrieve frames only when the query actually needs visual evidence that text memory cannot carry.",
                "conceptual_move": "Create a dual-track narrative index and route each query through a Visual-Need Router before bounded keyframe retrieval.",
                "mechanism": "An edge pass builds story and micro-log memory; cloud-side reasoning retrieves frames only for perceptual questions.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The router triggers keyframe retrieval for perceptual questions and keeps temporal-structural questions in language space."},
                    {"trace": "[Abstract]", "claim": "The framework caps per-query frame consumption regardless of video length while reporting strong accuracy-efficiency trade-offs."},
                    {"trace": "[Inference]", "claim": "APRL should treat robot video memory as query-conditioned evidence admission, not a fixed frame budget."},
                ],
                "falsification": "If decisive safety cues are rare and not predictable from the language memory, the router may skip exactly the frames needed for action.",
                "adversarial": "Place task-critical visual changes in brief off-center frames and ask queries whose language story sounds sufficient but is wrong.",
                "thinking_tool": "Retrieve pixels only when the decision contract names what text cannot know.",
                "transfer_boundary": "Useful for inspection robots and long-horizon video agents; needs safety guards before online control use.",
            },
            {
                "rank": 9,
                "title": "When Information is Worth the Risk: Behavioral Valuation for Hazardous Robotic Exploration",
                "arxiv_id": "2609.10726",
                "fit": "hazardous exploration - information-risk valuation - failure-truncated sensing",
                "status": "Tier A - abstract-only",
                "status_quo": "Active exploration often rewards the action that reduces uncertainty most, then adds risk as a secondary constraint.",
                "friction": "The abstract says a highly informative path can expose the robot to hazards, terminate execution, and prevent future observations.",
                "hidden_premise": "Information gain has value only after accounting for the chance that collecting it destroys the robot's ability to continue sensing.",
                "conceptual_move": "Keep belief update, sensor, risk, and planner fixed, and change only the scalar objective that ranks feasible paths.",
                "mechanism": "The paper introduces a risk-augmented Behavioral Information objective based on Prelec probability weighting and studies switching boundaries.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "Failure-truncated grid-world experiments show that valuation alone reshapes the information-risk frontier."},
                    {"trace": "[Abstract]", "claim": "Risk-aware objectives reduce hazard exposure and robot losses by avoiding failures that truncate future sensing."},
                    {"trace": "[Inference]", "claim": "APRL should measure exploration value by future-sensing survival as well as uncertainty reduction."},
                ],
                "falsification": "If risk valuation becomes too conservative under recoverable hazards, it may lose mission value while appearing safe.",
                "adversarial": "Compare Shannon information, risk-aware, and behavioral valuation objectives where hazards differ in reversibility and observability.",
                "thinking_tool": "Information is not valuable if acquiring it removes the robot from the experiment.",
                "transfer_boundary": "Direct for field robotics and inspection; less direct for offline perception datasets without action risk.",
            },
            {
                "rank": 10,
                "title": "OmniKVQuant: KV Cache Quantization for Omni-LLMs",
                "arxiv_id": "2609.11582",
                "fit": "omni-modal LLMs - KV cache quantization - temporal and modality geometry",
                "status": "Tier A - abstract-only",
                "status_quo": "Text-only KV quantization recipes are often assumed to transfer to multimodal or omni-modal caches.",
                "friction": "The abstract identifies temporal key drift and heterogeneous value geometry as critical issues for audio-video-text caches.",
                "hidden_premise": "Cache compression should preserve modality-specific value structure and short-window temporal key ranges before it is deployment-safe.",
                "conceptual_move": "Quantize keys over short input windows and rotate values separately per modality in a training-free omni-modal framework.",
                "mechanism": "OmniKVQuant adapts rotation-based cache quantization and includes a fused Triton decode kernel that avoids constructing dense FP16 cache.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "On Qwen2.5-Omni and Qwen3-Omni, the method enables 2-bit KV caches while substantially preserving performance across seven audio-visual benchmarks."},
                    {"trace": "[Abstract]", "claim": "The paper reports no dense FP16 cache is built during the fused Triton decode path."},
                    {"trace": "[Inference]", "claim": "APRL should audit whether robot multimodal cache compression preserves temporal and geometric evidence for later actions."},
                ],
                "falsification": "If compressed caches preserve benchmark averages but lose rare temporal cues, robot-agent safety can still degrade.",
                "adversarial": "Stress audio-visual streams with delayed cues, modality-specific distractors, and long action histories under 2-bit cache limits.",
                "thinking_tool": "Cache compression is an evidence geometry problem, not just a memory footprint problem.",
                "transfer_boundary": "Strong for omni-modal agents; needs embodied benchmarks before claiming control reliability.",
            },
        ],
        "synthesis": [
            {
                "title": "VLA reliability is becoming transition accountability",
                "links": "HuRo - IMLE-VLA - FARM - MaP-WAM - UniMPA - ActSafeGuard",
                "facts": "The abstracts separately test robotized video scale, single-step action sampling, frozen predictive-state failure signals, memory-grounded plans, transition realizability, and differentiable hard constraints.",
                "inference": "The shared decision is to expose the evidence that authorizes a transition before policy training, prediction, memory, or safety layers can change the action.",
            },
            {
                "title": "Robot geometry is moving toward sensor-survival protocols",
                "links": "RIDE - Visual-SLAM tomatoes - GRADE - LangStreet - 3D Point Splatting",
                "facts": "The papers attach 3DGS maps, monocular SfM localization, radar-conditioned depth, persistent language fields, and mmWave splatting to degraded or low-cost sensing.",
                "inference": "APRL should evaluate maps by relocalization, metric depth, semantic persistence, and planner outcome under the failures expected outside curated RGB scenes.",
            },
            {
                "title": "Generative and efficient models now need permission tests",
                "links": "EgoGenEval - VWG-Bench - MindTopo - CFD - OmniKVQuant",
                "facts": "The batch probes camera-motion grounding, rule-constrained video reasoning, topological planning, query-conditioned frame retrieval, and omni-modal cache geometry.",
                "inference": "A generated frame, retrieved keyframe, compressed cache, or topological answer should be used only after its decision-level evidence contract is tested.",
            },
        ],
        "frontier_memory": [
            {
                "label": "Strengthening",
                "history": "September 9 and 10 framed robot action as authorized by fresh evidence, verifiers, maps, and belief states.",
                "body": "September 11 strengthens the same line with explicit transition realizability, predictive-state failure scores, single-step action latency, and hard constraint layers.",
            },
            {
                "label": "New signal",
                "history": "Recent geometry releases emphasized map uncertainty, degeneracy, and planner-facing validity.",
                "body": "Today adds sensor-survival geometry: radar depth under smoke, monocular greenhouse SLAM, street Gaussian language fields, and 3DGS relocalization depth.",
            },
            {
                "label": "Commoditizing",
                "history": "World-model language has appeared repeatedly across VLA, video generation, and planning.",
                "body": "The phrase is no longer enough; the useful distinction is whether the model preserves ego-motion, topology, executable state, memory, or physical contact evidence.",
            },
            {
                "label": "Contradiction",
                "history": "More context, larger scale, and richer generated futures often look like the default answer.",
                "body": "Caption-once routes away from pixels unless needed, IMLE-VLA removes iterative sampling, and EgoGenEval shows pairwise supervision can improve camera motion without preserving scene state.",
            },
            {
                "label": "Missing axis",
                "history": "The repo has separate VLA, geometry, safety, and efficient-agent threads.",
                "body": "A unified benchmark should ask whether the same evidence packet authorizes memory update, map use, frame retrieval, failure warning, and action execution.",
            },
        ],
        "strategy": [
            {
                "priority": "Build moat",
                "portfolio": "Build moat",
                "title": "Transition-accountability suite for VLA policies",
                "thesis": "Build an evaluation harness where pretraining data, action heads, predictive states, memory banks, and safeguard layers must declare which transition evidence they authorize.",
                "scores": {"strategic_fit": 5, "asymmetry": 5, "timing": 5, "tractability": 4, "defensibility": 5, "scientific_depth": 5},
                "one_week": "Run a small LIBERO/RoboCasa-style suite with robotized-human-video pretraining, single-step action heads, frozen failure readouts, and hard-constraint interventions.",
                "one_week_probe": "Run a small LIBERO/RoboCasa-style suite with robotized-human-video pretraining, single-step action heads, frozen failure readouts, and hard-constraint interventions.",
                "four_week": "Add transition-realizability labels, memory-bank retrieval traces, per-step safety violations, jerk/action-frequency metrics, and recovery outcomes across real tabletop tasks.",
                "four_week_build": "Add transition-realizability labels, memory-bank retrieval traces, per-step safety violations, jerk/action-frequency metrics, and recovery outcomes across real tabletop tasks.",
                "success": "A transition-evidence score predicts recovery, jerk, safety violation, and task success better than terminal success or VLA confidence alone.",
                "success_metric": "A transition-evidence score predicts recovery, jerk, safety violation, and task success better than terminal success or VLA confidence alone.",
                "stop": "Stop if transition labels collapse to terminal success and do not change policy selection, monitor timing, or safety intervention choice.",
                "stop_condition": "Stop if transition labels collapse to terminal success and do not change policy selection, monitor timing, or safety intervention choice.",
                "paper_path": "Transition accountability for memory- and verifier-aware VLA control.",
                "asset_path": "Aligned episodes, transition labels, failure-readout traces, action-head latency, constraint violations, and recovery logs.",
                "asset": "Aligned episodes, transition labels, failure-readout traces, action-head latency, constraint violations, and recovery logs.",
            },
            {
                "priority": "Exploit",
                "portfolio": "Exploit",
                "title": "Sensor-survival geometry benchmark",
                "thesis": "Evaluate 3DGS, radar depth, monocular SLAM, language fields, and event-based relative localization by whether geometry remains useful when ordinary RGB evidence degrades.",
                "scores": {"strategic_fit": 5, "asymmetry": 4, "timing": 5, "tractability": 4, "defensibility": 5, "scientific_depth": 5},
                "one_week": "Collect a corridor/tabletop/greenhouse-style mini-suite with haze, occlusion, low light, sparse views, and degraded ground-robot sensing.",
                "one_week_probe": "Collect a corridor/tabletop/greenhouse-style mini-suite with haze, occlusion, low light, sparse views, and degraded ground-robot sensing.",
                "four_week": "Compare RIDE-style relocalization depth, GRADE-style radar conditioning, monocular SfM/GLOMAP, street Gaussian semantics, and event-camera relative localization.",
                "four_week_build": "Compare RIDE-style relocalization depth, GRADE-style radar conditioning, monocular SfM/GLOMAP, street Gaussian semantics, and event-camera relative localization.",
                "success": "A sensor-survival score predicts depth drift, wrong localization, semantic map decay, and navigation or manipulation failure under degraded sensing.",
                "success_metric": "A sensor-survival score predicts depth drift, wrong localization, semantic map decay, and navigation or manipulation failure under degraded sensing.",
                "stop": "Stop if degradation-specific geometry improves visual metrics without changing downstream action success or recovery behavior.",
                "stop_condition": "Stop if degradation-specific geometry improves visual metrics without changing downstream action success or recovery behavior.",
                "paper_path": "Robot-usable geometry under sensor degradation and low-cost mapping.",
                "asset_path": "Degraded RGB/radar/event datasets, monocular map reconstructions, relocalization traces, semantic persistence labels, and downstream task outcomes.",
                "asset": "Degraded RGB/radar/event datasets, monocular map reconstructions, relocalization traces, semantic persistence labels, and downstream task outcomes.",
            },
            {
                "priority": "Explore",
                "portfolio": "Explore",
                "title": "Physical-consequence permission benchmark",
                "thesis": "Unify reactive hazards, ego-motion generation, topological planning, hazardous exploration, and formal steering verification under one question: when may evidence change action?",
                "scores": {"strategic_fit": 4, "asymmetry": 5, "timing": 5, "tractability": 3, "defensibility": 4, "scientific_depth": 5},
                "one_week": "Prototype ten scenes where a generated view, topological relation, risk valuation, or formal bound recommends a different action than a baseline controller.",
                "one_week_probe": "Prototype ten scenes where a generated view, topological relation, risk valuation, or formal bound recommends a different action than a baseline controller.",
                "four_week": "Connect executable hazard tests, ego-motion rollouts, topology-preserving planning, information-risk frontiers, and between-test-case steering bounds.",
                "four_week_build": "Connect executable hazard tests, ego-motion rollouts, topology-preserving planning, information-risk frontiers, and between-test-case steering bounds.",
                "success": "The benchmark exposes action reversals that are invisible to visual fluency, scalar confidence, or simulated test-case pass rates.",
                "success_metric": "The benchmark exposes action reversals that are invisible to visual fluency, scalar confidence, or simulated test-case pass rates.",
                "stop": "Stop if the scenarios cannot produce reproducible physical consequences or if model ranking matches ordinary static QA metrics.",
                "stop_condition": "Stop if the scenarios cannot produce reproducible physical consequences or if model ranking matches ordinary static QA metrics.",
                "paper_path": "Permission tests for generated, formal, and embodied evidence in safety-critical robot action.",
                "asset_path": "Executable hazard scenes, ego-motion rollouts, topological tasks, risk-frontier maps, formal bounds, and action-reversal annotations.",
                "asset": "Executable hazard scenes, ego-motion rollouts, topological tasks, risk-frontier maps, formal bounds, and action-reversal annotations.",
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
