#!/usr/bin/env python3
"""Generate the 2026-W33 weekly briefing from parser and daily RI artifacts."""
from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-15"
WEEK = "2026-W33"
WEEK_START = "2026-08-09"
WEEK_END = DATE
SOURCE_LISTING_DATE = "2026-08-14"
DAILY_DATES = ["2026-08-10", "2026-08-11", "2026-08-12", "2026-08-13", "2026-08-14"]

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
    "This week moved robotics away from after-the-fact success scoring and toward pre-commit evidence contracts. "
    "Across VLA memory, world-action models, synthetic manipulation data, active navigation, geometry, and VLM reliability, "
    "the strongest papers ask what intermediate state can justify, veto, or repair the next action before the final failure is visible. "
    "For APRL, the defensible asset is not another larger policy; it is a shared failure-evidence protocol that measures memory state, "
    "physical world state, contact transfer, map uncertainty, and abstention or routing signals in the same closed-loop episodes."
)


CLUSTERS = [
    {
        "cluster": "VLA control moves from success-rate reporting to evidence-bearing execution contracts",
        "ids": ["2608.06729", "2608.07596", "2608.11671", "2608.13438", "2608.13474", "2608.11739"],
        "why_it_matters": (
            "Earlier VLA evaluation often treated a rollout as a black-box pass or fail. The week repeatedly exposes the state that comes before the action: "
            "persistent world-ego memory, local cross-layer routing, structured demonstrations, pre-contact latent futures, and progress probes. "
            "That changes the lab question from which policy wins to which evidence field can explain or veto a wrong action early enough to recover."
        ),
        "confidence": "High — every weekday contributed a distinct VLA paper that exposes memory, routing, demonstration structure, progress, or veto evidence.",
        "lab_action": (
            "Run one manipulation suite with direct VLA, memory-augmented VLA, routed action decoder, structured-demonstration VLA, and pre-contact monitor variants; "
            "compare failure-prediction lead time, veto precision, recovery success, and the exact action chunk each evidence field changes."
        ),
    },
    {
        "cluster": "World-action models become failure-conditioned planning and repair interfaces",
        "ids": ["2608.06799", "2608.07619", "2608.11204", "2608.10232", "2608.11174", "2608.12854", "2608.13489"],
        "why_it_matters": (
            "The world-model papers do not just ask for plausible futures. They ask whether physical state, geometry-aware latent state, surgical action state, "
            "failure-aware causal training, planning-relevant quality scores, or action-space coordination can change the next decision. "
            "World models are becoming interfaces for intervention, not only generators of better-looking videos."
        ),
        "confidence": "High — physical grounding, geometry, surgery, causal failure, quality diagnosis, driving, and manipulation all repeat the same planning-interface decision.",
        "lab_action": (
            "Compare visual-only, physical-state, geometry-aware, failure-causal, and action-conditioned world models on identical branches; "
            "measure whether each representation changes candidate action choice, contact failure, unsafe driving state, or recovery latency before final task score."
        ),
    },
    {
        "cluster": "Robot data quality shifts from demonstration volume to action-sensitive contact and embodiment transfer",
        "ids": ["2608.07045", "2608.06827", "2608.13049", "2608.13028", "2608.12416", "2608.13014", "2608.13489"],
        "why_it_matters": (
            "The week treats data as useful only when it preserves the variables that actually move robot behavior: contact consistency, sparse real-to-sim alignment, "
            "human-to-robot embodiment transfer, RGB-D handover timing, synthesized dexterity, force estimation, and action-conditioned futures. "
            "The actionable distinction is no longer real versus synthetic; it is whether the data changes a policy boundary under the same contact and embodiment constraints."
        ),
        "confidence": "High — contact, handover, retargeting, synthetic dexterity, egocentric force, and action-conditioned generation form a shared data-selection axis.",
        "lab_action": (
            "Under a fixed data budget, compare random demos, contact-consistent retargets, sparse real-to-sim clips, human-to-robot generated clips, and failure-correction examples; "
            "score contact timing, force plausibility, embodiment mismatch, imitation delta, and OOD execution success."
        ),
    },
    {
        "cluster": "Embodied navigation and geometry turn maps into executable evidence states",
        "ids": ["2608.07267", "2608.12683", "2608.12707", "2608.12860", "2608.13095", "2608.12825", "2608.08949", "2608.09146"],
        "why_it_matters": (
            "Navigation and geometry papers converge on the same decision: the map or view must justify an action, not just describe the scene. "
            "World navigation conditioning, active affordance views, open-vocabulary object navigation, humanoid VLN physics, semantic radiance-field simulators, "
            "spatially grounded 3DGS tokens, endoscopic Gaussian SLAM, and neural submaps all expose sensor source, uncertainty, association, or embodiment constraints."
        ),
        "confidence": "High — geometry and embodied-navigation evidence recurs across 3DGS, SLAM, semantic maps, active views, and humanoid embodiment.",
        "lab_action": (
            "Build paired navigation and tabletop scenes where one extra view, semantic map field, submap update, or Gaussian token can change the route or grasp plan; "
            "measure relocalization time, association flips, active-view value, route recovery, and downstream manipulation or navigation success."
        ),
    },
    {
        "cluster": "Reliability shifts from confidence calibration to early warning, abstention, routing, and attack-aware action guards",
        "ids": ["2608.07065", "2606.29699", "2608.09448", "2608.10835", "2608.12127", "2608.13167", "2608.10393"],
        "why_it_matters": (
            "Reliability papers this week split failure into separate operational families: calibrated intervention, visual-shift early warning, future-representation test-time training, "
            "token-level hallucination detection, cost-aware open-set routing, epistemic restraint, and unrestricted robotic attacks. "
            "A single confidence number is not enough when the useful signal may be a veto, abstention, router handoff, or attack trigger."
        ),
        "confidence": "Medium-High — the tasks differ, but the shared decision is when a runtime guard should stop, route, repair, or refuse an action.",
        "lab_action": (
            "Create failure-family splits for visual shift, ambiguous evidence, typographic or diffusion attack, and costly open-set queries; "
            "compare intervention threshold, abstention expression, route choice, false alarm, and unsafe-action prevention under the same episode labels."
        ),
    },
    {
        "cluster": "Deployment budgets force selective correction rather than blanket scaling",
        "ids": ["2608.07088", "2608.10824", "2608.12127", "2608.12132", "2608.12171", "2608.07361"],
        "why_it_matters": (
            "Efficiency appears throughout the week as a constraint on evidence, not just latency. Token pruning, introspection-gated cache reuse, router calibration, "
            "sparse video diffusion, compression, and planning-token probing all ask which signal can be removed without deleting the evidence needed for a safe action. "
            "This reframes efficiency as a preservation contract for task-relevant cues."
        ),
        "confidence": "Medium — efficiency signals are broad, but multiple papers connect budget decisions to retained visual, planning, routing, or generation evidence.",
        "lab_action": (
            "For each compression or routing policy, ablate retained region tokens, cache reuse, router choice, and planning-token depth; "
            "measure latency, memory, grounding error, failure-warning lead time, and downstream action delta rather than speed alone."
        ),
    },
]


