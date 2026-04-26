#!/usr/bin/env python3
"""Generate posts/2026-04-26.html from out/classified.json"""
import json, html, re, os

DATE = "2026-04-26"
WEEKDAY = "일"
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

SUMMARIES = {
'2604.21182': "Unconstrained 사진 컬렉션에서 카메라·조명 미지인 채로 feed-forward 3DGS를 푸는 시도예요. Appearance embedding으로 빛 변화 modulation까지 잡아서, pose-free 3DGS 라인의 오늘자 후보로 보입니다.",
'2604.21387': "Point cloud edge detection을 local patch + transformer로 가볍게 잡는 실용 지향 논문. 산업용 3D inspection 같이 reliable edge가 필요한 데서 바로 가져다 쓸만한 결입니다.",
'2604.21400': "3DGS의 stochastic growth, sparsity shield, multi-sensor pollution을 'production-grade' 관점에서 정조준. Deterministic budget controller + Immersion v1.0 ultra-dense 데이터셋 공개로 학계-산업 격차를 벤치 레벨에서 깨려는 시도예요. 자기-벤치마크 이슈는 Risk 섹션 참고.",
'2604.21442': "Two-level LSH로 point cloud 인덱싱을 Kd-tree/Octree 대비 큰 폭으로 가속. 알고리즘 자체는 고전이지만 3DGS·SLAM 대형 scene 파이프라인에 붙이면 즉시 효과 나올 후보입니다.",
'2604.21575': "Multi-modal body fitting을 scale-agnostic dense landmark prediction으로 통합 — RGB·3D·depth 섞인 입력에 유연하게 대응합니다. Avatar·AR 도메인 실용 코너의 오늘 기여예요.",
'2604.21631': "Transient object가 섞인 multi-view 학습에서 pseudo-mask bootstrapping으로 3DGS 품질 보존. 'reconstruction failure를 피드백 시그널로' 쓰는 자기-개선 루프가 깔끔합니다.",
'2604.21712': "Monocular 3D human mesh recovery에서 discriminative·generative를 상보적으로 묶어 occlusion robustness 확보. HMR 계열 고질병을 structural prior로 완화한 결입니다.",
'2604.21713': "Feed-forward visual geometry estimation의 multi-frame vs single-frame 트레이드오프를 critical factor 단위로 분해해 정리. 프레임워크 신작이 아니라 분석 논문이라 인용이 많이 붙을 타입입니다.",
'2604.21801': "항공 영상용 multi-task synthetic 벤치(깊이·도메인 적응·초해상). Remote sensing 쪽 GT 부족 문제를 정면으로 푸는 벤치로 공백을 채웁니다.",
'2604.21915': "입력 비디오를 4D point cloud에 anchor해 target camera trajectory로 재촬영하는 video reshooting. 4D 표현을 명시적으로 쓴다는 게 키 아이디어예요. 영상 후반작업 쪽 실용성이 큽니다.",
'2604.21518': "Sparse-view CT 재구성에 diffusion prior + neural representation을 합쳐 artifact 억제. SliceFixer라는 single-step diffusion으로 NR 최적화에 prior를 주입하는 게 핵심입니다.",
'2604.21693': "SLAM을 stochastic control with partial information으로 재정식화하면서 최적 해와 rigorous approximation을 제시. 실무 SLAM 엔진보다 후속 이론·증명 작업이 붙을 논문이에요.",
'2604.21914': "View-robust manipulation을 spatiotemporal-aware view synthesis로 구현. Feed-forward geometric model + video diffusion으로 카메라 관점 변화에 robust한 closed-loop 정책을 만듭니다. VLA가 다기관 데이터로 가는 흐름의 전제 조건.",

'2604.21313': "UAV로 해변 쓰레기를 pixel-level area segmentation. 정확한 '면적'이 생태학적 위험도 평가 핵심이라는 문제 정의가 깔끔하고, 환경 모니터링 표준 도구로 굳을 가능성이 보입니다.",
'2604.21453': "Instance-level visual active tracking + occlusion-aware planning — drone·감시 도메인에서 '어디로 움직여야 안 가려지나'를 정책 단에서 해결. 최근 active perception 재부상 흐름의 오늘자 대표.",
'2604.21053': "Manipulation을 enriched Semantic Event Chains에 neuro-symbolic 으로 얹어 uncertainty-aware 하게 푸는 시도. Symbolic 표현이 VLA 시대에 어떻게 살아남느냐는 질문에 대한 한 답입니다.",
'2604.20990': "Non-inertial(움직이는 지면·제한된 중력) 환경 legged robot 서베이. 오늘 humanoid long-tail 논문들과 정확히 호응하는 위치문서로, 평지 걷기 너머 다음 축이 뭔지 정리해줍니다.",
'2604.21017': "의료 로봇용 'foundation-scale' cross-modality·cross-task·cross-embodiment 데이터셋. Open X-Embodiment가 일반 manipulation에서 한 역할을 의료 VLA에서 하겠다는 포지셔닝이 선명합니다. Must-read에서 자세히.",
'2604.21138': "Multi-robot waypoint-based bi-level planning — clutter 환경에서 collision-free 경로를 계층적으로 분해. 군집·물류 도메인용 실용 알고리즘 결입니다.",
'2604.21192': "공개 VLA 들(openvla·pi0·GR00T)을 같은 open-world manipulation suite에서 뜯어보면서 '실제로 무엇이 generalization을 만드는가'를 정량 분석. VLA가 '누가 더 좋은가'에서 '왜 그런가'로 축이 옮겨가는 분기점입니다. Must-read에서 자세히.",
'2604.21241': "VLA 출력에 sparse anchor (Δ-position)을 explicit spatial constraint로 집어넣어 generative action head를 guide. 기존 VLA가 spatial guidance를 latent로만 흘려보내던 약점을 정조준합니다.",
'2604.21331': "Wrist-mount 단일 카메라의 occlusion 문제를 정면 격파 — 손가락 끝에 카메라를 박아 dexterous manipulation을 학습. 실세계 multi-view perception을 손가락 단위까지 끌어내린 게 신선합니다.",
'2604.21351': "Imitation + RL로 '무중력 같은 non-self-stabilizing 모션'을 humanoid에 학습시키는 시도. 'weightlessness'라는 환경 의존 행동 축을 실험적으로 잡은 게 오늘 long-tail dynamic 흐름의 핵심 한 편입니다.",
'2604.21355': "Humanoid 격투처럼 long-time, multi-skill 전환이 잦은 시나리오에서 robust policy gating을 제안. 단일 정책 switching의 jitter 문제를 정면으로 해결합니다.",
'2604.21377': "LLM-enabled robotics interaction을 활용해 인지 장애 cohort에 대한 robotics awareness를 측정하는 replicable 방법. 실험 reproducibility + clinical relevance를 묶는 결입니다.",
'2604.21541': "Wheel-legged humanoid X2-N — wheel을 별도 link로 분리해 hip DOF 늘리고, dual-mode locomotion + manipulation을 같은 플랫폼에서 푼다는 게 핵심. 휴머노이드 폼팩터 다양화 흐름의 한 표본입니다.",
'2604.21741': "Human-in-the-world-model post-training — 시뮬레이션 안에서 사람이 직접 정책을 가이드해 VLA scaling cost를 낮추는 프레임. World model을 '평가 대상'이 아니라 '훈련 도구'로 쓰는 RO 사례로 봐야 합니다.",
'2604.21924': "Long-horizon manipulation을 trace-conditioned VLA + task-management VLM 으로 분해해 푸는 LoHo-Manip. Short-horizon VLA executor 위에 일종의 manager VLM을 두는 modular 구조라 인용이 많이 붙을 타입입니다.",

'2604.21479': "Frozen LLM을 map-aware spatio-temporal reasoner로 써서 차량 trajectory 예측. '훈련하지 않고 LLM 그대로 써먹는' 라인의 자율주행 응용으로, 빠른 prototyping에 의미가 있습니다.",
'2604.21130': "Self-predictive representation으로 UAV object-goal navigation을 자율적으로 학습. 비전-제어 결합 RL의 representation learning 축에서 예외적으로 탄탄해 보이는 한 편입니다.",
'2604.21249': "Off-road 3D trajectory planning에 자연어 가이드를 결합해 '어디가 traversable한가'를 reasoning으로 푸는 시도. 야외 자율 시스템에서 '규칙'으로 나열할 수 없는 traversability를 LLM에 위임하는 결입니다.",
'2604.21337': "긴 articulated 차량(트레일러 등) swarm에 대한 context steering — 길이가 긴 차량의 jack-knife 회피를 swarm 단위로 다룬다는 게 신선합니다. 물류·항만 응용 코너의 디테일.",
'2604.21471': "Infrastructure 기반 localization을 위한 통합 프레임워크 Ufil — 다양한 센서·지도 소스를 한 데로 묶는 시스템 논문. 자율주행 stack 후반부의 깔끔한 정리물.",
'2604.21489': "Mixer-based single-step drifting motion planner MISTY — high-throughput을 강조. 전통 sampling-based planner의 latency 문제를 압축하는 결로, 실시간 제어 쪽에서 의미가 있습니다.",
'2604.21640': "Autonomous underwater navigation에 task-specific subnetwork discovery를 RL로 적용. 도메인 특수성이 강한 코너지만 '네트워크의 어느 일부가 실제로 일하는가'라는 분석 축은 일반화 가능합니다.",

'2604.20983': "MLLM에 '식물학자처럼 생각하기'를 부과하는 intent-driven CoT 벤치. Domain-specific reasoning evaluation의 한 변형으로, 일반 MMMU의 한계를 vertical로 푼다는 의미가 있습니다.",
'2604.21032': "Multi-spectral data를 MLLM이 처리할 수 있게 guided input + CoT로 풀어내는 방법. Remote sensing·과학 데이터 도메인에서 MLLM 활용 폭을 넓히는 결입니다.",
'2604.21079': "VLM의 visual focus를 'foveated' 방식의 stateful action으로 구현 — 한 번에 전체를 보지 않고 영역을 점진적으로 zoom-in 해 reasoning합니다. 인간 시각 모방 + 효율 두 마리 토끼.",
'2604.21102': "Street view 이미지 + MLLM 으로 건물·housing attribute를 자동 평가. Vertical foundation model 응용 코너의 또 다른 사례.",
'2604.21160': "Point cloud 기반 VLM의 3D 이해를 강화하기 위해 geometric reward를 도입한 RL credit assignment. 3D foundation model이 빠른 속도로 reasoning 축을 끌어들이는 흐름의 일부.",
'2604.21190': "Spatial reasoning을 VL 에이전트들이 test-time에 동적으로 orchestrate하는 SpatiO. 단일 모델이 아니라 여러 VLM/도구를 조합한다는 system-level 접근이 키.",
'2604.21360': "VLM의 prototype-based test-time adaptation — fine-tuning 없이 inference 단에서만 분포 이동에 대응. 오늘 TTA 폭증의 한 축입니다.",
'2604.21396': "Grounded chain-of-thought로 VLM의 visual reasoning trustworthiness를 끌어올리는 VG-CoT. '이미지 어디를 봤는지' 명시적으로 인용하게 강제하는 결.",
'2604.21409': "Scientific multimodal reasoning을 'thinking-with-images' 으로 푸는 S1-VL. 과학 시각 자료(그래프·도식)를 reasoning 일부로 끌어들이는 흐름.",
'2604.21461': "MLLM의 '가리키기(pointing) 이해'를 egocentric 시나리오에서 벤치마킹. 로봇·AR 응용에 직결되는 referential reasoning 평가 축.",
'2604.21523': "Evaluator VLM의 blind spot을 정면 진단 — '심사하는 모델'이 정작 못 보는 영역이 있다는 걸 정량 증거로 보여줍니다. VLM-as-judge 패러다임에 대한 강력한 경고문.",
'2604.21718': "Human-AI oversight 기반 '정밀 video language' 구축. 비디오 캡션을 정밀하게 잡으려는 노력의 연장선.",
'2604.21728': "Active sample selection으로 VLM TTA를 robust하게 만드는 Ramen. 단순 TTA가 catastrophic 한 경우를 sampling으로 누그러뜨림.",
'2604.21786': "Codebook → VLM 으로 visual discourse analysis 자동화 — 기후 변화 미디어 분석 같은 humanity 도메인에 VLM을 가져온 사례.",
'2604.21879': "Generative AI를 카메라가 ISP 단에서 쓰기 시작하면서 '이미지 진위'가 뭐냐를 다시 묻는 position 논문. Forensics·법적 문제까지 연결되는 무거운 어젠다입니다.",
'2604.21911': "Prompt가 vision input을 override 하는 'Prompt-Induced Hallucinations' — LVLM의 새로운 실패 모드 카테고리를 명명. POPE 다음 세대 hallucination 벤치 후보.",
'2604.20878': "교통사고 책임 배분을 multimodal LLM으로 자동화하려는 AITP. Vertical foundation 응용 코너의 또 다른 표본.",
'2604.21199': "ARFBench — 시계열 question answering 능력을 software incident response 도메인에서 평가. ML 외 도메인에서 LLM 평가 인프라가 늘어나는 흐름.",
'2604.21346': "Symbolic grounding 시각 추론에서 representational bottleneck을 정밀 측정 — VLM의 'reasoning은 잘하는데 시각은 못 본다'를 또 다른 각도에서 진단합니다.",

'2604.21008': "Linear image generation을 exposure bracket 합성으로 구현 — diffusion 없이 linear 한 합성 방식으로 사진 생성을 푸는 결로 신선합니다.",
'2604.21041': "Text-to-image diffusion에서 'unlearning' 을 projected gradient로 구현. 저작권·안전성 이슈의 핵심 도구라 산업적으로 의미가 큽니다.",
'2604.21066': "Single observation으로 diffusion prior를 최적화하는 결 — inverse problem 측에서 prior 활용을 극단화한 시도입니다.",
'2604.21146': "3D wavelet flow matching으로 multi-modal MRI를 ultra-fast 합성. 의료 영상 합성 + flow matching 의 결합으로, 임상 application 코너의 의미 있는 한 편입니다.",
'2604.21221': "Real-time autoregressive video diffusion에 native trainable sparse attention을 도입한 Sparse Forcing. AR video 진영에서 '훈련 가능한 sparsity'라는 새 축이 열리는 신호.",
'2604.21279': "Latent + reference-guided diffusion으로 facial attribute editing을 정밀하게 푸는 LatRef-Diff. Avatar·photo editing 코너의 점진 개선이지만 industry 영향력 있음.",
'2604.21289': "Diffusion + GAN을 hybrid로 묶어 facial attribute editing — 두 패러다임의 trade-off를 합성으로 푸는 결입니다.",
'2604.21291': "Synthetic data augmentation을 controllable human-centric video generation에 활용한 분석. 합성 데이터의 한계와 효과를 정량적으로 봅니다.",
'2604.21362': "Knowledge-driven creative video generation KD-CVG — '창의성'을 외부 지식으로 가이드하는 결, generic prompt 한계를 보완.",
'2604.21422': "Segmentation pre-process로 nonlinear diffusion filter를 활용 — 고전 PDE 기반 영상처리가 deep 시대에 어디서 쓸모 있는지 보여줍니다.",
'2604.21450': "VAR distillation으로 single-step real-world image super-resolution을 완성한 VARestorer. VAR 가속 라인의 오늘자 대표.",
'2604.21592': "Sculpt4D — 4D shape generation을 sparse-attention diffusion transformer로. 4D generation이 'shape' 까지 직접 들어가는 흐름의 한 표본.",
'2604.21627': "Face morphing을 dual-stream cross-attention diffusion으로 — DCMorph. 보안·forensics에 양날의 칼이 되는 결.",
'2604.21686': "Interactive video world model용 통합 벤치 WorldMark — Genie·YUME·HY-World·Matrix-Game 모두 private scene으로 평가해서 비교 불가하던 문제를 정조준. 다만 '제안자가 곧 평가자' 구조는 Risk 섹션 참고.",
'2604.21814': "Ultra-long capsule endoscopy 비디오를 'clinician-inspired contexts'로 weave해 진단을 돕는 Divide-then-Diagnose. 의료 비디오 + LLM 흐름의 한 사례.",
'2604.21909': "Rate-distortion geometry로 직진 방향 confusion이 모델별로 다른 inductive bias를 드러낸다는 분석. Generation 경계 너머 representation theory에 한 발 걸친 논문.",
'2604.21931': "Slow/fast video flow를 학습해 '시간의 흐름'을 명시적으로 잡는 Seeing Fast and Slow. Temporal reasoning + generation 두 축에 걸치는 결.",
'2604.20936': "Cross-attention manipulation을 video diffusion transformer 안에서 creative tool로 쓰는 AttentionBender. Creator-friendly 측면에서 흥미로운 결입니다.",
'2604.21689': "Stylization-agnostic facial identity 평가 데이터셋·메트릭 StyleID. 스타일 변환 후에도 '이 사람' 인식이 무너지지 않는지 정량화한 새 평가축.",
'2604.21030': "RL + MPC 통합을 systematic하게 정리한 review/taxonomy. Hybrid control 라인 학습자에게 좋은 reference로, 인용이 길게 갈 형식 논문.",

'2604.21280': "On-device continual learning을 hyperdimensional computing(HDC)으로 푸는 ImageHD — energy efficiency가 키. Edge 비전 쪽 systems 코너의 흥미로운 한 편.",
'2604.21290': "Vision GNN의 graph construction과 convolution을 분리해 FPGA에서 가속하는 GraphLeap. Vision GNN이 systems 코너로 내려오는 흐름의 표본.",
'2604.21330': "Vision MoE의 router를 teacher-guided로 학습 — sparse mixture-of-experts의 routing 안정화는 여전히 뜨거운 주제입니다.",
'2604.21356': "Height-aware sparse segmentation framework SparseGF — context compression으로 robust segmentation을 가볍게 만듭니다. Aerial·자율주행 응용에 효과.",
'2604.21435': "Ultra-high-resolution remote sensing의 small object detection을 end-to-end로 효율화한 UHR-DETR. Detection 코너의 systems-aware 결.",
'2604.21668': "Encoder 없이 motion description으로 human motion understanding을 푸는 결 — encoder의 representation 부담을 structured description에 위임.",
'2604.20981': "Pancreas tumor segmentation을 cohort-robust하게 — probabilistic pancreas conditioning이 키. 의료 segmentation의 확실한 영역 개선.",
'2604.21268': "RL-coupled proposer + visual critic 공진화 — '두 번 측정하고 한 번 클릭'이라는 슬로건이 인상적입니다. UI agent 흐름과 닿아 있어요.",
'2604.21743': "Training-deployment gap을 gated encoding + multi-scale refinement로 메우는 결. 실배포 단계의 quality regression을 정조준합니다.",
'2604.20898': "Tendon-driven wrist abduction-adduction joint — 5DOF 상지 보조의 mechanical 개선. 하드웨어 디테일 논문이지만 prosthetics 도메인 의미.",
'2604.20887': "Planetary surface graph용 spectral kernel dynamics 분석 — 우주·행성 도메인 응용 코너의 한 사례.",

'2604.21363': "Hierarchical cognition + cooperative planning으로 deployable embodied vision-language navigation 시스템을 제안. '실제 배포 가능한' VLN을 명시적 목표로 두는 게 키.",
'2604.20910': "Software-defined, radically adaptive space system을 설계한 Planetary Exploration 3.0 로드맵. Embodied + space-systems의 흥미로운 교집합.",

'2604.21060': "Pediatric brain tumor classification을 whole-slide histology에서 clinically-informed 하게 모델링 — 의료 AI 쪽에서 임상 정보 결합의 디테일을 보여주는 결.",
'2604.21198': "수중 이미지 dense object detection을 probabilistic framework로 robust하게 — 도메인 노이즈가 큰 환경에서 uncertainty 표현이 키.",
'2604.21227': "Facial occlusion 분류에서 evidential classification + uncertainty-aware representation 학습. UAU-Net으로 안전성 축에서 쓸 수 있는 결.",
'2604.21321': "Frying oil oxidation을 dual-stream adversarial fusion으로 비파괴 평가하는 FryNet. 식품·산업 쪽 응용 코너의 또 한 편.",
'2604.21324': "Visible-infrared person re-id를 unsupervised로 푸는 temporal prototyping + hierarchical alignment. Surveillance + privacy 양쪽 의미가 있는 결.",
'2604.21326': "Universal multimodal retrieval에서 visual modality collapse를 mitigate하는 MiMIC. Multimodal alignment 안정화 라인의 오늘자 대표.",
'2604.21343': "Latent denoising으로 LMM의 visual alignment를 개선 — '노이즈 한 번 걸러주면 정렬이 좋아진다'는 단순하지만 효과적인 발견.",
'2604.21349': "Aerial self-supervised learning을 additive-residual selective invariance로 robust하게 — Trust-SSL. 항공·remote sensing self-sup 쪽 안정성 한 단계.",
'2604.21465': "Identity perturbation으로 face swapping을 proactive하게 방어하는 ID-Eraser. Generative misuse defense 흐름의 한 편.",
'2604.21478': "Cross-domain face forgery detection을 semantic fine-grained 평가로 다시 봄 — 기존 평가 프로토콜의 over-optimism을 지적합니다.",
'2604.21502': "VFM⁴SDG — Vision Foundation Model을 single-domain generalized object detection에 활용. VFM의 downstream 해석 라인.",
'2604.21530': "Lung tumor predominant growth pattern을 attention-based MIL로 예측 — pathology + AI 도메인의 점진 개선이지만 임상 영향이 큰 결.",
'2604.21546': "Component-based out-of-distribution detection — OOD score를 모델 components 단위로 분해해 해석성 확보.",
'2604.21573': "Histology representation을 cross-modal로 잡고 post-hoc calibration까지 — spatial gene expression prediction 도메인에서 calibration 강조가 인상적입니다.",
'2604.21617': "Parametric projection의 local instability를 정량·시각 분석. Dimensionality reduction 신뢰성 평가 도구.",
'2604.21694': "Video copy detection을 logic gate network로 효율화 — 단순 fingerprint 대비 학습 가능한 결입니다.",
'2604.21772': "Open-set continual TTA를 'source로 돌아가기' 패러다임으로 푸는 결. 기존 TTA가 source representation을 잃어버리는 문제를 정조준.",
'2604.21776': "Self-supervised in-the-wild video reshooting Reshoot-Anything — Vista4D와 같은 흐름이지만 supervision 없는 버전.",
'2604.21806': "Multi-modification composed image retrieval에서 anchor 이미지 + text follow 하는 TEMA — 복합 검색의 정밀도를 끌어올립니다.",
'2604.21873': "Video reasoning을 'physical signal'에 grounding — VLM이 실제 물리적 signal과 어떻게 align되는지 직접 평가.",
'2604.21904': "Image generation/detection을 co-evolutionary로 푸는 UniGenDet. 생성-탐지 두 진영을 한 framework에서 묶는 시도, deepfake 군비경쟁 라인.",
'2604.20851': "Test-time video-text retrieval에서 query shift에 robust한 adaptation을 벤치마킹. 검색 쪽 TTA 라인의 오늘자 대표.",
'2604.21395': "ERM 기반 supervised 인코더의 '필연적 geometric blind spot' 을 이론적으로 증명. 하드코어 representation theory 인데 must-read 후보 — Cross-pair 섹션에서 활용.",
'2604.21078': "UAV가 흔들리는 plate에 안전하게 착륙하기 위한 impact-aware MPC — 실험적 디테일이 탄탄한 control 논문입니다.",
'2604.21189': "Manipulator full-body dynamic safety를 3D Poisson safety function + CBF로 푸는 결. 고전 안전제어 + 현대 manipulation의 깔끔한 결합.",
'2604.21391': "Generative VLA를 'noise → intent' 매핑으로 보고 residual bridge로 anchor — generation-from-noise paradigm의 약점을 직접 공격합니다.",
'2604.21707': "Operator workload가 swarm 크기 변동에 따라 어떻게 변하는지 측정 — HRI factor 코너의 user study 결.",
}

