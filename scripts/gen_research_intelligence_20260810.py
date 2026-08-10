#!/usr/bin/env python3
"""Generate the 2026-08-10 Research Intelligence edition."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PROMPT = "prompts/instruction_v20260713.md"


RI_BY_DATE = {
    "2026-08-10": {
        "date": "2026-08-10",
        "edition": "Research Intelligence",
        "source_prompt": SOURCE_PROMPT,
        "source_mode": "new",
        "scope_note": (
            "Daily edition from matching Monday /new listings: 102 non-replacement cs.CV rows, "
            "40 cs.RO rows, 132 deduplicated papers, and 112 ROI papers. Tier A cards use official "
            "arXiv abstract pages; official arXiv HTML was available for AtlasVLA, PSG-JEPA, "
            "AutoIntervene, TEMPO, planning-token pruning, and the accessibility-field paper."
        ),
        "executive_thesis": (
            "The August 10 batch is about making robot policies accountable to persistent state rather "
            "than plausible next frames or smooth action chunks. AtlasVLA adds world-ego memory to VLA "
            "control, PSG-JEPA asks whether latent prediction carries physical state, AutoIntervene "
            "turns action support into a deployment switch, WNM-3D routes 3D scene context into VLN, "
            "and distractor-augmented VPR shows that a retrieval score can reward the wrong variable. "
            "APRL should turn these papers into a state-to-action audit: memory, geometry, intervention, "
            "and compression are useful only when they change a robot decision under stress."
        ),
        "decision_cards": [
            {
                "label": "Decision",
                "title": "Persistent state is now a control variable",
                "body": (
                    "AtlasVLA and WNM-3D both reject single-frame reactivity: the useful question is "
                    "whether a world or navigation memory changes the next action when evidence leaves view."
                ),
            },
            {
                "label": "Decision",
                "title": "World models need physical probes",
                "body": (
                    "PSG-JEPA and TaskSense imply that forward prediction and reconstruction are weak "
                    "objectives unless the latent can expose proprioceptive state or task-relevant regions."
                ),
            },
            {
                "label": "Decision",
                "title": "Evaluation must attack shortcut variables",
                "body": (
                    "VPR distractors, intervention thresholds, viewpoint shifts, and planning-token pruning "
                    "all ask whether the measured success is attached to identity, state, or only conditions."
                ),
            },
        ],
        "papers": [
            {
                "rank": 1,
                "title": "AtlasVLA: Persistent World-Ego State Modeling for Vision-Language-Action Models",
                "arxiv_id": "2608.06729",
                "fit": "VLA execution memory - world state - ego task progress",
                "status": "Tier A - official arXiv abstract and HTML checked",
                "status_quo": "Many VLA policies remain reactive, conditioning the next action on the current observation and instruction.",
                "friction": "A wrist-camera robot loses objects outside the field of view and loses task progress during long-horizon execution.",
                "hidden_premise": "A persistent spatial memory and an ego-progress memory can be made action-relevant without requiring multiple live cameras.",
                "conceptual_move": "Lift transient wrist observations into a voxel-hashed 4D world state and pair it with an ego-working state memory for the policy.",
                "mechanism": "The abstract reports a dual-memory architecture that conditions a diffusion transformer on persistent world-ego state.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper names perception forgetting and temporal task-progress forgetting as the bottlenecks."},
                    {"trace": "[Abstract]", "claim": "It claims a 4D Persistent World State Memory plus Ego-Working State Memory improves LIBERO, RLBench, and real-world manipulation."},
                    {"trace": "[Inference]", "claim": "APRL should test memory usefulness by removing objects from view and measuring action changes before final failure."},
                ],
                "falsification": "If the persistent state does not improve recovery after occlusion, viewpoint change, or multi-step interruption, it is only an expensive context cache.",
                "adversarial": "Memory can hide benchmark priors, so success should be split by object exit, revisit, phase boundary, and recovery segment.",
                "thinking_tool": "Treat memory as a hypothesis about hidden task state, not as an extra perception feature.",
                "transfer_boundary": "Direct for manipulation and long-horizon tasks; weaker for purely reactive contact servoing where the state is fully observed.",
            },
            {
                "rank": 2,
                "title": "Is Forward Prediction Enough? Physical State Grounding for JEPA World Models",
                "arxiv_id": "2608.06799",
                "fit": "world model - latent grounding - proprioceptive state",
                "status": "Tier A - official arXiv abstract and HTML checked",
                "status_quo": "JEPA-style world models often optimize action-conditioned latent prediction rather than explicit robot-state identifiability.",
                "friction": "A latent can predict the next embedding while failing to expose joint state or state change needed by a planner.",
                "hidden_premise": "A useful world model should make physical state readable from individual latents and multi-horizon state change readable from latent pairs.",
                "conceptual_move": "Add proprioceptive-state and joint-angle-change grounding losses during training while keeping inference cost unchanged.",
                "mechanism": "The abstract states that PSG-JEPA adds two grounding objectives and evaluates probing, frozen-latent planning, and policy learning.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper directly asks whether forward prediction alone enforces reliable physical-state identifiability."},
                    {"trace": "[Abstract]", "claim": "It evaluates latent identifiability, goal-conditioned planning, simulation policy learning, and real-robot policy learning."},
                    {"trace": "[Inference]", "claim": "APRL should require a frozen-latent physical-state probe before trusting a world model for control."},
                ],
                "falsification": "If latent probes improve while planning and policy learning do not, physical grounding is diagnostic but not operational.",
                "adversarial": "Proprioceptive probes may overfit robot morphology, so cross-object and cross-task transfer should be separated.",
                "thinking_tool": "Ask whether the world model latent contains the state variable the controller will actually use.",
                "transfer_boundary": "Strong for robot world models and model-based control; less direct for video-only generation without action consumption.",
            },
            {
                "rank": 3,
                "title": "AutoIntervene: Calibrated Intervention for Action-Chunking Imitation Learning Policies",
                "arxiv_id": "2608.07065",
                "fit": "deployment intervention - action support memory - operator handoff",
                "status": "Tier A - official arXiv abstract and HTML checked",
                "status_quo": "Action-chunking policies can keep producing smooth chunks after perception or execution drift leaves the demonstration distribution.",
                "friction": "Smoothness can mask state inconsistency, so the system needs a calibrated handoff before damage accumulates.",
                "hidden_premise": "Support should be measured jointly in visual state and proposed action space, with separate thresholds for taking and returning control.",
                "conceptual_move": "Compare proposed chunks against a visual-action support memory from successful executions and use quantile-calibrated transfer thresholds.",
                "mechanism": "The abstract describes phase-local support for policy-to-operator transfer and global support for operator-to-policy return.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper names perception errors and execution drift as failure modes for action chunks."},
                    {"trace": "[Abstract]", "claim": "It calibrates separate switching thresholds from held-out expert demonstration score quantiles."},
                    {"trace": "[Inference]", "claim": "APRL should log intervention segments as training data only when they cover learner-induced states."},
                ],
                "falsification": "If support scores do not predict recoverable failure earlier than task failure, intervention is reactive teleoperation rather than policy governance.",
                "adversarial": "Operator return can bias the learner toward easy recovery states unless phase labels and failed interventions are retained.",
                "thinking_tool": "Measure whether confidence changes the controller authority, not only whether it correlates with success.",
                "transfer_boundary": "Direct for action-chunking imitation policies; less direct for policies without operator recovery or chunked action output.",
            },
            {
                "rank": 4,
                "title": "WNM-3D: A World Navigation Model with 3D Scene Conditioning for Closed-Loop VLN",
                "arxiv_id": "2608.07267",
                "fit": "vision-language navigation - 3D scene prefix - world-action diffusion",
                "status": "Tier A - official arXiv abstract checked; official /html returned 404 during this run",
                "status_quo": "VLN systems increasingly adapt VLMs into action policies without explicitly modeling how observations should evolve under motion.",
                "friction": "Action-centric training can follow language while ignoring geometry that determines which future view should appear after movement.",
                "hidden_premise": "A frozen geometry encoder can consolidate egocentric RGB history into a 3D scene prefix that conditions future video-action blocks.",
                "conceptual_move": "Feed geometry-aware tokens into a world-action diffusion transformer through block-causal attention for closed-loop VLN.",
                "mechanism": "The abstract describes monocular history, a 3D Scene-to-Token Adapter, and joint future-view/action generation.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper argues existing WAMs for continuous VLN lack geometry-aware conditioning from observed history."},
                    {"trace": "[Abstract]", "claim": "It proposes a fixed-length 3D scene prefix that conditions every future video-action block."},
                    {"trace": "[Inference]", "claim": "APRL should score whether geometry prefix errors predict wrong turns before navigation failure."},
                ],
                "falsification": "If 3D scene conditioning does not outperform history-only tokens under layout ambiguity, the geometry path is decorative.",
                "adversarial": "A frozen geometry encoder can import reconstruction biases that look like navigation competence in static scenes.",
                "thinking_tool": "Tie every map token to an action or future-view prediction it changes.",
                "transfer_boundary": "Strong for VLN and object navigation; weaker for manipulation unless scene geometry maps to reachable contacts.",
            },
            {
                "rank": 5,
                "title": "TEMPO: Semantic-Action Decoupled RL Post-Training for Vision-Language-Action Models",
                "arxiv_id": "2608.07314",
                "fit": "VLA post-training - semantic/action decoupling - two-timescale RL",
                "status": "Tier A - official arXiv abstract and HTML checked",
                "status_quo": "VLA post-training often applies one update strategy across semantic representations and low-level action modules.",
                "friction": "Fast online RL updates can destabilize pretrained semantic features even when only the action expert needs rapid adaptation.",
                "hidden_premise": "Semantic projection and action expert should be optimized at different rates because they serve different control roles.",
                "conceptual_move": "Freeze the vision-language backbone and use two dedicated RL loops: slow semantic projection updates and fast action expert updates.",
                "mechanism": "The abstract describes semantic-action decoupling, two-timescale RL, CALVIN evaluation, and real-world manipulation tasks.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper identifies distribution mismatch in SFT and uniform RL updates as the post-training problem."},
                    {"trace": "[Abstract]", "claim": "It updates semantic projection infrequently and the action expert frequently to preserve semantic stability."},
                    {"trace": "[Inference]", "claim": "APRL should monitor semantic drift and action improvement as separate curves during RL post-training."},
                ],
                "falsification": "If semantic drift is not lower than uniform RL at equal success, the decoupling does not solve the stated failure.",
                "adversarial": "Freezing the backbone can preserve a wrong semantic prior, so failures need object and instruction-level attribution.",
                "thinking_tool": "Separate what the robot understands from how it converts that understanding into motor correction.",
                "transfer_boundary": "Direct for VLA manipulation post-training; less direct for modular planners whose semantic and action modules are already separate.",
            },
            {
                "rank": 6,
                "title": "Depth-Wise Probing and Pruning of the Planning Token in a Driving Vision-Language-Action Model",
                "arxiv_id": "2608.07361",
                "fit": "driving VLA - planning token - depth pruning",
                "status": "Tier A - official arXiv abstract and HTML checked",
                "status_quo": "A driving VLA may route trajectory planning through the full depth of a language model even when the action signal appears early.",
                "friction": "Semantic intent can be linearly readable before the planning token is in the format expected by the deployed planner.",
                "hidden_premise": "Planner compatibility and semantic decodability are different signals and should be measured layer by layer.",
                "conceptual_move": "Use a trajectory-space logit lens to decode the planning token across 32 decoder layers and prune by angular deviation.",
                "mechanism": "The abstract reports early command decodability, gradual planner compatibility improvement, learned readouts, and layer ranking for pruning.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "Command-probe accuracy reaches 97.7 percent after the first decoder layer, while native planner compatibility improves across depth."},
                    {"trace": "[Abstract]", "claim": "The paper ranks decoder layers by angular deviation induced in the planning token."},
                    {"trace": "[Inference]", "claim": "APRL should distinguish intention availability from controller-usable action format."},
                ],
                "falsification": "If pruned layers fail under closed-loop perturbations despite open-loop compatibility, the token diagnostic misses feedback sensitivity.",
                "adversarial": "Open-loop Avg-L2 can hide rare safety-critical maneuvers, so pruning needs scenario-level failure stratification.",
                "thinking_tool": "Do not ask whether an LLM knows the command; ask when the action representation becomes executable.",
                "transfer_boundary": "Direct for token-based VLA planners; less direct for continuous policies without a discrete planning bottleneck.",
            },
            {
                "rank": 7,
                "title": "Are Visual Place Recognition Models Recognizing Places or Conditions? Distractor-Augmented Evaluation and Condition Suppression",
                "arxiv_id": "2608.06847",
                "fit": "place recognition - distractor evaluation - condition suppression",
                "status": "Tier A - official arXiv abstract checked; official /html returned 404 during this run",
                "status_quo": "Long-term VPR is usually judged by Recall@1 between one query condition and another database condition.",
                "friction": "Crowdsourced map databases can contain distractors that match illumination, weather, or season while depicting the wrong place.",
                "hidden_premise": "A descriptor can be discriminative by encoding condition information, which is useful for matching but harmful for place identity.",
                "conceptual_move": "Introduce Distractor-Augmented Recall and suppress condition information with INLP and LEACE.",
                "mechanism": "The abstract reports ranking reversals under DAR@1 and improvement after condition suppression without reducing standard R@1.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper says method rankings under DAR@1 differ from standard Recall@1."},
                    {"trace": "[Abstract]", "claim": "It reports that condition suppression can improve distractor robustness without reducing R@1."},
                    {"trace": "[Inference]", "claim": "APRL should apply condition distractors to localization and map retrieval before claiming place robustness."},
                ],
                "falsification": "If condition suppression hurts loop-closure precision in mixed real maps, the method trades one shortcut for another.",
                "adversarial": "A suppression method can remove condition evidence that is genuinely needed for localization under appearance change.",
                "thinking_tool": "Attack the nuisance variable that the benchmark quietly rewards.",
                "transfer_boundary": "Strong for place recognition and loop closure; less direct for semantic mapping without retrieval decisions.",
            },
            {
                "rank": 8,
                "title": "Beyond Visibility: Real-Time Surface Accessibility Fields from Sparse LiDAR",
                "arxiv_id": "2608.06412",
                "fit": "robot geometry - surface accessibility - sparse LiDAR",
                "status": "Tier A - official arXiv abstract and HTML checked",
                "status_quo": "3D perception often stops at visibility or reconstruction, leaving tool-specific physical access to later planning heuristics.",
                "friction": "Complete meshes and fixed bases are unrealistic for mobile robots mapping from sparse streaming LiDAR.",
                "hidden_premise": "Accessibility can be represented as a per-point field conditioned on the tool and approach corridor, updated at sensor rate.",
                "conceptual_move": "Evaluate each surface point against rotated tool-geometry kernels and approach-corridor clearance on a scan-centric TSDF.",
                "mechanism": "The abstract describes a GPU accessibility field from sparse LiDAR, collision kernels, and sensor-rate updates.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper distinguishes physical surface accessibility from visibility estimation."},
                    {"trace": "[Abstract]", "claim": "It checks tool collisions and approach-corridor clearance from streaming sparse LiDAR."},
                    {"trace": "[Inference]", "claim": "APRL should evaluate geometry by reachable-contact success rather than map completeness alone."},
                ],
                "falsification": "If accessibility labels do not predict successful approach and contact under sensor sparsity, the field is not robot-usable.",
                "adversarial": "Tool kernels can encode a narrow gripper model, so transfer to different end effectors needs explicit tests.",
                "thinking_tool": "A map is valuable when it names what the robot can physically do next.",
                "transfer_boundary": "Direct for mobile manipulation and inspection; less direct for scene understanding tasks without tool geometry.",
            },
        ],
        "synthesis": [
            {
                "title": "Memory and world models converge on state identifiability",
                "links": "AtlasVLA - PSG-JEPA - WNM-3D",
                "facts": "The papers separately add persistent world-ego state, physical grounding losses, and 3D scene prefixes.",
                "inference": "The common decision is whether hidden state can be recovered early enough to change action choice.",
            },
            {
                "title": "Control authority becomes a measured switch",
                "links": "AutoIntervene - TEMPO - planning-token pruning",
                "facts": "One paper transfers authority to an operator, one separates semantic/action RL rates, and one probes when a planning token becomes executable.",
                "inference": "APRL should instrument controller authority, semantic drift, and action-format readiness as separate deployment signals.",
            },
            {
                "title": "Geometry is useful when it resists shortcut evaluation",
                "links": "VPR distractors - accessibility fields - WNM-3D",
                "facts": "The batch tests whether descriptors encode conditions, surfaces are physically accessible, and navigation uses 3D scene history.",
                "inference": "Map and retrieval benchmarks should include nuisance-variable distractors and contact/navigation consequences.",
            },
        ],
        "frontier_memory": [
            {"label": "Strengthening", "history": "August 7 emphasized evidence-to-action audits.", "body": "August 10 strengthens the same axis by making persistent state, intervention thresholds, and planning-token readiness explicit."},
            {"label": "New signal", "history": "Recent WAM notes focused on future prediction and physical fidelity.", "body": "PSG-JEPA asks for physical-state identifiability inside the latent, not only better rollout quality."},
            {"label": "Missing axis", "history": "Late July and early August geometry notes focused on maps, SLAM, and reconstruction.", "body": "Accessibility fields and VPR distractors add action reachability and nuisance-variable suppression as missing evaluation axes."},
        ],
        "strategy": [
            {
                "priority": "Build moat",
                "title": "Persistent-state VLA failure audit",
                "thesis": "Measure whether world-ego memory, semantic-action decoupling, and action-support thresholds predict failure before the robot loses recoverability.",
                "scores": {"fit": 5, "novelty": 4, "feasibility": 4, "moat": 5, "timing": 5, "evidence": 5},
                "one_week": "Replay one LIBERO-style task with object exit, camera shift, and phase interruption while logging memory state, support score, and action deltas.",
                "four_week": "Build a benchmark that compares reactive VLA, persistent-memory VLA, and intervention-gated VLA under the same recoverability labels.",
                "success": "At least two state signals predict different failure families earlier than task-level failure.",
                "stop": "Memory and support scores collapse to generic confidence and do not change recovery ranking.",
                "asset": "Occlusion/interruption rollouts, state-memory dumps, intervention labels, and action-delta traces.",
            },
            {
                "priority": "Explore",
                "title": "Physical-state world-model probe suite",
                "thesis": "Require latent world models to expose proprioceptive state, state changes, and task-relevant visual regions before using them for planning.",
                "scores": {"fit": 5, "novelty": 4, "feasibility": 3, "moat": 4, "timing": 5, "evidence": 4},
                "one_week": "Add frozen-latent probes for joint state and state change to one existing robot world-model dataset.",
                "four_week": "Compare forward-prediction-only, physical-grounded, and task-attended world models on planning and real-robot transfer.",
                "success": "Probe quality explains planning improvement better than reconstruction loss or visual rollout quality.",
                "stop": "Physical probes improve but downstream planning and policy learning remain unchanged.",
                "asset": "Latent probe scripts, robot-state labels, task-attention masks, and planning success logs.",
            },
            {
                "priority": "Build moat",
                "title": "Robot-usable geometry and shortcut evaluation",
                "thesis": "Turn maps and descriptors into action-facing tests: accessibility, loop-closure distractors, and 3D navigation tokens must change robot decisions.",
                "scores": {"fit": 5, "novelty": 5, "feasibility": 4, "moat": 5, "timing": 4, "evidence": 5},
                "one_week": "Create a small testbed with condition distractors, sparse LiDAR surfaces, and tool-specific approach constraints.",
                "four_week": "Evaluate VPR, semantic mapping, and accessibility-field methods by navigation/contact success rather than standalone map quality.",
                "success": "The benchmark changes method ranking relative to standard retrieval or reconstruction metrics.",
                "stop": "Action-facing metrics track standard metrics so closely that the new labels add no decision value.",
                "asset": "Distractor maps, accessibility labels, tool kernels, and closed-loop navigation/contact traces.",
            },
        ],
    }
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
  <p class="assets"><strong>Asset path</strong> - {esc(item['asset'])}</p>
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
        f"<p><strong>Observed</strong> - {esc(item['facts'])}</p><p><strong>Inference</strong> - {esc(item['inference'])}</p></article>"
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
<header><a class="home" href="../">arXiv Daily Summary</a><h1>{esc(date)} arXiv Research Intelligence</h1>
<p class="lead">{esc(data['executive_thesis'])}</p><p class="scope">{esc(data['scope_note'])}</p></header>
<main>
<h2>Research decisions today</h2><div class="decision-grid">{decisions}</div>
<h2>Paper Reasoning Autopsy</h2>{papers}
<h2>Cross-paper decision synthesis</h2><div class="synthesis-grid">{synthesis}</div>
<h2>Frontier memory</h2><div class="memory-grid">{memory}</div>
<h2>APRL Leading Group Strategy Board</h2>{strategy}
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
