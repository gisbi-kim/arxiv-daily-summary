#!/usr/bin/env python3
"""Build posts/2026-05-02-weekly.html — Saturday Weekly Retrospective for 2026-W18."""
import json, os, sys, io, html as htmllib

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

TODAY = "2026-05-02"
WEEK_LABEL = "2026-W18"
WEEK_START = "2026-04-26"
WEEK_END = "2026-05-02"
OUT_HTML = f"posts/{TODAY}-weekly.html"

snap = json.load(open("trends/2026-05-02.json", encoding="utf-8"))
prev_snap = json.load(open("trends/2026-04-25.json", encoding="utf-8"))
buckets = snap["buckets"]
prev_buckets = prev_snap["buckets"]

def esc(s): return htmllib.escape(s, quote=False)

CSS = """
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif;background:#f6f7f9;color:#1f2328;line-height:1.74;font-size:15px;padding:32px 16px;word-wrap:break-word;word-break:keep-all}
.container{max-width:920px;margin:0 auto;background:#fff;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.06),0 1px 2px rgba(0,0,0,.04);padding:36px 48px 56px}
h1{font-size:28px;margin:0 0 6px;font-weight:700;color:#0d1117;letter-spacing:-.01em}
h2{font-size:21px;margin:44px 0 14px;padding-bottom:8px;border-bottom:2px solid #e5e7eb;color:#0d1117;font-weight:700}
h3{font-size:17px;margin:24px 0 8px;color:#0d1117;font-weight:600}
h4{font-size:15px;margin:14px 0 6px;color:#0d1117;font-weight:600}
p{margin:0 0 14px}
a{color:#0969da;text-decoration:none}
a:hover{text-decoration:underline}
.subtitle{margin:0 0 22px;color:#656d76;font-size:14px}
.weekly-banner{background:linear-gradient(135deg,#fef3c7 0%,#fde68a 100%);border:1px solid #f59e0b;border-radius:10px;padding:16px 22px;margin:0 0 26px;font-size:14px;color:#78350f;line-height:1.65;font-weight:500}
.weekly-banner strong{color:#451a03}
.home-button{display:inline-block;padding:7px 14px;background:#f3f4f6;color:#374151;border:1px solid #d1d5db;border-radius:8px;font-size:13px;text-decoration:none;font-weight:500;margin:0 0 18px}
.home-button:hover{background:#e5e7eb;color:#0d1117;text-decoration:none}
.meta{font-size:13px;color:#3b434d;padding:14px 18px;background:#f6f8fa;border-left:3px solid #7c3aed;border-radius:6px;margin:14px 0 28px}
.meta div{margin:2px 0}
.exec-summary{background:#f0f9ff;border:1px solid #bae6fd;border-radius:10px;padding:18px 22px;margin:14px 0;font-size:15.5px;line-height:1.78;color:#0c4a6e}
.exec-summary strong{color:#0c4a6e}
.hot-cold-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:14px 0}
.hot-cold-grid .panel{padding:14px 18px;border-radius:8px;border:1px solid;font-size:14px}
.panel-hot{background:#fef2f2;border-color:#fecaca;color:#7f1d1d}
.panel-cold{background:#eff6ff;border-color:#bfdbfe;color:#1e3a8a}
.panel h4{margin-top:0;font-size:14px}
.panel ul{margin:6px 0;padding-left:22px}
.panel li{margin:4px 0;line-height:1.6}
.bucket-bar{display:flex;align-items:center;gap:8px;margin:6px 0;font-size:13.5px}
.bucket-bar .name{flex:0 0 120px;color:#475569;font-weight:500}
.bucket-bar .bar{flex:1;height:14px;background:#e0f2fe;border-radius:3px;overflow:hidden;position:relative}
.bucket-bar .fill{height:100%;background:linear-gradient(90deg,#0ea5e9 0%,#7c3aed 100%);border-radius:3px}
.bucket-bar .num{flex:0 0 60px;text-align:right;font-variant-numeric:tabular-nums;color:#1e293b;font-weight:500}
.bucket-bar .split{flex:0 0 130px;font-size:11.5px;color:#64748b;font-family:ui-monospace,monospace}
.bucket-bar .delta{flex:0 0 60px;text-align:right;font-size:11.5px;font-weight:600;font-family:ui-monospace,monospace}
.delta-up{color:#b91c1c}
.delta-down{color:#0369a1}
.top5-list{counter-reset:t5;padding:0;list-style:none;margin:14px 0}
.top5-list li{counter-increment:t5;padding:14px 16px;background:#fafbfc;border:1px solid #e5e7eb;border-radius:8px;margin:8px 0;position:relative;padding-left:50px}
.top5-list li::before{content:counter(t5);position:absolute;left:14px;top:14px;width:26px;height:26px;background:#0d1117;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px}
.top5-list .why{display:block;color:#475569;font-size:13.5px;margin-top:4px;line-height:1.6}
.deep-dive{background:#fef9c3;border:1px solid #fde047;border-radius:10px;padding:20px 24px;margin:14px 0}
.deep-dive h3{margin-top:0;color:#713f12}
.deep-dive .section-tag{font-weight:600;color:#854d0e;text-transform:uppercase;letter-spacing:0.04em;font-size:12px;margin-top:14px;margin-bottom:4px}
.deep-dive table{width:100%;border-collapse:collapse;font-size:13px;margin:8px 0}
.deep-dive th,.deep-dive td{border:1px solid #fde68a;padding:6px 10px;text-align:left}
.deep-dive th{background:#fef3c7}
.theme-card{background:#fafbfc;border:1px solid #e5e7eb;border-radius:8px;padding:16px 20px;margin:12px 0}
.theme-card h3{margin:0 0 6px}
.predict-card{background:#f3e8ff;border:1px solid #c4b5fd;border-radius:8px;padding:14px 18px;margin:10px 0}
.predict-card h4{margin:0 0 4px;color:#5b21b6}
.predict-card .why{font-size:13.5px;color:#4c1d95;line-height:1.65}
.score-card{background:#ecfdf5;border:1px solid #a7f3d0;border-radius:8px;padding:14px 18px;margin:10px 0}
.score-card.partial{background:#fef9c3;border-color:#fde047}
.score-card.miss{background:#fef2f2;border-color:#fecaca}
.score-card h4{margin:0 0 4px;color:#065f46}
.score-card.partial h4{color:#854d0e}
.score-card.miss h4{color:#991b1b}
.score-card .body{font-size:13.5px;line-height:1.65}
.note{background:#fff7ed;border:1px solid #fed7aa;border-radius:6px;padding:10px 14px;margin:10px 0;font-size:13px;color:#7c2d12}
.commentary{background:#f0fdf4;border:1px solid #bbf7d0;border-radius:10px;padding:18px 22px;margin:14px 0}
.commentary h3{margin-top:0;color:#14532d}
.commentary .step{margin:10px 0;padding:8px 0;border-top:1px dashed #86efac}
.commentary .step:first-of-type{border-top:none}
.commentary .step-label{font-weight:700;color:#15803d;font-size:13px;margin-right:6px}
.commentary.mini{background:#ecfdf5;padding:14px 18px}
.commentary.mini h3{font-size:15px}
.kw-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:10px 0}
.kw-panel{background:#fafbfc;border:1px solid #e5e7eb;border-radius:8px;padding:12px 16px}
.kw-panel h4{margin:0 0 6px;font-size:13.5px;color:#475569}
.kw-row{font-family:ui-monospace,monospace;font-size:12.5px;display:flex;justify-content:space-between;padding:2px 0;border-bottom:1px dotted #e5e7eb}
.kw-row:last-child{border-bottom:none}
.kw-name{color:#1f2937}
.kw-num{color:#64748b;font-weight:600}
hr{border:none;border-top:1px solid #e5e7eb;margin:36px 0}
.footer{margin-top:48px;padding-top:18px;border-top:1px solid #e5e7eb;color:#656d76;font-size:13px;line-height:1.7}
"""