WEEKLY_SUMMARY = "이번주 pastweek 누적을 살펴보면, 가장 큰 변화는 <strong>Safety/Alignment</strong>가 31편(지난주) → 58편으로 거의 두 배 가까이 부풀어 오른 거예요. CV쪽 TTA·OOD·adversarial·face forgery 라인이 동시에 폭발하면서 일어난 현상입니다. 한편 <strong>Foundation Models</strong>는 112편 → 69편으로 -38% 빠졌는데, 일주일 단위로 보면 'VLM 폭주'가 잠시 호흡을 고르고 'VLM이 어디서 틀리는가'로 무게추가 옮겨가는 신호라고 봅니다. Generation은 +20%, Embodied AI는 +33%, Efficiency는 +21% 로 완만한 상승이라 dynamic이 살아있어요."

WEEKLY_P2 = "오늘 /new에서 제일 눈에 띄는 건 <strong>VLA 라인의 다층 진화</strong>입니다. <a href=\"https://arxiv.org/abs/2604.21192\">How VLAs (Really) Work</a>가 openvla·pi0·GR00T 같은 공개 모델들을 '무엇이 generalization을 만드는가' 관점에서 해부하고, <a href=\"https://arxiv.org/abs/2604.21241\">CorridorVLA</a>는 sparse anchor로 spatial constraint를 explicit하게 주입하며, <a href=\"https://arxiv.org/abs/2604.21924\">LoHo-Manip</a>은 long-horizon manipulation을 manager VLM + executor VLA의 modular 분해로 풉니다. 어제까지 VLA가 '훈련 레시피 경쟁' 단계였다면, 이번주부터 <em>해부 + spatial constraint + 계층 분해</em> 세 갈래가 동시에 열리는 중이에요. 한동안 갈 흐름으로 보입니다."

