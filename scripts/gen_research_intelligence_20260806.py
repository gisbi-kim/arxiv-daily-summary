#!/usr/bin/env python3
"""Generate the 2026-08-06 Research Intelligence edition."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PROMPT = "prompts/instruction_v20260713.md"


RI_BY_DATE = {
    "2026-08-06": {
        "date": "2026-08-06",
        "edition": "Research Intelligence",
        "source_prompt": SOURCE_PROMPT,
        "source_mode": "new",
        "scope_note": (
            "Daily edition from matching Thursday /new listings: 131 non-replacement cs.CV rows, "
            "37 cs.RO rows, 160 deduplicated papers, and 136 ROI papers. Tier A cards use official "
            "arXiv abstract pages plus available official arXiv HTML headings."
        ),
        "executive_thesis": (
            "The August 6 batch is about deciding which evidence channel is allowed to steer a robot action. "
            "CofactVLA treats visual dominance as a causal-confounding problem, Faster-WAM keeps future state "
            "available without paying full video-action cost, SAFECAST calibrates failure detectors under "
            "contrast-set shifts, and Talk2Sensors moves outdoor grounding toward sensor-specific physical cues. "
            "APRL should turn this into an evidence-channel audit: instruction, vision, future state, geometry, "
            "and risk probe each need separate perturbations and stop conditions."
        ),
        "decision_cards": [
            {
                "label": "Decision",
                "title": "VLA errors are becoming causal evidence errors",
                "body": (
                    "CofactVLA and GUARD both ask whether the action was grounded in the intended instruction "
                    "and visual evidence, rather than in a dominant but spurious cue."
                ),
            },
            {
                "label": "Decision",
                "title": "Future state must survive the inference budget",
                "body": (
                    "Faster-WAM, MobileWAM, and DreamWAM separate action-relevant future state from RGB-only "
                    "prediction and from expensive full future rollout."
                ),
            },
            {
                "label": "Decision",
                "title": "Geometry grounding must name the sensor cue",
                "body": (
                    "Talk2Sensors and the calibration papers make camera, LiDAR, radar, and 3D target cues "
                    "auditable instead of treating 3D grounding as a single score."
                ),
            },
        ],
        "papers": [
            {
                "rank": 1,
                "title": "CofactVLA: Deconfounding Vision-Language-Action Models via Counterfactual Intervention",
                "arxiv_id": "2608.04396",
                "fit": "VLA causality - vision override - counterfactual intervention",
                "status": "Tier A - official arXiv abstract and HTML structure checked",
                "status_quo": "VLA policies often assume the language instruction remains the primary causal driver of action.",
                "friction": "Dense visual streams can override sparse language, so policies latch onto familiar layouts or salient objects.",
                "hidden_premise": "The model needs a way to compare the instructed action against a language-masked counterfactual branch.",
                "conceptual_move": "Formalize VLA action generation as a deconfounding graph and neutralize visual confounders inside one forward pass.",
                "mechanism": "The abstract defines vision override as causal confusion and the official HTML exposes causal-view and action-level deconfounding sections.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper names modality imbalance and spurious visual confounders as the cause of instruction bypass."},
                    {"trace": "[HTML headings]", "claim": "Official HTML includes a causal view of VLA and action-level deconfounding method sections."},
                    {"trace": "[Inference]", "claim": "APRL should test whether language ablation changes action choice before accepting a VLA rollout as grounded."},
                ],
                "falsification": "If counterfactual masking does not separate instruction-sensitive from vision-dominated failures, the causal framing is weak.",
                "adversarial": "A masked branch can remove useful context, so gains must be checked under object, layout, and instruction perturbations.",
                "thinking_tool": "Before scaling demonstrations, ask which evidence channel would change the next action if removed.",
                "transfer_boundary": "Strong for language-conditioned manipulation; less direct for low-level servo tasks with no linguistic ambiguity.",
            },
            {
                "rank": 2,
                "title": "Faster-WAM: Efficient Inference-Time Future Conditioning for Robust World Action Models",
                "arxiv_id": "2608.04404",
                "fit": "world action model - future conditioning - inference efficiency",
                "status": "Tier A - official arXiv abstract and HTML structure checked",
                "status_quo": "WAMs often trade future-aware inference for prohibitive video-action computation.",
                "friction": "Removing future conditioning saves compute but may discard the temporal state that gives robustness under shift.",
                "hidden_premise": "Future representations can be computed once, reused sparsely, and still preserve the action-relevant signal.",
                "conceptual_move": "Keep inference-time future conditioning while decoupling it from expensive full video-action interaction.",
                "mechanism": "The abstract motivates sparse future conditioning and the official HTML includes problem formulation, method, and experiment sections.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper states that inference-time future conditioning is critical for generalization under distribution shifts."},
                    {"trace": "[HTML headings]", "claim": "Official HTML includes Faster-WAM, implementation, and experiment sections."},
                    {"trace": "[Inference]", "claim": "APRL should measure which future tokens change action success per unit of latency."},
                ],
                "falsification": "If sparse future conditioning only preserves visual plausibility and not action success under shift, the efficiency gain is insufficient.",
                "adversarial": "The method can hide stale-future errors unless the future cache is perturbed and aged in evaluation.",
                "thinking_tool": "Treat future state as a budgeted control resource, not as a decorative prediction target.",
                "transfer_boundary": "Strong for WAM-style manipulation and mobile manipulation; less direct for memoryless reactive policies.",
            },
            {
                "rank": 3,
                "title": "SAFECAST: Robust Failure Detection for VLA Policies with Contrast-Set Training and Calibration",
                "arxiv_id": "2608.04246",
                "fit": "VLA failure detection - contrast sets - calibrated risk",
                "status": "Tier A - official arXiv abstract and HTML structure checked",
                "status_quo": "Hidden-state risk probes are usually calibrated on data that may not match deployment shift.",
                "friction": "Clutter, distractors, lighting, novel objects, initial states, and reworded instructions can invalidate calibration.",
                "hidden_premise": "A failure detector must see controlled contrastive shifts before deployment, not only nominal successes and failures.",
                "conceptual_move": "Use visual and language contrast-set perturbations to train and calibrate VLA failure probes.",
                "mechanism": "The abstract reports improved ROC-AUC across DROID and LIBERO, and the official HTML exposes SAFECAST experiments and results sections.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper lists deployment-time shifts and ties detector reliability to matching calibration data."},
                    {"trace": "[HTML headings]", "claim": "Official HTML includes experimental setup and failure-detection improvement sections."},
                    {"trace": "[Inference]", "claim": "APRL should store contrast-set perturbation type next to every failure-warning metric."},
                ],
                "falsification": "If detector calibration fails on unseen shift families, contrast sets are still too narrow.",
                "adversarial": "A high ROC-AUC can hide poor early-warning lead time or poor recovery action quality.",
                "thinking_tool": "Calibrate risk probes by the exact shift family that should trigger a different robot decision.",
                "transfer_boundary": "Strong for VLA deployment monitoring; less complete for hardware faults that do not appear in policy hidden state.",
            },
            {
                "rank": 4,
                "title": "Talk2Sensors: 3D Visual Grounding in Autonomous Driving via Sensor-Adaptive Physical Cue Matching",
                "arxiv_id": "2608.04568",
                "fit": "outdoor 3D grounding - camera LiDAR radar - physical cue matching",
                "status": "Tier A - official arXiv abstract and HTML structure checked",
                "status_quo": "3D visual grounding is often evaluated indoors or with one dominant outdoor sensing modality.",
                "friction": "Outdoor driving queries depend on texture, geometry, and kinematics that different sensors observe unevenly.",
                "hidden_premise": "Language grounding should route the query to the physical cue and sensor that can actually verify it.",
                "conceptual_move": "Build a camera-LiDAR-4D radar grounding dataset and a sensor-adaptive cue matching framework.",
                "mechanism": "The abstract names sensor-specific physical cues, and official HTML includes dataset, annotation, statistics, and method sections.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper reports 8,682 language instructions and 20,558 referred objects aligned with sensor-specific cues."},
                    {"trace": "[HTML headings]", "claim": "Official HTML includes camera, LiDAR, radar fusion and dataset statistics sections."},
                    {"trace": "[Inference]", "claim": "APRL should evaluate 3D grounding by cue-source agreement, not only box accuracy."},
                ],
                "falsification": "If sensor-adaptive routing fails under weather, range, or occlusion changes, the grounding interface is not robust enough.",
                "adversarial": "A dataset can reward sensor-name correlations unless cue-level perturbations are tested.",
                "thinking_tool": "For every grounded command, record which sensor cue made the referent observable.",
                "transfer_boundary": "Direct for outdoor autonomy and multi-sensor robots; less direct for single-camera tabletop manipulation.",
            },
        ],
        "synthesis": [
            {
                "title": "Evidence channels replace monolithic policy confidence",
                "links": "CofactVLA - SAFECAST - GUARD",
                "facts": "The papers separate instruction causality, hidden-state risk, and token/KV grounding uncertainty.",
                "inference": "APRL should report failure warnings by evidence channel rather than one aggregate confidence number.",
            },
            {
                "title": "Future state and geometry must be budgeted together",
                "links": "Faster-WAM - MobileWAM - DreamWAM - Talk2Sensors",
                "facts": "The batch ties WAM future state to mobile manipulation and sensor-specific 3D grounding.",
                "inference": "A robot benchmark should cross future-cache age, sensor cue, and action success under the same rollout.",
            },
        ],
        "frontier_memory": [
            {"label": "Strengthening", "history": "August 5 framed state validity as the weekly axis.", "body": "August 6 makes the state-validity question evidence-channel specific."},
            {"label": "New signal", "history": "Earlier WAM notes emphasized future prediction quality.", "body": "Faster-WAM and DreamWAM shift the useful variable toward budgeted future-state representations."},
            {"label": "Missing axis", "history": "Late July geometry checks emphasized SLAM and maps.", "body": "Talk2Sensors adds sensor-cue agreement as a grounding validity axis."},
        ],
        "strategy": [
            {
                "priority": "Build moat",
                "title": "Evidence-channel VLA audit harness",
                "thesis": "Cross instruction masking, visual distractors, future-state cache age, sensor cue removal, and risk-probe calibration in one robot rollout suite.",
                "scores": {"fit": 5, "novelty": 5, "feasibility": 4, "moat": 5, "timing": 5, "evidence": 4},
                "one_week": "Instrument one VLA task with language-masked, visual-distractor, and future-cache ablations plus SAFECAST-style risk labels.",
                "four_week": "Build a reusable evidence-channel benchmark covering tabletop manipulation and one multi-sensor navigation scenario.",
                "success": "At least two evidence-channel perturbations predict distinct failure families before final action failure.",
                "stop": "Channel-specific probes collapse to the same signal as generic confidence or do not predict recovery choices.",
                "asset": "Evidence-channel perturbation logs, calibrated risk labels, and replayable sensor-cue ablation videos.",
            },
            {
                "priority": "Explore",
                "title": "Sensor-cue grounding protocol",
                "thesis": "Evaluate whether language grounding uses texture, 3D geometry, radar velocity, or calibration evidence under explicit sensor dropout.",
                "scores": {"fit": 4, "novelty": 4, "feasibility": 3, "moat": 4, "timing": 4, "evidence": 4},
                "one_week": "Create a small annotation sheet that labels every referred object by observable sensor cue and expected failure under cue removal.",
                "four_week": "Run camera-only, LiDAR-only, radar-only, and fused grounding on outdoor or campus robot scenes with controlled occlusion.",
                "success": "Grounding errors map to the removed cue rather than random box drift.",
                "stop": "Sensor-cue labels do not explain grounding failures beyond ordinary detection confidence.",
                "asset": "Cue-source annotation schema plus sensor-dropout grounding benchmark.",
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