def delta_pct(now, prev):
    if not prev: return None
    return int(round((now - prev) / prev * 100))

def bucket_bar(name, total, cv, ro, prev_total, max_total):
    pct = int(total / max_total * 100) if max_total else 0
    d = delta_pct(total, prev_total)
    if d is None:
        delta_html = '<span class="delta">—</span>'
    elif d > 0:
        delta_html = f'<span class="delta delta-up">+{d}%</span>'
    elif d < 0:
        delta_html = f'<span class="delta delta-down">{d}%</span>'
    else:
        delta_html = '<span class="delta">±0%</span>'
    return (f'<div class="bucket-bar"><span class="name">{esc(name)}</span>'
            f'<span class="bar"><span class="fill" style="width:{pct}%"></span></span>'
            f'<span class="num">{total}편</span>'
            f'<span class="split">CV {cv} / RO {ro}</span>'
            f'{delta_html}</div>')

parts = []
parts.append('<!DOCTYPE html>\n<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">')
parts.append(f'<title>arXiv Weekly Retrospective — {TODAY} ({WEEK_LABEL})</title>')
parts.append(f'<style>{CSS}</style></head><body><div class="container">')

parts.append('<a class="home-button" href="https://gisbi-kim.github.io/arxiv-daily-summary/">← 홈으로</a>')
parts.append('<h1>🗓 arXiv Weekly Retrospective</h1>')
parts.append(f'<p class="subtitle">{WEEK_LABEL} · {WEEK_START} ~ {WEEK_END} · cs.CV/cs.RO pastweek 누적 회고</p>')
parts.append('<div class="weekly-banner"><strong>토요일 주말판.</strong> arxiv가 안 도는 토요일이라 평일 단발 브리핑 대신 한 주 누적을 박사+교수급 시각으로 회고합니다. 상단은 30초 안에 끝나는 교수용 요약, 본문은 박사과정이 다음주 손 움직일 거리. 두 번째 weekly 발행이라 이번엔 <strong>지난주 W17 예측 채점</strong>도 같이 들어갑니다.</div>')
parts.append(f'<div class="meta"><div>📅 발행: {TODAY} (토)</div>'
             f'<div>📊 주간 시야: pastweek {snap["totals"]["total_scanned"]}편 스캔 · ROI {snap["totals"]["selected"]}편 선별</div>'
             f'<div>🗂 데이터: trends/insights/benchmarks {WEEK_START}~{WEEK_END} · 비교 기준 W17 (2026-04-19~04-25, 939편/429편)</div></div>')

# ============ ① Executive Summary ============
parts.append('<h2>🗓 ① Executive Summary <span style="font-size:13px;color:#656d76;font-weight:400">(교수용 30초)</span></h2>')
parts.append('''<div class="exec-summary">
이번주 가장 굵게 움직인 흐름은 <strong>VLA가 한 주 안에서 "분해 → 실행 → 추론"의 풀스택 paradigm shift를 동시에 그렸다</strong>는 점이에요. 월요일에 <a href="https://arxiv.org/abs/2604.23121">Breaking Lock-In</a>이 low-data post-training의 silent failure mode를 카탈로그화했고, 화·수에 <a href="https://arxiv.org/abs/2604.24921">Libra-VLA</a>·<a href="https://arxiv.org/abs/2604.25050">DiscreteRTC</a>·<a href="https://arxiv.org/abs/2604.24086">AsyncShield</a> 셋이 한 날 "async/dual-system/discrete diffusion"이라는 새 execution paradigm을 동시 점화. 그 위로 금요일 <a href="https://arxiv.org/abs/2604.28192">LaST-R1</a>이 latent CoT + LAPO로 LIBERO 99.8% — 거의 ceiling을 찍으면서 reasoning paradigm까지 한 단계 위로 옮겼어요. 지난주 W17이 "VLA 진단 페이즈 진입"이었다면 이번주 W18은 그 진단 위에서 "어떻게 다르게 실행하고 추론할 것인가"가 community의 다음 layer가 됐다는 뜻.
두 번째로 굵은 흐름은 <strong>World Model이 "asset" 너머 "evaluation substrate"가 됐다</strong>는 점입니다. <a href="https://arxiv.org/abs/2604.22152">dWorldEval</a>(discrete diffusion WM이 policy eval surrogate), <a href="https://arxiv.org/abs/2604.28196">HERMES++</a>(driving WM이 understanding+generation 통합), <a href="https://arxiv.org/abs/2604.28185">Visual Generation in the New Era</a>(5-level taxonomy) — 한 주 안에서 WM이 perception/generation/policy/eval 4 layer를 동시에 substrate로 점령. CV는 평가·생성, RO는 학습 환경으로 같은 단어가 정반대 layer에 활용되는 분기가 더 분명해졌어요.
가장 의외인 건 <strong>버킷 8개 중 7개가 W17 대비 감속</strong>이라는 점이에요. 전체 ROI 선별은 429→315편 (-27%). Embodied AI -52%, FM -44%, Generation -33%로 큰 폭 cooling — 단 Autonomous Driving만 22→28 (<span class="delta-up">+27%</span>) 단독 surge. 표면적으로는 community fatigue 같지만 실제로는 "단발 SOTA 카운트가 줄고 굵은 paradigm 결로 응축되는" 신호로 읽혀요. AD가 단독 riser인 건 LLM-driving·driving WM·V2V·CARLA closed-loop 4 axis가 한 주 안에서 동시에 누적된 결과로, 다음 1–2주 AD가 community 무게중심을 잡을 가능성 큼.
</div>''')

