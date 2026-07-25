#!/usr/bin/env python3
"""Generate the 2026-W30 weekly briefing from current /pastweek parser output."""
from __future__ import annotations

import datetime as dt
import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from classify import BUCKETS, assign_bucket, primary_badge
from daily_backfill_lib import phylogeny_for


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-07-25"
ISO_WEEK = "2026-W30"
WEEK_START = "2026-07-19"
WEEK_END = DATE
SOURCE_LISTING_DATE = "2026-07-24"
DAILY_DATES = ["2026-07-20", "2026-07-21", "2026-07-22", "2026-07-23", "2026-07-24"]
BUCKET_ORDER = [b for b, _ in BUCKETS]


WEEKLY_THESIS = (
    "2026-W30의 핵심은 VLA, world model, manipulation data, geometry/SLAM, MLLM reliability가 모두 더 큰 모델보다 "
    "실행 가능한 state contract와 failure-evidence contract를 소유하는 방향으로 수렴했다는 점입니다. "
    "월요일과 화요일의 VLA/action interface 흐름은 목요일의 KineBench/PerceptDrive, 금요일의 HyWorldVLA/MoE VLA로 이어졌고, "
    "EgoRecovery, FORGE-plus, AXIS, Scale Up Strategically는 data scaling을 success demo volume이 아니라 failure, bias, force, growth protocol로 재정의했습니다. "
    "GLAM-SLAM, DINS-IO, HGeo-TopoMap, Geo3R은 geometry를 rendering or answer support가 아니라 robot task가 소비하는 verified state로 끌어올렸습니다."
)

