#!/usr/bin/env python3
"""Generate Research Intelligence editions for the 2026-08-03..05 catch-up run."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PROMPT = "prompts/instruction_v20260713.md"


RI_BY_DATE = {
    "2026-08-03": {
        "date": "2026-08-03",
        "edition": "Research Intelligence",
        "source_prompt": SOURCE_PROMPT,
        "source_mode": "pastweek-date-section",
        "scope_note": (
            "Backfill edition from arXiv /pastweek date sections. The repo parser found "
            "98 cs.CV rows and 36 cs.RO rows; after deduplication, 127 papers remained and 58 were ROI. "
            "Tier A cards use official arXiv abstract pages plus available arXiv HTML headings, and avoid "
            "claiming PDF-only evidence."
        ),
        "executive_thesis": (
            "The August 3 backfill is about replacing generic VLA scaling with state-aware policy repair. "
            "WCM asks whether the critic should see temporal robot history, RayViT injects camera rays before "
            "imitation breaks under viewpoint shift, ST-WAM separates action-relevant future state from visual "
            "hallucination, and CorrelationFlow rejects the common LiDAR scene-flow formulation when sparse or "
            "fast objects violate its assumptions. APRL should treat viewpoint, temporal history, and failure "
            "geometry as separate audit axes before adding more robot demonstrations."
        ),
        "decision_cards": [
            {
                "label": "Decision",
                "title": "Critics need robot history, not only current-frame features",
                "body": (
                    "WCM frames single-frame critic latents as a mismatch for partially observable robot control. "
                    "That pushes APRL toward value diagnostics that condition on recent observation, action, and state transitions."
                ),
            },
            {
                "label": "Decision",
                "title": "Viewpoint robustness is a geometry interface problem",
                "body": (
                    "RayViT does not just add more augmentation; it gives the visual backbone camera-ray structure. "
                    "A VLA robustness run should ablate geometry encoding separately from data volume."
                ),
            },
            {
                "label": "Decision",
                "title": "World-action models must preserve task state under visual shift",
                "body": (
                    "ST-WAM identifies training-distribution hallucination in visually shifted futures. "
                    "Future prediction is useful for control only when it keeps the state that changes the action."
                ),
            },
        ],
        "papers": [
            {
                "rank": 1,
                "title": "WCM: A World Critic Model for Vision-Language-Action Reinforcement Learning",
                "arxiv_id": "2607.29613",
                "fit": "VLA reinforcement learning - temporal critic - partially observable control",
                "status": "Tier A - official arXiv abstract and HTML structure checked",
                "status_quo": "VLA RL post-training often attaches a critic to current visual state or current VLM latents.",
                "friction": "Robot manipulation is partially observable; a single frame can miss the causal state that explains success or failure.",
                "hidden_premise": "A useful critic must compress recent world history without exploding the visual-state complexity.",
                "conceptual_move": "Treat the value estimator as a world critic that reasons over temporally grounded robot state.",
                "mechanism": "The official abstract motivates history-aware critic modeling for VLA RL instead of a single-frame value head.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper explicitly calls single-frame critic observations a mismatch for partially observable robot control."},
                    {"trace": "[HTML headings]", "claim": "The official arXiv HTML exposes Methodology and Experiments sections for the world critic formulation."},
                    {"trace": "[Inference]", "claim": "The reusable APRL variable is critic state history, not a larger policy backbone."},
                ],
                "falsification": "If history-aware critics do not improve under occlusion, delayed reward, or contact ambiguity, the claimed world-state benefit is weak.",
                "adversarial": "A history critic can overfit benchmark progress signals unless evaluated on held-out failure families.",
                "thinking_tool": "Before RL post-training, decide which unobserved state the critic must remember and how to ablate it.",
                "transfer_boundary": "Best for multi-step manipulation and delayed-contact tasks; weaker for single-step pick tasks with full observability.",
            },
            {
                "rank": 2,
                "title": "RayViT: Ray-Conditioned Visual Representations for Viewpoint-Robust Imitation Learning",
                "arxiv_id": "2607.29622",
                "fit": "viewpoint-robust imitation - camera geometry - visual representation",
                "status": "Tier A - official arXiv abstract and HTML structure checked",
                "status_quo": "Imitation policies trained from RGB often absorb camera viewpoint as an untyped nuisance.",
                "friction": "RGB lacks explicit geometric cues, so policies become brittle when camera pose shifts.",
                "hidden_premise": "The perception backbone should know the camera ray geometry before it maps pixels to action state.",
                "conceptual_move": "Inject Plucker ray maps into a pretrained ViT with gated cross-attention.",
                "mechanism": "Ray features condition image patches, making viewpoint part of the representation rather than a hidden dataset bias.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper names RGB-only camera perturbation brittleness and proposes a ray-conditioned ViT encoder."},
                    {"trace": "[HTML headings]", "claim": "Official HTML includes simulated and real robot experiment sections."},
                    {"trace": "[Inference]", "claim": "APRL should compare ray-conditioned encoders against viewpoint augmentation at equal data size."},
                ],
                "falsification": "If ray conditioning helps only on synthetic camera shifts but not real robot camera recalibration, it is not a robust interface.",
                "adversarial": "Camera geometry can be miscalibrated; the robustness claim needs calibration-error stress splits.",
                "thinking_tool": "Expose camera geometry as a typed policy input before collecting more viewpoint-diverse demos.",
                "transfer_boundary": "Strong for multi-camera and mobile manipulation; less direct when proprioception or tactile state dominates.",
            },
            {
                "rank": 3,
                "title": "ST-WAM: Semantic-Temporal World Action Model for Robust Manipulation under Visual Distribution Shifts",
                "arxiv_id": "2607.28993",
                "fit": "world-action model - visual shift - manipulation robustness",
                "status": "Tier A - official arXiv abstract and HTML structure checked",
                "status_quo": "WAMs often supervise future pixels and actions together, assuming generated futures preserve control-relevant state.",
                "friction": "Under visual distribution shift, generated futures can hallucinate training-domain content rather than the actual shifted scene.",
                "hidden_premise": "The future state useful for action is semantic-temporal, not every visual detail in the predicted frame.",
                "conceptual_move": "Separate action-relevant future state from task-irrelevant visual content in WAM supervision.",
                "mechanism": "The abstract identifies Training-Distribution Hallucination and motivates a semantic-temporal WAM for robust manipulation.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The authors describe WAM future supervision entangling action-relevant transitions with irrelevant visual content."},
                    {"trace": "[HTML headings]", "claim": "Official HTML includes Methodology and Experiments sections."},
                    {"trace": "[Inference]", "claim": "The key APRL audit is whether the generated future preserves the state that changes action choice."},
                ],
                "falsification": "If shifted futures look wrong but action success remains unchanged, visual hallucination is not the operational failure.",
                "adversarial": "A semantic-temporal loss can still hide force, contact, and object-state errors.",
                "thinking_tool": "Evaluate WAMs by action-state preservation under controlled visual shifts.",
                "transfer_boundary": "Useful for visually shifted manipulation; less complete for contact-rich tasks without force channels.",
            },
            {
                "rank": 4,
                "title": "CorrelationFlow: A Training-Free Geometric Approach for LiDAR Scene Flow Estimation",
                "arxiv_id": "2607.29237",
                "fit": "LiDAR scene flow - geometric formulation - sparse moving objects",
                "status": "Tier A - official arXiv abstract and HTML structure checked",
                "status_quo": "Recent LiDAR scene-flow methods share feed-forward architectures and self-supervised losses.",
                "friction": "Those assumptions fail together for sparse, distant, or fast-moving objects.",
                "hidden_premise": "When a formulation fails, adding parameters or simulated data may not repair the geometric blind spot.",
                "conceptual_move": "Use a training-free geometric approach to scene flow instead of another learned variant of the same template.",
                "mechanism": "The official abstract frames the method as a deliberate escape from shared architectural monoculture.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper names sparse, distant, and fast-moving object failures as shared blind spots."},
                    {"trace": "[HTML headings]", "claim": "Official HTML includes CorrelationFlow, component, and keypoint sections."},
                    {"trace": "[Inference]", "claim": "APRL should keep a classical geometric baseline in dynamic-map evaluations."},
                ],
                "falsification": "If learned baselines recover under matched sparse-object stress, the formulation critique is overstated.",
                "adversarial": "Training-free geometry can be brittle under sensor noise, rain, or severe ego-motion.",
                "thinking_tool": "When a whole method family fails together, change the problem formulation before scaling it.",
                "transfer_boundary": "Direct for LiDAR flow and map update; indirect for RGB-only SLAM.",
            },
        ],
        "synthesis": [
            {
                "title": "State variables are becoming the real comparison unit",
                "links": "WCM - RayViT - ST-WAM",
                "facts": "The papers each introduce a missing state channel: temporal critic history, camera rays, or semantic-temporal future state.",
                "inference": "APRL should compare policies by which hidden state they expose and ablate, not by backbone family.",
            },
            {
                "title": "Geometry remains a counterweight to learned monoculture",
                "links": "CorrelationFlow - GO-PRE - FillGS",
                "facts": "The 3D/Scene bucket includes LiDAR scene flow, active reconstruction entropy, and Gaussian gap filling.",
                "inference": "A robot map benchmark should include geometric failure cases before accepting generated or learned map updates.",
            },
        ],
        "frontier_memory": [
            {"label": "Strengthening", "history": "Late July already emphasized WAM state channels.", "body": "August 3 adds critic history and camera-ray geometry as typed interfaces."},
            {"label": "Missing axis", "history": "Prior releases tracked geometry validity.", "body": "Force/contact uncertainty remains under-specified in the WAM papers selected today."},
        ],
        "strategy": [
            {
                "priority": "Build moat",
                "title": "Typed-state VLA audit harness",
                "thesis": "Measure whether temporal history, camera geometry, and generated future state independently change action success.",
                "scores": {"fit": 5, "novelty": 4, "feasibility": 4, "moat": 5, "timing": 5, "evidence": 4},
                "one_week": "Run one policy with camera-ray on/off, critic-history on/off, and shifted-background WAM probes.",
                "four_week": "Build a reusable typed-state benchmark for VLA and WAM failures.",
                "success": "At least one state channel predicts a held-out failure family better than a generic confidence score.",
                "stop": "No channel changes failure prediction or recovery under controlled stress.",
                "asset": "Typed-state audit schema plus small stress-suite videos.",
            }
        ],
    },
    "2026-08-04": {
        "date": "2026-08-04",
        "edition": "Research Intelligence",
        "source_prompt": SOURCE_PROMPT,
        "source_mode": "pastweek-date-section",
        "scope_note": (
            "Large Tuesday backfill from arXiv /pastweek date sections: 331 cs.CV rows, 118 cs.RO rows, "
            "431 deduplicated papers, and 194 ROI papers. Tier A cards use official arXiv abstract pages and "
            "available arXiv HTML headings."
        ),
        "executive_thesis": (
            "The August 4 backlog is the clearest contact-rich and evidence-compression day in this run. "
            "DynamicManip, Demystifying VLA Failures, ChainVLA, and Messages Not Tokens all reject periodic, "
            "opaque reuse: a robot needs to know which motion state, contact condition, cross-query memory, or "
            "visual evidence message remains valid. The strategy shift for APRL is to evaluate replanning, token "
            "compression, and WAM feedback by preserved decision state rather than average success alone."
        ),
        "decision_cards": [
            {
                "label": "Decision",
                "title": "Contact-rich VLA failures need diagnosis before architecture changes",
                "body": "The contact-rich papers separate precision, force, tactile, and trajectory-prior failures. That should become the first APRL ablation grid.",
            },
            {
                "label": "Decision",
                "title": "Cross-query memory is a VLA execution state",
                "body": "ChainVLA frames repeated action chunks as an incomplete handoff problem, not just a longer-horizon planning problem.",
            },
            {
                "label": "Decision",
                "title": "Compression should preserve messages, not isolated patches",
                "body": "Messages Not Tokens challenges Top-K token pruning and moves the evidence unit toward collective signed visual messages.",
            },
        ],
        "papers": [
            {
                "rank": 1,
                "title": "DynamicManip: Enabling Dynamic Manipulation from a Single Static Demonstration",
                "arxiv_id": "2608.01452",
                "fit": "dynamic manipulation - single demonstration - real-time policy execution",
                "status": "Tier A - official arXiv abstract and HTML structure checked",
                "status_quo": "Dynamic manipulation usually demands many demonstrations covering moving-object variations.",
                "friction": "Dynamic scenarios have combinatorial complexity and require rapid policy execution.",
                "hidden_premise": "A static demonstration can be useful if the missing dynamic variables are reconstructed and stress-tested.",
                "conceptual_move": "Treat a single demonstration as a seed for dynamic manipulation rather than a complete behavior distribution.",
                "mechanism": "The official abstract positions DynamicManip as a response to data requirements and real-time variation.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper names data complexity and rapid dynamics as its two central challenges."},
                    {"trace": "[HTML headings]", "claim": "Official HTML includes DynamicManip Benchmark and Experiments sections."},
                    {"trace": "[Inference]", "claim": "APRL should ask what dynamic state is inferred from a static demo before trusting generalization."},
                ],
                "falsification": "If performance drops on unseen motion profiles, the single-demo premise is not enough.",
                "adversarial": "A benchmark can hide how much dynamic variation is supplied by simulation rather than by the method.",
                "thinking_tool": "Convert static demonstrations into explicit dynamic-state hypotheses and test those hypotheses separately.",
                "transfer_boundary": "Best for tasks with reusable object geometry; weaker for deformable or contact-rich dynamics without sensing.",
            },
            {
                "rank": 2,
                "title": "Demystifying When and Why VLAs Fail in Contact-Rich Tasks and How to Fix Them",
                "arxiv_id": "2608.01402",
                "fit": "contact-rich manipulation - VLA failure diagnosis - force and precision",
                "status": "Tier A - official arXiv abstract and HTML structure checked",
                "status_quo": "Contact-rich VLA failures are often treated as a need for force modules or regularizers.",
                "friction": "The root causes are underexplored, so fixes may target the wrong failure family.",
                "hidden_premise": "Precision and force failures should be separated before the architecture is changed.",
                "conceptual_move": "Diagnose when and why VLA policies fail in physical interaction tasks.",
                "mechanism": "The official abstract identifies precision failures and force-related failures as distinct root causes.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The authors explicitly separate failure modes in contact-rich manipulation."},
                    {"trace": "[HTML headings]", "claim": "Official HTML includes Diagnosing Failures and Experiments sections."},
                    {"trace": "[Inference]", "claim": "APRL should label contact failures by precision, force, and policy-training mismatch."},
                ],
                "falsification": "If the proposed fixes do not transfer across contact materials and tools, the diagnosis is benchmark-specific.",
                "adversarial": "Force augmentation can improve apparent contact success while hiding unsafe contact impulses.",
                "thinking_tool": "Do not add tactile or force channels until the failure family is typed.",
                "transfer_boundary": "Strong for manipulation; less direct for locomotion and navigation.",
            },
            {
                "rank": 3,
                "title": "ChainVLA: Chaining Vision-Language-Action Queries through a Unified Execution State",
                "arxiv_id": "2608.02326",
                "fit": "long-horizon manipulation - VLA memory - execution state",
                "status": "Tier A - official arXiv abstract and HTML structure checked",
                "status_quo": "Action-chunked VLAs repeatedly replan from current input.",
                "friction": "That loses the handoff between long-term task evidence and short-term motion.",
                "hidden_premise": "The policy query should carry an execution state, not only the current image and language instruction.",
                "conceptual_move": "Chain VLA queries through a unified execution state for long-horizon manipulation.",
                "mechanism": "The official abstract frames ChainVLA as preserving what earlier actions established while adapting ongoing motion.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper contrasts repeated replanning with retaining prior action knowledge."},
                    {"trace": "[HTML headings]", "claim": "Official HTML includes Method and Experiments sections."},
                    {"trace": "[Inference]", "claim": "The reusable APRL variable is cross-query state validity."},
                ],
                "falsification": "If state chaining helps only by smoothing actions and not by preserving task evidence, its conceptual gain is narrower.",
                "adversarial": "A stale execution state can propagate early mistakes unless the policy also learns when to discard it.",
                "thinking_tool": "Every action chunk should test what it established and when that state expires.",
                "transfer_boundary": "Best for long-horizon manipulation; less important for one-step tasks.",
            },
            {
                "rank": 4,
                "title": "Messages, Not Tokens: Grounded Coresets for Faithful VLM Compression",
                "arxiv_id": "2608.02134",
                "fit": "VLM compression - visual evidence - token pruning",
                "status": "Tier A - official arXiv abstract and HTML structure checked",
                "status_quo": "Visual token compression often ranks individual patches and keeps Top-K tokens.",
                "friction": "Language decoders consume collective signed attention messages, not isolated visual patches.",
                "hidden_premise": "Faithful compression should preserve the message induced by the visual population.",
                "conceptual_move": "Move the compression unit from token importance to grounded coreset messages.",
                "mechanism": "The official abstract argues that equally sized Top-K sets can distort the collective evidence used by the decoder.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper explicitly rejects isolated Top-K token scores as the evidence unit."},
                    {"trace": "[HTML headings]", "claim": "Official HTML includes Methodology, Analysis, and Experiments sections."},
                    {"trace": "[Inference]", "claim": "APRL should evaluate visual compression by action evidence preservation, not just token count."},
                ],
                "falsification": "If message preservation does not improve downstream grounding under fixed compute, the coreset unit is not operationally better.",
                "adversarial": "Grounded coresets may be query-sensitive and expensive to recompute in real-time robotics.",
                "thinking_tool": "Ask what evidence message is preserved after compression, not how many tokens remain.",
                "transfer_boundary": "Direct for VLM inference and robot VLM grounding; indirect for low-level control.",
            },
        ],
        "synthesis": [
            {
                "title": "The execution state is now the bottleneck",
                "links": "DynamicManip - ChainVLA - Demystifying VLA Failures",
                "facts": "The papers expose dynamic object state, cross-query state, and contact failure state.",
                "inference": "APRL should make an execution-state benchmark before comparing VLA backbones.",
            },
            {
                "title": "Compression and replanning need validity tests",
                "links": "Messages Not Tokens - Budgeted Replanning - ET-Prune",
                "facts": "The backlog has many papers on token, memory, and replanning budgets.",
                "inference": "Budget savings should be accepted only if the state needed for action remains valid.",
            },
        ],
        "frontier_memory": [
            {"label": "Strengthening", "history": "Late July emphasized WAM and VLA state channels.", "body": "August 4 adds contact-rich diagnosis and cross-query execution memory."},
            {"label": "New signal", "history": "Prior compression notes focused on visual token count.", "body": "Messages Not Tokens reframes compression around preserved evidence messages."},
        ],
        "strategy": [
            {
                "priority": "Build moat",
                "title": "Contact-rich execution-state benchmark",
                "thesis": "Separate precision, force, tactile, memory, and replanning failures under the same manipulation tasks.",
                "scores": {"fit": 5, "novelty": 5, "feasibility": 4, "moat": 5, "timing": 5, "evidence": 4},
                "one_week": "Annotate 30 contact-rich failures by precision, force, memory, and replanning boundary.",
                "four_week": "Run a small VLA suite with state chaining, tactile prediction, and budgeted replanning ablations.",
                "success": "At least two failure families require different fixes under matched tasks.",
                "stop": "All failures collapse to generic perception error after replay inspection.",
                "asset": "Reusable failure taxonomy and manipulation replay set.",
            }
        ],
    },
    "2026-08-05": {
        "date": "2026-08-05",
        "edition": "Research Intelligence",
        "source_prompt": SOURCE_PROMPT,
        "source_mode": "new",
        "scope_note": (
            "Daily edition from matching Wednesday /new listings: 146 non-replacement cs.CV rows, 55 cs.RO rows, "
            "190 deduplicated papers, and 161 ROI papers. Tier A cards use official arXiv abstract pages plus "
            "available official arXiv HTML headings."
        ),
        "executive_thesis": (
            "The August 5 batch turns world models, SLAM, and VLA execution into one operational question: when should "
            "an agent trust, refresh, or discard its internal state? Quo Vadis broadens world models into agent-centric "
            "feedback proxies, SLAMFormer-infinity removes a fixed distance bound from SLAM processing, Continue or Replan "
            "turns action-chunk horizons into a learned continuation decision, and DRIFT shows flow-matching VLA robustness "
            "can fail along the denoising trajectory. APRL's best move is a state-validity benchmark that couples map memory, "
            "action horizon, proprioception, and adversarial physical attention."
        ),
        "decision_cards": [
            {
                "label": "Decision",
                "title": "World models are feedback interfaces, not only future-video predictors",
                "body": "Quo Vadis reframes world proxies around actionable feedback before real actions, matching APRL's need for cheap but typed robot trials.",
            },
            {
                "label": "Decision",
                "title": "Long-range SLAM needs flexible memory coordinates",
                "body": "SLAMFormer-infinity asks the frontend and backend to process unbounded structure without anchoring everything to the first frame.",
            },
            {
                "label": "Decision",
                "title": "Execution horizons and VLA attacks are state-validity problems",
                "body": "Continue/Replan and DRIFT both show that hidden trajectory state can become stale or steerable before the final action is emitted.",
            },
        ],
        "papers": [
            {
                "rank": 1,
                "title": "Quo Vadis, World Modeling?",
                "arxiv_id": "2608.02713",
                "fit": "agent-centric world proxies - feedback interface - world-model design space",
                "status": "Tier A - official arXiv abstract and HTML structure checked",
                "status_quo": "World models are commonly treated as future physical-state predictors.",
                "friction": "Improving agents need feedback that is cheaper and safer than direct real-environment interaction.",
                "hidden_premise": "The useful proxy can be any interface that gives actionable feedback before real action, not only a predicted video.",
                "conceptual_move": "Shift from physical-state prediction to agent-centric world proxies and their functional forms.",
                "mechanism": "The official HTML headings lay out motivation, definition, empowerment, instantiations, and design-space conclusion.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper says world models offer lower-cost, controllable feedback before real actions."},
                    {"trace": "[HTML headings]", "claim": "Official HTML includes Definition and Instantiations sections for agent-centric world proxies."},
                    {"trace": "[Inference]", "claim": "APRL should classify WAMs by feedback type: image, state, critic, planner, or monitor."},
                ],
                "falsification": "If proxy feedback does not predict real-world action improvement, the broadened design space becomes taxonomy without leverage.",
                "adversarial": "A broad proxy definition can hide weak grounding unless every proxy is tied to a success and stop condition.",
                "thinking_tool": "Before building a world model, name the feedback channel and the real action it is supposed to change.",
                "transfer_boundary": "Strong for robot learning and agent evaluation; less direct for pure generative-media tasks.",
            },
            {
                "rank": 2,
                "title": "SLAMFormer-infinity: Infinite SLAM Transformer for Unbounded Frontend and Backend Processing",
                "arxiv_id": "2608.03429",
                "fit": "SLAM transformer - unbounded memory - frontend/backend geometry",
                "status": "Tier A - official arXiv abstract and HTML structure checked",
                "status_quo": "Transformer SLAM often has a bounded context or first-frame-anchored coordinate formulation.",
                "friction": "Long-range frontend and backend processing need flexible coordinate systems and memory conditions.",
                "hidden_premise": "The SLAM memory coordinate should be redefined as the sequence grows rather than fixed at frame one.",
                "conceptual_move": "Use memory conditions to define flexible coordinate systems and scales for unbounded processing.",
                "mechanism": "The abstract describes memory-conditioned frontend and backend processing without an explicit distance bound.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper claims support for long-range frontend and backend processing without an explicit distance bound."},
                    {"trace": "[HTML headings]", "claim": "Official HTML includes Methodology and Experiments sections."},
                    {"trace": "[Inference]", "claim": "APRL's map benchmark should measure when memory coordinates become stale or inconsistent."},
                ],
                "falsification": "If unbounded processing fails under loop closure, dynamic objects, or calibration drift, the memory condition is not enough.",
                "adversarial": "Transformer context can appear unbounded while computation or map update cost still grows operationally.",
                "thinking_tool": "Evaluate SLAM memory by coordinate validity and update cost, not just endpoint trajectory error.",
                "transfer_boundary": "Direct for visual SLAM and localization; less direct for sparse LiDAR-only systems.",
            },
            {
                "rank": 3,
                "title": "Continue or Replan? Bernoulli-Continuation Policy Learning for Adaptive Horizon Execution",
                "arxiv_id": "2608.03483",
                "fit": "VLA execution horizon - replanning boundary - adaptive control",
                "status": "Tier A - official arXiv abstract and HTML structure checked",
                "status_quo": "Chunk-based VLA policies often execute a fixed number of actions before replanning.",
                "friction": "A critical manipulation stage can be executed from a stale chunk if no replanning boundary arrives in time.",
                "hidden_premise": "The policy should learn whether its current chunk remains valid.",
                "conceptual_move": "Add a Bernoulli continuation decision that adaptively decides continue versus replan.",
                "mechanism": "The official abstract positions BCP as a lightweight plug-and-play adaptive horizon framework.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper names fixed execution horizons as task-agnostic periodic schedules."},
                    {"trace": "[HTML headings]", "claim": "Official HTML includes Method and Experiments sections."},
                    {"trace": "[Inference]", "claim": "APRL should ablate chunk age, continuation probability, and failure onset together."},
                ],
                "falsification": "If adaptive replanning only increases compute without improving critical-stage success, the continuation signal is weak.",
                "adversarial": "A continuation head can learn dataset rhythm rather than true task progress.",
                "thinking_tool": "Treat replanning as a learned validity test for the current action chunk.",
                "transfer_boundary": "Strong for chunk-based manipulation; less relevant for continuous MPC controllers.",
            },
            {
                "rank": 4,
                "title": "DRIFT: Derailing Denoising Trajectories of Flow-Matching VLAs with Adversarial Patch Attack",
                "arxiv_id": "2608.03207",
                "fit": "flow-matching VLA security - denoising trajectory - physical attention hijacking",
                "status": "Tier A - official arXiv abstract and HTML structure checked",
                "status_quo": "Flow-matching VLAs have been reported to resist attacks that fool autoregressive VLAs.",
                "friction": "Prior attacks can ignore the multi-step denoising ODE where action trajectories are formed.",
                "hidden_premise": "Robustness must be tested along the denoising path, not only at the final output.",
                "conceptual_move": "Attack the denoising trajectory with a universal adversarial patch on the robot's scene.",
                "mechanism": "The official abstract says DRIFT redirects the flow-matching trajectory through test-time input perturbation.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper says apparent robustness stems from attacks ignoring the multi-step denoising ODE."},
                    {"trace": "[HTML headings]", "claim": "Official HTML includes Methodology and Experiments sections."},
                    {"trace": "[Inference]", "claim": "APRL should monitor intermediate denoising states for attack or drift evidence."},
                ],
                "falsification": "If trajectory attacks fail under real camera lighting, viewpoint, and object clutter, physical transfer is limited.",
                "adversarial": "Patch attacks can overstate risk if they require unrealistic placement or visibility.",
                "thinking_tool": "Audit generative policies at every internal refinement step, not only at the emitted action.",
                "transfer_boundary": "Direct for flow-matching VLA policies; less direct for discrete action decoders.",
            },
        ],
        "synthesis": [
            {
                "title": "State validity ties world models, maps, and action chunks",
                "links": "Quo Vadis - SLAMFormer-infinity - Continue/Replan",
                "facts": "The papers each replace a fixed state assumption: physical future only, first-frame coordinate, fixed action horizon.",
                "inference": "APRL should evaluate when internal state is valid enough to act and when it must be refreshed.",
            },
            {
                "title": "Robustness must be checked before the final decision",
                "links": "DRIFT - proprioceptive VLA state - visual evidence scheduling",
                "facts": "The batch has attacks, proprioception, token pruning, and evidence-scheduling papers.",
                "inference": "Intermediate state audits are a better moat than another end-to-end success comparison.",
            },
        ],
        "frontier_memory": [
            {"label": "New signal", "history": "Prior weeks framed WAMs as future prediction.", "body": "Quo Vadis reframes them as agent feedback proxies."},
            {"label": "Strengthening", "history": "Late July tracked geometry memory and WAM state.", "body": "SLAMFormer-infinity and Continue/Replan make state-validity timing explicit."},
        ],
        "strategy": [
            {
                "priority": "Build moat",
                "title": "State-validity benchmark for robot agents",
                "thesis": "Couple map memory, action chunk age, proprioceptive history, and attack trajectory into one validity benchmark.",
                "scores": {"fit": 5, "novelty": 5, "feasibility": 4, "moat": 5, "timing": 5, "evidence": 4},
                "one_week": "Instrument one VLA rollout with chunk age, replan decision, proprioception window, map age, and denoising-step drift.",
                "four_week": "Build a small suite where stale map, stale chunk, missing proprioception, and adversarial patch are crossed.",
                "success": "The benchmark predicts failure family before final action failure in at least two stress conditions.",
                "stop": "State validity signals do not separate failure families beyond generic confidence.",
                "asset": "Robot-agent state-validity logs plus replayable stress scenarios.",
            }
        ],
    },
}


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=False)


def render_paper(paper: dict) -> str:
    evidence = "".join(
        f"<li><strong>{esc(item['trace'])}</strong><span>{esc(item['claim'])}</span></li>"
        for item in paper["evidence"]
    )
    return f"""