WEEKLY_P3 = "부상 중인 미니 토픽 두 개. 첫째, <strong>휴머노이드의 long-tail dynamic 모션</strong> — 어제 Weightlessness·Fighting·X2-N 으로 한 번 터졌는데, 오늘 <a href=\"https://arxiv.org/abs/2604.20990\">non-inertial legged 서베이</a>가 '움직이는 지면' 같은 공백을 정리하면서 흐름이 굳어집니다. 둘째, <strong>3DGS의 production-grade 전환</strong> — <a href=\"https://arxiv.org/abs/2604.21400\">YOGO</a> 가 deterministic budget controller를 들고 나오면서 '학계-산업 격차'를 명시적으로 꺼냅니다. 두 미니 토픽 다 '평가 벤치 자체가 재설계되는' 신호라, 우리 랩이 들어갈 자리도 같은 곳에 있어요."

CV_VS_RO = "오늘 분포는 Safety(27)·Generation(20)·Foundation Models(19)가 CV 상위, Robot Learning(15)이 RO 거의 전부를 차지하는 어제와 비슷한 축 대칭입니다. 다만 <em>VLA가 오늘 CV 버전이 거의 없다</em>는 점이 어제와 동일하게 두드러져요 — Robot Learning 15편 중 12편이 순수 RO, 1편이 CV/RO, 2편은 응용 도메인의 CV(드론·tracking)라서 VLA 알고리즘 자체는 RO 전용입니다. 한편 <strong>3DGS는 13편 중 11편이 CV</strong>이고 RO는 SLAM(이론)·VistaBot 단 두 편 — 3DGS가 RO로 흘러들어오는 속도가 아직 느립니다."

