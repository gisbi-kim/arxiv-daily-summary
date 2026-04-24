#!/usr/bin/env python3
"""Classify today's /new papers into ROI buckets by keyword match."""
import io
import json
import re
import sys

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BUCKETS = [
    ("3D/Scene", [
        "3d gaussian", "gaussian splat", "3dgs", "nerf", "neural radiance",
        "slam", "scene reconstruction", "neural implicit", "splatting",
        "3d reconstruction", "point cloud", "mesh", "occupancy grid",
        "photogrammetry", "multi-view stereo", "4d reconstruction",
        "novel view", "lidar", "depth map", "odometry",
    ]),
    ("Robot Learning", [
        "vla", "vision-language-action", "imitation learning", "sim2real",
        "sim-to-real", "teleoperation", "dexterous", "humanoid", "manipulation",
        "grasping", "bimanual", "tactile", "robot learning", "policy learning",
        "robot policy", "demonstrations", "robotic assembly", "pick and place",
        "locomotion", "quadruped", "legged", "gripper",
    ]),
    ("Autonomous Driving", [
        "autonomous driving", "self-driving", "end-to-end driving", "bev",
        "motion planning", "nuscenes", "waymo", "nuplan", "carla",
        "lane detection", "trajectory prediction", "driving policy",
        "driver", "vehicle", "v2x", "traffic",
    ]),
    ("Foundation Models", [
        "vlm", "vision-language model", "multimodal llm", "hallucination",
        "mllm", "visual instruction", "chain-of-thought", "visual reasoning",
        "multimodal understanding", "vision-language pretraining",
        "visual question answering", "vqa",
    ]),
    ("Generation", [
        "diffusion", "video generation", "world model", "3d generation",
        "text-to-image", "t2i", "flow matching", "image editing",
        "video synthesis", "generative model", "inpainting", "outpainting",
        "image synthesis", "dalle", "stable diffusion", "gan",
        "text-to-3d", "text-to-video", "controllable generation",
    ]),
    ("Efficiency/Systems", [
        "sparse", "moe", "mixture of expert", "efficient attention",
        "kv cache", "on-device", "quantization", "pruning", "distillation",
        "compression", "acceleration", "lightweight", "edge device",
        "real-time inference", "low-rank", "lora", "linear attention",
        "token pruning", "token reduction",
    ]),
    ("Embodied AI", [
        "embodied", "navigation", "objectnav", "instruction following",
        "memory-augmented", "vln", "vision-and-language navigation",
        "r2r", "habitat", "embodied agent", "indoor navigation",
        "exploration", "scene graph memory",
    ]),
    ("Safety/Alignment", [
        "vla safety", "rl safety", "ood detection", "adversarial",
        "robust", "safety-critical", "backdoor attack", "jailbreak",
        "alignment", "red team", "certificate", "formal verification",
        "safety constraint", "barrier function", "signal temporal logic",
    ]),
]


def assign_bucket(title: str, abstract: str, subjects: str) -> str:
    """Return the strongest-matching bucket for a paper, or empty string if none."""
    text = (title + " " + abstract + " " + subjects).lower()
    best = ""
    best_hits = 0
    for bucket, kws in BUCKETS:
        hits = sum(1 for kw in kws if kw in text)
        if hits > best_hits:
            best_hits = hits
            best = bucket
    return best if best_hits > 0 else ""


def primary_badge(paper) -> str:
    subj = paper.get("subjects", "")
    cv = "cs.CV" in subj
    ro = "cs.RO" in subj
    # Primary cat is what the paper was submitted under.
    primary = paper.get("primary_cat", "")
    if primary == "cs.CV" and ro:
        return "CV/RO"
    if primary == "cs.RO" and cv:
        return "CV/RO"
    if "cs.CV" == primary:
        return "CV"
    if "cs.RO" == primary:
        return "RO"
    if cv and ro:
        return "CV/RO"
    if cv:
        return "CV"
    if ro:
        return "RO"
    return primary or "?"


def main():
    cv = json.load(open("out/cv_new.json", encoding="utf-8"))
    ro = json.load(open("out/ro_new.json", encoding="utf-8"))
    # Merge and dedupe on arxiv_id. Prefer CV source when duplicate.
    by_id = {}
    for p in cv + ro:
        if p["section"] == "replace":
            continue
        by_id.setdefault(p["arxiv_id"], p)
    papers = list(by_id.values())
    # Classify
    for p in papers:
        p["bucket"] = assign_bucket(p["title"], p.get("abstract", ""), p.get("subjects", ""))
        p["badge"] = primary_badge(p)
    # Group
    from collections import defaultdict
    grouped = defaultdict(list)
    for p in papers:
        if p["bucket"]:
            grouped[p["bucket"]].append(p)
    # Output summary
    order = [b for b, _ in BUCKETS]
    result = {
        "total": len(papers),
        "selected": sum(len(grouped[b]) for b in order),
        "buckets": {},
    }
    for b in order:
        items = grouped[b]
        cv_n = sum(1 for p in items if "CV" in p["badge"] and "/" not in p["badge"])
        ro_n = sum(1 for p in items if p["badge"] == "RO")
        cvro_n = sum(1 for p in items if p["badge"] == "CV/RO")
        result["buckets"][b] = {
            "total": len(items),
            "cv": cv_n,
            "ro": ro_n,
            "cvro": cvro_n,
            "papers": items,
        }
    print(json.dumps(result, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