# ============ ② Hot vs Cold ============
parts.append('<h2>⚖️ ② Hot vs Cold <span style="font-size:13px;color:#656d76;font-weight:400">(W17 → W18)</span></h2>')
ordered = sorted([(n, d["total"], d["cv"], d["ro"], prev_buckets.get(n, {}).get("total", 0))
                  for n, d in buckets.items()], key=lambda x: -x[1])
max_total = ordered[0][1]
parts.append('<div style="margin:14px 0">')
for name, total, cv, ro, prev_total in ordered:
    parts.append(bucket_bar(name, total, cv, ro, prev_total, max_total))
parts.append('</div>')

parts.append('''<div class="hot-cold-grid">
<div class="panel panel-hot"><h4>⬆ 가속 / 단독 riser</h4>
<ul>
<li><strong>Autonomous Driving 22→28편 (+27%)</strong> — 8개 버킷 중 유일한 surge. <a href="https://arxiv.org/abs/2604.28196">HERMES++</a>(driving WM 통합)·<a href="https://arxiv.org/abs/2604.27366">Judge Then Drive</a>(critic-VLA)·<a href="https://arxiv.org/abs/2604.25329">ProDrive</a>(proactive planning)·<a href="https://arxiv.org/abs/2604.27994">Dreaming Across Towns</a>(closed-loop CARLA) 4 axis 동시 누적. AD가 "world model + LLM-driving + V2V + CARLA"를 한 묶음으로 가속.</li>
<li><strong>Robot Learning 안에서 VLA execution paradigm</strong> — 총량은 67→51편(-24%)으로 줄었지만, <a href="https://arxiv.org/abs/2604.24921">Libra-VLA</a>·<a href="https://arxiv.org/abs/2604.25050">DiscreteRTC</a>·<a href="https://arxiv.org/abs/2604.24086">AsyncShield</a>·<a href="https://arxiv.org/abs/2604.28192">LaST-R1</a>·<a href="https://arxiv.org/abs/2604.23121">Breaking Lock-In</a>·<a href="https://arxiv.org/abs/2604.23775">VLA Safety Survey</a> 등 굵은 paradigm 결로 응축. "단발 알고리즘은 줄고 paradigm 결이 증가"의 가장 분명한 사례.</li>
<li><strong>3DGS sparse-view robustness 미니클러스터</strong> — 한 주 후반 4편(<a href="https://arxiv.org/abs/2604.27106">RecGen</a>·<a href="https://arxiv.org/abs/2604.27422">in the Wild</a>·<a href="https://arxiv.org/abs/2604.27552">Residual GS for CBCT</a>·<a href="https://arxiv.org/abs/2604.28193">Generalizable Sparse-View</a>) 동시 등장. 3D/Scene 총량은 -8%로 정체지만 안에서 focus가 "production cost → sparse data robustness"로 명확히 이동.</li>
</ul></div>
<div class="panel panel-cold"><h4>⬇ 감속 / 큰 폭 cooling</h4>
<ul>
<li><strong>Embodied AI 27→13편 (-52%)</strong> — 가장 큰 폭. VLN·ObjectNav 단발 결이 거의 사라지고 RL 버킷의 long-horizon manipulation으로 흡수되는 모양새. 명시적 navigation 결만 보면 community focus가 "navigation 자체"에서 "navigation as substrate for VLA"로 넘어가는 신호.</li>
<li><strong>Foundation Models 68→38편 (-44%)</strong> — VLM hallucination·reasoning 결의 단발 카운트가 거의 반토막. 단, 안에서 결이 "평가 calibration" → "epistemic honesty"로 한 단계 위. <a href="https://arxiv.org/abs/2604.26288">CheXthought</a>·<a href="https://arxiv.org/abs/2604.26250">Beyond Shortcuts</a>·<a href="https://arxiv.org/abs/2604.25102">VLM Failure Modes</a> 류 굵은 결만 살아남음.</li>
<li><strong>Generation 93→62편 (-33%)</strong> — diffusion 단발 결의 community fatigue. 단, <a href="https://arxiv.org/abs/2604.28185">Visual Generation in the New Era</a> 같은 종합 position paper와 video WM + policy 결합 결로 응축. "다음 단계는 spatial reasoning + persistent state"라는 메시지 정착.</li>
<li><strong>Safety/Alignment 50→37편 (-26%)</strong> — W17의 단발 cluster가 정리되고 <a href="https://arxiv.org/abs/2604.23775">VLA Safety Survey</a>·<a href="https://arxiv.org/abs/2604.27267">Prompt to Physical Actuation</a> 같은 architectural 결로 응축. Hierarchical safety 결은 안 줄고 단발 robustness만 줄어든 모양새.</li>
</ul></div>
</div>''')