CV_VS_RO_FOOTER = "하나만 꼽으라면 오늘의 CV/RO 교집합은 '<em>모델이 어디서, 왜 깨지는가</em>'입니다. CV쪽 <a href=\"https://arxiv.org/abs/2604.21523\">Seeing Isn't Believing</a>·<a href=\"https://arxiv.org/abs/2604.21911\">Prompt-Induced Hallucinations</a>·<a href=\"https://arxiv.org/abs/2604.21346\">Symbolic Grounding</a>·<a href=\"https://arxiv.org/abs/2604.21395\">Geometric Blind Spot</a> 가 한꺼번에 나오고, RO쪽 <a href=\"https://arxiv.org/abs/2604.21192\">How VLAs Really Work</a>이 VLA 내부를 해부합니다. 양쪽 커뮤니티가 '이 모델들이 정확히 어디서 깨지는가'를 독립적으로 파고드는 흐름이 한 주 내내 일관돼요. 올해 내내 갈 축이라 봅니다."

INSIGHTS = [
    {
        "title": "Safety/Alignment 폭증의 정체 — '새 안전 패러다임'이 아니라 '평가·robustness 인프라 정리'",
        "claim": "이번주 Safety/Alignment 가 31→58편(+87%) 으로 튀었는데 abstract를 들춰보면 새로운 'AI 안전' 어젠다가 아니라, TTA·OOD·face forgery·adversarial robustness 같은 <em>기존 평가/방어 인프라가 동시 정비되는</em> 양상입니다. 오늘만 봐도 <a href=\"https://arxiv.org/abs/2604.21772\">Open-Set Continual TTA</a>·<a href=\"https://arxiv.org/abs/2604.21478\">Cross-Domain Forgery Detection</a>·<a href=\"https://arxiv.org/abs/2604.21465\">ID-Eraser</a>가 같은 날 등장. 정책·alignment 쪽 안전이 아니라 'production model이 어떻게 실패하지 않게 만드냐' 의 robustness 라벨인 거죠. 우리 랩이 안전 키워드로 trend를 읽을 때 이 두 카테고리를 분리해 봐야 오해가 없습니다.",
        "papers": ["https://arxiv.org/abs/2604.21772","https://arxiv.org/abs/2604.21478","https://arxiv.org/abs/2604.21465"]
    },
    {
        "title": "VLA가 '규모 경쟁' → '해부 + 계층 분해' 페이즈로 넘어가는 중",
        "claim": "오늘 <a href=\"https://arxiv.org/abs/2604.21192\">How VLAs Really Work</a>이 공개 VLA 들의 generalization을 정량 해부하고, <a href=\"https://arxiv.org/abs/2604.21241\">CorridorVLA</a>가 sparse anchor로 spatial constraint를 explicit하게 넣으며, <a href=\"https://arxiv.org/abs/2604.21924\">LoHo-Manip</a>은 manager-executor 두 단계 분해를 제안합니다. 추가로 <a href=\"https://arxiv.org/abs/2604.21391\">Residual Bridge</a>가 generation-from-noise paradigm을 비판하면서, VLA가 'end-to-end big policy' 를 떠나 <em>모듈화 + 해석성 + 명시적 제약</em> 쪽으로 빠르게 옮겨가는 분기점입니다. 우리 매니퓰레이션 스택도 이 결을 따라가야 후속 연구를 받을 수 있어요.",
        "papers": ["https://arxiv.org/abs/2604.21192","https://arxiv.org/abs/2604.21241","https://arxiv.org/abs/2604.21924","https://arxiv.org/abs/2604.21391"]
    },
    {
        "title": "World Model이 '평가 대상(CV)'과 '훈련 도구(RO)'로 양분되는 현상의 고착화",
        "claim": "이번주 world model 키워드 CV 7편 / RO 8편으로 비슷하게 나오지만 결이 정반대입니다. CV쪽은 오늘 <a href=\"https://arxiv.org/abs/2604.21686\">WorldMark</a>(interactive video world model 통합 벤치)처럼 'world model이 잘 만들었나' 를 평가하는 데 쓰는 반면, RO쪽 <a href=\"https://arxiv.org/abs/2604.21741\">Hi-WM</a>은 'world model 안에서 사람이 정책을 가이드' 하는 훈련 인프라로 씁니다. 같은 단어가 한쪽은 <em>평가 대상</em>, 한쪽은 <em>훈련 도구</em>로 쓰여서 두 커뮤니티가 같은 페이퍼를 보고 다른 메시지를 받는 단절이 점점 커져요. 우리가 둘 다 들여다보는 입장이라 '양쪽이 만나는 지점'을 찾으면 차별화가 가능합니다.",
        "papers": ["https://arxiv.org/abs/2604.21686","https://arxiv.org/abs/2604.21741"]
    }
]