CLUSTERS = [
    {
        "cluster": "VLA가 action head 경쟁에서 world-state and execution-interface contract로 이동",
        "ids": ["2607.20988", "2607.20175", "2607.19876", "2607.20771", "2607.14635", "2607.14739", "2607.21582"],
        "why": (
            "이번 주 VLA 흐름은 action decoder를 더 키우는 경쟁이 아니라 action이 소비하는 state와 interface를 어떻게 검증할지로 이동했습니다. "
            "KineBench와 PerceptDrive는 generated/world-action output을 kinematic grounding and trajectory metric으로 판정하고, HyWorldVLA는 pixel and latent world modeling을 분리합니다. "
            "MoE VLA와 Action QFormer류는 action-facing representation and expert routing이 실제 skill phase와 instruction alignment를 바꾸는지 묻습니다."
        ),
        "confidence": "High — week 내 독립 저자군이 world model, action interface, expert routing, bias-aware evaluation을 반복",
        "lab_action": (
            "LIBERO/RoboCasa/NAVSIM mini-suite에서 action head, world-state latent, expert routing, representation anchoring을 factorial split으로 두고 "
            "execution success, semantic retention, trajectory robustness, failure-warning lead time을 비교한다."
        ),
    },
    {
        "cluster": "Robot data scaling이 fixed dataset release에서 bias-aware growable engine으로 이동",
        "ids": ["2607.21588", "2607.21582", "2607.21017", "2607.21071", "2607.19745", "2607.19633"],
        "why": (
            "데이터를 많이 모은다는 말은 이번 주에 더 구체적인 계약으로 바뀌었습니다. AXIS는 task generation, web teleoperation, refinement, augmentation, validation을 growable snapshot으로 묶고, "
            "Scale Up Strategically는 factor dominance를 먼저 측정한 뒤 collection을 설계합니다. EgoRecovery와 LENS는 failure state and planning abstraction이 data economy의 핵심임을 보여줍니다."
        ),
        "confidence": "High — AXIS/Scale Up/EgoRecovery 계열이 static dataset보다 growth, bias, failure data를 강조",
        "lab_action": (
            "same tabletop family에서 random collection, factor-targeted collection, human recovery collection, AXIS-style snapshot growth를 비교하고 "
            "OOD success, factor dominance, valid segments per hour, second-attempt recovery를 평가한다."
        ),
    },
    {
        "cluster": "Geometry 연구가 visual fidelity에서 robot-usable map and topology state로 이동",
        "ids": ["2607.21416", "2607.21281", "2607.20232", "2607.21023", "2607.21138", "2607.21595", "2607.21438"],
        "why": (
            "3D/Scene은 주간 46편이지만 숫자보다 중요한 것은 map/state contract입니다. GLAM-SLAM은 ORB-SLAM2 front-end와 Gaussian mapper를 decoupled real-time map으로 묶고, "
            "HGeo-TopoMap은 BEV topology에 hierarchical geometric priors를 넣습니다. DINS-IO, WAT3R, DTIF, 3D-aware VLMs, UAV depth까지 더하면 geometry는 rendering score가 아니라 localization, relation, topology, navigation success의 substrate입니다."
        ),
        "confidence": "High — SLAM, odometry, topology, depth, spatial VLM signals가 한 주에 반복",
        "lab_action": (
            "same indoor/outdoor route traces에서 sparse SLAM, Gaussian map, inertial odometry, BEV topology, geometric VLM card를 비교하고 "
            "metric drift, relocalization success, topology error, spatial relation error, downstream route recovery를 측정한다."
        ),
    },
    {
        "cluster": "Contact-rich manipulation이 success demo에서 force, recovery, and tactile failure boundary로 이동",
        "ids": ["2607.21227", "2607.19745", "2607.20912", "2607.20683", "2607.21341", "2607.14236", "2607.14578"],
        "why": (
            "contact-rich manipulation은 성공 demo를 더 모으는 것만으로는 fragile failure를 설명하지 못합니다. FORGE-plus는 LLM을 force budget setter로 제한하고, "
            "EgoRecovery는 human recovery segment를 corrective intent로 바꾸며, URF/FELT/bimanual diffusion papers는 force, tactile, composition boundary를 별도 state로 봅니다. "
            "지난 주 force/tactile 신호와 합치면 contact 평가의 중심은 peak success가 아니라 breakage, recovery, tactile ambiguity입니다."
        ),
        "confidence": "Medium-High — 일부 force/tactile 대표는 지난 W29 daily에서 이어진 strengthening signal이지만 recovery/contact boundary가 명확히 반복",
        "lab_action": (
            "assembly and tabletop tasks에서 visual-only policy, force-budget wrapper, tactile-signal wrapper, human-recovery data를 비교하고 "
            "peak force violation, breakage, recovery latency, tactile ambiguity failure, final success를 함께 평가한다."
        ),
    },
    {
        "cluster": "MLLM and robot-agent reliability가 final answer에서 evidence trajectory diagnosis로 이동",
        "ids": ["2607.21085", "2607.21105", "2607.19793", "2607.21155", "2607.20868", "2607.21401", "2607.20357"],
        "why": (
            "이번 주 Foundation Models 51편의 핵심은 answer accuracy가 아니라 evidence가 맞았는지입니다. Geo3R은 geometry cards로 spatial relation hallucination을 줄이고, "
            "HalluScope는 hallucinated span and type을 fine-grained diagnosis로 바꿉니다. Silent Failures, CRAG-MM-Diagnostics, ViSTR-Bench, ResponseGuard는 retrieval path, stage-wise VQA, dynamic visual cues, guardrail latency를 같은 diagnostic surface로 만듭니다."
        ),
        "confidence": "High — spatial, span, retrieval, dynamic-cue, guardrail diagnostics가 서로 다른 tasks에서 반복",
        "lab_action": (
            "robot VLM episodes에 geometry card, retrieval/evidence path, visual-cue timeline, span-level hallucination label을 붙이고 "
            "phantom grounding, stale state, wrong spatial relation, unsafe guardrail miss를 failure family별로 평가한다."
        ),
    },
    {
        "cluster": "Autonomy benchmark가 route success에서 body, capability, conflict, and safety constraints로 이동",
        "ids": ["2607.21400", "2607.19695", "2607.19880", "2607.21025", "2607.20679", "2607.20772", "2607.20665"],
        "why": (
            "navigation/autonomy는 성공률 한 줄로 충분하지 않습니다. NavVerse와 VoLN은 continuous execution and visual-goal input contract를 강조하고, "
            "EA-Nav는 embodiment geometry를 safety condition으로 넣습니다. ZONDA, capability-aware traversability, socially consistent multi-robot navigation, CBF payload transport까지 포함하면 constraint violation, false stop, recovery margin을 함께 봐야 합니다."
        ),
        "confidence": "High — embodied navigation and safety-control papers가 input contract와 constraint metrics를 공유",
        "lab_action": (
            "indoor-to-outdoor, UAV, sidewalk, multi-robot scenes에서 visual-goal policy, embodiment-aware policy, capability-aware planner, CBF safety wrapper를 비교하고 "
            "clearance violation, collision margin, false stop, human intervention, recovery latency를 평가한다."
        ),
    },
]