parts.append('''<p style="font-size:14px;color:#475569;margin-top:14px">한 줄 해석: <strong>"단발 카운트는 줄고 paradigm 결이 굵어졌다"</strong>는 게 W17→W18의 본질이에요. 8개 버킷 중 7개 감속이지만 안에서는 VLA·WM·AD·3DGS 4축 모두 \'정점 결\'이 한 주에 한꺼번에 등장. 표면 데이터는 cooling이지만 실제 community 무게중심은 "더 응축되고 더 굵은" 형태로 이동한 한 주.</p>''')

# ============ ② keyword grids ============
parts.append('<h3>📐 키워드 분포 (CV vs RO)</h3>')
parts.append('<div class="kw-grid">')
parts.append('<div class="kw-panel"><h4>CV top 10</h4>')
for kw, n in snap["keywords_cv"][:10]:
    parts.append(f'<div class="kw-row"><span class="kw-name">{esc(kw)}</span><span class="kw-num">{n}</span></div>')
parts.append('</div>')
parts.append('<div class="kw-panel"><h4>RO top 10</h4>')
for kw, n in snap["keywords_ro"][:10]:
    parts.append(f'<div class="kw-row"><span class="kw-name">{esc(kw)}</span><span class="kw-num">{n}</span></div>')
parts.append('</div>')
parts.append('</div>')
parts.append('<p style="font-size:13.5px;color:#475569"><strong>읽는 법:</strong> CV는 diffusion(34)·robust(27)·splatting(15+15)·VLM(13+13)이 head 4. <em>splatting/3DGS</em>가 W17 19→15로 줄어든 게 아니라 안에서 "sparse-view + 응용"으로 응축된 결. RO는 manipulation(13)·vehicle(12)·navigation(9)·VLA(7+7)·tactile(6) — vehicle이 RO 키워드 head 2위로 올라온 게 AD surge의 RO 측 evidence. tactile(6)이 정착한 게 새로운 변화.</p>')

# ============ ③ Top 5 ============
parts.append('<h2>🔥 ③ 주간 Top 5</h2>')
top5 = [
    ("LaST-R1: Reinforcing Action via Adaptive Physical Latent Reasoning for VLA Models",
     "https://arxiv.org/abs/2604.28192", "CV/RO",
     "VLA reasoning paradigm shift의 결정타. Latent CoT + LAPO(Latent-to-Action Policy Optimization)으로 LIBERO 99.8% — 거의 ceiling, 실 환경 4 task에서 +44%. \"linguistic CoT\" → \"physical latent reasoning + RL\"의 첫 fully-realized 결로, 다음 분기 VLA reasoning 라인의 baseline."),
    ("Vision-Language-Action Safety: Threats, Challenges, Evaluations, and Mechanisms",
     "https://arxiv.org/abs/2604.23775", "RO",
     "VLA safety가 한 편의 통합 survey로 정리된 시점. RedVLA(2604.22591) 같은 physical red-teaming 결과 LLM threat modeling(2604.27267)이 한 주에 동시에 떨어진 흐름의 종합. 다음 6개월 \"VLA + safety head\" 디폴트 컴포넌트화의 reference paper."),
    ("HERMES++: Toward a Unified Driving World Model for 3D Scene Understanding and Generation",
     "https://arxiv.org/abs/2604.28196", "CV",
     "Driving WM이 future scene generation에 치우쳤던 한계를 BEV-LLM + Joint Geometric Optimization으로 두 task를 한 모델로 푸는 framing. AD 단독 surge(+27%)의 정점 결로, 다음 분기 \"driving WM = 평가 + 생성 통합\"의 baseline."),
    ("Libra-VLA: Achieving Learning Equilibrium via Asynchronous Coarse-to-Fine Dual-System",
     "https://arxiv.org/abs/2604.24921", "CV/RO",
     "VLA execution paradigm의 \"async + dual-system\" 결의 정점. DiscreteRTC(2604.25050)·AsyncShield(2604.24086)와 한 날 cluster — \"무엇을 학습할 것인가\" 다음으로 \"어떻게 실행할 것인가\"가 community 새 layer. real-time hardware audit의 substrate."),
    ("dWorldEval: Scalable Robotic Policy Evaluation via Discrete Diffusion World Model",
     "https://arxiv.org/abs/2604.22152", "RO",
     "World Model이 처음으로 \"평가 surrogate\"로 명시 활용된 결. 기존 VLA eval은 sim/real rollout 비용이 컸는데, dWorldEval은 discrete diffusion WM으로 policy 성능을 surrogate로 평가. 다음 분기 evaluation infrastructure 라인의 변곡점 — \"WM = asset → environment → evaluator\" 3단계 진화의 마지막 layer."),
]
parts.append('<ol class="top5-list">')
for title, url, badge, why in top5:
    parts.append(f'<li><a href="{url}" target="_blank"><strong>{esc(title)}</strong></a> <span style="font-size:11px;font-weight:600;padding:1px 7px;border-radius:10px;background:#fff8c5;color:#7a4e00;border:1px solid #d4a72c;margin-left:6px">{badge}</span><span class="why">{esc(why)}</span></li>')
parts.append('</ol>')

