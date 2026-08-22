#!/usr/bin/env python3
"""Generate the 2026-W34 weekly briefing from parser and daily RI artifacts."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-22"
WEEK = "2026-W34"
WEEK_START = "2026-08-16"
WEEK_END = DATE
SOURCE_LISTING_DATE = "2026-08-21"
DAILY_DATES = ["2026-08-17", "2026-08-18", "2026-08-19", "2026-08-20", "2026-08-21"]

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
    if len(short) > 88:
        short = short[:85].rstrip() + "..."
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
    "This week made robot intelligence accountable before execution. Across VLAs, world-action models, "
    "geometry, safety, and generative models, the repeated question was not whether the final rollout "
    "succeeded; it was which observation, contact state, map property, predicate, latent future, or "
    "scenario condition had authority to change or veto the next action. For APRL, the defensible asset "
    "is a shared evidence-gated evaluation protocol that connects VLA adaptation, contact forecasting, "
    "map degeneracy, scenario-conditioned policy confidence, and process-valid generated worlds in the "
    "same closed-loop episodes."
)


CLUSTERS = [
    {
        "cluster": "VLA control shifts from policy outputs to runtime authority interfaces",
        "ids": ["2608.14047", "2608.14822", "2608.17209", "2608.16978", "2608.19490", "2608.19589", "2608.19613"],
        "why_it_matters": (
            "The week repeatedly exposes a measurable interface that can change a VLA action before terminal success is known: "
            "tool use, counterfactual recovery, skill-block composition, closed-loop code replanning, self-demonstrated adaptation, "
            "continual skill subspaces, and latent-action choices. This turns VLA evaluation from a single success rate into an "
            "authority audit over who may rewrite, route, adapt, or preserve an action."
        ),
        "confidence": "High - every weekday contributed a distinct VLA or robot-learning paper that localizes execution authority.",
        "lab_action": (
            "Run the same tabletop and mobile-manipulation perturbations through tool-use, recovery, skill-library, code-replanning, "
            "self-demonstration, skill-subspace, and latent-action variants; score next-action delta, old-skill forgetting, intervention "
            "timing, and clean-task success."
        ),
    },
    {
        "cluster": "World-action models become pre-commit forecasts for contact, safety, and whole-body state",
        "ids": ["2608.13678", "2608.14986", "2608.17496", "2608.19085", "2608.19574", "2608.20114", "2608.20284"],
        "why_it_matters": (
            "World models this week were not just future-video generators. They carried temporal-logic state, Gaussian scene memory, "
            "action-conditioned risk, decision-aligned driving latents, tactile contact hierarchy, decoupled base-arm futures, and "
            "surgical visual-trajectory forecasts. The shared research decision is to forecast the hidden state that would make the "
            "next action unsafe, ineffective, or worth repairing."
        ),
        "confidence": "High - navigation, manipulation, driving, safety, tactile, whole-body, and surgical papers repeat the pre-commit forecast pattern.",
        "lab_action": (
            "Create paired episodes where visual plausibility stays high but predicate state, tactile state, base-arm coupling, risk, "
            "or trajectory future changes; compare world-action objectives by action correction, safety veto, and recovery outcome."
        ),
    },
    {
        "cluster": "Robot-usable geometry is judged by operational validity rather than reconstruction quality",
        "ids": ["2608.14266", "2608.15024", "2608.17553", "2608.18028", "2608.19066", "2608.19522", "2608.19536"],
        "why_it_matters": (
            "Geometry papers repeatedly ask whether a map can survive robot use: LiDAR mapping must scale, event-modulated Gaussian "
            "SLAM must handle motion blur, monocular SLAM must carry uncertainty into scale, bundle adjustment must prove metric validity, "
            "GS-VLA must make viewpoint canonicalization affect a frozen policy, LiDAR odometry must reveal degeneracy axes, and registration "
            "must transfer across sensors and density shifts."
        ),
        "confidence": "High - 53 weekly 3D/Scene ROI papers plus multiple SLAM, LiDAR, Gaussian, BA, and registration signals trigger the geometry watch lens.",
        "lab_action": (
            "Compare SLAM, BA, Gaussian maps, viewpoint canonicalization, LiDAR odometry, and registration systems on corridors, tunnels, "
            "camera shifts, sparse views, dynamic objects, and sensor-density changes; score scale drift, localizability, registration failure, "
            "and downstream route or grasp recovery."
        ),
    },
    {
        "cluster": "Reliability moves from confidence to evidence authorization and abstention state",
        "ids": ["2608.13719", "2608.15410", "2608.17386", "2608.17318", "2608.17205", "2608.19739", "2608.20084", "2608.19376"],
        "why_it_matters": (
            "Reliability work made the evidence path explicit. Active evaluation searches for paired-system failures, flood response benchmarks "
            "preserve physical context, MANIGUARD separates task success from safety predicates, CondVLN isolates branch decisions, Which Source Wins "
            "tests modality authority, question-guided VQA acquires missing evidence, evidence-gated TAMP blocks unsupported subgoals, and conformal "
            "VLM audits show class tails can fail despite marginal coverage."
        ),
        "confidence": "High - safety, VLM, navigation, and TAMP papers independently expose authorization, abstention, or predicate evidence.",
        "lab_action": (
            "Build episodes with hidden objects, branch predicates, image-text conflict, flood-like degraded evidence, class-tail shifts, and safety "
            "constraints; compare answer accuracy, evidence acquisition, abstention, unsupported subgoal rate, predicate violation, and task outcome."
        ),
    },
    {
        "cluster": "Benchmark assets shift from bigger datasets to hidden-state labels",
        "ids": ["2608.18701", "2608.18618", "2608.19425", "2608.19372", "2608.19968", "2608.20251", "2608.20308"],
        "why_it_matters": (
            "The strongest benchmark papers name the state that final success hides: deformable-object state, lab-subtask hierarchy, scenario family, "
            "spatially distributed tactile feedback, assembly dependency, simulation-ready door articulation, and occluded egocentric hand trajectories. "
            "The durable asset is a label taxonomy for failure and recovery, not merely more demonstrations."
        ),
        "confidence": "High - manipulation and evaluation papers repeat hidden-state labels across deformable, dexterous, scenario, tactile, assembly, door, and hand-motion settings.",
        "lab_action": (
            "Annotate a compact manipulation and loco-manipulation set with material deformation, subtask boundary, scenario family, tactile coverage, "
            "assembly dependency, articulated door state, and occluded hand trajectory; compare final success against each hidden-state label."
        ),
    },
    {
        "cluster": "Generated worlds are tested by causal process validity, not local image realism",
        "ids": ["2608.19583", "2608.20107", "2608.19556", "2608.19723", "2608.19085", "2608.20284", "2608.20336"],
        "why_it_matters": (
            "Generative papers asked whether the output preserves the process a robot or planner would rely on. VGI-BENCH probes evolving processes, "
            "BeyondMasks demands causal and physical side effects after object removal, Stream4D attacks 4D drift, StreamSoccer uses bounded event memory, "
            "DA-WAM aligns latents with driving decisions, surgical WAM couples visual and trajectory futures, and WithEveryone binds identities to locations."
        ),
        "confidence": "Medium-High - generation, driving, surgical, and identity-grounding papers share process-validity evidence, though downstream robot use remains uneven.",
        "lab_action": (
            "Generate scenes where the final frame looks plausible but object permanence, contact order, physical side effects, route decision, surgical "
            "trajectory, event memory, or identity binding can fail; score planner action error and reject generated data that preserves appearance but breaks process state."
        ),
    },
]


TOP_PAPERS = [
    ("Imagining Recovery", "2608.14822", "counterfactual VLA realignment makes recovery an inference-time interface rather than a retraining afterthought"),
    ("Teach and Grow", "2608.17209", "skill-block composition turns general robot learning into a reusable execution-authority problem"),
    ("MANIGUARD", "2608.17386", "safety predicates become independent evidence that can fail even when the manipulation task succeeds"),
    ("GS-VLA", "2608.19066", "Gaussian viewpoint canonicalization connects geometry directly to frozen VLA action robustness"),
    ("HiTac-WAM", "2608.19574", "tactile future forecasting makes hidden contact state a pre-commit action signal"),
]


AUTOPSY_IDS = ["2608.14822", "2608.17209", "2608.17386", "2608.19066", "2608.19574", "2608.20084"]


FRONTIER_MEMORY = {
    "new": [
        "Friday added explicit evidence-gated TAMP and class-conditional VLM coverage to the week-long evidence-authority theme.",
        "Whole-body and tactile world-action models made hidden contact and base-arm factorization more explicit than earlier weekly artifacts.",
    ],
    "strengthening": [
        "Runtime interfaces repeated all week: tool use, counterfactual recovery, process rewards, code replanning, self-demonstration, latent actions, and safety gates.",
        "Robot-usable geometry strengthened through Gaussian scene memory, MotionGS-SLAM, uncertainty-aware SLAM, bundle-adjustment validity, GS-VLA, and degeneracy-aware LiDAR odometry.",
    ],
    "commoditizing": [
        "Generic VLA scaling, generic video realism, and generic reconstruction quality look less defensible unless they expose an action-relevant evidence variable.",
    ],
    "contradiction": [
        "Flexible VLA behavior wants broad semantic transfer, while evidence gates, safety predicates, and scenario conditioning deliberately restrict when actions are allowed.",
    ],
    "missing_axis": [
        "No single benchmark yet ties VLA adaptation, evidence-gated planning, tactile forecasting, and map degeneracy into one closed-loop robot episode.",
    ],
}


STRATEGY_BOARD = [
    {
        "opportunity": "Evidence-Gated Execution Benchmark",
        "portfolio": "Build moat",
        "why_now": "Every weekday produced a paper that asks which cue, predicate, memory, map, or latent is allowed to authorize an action.",
        "contrarian_bet": "APRL should own the authorization protocol instead of competing first on another VLA backbone.",
        "scores": {"strategic_fit": 5, "asymmetry": 5, "timing": 5, "tractability": 4, "defensibility": 5, "scientific_depth": 5},
        "one_week_probe": "Create ten mobile-manipulation episodes with hidden objects, cue conflicts, safety predicates, and map degeneracy labels.",
        "four_week_build": "Evaluate VLM-TAMP, VLA, tool-use, safety-shield, and map-aware policies with shared authorization traces.",
        "success_metric": "Evidence labels predict or prevent at least three unsupported actions before terminal failure while preserving clean-task success.",
        "stop_condition": "If authorization labels do not change policy ranking or recovery choice, split into planning-only and perception-only tracks.",
        "paper_path": "Evidence-gated execution for reliable mobile manipulation.",
        "asset_path": "APRL evidence-gated episodes with observations, predicates, map states, action deltas, and recovery outcomes.",
    },
    {
        "opportunity": "Contact and Whole-Body World-Action Suite",
        "portfolio": "Build moat",
        "why_now": "HiTac-WAM, DECOWAM, surgical WAM, DA-WAM, and safety JEPA make future-state quality accountable to candidate actions.",
        "contrarian_bet": "Treat hidden tactile and body-state forecasts as the moat, not video fidelity or generic latent prediction.",
        "scores": {"strategic_fit": 5, "asymmetry": 5, "timing": 4, "tractability": 4, "defensibility": 5, "scientific_depth": 5},
        "one_week_probe": "Instrument one door traversal, one dexterous grasp, and one base-arm task with tactile, ego-motion, and action-chunk labels.",
        "four_week_build": "Compare tactile WAM, whole-body WAM, decision-aligned latent, and action-conditioned safety models under matched episodes.",
        "success_metric": "A hidden forecast variable predicts next-action correction or safety veto earlier than visual future quality.",
        "stop_condition": "If hidden forecasts do not improve action correction beyond previous-action baselines, reduce scope to tactile-only tasks.",
        "paper_path": "Pre-commit world-action evidence for contact-rich mobile manipulation.",
        "asset_path": "Tactile traces, ego/arm action factors, action chunks, latent futures, and recovery labels.",
    },
    {
        "opportunity": "Robot-Usable Geometry Validity Protocol",
        "portfolio": "Exploit",
        "why_now": "The week connected geometry to policy viewpoint, scale, localizability, registration transfer, and route recovery.",
        "contrarian_bet": "Avoid rendering-fidelity competition by owning the validity tests that determine whether a map can guide a robot.",
        "scores": {"strategic_fit": 5, "asymmetry": 4, "timing": 5, "tractability": 4, "defensibility": 5, "scientific_depth": 4},
        "one_week_probe": "Record two corridor and tabletop scenes with scale drift, repeated structure, dynamic objects, and camera shifts.",
        "four_week_build": "Compare LiDAR odometry, monocular SLAM, Gaussian maps, BA, and registration systems on the same downstream route or grasp tasks.",
        "success_metric": "A geometry validity metric predicts route or grasp failure better than photometric, APD, or optimizer scores.",
        "stop_condition": "If validity metrics do not change downstream decisions, narrow the claim to localization diagnostics.",
        "paper_path": "Operational validity tests for robot geometry and SLAM.",
        "asset_path": "Scale ground truth, localizability fields, registration shifts, pose failures, and task outcome logs.",
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
    strategy_items = "".join(
        "<article>"
        f"<h3>{esc(item['opportunity'])}</h3>"
        f"<p><strong>{esc(item['portfolio'])}</strong> - {esc(item['why_now'])}</p>"
        f"<p><b>Contrarian bet:</b> {esc(item['contrarian_bet'])}</p>"
        f"<p><b>1-week probe:</b> {esc(item['one_week_probe'])}</p>"
        f"<p><b>4-week build:</b> {esc(item['four_week_build'])}</p>"
        f"<p><b>Success metric:</b> {esc(item['success_metric'])}</p>"
        f"<p><b>Stop condition:</b> {esc(item['stop_condition'])}</p>"
        f"<p><b>Paper path:</b> {esc(item['paper_path'])}</p>"
        f"<p><b>Asset path:</b> {esc(item['asset_path'])}</p>"
        "</article>"
        for item in payload["strategy_board"]
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
<p class="note">This week's core is not another VLA, world model, or 3D map. It is whether the system can name the evidence that authorizes the next action before the robot commits.</p>

<h2>주간 동향</h2>
<p>August 17-21 forms one execution-evidence arc. Monday wrapped VLA behavior with tools, process judges, fast reaction paths, belief memory, temporal logic, and failure-discovery evaluation. Tuesday made runtime evidence control explicit through counterfactual VLA recovery, tactile residuals, process rewards, Gaussian scene memory, and physical-condition benchmarks. Wednesday split execution authority into skill blocks, code rewrites, force reflexes, safety shields, metric geometry, and source-provenance diagnostics. Thursday and Friday turned the same idea into benchmark assets: deformation state, lab hierarchy, decision-aligned latents, evidence-gated TAMP, tactile world-action forecasts, LiDAR degeneracy, and causal process tests for generated worlds.</p>
<p>The highest-signal weekly trend is therefore not bucket growth alone, though Robot Learning leads with {payload['buckets']['Robot Learning']['total']} ROI papers and Generation follows with {payload['buckets']['Generation']['total']}. The trend is that separate communities are converging on a pre-commit evidence contract: an action, subgoal, map, or generated future should state what evidence made it permissible.</p>

<h2>Weekly Top 5</h2>
<ol class="top5">{top_items}</ol>

<h2>Weekly paper reasoning autopsy</h2>
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
