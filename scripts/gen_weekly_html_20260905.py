#!/usr/bin/env python3
"""Generate the 2026-W36 weekly briefing from parser and daily RI artifacts."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-05"
WEEK = "2026-W36"
WEEK_START = "2026-08-30"
WEEK_END = DATE
SOURCE_LISTING_DATE = "2026-09-04"
DAILY_DATES = ["2026-08-31", "2026-09-01", "2026-09-02", "2026-09-03", "2026-09-04"]

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
    "W36 made evidence authority the common interface between VLA policies, world models, maps, VLM judges, "
    "and runtime safety systems. The week began with metric geometry, horizon-aware VLA planning, executable "
    "world representations, and runtime alarms; it then sharpened into freshness-gated maps, typed action "
    "permissions, provenance-conserving fusion, feedback-matched world-model evaluation, and Friday's "
    "evidence-budgeted multimodal training and deployment papers. The weekly opportunity for APRL is to own "
    "a robot benchmark where every sensor, map update, generated future, compressed token set, and evaluator "
    "must prove that it changes action, recovery, privacy risk, or safety margin before it is allowed into the loop."
)


CLUSTERS = [
    {
        "cluster": "VLA authority moves from larger context to evidence-gated action permission",
        "ids": ["2608.27609", "2609.01215", "2609.00908", "2609.01662", "2609.03142", "2609.03276", "2609.04193"],
        "why_it_matters": (
            "The week repeatedly rejects the idea that a VLA should simply consume more prompts, memories, sensors, or demonstrations. "
            "Planning-horizon reasoning, typed motor programs, adaptive chunk stops, provenance-conserving action admission, evidence-gated modality regularization, "
            "real-to-sim behavior evaluation, and action-sufficient intermediate features all ask whether an input is authorized to change a command. "
            "APRL should therefore measure action delta, failure-warning lead time, and fallback timing before trusting context size or final success."
        ),
        "confidence": "High - every weekday produced independent evidence around VLA action authority, stop contracts, provenance, evaluation, or modality gates.",
        "lab_action": (
            "Run one shared manipulation suite with prompt authority, typed skill library, action chunk stop, provenance partition, modality relevance, real-to-sim judge, "
            "and intermediate structural supervision as independent conditions; compare action delta, unsafe permission, failure lead time, recovery success, and judge stability."
        ),
    },
    {
        "cluster": "Robot-usable geometry becomes the release gate for maps, reconstruction, and odometry",
        "ids": ["2608.27497", "2608.28891", "2609.00775", "2609.01899", "2609.02717", "2609.04201", "2609.03561"],
        "why_it_matters": (
            "Geometry papers no longer stop at plausible maps or lower trajectory error. Metric-aware perception, drone-satellite registration, open-vocabulary instance maps, "
            "multi-view 3D tracking, scanner-validated surgical perception, long-video pose repair, and adaptive radar-LiDAR odometry all ask whether recovered state can safely "
            "define route, grasp, surgery, inspection, or localization decisions. APRL's geometry benchmark should connect representation error directly to robot task error."
        ),
        "confidence": "High - daily artifacts include metric geometry, dynamic maps, multi-view tracking, surgical reconstruction, online reconstruction, and radar-LiDAR odometry.",
        "lab_action": (
            "Compare SLAM, Gaussian maps, feed-forward reconstruction, multi-view tracking, weak-label geo-registration, and radar-LiDAR odometry on repeated robot routes, "
            "deforming wires, surgical-like surfaces, and low-observability scenes; score relocalization, scale drift, correspondence failure, contact error, and downstream task success."
        ),
    },
    {
        "cluster": "World models are judged by feedback timing, action consequences, and risk qualification",
        "ids": ["2608.27549", "2609.00188", "2609.02531", "2609.02811", "2609.03681", "2609.03952", "2609.03565", "2609.03774"],
        "why_it_matters": (
            "The week turns world models from plausible future generators into controlled interventions. Executable worlds, video-pretrained WAMs, geometric latent diffusion, "
            "feedback-sensitive rollout evaluation, scheduled imagination, action-aligned reward models, state-aligned JEPA planning, and risk-informed world-model design all "
            "ask which future matters for the next action and when that future should be rejected. APRL should publish correction schedules and stop conditions for every imagined signal."
        ),
        "confidence": "High - action-faithfulness, feedback schedule, physical state, reward chunking, and safety-critical consequence signals recur across the full week.",
        "lab_action": (
            "Create mobile and manipulation episodes with matched open-loop rollouts, intermittent feedback, scheduled imagination, physical-obligation checks, and risk memories; "
            "compare closed-loop ranking, recovery timing, physical-state error, action consequence agreement, and compute spent per useful correction."
        ),
    },
    {
        "cluster": "Contact-rich embodiment shifts from success counting to continuation and recovery conditions",
        "ids": ["2608.29601", "2609.01596", "2609.02358", "2609.02402", "2609.03889", "2609.03591", "2609.03199"],
        "why_it_matters": (
            "Manipulation and HRI papers show that terminal success can hide the physical variables that matter most: tactile data, contact-rich foundation policies, stoppability, "
            "assistive-care force safety, force-aware whole-body compensation, bimanual on-policy correction, and retrieved human demonstrations. The shared weekly move is to decide "
            "when a robot may continue, reset, slow down, change grip, or ask for help before the terminal label arrives."
        ),
        "confidence": "High - tactile, contact, stop, assistive HRI, force-aware compensation, bimanual correction, and web-video retrieval evidence all target physical continuation.",
        "lab_action": (
            "Use deformable, articulated, bimanual, assistive-care, and loco-manipulation tasks with contact geometry, force threshold, tactile history, recovery branch, retrieved demo, "
            "and body compensation ablations; compare safe continuation, force violation, slip onset, reset quality, and task recovery."
        ),
    },
    {
        "cluster": "VLM reliability moves from answer scores to evidence provenance and shortcut tests",
        "ids": ["2608.28316", "2608.28698", "2608.29374", "2609.00232", "2609.00868", "2609.02028", "2609.03611", "2609.03261"],
        "why_it_matters": (
            "VLM papers attack the assumption that a correct or fluent answer proves visual understanding. Conditional evidence utility, state-conditioned retrieval, visual self-correction, "
            "task verification, visual insensitivity, attention-drift masking, robot failure judging, and medical shortcut benchmarks all inspect whether the model used the right evidence. "
            "For robot use, the question is whether evidence changes permission to act, abstain, confirm, or reject an evaluator's ranking."
        ),
        "confidence": "High - answer verification, visual-use diagnostics, provenance, hallucination detection, and robot judge reliability recur from Monday through Friday.",
        "lab_action": (
            "Evaluate robot VLMs and VLM judges with target absence, duplicated views, shortcut-rich questions, masked decisive regions, old-frame retrieval, task invalidity, and physically impossible scenes; "
            "compare refusal precision, evidence-use sensitivity, unsafe action permission, and policy-ranking stability."
        ),
    },
    {
        "cluster": "Efficiency and safety become evidence-retention contracts under budget and uncertainty",
        "ids": ["2608.27808", "2609.00291", "2609.02780", "2609.03158", "2609.03820", "2609.03055", "2609.03699", "2609.03475"],
        "why_it_matters": (
            "Deployment work this week is strongest when it refuses to equate cheaper execution with safer execution. Runtime alarms, adaptive streaming look-depth, shallow video indexing, "
            "token coverage pruning, controlled long-video allocation, robot privacy exports, predictive zonotope reduction, and detector-relative restoration certificates all ask what evidence "
            "or risk bound remains after compression, abstraction, or monitoring. APRL should score budget changes by decisive-cue retention and action-risk change, not latency alone."
        ),
        "confidence": "High - multiple independent systems papers tie compute, privacy, monitoring, restoration, and compression to evidence or risk preservation.",
        "lab_action": (
            "Sweep visual-token budget, frame-retrieval depth, shallow index layer, perception-export abstraction, zonotope reducer, and restoration gate on robot video, home navigation, industrial inspection, "
            "and arm monitoring tasks; compare decisive-cue recall, privacy leakage, false alarms, detector evidence loss, latency, and downstream action delta."
        ),
    },
]


TOP_PAPERS = [
    (
        "Sensing Which Modality Matters",
        "2609.03142",
        "makes multimodal VLA training a sensor-specific evidence admission problem with real-robot occlusion and distractor tests",
    ),
    (
        "Scal3R",
        "2609.04201",
        "separates stable local depth from breaking global pose and repairs online reconstruction through multi-reference pose queries",
    ),
    (
        "Do Better Imagined Rollouts Mean Better Robot Control?",
        "2609.02811",
        "shows world-model evaluation needs the deployment feedback schedule before it can predict closed-loop control ranking",
    ),
    (
        "Not All Agreement Counts as Corroboration",
        "2609.01662",
        "turns multi-view agreement into a provenance-countability test before human-robot action admission",
    ),
    (
        "Seeing Less Is Not Seeing Safely",
        "2609.03055",
        "shows task-scoped robot perception exports can preserve utility while leaking private household structure",
    ),
]


AUTOPSY_IDS = [
    "2609.03142",
    "2609.04201",
    "2609.02811",
    "2609.01662",
    "2609.03611",
    "2609.03055",
    "2609.03681",
    "2609.03561",
]


FRONTIER_MEMORY = {
    "new": [
        "Friday adds a clear evidence-budget axis: sensors, tokens, privacy exports, and imagination steps must prove action relevance before use.",
        "Robot privacy exports appear as an action-release concern rather than a logging or compliance side issue.",
        "World-model scheduling and physical verification make imagination timing a first-class experimental variable.",
    ],
    "strengthening": [
        "Action admission, provenance, and fallback permission strengthened across VLA, HRI, world models, and VLM judge papers.",
        "Robot-usable geometry strengthened through metric perception, dynamic semantic maps, multi-view tracking, surgical reconstruction, pose repair, and radar-LiDAR odometry.",
        "Efficiency work strengthened around decisive-cue retention rather than raw token, frame, or latency reduction.",
    ],
    "commoditizing": [
        "Generic more-data VLA claims, pretty world-model rollouts, and pruning-only speedups look weak unless they expose which evidence variable changed action.",
    ],
    "contradiction": [
        "The same week celebrates broader multimodal robot context and warns that extra context can be redundant, correlated, privacy-leaking, or unsafe without explicit evidence gates.",
    ],
    "missing_axis": [
        "No single public benchmark yet combines modality relevance, robot-usable geometry, world-model feedback timing, VLM judge reliability, privacy leakage, and runtime safety margin in one closed-loop robot episode.",
    ],
}


STRATEGY_BOARD = [
    {
        "opportunity": "Evidence-Budgeted Action Admission Suite",
        "portfolio": "Build moat",
        "why_now": "W36 produced repeated evidence gates across VLA, maps, world models, VLM judges, token pruning, privacy exports, and runtime monitors.",
        "what_others_optimize": "Most papers still optimize isolated success rate, reconstruction score, VQA accuracy, token count, or runtime false positives.",
        "our_contrarian_bet": "APRL should own the shared action-admission protocol that says when evidence is allowed to influence the robot.",
        "required_moat": "Synchronized robot episodes with sensor provenance, modality relevance, map drift, compressed evidence, privacy attack labels, safety margins, and fallback outcomes.",
        "scores": {"strategic_fit": 5, "asymmetry": 5, "timing": 5, "tractability": 4, "defensibility": 5, "scientific_depth": 5},
        "score_rationale": {
            "strategic_fit": "Directly matches APRL robot perception, SLAM, VLA, and safety interests.",
            "asymmetry": "A small lab can win by owning hard evidence episodes rather than model scale.",
            "timing": "The evidence-gate vocabulary is emerging before standards settle.",
            "tractability": "A five-episode probe can be started with existing robots and cameras.",
            "defensibility": "Curated evidence partitions and failure labels become hard-to-copy assets.",
            "scientific_depth": "The question separates evidence authority from final success.",
        },
        "one_week_probe": "Build five episodes with informative, irrelevant, duplicated, missing, and privacy-sensitive evidence sources.",
        "four_week_build": "Benchmark fusion, VLA, map, VLM judge, pruning, privacy export, and runtime-monitor variants on the same admission labels.",
        "success_metric": "Evidence gates change unsafe action permission or recovery timing before final success diverges on three failure families.",
        "stop_condition": "Stop if evidence partitions do not change decisions beyond ordinary confidence or terminal success.",
        "paper_path": "Evidence-budgeted action admission for multimodal robot intelligence.",
        "asset_path": "Robot episodes, synchronized evidence partitions, action deltas, fallback labels, privacy attacks, and safety margins.",
    },
    {
        "opportunity": "Robot-Usable Geometry and Drift Protocol",
        "portfolio": "Exploit",
        "why_now": "The week tied metric geometry, dynamic maps, multi-view tracking, surgical reconstruction, pose repair, and radar-LiDAR odometry into one release-gate problem.",
        "what_others_optimize": "Reconstruction appearance, ATE, correspondence accuracy, or isolated map quality.",
        "our_contrarian_bet": "A map should be accepted only if its error predicts route, grasp, inspection, or safety outcomes under robot deployment conditions.",
        "required_moat": "Robot trajectories, weak-label maps, dynamic scenes, deformable wires, inspection targets, sensor degeneracy, and downstream action outcomes.",
        "scores": {"strategic_fit": 5, "asymmetry": 4, "timing": 5, "tractability": 4, "defensibility": 5, "scientific_depth": 4},
        "score_rationale": {
            "strategic_fit": "Core APRL SLAM and robot perception work.",
            "asymmetry": "Deployment-validity episodes beat generic reconstruction scale.",
            "timing": "3D foundation models, Gaussian maps, and sensor fusion are converging now.",
            "tractability": "A corridor and tabletop probe are feasible in one week.",
            "defensibility": "Repeated robot routes and task outcomes are reusable assets.",
            "scientific_depth": "Links representation error to action consequence.",
        },
        "one_week_probe": "Record two route and tabletop scenes with pose aliases, moving objects, wire-like contacts, and weak semantic labels.",
        "four_week_build": "Compare reconstruction, SLAM, multi-view tracking, semantic maps, and radar-LiDAR odometry against downstream robot tasks.",
        "success_metric": "A robot-validity score predicts action failure better than ATE, PSNR, or segmentation mAP alone.",
        "stop_condition": "Stop if standard pose or segmentation error fully explains downstream failures.",
        "paper_path": "Operational geometry validity for robot maps and reconstruction.",
        "asset_path": "Robot route data, calibration, map states, object/contact annotations, drift labels, and downstream outcomes.",
    },
    {
        "opportunity": "Feedback-Faithful World-Model Release Gate",
        "portfolio": "Explore",
        "why_now": "W36 repeatedly asks whether imagined futures are timed, verified, action-faithful, and risk-qualified.",
        "what_others_optimize": "Visual plausibility, rollout error, video reward, or policy gain in isolation.",
        "our_contrarian_bet": "A world model should be blocked from policy learning unless it preserves the action consequence under the actual feedback schedule.",
        "required_moat": "Counterfactual robot futures, measurement-update schedules, physical-obligation labels, risk memories, and policy-correction outcomes.",
        "scores": {"strategic_fit": 4, "asymmetry": 5, "timing": 5, "tractability": 3, "defensibility": 4, "scientific_depth": 5},
        "score_rationale": {
            "strategic_fit": "Close to APRL robot execution, though model integration may be heavier.",
            "asymmetry": "A validity benchmark can expose failures in larger models.",
            "timing": "WAM and world-model evaluation criteria are still unsettled.",
            "tractability": "A small replay probe is easy; full WAM comparison is harder.",
            "defensibility": "Action-consequence traces and feedback schedules are reusable.",
            "scientific_depth": "Tests causal action state, not visual texture alone.",
        },
        "one_week_probe": "Replay two manipulation and one navigation task with open-loop, intermittent-feedback, and scheduled-imagination variants.",
        "four_week_build": "Compare WAM, JEPA, reward-model, and physical-verifier gates by closed-loop action ranking and recovery outcome.",
        "success_metric": "Feedback-matched metrics predict robot control ranking better than ordinary visual or rollout scores.",
        "stop_condition": "Stop if all metrics rank methods identically once realistic feedback is included.",
        "paper_path": "Feedback-faithful evaluation for robot world-action models.",
        "asset_path": "Rollout traces, feedback schedules, counterfactual actions, physical failures, risk labels, and policy outcomes.",
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
<p class="note">This week's core is not a bigger VLA, prettier generated future, or cheaper inference. It is the evidence-release gate that decides what may change the next robot action.</p>

<h2>주간 동향</h2>
<p>August 31 to September 4 formed one thread across separate communities. Monday made metric geometry, planning horizon, executable worlds, conditional evidence utility, and runtime alarms explicit action-release variables. Tuesday added dynamic 3D memory, typed VLA skill contracts, counterfactual driving affordance, visual evidence verification, and adaptive evidence escalation. Wednesday sharpened the same logic through provenance-countable multi-view fusion, contact-rich continuation, feedback-matched world-model evaluation, collision-intent scenario generation, and streaming evidence retrieval. Friday converted the week into an evidence-budget problem: modality gates, real-to-sim evaluation, world-model scheduling, action-sufficient features, robot judge reliability, coverage-preserving pruning, privacy-aware exports, and runtime uncertainty monitors all ask what evidence is safe to spend.</p>
<p>The weekly counts are useful only as context. Robot Learning, Generation, Foundation Models, Efficiency/Systems, 3D/Scene, Safety/Alignment, Autonomous Driving, and Embodied AI all contributed to the same decision: evidence should be admitted into the robot loop only when it changes action, safety margin, recovery, or privacy risk in a measurable way.</p>

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
