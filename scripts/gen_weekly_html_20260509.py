#!/usr/bin/env python3
"""Generate 2026-05-09 weekly retrospective from parser-derived weekly_full.json."""
from __future__ import annotations

import html
import io
import json
import os
import sys

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

TODAY = "2026-05-09"
WEEK_LABEL = "2026-W19"
WEEK_START = "2026-05-03"
WEEK_END = "2026-05-09"
PREV_SNAPSHOT = "2026-05-02"

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


def esc(s):
    return html.escape(str(s), quote=False)


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def link(aid, label=None):
    return f'<a href="https://arxiv.org/abs/{aid}" target="_blank" rel="noopener">{esc(label or aid)}</a>'


def pct(now, prev):
    if not prev:
        return "—", ""
    d = round((now - prev) / prev * 100)
    if d > 0:
        return f"+{d}%", "delta-up"
    if d < 0:
        return f"{d}%", "delta-down"
    return "±0%", ""


def main():
    weekly_full = load("out/weekly_full.json")
    snap = weekly_full["snapshot"]
    buckets = snap["buckets"]
    prev = load(f"trends/{PREV_SNAPSHOT}.json") if os.path.exists(f"trends/{PREV_SNAPSHOT}.json") else {"buckets": {}}
    prev_buckets = prev.get("buckets_pastweek") or prev.get("buckets") or {}

    os.makedirs("posts", exist_ok=True)
    os.makedirs("weekly", exist_ok=True)

    top5 = [
        {
            "title": "ActCam: Zero-Shot Joint Camera and 3D Motion Control for Video Generation",
            "arxiv": "https://arxiv.org/abs/2605.06667",
            "why": "video generation이 sample quality에서 camera/actor motion controllability로 이동했다는 주간 신호.",
        },
        {
            "title": "From Pixels to Tokens: A Systematic Study of Latent Action Supervision for VLA Models",
            "arxiv": "https://arxiv.org/abs/2605.04678",
            "why": "VLA latent action supervision을 image-based/action-based로 나눠 formulation-task correspondence를 처음 systematic하게 정리.",
        },
        {
            "title": "TriRelVLA: Triadic Relational Structure for Generalizable Embodied Manipulation",
            "arxiv": "https://arxiv.org/abs/2605.05714",
            "why": "VLA 일반화를 object-hand-task relation 구조로 다시 잡아, '큰 모델'보다 '노출된 구조' 쪽으로 논점을 이동.",
        },
        {
            "title": "VideoRouter: Query-Adaptive Dual Routing for Efficient Long-Video Understanding",
            "arxiv": "https://arxiv.org/abs/2605.05848",
            "why": "long-video VLM의 memory/latency 병목을 query-adaptive routing으로 직접 찌른 deployment-side 핵심 결.",
        },
        {
            "title": "CXR-ContraBench: Benchmarking Negated-Option Attraction in Medical VLMs",
            "arxiv": "https://arxiv.org/abs/2605.05810",
            "why": "medical VLM의 'No X' 선택 오류를 별도 failure mode로 꺼낸 reliability benchmark.",
        },
    ]

    themes = [
        {
            "title": "Generation이 주간 최대 버킷으로 재가속",
            "summary": "Generation이 101편으로 가장 두꺼웠습니다. 핵심은 diffusion 논문 수 자체보다 camera control, long-video generation, atmospheric world model, robotic world model latent 같은 '조종 가능한 생성' 쪽으로 이동했다는 점입니다.",
        },
        {
            "title": "VLA는 monolithic policy에서 구조 노출 단계로 이동",
            "summary": "From Pixels to Tokens, TriRelVLA, VLA-GSE, When to Trust Imagination이 모두 VLA 내부를 분해합니다. latent action, relation graph, expert routing, future-reality verification이 서로 다른 이름으로 같은 질문을 던지는 셈입니다.",
        },
        {
            "title": "Reliability가 배포 파이프라인의 중심축으로 부상",
            "summary": "Query2Uncertainty, CXR-ContraBench, VideoRouter, open-set ID fraud discovery가 한 주에 같이 두꺼워졌습니다. 이제 안전은 별도 섹션이 아니라 calibration/routing/benchmark 설계의 기본층으로 들어오고 있습니다.",
        },
    ]

    predictions = [
        {
            "title": "VLA structure ablation이 다음주에도 3편 이상 이어진다",
            "claim": "latent action, relation graph, expert routing, WAM verifier가 한 주에 동시에 나왔기 때문에 다음 배치는 이 구조들 간 비교나 hybrid가 나올 가능성이 큽니다.",
            "rationale": "나오지 않으면 이번 주 VLA cluster는 단발 burst로 볼 수 있습니다.",
        },
        {
            "title": "Controllable video generation 벤치가 camera path fidelity를 분리 측정하기 시작한다",
            "claim": "ActCam/RealCam류 논문이 동시에 등장해 controllability의 정량 기준이 필요해졌습니다.",
            "rationale": "identity preservation, camera trajectory error, latency를 분리한 표가 다음 자연스러운 후속입니다.",
        },
        {
            "title": "Reliability-aware routing과 medical/3D calibration이 한 논문 안에서 만난다",
            "claim": "VideoRouter의 compute routing과 CXR-ContraBench/Query2Uncertainty의 reliability 축이 아직 따로 움직입니다.",
            "rationale": "배포에서는 효율과 안전이 분리되지 않으므로, 이 둘을 동시에 보는 논문이 곧 나올 가능성이 높습니다.",
        },
    ]

    weekly_json = {
        "date": TODAY,
        "iso_week": WEEK_LABEL,
        "week_start": WEEK_START,
        "week_end": WEEK_END,
        "predictions": predictions,
        "themes": themes,
        "top5": [{"title": x["title"], "arxiv": x["arxiv"]} for x in top5],
        "buckets_summary": {k: v["total"] for k, v in buckets.items()},
    }
    with open(f"weekly/{WEEK_LABEL}.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(weekly_json, f, ensure_ascii=False, indent=2)

    css = """
*,*::before,*::after{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif;background:#f6f7f9;color:#1f2328;line-height:1.74;font-size:15px;padding:32px 16px;word-break:keep-all}
.container{max-width:920px;margin:0 auto;background:#fff;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.06),0 1px 2px rgba(0,0,0,.04);padding:36px 48px 56px}
h1{font-size:28px;margin:0 0 6px;font-weight:700;color:#0d1117}h2{font-size:21px;margin:44px 0 14px;padding-bottom:8px;border-bottom:2px solid #e5e7eb;color:#0d1117}h3{font-size:17px;margin:20px 0 8px}p{margin:0 0 14px}a{color:#0969da;text-decoration:none}.subtitle{margin:0 0 22px;color:#656d76;font-size:14px}
.home-button{display:inline-block;padding:7px 14px;background:#f3f4f6;color:#374151;border:1px solid #d1d5db;border-radius:8px;font-size:13px;text-decoration:none;font-weight:500;margin:0 0 18px}
.weekly-banner{background:linear-gradient(135deg,#fff7ed 0%,#ffedd5 100%);border:1px solid #fdba74;border-radius:10px;padding:16px 22px;margin:0 0 26px;color:#7c2d12}
.meta{font-size:13px;color:#3b434d;padding:14px 18px;background:#f6f8fa;border-left:3px solid #f97316;border-radius:6px;margin:14px 0 28px}.meta div{margin:2px 0}
.exec-summary{background:#f0f9ff;border:1px solid #bae6fd;border-radius:10px;padding:18px 22px;margin:14px 0;font-size:15.5px;color:#0c4a6e}.exec-summary strong{color:#0c4a6e}
.bucket-bar{display:flex;align-items:center;gap:8px;margin:6px 0;font-size:13.5px}.bucket-bar .name{flex:0 0 150px;color:#475569;font-weight:500}.bucket-bar .bar{flex:1;height:14px;background:#e0f2fe;border-radius:3px;overflow:hidden}.bucket-bar .fill{height:100%;background:linear-gradient(90deg,#0ea5e9 0%,#f97316 100%)}.bucket-bar .num{flex:0 0 64px;text-align:right;font-variant-numeric:tabular-nums}.bucket-bar .delta{flex:0 0 64px;text-align:right;font-family:ui-monospace,monospace;font-size:12px;font-weight:700}.delta-up{color:#b91c1c}.delta-down{color:#0369a1}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}.panel,.card{background:#fafbfc;border:1px solid #e5e7eb;border-radius:8px;padding:14px 18px;margin:10px 0}.panel h3,.card h3{margin-top:0}
.top5{counter-reset:t5;padding:0;list-style:none}.top5 li{counter-increment:t5;padding:14px 16px 14px 50px;background:#fafbfc;border:1px solid #e5e7eb;border-radius:8px;margin:8px 0;position:relative}.top5 li::before{content:counter(t5);position:absolute;left:14px;top:14px;width:26px;height:26px;background:#0d1117;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700}.why{display:block;color:#475569;font-size:13.5px;margin-top:4px}
.deep{background:#fffbeb;border:1px solid #fde68a;border-radius:10px;padding:18px 22px;margin:14px 0}.note{background:#fff7ed;border:1px solid #fed7aa;border-radius:6px;padding:10px 14px;margin:10px 0;font-size:13px;color:#7c2d12}
.kw{font-family:ui-monospace,monospace;font-size:12.5px;display:flex;justify-content:space-between;border-bottom:1px dotted #e5e7eb;padding:2px 0}
footer{margin-top:48px;padding-top:18px;border-top:1px solid #e5e7eb;color:#656d76;font-size:13px}
@media(max-width:720px){.container{padding:24px 20px}.grid{grid-template-columns:1fr}.bucket-bar .name{flex-basis:120px}}
"""

    ordered = sorted(buckets.items(), key=lambda x: -x[1]["total"])
    max_total = ordered[0][1]["total"] if ordered else 1
    bars = []
    for name, info in ordered:
        prev_total = prev_buckets.get(name, {}).get("total", 0)
        delta, cls = pct(info["total"], prev_total)
        width = round(info["total"] / max_total * 100)
        bars.append(
            f'<div class="bucket-bar"><span class="name">{EMOJI.get(name,"")} {esc(name)}</span>'
            f'<span class="bar"><span class="fill" style="width:{width}%"></span></span>'
            f'<span class="num">{info["total"]}편</span><span class="delta {cls}">{delta}</span></div>'
        )

    cv_kw = "".join(f'<div class="kw"><span>{esc(k)}</span><strong>{v}</strong></div>' for k, v in snap["keywords_cv"][:10])
    ro_kw = "".join(f'<div class="kw"><span>{esc(k)}</span><strong>{v}</strong></div>' for k, v in snap["keywords_ro"][:10])

    html_doc = f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>arXiv Weekly Retrospective — {TODAY}</title><style>{css}</style></head><body><div class="container">
<a class="home-button" href="https://gisbi-kim.github.io/arxiv-daily-summary/">← 홈으로</a>
<h1>🗓 arXiv Weekly Retrospective</h1>
<p class="subtitle">{WEEK_LABEL} · {WEEK_START} ~ {WEEK_END} · cs.CV/cs.RO pastweek 누적 회고</p>
<div class="weekly-banner"><strong>토요일 주말판.</strong> 5월 8일 금요일 브리핑 누락분을 먼저 복구한 뒤, 그 데이터를 포함해 만든 주간 회고입니다.</div>
<div class="meta"><div>📅 발행: {TODAY} (토)</div><div>📊 주간 시야: pastweek {snap['totals']['total_scanned']}편 스캔 · ROI {snap['totals']['selected']}편 선별</div><div>🗂 비교 기준: {PREV_SNAPSHOT} 토요일 스냅샷</div></div>

<h2>🗓 ① Executive Summary</h2>
<div class="exec-summary">
이번주는 <strong>Generation이 101편으로 가장 두꺼웠고</strong>, 그 안에서도 video generation·world model·few-step diffusion·camera control처럼 “조종 가능한 생성” 쪽이 중심으로 올라왔습니다.
동시에 <strong>VLA는 monolithic policy에서 내부 구조를 노출하는 단계</strong>로 이동했습니다. {link('2605.04678','From Pixels to Tokens')}가 latent action supervision을 정리했고, {link('2605.05714','TriRelVLA')}와 {link('2605.06175','VLA-GSE')}가 relation/expert 구조를 드러냈습니다.
세 번째 흐름은 <strong>reliability가 배포 파이프라인의 기본층으로 들어온 것</strong>이에요. {link('2605.05328','Query2Uncertainty')}, {link('2605.05810','CXR-ContraBench')}, {link('2605.05848','VideoRouter')}가 모두 “언제 믿고, 언제 계산하고, 언제 의심할지”를 다룹니다.
</div>

<h2>🔭 주간 동향</h2>
<p>이번주 가장 분명한 흐름은 <strong>Generation 101편</strong>이 단순 생성 품질 경쟁을 넘어 controllable video, world model, few-step diffusion, camera-control 쪽으로 재정렬됐다는 점입니다. 금요일 {link('2605.06667','ActCam')}과 {link('2605.06051','RealCam')}이 특히 상징적이에요. 배우 motion과 카메라 경로를 함께 다루거나 실시간 camera-controlled V2V로 가면서, 생성 모델 평가가 “예쁜 결과”에서 “원하는 시점과 움직임을 얼마나 안정적으로 조종하나”로 옮겨가는 느낌입니다.</p>
<p>두 번째 축은 <strong>VLA 구조 노출</strong>입니다. {link('2605.04678','From Pixels to Tokens')}는 latent action supervision을 image-based/action-based로 나누고, {link('2605.05714','TriRelVLA')}는 object-hand-task relation을, {link('2605.06175','VLA-GSE')}는 expert routing을, {link('2605.06222','When to Trust Imagination')}은 WAM rollout을 언제 믿을지 검증합니다. 한 주를 통째로 보면 VLA를 더 크게 만드는 경쟁보다, 내부 표현과 실행 신뢰도를 분해해서 조작 가능한 축으로 만드는 경쟁이 더 선명했습니다.</p>
<p>세 번째로는 <strong>reliability와 efficiency가 같이 두꺼워진 점</strong>이 중요합니다. Efficiency/Systems 54편, Safety/Alignment 37편이었고, {link('2605.05848','VideoRouter')}·{link('2605.05328','Query2Uncertainty')}·{link('2605.05810','CXR-ContraBench')}가 서로 다른 도메인에서 같은 질문을 던집니다. 모델을 어디까지 믿을지, 언제 계산을 아낄지, 어떤 negation/shift에서 실패하는지까지 파이프라인 안으로 들어오는 중이라, 다음주는 효율과 안전을 따로 보기 어려울 것 같습니다.</p>

<h2>⚖️ ② Hot vs Cold</h2>
{''.join(bars)}
<div class="grid">
<div class="panel"><h3>⬆ Hot</h3><p><strong>Generation</strong>이 101편으로 압도적입니다. ActCam·RealCam·Earth-o1·robotic world model latent 논문들이 같은 방향을 봅니다. 생성은 이제 이미지 품질보다 controllability, state, evaluation substrate가 핵심이에요.</p><p><strong>Efficiency/Systems</strong>도 54편으로 두껍습니다. long-video routing, quantization, low-rank, edge inference가 같이 올라와 “모델을 실제로 굴리는 비용”이 이번주 핵심 제약으로 보입니다.</p></div>
<div class="panel"><h3>⬇ Cold</h3><p><strong>Embodied AI</strong>는 16편으로 가장 얇습니다. 다만 NavOne, RobotEQ, proactive instance navigation처럼 “navigation 자체”보다 “언어/지도/사용자 ambiguity를 어떻게 실행으로 바꿀지”에 집중된 결이 남았습니다.</p><p><strong>Autonomous Driving</strong>은 30편으로 중간권입니다. Driver-WM·ethical driver monitoring·V2X coordination이 있어 완전히 식은 것은 아니지만, 이번주 중심은 AD보다 broader reliability와 generation입니다.</p></div>
</div>

<h3>📐 CV vs RO 키워드</h3>
<div class="grid"><div class="card"><h3>CV top</h3>{cv_kw}</div><div class="card"><h3>RO top</h3>{ro_kw}</div></div>

<h2>🔥 ③ 주간 Top 5</h2>
<ol class="top5">
{''.join(f'<li><a href="{x["arxiv"]}" target="_blank"><strong>{esc(x["title"])}</strong></a><span class="why">{esc(x["why"])}</span></li>' for x in top5)}
</ol>

<h2>🌟 ④ Deep-dive — ActCam이 보여준 video generation의 새 평가축</h2>
<div class="deep">
<h3>{link('2605.06667','ActCam: Zero-Shot Joint Camera and 3D Motion Control for Video Generation')}</h3>
<p>ActCam은 video generation을 “프롬프트 넣고 결과를 기다리는 모델”이 아니라, 배우 motion과 camera trajectory를 같이 제어하는 촬영 도구로 봅니다. pretrained image-to-video diffusion 위에서 pose와 sparse depth를 초기 denoising에 넣고, 뒤에서는 depth를 빼고 pose guidance로 detail을 살리는 두 단계 schedule을 씁니다.</p>
<p>이게 중요한 이유는 평가축이 바뀌기 때문이에요. 앞으로 video generation은 FVD나 visual quality만으로 부족하고, camera path fidelity, identity preservation, geometry consistency, latency를 같이 봐야 합니다. RealCam까지 같이 보면 W19의 핵심은 “생성 품질”보다 “interactive controllability”입니다.</p>
<p><strong>약점:</strong> depth/pose condition 품질과 pretrained backbone에 의존합니다. 특히 빠른 camera motion, occlusion, 긴 sequence에서 identity가 유지되는지는 본문 수치와 데모를 함께 봐야 합니다.</p>
</div>

<h2>🧭 ⑤ 주간 테마 3개</h2>
{''.join(f'<div class="card theme-card"><h3>{esc(t["title"])}</h3><p>{esc(t["summary"])}</p></div>' for t in themes)}

<h2>🔮 ⑥ 다음주 예측</h2>
{''.join(f'<div class="card"><h3>{esc(p["title"])}</h3><p>{esc(p["claim"])}</p><p class="why">{esc(p["rationale"])}</p></div>' for p in predictions)}

<h2>🎧 ⑦ 주간 오디오</h2>
<div class="note">TTS 키가 이 로컬 실행 환경에 연결되어 있지 않아 mp3는 생성하지 않았습니다. HTML/RSS/weekly JSON은 정상 생성했습니다.</div>

<a class="home-button" href="https://gisbi-kim.github.io/arxiv-daily-summary/">🏠 전체 목록으로</a>
<footer>Generated {TODAY} · stdlib parser → build_weekly.py → weekly retrospective · WebFetch 미사용</footer>
</div></body></html>
"""

    with open(f"posts/{TODAY}-weekly.html", "w", encoding="utf-8", newline="\n") as f:
        f.write(html_doc)
    sys.stderr.write(f"wrote posts/{TODAY}-weekly.html\n")
    sys.stderr.write(f"wrote weekly/{WEEK_LABEL}.json\n")


if __name__ == "__main__":
    main()
