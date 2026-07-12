#!/usr/bin/env python3
"""Generate the 2026-W28 retrospective from committed daily artifacts."""
from __future__ import annotations

import html
import json
from pathlib import Path

DATE = "2026-07-11"
WEEK = "2026-W28"
START = "2026-07-06"
END = "2026-07-12"
DAYS = ["2026-07-07", "2026-07-08", "2026-07-09", "2026-07-10"]
ROOT = Path(__file__).resolve().parents[1]
BUCKETS = ["3D/Scene", "Robot Learning", "Autonomous Driving", "Foundation Models", "Generation", "Efficiency/Systems", "Embodied AI", "Safety/Alignment"]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def esc(value):
    return html.escape(str(value or ""), quote=False)


def collect():
    trends = [load(ROOT / "trends" / f"{d}.json") for d in DAYS]
    insights = [load(ROOT / "insights" / f"{d}.json") for d in DAYS]
    totals = {
        "total_scanned": sum(x["totals"]["total_scanned"] for x in trends),
        "selected": sum(x["totals"]["selected"] for x in trends),
        "cv": sum(x["daily_new_counts"]["cv"] for x in trends),
        "ro": sum(x["daily_new_counts"]["ro"] for x in trends),
    }
    bucket_totals = {b: {"total": 0, "cv": 0, "ro": 0, "cvro": 0} for b in BUCKETS}
    for trend in trends:
        for b in BUCKETS:
            for key in bucket_totals[b]:
                bucket_totals[b][key] += int(trend["buckets"][b].get(key, 0))
    papers = {}
    for report in insights:
        for cluster in report.get("clusters", []):
            for paper in cluster.get("papers", []):
                key = paper.get("arxiv") or paper.get("arxiv_id")
                if key:
                    papers[key] = paper
    return totals, bucket_totals, papers


def choose(papers, ids):
    by_id = {}
    for p in papers.values():
        raw = p.get("arxiv") or p.get("arxiv_id", "")
        by_id[raw.rsplit("/", 1)[-1]] = p
    return [by_id[x] for x in ids if x in by_id]


