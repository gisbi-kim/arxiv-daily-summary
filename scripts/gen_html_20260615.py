#!/usr/bin/env python3
"""Generate the 2026-06-15 arXiv daily briefing artifacts from /new parser outputs."""
from __future__ import annotations

from daily_backfill_lib import build, week_start


DATE = "2026-06-15"

PROFILE = {
    "date": DATE,
    "weekday": "Mon",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Daily /new parser output",
    "benchmark_note": "Daily artifact generated from arXiv /new parser output with abstracts available.",
    "thesis": (
        "6/15 /new batch is unusually execution-heavy: real-time VLA distillation, 4D world-action modeling, "
        "physically grounded manipulation, multi-agent driving simulation, and camera-side attacks all ask the same "
        "question under different names. The useful APRL read is not 'more multimodal models'; it is whether a model "
        "can preserve state, causality, contact, and recovery behavior when perception becomes part of a control loop."
    ),
    "trend_note": (
        "Robot Learning is the largest bucket, but it is entangled with Generation and Safety/Alignment. World models "
        "are no longer just video predictors, VLA papers are being pushed toward latency and physics, and the safety "
        "papers make sensor-side and planner-side failure modes concrete. The day is therefore good for building an "
        "evaluation matrix that joins representation quality, action latency, contact evidence, adversarial exposure, "
        "and mission recovery."
    ),
    "cluster_specs": [
        {
            "title": "Real-time VLA moves from model capability to deployment contract",
            "buckets": ["Robot Learning"],
            "ids": ["2606.14010", "2606.14153", "2606.13856", "2606.13886"],
            "needles": [
                "real-time vision-language-action",
                "vla backbone",
                "vla fine-tuning",
                "physically-grounded vla",
                "distillation",
                "frozen-backbone",
            ],
            "why": (
                "RT-VLA, the frozen-backbone grafting diagnostic, output-level VLA regularization, and PhysVLA make "
                "VLA look less like a single leaderboard and more like a deployment contract: latency, transferable "
                "encoders, fine-tuning stability, and physical grounding have to be audited together."
            ),
            "confidence": "High",
            "confidence_note": "multiple VLA papers target latency, backbone transfer, fine-tuning stability, and physical grounding",
            "lab_action": "For every VLA baseline, log latency, backbone choice, fine-tuning seed variance, physical constraint violations, and task success.",
            "limit": 5,
        },
        {
            "title": "World-action models are becoming structured state interfaces",
            "buckets": ["Robot Learning", "Generation", "Autonomous Driving"],
            "ids": ["2606.14048", "2606.13769", "2606.13817", "2606.14058", "2606.13840"],
            "needles": [
                "world action model",
                "4d world action model",
                "interaction-trace world model",
                "world model with object momentum",
                "reactive behavior world model",
                "shared world models",
            ],
            "why": (
                "WAM4D, the scalable 3D interaction-trace world model, FlowMo-WM, ReactSim-Bench, and multi-agent "
                "embodied driving all point to the same shift: the world model is becoming a queryable state interface "
                "for control, not only a renderer of plausible futures."
            ),
            "confidence": "High",
            "confidence_note": "world-model language appears across robotics, driving, and simulation papers",
            "lab_action": "Evaluate state persistence, action conditioning, counterfactual query quality, and downstream recovery after model error.",
            "limit": 5,
        },
        {
            "title": "Contact-rich manipulation needs tactile and geometric evidence",
            "buckets": ["Robot Learning", "3D/Scene"],
            "ids": ["2606.13877", "2606.14699", "2606.14389", "2606.14237"],
            "needles": [
                "contactworld",
                "vision-tactile",
                "contact-rich manipulation",
                "3d object articulation",
                "kinematic control",
                "object pose estimation",
                "indoor localization",
            ],
            "why": (
                "ContactWorld, Instruct-Particulate, MooMIns, and BIM-Loc form a useful manipulation stack: contact "
                "signals, articulated object geometry, object pose, and localization all become evidence that a policy "
                "can use or lose during real interaction."
            ),
            "confidence": "Medium",
            "confidence_note": "the papers span manipulation, articulation, reconstruction, and localization but share evidence-grounding needs",
            "lab_action": "Create a contact audit sheet with tactile cue, object articulation state, pose source, localization drift, and failure label.",
            "limit": 5,
        },
        {
            "title": "Autonomous driving evaluation shifts toward causal recovery and adversarial curricula",
            "buckets": ["Autonomous Driving", "Safety/Alignment"],
            "ids": ["2606.14032", "2606.14438", "2606.14380", "2606.14504", "2606.14658"],
            "needles": [
                "adversarial training for safe autonomous driving",
                "causal auditing",
                "accident anticipation",
                "optical attacks",
                "acoustic adversarial attacks",
                "agentic recovery",
            ],
            "why": (
                "Learnability-guided adversarial training, CADET, FLaRA, scratched-lens attacks, and acoustic attacks "
                "make evaluation less about average prediction and more about causal fault isolation: what changed, "
                "who detected it, and how the planner or autonomy stack recovered."
            ),
            "confidence": "High",
            "confidence_note": "driving and safety papers explicitly target attacks, causal auditing, anticipation, and recovery",
            "lab_action": "Track perturbation source, causal feature shift, planner response, recovery action, and residual mission risk.",
            "limit": 5,
        },
        {
            "title": "Visual reasoning papers expose evidence chains rather than final answers",
            "buckets": ["Foundation Models", "Embodied AI"],
            "ids": ["2606.13870", "2606.13929", "2606.14702", "2606.14703", "2606.13878"],
            "needles": [
                "fake visual understanding",
                "visual questioner",
                "structured scripts and evidence chains",
                "gaze heads",
                "vision-language guided multi-agent exploration",
                "lifelong navigation",
            ],
            "why": (
                "Mirage Probes, Self-Evolving Visual Questioner, OmniVideo-100K, Gaze Heads, and AnyGoal all push on "
                "the same diagnostic surface: instead of accepting the final multimodal answer, inspect what evidence "
                "the model sought, attended to, scripted, or ignored."
            ),
            "confidence": "High",
            "confidence_note": "foundation and embodied papers repeatedly mention probes, question generation, evidence chains, gaze, and exploration",
            "lab_action": "For VLM/agent tests, save evidence request, gaze or attention target, intermediate script, final answer, and correction outcome.",
            "limit": 5,
        },
        {
            "title": "Efficient vision is becoming adaptive token and field deployment engineering",
            "buckets": ["Efficiency/Systems", "Generation", "Safety/Alignment"],
            "ids": ["2606.14277", "2606.13898", "2606.14631", "2606.14071", "2606.14081"],
            "needles": [
                "adaptive layer-wise visual token selection",
                "token compression",
                "distillation",
                "wildfire spread prediction",
                "geo-foundational models",
                "lightweight saliency",
            ],
            "why": (
                "Adaptive token selection, HiLo-Token, event saliency distillation, wildfire prediction, and geo-foundation "
                "hybrids show the practical side of the day. Efficiency is not only smaller models; it is choosing which "
                "visual evidence survives under deployment constraints."
            ),
            "confidence": "Medium",
            "confidence_note": "token, distillation, and field-risk papers connect through deployment-constrained evidence selection",
            "lab_action": "Report token budget, retained evidence type, latency, field domain shift, and safety-relevant miss cases together.",
            "limit": 5,
        },
    ],
    "research_topics": [
        {
            "title": "VLA deployment contract",
            "claim": "Benchmark VLA methods with latency, seed stability, physical grounding violations, and task success in one table.",
        },
        {
            "title": "World-model state audit",
            "claim": "Test whether a world-action model preserves object state, contact, and recovery-relevant information after interventions.",
        },
        {
            "title": "Sensor-side failure recovery",
            "claim": "Combine optical/acoustic perturbations with causal planner auditing to measure detection, attribution, and recovery.",
        },
    ],
}


if __name__ == "__main__":
    build(PROFILE, "out/cv_new.json", "out/ro_new.json")
