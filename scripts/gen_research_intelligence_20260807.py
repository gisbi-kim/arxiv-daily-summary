#!/usr/bin/env python3
"""Generate the 2026-08-07 Research Intelligence edition."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PROMPT = "prompts/instruction_v20260713.md"


RI_BY_DATE = {
    "2026-08-07": {
        "date": "2026-08-07",
        "edition": "Research Intelligence",
        "source_prompt": SOURCE_PROMPT,
        "source_mode": "new",
        "scope_note": (
            "Daily edition from matching Friday /new listings: 132 non-replacement cs.CV rows, "
            "42 cs.RO rows, 165 deduplicated papers, and 137 ROI papers. Tier A cards use official "
            "arXiv abstract pages plus available official arXiv HTML structure."
        ),
        "executive_thesis": (
            "The August 7 batch asks whether robot policies and world models are grounded in auditable "
            "physical state rather than plausible language, video, or visual similarity. In-Context VLA "
            "argues that low-level control should consume grounded language instead of narrating chain of "
            "thought, World-to-Wrist makes future wrist state a task-conditioned control interface, XEWorld "
            "shows action-conditioned world models still follow visual embodiment similarity, and UQ-Loc "
            "turns LiDAR localization uncertainty into a solver variable. APRL should turn this into an "
            "evidence-to-action audit: every language, future-state, geometry, and failure signal must show "
            "which robot decision it changes."
        ),
        "decision_cards": [
            {
                "label": "Decision",
                "title": "VLA language should be consumed, not performed",
                "body": (
                    "In-Context VLA separates grounded language context from free-form CoT generation, "
                    "which matters because narration can optimize against action timing."
                ),
            },
            {
                "label": "Decision",
                "title": "World models need embodiment and physics audits",
                "body": (
                    "XEWorld and GAUGE both turn attractive future prediction into a test of physical "
                    "correspondence, not just plausible pixels."
                ),
            },
            {
                "label": "Decision",
                "title": "Geometry confidence must reach planning",
                "body": (
                    "UQ-Loc, KILVO, and viewpoint-alignment work make uncertainty, sensor failure, and "
                    "viewpoint shifts explicit enough to route into downstream control."
                ),
            },
        ],
        "papers": [
            {
                "rank": 1,
                "title": "In-Context VLA: Endowing Vision-Language-Action Models with Language via In-Context Post-Training and Agentic Tool Use",
                "arxiv_id": "2608.05738",
                "fit": "VLA control - grounded language - tool acquired evidence",
                "status": "Tier A - official arXiv abstract and HTML structure checked",
                "status_quo": "VLA policies usually imitate action chunks from images and fixed instructions, with language treated as static conditioning.",
                "friction": "Free-form textual CoT can slow closed-loop control and optimize narration instead of action quality.",
                "hidden_premise": "The useful language channel is structured evidence that the policy consumes while still being supervised on actions only.",
                "conceptual_move": "Replace generated reasoning with in-context post-training plus an agentic tool interface for detectors, depth, and VLM evidence.",
                "mechanism": "The abstract states that free-form CoT degrades low-level control and that structured context plus tool use improves manipulation.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper names ungrounded reasoning, latency, and conflicting objectives as reasons CoT hurts control."},
                    {"trace": "[HTML headings]", "claim": "Official HTML includes Method, Why Generative CoT Hurts Low-Level Control, Agentic Tool Use for Grounded Evidence, and In-Context Post-Training."},
                    {"trace": "[Inference]", "claim": "APRL should score whether each language evidence tuple changes the next action under occlusion or distractor shifts."},
                ],
                "falsification": "If structured language context does not outperform direct perception under held-out object, viewpoint, or timing shifts, the language interface is decorative.",
                "adversarial": "Tool queries can leak benchmark-specific priors, so detector/depth/VLM evidence must be ablated separately.",
                "thinking_tool": "Ask whether language is adding executable state, or only producing a human-readable explanation after the policy has already acted.",
                "transfer_boundary": "Strong for instruction-conditioned manipulation; weaker for reactive servo loops where language is not part of the control state.",
            },
            {
                "rank": 2,
                "title": "World-to-Wrist: Task-Conditioned Future Wrist Modeling for Fine-Grained Robot Manipulation",
                "arxiv_id": "2608.05369",
                "fit": "fine manipulation - wrist-local future state - task-conditioned VLA",
                "status": "Tier A - official arXiv abstract and HTML structure checked",
                "status_quo": "Many VLAs treat main-view and wrist-view observations as parallel inputs with no explicit role separation.",
                "friction": "Contact-sensitive manipulation fails when the model cannot anticipate how local wrist evidence will evolve under the task.",
                "hidden_premise": "A compact latent interface can carry task context into future wrist prediction without slowing action generation.",
                "conceptual_move": "Forecast future wrist latents and feed them back as future-aware context for action prediction.",
                "mechanism": "The abstract describes latent modeling tokens, future wrist latents, W2-CoT annotations, and above-80 Hz action generation.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper ties future wrist modeling to progress cues, physical transition cues, and wrist-local evidence."},
                    {"trace": "[HTML headings]", "claim": "Official HTML exposes the main method, experiment, and supplementary structure for the model."},
                    {"trace": "[Inference]", "claim": "APRL should evaluate wrist future state by contact event prediction, not only task success."},
                ],
                "falsification": "If future wrist latents do not predict contact-sensitive failures earlier than raw wrist frames, the extra interface is not justified.",
                "adversarial": "Future-aware context may overfit scripted benchmarks unless contact timing and bimanual transfer are separated.",
                "thinking_tool": "Treat local future state as a control variable with latency and contact-value budgets.",
                "transfer_boundary": "Direct for manipulation with wrist cameras and fine contact; less direct for large-scale navigation without local interaction state.",
            },
            {
                "rank": 3,
                "title": "XEWorld: Can Action-Conditioned World Models Generalize to Unseen Robot Embodiments?",
                "arxiv_id": "2608.05799",
                "fit": "world model - cross-embodiment generalization - physical dynamics",
                "status": "Tier A - official arXiv abstract and HTML structure checked",
                "status_quo": "Action-conditioned world models are often evaluated on the same robot embodiments they saw during training.",
                "friction": "A visually plausible rollout can be driven by robot appearance similarity rather than learned physical dynamics.",
                "hidden_premise": "Held-out embodiments in physically identical scenes reveal whether actions are mapped to dynamics or to pixels.",
                "conceptual_move": "Build a controlled cross-embodiment testbed and evaluate unseen robots under paired physical scenes.",
                "mechanism": "The abstract reports that current models behave like 2D visual pattern matchers and need grounded pixel-space actions plus spatial-temporal alignment.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper reports failure to translate abstract numeric joint actions into coherent visual trajectories for unseen embodiments."},
                    {"trace": "[HTML headings]", "claim": "Official HTML includes action-conditioned embodied world models, benchmarks, cross-embodiment learning, embodiments, and evaluation protocols."},
                    {"trace": "[Inference]", "claim": "APRL should keep robot identity, kinematics, and scene physics separable in world-model tests."},
                ],
                "falsification": "If a world model transfers to held-out embodiments using only appearance-similar robots, it has not shown dynamics abstraction.",
                "adversarial": "Few-shot adaptation can recover appearance while forgetting seen embodiments, so transfer must include retention checks.",
                "thinking_tool": "Separate visual embodiment similarity from physical kinematic similarity before trusting generated rollouts.",
                "transfer_boundary": "Strong for robot world models and cross-embodiment manipulation; less direct for fixed-camera video prediction without actions.",
            },
            {
                "rank": 4,
                "title": "UQ-Loc: Uncertainty-Aware LiDAR Scene Coordinate Regression",
                "arxiv_id": "2608.06307",
                "fit": "LiDAR localization - covariance prediction - uncertainty-weighted registration",
                "status": "Tier A - official arXiv abstract and HTML structure checked",
                "status_quo": "Scene coordinate regression for LiDAR often outputs deterministic coordinates and drops aleatoric uncertainty.",
                "friction": "Downstream localization can treat all scene-coordinate predictions as equally reliable even when geometry is ambiguous.",
                "hidden_premise": "Per-voxel covariance can guide seed scoring and inlier testing inside the registration solver.",
                "conceptual_move": "Add an anisotropic Gaussian covariance head and use uncertainty-weighted SC2-PCR matching with Mahalanobis inliers.",
                "mechanism": "The abstract names the covariance head, NLL training, smoothness regularizer, uncertainty-weighted solver, and ECE calibration metric.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper reports improved 6-DoF localization and calibrated covariances."},
                    {"trace": "[HTML headings]", "claim": "Official HTML includes method and experiment sections for uncertainty-aware SCR."},
                    {"trace": "[Inference]", "claim": "APRL should propagate geometry uncertainty into map matching and recovery decisions."},
                ],
                "falsification": "If covariance estimates do not identify failure-prone voxels under sparse, repetitive, or degraded LiDAR scenes, calibration is not operational.",
                "adversarial": "ECE can look good while localization failures remain clustered in safety-critical map regions.",
                "thinking_tool": "Do not report a pose without the uncertainty path that changed the inlier set.",
                "transfer_boundary": "Direct for LiDAR localization and SLAM front ends; weaker for image-only policies unless uncertainty is made geometric.",
            },
            {
                "rank": 5,
                "title": "GAUGE: A Measurement-Grounded Benchmark for Physical Fidelity in Simulation Engines and Video World Models",
                "arxiv_id": "2608.05948",
                "fit": "physical fidelity - simulator/world-model benchmark - calibrated measurements",
                "status": "Tier A - official arXiv abstract and HTML structure checked",
                "status_quo": "Physics engine and video world model evaluations often rely on perceptual similarity or isolated task scores.",
                "friction": "A generated or simulated rollout can look plausible while violating friction, momentum transfer, self-contact, or deformation parameters.",
                "hidden_premise": "Physical fidelity should be scored against calibrated real trajectories and task-specific observables.",
                "conceptual_move": "Evaluate numerical simulators and generative video world models with one measurement-grounded benchmark.",
                "mechanism": "The abstract describes 22 task families, physical metadata, uncertainty annotations, generalized trajectory errors, and video-model law consistency checks.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper reports no uniformly faithful physics engine and large discrepancies in impulsive contact, textiles, and volumetric deformation."},
                    {"trace": "[HTML headings]", "claim": "Official HTML includes Real-World Validation of Physics Engines, Physical Consistency of Generative World Models, and Physical Parameter Supervision."},
                    {"trace": "[Inference]", "claim": "APRL should pair simulator choice with the physical observable that determines robot policy validity."},
                ],
                "falsification": "If policy success is insensitive to the measured physical discrepancies, the benchmark may not target the right robot decisions.",
                "adversarial": "Video models can fit equation form while missing parameter values, so both trajectory shape and recovered parameters must be checked.",
                "thinking_tool": "Replace visual plausibility with a named physical observable and failure threshold.",
                "transfer_boundary": "Strong for simulation-backed robot learning and video world models; less direct for tasks with no physical trajectory target.",
            },
            {
                "rank": 6,
                "title": "Robust-WAM: Bridging Generative Pretraining and Semantic Foresight in World-Action Models",
                "arxiv_id": "2608.05903",
                "fit": "world-action model - semantic foresight - OOD visual shift",
                "status": "Tier A - official arXiv abstract and HTML structure checked",
                "status_quo": "Video-generation-based WAMs inherit VAE latent spaces optimized for pixel reconstruction.",
                "friction": "Pixel detail can preserve appearance while making action prediction fragile under illumination and visual OOD shifts.",
                "hidden_premise": "Semantic foresight can be aligned into the action stream without discarding generative pretraining.",
                "conceptual_move": "Keep the VAE generative path and add semantic query tokens aligned to future-frame semantics for the action stream.",
                "mechanism": "The abstract names semantic foresight alignment, learnable query tokens, positional encodings for future steps, and OOD robot experiments.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper says semantic latent WAMs are more robust but lose large-scale VGM pretraining, motivating a bridge."},
                    {"trace": "[HTML headings]", "claim": "Official HTML includes World-Action Models, Representation Alignment, Per-Frame Semantic Query Tokens, Semantic Foresight Targets, and Alignment Objective."},
                    {"trace": "[Inference]", "claim": "APRL should test whether semantic foresight predicts action recovery under visual shift, not only video quality."},
                ],
                "falsification": "If semantic foresight improves video features but not action success under illumination or background shift, the bridge is incomplete.",
                "adversarial": "The alignment target can hide dataset semantics that fail on new task objects or camera viewpoints.",
                "thinking_tool": "Ask whether future prediction is attached to the action stream or only to the reconstructed image stream.",
                "transfer_boundary": "Strong for WAM-style robot manipulation; less direct for planners that do not consume future visual latents.",
            },
        ],
        "synthesis": [
            {
                "title": "Grounded evidence replaces verbal explanation",
                "links": "In-Context VLA - World-to-Wrist - Robust-WAM",
                "facts": "The papers move from generated text or pixels toward structured evidence: tool-acquired language, wrist future state, and semantic foresight.",
                "inference": "APRL should log the evidence representation that actually changes the action token or controller command.",
            },
            {
                "title": "Physical validity is becoming the audit surface",
                "links": "XEWorld - GAUGE - UQ-Loc",
                "facts": "The batch tests cross-embodiment dynamics, calibrated physical observables, and localization covariance instead of single aggregate scores.",
                "inference": "A robot benchmark should couple visual/world-model output to physical state variables with falsification thresholds.",
            },
        ],
        "frontier_memory": [
            {"label": "Strengthening", "history": "August 6 focused on evidence-channel validity.", "body": "August 7 strengthens that axis by moving the evidence closer to action timing, wrist state, and localization covariance."},
            {"label": "New signal", "history": "Recent WAM notes emphasized future-state usefulness.", "body": "XEWorld and GAUGE add an explicit physical-fidelity and embodiment-transfer audit."},
            {"label": "Missing axis", "history": "Late July geometry notes emphasized maps and SLAM.", "body": "UQ-Loc and KILVO indicate that confidence and sensor-degradation propagation should become first-class outputs."},
        ],
        "strategy": [
            {
                "priority": "Build moat",
                "title": "Evidence-to-action VLA audit harness",
                "thesis": "Measure which grounded language, wrist-future, geometry, and semantic-foresight signals change the next robot action under perturbation.",
                "scores": {"fit": 5, "novelty": 5, "feasibility": 4, "moat": 5, "timing": 5, "evidence": 5},
                "one_week": "Instrument one manipulation task with language-context ablation, wrist-future masking, visual distractors, and action-token delta logging.",
                "four_week": "Build a reusable benchmark that links each evidence channel to action success, early failure warning, and recovery choice.",
                "success": "At least two evidence channels predict distinct failure families before final task failure.",
                "stop": "Evidence channels collapse to generic confidence or do not change the controller decision.",
                "asset": "Perturbation logs, action-delta traces, wrist-future masks, and calibrated recovery labels.",
            },
            {
                "priority": "Explore",
                "title": "Measurement-grounded world-model validity suite",
                "thesis": "Evaluate world models and simulators on embodiment transfer, physical observables, and semantic foresight under identical robot tasks.",
                "scores": {"fit": 5, "novelty": 4, "feasibility": 3, "moat": 4, "timing": 5, "evidence": 4},
                "one_week": "Select two tabletop contact tasks and define friction, contact timing, object displacement, and appearance-shift observables.",
                "four_week": "Compare one simulator, one video world model, and one WAM using the same measurements and action-success threshold.",
                "success": "Physical observable error explains downstream policy failure better than perceptual similarity.",
                "stop": "Measurement errors do not correlate with action failure or recovery decisions.",
                "asset": "Calibrated task metadata, measurement scripts, and paired generated/simulated/real rollouts.",
            },
            {
                "priority": "Build moat",
                "title": "Recoverable robot failure and prompt-injection replay set",
                "thesis": "Combine inevitable-failure planning, physical prompt injection, simulator fuzzing, and constrained multi-agent navigation into a replayable safety suite.",
                "scores": {"fit": 4, "novelty": 4, "feasibility": 4, "moat": 4, "timing": 4, "evidence": 4},
                "one_week": "Create five failure scenes with signage attacks, actuator degradation, simulator mutation, and path-planning constraints.",
                "four_week": "Run VLM planners and robot policies with mitigation variants, measuring impact severity, detection, and recovery action quality.",
                "success": "The replay set separates avoidable perception attacks from unavoidable physical failures with different mitigation choices.",
                "stop": "The suite only reproduces known failures and does not change mitigation ranking.",
                "asset": "Safety replay scenarios, prompt-injection masks, failure-impact labels, and Isaac Sim mutation recipes.",
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
