#!/usr/bin/env python3
"""Generate the 2026-08-11 Research Intelligence edition."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PROMPT = "prompts/instruction_v20260713.md"


RI_BY_DATE = {
    "2026-08-11": {
        "date": "2026-08-11",
        "edition": "Research Intelligence",
        "source_prompt": SOURCE_PROMPT,
        "source_mode": "new",
        "scope_note": (
            "Daily edition from matching Tuesday /new listings: 313 non-replacement cs.CV rows, "
            "116 cs.RO rows, 409 deduplicated papers, and 336 ROI papers. Tier A cards use the "
            "repository parser abstracts and official arXiv HTML availability checks for the selected papers."
        ),
        "executive_thesis": (
            "The August 11 batch says the next robotics advantage is not a larger perception backbone; it is the "
            "instrumented interface between evidence, latent state, adaptation, and action. LIRA opens the VLM-to-action "
            "routing problem, GWM-VLA and SLIM ask which predictive latents are actually action-grounded, VANE and "
            "SC2-WM turn deployment feedback into selective correction, CMU-Drive and FactorDrive make driving reasoning "
            "conditional on cooperation and planning-critical factors, and EndoMD-SLAM shows that a map must know when "
            "not to update. APRL should treat every memory, world model, compressed token, and safety claim as a contract: "
            "which downstream action changes, under which stress condition, and what evidence would force us to stop using it."
        ),
        "decision_cards": [
            {
                "label": "Decision",
                "title": "Action interfaces are now first-class model components",
                "body": (
                    "LIRA, SLIM, JEPA-WAM, and World Tokens all focus on the interface that converts visual-language "
                    "representations into executable robot actions, not just the upstream encoder."
                ),
            },
            {
                "label": "Decision",
                "title": "Online adaptation needs delayed evidence",
                "body": (
                    "VANE, SC2-WM, SAFE-CHEM, and RecoverFly ask whether a correction should be committed only after "
                    "future observations, uncertainty, or failure replay support it."
                ),
            },
            {
                "label": "Decision",
                "title": "Benchmarks must attack shortcut variables",
                "body": (
                    "EMRD, Evidence-RL, consequence-sensitive compression, and EndoMD-SLAM all separate useful evidence "
                    "from priors, nuisance conditions, or transient artifacts that can silently corrupt a decision."
                ),
            },
        ],
        "papers": [
            {
                "rank": 1,
                "title": "LIRA: Local Cross-Layer Information Routing for Vision-Language-Action Decoding",
                "arxiv_id": "2608.07596",
                "fit": "VLA action decoding - representation routing - deployment transfer",
                "status": "Tier A - official arXiv abstract and HTML availability checked",
                "status_quo": "VLA action decoders often consume a narrow or rigid slice of the pretrained VLM hierarchy.",
                "friction": "A robot action can depend on low-level geometry, mid-level affordance, and high-level task tokens at the same control step.",
                "hidden_premise": "Layer-local routing can expose complementary evidence without changing the backbone or the supervised training recipe.",
                "conceptual_move": "Treat VLM-to-action conditioning as depth-aware local information routing into parallel fusion blocks.",
                "mechanism": "The abstract describes task-token features, LIRA query features from intermediate states, and proprioceptive fusion before action prediction.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper identifies the VLM-to-action routing interface as underexplored."},
                    {"trace": "[Abstract]", "claim": "It reports an 18.9-point zero-shot transfer gain on LIBERO-Plus over VLA-Adapter under the same 0.5B configuration."},
                    {"trace": "[Inference]", "claim": "APRL should log which encoder depths change each action under viewpoint and object-shift splits."},
                ],
                "falsification": "If the same layers route under every task phase, LIRA is an adapter regularizer rather than a state-sensitive interface.",
                "adversarial": "A local layer window may overfit benchmark phase structure; transfer needs novel camera pose, object layout, and contact-state shifts.",
                "thinking_tool": "Ask which representation depth changed the motor command, not only which backbone produced the embedding.",
                "transfer_boundary": "Direct for VLA manipulation; weaker for modular systems whose action decoder already receives explicit state estimates.",
            },
            {
                "rank": 2,
                "title": "GWM-VLA: Geometry-Aware Latent World Modeling for Vision-Language-Action Learning",
                "arxiv_id": "2608.07619",
                "fit": "geometry-aware world model - multi-view latent state - action supervision",
                "status": "Tier A - official arXiv abstract and HTML availability checked",
                "status_quo": "Latent VLA world models can predict view dynamics while treating camera views as independent evidence streams.",
                "friction": "Manipulation robustness under visual shift depends on end-effector geometry and gripper-object interaction, not holistic scene prediction alone.",
                "hidden_premise": "Multi-view aggregation and action supervision can force the latent transition to preserve geometry that matters for control.",
                "conceptual_move": "Aggregate multi-view observations into geometry-aware states, predict target-view patch tokens, and share latent-action representations with the action head.",
                "mechanism": "The abstract names VGGT-Omega aggregation, target wrist-view prediction, and flow-matching action supervision as the coupled path.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "Existing latent world models are described as weak at explicitly modeling geometric relationships across camera views."},
                    {"trace": "[Abstract]", "claim": "The proposed latent representation is grounded by both next-view prediction and robot-action supervision."},
                    {"trace": "[Inference]", "claim": "APRL should probe whether latent geometry predicts contact error before final task success changes."},
                ],
                "falsification": "If geometry-aware latents improve view prediction but not action recovery under camera shift, the geometry is not operational.",
                "adversarial": "Targeting the wrist view can hide failures in global scene state, so static-camera and wrist-camera ablations should be separated.",
                "thinking_tool": "World-model quality should be measured by the geometry variable a controller consumes.",
                "transfer_boundary": "Strong for manipulation with multi-view observations; less direct for single-camera policies without calibrated view geometry.",
            },
            {
                "rank": 3,
                "title": "VANE: Reliable Test-Time Training for Vision-Language-Action Models via Future Visual Representation Prediction",
                "arxiv_id": "2608.09448",
                "fit": "VLA test-time training - selective update - future evidence",
                "status": "Tier A - official arXiv abstract and HTML availability checked",
                "status_quo": "Deployment-time adaptation often updates a shared policy space before the consequence of that update is known.",
                "friction": "Closed-loop manipulation can be damaged by a correction that mixes incompatible task errors or commits too early.",
                "hidden_premise": "Adaptation should be isolated from the live policy and committed only when future visual observations support the update.",
                "conceptual_move": "Use future visual representation prediction as delayed evidence for selective, reversible prompt adaptation.",
                "mechanism": "The abstract describes candidate updates isolated from the live policy, evaluated on later observations, then committed only when supported.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper states that online updates can alter subsequent actions before their consequences are known."},
                    {"trace": "[Abstract]", "claim": "It reports a 3.2 percentage-point average success gain over a corresponding TTT baseline on SimplerEnv WidowX."},
                    {"trace": "[Inference]", "claim": "APRL should maintain an adaptation quarantine log before changing the deployed policy."},
                ],
                "falsification": "If future-evidence gating only accepts easy corrections, it may improve average success while avoiding the rare failures that matter.",
                "adversarial": "Future visual support can reward visually plausible but contact-wrong behavior unless contact and action residuals are also logged.",
                "thinking_tool": "Do not let a model update itself until a later observation has audited the proposed correction.",
                "transfer_boundary": "Direct for closed-loop VLA policies with unlabeled deployment streams; less direct for static offline evaluation.",
            },
            {
                "rank": 4,
                "title": "SLIM-0.5B: Learning Action-Grounded Predictive Latents for Robot Manipulation",
                "arxiv_id": "2608.09771",
                "fit": "compact VLA - predictive latent - low-latency manipulation",
                "status": "Tier A - official arXiv abstract and HTML availability checked",
                "status_quo": "Large VLA backbones spend capacity on open-domain semantics even when manipulation needs compact transition variables.",
                "friction": "Pixel-level world prediction can be expensive and can preserve visual detail that does not change control.",
                "hidden_premise": "A smaller model can compete if its latent space is explicitly grounded in action-conditioned future transitions and inverse action explanation.",
                "conceptual_move": "Train masked trajectory prediction with action reconstruction and future-latent prediction in a compact mixture-of-transformers backbone.",
                "mechanism": "The abstract says SLIM captures both action-conditioned transitions and the actions that explain observed changes, then uses flow matching for actions.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper argues continuous manipulation primarily requires compact observation-action-transition representations."},
                    {"trace": "[Abstract]", "claim": "It claims competitive simulation and real-world performance with fewer parameters, lower latency, and lower GPU memory."},
                    {"trace": "[Inference]", "claim": "APRL should compare latent transition error against real action correction, not only model size."},
                ],
                "falsification": "If latency improves but failure modes shift to unseen objects or contacts, compactness traded away necessary state.",
                "adversarial": "A 0.5B result can benefit from task distribution fit; evaluate out-of-family object geometry and contact timing.",
                "thinking_tool": "Compression is useful only after naming which action-relevant variable survives.",
                "transfer_boundary": "Strong for manipulation policies where transition labels are available; weaker for language-heavy embodied tasks.",
            },
            {
                "rank": 5,
                "title": "SC2-WM: A Self-Correcting World Model with Closed-Loop Feedback for Vision-and-Language Navigation in Continuous Environments",
                "arxiv_id": "2608.07548",
                "fit": "VLN-CE - self-correcting world model - state drift feedback",
                "status": "Tier A - official arXiv abstract and HTML availability checked",
                "status_quo": "VLN-CE policies often execute open loop under partial observability and detect failure only after navigation has drifted.",
                "friction": "A route can look locally plausible while the internal state has already diverged from the instruction and observed layout.",
                "hidden_premise": "World-model foresight can generate feedback before action execution and can trigger model-level correction at test time.",
                "conceptual_move": "Use internal closed-loop feedback for state-level plan refinement, then selectively update the world model when feedback exposes capacity insufficiency.",
                "mechanism": "The abstract describes self-correction through world-model foresight and conditional world-aware adaptation.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper names internal state drift during inference as the central VLN-CE failure."},
                    {"trace": "[Abstract]", "claim": "It uses feedback before action execution and selective world-model test-time updates."},
                    {"trace": "[Inference]", "claim": "APRL should log when a predicted next observation disagrees with the actual one before wrong turns accumulate."},
                ],
                "falsification": "If correction triggers after the same step as task failure, the feedback is diagnostic but not control-relevant.",
                "adversarial": "World-model foresight can inherit map priors and mask localization drift; evaluate unseen layouts and ambiguous turns.",
                "thinking_tool": "Treat navigation world models as drift sensors before treating them as planners.",
                "transfer_boundary": "Strong for VLN and object navigation; less direct for manipulation unless future observations can be tied to contact state.",
            },
            {
                "rank": 6,
                "title": "Explore, Map, Remember, Decide: Are Embodied VLMs Ready for Safety-Critical Scenarios?",
                "arxiv_id": "2608.08077",
                "fit": "embodied VLM safety - spatial memory - bias under partial observability",
                "status": "Tier A - official arXiv abstract and HTML availability checked",
                "status_quo": "Embodied VLMs can appear capable by producing plausible decisions without proving spatial memory or evidence grounding.",
                "friction": "Safety-critical evacuation decisions can be driven by textual priors rather than the explored physical environment.",
                "hidden_premise": "A safety benchmark must separate exploration coverage, map fidelity, memory persistence, and focal decision quality.",
                "conceptual_move": "Extend Theory of Space into an Explore-Map-Remember-Decide pipeline with coverage, fidelity, memory, and decision metrics.",
                "mechanism": "The abstract reports that VLMs often choose evacuation points from pre-trained textual priors and lose spatial reasoning in low light.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper tests whether decisions are based on physical evidence or visual-language bias."},
                    {"trace": "[Abstract]", "claim": "It reports divergence from human memory patterns and degraded spatial reasoning in low-light conditions."},
                    {"trace": "[Inference]", "claim": "APRL should score embodied policies by evidence-grounded memory, not final instruction answer alone."},
                ],
                "falsification": "If focal decisions improve without map fidelity or memory persistence, the benchmark may still reward response priors.",
                "adversarial": "The ToS task may not cover manipulation or locomotion hazards; include dynamic obstacles and irreversible actions before generalizing.",
                "thinking_tool": "Split a safety decision into explore, map, remember, and decide, then attack each stage separately.",
                "transfer_boundary": "Strong for navigation and safety-critical reasoning; weaker for low-level control unless connected to action authority.",
            },
            {
                "rank": 7,
                "title": "CMU-Drive and V2V-VLA: Cooperative Multi-agent Unified Driving with Reasoning Benchmark and Vehicle-to-Vehicle Vision-Language-Action Models",
                "arxiv_id": "2608.07621",
                "fit": "cooperative driving - multi-agent VLA - closed-loop benchmark",
                "status": "Tier A - official arXiv abstract and HTML availability checked",
                "status_quo": "End-to-end driving VLA work is usually framed around an individual vehicle with local perception and planning.",
                "friction": "Safety-critical traffic scenes require communication and cooperative perception, so single-agent reasoning hides coordination failure.",
                "hidden_premise": "Driving actions, future waypoints, language reasoning, and communication policy can be generated in one cooperative forward pass.",
                "conceptual_move": "Create a closed-loop cooperative driving benchmark and a V2V-VLA baseline for connected autonomous vehicles.",
                "mechanism": "The abstract describes CMU-Drive and V2V-VLA jointly generating actions, waypoints, reasoning, and communication policies.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper frames cooperative autonomous driving as a missing benchmark and baseline."},
                    {"trace": "[Abstract]", "claim": "It requires multiple connected vehicles in safety-critical scenarios with background traffic."},
                    {"trace": "[Inference]", "claim": "APRL should evaluate whether communication changes the action, not just whether the message is plausible."},
                ],
                "falsification": "If vehicle-to-vehicle language does not improve closed-loop safety under occlusion or conflicting intent, it is explanatory overhead.",
                "adversarial": "Communication can leak simulator priors; test delayed, missing, and adversarial messages separately.",
                "thinking_tool": "A cooperative VLA must prove which partner evidence changed the ego action.",
                "transfer_boundary": "Direct for driving and multi-robot systems; less direct for single-arm manipulation.",
            },
            {
                "rank": 8,
                "title": "EndoMD-SLAM: Endoscopic Gaussian Splatting SLAM under Optical Degradation with Memory and Static-Transient Decomposition",
                "arxiv_id": "2608.08949",
                "fit": "medical SLAM - transient artifact rejection - memory-gated mapping",
                "status": "Tier A - official arXiv abstract and HTML availability checked",
                "status_quo": "Gaussian Splatting SLAM assumes multi-view photometric consistency and can fuse temporary artifacts into a persistent map.",
                "friction": "Endoscopic debris and water flushing move with the camera, corrupting tracking and mapping if treated as anatomy.",
                "hidden_premise": "A SLAM system should sometimes suspend updates and isolate transient fields rather than always integrate observations.",
                "conceptual_move": "Use memory-driven tracking gates for unreliable observations and static-transient decomposition for mapping.",
                "mechanism": "The abstract reports drift-aware relocalization from historical keyframes and a separate transient field for contaminants.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper names camera-attached artifacts as a cause of irreversible map corruption."},
                    {"trace": "[Abstract]", "claim": "It reports 91 percent absolute trajectory error reduction and 9.9 dB PSNR improvement under severe degradation."},
                    {"trace": "[Inference]", "claim": "APRL should test when mapping should reject observations rather than improve reconstruction loss."},
                ],
                "falsification": "If gates only work for colonoscopy-specific artifacts, the static-transient split may not transfer to general robot mapping.",
                "adversarial": "A memory gate can preserve stale geometry after real scene change; dynamic-update tests are required.",
                "thinking_tool": "A map update is an action with a stop condition, not a passive accumulation step.",
                "transfer_boundary": "Strong for SLAM under corruption and medical navigation; weaker for static offline reconstruction.",
            },
        ],
        "synthesis": [
            {
                "title": "Predictive latents and action decoders are converging",
                "links": "LIRA - GWM-VLA - SLIM - JEPA-WAM - World Tokens",
                "facts": "The papers separately route intermediate VLM layers, ground latent transitions with action supervision, and remove online world-model cost after training.",
                "inference": "APRL should benchmark the interface variable that changes action: layer depth, latent transition, world token, or action expert state.",
            },
            {
                "title": "Adaptation is becoming an evidence contract",
                "links": "VANE - SC2-WM - SAFE-CHEM - RecoverFly",
                "facts": "The papers gate adaptation with future observations, self-correcting world-model feedback, uncertainty switching, or failure replay.",
                "inference": "The deployment question is when to commit an update, who holds authority before commitment, and which future evidence invalidates it.",
            },
            {
                "title": "Safety benchmarks now separate evidence from priors",
                "links": "EMRD - Evidence-RL - consequence-sensitive token compression - EndoMD-SLAM",
                "facts": "The batch tests physical evidence use, causal evidence regions, consequence-aware token budgets, and transient map corruption.",
                "inference": "Robot evaluation should attack the shortcut variable before trusting a policy, descriptor, map, or compressed perception stack.",
            },
        ],
        "frontier_memory": [
            {"label": "Strengthening", "history": "August 10 emphasized state accountability in VLA, world models, intervention, and geometry.", "body": "August 11 strengthens that axis with action routing, future-evidence TTT, self-correcting navigation, and memory-gated SLAM."},
            {"label": "New signal", "history": "Recent RI editions treated world models mostly as latent or rollout evaluators.", "body": "Today adds a stronger interface question: can a world-model latent be shared with the action head without carrying irrelevant prediction detail?"},
            {"label": "Missing axis", "history": "Prior driving and navigation notes focused on single-agent or single-robot execution.", "body": "CMU-Drive and EMRD add cooperation and safety-critical memory as axes that should be stressed explicitly."},
        ],
        "strategy": [
            {
                "priority": "Build moat",
                "title": "Action-interface audit for VLA policies",
                "thesis": "Measure which representation depth, latent transition, and world token changes the action under controlled visual, semantic, and contact shifts.",
                "scores": {"fit": 5, "novelty": 5, "feasibility": 4, "moat": 5, "timing": 5, "evidence": 5},
                "one_week": "Run one LIBERO-style replay with layer-depth routing logs, latent prediction loss, action delta, and contact-state labels.",
                "four_week": "Compare VLA-Adapter, LIRA-style routing, latent WAM, and compact predictive-latent policies on the same shift suite.",
                "success": "At least two interface signals predict different failure families before task-level success changes.",
                "stop": "Interface logs collapse to model confidence and do not change recovery or transfer ranking.",
                "asset": "Layer routing traces, world-token dumps, action deltas, contact labels, and shift-conditioned success tables.",
            },
            {
                "priority": "Explore",
                "title": "Future-evidence adaptation quarantine",
                "thesis": "Treat test-time updates as untrusted candidates until later observations, world-model feedback, or uncertainty thresholds prove they should enter the live controller.",
                "scores": {"fit": 5, "novelty": 4, "feasibility": 4, "moat": 4, "timing": 5, "evidence": 4},
                "one_week": "Implement a quarantine buffer that stores proposed prompt/model updates and replays the next observation before commit.",
                "four_week": "Evaluate VANE-style gating, SC2-WM correction, and uncertainty switching under object shifts, low light, and recovery tasks.",
                "success": "Gating reduces harmful updates while preserving at least half of the positive adaptation gain.",
                "stop": "Delayed evidence accepts only easy updates or fails to predict recoverability.",
                "asset": "Candidate-update logs, future-observation support scores, rejection labels, and operator handoff traces.",
            },
            {
                "priority": "Build moat",
                "title": "Shortcut-resistant robot evidence benchmark",
                "thesis": "Stress maps, VLM answers, token budgets, and driving communication with nuisance variables that look plausible but should not change the action.",
                "scores": {"fit": 5, "novelty": 5, "feasibility": 3, "moat": 5, "timing": 4, "evidence": 5},
                "one_week": "Create a small suite with transient visual artifacts, low-light navigation, token-budget cost labels, and delayed V2V messages.",
                "four_week": "Evaluate SLAM, embodied VLM, VLA driving, and VLM compression methods by action change, not only answer or reconstruction quality.",
                "success": "The benchmark reverses at least one method ranking relative to a standard metric.",
                "stop": "Nuisance labels do not reveal failures beyond ordinary held-out splits.",
                "asset": "Artifact-corrupted videos, EMRD-style memory traces, cost-tagged VQA tasks, V2V message perturbations, and closed-loop action logs.",
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
