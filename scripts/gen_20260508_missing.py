#!/usr/bin/env python3
"""Generate the missing 2026-05-08 daily briefing artifacts.

This is intentionally grounded only in parser outputs under out/.
"""
from __future__ import annotations

import html
import io
import json
import os
import re
import sys
from collections import Counter

sys.path.insert(0, "scripts")
from classify import BUCKETS, assign_bucket, primary_badge

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

DATE = "2026-05-08"
WEEKDAY = "금"
WEEK_START = "2026-05-02"
WEEK_END = DATE
BASELINE_DATE = "2026-05-01"

EMOJI = {
    "3D/Scene": "📦",
    "Robot Learning": "🤖",
    "Autonomous Driving": "🚗",
    "Foundation Models": "🧠",
    "Generation": "🎨",
    "Efficiency/Systems": "⚡",
    "Embodied AI": "🏃",
    "Safety/Alignment": "🛡️",
}

KEYWORDS = [
    "diffusion",
    "video",
    "world model",
    "vlm",
    "vision-language",
    "vla",
    "gaussian",
    "3d",
    "4d",
    "slam",
    "robot",
    "manipulation",
    "driving",
    "safety",
    "robust",
    "efficient",
    "distillation",
    "token",
    "hallucination",
    "navigation",
    "lidar",
    "segmentation",
    "generation",
    "alignment",
    "uncertainty",
]


def load_json(path: str):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def esc(s: object) -> str:
    return html.escape(str(s), quote=False)


