#!/usr/bin/env python3
"""Generate the 2026-06-05 arXiv daily briefing artifacts from /new parser outputs."""
from __future__ import annotations

from daily_backfill_lib import build, week_start


DATE = "2026-06-05"

PROFILE = {
    "date": DATE,
    "weekday": "Fri",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Daily /new parser output",
    "benchmark_note": "Daily artifact generated from arXiv /new parser output with abstracts available.",
    "thesis": (
        "6/5 /new batch is less about a single flagship model and more about execution surfaces: "
        "VLA action generation, humanoid and dexterous manipulation, geometry-grounded navigation, "
        "video/world-model evaluation, and safety-critical driving all show up as deployable robot-stack checks."
    ),
    "trend_note": (
        "The strongest signal is that robot learning and generation are both broad, while 3D/Scene, "
        "Foundation Models, Efficiency/Systems, and Safety/Alignment provide the evidence and runtime gates. "
        "For APRL use, this batch should be read as a set of evaluation knobs: affordance grounding, spatial memory, "
        "trajectory risk, token/cache budget, and OOD or safety failure modes."
    ),
    "cluster_specs": [
        {
            "title": "VLA and robot policies move toward simpler action interfaces",
            "buckets": ["Robot Learning", "Efficiency/Systems"],
            "ids": ["2606.05737", "2606.06155", "2606.05254", "2606.06194"],
            "needles": [
                "vision-language-action",
                "vla",
                "world action model",
                "affordance",
                "egocentric",
                "one-step action",
            ],
            "why": (
                "The VLA papers here ask whether policy execution can be compressed into simpler action-generation "
                "interfaces without losing the grounding that makes robots useful. One-step action generation, "
                "affordance-conditioned action, world-action distillation, and egocentric active-perception pretraining "
                "are complementary stress tests for the same question: which intermediate representation is actually "
                "needed before a robot commits to an action?"
            ),
            "confidence": "High",
            "confidence_note": "direct VLA, affordance, world-action, and egocentric pretraining papers are present",
            "lab_action": "Run a shared manipulation split with action-token budget, affordance hit rate, recovery rate, and policy latency logged together.",
        },
        {
            "title": "Manipulation broadens into bimanual cloth, dexterous grasping, and symbolic recovery",
            "buckets": ["Robot Learning", "Embodied AI"],
            "ids": ["2606.06292", "2606.05407", "2606.05248", "2606.05873", "2606.06040"],
            "needles": [
                "bimanual",
                "cloth",
                "dexterous",
                "grasping",
                "symbolic planning",
                "humanoid",
                "vine robots",
            ],
            "why": (
                "The manipulation group is not only another demonstration-data batch. It mixes synthetic data for "
                "bimanual cloth perception, diffusion-policy dexterous grasping, symbolic planning with residual "
                "operator learning, humanoid ladder climbing, and fast vine-robot hardware. That makes the batch useful "
                "for comparing where structure should live: perception labels, policy priors, symbolic recovery logic, "
                "or platform-specific mechanics."
            ),
            "confidence": "High",
            "confidence_note": "multiple manipulation and embodied-hardware papers connect through contact-rich execution",
            "lab_action": "Track contact-rich tasks with phase labels, recovery trigger, synthetic-data source, and hardware-specific failure tags.",
        },
        {
            "title": "Geometry and navigation become grounded state rather than visual garnish",
            "buckets": ["3D/Scene", "Embodied AI", "Autonomous Driving"],
            "ids": ["2606.05506", "2606.05774", "2606.05833", "2606.05975", "2606.06312", "2606.05372"],
            "needles": [
                "navigation",
                "geometric",
                "grounded",
                "spatial",
                "3d functionality",
                "geo-localization",
                "distance functions",
            ],
            "why": (
                "This cluster is the Geometry/SLAM/Reconstruction watch lens for the day. PointGoal navigation with "
                "privileged sensor contrast, grounded driving transformers, video-derived geometric representations, "
                "open-vocabulary 3D functionality segmentation, cross-view geo-localization, and navigation vector-field "
                "distance functions all point to the same operational need: spatial state must be queryable by a policy, "
                "not just rendered in a pretty scene representation."
            ),
            "confidence": "High",
            "confidence_note": "navigation, grounded driving, spatial MLLM, functionality segmentation, and geo-localization are all present",
            "lab_action": "Evaluate maps by localization error, traversability or functionality query accuracy, and downstream navigation success.",
        },
        {
            "title": "Video and world-model evaluation shifts toward control, memory, and preference",
            "buckets": ["Generation", "Autonomous Driving", "Foundation Models"],
            "ids": ["2606.05665", "2606.05677", "2606.06423", "2606.05259", "2606.05399", "2606.05478"],
            "needles": [
                "video-to-video",
                "video understanding",
                "spatial memory",
                "scenario generation",
                "flow matching",
                "human preference",
            ],
            "why": (
                "The generation papers are useful because they put evaluation pressure on controllability instead of "
                "only image quality. V2V-Bench, long-horizon spatial memory, safety-critical traffic scenario generation, "
                "knowledge-intensive video understanding, physics learning via flow matching, and preference prediction "
                "together suggest that world-model work should report intervention consistency, remembered spatial facts, "
                "and risk coverage, not only visual realism."
            ),
            "confidence": "High",
            "confidence_note": "video generation, spatial memory, risk scenario generation, and physics learning papers align",
            "lab_action": "Add intervention consistency, spatial recall, preference prediction, and risk-scenario diversity to world-model evals.",
        },
        {
            "title": "Efficiency papers expose the runtime knobs hidden in multimodal systems",
            "buckets": ["Efficiency/Systems", "Foundation Models", "Generation"],
            "ids": ["2606.05703", "2606.05624", "2606.05489", "2606.05826", "2606.05758", "2606.05535"],
            "needles": [
                "fast",
                "kv",
                "index optimization",
                "adapter",
                "noise-aware",
                "efficient",
                "decoding",
            ],
            "why": (
                "Efficiency is scattered across retrieval, generation, representation learning, and control. Fast "
                "autoregressive image decoding, K/V injection for motion control, ANN index optimization, residual-flow "
                "adapters, and noise-aware visual representation learning are all knobs that can change the result under "
                "the same nominal model. The practical lesson is to log the systems choice as part of the scientific claim."
            ),
            "confidence": "Medium",
            "confidence_note": "papers share runtime or parameter-efficiency pressure, though they span different application surfaces",
            "lab_action": "Report latency, memory, retrieval recall, control fidelity, and accuracy on one Pareto table before comparing methods.",
        },
        {
            "title": "Reliability and safety split into OOD, representation steering, and traffic risk",
            "buckets": ["Safety/Alignment", "Foundation Models", "Autonomous Driving", "Generation"],
            "ids": ["2606.05536", "2606.05290", "2606.06423", "2606.06074", "2606.06219", "2606.05576"],
            "needles": [
                "ood",
                "safety",
                "risk",
                "crash",
                "adaptive routing",
                "evidence-grounded",
                "safe visual generation",
            ],
            "why": (
                "Reliability is not one metric in this batch. Fine-grained OOD detection, cross-model steering for safe "
                "visual generation, crash data, cognition-aware routing for end-to-end driving, risk-flow traffic scenarios, "
                "and evidence-grounded VQA all separate different failure origins. This is useful for robot and driving work "
                "because it forces the evaluation to say whether the failure came from distribution shift, routing, scenario "
                "coverage, or unsupported visual evidence."
            ),
            "confidence": "High",
            "confidence_note": "OOD, safety steering, crash/risk data, adaptive routing, and evidence-grounding papers are directly represented",
            "lab_action": "Tag each failure with OOD source, routing decision, scenario-risk class, and evidence support before aggregate scoring.",
        },
    ],
    "research_topics": [
        {
            "title": "Affordance-conditioned VLA action budget",
            "claim": "Compare one-step action, affordance grounding, and world-action distillation under the same manipulation tasks.",
        },
        {
            "title": "Geometry-as-state navigation eval",
            "claim": "Measure whether geometric representations improve localization, traversability, functionality queries, and policy success.",
        },
        {
            "title": "Risk-aware world-model benchmark",
            "claim": "Combine video-to-video quality, spatial recall, intervention consistency, and safety-critical scenario diversity.",
        },
    ],
}


if __name__ == "__main__":
    build(PROFILE, "out/cv_new.json", "out/ro_new.json")
