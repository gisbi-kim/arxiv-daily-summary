#!/usr/bin/env python3
"""Generate the full-text Research Intelligence edition for 2026-07-30."""

from __future__ import annotations

import json
from pathlib import Path

import gen_research_intelligence_20260713 as template


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-07-30"
SLUG = f"{DATE}-research-intelligence"


DATA = {
    "date": DATE,
    "edition": "Research Intelligence",
    "source_prompt": "prompts/instruction_v20260713.md",
    "scope_note": (
        "The 2026-07-30 daily is a backfill from the arXiv /pastweek date section. "
        "The parser found 96 non-replacement cs.CV rows and 43 non-replacement cs.RO rows; "
        "after deduplication, 130 papers remained and 64 were classified as ROI. Tier A uses "
        "official arXiv HTML for TurboVLA, RL2-VLA, CheckVLA, CG-World, ActSWM, BioVLN, and HumanCLAW."
    ),
    "executive_thesis": (
        "The July 30 batch makes execution-time evidence the center of the robotics story. "
        "TurboVLA removes the LLM bottleneck from the action path and asks whether language-conditioned "
        "control can run at local control-loop speed. RL2-VLA and CheckVLA then show the next problem: "
        "a fast or strong base policy still needs adaptive steering, failure prediction, and calibrated "
        "repair while the episode is unfolding. CG-World and ActSWM move the same question into world "
        "models by requiring typed state, branch lineage, action sensitivity, and recovery of the action "
        "behind a transition. BioVLN and HumanCLAW make embodiment measurable by separating operational "
        "face, clearance, body skill, and decision quality from generic navigation or VLM answer accuracy. "
        "APRL should treat this as a push toward execution ledgers: latency, hidden policy state, action "
        "consequence, body constraint, and repair trigger should be logged before success rate is compared."
    ),
    "decision_cards": [
        {
            "label": "Decision",
            "title": "Fast VLA inference is useful only if the execution state remains inspectable",
            "body": (
                "TurboVLA proves that the LLM-centered pathway is not inevitable. The research consequence "
                "is not just lower latency; it is a new interface where instruction, visual feature, and "
                "continuous action chunk can be audited without decoding a language chain at every step."
            ),
        },
        {
            "label": "Decision",
            "title": "Test-time repair needs an action-conditioned reference",
            "body": (
                "RL2-VLA steers only when failure is likely, while CheckVLA predicts what the committed "
                "action chunk should make the world look like. Both reject one fixed intervention policy "
                "for every timestep."
            ),
        },
        {
            "label": "Decision",
            "title": "World models need state contracts, not just plausible futures",
            "body": (
                "CG-World records typed intermediate state and branch lineage; ActSWM diagnoses context "
                "collapse when different actions produce indistinguishable futures. For APRL, a world "
                "model must expose which action variable it preserves."
            ),
        },
    ],
    "papers": [
        {
            "rank": 1,
            "title": "TurboVLA: Real-Time Vision-Language-Action Model at 32 Hz on an RTX 4090 with <1 GB VRAM",
            "arxiv_id": "2607.27205",
            "fit": "real-time VLA - direct vision-language-to-action mapping - local deployment",
            "status": "Tier A - official arXiv HTML verified",
            "status_quo": (
                "Many VLA systems route visual observations through a large language model before actions, "
                "which makes the LLM the central execution interface even for routine manipulation."
            ),
            "friction": (
                "That pathway spends memory and latency every policy call, making high-frequency local control "
                "hard even when the instruction has already specified the manipulation intent."
            ),
            "hidden_premise": (
                "For execution-level control, the policy may only need language-conditioned visual features, "
                "not open-ended language generation at every action step."
            ),
            "conceptual_move": (
                "TurboVLA reformulates the V-to-L-to-A pipeline as direct V+L-to-A fusion with lightweight "
                "bidirectional interaction and continuous action chunk prediction."
            ),
            "mechanism": (
                "Independent visual and instruction encoders exchange information through a compact interaction "
                "module, then a decoder emits continuous action chunks without centering an LLM."
            ),
            "evidence": [
                {"trace": "Figure 1 [Verified]", "claim": "The paper reports compact local deployment with 0.2B parameters, 0.9 GB inference VRAM, and 31.2 ms policy latency."},
                {"trace": "Figure 2 [Verified]", "claim": "The method is framed as a move from LLM-centric VLA to direct visual-instruction fusion for continuous control."},
                {"trace": "Table 1 [Verified]", "claim": "LIBERO results are reported together with parameter count, VRAM, latency, and success rate on a single RTX 4090."},
                {"trace": "Table 3 [Verified]", "claim": "Language conditioning is ablated against no language and task-ID embedding, separating semantic instruction from mere task identity."},
            ],
            "falsification": (
                "If the latency gain disappears on real robot sensing and preprocessing, or if direct fusion loses robustness under compositional instructions, "
                "the method is a benchmark-speed win rather than a general VLA interface shift."
            ),
            "adversarial": (
                "Removing the LLM can also remove useful reasoning or recovery behavior. The paper needs failure cases where the fast policy chooses the wrong object or phase."
            ),
            "thinking_tool": (
                "Treat the VLA pathway as an execution interface: log instruction embedding age, visual token set, action chunk, latency, and failure phase."
            ),
            "transfer_boundary": (
                "The idea transfers to language-conditioned manipulation with stable skill semantics. It is less direct for tasks that require open-ended replanning or dialogue."
            ),
        },
        {
            "rank": 2,
            "title": "RL2-VLA: Adaptive RL Latent Compositional Steering with Test-Time Scaling for Vision-Language-Action Models",
            "arxiv_id": "2607.26991",
            "fit": "VLA test-time steering - latent RL policy - adaptive failure prediction",
            "status": "Tier A - official arXiv HTML verified",
            "status_quo": (
                "Inference-time steering often applies one intervention recipe at every step, even when the base policy is already producing good action samples."
            ),
            "friction": (
                "OOD language or environments can collapse VLA success, but unnecessary steering can also push a good action into a correlated failure mode."
            ),
            "hidden_premise": (
                "A lightweight RL policy over VLA latents can help only when its intervention is gated by likely failure."
            ),
            "conceptual_move": (
                "RL2-VLA composes an offline RL latent policy with the frozen VLA flow at inference time and adapts the intervention through failure detection."
            ),
            "mechanism": (
                "The method extracts expressive VLA action latents, trains a lightweight RL policy, composes flow velocities, and uses conformal prediction to decide when to steer."
            ),
            "evidence": [
                {"trace": "Figure 1 [Verified]", "claim": "The paper highlights OOD drops from 38.2% to 14.2% for unseen language and from 70.2% to 36.0% for unseen environments in cited VLA settings."},
                {"trace": "Figure 2 [Verified]", "claim": "The tape-in-toolbox real-robot example contrasts rephrasing, non-adaptive RL2, and adaptive RL2 under a collision-prone OOD task."},
                {"trace": "Method sections V-A to V-D [Verified]", "claim": "The paper separates latent policy training, compositional steering, failure detection, and action verification."},
                {"trace": "Conclusion page metadata [Verified]", "claim": "The official arXiv HTML is version v2 dated 30 Jul 2026, matching the backfill source date."},
            ],
            "falsification": (
                "If the detector fires mostly after the failure is already unrecoverable, adaptive steering becomes a post-hoc explanation rather than a repair mechanism."
            ),
            "adversarial": (
                "RL over latents may inherit the same simulator or training distribution shortcuts as the VLA. The conformal gate needs calibration under true deployment shifts."
            ),
            "thinking_tool": (
                "For every intervention, store base action sample diversity, latent steering magnitude, failure probability, and whether the repair was necessary."
            ),
            "transfer_boundary": (
                "This transfers to flow-matching or latent-action VLAs with accessible internal latents. It is weaker for black-box policies without a stable action manifold."
            ),
        },
        {
            "rank": 3,
            "title": "CheckVLA: Execution-Time Verification with Action-Conditioned World Model for Long-Horizon Mobile Manipulation",
            "arxiv_id": "2607.26789",
            "fit": "execution-time verification - action-conditioned world model - long-horizon mobile manipulation",
            "status": "Tier A - official arXiv HTML verified",
            "status_quo": (
                "Long-horizon VLA policies often commit action chunks and keep executing after a deviation, because commit-time confidence cannot see post-dispatch drift."
            ),
            "friction": (
                "Observation-only anomaly detection cannot tell the difference between expected consequences of the action and unexplained changes that require intervention."
            ),
            "hidden_premise": (
                "A verifier should predict the world conditioned on the remaining committed action, then calibrate a risk trigger before rewriting the suffix."
            ),
            "conceptual_move": (
                "CheckVLA adds a frozen action-conditioned world model, conformal risk threshold, latency-aware suffix rewriting, and episodic context to the execution loop."
            ),
            "mechanism": (
                "Rolling prediction estimates near-term consequences; a causal risk head compares prediction to observation; threshold crossing controls repair timing and suffix retention."
            ),
            "evidence": [
                {"trace": "Figure 1 [Verified]", "claim": "The verifier predicts short-horizon features from latest observation and remaining actions, then uses a conformal threshold for the first intervention."},
                {"trace": "Figure 2 [Verified]", "claim": "The framework couples action-conditioned rolling prediction, calibrated risk triggering, latency-aware suffix rewriting, and episodic context."},
                {"trace": "Table 1 [Verified]", "claim": "The comparison table marks CheckVLA as covering action-conditioned signal, calibrated trigger, in-chunk repair, latency awareness, and episodic memory."},
                {"trace": "Appendix headings [Verified]", "claim": "The HTML lists calibration, action-consequence binding, latency, natural failures, runtime, and failure-analysis sections."},
            ],
            "falsification": (
                "If the world model is wrong in exactly the OOD states that matter, calibrated risk can be confidently late or confidently unnecessary."
            ),
            "adversarial": (
                "A separate verifier can learn benchmark-specific consequence features. It must be tested on natural disturbances and not only injected deviations."
            ),
            "thinking_tool": (
                "Log committed action, predicted consequence, observed consequence, risk trace, threshold crossing, suffix rewrite, and final recovery."
            ),
            "transfer_boundary": (
                "This transfers to chunked mobile manipulation and navigation. It is harder for high-rate contact control where consequence prediction must run at tactile timescales."
            ),
        },
        {
            "rank": 4,
            "title": "CG-World: A Large-Scale World-State Dataset and Protocol for World Models",
            "arxiv_id": "2607.26452",
            "fit": "world-state dataset - branch lineage - intervention and counterfactual protocol",
            "status": "Tier A - official arXiv HTML verified",
            "status_quo": (
                "Video and robotics datasets often expose observations but hide intermediate state, branch metadata, contact events, and production provenance."
            ),
            "friction": (
                "A world model cannot learn intervention or counterfactual structure if the data records only final pixels or partial trajectories."
            ),
            "hidden_premise": (
                "Industrial computer graphics pipelines already preserve the typed state variables that world models need but ordinary video datasets discard."
            ),
            "conceptual_move": (
                "CG-World turns CG production records into a world-state protocol with states, observations, relations, events, branch lineage, and provenance."
            ),
            "mechanism": (
                "The dataset aligns temporally indexed segments with multimodal semantics, spatial structure, skeletal/controller states, motion curves, camera and lighting parameters, physics caches, contacts, and render passes."
            ),
            "evidence": [
                {"trace": "Abstract [Author claim]", "claim": "CG-World v1 contains about 850,000 temporally aligned 1-5 second segments."},
                {"trace": "Figure 1 [Verified]", "claim": "The protocol declares data type, tensor shape, temporal index, units, coordinate system, availability, and provenance for core fields."},
                {"trace": "Figure 2 [Verified]", "claim": "The pipeline converts industrial CG projects into data packages with production-quality source records."},
                {"trace": "Experiment headings [Verified]", "claim": "The HTML lists observation video generation, multi-step action prediction, and VLA transfer in simulation as experiments."},
            ],
            "falsification": (
                "If production CG branch lineage does not transfer to physical contact, sensor noise, or robot embodiment, the dataset may teach clean-state reasoning but not deployment dynamics."
            ),
            "adversarial": (
                "CG provenance can be a strength and a bias. The release needs explicit domain-gap labels before robot world-model claims are accepted."
            ),
            "thinking_tool": (
                "Define a world-model sample by state fields and branch lineage before training: observations are only one view of the state contract."
            ),
            "transfer_boundary": (
                "The protocol transfers to simulation, planning, and counterfactual data design. Real manipulation still needs contact, calibration, and sensor-noise anchoring."
            ),
        },
        {
            "rank": 5,
            "title": "ActSWM: Action-Sensitive World Models for Long-Horizon Planning in Open-World Games",
            "arxiv_id": "2607.26712",
            "fit": "latent world model - action sensitivity - long-horizon planning",
            "status": "Tier A - official arXiv HTML verified",
            "status_quo": (
                "Latent world models can produce plausible future states while becoming insensitive to the different actions a planner is considering."
            ),
            "friction": (
                "Prediction accuracy alone does not make a world model useful for planning if alternative actions collapse into nearly the same rollout."
            ),
            "hidden_premise": (
                "A planning-useful latent dynamics model should preserve enough transition information to recover which action caused a local change."
            ),
            "conceptual_move": (
                "ActSWM diagnoses context collapse and trains latent rollouts with an action-sensitivity principle and action-readout separation."
            ),
            "mechanism": (
                "JEPA-based latent prediction, multi-step rollout training, a hinge loss, and a fixed action readout encourage futures for different actions to remain distinguishable."
            ),
            "evidence": [
                {"trace": "Figure 1 [Verified]", "claim": "The overview defines context collapse as plausible rollouts that are insensitive to action inputs."},
                {"trace": "Figure 2 [Verified]", "claim": "The framework combines latent prediction, multi-step rollout training, action-sensitivity loss, and action readout."},
                {"trace": "Table 1 [Verified]", "claim": "Local action-recovery results compare ActSWM with D2E and LeWM across Counter-Strike, GTA, and Apex settings."},
                {"trace": "Experiment headings [Verified]", "claim": "The paper separates context-collapse diagnosis, closed-loop planning, and discriminative action representations."},
            ],
            "falsification": (
                "If action recoverability improves while downstream planning does not, the auxiliary objective may preserve labels but not the right control variables."
            ),
            "adversarial": (
                "Open-world games are useful stress tests but do not guarantee physical contact validity. The same principle needs robot action-space and embodiment checks."
            ),
            "thinking_tool": (
                "Before using a world model for planning, test whether different candidate actions remain distinguishable in the predicted latent future."
            ),
            "transfer_boundary": (
                "The principle transfers to action-conditioned planning models. It needs adaptation for continuous robot actions and partial observability."
            ),
        },
        {
            "rank": 6,
            "title": "BioVLN: A Simulation Platform for Visual Language Navigation in Biomedical Laboratories",
            "arxiv_id": "2607.26914",
            "fit": "laboratory navigation - operational-face goal - safety envelope",
            "status": "Tier A - official arXiv HTML verified",
            "status_quo": (
                "Object-goal navigation benchmarks often define success as reaching an object center or arbitrary near position."
            ),
            "friction": (
                "A lab robot must approach the instrument from the operating side while keeping clearance from benches, walls, and nearby equipment."
            ),
            "hidden_premise": (
                "The target should be modeled as body, clearance region, and operational face, not as a point object."
            ),
            "conceptual_move": (
                "BioVLN builds laboratory scenes and navigation episodes around a three-zone operational envelope for each instrument."
            ),
            "mechanism": (
                "Designer-authored or procedurally generated scenes flow through asset annotation, navigation mesh generation, episode construction, and safety metrics."
            ),
            "evidence": [
                {"trace": "Figure 1 [Verified]", "claim": "The platform architecture includes designer-authored scene import and procedural generation paths converging into a shared benchmark pipeline."},
                {"trace": "Figure 2 [Verified]", "claim": "Operational-face goal navigation distinguishes physical body, clearance region, and usable-side operation area."},
                {"trace": "Table 1 [Verified]", "claim": "BioVLN is compared against Habitat, AI2-THOR, ProcTHOR, and iGibson on domain, procedural generation, scene import, and lab-specific support."},
                {"trace": "Experiment headings [Verified]", "claim": "The paper evaluates geometric coverage, instrument difficulty, layout-density safety, VLM analysis, and operational-face ablation."},
            ],
            "falsification": (
                "If operational-face success does not predict procedure readiness, the benchmark may be more geometric than task-completion relevant."
            ),
            "adversarial": (
                "Procedural labs may miss clutter, contamination constraints, human technicians, or instrument-state dependencies that decide real operation."
            ),
            "thinking_tool": (
                "Represent every navigation target with body, clearance, usable face, and required post-arrival manipulation affordance."
            ),
            "transfer_boundary": (
                "This transfers to lab and equipment-rich navigation. It is less direct for open homes or outdoor navigation where target affordance is less face-specific."
            ),
        },
        {
            "rank": 7,
            "title": "HumanCLAW: Can Vision-Language Models Act Through a Body?",
            "arxiv_id": "2607.27180",
            "fit": "embodied VLM evaluation - body action intelligence - motor-decoupled physical loop",
            "status": "Tier A - official arXiv HTML verified",
            "status_quo": (
                "When a physically embodied VLM fails, success metrics often mix a poor high-level decision with low-level motor or balance failure."
            ),
            "friction": (
                "Without decoupling, it is unclear whether the VLM selected the wrong action or the controller failed to execute a reasonable command."
            ),
            "hidden_premise": (
                "A benchmark can keep real physical consequences while factoring out low-level execution disturbances."
            ),
            "conceptual_move": (
                "HumanCLAW lets a harnessed VLM issue atomic skill commands that are translated into sub-second full-body motion under gravity and collision."
            ),
            "mechanism": (
                "A skill-conditioned generator executes each command in a physics loop and returns the next egocentric observation, isolating action decision quality."
            ),
            "evidence": [
                {"trace": "Figure 1 [Verified]", "claim": "The framework positions HumanCLAW between action without a body and embodied action confounded by balance or motor control."},
                {"trace": "Figure 2 [Verified]", "claim": "A VLM maps each egocentric observation to a skill call, which becomes a 0.5 second full-body motion chunk."},
                {"trace": "Table 1 [Verified]", "claim": "Skill achievement ratios are reported near unity for walking, turning, side-stepping, stepping back, sitting, and stair climbing with small variance."},
                {"trace": "Ablation headings [Verified]", "claim": "The HTML lists verifier, text history, image frames, and mid-level reasoning as ablated components."},
            ],
            "falsification": (
                "If the harnessed skills remove the hard part of embodiment, the benchmark measures symbolic skill sequencing more than physical action intelligence."
            ),
            "adversarial": (
                "Factoring out low-level control is analytically clean but can overstate deployment readiness where balance, contact, and action choice interact."
            ),
            "thinking_tool": (
                "Separate body-aware decision quality from motor fidelity, then rejoin them only after the failure attribution is clear."
            ),
            "transfer_boundary": (
                "The setup transfers to embodied decision benchmarks. It should not be used alone to claim full robot deployment capability."
            ),
        },
    ],
    "synthesis": [
        {
            "title": "S1 - VLA progress is moving inside the execution loop",
            "links": "TurboVLA - RL2-VLA - CheckVLA",
            "facts": (
                "TurboVLA removes the LLM execution bottleneck; RL2-VLA gates latent steering by likely failure; CheckVLA verifies action chunks against predicted consequences."
            ),
            "inference": (
                "The shared research decision is to expose the state of the policy while the episode is still repairable."
            ),
            "decision": "APRL should build VLA logs around latency, intervention trigger, action-conditioned prediction, and repair result.",
        },
        {
            "title": "S2 - World models need action-sensitive state, not just convincing futures",
            "links": "CG-World - ActSWM",
            "facts": (
                "CG-World records typed state and branch metadata, while ActSWM tests whether different actions remain distinguishable in latent rollouts."
            ),
            "inference": (
                "A world model is a planning asset only when it preserves the action variable the planner is choosing."
            ),
            "decision": "APRL should require action recoverability and branch-lineage metadata in world-model evaluation.",
        },
        {
            "title": "S3 - Embodied benchmarks are becoming geometry-of-use benchmarks",
            "links": "BioVLN - HumanCLAW",
            "facts": (
                "BioVLN types the operational side and clearance of lab instruments; HumanCLAW factors motor control away from body-aware decision quality."
            ),
            "inference": (
                "Embodiment is no longer a generic 3D scene label; it is the set of constraints that make an action usable."
            ),
            "decision": "APRL should add target affordance, clearance, body command, and failure-attribution fields to embodied tasks.",
        },
    ],
    "frontier_memory": [
        {
            "signal": "strengthening",
            "title": "VLA work keeps moving from model size to execution state",
            "history": "Recent July runs tracked compact VLA reasoning, causal modality effects, and dynamic tokens.",
            "read": "July 30 adds real-time direct VLA execution, adaptive latent steering, and action-conditioned verification.",
        },
        {
            "signal": "new",
            "title": "World-state datasets are becoming an APRL asset direction",
            "history": "Prior world-model papers often optimized generated video or future prediction.",
            "read": "CG-World foregrounds typed state, branch lineage, and provenance as the missing substrate for intervention learning.",
        },
        {
            "signal": "strengthening",
            "title": "Embodied benchmarks are typing the physical interface",
            "history": "Earlier navigation and manipulation benchmarks emphasized task success, memory, or object finding.",
            "read": "BioVLN and HumanCLAW define usable side, clearance, body skill, and decision attribution as first-class variables.",
        },
        {
            "signal": "missing_axis",
            "title": "Fast policy papers still need natural-failure repair audits",
            "history": "Most VLA comparisons report aggregate success or benchmark perturbations.",
            "read": "The missing artifact is a public per-step repair ledger showing when the verifier or steering module prevented a real failure.",
        },
    ],
    "strategy": [
        {
            "priority": "BUILD",
            "title": "Execution-Time VLA Evidence Ledger",
            "thesis": (
                "Instrument a VLA episode with direct policy latency, latent steering, action-conditioned predicted consequence, calibrated risk, and suffix repair outcome."
            ),
            "scores": {"fit": 5, "novelty": 5, "feasibility": 4, "moat": 5, "timing": 5, "evidence": 5},
            "one_week": (
                "Run two manipulation tasks with a baseline VLA and record action chunk latency, base action, failure probability, verifier risk, and repair decision."
            ),
            "four_week": (
                "Compare direct fast VLA, adaptive latent steering, and action-conditioned verification under the same induced and natural failure set."
            ),
            "metric": "At least one evidence field predicts or prevents failure two steps before terminal failure with AUC >= 0.75 or recovery +10p.",
            "stop": "If the ledger fields do not improve failure prediction over previous success and task ID, narrow to one failure family.",
            "assets": [
                {"label": "TurboVLA", "url": "https://arxiv.org/abs/2607.27205"},
                {"label": "RL2-VLA", "url": "https://arxiv.org/abs/2607.26991"},
                {"label": "CheckVLA", "url": "https://arxiv.org/abs/2607.26789"},
                {"label": "APRL execution ledger", "url": "APRL internal VLA execution ledger"},
            ],
        },
        {
            "priority": "EXPLORE",
            "title": "Action-Sensitive World-State Protocol",
            "thesis": (
                "Evaluate world models by whether they preserve typed state, branch lineage, and action-distinguishable futures under planning."
            ),
            "scores": {"fit": 5, "novelty": 5, "feasibility": 3, "moat": 5, "timing": 4, "evidence": 4},
            "one_week": (
                "Build a small schema for one robot or game trace: state fields, action, observation, branch ID, and action-recovery probe."
            ),
            "four_week": (
                "Train or adapt a latent predictor and score prediction loss, action recoverability, counterfactual branch consistency, and plan success."
            ),
            "metric": "Action-recovery accuracy and plan success improve together; if they diverge, identify the missing state variable.",
            "stop": "If typed state does not change planning results on two tasks, keep it as dataset documentation rather than a model objective.",
            "assets": [
                {"label": "CG-World", "url": "https://arxiv.org/abs/2607.26452"},
                {"label": "ActSWM", "url": "https://arxiv.org/abs/2607.26712"},
                {"label": "APRL world-state schema", "url": "APRL internal world-state protocol"},
            ],
        },
        {
            "priority": "EXPLOIT",
            "title": "Operational-Face Embodiment Benchmark",
            "thesis": (
                "Redefine navigation and embodied decision tasks around usable side, clearance, body skill, and failure attribution instead of reaching a target point."
            ),
            "scores": {"fit": 5, "novelty": 4, "feasibility": 5, "moat": 4, "timing": 5, "evidence": 4},
            "one_week": (
                "Annotate ten APRL lab or tabletop goals with physical body, clearance zone, operational face, and required post-arrival action."
            ),
            "four_week": (
                "Run a small embodied-agent benchmark that reports target success, operational-face success, collision/clearance violation, and body-command attribution."
            ),
            "metric": "Operational-face success reveals at least one failure hidden by point-goal success; body-command attribution separates decision vs execution failures.",
            "stop": "If point-goal success and operational-face success rank methods identically, fold the benchmark into existing navigation tests.",
            "assets": [
                {"label": "BioVLN", "url": "https://arxiv.org/abs/2607.26914"},
                {"label": "HumanCLAW", "url": "https://arxiv.org/abs/2607.27180"},
                {"label": "APRL operational-face labels", "url": "APRL internal lab navigation labels"},
            ],
        },
    ],
}


def main() -> None:
    template.DATE = DATE
    template.SLUG = SLUG
    template.DATA = DATA
    doc = template.build_html()
    doc = doc.replace("2026-07-13 arXiv Research Intelligence", f"{DATE} arXiv Research Intelligence")
    doc = doc.replace("Tier A 5", f"Tier A {len(DATA['papers'])}")
    doc = doc.replace(
        "기존 daily 요약을 보완한 별도 에디션입니다.",
        "Today's parser corpus is distilled into a separate Research Intelligence edition.",
    )
    json_dir = ROOT / "intelligence"
    json_dir.mkdir(exist_ok=True)
    json_path = json_dir / f"{DATE}.json"
    html_path = ROOT / "posts" / f"{SLUG}.html"
    json_path.write_text(json.dumps(DATA, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    html_path.write_text(doc, encoding="utf-8")
    print(f"wrote {json_path.relative_to(ROOT)}")
    print(f"wrote {html_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
