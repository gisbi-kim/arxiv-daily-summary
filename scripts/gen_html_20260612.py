#!/usr/bin/env python3
"""Generate the 2026-06-12 arXiv daily briefing artifacts from /new parser outputs."""
from __future__ import annotations

from daily_backfill_lib import build, week_start


DATE = "2026-06-12"

PROFILE = {
    "date": DATE,
    "weekday": "Fri",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Daily /new parser output",
    "benchmark_note": "Daily artifact generated from arXiv /new parser output with abstracts available.",
    "thesis": (
        "6/12 /new batch is less about a single new model class and more about execution interfaces: "
        "world-action models, VLA control, dexterous tool use, visual agents, and deployable perception are all "
        "asking how representation turns into reliable action. For APRL, the useful read is to treat generation, "
        "spatial reasoning, and robot learning as one evaluation stack: predict the world, expose the evidence, "
        "then measure whether the robot or agent can act on it."
    ),
    "trend_note": (
        "Robot Learning and Generation are the two largest buckets, but they point to the same pressure point. "
        "World-action papers are moving from visual prediction toward action transfer, while VLA and manipulation "
        "papers are adding memory, preference, spatial annotation, and attack surfaces. The systems bucket is also "
        "large, which makes the day practical rather than purely model-centric: on-device fall detection, forest "
        "place recognition, distributed tracking, and unified tokenizers all ask what survives outside clean demos."
    ),
    "cluster_specs": [
        {
            "title": "World-action models become the bridge between video prediction and control",
            "buckets": ["Robot Learning", "Autonomous Driving", "Generation", "Safety/Alignment"],
            "ids": ["2606.13674", "2606.12987", "2606.13376", "2606.13515", "2606.13679"],
            "needles": [
                "world action model",
                "world-action",
                "visual-action tokenizers",
                "av scene prediction",
                "video world modeling",
                "maskwam",
                "interleaved generation",
            ],
            "why": (
                "RepWAM, the diffusion-transformer WAM for AV scene prediction, MoVerse, and MaskWAM all sit on the "
                "same boundary: video/world prediction is only valuable if its latent state can be queried, masked, "
                "or converted into action. The signal is that 'world model' is becoming an interface contract, not "
                "just a prettier forecast."
            ),
            "confidence": "High",
            "confidence_note": "multiple WAM/world-model titles appear across robot learning, driving, generation, and safety buckets",
            "lab_action": "Log forecast quality, mask/prompt controllability, action-token alignment, and downstream policy success in the same table.",
            "limit": 5,
        },
        {
            "title": "VLA evaluation shifts from success rate to interaction failure modes",
            "buckets": ["Robot Learning", "Autonomous Driving"],
            "ids": ["2606.12706", "2606.12475", "2606.12978", "2606.12499", "2606.12603"],
            "needles": [
                "vla",
                "cot-action",
                "collaborative",
                "trajectory-level redirection attacks",
                "action-effect memory",
                "human-preference",
                "long-horizon",
            ],
            "why": (
                "VLADriveBench asks whether chain-of-thought actually matches action, Learning to Assist moves VLA "
                "toward implicit collaboration, and the redirection-attack paper makes the failure surface explicit. "
                "Action-effect memory and preference-flow policies add the missing temporal layer: the benchmark "
                "should measure how instructions, memories, and attacks change behavior over a trajectory."
            ),
            "confidence": "High",
            "confidence_note": "VLA appears in benchmark, collaboration, navigation, memory, and attack papers on the same day",
            "lab_action": "For each VLA run, save language trace, intended action, executed action, intervention point, and recovery behavior.",
            "limit": 5,
        },
        {
            "title": "Dexterous manipulation is moving toward grounded data and tool-level capability",
            "buckets": ["Robot Learning", "3D/Scene"],
            "ids": ["2606.13677", "2606.12604", "2606.12728", "2606.12910", "2606.13497"],
            "needles": [
                "dexterous",
                "articulated tools",
                "egocentric human videos",
                "contact-grounded",
                "grasping",
                "spatial annotations",
                "robot demonstrations",
            ],
            "why": (
                "Mana, EgoEngine, EquiDexFlow, language-conditioned grasping, and SPARC form a coherent manipulation "
                "stack: recover demonstrations from human video, ground contact and SE(3) structure, then annotate "
                "the robot data at scale. The interesting part is the data interface, not just the final hand policy."
            ),
            "confidence": "High",
            "confidence_note": "dexterous, grasping, egocentric demonstrations, and robot annotation papers connect directly",
            "lab_action": "Build a small audit sheet linking human-video source, contact labels, object articulation, grasp success, and annotation noise.",
            "limit": 5,
        },
        {
            "title": "Visual agents need explicit tools, feedback, and spatial self-correction",
            "buckets": ["Foundation Models", "Robot Learning"],
            "ids": ["2606.12830", "2606.13156", "2606.12886", "2606.12744", "2606.13061"],
            "needles": [
                "tool-augmented visual agents",
                "spatial reasoning",
                "visual feedback",
                "interleaved thinking",
                "prompt retrieval",
                "latent space",
                "multimodal embedding",
            ],
            "why": (
                "The foundation-model cluster is less about bigger VLMs and more about control over the reasoning loop. "
                "Tool-augmented visual agents, iterative visual thinking, stepwise modality transitions, and prompt "
                "retrieval all treat perception as an interactive process where the model can ask for better evidence."
            ),
            "confidence": "High",
            "confidence_note": "several Foundation Models papers explicitly target tools, feedback, modality transitions, or spatial correction",
            "lab_action": "Evaluate visual agents with evidence-request count, correction success, spatial error type, and final task success.",
            "limit": 5,
        },
        {
            "title": "Generation papers are optimizing controllability, memory, and provenance",
            "buckets": ["Generation"],
            "ids": ["2606.13035", "2606.13303", "2606.13345", "2606.12977", "2606.13366"],
            "needles": [
                "long-form video generation",
                "gated recall",
                "diffusion image editing",
                "3d scene editing",
                "fingerprinting",
                "diffusion models",
                "rate-distortion-perception",
            ],
            "why": (
                "TetherCache, DuET, JointEdit3D, diffusion fingerprinting, and diffusion compression show the same "
                "maturity pattern: generation quality is assumed, while the new work asks how to stabilize memory, "
                "edit structure, identify provenance, and trade compression against perceptual usefulness."
            ),
            "confidence": "High",
            "confidence_note": "top generation titles emphasize memory, editing, fingerprinting, and operational tradeoffs",
            "lab_action": "Track temporal drift, edit locality, identity/provenance recovery, and downstream scene-usefulness rather than FID alone.",
            "limit": 5,
        },
        {
            "title": "Deployment papers make perception reliability an edge and field problem",
            "buckets": ["Efficiency/Systems", "3D/Scene", "Autonomous Driving"],
            "ids": ["2606.12473", "2606.13206", "2606.13127", "2606.13503", "2606.12981"],
            "needles": [
                "on-device",
                "amd kria",
                "forest",
                "depth-aware distillation",
                "distributed",
                "real-time",
                "long-term place recognition",
                "bev fusion",
            ],
            "why": (
                "The day has several papers that force the model story into hardware and field constraints: fall "
                "prediction on an AMD SOM, forest visual place recognition, distributed real-time multi-view tracking, "
                "unstructured-environment LiDAR place recognition, and cooperative BEV fusion. This is where latency, "
                "sensor mix, and place shift become first-class metrics."
            ),
            "confidence": "Medium",
            "confidence_note": "the papers span different domains but share deployment constraints and sensor robustness",
            "lab_action": "Add hardware budget, sensor modality, location shift, and recovery latency to perception benchmark reports.",
            "limit": 5,
        },
    ],
    "research_topics": [
        {
            "title": "World-action interface benchmark",
            "claim": "Compare video prediction, masked world-state querying, and action-token transfer on the same robot or driving episodes.",
        },
        {
            "title": "Trajectory-level VLA safety audit",
            "claim": "Move beyond final success rate by logging instruction trace, action trace, attack/redirection point, and recovery outcome.",
        },
        {
            "title": "Field perception deployment sheet",
            "claim": "For every perception model, record hardware target, sensor mix, shift condition, latency, and failure recovery path.",
        },
    ],
}


if __name__ == "__main__":
    build(PROFILE, "out/cv_new.json", "out/ro_new.json")
