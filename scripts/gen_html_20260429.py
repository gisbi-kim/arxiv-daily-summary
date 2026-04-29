#!/usr/bin/env python3
"""Generate posts/2026-04-29.html from out/classified.json + out/summaries.py"""
import json, html, io, os, sys

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

sys.path.insert(0, "out")
from summaries import SUMMARIES

DATE = "2026-04-29"
WEEKDAY = "수"
OUT = f"posts/{DATE}.html"

CSS = """*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif;background:#f6f7f9;color:#1f2328;line-height:1.72;font-size:15px;padding:32px 16px;word-wrap:break-word;word-break:keep-all}
.container{max-width:860px;margin:0 auto;background:#fff;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.06),0 1px 2px rgba(0,0,0,.04);padding:40px 48px}
h1{font-size:28px;margin:0 0 6px;font-weight:700;color:#0d1117;letter-spacing:-.01em}
h2{font-size:21px;margin:40px 0 14px;padding-bottom:8px;border-bottom:2px solid #e5e7eb;color:#0d1117;font-weight:700}
h3{font-size:17px;margin:22px 0 10px;color:#0d1117;font-weight:600}
h4.bucket{margin:40px 0 16px;padding:10px 0 8px;border-top:3px solid #0d1117;border-bottom:1px solid #eaeef2;font-size:19px;font-weight:700;color:#0d1117}
h4.bucket .count{font-size:13px;font-weight:400;color:#656d76;font-style:italic;margin-left:8px}
p{margin:0 0 14px}
a{color:#0969da;text-decoration:none}
a:hover{text-decoration:underline}
.meta{font-size:13px;color:#3b434d;padding:14px 18px;background:#f6f8fa;border-left:3px solid #0969da;border-radius:6px;margin:14px 0 28px}
.meta div{margin:2px 0}
.bucket-line{font-family:ui-monospace,SFMono-Regular,Consolas,Menlo,monospace;background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;padding:10px 14px;font-size:13px;color:#24292f;margin:10px 0;overflow-x:auto;white-space:pre}
.paper{padding:16px 0;border-top:1px solid #eaeef2}
.paper:first-of-type{border-top:none}
.paper-line1{margin-bottom:4px}
.paper-line1 a{font-weight:600}
.paper-authors{font-style:italic;color:#656d76;font-size:14px;margin:2px 0 10px}
.badge{display:inline-block;font-size:11px;font-weight:600;padding:1px 8px;border-radius:10px;margin-left:6px;vertical-align:middle;font-family:ui-monospace,monospace;letter-spacing:.02em}
.badge-cv{background:#ddf4ff;color:#0550ae;border:1px solid #54aeff}
.badge-ro{background:#fff8c5;color:#7a4e00;border:1px solid #d4a72c}
.badge-cvro{background:#ffe5d9;color:#9a3412;border:1px solid #f59e0b}
.cbadge{display:inline-block;font-size:10.5px;font-weight:500;padding:1px 7px;border-radius:10px;margin-left:4px;vertical-align:middle;font-family:ui-monospace,monospace}
.cbadge-code{background:#dcfce7;color:#166534;border:1px solid #86efac;text-decoration:none}
.cbadge-hf{background:#fef9c3;color:#854d0e;border:1px solid #fde047;text-decoration:none}
.cbadge-page{background:#e0f2fe;color:#075985;border:1px solid #7dd3fc;text-decoration:none}
.cbadge-nocode{background:#f3f4f6;color:#6b7280;border:1px solid #d1d5db}
.insight,.topic{background:#fafbfc;border:1px solid #eaeef2;border-radius:8px;padding:14px 18px;margin:12px 0}
.insight h3,.topic h3{margin-top:0}
.contrast{background:#fdf6ff;border:1px solid #e9d5ff;border-radius:8px;padding:14px 18px;margin:12px 0}
.contrast ul{margin:6px 0;padding-left:22px}
.contrast li{margin:3px 0}
.crosspair{background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;padding:14px 18px;margin:12px 0}
.crosspair h3{margin:0 0 6px 0;font-size:15px}
.mustread{background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:16px 20px;margin:14px 0}
.mustread h3{margin-top:0}
.mustread .section-title{font-weight:600;color:#92400e;margin-top:12px;margin-bottom:4px;font-size:13.5px;text-transform:uppercase;letter-spacing:0.02em}
.mustread pre{background:#fff;border:1px solid #fde68a;border-radius:4px;padding:10px;font-size:12.5px;overflow-x:auto}
.risk{background:#fef2f2;border:1px solid #fecaca;border-radius:8px;padding:14px 18px;margin:12px 0}
.risk h3{margin:0 0 6px 0;font-size:15px;color:#991b1b}
blockquote{border-left:3px solid #d0d7de;margin:10px 0;padding:6px 14px;color:#656d76;background:#f6f8fa;border-radius:0 6px 6px 0;font-size:13.5px}
.hot{font-weight:600;color:#b91c1c}
.cold{font-weight:600;color:#0369a1}
hr{border:none;border-top:1px solid #eaeef2;margin:28px 0}
footer{margin-top:40px;padding-top:16px;border-top:1px solid #eaeef2;font-size:12px;color:#656d76;text-align:center}
ul.links{padding-left:20px}
ul.links li{margin:4px 0}
.home-btn{display:inline-block;padding:6px 14px;font-size:13px;font-weight:500;color:#0969da;background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;text-decoration:none;transition:background-color .12s ease,border-color .12s ease}
.home-btn:hover{background:#eaeef2;border-color:#8b95a1;text-decoration:none}
.home-btn-top{margin:0 0 18px}
.home-btn-bottom{display:block;text-align:center;margin:18px 0 0}
@media (max-width:640px){.container{padding:24px 20px}h1{font-size:23px}h2{font-size:19px}body{padding:16px 8px}}"""