TOP_PAPERS = [
    ("HyWorldVLA", "2607.20988", "hybrid pixel/latent world model로 driving VLA의 state contract를 직접 제시"),
    ("Scale Up Strategically", "2607.21582", "factor dominance를 data collection target으로 바꾼 manipulation scaling paper"),
    ("GLAM-SLAM", "2607.21416", "Gaussian map을 ORB-SLAM2 tracking과 large-scale real-time mapping으로 연결"),
    ("AXIS", "2607.21588", "robot data를 growable community-driven benchmark snapshot engine으로 설계"),
    ("Geo3R", "2607.21085", "MLLM spatial hallucination을 explicit geometry card problem으로 전환"),
]

STRATEGY = [
    {
        "opportunity": "State Contract Evaluation Harness",
        "portfolio": "Build moat",
        "one_week_probe": "Select one manipulation and one navigation trace, define latent/world/geometry/evidence contract fields, and score existing policies under three perturbations.",
        "four_week_build": "Release a small reusable evaluation harness with state contract schema, failure family labels, and downstream execution metrics.",
        "success_metric": "state contract score predicts execution failure with AUC >=0.75 and isolates at least three actionable failure families.",
        "stop_condition": "If contract fields do not outperform task success history or visual score, narrow scope to geometry-only state estimation.",
        "paper_path": ["https://arxiv.org/abs/2607.20988", "https://arxiv.org/abs/2607.21416", "https://arxiv.org/abs/2607.21085"],
        "asset_path": ["APRL internal state-contract schema", "robot episode failure-family taxonomy"],
    },
    {
        "opportunity": "Bias-Aware Data Growth Protocol",
        "portfolio": "Exploit",
        "one_week_probe": "Run factor dominance tests for verb/object/color/material on three tabletop tasks before adding new demonstrations.",
        "four_week_build": "Build a small growable snapshot with targeted bias-breaking trajectories and controlled augmentation variants.",
        "success_metric": "OOD success improves by 15 percentage points over random collection and factor dominance magnitude drops by 30%.",
        "stop_condition": "If factor dominance fails to predict OOD errors, switch to recovery/force factor labels.",
        "paper_path": ["https://arxiv.org/abs/2607.21582", "https://arxiv.org/abs/2607.21588"],
        "asset_path": ["factor dominance test suite", "task snapshot validation script"],
    },
    {
        "opportunity": "Bounded Supervisor for Robot Safety",
        "portfolio": "Explore",
        "one_week_probe": "Prototype force-budget and geometry-card supervisors that expose only bounded choices to a policy.",
        "four_week_build": "Compare free-form planner, bounded force supervisor, and geometry-card supervisor on fragile assembly and wrong-goal navigation.",
        "success_metric": "breakage or collision drops by 40% while success drop remains below 10 percentage points.",
        "stop_condition": "If bounded supervision only delays failures, convert it into offline diagnostic labeling first.",
        "paper_path": ["https://arxiv.org/abs/2607.21227", "https://arxiv.org/abs/2607.21085", "https://arxiv.org/abs/2607.21400"],
        "asset_path": ["bounded-supervisor API", "force/geometry intervention logs"],
    },
]


