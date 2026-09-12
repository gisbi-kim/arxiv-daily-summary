#!/usr/bin/env python3
"""Generate the 2026-W37 weekly briefing from parser and daily RI artifacts."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-12"
WEEK = "2026-W37"
WEEK_START = "2026-09-06"
WEEK_END = DATE
SOURCE_LISTING_DATE = "2026-09-11"
DAILY_DATES = ["2026-09-07", "2026-09-09", "2026-09-10", "2026-09-11"]
NO_LISTING_DATES = ["2026-09-08"]

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
    "W37 made robot intelligence an evidence-commitment problem. Monday asked whether VLA success, maps, "
    "world models, VLM explanations, and efficient memories expose the cue that should change action before "
    "failure. Wednesday enlarged that into evidence freshness: policies, maps, occupancy, generated physics, "
    "driving scenes, and navigation beliefs had to show when their support goes stale. Thursday made the same "
    "contract sharper through verifier-aware post-training, uncertainty-aware geometry, relative driving risk, "
    "evidence-order VLM calibration, and irreversible token admission. Friday then converted the week into "
    "transition accountability: a memory, generated future, 3DGS map, safety layer, cache, or dexterous contact "
    "structure is useful only if it states which transition it may authorize and which deployment condition "
    "revokes that authority."
)


CLUSTERS = [
    {
        "cluster": "VLA authority shifts from final success to transition-level evidence gates",
        "ids": [
            "2609.04277",
            "2609.05324",
            "2609.05376",
            "2609.05832",
            "2609.06114",
            "2609.09941",
            "2609.10706",
            "2609.10915",
            "2609.11445",
            "2609.11875",
        ],
        "why_it_matters": (
            "The week repeatedly rejects terminal success as the only VLA evidence. FailureSpot, RoboSPA, and "
            "What Matters When split timestamped failure, spatial-procedural difficulty, and conditional visual grounding; "
            "CR-VLA-Force and Where Success Breaks make force or boundary signals interrupt the policy; HaWMPO, HuRo, "
            "IMLE-VLA, FARM, and UniMPA ask whether imagined worlds, robotized human videos, faster action heads, "
            "predictive states, and memory banks are authorized to change a transition. APRL should evaluate the "
            "permission signal before the final success label."
        ),
        "confidence": "High - every available listing day contributed independent VLA evidence around failure timing, grounding, force, boundary, world-model, pretraining, or memory authority.",
        "lab_action": (
            "Run one manipulation suite with task difficulty, conditional visual grounding, force interruption, failure-boundary labels, world-model rollouts, robotized pretraining, "
            "single-step action heads, predictive-state readouts, and memory banks as separate interventions; compare action delta, warning lead time, jerk, unsafe permission, recovery, and OOD success."
        ),
    },
    {
        "cluster": "Robot geometry release gates move from reconstruction quality to degraded-sensor validity",
        "ids": [
            "2609.04602",
            "2609.05325",
            "2609.07274",
            "2609.09069",
            "2609.10307",
            "2509.06285",
            "2609.11079",
            "2609.10756",
            "2609.11616",
            "2609.11894",
        ],
        "why_it_matters": (
            "The 3D/SLAM signal is not just more Gaussian splats or cleaner registration. NavArena turns 3DGS reconstructions into navigation benchmarks, FIRE-LIVWO and DCReg expose sensor failure and LiDAR degeneracy, "
            "LightSplat and View-Structured conformal prediction add loop closure and uncertainty contracts, and RIDE, GRADE, LangStreet, and mmWave point splatting ask whether geometry survives occlusion, haze, radar sensing, "
            "street semantics, and relocalization. The release gate should be robot validity under degraded evidence, not visual fidelity alone."
        ),
        "confidence": "High - 59 weekly 3D/Scene ROI papers plus repeated SLAM, LiDAR, Gaussian, radar, occupancy, uncertainty, and relocalization evidence trigger the geometry watch lens.",
        "lab_action": (
            "Compare 3DGS maps, LiDAR-inertial-wheel odometry, learned occupancy, conformal 3DGS uncertainty, degenerate LiDAR registration, radar depth, street language fields, and mmWave splats on repeated robot routes with haze, occlusion, dynamic objects, and sparse viewpoints; score relocalization, depth drift, semantic persistence, uncertainty calibration, and downstream navigation success."
        ),
    },
    {
        "cluster": "World models are judged by physical commitments and feedback timing",
        "ids": [
            "2609.04911",
            "2609.05266",
            "2609.06207",
            "2609.10506",
            "2609.09941",
            "2609.11172",
            "2609.11242",
            "2609.11900",
            "2609.11499",
        ],
        "why_it_matters": (
            "World-model papers moved away from plausible videos toward testable physical commitments. TourPhysics and TacPAC make physics and tactile contact influence exploration and correction; PhysWeep asks whether a generator realizes the requested physical variable; DUET-DINO and HaWMPO connect cross-view latent worlds and hallucination-aware rollouts to policy learning; EgoGenEval, Think-with-Video, MindTopo, and Recursive Code World Models separate ego-motion, symbolic rules, topology, and scene programs. APRL should decide which imagined signal may enter control only after testing feedback schedule and physical-state preservation."
        ),
        "confidence": "High - generation, robot learning, and planning papers all converged on physical variable, feedback timing, topology, or executable-scene commitments.",
        "lab_action": (
            "Build matched manipulation and navigation episodes with open-loop imagination, tactile feedback, cross-view latent prediction, ego-motion target views, topological relations, and recursive scene programs; compare physical-state error, topology violation, action ranking, recovery timing, and compute spent per useful correction."
        ),
    },
    {
        "cluster": "Safety and autonomy move into executable hazard and recovery contracts",
        "ids": [
            "2609.05178",
            "2609.05401",
            "2609.10377",
            "2609.10297",
            "2609.10895",
            "2609.10951",
            "2609.10726",
            "2609.11697",
        ],
        "why_it_matters": (
            "Safety was strongest when it stopped being a passive score. LIBERO-RECOVER and ROBORMBENCH expose recovery and reward fragility after apparent success; Data-Driven Risk Fields and TRACE make autonomy decisions depend on relative risk and evidence order; ReactHuman executes committed hazard reactions; Testing Between the Test Cases reasons about steering conditions never driven; information-risk valuation and ActSafeGuard ask when information gathering or a flow-matching action should be blocked. The shared decision is whether evidence has enough operational authority to continue, interrupt, or recover."
        ),
        "confidence": "High - recovery, reward fragility, risk fields, evidence ordering, embodied hazards, formal steering, hazardous exploration, and differentiable constraints form one executable-safety axis.",
        "lab_action": (
            "Use household hazard scenes, LIBERO recovery tasks, CARLA steering intervals, hazardous exploration grids, GUI evidence-order tasks, and flow-policy manipulation with hard constraints; compare reaction deadline, recovery branch quality, unsafe continuation, risk-weighted information gain, intervention count, and trace replayability."
        ),
    },
    {
        "cluster": "VLM and multimodal reliability shifts from confidence to evidence-use diagnostics",
        "ids": [
            "2609.04276",
            "2609.09184",
            "2609.09528",
            "2609.09895",
            "2609.09790",
            "2609.11244",
            "2609.11899",
            "2609.11582",
            "2609.10798",
        ],
        "why_it_matters": (
            "The reliability thread was not merely better calibration. FailSAE tries to expose interpretable VLM failure features; Evidence-Order Calibration tests whether answers survive progressive loss of question-critical evidence; MotionBlind and VidHalLoc probe whether video systems and hallucination detectors see the motion they claim; LogiScope-VQA and OmniHallu turn industrial hazards and cross-modal hallucinations into explicit evidence tests. Caption-once, OmniKVQuant, and RiVaT-Fuse then make frame retrieval, cache compression, and modality trust part of the same evidence-use contract."
        ),
        "confidence": "High - interpretability, evidence-order loss, video hallucination, logistics hazards, cross-modal hallucination, frame routing, KV compression, and modality uncertainty all test whether the model used the right cue.",
        "lab_action": (
            "Evaluate robot VLMs and multimodal agents with decisive-region masking, stale frames, brief motion cues, duplicated views, industrial hazard scenes, hallucinated cross-modal claims, frame-router failures, low-bit KV caches, and missing modalities; compare refusal precision, answer flips, decisive-cue recall, action permission, cache drift, and modality-trust calibration."
        ),
    },
    {
        "cluster": "Embodied contact and navigation become reusable physical-structure tests",
        "ids": [
            "2609.05266",
            "2609.11753",
            "2609.11775",
            "2609.11361",
            "2609.11553",
            "2609.11043",
            "2609.08442",
            "2609.08159",
            "2609.05596",
        ],
        "why_it_matters": (
            "Contact-rich and embodied navigation papers ask which physical structure can be reused across tasks, not just whether a larger dataset solves the task. TacPAC turns tactile prediction into real-time correction, SEED-UMI shares the exoskeleton measurement frame across human and robot, online Jacobian pen writing learns without precollected demonstrations, GeoTrussRover and CAP expose morphology and perception-blind locomotion structure, LTLDiff uses temporal logic in multi-agent manipulation, and AirAnchor, OmniNav, and Time-Aware Assistive Navigation test spatial belief and assistance timing. APRL can own the physical variable, not the average success curve."
        ),
        "confidence": "Medium-High - tactile, exoskeleton, Jacobian, morphology, denoised locomotion, temporal logic, aerial/global anchors, stale navigation beliefs, and timed assistance are coherent but spread across embodiments.",
        "lab_action": (
            "Create dexterous, morphable, aerial, and assistive-navigation tasks with tactile history, shared exoskeleton frame, online Jacobian update, morphology parameter, depth corruption, LTL action order, global-local anchor, and assistive timing as interventions; compare contact stability, transfer success, belief staleness, safe continuation, and recovery cost."
        ),
    },
]


TOP_PAPERS = [
    (
        "FailureSpot",
        "2609.04277",
        "makes VLA failure a timestamped signal rather than a terminal label",
    ),
    (
        "CR-VLA-Force",
        "2609.05832",
        "turns force feedback into an action-interruption contract for contact-rich manipulation",
    ),
    (
        "HaWMPO",
        "2609.09941",
        "asks whether hallucination-aware imagined rollouts deserve policy authority",
    ),
    (
        "RIDE",
        "2609.11079",
        "uses 3DGS relocalization evidence to correct dense robot depth",
    ),
    (
        "ReactHuman",
        "2609.10895",
        "evaluates embodied MLLMs by executed physical reactions to hazards",
    ),
]


AUTOPSY_IDS = [
    "2609.04277",
    "2609.05832",
    "2609.09941",
    "2609.10307",
    "2609.10706",
    "2609.11079",
    "2609.10895",
    "2609.11899",
]


FRONTIER_MEMORY = {
    "new": [
        "The week adds explicit transition accountability: action heads, memories, maps, generated futures, and constraints must state which transition they authorize.",
        "Sep 8 had no arXiv listing in cs.CV or cs.RO, making the week unusually compressed but not incomplete.",
        "Radar, haze, street-language Gaussian fields, and mmWave splats turn degraded sensing into a geometry release gate rather than a side benchmark.",
    ],
    "strengthening": [
        "Evidence admission strengthened across VLA failures, force interruption, verifier-aware post-training, predictive-state readouts, and hard constraints.",
        "Robot-usable geometry strengthened through 3DGS navigation, LiDAR-wheel-radar odometry, learned occupancy, conformal 3DGS, degenerate registration, RIDE, and GRADE.",
        "World-model evaluation strengthened around physical variables, ego-motion, topology, tactile correction, and feedback timing.",
    ],
    "commoditizing": [
        "Generic world-model, VLA scaling, and token-pruning claims look weak unless they expose the specific evidence variable that changes action or recovery.",
    ],
    "contradiction": [
        "The week rewards richer context but repeatedly warns that stale memories, unverified imagined futures, degraded sensors, and compressed caches can create false authority.",
    ],
    "missing_axis": [
        "No public benchmark yet ties transition evidence, degraded-sensor geometry, physical world-model commitments, VLM evidence use, and embodied recovery into one closed-loop robot episode.",
    ],
}


STRATEGY_BOARD = [
    {
        "opportunity": "Transition-Accountability Benchmark for VLA Control",
        "portfolio": "Build moat",
        "why_now": "W37 repeatedly exposed the same gap across failure detection, force feedback, world-model rollouts, robotized pretraining, single-step action heads, and hard constraints.",
        "what_others_optimize": "Most papers still optimize success rate, throughput, or isolated benchmark accuracy.",
        "our_contrarian_bet": "APRL should own the transition-level evidence labels that decide when a policy may continue, interrupt, recover, or fall back.",
        "required_moat": "Robot episodes with transition labels, force events, stale memory, imagined rollout mismatch, predictive-state warning, and recovery outcomes.",
        "scores": {"strategic_fit": 5, "asymmetry": 5, "timing": 5, "tractability": 4, "defensibility": 5, "scientific_depth": 5},
        "score_rationale": {
            "strategic_fit": "Directly matches APRL interests in robot perception, VLA, and failure analysis.",
            "asymmetry": "A small lab can win by owning hard failure episodes rather than model scale.",
            "timing": "The field is naming evidence gates before standards settle.",
            "tractability": "A tabletop probe with force, memory, and recovery labels is feasible in one week.",
            "defensibility": "Curated transition labels and recovery traces are difficult to copy.",
            "scientific_depth": "The benchmark separates evidence authority from final task success.",
        },
        "one_week_probe": "Record five manipulation episodes where force, memory, visual grounding, or predictive-state warning should change the next action.",
        "four_week_build": "Compare VLA, single-step action head, memory bank, force-interruption, and safeguard variants on the same transition labels.",
        "success_metric": "Transition evidence predicts recovery, unsafe continuation, and action correction before terminal success diverges.",
        "stop_condition": "Stop if transition labels add no information beyond terminal success and ordinary confidence.",
        "paper_path": "Transition accountability for evidence-gated VLA control.",
        "asset_path": "Synchronized robot episodes, transition labels, force traces, predictive-state warnings, memory retrieval logs, and recovery outcomes.",
    },
    {
        "opportunity": "Degraded-Sensor Geometry Release Gate",
        "portfolio": "Exploit",
        "why_now": "This week tied 3DGS, LiDAR, radar, learned occupancy, conformal uncertainty, street language fields, and relocalization depth to deployment failures.",
        "what_others_optimize": "Reconstruction appearance, isolated pose error, segmentation accuracy, or rendering quality.",
        "our_contrarian_bet": "A map or reconstruction should enter the robot loop only if it survives the sensor condition that will break the task.",
        "required_moat": "Repeated robot routes with haze, occlusion, sparse views, radar/RGB disagreement, dynamic objects, and downstream action outcomes.",
        "scores": {"strategic_fit": 5, "asymmetry": 4, "timing": 5, "tractability": 4, "defensibility": 5, "scientific_depth": 5},
        "score_rationale": {
            "strategic_fit": "This is core SLAM, mapping, and robot perception territory.",
            "asymmetry": "Deployment-validity scenes beat generic 3D scale.",
            "timing": "Gaussian maps and foundation geometry models are converging now.",
            "tractability": "A corridor and tabletop degraded-sensor suite can start quickly.",
            "defensibility": "Sensor-survival labels and repeated robot routes become reusable assets.",
            "scientific_depth": "The work connects representation uncertainty to action consequence.",
        },
        "one_week_probe": "Collect a small route/tabletop suite with haze, occlusion, sparse views, radar or depth disagreement, and moving clutter.",
        "four_week_build": "Evaluate 3DGS, LiDAR odometry, learned occupancy, conformal uncertainty, radar depth, and street semantic maps against downstream robot tasks.",
        "success_metric": "A degraded-sensor validity score predicts relocalization failure and task failure better than visual quality or ATE alone.",
        "stop_condition": "Stop if ordinary pose or reconstruction metrics fully explain downstream failures.",
        "paper_path": "Robot-usable geometry under degraded sensing.",
        "asset_path": "Sensor-degraded routes, maps, uncertainty outputs, relocalization traces, semantic persistence labels, and downstream outcomes.",
    },
    {
        "opportunity": "Physical-Commitment Gate for World Models",
        "portfolio": "Explore",
        "why_now": "World-model papers this week asked whether generated futures preserve physics, tactile state, ego-motion, topology, and feedback timing.",
        "what_others_optimize": "Visual plausibility, rollout loss, or policy gain in separate setups.",
        "our_contrarian_bet": "A generated future should be blocked from policy authority unless it preserves the physical variable that changes the next action.",
        "required_moat": "Counterfactual futures with tactile/contact labels, camera motion, topology, physical-rule violations, and feedback schedules.",
        "scores": {"strategic_fit": 4, "asymmetry": 5, "timing": 5, "tractability": 3, "defensibility": 4, "scientific_depth": 5},
        "score_rationale": {
            "strategic_fit": "Close to APRL robot execution, though world-model integration may be heavier.",
            "asymmetry": "A validity benchmark can expose failures in larger models.",
            "timing": "World-action model evaluation criteria are unsettled.",
            "tractability": "A replay probe is feasible; full policy integration is harder.",
            "defensibility": "Feedback schedules and physical-failure labels become reusable.",
            "scientific_depth": "The test separates physical commitment from visual fluency.",
        },
        "one_week_probe": "Replay two manipulation and one navigation scene with generated futures that disagree on contact, topology, or ego-motion.",
        "four_week_build": "Compare world models, tactile predictors, topological planners, and hallucination-aware policy updates by action ranking and recovery outcomes.",
        "success_metric": "Physical-commitment metrics predict closed-loop action ranking better than ordinary video quality or rollout score.",
        "stop_condition": "Stop if all world-model metrics rank methods identically after realistic feedback is included.",
        "paper_path": "Physical commitment tests for robot world models.",
        "asset_path": "Rollout traces, physical-variable labels, feedback schedules, topology constraints, counterfactual actions, and policy outcomes.",
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
        "no_listing_dates": NO_LISTING_DATES,
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
    no_listing = ", ".join(payload["no_listing_dates"])
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
<div>Window: {WEEK_START} to {WEEK_END} - daily artifacts: {", ".join(DAILY_DATES)} - no arXiv listing: {no_listing}</div>
<div>Pastweek parser: {totals['total_scanned']} dedup scanned - {totals['selected']} ROI selected</div>
<div>Weekday daily parser totals: cs.CV {daily['cv']} + cs.RO {daily['ro']} - {daily['total_scanned']} scanned - {daily['selected']} ROI selected</div>
</div>
<section class="thesis"><strong>Weekly conclusion:</strong> {esc(payload['weekly_thesis'])}</section>

<h2>주간 클러스터 표</h2>
<table class="cluster-table"><thead><tr><th>Cluster</th><th>Representative papers / 대표 논문</th><th>Why it matters / 왜 중요?</th><th>Confidence</th><th>Lab action</th></tr></thead><tbody>{''.join(cluster_rows)}</tbody></table>
<p class="note">This week's core is not more context, better-looking reconstructions, or faster inference alone. It is deciding which evidence is allowed to change a robot transition, and when that authority expires.</p>

<h2>주간 동향</h2>
<p>September 7, 9, 10, and 11 formed a compressed week because September 8 had no cs.CV or cs.RO arXiv listing. The compression made the research decision clearer rather than weaker: across 1,055 deduplicated pastweek papers and 453 ROI papers, the strongest robotics signal was evidence authority. VLA, geometry, world models, autonomy safety, VLM reliability, efficient agents, dexterity, and navigation all asked whether a cue is fresh, physical, grounded, and useful enough to alter the next action.</p>
<p>The weekly counts are useful context, not the conclusion. Robot Learning led with {payload['buckets']['Robot Learning']['total']} ROI papers, Generation followed with {payload['buckets']['Generation']['total']}, and 3D/Scene reached {payload['buckets']['3D/Scene']['total']}; the deeper shift is that these buckets now share the same release question. Evidence should enter the robot loop only when it changes transition choice, recovery timing, safety margin, map validity, or privacy and compute risk in a measurable way.</p>

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
            "no_listing_dates": NO_LISTING_DATES,
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