TOPICS = [
    {
        "title": "VLA Failure Atlas — 공개 VLA들의 실패 모드를 표준 분류 + 측정",
        "claim": "오늘 How VLAs Really Work·CorridorVLA(spatial)·Residual Bridge(noise-to-intent)·VistaBot(view robustness) 가 각자 다른 실패 모드를 측정하지만 표준 분류는 없어요. 'objects identity 의존 / out-of-embodiment 급락 / spatial guidance 누락 / view shift / temporal drift' 같이 표준 taxonomy + 측정 태스크 세트가 있으면 VLA 논문 비교가 정량 가능해집니다. 우리 랩이 manipulation VLA 스택을 돌리고 있으니, failure 수집 + 분류 벤치 선점 기회로 보여요. POPE가 LVLM hallucination에 한 일을 VLA에서 하면 됩니다.",
    },
    {
        "title": "World Model 통합 평가 — CV의 '세계 만들기'와 RO의 '세계 안에서 학습'이 만나는 벤치",
        "claim": "WorldMark(CV, 평가)와 Hi-WM(RO, 훈련)이 갈라지는 걸 봤을 때, 두 진영이 같은 world model을 두고 다른 메트릭을 측정합니다. CV는 visual fidelity·trajectory error·user study, RO는 policy success rate·sim2real gap·sample efficiency. <em>한 world model에 두 메트릭을 같이 돌리는 통합 평가</em>를 제안하면 양쪽 커뮤니티 모두에 어필 가능. 특히 '좋은 video world model 이 정말 좋은 정책 훈련장인가?' 라는 질문이 답이 안 났는데, 우리가 이걸 설계할 위치에 있어요.",
    },
    {
        "title": "VLM Blind-Spot Atlas — 진단 논문들을 통합 벤치로 응고",
        "claim": "오늘만 Prompt-Induced Hallucinations·Seeing Isn't Believing·Symbolic Grounding·Geometric Blind Spot(이론)·VG-CoT(grounding 강제) 가 동시에 등장. 각각 다른 축(prompt override / 평가자 편향 / 추상 reasoning / ERM 한계 / grounding 부재)이라 통합 매핑이 없어요. <em>'VLM Blind-Spot Atlas'</em> 통합 벤치 + 분류학을 잡으면 POPE 다음 세대 표준이 될 가능성이 큽니다. 우리 VLM QA 도구로도 즉시 사용 가능하니 일석이조.",
    }
]