<article class="autopsy-card">
  <div class="paper-top"><span class="rank">#{paper['rank']}</span><span class="tier">{esc(paper['status'])}</span></div>
  <h3><a href="https://arxiv.org/abs/{esc(paper['arxiv_id'])}" target="_blank" rel="noopener">{esc(paper['title'])}</a></h3>
  <p class="fit">{esc(paper['fit'])}</p>
  <div class="field-grid">
    <div><h4>Status quo belief</h4><p>{esc(paper['status_quo'])}</p></div>
    <div><h4>Friction / anomaly</h4><p>{esc(paper['friction'])}</p></div>
    <div><h4>Hidden premise</h4><p>{esc(paper['hidden_premise'])}</p></div>
    <div><h4>Conceptual move</h4><p>{esc(paper['conceptual_move'])}</p></div>
  </div>
  <div class="evidence"><h4>Evidence trace</h4><ul>{evidence}</ul></div>
  <div class="critical-grid">
    <div><h4>Mechanism</h4><p>{esc(paper['mechanism'])}</p></div>
    <div><h4>Falsification frontier</h4><p>{esc(paper['falsification'])}</p></div>
    <div><h4>Adversarial read</h4><p>{esc(paper['adversarial'])}</p></div>
    <div class="tool"><h4>Transferable thinking tool</h4><p>{esc(paper['thinking_tool'])}</p><p>{esc(paper['transfer_boundary'])}</p></div>
  </div>