TOP_PAPERS = [
    ("ContactGuard", "2608.13438", "pre-contact latent futures make action veto timing measurable before physical failure"),
    ("AtlasVLA", "2608.06729", "persistent world-ego state turns VLA memory into an inspectable execution variable"),
    ("Surgical WAM", "2608.11204", "world-action modeling enters a high-stakes robot domain where data efficiency and failure state matter"),
    ("H2R-Bench", "2608.13049", "synthetic manipulation video is judged by human-to-robot contact and embodiment transfer, not video realism alone"),
    ("LocusGS", "2608.12825", "feed-forward 3DGS gains spatially grounded tokens that can become robot-usable map evidence"),
]


AUTOPSY_IDS = ["2608.06729", "2608.07596", "2608.11204", "2608.13438", "2608.13049", "2608.12825"]


FRONTIER_MEMORY = {
    "new": [
        "Pre-contact execution monitoring and VLA progress decoding became explicit daily signals on August 14.",
        "Human-to-robot manipulation generation moved from visual realism to contact and embodiment transfer metrics.",
    ],
    "strengthening": [
        "The August 10-14 sequence repeatedly strengthened an execution-evidence thesis: memory state, physical world state, causal failure state, active evidence, and abstention all precede the action.",
        "Robot-usable geometry strengthened through navigation-conditioned 3D state, active affordance views, semantic maps, Gaussian tokens, SLAM memory, and submap loop closure.",
    ],
    "commoditizing": [
        "Generic VLA scaling, generic world-model video quality, and generic token compression look less defensible unless they preserve a measurable action-relevant evidence field.",
    ],
    "contradiction": [
        "Direct low-latency execution pulls toward fewer modules, while monitors, routers, and repair loops add diagnostic depth; the useful boundary must be measured per failure family.",
    ],
    "missing_axis": [
        "The week still lacks one common closed-loop protocol that evaluates VLA memory, world-state quality, map uncertainty, contact transfer, and abstention/routing in the same episodes.",
    ],
}


