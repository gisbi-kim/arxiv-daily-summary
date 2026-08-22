#!/usr/bin/env python3
"""Generate the 2026-08-21 Research Intelligence edition."""

from __future__ import annotations

import json
from pathlib import Path

from gen_research_intelligence_20260811 import build_html


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PROMPT = "prompts/instruction_v20260713.md"


RI_BY_DATE = {
    "2026-08-21": {
        "date": "2026-08-21",
        "edition": "Research Intelligence",
        "source_prompt": SOURCE_PROMPT,
        "source_mode": "new",
        "scope_note": (
            "Daily edition from matching Friday /new listings: 86 non-replacement cs.CV rows, "
            "37 cs.RO rows, 115 deduplicated papers, and 95 ROI papers. Tier A cards are "
            "conservative abstract-only autopsies from the repository parser output; no figure, "
            "table, full-text, code, or dataset-release claims are asserted."
        ),
        "executive_thesis": (
            "The August 21 batch turns action generation into an evidence contract. VLA papers ask "
            "whether embodiment mismatch, continual skill learning, latent-action choices, tactile "
            "world-action forecasts, and whole-body factorization can be measured before a policy is "
            "declared adapted. Planning and autonomy papers ask whether scenario conditions, temporal "
            "logic, world-model grounding, reachability, and causal accident evidence should audit the "
            "plan before deployment. Geometry and VLM papers make the same move: registration, LiDAR "
            "odometry, sparse-view reconstruction, coverage guarantees, and evidence-gated TAMP are "
            "useful only when the decisive evidence path is visible."
        ),
        "decision_cards": [
            {
                "label": "Decision",
                "title": "VLA adaptation needs interface-level evidence",
                "body": (
                    "Self-demonstrated VLA finetuning, OrthoSkillVLA, latent-action analysis, HiTac-WAM, "
                    "and DECOWAM all expose a different interface where adaptation can succeed, forget, "
                    "or lose physical meaning."
                ),
            },
            {
                "label": "Decision",
                "title": "Robot evaluation is becoming scenario-conditioned",
                "body": (
                    "SCAPE, temporal-logic compilation for stream-based TAMP, world-model-grounded LLM "
                    "navigation, SAGE, and DART-S all make the queried scenario or reachable state part "
                    "of the performance claim."
                ),
            },
            {
                "label": "Decision",
                "title": "Generative and VLM systems must expose evidence paths",
                "body": (
                    "VGI-BENCH, BeyondMasks, Question-Guided Evidence Acquisition, marginal-coverage "
                    "audits, and Evidence-Gated TAMP ask whether the output is supported by the right "
                    "visual, causal, physical, or observational evidence."
                ),
            },
        ],
        "papers": [
            {
                "rank": 1,
                "title": "Fine-Tuning VLAs with Self-Demonstrated Generative Control for Multi-Task Manipulation",
                "arxiv_id": "2608.19490",
                "fit": "VLA finetuning - embodiment mismatch - self-demonstrated control",
                "status": "Tier A - abstract-only",
                "status_quo": "VLA adaptation is often treated as in-domain expert-data finetuning on the target robot.",
                "friction": "The abstract states that even minor hardware mismatch can cause severe drops, while expert-task finetuning can degrade general VLA competence.",
                "hidden_premise": "A useful adaptation method must generate or reuse task evidence without destroying the pretrained semantic and action prior.",
                "conceptual_move": "Treat embodiment adaptation as a controlled self-demonstration problem rather than a simple supervised finetune.",
                "mechanism": "The safe abstract-level claim is that generative control creates self-demonstrated data for multi-task manipulation under a new embodiment.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper names hardware-configuration mismatch as a cause of severe VLA performance drop."},
                    {"trace": "[Abstract]", "claim": "It says expert-task finetuning improves that task but harms general capabilities."},
                    {"trace": "[Inference]", "claim": "APRL should score adaptation by retained old-skill behavior as well as new-robot success."},
                ],
                "falsification": "If self-demonstrated data improves only the expert task while old skills or unseen objects regress, the adaptation contract is weak.",
                "adversarial": "Test camera mount, gripper geometry, object pose, and instruction variants that isolate embodiment mismatch from semantic misunderstanding.",
                "thinking_tool": "Measure VLA finetuning as a stability-plasticity trade-off at the robot interface.",
                "transfer_boundary": "Most relevant to new-arm or new-gripper deployment; less direct for purely language-side alignment.",
            },
            {
                "rank": 2,
                "title": "HiTac-WAM: A Hierarchical Tactile World Action Model for Contact-Rich Robot Manipulation",
                "arxiv_id": "2608.19574",
                "fit": "tactile world-action model - contact hierarchy - action chunks",
                "status": "Tier A - abstract-only",
                "status_quo": "World-action models usually predict visual futures and actions, while tactile futures are treated as images or flat latent streams.",
                "friction": "Contact-rich manipulation can fail because tactile states have physical dependencies that a flat latent may not preserve.",
                "hidden_premise": "Future touch should be forecast with a hierarchy that reflects contact physics across candidate action chunks.",
                "conceptual_move": "Move world-action modeling from visual prediction to hierarchical tactile state forecasting.",
                "mechanism": "The abstract describes forecasting future tactile states for candidate action chunks before execution.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper contrasts existing tactile-aware variants with hierarchical physical dependencies."},
                    {"trace": "[Abstract]", "claim": "It forecasts a sequence of future tactile states for each candidate action chunk."},
                    {"trace": "[Inference]", "claim": "APRL should compare tactile forecast error against contact failure and recovery behavior."},
                ],
                "falsification": "If tactile hierarchy improves prediction but not grasp correction, slip avoidance, or recovery, the world-action value is limited.",
                "adversarial": "Use contact transitions where visual state is stable but force distribution, slip, or deformation changes the correct next action.",
                "thinking_tool": "Before acting, ask which hidden contact state must be forecast to make the action safe.",
                "transfer_boundary": "Strong for dexterous and deformable manipulation; weaker for navigation tasks without rich contact.",
            },
            {
                "rank": 3,
                "title": "SCAPE: Scenario-Conditioned Simulation-Augmented Policy Evaluation",
                "arxiv_id": "2608.19425",
                "fit": "robot policy evaluation - scenario conditioning - sim-to-real bias",
                "status": "Tier A - abstract-only",
                "status_quo": "Simulation-augmented robot evaluation often estimates average performance from limited real rollouts and many biased simulated rollouts.",
                "friction": "A policy can look good on average while failing in the specific scenario family that matters for deployment.",
                "hidden_premise": "Simulation should be conditioned on scenario variables so that real-world evidence audits the failure family, not just the mean.",
                "conceptual_move": "Turn policy evaluation into scenario-conditioned estimation under explicit sim-to-real bias.",
                "mechanism": "The abstract frames real testing as faithful but costly, simulation as scalable but biased, and SCAPE as scenario-conditioned evaluation.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper identifies reliable performance evaluation as a central deployment bottleneck."},
                    {"trace": "[Abstract]", "claim": "It contrasts faithful real-world testing with biased scalable simulation."},
                    {"trace": "[Inference]", "claim": "APRL should report policy confidence per scenario family instead of one aggregate score."},
                ],
                "falsification": "If scenario conditioning does not change confidence intervals or policy ranking, the method is not exposing hidden deployment risk.",
                "adversarial": "Choose scenarios where simulation is known to miss contact, lighting, terrain, or occlusion effects.",
                "thinking_tool": "Evaluate a policy by the scenario that can break it, not by the average simulator proxy.",
                "transfer_boundary": "Strong for deployable robot policies; weaker for purely offline perception benchmarks.",
            },
            {
                "rank": 4,
                "title": "LF-GICP: Parameter-Free Degeneracy-Aware LiDAR Odometry via a Voxel-Normal Localizability Field",
                "arxiv_id": "2608.19522",
                "fit": "LiDAR odometry - degeneracy - localizability field",
                "status": "Tier A - abstract-only",
                "status_quo": "Scan-to-map LiDAR odometry is often tuned per environment to handle degeneracy in corridors, tunnels, or other weakly constrained scenes.",
                "friction": "The abstract states that odometry can drift unboundedly along unobservable axes and existing handling requires environment-specific tuning.",
                "hidden_premise": "Localizability can be estimated from voxel-normal structure so the odometry system can identify weak axes without manual parameters.",
                "conceptual_move": "Make degeneracy a first-class field in the map rather than an after-the-fact tuning problem.",
                "mechanism": "The abstract-level mechanism is a voxel-normal localizability field for parameter-free degeneracy-aware LiDAR odometry.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper names tunnels and corridors as geometrically degenerate environments with unbounded drift along unobservable axes."},
                    {"trace": "[Abstract]", "claim": "It proposes a parameter-free voxel-normal localizability field."},
                    {"trace": "[Inference]", "claim": "APRL should score odometry by detecting unobservable axes before navigation fails."},
                ],
                "falsification": "If localizability does not predict drift direction or recovery behavior in field routes, it is not robot-useful.",
                "adversarial": "Test corridors, tunnels, crop rows, repeated pillars, and dynamic-object contamination with matched ground-truth trajectories.",
                "thinking_tool": "Treat map degeneracy as a warning signal that should alter navigation confidence.",
                "transfer_boundary": "Strong for LiDAR mobile robots; less direct for vision-only manipulation.",
            },
            {
                "rank": 5,
                "title": "Question-Guided Evidence Acquisition for Multimodal Visual Question Answering",
                "arxiv_id": "2608.19739",
                "fit": "document VQA - deliberate perception - evidence acquisition",
                "status": "Tier A - abstract-only",
                "status_quo": "Document and multimodal VQA often encode the page once and answer from whatever evidence the model extracted in that pass.",
                "friction": "The abstract says small text, tables, visual cues, and topology trip models even when the page is already in context.",
                "hidden_premise": "The question should decide which evidence to acquire, inspect, or revisit before the model answers.",
                "conceptual_move": "Move VQA from fixed perception to slower, question-conditioned evidence acquisition.",
                "mechanism": "The abstract argues for deliberate perception rather than single-pass extraction; detailed mechanism requires full paper reading.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper states that MLLMs can see a document but often cannot read it reliably."},
                    {"trace": "[Abstract]", "claim": "It names small text, tables, visual cues, and topology as failure cases."},
                    {"trace": "[Inference]", "claim": "Robot VLMs should acquire the missing view, cue, or region before authorizing an action."},
                ],
                "falsification": "If question-guided acquisition improves document accuracy but does not reduce embodied action errors under missing evidence, transfer is limited.",
                "adversarial": "Use robot instructions where the relevant object label, gauge, or spatial relation is small, occluded, or topologically ambiguous.",
                "thinking_tool": "Let the question define the next observation before producing the answer.",
                "transfer_boundary": "Strong for inspection, OCR, gauges, and form-like robot tasks; weaker for low-level control without explicit questions.",
            },
            {
                "rank": 6,
                "title": "Evidence-Gated Task and Motion Planning with Vision-Language Models",
                "arxiv_id": "2608.20084",
                "fit": "VLM-TAMP - partial observability - evidence-gated subgoals",
                "status": "Tier A - abstract-only",
                "status_quo": "VLM-assisted TAMP can generate plausible subgoals from prior knowledge even when the required object evidence has not been observed.",
                "friction": "The abstract warns that under partial observability, unsupported subgoals can cause execution failures or unintended outcomes.",
                "hidden_premise": "A task planner should gate subgoals on explicit observational support, not only semantic plausibility.",
                "conceptual_move": "Make evidence availability a hard interface between VLM semantic planning and geometric execution.",
                "mechanism": "The abstract-level mechanism is evidence-gated task and motion planning under partial observability.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper names uncertain availability of goal-relevant objects under partial observability."},
                    {"trace": "[Abstract]", "claim": "It says VLM priors can generate unsupported subgoals that lead to failures or unintended outcomes."},
                    {"trace": "[Inference]", "claim": "APRL should require a visible evidence gate before geometric planning commits."},
                ],
                "falsification": "If evidence gating only delays execution without reducing unsupported subgoals or failures, the gate is not useful.",
                "adversarial": "Hide goal objects, provide plausible but false priors, and vary when the robot can acquire the decisive observation.",
                "thinking_tool": "Do not allow semantic priors to become motion goals until observation supports them.",
                "transfer_boundary": "Strong for long-horizon mobile manipulation; weaker for fully observed pick-place.",
            },
            {
                "rank": 7,
                "title": "VGI-BENCH: Probing Visual Intelligence in Video Generation Models",
                "arxiv_id": "2608.19583",
                "fit": "video generation benchmark - evolving process - visual intelligence",
                "status": "Tier A - abstract-only",
                "status_quo": "Video generation can be evaluated by plausibility or final-frame quality without testing whether the generated process obeys the task.",
                "friction": "The abstract says benchmarks need valid evolving processes, not only plausible final states, and should be aligned with current video priors.",
                "hidden_premise": "A video generator's reasoning claim requires process-level tasks whose difficulty is calibrated and partially feasible.",
                "conceptual_move": "Evaluate video generation as visual intelligence over evolving processes.",
                "mechanism": "The abstract introduces 27 tasks and 810 instances organized for probing visual intelligence in video generation models.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper argues that benchmarks should require valid evolving processes rather than only plausible final states."},
                    {"trace": "[Abstract]", "claim": "It introduces VGI-BENCH with 27 tasks and 810 instances."},
                    {"trace": "[Inference]", "claim": "Robot world-model evaluation should separate visual realism from process validity."},
                ],
                "falsification": "If process tasks do not predict downstream planning or physical consistency, the benchmark remains generation-specific.",
                "adversarial": "Test videos where the final frame is plausible but contact order, object permanence, or causal timing is wrong.",
                "thinking_tool": "Ask whether the generated process preserves the state transition that a planner would rely on.",
                "transfer_boundary": "Strong for world-model and simulation evaluation; less direct for single-image generation.",
            },
            {
                "rank": 8,
                "title": "BeyondMasks: Evaluating Causal and Physical Consistency in Video Object Removal",
                "arxiv_id": "2608.20107",
                "fit": "video object removal - causal consistency - physical effects",
                "status": "Tier A - abstract-only",
                "status_quo": "Object-removal evaluation often focuses on local masked-region fidelity.",
                "friction": "The abstract argues that real removal is a causal intervention: shadows, reflections, illumination, translucency, and dynamic traces must also change.",
                "hidden_premise": "A video edit should be judged by whether it updates the physical consequences of the removed object.",
                "conceptual_move": "Move object-removal evaluation from local inpainting quality to causal and physical consistency.",
                "mechanism": "The abstract-level mechanism is an evaluation protocol for causal and physical consistency in video object removal.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper states that object removal requires removing induced physical effects."},
                    {"trace": "[Abstract]", "claim": "It lists shadows, reflections, illumination changes, translucency, and dynamic traces."},
                    {"trace": "[Inference]", "claim": "Robot simulation edits should be rejected if physical side effects remain inconsistent."},
                ],
                "falsification": "If physical consistency metrics do not detect edits that break robot perception or planning, the evaluation is incomplete.",
                "adversarial": "Remove obstacles, humans, or tools from videos while checking contact shadows, reflections, and motion traces used by perception models.",
                "thinking_tool": "Treat visual edits as interventions that must update all downstream physical evidence.",
                "transfer_boundary": "Strong for simulation and dataset editing; weaker for tasks where removed content has no physical consequence.",
            },
        ],
        "synthesis": [
            {
                "title": "Adaptation is becoming an interface audit",
                "links": "self-demonstrated VLA - OrthoSkillVLA - latent actions - HiTac-WAM - DECOWAM",
                "facts": "The selected robot-learning abstracts expose embodiment mismatch, forgetting, latent-action fragmentation, tactile hierarchy, and whole-body factorization.",
                "inference": "APRL should measure which interface changes the next action and which interface preserves old skill competence.",
            },
            {
                "title": "Deployment evaluation is scenario-conditioned",
                "links": "SCAPE - temporal-logic TAMP - world-model-grounded LLM planning - SAGE - DART-S",
                "facts": "The autonomy papers attach policy confidence to scenario variables, generated streams, physical world state, risk-weighted inspection, and reachable takeoff states.",
                "inference": "A deployable score should state which scenario family, constraint, or reachable state it covers.",
            },
            {
                "title": "Evidence gates are replacing generic confidence",
                "links": "Question-Guided Evidence Acquisition - Evidence-Gated TAMP - class-conditional coverage - SafeBranch - ArmorOCR",
                "facts": "The VLM and safety papers target missing observations, class tails, unsupported subgoals, unsafe branch pairs, and adversarial text localization.",
                "inference": "Robot agents should identify the evidence that authorizes an answer or motion goal before execution.",
            },
        ],
        "frontier_memory": [
            {
                "label": "Strengthening",
                "history": "August 18-20 repeatedly emphasized runtime evidence, robot-usable geometry, and benchmark-state labels.",
                "body": "August 21 strengthens the same thesis with scenario-conditioned evaluation, evidence-gated TAMP, tactile world-action forecasting, LiDAR degeneracy fields, and process-valid video-generation benchmarks.",
            },
            {
                "label": "New signal",
                "history": "Earlier weekly artifacts emphasized world-action models but less explicit embodiment-factor separation.",
                "body": "DECOWAM and HiTac-WAM make whole-body ego-motion/arm factorization and tactile hierarchy explicit interfaces for future-state prediction.",
            },
            {
                "label": "Contradiction",
                "history": "Recent VLA adaptation work wants broad transfer, while safety and evaluation papers require narrow evidence gates.",
                "body": "The useful research tension is whether gating, shielding, and scenario conditioning improve deployment without destroying the flexibility that made VLA policies attractive.",
            },
            {
                "label": "Missing axis",
                "history": "The repo still lacks a shared benchmark that connects VLA adaptation, evidence-gated planning, contact-state prediction, and map degeneracy in one episode.",
                "body": "APRL can own that missing axis by designing episodes where the same hidden evidence variable affects planning, contact, and localization decisions.",
            },
        ],
        "strategy": [
            {
                "priority": "Build moat",
                "title": "Evidence-gated mobile manipulation protocol",
                "thesis": "Require each VLM-TAMP subgoal, VLA action, and safety branch to cite the observation or predicate that authorizes execution.",
                "scores": {"fit": 5, "novelty": 5, "feasibility": 4, "moat": 5, "timing": 5, "evidence": 5},
                "one_week": "Create ten tasks with hidden goal objects, misleading language priors, branch-pair safety conflicts, and small visual evidence.",
                "four_week": "Evaluate VLM-TAMP, VLA, and embodied-agent baselines with evidence availability, unauthorized subgoal, branch violation, and recovery labels.",
                "success": "Evidence gates reduce unsupported subgoals or unsafe actions while preserving at least 90% of clean-task success.",
                "stop": "If gates only delay execution and do not change failure or safety outcomes, narrow the protocol to observation acquisition.",
                "asset": "Evidence-gated task set, observation labels, branch-pair predicates, subgoal authorization traces, and recovery outcomes.",
            },
            {
                "priority": "Build moat",
                "title": "Contact-and-whole-body world-action benchmark",
                "thesis": "Compare tactile hierarchy, latent actions, self-demonstrated VLA adaptation, and decoupled whole-body forecasts under the same contact-rich tasks.",
                "scores": {"fit": 5, "novelty": 5, "feasibility": 4, "moat": 5, "timing": 4, "evidence": 5},
                "one_week": "Instrument one door traversal and one dexterous grasp task with tactile, ego-motion, arm-motion, and action-chunk labels.",
                "four_week": "Train or evaluate equal-budget policies with self-demonstrated data, latent-action variants, tactile WAM, and decoupled whole-body WAM.",
                "success": "A hidden contact or ego-motion label predicts the next-action correction before terminal success changes.",
                "stop": "If hidden labels do not change policy ranking or recovery choice, split manipulation and locomotion tracks.",
                "asset": "Contact traces, tactile forecasts, ego/arm action factors, latent-action labels, and whole-body recovery logs.",
            },
            {
                "priority": "Explore",
                "title": "Scenario-conditioned deployment confidence",
                "thesis": "Turn simulation-augmented evaluation, temporal logic, risk-weighted inspection, and reachability into explicit scenario coverage claims.",
                "scores": {"fit": 4, "novelty": 4, "feasibility": 4, "moat": 4, "timing": 5, "evidence": 4},
                "one_week": "Define four scenario families: partial observability, degenerate map, dynamic obstacle, and reachability boundary.",
                "four_week": "Compare policy confidence from real rollouts, simulation proxies, temporal-logic monitors, and reachability audits across those families.",
                "success": "Scenario-conditioned confidence changes deployment decisions relative to one aggregate success estimate.",
                "stop": "If confidence intervals and policy rankings remain unchanged across scenario families, keep only the cheapest evaluator.",
                "asset": "Scenario taxonomy, monitor predicates, simulation-real pairs, reachability labels, and deployment confidence reports.",
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
