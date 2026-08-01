#!/usr/bin/env python3
"""Generate the 2026-W31 weekly briefing from parser and daily RI artifacts."""
from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-08-01"
WEEK = "2026-W31"
WEEK_START = "2026-07-26"
WEEK_END = DATE
SOURCE_LISTING_DATE = "2026-07-31"
DAILY_DATES = ["2026-07-27", "2026-07-28", "2026-07-29", "2026-07-30", "2026-07-31"]
SITE_URL = "https://gisbi-kim.github.io/arxiv-daily-summary"

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
    context = {
        "trends": {},
        "insights": {},
        "intelligence": {},
        "papers": {},
        "autopsies": {},
    }
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
                if arxiv_id:
                    row = dict(paper)
                    row["arxiv_id"] = arxiv_id
                    context["papers"].setdefault(arxiv_id, row)
        for paper in intelligence.get("papers", []):
            arxiv_id = paper.get("arxiv_id")
            if arxiv_id:
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
    if len(short) > 86:
        short = short[:83].rstrip() + "..."
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
    "이번 주의 핵심은 VLA, robot data, world model, geometry, VLM reliability가 따로 움직인 것이 아니라 "
    "모두 '행동을 믿기 전에 어떤 중간 evidence state를 노출하고 검증할 것인가'로 수렴했다는 점입니다. "
    "월요일의 robot-rendered state와 gradient-free guidance는 화요일의 depth/tactile state, 수요일의 causal modality evidence, "
    "목요일의 real-time execution plus repair, 금요일의 counterfactual action drift와 ambient state capture로 이어졌습니다. "
    "APRL 관점에서 이번 주의 승부처는 더 큰 backbone이 아니라 action-sensitive data, robot-usable geometry, runtime repair, "
    "evidence-routed VLM을 같은 closed-loop failure protocol 안에서 비교할 수 있는 자산을 먼저 소유하는 것입니다."
)