# ============ ④ Deep-dive ============
parts.append('<h2>🌟 ④ Deep-dive — VLA Execution Paradigm: 한 날 3편이 만든 변곡점</h2>')
parts.append('''<div class="deep-dive">
<h3><a href="https://arxiv.org/abs/2604.24921" target="_blank">Libra-VLA</a> + <a href="https://arxiv.org/abs/2604.25050" target="_blank">DiscreteRTC</a> + <a href="https://arxiv.org/abs/2604.24086" target="_blank">AsyncShield</a> (2026-04-29)</h3>
<p style="color:#713f12;font-size:13.5px"><em>이 셋을 한 묶음으로 고른 이유: VLA가 W17의 "분해/진단" 단계를 지나 "어떻게 실행할 것인가"라는 새 paradigm layer를 한 날 동시에 점화한 결정적 신호이기 때문. 셋이 같은 문제(긴 추론과 빠른 액션을 한 시스템에 엮기)를 서로 다른 메커니즘으로 풀고 있어, 다음 분기 VLA execution 라인의 분기를 그대로 보여줍니다.</em></p>

<div class="section-tag">공통 문제 정의</div>
<p>기존 VLA는 "한 step에 reasoning + action을 동시에"라는 동기식 구조라, reasoning 길이가 늘면 control loop hz가 떨어지고, control hz를 맞추면 reasoning depth를 희생해야 했어요. LIBERO 같은 짧은 horizon에서는 안 보이지만, 실세계 manipulation·navigation의 long-horizon에서는 이게 병목. 셋 다 이 \"reasoning ↔ action 동기화의 hardware-level 비효율\"을 정조준합니다.</p>

<div class="section-tag">세 가지 해법 비교</div>
<table>
<tr><th>접근</th><th>핵심 아이디어</th><th>장점</th><th>약점</th></tr>
<tr><td><strong>Libra-VLA</strong></td><td>Coarse-to-fine 두 system을 비동기로 실행 — coarse가 high-level intent, fine이 fast control. \"Learning Equilibrium\"이라 불리는 두 system 간 균형을 학습으로 잡음.</td><td>System 1/2의 이론적 framing이 깔끔, generality.</td><td>두 system 간 sync overhead가 결국 새 bottleneck. real-time profile 부족.</td></tr>
<tr><td><strong>DiscreteRTC</strong></td><td>Discrete diffusion policy를 \"natural async executor\"로 framing — token decoding 자체가 비동기 가능하다는 구조적 이점 활용.</td><td>Discrete diffusion 자체의 LLM tokenizer 친화성을 그대로 가져옴. 추가 system 분리 없이 paradigm 자체에 비동기 내장.</td><td>Continuous action space에서 quantization loss가 fine motor에서 여전히 문제. high-precision manipulation에선 약점.</td></tr>
<tr><td><strong>AsyncShield</strong></td><td>Cloud-based VLA에 plug-in edge adapter — 실 환경 배포 측 architectural shim. cloud에서 reasoning, edge에서 action.</td><td>Deployment-first framing. 기존 VLA를 그대로 두고 적용 가능.</td><td>Network latency 측 결로 algorithmic novelty는 낮음. 실용적 가치는 높음.</td></tr>
</table>

<div class="section-tag">왜 한 날에 동시에 등장했나</div>
<p>이건 우연이 아니에요. W17의 mechanistic 분해(How VLAs Really Work)가 \"action decoder는 robust한데 V-L 정렬이 병목\"이라는 결론을 깔았고, 4월 둘째 주에 등장한 <a href="https://arxiv.org/abs/2604.21391">Residual Bridge</a>·<a href="https://arxiv.org/abs/2604.21192">VLA Foundry</a>가 \"통합 학습 스택\" 결로 인프라를 깔았어요. 그 위에 \"이제 reasoning을 어떻게 실행할 것인가\"라는 다음 layer 질문이 자연스럽게 올라온 시점. 셋이 한 날 떨어진 건 community의 collective realization 신호로 봐야 합니다.</p>

<div class="section-tag">독자 관점 의심 지점</div>
<p>(1) 셋 모두 \"async가 답\"이라는 가정을 공유하는데, 진짜로 그런가? CALVIN·LIBERO 같은 표준 벤치는 short-horizon이라 async의 이점이 거의 안 잡혀요. real-world long-horizon에서 async profile이 정량 검증된 결은 아직 없어, \"이론적으로 좋아 보이지만 실측 부재\"의 위험. (2) Discrete diffusion이 fine motor에서 quantization loss로 여전히 막힐 가능성. dexterous manipulation에 적용해보면 이 약점이 6개월 안에 돌발적으로 표면화할 듯. (3) Libra-VLA의 \"Learning Equilibrium\" framing이 두 system 사이 trade-off를 학습으로 자동 잡는다는 주장인데, 이게 실제로 일반화하는지(다른 task에서도 같은 균형이 잡히는지) ablation이 좁아요.</p>

<div class="section-tag">우리 분야 영향</div>
<p>다음 분기에 VLA paper baseline에 \"sync vs async execution\" 비교 칸이 추가될 가능성 높음. 우리 랩이 VLA를 손댄다면 (a) 평가 hardware spec(control hz, latency)을 결과 표에 명시하는 게 새 표준이 될 것, (b) discrete vs continuous action representation 둘 다 baseline으로 갖춰야 reviewer 방어 가능. 그리고 LaST-R1이 latent CoT로 reasoning 깊이를 늘렸다는 점에서, 다음 분기 cluster는 \"latent reasoning + async execution\"의 결합 결로 모일 것 같습니다.</p>
</div>''')