def load_json(path: str) -> object:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def classify_pastweek() -> tuple[list[dict], dict]:
    cv = load_json("out/cv_pastweek.json")
    ro = load_json("out/ro_pastweek.json")
    by_id: dict[str, dict] = {}
    for paper in cv + ro:
        by_id.setdefault(paper["arxiv_id"], paper)
    papers: list[dict] = []
    buckets = {b: {"total": 0, "cv": 0, "ro": 0, "cvro": 0, "papers": []} for b in BUCKET_ORDER}
    for paper in by_id.values():
        bucket = assign_bucket(paper.get("title", ""), paper.get("abstract", ""), paper.get("subjects", ""))
        if not bucket:
            continue
        row = dict(paper)
        row["bucket"] = bucket
        row["badge"] = primary_badge(row)
        papers.append(row)
        buckets[bucket]["total"] += 1
        if row["badge"] == "CV":
            buckets[bucket]["cv"] += 1
        elif row["badge"] == "RO":
            buckets[bucket]["ro"] += 1
        elif row["badge"] == "CV/RO":
            buckets[bucket]["cvro"] += 1
        buckets[bucket]["papers"].append(row)
    return papers, buckets


def paper_ref(paper: dict) -> dict:
    phy = phylogeny_for(paper["bucket"], paper)
    return {
        "title": paper["title"],
        "arxiv": f"https://arxiv.org/abs/{paper['arxiv_id']}",
        "short": paper["title"].split(":")[0][:70],
        "badge": paper.get("badge", ""),
        "phylogeny": phy,
    }


def render_html(payload: dict) -> str:
    def esc(value: object) -> str:
        return html.escape(str(value or ""), quote=False)

    cluster_rows = []
    for cluster in payload["clusters"]:
        reps = "<br>".join(
            f'<a href="{esc(p["arxiv"])}">{esc(p["short"])}</a> <span class="badge">{esc(p["badge"])}</span>'
            for p in cluster["representative_papers"]
        )
        cluster_rows.append(
            "<tr>"
            f"<td><strong>{esc(cluster['cluster'])}</strong></td>"
            f"<td>{reps}</td>"
            f"<td>{esc(cluster['why_it_matters'])}</td>"
            f"<td>{esc(cluster['confidence'])}</td>"
            f"<td>{esc(cluster['lab_action'])}</td>"
            "</tr>"
        )
    top = "".join(
        f'<li><a href="https://arxiv.org/abs/{aid}"><strong>{esc(title)}</strong></a><span>{esc(why)}</span></li>'
        for title, aid, why in TOP_PAPERS
    )
    buckets = "".join(
        f"<div><span>{esc(name)}</span><b>{info['total']}</b><small>CV {info['cv']} / RO {info['ro']} / CVRO {info['cvro']}</small></div>"
        for name, info in payload["buckets"].items()
    )
    strategies = "".join(
        f"<article><h3>{esc(item['opportunity'])}</h3><p><strong>{esc(item['portfolio'])}</strong></p>"
        f"<p><b>1-week probe:</b> {esc(item['one_week_probe'])}</p><p><b>4-week build:</b> {esc(item['four_week_build'])}</p>"
        f"<p><b>Success metric:</b> {esc(item['success_metric'])}</p><p><b>Stop condition:</b> {esc(item['stop_condition'])}</p></article>"
        for item in STRATEGY
    )
    return f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>arXiv Weekly Briefing - {ISO_WEEK}</title>
