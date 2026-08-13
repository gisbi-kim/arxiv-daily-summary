#!/usr/bin/env python3
"""Generate the 2026-08-13 Research Intelligence edition."""

from __future__ import annotations

import json
from pathlib import Path

from gen_research_intelligence_20260811 import build_html


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PROMPT = "prompts/instruction_v20260713.md"


RI_BY_DATE = {
    "2026-08-13": {
        "date": "2026-08-13",
        "edition": "Research Intelligence",
        "source_prompt": SOURCE_PROMPT,
        "source_mode": "new",
        "scope_note": (
            "Daily edition from matching Thursday /new listings: 126 non-replacement cs.CV rows, "
            "28 cs.RO rows, 152 deduplicated papers, and 121 ROI papers. Tier A cards are conservative "
            "abstract-only autopsies from the repository parser output; no figure/table claims are asserted."
        ),
        "executive_thesis": (
            "The August 13 batch says that robotics progress is moving from larger end-to-end policies toward "
            "auditable execution contracts. StellaVLA, G0.5, MiDAS, and OpenVLA failure monitors ask what evidence "
            "should be carried into a new task and when adaptation should stop. RISC, neuro-symbolic driving guards, "
            "counterfactual driving world models, and RoadWeaver ask whether evaluation covers the safety slice that "
            "will actually fail. DreamFly, DaViNCi, D3D-GEN, Map-Det3D, Seed2GS, and GeoUniPR shift 3D and navigation "
            "work toward memory, reachability, and dynamic-world stress. APRL should turn this into logged probes: "
            "which evidence changes the action, which monitor warns early, and which map or simulator state is trusted "
            "enough to drive a robot decision."
        ),
        "decision_cards": [
            {
                "label": "Decision",
                "title": "Adaptation needs evidence, not only more demonstrations",
                "body": (
                    "StellaVLA, MiDAS, G0.5, HandEdit, and OpenVLA failure monitoring all separate reusable task "
                    "structure from raw trajectory imitation."
                ),
            },
            {
                "label": "Decision",
                "title": "Driving evaluation is becoming slice and rule aware",
                "body": (
                    "RISC, neuro-symbolic safety guards, counterfactual driving world models, TrafficDiffuser, "
                    "RoadWeaver, and real-world behavior planning all expose the limits of aggregate driving scores."
                ),
            },
            {
                "label": "Decision",
                "title": "3D memory must be executable",
                "body": (
                    "DreamFly, DaViNCi, D3D-GEN, Map-Det3D, Seed2GS, and GeoUniPR make maps and generated worlds "
                    "useful only when they change navigation, grounding, localization, or simulator coverage."
                ),
            },
        ],
        "papers": [
            {
                "rank": 1,
                "title": "StellaVLA: In-Context Structured Demonstration for Generalizable Vision-Language-Action Models",
                "arxiv_id": "2608.11671",
                "fit": "VLA test-time adaptation - structured demonstrations - cross-embodiment transfer",
                "status": "Tier A - abstract-only",
                "status_quo": "VLA adaptation often means collecting more task data or fine-tuning after the policy fails out of distribution.",
                "friction": "A raw demonstration can show what happened without explaining the task plan, sub-goals, or 3D motion that should transfer to a new embodiment.",
                "hidden_premise": "A retrieved trajectory becomes reusable only if it is converted into structured task evidence rather than copied as pixels and actions.",
                "conceptual_move": "Use an offline pipeline to turn a raw trajectory into a task plan, sub-goal descriptions, and verbalized 3D motion for in-context VLA guidance.",
                "mechanism": "The abstract describes structured demonstrations, a dual training design, and inference through the action expert alone to preserve real-time control.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper states that VLA performance often collapses when scene, viewpoint, or object differs from training."},
                    {"trace": "[Abstract]", "claim": "It converts raw trajectories into structured demonstrations at zero human-annotation cost."},
                    {"trace": "[Inference]", "claim": "APRL should log which part of a demonstration transfers: plan, sub-goal, motion phrase, or action residual."},
                ],
                "falsification": "If structured demonstrations help only when retrieved scenes closely match training scenes, the method is retrieval similarity rather than reasoning transfer.",
                "adversarial": "Cross-embodiment transfer needs object, camera, and gripper mismatches; otherwise the structure could hide ordinary imitation bias.",
                "thinking_tool": "Treat demonstrations as decomposed evidence objects instead of trajectories to replay.",
                "transfer_boundary": "Strong for VLA manipulation and XR/human-hand transfer; weaker for tasks where language plans are not the bottleneck.",
            },
            {
                "rank": 2,
                "title": "G0.5: One Autoregressive Stream for Robot Reasoning and Action",
                "arxiv_id": "2608.11739",
                "fit": "autoregressive VLA - reasoning tokens - action tokenizer",
                "status": "Tier A - abstract-only",
                "status_quo": "Many VLA systems use a pretrained VLM as a context encoder and rely on a separate action expert for control.",
                "friction": "Separating reasoning and action can make prompts steer text while the executable policy follows a different representation path.",
                "hidden_premise": "Robot reasoning becomes more controllable if task decomposition, object grounding, action hints, and action tokens share one training stream.",
                "conceptual_move": "Emit reasoning and action tokens from a single autoregressive transformer with a cross-embodiment action tokenizer and visual memory.",
                "mechanism": "The abstract names a shared action vocabulary, native chain-of-thought stream, and multi-second visual memory through the vision encoder.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper says the current recipe makes the VLM a context encoder rather than a decision-maker."},
                    {"trace": "[Abstract]", "claim": "It interleaves task decomposition, object grounding, action hints, and action tokens under one objective."},
                    {"trace": "[Inference]", "claim": "APRL should test whether prompt changes alter action granularity and horizon under the same visual state."},
                ],
                "falsification": "If reasoning tokens are fluent but do not predict action changes, the shared stream is an explanation layer rather than a control interface.",
                "adversarial": "Chain-of-thought steering can create brittle prompt dependence; evaluate with equivalent instructions and object distractors.",
                "thinking_tool": "Ask whether a reasoning token has motor authority before treating it as robotics evidence.",
                "transfer_boundary": "Strong for language-conditioned robot policies; less direct for low-level controllers without tokenized actions.",
            },
            {
                "rank": 3,
                "title": "Adaptation of Generalist Robot Policies with Minimal Data",
                "arxiv_id": "2608.11363",
                "fit": "minimal-data adaptation - offline-to-online RL - residual policy",
                "status": "Tier A - abstract-only",
                "status_quo": "Fully autonomous robot learning remains blocked by sparse rewards and weak zero-shot exploration.",
                "friction": "A generalist policy can know many behaviors yet still fail to discover the first successful trajectory for a new task.",
                "hidden_premise": "One or a few demonstrations can anchor the target task enough for autonomous online improvement to become feasible.",
                "conceptual_move": "Use behavior cloning on single/few demonstrations, then value-based online RL over a residual policy parameterization.",
                "mechanism": "The abstract frames MiDAS as an offline-to-online recipe evaluated on LIBERO and RoboCasa.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper defines minimal-data adaptation as one demonstration followed by autonomous online interaction."},
                    {"trace": "[Abstract]", "claim": "It combines behavior cloning anchoring with value-based online RL on a residual policy."},
                    {"trace": "[Inference]", "claim": "APRL should measure how much human guidance is needed before online exploration becomes non-random."},
                ],
                "falsification": "If residual RL improves only demonstrated variations, it has not crossed into autonomous improvement.",
                "adversarial": "Sparse reward success can hide unsafe exploration; compare intervention count, failure type, and recovery trajectory.",
                "thinking_tool": "Use one-demo bootstrapping as a measurable proxy for autonomous robot improvement.",
                "transfer_boundary": "Strong for manipulation benchmarks with resettable online interaction; weaker for safety-critical hardware without cheap exploration.",
            },
            {
                "rank": 4,
                "title": "Early Warning Signals for OpenVLA Failure under Visual Distribution Shift",
                "arxiv_id": "2606.29699",
                "fit": "VLA failure monitoring - visual distribution shift - internal activations",
                "status": "Tier A - abstract-only",
                "status_quo": "VLA failures are often diagnosed after the task has already failed under visual shift.",
                "friction": "A fixed policy can show confident actions while internal activations already contain near-term failure evidence.",
                "hidden_premise": "Lightweight probes on feedforward activations can forecast failure without changing the deployed OpenVLA policy.",
                "conceptual_move": "Train post-hoc monitors on execution activations and ask whether they predict failure within a fixed horizon.",
                "mechanism": "The abstract logs OpenVLA activations in LIBERO rollouts and fits lightweight monitors after collection.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "Occlusion reduces OpenVLA success from 57 percent to 17 percent over 100 episodes per condition."},
                    {"trace": "[Abstract]", "claim": "A logistic probe at layer 16 reaches AUROC 0.972 for predicting failure within a 15 step horizon under occlusion."},
                    {"trace": "[Inference]", "claim": "APRL should collect warning lead time before evaluating only task success."},
                ],
                "falsification": "If the monitor fires only after irreversible contact or does not transfer to other visual shifts, it is a shift detector rather than a failure warning.",
                "adversarial": "Occlusion is only one stressor; color, camera jitter, viewpoint, and object identity should separate benign shift from task failure.",
                "thinking_tool": "Treat internal activations as early warning sensors with lead-time metrics.",
                "transfer_boundary": "Strong for feedforward VLA policies with accessible activations; weaker for black-box closed models.",
            },
            {
                "rank": 5,
                "title": "Do Not Forget the Obvious - RISC: A Risk-Informed Slice-Coverage Protocol for Safe Autonomous Driving",
                "arxiv_id": "2608.12051",
                "fit": "risk-informed driving evaluation - slice coverage - audit budget",
                "status": "Tier A - abstract-only",
                "status_quo": "Aggregate autonomous-driving metrics can look acceptable while high-risk conditions remain under-audited.",
                "friction": "A finite validation budget must choose which weather, scene, actor, and perception slices deserve manual or model audit.",
                "hidden_premise": "Safety concerns can be translated into machine-readable risk slices and coverage-qualified reports.",
                "conceptual_move": "Use risk-guided stress testing plus explicit coverage statements about sufficiently and insufficiently covered slices.",
                "mechanism": "The abstract describes lightweight signals for candidate tagging, compact audit selection by risk, and coverage-qualified reporting.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper says aggregate metrics may not reflect insufficiently examined high-risk conditions."},
                    {"trace": "[Abstract]", "claim": "It instantiates RISC for monocular pedestrian perception using 1,000 frames and a detector proxy."},
                    {"trace": "[Inference]", "claim": "APRL should make every driving or robot benchmark publish uncovered risk slices next to the score."},
                ],
                "falsification": "If risk slices are broad or manually chosen after results, coverage qualification can become a reporting label rather than a stress protocol.",
                "adversarial": "LLM-supported slice discovery should be audited for missed obvious conditions and hallucinated irrelevant slices.",
                "thinking_tool": "Every score needs a coverage statement for the risk it does not measure.",
                "transfer_boundary": "Strong for perception, driving, and robotics benchmarks with finite audit sets.",
            },
            {
                "rank": 6,
                "title": "Herding End-to-End Autonomous Driving via Neuro-Symbolic Safety Guards",
                "arxiv_id": "2608.11451",
                "fit": "driving safety guard - command interface - traceable intervention",
                "status": "Tier A - abstract-only",
                "status_quo": "End-to-end driving agents can achieve high average performance while violating basic traffic rules.",
                "friction": "A learned agent may not expose or enforce the physical conditions that make a command safe.",
                "hidden_premise": "A non-learned rule guard can improve safety if it sits at the final command interface and changes only unsafe actions.",
                "conceptual_move": "Attach a lightweight neuro-symbolic guard that checks commands against explicit rules and replaces unsafe commands with nearest safe alternatives.",
                "mechanism": "The abstract reports that each intervention is executable and traceable to the triggering rule without retraining.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The guard attaches immediately before commands reach the vehicle."},
                    {"trace": "[Abstract]", "claim": "It reports 15 percent Success Rate improvement and up to 53 percent fewer safety-critical collisions in evaluated benchmarks."},
                    {"trace": "[Inference]", "claim": "APRL should log every rule intervention as a counterfactual action label."},
                ],
                "falsification": "If guards preserve benchmark score by over-constraining rare maneuvers, they may hide autonomy limits rather than solve them.",
                "adversarial": "Rules must handle conflicts, sensor uncertainty, and off-policy recovery after intervention.",
                "thinking_tool": "Put a traceable contract at the final command boundary.",
                "transfer_boundary": "Strong for driving and mobile robots with explicit command interfaces; weaker for high-dimensional manipulation without simple safety alternatives.",
            },
            {
                "rank": 7,
                "title": "How Can Driving World Models Do Counterfactual Prediction?",
                "arxiv_id": "2608.11601",
                "fit": "driving world model - counterfactual prediction - abduction action prediction",
                "status": "Tier A - abstract-only",
                "status_quo": "Driving world models are often treated as counterfactual simulators for alternative ego actions.",
                "friction": "Direct action-conditioned prediction can ignore the factual continuation and produce a plausible future that is not the counterfactual for this episode.",
                "hidden_premise": "Counterfactual driving prediction needs abduction from observed evidence before applying the alternative action.",
                "conceptual_move": "Formalize the gap using abduction, action, and prediction, then build controlled factual and matched counterfactual outcomes.",
                "mechanism": "The abstract evaluates two representative world models and introduces a training-free pipeline that moves observed evidence into the counterfactual view.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper identifies a mismatch between counterfactual simulation and direct action-conditioned prediction."},
                    {"trace": "[Abstract]", "claim": "It constructs a controlled simulation benchmark with factual and matched counterfactual outcomes."},
                    {"trace": "[Inference]", "claim": "APRL should require factual evidence preservation before using a world model for intervention planning."},
                ],
                "falsification": "If abduction helps only on short horizons where other agents do not respond, the result may not scale to interactive traffic.",
                "adversarial": "Longer horizons and social response break the assumption that surrounding agents evolve independently of the ego change.",
                "thinking_tool": "Counterfactual prediction must preserve what actually happened before imagining what could have happened.",
                "transfer_boundary": "Strong for driving evaluation and replay; less direct for manipulation unless factual rollouts have matched counterfactual labels.",
            },
            {
                "rank": 8,
                "title": "DreamFly: Causal Memory and Receding-Horizon Diffusion Planning for Aerial Vision-Language Navigation",
                "arxiv_id": "2608.12308",
                "fit": "aerial VLN - causal memory - receding-horizon diffusion planning",
                "status": "Tier A - abstract-only",
                "status_quo": "Aerial VLN agents must integrate partial observations, plan ahead, and decide when to stop under limited history.",
                "friction": "Implicit history and termination can leak future evidence or stop for the wrong reason in partially observable navigation.",
                "hidden_premise": "Navigation planning can use future action chunks as auxiliary targets while executing only one action before replanning.",
                "conceptual_move": "Combine causally aligned historical memory with receding-horizon diffusion planning and action-logit stop estimation.",
                "mechanism": "The abstract describes plan-K execute-one replanning, LiteStop, and memory that uses only observations before the current decision step.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper names limited historical context, short planning horizons, and unreliable implicit termination as aerial VLN challenges."},
                    {"trace": "[Abstract]", "claim": "It uses causally aligned historical memory and receding-horizon diffusion planning."},
                    {"trace": "[Inference]", "claim": "APRL should evaluate whether memory improves stop decisions and not only path success."},
                ],
                "falsification": "If the stop signal improves in static scenes but fails with dynamic distractors, causal memory is not sufficient for outdoor deployment.",
                "adversarial": "Plan-K execute-one can still optimize short-horizon visibility unless routes include occlusion and dynamic elements.",
                "thinking_tool": "Use future action chunks as planning scaffolds, not commitments.",
                "transfer_boundary": "Strong for aerial and mobile navigation; weaker for contact manipulation unless a replanning horizon is explicit.",
            },
        ],
        "synthesis": [
            {
                "title": "VLA adaptation is becoming an evidence-routing problem",
                "links": "StellaVLA - G0.5 - MiDAS - OpenVLA warning signals",
                "facts": "The papers use structured demonstrations, shared reasoning/action tokens, one-demo online RL, and activation probes.",
                "inference": "APRL should compare which evidence source changes the action before adding larger task datasets.",
            },
            {
                "title": "Driving world models need factual anchors and rule exits",
                "links": "RISC - safety guards - counterfactual world models - RoadWeaver",
                "facts": "The papers focus on risk slices, traceable command interventions, factual counterfactual alignment, and scalable simulator maps.",
                "inference": "The useful driving benchmark records which slice, rule, or factual continuation controlled the decision.",
            },
            {
                "title": "3D and navigation assets are shifting toward executable memory",
                "links": "DreamFly - DaViNCi - D3D-GEN - Map-Det3D - Seed2GS",
                "facts": "The papers tie memory, dynamic elements, simulator generation, metric reconstruction, and object extraction to downstream decisions.",
                "inference": "APRL should evaluate maps by action, stop, and target changes under corrupted or missing evidence.",
            },
        ],
        "frontier_memory": [
            {
                "label": "Strengthening",
                "history": "August 12 emphasized update, reject, cache, retrieve, and intervene decisions.",
                "body": "August 13 strengthens this into explicit adaptation, warning, safety-guard, and risk-slice contracts.",
            },
            {
                "label": "New signal",
                "history": "Recent editions treated geometry as an execution substrate.",
                "body": "Today adds generated simulator worlds and camera-free 3DGS object extraction as map assets that must be tested through decisions.",
            },
            {
                "label": "Missing axis",
                "history": "Prior VLA notes focused on action routing and cache invalidation.",
                "body": "The current batch still lacks a shared benchmark for when a robot should trust, revise, or discard a retrieved demonstration.",
            },
        ],
        "strategy": [
            {
                "priority": "Build moat",
                "title": "Evidence-routed VLA adaptation benchmark",
                "thesis": "Build a benchmark where each VLA adaptation step is traced to demonstration structure, reasoning tokens, one-demo RL, or activation warnings.",
                "scores": {"fit": 5, "novelty": 5, "feasibility": 4, "moat": 5, "timing": 5, "evidence": 5},
                "one_week": "Create paired LIBERO or RoboCasa tasks with one raw demo, one structured demo, and one activation-warning log.",
                "four_week": "Compare Stella-style structure, G0.5-style reasoning/action traces, MiDAS residual adaptation, and failure probes under object/viewpoint shifts.",
                "success": "The benchmark predicts which evidence source changes the action before the first failed contact in at least two task families.",
                "stop": "All methods improve only final success while evidence traces fail to predict recovery or unsafe actions.",
                "asset": "Structured demonstrations, action-token logs, residual adaptation traces, warning lead-time labels, and task-shift splits.",
            },
            {
                "priority": "Explore",
                "title": "Risk-slice and guard contract for closed-loop driving",
                "thesis": "Unify RISC slice coverage, neuro-symbolic guard interventions, and counterfactual world-model evidence in one closed-loop audit protocol.",
                "scores": {"fit": 4, "novelty": 5, "feasibility": 4, "moat": 4, "timing": 5, "evidence": 5},
                "one_week": "Choose three obvious high-risk slices and define the rule or factual evidence that should change the planner command.",
                "four_week": "Replay the same episodes through a world model, a safety guard, and a learned planner, then report uncovered slices and command substitutions.",
                "success": "At least one guard or factual-anchor signal prevents a failure that aggregate driving score hides.",
                "stop": "Coverage statements do not change audit selection, command intervention, or failure discovery.",
                "asset": "Risk-slice schema, command-substitution log, factual/counterfactual pairs, and coverage-qualified scorecards.",
            },
            {
                "priority": "Build moat",
                "title": "Executable 3D memory stress suite",
                "thesis": "Evaluate 3D maps, generated worlds, and navigation memory by whether corrupted evidence changes target, stop, route, or base-placement decisions.",
                "scores": {"fit": 5, "novelty": 5, "feasibility": 3, "moat": 5, "timing": 4, "evidence": 5},
                "one_week": "Assemble one indoor and one outdoor scene with object distractors, dynamic movers, and missing-view 3D evidence.",
                "four_week": "Compare DreamFly-style memory, DaViNCi dynamic navigation, Seed2GS object extraction, Map-Det3D metric priors, and generated simulator scenes.",
                "success": "Evidence corruption predicts a measurable route, stop, target, or base-placement change before final success drops.",
                "stop": "3D or memory assets improve visualization quality but do not affect executable robot choices.",
                "asset": "Evidence-corrupted 3D scenes, route and stop labels, map-update logs, target masks, and simulator-state manifests.",
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