# ============ ⑤ Themes ============
parts.append('<h2>🧭 ⑤ 주간 테마 4개 (메타 흐름)</h2>')
themes = [
    ("VLA paradigm의 풀스택 shift — 한 주 안에 분해·실행·추론·안전 4 layer 동시 점화",
     "월요일 Breaking Lock-In(저data post-training failure mode 카탈로그) → 화 KinDER(physical reasoning bench) → 수 Libra-VLA·DiscreteRTC·AsyncShield(execution paradigm) → 목 X-WAM·STARRY·World2VLM(world model substrate) → 금 LaST-R1(reasoning paradigm)·VLA Safety Survey(safety 통합) → 토 LLM-Robot Threat Modeling(architectural risk). 한 주 동안 VLA가 \"진단 → 실행 → 추론 → 안전\" 4 layer를 모두 새 paradigm으로 갈아치웠어요. W17의 \"진단 페이즈 진입\" 다음으로 W18은 \"진단된 약점들을 어떻게 다르게 풀 것인가\"의 paradigm proliferation 단계."),
    ("World Model이 \"asset → environment → evaluator\" 3단계 진화 완성",
     "dWorldEval(2604.22152)이 \"WM을 policy eval surrogate로 사용\"이라는 마지막 layer를 점화하면서, World Model의 community 활용 범위가 \"3D 표현 asset(2024) → RL training environment(2025 H1) → evaluation substrate(2026 W18)\"의 3단계 stepwise 진화를 완성. HERMES++가 driving WM을 \"understanding + generation\" 통합으로, Visual Generation in the New Era가 \"5-level taxonomy\"로 framing 정리. 다음 분기는 \"WM 평가의 calibration\"(dWorldEval surrogate가 real eval과 얼마나 align되나)이 새 evaluation infra 라인이 될 것."),
    ("Autonomous Driving이 community 단독 riser — LLM-driving · driving WM · V2V · CARLA closed-loop 4축 동시",
     "AD 22→28편(+27%)은 8개 버킷 중 유일한 surge. HERMES++(WM)·Judge Then Drive(critic-VLA)·ProDrive(proactive planning)·Dreaming Across Towns(closed-loop CARLA)·SwarmDrive(V2V)·Large LLM Decision-Making 등 한 주 안에서 4 axis 동시 누적. W17이 \"AD가 vertical foundation 흐름과 모순적으로 얇음\"이었다면 W18에서 정확히 그 공백이 메워진 모양. 다음 1–2주 AD가 community 무게중심을 잡을 가능성 매우 큼."),
    ("LLM-controlled Robot의 architectural threat surface가 처음으로 통합 분석",
     "<a href=\"https://arxiv.org/abs/2604.27267\">From Prompt to Physical Actuation</a>이 STRIDE-per-interaction을 LLM-enabled robot의 6 boundary point에 적용해 \"prompt → unsafe physical actuation\" cross-boundary attack chain 3가지를 trace. 같은 주에 RedVLA(physical red-teaming) + VLA Safety Survey(통합 정리)가 떨어진 흐름의 정점. 어제까지 \"sample 단위\" risk였던 게 \"architecture 단위\" risk로 한 단계 위. 우리 랩이 LLM-as-controller 라인이 있다면 boundary diagram + STRIDE audit이 즉시 first follow-up."),
]
for title, body in themes:
    parts.append(f'<div class="theme-card"><h3>{esc(title)}</h3><p>{body}</p></div>')

# ============ ⑥ W17 prediction grading ============
parts.append('<h2>🪞 ⑥ W17 예측 채점 <span style="font-size:13px;color:#656d76;font-weight:400">(2주 회고 = W17 → W18)</span></h2>')
parts.append('<p style="font-size:13.5px;color:#475569">지난주 토요일 회고에서 던진 3개 예측을 W18 실제 흐름과 매칭해 채점합니다.</p>')

scores = [
    ("hit", "✅ 적중", "VLA 회로 분해 follow-up이 다음주에만 3편+ 떨어진다",
     "결과적으로 3편을 훨씬 넘었어요. <a href=\"https://arxiv.org/abs/2604.23121\">Breaking Lock-In</a>(post-training failure)·<a href=\"https://arxiv.org/abs/2604.25788\">KinDER</a>(physical reasoning bench)·<a href=\"https://arxiv.org/abs/2604.24921\">Libra-VLA</a>(execution paradigm)·<a href=\"https://arxiv.org/abs/2604.28192\">LaST-R1</a>(reasoning paradigm)·<a href=\"https://arxiv.org/abs/2604.23775\">VLA Safety Survey</a>·<a href=\"https://arxiv.org/abs/2604.22591\">RedVLA</a> — 적어도 6편이 W17의 \"How VLAs Really Work\" 분해 위에서 follow-up 결로 등장. 예측이 fluke가 아니라 community trend였다는 증거."),
    ("partial", "◐ 부분적중", "Open-H-Embodiment 패턴을 따라 산업·조립 vertical 데이터셋이 1편 이상 등장",
     "산업·조립 측 vertical dataset 결은 W18에 명확히는 안 나타났어요. 단, 의료 측 결은 <a href=\"https://arxiv.org/abs/2604.26288\">CheXthought</a>·<a href=\"https://arxiv.org/abs/2604.22156\">Sum-of-Checks Surgical Safety</a> 등 계속 누적. \"vertical foundation dataset\" 흐름이 의료에 한정돼 stuck — 의료 외 도메인(industrial assembly, lab automation)으로 확산은 아직. 4주 회고에서 다시 채점 가치 있음."),
    ("hit", "✅ 적중", "Generation 버킷에서 video world model + policy 결합 논문이 5편 이상",
     "총량으로는 Generation 버킷이 -33%로 줄었지만, video WM + policy 결합 결만 보면 <a href=\"https://arxiv.org/abs/2604.26848\">STARRY</a>·<a href=\"https://arxiv.org/abs/2604.27792\">MotuBrain</a>·<a href=\"https://arxiv.org/abs/2604.26934\">World2VLM</a>·<a href=\"https://arxiv.org/abs/2604.26182\">Lifting Embodied World Models</a>·<a href=\"https://arxiv.org/abs/2604.28196\">HERMES++</a>·<a href=\"https://arxiv.org/abs/2604.22152\">dWorldEval</a> 6편 이상. 예측대로 \"단독 video gen은 줄고 policy 결합 결이 늘어남\"이 그대로 실현. World Model이 substrate가 됐다는 더 큰 메타 흐름 안에서 자연스러운 결과."),
]
for cls, label, title, body in scores:
    parts.append(f'<div class="score-card {cls}"><h4>{label} — {esc(title)}</h4><div class="body">{body}</div></div>')

parts.append('<p style="font-size:13px;color:#475569;margin-top:14px"><strong>채점 요약:</strong> 3개 중 2 적중 + 1 부분적중. 적중 2개(VLA follow-up · video WM + policy)는 \"방향성 + 카운트\" 모두 맞췄고, 부분적중은 vertical dataset 흐름이 의료에 한정돼 확산이 더딘 모양. 전체적으로 W17 회고가 community trend를 잘 catch한 셈 — 다음주부터 4주 전 회고도 활성화 예정.</p>')

# ============ ⑦ Trend commentary ============
parts.append('<h2>🎓 ⑦ 트렌드 해설 (박사+교수급 시각)</h2>')
parts.append('<p style="font-size:13.5px;color:#475569"><em>특정 논문 줄거리가 아니라 흐름을 historical context와 함께 해석합니다.</em></p>')