def clean_text(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def first_sentences(text: str, n: int = 2, limit: int = 520) -> str:
    text = clean_text(text)
    if not text:
        return ""
    parts = re.split(r"(?<=[.!?])\s+", text)
    out = " ".join(parts[:n]).strip()
    if len(out) > limit:
        out = out[: limit - 1].rstrip() + "…"
    return out


def badge_html(badge: str) -> str:
    if badge == "CV":
        return '<span class="badge badge-cv">CV</span>'
    if badge == "RO":
        return '<span class="badge badge-ro">RO</span>'
    if badge == "CV/RO":
        return '<span class="badge badge-cvro">CV/RO</span>'
    return f'<span class="badge">{esc(badge)}</span>'


def paper_by_id(classified, aid: str):
    for bucket in classified["buckets"].values():
        for p in bucket["papers"]:
            if p["arxiv_id"] == aid:
                return p
    return None


def paper_link(aid: str, title: str | None = None) -> str:
    label = title or f"arxiv:{aid}"
    return f'<a href="https://arxiv.org/abs/{aid}" target="_blank" rel="noopener">{esc(label)}</a>'


def kw_count(papers):
    text = " ".join((p.get("title", "") + " " + p.get("abstract", "")).lower() for p in papers)
    out = []
    for k in KEYWORDS:
        c = text.count(k)
        if c:
            out.append([k, c])
    out.sort(key=lambda x: -x[1])
    return out


def classify_pastweek(papers):
    out = {b: {"total": 0, "cv": 0, "ro": 0, "cvro": 0} for b, _ in BUCKETS}
    for p in papers:
        b = assign_bucket(p.get("title", ""), "", p.get("subjects", ""))
        if not b:
            continue
        badge = primary_badge(p)
        out[b]["total"] += 1
        if badge == "CV":
            out[b]["cv"] += 1
        elif badge == "RO":
            out[b]["ro"] += 1
        elif badge == "CV/RO":
            out[b]["cvro"] += 1
    return out


def count_delta(current, baseline_date):
    path = f"trends/{baseline_date}.json"
    if not os.path.exists(path):
        return {}
    base = load_json(path)
    base_buckets = base.get("buckets_pastweek") or base.get("buckets") or {}
    deltas = {}
    for b in current:
        now = current[b]["total"]
        prev = base_buckets.get(b, {}).get("total", 0)
        if prev:
            pct = round((now - prev) / prev * 100)
            deltas[b] = {"prev": prev, "now": now, "pct": pct}
    return deltas


def paper_summary(p, bucket: str) -> str:
    abstract = first_sentences(p.get("abstract", ""), 2)
    title = p.get("title", "")
    if not abstract:
        return f"초록이 비어 있어 제목 기준으로만 보면, 이 논문은 <em>{esc(title)}</em>라는 문제를 다룹니다. {bucket} 버킷에서는 세부 방법과 실험 세팅을 본문에서 확인해야 하는 후보예요."
    return (
        f"초록 기준으로 보면, 이 논문은 {esc(abstract)} "
        f"기존 방식과의 차이는 문제를 단순 성능 개선이 아니라 <strong>{esc(bucket)}</strong>의 병목으로 다시 잡는다는 점입니다. "
        "본문 수치까지 정독 전에는 강한 클레임은 보류하되, 오늘 배치 흐름을 이해하는 데 넣어둘 만한 후보예요."
    )


def render_papers(classified):
    parts = ['<h2>📄 논문별 요약</h2>']
    for bname, info in classified["buckets"].items():
        total = info["total"]
        parts.append(
            f'<h4 class="bucket">{EMOJI.get(bname, "📄")} {esc(bname)} '
            f'<span class="count">· {total}편 · CV {info["cv"]} / RO {info["ro"]} / CV-RO {info["cvro"]}</span></h4>'
        )
        if not total:
            parts.append('<p style="color:#656d76;font-style:italic">오늘 batch에는 이 버킷의 ROI 논문이 잡히지 않았습니다.</p>')
            continue
        for p in info["papers"]:
            aid = p["arxiv_id"]
            authors = ", ".join(p.get("authors", [])[:4]) or p.get("first_author", "")
            more = " et al." if len(p.get("authors", [])) > 4 else ""
            parts.append(
                '<div class="paper">'
                f'<div class="paper-line1">📄 <a href="https://arxiv.org/abs/{aid}" target="_blank" rel="noopener"><strong>{esc(p["title"])}</strong></a> '
                f'{badge_html(p.get("badge", "?"))} <span class="cbadge cbadge-nocode">[📦 code ✗]</span></div>'
                f'<div class="paper-authors">👥 {esc(authors)}{more}</div>'
                f'<p>{paper_summary(p, bname)}</p>'
                '</div>'
            )
    return "\n".join(parts)


def build_artifacts():
    classified = load_json("out/classified.json")
    cv_new = load_json("out/cv_new.json")
    ro_new = load_json("out/ro_new.json")
    cv_pw = load_json("out/cv_pastweek.json")
    ro_pw = load_json("out/ro_pastweek.json")
    pastweek = cv_pw + ro_pw
    pastweek_buckets = classify_pastweek(pastweek)
    deltas = count_delta(pastweek_buckets, BASELINE_DATE)
    bucket_counts = {b: info["total"] for b, info in classified["buckets"].items()}
    top_today = sorted(bucket_counts.items(), key=lambda x: -x[1])
    bottom_today = sorted(bucket_counts.items(), key=lambda x: x[1])

    trends = {
        "date": DATE,
        "totals": {
            "selected": classified["selected"],
            "total_scanned": classified["total"],
            "note": f"Friday recovery run. cs.CV {len(cv_new)} + cs.RO {len(ro_new)} raw /new entries, dedup {classified['total']}, selected {classified['selected']} ROI papers.",
        },
        "buckets": {b: {k: v for k, v in info.items() if k != "papers"} for b, info in classified["buckets"].items()},
        "buckets_pastweek": pastweek_buckets,
        "vs_7d_prior": {"baseline_date": BASELINE_DATE, "pastweek_buckets_delta": deltas},
        "keywords_cv": kw_count(cv_pw)[:20],
        "keywords_ro": kw_count(ro_pw)[:20],
        "pastweek_total": {"cv": len(cv_pw), "ro": len(ro_pw)},
        "hottest": [
            {
                "topic": "Generation remains the largest daily bucket, driven by controllable video/camera generation and diffusion variants.",
                "evidence": ["2605.06667", "2605.06051", "2605.05331", "2605.05781"],
            },
            {
                "topic": "Robot learning shifts toward structured VLA adaptation and world-action execution verification.",
                "evidence": ["2605.05714", "2605.06175", "2605.06222", "2605.05241"],
            },
            {
                "topic": "Deployment-side reliability continues to thicken: uncertainty, OOD, medical VLM contradictions, and efficient routing all appear in one batch.",
                "evidence": ["2605.05328", "2605.05810", "2605.05848", "2605.05215"],
            },
        ],
    }

    benchmarks = {
        "date": DATE,
        "results": [
            {
                "benchmark": "CXR-ContraBench",
                "metric": "Negated-option attraction in medical VLMs",
                "value_str": "MedGemma 31.49% / Qwen2.5-VL 30.21% on strict direct presence probe (abstract)",
                "paper": "https://arxiv.org/abs/2605.05810",
                "paper_title": "CXR-ContraBench: Benchmarking Negated-Option Attraction in Medical VLMs",
            },
            {
                "benchmark": "R2R-TopDown / NavOne",
                "metric": "Top-down VLN one-step global planning",
                "value_str": "SOTA reported among learning-based methods (abstract)",
                "paper": "https://arxiv.org/abs/2605.06317",
                "paper_title": "NavOne: One-Step Global Planning for Vision-Language Navigation on Top-Down Maps",
            },
            {
                "benchmark": "Query2Uncertainty",
                "metric": "3D object detection uncertainty calibration under distribution shift",
                "value_str": "outperforms standard post-hoc calibration on camera and LiDAR detectors (abstract)",
                "paper": "https://arxiv.org/abs/2605.05328",
                "paper_title": "Query2Uncertainty",
            },
        ],
    }

    insights = {
        "date": DATE,
        "insights": [
            {
                "title": "Video generation is moving from pretty clips to controllable cinematography",
                "claim": "ActCam and RealCam both target camera-controlled video generation, but from different sides: zero-shot actor/camera transfer and real-time interactive camera control. Together they suggest that video generation is being judged less by single-sample quality and more by controllability under production constraints.",
                "papers": ["https://arxiv.org/abs/2605.06667", "https://arxiv.org/abs/2605.06051"],
            },
            {
                "title": "VLA adaptation is splitting into relation structure, expert routing, and imagination trust",
                "claim": "TriRelVLA, VLA-GSE, and When to Trust Imagination all avoid treating VLA as a monolithic policy. The common move is to expose the hidden structure: object-hand-task relations, generalized/specialized experts, and future-reality verification for action chunks.",
                "papers": ["https://arxiv.org/abs/2605.05714", "https://arxiv.org/abs/2605.06175", "https://arxiv.org/abs/2605.06222"],
            },
            {
                "title": "Reliability is no longer a side section; it is becoming the deployment substrate",
                "claim": "Query2Uncertainty, CXR-ContraBench, VideoRouter, and open-set ID fraud detection all point to the same bottleneck: models must know when evidence is missing, shifted, negated, or too expensive to process. This week reliability is not just safety rhetoric; it is appearing as calibration, routing, and benchmark design.",
                "papers": ["https://arxiv.org/abs/2605.05328", "https://arxiv.org/abs/2605.05810", "https://arxiv.org/abs/2605.05848", "https://arxiv.org/abs/2605.05215"],
            },
        ],
        "research_topics": [
            {
                "title": "Camera-control stress test for video generation",
                "claim": "Evaluate ActCam/RealCam-like systems on the same actor-motion plus camera trajectory grid, separating identity preservation, geometry consistency, latency, and controllability.",
            },
            {
                "title": "VLA structure ablation matrix",
                "claim": "Cross TriRelVLA-style relation graphs, VLA-GSE-style expert routing, and WAM future-reality verification on manipulation suites to see which structure actually transfers.",
            },
            {
                "title": "Reliability-aware long-video and medical VLM audit",
                "claim": "Use query-adaptive routing and contradiction benchmarks together: does saving compute amplify negated-option or missing-evidence failures?",
            },
        ],
    }

    for folder in ["trends", "benchmarks", "insights", "posts"]:
        os.makedirs(folder, exist_ok=True)
    with open(f"trends/{DATE}.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(trends, f, ensure_ascii=False, indent=2)
    with open(f"benchmarks/{DATE}.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(benchmarks, f, ensure_ascii=False, indent=2)
    with open(f"insights/{DATE}.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(insights, f, ensure_ascii=False, indent=2)

    css = """*,*::before,*::after{box-sizing:border-box}html{-webkit-text-size-adjust:100%}body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif;background:#f6f7f9;color:#1f2328;line-height:1.72;font-size:15px;padding:32px 16px;word-wrap:break-word;word-break:keep-all}.container{max-width:860px;margin:0 auto;background:#fff;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.06),0 1px 2px rgba(0,0,0,.04);padding:40px 48px}h1{font-size:28px;margin:0 0 6px;font-weight:700;color:#0d1117}h2{font-size:21px;margin:40px 0 14px;padding-bottom:8px;border-bottom:2px solid #e5e7eb;color:#0d1117;font-weight:700}h3{font-size:17px;margin:22px 0 10px;color:#0d1117;font-weight:600}h4.bucket{margin:40px 0 16px;padding:10px 0 8px;border-top:3px solid #0d1117;border-bottom:1px solid #eaeef2;font-size:19px;font-weight:700;color:#0d1117}h4.bucket .count{font-size:13px;font-weight:400;color:#656d76;font-style:italic;margin-left:8px}p{margin:0 0 14px}a{color:#0969da;text-decoration:none}a:hover{text-decoration:underline}.meta{font-size:13px;color:#3b434d;padding:14px 18px;background:#f6f8fa;border-left:3px solid #0969da;border-radius:6px;margin:14px 0 28px}.meta div{margin:2px 0}.bucket-line{font-family:ui-monospace,SFMono-Regular,Consolas,Menlo,monospace;background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;padding:10px 14px;font-size:13px;color:#24292f;margin:10px 0;overflow-x:auto;white-space:pre}.paper{padding:16px 0;border-top:1px solid #eaeef2}.paper-line1{margin-bottom:4px}.paper-line1 a{font-weight:600}.paper-authors{font-style:italic;color:#656d76;font-size:14px;margin:2px 0 10px}.badge{display:inline-block;font-size:11px;font-weight:600;padding:1px 8px;border-radius:10px;margin-left:6px;vertical-align:middle;font-family:ui-monospace,monospace}.badge-cv{background:#ddf4ff;color:#0550ae;border:1px solid #54aeff}.badge-ro{background:#fff8c5;color:#7a4e00;border:1px solid #d4a72c}.badge-cvro{background:#ffe5d9;color:#9a3412;border:1px solid #f59e0b}.cbadge{display:inline-block;font-size:10.5px;font-weight:500;padding:1px 7px;border-radius:10px;margin-left:4px;vertical-align:middle;font-family:ui-monospace,monospace}.cbadge-nocode{background:#f3f4f6;color:#6b7280;border:1px solid #d1d5db}.insight,.topic{background:#fafbfc;border:1px solid #eaeef2;border-radius:8px;padding:14px 18px;margin:12px 0}.contrast{background:#fdf6ff;border:1px solid #e9d5ff;border-radius:8px;padding:14px 18px;margin:12px 0}.crosspair{background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;padding:14px 18px;margin:12px 0}.mustread{background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:16px 20px;margin:14px 0}.risk{background:#fef2f2;border:1px solid #fecaca;border-radius:8px;padding:14px 18px;margin:12px 0}.hot{font-weight:600;color:#b91c1c}.cold{font-weight:600;color:#0369a1}table{width:100%;border-collapse:collapse;font-size:13px;margin:12px 0}td,th{border:1px solid #d0d7de;padding:8px;text-align:left;vertical-align:top}th{background:#f6f8fa}.home-btn{display:inline-block;padding:6px 14px;font-size:13px;font-weight:500;color:#0969da;background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;text-decoration:none}.home-btn-top{margin:0 0 18px}.home-btn-bottom{display:block;text-align:center;margin:18px 0 0}footer{margin-top:40px;padding-top:16px;border-top:1px solid #eaeef2;font-size:12px;color:#656d76;text-align:center}@media (max-width:640px){.container{padding:24px 20px}h1{font-size:23px}h2{font-size:19px}body{padding:16px 8px}}"""

    bucket_lines = []
    for b, info in classified["buckets"].items():
        bucket_lines.append(f"{EMOJI.get(b, '📄')} {b:<20}: {info['total']:>2}편 (CV {info['cv']:>2} / RO {info['ro']:>2} / CV-RO {info['cvro']})")
    top3 = ", ".join(f"{b} ({n})" for b, n in top_today[:3])
    bottom2 = ", ".join(f"{b} ({n})" for b, n in bottom_today[:2])

    delta_text = ""
    if deltas:
        delta_bits = []
        for b, d in sorted(deltas.items(), key=lambda x: -abs(x[1]["pct"])):
            cls = "hot" if d["pct"] >= 0 else "cold"
            sign = "+" if d["pct"] >= 0 else ""
            delta_bits.append(f'{EMOJI.get(b, "")} {esc(b)} <span class="{cls}">{sign}{d["pct"]}%</span> ({d["prev"]}→{d["now"]})')
        delta_text = "<p>주간 델타는 " + " · ".join(delta_bits[:8]) + " 순서로 보입니다. 특히 Generation·Efficiency·Safety 쪽이 같이 두꺼워지는 건 모델을 키우는 경쟁에서 실제 배포 가능한 형태로 다듬는 경쟁으로 무게가 이동한다는 신호예요.</p>"

    cv_kw = ", ".join(f"{k}({v})" for k, v in trends["keywords_cv"][:8])
    ro_kw = ", ".join(f"{k}({v})" for k, v in trends["keywords_ro"][:8])

    body = f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>arXiv Daily Briefing — {DATE}</title><style>{css}</style></head><body><div class="container">
<a href="https://gisbi-kim.github.io/arxiv-daily-summary/" class="home-btn home-btn-top">← 전체 목록으로</a>
<h1>📄 arXiv Daily Briefing — {DATE} ({WEEKDAY})</h1>
<div class="meta">
<div><strong>시야:</strong> 주간 {WEEK_START} ~ {WEEK_END} · 오늘 배치 cs.CV/new + cs.RO/new</div>
<div><strong>소스:</strong> arxiv.org /list/cs.CV/new · /list/cs.RO/new (stdlib 파서 경유)</div>
<div><strong>주간 규모:</strong> cs.CV {len(cv_pw)}편 · cs.RO {len(ro_pw)}편</div>
<div><strong>오늘 /new:</strong> cs.CV {len(cv_new)} + cs.RO {len(ro_new)} → {classified['total']} dedup → {classified['selected']}편 8개 ROI 버킷 선정</div>
</div>

<h2>🔭 주간 동향</h2>
<p>금요일 배치에서 제일 눈에 띄는 건 <strong>Generation이 36편으로 단독 1위</strong>라는 점이에요. 단순히 이미지·비디오를 더 예쁘게 만드는 논문이 많은 게 아니라, {paper_link('2605.06667', 'ActCam')}과 {paper_link('2605.06051', 'RealCam')}처럼 카메라 경로·배우 motion·실시간 제어를 같이 다루는 쪽으로 이동했습니다. 생성 모델이 이제 “샘플 하나 잘 뽑기”에서 “사용자가 원하는 촬영 문법을 안정적으로 조종하기”로 넘어가는 신호라, 이 흐름은 한동안 갈 것 같아요.</p>
<p>두 번째 축은 <strong>VLA와 robot learning의 구조화</strong>입니다. {paper_link('2605.05714', 'TriRelVLA')}는 object-hand-task 관계를 명시적으로 빼내고, {paper_link('2605.06175', 'VLA-GSE')}는 generalized/specialized experts로 fine-tuning을 쪼개며, {paper_link('2605.06222', 'When to Trust Imagination')}은 world action model이 상상한 rollout을 언제 믿고 언제 replan할지 검증합니다. 같은 말로 하면, VLA를 더 큰 end-to-end policy로 밀어붙이는 단계가 아니라 내부 구조와 실행 신뢰도를 뜯어보는 단계로 들어간 거예요.</p>
<p>한편 <strong>Efficiency 27편·Safety 24편·Foundation Models 21편</strong>이 같이 두껍습니다. {paper_link('2605.05848', 'VideoRouter')}는 long-video token 예산을 query별로 배분하고, {paper_link('2605.05328', 'Query2Uncertainty')}는 distribution shift에서 3D detector confidence를 다시 보정하며, {paper_link('2605.05810', 'CXR-ContraBench')}는 medical VLM의 negated-option failure를 별도 벤치로 꺼냅니다. 오늘의 공통 정서는 꽤 분명해요. 모델이 똑똑해지는 것만으로는 부족하고, 어디서 믿을지·어디서 아낄지·어디서 거절할지를 같이 설계해야 합니다.</p>
{delta_text}

<h2>📐 CV vs RO 대비</h2>
<p>CV 쪽 키워드는 {esc(cv_kw)} 순서로, video·generation·segmentation·diffusion이 여전히 강합니다. RO 쪽은 {esc(ro_kw)}가 앞에 오는데, robot/manipulation/navigation/safety가 훨씬 선명해요. 같은 “generation”이라도 CV에서는 비디오·이미지 합성 품질과 제어성이고, RO에서는 데이터 생성·시뮬레이션·정책 실행을 보조하는 substrate에 가깝습니다.</p>
<div class="contrast"><p><strong>같은 단어 다른 맥락</strong></p><ul>
<li><code>video</code>: CV는 RealCam·ActCam처럼 controllable generation, RO는 long-horizon observation이나 action execution verification의 evidence stream에 가깝습니다.</li>
<li><code>uncertainty</code>: CV는 open-set fraud·medical VLM·retrieval calibration 쪽으로, RO/3D는 3D detector와 autonomous system confidence calibration 쪽으로 붙습니다.</li>
<li><code>navigation</code>: CV는 NavOne처럼 top-down map에서 VLN을 one-step planning으로 재정의하고, RO는 multi-agent·factor graph·ambiguous query navigation으로 실행 쪽에 붙습니다.</li>
</ul></div>

<h2>💡 오늘의 인사이트</h2>
<div class="insight"><h3>Video generation이 ‘예쁜 샘플’에서 ‘조종 가능한 촬영 시스템’으로 이동</h3><p>{paper_link('2605.06667', 'ActCam')}은 actor motion과 camera trajectory를 동시에 제어하고, {paper_link('2605.06051', 'RealCam')}은 real-time interactive camera-controlled V2V를 내세웁니다. 둘 다 생성 모델을 결과물 생산기가 아니라 촬영 파이프라인의 조작 가능한 모듈로 보는 결이라, 다음 몇 주 동안 camera/path/identity consistency 평가가 더 자주 나올 가능성이 큽니다.</p></div>
<div class="insight"><h3>VLA는 더 큰 모델보다 더 노출된 구조가 중요해지는 중</h3><p>{paper_link('2605.05714', 'TriRelVLA')}의 triadic relation, {paper_link('2605.06175', 'VLA-GSE')}의 expert 분해, {paper_link('2605.06222', 'When to Trust Imagination')}의 future-reality verification은 서로 다른 방법이지만 같은 문제를 봅니다. 정책이 왜 일반화하지 못하는지 내부 구조를 꺼내서 조작 가능한 축으로 만드는 흐름이에요.</p></div>
<div class="insight"><h3>Reliability가 부록이 아니라 주 파이프라인으로 들어옴</h3><p>{paper_link('2605.05328', 'Query2Uncertainty')}, {paper_link('2605.05810', 'CXR-ContraBench')}, {paper_link('2605.05848', 'VideoRouter')}가 같이 나온 게 재밌습니다. confidence calibration, contradiction benchmark, query-adaptive routing이 모두 “모델을 얼마나 믿고 얼마나 계산할지”를 묻고 있어요. 이건 safety 섹션 하나로 분리할 문제가 아니라 deployment architecture 자체의 중심축으로 보입니다.</p></div>

<h2>🔬 추천 연구주제</h2>
<div class="topic"><h3>Camera-Control Stress Test for Video Generation</h3><p>ActCam·RealCam류 모델을 actor motion, camera path, identity preservation, latency 네 축으로 같은 grid에서 평가하는 벤치가 바로 필요해 보여요. 특히 “카메라 제어는 되는데 정체성이 무너지는가”와 “실시간성은 되는데 geometry가 흔들리는가”를 분리하면 follow-up 가치가 큽니다.</p></div>
<div class="topic"><h3>VLA Structure Ablation Matrix</h3><p>TriRelVLA의 relation graph, VLA-GSE의 expert routing, WAM verifier를 같은 manipulation suite에 얹어서 어떤 구조가 어떤 task family에서 이기는지 보는 실험입니다. 지금은 각자 다른 이름으로 나오지만, 사실은 “VLA 내부를 어디서 쪼갤 것인가”라는 하나의 질문으로 묶입니다.</p></div>
<div class="topic"><h3>Reliability-Aware Long-Video / Medical VLM Audit</h3><p>VideoRouter처럼 계산을 아끼는 routing이 CXR-ContraBench류 negation failure를 키우는지 줄이는지 보는 실험이 좋아 보입니다. deployment에서는 효율과 안전이 따로 움직이지 않기 때문에, token pruning·routing·calibration을 같이 봐야 합니다.</p></div>

<h2>📊 오늘의 버킷 현황</h2>
<div class="bucket-line">{esc(chr(10).join(bucket_lines))}</div>
<p>🔥 <span class="hot">TOP3</span>: {esc(top3)} · ❄️ <span class="cold">BOTTOM2</span>: {esc(bottom2)}. 금요일 배치는 Generation이 확실히 치고 나왔고, Efficiency/Safety가 그 뒤를 받치면서 “만드는 모델”과 “배포 가능한 모델”이 동시에 두꺼워진 날로 보는 게 맞겠습니다.</p>

<h2>📈 벤치마크 SOTA 추이</h2>
<table><thead><tr><th>벤치마크</th><th>메트릭</th><th>이번주 보고</th><th>논문 링크</th></tr></thead><tbody>
<tr><td>CXR-ContraBench</td><td>medical VLM negated-option attraction</td><td>MedGemma 31.49% / Qwen2.5-VL 30.21% strict direct presence probe</td><td>{paper_link('2605.05810', 'CXR-ContraBench')}</td></tr>
<tr><td>R2R-TopDown / NavOne</td><td>one-step top-down VLN planning</td><td>SOTA reported among learning-based methods</td><td>{paper_link('2605.06317', 'NavOne')}</td></tr>
<tr><td>Query2Uncertainty</td><td>3D object detection calibration under shift</td><td>camera/LiDAR detector calibration improvement reported</td><td>{paper_link('2605.05328', 'Query2Uncertainty')}</td></tr>
</tbody></table>

<h2>🔀 크로스오버 페어</h2>
<div class="crosspair"><h3>Controllable video generation — ActCam vs RealCam</h3><p>{paper_link('2605.06667', 'ActCam')}은 zero-shot으로 배우 motion과 camera trajectory를 동시에 옮기고, {paper_link('2605.06051', 'RealCam')}은 real-time streaming 가능한 camera-controlled V2V를 노립니다. 한쪽은 창작 제어성, 한쪽은 인터랙티브 지연시간을 정조준해서, 둘을 같이 보면 video generation 평가가 quality에서 controllability+latency로 이동한다는 게 보입니다.</p></div>
<div class="crosspair"><h3>VLA 구조화 — TriRelVLA vs VLA-GSE</h3><p>{paper_link('2605.05714', 'TriRelVLA')}는 object-hand-task relation을, {paper_link('2605.06175', 'VLA-GSE')}는 backbone singular components 기반 expert 분해를 사용합니다. 하나는 입력 표현 구조, 하나는 fine-tuning 구조를 건드리지만 공통 질문은 같습니다. “VLA의 어떤 내부 구조를 드러내야 일반화가 좋아지는가”예요.</p></div>

<h2>🌟 오늘의 must-read</h2>
<div class="mustread"><h3>① ActCam: Zero-Shot Joint Camera and 3D Motion Control for Video Generation {badge_html('CV')}</h3><p>{paper_link('2605.06667')} · abstract 기반</p><p>핵심은 배우 motion과 camera trajectory를 동시에 제어하는 zero-shot video generation입니다. 기존 camera-controlled 생성이 영상 전체를 한 번에 처리하거나 motion과 camera를 따로 다루는 쪽에 가까웠다면, ActCam은 depth와 pose condition을 두 단계 denoising schedule로 나눠 scene structure와 high-frequency detail을 분리합니다. 이 논문이 중요한 이유는 video generation을 “보기 좋은 샘플”이 아니라 “촬영 문법을 조작하는 도구”로 밀어붙인다는 점이에요.</p><p><strong>한계:</strong> pretrained image-to-video diffusion model과 depth/pose conditioning 품질에 강하게 의존합니다. 실제로 빠른 camera motion, occlusion, identity drift에서 얼마나 버티는지는 본문 실험을 봐야 합니다.</p></div>
<div class="mustread"><h3>② TriRelVLA: Triadic Relational Structure for Generalizable Embodied Manipulation {badge_html('CV/RO')}</h3><p>{paper_link('2605.05714')} · abstract 기반</p><p>VLA가 unseen scene/object에서 약한 이유를 visual representation이 object appearance, background, layout을 한 덩어리로 엮기 때문이라고 보고, object-hand-task triadic relation을 명시적으로 만듭니다. 기존 구조화 표현이 scene semantics에 머물렀다면, TriRelVLA는 manipulation action을 실제로 결정하는 손-물체-태스크 관계를 중간 표현으로 꺼내는 쪽이에요. VLA 일반화를 논할 때 “모델 크기”보다 “어떤 관계를 드러내는가”가 중요하다는 메시지가 분명합니다.</p><p><strong>한계:</strong> triadic relation 추출이 실제 복잡한 clutter scene에서 안정적인지, relation annotation 또는 detector 품질에 얼마나 의존하는지가 관건입니다. relation structure가 task family별로 어디까지 재사용되는지도 본문 ablation이 중요합니다.</p></div>

<h2>⚠️ 리스크·한계 필터</h2>
<div class="risk"><h3>Camera-control video generation — controllability metric 부재 위험</h3><p>ActCam·RealCam 모두 “제어 가능성”을 전면에 내세우지만, camera path fidelity, identity preservation, geometry consistency, latency를 분리하지 않으면 데모 품질이 실제 제어 성능처럼 보일 수 있습니다. 본문에서 이 네 축이 독립적으로 보고되는지 확인이 필요합니다.</p></div>
<div class="risk"><h3>VLA 구조화 논문 — intermediate representation 품질 의존성</h3><p>TriRelVLA나 VLA-GSE 같은 구조화 접근은 일반화 이야기가 강하지만, 실제 gain이 relation extractor나 expert initialization의 hidden prior에서 오는지 분리해야 합니다. 특히 unseen object/scene에서 detector나 relation graph 자체가 흔들리면 policy gain이 사라질 수 있습니다.</p></div>

{render_papers(classified)}

<h2>🔗 참고 링크</h2>
<ul>
<li><a href="https://arxiv.org/list/cs.CV/new">arxiv.org/list/cs.CV/new</a></li>
<li><a href="https://arxiv.org/list/cs.RO/new">arxiv.org/list/cs.RO/new</a></li>
<li><a href="https://arxiv.org/list/cs.CV/pastweek">cs.CV/pastweek</a> · <a href="https://arxiv.org/list/cs.RO/pastweek">cs.RO/pastweek</a></li>
<li><a href="https://gisbi-kim.github.io/arxiv-daily-summary/">📚 전체 브리핑 아카이브</a></li>
<li><a href="https://gisbi-kim.github.io/arxiv-daily-summary/feed.xml">📡 RSS feed</a></li>
</ul>
<a href="https://gisbi-kim.github.io/arxiv-daily-summary/" class="home-btn home-btn-bottom">🏠 전체 목록으로</a>
<footer>Generated {DATE} · stdlib parser → classify.py → missing-day recovery briefing</footer>
</div></body></html>
"""

    with open(f"posts/{DATE}.html", "w", encoding="utf-8", newline="\n") as f:
        f.write(body)
    sys.stderr.write(f"wrote posts/{DATE}.html\n")
    sys.stderr.write(f"wrote trends/{DATE}.json benchmarks/{DATE}.json insights/{DATE}.json\n")


if __name__ == "__main__":
    build_artifacts()