BUCKET_ICON = {
    '3D/Scene':'📦','Robot Learning':'🤖','Autonomous Driving':'🚗',
    'Foundation Models':'🧠','Generation':'🎨','Efficiency/Systems':'⚡',
    'Embodied AI':'🏃','Safety/Alignment':'🛡️',
}

def esc(s): return html.escape(s or '', quote=True)

def badge_html(p):
    b = p.get('badge','')
    cls = {'CV':'badge-cv','RO':'badge-ro','CV/RO':'badge-cvro'}.get(b,'badge-cv')
    return f'<span class="badge {cls}">{esc(b)}</span>'

def summary_for(arxiv_id, title):
    s = SUMMARIES.get(arxiv_id)
    if s: return s
    return f"오늘 /new에 등록된 결로, 제목('{title[:80]}…')만으로는 정확한 평가가 어려워 본문 확인이 필요합니다."

def render_paper(p):
    aid = p['arxiv_id']
    title = esc(p['title'])
    auth = esc(p['first_author'] or '')
    badge = badge_html(p)
    cbadge = '<span class="cbadge cbadge-nocode">[📦 code ✗]</span>'
    summary = summary_for(aid, p['title'])
    return (
        f'<div class="paper">'
        f'<div class="paper-line1">📄 <a href="https://arxiv.org/abs/{aid}" target="_blank" rel="noopener"><strong>{title}</strong></a> {badge} {cbadge}</div>'
        f'<div class="paper-authors">👥 {auth} et al.</div>'
        f'<p>{summary}</p>'
        f'</div>'
    )