CROSSPAIRS = [
    {
        "title": "VLA의 spatial constraint를 implicit vs explicit으로 푸는 두 접근",
        "body": "<a href=\"https://arxiv.org/abs/2604.21192\">How VLAs Really Work</a>(RO)는 공개 VLA 들이 <em>implicit latent feature</em> 만으로 spatial guidance를 처리하는 한계를 정량 해부합니다. 같은 날 <a href=\"https://arxiv.org/abs/2604.21241\">CorridorVLA</a>(RO)는 <em>sparse anchor를 explicit하게</em> 박아 tolerance region을 training objective에 직접 넣는 정반대 처방을 제안해요. 한쪽은 '무엇이 망가지는지' 진단, 한쪽은 '어떻게 고치는지' 처방 — 같은 문제(spatial guidance 부재)를 두고 짝을 이루는 양면입니다. 두 편 같이 읽으면 VLA 다음 세대 설계 원칙이 잡힙니다."
    },
    {
        "title": "Hallucination을 시각 모델 내부(CV)와 generative 정책 출력(RO)에서 각각 진단",
        "body": "<a href=\"https://arxiv.org/abs/2604.21911\">Prompt-Induced Hallucinations</a>(CV)는 prompt가 vision input을 override 해 LVLM이 '보지 않은 것을 본다' 는 새 실패 모드를 명명. 한편 <a href=\"https://arxiv.org/abs/2604.21391\">Residual Bridge</a>(RO)는 generative VLA가 noise → action으로 가는 길에서 'intent 없이 noise만 섞이는' 실패를 정조준해 anchoring 처방을 줍니다. 한쪽은 '입력 modality 사이 충돌', 한쪽은 '출력 generation의 의미 결여' — generative 모델에서 hallucination이 어디서 나오는지 보는 두 입체적 시각이에요."
    }
]

MUSTREAD = [
    {
        "title": "How VLAs (Really) Work In Open-World Environments",
        "id": "2604.21192",
        "badge": "RO",
        "authors": "Varun Bhatt et al.",
        "claim": "공개 VLA 세 종(openvla·pi0·GR00T)을 같은 open-world manipulation suite에서 평가하면서 <em>무엇이 generalization을 만드는가</em>를 입력·구조·훈련 레시피 축으로 분리 분석합니다. 지금까지 VLA 논문이 '우리가 더 좋다' 식 SOTA 경쟁이었다면 이 논문은 '왜 그런가'로 축을 옮기는 분기점이에요. 결과적으로 '현재 VLA들은 objects identity에 과의존하고, out-of-embodiment에서 성능이 급락한다'는 정량 증거를 남깁니다.",
        "method": """method:
  - fix open-world manipulation suite, vary backbone/recipe/inputs
  - per-component contribution via ablation & counterfactual probing
  - generalization axes:
    * object identity   (high sensitivity)
    * scene layout      (medium)
    * embodiment shift  (brittle / large drop)""",
        "weakness": "(a) 세 모델 비교라 일반화 결론의 범위가 한정. (b) open-world suite가 시뮬레이션 기반이면 real-world transfer gap이 별도 검증 필요. (c) 'objects identity 과의존'이라는 발견을 '어떻게 고치냐' 까지 본문이 끌고 가는지 abstract만으로는 불분명 — 진단 논문인지 처방 논문인지 본문 확인 필요.",
        "lab": "우리 VLA 스택의 평가 체크리스트에 'objects identity / embodiment / spatial layout' 세 축을 그대로 붙일 수 있습니다. 특히 cross-embodiment 실패 모드는 명시적으로 측정해야 한다는 시그널이에요."
    },
    {
        "title": "Sparse Forcing: Native Trainable Sparse Attention for Real-time Autoregressive Diffusion Video",
        "id": "2604.21221",
        "badge": "CV",
        "authors": "Kaichen Zhou et al.",
        "claim": "Real-time autoregressive video diffusion에서 sparse attention을 '훈련 가능한' 형태로 native하게 도입한 결입니다. 기존 sparse attention이 inference 가속용 휴리스틱이었던 반면, training time 부터 sparsity를 학습 가능 파라미터로 잡아 성능과 속도 trade-off를 명시적으로 푸는 게 핵심. AR video diffusion 진영의 systems 축에서 새 변곡점이 될 가능성이 큽니다.",
        "method": """method:
  - sparse attention with learnable per-query sparsity
  - jointly train AR video diffusion + sparsity mask
  - real-time inference: O(N log N) instead of O(N^2)
  - retain quality while cutting compute substantially""",
        "weakness": "(a) AR video 도메인 한정 — image diffusion 으로의 transfer는 별도 실험 필요. (b) '학습 가능한 sparsity'가 long-horizon 비디오에서 stability를 잃지 않는지 추가 검증 필요. (c) Sparse attention이 모델 capacity를 떨어뜨리는 임계점이 있을 수 있는데 abstract에선 미명시.",
        "lab": "우리가 video generation 파이프라인을 운영한다면, real-time inference의 latency budget 직접 영향. 또한 sparsity 학습 자체가 일반 transformer system에 일반화 가능한지 follow-up 가치 있어요."
    }
]

RISKS = [
    {
        "title": "WorldMark: '통합 벤치' 제안자가 평가 프로토콜 설계자라는 구조적 편향",
        "body": "Genie·YUME·HY-World·Matrix-Game 같은 interactive video world model이 각자 private scene으로 평가해서 비교 불가하다는 문제 의식은 정확합니다. 다만 평가 프로토콜을 들고 나오는 주체가 사후적으로 '통합 스위트'를 설계하면, 자기가 잘 풀리는 metric/scene을 우선 채택할 인센티브가 자동으로 생겨요. 외부 third-party reproduction 이전엔 '제안된 baseline 순위'를 강한 평가로 받지 말고 '메트릭 자체의 기여'만 인정하는 게 안전합니다."
    },
    {
        "title": "YOGO + Immersion v1.0 — 자기-데이터셋·자기-프레임워크의 단일-팀 SOTA",
        "body": "어제 짚었던 risk가 오늘 다시 후속으로 묶입니다. '기존 3DGS 벤치가 sparsity shield로 hallucination에 관대하다' 는 비판은 건강한데, 그 진단이 실린 논문이 자기 dataset(Immersion v1.0)에서 자기 framework(YOGO)로 SOTA를 주장하는 구조는 bias-prone 합니다. 외부 평가자가 같은 framework를 다른 scene에서 돌려 결과를 재확인할 때까지는 'production-grade' 라는 강한 클레임은 잠정 보류하는 게 맞아요."
    },
    {
        "title": "Open-H-Embodiment 라이선스·demographic 메타데이터 불투명 가능성",
        "body": "어제 같은 risk를 적었는데 오늘도 그대로 유효합니다. 의료 로봇 foundation dataset은 IRB 범위·de-identification 수준·demographic distribution(인종/성별/연령) 메타데이터가 abstract에 명시되지 않으면 '공개 foundation' 클레임 대비 실제 접근성이 훨씬 제한됩니다. 또한 demographic bias가 그대로 학습되면 임상 배포에서 안전 이슈로 돌아옵니다 — 본문 메타데이터 섹션 정독이 의무입니다."
    }
]