CLUSTERS = [
    {
        "cluster": "VLA가 action decoder 경쟁에서 evidence-bearing execution contract로 이동",
        "ids": ["2607.22535", "2607.24159", "2607.25487", "2607.27205", "2607.26789"],
        "why_it_matters": (
            "기존 VLA 비교는 같은 task success를 놓고 backbone, action head, data 규모를 겨루는 방식이 많았습니다. "
            "이번 주 논문들은 action을 바로 신뢰하지 않고 rendered robot state, physical guidance, Plan/Think span, "
            "direct local latency, action-conditioned verifier를 중간 evidence로 세웁니다. "
            "따라서 VLA 평가는 최종 성공률보다 어떤 evidence가 실패 직전에 먼저 무너지는지를 드러내야 합니다."
        ),
        "confidence": "High — 5일 연속 VLA/action 논문이 서로 다른 구현으로 같은 execution-evidence 축을 반복했습니다.",
        "lab_action": (
            "LIBERO/RoboCasa와 실제 tabletop trace에서 direct VLA, physical-guided VLA, reasoning-distilled VLA, "
            "action-conditioned verifier를 같은 task family에 배치하고 latency, physical-state prediction, intervention timing, "
            "repair outcome이 failure-prediction lead time과 task success를 얼마나 바꾸는지 비교합니다."
        ),
    },
    {
        "cluster": "Robot data scaling이 demo volume에서 action-sensitive counterfactual coverage로 이동",
        "ids": ["2607.24744", "2607.25895", "2607.27261", "2607.27782", "2607.28625"],
        "why_it_matters": (
            "이번 주 data 논문들은 demonstration을 더 모으는 문제보다 어떤 example이 action boundary를 실제로 바꾸는지 묻습니다. "
            "Data Pyramid와 HiFi-UMI는 source fidelity와 pose/synchronization을 분리하고, Counterfactual Action Sensitivity Coverage와 RedFlow는 "
            "nuisance-induced action drift와 failure-to-correction target을 데이터 선택 기준으로 만듭니다. "
            "ACE-Data-0는 ambient interaction을 synchronized state engine으로 제시해, 데이터의 가치를 volume이 아니라 action information으로 재정의합니다."
        ),
        "confidence": "High — source fidelity, action drift, failure correction, ambient capture가 같은 data-selection decision으로 연결됩니다.",
        "lab_action": (
            "동일 imitation policy에서 random demo, fidelity-filtered demo, action-drift example, failure-correction example을 같은 budget으로 비교하고 "
            "OOD success, failure-family coverage, collection cost, corrective transfer가 어떤 data family에서 개선되는지 평가합니다."
        ),
    },
    {
        "cluster": "World-action models가 plausible future에서 physically grounded planning interface로 이동",
        "ids": ["2607.26056", "2607.26452", "2607.26712", "2607.28243", "2607.28391", "2607.27924"],
        "why_it_matters": (
            "World model은 더 그럴듯한 future frame을 만드는 것만으로 robot policy에 충분하지 않습니다. "
            "INTACT, CG-World, ActSWM은 action-sensitive state, branch lineage, distinguishable futures를 planning interface로 만들고, "
            "EgoGenesis와 TacWAM은 anchored 3D memory와 tactile mechanics를 future prediction에 주입합니다. "
            "즉 world model의 평가는 video quality가 아니라 action choice를 바꾸는 physical channel을 보존하는지로 옮겨야 합니다."
        ),
        "confidence": "High — action law, typed state, branch lineage, 3D memory, tactile mechanics가 주간 corpus에서 반복되었습니다.",
        "lab_action": (
            "visual-only, anchored-3D, tactile, pose-image, physical-time channel을 같은 world-action task에 놓고 "
            "candidate rollout 수, planning success, contact failure, recovery behavior, latency trade-off를 분리해 검증합니다."
        ),
    },
    {
        "cluster": "Geometry and SLAM이 visual fidelity에서 action-usable map state와 uncertainty tags로 이동",
        "ids": ["2607.21986", "2607.23384", "2607.24852", "2607.26889", "2607.27749", "2607.28045"],
        "why_it_matters": (
            "이번 주 3D/Scene 신호는 rendering quality만의 문제가 아니었습니다. "
            "Mag4D-SLAM, Semantic Object SLAM, leakage-aware photogrammetry, StructureGS, articulated reconstruction, radar odometry는 "
            "map field가 어떤 sensor source, uncertainty, association stability, action use를 갖는지 묻습니다. "
            "로봇에게 필요한 geometry는 예쁜 view가 아니라 sensor dropout, repeated objects, dynamic objects 아래에서도 route recovery나 manipulation pose를 지탱하는 state입니다."
        ),
        "confidence": "High — pastweek 3D/Scene ROI가 크고, localization, odometry, semantic association, articulated prior가 독립적으로 반복되었습니다.",
        "lab_action": (
            "동일 route와 tabletop scene에서 visual-inertial SLAM, semantic-object map, Gaussian/object map, radar odometry를 비교하고 "
            "association flips, relocalization time, uncertainty calibration, downstream navigation or manipulation success를 함께 평가합니다."
        ),
    },
    {
        "cluster": "VLM reliability가 answer confidence에서 evidence routing and failure-family diagnosis로 이동",
        "ids": ["2607.22864", "2607.24957", "2607.27667", "2607.27700", "2607.27830", "2607.28463"],
        "why_it_matters": (
            "Foundation-model reliability 논문들은 정답 여부나 confidence 하나로는 robot VLM failure를 설명하지 못한다고 봅니다. "
            "Spatial-IQ와 PerceptionBench는 perception을 atomic test로 쪼개고, Witness, token calibration, VisualRouter, FaithEyes는 "
            "어떤 evidence가 retrieval, compression, verifier, routing을 지나 행동 판단까지 살아남는지 묻습니다. "
            "따라서 robot VLM 평가는 right-answer-wrong-evidence를 별도 failure family로 다뤄야 합니다."
        ),
        "confidence": "High — spatial, atomic perception, token, routing, verifier evidence가 서로 다른 task에서 같은 reliability decision을 만듭니다.",
        "lab_action": (
            "하나의 robot VLM benchmark에 spatial relation, kept tokens, routed frames, verifier correction, final action을 결합한 조건을 만들고 "
            "정답-근거 불일치, wrong grounding, unsafe action을 failure family별로 비교합니다."
        ),
    },
    {
        "cluster": "Safety and autonomy가 route success에서 risk horizon and runtime repair constraints로 이동",
        "ids": ["2607.22494", "2607.23565", "2607.25049", "2607.26789", "2607.28474", "2607.28623"],
        "why_it_matters": (
            "Autonomy와 safety는 이번 주에 final route success나 nominal grasp score에서 벗어났습니다. "
            "CARA와 risk-guided flight는 위험이 언제 보이기 시작하는지 묻고, FIRMGrasp는 adverse-tail friction을 안전 margin에 넣으며, "
            "CheckVLA와 surgical/agri failure detectors는 execution 중 repair timing과 alarm condition을 policy module로 만듭니다. "
            "평균 성능보다 중요한 것은 어떤 risk evidence가 intervention을 정당화하는지입니다."
        ),
        "confidence": "Medium-High — driving, flight, grasping, mobile manipulation, surgery, agriculture가 risk-horizon decision을 공유합니다.",
        "lab_action": (
            "navigation과 manipulation episode에서 nominal score, risk horizon, adverse-tail variable, predicted consequence, intervention timing을 바꿔가며 "
            "near miss, unsafe contact, false alarm, recovery latency, terminal success를 비교합니다."
        ),
    },
]