def main():
    totals, bucket_totals, all_papers = collect()
    specs = [
        ("VLA가 규모 경쟁에서 memory·safety·embodiment stress test로 이동",
         ["2607.03693", "2607.04171", "2607.06564", "2607.07608", "2607.08575", "2607.08751"],
         "이번 주 Robot Learning은 가장 두꺼운 축 중 하나였지만 핵심은 모델 크기가 아닙니다. CoRE-VLA와 XS-VLA의 확장성, Lift3D-VLA의 geometry, Dual Latent Memory의 장기 상태, FabriVLA의 경량 배포, DexVerse의 embodiment 다양성이 한꺼번에 등장했습니다. VLA 평가는 seen-task 성공률보다 기억, 3D dynamics, 새 embodiment에서 어디서 무너지는지를 분리해야 합니다.",
         "LIBERO/RoboCasa에서 memory length, 3D cue, compute budget, embodiment를 독립 ablation으로 두고 success, recovery time, unsafe action을 비교합니다."),
        ("Geometry/SLAM이 Gaussian 렌더링에서 localization 가능한 동적 map으로 이동",
         ["2607.04127", "2607.06464", "2607.06023", "2607.07452", "2607.08408", "2607.08250"],
         "Real-Time LiDAR Gaussian Splatting SLAM, Hilti-Trimble-Oxford, visual SLAM 분석, GeoGS-SLAM, Track2Map, dynamic Gaussian MoE는 3D 표현을 예쁜 장면이 아니라 움직이는 환경에서 갱신 가능한 로봇 map으로 밀고 있습니다. 렌더링 점수만으로는 pose drift와 loop closure 실패를 가리므로 robot-usable validity가 중심 평가가 되어야 합니다.",
         "동일 indoor/outdoor trajectory에서 Gaussian, LiDAR-inertial, deformable map을 비교하고 pose drift, loop closure, update cost, navigation success를 측정합니다."),
        ("Embodied navigation이 long-horizon·social interaction·on-device 제약을 함께 다루기 시작",
         ["2607.03920", "2607.05377", "2607.05765", "2607.06537", "2607.06882", "2607.08359"],
         "LH-AVLN, Cortex, Image2Sim, UniLM-Nav, GemNav, FSD-VLN은 navigation을 정적 goal-reaching에서 긴 horizon의 multimodal memory와 빠른/느린 판단 구조로 확장합니다. 실제 배포에서는 시점 변화, 사람과의 상호작용, 제한된 계산량이 동시에 나타나므로 이 조건들을 분리한 폐루프 평가가 필요합니다.",
         "VLN/ObjectNav에서 horizon, social density, observation corruption, compute budget을 stress split으로 만들고 goal success, collision, recovery를 비교합니다."),
        ("Driving 평가는 open-loop 정확도에서 long-tail shift와 closed-loop recovery로 이동",
         ["2607.02841", "2607.04331", "2607.05783", "2607.06328", "2607.07601", "2607.07844"],
         "CLEAR, agent-driven long-tail simulation, 환경 교란 robustness, interpretability 기반 failure 분석, CARLA-GS, Shift & Drift는 자율주행의 평균 성능보다 재현 가능한 분포 변화와 회복 능력을 묻습니다. long-tail을 생성하는 것과 그 안에서 policy가 안전하게 복구하는 것을 같은 benchmark에서 연결해야 합니다.",
         "CARLA에서 weather, sensor drift, rare interaction, map shift를 조작하고 near-miss, rule violation, recovery success를 공동 측정합니다."),
        ("Multimodal 신뢰성이 hallucination 점수에서 evidence grounding과 구조 보존으로 확장",
         ["2607.04163", "2607.04401", "2607.05978", "2607.06420", "2607.07395", "2607.07507"],
         "SeeMe, brittle VLM benchmark, grounding confidence, HoloCount, graph-attribute reasoning, HIVE는 정답 여부만으로 모델이 실제 시각 근거를 사용했는지 알 수 없음을 보여줍니다. cue removal과 구조 교란을 통해 shortcut, post-hallucination reasoning, calibration failure를 분리해야 합니다.",
         "VQA/robotic instruction에서 cue removal, graph structure corruption, viewpoint shift를 적용하고 evidence recall, calibration, task success를 비교합니다."),
        ("효율화가 FLOPs 절감에서 task-critical token과 실시간 제어 보존으로 이동",
         ["2607.03050", "2607.04098", "2607.06982", "2607.07033", "2607.08221", "2607.08771"],
         "OmniFocus, Sparse4D-Radar, EdgeCompress, AnchorPrune, LUMI, ZipDepth는 압축률 자체보다 중요한 공간 정보와 downstream decision을 보존하는 문제를 다룹니다. 로봇 배포에서 효율성은 latency와 memory뿐 아니라 OOD scene에서 perception 및 control 성능이 얼마나 유지되는지로 판단해야 합니다.",
         "token budget, compression ratio, input resolution을 조절하고 latency, memory, OOD perception, downstream control의 Pareto frontier를 비교합니다."),
    ]
    clusters = []
    for title, ids, why, action in specs:
        ps = choose(all_papers, ids)
        clusters.append({"title": title, "papers": ps, "why": why, "action": action})

    payload = {
        "date": DATE, "iso_week": WEEK, "week_start": START, "week_end": END,
        "source_mode": "committed-daily-artifacts", "source_dates": DAYS,
        "weekly_thesis": "이번 주는 VLA, Gaussian SLAM, embodied navigation, driving, VLM reliability, efficiency가 모두 규모 확대보다 실패 조건과 폐루프 회복을 검증하는 방향으로 수렴했습니다.",
        "totals": totals, "buckets": bucket_totals,
        "clusters": [{"cluster": c["title"], "representative_papers": c["papers"], "why_it_matters": c["why"], "lab_action": c["action"]} for c in clusters],
    }
    (ROOT / "weekly" / f"{WEEK}.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    rows = []
    for c in clusters:
        links = []
        for p in c["papers"]:
            url = p.get("arxiv") or f"https://arxiv.org/abs/{p.get('arxiv_id','')}"
            phy = p.get("phylogeny", {})
            lineage = " &gt; ".join(esc(phy.get(k, "")) for k in ["phylum", "class", "order", "genus"] if phy.get(k))
            links.append(f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(p.get("title"))}</a><span class="phy">Phylogeny: {lineage}</span>')
        rows.append(f'<article class="theme-card"><h3>{esc(c["title"])}</h3><div class="papers">{"".join(links)}</div><p><strong>왜 중요?</strong> {esc(c["why"])}</p><p class="action"><strong>Lab action</strong> {esc(c["action"])}</p></article>')
    bars = "".join(f'<div class="bar"><span>{esc(b)}</span><b>{x["total"]}편</b></div>' for b, x in sorted(bucket_totals.items(), key=lambda kv: -kv[1]["total"]))
    css = """body{margin:0;background:#f5f7fa;color:#1f2937;font:15px/1.7 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}.wrap{max-width:980px;margin:30px auto;padding:38px 46px;background:white;border-radius:14px;box-shadow:0 2px 12px #0001}a{color:#0969da;text-decoration:none}h1{margin:0;font-size:29px}h2{margin-top:38px;border-bottom:2px solid #e5e7eb;padding-bottom:8px}.meta,.thesis{padding:16px 20px;border-radius:9px;margin:18px 0}.meta{background:#f3f4f6}.thesis{background:#172554;color:white;font-size:17px}.bars{display:grid;grid-template-columns:repeat(2,1fr);gap:8px}.bar{display:flex;justify-content:space-between;background:#eff6ff;padding:8px 12px;border-radius:6px}.theme-card{border:1px solid #dbe2ea;border-radius:10px;padding:17px 20px;margin:14px 0;background:#fbfdff}.theme-card h3{margin:0 0 12px}.papers{display:grid;grid-template-columns:repeat(2,1fr);gap:8px}.papers a{display:block;font-weight:600}.phy{display:block;font-size:11px;color:#64748b;margin-bottom:5px}.action{border-left:3px solid #22c55e;padding-left:12px;background:#f0fdf4}.home{display:inline-block;margin-bottom:15px}.footer{margin-top:36px;color:#6b7280;font-size:12px}@media(max-width:700px){.wrap{margin:0;padding:24px 18px;border-radius:0}.papers,.bars{grid-template-columns:1fr}}"""
    doc = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>arXiv Weekly Retrospective — {DATE}</title><style>{css}</style></head><body><main class="wrap"><a class="home" href="../index.html">← 홈으로</a><h1>🗓 arXiv Weekly Retrospective — {WEEK}</h1><div class="meta">{START} ~ {END} · 실제 listing {len(DAYS)}일 · cs.CV {totals['cv']}편 · cs.RO {totals['ro']}편 · dedupe 기준 {totals['total_scanned']}편 스캔 / ROI {totals['selected']}편</div><div class="thesis"><strong>이번 주 결론:</strong> {esc(payload['weekly_thesis'])}</div><h2>버킷 분포</h2><section class="bars">{bars}</section><h2>주간 핵심 흐름</h2>{''.join(rows)}<div class="footer">Source: committed daily artifacts for {', '.join(DAYS)} · generated {DATE}</div></main></body></html>'''
    (ROOT / "posts" / f"{DATE}-weekly.html").write_text(doc, encoding="utf-8")
    print(f"wrote {WEEK}: {len(clusters)} themes, {sum(len(c['papers']) for c in clusters)} paper references")


if __name__ == "__main__":
    main()
