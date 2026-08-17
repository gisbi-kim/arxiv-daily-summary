#!/usr/bin/env python3
"""Generate the 2026-08-17 Research Intelligence edition."""

from __future__ import annotations

import json
from pathlib import Path

from gen_research_intelligence_20260811 import build_html


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PROMPT = "prompts/instruction_v20260713.md"


RI_BY_DATE = {
    "2026-08-17": {
        "date": "2026-08-17",
        "edition": "Research Intelligence",
        "source_prompt": SOURCE_PROMPT,
        "source_mode": "new",
        "scope_note": (
            "Daily edition from matching Monday /new listings: 89 non-replacement cs.CV rows, "
            "32 cs.RO rows, 116 deduplicated papers, and 97 ROI papers. Tier A cards are conservative "
            "abstract-only autopsies from the repository parser output; no figure/table/full-text claims are asserted."
        ),
        "executive_thesis": (
            "The August 17 batch pushes robotics toward explicit commitment contracts: a VLA should expose which tool, "
            "judge, progress signal, or latency path can change the next action; a world model should preserve belief, "
            "temporal-logic state, or failed predicate arguments rather than only rendering plausible futures; and a "
            "navigation or driving system should prove safety through matched events, certificates, and failure-discovery "
            "coverage before average success is trusted."
        ),
        "decision_cards": [
            {
                "label": "Decision",
                "title": "VLAs are being wrapped with process interfaces",
                "body": (
                    "ART, PRM-as-a-Judge, BICPO-VLA, ReflexVLA, and self-supervised on-policy distillation all ask "
                    "which intermediate tool, progress curve, handoff state, or future prediction should control action authority."
                ),
            },
            {
                "label": "Decision",
                "title": "World models must remember verifiable predicates",
                "body": (
                    "OpenBelief-Nav, hint2, Onto-EV-WM, ForgeWM, and Marionette separate belief, temporal logic, "
                    "predicate repair, low-latency action futures, and explicit geometry so the future can be audited."
                ),
            },
            {
                "label": "Decision",
                "title": "Safety evaluation is moving to matched failures",
                "body": (
                    "SSP, coverage-aware active evaluation, temporal barriers, tube certificates, and hazard-informed "
                    "envelopes all make the tested event, risk metric, and allowed correction explicit."
                ),
            },
        ],
        "papers": [
            {
                "rank": 1,
                "title": "Evolve Vision-Language-Action Model into an Agent with On-the-fly Tool-use",
                "arxiv_id": "2608.14047",
                "fit": "VLA tool use - modular action space - data-efficient generalization",
                "status": "Tier A - abstract-only",
                "status_quo": "End-to-end VLAs usually ask one policy head to cover the full continuous action space.",
                "friction": "Dark scenes, novel viewpoints, and low-level perception gaps can make a monolithic action decoder spend data on skills that tools already solve.",
                "hidden_premise": "A VLA can learn when to call tool modules without losing the embodied action contract.",
                "conceptual_move": "Turn the VLA into an agentic robot interface that injects low-level vision, affordance, and embodiment tools on demand.",
                "mechanism": "The abstract describes a tool-injection framework, 30K tool-use trajectories, and long-trajectory tool-use reasoning training.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "ART tunes VLA models to leverage off-the-shelf tool modules for vision, affordance, and embodiment enhancement."},
                    {"trace": "[Abstract]", "claim": "The authors report higher success than mainstream baselines on simulation and real-world tasks including dark pick-and-place and novel viewpoints."},
                    {"trace": "[Inference]", "claim": "APRL should measure which tool call changed the next action, not only whether the rollout succeeded."},
                ],
                "falsification": "If tool calls improve easy visual cases but not out-of-view, low-light, or affordance-confusing cases, the method is extra routing overhead.",
                "adversarial": "Off-the-shelf tools may leak strong priors; test scenes where the correct tool output is misleading or unavailable.",
                "thinking_tool": "Treat action generation as a tool-authority allocation problem.",
                "transfer_boundary": "Strong for modular robot stacks; weaker for hardware where useful tool interfaces are not exposed.",
            },
            {
                "rank": 2,
                "title": "PRM-as-a-Judge 1.5: A Toolkit for Robot Process Assessment",
                "arxiv_id": "2608.14284",
                "fit": "robot process assessment - progress curves - failure-side diagnostics",
                "status": "Tier A - abstract-only",
                "status_quo": "Robot evaluation often compresses a rollout into binary success or a coarse rule-based process score.",
                "friction": "A policy can fail late after real progress, recover from drawdown, or succeed with fragile execution, and final success hides those differences.",
                "hidden_premise": "Dense progress curves can become evaluation evidence if the evaluator itself is reliability-tested.",
                "conceptual_move": "Convert rollout videos into process-reward-model judgments and fine metrics for failure-side progress, recovery, and success-side quality.",
                "mechanism": "The abstract introduces new metrics plus RoboPulse++ to test PRM reliability and a reproducible assessment suite.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The toolkit turns rollout videos into dense progress curves and derives failure-side, recovery, and execution-quality metrics."},
                    {"trace": "[Abstract]", "claim": "It includes RoboPulse++ to evaluate process reward model reliability."},
                    {"trace": "[Inference]", "claim": "APRL should separate evaluator reliability from robot-policy quality when using video judges."},
                ],
                "falsification": "If PRM curves correlate with visual smoothness rather than task-state progress, the judge is not measuring the robot process.",
                "adversarial": "Test occlusion, camera jitter, similar-looking subgoals, and failed recoveries that appear visually fluent.",
                "thinking_tool": "Evaluate the trajectory shape, not only the terminal label.",
                "transfer_boundary": "Strong when rollout videos expose state progress; weaker for tactile or force-critical tasks hidden from camera.",
            },
            {
                "rank": 3,
                "title": "Reflex: Enabling Fast and Predictive Vision-Language-Action Models for Reaction-Critical Manipulation",
                "arxiv_id": "2608.14379",
                "fit": "reaction-critical manipulation - VLA latency - latent future prediction",
                "status": "Tier A - abstract-only",
                "status_quo": "VLA benchmarks usually emphasize static manipulation generalization and under-specify inference latency.",
                "friction": "Dynamic manipulation can fail because the policy reasons correctly but reacts after the interaction window has closed.",
                "hidden_premise": "A useful VLA for dynamic tasks must couple temporal prediction with an explicit latency budget.",
                "conceptual_move": "Build ReflexBench for reaction-critical tasks and a faster VLA with latent future prediction, multi-frame fusion, and deployment optimizations.",
                "mechanism": "The abstract describes configurable latency under synchronous/asynchronous inference, batched encoding, and CUDA Graph replay.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "ReflexBench decouples simulator stepping from robot control and supports configurable latency."},
                    {"trace": "[Abstract]", "claim": "ReflexVLA combines latent future prediction, multi-frame temporal fusion, and reduced deployment latency."},
                    {"trace": "[Inference]", "claim": "APRL should report success as a function of allowed reaction time, not only task family."},
                ],
                "falsification": "If gains disappear when latency is equalized against strong baselines, the benefit is systems engineering rather than predictive representation.",
                "adversarial": "Stress moving objects, delayed observations, and asynchronous controller updates separately.",
                "thinking_tool": "Make reaction time an experimental variable in VLA evaluation.",
                "transfer_boundary": "Strong for dynamic manipulation; less direct for slow quasi-static tasks.",
            },
            {
                "rank": 4,
                "title": "OpenBelief-Nav: Evidence-Preserving Object Memory for Open-Vocabulary Language-Guided Navigation",
                "arxiv_id": "2608.13923",
                "fit": "open-vocabulary navigation - object belief memory - provenance",
                "status": "Tier A - abstract-only",
                "status_quo": "Open-vocabulary scene graphs often fuse observations into one label or feature per object.",
                "friction": "Early semantic commitment can erase minority but task-relevant hypotheses needed at instruction time.",
                "hidden_premise": "Navigation memory should preserve phrase, reliability, mask, and frame provenance until the task readout is known.",
                "conceptual_move": "Store observation-level evidence and maintain separate geometric and visual representations for task-specific readout.",
                "mechanism": "The abstract describes vocabulary-independent object belief, fixed-vocabulary projection, free-form retrieval, and verified candidate attempts.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The method retains observation-level phrases, reliability cues, and frame-mask provenance."},
                    {"trace": "[Abstract]", "claim": "The authors report improvements over early-commit readouts on ScanNet200/Replica and navigation trials."},
                    {"trace": "[Inference]", "claim": "APRL should keep conflicting object hypotheses alive until a robot action needs them resolved."},
                ],
                "falsification": "If belief preservation improves segmentation but not target selection under ambiguity, the memory is not action-relevant.",
                "adversarial": "Use objects with ambiguous labels, occluded affordances, and repeated instances to test when provenance changes the route.",
                "thinking_tool": "Do not collapse semantic evidence before the downstream action asks its question.",
                "transfer_boundary": "Strong for navigation and scene memory; weaker for tasks with closed object vocabularies and canonical views.",
            },
            {
                "rank": 5,
                "title": "hint2: Hierarchical World Models for Inference-Time Temporal Logic Guidance",
                "arxiv_id": "2608.13678",
                "fit": "temporal logic guidance - hierarchical world models - closed-loop policy constraints",
                "status": "Tier A - abstract-only",
                "status_quo": "Language-conditioned policies generate short action chunks while temporal-logic constraints are evaluated over long trajectories.",
                "friction": "A locally plausible chunk can violate a non-Markovian safety or ordering rule that only appears across the full task.",
                "hidden_premise": "High-level proposition transitions and low-level local dynamics can provide complementary guidance at inference time.",
                "conceptual_move": "Use hierarchical world models to guide short-horizon policies toward LTL satisfaction without retraining the policy.",
                "mechanism": "The abstract separates high-level atomic-proposition progress through an automaton from low-level state-evolution safety guidance.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper derives two guidance objectives from different abstraction levels of world models."},
                    {"trace": "[Abstract]", "claim": "The high-level model predicts action-induced transitions in task-relevant atomic propositions."},
                    {"trace": "[Inference]", "claim": "APRL should test whether temporal-logic guidance blocks the exact action that would violate the specification."},
                ],
                "falsification": "If LTL satisfaction improves only on specs with easy proposition labels, the guidance may not survive real perceptual uncertainty.",
                "adversarial": "Stress ambiguous proposition detection, delayed effects, and safety rules that conflict with progress.",
                "thinking_tool": "Split long-horizon constraints into proposition progress and local safety signals.",
                "transfer_boundary": "Strong for instruction-following manipulation with symbolic milestones; weaker when predicates cannot be grounded reliably.",
            },
            {
                "rank": 6,
                "title": "Ontology-Grounded World Models for Failure Diagnosis and Closed-Loop Repair in Physical AI Systems",
                "arxiv_id": "2608.13901",
                "fit": "failure diagnosis - ontology interface - verification-gated repair",
                "status": "Tier A - abstract-only",
                "status_quo": "World-model repair can report quality scores without naming the failed task predicate or the allowed correction route.",
                "friction": "A repair loop is hard to trust if failed predicates, arguments, and post-correction acceptance are not retained.",
                "hidden_premise": "Symbolic task-local records can make learned or heuristic proposers auditable without replacing the world model.",
                "conceptual_move": "Layer an ontology-grounded diagnosis and verification-gated correction interface above EV-WM.",
                "mechanism": "The abstract describes task-local TBox/ABox grounding, deterministic rule retention, route labels, and bounded retry verification.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "Onto-EV-WM records unmet task predicates, route labels, and post-correction acceptance results."},
                    {"trace": "[Abstract]", "claim": "The interface keeps learned or heuristic proposers separate from native predicate verification."},
                    {"trace": "[Inference]", "claim": "APRL should require every repair proposal to carry the predicate it claims to fix."},
                ],
                "falsification": "If predicate records do not improve correction selection beyond a tuned continuous score, the ontology adds bookkeeping without control value.",
                "adversarial": "Test failures where the same visible state supports multiple missing predicates or where a repair fixes one predicate and breaks another.",
                "thinking_tool": "Make failure repair answerable to named predicates and bounded retries.",
                "transfer_boundary": "Strong for task families with explicit predicates; weaker for open-ended manipulation where predicate design is unstable.",
            },
            {
                "rank": 7,
                "title": "Accelerating Large-scale Bundle Adjustment for LiDAR Mapping via Parallel Computing",
                "arxiv_id": "2608.14266",
                "fit": "LiDAR mapping - parallel bundle adjustment - large-scale map consistency",
                "status": "Tier A - abstract-only",
                "status_quo": "Bundle adjustment is central for globally consistent LiDAR maps but can be too slow for large-scale robotic mapping.",
                "friction": "A mapping method that preserves accuracy but cannot process large point clouds under memory limits may not be deployable.",
                "hidden_premise": "Optimization speed can be a map-quality interface if residuals, Jacobians, Hessians, and solver increments stay faithful.",
                "conceptual_move": "Parallelize data loading, planar feature extraction, and majorization-minimization optimization for large-scale LiDAR BA.",
                "mechanism": "The abstract describes asynchronous GPU data loading, bottom-up voxelization, parallel residual/Jacobian/Hessian computation, and a parallel increment solver.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper claims a fully parallel computing framework for LiDAR bundle adjustment."},
                    {"trace": "[Abstract]", "claim": "It reports up to tenfold computational efficiency while preserving mapping accuracy comparable to state-of-the-art methods."},
                    {"trace": "[Inference]", "claim": "APRL should compare speedups under loop-closure, dynamic objects, and memory-constrained mapping rather than only offline runtime."},
                ],
                "falsification": "If speedups require benign planar scenes or large GPUs, the deployment value narrows.",
                "adversarial": "Stress sparse structure, dynamic objects, non-planar geometry, and limited-memory GPU settings.",
                "thinking_tool": "Treat mapping efficiency as part of the robot-usable map contract.",
                "transfer_boundary": "Strong for LiDAR mapping and long-range navigation; less direct for purely visual tabletop tasks.",
            },
            {
                "rank": 8,
                "title": "Coverage Aware Active Evaluation for Failure Discovery with Paired Systems",
                "arxiv_id": "2608.13719",
                "fit": "failure discovery - proxy systems - target-risk selection",
                "status": "Tier A - abstract-only",
                "status_quo": "Autonomous-system testing often samples real target failures sparsely because target evaluations are expensive.",
                "friction": "Proxy failures from simulators or related policies do not transfer cleanly to the real target system.",
                "hidden_premise": "Proxy signals are useful only after a local residual model corrects their target-risk error and keeps scenario coverage realistic.",
                "conceptual_move": "Combine proxy evaluations with limited target results to actively select diverse, well-supported failure scenarios.",
                "mechanism": "The abstract describes control-variate-inspired residual modeling and a support-aware mutual-information objective.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The method learns a local predictor of target risk by correcting proxy failure signals."},
                    {"trace": "[Abstract]", "claim": "Across driving, manipulation, and quadruped tasks, it discovers up to two times as many failures as random sampling and active-learning baselines."},
                    {"trace": "[Inference]", "claim": "APRL should report which proxy failures transferred and which target failures proxies missed."},
                ],
                "falsification": "If proxy correction overfits early target failures, it may stop discovering rare but severe new modes.",
                "adversarial": "Use proxy systems with systematic blind spots and hold out one failure family from initial target labels.",
                "thinking_tool": "Spend real robot tests where proxy disagreement and scenario support jointly predict severe failure.",
                "transfer_boundary": "Strong for expensive robot or driving evaluations; weaker when target tests are already cheap and exhaustive.",
            },
        ],
        "synthesis": [
            {
                "title": "Process interfaces are becoming the unit of VLA evaluation",
                "links": "ART - PRM-as-a-Judge - BICPO-VLA - ReflexVLA",
                "facts": "The papers expose tool calls, progress curves, request-to-handoff state, and reaction latency as measurable decision interfaces.",
                "inference": "APRL should evaluate which interface changes action authority before accepting an end-to-end VLA improvement.",
            },
            {
                "title": "World models are being asked to preserve predicates, not only pixels",
                "links": "OpenBelief-Nav - hint2 - Onto-EV-WM - Marionette",
                "facts": "The batch preserves observation provenance, temporal-logic propositions, failed predicate arguments, and explicit world state.",
                "inference": "Robot-useful world models should be judged by the belief or predicate that changes a route, repair, or safety decision.",
            },
            {
                "title": "Failure evaluation is shifting from score averages to certified event coverage",
                "links": "SSP - coverage-aware active evaluation - aTTC-CBF - tube safety certificates",
                "facts": "The papers define matched safety events, target-risk sampling, anticipatory time-to-collision, and route safety tubes.",
                "inference": "A deployment benchmark should state which event was preserved, which correction is allowed, and which failure family remains uncovered.",
            },
        ],
        "frontier_memory": [
            {
                "label": "Strengthening",
                "history": "August 14 emphasized pre-commit evidence, active evidence acquisition, and world-model transfer diagnostics.",
                "body": "August 17 strengthens the same commitment-before-action axis with VLA tool routing, PRM process curves, temporal-logic guidance, and proxy-corrected failure discovery.",
            },
            {
                "label": "New signal",
                "history": "Recent notes treated robot memory mostly as navigation or VLA state.",
                "body": "OpenBelief-Nav and Onto-EV-WM add a sharper requirement: keep provenance, predicate arguments, and verification results until the robot knows which action needs them.",
            },
            {
                "label": "Missing axis",
                "history": "Prior editions repeatedly called for robot-usable geometry and safety diagnostics.",
                "body": "The current batch still lacks a shared protocol that joins geometry degradation, monitor authority, and closed-loop recovery in the same robot task.",
            },
        ],
        "strategy": [
            {
                "priority": "Build moat",
                "title": "Commitment-interface VLA benchmark",
                "thesis": "Measure whether tool calls, process curves, progress probes, handoff states, and reaction-latency controls actually veto or alter robot actions.",
                "scores": {"fit": 5, "novelty": 5, "feasibility": 4, "moat": 5, "timing": 5, "evidence": 5},
                "one_week": "Select two manipulation tasks with low light, moving objects, and delayed handoff; log tool calls, progress curves, action chunks, and reaction latency.",
                "four_week": "Compare ART-style tool routing, PRM process judging, BICPO handoff adaptation, and Reflex-style future prediction on identical episodes.",
                "success": "At least one interface predicts or prevents a failure with usable lead time while preserving success on non-failure episodes.",
                "stop": "Interfaces correlate only with final success and cannot identify which next action should change.",
                "asset": "Paired videos, action chunks, tool-call traces, PRM curves, latency schedules, handoff-state labels, and veto outcomes.",
            },
            {
                "priority": "Explore",
                "title": "Predicate-preserving robot world memory",
                "thesis": "Build a navigation/manipulation memory that keeps observation provenance, competing object beliefs, temporal-logic state, and failed predicate arguments until action time.",
                "scores": {"fit": 5, "novelty": 5, "feasibility": 3, "moat": 5, "timing": 4, "evidence": 5},
                "one_week": "Construct five ambiguous object-goal scenes and two predicate-repair manipulation cases with retained frame-mask provenance and task predicates.",
                "four_week": "Compare early-commit labels, belief-preserving memory, LTL-guided policy checks, and ontology-gated repair on the same tasks.",
                "success": "Preserved evidence changes target selection or repair acceptance in cases where early commitment fails.",
                "stop": "Provenance and predicates increase bookkeeping but do not alter route, repair, or stop decisions.",
                "asset": "Belief records, frame-mask provenance, predicate traces, repair attempts, verification outcomes, and action-difference logs.",
            },
            {
                "priority": "Exploit",
                "title": "Matched-event failure discovery harness",
                "thesis": "Own a testing harness where synthetic, simulated, proxy, and physical runs preserve the same event contract before failure rates are compared.",
                "scores": {"fit": 5, "novelty": 4, "feasibility": 4, "moat": 5, "timing": 5, "evidence": 5},
                "one_week": "Define one driving or UAV event with topology, participant roles, timing, risk response, and allowed corrections preserved across proxy and target tests.",
                "four_week": "Implement SSP-style event transfer audits plus coverage-aware target selection and a temporal-barrier or tube-certificate baseline.",
                "success": "The harness finds a severe target failure missed by random or proxy-only sampling and explains which event field caused transfer failure.",
                "stop": "Event matching is too loose to distinguish domain sensitivity from scenario-content changes.",
                "asset": "Event specs, transfer audits, proxy/target paired outcomes, risk residuals, coverage maps, and certificate violation cases.",
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
