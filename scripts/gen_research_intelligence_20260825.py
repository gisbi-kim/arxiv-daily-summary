#!/usr/bin/env python3
"""Generate the 2026-08-25 Research Intelligence edition."""

from __future__ import annotations

import json
from pathlib import Path

from gen_research_intelligence_20260811 import build_html


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PROMPT = "prompts/instruction_v20260713.md"


RI_BY_DATE = {
    "2026-08-25": {
        "date": "2026-08-25",
        "edition": "Research Intelligence",
        "source_prompt": SOURCE_PROMPT,
        "source_mode": "new",
        "scope_note": (
            "Daily edition from matching Tuesday /new listings: 234 non-replacement cs.CV rows, "
            "92 cs.RO rows, 307 deduplicated papers, and 254 ROI papers. Tier A cards are "
            "conservative abstract-only autopsies from the repository parser output; no figure, "
            "table, full-text, code, or dataset-release claims are asserted."
        ),
        "executive_thesis": (
            "The August 25 batch makes robot and multimodal systems answer a harder question: "
            "what evidence is allowed to change an action, a map, a memory, or a generated future? "
            "VLA papers expose prompt authority, typed spatial readouts, event-gated memory, intent "
            "distillation, and modality masking as explicit control interfaces. Geometry and SLAM "
            "papers ask when a map can remain localizable, updatable, private, or semantically stable. "
            "World-action and driving papers move away from video fidelity toward future state, "
            "view-invariant action coordinates, risk objects, and behavior-aware simulators. The "
            "APRL move is to own evaluation episodes where the evidence variable must be named before "
            "the policy, planner, mapper, or VLM answer is trusted."
        ),
        "decision_cards": [
            {
                "label": "Decision",
                "title": "VLA control now needs an authority boundary",
                "body": (
                    "TOWN-VLA, Pointing-VLA, UniMem, INDI, modality masking, and CounterAlign all "
                    "ask which prompt, spatial target, memory update, intent label, modality, or "
                    "negative action evidence is permitted to alter the executed action."
                ),
            },
            {
                "label": "Decision",
                "title": "Maps are becoming evidence-managed robot state",
                "body": (
                    "AquaFlow, SuperMap, Spotter, GeoWAM, robust global SfM, and M3ISR treat "
                    "geometry as a state whose pose, semantics, privacy, dynamic update, and "
                    "compression behavior must remain inspectable."
                ),
            },
            {
                "label": "Decision",
                "title": "Reasoning budgets are routed before expensive perception",
                "body": (
                    "GapSight, long-video RAG, acoustic triage, FOVEA, VIG, and GuardianBench shift "
                    "evaluation from final answer quality toward whether the system acquired the "
                    "right local, temporal, audio, or risk evidence before answering."
                ),
            },
        ],
        "papers": [
            {
                "rank": 1,
                "title": "Think Only When Needed: Prompt-Authority Control for Selective Slow-Path Intervention in Vision-Language-Action Manipulation",
                "arxiv_id": "2608.23224",
                "fit": "VLA manipulation - prompt authority - selective intervention",
                "status": "Tier A - abstract-only",
                "status_quo": "Retrieval-augmented VLA work often treats retrieved text as harmless context once it improves language-side reasoning.",
                "friction": "The abstract reports that raw appended text can collapse VLA execution, so prompt form itself becomes a control intervention.",
                "hidden_premise": "A deployed VLA should preserve its base prompt unless an explicit compatibility rule authorizes a canonical replacement.",
                "conceptual_move": "Separate slow-path candidate generation from permission to alter the executed policy input.",
                "mechanism": "The abstract describes a prompt-authority interface that authorizes a compact canonical instruction or restores the original Base prompt.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper identifies prompt-form collapse when appended text enters a frozen VLA policy."},
                    {"trace": "[Abstract]", "claim": "It frames retrieved text as a control intervention requiring an authorization contract."},
                    {"trace": "[Inference]", "claim": "APRL should test retrieval, memory, and tool text by action delta, not only semantic helpfulness."},
                ],
                "falsification": "If the compatibility rule only restores base behavior on easy tasks and cannot authorize genuinely useful corrections, it is a guardrail rather than a reasoning interface.",
                "adversarial": "Use meaningful, irrelevant, adversarial, and length-matched prompts under identical visual states to separate semantic benefit from prompt-form disturbance.",
                "thinking_tool": "Treat every text injection into a robot policy as an actuator with an authority boundary.",
                "transfer_boundary": "Direct for VLA manipulation and retrieval-augmented policies; weaker for modular stacks where language never touches the low-level controller.",
            },
            {
                "rank": 2,
                "title": "Pointing-VLA: Typed Spatial Grounding Interfaces for Vision-Language-Action Manipulation",
                "arxiv_id": "2608.23138",
                "fit": "VLA manipulation - typed spatial readout - execution contract",
                "status": "Tier A - abstract-only",
                "status_quo": "Spatial grounding in VLA policies is often exposed through text coordinates or opaque action tokens.",
                "friction": "The abstract argues that serializing geometry as language creates brittle interfaces between multimodal reasoning and execution.",
                "hidden_premise": "Different manipulation stages need different spatial targets, so one generic grounding channel is under-specified.",
                "conceptual_move": "Use typed hidden-state spatial readouts for points, object-functional grounding heatmaps, and visual trajectories.",
                "mechanism": "The abstract assigns PICK to source-conditioned object-functional grounding and PLACE to pointing, turning geometry into a stage-aligned contract.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper proposes geometry-specific heads rather than text-serialized coordinates."},
                    {"trace": "[Abstract]", "claim": "It reports physical pick-place deployments and a collision-enabled CuRobo execution setting."},
                    {"trace": "[Inference]", "claim": "APRL should evaluate whether typed spatial outputs reduce stage-specific failures."},
                ],
                "falsification": "If typed heads improve benchmark averages but fail when PICK and PLACE require different occlusion or contact evidence, the interface is not stage-aligned enough.",
                "adversarial": "Swap target-source ambiguity, distractor affordances, occlusion, and collision constraints to see which head changes the action incorrectly.",
                "thinking_tool": "Do not ask one representation to carry all spatial intent; type the interface by execution stage.",
                "transfer_boundary": "Strong for pick-place and mobile manipulation; less direct for navigation policies whose spatial targets are already explicit waypoints.",
            },
            {
                "rank": 3,
                "title": "UniMem: Unifying Multimodal Memory and Control for Vision-Language-Action Models",
                "arxiv_id": "2608.22869",
                "fit": "VLA memory - event-gated keyframes - non-Markovian control",
                "status": "Tier A - abstract-only",
                "status_quo": "Long-horizon VLA memory is often bolted on as an external VLM memory manager or a fixed historical-frame window.",
                "friction": "The abstract says arbitrary fixed-interval frames can degrade performance and external VLM memory creates a fractured pipeline.",
                "hidden_premise": "A useful robot memory should update only at events that preserve action-relevant state while staying inside the control backbone.",
                "conceptual_move": "Unify high-level multimodal memory and low-level control with event classification, keyframe encoding, and cached spatial memory.",
                "mechanism": "The abstract describes event-triggered memory updates, keyframe encoding, and keyframe caching to retain dense spatial information.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper identifies non-Markovian tasks as a failure case for current VLA policies."},
                    {"trace": "[Abstract]", "claim": "It argues that fixed historical-frame selection can hurt rather than help."},
                    {"trace": "[Inference]", "claim": "APRL should score memory by whether event choice predicts future action correction."},
                ],
                "falsification": "If event-gated memory helps only on scripted long-horizon tasks but not under distractor events or changed subgoal order, the memory trigger is too narrow.",
                "adversarial": "Insert visually salient but task-irrelevant events, delayed object moves, and repeated subgoals to test whether memory updates are action-relevant.",
                "thinking_tool": "Memory should be evaluated as an update policy, not as a larger context window.",
                "transfer_boundary": "Direct for non-Markovian manipulation; weaker for one-step reaching or tasks whose state is fully observable at execution time.",
            },
            {
                "rank": 4,
                "title": "AquaFlow: A Monocular Gaussian Splatting SLAM for Underwater Streaming Reconstruction",
                "arxiv_id": "2608.22906",
                "fit": "underwater SLAM - Gaussian streaming reconstruction - degraded visual media",
                "status": "Tier A - abstract-only",
                "status_quo": "Streaming 3DGS reconstruction methods often assume visual conditions where pose tracking and scene geometry remain photometrically reliable.",
                "friction": "The abstract names light attenuation and scattering as causes of pose degradation and distorted underwater scene geometry.",
                "hidden_premise": "A robot-usable underwater map needs media-aware pose and pointmap estimates before Gaussian initialization can be trusted.",
                "conceptual_move": "Adapt a 3D vision foundation model to underwater data and use medium-guided incremental Gaussian initialization for streaming mapping.",
                "mechanism": "The abstract describes robust pose and pointmap estimation, medium-guided initialization, and a hybrid structured plus disordered scene representation.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper identifies underwater optical degradation as a tracking and geometry failure source."},
                    {"trace": "[Abstract]", "claim": "It proposes a monocular Gaussian Splatting streaming reconstruction framework for underwater scenes."},
                    {"trace": "[Inference]", "claim": "APRL should judge map quality by localization recovery under optical degradation, not just rendering fidelity."},
                ],
                "falsification": "If reconstructions look better but relocalization, loop closure, or navigation recovery do not improve under turbidity, the mapping state is not robot-usable.",
                "adversarial": "Vary scattering, lighting, moving fauna, textureless seabed, and viewpoint gaps while measuring pose drift and downstream route recovery.",
                "thinking_tool": "Treat the sensing medium as a map-state variable rather than an image pre-processing nuisance.",
                "transfer_boundary": "Strong for underwater inspection and degraded-vision SLAM; less direct for clean indoor RGB-D mapping.",
            },
            {
                "rank": 5,
                "title": "SuperMap: A Spatio-Temporal SLAM System for Visual-Language Navigation",
                "arxiv_id": "2608.22896",
                "fit": "semantic SLAM - long-term object identity - visual-language navigation",
                "status": "Tier A - abstract-only",
                "status_quo": "Open-vocabulary perception is often fused into maps as if labels were stable observations of persistent objects.",
                "friction": "The abstract says foundation-model predictions are intermittent and view-dependent, causing identity drift and stale semantics in mapping pipelines.",
                "hidden_premise": "Language-guided navigation needs a map that can reactivate object identities and prune outdated content as the environment changes.",
                "conceptual_move": "Combine high-frequency geometric SLAM with asynchronous open-vocabulary perception and confidence-managed 4D object memory.",
                "mechanism": "The abstract names 3D-aware instance association, reactivation, and existence-label confidence updates for a queryable spatio-temporal scene graph.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper frames stale semantics and identity drift as map-level failures."},
                    {"trace": "[Abstract]", "claim": "It proposes consistency-driven mapping for stable object identity and pruning under occlusion or scene change."},
                    {"trace": "[Inference]", "claim": "APRL should evaluate semantic maps by query success after object disappearance, reappearance, and label flips."},
                ],
                "falsification": "If confidence updates preserve stale objects under real rearrangement, the map may improve language retrieval while hurting navigation.",
                "adversarial": "Move, hide, rename, and replace objects across revisits while measuring object identity, query routing, and navigation success.",
                "thinking_tool": "A semantic map must have object existence and label confidence with explicit decay and reactivation rules.",
                "transfer_boundary": "Strong for long-term indoor navigation; less direct for short static episodes or metric-only localization.",
            },
            {
                "rank": 6,
                "title": "GeoWAM: Visual Geometry World Action Models for Autonomous Driving",
                "arxiv_id": "2608.23486",
                "fit": "driving WAM - point-cloud state - action-aligned world model",
                "status": "Tier A - abstract-only",
                "status_quo": "Driving world-action models often use pixel future prediction as the shared state for scene dynamics and ego action.",
                "friction": "The abstract argues pixels entangle geometry and motion with texture and illumination, leaving driving actions only indirectly represented.",
                "hidden_premise": "Driving actions live in geometric space, so the world model should predict a state representation aligned with that space.",
                "conceptual_move": "Move WAM state from visual frames toward point-cloud geometry that directly encodes rigid and non-rigid transformations.",
                "mechanism": "The abstract frames point clouds as a more natural dynamics state for future evolution and ego-trajectory prediction.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper identifies pixel-space dynamics as an indirect representation for driving."},
                    {"trace": "[Abstract]", "claim": "It proposes geometry, represented by point clouds, as the WAM state space."},
                    {"trace": "[Inference]", "claim": "APRL should compare pixel-WAM and geometry-WAM failures on action-changing scene dynamics."},
                ],
                "falsification": "If point-cloud state improves geometry metrics but not object-risk localization or ego-trajectory recovery, the state is not action-aligned enough.",
                "adversarial": "Stress illumination, texture, articulated traffic participants, occluded risks, and long-range depth sparsity while measuring action change.",
                "thinking_tool": "Choose the world-model state by the coordinate system where the action is executed.",
                "transfer_boundary": "Direct for driving and mobile robots; less direct for image-editing world models without executable actions.",
            },
            {
                "rank": 7,
                "title": "Learning to Look Again: Loss-Gap Supervision for Free-form Crop Routing in Vision-Language Models",
                "arxiv_id": "2608.21762",
                "fit": "VLM evidence routing - selective crop review - model-specific failure signal",
                "status": "Tier A - abstract-only",
                "status_quo": "VLM detail failures are often addressed by allocating more visual tokens globally or by using fixed crops.",
                "friction": "The abstract says the answer can be visible but lost after compression into a low-resolution global view, while more tokens can waste compute or hurt global-context tasks.",
                "hidden_premise": "A re-reading policy should be supervised by whether a crop reduces the target model's own answer loss.",
                "conceptual_move": "Turn local visual evidence acquisition into a free-form crop-routing decision learned from global-versus-crop loss gaps.",
                "mechanism": "The abstract describes comparing answer loss or option margin under global-only and crop-augmented views, then distilling useful crops into a lightweight router.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper frames many detail-centric errors as evidence loss during visual compression."},
                    {"trace": "[Abstract]", "claim": "It uses the target VLM's own loss gap to label useful crop reviews."},
                    {"trace": "[Inference]", "claim": "APRL should route expensive visual perception only when the missing evidence can change a downstream action."},
                ],
                "falsification": "If loss-gap crops improve VQA but fail to predict manipulation, inspection, or navigation decisions, the router remains answer-centric.",
                "adversarial": "Use small signs, grasp-relevant contact regions, occluded defects, and distractor crops where local evidence conflicts with global context.",
                "thinking_tool": "Budget perception by the marginal decision value of looking again.",
                "transfer_boundary": "Strong for VLM inspection and detail-centric embodied prompts; weaker for sensors where the bottleneck is temporal or tactile, not image resolution.",
            },
            {
                "rank": 8,
                "title": "GuardianBench: A Same-Scene Instruction-Contrastive Benchmark for Latent Contextual Risk in Embodied AI",
                "arxiv_id": "2608.21928",
                "fit": "embodied safety - instruction contrast - latent contextual risk",
                "status": "Tier A - abstract-only",
                "status_quo": "Embodied safety benchmarks often vary scenes or dynamics, allowing models to rely on scene-level risk priors.",
                "friction": "The abstract says a safe scene and a benign instruction can become hazardous only in composition, and models show instruction-insensitive verdicts.",
                "hidden_premise": "A safety benchmark should fix the scene and vary only the instruction to isolate whether the model understands contextual risk.",
                "conceptual_move": "Use same-scene Safe/Unsafe instruction pairs grounded in safety standards to test latent risk sensitivity.",
                "mechanism": "The abstract describes 3,024 instruction-scene examples and a rationale audit that localizes instruction-insensitive failure modes.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The benchmark uses same-scene Safe/Unsafe contrastive pairs across hazard categories."},
                    {"trace": "[Abstract]", "claim": "The abstract reports low pair accuracy caused by approving both instructions under a fixed scene."},
                    {"trace": "[Inference]", "claim": "APRL should evaluate robot safety by instruction-conditioned permission, not by scene risk alone."},
                ],
                "falsification": "If models improve by memorizing benchmark hazard wording rather than changing action permission, the benchmark will not transfer to robots.",
                "adversarial": "Hold scene constant while swapping instructions that differ only in user role, timing, tool affordance, or irreversible consequence.",
                "thinking_tool": "Safety is a composition of instruction, scene, capability, and consequence; holding one fixed reveals shortcut approval.",
                "transfer_boundary": "Strong for embodied VLM safety and task permission; weaker for low-level collision avoidance without language goals.",
            },
        ],
        "synthesis": [
            {
                "title": "VLA papers are exposing who may change the action",
                "links": "TOWN-VLA - Pointing-VLA - UniMem - INDI - M3 - CounterAlign",
                "facts": "The selected abstracts expose prompt compatibility, typed spatial heads, event memory updates, distilled intent, modality masking, and counterfactual negative supervision.",
                "inference": "A VLA benchmark should report which authority changed the motor command and which stress condition invalidates that authority.",
            },
            {
                "title": "Geometry papers are moving from reconstruction artifacts to map governance",
                "links": "AquaFlow - SuperMap - Spotter - robust global SfM - M3ISR - RoboShape",
                "facts": "The batch repeatedly names degraded media, stale semantics, GPS drift, view-graph outliers, controlled camera geometry, and privacy leakage as map-state problems.",
                "inference": "APRL should score maps by localizability, update correctness, privacy leakage, and downstream task recovery rather than by visual quality alone.",
            },
            {
                "title": "Reasoning systems are budgeting evidence before answering",
                "links": "GapSight - DAGC long-video RAG - acoustic triage - FOVEA - VIG - GuardianBench",
                "facts": "The papers route crops, temporal chunks, audio windows, focused visual evidence, compressed reasoning tokens, and same-scene instruction contrasts.",
                "inference": "Embodied VLM evaluation should ask when additional evidence was purchased, whether it changed the decision, and when the system should abstain.",
            },
        ],
        "frontier_memory": [
            {
                "label": "Strengthening",
                "history": "August 21 and August 24 emphasized action authorization, robot-facing geometry, runtime evidence routes, and world-action risk.",
                "body": "August 25 strengthens the same axis with prompt authority, typed spatial readouts, event-gated memory, geometry WAMs, and evidence-routed perception budgets.",
            },
            {
                "label": "New signal",
                "history": "Recent daily artifacts treated VLA memory and retrieval mostly as helpful context providers.",
                "body": "Today makes the authority boundary sharper: text, memory, spatial heads, and intent labels are not context until they have permission to change the action.",
            },
            {
                "label": "Commoditizing",
                "history": "The repo has repeatedly seen new world-model, VLM, and 3DGS variants.",
                "body": "The crowded axis is model form. The defensible axis is a measurable evidence contract: action delta, localizability, update validity, risk-object identity, or crop value.",
            },
            {
                "label": "Missing axis",
                "history": "Prior reports still lack one shared suite that joins VLA prompt authority, semantic map aging, and evidence-budgeted VLM perception.",
                "body": "APRL can own episodes where a wrong prompt, stale object, hidden risk, or missing crop causes the same downstream action to fail.",
            },
        ],
        "strategy": [
            {
                "priority": "Build moat",
                "title": "VLA authority-boundary benchmark",
                "thesis": "Measure when prompt text, memory updates, spatial readouts, intent labels, and modality masking are allowed to change a VLA action.",
                "scores": {"fit": 5, "novelty": 5, "feasibility": 4, "moat": 5, "timing": 5, "evidence": 5},
                "one_week": "Create twenty replay states across bimanual pick-place, long-horizon manipulation, and instruction-ambiguous tasks with controlled text, memory, spatial, and modality interventions.",
                "four_week": "Compare Base VLA, prompt-authority gating, typed spatial heads, event-gated memory, intent distillation, and modality masking under the same closed-loop episodes.",
                "success": "The benchmark predicts action divergence, discontinuity, or task failure before terminal success changes.",
                "stop": "If all interventions rank methods the same as ordinary success rate, reduce the suite to the single strongest failure family.",
                "asset": "Prompt intervention pairs, memory-event labels, typed spatial targets, modality masks, action-delta traces, and failure-family annotations.",
            },
            {
                "priority": "Build moat",
                "title": "Robot-usable map governance suite",
                "thesis": "Evaluate maps by when they should update, forget, hide, relocalize, or expose semantics for a downstream robot task.",
                "scores": {"fit": 5, "novelty": 4, "feasibility": 4, "moat": 5, "timing": 5, "evidence": 5},
                "one_week": "Assemble degraded underwater clips, indoor object-revisit scenes, GPS-degraded facades, and privacy-sensitive point clouds with named map-state perturbations.",
                "four_week": "Compare 3DGS SLAM, semantic 4D maps, facade localization, SfM pruning, and privacy encoders under localization, navigation, and information-leakage metrics.",
                "success": "A map-governance variable changes method ranking relative to rendering quality or ordinary pose error.",
                "stop": "If governance labels do not predict downstream task recovery, split mapping and privacy tracks before scaling data collection.",
                "asset": "Map update and decay labels, object identity timelines, localization recovery cases, privacy leakage probes, and robot-usable geometry scores.",
            },
            {
                "priority": "Explore",
                "title": "Evidence-budgeted embodied VLM evaluator",
                "thesis": "Force VLM agents to decide whether a crop, temporal chunk, audio cue, focused visual evidence path, or same-scene instruction contrast is worth paying for.",
                "scores": {"fit": 4, "novelty": 5, "feasibility": 4, "moat": 4, "timing": 5, "evidence": 4},
                "one_week": "Create inspection and navigation prompts with small defects, hidden signs, long-video evidence, audio pre-cues, and same-scene safe versus unsafe instructions.",
                "four_week": "Compare direct VLM answers, crop routing, temporal graph retrieval, audio-first triage, focused speculative decoding, and abstention policies.",
                "success": "Evidence purchase improves decision accuracy only in cases where the added evidence changes action permission or hazard assessment.",
                "stop": "If routing decisions correlate only with image size, video length, or token count, replace learned routers with a cheaper uncertainty baseline.",
                "asset": "Evidence-cost annotations, crop and temporal mappings, audio triage labels, same-scene risk pairs, and action-permission outcomes.",
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