parts.append('''<div class="commentary">
<h3>🧠 메인 — \"Latent Reasoning\"이 VLA의 새 표준 layer로 자리잡는 이유</h3>

<div class="step"><span class="step-label">🔍 무엇이 부상했나</span>
이번주 가장 굵게 움직인 paradigm 결은 <strong>VLA가 explicit linguistic CoT(Chain-of-Thought)에서 latent CoT로 옮겨가는 흐름</strong>입니다. <a href="https://arxiv.org/abs/2604.28192">LaST-R1</a>이 LIBERO 99.8% + 실 환경 +44%로 정점을 찍었고, <a href="https://arxiv.org/abs/2604.27472">PRTS</a>가 같은 axis에서 contrastive primitive reasoning으로 우회. 그리고 W18 초반에 등장한 <a href="https://arxiv.org/abs/2604.25299">The Thinking Pixel</a>(multimodal diffusion latents에서 recursive sparse reasoning)·<a href="https://arxiv.org/abs/2604.24339">See Further, Think Deeper</a>가 같은 \"latent space에서 추론\"을 다른 modality로 확장.</div>

<div class="step"><span class="step-label">🧠 그게 뭔지</span>
Linguistic CoT는 \"step 1: 객체 인식 → step 2: 그립 위치 계산 → step 3: 액션\"처럼 자연어로 추론을 풀어내는 방식인데, 이건 LLM에서 잘 동작하는 패턴이지만 robotics에서는 (a) 자연어 token 비용이 크고 (b) physical 세계의 continuous한 reasoning(예: \"이만큼 더 위로\")이 token으로 표현이 어색하다는 약점이 있어요. Latent CoT는 자연어 token 대신 latent vector 시퀀스에서 reasoning을 굴려, physical reasoning에 더 fit한 representation을 사용. 2024년 Coconut(Continuous CoT)·2025년 latent reasoning LLM 결의 \"text-to-latent\" 흐름이 1년 시차로 robotics에 도착한 셈.</div>

<div class="step"><span class="step-label">⚙️ 왜 지금</span>
세 가지 trigger가 한 시점에 정렬됐어요. (1) W17의 mechanistic 분해(How VLAs Really Work)가 \"V-L 정렬이 병목, action decoder는 robust\"라고 진단을 낸 게 \"reasoning을 V-L 정렬 단에서 강화하면 된다\"는 명확한 leverage point를 제공. (2) latent reasoning LLM 결(Coconut, COCOMix 등)이 2025년 표준 라인이 된 게 \"latent space reasoning\"의 community 친숙도를 높였어요. (3) RL이 다시 robotics 표준 wrapper(Group Relative Policy Optimization, LAPO 같은 변형)로 자리잡은 게 \"latent reasoning + RL\"의 결합을 자연스럽게 만들었습니다. LaST-R1이 LAPO를 명시적으로 제시한 게 결정적.</div>

<div class="step"><span class="step-label">🪞 재포장인가, 새로운가</span>
솔직히 말하면 <strong>절반은 재포장, 절반은 진짜 새로움</strong>입니다. \"latent reasoning\" 자체는 2017년 Differentiable Neural Computer, 2018년 Memory-Augmented NN까지 거슬러 올라가요. 2024 Coconut이 LLM에서 부활. 새로운 건 (a) RL과의 결합 framing(LAPO처럼 latent reasoning을 policy gradient로 직접 최적화), (b) physical task의 continuous nature와 latent space의 representation이 \"자연 fit\"이라는 community realization. 후자는 진짜로 새 insight고 6개월 안에 \"VLA = latent reasoning + RL\"이 default formulation으로 굳을 가능성 70%.</div>

<div class="step"><span class="step-label">🔭 6–12개월 뒤</span>
12개월 안에 두 가지 분기 예상. 첫째, \"latent reasoning depth ↔ control hz\" trade-off에 대한 새 hardware/architecture 결이 쏟아질 것. 이번주 async execution paradigm(Libra-VLA·DiscreteRTC) 셋이 그 분기의 첫 결. 둘째, \"latent reasoning이 진짜 reasoning인가, 아니면 단순 representation refinement인가\"에 대한 mechanistic interpretability 결이 도착할 것 — Anthropic의 mechanistic line이 LLM에서 했던 것과 동일한 패턴이 robotics latent space로 옮겨오는 시기. 어디서 막히냐면, latent reasoning의 \"interpretability\"가 결정적 약점 — debug 어려움이 production deployment의 silent killer가 될 가능성이 큽니다.</div>

<div class="step"><span class="step-label">🎯 우리 분야 시사점</span>
교수 시점에선 박사과정 토픽 배정에서 \"latent CoT\" + \"async execution\" + \"RL with latent action\" 이 셋의 교집합을 다음 6개월 핵심 분기로 잡아야 한다는 뜻. 박사과정 시점에선 baseline 표에 \"explicit CoT vs latent CoT vs no CoT\"를 의무 ablation으로 넣는 게 최소 방어선. 그리고 우리 랩이 manipulation 측에서 굴린다면 \"latent reasoning이 fine motor에서 진짜로 도움이 되는가\" — 이게 다음 6개월의 가장 informative한 질문. LIBERO에서 99.8% 찍은 LaST-R1이 dexterous manipulation에서도 같은 차이를 만드는지가 community의 다음 reality check.</div>
</div>''')

# Side mini 1
parts.append('''<div class="commentary mini">
<h3>📎 사이드 — Discrete Diffusion이 \"async execution + LLM tokenizer 친화\" 두 마리 토끼를 잡는 자리</h3>
<div class="step"><span class="step-label">🔍 관찰</span>
이번주 <a href="https://arxiv.org/abs/2604.25050">DiscreteRTC</a>가 \"discrete diffusion이 자연 async executor\"라는 framing을 명시적으로 제시했고, <a href="https://arxiv.org/abs/2604.22152">dWorldEval</a>이 같은 discrete diffusion 구조로 policy eval surrogate를 만들었어요. W17 회고에서 메인 토픽으로 잡았던 \"discrete diffusion action decoding의 부상\" 흐름이 W18에서 정확히 한 단계 더 진행.</div>
<div class="step"><span class="step-label">⚙️ 왜 지금</span>
두 차원에서 동시에 친화성이 좋아요. (1) LLM tokenizer와 같은 discrete vocabulary를 공유하므로 VLM head를 그대로 action head로 재사용 가능. (2) Token-level decoding이 본질적으로 부분적/비동기 가능하니 control loop hz를 reasoning depth와 분리 가능. continuous policy는 두 측면 모두에서 약했어요.</div>
<div class="step"><span class="step-label">🔭 전망</span>
6개월 안에 \"discrete diffusion = navigation/long-horizon manipulation의 default\", \"continuous = fine motor·dexterous의 default\"로 분기가 굳을 것. 두 representation의 hybrid (high-level discrete + low-level continuous residual) 결이 다음 분기의 새 결.</div>
</div>''')

