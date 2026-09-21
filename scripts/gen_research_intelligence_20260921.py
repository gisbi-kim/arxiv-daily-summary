#!/usr/bin/env python3
"""Generate the 2026-09-21 Research Intelligence edition."""

from __future__ import annotations

import json
from pathlib import Path

from gen_research_intelligence_20260811 import build_html


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PROMPT = "prompts/instruction_v20260713.md"


RI_BY_DATE = {
    "2026-09-21": {
        "date": "2026-09-21",
        "edition": "Research Intelligence",
        "source_prompt": SOURCE_PROMPT,
        "source_mode": "new",
        "scope_note": (
            "Daily edition from matching Monday /new listings: 98 non-replacement cs.CV rows, "
            "114 cs.RO rows, 197 deduplicated papers, and 166 ROI papers. Tier A cards are "
            "conservative abstract-only autopsies from repository parser output; no figure, "
            "table, full-text, code, or dataset-release claim is asserted unless the abstract "
            "itself states it."
        ),
        "executive_thesis": (
            "The September 21 batch turns robot intelligence into a question of evidence timing. "
            "VLA papers such as VLA-Scope, SafeStage, ProTracer, and CommitFlow ask not merely "
            "whether a policy succeeds, but when a shift, unsafe stage, proprioceptive deviation, "
            "or semantic commitment first becomes visible. Contact papers including ME-Dex, "
            "ForeTac-VLA, ZeroTouch, PSR, and ForceTwin make the same move for physical interaction: "
            "touch, force, future contact, and human-instrumented dynamics become state variables "
            "that must predict failure before vision catches it. Geometry papers including "
            "Cube-Splat, 2D GauSS-MI, SFVO, VideoReloc, Noctif3R, and adaptive world-memory 3D "
            "models push reconstruction toward online evidence budgets under panoramic, active-view, "
            "low-light, semantic-memory, and confidence-guided odometry constraints. Social navigation "
            "and recovery papers then add the deployment question: DPed-VLN, PopNavShift, PIVOT, RAYA, "
            "LIMBO, and ASGARD ask when the robot should slow down, ask, intervene, or preserve control "
            "authority instead of simply continuing the nominal plan. APRL's opening is to own "
            "benchmarks where every module exposes the earliest observable evidence that changes "
            "a robot decision."
        ),
        "decision_cards": [
            {
                "label": "Decision",
                "title": "Failures are becoming timed evidence, not terminal labels",
                "body": (
                    "VLA-Scope, SafeStage, ProTracer, CommitFlow, Outcome-Conditioned End-Effector "
                    "Geometry, and When Should a Failing Robot Ask? all split failure into onset, "
                    "stage, evidence source, commitment, and dialogue timing."
                ),
            },
            {
                "label": "Decision",
                "title": "Contact state is being promoted into world-model state",
                "body": (
                    "ME-Dex, ForeTac-VLA, ZeroTouch, PSR, ForceTwin, and Robotic Multiphase Interaction "
                    "treat tactile, force, hidden physical property, and liquid-solid dynamics as "
                    "predictive state rather than after-the-fact feedback."
                ),
            },
            {
                "label": "Decision",
                "title": "Maps and world models now need action-facing evidence budgets",
                "body": (
                    "Cube-Splat, 2D GauSS-MI, SFVO, VideoReloc, Noctif3R, MT-WAM, WM-VS, and ZYT-World "
                    "all ask what evidence is worth spending compute on before pose, view, simulation, "
                    "or servo decisions are trusted."
                ),
            },
        ],
        "papers": [
            {
                "rank": 1,
                "title": "VLA-Scope: Shift-Aware Failure Prediction for Vision-Language-Action Models",
                "arxiv_id": "2609.21246",
                "fit": "VLA reliability - distribution shift - failure prediction",
                "status": "Tier A - abstract-only",
                "status_quo": "VLA robustness is often tested by detecting out-of-distribution inputs or reporting final task success.",
                "friction": "A shifted input can still succeed, and an in-distribution input can still fail, so OOD detection alone is not a useful robot stop signal.",
                "hidden_premise": "The useful quantity is not whether the observation is shifted, but whether that shift changes execution risk.",
                "conceptual_move": "Turn shift detection into shift-aware failure prediction for closed-loop VLA execution.",
                "mechanism": "The abstract frames OOD detection as insufficient and introduces a failure-prediction model for VLA policies under distribution shift.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper states that VLA models may still succeed under OOD conditions, making OOD detection alone insufficient."},
                    {"trace": "[Abstract]", "claim": "The target is execution failure prediction rather than generic shift detection."},
                    {"trace": "[Inference]", "claim": "APRL should evaluate shift monitors by intervention precision and missed recoverable failures."},
                ],
                "falsification": "If predicted shift risk does not improve intervention timing over calibrated policy confidence, the extra shift model is not operationally useful.",
                "adversarial": "Test benign visual shifts, task-critical geometric shifts, and contact-state shifts separately; a single OOD score can mix them.",
                "thinking_tool": "Convert dataset shift into an action-specific failure forecast.",
                "transfer_boundary": "Strong for VLA manipulation and driving policies; weaker for modular stacks that already expose explicit state uncertainty.",
            },
            {
                "rank": 2,
                "title": "SafeStage: Evaluating Safety Before, During, and After Vision-Language-Conditioned Robot Manipulation",
                "arxiv_id": "2609.21223",
                "fit": "staged manipulation safety - VLA evaluation - closed-loop diagnosis",
                "status": "Tier A - abstract-only",
                "status_quo": "Robot safety evaluation often compresses a rollout into task success, refusal, constraint violation, or physical damage.",
                "friction": "A manipulation episode can become unsafe before the terminal failure appears, and different stages need different safety evidence.",
                "hidden_premise": "Safety is stage-local: perception, language grounding, approach, contact, and completion can each fail in a distinct way.",
                "conceptual_move": "Evaluate safety before, during, and after vision-language-conditioned manipulation rather than after the whole rollout.",
                "mechanism": "The abstract positions the benchmark as diagnosing where safety fails during closed-loop manipulation.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "Existing evaluations are described as insufficient for locating where safety fails."},
                    {"trace": "[Abstract]", "claim": "The framework separates safety assessment across rollout phases."},
                    {"trace": "[Inference]", "claim": "APRL should attach a stage label and recovery option to every manipulation failure."},
                ],
                "falsification": "If stage labels do not predict which recovery policy helps, they remain descriptive rather than control-relevant.",
                "adversarial": "Probe whether semantic refusal, physical constraints, and contact damage disagree under ambiguous instructions.",
                "thinking_tool": "Make safety a temporal trace with phase-specific stop conditions.",
                "transfer_boundary": "Direct for manipulation; less direct for navigation unless route phases are similarly defined.",
            },
            {
                "rank": 3,
                "title": "ProTracer: Proprioception-Guided Failure Diagnosis in Robot Manipulation",
                "arxiv_id": "2609.21369",
                "fit": "proprioceptive failure diagnosis - onset localization - robot manipulation",
                "status": "Tier A - abstract-only",
                "status_quo": "Failure analysis for manipulation often stops at binary success/failure or a coarse failure category.",
                "friction": "Useful recovery requires knowing the earliest moment the trajectory deviated, not only the final visible symptom.",
                "hidden_premise": "Proprioceptive traces can expose failure onset earlier than external visual inspection for many manipulation tasks.",
                "conceptual_move": "Add failure onset localization and explanation generation to robot manipulation diagnosis.",
                "mechanism": "The abstract says the framework covers failure detection, categorization, explanation generation, and onset localization.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper explicitly targets the earliest moment a robot execution deviates from a valid trajectory."},
                    {"trace": "[Abstract]", "claim": "The diagnosis is guided by proprioception."},
                    {"trace": "[Inference]", "claim": "APRL should log proprioceptive onset against visual and tactile onset to choose recovery sensors."},
                ],
                "falsification": "If onset localization trails visual or tactile cues in contact-heavy tasks, proprioception alone is insufficient.",
                "adversarial": "Stress soft contacts, tool use, and payload changes where proprioception and visual evidence disagree.",
                "thinking_tool": "Score diagnosis by the first recoverable deviation, not the final failure label.",
                "transfer_boundary": "Strong for manipulators with rich joint/force traces; weaker for underinstrumented platforms.",
            },
            {
                "rank": 4,
                "title": "ME-Dex 1.0: Bringing Heterogeneous Tactile Sensing into World Action Modeling",
                "arxiv_id": "2609.21449",
                "fit": "tactile world action modeling - future tactile state - heterogeneous sensors",
                "status": "Tier A - abstract-only",
                "status_quo": "World action models are usually built around visual future prediction and action generation.",
                "friction": "Contact-rich manipulation depends on physical interaction states that may not be visible in RGB video.",
                "hidden_premise": "Tactile signals should be modeled as evolving world state, not merely as conditioning features.",
                "conceptual_move": "Bring heterogeneous tactile sensing into world action modeling through joint tactile, visual, and action prediction.",
                "mechanism": "The abstract says tactile sensing complements video with direct physical-interaction measurements and should be predicted jointly with future observations and actions.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "Existing tactile-enhanced methods are described as using tactile features without jointly predicting future tactile states."},
                    {"trace": "[Abstract]", "claim": "The key insight is to treat tactile signals like video observations of the evolving world state."},
                    {"trace": "[Inference]", "claim": "APRL should require contact world models to forecast tactile failure precursors, not only video frames."},
                ],
                "falsification": "If tactile prediction improves reconstruction metrics without changing action success or recovery timing, it is not yet a control variable.",
                "adversarial": "Evaluate across sensor types, object materials, and unseen contact geometries to separate tactile semantics from sensor overfitting.",
                "thinking_tool": "Make touch a predicted state variable in the action model.",
                "transfer_boundary": "Strong for dexterous/contact-rich manipulation; weaker for tasks with no contact sensing at deployment.",
            },
            {
                "rank": 5,
                "title": "ForeTac-VLA: A Forecasting-Based Tactile-Vision-Language-Action Model for Contact-Rich Robotic Manipulation",
                "arxiv_id": "2609.20980",
                "fit": "forecasting tactile VLA - contact-rich manipulation - hidden interaction state",
                "status": "Tier A - abstract-only",
                "status_quo": "VLA models often rely on visual observations even when the decisive physical state is hidden from sight.",
                "friction": "Contact-rich states such as incipient slip, compression, or force direction may be visually ambiguous until the task has already failed.",
                "hidden_premise": "Forecasting future tactile state can give the policy a pre-contact or early-contact warning signal.",
                "conceptual_move": "Use tactile forecasting inside a tactile-vision-language-action model rather than merely reacting to observed touch.",
                "mechanism": "The abstract highlights forecasting for contact-rich manipulation where visual perception alone is not robust.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper states that visual reliance limits robustness in contact-rich environments."},
                    {"trace": "[Abstract]", "claim": "The method is forecasting-based and tactile-vision-language-action."},
                    {"trace": "[Inference]", "claim": "APRL should compare observed tactile feedback with forecasted tactile risk as separate policy inputs."},
                ],
                "falsification": "If forecasts are only accurate after contact failure has begun, they cannot prevent failure.",
                "adversarial": "Test transparent objects, high-friction surfaces, and deformable objects where visual and tactile priors conflict.",
                "thinking_tool": "Use predicted touch as an early warning channel for action selection.",
                "transfer_boundary": "Direct for tactile VLA systems; less direct for vision-only robots unless ZeroTouch-style visual contact estimation is available.",
            },
            {
                "rank": 6,
                "title": "Cube-Splat: High-Fidelity 360° Gaussian Splatting SLAM via Cubemap Factorization and Adjoint-Consistent Optimization",
                "arxiv_id": "2609.21347",
                "fit": "panoramic GS-SLAM - cubemap factorization - pose optimization",
                "status": "Tier A - abstract-only",
                "status_quo": "Dense GS-SLAM has largely been designed for pinhole camera assumptions rather than panoramic observations.",
                "friction": "A 360-degree frame contains multi-face observations that can improve constraints, but naive factorization can make pose optimization inconsistent.",
                "hidden_premise": "Panoramic SLAM needs a pose-state contract that lets all faces contribute coherent gradients to one robot pose.",
                "conceptual_move": "Factorize each 360-degree frame into cubemap views that share one optical center and aggregate gradients through adjoint mapping.",
                "mechanism": "The abstract describes front-face primary pose state, multi-face gradient accumulation, and adjoint-consistent optimization.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The method is presented as a panoramic GS-SLAM framework rather than a pinhole adaptation."},
                    {"trace": "[Abstract]", "claim": "It uses a cubemap of fixed-orientation virtual pinhole views sharing a single optical center."},
                    {"trace": "[Inference]", "claim": "APRL should test panoramic map updates by downstream relocalization and collision checking, not only rendering quality."},
                ],
                "falsification": "If cubemap consistency holds only for static, texture-rich indoor scenes, robot deployment claims remain narrow.",
                "adversarial": "Stress motion blur, moving people, reflective surfaces, and turns where face boundaries carry important geometry.",
                "thinking_tool": "Treat each camera model as an optimization contract for robot pose authority.",
                "transfer_boundary": "Strong for panoramic navigation and inspection; less direct for narrow-FOV manipulation cameras.",
            },
            {
                "rank": 7,
                "title": "2D GauSS-MI: Efficient Active Scene Reconstruction with Balanced Visual and Geometric Quality",
                "arxiv_id": "2609.21516",
                "fit": "active reconstruction - view selection - 2D Gaussian mapping",
                "status": "Tier A - abstract-only",
                "status_quo": "Active reconstruction often optimizes view choice for quality while treating onboard compute as a secondary constraint.",
                "friction": "A robot must choose the next view under limited computation while balancing visual fidelity and geometric completeness.",
                "hidden_premise": "View selection is a resource allocation decision, not just an information gain maximization step.",
                "conceptual_move": "Build an active 2DGS reconstruction framework with a mutual-information criterion balancing visual and geometric quality.",
                "mechanism": "The abstract names efficient online 2DGS mapping and probabilistic view selection for real-time active reconstruction.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "Existing methods face challenges balancing visual/geometric quality with real-time computational efficiency."},
                    {"trace": "[Abstract]", "claim": "The proposed system uses an efficient online 2DGS mapping pipeline for incremental RGB-D observations."},
                    {"trace": "[Inference]", "claim": "APRL should compare active views by task-relevant geometry gained per compute budget."},
                ],
                "falsification": "If selected views improve reconstruction metrics but not manipulation or navigation decisions, the balance is not robot-facing.",
                "adversarial": "Evaluate under occluded affordances, specular objects, and moving distractors where visual and geometric gains diverge.",
                "thinking_tool": "Score next-best-view by the decision evidence it buys.",
                "transfer_boundary": "Strong for mobile manipulation and mapping; weaker for offline reconstruction without action cost.",
            },
            {
                "rank": 8,
                "title": "DPed-VLN: A Benchmark for Socially Compliant Vision-and-Language Navigation in Dynamic Pedestrian Environments",
                "arxiv_id": "2609.21504",
                "fit": "dynamic-pedestrian VLN - social constraints - navigation benchmark",
                "status": "Tier A - abstract-only",
                "status_quo": "VLN benchmarks often assume static indoor scenes and evaluate efficiency or final success.",
                "friction": "Human-populated environments require language grounding while respecting moving pedestrians and social safety constraints.",
                "hidden_premise": "A route is not valid unless it remains socially compliant under dynamic pedestrian responses.",
                "conceptual_move": "Construct a dynamic-pedestrian VLN benchmark with paired instructions, ORCA-controlled humanoids, expert social paths, and social metrics.",
                "mechanism": "The abstract reports 33,093 navigation episodes and metrics for both navigation efficiency and social compliance.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The benchmark couples global and prior-augmented instructions with dynamic pedestrian environments."},
                    {"trace": "[Abstract]", "claim": "It evaluates social-safety constraints together with navigation behavior."},
                    {"trace": "[Inference]", "claim": "APRL should treat pedestrian behavior distribution as a navigation stress split."},
                ],
                "falsification": "If policies optimize social metrics in simulation but fail with real pedestrian reactions, the benchmark needs population-shift validation.",
                "adversarial": "Pair with PopNavShift-style behavioral populations to test whether social compliance survives different pedestrian personalities.",
                "thinking_tool": "Navigation success must include the social dynamics it induces.",
                "transfer_boundary": "Strong for indoor social navigation; less direct for isolated warehouse routes without human interaction.",
            },
            {
                "rank": 9,
                "title": "RAYA: Learning Where and When to Intervene for Robot Recovery",
                "arxiv_id": "2609.21690",
                "fit": "robot recovery - intervention timing - control authority",
                "status": "Tier A - abstract-only",
                "status_quo": "Safety mechanisms often react after a failure predictor raises an alarm or veto a nominal action late in the loop.",
                "friction": "By the time the robot predicts failure, the nominal plan may already have spent the control authority needed for recovery.",
                "hidden_premise": "Recoverability must influence action choice before the state becomes unrecoverable.",
                "conceptual_move": "Learn where and when to intervene so recovery is planned into the controller rather than appended afterward.",
                "mechanism": "The abstract frames both failure prevention and recoverability as decisions inside the controller.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper states that a robot can predict failure and still be unable to prevent it."},
                    {"trace": "[Abstract]", "claim": "Recoverability must inform actions while they are chosen rather than vetoing them afterward."},
                    {"trace": "[Inference]", "claim": "APRL should measure the remaining control authority at each warning time."},
                ],
                "falsification": "If interventions reduce failures only by becoming overly conservative, recovery timing is not yet separated from avoidance.",
                "adversarial": "Test delayed warnings, high-speed dynamics, and conflicting task priorities where intervention has opportunity cost.",
                "thinking_tool": "Ask whether a warning still leaves enough authority to recover.",
                "transfer_boundary": "Strong for mobile robots and dynamic manipulation; weaker for tasks with easy stop-and-reset options.",
            },
            {
                "rank": 10,
                "title": "When Should a Failing Robot Ask? Initiating Corrective Human-Robot Dialogue from Audited Sensor Evidence",
                "arxiv_id": "2609.21942",
                "fit": "human-robot dialogue - failure evidence audit - corrective assistance",
                "status": "Tier A - abstract-only",
                "status_quo": "Corrective dialogue is often triggered by a generic failure detector or a low-confidence answer.",
                "friction": "A robot must decide whether its own sensors reveal enough cause evidence, whether another sensor should be consulted, or whether a person should be interrupted.",
                "hidden_premise": "Asking a human is an evidence-allocation decision, not a default fallback.",
                "conceptual_move": "Use audited sensor evidence and injected true failure causes to decide when corrective dialogue should begin.",
                "mechanism": "The abstract describes a simulated benchmark where true causes are known and each sensor's diagnostic value can be measured.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The first decision is whether to act on its own diagnosis, consult another sensor, or interrupt a person."},
                    {"trace": "[Abstract]", "claim": "The benchmark injects true causes so sensor evidence can be audited."},
                    {"trace": "[Inference]", "claim": "APRL should measure human interruption by evidence value and recovery benefit, not only user preference."},
                ],
                "falsification": "If the ask policy depends on simulated cause labels that are unavailable in real tasks, transfer needs real diagnostic uncertainty calibration.",
                "adversarial": "Test when the best sensor evidence is misleading or when human correction arrives late.",
                "thinking_tool": "Treat dialogue as a costly diagnostic action.",
                "transfer_boundary": "Strong for collaborative manipulation and service robots; less direct for fully autonomous safety-critical systems where asking is impossible.",
            },
        ],
        "synthesis": [
            {
                "title": "Failure timing is becoming the central evaluation variable",
                "links": "VLA-Scope - SafeStage - ProTracer - CommitFlow - RAYA",
                "facts": "The papers separately predict failure under shift, localize safety stages, find proprioceptive onset, verify semantic commitments, and intervene before recovery authority is gone.",
                "inference": "APRL should build a shared failure-timing log with onset, warning, intervention, and irrecoverability timestamps.",
            },
            {
                "title": "Contact papers are turning hidden physics into forecast state",
                "links": "ME-Dex - ForeTac-VLA - ZeroTouch - PSR - ForceTwin - RMI",
                "facts": "The batch predicts tactile state, estimates visual contact deformation, models force and articulated properties, and includes liquid-solid manipulation dynamics.",
                "inference": "A contact benchmark should ask which physical variable becomes known before vision can explain the failure.",
            },
            {
                "title": "Geometry and world models are being judged by useful evidence per budget",
                "links": "2D GauSS-MI - SFVO - VideoReloc - Noctif3R - MT-WAM - WM-VS - ZYT-World",
                "facts": "The papers allocate active views, confidence-guided correspondence, adaptive video clips, photon-limited compute, action-oriented representation, and low-latency simulation.",
                "inference": "The common decision is how much evidence the robot buys before committing pose, map, servo, or simulated rollout decisions.",
            },
        ],
        "frontier_memory": [
            {
                "label": "Strengthening",
                "history": "The September 18 edition emphasized evidence gates for maps, navigation, tactile correction, safety filters, and deployment compression.",
                "body": "September 21 strengthens that axis but shifts from authority gates to evidence timing: onset, forecast, active view, recovery authority, and asking decisions dominate the corpus.",
            },
            {
                "label": "New signal",
                "history": "Recent releases had VLA safety and geometry trust signals, but less emphasis on human/social intervention timing.",
                "body": "DPed-VLN, PopNavShift, Visual Proactivity, and When Should a Failing Robot Ask? make human behavior and interruption timing part of the same robot evidence contract.",
            },
            {
                "label": "Commoditizing",
                "history": "World action models, 3DGS, VLA adaptation, and tactile-augmented policies now appear in nearly every batch.",
                "body": "The differentiator is no longer adding a world model, Gaussian map, or tactile input; it is whether the module exposes a measurable decision variable before failure.",
            },
            {
                "label": "Contradiction",
                "history": "End-to-end VLA progress often implies that richer foundation models can subsume diagnosis.",
                "body": "SafeStage, ProTracer, RAYA, and When Should a Failing Robot Ask? argue for explicit diagnosis, staged safety, recovery timing, and sensor-evidence audits around those policies.",
            },
            {
                "label": "Missing axis",
                "history": "The repo has separate signals for contact, navigation, mapping, safety, social behavior, and deployment.",
                "body": "A unified early-evidence benchmark is still missing: one suite should compare which modality first predicts an avoidable failure across map, touch, language, human, and control traces.",
            },
        ],
        "strategy": [
            {
                "priority": "Build moat",
                "title": "Early-evidence robot failure benchmark",
                "thesis": "Build an APRL benchmark where every episode logs the first observable cue, first useful warning, intervention point, and irrecoverability boundary.",
                "scores": {"strategic_fit": 5, "asymmetry": 5, "timing": 5, "tractability": 4, "defensibility": 5, "scientific_depth": 5},
                "one_week": "Instrument one manipulation and one navigation task with VLA-Scope-style shift risk, ProTracer-style proprioceptive onset, and RAYA-style recovery authority labels.",
                "four_week": "Add tactile forecast, active-view reconstruction, social-navigation pedestrian shift, and ask-human decisions into a shared evidence-timing schema.",
                "success": "At least three evidence channels predict avoidable failure earlier than terminal success/failure while preserving task progress.",
                "stop": "Stop if early signals only correlate with generic confidence and do not change recovery, asking, or intervention decisions.",
                "paper_path": "Benchmark paper on early evidence timing for robot failure prediction, intervention, and dialogue.",
                "asset_path": "Synchronized video, proprioception, tactile, map-confidence, social-state, intervention, and human-query traces.",
                "asset": "Synchronized video, proprioception, tactile, map-confidence, social-state, intervention, and human-query traces.",
            },
            {
                "priority": "Exploit",
                "title": "Contact-state world model for correction authority",
                "thesis": "Treat tactile, force, deformation, and human-instrumented physical properties as predicted world state that can override nominal VLA actions.",
                "scores": {"strategic_fit": 5, "asymmetry": 4, "timing": 5, "tractability": 4, "defensibility": 4, "scientific_depth": 5},
                "one_week": "Compare ForeTac-VLA, ZeroTouch-style visual contact estimates, and PSR-style predictive force state on one contact-rich task.",
                "four_week": "Add ME-Dex heterogeneous tactile sensors, ForceTwin property estimates, and multiphase liquid-solid manipulation to define correction channels.",
                "success": "Forecast contact state predicts slip, jamming, force overshoot, or failed insertion early enough to change the action chunk.",
                "stop": "Stop if tactile/world-model features improve offline prediction but cannot improve recovery timing or reduce damage.",
                "paper_path": "Manipulation paper on contact-state forecasting as correction authority for VLA policies.",
                "asset_path": "Tactile-video-action logs, visual contact deformation labels, force/property estimates, and correction outcome traces.",
                "asset": "Tactile-video-action logs, visual contact deformation labels, force/property estimates, and correction outcome traces.",
            },
            {
                "priority": "Explore",
                "title": "Evidence-budgeted mapping and navigation",
                "thesis": "Use active reconstruction, confidence-guided odometry, semantic relocalization, low-light SLAM, and social-navigation stress splits to decide what evidence is worth collecting before motion commitment.",
                "scores": {"strategic_fit": 5, "asymmetry": 4, "timing": 4, "tractability": 4, "defensibility": 4, "scientific_depth": 5},
                "one_week": "Run a small indoor route with 2D GauSS-MI active views, VideoReloc adaptive clips, and DPed-VLN/PopNavShift social stress annotations.",
                "four_week": "Add Cube-Splat panoramic mapping, SFVO confidence, Noctif3R low-light sequences, and PIVOT off-road traversability into one evidence budget study.",
                "success": "Additional evidence collection improves route safety or localization reliability more than its time/compute cost.",
                "stop": "Stop if evidence collection improves map metrics but not route commitment, collision avoidance, or social compliance.",
                "paper_path": "Navigation and mapping paper on evidence budgets before motion commitment.",
                "asset_path": "Active-view logs, adaptive clip lengths, odometry confidence, low-light map sequences, social-pedestrian profiles, and route outcomes.",
                "asset": "Active-view logs, adaptive clip lengths, odometry confidence, low-light map sequences, social-pedestrian profiles, and route outcomes.",
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
