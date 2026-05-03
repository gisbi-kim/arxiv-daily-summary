#!/usr/bin/env python3
"""Generate posts/2026-05-03.html (Sunday — same Friday May 1 batch, fresh weekend angle)."""
import json, html, io, os, sys

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

DATE = "2026-05-03"
WEEKDAY = "일"
OUT = f"posts/{DATE}.html"

# Reuse identical CSS as 2026-05-01
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
.note-banner{background:linear-gradient(135deg,#eff6ff 0%,#dbeafe 100%);border:1px solid #93c5fd;border-radius:10px;padding:14px 22px;margin:0 0 22px;font-size:13.5px;color:#1e3a8a;line-height:1.65}
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

# Reuse identical SUMMARIES from 2026-05-01 (same arxiv batch)
exec(open('out/summaries_extract.py', encoding='utf-8').read())

def esc(s): return html.escape(s or '', quote=True)

def badge_html(p):
    b = p.get('badge','')
    cls = {'CV':'badge-cv','RO':'badge-ro','CV/RO':'badge-cvro'}.get(b,'badge-cv')
    return f'<span class="badge {cls}">{esc(b)}</span>'

def summary_for(arxiv_id, title):
    s = SUMMARIES.get(arxiv_id)
    if s: return s
    return "오늘 /new에 등록된 결로, abstract 정독 전엔 정확한 평가가 어려워 본문 확인 권장합니다."

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

    # Sunday note: arxiv has no weekend listings, so today's batch = Friday May 1
    parts.append('<div class="note-banner">📌 <strong>Sunday note</strong> · arXiv는 주말에 새 announcement를 내지 않아서 오늘의 /new 배치는 금요일 5월 1일자와 동일합니다(arxiv 페이지 헤더 \"Showing new listings for Friday, 1 May 2026\" 확인). 이 리포트는 같은 107편을 <strong>주말이 지난 시점에서 다시 본</strong> 회고이며, 주간 시야는 한 칸 앞으로 굴려 <strong>2026-04-27 → 2026-05-03</strong>로 갱신했습니다. 7일 전 동급 스냅샷(2026-04-26)과 비교한 델타도 새로 계산.</div>')

    parts.append('<div class="meta">')
    parts.append('<div><strong>시야:</strong> 주간 2026-04-27 ~ 2026-05-03 · 오늘 배치 cs.CV/new + cs.RO/new (Friday 5/1 listing)</div>')
    parts.append('<div><strong>소스:</strong> arxiv.org /list/cs.CV/new · /list/cs.RO/new (stdlib 파서 경유)</div>')
    parts.append('<div><strong>주간 규모:</strong> cs.CV 598편 · cs.RO 187편 (union ~785편 후보)</div>')
    parts.append('<div><strong>오늘 /new (=금요일 배치):</strong> cs.CV 166 + cs.RO 52 → 218 candidates → 132 ROI 매칭 → 107편 8개 ROI 버킷 선정</div>')
    parts.append('<div><strong>델타 기준:</strong> 7일 전 동급 스냅샷(2026-04-26 — 같은 1일 /new 단위)과 비교</div>')
    parts.append('</div>')

    # 주간 동향
    parts.append('<h2>🔭 주간 동향</h2>')
    parts.append('<p>주말이 지난 일요일 시점에서 같은 금요일 배치를 다시 보면, <strong>3D/Scene과 Robot Learning이 deployment 라인의 양 축으로 자리잡은 게 더 분명하게 보여요</strong>. 7일 전(2026-04-26 동급 스냅샷) 대비 3D/Scene이 <span class="hot">20편</span>으로 굳었고(7일 전 13편 → +54%), Robot Learning도 17편으로(+13%) 한 주 안에서 단단해진 자리. pastweek 598편(CV) + 187편(RO) 누적 안에서도 두 라인이 가장 dense한 자리고, 특히 sparse-view 3DGS 4편이 한 날 등장한 게 라인 성숙의 측면에서 가장 분명한 신호입니다. 한 주 더 지나면 ScanNet++/Mip-NeRF 360 측 새 SOTA 보고가 누적될 가능성이 높아 보여요.</p>')
    parts.append('<p>두 번째로 두드러지는 건 <strong>VLA reasoning paradigm의 \"latent CoT + RL\" 방향</strong>이에요. 주중(<a href="https://arxiv.org/abs/2604.28192">LaST-R1</a>) 등장 후 이틀이 지나도 같은 paradigm을 직접 반박하거나 대체하는 결이 안 보이는 자리(주말 사이라 어쩔 수 없지만), 즉 community가 \"이 paradigm을 받아들이고 다음 layer를 보러 갈\" 시간이 주어진 모양새. <a href="https://arxiv.org/abs/2604.27792">MotuBrain</a>의 unified video-action MoT와 <a href="https://arxiv.org/abs/2604.27472">PRTS</a>의 contrastive primitive reasoning이 같은 paradigm shift의 두 측면이고, 다음주 월~화 announcement에서 \"latent reasoning ablation\" 류 후속 결이 표면화하는지가 paradigm 정착 신호의 첫 단서가 될 것 같아요.</p>')
    parts.append('<p>한편 <strong>Safety/Alignment가 14편으로 일주일 만에 -48% cooling</strong>한 점은 일요일 시점에서도 변하지 않은 사실이라, 지난주 \"Safety surge\"가 일시적 burst였음이 더 분명해졌어요. 그 안에서 <a href="https://arxiv.org/abs/2604.27267">Prompt to Physical Actuation</a>(LLM-controlled robot의 architectural threat modeling)이 한 주 가장 substantive한 결로 남는데, 이건 \"safety 키워드 안에서도 image forensics 같은 잡음을 빼면 진짜 \'AI safety\' 결은 1~2편밖에 안 된다\"는 사실을 일깨워요. 우리 랩이 safety 라인에서 무엇을 follow할지 정할 때 \"키워드 surge\"보다 \"architecture/threat-model 측 결\"을 따로 골라야 한다는 결론이 일요일 회고 후 더 단단해졌습니다.</p>')

    # CV vs RO
    parts.append('<h2>📐 CV vs RO 대비</h2>')
    parts.append('<p>오늘 분포는 3D/Scene(20)·Robot Learning(17)·Foundation Models(16)·Generation(15)·Safety(14)·Autonomous Driving(11)·Efficiency(11)·Embodied AI(3) — 단일일 단위로 보면 \"deployment 측(3D + RL + AD)\"이 \"generation/perception 측(Gen + FM + Safety)\"과 거의 동률. pastweek 시야로 한 칸 미뤄서 보면 CV 598편 / RO 187편 (3.2:1)로 CV가 압도적인데, 오늘 배치만 보면 RL의 RO 비중이 11/17(65%)·AD의 RO 비중 6/11(55%)로 \"deployment 라인은 RO가 주도\"하는 게 분명하게 드러나요. \"CV가 만들고 RO가 굴린다\"는 community 노동 분업이 한 날 batch에 압축돼 보이는 자리.</p>')
    parts.append('<div class="contrast">')
    parts.append('<p><strong>① 공통으로 뜨는 키워드</strong></p>')
    parts.append('<ul>')
    parts.append('<li><code>3DGS</code> — CV(<a href="https://arxiv.org/abs/2604.27422">Sparse-View in the Wild</a>·<a href="https://arxiv.org/abs/2604.27437">Softmax-GS</a>·<a href="https://arxiv.org/abs/2604.27552">Residual GS</a>·<a href="https://arxiv.org/abs/2604.28016">Faster Convergence</a>) + RO(<a href="https://arxiv.org/abs/2604.28111">GSDrive</a>) — CV는 \"sparse view + 효율\", RO는 \"RL training environment\"로 같은 기술을 다른 layer에서 활용 (이 분기는 한 주 내내 안 좁혀짐)</li>')
    parts.append('<li><code>world model + action</code> — CV(<a href="https://arxiv.org/abs/2604.28196">HERMES++</a>·<a href="https://arxiv.org/abs/2604.28185">Visual Generation taxonomy</a>) + RO(<a href="https://arxiv.org/abs/2604.27792">MotuBrain</a>·<a href="https://arxiv.org/abs/2604.28192">LaST-R1</a>·<a href="https://arxiv.org/abs/2604.27472">PRTS</a>) — \"substrate\" 흐름 위에서 \"reasoning + action\" 측 후속 — 이틀이 지나도 두 진영 통합 결은 아직 안 등장</li>')
    parts.append('<li><code>tactile / contact-rich</code> — RO(<a href="https://arxiv.org/abs/2604.27367">DOT-Sim</a>·<a href="https://arxiv.org/abs/2604.27224">Tactile Quadruped</a>·<a href="https://arxiv.org/abs/2604.28156">FlexiTac</a>·<a href="https://arxiv.org/abs/2604.27175">KernelSOS contact-rich</a>) — sim 측·real 측·planning 측이 한 날 같이 등장 — 라인 성숙의 분명한 신호</li>')
    parts.append('</ul>')
    parts.append('<p><strong>② CV에만 뜨는 키워드</strong></p>')
    parts.append('<ul>')
    parts.append('<li><code>AI-image forensics</code> — <a href="https://arxiv.org/abs/2604.27590">Fake3DGS</a>·<a href="https://arxiv.org/abs/2604.27875">Frequency-Aware Detection</a>·<a href="https://arxiv.org/abs/2604.27903">HiMix</a>·<a href="https://arxiv.org/abs/2604.28177">AEGIS</a> — 한 날 4편 + 3DGS forensic까지 — \"safety\" 라벨의 핵심 잡음 자리</li>')
    parts.append('<li><code>VLM evaluation 인프라</code> — <a href="https://arxiv.org/abs/2604.27389">COHERENCE</a>·<a href="https://arxiv.org/abs/2604.27604">SPUR</a>·<a href="https://arxiv.org/abs/2604.27974">FineState-Bench</a>·<a href="https://arxiv.org/abs/2604.27553">Visual Text Style</a> — interleaved/scientific/GUI/style 4 axis</li>')
    parts.append('<li><code>video generation refinement</code> — <a href="https://arxiv.org/abs/2604.28078">AesRM</a>·<a href="https://arxiv.org/abs/2604.28169">PhyCo</a>·<a href="https://arxiv.org/abs/2604.28126">AdvDMD</a> — photorealism 너머 \"aesthetics·physics·distillation\"로 한 단계 위</li>')
    parts.append('</ul>')
    parts.append('<p><strong>③ RO에만 뜨는 키워드</strong></p>')
    parts.append('<ul>')
    parts.append('<li><code>tactile sensor 인프라</code> — <a href="https://arxiv.org/abs/2604.27367">DOT-Sim</a>(sim) + <a href="https://arxiv.org/abs/2604.28156">FlexiTac</a>(real) — sim/real 양쪽 인프라가 같은 날 등장</li>')
    parts.append('<li><code>deformable / dexterous manipulation</code> — <a href="https://arxiv.org/abs/2604.28161">RopeDreamer</a> DLO·<a href="https://arxiv.org/abs/2604.27557">Dexterous Co-Design</a>·<a href="https://arxiv.org/abs/2604.27175">KernelSOS</a> — \"hard manipulation\" 자리</li>')
    parts.append('<li><code>UAV swarm / autonomous fleet</code> — <a href="https://arxiv.org/abs/2604.27935">Active Inference UAV Swarm</a>·<a href="https://arxiv.org/abs/2604.28057">Marshaling Yard Delivery</a></li>')
    parts.append('<li><code>LLM threat modeling</code> — <a href="https://arxiv.org/abs/2604.27267">Prompt to Physical Actuation</a> — LLM-as-controller의 architectural risk를 처음으로 통합 분석</li>')
    parts.append('</ul>')
    parts.append('<p><strong>④ 같은 단어 다른 맥락</strong></p>')
    parts.append('<ul>')
    parts.append('<li><code>3DGS</code>: CV는 \'sparse view + production cost\'(렌더링 품질) / RO는 \'closed-loop RL training environment\'(GSDrive처럼 simulation substrate) — 같은 기술이 \"asset\" vs \"environment\"로 정반대 layer 활용</li>')
    parts.append('<li><code>world model</code>: CV는 \'driving scene understanding + generation 통합\'(HERMES++) / RO는 \'video-action unified 정책 학습\'(MotuBrain·LaST-R1) — \"perception + prediction\" vs \"perception + action\"</li>')
    parts.append('<li><code>safety</code>: CV는 \'AI-image forensics·OOD\' (Fake3DGS·AEGIS·HiMix) / RO는 \'physical actuation 측 architectural risk\'(<a href="https://arxiv.org/abs/2604.27267">Prompt-to-Actuation</a>·<a href="https://arxiv.org/abs/2604.27728">Dependability Cage</a>) — \"위조 검출\" vs \"행동 결과 통제\"로 정반대</li>')
    parts.append('</ul>')
    parts.append('</div>')
    parts.append('<p>이틀이 지난 일요일 시점에서 위 ①~④를 다시 보니 <em>\"같은 단어 다른 맥락\"이 한 주 사이에 좁혀진 자리는 거의 없다</em>는 게 흥미로워요. CV/RO가 동시에 같은 키워드를 다루지만 두 진영이 서로의 결을 직접 인용하거나 통합하는 결은 한 주 내내 안 등장 — 이건 community가 아직 두 layer를 \"separate concerns\"로 보고 있다는 신호. 우리 랩이 양쪽을 다 들여다보는 입장이라면, \"두 진영의 같은 단어가 만나는 통합 평가\"를 제안하는 게 향후 6개월 가장 빠른 차별화 자리예요.</p>')

    # 인사이트 (Sunday angle)
    parts.append('<h2>💡 오늘의 인사이트</h2>')
    parts.append('<div class="insight"><h3>같은 batch을 이틀 후 회고해도 \"latent CoT + RL\"이 VLA paradigm shift의 분명한 결로 살아있음</h3><p><a href="https://arxiv.org/abs/2604.28192">LaST-R1</a> + <a href="https://arxiv.org/abs/2604.27792">MotuBrain</a> + <a href="https://arxiv.org/abs/2604.27472">PRTS</a> 셋이 \"VLA reasoning을 어디서 표현할 것인가\"를 다른 axis로 정조준한 게 일요일 시점에서 더 또렷이 보여요. 같은 paradigm을 직접 반박하거나 우회하는 결이 주말 사이에 등장하지 않은 자리(arxiv 주말 휴식 때문이긴 하지만), 즉 community가 \"reading + digestion\" 시간에 들어간 모양새. <em>다음주 월·화 announcement에서 latent reasoning ablation·comparison 류 후속이 안 나오면</em> 이 paradigm은 \"제안만 있고 검증은 다른 랩 몫\"으로 굳을 risk — 우리 랩이 latent CoT 측 비교 실험을 빠르게 굴릴 수 있다면 first follower 자리가 비어있어요.</p></div>')
    parts.append('<div class="insight"><h3>\"Safety surge\" -48%는 일시적 burst였고, 진짜 safety 결은 architecture-level 1~2편 — 키워드 vs architecture를 분리해 봐야 함</h3><p>일요일 회고 후 더 분명해진 건 \"Safety/Alignment\" 라벨이 27→14편으로 cool했지만, 그 14편 안에서 우리 ROI에 진짜 substantive한 결은 <a href="https://arxiv.org/abs/2604.27267">Prompt to Physical Actuation</a>(LLM-controlled robot architectural threat) 1편 + <a href="https://arxiv.org/abs/2604.27508">SASI</a>(early action recognition for HRI)·<a href="https://arxiv.org/abs/2604.28197">OmniRobotHome</a>(multiadic HRI) 정도. 나머지는 medical/forensics/generic robustness — 키워드는 safety지만 \"AI safety/policy 안전성\" 결은 거의 없어요. 우리 랩이 safety follow할 때 \"키워드 surge 추적\"으로는 잡히지 않고, <em>STRIDE/threat-model/architectural-failure 류 결만 따로 추출하는 별도 필터</em>가 필요하다는 결론이 일요일 시점에서 단단해졌습니다.</p></div>')
    parts.append('<div class="insight"><h3>3D/Scene + AD + RL 3축 surge가 일요일에도 변함없이 deployment 측 무게중심을 잡고 있음</h3><p>금요일 시점에서 잡혔던 \"3D/Scene +54% · AD +57% · RL +13%\" 3축 surge가 일요일에도 그대로 유지됐고(주말이라 어차피 변할 일 없지만), pastweek 598+187편 누적 안에서도 deployment 측 결이 가장 dense한 자리로 굳어요. 어제 GSDrive·HERMES++ + 오늘(=금요일) sparse-view 3DGS 4편 + LaST-R1까지 \"physical world deployment\"라는 한 narrative 위에서 일관되게 누적되는 결이라, 이건 한 주 burst가 아니라 <em>community 무게중심의 진짜 이동</em>으로 봐야 할 것 같아요. 우리 랩이 perception-only 측에 무게가 있다면 이번주 안에 deployment 측 paper 1편의 audit이 시급한 시점.</p></div>')

    # 추천 연구주제 (Sunday angle — emphasize gaps that pastweek made obvious)
    parts.append('<h2>🔬 추천 연구주제</h2>')
    parts.append('<div class="topic"><h3>VLA Reasoning Atlas — Linguistic CoT vs Latent CoT vs Continuous Latent × LIBERO/CALVIN/RoboCasa (일요일 시점에서 더 시급)</h3><p>한 주 회고 후에도 LaST-R1·MotuBrain·PRTS가 다른 axis로 같은 paradigm을 정조준했지만 정량 비교가 비어 있는 자리. 일요일까지도 후속 ablation 결이 안 나온 자리라, <em>지금이 first-mover 자리가 가장 비어있는 타이밍</em>이에요. \"linguistic CoT vs latent CoT vs continuous latent vs no reasoning\" 4 paradigm × 3 표준 벤치 atlas로 묶으면 향후 6주 안에 community standard 후보. LaST-R1의 99.8% LIBERO ceiling이 진짜 ceiling인지, 아니면 paradigm bias로 뜬 수치인지가 atlas에서 결정 — 우리 VLA 인프라가 있다면 이번주 sprint 시작이 적절한 시점.</p></div>')
    parts.append('<div class="topic"><h3>Sparse-View 3DGS Robustness Suite — In-the-Wild × Generalizable × Domain-Transfer atlas</h3><p>오늘 sparse-view 3DGS 4편이 모두 다른 \"sparse\" 정의로 정조준한 자리에서, ScanNet++/Mip-NeRF 360 위 통합 robustness suite는 여전히 비어 있어요. 일요일 회고 후 더 명확해진 건 4편의 평가 프로토콜이 너무 달라 community가 \"누가 진짜 sparse-view에서 robust한가\" 비교를 못 하는 자리 — 이건 통합 벤치 제안의 timing이 가장 좋은 자리. 4 axis(view 수 / illumination / data quantity / domain) × 2 표준 데이터셋 통합 suite paper 1편으로도 6주 안에 인용 모일 자리예요.</p></div>')
    parts.append('<div class="topic"><h3>LLM-Robot Threat Audit Framework — STRIDE × DFD × 우리 랩 LLM-controlled robot 시스템 case study</h3><p><a href="https://arxiv.org/abs/2604.27267">Prompt to Physical Actuation</a>이 LLM-enabled robot의 첫 architectural threat model을 정의했지만 \"실제 lab 시스템에 적용한 case study\"는 비어 있고, 일요일까지도 그 자리는 비어 있어요. 같은 STRIDE-per-interaction framework로 \"우리 시스템의 boundary 어디가 attack chain의 weak point인가\"를 audit한 case study paper가 즉시 가치. 일반 cybersecurity audit과 다른 \"physical world consequence\" 측 정량 평가 framework가 동시에 필요한 자리고, 이건 향후 1년 robotics safety 측 첫 표준이 될 가능성이 큽니다.</p></div>')

    # 회고 — 일요일이라 skip (월요일 실행에서만)

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
    parts.append(f'<p>🔥 <span class="hot">TOP3</span>: {top3[0][0]} ({top3[0][1]}), {top3[1][0]} ({top3[1][1]}), {top3[2][0]} ({top3[2][1]}) · ❄️ <span class="cold">BOTTOM2</span>: {bot2[0][0]} ({bot2[0][1]}), {bot2[1][0]} ({bot2[1][1]}). 일요일 회고 시점에서도 3D/Scene 단독 1위(7일 전 13편 → 오늘 20편, +54%) + AD +57%(7→11) + RL +13%(15→17) 3축 surge가 그대로 유지. Safety -48%(27→14)·Generation -25%(20→15)도 변함없어요. Embodied AI는 3편으로 한 주 내내 가장 조용한 자리.</p>')

    # 델타 (vs 7일 전)
    parts.append('<p>📈 <strong>주간 델타(2026-04-26 → 2026-05-03, 7일 시야 — 같은 1일 /new 단위)</strong>: 🚗 Autonomous Driving <span class="hot">+57%</span> (7→11), 📦 3D/Scene <span class="hot">+54%</span> (13→20), 🏃 Embodied AI <span class="hot">+50%</span> (2→3), 🤖 Robot Learning <span class="hot">+13%</span> (15→17), ⚡ Efficiency <span class="cold">+0%</span> (11→11), 🧠 Foundation Models <span class="cold">-16%</span> (19→16), 🎨 Generation <span class="cold">-25%</span> (20→15), 🛡️ Safety/Alignment <span class="cold">-48%</span> (27→14). 가장 명확한 신호는 \"AD·3D·Embodied\" 3축이 동시에 surge한 것 — 모두 \"physical world deployment\" 측 결이라는 공통점. 한 주 누적 패턴은 \"Generation·Safety 양강\"에서 \"deployment-heavy 3축\"으로 무게중심이 이동하는 모양새고, 일요일까지도 이 흐름이 변하지 않은 자리.</p>')

    # 벤치마크 SOTA
    parts.append('<h2>📈 벤치마크 SOTA 추이</h2>')
    parts.append('<table style="border-collapse:collapse;width:100%;font-size:13.5px;margin:12px 0">')
    parts.append('<thead><tr style="background:#f6f8fa;border-bottom:1px solid #d0d7de"><th style="text-align:left;padding:8px">벤치마크</th><th style="text-align:left;padding:8px">메트릭</th><th style="text-align:right;padding:8px">이번주 최고</th><th style="text-align:left;padding:8px;padding-left:14px">논문</th></tr></thead>')
    parts.append('<tbody>')
    parts.append('<tr style="border-bottom:1px solid #eaeef2"><td style="padding:8px"><strong>LIBERO</strong></td><td style="padding:8px">평균 SR</td><td style="padding:8px;text-align:right;font-family:ui-monospace,monospace">99.8%</td><td style="padding:8px;padding-left:14px"><a href="https://arxiv.org/abs/2604.28192">LaST-R1</a></td></tr>')
    parts.append('<tr style="border-bottom:1px solid #eaeef2"><td style="padding:8px"><strong>real-world manipulation (4 task)</strong></td><td style="padding:8px">improvement vs warm-up</td><td style="padding:8px;text-align:right;font-family:ui-monospace,monospace">+44%</td><td style="padding:8px;padding-left:14px"><a href="https://arxiv.org/abs/2604.28192">LaST-R1</a></td></tr>')
    parts.append('<tr style="border-bottom:1px solid #eaeef2"><td style="padding:8px"><strong>SAM3D-style sparse recon</strong></td><td style="padding:8px">Geometric quality</td><td style="padding:8px;text-align:right;font-family:ui-monospace,monospace">+30.1%</td><td style="padding:8px;padding-left:14px"><a href="https://arxiv.org/abs/2604.27106">RecGen</a></td></tr>')
    parts.append('<tr><td style="padding:8px"><strong>real-time VLA inference</strong></td><td style="padding:8px">speedup</td><td style="padding:8px;text-align:right;font-family:ui-monospace,monospace">50×</td><td style="padding:8px;padding-left:14px"><a href="https://arxiv.org/abs/2604.27792">MotuBrain</a></td></tr>')
    parts.append('</tbody></table>')
    parts.append('<p>일요일까지 같은 4건의 SOTA 보고가 그대로 유지. LIBERO 평균 99.8%는 ceiling 측 분명한 신호고, RecGen의 sparse recon +30.1%·MotuBrain 50× speedup도 baseline 정의 측 의심은 남지만 보고 자체는 강한 자리. ScanNet++/Mip-NeRF 360 측 새 SOTA 보고는 잡힌 게 없어, 표는 최소 보고만.</p>')

    # 크로스오버 페어
    parts.append('<h2>🔀 크로스오버 페어</h2>')
    parts.append('<div class="crosspair"><h3>같은 \"world model\", 다른 task layer — HERMES++(CV/AD) vs MotuBrain(RO)</h3><p><a href="https://arxiv.org/abs/2604.28196">HERMES++</a>(CV/AD)이 driving world model의 \"future scene generation\" + \"3D scene understanding\"을 한 framework로 통합하고, 같은 날 <a href="https://arxiv.org/abs/2604.27792">MotuBrain</a>(RO)은 video와 action을 UniDiffuser + 3-stream MoT로 unified 학습. 둘 다 \"world model을 단일 unified framework로\"라는 같은 paradigm을 공유하지만, HERMES++는 \"perception + prediction\"이고 MotuBrain은 \"perception + action\"이라 같은 단어가 \"이해 측\" vs \"행동 측\"으로 분기. 같은 paradigm이 두 측면에서 동시 표면화하는 건 \"world model = unified substrate\"가 community 양쪽에서 설계 표준이 되는 신호 — 일요일까지도 두 결을 직접 통합하는 결은 안 등장한 자리.</p></div>')
    parts.append('<div class="crosspair"><h3>3DGS의 두 활용 layer — Sparse-View Recon(CV) vs GSDrive(RO)</h3><p><a href="https://arxiv.org/abs/2604.28193">Generalizable Sparse-View Recon</a>(CV)이 unconstrained image에서도 generalizable한 3D recon을 정조준하고, 같은 날 <a href="https://arxiv.org/abs/2604.28111">GSDrive</a>(RO)는 같은 3DGS 기술을 driving policy의 RL training environment로 활용. 같은 기술이 \"asset 만들기\" vs \"closed-loop 학습 환경 substrate\"로 layer 자체가 다른 게 흥미롭네요. 3DGS가 \"렌더링 결과물\"에서 \"reusable infrastructure\"로 굳어가는 흐름의 양 측면 결로, 이건 향후 driving simulation·embodied data scaling 양 라인에 substrate가 됩니다.</p></div>')

    # Must-read
    parts.append('<h2>🌟 오늘의 must-read</h2>')

    parts.append('<div class="mustread">')
    parts.append('<h3>① LaST-R1: Reinforcing Action via Adaptive Physical Latent Reasoning for VLA Models <span class="badge badge-cvro">CV/RO</span></h3>')
    parts.append('<p><a href="https://arxiv.org/abs/2604.28192">arxiv:2604.28192</a> · 저자 Hao Chen et al. · abstract 기반</p>')
    parts.append('<div class="section-title">핵심 주장</div>')
    parts.append('<p>기존 VLA reasoning은 \"explicit linguistic CoT\"(latency·discretization 측 한계)나 \"continuous latent reasoning\"(static imitation에 갇힘) 둘 중 하나에 갇혔고, RL을 적용해도 vanilla action space만 최적화해 underlying physical reasoning을 우회한다는 진단에서 출발해요. LaST-R1은 latent CoT reasoning을 physical dynamics 위에서 굴리고, LAPO(Latent-to-Action Policy Optimization)로 \"reasoning과 action을 동시에\" RL 최적화 — 즉 VLA가 \"physical하게 생각\"하면서 \"환경 복잡도에 따라 reasoning horizon을 dynamic하게 조절\"하게 만들었습니다. LIBERO에서 평균 99.8% (one-shot warm-up만으로) + 실 환경 4 task에서 +44% — paradigm shift 측면 가장 분명한 결.</p>')
    parts.append('<div class="section-title">방법의 핵심 (직관)</div>')
    parts.append('<pre># 기존 VLA + RL: action space만 최적화\nfor episode in env:\n    a = pi(s)            # 정책 직접\n    update(pi, reward)    # vanilla PG/PPO\n# 한계: \"physical reasoning\"이 black box로 우회됨\n\n# LaST-R1: LAPO joint optimization\nfor episode in env:\n    z_cot = latent_cot(s, horizon=adaptive)  # physical dynamics\n    a = action_head(s, z_cot)                # latent CoT 조건\n    # joint update — reasoning + action 동시\n    update((latent_cot, action_head), reward)\n# adaptive horizon: complex env일수록 K_steps 더 많이</pre>')
    parts.append('<div class="section-title">약점·한계</div>')
    parts.append('<p>(a) LIBERO 99.8%는 \"평균\"이라 task-individual 측면 한계는 abstract만으론 안 보임 — 가장 어려운 individual task에서도 ceiling인지 본문 정독 필수. (b) \"adaptive latent CoT\"의 reasoning horizon 조절 mechanism이 \"실제로 환경 복잡도를 측정하는가\" vs \"학습 데이터 분포에 fit하는가\" 구분이 ablation의 핵심 자리 — overconfident horizon이 silent failure로 이어질 risk. (c) 실 환경 +44%가 \"single-arm + dual-arm\"이라는데 dual-arm이 단순 mirroring인지 진짜 협업 task인지가 generalization claim의 결정. (d) LAPO의 학습 비용이 vanilla VLA + RL 대비 어디쯤인지가 deployment 의사결정에 결정 — abstract엔 efficiency 비교가 약함.</p>')
    parts.append('<div class="section-title">랩 파이프라인 영향</div>')
    parts.append('<p>VLA + RL 인프라를 굴리는 랩이라면 즉각 paradigm 비교 후보예요. 어제 X-WAM·STARRY가 \"world model substrate\"였다면 오늘 LaST-R1은 그 위에서 \"reasoning을 어떻게 RL로 강화\"인데, 우리 VLA가 explicit CoT에 갇혀 있다면 latent CoT + joint RL로 audit이 첫 단계. 특히 \"long-horizon manipulation\"에 약한 우리 시나리오에서는 LAPO 류 joint optimization이 직접적 가치 — LIBERO ceiling은 닿았으니 CALVIN/RoboCasa 측에서 우리 task로 paradigm 비교가 즉시 가치 있는 작업입니다.</p>')
    parts.append('</div>')

    parts.append('<div class="mustread">')
    parts.append('<h3>② HERMES++: Toward a Unified Driving World Model for 3D Scene Understanding and Generation <span class="badge badge-cv">CV</span></h3>')
    parts.append('<p><a href="https://arxiv.org/abs/2604.28196">arxiv:2604.28196</a> · 저자 Xin Zhou et al. · abstract 기반</p>')
    parts.append('<div class="section-title">핵심 주장</div>')
    parts.append('<p>기존 driving world model은 future scene generation에 치우쳐 3D scene understanding이 약했고, LLM은 reasoning은 강하지만 future geometry 예측이 약한 \"semantic interpretation vs physical simulation\" 단절 문제가 있었어요. HERMES++는 \"BEV로 multi-view 공간을 LLM-호환 구조로 통합\" + \"LLM-enhanced world queries\" + \"Current-to-Future Link\" + \"Joint Geometric Optimization\"으로 두 task를 한 framework에서 굴립니다. 결과적으로 future point cloud prediction과 3D scene understanding 양 task에서 specialist 대비 outperform — driving WM이 \"generation-only\"에서 \"understanding + generation 통합\"으로 paradigm shift하는 측면 첫 분명한 결입니다.</p>')
    parts.append('<div class="section-title">방법의 핵심 (직관)</div>')
    parts.append('<pre># 기존 driving WM: future scene만\nfuture_scene = wm(past_scenes, action)\n# 한계: \"이 장면이 무엇을 의미하나\"는 별도 LLM이 이해\n\n# HERMES++: unified BEV + LLM + future geometry\nbev = bev_encode(multi_view_imgs)         # 공간 통합\nworld_q = llm_world_queries(bev, lang)     # LLM 강화\ncurrent_feat = understanding_branch(bev, world_q)\n# Current-to-Future Link\nfuture_feat = c2f_link(current_feat, world_q)\n# Joint Geometric Optimization (explicit + latent)\nloss = task_loss + lambda * geo_consist(future_feat)\n# 단일 모델이 \"이해\" + \"예측\"을 같이</pre>')
    parts.append('<div class="section-title">약점·한계</div>')
    parts.append('<p>(a) \"specialist 대비 outperform\"이 두 task 모두에서라는 abstract 클레임이 강한데, multi-task 학습은 종종 평균만 좋아지고 individual은 trade-off되는 silent failure가 흔함 — task별 개별 specialist 대비 정량 비교가 본문에서 명확해야 의미. (b) BEV-LLM coupling이 LLM의 hallucination을 future geometry로 흘릴 risk — \"LLM이 잘못 추론한 semantic\"이 future point cloud의 silent error로 이어지는 자리. (c) Closed-loop driving simulation(CARLA·nuPlan)에서의 평가가 abstract엔 없어 \"static prediction에서만 잘하나\"가 의심 자리 — CARLA closed-loop 측 결과가 결정적. (d) Joint geometric optimization의 hyperparameter sensitivity가 abstract만으론 안 보임.</p>')
    parts.append('<div class="section-title">랩 파이프라인 영향</div>')
    parts.append('<p>AD/driving world model 인프라를 굴리는 랩이라면 즉각 architecture 비교 후보. 우리 driving WM이 \"future scene generation\"만 하고 있다면 HERMES++ 류 unified framework로 audit이 첫 follow-up이고, BEV-LLM coupling이 우리 시스템에 transfer 가능한지가 핵심 질문. 특히 어제까지 driving 라인이 weekly +57% surge로 가장 빠른 자리라 community 표준이 빠르게 굳을 가능성 — 늦게 따라가면 비용 큰 자리예요.</p>')
    parts.append('</div>')

    # 리스크 필터
    parts.append('<h2>⚠️ 리스크·한계 필터</h2>')
    parts.append('<div class="risk"><h3>LaST-R1 99.8% \"평균\" 클레임 — task-individual 측면의 silent saturation 의심</h3><p><a href="https://arxiv.org/abs/2604.28192">LaST-R1</a>의 LIBERO 99.8% 평균 SR이 강한 클레임이지만, LIBERO suite는 task별 난이도 분포가 매우 unequal — 평균이 ceiling에 닿아도 hardest individual task에서 80%대일 가능성을 배제하기 어려워요. 특히 LIBERO-Long과 LIBERO-Goal 같은 hard subset이 평균 안에서 어떻게 분포되는지가 결정적. 본문에서 task-by-task breakdown + 가장 어려운 subset의 absolute SR + variance 정독 전엔 \"LIBERO solved\" 강한 결론은 잠정 보류, CALVIN/RoboCasa 같은 더 큰 suite에서의 ceiling 검증이 follow-up 자리.</p></div>')
    parts.append('<div class="risk"><h3>HERMES++ \"specialist 대비 outperform\" — multi-task 학습의 individual-task trade-off 의심</h3><p><a href="https://arxiv.org/abs/2604.28196">HERMES++</a>가 future point cloud prediction과 3D scene understanding 양 task 모두에서 specialist를 outperform한다고 하지만, multi-task framework가 평균에선 강하고 individual specialist 대비 일부 metric에서 깨지는 패턴은 driving WM line의 흔한 silent failure. 특히 understanding 측에서는 mAP/NDS, generation 측에서는 Chamfer/EMD 같은 metric이 trade-off 관계 가능성이 큰 자리. closed-loop 평가(CARLA/nuPlan)에서 specialist와의 정량 비교 + ablation 없이는 \"통합이 손해 없이 우월\" 강한 결론 보류.</p></div>')
    parts.append('<div class="risk"><h3>MotuBrain \"50배 speedup\" 클레임 — baseline 정의의 marketing 의심</h3><p><a href="https://arxiv.org/abs/2604.27792">MotuBrain</a>의 50배 speedup이 강한 인상을 주지만, 비교 baseline이 \"naive UniDiffuser inference\"인지 \"이미 가속된 video diffusion\"인지가 결정적이에요. 50배가 \"비효율적인 reference 대비\"면 marketing 측 표현일 가능성이 높고, 최신 distillation/few-step diffusion 대비라면 의미 있는 진보. 특히 \"three-stream MoT\"가 inference 시 어떻게 분기되는지가 latency 측면 핵심 — 본문의 정확한 latency profile + apples-to-apples baseline 정독 전엔 \"real-time deployment 가능\" 강한 결론 잠정 보류.</p></div>')
    parts.append('<div class="risk"><h3>Sparse-View 3DGS surge — 4편의 \"sparse view\" 정의 차이로 인한 평가 비교 어려움</h3><p>오늘 sparse-view 3DGS 4편(<a href="https://arxiv.org/abs/2604.27106">RecGen</a>·<a href="https://arxiv.org/abs/2604.27422">In the Wild</a>·<a href="https://arxiv.org/abs/2604.27552">Residual GS for CBCT</a>·<a href="https://arxiv.org/abs/2604.28193">Generalizable Sparse-View</a>)이 모두 \"sparse view\"를 정조준하지만, 각 paper의 \"sparse\" 정의가 다 달라요(view 수·illumination 변화·data quantity·domain). 같은 ScanNet++ 위 비교가 없어 community가 \"누가 진짜 sparse-view에서 robust한가\" 판단 못 하는 자리. 4편이 동시에 등장한 surge가 학술 가치 있는지, 아니면 단순 \"sparse\" 키워드의 ambiguity로 정의 다른 결이 한 자리에 모인 건지 한 주 더 누적 후 판단이 안전.</p></div>')

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
