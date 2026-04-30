#!/usr/bin/env python3
"""Generate posts/2026-04-30.html from out/classified.json + out/summaries.py"""
import json, html, io, os, sys

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

sys.path.insert(0, "out")
from summaries import SUMMARIES

DATE = "2026-04-30"
WEEKDAY = "목"
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
    return f"오늘 /new에 등록된 결로, abstract 정독 전엔 정확한 평가가 어려워 본문 확인 권장합니다."

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
    parts.append('<div><strong>시야:</strong> 주간 2026-04-24 ~ 2026-04-30 · 오늘 배치 cs.CV/new + cs.RO/new</div>')
    parts.append('<div><strong>소스:</strong> arxiv.org /list/cs.CV/new · /list/cs.RO/new (stdlib 파서 경유)</div>')
    parts.append('<div><strong>주간 규모:</strong> cs.CV 594편 · cs.RO 192편 (union ~744편 후보)</div>')
    parts.append('<div><strong>오늘 /new:</strong> cs.CV 166 + cs.RO 54 → 220 candidates → 115 ROI 매칭 → 91편 8개 ROI 버킷 선정</div>')
    parts.append('<div><strong>델타 기준:</strong> 어제 스냅샷(2026-04-29)과 비교 (1일 시야)</div>')
    parts.append('</div>')

    # 주간 동향 (3 paragraphs)
    parts.append('<h2>🔭 주간 동향</h2>')
    parts.append('<p>이번주 가장 두드러진 매크로 신호는 <strong>Generation 76편</strong>으로 한 주 내내 1위를 잡고 있다는 점이에요. 어제 66편 → 오늘 76편으로 <span class="hot">+15%</span> 더 붙었고, 오늘 /new 15편으로도 상위 버킷이라 \'생성 모델 라인의 광폭 누적\'이 6일째 끊기지 않고 있습니다. 의료 video generation·SR·diffusion sampling acceleration·post-train 측 결들이 한꺼번에 누적되는 모양새고, 이는 어제까지 지적했던 \'단독 신규 모델보다 deployment·post-train\'으로 무게가 옮겨가는 흐름의 정점이라고 봐요. 반면 어제 절정이었던 <strong>Safety/Alignment</strong>는 67편 → 26편으로 <span class="cold">-61%</span> 급락했는데, 이건 분류 keyword set 차이가 큰 변수로 보이긴 하지만 \'production-deployment 라인이 한 주 단위로 광폭 → 정착\'으로 호흡 조절에 들어간 가능성도 같이 봐야 할 것 같습니다.</p>')
    parts.append('<p>오늘 /new에서 제일 흥미로운 건 <strong>world model이 \"action·VLM·spatial reasoning의 substrate\"로 동시 등장</strong>했다는 점이에요. <a href="https://arxiv.org/abs/2604.26694">X-WAM</a>이 4D world action modeling으로 video synthesis + 3D reconstruction + robotic action을 하나의 framework로 묶었고, <a href="https://arxiv.org/abs/2604.26848">STARRY</a>는 spatial-temporal action-centric world modeling으로 VLA가 action-relevant 구조를 명시 모델링하게 만들었으며, <a href="https://arxiv.org/abs/2604.26934">World2VLM</a>은 world model의 미래 상상 능력을 VLM에 distill해 dynamic spatial reasoning을 강화. 거기에 <a href="https://arxiv.org/abs/2604.26182">Lifting Embodied World Models</a>까지 — 한 날 4편의 world-model 결이 \"action paradigm/VLM 강화/spatial reasoning\"이라는 서로 다른 axis로 동시 등장한 건 우연이 아닙니다. 어제까지 VLA execution paradigm(Libra-VLA·DiscreteRTC) 흐름 다음으로, world model 자체가 \"foundation layer\"로 정착하는 단계에 들어왔다고 봐요. 이건 한동안 갈 것 같습니다.</p>')
    parts.append('<p>부상 중인 미니 토픽 두 개. 첫째, <strong>VLM honesty/knowledge boundary가 새 evaluation axis로 굳어가는 흐름</strong>이에요. 오늘 <a href="https://arxiv.org/abs/2604.26419">Delineating Knowledge Boundaries</a>가 \"long-tail/specialized 도메인에서 hallucinate + parametric knowledge 초과 query 거절 못함\" 두 axis를 동시에 정조준했고, <a href="https://arxiv.org/abs/2604.26283">MedSynapse-V</a>는 medical VLM의 cognitive misalignment를 latent memory evolution으로, <a href="https://arxiv.org/abs/2604.26288">CheXthought</a>는 \"임상의가 어떤 순서로 추론하나\"를 데이터 자체로 만들어버림, <a href="https://arxiv.org/abs/2604.26614">State Beyond Appearance</a>는 dial reading에서 \"외형 인식 vs 상태 일관성\" 분리. 어제 VLM-Judges-Cannot-Score · XTC-Bench 흐름이 \"평가의 calibration\"이었다면 오늘은 \"VLM이 무엇을 알고 무엇을 모르는지\" 단계로 한 단계 더 깊이 들어갔어요. 둘째, <strong>3DGS deployment 라인이 두 paper로 동시 표면화</strong> — <a href="https://arxiv.org/abs/2604.26238">EnerGS</a>가 partial geometric prior 기반 energy formulation으로 학습 안정성, <a href="https://arxiv.org/abs/2604.26799">MesonGS++</a>가 post-train compression의 hyperparameter searching 자동화. 3DGS 버킷이 일주일 +16%(37→43)로 꾸준히 누적되는 가운데 한 날 두 \"deployment\" 결이 동시에 나오는 건 \"렌더링 quality 다음으로 production cost\"가 community focal point로 굳는 신호로 봅니다.</p>')

    # CV vs RO
    parts.append('<h2>📐 CV vs RO 대비</h2>')
    parts.append('<p>오늘 분포는 Safety(21)·3D/Scene(15)·Generation(15)·Robot Learning(12)·Foundation Models(12)·Efficiency(10)·AD(3)·Embodied(3)으로, <em>CV 측 결이 상위 세 자리를 다 차지하면서</em> Robot Learning이 그 뒤를 따르는 모양새예요. 어제는 Generation 23·Efficiency 19·RL 12·FM 12 분포였는데 오늘은 Safety가 21편으로 급등했고(어제 11) 3D/Scene이 15편으로 어제(7)의 두 배 — \"Safety 라벨 회복 + 3D 결 회귀\"가 동시에 일어난 모양새. RO 비중은 12편 RL 중 10편이 RO 전용이라 어제와 비슷하게 RO 분야의 \"manipulation·navigation·gripper\" 결들이 균형 있게 등장했어요. AD는 3편 모두 RO이고, Embodied도 3편(2 CV + 1 CV/RO)이라 양 측 모두 한 주 내내 가장 조용한 자리.</p>')
    parts.append('<div class="contrast">')
    parts.append('<p><strong>① 공통으로 뜨는 키워드</strong></p>')
    parts.append('<ul>')
    parts.append('<li><code>world model</code> — CV(World2VLM, Lifting Embodied World Models) + RO(STARRY) + CV/RO(X-WAM) — 한 날 4편이 \"action·VLM·spatial reasoning\" 세 axis에서 동시 점화</li>')
    parts.append('<li><code>3D content / open-vocab grounding</code> — CV(RADIO-ViPE, Multiple Consistent 2D-3D Mappings, Three-Step Nav) + RO(3D Generation Survey for Embodied) — 양쪽 모두 \"3D content/grounding이 substrate\"</li>')
    parts.append('<li><code>diffusion 응용 확장</code> — CV(L2P, ACPO, MetaSR, SnapPose3D, Manifold-Space Diffusion) + RO(FlowS) — diffusion이 generation 외 motion prediction·SR·pose lifting 측으로 흡수되는 흐름이 또 누적</li>')
    parts.append('</ul>')
    parts.append('<p><strong>② CV에만 뜨는 키워드</strong></p>')
    parts.append('<ul>')
    parts.append('<li><code>VLM honesty / knowledge boundary</code> — Delineating Knowledge Boundaries, MedSynapse-V, CheXthought, State Beyond Appearance, Beyond Shortcuts(Visual Illusions) — 5편이 \"VLM이 무엇을 아는가/모르는가\"를 새 axis로 정조준</li>')
    parts.append('<li><code>3DGS deployment</code> — EnerGS, MesonGS++, SAND(implicit query 가속) — 3DGS의 \"렌더링 품질\"에서 \"production cost\"로 무게중심 이동</li>')
    parts.append('<li><code>medical robustness/eval</code> — DepthPilot(colonoscopy gen), MedSynapse-V, CheXthought, MTCurv microtubule, Glioma FLIm, ViBE EEG — 의료 측 결이 한 날 6편 — Safety 21편의 큰 부분</li>')
    parts.append('</ul>')
    parts.append('<p><strong>③ RO에만 뜨는 키워드</strong></p>')
    parts.append('<ul>')
    parts.append('<li><code>UAV/UGV nighttime localization & SAR</code> — Lights Out(thermal night UAV), SAR UAV rule-based RL, Three-Vehicle Platooning — UAV deployment의 \"silent failure 자리\"(GNSS 차단·야간·SAR) 정조준 결 3편</li>')
    parts.append('<li><code>compositional / atomic skill governance</code> — Atomic-Probe Governance, Skill Updates — 기존 BLADE·SymSkill 결을 \"frozen → 동적 lifecycle\"로 끌어올리는 새 line</li>')
    parts.append('<li><code>health attendant LLM safety</code> — Benchmarking Safety of LLMs for Robotic Health Attendant — LLM-as-controller의 robotic embodiment 측 safety가 표면화</li>')
    parts.append('</ul>')
    parts.append('<p><strong>④ 같은 단어 다른 맥락</strong></p>')
    parts.append('<ul>')
    parts.append('<li><code>world model</code>: CV는 \'VLM의 dynamic spatial reasoning 강화\'(World2VLM) / RO는 \'manipulation policy의 spatial-temporal action 모델링\'(STARRY) — 같은 단어가 \'reasoning prior\' vs \'action substrate\'로 정반대 측 활용</li>')
    parts.append('<li><code>diffusion</code>: CV는 \'image SR/T2I quality/DiT acceleration\'(L2P, ACPO, MetaSR) / RO는 \'one-step motion prediction with bounded latency\'(FlowS) — 같은 단어가 \'visual quality\' vs \'real-time prediction\'</li>')
    parts.append('<li><code>safety</code>: CV는 \'adversarial patch defense, OOD via SAE, deepfake forensic fingerprint\' / RO는 \'LLM health attendant harmful-instruction benchmark, NeRF safety reachable set\' — \'시각 모델 robustness\' vs \'physical actuation guarantee\'로 정반대 측 결</li>')
    parts.append('</ul>')
    parts.append('</div>')
    parts.append('<p>오늘의 CV/RO 교집합은 <em>world model이 단순 generation을 넘어 \"action·VLM·spatial reasoning의 공통 substrate\"가 되는 흐름</em>이에요. CV쪽은 World2VLM/Lifting Embodied가 \"VLM의 reasoning 능력 강화 substrate\"로 쓰고, RO쪽 STARRY/X-WAM은 \"action의 spatial-temporal 구조 substrate\"로 씁니다. 어제까지 \"VLA execution paradigm\"이 변곡점이었다면, 오늘은 그 한 단계 위 — \"VLA가 의존하는 world model 자체가 foundation layer로 굳는다\"는 단계입니다. 이 흐름은 향후 6개월 community 공통 키워드가 될 것 같습니다.</p>')

    # 인사이트
    parts.append('<h2>💡 오늘의 인사이트</h2>')
    parts.append('<div class="insight"><h3>World model이 \"foundation layer\"로 굳는 단계 진입 — action·VLM·spatial reasoning 세 축이 한 날 동시 등장</h3><p>오늘 <a href="https://arxiv.org/abs/2604.26694">X-WAM</a>이 4D world action modeling으로 video synthesis + 3D reconstruction + robotic action을 하나로 묶고, <a href="https://arxiv.org/abs/2604.26848">STARRY</a>는 spatial-temporal action-centric world modeling으로 VLA가 action-relevant 구조를 명시 모델링하게 만들었으며, <a href="https://arxiv.org/abs/2604.26934">World2VLM</a>은 world model의 미래 상상을 VLM에 distill해 dynamic spatial reasoning 강화. 거기에 <a href="https://arxiv.org/abs/2604.26182">Lifting Embodied World Models</a>까지 — 한 날 4편이 서로 다른 axis로 \"world model을 substrate로 삼는다\"는 paradigm을 동시 점화. 어제까지 VLA execution paradigm(Libra-VLA·DiscreteRTC) 흐름이 \"실행 layer\"였다면, 오늘은 그보다 한 층 더 아래 — \"world model 자체가 foundation\"이라는 단계입니다. 우리 manipulation/VLM 스택이 어떤 world model 위에 서 있는지 audit이 절실해진 시점이에요.</p></div>')
    parts.append('<div class="insight"><h3>VLM 평가가 \"calibration\" → \"epistemic honesty(무엇을 아는가/모르는가)\" 한 단계 더 깊이</h3><p>어제 <a href="https://arxiv.org/abs/2604.25235">VLM-Judges-Cannot-Score</a>·XTC-Bench가 \"평가 framework의 calibration\"이었다면, 오늘은 그 한 axis 더 깊이 — \"VLM이 무엇을 아는가/모르는가\"가 정조준돼요. <a href="https://arxiv.org/abs/2604.26419">Delineating Knowledge Boundaries</a>는 \"hallucinate + 거절 못함\" 두 axis를 함께, <a href="https://arxiv.org/abs/2604.26283">MedSynapse-V</a>는 의료 VLM의 cognitive misalignment를 latent memory로, <a href="https://arxiv.org/abs/2604.26288">CheXthought</a>는 의사의 visual attention과 CoT를 데이터로, <a href="https://arxiv.org/abs/2604.26614">State Beyond Appearance</a>는 \"외형 vs 상태 일관성\"을 분리. 5편이 한 날 \"epistemic honesty\"라는 새 axis로 수렴하는 건 우연이 아닙니다. evaluation 인프라를 갖춘 랩이라면 \"hallucination test → knowledge boundary test\"로 한 단계 끌어올리는 게 가장 빠른 follow-up 자리예요.</p></div>')
    parts.append('<div class="insight"><h3>3DGS deployment 라인이 \"렌더링 quality\" 다음으로 \"production cost\"를 community focal point로 굳히는 신호</h3><p>오늘 <a href="https://arxiv.org/abs/2604.26238">EnerGS</a>가 partial LiDAR prior 기반 energy formulation으로 학습 안정성을 끌어올리고, <a href="https://arxiv.org/abs/2604.26799">MesonGS++</a>는 post-train compression의 hyperparameter searching을 자동화. 거기에 <a href="https://arxiv.org/abs/2604.25936">SAND</a>가 implicit query cost를 spatially-adaptive depth로 가속. 3D/Scene 버킷이 한 주 +16%(37→43)로 꾸준히 누적되는 흐름 위에서 \"품질이 아닌 cost\"를 정조준한 결이 한 날 3편 동시 등장하는 건, deployment focal point가 \"무엇을 그리나\"에서 \"얼마나 싸게 그리나\"로 옮겨갔다는 변곡점 신호. 솔직히 이건 한동안 갈 것 같고, 우리 3D 스택이 production cost 측에서 어디 위치해 있는지 audit 후보로 즉시.</p></div>')

    # 추천 연구주제
    parts.append('<h2>🔬 추천 연구주제</h2>')
    parts.append('<div class="topic"><h3>World Model Atlas — \"VLM·VLA·embodied\" 세 axis 위에서 같은 world model이 substrate로 어디까지 호환되나</h3><p>오늘 X-WAM(robot action) · STARRY(VLA 강화) · World2VLM(VLM 강화) · Lifting Embodied(planning/control)이 모두 world model을 substrate로 쓰지만, 같은 world model 위에서 \"VLM 강화 vs VLA 강화 vs planning 효율\" 세 axis가 어떻게 trade-off되는지 통합 비교는 비어 있어요. 우리 랩이 video diffusion/world model 인프라를 갖췄다면 \"동일 backbone × 세 downstream\" atlas를 빠르게 만들 수 있고, 4~6주 안에 community standard 후보. 특히 어제 VLA execution paradigm 흐름과 결합하면 \"world model × execution paradigm × downstream task\" 3축 atlas로 즉시 가치가 있는 reference.</p></div>')
    parts.append('<div class="topic"><h3>VLM Epistemic Honesty Suite — Hallucination·Knowledge-Boundary·State-Consistency·Calibration 4 axis 통합</h3><p>오늘 Delineating Knowledge Boundaries · MedSynapse-V · CheXthought · State Beyond Appearance와 어제 VLM-Judges-Cannot-Score · POPE 등을 흩어진 axis에서 묶으면, \"VLM이 무엇을 아는가/모르는가\"의 표준 진단 suite가 가능합니다. \"hallucination · knowledge boundary · state consistency · judge calibration\" 4 axis로 묶어 medical/embodied/general 측 deployment 모두 reference할 수 있는 결. POPE가 hallucination에 한 일을 \"epistemic honesty\" 축에서 반복할 자리고, evaluation 인프라가 있는 랩이면 first-mover 위치를 잡을 수 있는 결입니다.</p></div>')
    parts.append('<div class="topic"><h3>3DGS Production Cost Atlas — Compression·Energy·Quantization × 표준 벤치마크 trade-off</h3><p>오늘 MesonGS++(post-train compression) · EnerGS(energy formulation으로 학습 안정 + LiDAR partial) · SAND(implicit query 가속)이 \"3DGS의 production cost\"를 다른 axis에서 정조준했지만, 같은 ScanNet++/Mip-NeRF 360 위에서 통합 trade-off 비교는 비어 있어요. \"compression ratio × 학습 안정성 × inference latency × 품질\" 4축 atlas로 묶으면 3DGS deployment 측 가장 빠르게 인용을 모을 자리고, 6주 내 community focal point로 굳을 가능성이 큽니다. 우리 랩이 3D 인프라를 가졌다면 즉시 후보.</p></div>')

    # 회고 — 목요일이라 skip
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
    parts.append(f'<p>🔥 <span class="hot">TOP3</span>: {top3[0][0]} ({top3[0][1]}), {top3[1][0]} ({top3[1][1]}), {top3[2][0]} ({top3[2][1]}) · ❄️ <span class="cold">BOTTOM2</span>: {bot2[0][0]} ({bot2[0][1]}), {bot2[1][0]} ({bot2[1][1]}). 오늘은 Safety가 21편으로 1위에 올라온 게 가장 큰 변화고(어제 11편 → +91%), 3D/Scene이 15편으로 어제(7편) 대비 두 배 회귀. 반면 Efficiency가 10편으로 어제(19편) 절반 수준이고 Embodied AI는 3편으로 한 주 내내 가장 조용한 자리예요. 어제 우려한 \"FM 단독 모델 라인 식어가는\" 흐름은 12편으로 누적 51→46(-10%) 동조하지만, 그 자리에 \"VLM honesty\" 세부 결들이 들어와 무게중심이 옮겨간 모양새입니다.</p>')

    # 델타 (vs 어제)
    parts.append('<p>📈 <strong>주간 델타(2026-04-29 → 2026-04-30, 1일 시야)</strong>: 🚗 Autonomous Driving <span class="hot">+25%</span> (16→20), 📦 3D/Scene <span class="hot">+16%</span> (37→43), 🎨 Generation <span class="hot">+15%</span> (66→76), 🏃 Embodied AI <span class="hot">+7%</span> (15→16), 🤖 Robot Learning <span class="cold">-8%</span> (53→49), 🧠 Foundation Models <span class="cold">-10%</span> (51→46), ⚡ Efficiency <span class="cold">-20%</span> (25→20), 🛡️ Safety/Alignment <span class="cold">-61%</span> (67→26). Generation +15%로 한 주 내내 1위를 강화하는 신호가 가장 명확하고, AD +25%로 어제 흐름 유지. Safety의 -61% 급락은 keyword 매칭 차이가 큰 변수라 내일 한 번 더 봐야 정확히 판단 가능하지만, 그렇더라도 26편으로 여전히 상위 자리는 지키고 있어요. 이번주 누적 패턴은 \"Generation·Safety가 양강 구도\"에서 \"Generation 단강 + Safety 호흡 조절\"로 다시 옮겨가는 모양새입니다.</p>')

    # 벤치마크 SOTA — 신규 SOTA 보고 없음
    parts.append('<h2>📈 벤치마크 SOTA 추이</h2>')
    parts.append('<p>이번주 추적 벤치마크(ScanNet++·LIBERO·nuScenes·MMMU·VBench 등)에서 새 SOTA 수치 보고는 잡힌 게 없습니다. 어제 KinDER가 새 \"physical reasoning\" 평가 카테고리를 정의했고, 오늘 <a href="https://arxiv.org/abs/2604.26567">AirZoo</a>는 \"aerial geometric 3D vision\"이라는 새 데이터셋 카테고리를 정의해 향후 벤치 측 reference로 가치가 있을 결. <a href="https://arxiv.org/abs/2604.26288">CheXthought</a>도 medical VLM evaluation의 ground truth axis(visual attention + CoT)를 새로 만든 결로, 표준 벤치보다 \"새 axis 정의\"가 일주일 내내 더 활발한 모양새. 다음주 LIBERO/MMMU 측 결과 누적되면 표 갱신할게요.</p>')

    # 크로스오버 페어
    parts.append('<h2>🔀 크로스오버 페어</h2>')
    parts.append('<div class="crosspair"><h3>같은 world model, 다른 substrate — World2VLM(CV) vs STARRY(RO)</h3><p><a href="https://arxiv.org/abs/2604.26934">World2VLM</a>(CV)이 world model의 \"미래 상상\" 능력을 VLM에 distill해 dynamic spatial reasoning을 강화하고, 같은 날 <a href="https://arxiv.org/abs/2604.26848">STARRY</a>(RO)는 spatial-temporal action-centric world modeling으로 manipulation policy가 action-relevant 구조를 명시 모델링하게 만들었어요. 양쪽 모두 \"world model이 downstream의 substrate\"라는 같은 paradigm을 공유하지만, CV는 \"reasoning prior 강화\" RO는 \"action 구조 substrate\"로 정반대 측 활용. 같은 substrate가 두 modality에서 동시 표면화하는 건 \"world model = foundation layer\"라는 변곡점이 community 양쪽에서 공감대를 얻은 신호로 봅니다.</p></div>')
    parts.append('<div class="crosspair"><h3>긴 horizon navigation — Three-Step Nav(CV/RO) vs Walk With Me(RO)</h3><p><a href="https://arxiv.org/abs/2604.26946">Three-Step Nav</a>(CV/RO)이 zero-shot vision-and-language navigation을 hierarchical global-local planner(3단계)로 분해해 MLLM의 step-wise 한계를 끄고, 같은 날 <a href="https://arxiv.org/abs/2604.26839">Walk With Me</a>(RO)는 open-world outdoor의 long-horizon social navigation을 \"high-level NL intention → safe long-horizon socially-compliant\"로 풀어요. 둘 다 \"긴 시간 + 긴 거리에서 instruction을 어떻게 풀 것인가\"라는 같은 문제 인식을 공유하지만, CV는 \"hierarchical planning을 통한 zero-shot generalization\" RO는 \"social-compliance를 통한 outdoor deployment\"로 측면 차이. 같은 문제가 두 axis에서 동시 등장하는 건 \"long-horizon nav이 navigation community의 다음 standard 자리\"가 굳어가는 신호.</p></div>')

    # Must-read
    parts.append('<h2>🌟 오늘의 must-read</h2>')

    parts.append('<div class="mustread">')
    parts.append('<h3>① Unified 4D World Action Modeling from Video Priors with Asynchronous Denoising (X-WAM) <span class="badge badge-cvro">CV/RO</span></h3>')
    parts.append('<p><a href="https://arxiv.org/abs/2604.26694">arxiv:2604.26694</a> · 저자 Jun Guo et al. · abstract 기반</p>')
    parts.append('<div class="section-title">핵심 주장</div>')
    parts.append('<p>기존 unified world model(예: UWM)은 2D pixel-space만 모델링해 \"4D 합성 + 실시간 action\"을 동시에 처리하지 못했어요. X-WAM은 video + 3D reconstruction + robot action을 하나의 framework로 묶고, asynchronous denoising으로 \"high-fidelity 4D synthesis\"와 \"real-time action execution\" 사이의 fundamental tension을 해결합니다. 기존엔 \"world generation은 느리고 정확, action은 빠르고 단순\"이었는데, X-WAM은 두 timescale을 비동기 denoising으로 분리하면서 video prior에서 직접 action을 distill — \"world model이 generation을 넘어 action의 substrate가 된다\"는 paradigm의 가장 분명한 결입니다.</p>')
    parts.append('<div class="section-title">방법의 핵심 (직관)</div>')
    parts.append('<pre># 기존 UWM 류: 2D pixel만 모델링\nfor t in range(horizon):\n    pixel[t] = world_model_2d(pixel[t-1], action[t-1])\n# 한계: 3D geometry/long-horizon physics 미반영,\n#       action은 별도 policy network에서 분리 학습\n\n# X-WAM: 4D unified + asynchronous denoising\n# Slow branch (high-fidelity 4D synthesis):\nvideo, recon3d = denoise_4d(noise, condition, K_slow_steps)\n# Fast branch (real-time action):\naction = denoise_action(video_prior, K_fast_steps)\n# Asynchronous: slow updates every K steps, fast every step\n# Key: action distilled from SAME video prior</pre>')
    parts.append('<div class="section-title">약점·한계</div>')
    parts.append('<p>(a) \"video prior로부터 action distill\"의 정량 gain이 abstract만으론 single-task에서 unified vs separate trained 비교가 명확하지 않아, multi-task 학습의 평균 효과인지 individual task 성능인지 본문 정독 필요. (b) Asynchronous denoising의 동기화 jitter가 실 hardware deployment 시 어디까지 robust한지 — 어제 Libra-VLA·DiscreteRTC와 같은 paradigm 측 결로, 세 paradigm 사이 정량 비교가 community 표준화에 결정적. (c) 4D 합성과 action distill의 학습 cost 비교 — \"하나의 framework\"라는 marketing 주장이 학습 efficiency 측에서도 유효한지 확인 필요. (d) 3D reconstruction 품질이 video synthesis quality와 trade-off되는 자리도 ablation 필수.</p>')
    parts.append('<div class="section-title">랩 파이프라인 영향</div>')
    parts.append('<p>VLA 기반 manipulation 스택을 굴리는 랩이라면 architecture 측에서 즉각 audit 후보입니다. \"video diffusion + action policy 분리\" 학습이 unified로 묶을 때 어떤 trade-off가 생기는지가 우리 long-horizon manipulation 시나리오에 직접 영향. 어제 Libra-VLA(dual-system) · DiscreteRTC(discrete diffusion) · 오늘 X-WAM(unified 4D)의 세 paradigm 사이에서 우리 task가 어디 위치하는지 정량 비교가 첫 단계.</p>')
    parts.append('</div>')

    parts.append('<div class="mustread">')
    parts.append('<h3>② World2VLM: Distilling World Model Imagination into VLMs for Dynamic Spatial Reasoning <span class="badge badge-cv">CV</span></h3>')
    parts.append('<p><a href="https://arxiv.org/abs/2604.26934">arxiv:2604.26934</a> · 저자 Wanyue Zhang et al. · abstract 기반</p>')
    parts.append('<div class="section-title">핵심 주장</div>')
    parts.append('<p>VLM이 정적 visual understanding에는 강하지만 \"dynamic spatial reasoning\" — egocentric motion 하의 scene evolution 상상 — 은 약하다는 진단에서 출발해, world model의 \"미래 상상\" 능력을 VLM에 distill하는 framework. 기존엔 \"spatial 데이터 scaling\"이나 \"world model을 별도 inference time에 호출\"이었는데, World2VLM은 학습 단계에서 distillation으로 \"VLM이 정적 representation 안에 dynamic prior를 흡수\"하게 만듭니다. \"world model = foundation layer\"라는 흐름의 가장 직접적 결로, X-WAM이 action 측 substrate라면 World2VLM은 reasoning 측 substrate.</p>')
    parts.append('<div class="section-title">방법의 핵심 (직관)</div>')
    parts.append('<pre># 기존 VLM: 정적 visual understanding\nanswer = vlm(image, question)\n# 한계: \"이 장면이 5초 후 어떻게 변할까\" 같은 dynamic Q\n#       에선 정적 prior만 활용 — 깨짐\n\n# World2VLM: distill world model\'s imagination\nwm_traj = world_model.imagine(image, K_steps)  # future frames\nvlm_logits = vlm(image, question)\nteacher_logits = vlm_with_traj(image, wm_traj, question)\nloss = KL(vlm_logits, teacher_logits)\n# 학습 후: vlm 단독으로도 dynamic prior가 weight 안에</pre>')
    parts.append('<div class="section-title">약점·한계</div>')
    parts.append('<p>(a) \"world model imagination\"의 품질이 VLM 학습 시그널의 ceiling을 결정 — 부정확한 future trajectory를 distill하면 VLM이 wrong dynamic prior를 internalize할 위험. (b) Distillation이 정적 visual understanding 성능을 trade-off하는지 ablation 필수 — \"dynamic은 +X, static은 -Y\"의 trade-off가 명확해야 deployment 의사결정 가능. (c) Egocentric motion 시나리오 측 데이터 분포 bias가 클 가능성 — 일반화 axis 측 평가가 abstract만으론 안 보임. (d) STARRY/X-WAM과 같은 \"world model substrate\" 흐름 안에서 \"VLM에 distill하는 것이 가장 효율적인지\"가 다른 paradigm과 직접 비교돼야 의미.</p>')
    parts.append('<div class="section-title">랩 파이프라인 영향</div>')
    parts.append('<p>VLM 기반 spatial reasoning 스택을 굴리는 랩이라면 \"정적 prior만으로 부족한 자리\"를 audit하는 게 첫 단계. 특히 embodied AI/AD 측 시나리오에서 \"이 장면이 어떻게 evolve하나\" 류 query가 핵심인 경우, 우리 VLM이 정적 prior에만 의존하고 있는지 dynamic prior가 들어와 있는지 측정 가치 큰 결. 학습 인프라가 있다면 video diffusion → VLM distillation을 빠르게 prototype할 수 있습니다.</p>')
    parts.append('</div>')

    # 리스크 필터
    parts.append('<h2>⚠️ 리스크·한계 필터</h2>')
    parts.append('<div class="risk"><h3>X-WAM — \"하나의 framework로 4D + action 통합\" 클레임의 multi-task vs single-task 검증</h3><p><a href="https://arxiv.org/abs/2604.26694">X-WAM</a>이 video synthesis + 3D reconstruction + robotic action 셋을 하나로 묶었다고 하지만, 통합 학습이 individual task 성능을 trade-off 없이 보존하는지가 결정적이에요. multi-task 학습의 평균 효과로 \"통합되어 보이지만 individual에선 깨지는\" 패턴은 unified world model line의 흔한 silent failure. 본문에서 task-individual 측 성능 vs 통합 학습 측 성능 비교 + KinDER 같은 표준 벤치 위 ablation 정독 전엔 \"unified가 separate보다 우수\" 강한 결론은 잠정 보류.</p></div>')
    parts.append('<div class="risk"><h3>Delineating Knowledge Boundaries — \"hallucination + 거절 못함\" 두 axis 동시 풀이의 trade-off</h3><p><a href="https://arxiv.org/abs/2604.26419">Delineating Knowledge Boundaries</a>가 \"long-tail hallucination + 거절 못함\" 두 axis를 동시 정조준하지만, 이 두 axis는 본질적으로 trade-off 관계 — \"잘 거절하는 모델\"은 conservative해지면서 정상 query까지 거절하는 over-refusal이 silent killer. 본문에서 정상 query 측 거절율(false-refusal)과 hallucination 측 정량 trade-off가 정직하게 보고됐는지 확인 전엔 \"양 axis 동시 개선\" 강한 클레임 잠정 보류.</p></div>')
    parts.append('<div class="risk"><h3>QYOLO \"quantum inspired\" — marketing 측 표현일 가능성</h3><p><a href="https://arxiv.org/abs/2604.26435">QYOLO</a>의 \"quantum inspired shared channel mixing\"이라는 표현이 실제 quantum 알고리즘과의 정합성 측면에서 의심 여지가 있어요. 최근 quantum inspired 라인의 결들이 \"marketing 측 명명\" 패턴이 누적된 자리라, 본문의 정확한 mathematical formulation + 기존 channel mixing(MLP-Mixer 류) 대비 정량 gain이 어디서 오는지 정독 전엔 \"quantum이 본질적으로 기여한다\" 강한 클레임 잠정 보류. classic shared channel mixing과의 ablation이 결정적 자리.</p></div>')
    parts.append('<div class="risk"><h3>LLM Robotic Health Attendant Safety — 270 instruction sample size의 통계 power</h3><p><a href="https://arxiv.org/abs/2604.26577">Benchmarking Safety of LLMs for Robotic Health Attendant Control</a>이 270개 harmful instruction(9 카테고리)으로 평가하지만, 9 카테고리 × 30 sample/cat 정도 — robotic embodiment의 다양한 silent failure 자리(센서 noise·사용자 변형 instruction·multi-step interaction)를 cover하기에는 sample 분포 power가 부족할 가능성. \"safety가 poorly characterized\"라는 진단 자체는 가치 있지만, \"이 270 sample이 전체 deployment risk를 represent한다\"는 강한 클레임은 sample expansion 후속 결을 기다려 판단하는 게 안전.</p></div>')

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
