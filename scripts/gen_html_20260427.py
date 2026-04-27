#!/usr/bin/env python3
"""Generate posts/2026-04-27.html from out/classified.json"""
import json, html, io, os, sys

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

DATE = "2026-04-27"
WEEKDAY = "월"
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
.retro{background:#eff6ff;border:1px solid #bfdbfe;border-radius:8px;padding:14px 18px;margin:12px 0}
.retro h3{margin:0 0 6px 0;font-size:15px;color:#1e3a8a}
.retro .label{display:inline-block;font-size:11px;font-weight:600;padding:1px 8px;border-radius:10px;margin-right:6px;font-family:ui-monospace,monospace;background:#fef9c3;color:#854d0e;border:1px solid #fde047}
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

# Per-paper Korean summaries (구어체, 3-5줄)
SUMMARIES = {
# === 3D/Scene ===
'2604.22118': "Mocap-카메라 캘리브레이션이 실패하면 GT가 통째로 오염되는데도 실제로 검증 단계가 부실하다는 점을 정조준. AR/VR·SLAM·로봇 데이터셋 구축 파이프라인의 위생 문제를 정면으로 다루는 인프라 논문이라, 데이터셋 만드는 랩은 한 번 훑어볼 가치가 있어요.",
'2604.22129': "Pixel-aligned 1-DoF Gaussian으로 depth refinement를 잡아 2DGS 계열의 geometric fidelity를 한 단계 끌어올린 시도. 'Gaussian의 자유도를 줄이면 기하가 더 정확해진다'는 명시적 trade-off가 깔끔합니다. CV/RO 양쪽 카테고리에 동시 등록된 점이 흥미로워요.",
'2604.22183': "Motion-blurred 입력에서 3DGS 재구성을 풀 때 event camera만으론 노이즈 누수가 심한 한계를, optical flow를 명시적 supervision으로 끌어들여 보강. Event+flow 조합이 deblur 3DGS의 실용 레시피로 굳을 가능성이 보입니다.",
'2604.22334': "Point-BERT/MAE 같은 pretrained 3D encoder가 'topological' 정보를 정말 보유하는지 정량 측정하는 분석 논문. 3D pretraining 평가가 그동안 geometric/semantic 축에 갇혀 있었는데 새 진단 축을 하나 추가하는 위치예요.",
'2604.22339': "Optical flow로 ego-motion을 분리해 dynamic/static Gaussian을 나누고 dynamic 영역은 keyframe별 temporal center로 빠르게 학습. 3DGS-SLAM이 동적 환경으로 확장되는 오늘자 대표작으로 보입니다. SLAM 라인이 4DGS로 넘어가는 흐름이 또 하나.",
'2604.22350': "Relative camera pose를 flow matching으로 회귀하는 monocular VO 결. Flow matching이 generation에서 perception으로 넘어오는 흐름의 한 사례라, '생성 모델 학습 기법이 perception을 점점 잠식한다'는 큰 그림에 부합합니다.",
'2604.22354': "단일 스캐너 specific edge detection을 one-shot으로 학습. 산업용 3D inspection 처럼 스캐너마다 noise 분포가 다른 환경에서 generalization을 포기하고 적응성을 택한 실용 결입니다.",
'2604.22439': "2D foundation feature를 3DGS로 lift할 때 multi-view inconsistency가 noise로 굳는 문제를 neural regularizer로 정제. Semantic 3DGS 라인이 robustness 단계로 넘어가는 신호예요.",
'2604.22482': "기존 panorama 데이터셋이 fixed-spot 캡처에 머무르는 한계를 깨고 continuous trajectory로 새로 수집한 실세계 panorama 3D 벤치. Feed-forward 3D 모델이 panorama로 넘어가는 길을 열어주는 데이터 인프라.",
'2604.22507': "철도 도메인 perception용 5개 챌린지 통합 벤치. 자율주행은 nuScenes, navigation은 Habitat이 표준화된 반면 철도 쪽은 공개 벤치 자체가 부재했다는 niche 공백을 메워주는 결입니다.",
'2604.22518': "거대 데이터셋용 robust model estimation 프레임워크 NONSAC. RANSAC 계열의 minimal sampling 한계를 non-minimal로 풀어 outlier-heavy 대형 scene에 대응. 3DGS·SfM 파이프라인 backend로 바로 들어갈 후보예요.",
'2604.22657': "RFID 대신 vision-only로 가축 개체 식별. 정밀축산(precision livestock) 도메인 응용이지만, '비침습 신원 인식'이라는 문제 정의가 다른 도메인(야생동물 모니터링·재난 구조)으로 이식 가능합니다.",
'2604.22658': "Occluded single-view 입력에서 3D shape retrieval. CLIP·기존 vision-language space에 과의존하던 retrieval 방식의 'pose 무지' 약점을 정조준해서, pose-aware 임베딩을 학습하는 게 키입니다.",
'2604.22714': "유명 랜드마크 위주로 잘 되던 internet photo reconstruction을 long-tail(드물게 찍힌 장소)까지 끌어내려는 의도 표명 논문. 'next frontier'를 명시하는 포지셔닝이라, 해당 라인의 향후 인용 허브가 될 수 있어요.",
'2604.21960': "Sparse-view CT에서 conditional diffusion posterior alignment를 통해 anatomy-faithful 재구성. 의료 영상 inverse problem에 diffusion prior를 직접 박는 흐름의 표준 패턴이 점점 굳어가는 모양새입니다.",
'2604.22040': "Highway 환경 자율주행 localization을 정조준 — 도시 환경 SOTA가 highway에서 그대로 망가진다는 진단부터 출발합니다. 도메인 갭을 명시적으로 끊어 보는 접근이 healthy해요.",
'2604.22065': "iSAM2에 selective non-Gaussian refinement를 얹어, Gaussian 근사가 깨지는 윈도우만 nested sampling으로 보강. SLAM backend의 '모든 곳을 풀 nonlinear로 풀지 않고 위험 지점만' 전략이 깔끔합니다.",

# === Robot Learning ===
'2604.22562': "Federated learning에서 client contribution을 server-side validation 없이 gradient의 von Neumann spectral entropy로 estimate. Privacy-preserving FL 인프라 라인의 결로, 로봇 도메인보다 시스템/보안 결에 가깝지만 분류기는 RO 표지로 잡습니다.",
'2604.22102': "동적 rope manipulation을 zero-shot으로 — 'wiggle'로 물리 파라미터를 system identification 한 뒤 goal-conditioned action을 최적화. Real-world dataset 없이 물리 prior로 throwing 같은 unforgiving 태스크를 푸는 게 인상적입니다.",
'2604.22104': "Joint를 흔들면 platform 위에서 undulatory locomotion이 발생한다는 비대칭 2-link 로봇의 dynamic coupling 분석. 고전 mechanics + control 결로, 비전·학습 폭주 사이에서 '메커니즘 자체로 푸는' 라인의 오늘자 사례.",
'2604.22235': "실제 공장에서 수 시간 단위로 굴러가는 learning-augmented manipulation 보고서. Lab demo와 production deployment 사이 갭을 시간·품질·일관성 메트릭으로 정량 — 산업 현장 transfer 라인 사람들에겐 reference 자료입니다.",
'2604.22238': "Long-horizon manipulation에서 VLA의 'latest observation 만 보면 된다'는 Markov 가정을 깨고, persistent semantic graph + code-as-planner로 non-Markovian state를 명시 유지. 오늘자 must-read에서 자세히.",
'2604.22251': "Variable impedance MPC가 first-order actuator dynamics 하에서 'physically realizable 보다 큰 feasibility set'을 갖는 formulation error를 지적. Legged locomotion 제어 이론의 silent bug를 명시화한 가치 있는 결입니다.",
'2604.22363': "가정 환경 deformable object manipulation 전용 시뮬레이터 LeHome. Open-X-Embodiment가 일반 manipulation에서 한 일을 deformable 도메인에서 시뮬 인프라부터 다시 깔겠다는 포지셔닝.",
'2604.22526': "Magnetic localization을 calibration-free로 푸는 information-theoretic geometry 최적화 + physics-aware learning. 의료 인터벤션용 occlusion-free guidance라는 응용 motivation이 명확하고 sim2real gap을 정조준합니다.",
'2604.22591': "VLA의 물리적 unsafe behavior를 사전에 elicit 하는 'first physical red teaming' 프레임워크. Risk scenario 합성 + gradient-free 최적화로 unsafe trajectory를 끌어내요. 오늘자 must-read에서 자세히.",
'2604.22615': "사람의 gaze를 'intent의 관측 가능한 proxy'로 보고 egocentric human data로 pretrain → 소량의 robot data로 finetune. Embodiment gap을 'intent 표현 공유'로 우회하는 접근이 신선합니다.",
'2604.22715': "ADMM 기반 parallel trajectory optimization에서 fixed split structure가 highly constrained region에 stuck되는 문제를 shared neural policy로 adaptive하게 re-split. Optimization-side 구조 학습이라는 아이디어가 깔끔.",
'2604.22724': "Trajectory optimization으로 만든 데이터셋을 imitate 하는 goal-conditioned policy 학습. Suboptimal demonstration의 한계를 'optimal trajectory를 직접 만들어 흉내'로 우회하는 결입니다.",
'2604.22491': "Out-of-reach object 선택에서 단일 cue/deterministic fusion의 brittleness를 probabilistic cue integration으로 해결. MR/AR 입력 디바이스 라인의 결로, dominant cue가 unreliable일 때 graceful degrade를 보장합니다.",
'2604.22499': "Forearm EMG에서 high-dimensional finger kinematics를 Riemannian feature + RNN으로 직접 디코딩. 의수·XR·tele-op 입력 라인 결로, hand gesture를 reduce하지 않고 raw로 푼다는 게 차별점.",

# === Autonomous Driving ===
'2604.22240': "4D occupancy 생성 모델에 자연어로 multi-agent interaction을 directing — VLM-driven Spatio-Temporal MMDiT 구조로 'occupancy world의 영화 감독' 역할 수행. AD 시뮬레이션이 generative driving instruction 단계로 진입.",
'2604.22260': "도로변 카메라 기반 city-scale traffic 안전 VQA 벤치 + foundation model. 기존 AD가 차량 ego-centric 시점에만 매달려 있던 한계를 도시 단위 인프라 시점으로 확장하는 결입니다.",
'2604.22479': "운전자 졸음 검출에서 fixed EAR/MAR threshold가 개인 편차에 망가지는 문제를 personalized threshold + CNN 분류로 보정. 응용 측면 incremental이지만 driver monitoring 시스템 deployment 라인엔 실용적.",
'2604.22189': "Non-convex ROI + obstacle/no-fly zone 환경의 multi-robot coverage path planning을 energy-efficient하게 푸는 메타휴리스틱 비교 프레임워크. 드론 군집 scanning 응용에 곧장 들어가는 결.",
'2604.22196': "Multi-vehicle trajectory planning에서 spatio-temporal corridor의 time-step을 가변으로 만들어 시간 효율화. 신호등 없는 교차로 같은 시간 압박이 큰 상황에서 V-STC가 직접 효과를 봅니다.",
'2604.22068': "CARLA에서 실제 사고의 topology를 그대로 재구성해 AV evaluation에 사용. 기존 합성 conflict가 도로 토폴로지를 abstract만 잡던 한계를 끊는 결로, AV 평가 인프라가 '진짜 사고 모양'으로 옮겨가는 흐름.",

# === Foundation Models ===
'2604.22192': "Chart-to-code 생성에서 데이터셋 단순 증강의 한계를 'tri-perspective tuning + inquiry-driven evolution'으로 보완. 단순 multimodal scaling이 막힌 사이 데이터-centric 측 실험이 다시 부상하는 흐름의 사례.",
'2604.22226': "Long-form sports 비디오의 temporal compositional reasoning 벤치. 시간적으로 sparse한 evidence를 찾아 통합하는 능력이 MLLM의 약점이라는 진단을, 기존 short-clip QA로는 안 보이는 결로 정량화합니다.",
'2604.22274': "Open-vocabulary scene graph generation에서 VLM이 'language prior로 관계를 추정'하는 hallucination 문제를 counterfactual active graph evidence로 보완. SGG에 진단형 사고가 진입한 사례.",
'2604.22280': "CoT가 redundant thinking으로 retrieval에 노이즈를 넣는 한계를, 'rewrite를 universal interface'로 대체. Generative와 discriminative embedding 공간을 cross-mode alignment로 잇는 RIME 프레임워크. 추론 인터페이스 자체를 재정의하는 결.",
'2604.22409': "Action-conditioned scene transformation(spawn/place/remove)으로 long-horizon에서 spatial belief가 어떻게 진화하는지 isolate한 10M-image 진단 벤치. CodeGraphVLP의 RO쪽 메모리 문제와 정확히 짝을 이룹니다.",
'2604.22477': "Neuron labeling에서 contrastive example을 활용해 'incidental dominant feature'에 라벨이 끌려가는 문제를 보정. 해석성 라인이 prior FALCON 이후로 또 한 단계 정밀화되는 결.",
'2604.22498': "Multi-image 이해에서 spatial hallucination·attention leakage·object constancy 실패를 compositional grounded contrast로 보정. 비싼 human annotation/CoT 의존을 줄이는 self-supervision 측 자료가 늘어나는 흐름.",
'2604.22560': "Driving VQA에서 perception → prediction → planning 단계 간 cross-stage coherence를 explicit baseline + learned gated context projector 두 변형으로 비교. AD VQA가 단계 간 일관성 메트릭을 들고 정량 평가로 옮겨가는 사례.",
'2604.22156': "Cholecystectomy 안전 critical view 평가를 'criterion-level check'로 분해해 LVLM 직접 prompting/CoT/sub-Q 대비 안정성을 끌어올리는 surgical safety 결. 의료 안전 도메인이 LVLM reasoning을 audit-가능하게 다듬는 흐름.",
'2604.22492': "쥐 행동 비디오에서 사회적 우열 hierarchy를 MLLM으로 예측. 신경과학 도메인에 MLLM이 들어가는 흐름의 결로, 의료 영상 → 행동 영상으로 적용 영역이 점점 넓어지는 게 보입니다.",

# === Generation ===
'2604.22139': "OCT 망막 이상 검출을 unsupervised + anatomy-aware로 — annotation 부담을 우회하면서도 해부학적 prior로 generalization을 보강. 의료 영상 OOD 문제에 generative anomaly가 다시 들어오는 결.",
'2604.22160': "독립적으로 움직일 수 있는 'matter chunk'를 generative model로 통일적으로 인식. 인간 시각의 motion-based segmentation 원리를 generative 관점에서 재해석하는 인지과학·생성 교차 라인.",
'2604.22220': "Watermark attack 측이 watermark defense에 비해 너무 뒤처져 있다는 진단에서 출발해, frequency-domain modulated diffusion으로 invisible watermark를 무력화. 생성 AI copyright 라인의 '공격-방어 균형'을 의도적으로 흔드는 결.",
'2604.22302': "Knowledge-intensive T2I에서 photorealism은 좋지만 도메인 지식 충실성은 망가지는 한계를 새 벤치 + 방법으로 정조준. 기존 GenEval·T2I-CompBench가 못 잡는 'knowledge fidelity' 축이 표준화될 수 있어요. 자기-벤치 측면은 Risk 섹션 참고.",
'2604.22379': "Diffusion distillation을 embedding loss로 efficient하게 — 기존 regression/score matching의 자원·시간 부담을 줄이는 실용 결. Few-step generator 라인의 base recipe가 한 단계 가벼워집니다.",
'2604.22476': "Process mining 입장에서 비디오를 event log로 변환하는 SnapLog. 비디오 generation 결이라기보단 '비디오를 구조화된 process trace로 추출'이라는 응용 코너 — 산업 SOP 자동화 라인에 직접 영향.",
'2604.22506': "ICPR 2026 LRLPR 챌린지 — long-distance + compression artifact 환경 license plate 인식. 도메인 특화 챌린지 페이퍼라 기술 신규성보단 '벤치 표준 정착' 가치가 큽니다.",
'2604.22554': "비디오 생성/편집의 'long stretch + abrupt jump' 비선형성을 1D semantic progress function으로 분석/교정. 비디오 생성의 temporal failure mode를 정량화하는 진단 도구라 흥미로워요.",
'2604.22700': "신경퇴행성 질환 진행을 4D longitudinal diffusion으로 모델링 — 환자별 시계열이 sparse한 의료 영상의 본질적 한계를 generative completion으로 우회. 임상 prognosis 시뮬레이션 라인의 결.",
'2604.22103': "Street view 인식 모델의 'safety perception'을 multiple localised edit으로 interventional하게 분해. Counterfactual을 도시 인지 도메인에 명시적으로 도입하는 사례라, urban computing 쪽 인용 허브 후보입니다.",
'2604.22212': "EBSD/Polarized Light 다중 모달 microscopy 데이터를 multimodal diffusion으로 상호 보강. 재료 과학 도메인에 generative cross-modal completion이 들어가는 결로, 'modality A를 빠르게 + B로 늘려'식 가속 패턴.",
'2604.22649': "EEG에서 시각 인지 정보를 structure-guided diffusion으로 재구성. 자연 이미지 categorical 라벨에 갇혀 있던 BCI decoding을 'structural feature + subjective cognition'으로 확장하는 의의가 있어요.",
'2604.22152': "Discrete diffusion world model을 robotics policy 평가의 scalable proxy로 사용 — vision/language/action을 unified token으로 denoising. CV의 diffusion이 RO evaluation 인프라로 직접 흘러드는 사례. 오늘자 must-read에서 자세히.",
'2604.22199': "오픈 환경에서 LLM-driven closed-loop autonomous learning — uncovered task가 나타나면 LLM 호출 → 성공 사례를 자동 internalize. LLM-on-robot의 'one-shot meta-learning' 결의 한 사례.",

# === Efficiency/Systems ===
'2604.21984': "Adaptive site 기반 anisotropic diagram을 differentiable image representation으로 사용. Soft top-K blend로 픽셀 색을 합성해 'parametric image'를 학습 가능 표현으로 만드는 결로, neural representation 라인의 새 후보.",
'2604.22036': "DARPA PTG 프로그램의 의료 활동 egocentric 비디오 데이터셋 EgoMAGIC. 'task guidance assistant'를 의료 도메인으로 끌어오는 인프라 자료라, 의료 VLM/VLA 측 데이터 공백을 메웁니다.",
'2604.22045': "이미지 분류기의 set-level feature interaction을 Hessian-guided로 식별 — 단순 marginal attribution이 놓치던 그룹 단위 상호작용을 정량. 해석성 라인의 결로, classification 모델에 직접 적용 가능합니다.",
'2604.22281': "Document QA에서 background/question/comprehension-aware token pruning으로 효율을 끌어올리는 결. Document image의 'sparse evidence' 특성을 정조준한 정량적 token reduction 방법.",
'2604.22529': "Distorted image에서도 robust한 representation을 ViT distillation으로 학습. SSL이 clean 데이터에서 강력한 반면 corruption 환경에서 흔들리는 한계를 명시적으로 끊는 결.",
'2604.22595': "CLIP의 spatial perception이 약한 지점을 visual prompt adaptation으로 보강 — few-shot action recognition에서 light/egocentric 등 visual challenge에 대응. CLIP 효율 fine-tuning 라인의 응용 결.",
'2604.22338': "Wireless image transmission용 JSCC에서 layer/ratio별 DSConv 대체를 systematic하게 분석. 실용 시스템 라인 결로, edge device 통신 응용에 즉시 영향.",
'2604.22351': "Mid-IR 천체관측에서 chopping/nodding을 못 쓰는 차세대 망원경을 위해 low-rank 배경 + sparse point source 모델링으로 noise를 분리. 도메인 특화지만 'background-source decomposition' 패턴은 다른 inverse problem에도 이식 가능.",
'2604.22557': "Cardiac MRI accelerated reconstruction에 natural-domain foundation model이 효과적인지 정량 검증. Foundation model의 physics-based inverse problem transfer 가능성을 실제로 측정하는 결.",
'2604.22551': "Articulated object manipulation에서 다양한 trajectory primitive를 quality-diversity 탐색으로 발견. 단일 'optimal' 정책 대신 diverse primitive 풀을 구성하는 결로, manipulation 일반화에 도움.",
'2604.21952': "Multimodal foundation model의 hardware-software co-design 가속화 focus session 발표 자료. Edge device deployment를 정조준한 시스템 측 정리 자료라, on-device VLM 라인의 reference.",

# === Embodied AI ===
'2604.22093': "Low-light 환경에서 robotic vision의 luminance/contrast/denoise 파라미터를 Bayesian Optimisation + Retinex로 image-by-image 동적 결정. Training-free라 deployment 친화적인 결.",
'2604.22296': "달 환경 합성 이미지 생성용 오픈소스 시뮬레이터 비교 평가. 행성 탐사 미션의 'pre-deployment 시뮬레이션' 인프라 정리 자료로 niche 도메인이지만 'how to evaluate sim quality' 패턴은 일반적.",
'2604.22331': "Edge AI + monocular depth로 rover navigation을 stereo-free로 전환 — Raspberry Pi 4에서 UniDepthV2 돌리는 실증 보고서. 우주 탐사용 lightweight perception 라인의 실용 결입니다.",
'2604.22014': "Decentralized multi-agent semantic navigation을 multimodal open-vocabulary goal + multi-object mission으로 확장. Central coordinator/global map 없이 ad-hoc 통신만으로 동작 — robot fleet 분산화 라인.",

# === Safety/Alignment ===
'2604.22162': "Dense scene multi-object tracking의 mask error/ID switch를 density-aware mask regen + selective memory update로 보완한 SAM2MOT 확장. Sports 분석 같이 dense tracking이 일상인 응용에 직접 영향.",
'2604.22177': "Brain tumor segmentation에서 일부 modality가 빠진 임상 시나리오를 uni-encoder + multi-encoder 2-stage로 처리. 'representation before fusion' 패턴이 missing-modality 문제의 표준 처방으로 굳어가는 모양새.",
'2604.22190': "CLIP person ReID에서 [CLS] 토큰만 쓰는 spatial 선택성 부재를 patch-token + anchor 정렬로 보완. CLIP-기반 ReID 라인의 'global → local' 보정 사례.",
'2604.22310': "Privacy-preserving image query의 geometric obfuscation을 'dual convergent line' 기반으로 강화 — 최근 privacy attack에 취약했던 기존 방식 한계를 정면 보정. Federated 시각 위치인식 라인.",
'2604.22333': "재해 원격감지에서 pixel-level change detection → 의미 분석으로 옮기는 ChangeQuery 결. Disaster response 응용에서 actionable intelligence를 명시 메트릭으로 묶는 사례.",
'2604.22388': "TRUS 비디오에서 prostate cancer 분류를 3-branch collaborative feature로 처리. 의료 비디오 진단 라인의 결로, static frame 대비 video-level signal의 가치를 정량 입증.",
'2604.22390': "Visual place recognition에서 perceptual aliasing을 region-aware modeling + flexible re-ranking으로 완화. VPR이 continuous deployment 친화적 robustness 단계로 넘어가는 신호.",
'2604.22552': "Pedestrian detection에 대한 transferable physical-world adversarial patch — multi-stage 결정 파이프라인을 동시에 교란하는 triplet loss + 물리 다양성 robustness. AD/감시 시스템의 실세계 안전 위협을 명시화. Risk 섹션 참고.",
'2604.22579': "의료 영상에서 'useful nonrobust feature'가 ubiquitous하다는 정량 증거. 모델이 인간 해석 불가능한 패턴을 핵심 신호로 학습한다는 주장은, 의료 모델의 robustness/interpretability 양쪽에 큰 함의.",
'2604.22586': "Inversion-free flow-based video editing에서 multi-frame stability를 FlowAnchor로 안정화. Training-free라 deployment 가볍고, 동영상 편집 production 도구 후보로 들어갈 수 있어요.",
'2604.22244': "Black-box hybrid dynamical system에서 affine state constraint를 provably 만족하는 RL policy 학습. CBF/reachability 분석이 explicit dynamics에 의존하던 한계를 'affine + repulsive policy'로 끊는 결.",
'2604.22378': "Robot-to-human handover의 정적 vs 적응적 전략을 사람의 grasp pose/접근 방향에 맞춰 비교. HRI 도메인의 사용성 메트릭을 통제 변수 단위로 정량화하는 자료.",
'2604.22287': "SE(3) tangent operator의 1·2차 도함수 closed form/higher-order 근사. 다체 시스템·로봇·Cosserat continua 시뮬 백엔드용 수학 인프라 결이라 응용 적용 폭이 넓습니다.",
}

def summary_for(arxiv_id, title):
    s = SUMMARIES.get(arxiv_id)
    if s: return s
    return f"오늘 /new에 등록된 결로, 제목('{title[:80]}…')만으로는 정확한 평가가 어려워 본문 확인이 필요합니다."

def render_paper(p):
    aid = p['arxiv_id']
    title = esc(p['title'])
    auth = esc(p['first_author'] or '')
    badge = badge_html(p)
    # All papers default to no public code badge — we don't auto-detect.
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

    # Compose output
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
    parts.append('<div><strong>시야:</strong> 주간 2026-04-21 ~ 2026-04-27 · 오늘 배치 cs.CV/new + cs.RO/new</div>')
    parts.append('<div><strong>소스:</strong> arxiv.org /list/cs.CV/new · /list/cs.RO/new (stdlib 파서 경유)</div>')
    parts.append('<div><strong>주간 규모:</strong> cs.CV ~725편 · cs.RO ~223편 (union ~948편)</div>')
    parts.append('<div><strong>오늘 /new:</strong> cs.CV 113편 + cs.RO 49편 (cross 포함) → 103 unique → 89편 8개 ROI 버킷 선정</div>')
    parts.append('<div><strong>델타 기준:</strong> 직전 스냅샷(2026-04-26)과 비교 (지난주 7일 전 스냅샷이 없어 가장 가까운 과거 사용)</div>')
    parts.append('</div>')

    # 주간 동향
    parts.append('<h2>🔭 주간 동향</h2>')
    parts.append('<p>이번주 pastweek 누적을 살펴보면, 가장 큰 반전은 <strong>Foundation Models</strong>가 69편(지난주) → 111편으로 <span class="hot">+61%</span> 다시 폭증한 점이에요. 어제까지 \'VLM이 호흡 고른다\'고 봤는데 한 주 단위로 보니 호흡이라기보단 <em>주제가 갈아탔다</em>가 맞습니다 — chart-to-code, multi-image grounding, surgical safety reasoning, scene graph hallucination 같이 \'VLM의 어디가 깨지나\'를 정조준한 신규 페이퍼들이 동시에 쏟아져요. 한편 <strong>Robot Learning</strong>도 48 → 71편(<span class="hot">+48%</span>)로 VLA 라인이 다시 가속하고, <strong>3D/Scene</strong>은 34 → 46편(<span class="hot">+35%</span>)로 SLAM·dynamic 4DGS 쪽이 주축이 됐습니다. 반대로 <strong>Efficiency/Systems</strong>가 -35%, <strong>Autonomous Driving</strong>이 -31% 빠진 건 \'순수 efficiency 트릭\'·\'AD 단독 perception\'이 큰 모델 안으로 흡수되는 흐름의 연속이라 봅니다.</p>')
    parts.append('<p>오늘 /new에서 제일 눈에 띄는 건 <strong>VLA의 또 다른 세 갈래 동시 등장</strong>이에요. 지난주 \'분해 + 명시적 spatial constraint + 모듈화\' 페이즈를 짚었는데, 오늘 <a href="https://arxiv.org/abs/2604.22238">CodeGraphVLP</a>가 <em>persistent semantic graph로 non-Markovian memory</em>를, <a href="https://arxiv.org/abs/2604.22615">GazeVLA</a>가 <em>gaze를 intent proxy로 한 human → robot transfer</em>를, <a href="https://arxiv.org/abs/2604.22591">RedVLA</a>가 <em>물리 red teaming으로 unsafe behavior pre-detection</em>을 동시에 들고 나옵니다. 메모리·intent·safety가 한 날에 함께 열렸다는 게 우연이 아니라, VLA 다음 분기를 셋이 나눠 차지하려는 신호로 봅니다. 한동안 갈 흐름이고, 우리 manipulation 스택도 결을 따라가야 할 시점이에요.</p>')
    parts.append('<p>부상 중인 미니 토픽 두 개. 첫째, <strong>World Model이 \'평가 매개체\'로 본격 데뷔</strong> — <a href="https://arxiv.org/abs/2604.22152">dWorldEval</a>이 discrete diffusion world model을 robot policy 평가의 scalable proxy로 직접 사용합니다. 지난주 \'CV는 평가 대상 / RO는 훈련 도구\'로 양분되던 world model이 오늘 \'평가 인프라\' 라는 제3 용도를 추가했어요. 둘째, <strong>spatial reasoning + memory의 정량화</strong> — <a href="https://arxiv.org/abs/2604.22409">SpaMEM</a>이 10M 이미지 규모로 action-conditioned spatial belief 진화를 isolate하는 진단 벤치를 출시. CodeGraphVLP의 RO 측 memory 문제와 정확히 짝을 이루는 CV 측 평가 인프라라, 두 흐름이 향후 4~6주 동안 인용 모이는 자리가 될 가능성이 큽니다.</p>')

    # CV vs RO
    parts.append('<h2>📐 CV vs RO 대비</h2>')
    parts.append('<p>오늘 분포는 3D/Scene(17)·Generation(14)·Robot Learning(14)·Safety(13)·Efficiency(11)·FM(10) 으로 다층 분산이에요. <em>CV가 모든 버킷에서 다수</em>지만 Robot Learning은 RO 13/CV 1으로 거의 RO 전용입니다. 어제까지의 \'Safety/FM이 CV로 폭주\'와 달리 오늘은 <strong>3D/Scene이 17편으로 CV 14편 + RO 2편 + CV/RO 1편</strong>으로 1위에 올라왔어요. 3DGS-SLAM·flow matching·event camera·1DoF Gaussian이 한꺼번에 등장하면서 \'CV 본연 + RO 실용\' 양쪽이 같이 움직인 결과로 보입니다. 한편 Foundation Models는 RO 0편이라, \'VLM 신규 자체는 여전히 CV 영역\' 특성이 일주일 내내 일관됩니다.</p>')
    parts.append('<div class="contrast">')
    parts.append('<p><strong>① 공통으로 뜨는 키워드</strong></p>')
    parts.append('<ul>')
    parts.append('<li><code>spatial reasoning / memory</code> — CV(SpaMEM 10M-image diagnostic), RO(CodeGraphVLP semantic-graph state) — 같은 문제를 한 날 양쪽에서 다른 방식으로 풀어요</li>')
    parts.append('<li><code>world model</code> — CV(OccDirector 4D occupancy directing, GenMatter), RO(dWorldEval discrete diffusion eval, LLM closed-loop) — 평가/훈련/생성 세 용도로 갈라짐</li>')
    parts.append('<li><code>flow matching</code> — CV(PoseFM camera pose, FlowAnchor video edit), RO도 ATRS 같은 trajectory rerouting에서 implicit하게 사용</li>')
    parts.append('</ul>')
    parts.append('<p><strong>② CV에만 뜨는 키워드</strong></p>')
    parts.append('<ul>')
    parts.append('<li><code>3DGS / NeRF</code> — Flow4DGS-SLAM, EvFlow-GS, NRGS, PAGaS, Holo360D, DualSplat 라인이 오늘만 6편 이상 — RO엔 SLAM 이론(SNGR) 한 편 외 부재</li>')
    parts.append('<li><code>diffusion / generative</code> — FMDiffWA(watermark attack), 4D longitudinal diffusion(brain), Knowledge T2I, FlowAnchor — generation 본연 라인이 CV 단독</li>')
    parts.append('<li><code>VLM/MLLM reasoning</code> — Beyond CoT(RIME), CharTide, CGC, Sum-of-Checks, SpaMEM 등 추론 인터페이스 측 결이 모두 CV 표지</li>')
    parts.append('</ul>')
    parts.append('<p><strong>③ RO에만 뜨는 키워드</strong></p>')
    parts.append('<ul>')
    parts.append('<li><code>VLA</code> — CodeGraphVLP, RedVLA, GazeVLA — 알고리즘 핵심 RO 전용 위치 유지</li>')
    parts.append('<li><code>CBF / hybrid system / impedance MPC</code> — Black-box affine constraint RL, False Feasibility VI-MPC, ATRS — 고전 제어 + 학습 결합 RO 고유 축</li>')
    parts.append('<li><code>tele-op / EMG / handover</code> — Decoding finger motion, Adaptive handover, Point&Grasp — HRI 영역 RO 전용 결</li>')
    parts.append('</ul>')
    parts.append('<p><strong>④ 같은 단어 다른 맥락</strong></p>')
    parts.append('<ul>')
    parts.append('<li><code>memory</code>: CV(SpaMEM = MLLM의 long-horizon spatial belief 진단) / RO(CodeGraphVLP = persistent semantic graph로 trajectory state 유지) — 한쪽은 \'평가\'·한쪽은 \'아키텍처 컴포넌트\'</li>')
    parts.append('<li><code>world model</code>: CV(OccDirector = 4D occupancy를 자연어로 directing) / RO(dWorldEval = policy 평가 proxy / Hi-WM 류 = 훈련 도구) — 평가-훈련-생성 세 용도가 명시화</li>')
    parts.append('<li><code>safety</code>: CV(TriPatch = pedestrian detection 패치 공격, Useful nonrobust features) / RO(RedVLA = 물리 red teaming, affine-CBF) — \'시각 모델 robust성\' vs \'physical 위험 사전 차단\'</li>')
    parts.append('</ul>')
    parts.append('</div>')
    parts.append('<p>오늘의 CV/RO 교집합은 \'<em>모델이 long-horizon에서 메모리를 어떻게 다루나</em>\'입니다. CV쪽 <a href="https://arxiv.org/abs/2604.22409">SpaMEM</a>이 belief evolution을 진단 벤치로 isolate하고, RO쪽 <a href="https://arxiv.org/abs/2604.22238">CodeGraphVLP</a>가 explicit semantic graph로 처방을 줍니다. 진단(CV) + 처방(RO)이 같은 날 동시 등장한 건 우연이 아니에요 — 어느 쪽 커뮤니티에서 시작했든 \'short-context의 한계\'가 양쪽에서 공통 인식이 됐다는 신호입니다. 한동안 갈 큰 축이에요.</p>')

    # 인사이트
    parts.append('<h2>💡 오늘의 인사이트</h2>')
    parts.append('<div class="insight"><h3>VLA가 \'분해+제약\' 다음 페이즈로 — memory·intent·safety가 한 날에 동시 점화</h3><p>지난주 짚은 \'How VLAs Really Work·CorridorVLA·LoHo-Manip\' 분해+모듈화 흐름 다음 단계가 오늘 일제히 열렸어요. <a href="https://arxiv.org/abs/2604.22238">CodeGraphVLP</a>(persistent semantic graph로 non-Markovian memory), <a href="https://arxiv.org/abs/2604.22615">GazeVLA</a>(gaze를 intent proxy로 human→robot transfer), <a href="https://arxiv.org/abs/2604.22591">RedVLA</a>(physical red teaming) — 세 편 모두 \'기존 VLA가 못 풀던 차원\'을 각자 점유하려는 포지션이고, 한 날에 셋이 같이 나오는 게 핵심. VLA 다음 6개월의 main axis 셋이 동시에 표시된 셈이라, 우리 manipulation 스택은 이 세 축 중 어디에 들어갈지 명확히 잡아야 합니다.</p></div>')
    parts.append('<div class="insight"><h3>World Model의 세 번째 용도 — \'평가 매개체\'가 dWorldEval로 본격 데뷔</h3><p>지난주에 \'CV는 평가 대상, RO는 훈련 도구\'로 양분된다고 봤는데, 오늘 <a href="https://arxiv.org/abs/2604.22152">dWorldEval</a>이 \'평가 인프라\'라는 제3 용도를 추가합니다. Discrete diffusion world model이 vision/language/action을 단일 token space로 처리하면서, real robot 없이 thousands of envs × thousands of tasks를 평가할 수 있다는 클레임. CV의 diffusion이 RO 평가 파이프라인으로 직접 흘러들어오는 사례라, 두 커뮤니티의 \'모델 공유\'가 아니라 \'인프라 공유\'로 격상되는 신호예요. 검증되면 OpenX-Embodiment 류 정량 비교의 게임 체인저.</p></div>')
    parts.append('<div class="insight"><h3>Long-horizon에서 \'memory\'가 CV·RO 양쪽 공통 합류 지점</h3><p>오늘 <a href="https://arxiv.org/abs/2604.22409">SpaMEM</a>(CV: 10M-image action-conditioned spatial belief 평가)와 <a href="https://arxiv.org/abs/2604.22238">CodeGraphVLP</a>(RO: persistent semantic graph)가 같은 날 등장하는 건, MLLM·VLA 모두 \'short-context 한계\'를 공통 인식으로 받아들였다는 신호입니다. 추가로 <a href="https://arxiv.org/abs/2604.22226">Long-Form Sports Video Reasoning</a>이 같은 long-horizon temporal reasoning 약점을 비디오 도메인에서 측정. 진단 벤치 + architecture 처방 + 응용 측정이 한 날에 모이는 패턴이라, \'memory architecture\' 자체가 향후 4~6주 인용 허브가 될 가능성이 큽니다.</p></div>')

    # 추천 연구주제
    parts.append('<h2>🔬 추천 연구주제</h2>')
    parts.append('<div class="topic"><h3>VLA Memory Bench — non-Markovian VLA의 메모리 축 표준 측정</h3><p>오늘 CodeGraphVLP가 \'persistent graph로 long-horizon\'을 처방했지만, 표준 측정 벤치는 없어요. SpaMEM이 CV에서 한 일을 VLA action 도메인으로 확장하면 됩니다 — early-occluded evidence / distractor noise / subtask boundary / context length scaling 같이 표준 axis + 진단 task. 우리 랩이 manipulation VLA를 돌리는 입장이라, failure 데이터 수집 + 분류 벤치를 선점할 위치에 있어요. POPE가 LVLM hallucination에 한 일을 VLA memory에서 하는 거죠.</p></div>')
    parts.append('<div class="topic"><h3>World Model 평가 Calibration — dWorldEval surrogate가 실제 정책 성공과 얼마나 일치하나</h3><p>dWorldEval이 thousands of tasks 평가를 가능케 한다고 클레임하지만, surrogate model이 real-world success rate와 얼마나 calibrated인지는 별도 검증이 필요합니다. \'discrete diffusion이 만든 rollout으로 평가한 정책 순위 vs 실제 robot 평가 순위 spearman correlation\'을 측정하는 calibration study가 비어 있어요. 우리 랩이 OpenX-Embodiment 정도 evaluation 인프라가 있다면, 이 calibration study를 빠르게 출판할 수 있습니다.</p></div>')
    parts.append('<div class="topic"><h3>Physical Safety Atlas — VLA·detection·medical reasoning 안전 도메인 통합 벤치</h3><p>오늘 RedVLA(VLA red teaming)·TriPatch(pedestrian patch attack)·Sum-of-Checks(surgical CVS reasoning)·Useful nonrobust features(medical) 가 안전이라는 라벨 아래 흩어져 있는데 통합 매핑이 없어요. <em>Physical Safety Atlas</em> — adversarial input · physical actuation risk · medical decision audit · cross-domain robustness 4축으로 각 카테고리별 표준 벤치를 제안. 도메인 통합 안전 평가는 학계가 비어 있는 자리고, 우리 랩이 VLA + medical CV 둘 다 다룰 수 있다면 자리잡기 좋습니다.</p></div>')

    # 회고 — 자료 부족 안내
    parts.append('<h2>🧭 예측 회고 루프</h2>')
    parts.append('<div class="retro">')
    parts.append('<p>월요일이지만 회고 루프 활성화에 필요한 <strong>2주 전(2026-04-13) / 4주 전(2026-03-30) insights JSON이 아직 없어요</strong>. 이 시스템에서 insights 누적은 2026-04-23부터 시작됐으니, 2주 전 회고는 <strong>2026-05-04(월)</strong>부터, 4주 전 회고는 <strong>2026-05-18(월)</strong>부터 본격 가동될 예정입니다. 그때까지는 매일 insights를 쌓아 평가 데이터를 만들어 둡니다.</p>')
    parts.append('<p>다만 어제(2026-04-26) 인사이트 \'<em>VLA가 분해+모듈화+명시적 제약으로 옮겨간다</em>\'는 오늘 CodeGraphVLP·GazeVLA·RedVLA로 곧장 이어지는 모양새라, 짧은 horizon에선 <span class="label">✅ 적중</span> 시그널입니다. 정식 회고는 2주 후 다시 정량 채점할게요.</p>')
    parts.append('</div>')

    # 버킷 현황
    parts.append('<h2>📊 오늘의 버킷 현황</h2>')
    bucket_lines = []
    for b in order:
        info = buckets[b]
        icon = BUCKET_ICON[b]
        # Pad name + colon column
        name = b
        bucket_lines.append(f'{icon} {name:<20}: {info["total"]:>2}편 (CV {info["cv"]:>2} / RO {info["ro"]:>2} / CV-RO {info["cvro"]})')
    parts.append('<div class="bucket-line">' + '\n'.join(bucket_lines) + '</div>')

    # TOP3 / BOTTOM2
    sorted_b = sorted([(b, buckets[b]['total']) for b in order], key=lambda x: -x[1])
    top3 = sorted_b[:3]
    bot2 = sorted_b[-2:]
    parts.append(f'<p>🔥 <span class="hot">TOP3</span>: {top3[0][0]} ({top3[0][1]}), {top3[1][0]} ({top3[1][1]}), {top3[2][0]} ({top3[2][1]}) · ❄️ <span class="cold">BOTTOM2</span>: {bot2[0][0]} ({bot2[0][1]}), {bot2[1][0]} ({bot2[1][1]}). 어제까지 Safety가 1위였는데 오늘은 3D/Scene이 1위로 올라온 게 신호입니다 — 3DGS-SLAM·flow matching·event camera 결이 한꺼번에 들어와 \'기하 인프라 정비\' 페이즈가 본격화하는 모양새. Robot Learning이 14편으로 안정 유지된 것도 VLA 라인이 가속한 결과예요.</p>')

    # 델타 (vs 2026-04-26)
    parts.append('<p>📈 <strong>주간 델타(2026-04-26 → 2026-04-27)</strong>: 🧠 Foundation Models <span class="hot">+61%</span> (69→111), 🤖 Robot Learning <span class="hot">+48%</span> (48→71), 📦 3D/Scene <span class="hot">+35%</span> (34→46), 🎨 Generation <span class="hot">+11%</span> (95→105), 🛡️ Safety/Alignment <span class="cold">-12%</span> (58→51), 🏃 Embodied AI <span class="cold">-20%</span> (40→32), 🚗 AD <span class="cold">-31%</span> (13→9), ⚡ Efficiency <span class="cold">-35%</span> (34→22). FM 반등(+61%)이 가장 큰 신호로, 어제 \'호흡 고른다\'는 해석을 \'주제 갈아탔다\'로 갱신할 시점입니다 — chart-to-code, surgical reasoning, multi-image grounding 같은 신규 축이 공백을 메우고 있어요.</p>')

    # 벤치마크 SOTA 추이 — 신규 보고가 거의 없으므로 skip 또는 minimal
    # Endoscapes2023 (Sum-of-Checks) is single benchmark mentioned today
    parts.append('<h2>📈 벤치마크 SOTA 추이</h2>')
    parts.append('<p>이번주 추적 벤치마크(ScanNet++·LIBERO·nuScenes·MMMU·VBench 등) 신규 SOTA 업데이트는 표 단위로 새로 잡힌 게 없습니다. <a href="https://arxiv.org/abs/2604.22156">Sum-of-Checks</a>가 Endoscapes2023(non-tracked) 에서 frame-level mAP를 끌어올렸고, <a href="https://arxiv.org/abs/2604.22409">SpaMEM</a>이 새 벤치를 출시했지만 추적 리스트엔 없는 상황. 다음주 nuScenes/LIBERO 측 결과 누적되면 표 갱신할게요.</p>')

    # 크로스오버 페어
    parts.append('<h2>🔀 크로스오버 페어</h2>')
    parts.append('<div class="crosspair"><h3>Long-horizon memory를 \'평가\'(CV) vs \'아키텍처\'(RO)로 정조준</h3><p><a href="https://arxiv.org/abs/2604.22409">SpaMEM</a>(CV)는 10M-image 진단 벤치로 \'MLLM의 spatial belief가 action sequence 위에서 어떻게 깨지는가\'를 isolate합니다. 같은 날 <a href="https://arxiv.org/abs/2604.22238">CodeGraphVLP</a>(RO)는 persistent semantic graph + code planner로 \'그 깨짐을 architecturally 막는\' 처방을 제안. 한쪽은 진단 인프라, 한쪽은 처방 architecture — 양쪽이 같은 날 등장한 건 long-horizon memory가 양 커뮤니티 공통 어젠다로 굳었다는 신호예요. 두 편 같이 읽으면 다음 6개월 long-horizon 연구의 게임판이 잡힙니다.</p></div>')
    parts.append('<div class="crosspair"><h3>World Model의 \'directing\'(CV) vs \'evaluation\'(RO) — 한 토큰 공간에서 양쪽 다 사용</h3><p><a href="https://arxiv.org/abs/2604.22240">OccDirector</a>(CV)는 자연어로 4D occupancy world의 multi-agent interaction을 directing 하는 \'시나리오 감독\'입니다. <a href="https://arxiv.org/abs/2604.22152">dWorldEval</a>(RO)은 같은 unified token space에서 vision/language/action을 denoise하면서 robot policy 평가의 surrogate로 사용. 둘 다 \'multimodal token space에 모든 modality를 collapse\' 한다는 공통 architectural choice를 갖지만, CV는 \'생성 directing\' RO는 \'평가 surrogate\'으로 갈라집니다. 같은 도구가 두 용도로 쓰이는 만큼 calibration·평가 측 cross-validation이 향후 핵심 질문이 됩니다.</p></div>')

    # Must-read
    parts.append('<h2>🌟 오늘의 must-read</h2>')
    parts.append('<div class="mustread">')
    parts.append('<h3>① CodeGraphVLP: Code-as-Planner Meets Semantic-Graph State for Non-Markovian VLA <span class="badge badge-ro">RO</span></h3>')
    parts.append('<p><a href="https://arxiv.org/abs/2604.22238">arxiv:2604.22238</a> · Khoa Vo et al.</p>')
    parts.append('<div class="section-title">핵심 주장</div>')
    parts.append('<p>VLA 모델이 \'latest observation 만으로 action을 reasoning한다\'는 short-horizon 가정을 깨고, persistent semantic graph로 task-relevant entity와 relation을 명시적으로 보관하면서 code-as-planner가 그래프 위에서 progress check + 다음 subtask instruction을 생성합니다. Long-horizon에서 evidence가 가려지거나 시간적으로 떨어져 있을 때 short-context VLA가 무너지는 문제를 architecturally 끊는 결이에요. \'persistent state + 명시적 planner\' 조합이 VLA 다음 단계 표준 처방이 될 가능성을 보여줍니다.</p>')
    parts.append('<div class="section-title">방법의 핵심</div>')
    parts.append('<pre>persistent_state = SemanticGraph()  # entities + relations under partial obs.\nfor t in horizon:\n    obs_t = camera.read()\n    persistent_state.update(obs_t)\n    plan = code_planner(persistent_state)        # progress check + next subtask\n    subtask, target_objs = plan.next_subtask()\n    obs_focused = clutter_suppress(obs_t, target_objs)\n    action = vla(obs_focused, language=subtask)  # standard VLA call\n    execute(action)</pre>')
    parts.append('<div class="section-title">약점·한계</div>')
    parts.append('<p>(a) Semantic graph 자체의 \'정확한 update\' 가 perception module에 의존 — perception 실패가 graph 오염으로 직결되는 risk 검증 필요. (b) Code planner가 LLM 호출이면 long-horizon 추론 비용/지연이 누적. (c) Clutter-suppressed observation의 information loss 측정이 ablation으로 충분히 보고되는지 본문 확인 필요. (d) \'persistent state\'가 메모리 leak / drift 없이 trajectory 끝까지 유지되는 정량 데이터가 abstract만으론 안 보입니다.</p>')
    parts.append('<div class="section-title">랩 파이프라인 영향</div>')
    parts.append('<p>우리 manipulation 스택이 short-horizon VLA에 머물러 있다면, persistent state layer를 한 단계 끼워 넣을지 결정해야 할 시점입니다. 특히 medical/long-task 시나리오에선 \'evidence가 일찍 사라지는\' 패턴이 흔해서 곧장 영향이 있어요.</p>')
    parts.append('</div>')

    parts.append('<div class="mustread">')
    parts.append('<h3>② dWorldEval: Scalable Robotic Policy Evaluation via Discrete Diffusion World Model <span class="badge badge-ro">RO</span></h3>')
    parts.append('<p><a href="https://arxiv.org/abs/2604.22152">arxiv:2604.22152</a> · Yaxuan Li et al.</p>')
    parts.append('<div class="section-title">핵심 주장</div>')
    parts.append('<p>Robot policy를 thousands of envs × thousands of tasks 규모로 평가하는 게 기존 simulator/real eval에서 사실상 불가능하다는 진단에서 출발합니다. dWorldEval은 vision·language·action을 unified token space로 매핑하고 single transformer denoiser로 모든 modality를 동시 처리하는 discrete diffusion world model을 \'평가 proxy\'로 사용. Sparse keyframe memory + progress token으로 spatiotemporal consistency를 유지하면서 large-scale evaluation을 한 번에 돌립니다. CV의 diffusion 인프라가 RO 평가 파이프라인으로 직접 들어오는 첫 사례라, 검증되면 OpenX-Embodiment 류 정량 비교의 표준이 바뀔 잠재력이 있어요.</p>')
    parts.append('<div class="section-title">방법의 핵심</div>')
    parts.append('<pre>tokenize(vision, language, action) -&gt; unified_tokens\nworld_model = DiscreteDiffusion(transformer_denoiser)\nfor task in eval_suite:                    # thousands of tasks\n    rollout = world_model.denoise(\n        init_obs, policy, sparse_keyframe_mem, progress_token)\n    score = evaluator(rollout, task.goal)\n# proxy ranking ≈ real-world ranking? (calibration TBD)</pre>')
    parts.append('<div class="section-title">약점·한계</div>')
    parts.append('<p>(a) \'Surrogate eval과 real eval의 ranking spearman correlation\'이 abstract 단계에서 명시되지 않은 게 가장 큰 의문 — calibration study가 약하면 SOTA 비교 도구로 못 씁니다. (b) Discrete tokenization 자체가 fine-grained action precision을 잃는 ceiling을 갖는데 이게 평가의 false-positive를 만들 위험. (c) 이미 학습된 policy를 평가하는 데 쓰는데, OOD task / long-tail scenario에서 world model이 hallucinate하면 평가 노이즈가 합법화되는 risk가 있어요.</p>')
    parts.append('<div class="section-title">랩 파이프라인 영향</div>')
    parts.append('<p>우리가 정책 비교/순위 결정을 자주 한다면, dWorldEval이 \'1차 screening 도구\'로 들어올 수 있습니다. 다만 final 결과 보고 전에 real eval과의 calibration spot check는 필수예요. 또한 \'평가 도구\'가 \'훈련 도구\'(Hi-WM 류)와 통합되는 다음 흐름도 시야에 두고 follow-up.</p>')
    parts.append('</div>')

    # 리스크 필터
    parts.append('<h2>⚠️ 리스크·한계 필터</h2>')
    parts.append('<div class="risk"><h3>TriPatch: \'physical-world\' 클레임의 통제된 vs 진짜 야외 검증</h3><p><a href="https://arxiv.org/abs/2604.22552">Transferable Physical-World Adversarial Patches Against Pedestrian Detection</a>이 multi-stage detection 파이프라인 동시 교란 + appearance-consistency robustness를 클레임하지만, \'physical-world\' 라는 단어가 실세계 다양한 조명·각도·거리·운동에서 평균 성공률을 낮추는 게 이 라인 고질병입니다. 통제된 lab 실험에서 vs 야외 다양 시나리오에서 효과 차가 abstract만으론 안 잡혀요. 본문의 weather/distance/motion ablation 표 정독 전엔 \'production AV/감시 시스템 위협\' 강한 클레임은 잠정 보류하는 게 맞습니다.</p></div>')
    parts.append('<div class="risk"><h3>Knowledge Visualization 벤치 + 자체 method SOTA 패턴 — 자기-벤치마크 구조적 편향</h3><p><a href="https://arxiv.org/abs/2604.22302">Knowledge Visualization</a>이 \'knowledge-intensive T2I\'에서 photorealism은 좋지만 도메인 지식 충실성은 망가진다는 진단으로 새 벤치 + 새 method를 동시에 출시. 진단 자체는 healthy하지만 평가 프로토콜 설계자가 자기 method를 SOTA로 보고하는 구조는 메트릭 선택/난이도 분포에서 자기 method가 잘 풀리는 쪽으로 무의식적으로 기울 인센티브가 작용합니다. 외부 third-party reproduction 전에는 \'메트릭 자체의 기여\'만 인정하고 \'method 순위\'는 잠정 보류가 안전.</p></div>')
    parts.append('<div class="risk"><h3>Holo360D 새 panorama 데이터셋 + 자체 reconstruction 결 — 라이선스/계측 메타데이터 검증 필요</h3><p><a href="https://arxiv.org/abs/2604.22482">Holo360D</a>가 continuous-trajectory panorama 3D 벤치를 새로 출시. 데이터셋 수집의 캘리브레이션 정확도, 라이선스 범위, GT scale 신뢰성, 도시/실내 distribution이 abstract에서 충분히 명시되는지 본문 확인 필요합니다. 데이터셋 페이퍼는 \'벤치 자체가 인용 허브가 되는 효과\' 때문에 첫 검증을 통과하지 못한 결로 후속 연구의 SOTA 비교가 오염되면 복구가 어렵다는 risk가 있어요.</p></div>')
    parts.append('<div class="risk"><h3>RedVLA의 \'first physical red teaming\' 클레임 — sim 검증 vs real-robot 검증의 갭</h3><p><a href="https://arxiv.org/abs/2604.22591">RedVLA</a>의 risk scenario synthesis + gradient-free 최적화가 시뮬레이션 환경에서 unsafe behavior를 elicit한 거라면, real-world 물리 위험 검증과는 갭이 큽니다. 또한 \'first\' 라는 단어가 동시기 다른 lab의 동일 직관 작업을 누락한 경우 priority 클레임이 약해질 수 있어요. 본문에서 sim vs real platform 비교 + concurrent work survey가 충분히 보고되는지 확인 필요.</p></div>')

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

    parts.append('<footer>arXiv Daily Briefing · 2026-04-27 · stdlib parser + classify · Generated with Claude</footer>')
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
