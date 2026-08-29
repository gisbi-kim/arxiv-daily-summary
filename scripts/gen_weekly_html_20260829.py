#!/usr/bin/env python3
"""Generate the 2026-W35 weekly briefing from parser and daily RI artifacts."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-29"
WEEK = "2026-W35"
WEEK_START = "2026-08-23"
WEEK_END = DATE
SOURCE_LISTING_DATE = "2026-08-28"
DAILY_DATES = ["2026-08-24", "2026-08-25", "2026-08-26", "2026-08-27", "2026-08-28"]

BUCKET_ORDER = [
    "3D/Scene",
    "Robot Learning",
    "Autonomous Driving",
    "Foundation Models",
    "Generation",
    "Efficiency/Systems",
    "Embodied AI",
    "Safety/Alignment",
]


def load_json(path: str | Path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def write_json(path: str | Path, payload) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def esc(value) -> str:
    return html.escape(str(value or ""), quote=False)


def arxiv_id_from_url(value: str) -> str:
    return value.rstrip("/").split("/")[-1]


def weekly_lookup(weekly_full: dict) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for bucket_name, bucket in weekly_full.get("buckets_full", {}).items():
        for item in bucket.get("papers", []):
            p = dict(item)
            p["bucket"] = bucket_name
            out[p["arxiv_id"]] = p
    return out


def collect_daily_context() -> dict:
    context = {"trends": {}, "insights": {}, "intelligence": {}, "papers": {}, "autopsies": {}}
    for date in DAILY_DATES:
        trends = load_json(Path("trends") / f"{date}.json")
        insights = load_json(Path("insights") / f"{date}.json")
        intelligence = load_json(Path("intelligence") / f"{date}.json")
        context["trends"][date] = trends
        context["insights"][date] = insights
        context["intelligence"][date] = intelligence

        for cluster in insights.get("clusters", []):
            for paper in cluster.get("papers", []):
                arxiv_id = arxiv_id_from_url(paper.get("arxiv", ""))
                if not arxiv_id:
                    continue
                row = dict(paper)
                row["arxiv_id"] = arxiv_id
                context["papers"].setdefault(arxiv_id, row)

        for paper in intelligence.get("papers", []):
            arxiv_id = paper.get("arxiv_id")
            if not arxiv_id:
                continue
            context["autopsies"][arxiv_id] = dict(paper)
            context["papers"].setdefault(
                arxiv_id,
                {
                    "title": paper.get("title", arxiv_id),
                    "arxiv": f"https://arxiv.org/abs/{arxiv_id}",
                    "arxiv_id": arxiv_id,
                },
            )
    return context


def merge_paper(arxiv_id: str, weekly_papers: dict[str, dict], daily_context: dict) -> dict:
    daily = dict(daily_context["papers"].get(arxiv_id, {}))
    weekly = dict(weekly_papers.get(arxiv_id, {}))
    title = daily.get("title") or weekly.get("title") or arxiv_id
    arxiv = daily.get("arxiv") or f"https://arxiv.org/abs/{arxiv_id}"
    short = title.split(":")[0]
    if len(short) > 90:
        short = short[:87].rstrip() + "..."
    phylogeny = daily.get("phylogeny") or weekly.get("phylogeny") or {
        "source": "tentative",
        "phylum": weekly.get("bucket", ""),
        "class": "weekly representative",
        "order": "research decision",
        "genus": "evidence set",
        "confidence": "Low",
    }
    return {
        "arxiv_id": arxiv_id,
        "title": title,
        "short": short,
        "arxiv": arxiv,
        "badge": daily.get("badge") or weekly.get("badge") or "",
        "bucket": weekly.get("bucket") or daily.get("bucket") or "",
        "importance_tags": daily.get("importance_tags", []),
        "phylogeny": phylogeny,
    }


WEEKLY_THESIS = (
    "W35 turned robot intelligence into an evidence-authorized execution problem. The strongest papers did not "
    "only ask whether a VLA, world-action model, map, or VLM produces the right final output; they asked which "
    "prompt, memory, contact state, geometry token, failure mode, hidden trajectory, or safety margin is allowed "
    "to change the next action before commitment. For APRL, the weekly opportunity is to own a shared release "
    "gate that connects VLA failure recovery, action-faithful imagination, tactile/contact refresh, robot-usable "
    "geometry, evidence retrieval, and calibrated safety clearance inside the same closed-loop episodes."
)


CLUSTERS = [
    {
        "cluster": "VLA authority moves from broad context injection to pre-failure recovery interfaces",
        "ids": ["2608.23224", "2608.23138", "2608.24959", "2608.26578", "2608.26645", "2608.26821"],
        "why_it_matters": (
            "Earlier VLA work often treated language, retrieval, memory, and geometry as helpful context. This week makes them control "
            "interfaces that can disturb or authorize an action: prompt changes need permission, pointing and Gaussian tokens expose spatial "
            "state, configured failures reveal dangerous residuals, recovery becomes a branch, and execution history becomes a supervised "
            "state variable. VLA evaluation should therefore measure when an interface changes the motor command, not only whether the final task succeeds."
        ),
        "confidence": "High - five consecutive weekday artifacts include independent VLA authority, geometry, failure, recovery, and history signals.",
        "lab_action": (
            "Run LIBERO, RoboCasa, and one APRL tabletop task with matched visual states while varying prompt authority, pointing target, Gaussian token, "
            "configured trigger, recovery branch, and history order; compare action delta, intervention timing, object-generalization success, and pre-failure warning."
        ),
    },
    {
        "cluster": "World-action models are judged by action-faithful futures and relative memory controls",
        "ids": ["2608.24885", "2608.23863", "2608.24714", "2608.25956", "2608.27406", "2608.27328"],
        "why_it_matters": (
            "The week repeatedly rejects pretty rollouts as sufficient evidence. Robotic world models are probed for action following, imagined predictions are settled "
            "against later reality, Gaussian scene fields become WAM teachers, 4D Gaussian object state bridges past and future, cross-embodiment videos are treated as "
            "physical simulators, and revisit memory is measured against controls that stop slow-motion shortcuts. The shared decision is to ask whether a generated future "
            "preserves the state that would change a robot action."
        ),
        "confidence": "High - robot, driving, Gaussian, cross-embodiment, and video-memory papers repeat the same action-faithfulness contract.",
        "lab_action": (
            "Create valid but rare robot actions, revisit paths, gripper changes, and object-motion edits where visual plausibility can stay high; compare WAM variants by "
            "SE(3) consequence agreement, contact-order preservation, revisit-memory gain, and policy correction value."
        ),
    },
    {
        "cluster": "Manipulation learning shifts from demonstration volume to contact and embodiment diagnostics",
        "ids": ["2608.21290", "2608.20546", "2608.21355", "2608.24741", "2608.25798", "2608.27079"],
        "why_it_matters": (
            "The manipulation papers do not simply ask for more demonstrations. They expose which state is missing from the demonstration stream: visuotactile temporal "
            "alignment, hardware-specific data capture, human visual-tactile physical properties, physical interaction discovery, tactile refresh during action chunks, "
            "and online reinforcement adaptation for fine-grained manipulation. The weekly signal is that contact state should be an evaluated variable, not a hidden nuisance."
        ),
        "confidence": "High - tactile, gripper, contact-rich, and online-adaptation papers arrive from separate groups and point to the same missing state.",
        "lab_action": (
            "Use one deformable, one thin-object, and one tool-use manipulation task; ablate tactile history, gripper geometry, material property, contact transition, and "
            "online adaptation while scoring slip onset, reset choice, final success, and action-chunk correction."
        ),
    },
    {
        "cluster": "Robot-usable geometry becomes a release gate for maps, calibration, and reconstruction stacks",
        "ids": ["2608.22906", "2608.22896", "2608.25401", "2608.25427", "2608.26868", "2608.26383"],
        "why_it_matters": (
            "The geometry watch lens is strongly triggered. Underwater Gaussian SLAM, spatio-temporal VLN maps, multi-trajectory reconstruction tests, resilient odometry, "
            "collaborative 3DGS SLAM, and cross-platform lab-robot reconstruction benchmarks all move beyond appearance quality. They ask whether the map, calibration, "
            "odometry, and compute stack survive the conditions under which a robot must localize, navigate, or manipulate."
        ),
        "confidence": "High - 43 weekly 3D/Scene ROI papers plus repeated SLAM, LiDAR, Gaussian, calibration, odometry, and robot-compute evidence.",
        "lab_action": (
            "Compare NeRF, 3DGS, feed-forward reconstruction, SLAM, odometry, and registration pipelines on the same robot camera trajectories, low-overlap routes, "
            "tilted surfaces, underwater or lab-object scenes, delayed map sharing, and onboard compute budgets; score scale drift, relocalization, grasp or route success, and update latency."
        ),
    },
    {
        "cluster": "VLM reasoning moves from final answer scoring to evidence acquisition and calibration units",
        "ids": ["2608.20414", "2608.21762", "2608.23011", "2608.24966", "2608.26355", "2608.27417", "2608.27004"],
        "why_it_matters": (
            "Foundation-model reliability papers repeatedly name the evidence unit that should be inspected before trusting an answer. Latent spatial state, crop routing, "
            "long-video evidence granularity, hallucination heads, factor-guided clip retrieval, visual retrieval heads, and medical VLM calibration all make fluent output secondary "
            "to whether the model can locate, request, and calibrate the evidence that supports it."
        ),
        "confidence": "High - spatial-state, long-video, medical, hallucination, and retrieval-head papers independently expose evidence-acquisition failure modes.",
        "lab_action": (
            "Build a compact VLM evaluation with hidden spatial relations, long-video distractors, medical uncertainty, and hallucination-prone object mentions; compare answer accuracy, "
            "evidence localization, crop or clip request quality, confidence calibration, and abstention under the same questions."
        ),
    },
    {
        "cluster": "Autonomy certification moves from closed-course outcomes to pre-commit risk and clearance guarantees",
        "ids": ["2608.21928", "2608.23839", "2608.24094", "2608.25344", "2608.26074", "2608.26533", "2608.26669"],
        "why_it_matters": (
            "Autonomy evaluation is no longer just pass or fail at the route level. Same-scene risk benchmarks, resilience metrics, emergency-vehicle generation, driving risk evidence, "
            "intent-divergence gating, conformal clearance certification, and independent public-road LiDAR tests all move the decision point before the maneuver commits. The useful "
            "artifact is a risk trajectory that can veto or rerank a plan before the failure is visible in terminal metrics."
        ),
        "confidence": "High - embodied, driving, public-road, safety-certification, and multi-agent evidence repeats the pre-commit risk pattern.",
        "lab_action": (
            "Construct public-road, warehouse, and mobile-robot scenarios with same-scene unsafe instructions, emergency vehicles, intent divergence, dense interactions, and clearance tails; "
            "compare closed-loop success, near miss, certified margin, intervention timing, and recovery behavior."
        ),
    },
    {
        "cluster": "Efficiency research shifts from cheaper inference to action-critical evidence preservation",
        "ids": ["2608.21247", "2608.23921", "2608.24063", "2608.25332", "2608.27206", "2608.26806", "2608.26948"],
        "why_it_matters": (
            "Compression and pruning papers are strongest when they state which evidence must survive the speedup. JND-based VLA token compression, head-adaptive token pruning, VLM cache pruning, "
            "critical-token head pruning, condense-and-extract inference, multi-image token pruning, and simple 3DGS compression all imply that latency is not the release criterion. A faster model "
            "must still preserve the spatial, visual, or map evidence needed by the downstream action."
        ),
        "confidence": "Medium-High - efficiency papers share the evidence-preservation decision, though their benchmarks are still fragmented across VLA, VLM, and 3DGS settings.",
        "lab_action": (
            "For the same VLA, VLM, and 3DGS tasks, sweep token budget, cache pruning, attention-head pruning, low-bit quantization, and map compression; compare latency and memory against "
            "spatial grounding error, action delta, localization failure, and downstream task success."
        ),
    },
]


TOP_PAPERS = [
    ("TrapVLA", "2608.26578", "configured failure modes turn VLA safety from terminal failure counting into action-residual control evidence"),
    ("FLARE", "2608.26645", "recovery becomes a first-class policy branch with online arbitration between retry and reset skills"),
    (
        "Do Robotic World Models Really Follow Actions?",
        "2608.24885",
        "world-action models are released only if imagined futures preserve the consequences of valid actions",
    ),
    ("GaussVLA", "2608.24959", "Gaussian spatial tokens make geometry a control-facing evidence interface rather than an offline map artifact"),
    (
        "Cross-Platform Benchmark of Neural 3D Reconstruction for Autonomous Laboratory Robots",
        "2608.26383",
        "reconstruction methods are compared on the compute platforms and downstream adequacy constraints a lab robot actually has",
    ),
]


AUTOPSY_IDS = [
    "2608.26578",
    "2608.26645",
    "2608.24885",
    "2608.24959",
    "2608.26383",
    "2608.26355",
    "2608.27328",
]


FRONTIER_MEMORY = {
    "new": [
        "Configured VLA failure fidelity and recovery arbitration became explicit Friday signals rather than generic robustness language.",
        "Cross-platform lab-robot reconstruction made compute ownership part of the geometry release gate.",
        "Relative revisit-memory controls gave world-model memory a way to avoid rewarding slow or static videos.",
    ],
    "strengthening": [
        "VLA authority repeated across prompt permission, typed pointing, memory, Gaussian spatial reasoning, failure traps, recovery, and execution history.",
        "World-action model evaluation strengthened around action-faithfulness, credit settlement, Gaussian state, cross-embodiment physics, and memory controls.",
        "Robot-usable geometry strengthened through underwater SLAM, VLN maps, multi-trajectory reconstruction, resilient odometry, collaborative 3DGS SLAM, and lab-robot compute benchmarks.",
    ],
    "commoditizing": [
        "Generic VLA context injection, generic video realism, generic 3D reconstruction fidelity, and generic pruning claims look weak unless they expose a control-relevant evidence variable.",
    ],
    "contradiction": [
        "Broad-context VLAs want more prompt, memory, retrieval, and geometry input, while the strongest safety papers insist those inputs need explicit authority boundaries before they touch actions.",
    ],
    "missing_axis": [
        "No weekly paper yet ties configured VLA failures, tactile refresh, robot-usable maps, evidence-gated VLM reasoning, and conformal safety clearance in one closed-loop robot benchmark.",
    ],
}


STRATEGY_BOARD = [
    {
        "opportunity": "Pre-Failure VLA Recovery Benchmark",
        "portfolio": "Build moat",
        "why_now": "The same week produced configured VLA traps, autonomous correction, execution history, prompt authority, and geometry-aware VLA reasoning.",
        "what_others_optimize": "Most papers still optimize final task success, isolated robustness, or context usefulness.",
        "our_contrarian_bet": "APRL should own the failure-shape and recovery-timing protocol before competing on another VLA backbone.",
        "required_moat": "Named failure modes, reset/retry labels, action residual traces, contact events, and recovery outcomes from reproducible robot episodes.",
        "scores": {"strategic_fit": 5, "asymmetry": 5, "timing": 5, "tractability": 4, "defensibility": 5, "scientific_depth": 5},
        "score_rationale": {
            "strategic_fit": "Matches APRL manipulation, robot perception, and evaluation strengths.",
            "asymmetry": "Small labs can win by owning hard failure episodes rather than training scale.",
            "timing": "Failure-mode benchmarks are appearing before a standard protocol has hardened.",
            "tractability": "A ten-episode tabletop probe is feasible within one week.",
            "defensibility": "The moat is the curated failure taxonomy and recovery trace dataset.",
            "scientific_depth": "The research question separates failure onset, recovery authority, and terminal success.",
        },
        "one_week_probe": "Build ten tabletop episodes with prompt perturbation, object pose shift, occlusion, missed grasp, and configured residual targets.",
        "four_week_build": "Evaluate base VLA, prompt-authority VLA, recovery VLA, history-conditioned VLA, and geometry-token VLA under the same failures.",
        "success_metric": "A pre-failure variable predicts or improves recovery at least two action chunks before terminal failure on three failure families.",
        "stop_condition": "Stop if recovery labels do not change policy ranking or intervention timing beyond final success rate.",
        "paper_path": "Configured failure recovery as an evaluation protocol for vision-language-action manipulation.",
        "asset_path": "APRL VLA failure-mode episodes with action residuals, prompts, contact states, resets, and recovery traces.",
    },
    {
        "opportunity": "Action-Faithful World-Action Release Gate",
        "portfolio": "Explore",
        "why_now": "WorldEcho, DreamLedger, GaussianWAM, 4DGS-WAM, CLAP, and R2M-Bench all challenge plausible future generation as a sufficient signal.",
        "what_others_optimize": "Video quality, short-horizon rollout plausibility, or single-embodiment imitation.",
        "our_contrarian_bet": "A learned simulator should be blocked from policy learning unless it preserves action consequences, contact order, and revisit state.",
        "required_moat": "Matched actions, counterfactual futures, revisit controls, contact annotations, and downstream correction measurements.",
        "scores": {"strategic_fit": 4, "asymmetry": 5, "timing": 5, "tractability": 3, "defensibility": 4, "scientific_depth": 5},
        "score_rationale": {
            "strategic_fit": "World-action modeling is adjacent to APRL robot execution and perception.",
            "asymmetry": "The benchmark can expose failures in larger generative systems without matching their scale.",
            "timing": "Multiple groups are now naming action-faithfulness but no shared release gate exists.",
            "tractability": "A small valid-action probe is feasible, but model integration may take more than one week.",
            "defensibility": "Counterfactual action traces and revisit controls become reusable assets.",
            "scientific_depth": "It tests whether imagination carries causal action state rather than visual texture.",
        },
        "one_week_probe": "Create paired rare-action and revisit episodes for two manipulation tasks and one mobile-navigation route.",
        "four_week_build": "Compare video WAM, Gaussian WAM, and cross-embodiment WAM outputs against action consequence, contact, and policy-correction labels.",
        "success_metric": "Action-faithfulness errors predict policy degradation better than visual similarity or frame-level consistency.",
        "stop_condition": "Stop if action-faithfulness probes rank models the same as ordinary video-quality scores.",
        "paper_path": "Action-faithful imagination as a release gate for robot world-action models.",
        "asset_path": "Counterfactual action futures, revisit controls, contact-state labels, and policy-correction outcomes.",
    },
    {
        "opportunity": "Robot-Usable Geometry Validity Suite",
        "portfolio": "Exploit",
        "why_now": "W35 tied Gaussian SLAM, VLN maps, trajectory-aware reconstruction, odometry adaptation, collaborative maps, and lab-robot compute into one evaluation need.",
        "what_others_optimize": "Rendering fidelity, isolated SLAM drift, or benchmark scores detached from the robot compute loop.",
        "our_contrarian_bet": "A map is publishable for robotics only if it predicts localization, route, grasp, or update failure under deployment-like camera and compute conditions.",
        "required_moat": "Robot trajectories, calibration stress, compute profiles, relocalization traces, dynamic-object failures, and downstream task outcomes.",
        "scores": {"strategic_fit": 5, "asymmetry": 4, "timing": 5, "tractability": 4, "defensibility": 5, "scientific_depth": 4},
        "score_rationale": {
            "strategic_fit": "Directly matches APRL SLAM, robot perception, and autonomous lab-robot interests.",
            "asymmetry": "Validity episodes can beat generic reconstruction scale by owning deployment conditions.",
            "timing": "3DGS, feed-forward reconstruction, and SLAM are converging before robotics-specific gates are settled.",
            "tractability": "A corridor and lab-object benchmark can start with existing sensors.",
            "defensibility": "Repeated robot trajectories and compute traces are hard to reproduce casually.",
            "scientific_depth": "It links map representation quality to action-level consequences.",
        },
        "one_week_probe": "Record two robot-camera paths with repeated structures, pose noise, dynamic objects, shiny labware, and onboard/desktop compute profiles.",
        "four_week_build": "Benchmark NeRF, 3DGS, feed-forward reconstruction, SLAM, odometry, and registration under the same route and grasp tasks.",
        "success_metric": "A geometry validity score predicts downstream relocalization, grasp, or route failure better than PSNR-like reconstruction scores.",
        "stop_condition": "Stop if downstream failures are explained entirely by ordinary pose error without representation-specific effects.",
        "paper_path": "Operational validity tests for robot-usable geometry and neural reconstruction.",
        "asset_path": "Robot camera trajectories, calibration files, compute profiles, map updates, pose failures, and task outcomes.",
    },
]


def daily_totals(context: dict) -> dict:
    totals = {"cv": 0, "ro": 0, "selected": 0, "total_scanned": 0}
    for date in DAILY_DATES:
        trend = context["trends"][date]
        counts = trend.get("daily_new_counts", {})
        parsed = trend.get("totals", {})
        totals["cv"] += int(counts.get("cv", 0))
        totals["ro"] += int(counts.get("ro", 0))
        totals["selected"] += int(parsed.get("selected", 0))
        totals["total_scanned"] += int(parsed.get("total_scanned", 0))
    return totals


def paper_link(paper: dict) -> str:
    badge = f" <span class='badge'>{esc(paper.get('badge'))}</span>" if paper.get("badge") else ""
    tags = " ".join(f"<span class='tag'>{esc(tag)}</span>" for tag in paper.get("importance_tags", [])[:2])
    phy = paper.get("phylogeny", {})
    if isinstance(phy, dict):
        phy_parts = [phy.get("source"), phy.get("phylum"), phy.get("class"), phy.get("order"), phy.get("genus")]
        phy_text = " > ".join(str(x) for x in phy_parts if x)
    else:
        phy_text = str(phy)
    return (
        f'<a href="{esc(paper["arxiv"])}" target="_blank" rel="noopener">{esc(paper["short"])}</a>{badge}<br>'
        f'<span class="phy">Phylogeny: {esc(phy_text)}</span><br>{tags}'
    )


def autopsy_card(raw: dict, display_paper: dict) -> dict:
    evidence = raw.get("evidence", [])[:3]
    return {
        "arxiv_id": display_paper["arxiv_id"],
        "title": display_paper["title"],
        "reading_depth": raw.get("status", "reading depth from daily artifact"),
        "status_quo_belief": raw.get("status_quo", ""),
        "friction": raw.get("friction", ""),
        "hidden_premise": raw.get("hidden_premise", ""),
        "conceptual_move": raw.get("conceptual_move", ""),
        "mechanism": raw.get("mechanism", ""),
        "decisive_evidence": evidence,
        "falsification_frontier": raw.get("falsification", ""),
        "adversarial_read": raw.get("adversarial", ""),
        "transferable_thinking_tool": raw.get("thinking_tool", ""),
        "transfer_boundary": raw.get("transfer_boundary", ""),
    }


def build_payload() -> dict:
    weekly_full = load_json("out/weekly_full.json")
    context = collect_daily_context()
    weekly_papers = weekly_lookup(weekly_full)

    clusters = []
    for spec in CLUSTERS:
        reps = [merge_paper(arxiv_id, weekly_papers, context) for arxiv_id in spec["ids"]]
        if len(reps) < 2:
            raise SystemExit(f"cluster has too few representatives: {spec['cluster']}")
        clusters.append({**spec, "representative_papers": reps})

    autopsies = []
    for arxiv_id in AUTOPSY_IDS:
        paper = merge_paper(arxiv_id, weekly_papers, context)
        raw = context["autopsies"].get(arxiv_id, {})
        if raw:
            autopsies.append(autopsy_card(raw, paper))

    buckets = {
        bucket: {k: v for k, v in weekly_full["buckets_full"].get(bucket, {}).items() if k != "papers"}
        for bucket in BUCKET_ORDER
    }
    weekly_totals = {
        "selected": sum(info.get("total", 0) for info in buckets.values()),
        "total_scanned": weekly_full["snapshot"]["totals"]["total_scanned"],
    }

    return {
        "date": DATE,
        "iso_week": WEEK,
        "week_start": WEEK_START,
        "week_end": WEEK_END,
        "source_listing_date": SOURCE_LISTING_DATE,
        "source_mode": "pastweek",
        "source_daily_artifacts": DAILY_DATES,
        "source_prompt": "prompts/instruction_v20260713.md",
        "weekly_thesis": WEEKLY_THESIS,
        "totals": weekly_totals,
        "daily_totals": daily_totals(context),
        "buckets": buckets,
        "clusters": clusters,
        "top_papers": [
            {**merge_paper(arxiv_id, weekly_papers, context), "why": why, "label": label}
            for label, arxiv_id, why in TOP_PAPERS
        ],
        "paper_autopsies": autopsies,
        "frontier_memory": FRONTIER_MEMORY,
        "strategy_board": STRATEGY_BOARD,
    }


def render_html(payload: dict) -> str:
    cluster_rows = []
    for cluster in payload["clusters"]:
        reps = "<br><br>".join(paper_link(paper) for paper in cluster["representative_papers"])
        cluster_rows.append(
            "<tr>"
            f"<td><strong>{esc(cluster['cluster'])}</strong></td>"
            f"<td>{reps}</td>"
            f"<td>{esc(cluster['why_it_matters'])}</td>"
            f"<td>{esc(cluster['confidence'])}</td>"
            f"<td>{esc(cluster['lab_action'])}</td>"
            "</tr>"
        )

    top_items = "".join(
        "<li>"
        f'<a href="{esc(paper["arxiv"])}" target="_blank" rel="noopener"><strong>{esc(paper["label"])}</strong></a>'
        f"<span>{esc(paper['why'])}</span>"
        "</li>"
        for paper in payload["top_papers"]
    )
    bucket_cards = "".join(
        f"<div><span>{esc(bucket)}</span><b>{info.get('total', 0)}</b>"
        f"<small>CV {info.get('cv', 0)} / RO {info.get('ro', 0)} / CVRO {info.get('cvro', 0)}</small></div>"
        for bucket, info in payload["buckets"].items()
    )
    frontier_items = "".join(
        f"<h3>{esc(key)}</h3><ul>" + "".join(f"<li>{esc(item)}</li>" for item in values) + "</ul>"
        for key, values in payload["frontier_memory"].items()
    )
    strategy_items = ""
    for item in payload["strategy_board"]:
        scores = " / ".join(f"{key}: {value}" for key, value in item["scores"].items())
        strategy_items += (
            "<article>"
            f"<h3>{esc(item['opportunity'])}</h3>"
            f"<p><strong>{esc(item['portfolio'])}</strong> - {esc(item['why_now'])}</p>"
            f"<p><b>What others optimize:</b> {esc(item['what_others_optimize'])}</p>"
            f"<p><b>Our contrarian bet:</b> {esc(item['our_contrarian_bet'])}</p>"
            f"<p><b>Required moat:</b> {esc(item['required_moat'])}</p>"
            f"<p><b>Scores:</b> {esc(scores)}</p>"
            f"<p><b>1-week probe:</b> {esc(item['one_week_probe'])}</p>"
            f"<p><b>4-week build:</b> {esc(item['four_week_build'])}</p>"
            f"<p><b>Success metric:</b> {esc(item['success_metric'])}</p>"
            f"<p><b>Stop condition:</b> {esc(item['stop_condition'])}</p>"
            f"<p><b>Paper path:</b> {esc(item['paper_path'])}</p>"
            f"<p><b>Asset path:</b> {esc(item['asset_path'])}</p>"
            "</article>"
        )

    autopsy_items = ""
    for card in payload["paper_autopsies"]:
        evidence_text = "; ".join(
            f"{e.get('trace', '')}: {e.get('claim', '')}" for e in card.get("decisive_evidence", [])
        )
        autopsy_items += (
            "<article>"
            f'<h3><a href="https://arxiv.org/abs/{esc(card["arxiv_id"])}" target="_blank" rel="noopener">{esc(card["title"])}</a></h3>'
            f"<p><b>Reading depth:</b> {esc(card['reading_depth'])}</p>"
            f"<p><b>Status quo belief:</b> {esc(card['status_quo_belief'])}</p>"
            f"<p><b>Friction:</b> {esc(card['friction'])}</p>"
            f"<p><b>Conceptual move:</b> {esc(card['conceptual_move'])}</p>"
            f"<p><b>Mechanism:</b> {esc(card['mechanism'])}</p>"
            f"<p><b>Decisive evidence:</b> {esc(evidence_text)}</p>"
            f"<p><b>Falsification frontier:</b> {esc(card['falsification_frontier'])}</p>"
            f"<p><b>Adversarial read:</b> {esc(card['adversarial_read'])}</p>"
            f"<p><b>Transferable thinking tool:</b> {esc(card['transferable_thinking_tool'])}</p>"
            "</article>"
        )

    daily = payload["daily_totals"]
    totals = payload["totals"]
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>arXiv Weekly Briefing - {WEEK}</title>
<style>
body{{margin:0;background:#eef2f7;color:#1f2937;font:15px/1.72 -apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans KR","Malgun Gothic",sans-serif;padding:28px 12px}}
.wrap{{max-width:1120px;margin:0 auto;background:#fff;border-radius:12px;box-shadow:0 8px 28px #243b5314;padding:42px 52px}}
a{{color:#075bb5;text-decoration:none}}a:hover{{text-decoration:underline}}.home{{display:inline-block;margin-bottom:16px;color:#0969da}}
h1{{font-size:32px;margin:0 0 8px;color:#10233f}}h2{{font-size:23px;margin:42px 0 14px;border-bottom:2px solid #dbe4ef;padding-bottom:8px;color:#10233f}}h3{{font-size:17px;margin:18px 0 8px;color:#10233f}}
.meta{{background:#f8fafc;border-left:4px solid #0891b2;border-radius:8px;padding:14px 18px;color:#42566b;font-size:13px;margin:16px 0 22px}}
.thesis{{background:#10233f;color:#f8fafc;border-radius:12px;padding:19px 23px;font-size:16px}}
.cluster-table{{width:100%;table-layout:fixed;border-collapse:collapse;font-size:13px;margin-top:12px}}
th,td{{border:1px solid #d7dde6;padding:9px;vertical-align:top;overflow-wrap:anywhere}}th{{background:#f1f5f9;color:#10233f}}
.badge{{font-size:11px;background:#fff7ed;border:1px solid #fed7aa;color:#9a3412;border-radius:999px;padding:1px 6px;margin-left:4px}}
.tag{{display:inline-block;font-size:11px;background:#eef6ff;border:1px solid #bfdbfe;color:#1d4ed8;border-radius:999px;padding:1px 6px;margin:2px 2px 0 0}}
.phy{{font-size:11px;color:#64748b}}.bucket-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}}
.bucket-grid div{{background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:10px}}.bucket-grid span{{display:block;font-size:12px;color:#64748b}}.bucket-grid b{{font-size:22px;color:#10233f}}.bucket-grid small{{display:block;color:#64748b}}
.top5 li{{margin:10px 0;padding:12px 14px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px}}.top5 span{{display:block;color:#475569;font-size:13px;margin-top:3px}}
.cards{{display:grid;grid-template-columns:1fr;gap:12px}}.cards article,.strategy article{{border:1px solid #d7dde6;border-radius:12px;padding:16px;background:#fbfdff}}
.strategy{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}.frontier{{background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:18px 22px}}.frontier ul{{margin-top:4px}}
.note{{padding:13px 16px;background:#fff8e1;border-left:4px solid #d97706;border-radius:8px;color:#594315}}footer{{margin-top:38px;padding-top:16px;border-top:1px solid #e2e8f0;color:#64748b;font-size:12px}}
@media(max-width:860px){{.wrap{{padding:26px 20px}}.bucket-grid,.strategy{{grid-template-columns:1fr}}.cluster-table{{font-size:12.5px}}}}
</style>
</head>
<body><main class="wrap">
<a class="home" href="../index.html">Home</a>
<h1>arXiv Weekly Briefing - {WEEK}</h1>
<div class="meta">
<div>Source: arXiv cs.CV/pastweek + cs.RO/pastweek - latest /new listing={SOURCE_LISTING_DATE} - source_mode=pastweek</div>
<div>Window: {WEEK_START} to {WEEK_END} - daily artifacts: {", ".join(DAILY_DATES)}</div>
<div>Pastweek parser: {totals['total_scanned']} dedup scanned - {totals['selected']} ROI selected</div>
<div>Weekday daily parser totals: cs.CV {daily['cv']} + cs.RO {daily['ro']} - {daily['total_scanned']} scanned - {daily['selected']} ROI selected</div>
</div>
<section class="thesis"><strong>Weekly conclusion:</strong> {esc(payload['weekly_thesis'])}</section>

<h2>주간 클러스터 표</h2>
<table class="cluster-table"><thead><tr><th>Cluster</th><th>Representative papers</th><th>Why it matters</th><th>Confidence</th><th>Lab action</th></tr></thead><tbody>{''.join(cluster_rows)}</tbody></table>
<p class="note">This week's core is not a bigger VLA, prettier generated video, or cleaner reconstruction. It is the release gate that proves which evidence may authorize the next action before the robot commits.</p>

<h2>주간 동향</h2>
<p>August 24-28 made one argument through separate communities. Monday introduced certified VLA defenses, temporal-logic conditioning, visuotactile learning, thin-object reconstruction, spatial-state VLM benchmarks, and adaptive world-action imagination. Tuesday turned that into prompt-authority control, typed pointing, unified memory, underwater Gaussian SLAM, geometry WAMs, evidence crop routing, and same-scene risk benchmarks. Wednesday asked whether world models actually follow actions while manipulation papers isolated latency, hierarchy, gripper, trajectory, and contact variables. Thursday tied VLA reasoning to Gaussian spatial evidence, streaming temporal modeling, retrieval adaptation, tactile forcing, reconstruction testbeds, resilient odometry, and intent-divergence gates. Friday converted the week into release gates: configured VLA failures, autonomous correction, execution history, cross-embodiment simulators, collaborative 3DGS SLAM, lab-robot reconstruction compute, long-video evidence retrieval, revisit memory, and conformal safety clearance.</p>
<p>The high-count buckets matter, but the counts are not the conclusion. Robot Learning leads with {payload['buckets']['Robot Learning']['total']} ROI papers, followed by Generation {payload['buckets']['Generation']['total']}, Efficiency/Systems {payload['buckets']['Efficiency/Systems']['total']}, Foundation Models {payload['buckets']['Foundation Models']['total']}, and 3D/Scene {payload['buckets']['3D/Scene']['total']}. The shared movement is that models, maps, and generated futures are being asked to expose the evidence variable that justifies a downstream action.</p>

<h2>Weekly Top 5</h2>
<ol class="top5">{top_items}</ol>

<h2>Weekly paper reasoning autopsy</h2>
<p class="note">These cards reuse the committed daily Research Intelligence artifacts. All listed cards are marked abstract-only unless a daily artifact explicitly recorded deeper reading.</p>
<div class="cards">{autopsy_items}</div>

<h2>Frontier memory</h2>
<div class="frontier">{frontier_items}</div>

<h2>APRL Leading Group Strategy Board</h2>
<div class="strategy">{strategy_items}</div>

<h2>Bucket snapshot</h2>
<div class="bucket-grid">{bucket_cards}</div>

<footer>Generated from repository parser outputs and daily Research Intelligence artifacts. Source prompt: prompts/instruction_v20260713.md.</footer>
</main></body></html>
"""