</article>
"""


def render_strategy(item: dict) -> str:
    scores = "".join(f"<span>{esc(k)} {esc(v)}</span>" for k, v in item["scores"].items())
    total = sum(int(v) for v in item["scores"].values())
    return f"""
<article class="strategy-card">
  <div class="strategy-head"><span class="priority">{esc(item['priority'])}</span><span class="total">total {total}/30</span></div>
  <h3>{esc(item['title'])}</h3><p class="thesis">{esc(item['thesis'])}</p>
  <div class="scores">{scores}</div>
  <div class="strategy-grid">
    <div><strong>1-week probe</strong><p>{esc(item['one_week'])}</p></div>
    <div><strong>4-week build</strong><p>{esc(item['four_week'])}</p></div>
    <div><strong>Success metric</strong><p>{esc(item['success'])}</p></div>
    <div><strong>Stop condition</strong><p>{esc(item['stop'])}</p></div>
  </div>
  <p class="assets"><strong>Asset path</strong> · {esc(item['asset'])}</p>
</article>
"""


def build_html(data: dict) -> str:
    decisions = "".join(
        f"<article><span>{esc(item['label'])}</span><h3>{esc(item['title'])}</h3><p>{esc(item['body'])}</p></article>"
        for item in data["decision_cards"]
    )
    papers = "".join(render_paper(paper) for paper in data["papers"])
    synthesis = "".join(
        f"<article><h3>{esc(item['title'])}</h3><p class='links'>{esc(item['links'])}</p>"
        f"<p><strong>Observed</strong> · {esc(item['facts'])}</p><p><strong>Inference</strong> · {esc(item['inference'])}</p></article>"
        for item in data["synthesis"]
    )
    memory = "".join(
        f"<article><span>{esc(item['label'])}</span><p class='history'>{esc(item['history'])}</p><p>{esc(item['body'])}</p></article>"
        for item in data["frontier_memory"]
    )
    strategy = "".join(render_strategy(item) for item in data["strategy"])
    date = data["date"]
    return f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(date)} arXiv Research Intelligence</title>
<style>
:root{{--ink:#162033;--muted:#5b677a;--line:#dce3ea;--blue:#0f4c81;--cyan:#087990;--soft:#f6f8fb}}
*{{box-sizing:border-box}}body{{margin:0;background:#f4f7fb;color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.62}}
header,main,footer{{max-width:1120px;margin:0 auto;padding:36px 40px}}header{{padding-top:52px}}.home{{display:inline-block;margin-bottom:18px;color:var(--blue);text-decoration:none;font-weight:700}}
h1{{font-size:38px;line-height:1.12;margin:0 0 10px}}h2{{font-size:24px;margin:42px 0 16px}}h3{{margin:6px 0 8px}}p{{margin:0 0 10px}}.lead{{font-size:18px;color:#304258;max-width:960px}}.scope{{padding:14px 16px;background:#fff;border-left:4px solid var(--cyan);border-radius:10px;color:#3d4c5f}}
.decision-grid,.synthesis-grid,.memory-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}.decision-grid article,.synthesis-grid article,.memory-grid article{{background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px}}.decision-grid span,.memory-grid span{{font-size:11px;font-weight:800;color:#075985;background:#e0f2fe;border-radius:999px;padding:3px 8px}}
.autopsy-card{{background:#fff;border:1px solid var(--line);border-radius:18px;padding:24px;margin:18px 0;box-shadow:0 8px 22px #1d29390a}}.paper-top{{display:flex;justify-content:space-between;gap:12px}}.rank{{font-size:26px;font-weight:900;color:#b7c4d4}}.tier{{font-size:11px;font-weight:800;background:#ecfeff;color:#075985;border-radius:999px;padding:5px 10px;align-self:center}}.fit,.links,.history{{color:var(--muted);font-size:13px}}
.field-grid,.critical-grid,.strategy-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}.field-grid>div,.critical-grid>div,.strategy-grid>div{{border:1px solid var(--line);border-radius:12px;padding:14px 16px;background:#fff}}.evidence{{background:#f8fafc;border:1px solid var(--line);border-radius:12px;padding:16px;margin:16px 0}}.evidence li{{margin:8px 0}}.evidence strong{{display:block;color:#075985;font-size:12px}}.tool{{background:#fff9e8!important;border-color:#f3ce71!important}}
.strategy-card{{background:#fff;border:1px solid var(--line);border-radius:18px;padding:22px;margin:16px 0}}.strategy-head{{display:flex;justify-content:space-between}}.priority{{font-size:11px;font-weight:900;background:#dcfce7;color:#166534;border-radius:999px;padding:5px 10px}}.scores{{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}}.scores span{{font-size:11px;background:#eef2f6;border-radius:6px;padding:4px 8px}}.assets{{background:var(--soft);padding:10px 12px;border-radius:8px}}
footer{{color:var(--muted);font-size:13px}}@media(max-width:800px){{header,main,footer{{padding-left:22px;padding-right:22px}}.decision-grid,.synthesis-grid,.memory-grid,.field-grid,.critical-grid,.strategy-grid{{grid-template-columns:1fr}}h1{{font-size:30px}}}}
</style></head><body>
<header><a class="home" href="../">← arXiv Daily Summary</a><h1>{esc(date)} arXiv Research Intelligence</h1>
<p class="lead">{esc(data['executive_thesis'])}</p><p class="scope">{esc(data['scope_note'])}</p></header>
<main>
<h2>🔭 주간 동향을 넘어: 오늘의 판단</h2><div class="decision-grid">{decisions}</div>
<h2>🧠 Paper Reasoning Autopsy</h2>{papers}
<h2>🔗 Cross-paper decision synthesis</h2><div class="synthesis-grid">{synthesis}</div>
<h2>🧭 Frontier memory</h2><div class="memory-grid">{memory}</div>
<h2>🧪 APRL Leading Group Strategy Board</h2>{strategy}
</main><footer>Source prompt: <a href="../{esc(data['source_prompt'])}">{esc(data['source_prompt'])}</a>. Structured source: <a href="../intelligence/{date}.json">intelligence/{date}.json</a>.</footer>
</body></html>
"""


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