STRATEGY_BOARD = [
    {
        "opportunity": "Pre-Commit VLA Evidence Protocol",
        "portfolio": "Build moat",
        "why_now": "The week produced repeated signals that useful VLA evidence appears before contact, completion, or final success.",
        "contrarian_bet": "APRL should own the failure-evidence protocol rather than compete first on another policy backbone.",
        "scores": {"strategic_fit": 5, "asymmetry": 5, "timing": 5, "tractability": 4, "defensibility": 5, "scientific_depth": 5},
        "one_week_probe": "Instrument two manipulation tasks with persistent state, progress probe, latent future, abstention, and repair-decision traces.",
        "four_week_build": "Compare memory VLA, routed action decoder, structured-demonstration VLA, pre-contact monitor, and task-progress probe under identical failure labels.",
        "success_metric": "At least one evidence field predicts terminal failure two action chunks earlier with AUC >= 0.75 while keeping false vetoes below a declared threshold.",
        "stop_condition": "If the fields do not beat previous-action error and task ID baselines, split the benchmark into contact-only and route-only failure families.",
        "paper_path": "Execution evidence contracts for reliable VLA control.",
        "asset_path": "Annotated APRL VLA rollout set with evidence traces, veto decisions, and recovery outcomes.",
    },
    {
        "opportunity": "Action-Sensitive Synthetic Manipulation Data Engine",
        "portfolio": "Exploit",
        "why_now": "The week made contact, force, embodiment, and action-conditioned futures the meaningful tests for synthetic or retargeted data.",
        "contrarian_bet": "Select data by how it changes the learned action boundary, not by how realistic the clip looks.",
        "scores": {"strategic_fit": 5, "asymmetry": 4, "timing": 5, "tractability": 4, "defensibility": 5, "scientific_depth": 4},
        "one_week_probe": "Choose one handover and one dexterous task, then label contact time, force plausibility, embodiment mismatch, and failure-correction target.",
        "four_week_build": "Train equal-budget policies from random demos, contact-consistent retargets, generated RGB-D clips, and failure-correction examples.",
        "success_metric": "OOD success improves by at least 10 points only when contact and embodiment-transfer metrics also improve.",
        "stop_condition": "If video realism improves without contact timing or policy improvement, stop using the generator as a data source.",
        "paper_path": "Action-sensitive data selection for contact-rich robot imitation.",
        "asset_path": "Retargeted and generated manipulation clips with contact, force, embodiment, and policy-delta labels.",
    },
    {
        "opportunity": "Robot-Usable Geometry and Active Evidence Harness",
        "portfolio": "Build moat",
        "why_now": "3D, SLAM, active navigation, and semantic-field papers all reframed maps as evidence states that must justify an action.",
        "contrarian_bet": "APRL can avoid rendering-fidelity competition by owning task-grounded map validity and active-view value.",
        "scores": {"strategic_fit": 5, "asymmetry": 5, "timing": 4, "tractability": 4, "defensibility": 5, "scientific_depth": 5},
        "one_week_probe": "Build two scenes where an active view, semantic map update, Gaussian token, or submap correction changes route or grasp choice.",
        "four_week_build": "Compare semantic map, Gaussian token, neural submap, and radiance-field simulator evidence under the same route and tabletop recovery tasks.",
        "success_metric": "The evidence state explains at least three failure families and improves recovery or relocalization over a visual-only baseline.",
        "stop_condition": "If the geometry fields only improve image metrics and not route or grasp decisions, narrow to localization-only claims.",
        "paper_path": "Robot-usable geometry as an action evidence state.",
        "asset_path": "APRL active-evidence scenes with map uncertainty, view value, route decision, and manipulation outcome labels.",
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
<div>Source: arXiv cs.CV/pastweek + cs.RO/pastweek - source_listing_date={SOURCE_LISTING_DATE} - source_mode=pastweek</div>
<div>Window: {WEEK_START} to {WEEK_END} - daily artifacts: {", ".join(DAILY_DATES)}</div>
<div>Pastweek parser: {totals['total_scanned']} dedup scanned - {totals['selected']} ROI selected</div>
<div>Weekday daily parser totals: cs.CV {daily['cv']} + cs.RO {daily['ro']} - {daily['total_scanned']} scanned - {daily['selected']} ROI selected</div>
</div>
<section class="thesis"><strong>Weekly conclusion:</strong> {esc(payload['weekly_thesis'])}</section>

<h2>주간 클러스터 표</h2>
<table class="cluster-table"><thead><tr><th>Cluster</th><th>Representative papers</th><th>Why it matters</th><th>Confidence</th><th>Lab action</th></tr></thead><tbody>{''.join(cluster_rows)}</tbody></table>
<p class="note">This week's core is not a bigger VLA or prettier world model; it is whether action, data, geometry, and reliability evidence can justify or block execution before failure becomes irreversible.</p>

<h2>주간 동향</h2>
<p>August 10-14 forms one coherent arc. Monday exposed state accountability through persistent VLA memory, physical world-state grounding, intervention calibration, and action-budget geometry. Tuesday and Wednesday moved that evidence into action decoders, geometry-aware world-action models, failure-aware causal training, navigation risk, and active evidence consolidation. Thursday and Friday then made the same evidence operational: structured demonstrations, early OpenVLA warnings, safety guards, pre-contact monitors, task-progress probes, H2R manipulation generation, active affordance grounding, and VLM restraint.</p>
<p>The useful weekly signal is a research-decision shift. The leading papers do not merely ask whether a model is accurate; they ask which intermediate state should be trusted, when it should be rejected, and what intervention it licenses. This is why VLA, world models, synthetic data, geometry, navigation, and reliability belong in one weekly synthesis rather than six separate buckets.</p>

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