def render_paper(p):
    aid = p['arxiv_id']
    title = esc(p['title'])
    badge = badge_html(p)
    fa = p.get('first_author','')
    others = len(p.get('authors',[])) - 1 if p.get('authors') else 0
    auth = f"👥 {esc(fa)}{(' et al.' if others>0 else '')}"
    summ = SUMMARIES.get(aid)
    if not summ:
        abst = p.get('abstract','').strip()
        m = re.split(r'(?<=[.!?])\s+', abst)
        summ = ' '.join(m[:2])[:380]
        summ = esc(summ)
    code_badge = '<span class="cbadge cbadge-nocode">[📦 code ✗]</span>'
    return f"""<div class="paper">
<div class="paper-line1">📄 <a href="https://arxiv.org/abs/{aid}" target="_blank" rel="noopener"><strong>{title}</strong></a> {badge} {code_badge}</div>
<div class="paper-authors">{auth}</div>
<p>{summ}</p>
</div>"""

def render_bucket(name, info):
    icon = BUCKET_ICON[name]
    cnt = info['total']
    cv = info['cv']; ro = info['ro']; cvro = info['cvro']
    head = f'<h4 class="bucket">{icon} {esc(name)} <span class="count">· {cnt}편 · CV {cv} / RO {ro} / CV-RO {cvro}</span></h4>'
    body = '\n'.join(render_paper(p) for p in info['papers'])
    return head + '\n' + body

def main():
    d = json.load(open('out/classified.json',encoding='utf-8'))
    buckets = d['buckets']

    bucket_line_lines = []
    bucket_line_lines.append(f"📦 3D/Scene            : {buckets['3D/Scene']['total']:>2}편 (CV {buckets['3D/Scene']['cv']} / RO {buckets['3D/Scene']['ro']} / CV-RO {buckets['3D/Scene']['cvro']})")
    bucket_line_lines.append(f"🤖 Robot Learning      : {buckets['Robot Learning']['total']:>2}편 (CV {buckets['Robot Learning']['cv']} / RO {buckets['Robot Learning']['ro']} / CV-RO {buckets['Robot Learning']['cvro']})")
    bucket_line_lines.append(f"🚗 Autonomous Driving  : {buckets['Autonomous Driving']['total']:>2}편 (CV {buckets['Autonomous Driving']['cv']} / RO {buckets['Autonomous Driving']['ro']} / CV-RO {buckets['Autonomous Driving']['cvro']})")
    bucket_line_lines.append(f"🧠 Foundation Models   : {buckets['Foundation Models']['total']:>2}편 (CV {buckets['Foundation Models']['cv']} / RO {buckets['Foundation Models']['ro']} / CV-RO {buckets['Foundation Models']['cvro']})")
    bucket_line_lines.append(f"🎨 Generation          : {buckets['Generation']['total']:>2}편 (CV {buckets['Generation']['cv']} / RO {buckets['Generation']['ro']} / CV-RO {buckets['Generation']['cvro']})")
    bucket_line_lines.append(f"⚡ Efficiency/Systems  : {buckets['Efficiency/Systems']['total']:>2}편 (CV {buckets['Efficiency/Systems']['cv']} / RO {buckets['Efficiency/Systems']['ro']} / CV-RO {buckets['Efficiency/Systems']['cvro']})")
    bucket_line_lines.append(f"🏃 Embodied AI         : {buckets['Embodied AI']['total']:>2}편 (CV {buckets['Embodied AI']['cv']} / RO {buckets['Embodied AI']['ro']} / CV-RO {buckets['Embodied AI']['cvro']})")
    bucket_line_lines.append(f"🛡️ Safety/Alignment    : {buckets['Safety/Alignment']['total']:>2}편 (CV {buckets['Safety/Alignment']['cv']} / RO {buckets['Safety/Alignment']['ro']} / CV-RO {buckets['Safety/Alignment']['cvro']})")
    bucket_block = '\n'.join(bucket_line_lines)

    insights_html = '\n'.join(
        f'<div class="insight"><h3>{i["title"]}</h3><p>{i["claim"]}</p></div>' for i in INSIGHTS
    )
    topics_html = '\n'.join(
        f'<div class="topic"><h3>{t["title"]}</h3><p>{t["claim"]}</p></div>' for t in TOPICS
    )
    cross_html = '\n'.join(
        f'<div class="crosspair"><h3>{c["title"]}</h3><p>{c["body"]}</p></div>' for c in CROSSPAIRS
    )
    mustread_blocks = []
    for i,m in enumerate(MUSTREAD,1):
        bcls = {'CV':'badge-cv','RO':'badge-ro','CV/RO':'badge-cvro'}[m['badge']]
        mustread_blocks.append(f"""<div class="mustread">
<h3>{['①','②','③'][i-1]} {esc(m['title'])} <span class="badge {bcls}">{esc(m['badge'])}</span></h3>
<p><a href="https://arxiv.org/abs/{m['id']}">arxiv:{m['id']}</a> · {esc(m['authors'])}</p>
<div class="section-title">핵심 주장</div>
<p>{m['claim']}</p>
<div class="section-title">방법의 핵심</div>
<pre>{esc(m['method'])}</pre>
<div class="section-title">약점·한계</div>
<p>{m['weakness']}</p>
<div class="section-title">랩 파이프라인 영향</div>
<p>{m['lab']}</p>
</div>""")
    mustread_html = '\n'.join(mustread_blocks)
    risk_html = '\n'.join(
        f'<div class="risk"><h3>{r["title"]}</h3><p>{r["body"]}</p></div>' for r in RISKS
    )

    bucket_render = '\n'.join(render_bucket(name, buckets[name]) for name in
                              ['3D/Scene','Robot Learning','Autonomous Driving',
                               'Foundation Models','Generation','Efficiency/Systems',
                               'Embodied AI','Safety/Alignment'])

    h = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>arXiv Daily Briefing — {DATE}</title>