TOP_PAPERS = [
    ("TurboVLA", "2607.27205", "real-time VLA가 LLM-centric interface 없이 control-loop latency를 직접 건드린 주간 전환점"),
    ("It's Not Just More Demos", "2607.27261", "demo volume 대신 counterfactual action drift를 데이터 가치로 삼은 금요일 핵심 논문"),
    ("DeVA", "2607.24159", "video-action policy 안에 depth/affordance physical guidance를 노출한 화요일의 대표 신호"),
    ("CheckVLA", "2607.26789", "action-conditioned world model과 conformal risk trigger로 runtime repair를 policy module로 만든 논문"),
    ("EgoGenesis", "2607.28243", "egocentric world-action generation을 anchored 3D memory와 action geometry 문제로 재정의한 논문"),
]

AUTOPSY_IDS = ["2607.27205", "2607.27261", "2607.24159", "2607.26789", "2607.28243"]

FRONTIER_MEMORY = {
    "new": [
        "Counterfactual action drift and failure-to-correction targets became explicit data-selection mechanisms on July 31.",
        "Ambient capture moved embodied data from video archive to synchronized state engine.",
    ],
    "strengthening": [
        "The July action-state contract thread strengthened every day from robot rendering to tactile state, causal modality evidence, real-time execution, and runtime repair.",
        "Robot-usable geometry appeared repeatedly as localization, semantic association, articulated prior, radar odometry, and action-conditioned map state.",
    ],
    "commoditizing": [
        "Generic VLA scale and generic video/world-model quality are less defensible unless they expose an intervention-ready evidence field.",
    ],
    "contradiction": [
        "Fast direct VLA execution reduces latency, while verifier and repair modules add diagnostic depth; the useful boundary is task-dependent and needs controlled measurement.",
    ],
    "missing_axis": [
        "The corpus still lacks a shared multi-sensor closed-loop benchmark that evaluates action evidence, geometry evidence, and VLM evidence in the same episodes.",
    ],
}

