#!/usr/bin/env python3
"""Compute pastweek bucket totals + keywords using classify.py logic."""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# Import BUCKETS keyword list and helpers without running main()
import importlib.util
spec = importlib.util.spec_from_file_location("classify", os.path.join(HERE, "classify.py"))
classify = importlib.util.module_from_spec(spec)
# classify.py reassigns sys.stdout at import — preserve our utf-8 wrapper
saved = sys.stdout
spec.loader.exec_module(classify)
sys.stdout = saved


def main():
    cv_pw = json.load(open("out/cv_pastweek.json", encoding="utf-8"))
    ro_pw = json.load(open("out/ro_pastweek.json", encoding="utf-8"))
    by_id = {}
    for p in cv_pw + ro_pw:
        if p.get("section") == "replace":
            continue
        by_id.setdefault(p["arxiv_id"], p)
    papers = list(by_id.values())
    for p in papers:
        p["bucket"] = classify.assign_bucket(
            p["title"], p.get("abstract", ""), p.get("subjects", "")
        )
        p["badge"] = classify.primary_badge(p)

    from collections import defaultdict
    grouped = defaultdict(list)
    for p in papers:
        if p["bucket"]:
            grouped[p["bucket"]].append(p)

    order = [b for b, _ in classify.BUCKETS]
    out = {
        "date": "2026-05-05",
        "pastweek_total": len(papers),
        "selected": sum(len(grouped[b]) for b in order),
        "buckets": {},
    }
    for b in order:
        items = grouped[b]
        cv_n = sum(1 for p in items if "CV" in p["badge"] and "/" not in p["badge"])
        ro_n = sum(1 for p in items if p["badge"] == "RO")
        cvro_n = sum(1 for p in items if p["badge"] == "CV/RO")
        out["buckets"][b] = {
            "total": len(items),
            "cv": cv_n,
            "ro": ro_n,
            "cvro": cvro_n,
        }

    KW_CV = [
        "gaussian", "3dgs", "nerf", "slam", "vla", "manipulation", "diffusion",
        "generation", "reasoning", "transformer", "benchmark", "llm", "video",
        "3d", "attention", "tokenizer", "agent", "distillation", "retrieval",
        "navigation", "reward", "reinforcement", "quantization", "sparse",
        "moe", "consistency", "flow matching", "t2i", "t2v", "editing",
        "restoration", "segmentation", "detection", "pretraining", "world model",
        "tokenization", "rectified flow", "world-model", "vlm",
    ]
    KW_RO = [
        "vla", "manipulation", "imitation", "sim2real", "reinforcement learning",
        "humanoid", "grasp", "bimanual", "dexterous", "locomotion", "navigation",
        "planning", "tactile", "teleoperation", "policy", "reward", "quadruped",
        "occupancy", "slam", "obstacle", "autonomous", "traffic", "vehicle",
        "vision-language-action", "world model", "trajectory", "exploration",
        "diffusion policy", "rl", "lidar",
    ]

    def kwcount(plist, kws):
        cnt = {k: 0 for k in kws}
        for p in plist:
            text = (p["title"] + " " + p.get("abstract", "")).lower()
            for k in kws:
                if k in text:
                    cnt[k] += 1
        return sorted(cnt.items(), key=lambda x: -x[1])

    cv_papers = [p for p in papers if "cs.CV" in p.get("subjects", "")]
    ro_papers = [p for p in papers if "cs.RO" in p.get("subjects", "")]
    out["keywords_cv"] = kwcount(cv_papers, KW_CV)[:20]
    out["keywords_ro"] = kwcount(ro_papers, KW_RO)[:20]

    with open("out/pastweek_full.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    summary_lines = ["=== Pastweek using classify.py BUCKETS ==="]
    total = 0
    for k, v in out["buckets"].items():
        summary_lines.append(f'  {k}: total={v["total"]} cv={v["cv"]} ro={v["ro"]}')
        total += v["total"]
    summary_lines.append(f"TOTAL: {total}")
    summary_lines.append("Top CV keywords: " + str(out["keywords_cv"][:10]))
    summary_lines.append("Top RO keywords: " + str(out["keywords_ro"][:10]))
    with open("out/pastweek_summary.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(summary_lines))


if __name__ == "__main__":
    main()
