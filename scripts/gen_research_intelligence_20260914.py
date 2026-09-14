#!/usr/bin/env python3
"""Generate the 2026-09-14 Research Intelligence edition."""

from __future__ import annotations

import json
from pathlib import Path

from gen_research_intelligence_20260811 import build_html


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PROMPT = "prompts/instruction_v20260713.md"


RI_BY_DATE = {
    "2026-09-14": {
        "date": "2026-09-14",
        "edition": "Research Intelligence",
        "source_prompt": SOURCE_PROMPT,
        "source_mode": "new",
        "scope_note": (
            "Daily edition from matching Monday /new listings: 90 non-replacement cs.CV rows, "
            "59 cs.RO rows, 142 deduplicated papers, and 115 ROI papers. Tier A cards are "
            "conservative abstract-only autopsies from the repository parser output; no figure, "
            "table, full-text, code, or dataset-release claim is asserted unless the abstract itself states it."
        ),
        "executive_thesis": (
            "The September 14 batch turns robot intelligence into an evidence-interface problem. "
            "VLA and manipulation papers do not merely ask for more demonstrations; they ask which visual, "
            "geometric, tactile, material, or planner-generated signal is allowed to condition the next action. "
            "Geometry papers move from standalone reconstruction toward scan relocalization, multi-session map reuse, "
            "room-object assignment, and low-altitude LIO sensitivity. Driving and aerial papers expose risk as an explicit "
            "field, criticality score, battery envelope, comfort bound, or communication window. World-model and video papers "
            "then attack the assumption that memory, generated rollouts, or compact tokens are faithful just because they look "
            "coherent. APRL's opportunity is to own the interface tests that decide when a map, memory, world model, or modality "
            "may change a robot action."
        ),
        "decision_cards": [
            {
                "label": "Decision",
                "title": "Robot actions need scoped evidence interfaces",
                "body": (
                    "LIT, MoPA, DATAFARM, Dynin-Robotics, and VLA serving papers all isolate the path by which perception, "
                    "planner data, or runtime serving actually conditions action generation."
                ),
            },
            {
                "label": "Decision",
                "title": "Physical state is replacing generic demonstrations",
                "body": (
                    "STAR, RodForesight, material-conditioned diffusion, force-guided CoM estimation, and safe grasping papers "
                    "treat tactile sparsity, rod deformation, material identity, tipping margin, and fragility as first-class state."
                ),
            },
            {
                "label": "Decision",
                "title": "Maps and memories must prove functional use",
                "body": (
                    "DRS-VPT, Chain-SLAM, AnchorVLN, IMPLY, VideoTok4D, and pixel-decoding audits ask whether geometry or memory "
                    "survives the downstream decision, not whether it can be reconstructed prettily."
                ),
            },
        ],
        "papers": [
            {
                "rank": 1,
                "title": "Breaking the Vision-Action Shortcut: Latent Interface Training for Generalizable Robotics Foundation Models",
                "arxiv_id": "2609.12641",
                "fit": "VLA generalization - latent action interface - visual shortcut control",
                "status": "Tier A - abstract-only",
                "status_quo": "Robot foundation models can learn action correlations from pretrained visual features and look strong in distribution.",
                "friction": "The abstract says task-irrelevant visual cues can correlate with demonstrated actions and then break under visual distribution shift.",
                "hidden_premise": "A policy should only receive visual information through an interface that preserves task-relevant spatial goals for action generation.",
                "conceptual_move": "Train an image-free spatial-goal action prior first, then constrain visual conditioning through a pose-supervised latent interface.",
                "mechanism": "LIT conditions action chunks on language, robot state, and terminal SE(3) pose, then makes the latent interface reconstruct that pose as the only visual pathway.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper evaluates LIT across Pi0.5, MolmoAct2, FAST-WAM, and ImageWAM."},
                    {"trace": "[Abstract]", "claim": "It reports 3.87-10.70 percentage-point LIBERO-Plus gains and 13.30-16.70 point real-world gains under unseen camera, lighting, and distractor shifts."},
                    {"trace": "[Inference]", "claim": "APRL should test whether a latent interface prevents shortcuts by attacking camera, lighting, and distractor correlations separately."},
                ],
                "falsification": "If the interface still tracks nuisance visual changes more than terminal-pose-relevant state, shortcut mitigation is incomplete.",
                "adversarial": "Hold action priors fixed and perturb camera pose, background, distractor objects, and language goals independently.",
                "thinking_tool": "Do not let the visual encoder talk to the action head until the interface names the spatial variable it carries.",
                "transfer_boundary": "Strong for manipulation VLAs; weaker for tasks where the action-relevant latent is not expressible as a compact spatial goal.",
            },
            {
                "rank": 2,
                "title": "MoPA: Coordinated Mobile Manipulation via Subsystem-Specific Perception Alignment",
                "arxiv_id": "2609.12081",
                "fit": "mobile manipulation - subsystem-specific perception - coupled action generation",
                "status": "Tier A - abstract-only",
                "status_quo": "Mobile manipulation policies often share a single visual representation while base and arm actions need different spatial evidence.",
                "friction": "The abstract argues that heterogeneous action branches leave perception-action correspondence implicit.",
                "hidden_premise": "Base motion and arm control should use different perceptual query streams while remaining coordinated at the action level.",
                "conceptual_move": "Split perceptual conditioning into mobility and manipulation streams, then coordinate the generated action chunks with coupled flow matching.",
                "mechanism": "Dual masked query banks and layerwise Perception2Action adaptation feed subsystem action streams inside a structured Mixture-of-Transformers decoder.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "MoPA reports state-of-the-art results across all three ManiSkill-HAB task suites."},
                    {"trace": "[Abstract]", "claim": "Across four real-world tasks, it reports 76.3 percent mean full-task success, 12.5 points above the best baseline."},
                    {"trace": "[Inference]", "claim": "APRL should evaluate whether different spatial scales change base and arm actions in recoverable ways."},
                ],
                "falsification": "If the separated perception streams collapse to the same cues, the gain may come from decoder capacity rather than subsystem alignment.",
                "adversarial": "Swap navigation-scale obstacles and manipulation-scale object details independently while measuring base-arm coordination failures.",
                "thinking_tool": "A mobile manipulator needs evidence routing by actuator subsystem, not a single pooled scene embedding.",
                "transfer_boundary": "Direct for mobile manipulation; less direct for fixed-base arms without coupled base motion.",
            },
            {
                "rank": 3,
                "title": "DATAFARM: Distribution-Aligned Task and Motion Planning for Fine-Tuning Vision-Language-Action Models",
                "arxiv_id": "2609.12316",
                "fit": "VLA fine-tuning data - TAMP demonstrations - distribution alignment",
                "status": "Tier A - abstract-only",
                "status_quo": "Task and motion planning can solve target robot tasks and seems like a cheap demonstration generator.",
                "friction": "The abstract says raw TAMP trajectories give surprisingly little fine-tuning benefit despite solving the tasks.",
                "hidden_premise": "Synthetic or planned demonstrations help a pretrained VLA only when their robot joint, style, and timing statistics resemble the pretraining distribution.",
                "conceptual_move": "Make the planner generate demonstrations that are distribution-aligned to the pretrained VLA rather than merely task-valid.",
                "mechanism": "DATAFARM incorporates pretraining-distribution constraints into TAMP trajectory generation across joint configuration, motion style, and temporal execution.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "DATAFARM reports 56.7 percent average success versus 8.3 percent for raw TAMP and 61.7 percent for human teleoperation."},
                    {"trace": "[Abstract]", "claim": "On deformable manipulation outside the fine-tuning distribution, the model retains 85 percent success versus 90 percent pretrained."},
                    {"trace": "[Inference]", "claim": "APRL should score generated robot data by pretraining-distribution compatibility, not only task success."},
                ],
                "falsification": "If aligned trajectories help only tasks where TAMP already matches human style, the method may not generalize to novel contact regimes.",
                "adversarial": "Generate task-valid trajectories with deliberately shifted joint poses, timing, and motion smoothness, then measure fine-tuning damage.",
                "thinking_tool": "A demonstration is training data only after it is behaviorally legible to the pretrained policy.",
                "transfer_boundary": "Strong for manipulation fine-tuning with planner access; weaker where no planner can express the target behavior.",
            },
            {
                "rank": 4,
                "title": "STAR: Sparse Tactile Representation Learning in Vision-Tactile-Language-Action Models for Dexterous Manipulation",
                "arxiv_id": "2609.12549",
                "fit": "dexterous manipulation - sparse tactile tokens - VTLA post-training",
                "status": "Tier A - abstract-only",
                "status_quo": "Dexterous manipulation systems often lean on vision and demonstrations while tactile signals are sparse and hard to represent.",
                "friction": "The abstract points to limited real-world data and sparse tactile representation as the central bottlenecks.",
                "hidden_premise": "Sparse touch can improve dexterity if it is represented as a global, predictive signal rather than a dense image-like stream.",
                "conceptual_move": "Build a VTLA training recipe that treats tactile sparsity spatially, temporally, and informationally.",
                "mechanism": "STAR combines visual-tactile joint pretraining, sparse-global tactile token representation, and sparse future tactile prediction on a bimanual dataset.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The dataset has 200 hours, 10,576 trajectories, 65 tasks, and 69.5 percent dexterous multi-finger manipulation."},
                    {"trace": "[Abstract]", "claim": "STAR reports 61 percent average success across four real-world tasks with 100 post-training trajectories per task."},
                    {"trace": "[Inference]", "claim": "APRL should test whether sparse tactile prediction changes contact recovery before terminal success changes."},
                ],
                "falsification": "If tactile tokens help only task-specific post-training and not unseen contact states, they are data augmentation rather than reusable contact structure.",
                "adversarial": "Mask tactile bursts, change object compliance, and alter contact timing while measuring recovery and slip before failure.",
                "thinking_tool": "Touch should be evaluated by what future contact state it predicts, not by how dense the sensor stream is.",
                "transfer_boundary": "Strong for bimanual dexterity; weaker for tasks where tactile sensing is unavailable or not action-limiting.",
            },
            {
                "rank": 5,
                "title": "DRS-VPT: Directly Relocalizing in a Scan with Vision Point Transformers",
                "arxiv_id": "2609.12557",
                "fit": "image-to-scan registration - relocalization - 3D point maps",
                "status": "Tier A - abstract-only",
                "status_quo": "Camera-LiDAR calibration and indoor relocalization are often treated as separate tasks with map-specific optimization.",
                "friction": "The abstract targets a unified feed-forward image-to-scan registration formulation that transfers across environments.",
                "hidden_premise": "A relocalization model is foundational only if it predicts pose and point-map structure in a common geometric frame.",
                "conceptual_move": "Predict scan pose, camera poses, point maps, and coarse-to-fine alignment features directly from query images plus a reference scan.",
                "mechanism": "DRS-VPT expresses outputs in the first camera frame and learns direct reprojective scan-to-image alignment features.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The same model targets camera-LiDAR calibration and indoor camera-to-map relocalization."},
                    {"trace": "[Abstract]", "claim": "It reports state-of-the-art autonomous-driving image-to-LiDAR registration, competitive indoor relocalization, and zero-shot transfer."},
                    {"trace": "[Inference]", "claim": "APRL should evaluate relocalization by pose recovery and point-map consistency under sparse views and occlusion."},
                ],
                "falsification": "If zero-shot transfer fails when geometry is repetitive or dynamic objects occlude key points, it is not yet a general scan interface.",
                "adversarial": "Stress low-overlap, repeated-corridor, moving-object, and calibration-offset cases while measuring pose and map-point failure.",
                "thinking_tool": "Treat image-to-scan relocalization as a reusable geometric interface for multiple robot stacks.",
                "transfer_boundary": "Strong for scanned indoor and driving environments; weaker when no reliable reference point cloud exists.",
            },
            {
                "rank": 6,
                "title": "Chain-SLAM: Globally Consistent Backend for Multi-Session LiDAR SLAM via Chained Loop Closure",
                "arxiv_id": "2609.12221",
                "fit": "multi-session LiDAR SLAM - map reuse - chained loop closure",
                "status": "Tier A - abstract-only",
                "status_quo": "Large-scale LiDAR maps drift when separate sessions are merged over long spatial and temporal horizons.",
                "friction": "The abstract says multi-session map alignment needs global consistency while operating online across loaded maps and new trajectories.",
                "hidden_premise": "Short-horizon reliable loop closures can propagate enough constraints to keep long-horizon map reuse consistent.",
                "conceptual_move": "Use chained loop closures through an adjacency graph to align sessions inside one factor graph.",
                "mechanism": "GNSS-proximity place recognition initializes inter-session alignment, then on-the-fly loop closure and joint optimization maintain inter- and intra-session consistency.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "Chain-SLAM is described as an online backend for multi-session map alignment and reuse."},
                    {"trace": "[Abstract]", "claim": "It reports improved trajectory accuracy and robust multi-session integration on large-scale datasets."},
                    {"trace": "[Inference]", "claim": "APRL should ask when a reused map is allowed to constrain a new trajectory."},
                ],
                "falsification": "If a wrong short-horizon loop closure propagates globally without detection, chained consistency can amplify rather than repair error.",
                "adversarial": "Inject near-place aliasing, seasonal changes, and dynamic-object clutter while tracking map reuse, factor residuals, and localization drift.",
                "thinking_tool": "A map reuse event is a decision that needs a local evidence threshold and a global damage monitor.",
                "transfer_boundary": "Strong for LiDAR mapping fleets; weaker for single-session or purely visual navigation setups.",
            },
            {
                "rank": 7,
                "title": "IMPLY: Physically Anchored Consistency for World-Model Rollouts",
                "arxiv_id": "2609.12441",
                "fit": "world-action models - physical consistency - rollout evidence anchoring",
                "status": "Tier A - abstract-only",
                "status_quo": "World-model rollout checks often reward futures that agree with each other.",
                "friction": "The abstract argues self-consistency can give a perfect score to a model that ignores the object and predicts a typical push.",
                "hidden_premise": "Consistency is meaningful only when rollouts agree on the physical object identified by calibration evidence.",
                "conceptual_move": "Invert a simulator to read the mass and friction implied by multiple rollouts, then anchor agreement to calibration pushes.",
                "mechanism": "IMPLY scores rollout sets by whether one object explains all futures, rather than whether futures merely resemble each other.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "Anchoring exposes an object-ignoring model where self-consistency fails, with AUROC 0.70 versus 1.00 in the controlled setting."},
                    {"trace": "[Abstract]", "claim": "On V-JEPA 2-AC, anchored disagreement prefers the right evidence on 73 percent of objects and correlates 0.92-0.99 with rollout error."},
                    {"trace": "[Inference]", "claim": "APRL should anchor generated futures to object-level physical evidence before using them for action choice."},
                ],
                "falsification": "If simulator inversion fails under contact-rich real objects, physical anchoring may become brittle outside controlled pushing.",
                "adversarial": "Vary object mass, friction, contact geometry, and calibration-push coverage while comparing self-consistency to action outcome.",
                "thinking_tool": "A coherent future is not useful unless it is coherent about the right physical object.",
                "transfer_boundary": "Strong for push-like world-action models; weaker for dynamics without an invertible physical proxy.",
            },
            {
                "rank": 8,
                "title": "Does Video Memory Use What It Retrieves? A Causal Audit of Memory Specificity",
                "arxiv_id": "2609.12090",
                "fit": "video memory - causal substitution - memory specificity",
                "status": "Tier A - abstract-only",
                "status_quo": "Memory-enabled video models are often evaluated by whether memory improves output quality.",
                "friction": "The abstract says standard ablations do not test whether the retrieved content is actually responsible for the gain.",
                "hidden_premise": "A memory module should be trusted only if replacing consumed memory changes the result in content-specific ways.",
                "conceptual_move": "Use read-time memory substitution while keeping the rest of computation unchanged to separate memory benefit from memory specificity.",
                "mechanism": "The audit swaps consumed memory values and measures whether gains come from generic representation repair, broad context, or exact episodic content.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "Identity-free controls recover essentially the full benefit on Ego-Exo4D and 7-Scenes and about 70 percent on TUM."},
                    {"trace": "[Abstract]", "claim": "SAM 2 shows strong content dependence, with DAVIS score dropping from 0.926 to 0.182 under valid wrong memory."},
                    {"trace": "[Inference]", "claim": "APRL should audit robot memory by substitution before assuming retrieved context is causal."},
                ],
                "falsification": "If robot memory substitutions are confounded with distribution shift, the audit may overstate or understate true causal memory use.",
                "adversarial": "Swap same-episode, wrong-episode, identity-free, and physically impossible memories while measuring action changes and failure onset.",
                "thinking_tool": "Ask whether memory content caused the action, not whether memory helped the benchmark.",
                "transfer_boundary": "Strong for video and memory-augmented agents; needs action-level adaptation for closed-loop robot policies.",
            },
            {
                "rank": 9,
                "title": "Scenario-Independent Criticality Assessment and Prediction for Vulnerable Road Users in Autonomous Driving",
                "arxiv_id": "2609.11947",
                "fit": "autonomous driving safety - VRU criticality - scenario-independent prediction",
                "status": "Tier A - abstract-only",
                "status_quo": "Driving criticality metrics are often scenario-specific and centered on vehicle-to-vehicle interaction.",
                "friction": "The abstract says vulnerable road users require special treatment because their motion behavior is less predictable.",
                "hidden_premise": "A safety metric should separate critical and non-critical objects across participant classes without handcrafting a scenario-specific rule.",
                "conceptual_move": "Define a VRU-centric criticality metric and a scenario-independent prediction framework for all traffic participant classes.",
                "mechanism": "The method incorporates object type, velocity, and criticality factors and evaluates them on diverse DeepAccident scenarios.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The VRU-centric metric improves pedestrian criticality classification by up to 50 percent."},
                    {"trace": "[Abstract]", "claim": "The prediction framework reports F1-score 0.96 and 275 percent improvement over state-of-the-art metrics."},
                    {"trace": "[Inference]", "claim": "APRL should use criticality as an action-relevance gate rather than an after-the-fact risk label."},
                ],
                "falsification": "If metric rankings fail under rare VRU maneuvers or sensor occlusion, scenario independence is weaker than reported.",
                "adversarial": "Stress children, cyclists, occluded pedestrians, and sudden acceleration while measuring whether criticality predicts planner intervention.",
                "thinking_tool": "Risk metrics should identify which object gets control authority next.",
                "transfer_boundary": "Direct for autonomous driving; transferable to mobile robots if object-specific motion unpredictability is represented.",
            },
            {
                "rank": 10,
                "title": "Pixel Decodability Is Not a Compression Signal: Causally Evaluating Importance Proxies for Visual KV-Cache Eviction",
                "arxiv_id": "2609.13012",
                "fit": "visual KV cache - causal importance proxy - compression negative result",
                "status": "Tier A - abstract-only",
                "status_quo": "It is tempting to evict visual cache units based on how much pixel content they preserve.",
                "friction": "The abstract reports that pixel-decodable retention is task-inert in the tested setting.",
                "hidden_premise": "Compression should preserve units the answer causally relies on, not units that reconstruct the input well.",
                "conceptual_move": "Separate pixel retention from causal use with pixel inversion, KV ablation, teacher-forced log-probability drop, and preregistered tests.",
                "mechanism": "The paper compares retention, attention, and utilization within images under a sign-calibrated held-out design.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "Retention never positively tracks causal utilization across the preregistered tests, while attention weakly but significantly tracks it."},
                    {"trace": "[Abstract]", "claim": "At super-patch granularity, retention ranks KV eviction no better than random in this setting."},
                    {"trace": "[Inference]", "claim": "APRL should treat visual cache pruning as a causal evidence problem before using it on robot agents."},
                ],
                "falsification": "If different architectures or action-conditioned VLMs make pixel decodability causal, the negative result may be scope-limited.",
                "adversarial": "Test cache eviction under rare-object, spatial-relation, and action-choice queries where preserved pixels may become functional.",
                "thinking_tool": "A representation is compressible only after causal-use tests, not reconstruction probes.",
                "transfer_boundary": "Strong warning for VLM compression; embodied transfer needs action-level cache-ablation experiments.",
            },
        ],
        "synthesis": [
            {
                "title": "Action conditioning is being narrowed to auditable interfaces",
                "links": "LIT - MoPA - DATAFARM - Dynin-Robotics - VLA serving",
                "facts": "The abstracts separately constrain visual conditioning, split base and arm evidence, align planner demonstrations, and expose VLA serving constraints.",
                "inference": "The shared decision is to make the interface that changes the action inspectable before trusting scale, data, or model capacity.",
            },
            {
                "title": "Physical state is the new robustness variable",
                "links": "STAR - RodForesight - Material-conditioned diffusion - CoM tipping - Chain-SLAM",
                "facts": "The batch names tactile sparsity, rod bending, material identity, tipping margin, and map reuse consistency as explicit state variables.",
                "inference": "APRL should move from demonstration count to contact, material, force, and map-state variables that predict recovery before success changes.",
            },
            {
                "title": "Memory and generation need causal use tests",
                "links": "Video memory audit - IMPLY - VideoTok4D - PhysPlan - Pixel KV audit",
                "facts": "The papers attack memory specificity, physically anchored rollout consistency, 4D token structure, physics-aware generation, and cache-utilization proxies.",
                "inference": "A memory, token, or generated future should be used only after a substitution or intervention test shows that it carries decision-relevant evidence.",
            },
        ],
        "frontier_memory": [
            {
                "label": "Strengthening",
                "history": "September 11 emphasized transition accountability across VLA, geometry, safety, and efficient multimodal agents.",
                "body": "September 14 strengthens that line with explicit latent interfaces, subsystem perception streams, planner-data alignment, and causal cache/memory audits.",
            },
            {
                "label": "New signal",
                "history": "Recent geometry notes focused on 3DGS relocalization, radar depth, and degraded sensing.",
                "body": "Today adds map governance: direct image-to-scan registration, chained multi-session SLAM, room-object closure, and LIO parameter sensitivity.",
            },
            {
                "label": "Commoditizing",
                "history": "World-model language has appeared repeatedly in VLA, video generation, simulation, and planning.",
                "body": "The useful distinction is no longer whether a model predicts futures, but whether rollouts are physically anchored, causally memory-specific, and action-controllable.",
            },
            {
                "label": "Contradiction",
                "history": "More retained visual content or more planner-generated data can look like a straightforward improvement path.",
                "body": "Pixel retention is a poor KV-eviction proxy in the tested setting, and raw TAMP demonstrations can underperform unless distribution-aligned.",
            },
            {
                "label": "Missing axis",
                "history": "The repo has separate evaluation threads for robot maps, VLA actions, and multimodal compression.",
                "body": "A single interface benchmark should ask whether the same evidence packet changes localization, action generation, cache eviction, and safety intervention.",
            },
        ],
        "strategy": [
            {
                "priority": "Build moat",
                "portfolio": "Build moat",
                "title": "Evidence-interface benchmark for VLA and mobile manipulation",
                "thesis": "Build a suite where visual latents, subsystem perception streams, planner demonstrations, tactile tokens, and material estimates must prove which action variable they condition.",
                "scores": {"strategic_fit": 5, "asymmetry": 5, "timing": 5, "tractability": 4, "defensibility": 5, "scientific_depth": 5},
                "one_week": "Run a small LIBERO/RoboCasa and mobile-manipulation probe with camera shifts, distractors, base-arm conflicts, raw TAMP data, and distribution-aligned TAMP data.",
                "one_week_probe": "Run a small LIBERO/RoboCasa and mobile-manipulation probe with camera shifts, distractors, base-arm conflicts, raw TAMP data, and distribution-aligned TAMP data.",
                "four_week": "Add latent-interface probes, subsystem evidence masks, tactile/contact streams, material labels, and planner-data style metrics across tabletop and mobile tasks.",
                "four_week_build": "Add latent-interface probes, subsystem evidence masks, tactile/contact streams, material labels, and planner-data style metrics across tabletop and mobile tasks.",
                "success": "Interface-specific scores predict OOD action success, recovery, slip, and base-arm coordination better than terminal success or imitation loss alone.",
                "success_metric": "Interface-specific scores predict OOD action success, recovery, slip, and base-arm coordination better than terminal success or imitation loss alone.",
                "stop": "Stop if interface probes do not change policy choice, failure prediction, or intervention timing beyond ordinary success-rate ranking.",
                "stop_condition": "Stop if interface probes do not change policy choice, failure prediction, or intervention timing beyond ordinary success-rate ranking.",
                "paper_path": "Auditable evidence interfaces for generalizable robot foundation models.",
                "asset_path": "Camera-shift episodes, subsystem masks, planner-style descriptors, tactile traces, material labels, and recovery annotations.",
                "asset": "Camera-shift episodes, subsystem masks, planner-style descriptors, tactile traces, material labels, and recovery annotations.",
            },
            {
                "priority": "Exploit",
                "portfolio": "Exploit",
                "title": "Map-governance protocol for reusable robot geometry",
                "thesis": "Evaluate when a scan, SLAM session, room-object graph, or low-altitude LIO estimate is allowed to constrain localization and planning.",
                "scores": {"strategic_fit": 5, "asymmetry": 4, "timing": 5, "tractability": 4, "defensibility": 5, "scientific_depth": 5},
                "one_week": "Collect a small indoor scan and mobile-robot sequence with repeated corridors, room-object boundaries, low-overlap scans, and changed objects.",
                "one_week_probe": "Collect a small indoor scan and mobile-robot sequence with repeated corridors, room-object boundaries, low-overlap scans, and changed objects.",
                "four_week": "Compare DRS-style image-to-scan registration, chained loop closure, ProClosure-style room assignment, and LIO parameter sweeps under map reuse.",
                "four_week_build": "Compare DRS-style image-to-scan registration, chained loop closure, ProClosure-style room assignment, and LIO parameter sweeps under map reuse.",
                "success": "A map-governance score predicts wrong-room retrieval, relocalization failure, loop-closure damage, and navigation recovery under map changes.",
                "success_metric": "A map-governance score predicts wrong-room retrieval, relocalization failure, loop-closure damage, and navigation recovery under map changes.",
                "stop": "Stop if map scores improve pose error only offline and do not alter object retrieval, navigation, or recovery decisions.",
                "stop_condition": "Stop if map scores improve pose error only offline and do not alter object retrieval, navigation, or recovery decisions.",
                "paper_path": "Robot map reuse as an evidence-governed decision rather than passive memory.",
                "asset_path": "Multi-session scans, room-object labels, loop-closure traces, LIO sweeps, and downstream task outcomes.",
                "asset": "Multi-session scans, room-object labels, loop-closure traces, LIO sweeps, and downstream task outcomes.",
            },
            {
                "priority": "Explore",
                "portfolio": "Explore",
                "title": "Causal memory and rollout permission tests",
                "thesis": "Unify video-memory substitution, physically anchored rollout checks, 4D token interventions, and visual KV ablations into a robot-agent evidence test.",
                "scores": {"strategic_fit": 4, "asymmetry": 5, "timing": 5, "tractability": 3, "defensibility": 4, "scientific_depth": 5},
                "one_week": "Prototype memory swaps and rollout-anchor checks on a small pushing or tabletop world-model setup plus long-video robot QA traces.",
                "one_week_probe": "Prototype memory swaps and rollout-anchor checks on a small pushing or tabletop world-model setup plus long-video robot QA traces.",
                "four_week": "Add physical calibration pushes, 4D token perturbations, cache-ablation probes, and action-choice evaluation in generated and real episodes.",
                "four_week_build": "Add physical calibration pushes, 4D token perturbations, cache-ablation probes, and action-choice evaluation in generated and real episodes.",
                "success": "Permission tests identify memories, rollouts, or cache units whose removal changes action choice or failure prediction before terminal failure.",
                "success_metric": "Permission tests identify memories, rollouts, or cache units whose removal changes action choice or failure prediction before terminal failure.",
                "stop": "Stop if substitution and anchoring tests rank evidence the same as reconstruction, attention, or visual-quality proxies.",
                "stop_condition": "Stop if substitution and anchoring tests rank evidence the same as reconstruction, attention, or visual-quality proxies.",
                "paper_path": "Causal evidence tests for memory- and world-model-guided robot agents.",
                "asset_path": "Memory-substitution traces, calibration pushes, rollout physics scores, KV ablation logs, and action-change labels.",
                "asset": "Memory-substitution traces, calibration pushes, rollout physics scores, KV ablation logs, and action-change labels.",
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