def main() -> None:
    payload = build_payload()
    write_json(Path("weekly") / f"{WEEK}.json", payload)
    write_json(
        Path("trends") / f"{DATE}.json",
        {
            "date": DATE,
            "iso_week": WEEK,
            "week_start": WEEK_START,
            "week_end": WEEK_END,
            "source_listing_date": SOURCE_LISTING_DATE,
            "source_mode": "pastweek",
            "source_daily_artifacts": DAILY_DATES,
            "source_prompt": "prompts/instruction_v20260713.md",
            "totals": payload["totals"],
            "daily_totals": payload["daily_totals"],
            "buckets": payload["buckets"],
            "clusters": [
                {
                    "cluster": cluster["cluster"],
                    "representative_ids": cluster["ids"],
                    "why": cluster["why_it_matters"],
                    "confidence": cluster["confidence"],
                    "lab_action": cluster["lab_action"],
                }
                for cluster in payload["clusters"]
            ],
            "frontier_memory": FRONTIER_MEMORY,
            "strategy_board": STRATEGY_BOARD,
        },
    )
    post_path = ROOT / "posts" / f"{DATE}-weekly.html"
    post_path.parent.mkdir(exist_ok=True)
    post_path.write_text(render_html(payload), encoding="utf-8", newline="\n")
    print(f"wrote weekly/{WEEK}.json")
    print(f"wrote trends/{DATE}.json")
    print(f"wrote posts/{DATE}-weekly.html")


if __name__ == "__main__":
    main()