STRATEGY_BOARD = [
    {
        "opportunity": "Evidence-Bearing VLA Execution Ledger",
        "portfolio": "Build moat",
        "why_now": "Five consecutive daily batches made action validity depend on exposed intermediate evidence rather than final success alone.",
        "contrarian_bet": "APRL should own the failure-evidence protocol before competing on another VLA backbone.",
        "scores": {"strategic_fit": 5, "asymmetry": 5, "timing": 5, "tractability": 4, "defensibility": 5, "scientific_depth": 5},
        "one_week_probe": "Instrument two manipulation tasks with action chunk, physical-state prediction, causal modality delta, verifier risk, and repair decision.",
        "four_week_build": "Compare TurboVLA-style direct execution, DeVA-style physical guidance, IDR-style modality diagnosis, and CheckVLA-style repair under one failure-labeled protocol.",
        "success_metric": "At least one evidence field predicts terminal failure two steps earlier than success history with AUC >= 0.75 or improves recovery by 10 points.",
        "stop_condition": "If evidence fields do not outperform task ID and previous action error, narrow to one failure family before scaling.",
        "paper_path": "Execution-evidence contracts for reliable VLA control.",
        "asset_path": "Reusable APRL VLA failure-evidence protocol and annotated rollout set.",
    },
    {
        "opportunity": "Counterfactual Action-Sensitivity Data Engine",
        "portfolio": "Exploit",
        "why_now": "July 31 made action drift a concrete selection criterion, while earlier days showed typed data-source and fidelity constraints.",
        "contrarian_bet": "Instead of collecting broader demos, select examples that move the trained policy's action boundary.",
        "scores": {"strategic_fit": 5, "asymmetry": 4, "timing": 5, "tractability": 4, "defensibility": 5, "scientific_depth": 4},
        "one_week_probe": "Generate nuisance pairs for lighting, distractor, support, object pose, and moving-object state on one imitation policy.",
        "four_week_build": "Compare random demos, fidelity-filtered demos, action-drift examples, and failure-correction examples under the same data budget.",
        "success_metric": "OOD success improves by at least 10 points at equal budget, with selected examples explaining a specific failure family.",
        "stop_condition": "If action-drift examples do not beat random additions on two nuisance families, switch to real perturbation collection.",
        "paper_path": "Data-efficient imitation repair through action-sensitive counterfactual coverage.",
        "asset_path": "Counterfactual data-selection harness plus failure-correction library.",
    },
    {
        "opportunity": "Robot-Usable Geometry and World-State Protocol",
        "portfolio": "Build moat",
        "why_now": "3D/Scene and world-action papers repeatedly moved from visual quality to sensor source, uncertainty, contact, and action use.",
        "contrarian_bet": "APRL can avoid photorealism competition by owning task-grounded geometry validity.",
        "scores": {"strategic_fit": 5, "asymmetry": 5, "timing": 4, "tractability": 4, "defensibility": 5, "scientific_depth": 5},
        "one_week_probe": "Build a small route plus tabletop card with map source, uncertainty, action use, and expected failure mode for each geometry field.",
        "four_week_build": "Compare visual-inertial SLAM, semantic-object maps, Gaussian/object maps, anchored 3D world models, and tactile world models on downstream recovery.",
        "success_metric": "Geometry/world-state fields explain at least three distinct failure families and improve navigation or manipulation recovery over visual-only state.",
        "stop_condition": "If fields only correlate with visual quality and not recovery, split the work into localization-only and contact-only protocols.",
        "paper_path": "Robot-usable geometry state as an execution contract.",
        "asset_path": "APRL map/world-state validity suite.",
    },
]


def daily_totals(context: dict) -> dict:
    totals = {"cv": 0, "ro": 0, "selected": 0, "total_scanned": 0}
    for date in DAILY_DATES:
        trend = context["trends"][date]
        counts = trend.get("daily_new_counts", {})
        t = trend.get("totals", {})
        totals["cv"] += int(counts.get("cv", 0))
        totals["ro"] += int(counts.get("ro", 0))
        totals["selected"] += int(t.get("selected", 0))
        totals["total_scanned"] += int(t.get("total_scanned", 0))
    return totals


def paper_link(paper: dict) -> str:
    badge = f" <span class='badge'>{esc(paper.get('badge'))}</span>" if paper.get("badge") else ""
    tags = " ".join(f"<span class='tag'>{esc(tag)}</span>" for tag in paper.get("importance_tags", [])[:2])
    phy = paper.get("phylogeny", {})
    phy_parts = [phy.get("source"), phy.get("phylum"), phy.get("class"), phy.get("order"), phy.get("genus")]
    phy_text = " > ".join(str(x) for x in phy_parts if x)
    return (
        f'<a href="{esc(paper["arxiv"])}" target="_blank" rel="noopener">{esc(paper["short"])}</a>{badge}<br>'
        f'<span class="phy">Phylogeny: {esc(phy_text)}</span><br>{tags}'
    )