<style>
body{{margin:0;background:#eef2f7;color:#202936;font:15px/1.72 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;padding:28px 12px}}
.wrap{{max-width:1060px;margin:0 auto;background:#fff;border-radius:12px;box-shadow:0 8px 28px #243b530f;padding:42px 52px}}
a{{color:#075bb5;text-decoration:none}}a:hover{{text-decoration:underline}}.home{{display:inline-block;margin-bottom:16px;color:#0969da}}
h1{{font-size:32px;margin:0 0 8px;color:#10233f;letter-spacing:-.03em}}h2{{font-size:23px;margin:42px 0 14px;border-bottom:2px solid #dbe4ef;padding-bottom:8px;color:#10233f}}
.meta{{background:#f8fafc;border-left:4px solid #0891b2;border-radius:8px;padding:14px 18px;color:#42566b;font-size:13px;margin:16px 0 22px}}
.thesis{{background:#10233f;color:#f8fafc;border-radius:12px;padding:19px 23px;font-size:16px}}.cluster-table{{width:100%;table-layout:fixed;border-collapse:collapse;font-size:13px;margin-top:12px}}
th,td{{border:1px solid #d7dde6;padding:9px;vertical-align:top;overflow-wrap:anywhere}}th{{background:#f1f5f9;color:#10233f}}.badge{{font-size:11px;background:#fff7ed;border:1px solid #fed7aa;color:#9a3412;border-radius:999px;padding:1px 6px;margin-left:4px}}
.bucket-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}}.bucket-grid div{{background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px;padding:10px}}.bucket-grid span{{display:block;font-size:12px;color:#64748b}}.bucket-grid b{{font-size:22px;color:#10233f}}.bucket-grid small{{display:block;color:#64748b}}
.top5 li{{margin:10px 0;padding:12px 14px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:8px}}.top5 span{{display:block;color:#475569;font-size:13px;margin-top:3px}}
.strategy-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}.strategy-grid article{{border:1px solid #d7dde6;border-radius:12px;padding:16px;background:#fbfdff}}.strategy-grid h3{{font-size:17px;margin:0 0 6px}}
.note{{padding:13px 16px;background:#fff8e1;border-left:4px solid #d97706;border-radius:8px;color:#594315}}
footer{{margin-top:38px;padding-top:16px;border-top:1px solid #e2e8f0;color:#64748b;font-size:12px}}
@media(max-width:820px){{.wrap{{padding:26px 20px}}.bucket-grid,.strategy-grid{{grid-template-columns:1fr}}.cluster-table{{font-size:12.5px}}}}
</style></head><body><main class="wrap">
<a class="home" href="../index.html">← Home</a>
<h1>arXiv Weekly Briefing — {ISO_WEEK}</h1>
<div class="meta"><div>소스: arXiv cs.CV/pastweek + cs.RO/pastweek · source_listing_date={SOURCE_LISTING_DATE}</div>
<div>주간 시야: {WEEK_START} ~ {WEEK_END} · daily artifacts: {", ".join(DAILY_DATES)}</div>
<div>pastweek parser: {payload['totals']['total_scanned']} dedup scanned · {payload['totals']['selected']} ROI selected</div></div>
<section class="thesis"><strong>이번 주의 결론:</strong> {esc(payload['weekly_thesis'])}</section>
<h2>주간 클러스터 표</h2><table class="cluster-table"><thead><tr><th>Cluster</th><th>대표 논문</th><th>왜 중요?</th><th>Confidence</th><th>Lab action</th></tr></thead><tbody>{''.join(cluster_rows)}</tbody></table>
<p class="note">이번 주의 핵심은 더 큰 모델을 찾는 것이 아니라, world state, data factor, geometry map, force budget, evidence trace가 실제 robot failure를 어느 지점에서 드러내는지 검증하는 것입니다.</p>
<h2>주간 Top 5</h2><ol class="top5">{top}</ol>
<h2>Bucket snapshot</h2><div class="bucket-grid">{buckets}</div>
<h2>APRL Leading Group Strategy Board</h2><div class="strategy-grid">{strategies}</div>
<footer>Generated from repository parser outputs and daily artifacts. Source prompt: prompts/instruction_v20260713.md.</footer>
</main></body></html>"""


def main() -> None:
    papers, buckets_full = classify_pastweek()
    by_id = {paper["arxiv_id"]: paper for paper in papers}
    clusters = []
    for spec in CLUSTERS:
        reps = [paper_ref(by_id[aid]) for aid in spec["ids"] if aid in by_id]
        if len(reps) < 2:
            raise SystemExit(f"cluster has too few representatives: {spec['cluster']}")
        clusters.append({
            "cluster": spec["cluster"],
            "representative_papers": reps,
            "why_it_matters": spec["why"],
            "confidence": spec["confidence"],
            "lab_action": spec["lab_action"],
        })

    daily_totals = {"cv": 0, "ro": 0, "selected": 0, "total_scanned": 0}
    for date in DAILY_DATES:
        trends = load_json(f"trends/{date}.json")
        counts = trends["daily_new_counts"]
        totals = trends["totals"]
        daily_totals["cv"] += counts["cv"]
        daily_totals["ro"] += counts["ro"]
        daily_totals["selected"] += totals["selected"]
        daily_totals["total_scanned"] += totals["total_scanned"]

    buckets = {b: {k: v for k, v in buckets_full[b].items() if k != "papers"} for b in BUCKET_ORDER}
    payload = {
        "date": DATE,
        "iso_week": ISO_WEEK,
        "week_start": WEEK_START,
        "week_end": WEEK_END,
        "source_mode": "pastweek",
        "source_listing_date": SOURCE_LISTING_DATE,
        "source_daily_artifacts": DAILY_DATES,
        "weekly_thesis": WEEKLY_THESIS,
        "totals": {"selected": sum(b["total"] for b in buckets.values()), "total_scanned": len({p["arxiv_id"] for p in papers})},
        "daily_totals": daily_totals,
        "buckets": buckets,
        "clusters": clusters,
        "top_papers": [{"title": title, "arxiv": f"https://arxiv.org/abs/{aid}", "why": why} for title, aid, why in TOP_PAPERS],
        "strategy_board": STRATEGY,
        "frontier_memory": {
            "strengthening": [
                "VLA execution interface and world-state contract repeated across all five daily briefings.",
                "Robot-usable geometry appeared as mapping, odometry, topology, and spatial-reasoning infrastructure.",
            ],
            "new": [
                "Bias-aware robot data scaling became explicit through Factor Dominance and AXIS-style growable snapshots.",
            ],
            "missing_axis": [
                "Few papers test the proposed contracts on shared real multi-sensor closed-loop episodes.",
            ],
        },
    }
    (ROOT / "weekly").mkdir(exist_ok=True)
    (ROOT / "posts").mkdir(exist_ok=True)
    (ROOT / "trends").mkdir(exist_ok=True)
    (ROOT / "weekly" / f"{ISO_WEEK}.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (ROOT / "posts" / f"{DATE}-weekly.html").write_text(render_html(payload), encoding="utf-8")
    trends = {
        "date": DATE,
        "source_listing_date": SOURCE_LISTING_DATE,
        "source_mode": "pastweek",
        "iso_week": ISO_WEEK,
        "totals": payload["totals"],
        "daily_totals": daily_totals,
        "buckets": buckets,
        "clusters": [{"cluster": c["cluster"], "why": c["why_it_matters"], "confidence": c["confidence"]} for c in clusters],
    }
    (ROOT / "trends" / f"{DATE}.json").write_text(json.dumps(trends, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote weekly/{ISO_WEEK}.json")
    print(f"wrote posts/{DATE}-weekly.html")
    print(f"wrote trends/{DATE}.json")


if __name__ == "__main__":
    main()