# Side mini 2
parts.append('''<div class="commentary mini">
<h3>📎 사이드 — AD가 단독 surge한 이유: \"general VLA 모델\"의 첫 vertical 흡수처</h3>
<div class="step"><span class="step-label">🔍 관찰</span>
AD가 22→28편(+27%) 단독 riser. 안에서 보면 <a href="https://arxiv.org/abs/2604.27366">Judge Then Drive</a>(critic-VLA)·<a href="https://arxiv.org/abs/2604.23513">Large LLM Decision-Making for AD</a>·<a href="https://arxiv.org/abs/2604.28196">HERMES++</a>(driving WM) — 모두 \"general VLA/LLM/WM 모델을 driving 도메인에 흡수\" 패턴.</div>
<div class="step"><span class="step-label">⚙️ 왜 지금</span>
W17에서 \"general VLA가 진단 페이즈\"였는데, 진단된 모델이 첫 vertical로 흡수되는 자연스러운 다음 단계가 driving이에요. 의료(W17 Open-H-Embodiment)는 데이터셋부터 시작했지만, AD는 이미 nuScenes/Waymo/CARLA로 인프라가 갖춰져 있어 \"VLA만 가져오면 즉시 적용 가능\". community가 가장 낮은 friction의 vertical을 먼저 친 결.</div>
<div class="step"><span class="step-label">🔭 전망</span>
다음 1–2주 AD에서 \"VLA + driving WM + closed-loop CARLA\"의 3-stack 결이 더 누적될 것. 단, 실 도로 측 결은 안전·인증 issue로 단발 paper로 가기 어렵고 이게 AD가 결국 vertical foundation paper의 \"중간 layer\"에 머물 한계.</div>
</div>''')

# ============ ⑧ Predictions for next week ============
parts.append('<h2>🔮 ⑧ 다음주(W19) 예측</h2>')
predictions = [
    ("Latent CoT VLA follow-up이 W19에 4편 이상 (LIBERO 외 다른 벤치 검증 포함)",
     "LaST-R1이 LIBERO 99.8% 찍은 게 너무 굵어서 community가 다른 벤치(CALVIN/RoboCasa/RLBench)에서 같은 분해를 검증하려 들 것. 안 나오면 LaST-R1이 LIBERO-overfitting의 결로 평가절하될 risk."),
    ("Async execution paradigm을 비교한 \"sync vs async hardware-profile\" 측 ablation paper가 1편 이상 등장",
     "이번주 Libra-VLA·DiscreteRTC·AsyncShield 셋이 한 날 떨어졌는데, 정작 \"sync 대비 async가 진짜 유리한가\"의 정량 비교 결은 아직 없음. 누군가 6주 안에 ablation 결을 내놓을 가능성 매우 큼. 안 나오면 async paradigm이 fluke 위험."),
    ("dWorldEval의 calibration(WM eval과 real eval의 align)을 정조준한 후속 논문이 2편 이상",
     "WM이 eval substrate가 된 건 좋은데, 그 substrate가 real eval과 얼마나 align되는지가 다음 community의 자연스러운 검증 질문. 안 나오면 WM-as-evaluator 흐름이 적용 단계에서 막힐 것."),
    ("AD에서 \"driving WM + LLM-driving\" 결합 결이 W19에 3편 이상",
     "이번주 HERMES++(WM 통합) + Judge Then Drive(critic-VLA) + ProDrive(proactive)가 따로 떨어졌는데, 다음주에 셋의 결합 결이 자연스럽게 등장할 것. 안 나오면 AD surge가 한 주짜리 burst로 그칠 risk."),
]
for title, why in predictions:
    parts.append(f'<div class="predict-card"><h4>🔮 {esc(title)}</h4><p class="why">{esc(why)}</p></div>')

# ============ ⑨ Audio note ============
parts.append('<h2>🎧 ⑨ 주간 오디오</h2>')
parts.append('<div class="note">🛠 이번주는 TTS 파이프라인이 이 환경에서 미연결이라 mp3 생성을 건너뜁니다. 다음 주말판부터 정상 발행 예정.</div>')

# ============ Footer ============
parts.append('<hr>')
parts.append('<a class="home-button" href="https://gisbi-kim.github.io/arxiv-daily-summary/">🏠 전체 목록으로</a>')
parts.append(f'''<div class="footer">
<p>📚 입력: cs.CV/cs.RO pastweek {snap["totals"]["total_scanned"]}편 스캔 · ROI {snap["totals"]["selected"]}편 분류 · trends/insights/benchmarks {WEEK_START}~{WEEK_END} 누적 + W17(2026-04-19~04-25) 비교 기준</p>
<p>🛠 생성 파이프라인: <code>scripts/build_weekly.py</code> + <code>scripts/gen_weekly_html_20260502.py</code> · arxiv 리스트는 stdlib 파서 직접 파싱(WebFetch 미사용)</p>
<p>📝 톤·구조: arxiv-daily-summary 주말 모드(Weekly Retrospective) — W17 후속, W17 예측 채점 추가</p>
<p>📡 RSS 구독: <a href="https://gisbi-kim.github.io/arxiv-daily-summary/feed.xml">/feed.xml</a></p>
</div>''')

parts.append('</div></body></html>')

html_doc = "\n".join(parts)
os.makedirs("posts", exist_ok=True)
with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_doc)
print(f"WROTE {OUT_HTML} ({len(html_doc)} bytes)")