def autopsy_card(raw: dict, display_paper: dict) -> dict:
    evidence = raw.get("evidence", [])[:3]
    return {
        "arxiv_id": display_paper["arxiv_id"],
        "title": display_paper["title"],
        "status": raw.get("status", "reading depth from daily artifact"),
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
        f"<p><strong>{esc(item['portfolio'])}</strong> — {esc(item['why_now'])}</p>"
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
    autopsy_items = "".join(
        "<article>"
        f'<h3><a href="https://arxiv.org/abs/{esc(card["arxiv_id"])}" target="_blank" rel="noopener">{esc(card["title"])}</a></h3>'
        f"<p><b>Reading depth:</b> {esc(card['status'])}</p>"
        f"<p><b>Status quo belief:</b> {esc(card['status_quo_belief'])}</p>"
        f"<p><b>Conceptual move:</b> {esc(card['conceptual_move'])}</p>"
        f"<p><b>Mechanism:</b> {esc(card['mechanism'])}</p>"
        f"<p><b>Decisive evidence:</b> {esc('; '.join(f'{e.get('trace', '')}: {e.get('claim', '')}' for e in card['decisive_evidence']))}</p>"
        f"<p><b>Falsification frontier:</b> {esc(card['falsification_frontier'])}</p>"
        f"<p><b>Adversarial read:</b> {esc(card['adversarial_read'])}</p>"
        f"<p><b>Transferable thinking tool:</b> {esc(card['transferable_thinking_tool'])}</p>"
        "</article>"
        for card in payload["paper_autopsies"]
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
<h1>arXiv Weekly Briefing — {WEEK}</h1>
<div class="meta">
<div>소스: arXiv cs.CV/pastweek + cs.RO/pastweek · source_listing_date={SOURCE_LISTING_DATE} · source_mode=pastweek</div>
<div>주간 시야: {WEEK_START} ~ {WEEK_END} · daily artifacts: {", ".join(DAILY_DATES)}</div>
<div>pastweek parser: {totals['total_scanned']} dedup scanned · {totals['selected']} ROI selected</div>
<div>weekday daily parser totals: cs.CV {daily['cv']} + cs.RO {daily['ro']} · {daily['total_scanned']} scanned · {daily['selected']} ROI selected</div>
</div>
<section class="thesis"><strong>이번 주의 결론:</strong> {esc(payload['weekly_thesis'])}</section>

<h2>주간 클러스터 표</h2>
<table class="cluster-table"><thead><tr><th>Cluster</th><th>대표 논문</th><th>왜 중요?</th><th>Confidence</th><th>Lab action</th></tr></thead><tbody>{''.join(cluster_rows)}</tbody></table>
<p class="note">이번 주의 핵심은 더 큰 VLA나 더 예쁜 world model이 아니라, action, data, geometry, evidence route가 실제 failure와 recovery를 얼마나 먼저 드러내는지 검증하는 것입니다.</p>

<h2>주간 동향</h2>
<p>월요일부터 금요일까지 같은 decision이 다른 구현으로 반복되었습니다. 월요일에는 action을 rendered robot state로 분리했고, 화요일에는 physical and tactile state를 action chunk 앞에 세웠으며, 수요일에는 causal modality와 3D object prior를 드러냈습니다. 목요일에는 real-time direct VLA와 runtime verifier가 같은 실행 문제를 양쪽에서 압박했고, 금요일에는 counterfactual action sensitivity가 data selection의 기준으로 들어왔습니다.</p>
<p>Geometry와 VLM reliability도 같은 축으로 읽어야 합니다. 이번 주 3D/SLAM 흐름은 map이 얼마나 보기 좋은지가 아니라 source, uncertainty, association, articulated prior가 downstream action을 버티는지로 이동했습니다. VLM reliability는 confidence 대신 evidence portfolio, kept token, routed frame, verifier correction이 action error와 어떻게 연결되는지 묻는 방향으로 이동했습니다.</p>

<h2>주간 Top 5</h2>
<ol class="top5">{top_items}</ol>

<h2>주간 논문 사고 해부</h2>
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
