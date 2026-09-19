#!/usr/bin/env python3
"""Generate the 2026-W38 weekly briefing from parser and daily RI artifacts."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-19"
WEEK = "2026-W38"
WEEK_START = "2026-09-13"
WEEK_END = DATE
SOURCE_LISTING_DATE = "2026-09-18"
DAILY_DATES = ["2026-09-14", "2026-09-15", "2026-09-16", "2026-09-17", "2026-09-18"]

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
                arxiv = paper.get("arxiv", "")
                arxiv_id = arxiv_id_from_url(arxiv) if arxiv else paper.get("arxiv_id", "")
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
        "phylum": weekly.get("bucket", "") or daily.get("bucket", ""),
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
    "W38 made robot intelligence a revocation problem. Monday separated visual shortcut, tactile state, map evidence, "
    "risk envelope, and physical world-model claims into auditable interfaces; Tuesday asked which affordance, action head, "
    "geometry update, rollout, token, or navigation commitment is allowed to change behavior; Wednesday converted world-action "
    "models, Gaussian maps, dexterous contact, conformal navigation, and deployment compression into trust gates; Thursday made "
    "adaptation, action tokenization, geometry reliability, active perception, force correction, anomaly detection, and cloud fallback "
    "state when evidence should be accepted or withdrawn; Friday tied the week together by making maps, navigation agents, tactile "
    "world models, adversarial VLA patches, command authorization, scenario generators, and pruning routers expose the exact condition "
    "that should stop, correct, or defer the next robot transition."
)


CLUSTERS = [
    {
        "cluster": "VLA control shifts from bigger backbones to measured action interfaces",
        "ids": [
            "2609.12641",
            "2609.13225",
            "2609.13231",
            "2609.13984",
            "2609.19138",
            "2609.18084",
            "2609.18487",
            "2609.18259",
            "2609.19669",
            "2609.20822",
        ],
        "why_it_matters": (
            "The week repeatedly weakens the idea that VLA reliability is mainly a larger-model problem. Breaking the Vision-Action Shortcut, Part Grounding, ShieldVLA, "
            "and Efficient VLA split perception grounding, feasibility, latency, and action-head design; In-Context Robot Learning, layer-selective adaptation, ActionPiece, "
            "M2Tok, persistent adversarial patches, and obstacle-aware coding agents all ask where action authority enters the system. APRL should evaluate the action interface "
            "that grants or withdraws permission, not just final task success."
        ),
        "confidence": "High - all five daily releases contributed independent VLA evidence around grounding, feasibility, action-head design, tokenization, adaptation, adversarial persistence, or obstacle-aware control.",
        "lab_action": (
            "Run LIBERO/RoboCasa and one real tabletop suite with visual shortcut removal, part grounding, feasibility shield, action-head variants, layer tuning, action tokenization, "
            "persistent adversarial patches, and obstacle-aware code harnesses as separate interventions; compare action delta, unsafe continuation, latency, recovery, and OOD object success."
        ),
    },
    {
        "cluster": "Robot geometry becomes a trust-gated map state rather than reconstruction output",
        "ids": [
            "2609.12557",
            "2609.12221",
            "2609.14634",
            "2609.15795",
            "2609.17387",
            "2609.17168",
            "2609.18465",
            "2609.17810",
            "2609.19518",
            "2609.19628",
            "2609.20348",
            "2609.20589",
        ],
        "why_it_matters": (
            "The geometry signal is not another Gaussian or LiDAR quality contest. DRS-VPT and Chain-SLAM make relocalization and global consistency explicit; SCOUT-SLAM, SURE-Map, "
            "PanoGS-SLAM, HuMemSLAM, GeoCond, Wind on Trees, AMB3R-SLAM, VGGT-GS SLAM, EliGSiR, and RawSLAM ask whether map state remains valid under uncertainty, dynamic 4D motion, "
            "bounded compute, feed-forward priors, HDR radiance, and kilometer-scale loops. The release gate is when the map should be trusted, corrected, or revoked for robot use."
        ),
        "confidence": "High - 67 weekly 3D/Scene ROI papers and repeated SLAM, Gaussian, LiDAR, relocalization, uncertainty, dynamic-scene, bounded-compute, and HDR map evidence trigger the geometry watch lens.",
        "lab_action": (
            "Compare 3DGS maps, LiDAR SLAM, feed-forward Gaussian priors, semantic place recognition, self-correcting maps, bounded-compute RGB-D mapping, and HDR Gaussian SLAM on repeated robot routes with lighting change, dynamic objects, sparse viewpoints, and loop closures; score relocalization, map revocation timing, update cost, uncertainty calibration, and downstream navigation success."
        ),
    },
    {
        "cluster": "Contact-rich manipulation moves from nominal motion to correction authority",
        "ids": [
            "2609.12549",
            "2609.12103",
            "2609.12634",
            "2609.16319",
            "2609.16504",
            "2609.18164",
            "2609.18242",
            "2609.20649",
            "2609.20669",
            "2609.14219",
        ],
        "why_it_matters": (
            "Manipulation papers converge on the same research decision: contact, material, tactile history, energy, and measurement evidence should decide when motion continues or changes. STAR, "
            "RodForesight, material-conditioned diffusion, ConGraspXL, UniDex-ViTac, energy-regularized imitation, ForceDelta-VLA, DexTouch-WM, trajectory-free foresight, and metrological inspection "
            "all move beyond collecting more demonstrations toward specifying which physical variable has correction authority."
        ),
        "confidence": "High - tactile, material, force, dexterous grasping, energy, measurement, and foresight papers recur across the week and share contact-state intervention logic.",
        "lab_action": (
            "Use deformable rods, articulated in-hand manipulation, dexterous bimanual tasks, and metrological inspection with tactile sparsity, material estimate, force correction, energy cost, and foresight horizon as ablation axes; compare slip onset, correction timing, work, measurement error, and recovery success."
        ),
    },
    {
        "cluster": "Embodied navigation becomes evidence gathering before motion commitment",
        "ids": [
            "2609.15098",
            "2609.15142",
            "2609.15195",
            "2609.14806",
            "2609.17499",
            "2609.17628",
            "2609.18581",
            "2609.19554",
            "2609.20191",
            "2609.20388",
        ],
        "why_it_matters": (
            "Navigation and embodied-agent papers repeatedly make motion a revocable commitment. LG-VLN, C2Nav, HarnessVLN, belief-adaptive quadrotor autonomy, ENCP, LEAP, GroundingVLN, VABench, "
            "VLN on the Fly, and Navi-Agent separate route language, geometry anchors, active perception, uncertainty, and onboard constraints before action. The common decision is to gather or verify missing evidence before the robot spends motion authority."
        ),
        "confidence": "High - the evidence-gathering signal appears in zero-shot VLN, quadrotor GNSS degradation, conformal prediction, active perception, embodied spatial benchmarks, aerial onboard stacks, and unlocalized monocular navigation.",
        "lab_action": (
            "Create navigation episodes with missing landmarks, stale maps, GNSS degradation, unknown scale, active perception choices, and onboard compute limits; compare commitment timing, evidence-gathering cost, path regret, conformal abstention, and recovery after a wrong turn."
        ),
    },
    {
        "cluster": "World-action models become closed-loop instruments with falsifiable physical commitments",
        "ids": [
            "2609.12441",
            "2609.14973",
            "2609.14073",
            "2609.13257",
            "2609.17524",
            "2609.16074",
            "2609.16697",
            "2609.20034",
            "2609.20377",
            "2609.20277",
            "2609.19315",
        ],
        "why_it_matters": (
            "World-model work this week is strongest when it states what physical or action consequence would falsify the imagined future. IMPLY, PhysBrain, learned adjudicators, compute-value audits, "
            "modality-autoregressive WAMs, WAM surveys, embodied-intelligence world models, Astronex-World, MM-Future, JEPA-WAM, and GAVEL ask whether a generated state can guide action, scenario stress, "
            "or verification. APRL should test when a generated future is useful enough to enter the loop and when it should be rejected."
        ),
        "confidence": "High - daily and Friday papers repeatedly connect world models to physical consistency, selection value, generated instruction, scenario evaluation, graph verification, and control authority.",
        "lab_action": (
            "Replay manipulation, off-road, and driving episodes with generated futures, physical adjudicators, world-action rollouts, graph constraints, and multi-mode driving predictions; compare physical-state error, action ranking, scenario criticality, verification failures, and closed-loop recovery."
        ),
    },
    {
        "cluster": "Multimodal deployment is judged by decisive evidence surviving pruning, routing, and fallback",
        "ids": [
            "2609.13804",
            "2609.13250",
            "2609.13293",
            "2609.17953",
            "2609.17269",
            "2609.16646",
            "2609.18663",
            "2609.19104",
            "2609.19990",
            "2609.20299",
            "2609.15671",
        ],
        "why_it_matters": (
            "Efficiency and reliability papers are no longer just shrinking models. StepPrune, plug-and-play key-value evaluation, egocentric anticipation, EDCT-Bench, semantic-spatial verification, "
            "hallucination probes, VLA-ULAP, robotic muscle memory, QCPruner, dynamic CLIP layer routing, and question-guided token pruning all ask which evidence survives compression, routing, "
            "fallback, or privacy defense. Deployment wins only if decisive cues remain available when action or refusal depends on them."
        ),
        "confidence": "High - pruning, KV routing, anticipation, counterfactual testing, hallucination diagnosis, cloud fallback, memory, OOD routing, and privacy token pruning all share evidence-retention criteria.",
        "lab_action": (
            "Sweep visual-token pruning, KV routing, local/cloud fallback, muscle-memory cache, dynamic layer routing, privacy pruning, and hallucination probes on robot video and VLM-control tasks; compare decisive-cue recall, action-permission flips, OOD rejection, privacy leakage, latency, and downstream failure."
        ),
    },
]


TOP_PAPERS = [
    (
        "ActionPiece",
        "2609.18487",
        "turns VLA action design into a tokenization contract that can be ablated instead of a hidden decoder detail",
    ),
    (
        "AMB3R-SLAM",
        "2609.19518",
        "makes kilometer-scale SLAM a hierarchical trust-state problem rather than a single trajectory score",
    ),
    (
        "DexTouch-WM",
        "2609.20649",
        "connects tactile world models to action-conditioned correction for dexterous manipulation",
    ),
    (
        "VABench",
        "2609.19554",
        "measures embodied spatial intelligence through demonstration, active perception, and metric control rather than passive QA",
    ),
    (
        "Beyond Patch Removal",
        "2609.19669",
        "shows VLA adversarial effects can persist after apparent visual cleanup, making safety a revocation-timing problem",
    ),
]


AUTOPSY_IDS = [
    "2609.12641",
    "2609.13231",
    "2609.13984",
    "2609.17524",
    "2609.17387",
    "2609.18487",
    "2609.19518",
    "2609.20649",
    "2609.19669",
]


FRONTIER_MEMORY = {
    "new": [
        "W38 adds revocation timing as the shared contract: VLA actions, maps, navigation commitments, generated futures, tactile corrections, and pruned evidence must say when authority expires.",
        "Friday's map stack, adversarial VLA, command authorization, and obstacle-aware coding papers make safety less about detection alone and more about withdrawing permission before the next transition.",
        "Action tokenization and tactile world models appear as actionable system interfaces rather than model-internal representation choices.",
    ],
    "strengthening": [
        "Robot-usable geometry strengthened across relocalization, multi-session LiDAR, self-correcting maps, panoramic 3DGS SLAM, feed-forward Gaussian SLAM, bounded-compute RGB-D mapping, and HDR Gaussian SLAM.",
        "Evidence-gated VLA strengthened from visual shortcut diagnosis through feasibility shields, action-head latency, layer-selective adaptation, action tokenization, adversarial persistence, and obstacle-aware control.",
        "Physical correction strengthened across tactile representation, material-conditioned diffusion, visuo-tactile dexterity, force-aware imitation, and action-conditioned tactile world models.",
    ],
    "commoditizing": [
        "Generic larger-context VLA, prettier Gaussian reconstructions, and lower-latency deployment claims look weak unless they specify the exact evidence variable that changes or revokes action.",
    ],
    "contradiction": [
        "The week rewards richer sensor and memory context while repeatedly warning that stale maps, persistent adversarial cues, over-pruned tokens, and unverified generated futures can create false action authority.",
    ],
    "missing_axis": [
        "No public benchmark yet couples action-interface ablations, map-trust revocation, tactile correction authority, navigation evidence gathering, world-model falsification, and evidence-pruning survival in one robot episode family.",
    ],
}


STRATEGY_BOARD = [
    {
        "opportunity": "Revocation-Timed VLA Evaluation Harness",
        "portfolio": "Build moat",
        "why_now": "W38 repeatedly exposed that VLA, command authorization, adversarial patches, action tokenization, feasibility shields, and obstacle-aware coding all need a transition-level withdrawal signal.",
        "what_others_optimize": "Average success, larger backbones, lower action-head latency, or isolated safety classifiers.",
        "our_contrarian_bet": "APRL should own episodes where evidence says when a policy must stop, switch, ask for help, or fall back before terminal failure.",
        "required_moat": "Robot episodes with visual shortcuts, adversarial residues, infeasible commands, obstacle conflicts, tokenization variants, latency traces, and recovery labels.",
        "scores": {"strategic_fit": 5, "asymmetry": 5, "timing": 5, "tractability": 4, "defensibility": 5, "scientific_depth": 5},
        "score_rationale": {
            "strategic_fit": "Directly matches APRL robot perception, VLA, safety, and failure analysis.",
            "asymmetry": "A small lab can own rare transition failures rather than model scale.",
            "timing": "Action interfaces and safety authorization are emerging before standards settle.",
            "tractability": "A tabletop probe with obstacle, command, and adversarial conditions can start in one week.",
            "defensibility": "Revocation labels and synchronized recovery traces are difficult to copy.",
            "scientific_depth": "The work separates action authority from final task success.",
        },
        "one_week_probe": "Record five manipulation/navigation episodes where a visual shortcut, infeasible command, adversarial patch residue, or obstacle condition should revoke the next action.",
        "four_week_build": "Compare VLA variants, action tokenizers, feasibility shields, local fallback, and obstacle-aware coding agents on the same revocation labels.",
        "success_metric": "Revocation labels predict unsafe continuation and recovery success earlier than terminal success or confidence.",
        "stop_condition": "Stop if revocation labels do not add predictive value beyond ordinary confidence and final success.",
        "paper_path": "Revocation-timed evaluation for evidence-gated VLA control.",
        "asset_path": "Robot videos, action tokens, command states, adversarial residue labels, obstacle maps, fallback traces, and recovery outcomes.",
    },
    {
        "opportunity": "Robot Map Trust-State Protocol",
        "portfolio": "Exploit",
        "why_now": "The week produced unusually dense SLAM and Gaussian map evidence around relocalization, bounded compute, dynamic motion, feed-forward priors, and HDR radiance.",
        "what_others_optimize": "Reconstruction quality, ATE, loop-closure accuracy, or isolated map update speed.",
        "our_contrarian_bet": "A robot map should expose a trust state that predicts when navigation, manipulation, or inspection decisions should use, repair, or reject it.",
        "required_moat": "Repeated routes and tabletop scenes with lighting shifts, dynamic clutter, sparse views, loop closures, bounded-compute updates, and downstream task outcomes.",
        "scores": {"strategic_fit": 5, "asymmetry": 4, "timing": 5, "tractability": 4, "defensibility": 5, "scientific_depth": 5},
        "score_rationale": {
            "strategic_fit": "This is core APRL SLAM, mapping, and robot perception territory.",
            "asymmetry": "Deployment trust-state data beats generic 3D scale.",
            "timing": "Gaussian SLAM and foundation geometry models are converging now.",
            "tractability": "A corridor and tabletop map-trust probe is feasible.",
            "defensibility": "Repeated robot routes and trust labels become reusable assets.",
            "scientific_depth": "Links representation validity to action consequence.",
        },
        "one_week_probe": "Run one robot route under lighting, viewpoint, and moving-clutter shifts; label when map evidence should be trusted, corrected, or ignored.",
        "four_week_build": "Compare LiDAR SLAM, Gaussian SLAM, feed-forward priors, self-correcting maps, bounded-compute RGB-D mapping, and HDR Gaussian SLAM against downstream route and manipulation tasks.",
        "success_metric": "Trust-state labels predict relocalization and task failure better than ATE, PSNR, or update cost alone.",
        "stop_condition": "Stop if standard pose/reconstruction metrics fully explain downstream failures.",
        "paper_path": "Trust-state release gates for robot maps and Gaussian SLAM.",
        "asset_path": "Repeated routes, map states, uncertainty outputs, lighting/dynamic-object labels, relocalization traces, and downstream outcomes.",
    },
    {
        "opportunity": "Contact-Correction Authority Dataset",
        "portfolio": "Build moat",
        "why_now": "Tactile representation, material estimation, force-aware imitation, dexterous grasping, and tactile world models all asked which physical signal may correct motion.",
        "what_others_optimize": "Demonstration volume, final grasp success, or isolated tactile prediction accuracy.",
        "our_contrarian_bet": "APRL can own the correction moment: the instant tactile, material, force, or foresight evidence should change the command.",
        "required_moat": "Synchronized tactile, force, material, vision, action, and recovery traces across deformable, articulated, and dexterous tasks.",
        "scores": {"strategic_fit": 5, "asymmetry": 5, "timing": 4, "tractability": 4, "defensibility": 5, "scientific_depth": 5},
        "score_rationale": {
            "strategic_fit": "Strong fit with APRL manipulation and perception interests.",
            "asymmetry": "Correction traces are harder to scrape than demonstrations.",
            "timing": "Visuo-tactile and tactile world models are getting enough density to standardize evaluation.",
            "tractability": "A small tactile probe can start quickly with a few objects.",
            "defensibility": "Force/tactile correction labels become hard-to-copy assets.",
            "scientific_depth": "The question separates nominal policy from physical evidence authority.",
        },
        "one_week_probe": "Collect ten failed or near-failed contact episodes where tactile, material, or force evidence should change the next command.",
        "four_week_build": "Evaluate tactile representations, material-conditioned policies, force-conditioned correction, and tactile world models on the same correction labels.",
        "success_metric": "Correction authority labels reduce slip, excess work, and reset count before final success diverges.",
        "stop_condition": "Stop if physical correction signals do not predict recovery better than vision-only state.",
        "paper_path": "Contact-correction authority for dexterous robot manipulation.",
        "asset_path": "Tactile streams, force traces, material labels, action corrections, recovery branches, and failure taxonomy.",
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
<table class="cluster-table"><thead><tr><th>Cluster</th><th>Representative papers / 대표 논문</th><th>Why it matters / 왜 중요?</th><th>Confidence</th><th>Lab action</th></tr></thead><tbody>{''.join(cluster_rows)}</tbody></table>
<p class="note">This week's core is not a bigger VLA, prettier map, or cheaper model. It is deciding when evidence should grant, correct, or revoke the next robot transition.</p>

<h2>주간 동향</h2>
<p>September 14 to 18 produced a dense robot-evidence week: {totals['total_scanned']} deduplicated pastweek papers and {totals['selected']} ROI papers, with Robot Learning at {payload['buckets']['Robot Learning']['total']} and 3D/Scene at {payload['buckets']['3D/Scene']['total']}. The count spike matters less than the common research decision. VLA papers, SLAM papers, tactile manipulation papers, embodied navigation papers, world-model papers, and deployment-efficiency papers all ask whether a particular piece of evidence is valid enough to change action.</p>
<p>The strongest shift is revocation. The week did not merely add more maps, memories, tokens, or generated futures; it asked when those sources should lose authority. APRL can turn that into a shared benchmark family where maps, tactile state, action tokens, navigation beliefs, world-model rollouts, and compressed multimodal context must predict the same downstream transition failures.</p>

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