<style>{CSS}</style>
</head>
<body>
<div class="container">
<a href="https://gisbi-kim.github.io/arxiv-daily-summary/" class="home-btn home-btn-top">← 전체 목록으로</a>
<h1>📄 arXiv Daily Briefing — {DATE} ({WEEKDAY})</h1>
<div class="meta">
<div><strong>시야:</strong> 주간 2026-04-20 ~ {DATE} · 오늘 배치 cs.CV/new + cs.RO/new</div>
<div><strong>소스:</strong> arxiv.org /list/cs.CV/new · /list/cs.RO/new (stdlib 파서 경유)</div>
<div><strong>주간 규모:</strong> cs.CV ~756편 · cs.RO ~222편 (union ~978편)</div>
<div><strong>오늘 /new:</strong> cs.CV 172편 + cs.RO 56편 (cross 포함) → 138 unique → 114편 8개 ROI 버킷 선정</div>
<div><strong>델타 기준:</strong> 직전 스냅샷(2026-04-23)과 비교 (지난주 7일 전 스냅샷이 없어 가장 가까운 과거 사용)</div>
</div>
<h2>🔭 주간 동향</h2>
<p>{WEEKLY_SUMMARY}</p>
<p>{WEEKLY_P2}</p>
<p>{WEEKLY_P3}</p>
<h2>📐 CV vs RO 대비</h2>
<p>{CV_VS_RO}</p>
<div class="contrast">
<p><strong>① 공통으로 뜨는 키워드</strong></p>
<ul>
<li><code>test-time adaptation / TTA</code> — CV(Prototype-TTA, Ramen, Open-Set Continual TTA, Back to Source), RO(adaptation-style policy update)에서 양쪽 다 등장</li>
<li><code>world model</code> — CV(WorldMark 통합 벤치), RO(Hi-WM post-training infra) 양쪽 한 편씩</li>
<li><code>view robustness</code> — CV(WildSplatter unconstrained, Vista4D reshooting), RO(VistaBot view-robust manipulation) 공통 관심사</li>
</ul>
<p><strong>② CV에만 뜨는 키워드</strong></p>
<ul>
<li><code>diffusion / flow matching / VAR</code> — Sparse Forcing, WFM, VARestorer, Sculpt4D, LatRef-Diff 다수가 생성 본연의 축</li>
<li><code>hallucination / blind spot</code> — Prompt-Induced Hallucinations, Seeing Isn't Believing, Symbolic Grounding, Geometric Blind Spot 이론 — 오늘만 4편 이상</li>
<li><code>3DGS</code> — WildSplatter·YOGO·DualSplat·Vista4D, RO엔 SLAM 이론 한 편 외 거의 없음</li>
</ul>
<p><strong>③ RO에만 뜨는 키워드</strong></p>
<ul>
<li><code>VLA / dexterous manipulation</code> — How VLAs Work, CorridorVLA, FingerViP, LoHo-Manip, VistaBot, Residual Bridge — 대부분 RO 전용</li>
<li><code>humanoid / wheel-legged / legged</code> — Weightlessness(어제)·X2-N(어제) 이어 오늘 non-inertial legged 서베이로 흐름 굳힘 — CV에는 안 등장</li>
<li><code>CBF / safety filter / impact-aware MPC</code> — 3D Poisson CBF, Impact-aware UAV landing, RL-MPC taxonomy — 고전 제어 + 현대 학습 결합 RO 고유 축</li>
</ul>
<p><strong>④ 같은 단어 다른 맥락</strong></p>
<ul>
<li><code>world model</code>: CV(WorldMark) = 생성 비디오 통합 벤치 / RO(Hi-WM) = 정책 post-training 시뮬레이션 — 한쪽은 '평가 대상', 한쪽은 '훈련 도구'</li>
<li><code>view robustness</code>: CV(WildSplatter, Vista4D) = 미지 카메라/조명에서 렌더링 / RO(VistaBot) = 관점 변화에도 정책 success rate 유지 — 같은 robust 라는 말이 '시각적 품질' vs '제어 성공'</li>
<li><code>hallucination</code>: CV(LVLM 시각 접지 실패) / RO(Residual Bridge 'intent 없는 noise' 진단) — 같은 단어가 LVLM 출력 vs VLA action generation으로 차원이 갈림</li>
</ul>
</div>
<p>{CV_VS_RO_FOOTER}</p>
<h2>💡 오늘의 인사이트</h2>
{insights_html}
<h2>🔬 추천 연구주제</h2>
{topics_html}
<h2>📊 오늘의 버킷 현황</h2>
<div class="bucket-line">{bucket_block}</div>
<p>🔥 <span class="hot">TOP3</span>: Safety/Alignment (27), Generation (20), Foundation Models (19) · ❄️ <span class="cold">BOTTOM2</span>: Embodied AI (2), Autonomous Driving (7). 어제와 거의 동일한 분포라 <em>주간 흐름이 안정적으로 굳었다</em>는 신호로 봅니다. Safety가 다시 1위인데 결국 TTA·OOD·face forgery·adversarial 인프라 정리 페이즈가 한 주 내내 이어지는 중.</p>
<p>📈 <strong>주간 델타(2026-04-23 → 2026-04-26)</strong>: 🛡️ Safety/Alignment <span class="hot">+87%</span> (31→58), 🏃 Embodied AI <span class="hot">+33%</span> (30→40), ⚡ Efficiency <span class="hot">+21%</span> (28→34), 🎨 Generation <span class="hot">+20%</span> (79→95), 🚗 AD ±0% (13→13), 📦 3D/Scene <span class="cold">-15%</span> (40→34), 🤖 Robot Learning <span class="cold">-17%</span> (58→48), 🧠 Foundation Models <span class="cold">-38%</span> (112→69). FM의 큰 폭 조정이 'VLM 호흡 고르기' 신호로 가장 눈에 띕니다.</p>
<h2>🔀 크로스오버 페어</h2>
{cross_html}
<h2>🌟 오늘의 must-read</h2>
{mustread_html}
<h2>⚠️ 리스크·한계 필터</h2>
{risk_html}
<h2>📄 논문별 요약</h2>
{bucket_render}
<h2>🔗 참고 링크</h2>
<ul class="links">
<li><a href="https://arxiv.org/list/cs.CV/new">cs.CV /new</a> · <a href="https://arxiv.org/list/cs.RO/new">cs.RO /new</a></li>
<li><a href="https://arxiv.org/list/cs.CV/pastweek?skip=0&amp;show=2000">cs.CV pastweek</a> · <a href="https://arxiv.org/list/cs.RO/pastweek?skip=0&amp;show=2000">cs.RO pastweek</a></li>
<li><a href="https://gisbi-kim.github.io/arxiv-daily-summary/">📚 전체 브리핑 목록</a></li>
</ul>
<a href="https://gisbi-kim.github.io/arxiv-daily-summary/" class="home-btn home-btn-bottom">🏠 전체 목록으로</a>
<footer>arxiv-daily-summary · {DATE} · stdlib 파서 + classify.py · 138 unique → 114 buckets</footer>
</div>
</body>
</html>
"""
    os.makedirs('posts', exist_ok=True)
    with open(OUT,'w',encoding='utf-8') as f:
        f.write(h)
    print(f"Wrote {OUT}, {len(h)} bytes")

if __name__=='__main__':
    main()