def main():
    d = json.load(io.open("out/classified.json", encoding="utf-8"))
    buckets = d['buckets']

    order = ['3D/Scene','Robot Learning','Autonomous Driving','Foundation Models','Generation','Efficiency/Systems','Embodied AI','Safety/Alignment']

    parts = []
    parts.append('<!DOCTYPE html>')
    parts.append('<html lang="ko">')
    parts.append('<head>')
    parts.append('<meta charset="UTF-8">')
    parts.append('<meta name="viewport" content="width=device-width,initial-scale=1">')
    parts.append(f'<title>arXiv Daily Briefing — {DATE}</title>')
    parts.append(f'<style>{CSS}</style>')
    parts.append('</head>')
    parts.append('<body>')
    parts.append('<div class="container">')
    parts.append('<a href="https://gisbi-kim.github.io/arxiv-daily-summary/" class="home-btn home-btn-top">← 전체 목록으로</a>')
    parts.append(f'<h1>📄 arXiv Daily Briefing — {DATE} ({WEEKDAY})</h1>')
    parts.append('<div class="meta">')
    parts.append('<div><strong>시야:</strong> 주간 2026-04-23 ~ 2026-04-29 · 오늘 배치 cs.CV/new + cs.RO/new</div>')
    parts.append('<div><strong>소스:</strong> arxiv.org /list/cs.CV/new · /list/cs.RO/new (stdlib 파서 경유)</div>')
    parts.append('<div><strong>주간 규모:</strong> cs.CV 607편 · cs.RO 201편 (union ~744편)</div>')
    parts.append('<div><strong>오늘 /new:</strong> cs.CV 152 + cs.RO 52 → 114 unique → 96편 8개 ROI 버킷 선정</div>')
    parts.append('<div><strong>델타 기준:</strong> 6일 전 스냅샷(2026-04-23)과 비교 (7일 전 스냅샷 부재로 가장 가까운 과거 사용)</div>')
    parts.append('</div>')

    # 주간 동향 (3 paragraphs)
    parts.append('<h2>🔭 주간 동향</h2>')
    parts.append('<p>이번주 가장 강한 매크로 신호는 <strong>Safety/Alignment</strong>가 31→67편으로 <span class="hot">+116%</span>나 폭증했다는 점이에요. 솔직히 한 주 사이에 두 배가 넘게 뛰는 건 흔치 않은 일이고, 어제까지 Safety가 39편이었던 것에서도 +72%가 더 붙은 거라 우연이 아닙니다. 의료 영상 robustness audit, foundation segmentation의 도메인 shift, deepfake detection robustness, label noise·OOD·adversarial 같은 정통 라인이 한꺼번에 쏟아지는 모양새고, 어제까지 보던 \'production-deployment 라인이 굵어진다\'는 흐름의 정점이 이번주에 찍혔다고 봐요. 반면 <strong>Foundation Models</strong>는 112→51편(<span class="cold">-54%</span>), <strong>Embodied AI</strong>는 30→15편(<span class="cold">-50%</span>)으로 절반 가까이 빠졌습니다. FM·Embodied AI가 동시에 절반으로 빠지는 건 한 주 전 폭증의 평균 회귀로 해석되고, FM 결들이 \'단독 신규 모델\'에서 \'evaluation 인프라·measurement\'로 무게중심이 옮겨가는 흐름과도 일관됩니다.</p>')
    parts.append('<p>오늘 /new에서 제일 눈에 띄는 건 <strong>VLA 라인이 \'execution paradigm\'을 새로 정의하는 시도들이 나란히 등장</strong>했다는 점이에요. <a href="https://arxiv.org/abs/2604.24921">Libra-VLA</a>가 monolithic VLA를 dual-system(macro discrete + micro continuous)으로 분해하는 비동기 실행 paradigm을 들고 나왔고, <a href="https://arxiv.org/abs/2604.25050">DiscreteRTC</a>는 \'discrete diffusion policy가 비동기 실행에 자연스럽게 fit\'한다며 flow-matching의 inpainting 한계를 정조준합니다. <a href="https://arxiv.org/abs/2604.25859">Privileged Foresight Distillation</a>은 world action model의 future-prediction branch를 \'정규화기\'로 보던 통념을 뒤집어 \'action-conditioned correction\'으로 재해석. VLA가 \'학습 paradigm\' 다음으로 \'실행 paradigm\'을 다시 짜는 단계로 진입한 신호로 봅니다. 이건 한동안 갈 것 같아요.</p>')
    parts.append('<p>부상 중인 미니 토픽 두 개. 첫째, <strong>VLM 평가 자체에 대한 진단</strong>이 한 날에 다섯 편이 뭉쳐 등장했어요 — <a href="https://arxiv.org/abs/2604.25235">VLM Judges Can Rank but Cannot Score</a>(VLM-as-Judge의 score는 unreliable, ranking만 의미), <a href="https://arxiv.org/abs/2604.25072">XTC-Bench</a>(Unified MM의 cross-task consistency 측정), <a href="https://arxiv.org/abs/2604.25855">SIEVES</a>(selective prediction을 visual evidence scoring으로), <a href="https://arxiv.org/abs/2604.25642">Prefill-Time Intervention</a>(hallucination을 decoding 아니라 prefill에서 잡기), <a href="https://arxiv.org/abs/2604.25685">Foundation Segmentation Robustness</a>(SAM의 의료 도메인 shift 감사). 어제 PushupBench·DO-Bench가 \'무엇이 깨지나\'였다면 오늘은 \'어떻게 측정해야 신뢰할 만한가\'로 한 단계 위 메타-평가로 올라간 셈입니다. 둘째, <strong>물리 reasoning 벤치마크</strong>가 새 카테고리로 자리잡는 흐름 — <a href="https://arxiv.org/abs/2604.25788">KinDER</a>(kinematic+dynamic embodied reasoning, 25개 환경 + 13 baseline)는 \'embodiment·환경·task의 세 축 reasoning\'이라는 새 평가 지점을 정의해, LIBERO/CALVIN가 했던 \'manipulation 평가\' 다음 단계로 \'physical reasoning 평가\'를 community standard로 끌어올릴 가능성이 큽니다.</p>')

    # CV vs RO
    parts.append('<h2>📐 CV vs RO 대비</h2>')
    parts.append('<p>오늘 분포는 Generation(23)·Efficiency(19)·Robot Learning(12)·Foundation Models(12)·Safety(11)·AD(10)·3D/Scene(7)·Embodied(2)으로, <em>CV 측 버킷이 상위 두 자리를 잡고</em> Robot Learning이 그 뒤를 따르는 모양새예요. 어제 Generation·FM·Safety가 동시에 41~44편 상위 3개를 차지하던 것과 비교하면 오늘은 전반적으로 \'상한 22편\' 정도로 줄어들면서 좀 더 조용한 날에 가깝고, 대신 Robot Learning 12편 중 9편이 RO 전용이라 RO쪽 비중이 한 주 평균보다 높은 편입니다. 누적 시야로는 Safety/Alignment 67편이 최상위로 올라온 게 가장 큰 변화고, FM이 51편으로 어제와 거의 같이 정체되면서 \'단독 신규 모델 라인\'이 식어가는 흐름이 일주일 사이 명확해졌습니다.</p>')
    parts.append('<div class="contrast">')
    parts.append('<p><strong>① 공통으로 뜨는 키워드</strong></p>')
    parts.append('<ul>')
    parts.append('<li><code>VLA execution</code> — CV/RO(Libra-VLA dual-system), RO(DiscreteRTC, Privileged Foresight Distillation) — 한 날 세 편이 동시에 \'execution paradigm 재정의\' 라인을 점화</li>')
    parts.append('<li><code>VLM 평가 신뢰성</code> — CV(VLM-Judges-Cannot-Score, XTC-Bench, SIEVES, Prefill-Time Intervention, Foundation Segmentation Robustness) + RO(KinDER physical reasoning bench) — 양쪽 모두 \'무엇을 측정할지\' 단계에서 \'어떻게 측정이 신뢰할 만한지\' 단계로 이동</li>')
    parts.append('<li><code>diffusion as policy/SR/edit</code> — CV(GramSR, ResetEdit, ResetEdit, Refinement-via-Regeneration), RO(DiscreteRTC) — diffusion이 generation 외 perception/control 라인에 흡수되는 흐름이 또 누적</li>')
    parts.append('</ul>')
    parts.append('<p><strong>② CV에만 뜨는 키워드</strong></p>')
    parts.append('<ul>')
    parts.append('<li><code>medical imaging robustness</code> — Foundation Segmentation Robustness(abdominal CT), CRC-SAM(CT/Colonoscopy/Histology), CoRE(brain lesion continual), TopoMamba(heterogeneous medical) — Safety 11편의 절반 이상이 의료 측 결로, CV deployment의 가장 큰 industry segment가 의료라는 점이 분포로 꽂힘</li>')
    parts.append('<li><code>spiking / quantization / pruning</code> — Vision SmolMamba, QB-LIF burst neurons, Quantum-Inspired SAR, Diverse Image Priors — efficiency 19편 중 하드웨어 측 결이 한 day 같이 등장</li>')
    parts.append('<li><code>video generation post-train</code> — Mutual Forcing(audio-video), Systematic Post-Train Framework, ViPO Visual Preference, DDA-Thinker reasoning — generation 라인이 \'학습\'에서 \'post-train\'으로 무게중심 이동</li>')
    parts.append('</ul>')
    parts.append('<p><strong>③ RO에만 뜨는 키워드</strong></p>')
    parts.append('<ul>')
    parts.append('<li><code>UAV/UGV cooperation</code> — Dynamic UGV-UAV Path Planning, UGV-UAV Cooperative Partitioning, Tube NMPC for Cooperative Aerial — 멀티 플랫폼 cooperation이 한 날 세 편 — drone+ground 협력이 뜨는 신호</li>')
    parts.append('<li><code>tendon/continuum/soft control</code> — Tendon-Driven Continuum Robot, 3D-Printed Artificial Skin Multi-Modal Sensing — soft robotics 측 결이 일관 유지</li>')
    parts.append('<li><code>physical reasoning bench</code> — KinDER 25 envs + 13 baselines — 어제까지 \'manipulation 벤치\'로 묶이던 라인을 \'physical reasoning\'이라는 더 큰 우산 아래로 재배치하는 결</li>')
    parts.append('</ul>')
    parts.append('<p><strong>④ 같은 단어 다른 맥락</strong></p>')
    parts.append('<ul>')
    parts.append('<li><code>diffusion</code>: CV는 \'image SR/edit/T2I quality\' (GramSR, ResetEdit, Mutual Forcing) / RO는 \'asynchronous policy executor\' (DiscreteRTC) — 같은 단어가 \'pixel quality\' vs \'real-time control\'로 정반대 측 활용</li>')
    parts.append('<li><code>safety</code>: CV는 \'embedding-guided typographic perturb\'·\'cross-task consistency\'·\'OOD detection\' / RO는 \'closed-loop home-service mobile manipulation\'·\'tendon-driven robust control\'·\'threat-oriented digital twinning\' — \'시각 모델 robustness\' vs \'physical actuation 보장\'으로 정반대 측 결</li>')
    parts.append('<li><code>memory / context</code>: CV(Interactive Episodic Memory with User Feedback — ambiguous query에 user feedback 추가) / RO(Privileged Foresight Distillation — joint training의 future branch 재해석) — CV는 \'사람과의 상호작용\', RO는 \'training-time privileged info\'</li>')
    parts.append('</ul>')
    parts.append('</div>')
    parts.append('<p>오늘의 CV/RO 교집합은 \'<em>평가/측정의 신뢰성을 다시 짜는</em>\' 흐름이에요. CV쪽은 VLM-as-Judge가 score는 못 주고 ranking만 줄 수 있다는 진단(VLM Judges Cannot Score)에서 시작해 cross-task consistency·selective prediction·prefill intervention까지 \'평가 자체의 calibration\'을 정조준하고, RO쪽 KinDER는 \'physical reasoning 평가\'라는 새 카테고리를 community standard로 끌어올립니다. 어제까지 \'무엇이 깨지나\' 단계였다면 오늘은 \'어떻게 측정해야 깨지지 않은 결과인지 확인할 수 있나\' 단계 — 한 단계 메타-올라간 신호로 봅니다.</p>')

    # 인사이트
    parts.append('<h2>💡 오늘의 인사이트</h2>')
    parts.append('<div class="insight"><h3>VLA가 학습 paradigm 다음으로 \'execution paradigm\'을 재정의하는 단계 진입 — 비동기·dual-system·discrete diffusion 셋이 한 날 동시 등장</h3><p>오늘 <a href="https://arxiv.org/abs/2604.24921">Libra-VLA</a>가 monolithic VLA를 \'macro discrete reaching + micro continuous pose alignment\' dual-system으로 비동기 실행하는 paradigm을 들고 나왔고, <a href="https://arxiv.org/abs/2604.25050">DiscreteRTC</a>는 flow-matching 정책의 RTC 한계를 정조준해 \'discrete diffusion이 비동기 executor에 자연스럽게 fit한다\'는 paradigm shift를 제시. <a href="https://arxiv.org/abs/2604.25859">Privileged Foresight Distillation</a>은 world action model의 future-prediction branch를 \'정규화기\'로 보던 통념을 뒤집어 \'training-time privileged correction\'으로 재해석합니다. 어제까지 \'VLA failure mode 진단\' 단계였다면 오늘은 \'paradigm 자체를 다시 짠다\'는 다음 단계 — 우리 manipulation 스택의 inference 디자인을 한 번 더 audit해야 할 시점입니다.</p></div>')
    parts.append('<div class="insight"><h3>VLM 평가가 \'무엇이 깨지나\' 단계에서 \'어떻게 측정해야 신뢰할 만한가\' 메타-단계로 이동</h3><p>오늘 <a href="https://arxiv.org/abs/2604.25235">VLM Judges Can Rank but Cannot Score</a>가 \'VLM-as-Judge가 conformal interval로 봤을 때 score는 unreliable, ranking만 의미가 있다\'는 결을 내놓고, <a href="https://arxiv.org/abs/2604.25072">XTC-Bench</a>는 unified MM의 cross-task semantic consistency를 scene-graph로 측정, <a href="https://arxiv.org/abs/2604.25855">SIEVES</a>는 selective prediction을 visual evidence scoring으로, <a href="https://arxiv.org/abs/2604.25642">Prefill-Time Intervention</a>은 hallucination을 decoding이 아니라 prefill에서 잡습니다. 어제 PushupBench·DO-Bench·ReVSI가 \'단일 axis failure\'였다면 오늘은 \'평가 framework 자체의 calibration\'으로 한 단계 메타-위로 — POPE가 hallucination에 한 일을 \'meta-evaluation\' 축에서 반복하는 패턴이고, evaluation 인프라를 가진 랩이라면 가장 빠르게 follow-up할 자리예요.</p></div>')
    parts.append('<div class="insight"><h3>Safety/Alignment 6일 만에 +116% 폭증 — production-deployment 라인이 한 주 단위로 분기점</h3><p>이번주 누적 67편은 6일 전 31편 대비 두 배 이상 — 의료 영상 robustness audit(<a href="https://arxiv.org/abs/2604.25685">Foundation Segmentation Robustness</a>), embedding-guided typographic perturbation으로 VLM safety 분석(<a href="https://arxiv.org/abs/2604.25102">Embedding-Guided Perturb</a>), home-service mobile manipulation의 closed-loop physical grounding(<a href="https://arxiv.org/abs/2604.25323">ANCHOR</a>), threat-oriented digital twinning(<a href="https://arxiv.org/abs/2604.25757">Threat-Oriented Digital Twinning</a>)이 한 주 내내 누적되면서 \'production deployment를 막는 silent killer\'를 정조준한 결들이 한꺼번에 등장. AD 분야가 어제까지 \'social-aware decision\'이었다면 이번주는 분야를 가리지 않고 \'deployment 시 무너지는 자리 audit\'이 평행하게 가속하는 흐름. 솔직히 이 인사이트가 가장 무거워요 — 향후 4~6주 동안 \'deployment audit\'이 evaluation을 이어 다음 community 표준이 될 가능성이 큽니다.</p></div>')

    # 추천 연구주제
    parts.append('<h2>🔬 추천 연구주제</h2>')
    parts.append('<div class="topic"><h3>VLA Asynchronous Execution Atlas — paradigm 셋의 정량 비교 + 실시간 hardware audit</h3><p>오늘 Libra-VLA(dual-system) · DiscreteRTC(discrete diffusion) · Privileged Foresight Distillation(world action correction) 셋이 모두 \'VLA 비동기 실행\'을 다른 각도에서 다루지만, 단일 hardware/task에서 통합 비교한 결은 비어 있어요. 우리 랩이 manipulation 인프라를 갖췄다면 \'세 paradigm × 동일 task × 실제 inference latency/jitter/throughput\' 측 벤치를 빠르게 만들 수 있고, 4~6주 안에 community standard 후보가 될 자리. 특히 어제 XPU characterization과 결합하면 \'paradigm × hardware × task\' 3축 atlas가 되는데, 이건 deployment 측에서 즉시 가치 있는 reference가 됩니다.</p></div>')
    parts.append('<div class="topic"><h3>VLM Meta-Eval Calibration Suite — Judge·Score·Consistency·Selective·Prefill 다섯 axis 통합</h3><p>오늘 VLM-Judges-Cannot-Score · XTC-Bench · SIEVES · Prefill-Time Intervention · Foundation Segmentation Robustness가 흩어진 axis에서 각자 evaluation calibration 결을 내놨는데, 통합 framework가 비어 있어요. \'judge reliability·cross-task consistency·selective prediction·prefill stage·domain shift robustness\' 5축으로 표준 진단을 묶으면 POPE·MMMU가 한 일을 \'meta-eval\' 축에서 반복할 수 있습니다. 우리 랩이 VLM evaluation 인프라를 갖췄다면 가장 빠르게 \'first-mover\' 위치를 잡을 자리고, AD/medical/embodied 측 deployment 응용 모두 즉시 reference로 사용할 만한 결.</p></div>')
    parts.append('<div class="topic"><h3>Physical Reasoning as a New Eval Category — KinDER를 community 표준으로 굳히는 후속</h3><p>오늘 <a href="https://arxiv.org/abs/2604.25788">KinDER</a>가 \'embodiment·환경·task 세 축 physical reasoning\'을 25개 환경 + 13 baseline로 표준화했지만, LIBERO·CALVIN·RLBench 같은 manipulation 벤치와 어떻게 상호 호환·차별화되는지 정량 분해가 비어 있어요. 우리 랩이 manipulation 데이터를 갖췄다면 \'KinDER vs LIBERO/CALVIN/RLBench의 점수 상관계수 + KinDER 고유 어려움 axis 분해\'를 빠르게 측정 가능. \'physical reasoning\'이 manipulation을 잇는 community 표준으로 굳을지 여부가 4~6주 내 결정될 가능성이 크고, 그 자리를 follow-up하는 결이 가장 빠르게 인용을 모을 후보입니다.</p></div>')

    # 회고 — 수요일이라 skip
    # parts.append('<h2>🧭 예측 회고 루프</h2>')

    # 버킷 현황
    parts.append('<h2>📊 오늘의 버킷 현황</h2>')
    bucket_lines = []
    for b in order:
        info = buckets[b]
        icon = BUCKET_ICON[b]
        bucket_lines.append(f'{icon} {b:<20}: {info["total"]:>2}편 (CV {info["cv"]:>2} / RO {info["ro"]:>2} / CV-RO {info["cvro"]})')
    parts.append('<div class="bucket-line">' + '\n'.join(bucket_lines) + '</div>')

    sorted_b = sorted([(b, buckets[b]['total']) for b in order], key=lambda x: -x[1])
    top3 = sorted_b[:3]
    bot2 = sorted_b[-2:]
    parts.append(f'<p>🔥 <span class="hot">TOP3</span>: {top3[0][0]} ({top3[0][1]}), {top3[1][0]} ({top3[1][1]}), {top3[2][0]} ({top3[2][1]}) · ❄️ <span class="cold">BOTTOM2</span>: {bot2[0][0]} ({bot2[0][1]}), {bot2[1][0]} ({bot2[1][1]}). 어제 Generation·FM·Safety 41~44편으로 광폭이었던 것에 비해 오늘은 상한이 23편(Generation)으로 좀 더 차분한 분포예요. Robot Learning 12편 중 9편이 RO 전용이라 RO 비중이 평소보다 높고, Embodied AI는 2편으로 한 주 내내 가장 조용한 자리. 어제 우려한 FM mean-reversion이 51편으로 정체되면서 \'단독 모델 라인 식어가는\' 흐름이 더 뚜렷해진 모양새입니다.</p>')

    # 델타 (vs 2026-04-23, 6일 전)
    parts.append('<p>📈 <strong>주간 델타(2026-04-23 → 2026-04-29, 6일 시야)</strong>: 🛡️ Safety/Alignment <span class="hot">+116%</span> (31→67), 🚗 Autonomous Driving <span class="hot">+23%</span> (13→16), 🤖 Robot Learning <span class="cold">-9%</span> (58→53), 📦 3D/Scene <span class="cold">-7%</span> (40→37), ⚡ Efficiency <span class="cold">-11%</span> (28→25), 🎨 Generation <span class="cold">-16%</span> (79→66), 🏃 Embodied AI <span class="cold">-50%</span> (30→15), 🧠 Foundation Models <span class="cold">-54%</span> (112→51). Safety 폭증(+116%)이 가장 큰 매크로 신호로, \'production deployment audit\' 라인이 한 주 단위 분기점에 진입했음을 분명하게 보여줍니다. FM·Embodied AI 동시 -50%대 빠짐은 한 주 전 폭증 후 평균 회귀로 보이고, AD가 +23%로 \'social-aware decision\' 흐름의 기세는 살아있어요. 어제 우려했던 \'FM·Embodied가 자연스러운 호흡\' 가정이 6일 시야에선 더 뚜렷해지고 있습니다.</p>')

    # 벤치마크 SOTA — 오늘은 신규 SOTA 보고 없음
    parts.append('<h2>📈 벤치마크 SOTA 추이</h2>')
    parts.append('<p>이번주 추적 벤치마크(ScanNet++·LIBERO·nuScenes·MMMU·VBench 등)에서 새 SOTA 수치 보고는 잡힌 게 없습니다. 다만 <a href="https://arxiv.org/abs/2604.25788">KinDER</a>가 25개 환경 + 13 baseline로 \'physical reasoning\' 평가 카테고리를 새로 정의해 LIBERO/CALVIN/RLBench 등 기존 벤치와 \'어디까지 호환·어디서 차별화\'되는지 정량 비교가 향후 결에서 필요하고, <a href="https://arxiv.org/abs/2604.25072">XTC-Bench</a>는 unified MM의 \'cross-task consistency\'라는 새 axis를 측정. 다음주 LIBERO/MMMU 측 결과 누적되면 표 갱신할게요.</p>')

    # 크로스오버 페어
    parts.append('<h2>🔀 크로스오버 페어</h2>')
    parts.append('<div class="crosspair"><h3>평가의 신뢰성을 다시 짜기 — VLM Judges(CV) vs KinDER(RO)</h3><p><a href="https://arxiv.org/abs/2604.25235">VLM Judges Can Rank but Cannot Score</a>(CV)가 conformal prediction으로 \'VLM-as-Judge의 score는 unreliable, ranking만 의미\'라는 진단을 정량 입증하고, 같은 날 <a href="https://arxiv.org/abs/2604.25788">KinDER</a>(RO)는 \'embodiment·환경·task 세 축 physical reasoning\'을 25 envs + 13 baselines로 표준화. 양쪽 모두 \'기존 metric/벤치가 무엇을 정직하게 측정하지 못하는가\'를 정조준한 결인데, CV는 \'judge calibration\' RO는 \'evaluation 카테고리 재정의\' 측면에서. 같은 진단이 두 community에서 동시 표면화하는 건 \'평가 framework 자체의 maturity\'가 향후 6개월 양쪽 공통 키워드가 될 신호로 봅니다.</p></div>')
    parts.append('<div class="crosspair"><h3>Closed-loop physical grounding — Prefill Hallucination(CV) vs ANCHOR(RO)</h3><p><a href="https://arxiv.org/abs/2604.25642">Prefill-Time Intervention</a>(CV)이 LVLM hallucination을 decoding 단계가 아닌 prefill 단계에서 잡아 \'autoregressive accumulation\'을 끊고, 같은 날 <a href="https://arxiv.org/abs/2604.25323">ANCHOR</a>(RO)는 home-service mobile manipulation의 \'symbolic plan vs evolving physical world\' 불일치를 closed-loop physical grounding으로 보정. 둘 다 \'reasoning trajectory 중간 어딘가에서 grounding이 무너진다\'는 같은 진단을 공유하지만, CV는 \'token decoding 시점\' RO는 \'physical execution 시점\' 측을 정조준. 같은 문제 인식이 modality를 넘나들며 동시 등장하는 건 \'intermediate-stage grounding\'이 양쪽 공통 fix 패러다임이 될 신호로 봅니다.</p></div>')

    # Must-read
    parts.append('<h2>🌟 오늘의 must-read</h2>')

    parts.append('<div class="mustread">')
    parts.append('<h3>① Libra-VLA: Achieving Learning Equilibrium via Asynchronous Coarse-to-Fine Dual-System <span class="badge badge-cvro">CV/RO</span></h3>')
    parts.append('<p><a href="https://arxiv.org/abs/2604.24921">arxiv:2604.24921</a> · 저자 정보 첨부 abstract 기반</p>')
    parts.append('<div class="section-title">핵심 주장</div>')
    parts.append('<p>현재 VLA 모델들이 visual-linguistic feature를 high-frequency motor command에 \'flat·non-hierarchical\'하게 직접 매핑하는 monolithic paradigm을 쓰는데, 이 논문은 manipulation의 본질적 hierarchy를 \'macro discrete reaching + micro continuous pose alignment\'로 분해하는 Hybrid Action Space + 비동기 dual-system으로 학습 equilibrium을 잡습니다. 기존엔 high-frequency action 생성에서 macro-level decision이 미세 잡음에 묻혔는데, dual-system으로 분리하면서 두 axis가 서로 다른 timescale로 학습돼 \'learning equilibrium\'에 도달하는 게 차이점이에요. VLA 분야에서 \'학습 paradigm\' 다음으로 \'실행 paradigm\'을 다시 짜는 첫 결로 봐도 무방.</p>')
    parts.append('<div class="section-title">방법의 핵심 (직관)</div>')
    parts.append('<pre># Monolithic VLA (기존)\naction = vla(visual, language)  # flat mapping, all axes\n# Side effect: high-frequency motor noise dominates,\n#              macro reaching decision gets buried\n\n# Libra-VLA: Hybrid Action Space + Dual-System\nmacro_a = system1_discrete(visual, language)   # slow/coarse\nmicro_a = system2_continuous(macro_a, visual)  # fast/fine\n# Asynchronous: system1 every K steps, system2 every step\n# Equilibrium: each system specializes its own timescale</pre>')
    parts.append('<div class="section-title">약점·한계</div>')
    parts.append('<p>(a) Hybrid Action Space의 \'discrete reaching vs continuous pose\' 경계가 task-dependent라, 새 task에 일반화될 때 hand-engineering 부담 가능성. (b) System 1↔2 비동기 동기화 시점에 jitter가 어떻게 생기는지 abstract만으론 안 보여, 실 hardware deployment에서 latency variance가 새 silent killer가 될 위험. (c) \'Learning equilibrium\' 클레임이 정성적 narrative로 그치지 않으려면 두 system 각각의 loss curve와 mutual information 분석이 필요. (d) DiscreteRTC와 동일 모달의 problem statement인데, 두 paradigm 사이 \'언제 dual-system이 낫고 언제 discrete diffusion이 나은지\' 비교 부재.</p>')
    parts.append('<div class="section-title">랩 파이프라인 영향</div>')
    parts.append('<p>VLA 기반 manipulation 스택을 굴리는 랩이라면 architecture 측에서 즉각 audit 후보입니다. 특히 medical/long-task 시나리오처럼 \'macro 의사결정과 micro 동작 안정성\'이 모두 중요한 환경에서 monolithic VLA가 silent하게 한 쪽을 희생하는지 확인 필요. Asynchronous 실행 deployment 측이라면 어제까지의 XPU characterization 결과와 결합해 \'system1·system2가 각자 어느 hardware에 fit\'하는지 비교가 즉시 가치 있는 후속.</p>')
    parts.append('</div>')

    parts.append('<div class="mustread">')
    parts.append('<h3>② DiscreteRTC: Discrete Diffusion Policies are Natural Asynchronous Executors <span class="badge badge-ro">RO</span></h3>')
    parts.append('<p><a href="https://arxiv.org/abs/2604.25050">arxiv:2604.25050</a> · 저자 정보 첨부 abstract 기반</p>')
    parts.append('<div class="section-title">핵심 주장</div>')
    parts.append('<p>Physical AI는 chatbot과 달리 세계가 실시간 evolving하기 때문에 synchronous executor의 inter-chunk pause가 dynamic task에선 fatal — inference가 아무리 빨라도. Real-time chunking(RTC)이 chunk 전환을 inpainting으로 재해석해 비동기 실행을 viable하게 했지만, flow-matching policy + RTC 조합은 inpainting이 \'inference-time correction\'에 의존하느라 base policy의 분포에서 벗어나 구조적으로 suboptimal. 이 논문은 \'discrete diffusion policy가 inpainting을 base policy의 학습된 conditional으로 자연스럽게 수행하는 natural asynchronous executor\'라는 paradigm shift를 제시. 기존엔 \'flow-matching이 빠르고 부드럽다\' 통념이었는데, 비동기 실행 측면에선 discrete diffusion이 구조적으로 더 fit한다는 결이라 흥미로워요.</p>')
    parts.append('<div class="section-title">방법의 핵심 (직관)</div>')
    parts.append('<pre># Flow-matching RTC (기존)\nfor t in range(action_chunk):\n    if committed[t]: freeze(t)\n    else: a[t] = inference_time_inpaint(committed)\n# Issue: inpainting != base policy distribution\n#        → suboptimal, distribution shift\n\n# DiscreteRTC: discrete diffusion as natural inpainter\n# Discrete diffusion already learns p(unmasked | masked)\n# → committed actions become \"masked\" tokens\n# → base policy ITSELF generates remainder consistently\nfor t in range(action_chunk):\n    a[t] = discrete_diffusion.denoise(committed_mask)</pre>')
    parts.append('<div class="section-title">약점·한계</div>')
    parts.append('<p>(a) Discrete action space로의 quantization이 fine-grained pose에서 표현력 손실을 만들 수 있어, 적절한 token 수와 task-specific quantization 디자인이 새 hyperparameter. (b) Flow-matching 대비 학습 cost·수렴 속도 비교 정량이 abstract만으론 안 보임. (c) 비동기 실행에서 \'committed mask\'가 인공적이라, 실제 hardware에서 commit timing의 정확성에 paradigm 전체가 민감할 가능성. (d) Libra-VLA의 dual-system과 직접 비교 부재 — 두 paradigm 사이의 trade-off가 명확해야 community가 어느 쪽으로 정착할지 결정 가능.</p>')
    parts.append('<div class="section-title">랩 파이프라인 영향</div>')
    parts.append('<p>Flow-matching policy를 굴리는 manipulation 스택이라면 비동기 실행 측면에서 immediate audit 가치가 큽니다. 특히 dynamic environment(이동 물체, 사람 interaction, deformable object) 시나리오에서 inter-chunk pause가 silent failure를 만들고 있는지 측정 필요. Discrete diffusion 학습 인프라가 이미 갖춰진 랩이라면 빠르게 transfer 후보로 채택 가능하고, 그렇지 않다면 \'flow-matching이 정말 비동기에 suboptimal한가\'를 우리 데이터로 재현하는 게 첫 단계입니다.</p>')
    parts.append('</div>')

    # 리스크 필터
    parts.append('<h2>⚠️ 리스크·한계 필터</h2>')
    parts.append('<div class="risk"><h3>VLM Judges Can Rank but Cannot Score — \'14 visual task\' 일반화 클레임의 task selection bias</h3><p><a href="https://arxiv.org/abs/2604.25235">VLM Judges Can Rank but Cannot Score</a>가 conformal prediction으로 \'3 judges × 14 visual task\'에서 score는 unreliable이라는 결을 내놨는데, \'14개 task\'가 어떻게 선정됐는지가 결론의 generalizability에 결정적입니다. Task가 cherry-picked이면 \'judge가 score 못 준다\'는 강한 클레임이 약화될 수 있어, 본문의 task selection criteria + 미선정 task에 대한 generalization 논의 정독 전엔 \'VLM-as-Judge는 score 금지\' 강한 행동 가이드는 보류하는 게 안전.</p></div>')
    parts.append('<div class="risk"><h3>Privileged Foresight Distillation — \'future branch는 정규화기\' 통설 반박의 정량 강도</h3><p><a href="https://arxiv.org/abs/2604.25859">Privileged Foresight Distillation</a>이 world action model의 future-prediction branch를 \'training-time privileged correction\'으로 재해석하지만, 기존 \'inference에서 future branch 제거해도 거의 손실 없음\' 결과가 robust하다면 새 해석의 정량적 우위가 명확하지 않을 수 있어요. 비교 baseline·평가 manipulation suite·정량 gain이 abstract만으론 안 보여, 본문 ablation 정독 전엔 \'future branch 재해석\' 강한 클레임은 잠정 보류. 둘 중 어느 해석이 더 잘 맞는지가 ablation의 specific gain 수치로 결정될 자리.</p></div>')
    parts.append('<div class="risk"><h3>KinDER — \'표준 평가 suite + 13 baseline\' 클레임의 baseline coverage</h3><p><a href="https://arxiv.org/abs/2604.25788">KinDER</a>가 25 environments + 13 baselines를 들고 \'physical reasoning 표준\' 자리를 노리지만, 13 baseline이 \'TAMP·imitation·LLM-based\' 등 다양 카테고리를 균형 있게 cover하지 않으면 single-paradigm이 우세한 결과로 보일 위험. \'어떤 baseline이 어떤 axis에서 어디까지 cover하는지\' matrix가 본문에 정직하게 보고됐는지 확인 전엔 \'community standard 후보\' 강한 결론은 잠정 보류.</p></div>')
    parts.append('<div class="risk"><h3>Foundation Segmentation Robustness on Abdominal CT — \'1051 slices · 41 volumes\'의 통계 power</h3><p><a href="https://arxiv.org/abs/2604.25685">Robustness Evaluation of Foundation Segmentation Model</a>이 SAM(ViT-B)를 abdominal CT 1051 slices/41 volumes로 audit한 결과인데, 41 volume이 도메인 shift의 다양성을 충분히 cover하는 sample size인지 통계 power 측면에서 claim 강도와 균형을 맞춰야 합니다. \'simulated domain shift\'가 실제 임상 다양성을 reflect하는지도 검증 필요 — 임상 multi-center 데이터로의 외삽 결론은 잠정 보류.</p></div>')

    # 논문별 요약
    parts.append('<h2>📄 논문별 요약</h2>')
    for b in order:
        info = buckets[b]
        if info['total'] == 0: continue
        icon = BUCKET_ICON[b]
        parts.append(f'<h4 class="bucket">{icon} {b} <span class="count">· {info["total"]}편 · CV {info["cv"]} / RO {info["ro"]} / CV-RO {info["cvro"]}</span></h4>')
        for p in info['papers']:
            parts.append(render_paper(p))

    # 참고 링크
    parts.append('<h2>🔗 참고 링크</h2>')
    parts.append('<ul class="links">')
    parts.append('<li>arXiv cs.CV /new — <a href="https://arxiv.org/list/cs.CV/new">arxiv.org/list/cs.CV/new</a></li>')
    parts.append('<li>arXiv cs.RO /new — <a href="https://arxiv.org/list/cs.RO/new">arxiv.org/list/cs.RO/new</a></li>')
    parts.append('<li>RSS feed — <a href="https://gisbi-kim.github.io/arxiv-daily-summary/feed.xml">feed.xml</a></li>')
    parts.append('<li>repo — <a href="https://github.com/gisbi-kim/arxiv-daily-summary">github.com/gisbi-kim/arxiv-daily-summary</a></li>')
    parts.append('</ul>')

    parts.append(f'<footer>arXiv Daily Briefing · {DATE} · stdlib parser + classify · Generated with Claude</footer>')
    parts.append('<a href="https://gisbi-kim.github.io/arxiv-daily-summary/" class="home-btn home-btn-bottom">🏠 전체 목록으로</a>')
    parts.append('</div>')
    parts.append('</body>')
    parts.append('</html>')

    out = '\n'.join(parts)
    os.makedirs("posts", exist_ok=True)
    io.open(OUT, "w", encoding="utf-8").write(out)
    print(f"wrote {OUT} ({len(out)} bytes)")

if __name__ == "__main__":
    main()
