#!/usr/bin/env python3
"""Generate posts/2026-05-01.html from out/classified.json.

Self-contained: summaries are embedded inline rather than relying on out/summaries.py
(today's papers are not in that legacy file anyway).
"""
import json, html, io, os, sys

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

DATE = "2026-05-01"
WEEKDAY = "금"
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

# === Per-paper summaries (구어체, 3-5줄). Off-topic은 한 줄 코멘트로 짧게. ===
SUMMARIES = {
    # 3D/Scene
    "2604.27106": "RecGen이라는 generative framework로 occlusion이 심한 multi-object 장면을 sparse RGB-D 한두 장으로부터 확률적으로 재구성하는 결이에요. 기존 SAM3D는 강한 prior + 대규모 mesh가 필요했는데, RecGen은 80% 적은 학습 mesh로 geometric quality +30.1%, pose +33.9% 끌어올렸습니다. 'reconstruction by generation' framing이 sim2real 시뮬레이션 자산 만들기 측에서 즉시 가치가 있어 보여요.",
    "2604.27422": "Sparse view 3DGS인데 'in-the-wild' — 즉 distractor·illumination 변화가 있는 진짜 환경을 정조준한 결입니다. 기존 sparse 3DGS는 깨끗한 캡쳐 가정이 강했는데, 여기선 변동 환경에서도 robust한 학습. 오늘 sparse-view 3DGS 결이 4편 동시 등장한 것 중 가장 'wild' 측 결이라, 3DGS deployment의 실 환경 측면에서 흥미로워요.",
    "2604.27437": "Softmax-GS. 3DGS의 효율 가정 — Gaussian이 3D 공간에서 안 겹친다 — 이 장면 복잡도 올라가면 깨지는 문제를 generalized Gaussian 가족으로 풀어요. 각 Gaussian이 'blend할지 bound할지'를 학습해 결정하는 구조. 3DGS의 representation 측면 한계를 정조준한 결로 'production cost' 라인의 한 결입니다.",
    "2604.27552": "Cone-beam CT에서 ultra sparse-view(매우 적은 angle) 재구성용 residual 3DGS. 의료 응용이지만 'spectral bias under undersampling'을 residual 학습으로 푸는 아이디어는 일반 3DGS sparse view 결에도 transfer 가능. 오늘 sparse-view 4편 중 가장 도메인 특화된 결.",
    "2604.27590": "Fake3DGS — 3DGS scene 자체가 manipulate 가능해진 시점에 'editing detection'을 정조준한 첫 벤치마크. 기존 image forgery detection을 넘어 3D representation의 forensic axis를 새로 정의하는 결로, 향후 인용 모일 자리예요. 3DGS generation이 누적되는 흐름의 자연스러운 후속 자리.",
    "2604.27702": "RayFormer. NeRF 기반 video snapshot compressive imaging에서 'inter-/intra-ray similarity'를 transformer로 모델링한 결입니다. NeRF가 정적 scene 외 video SCI 같은 응용으로 확장되는 한 신호고, low-level vision 쪽 NeRF 응용 예시로 reference 가치 있어요.",
    "2604.28016": "Faster 3DGS convergence를 'structure-aware densification'으로 푸는 결. 기존 ADC가 screen-space gradient만 보던 것을 3D structure를 같이 보게 만들어 학습 시간을 줄였어요. 3DGS production cost 라인 — 학습 속도 측면에서 incremental하지만 잘 정렬된 결입니다.",
    "2604.28025": "절단된 사지(limb loss) 사용자에 대한 single-image human mesh recovery. 기존 SMPL 류는 표준 human topology를 가정해 절단 사례에서 깨졌던 자리를 'residual-limb aware' 모델링으로 풀어요. AR/VR rehabilitation 측 응용 결로, 일반 robot learning과는 거리가 있지만 fairness 측면에서 가치 있는 자리.",
    "2604.28045": "Point cloud geometry compression의 group-wise scalable 결. progressive residual refinement로 한 codec이 다양한 rate point에서 동작하게 만들어요. autonomous driving 측 LiDAR 데이터 압축 응용에서 흥미로운 결.",
    "2604.28064": "제조 도메인의 3D reconstruction 기법 review 논문. survey 측면에서 industry-context 정리에 가치 있고, 기존 학술 SOTA가 어디서 막히고 어디서 수용됐는지 단서로 읽으면 좋아요. 직접 모델 결은 아닙니다.",
    "2604.28122": "Vision Transformer의 feature space가 'Gaussian bottleneck'(즉 단순한 Gaussian 분포 가정)을 깨고 더 실제 분포에 fit하는 topologically aligned encoding을 제안. world model + 3D geometry의 physical consistency 측면에서 의미 있는 representation 결로, 단순 generation 너머 'physical structure preserving' 흐름과 같이 봐야 합니다.",
    "2604.28130": "MoCapAnything V2 — 임의 skeleton(로봇·만화캐릭터·동물 등)에 대해 monocular video로 end-to-end motion capture. 기존엔 video→pose→IK가 분리됐는데 V2는 통합 학습으로 skeleton diversity를 한 모델로 처리. 데이터 paper에 가까운 시스템 결이지만 manipulation 측 retargeting 인프라로 활용 가능.",
    "2604.28179": "Bronchoscopy navigation에서 호흡으로 인한 5~20mm CT-to-body divergence를 CT-informed dynamic GS로 보정. medical 측 결이지만 'dynamic GS + prior anatomy'라는 framing이 흥미롭고, 일반 dynamic 3DGS 라인과 같이 봐야 합니다.",
    "2604.28193": "Sparse view 3D reconstruction + 'unconstrained images'(illumination 변화·transient occlusion). 기존 scene-specific optimization을 generalizable feed-forward 모델로 끌어올린 결로 27422와 형제 자리. sparse view 3DGS line이 한 날 4편 동시에 누적된 강한 신호.",
    "2604.27323": "Hyperspectral image와 SAR/LiDAR fusion classification — remote sensing 측 결이라 우리 ROI와는 거리. 응용 대비는 reference로만.",
    "2604.27329": "SQuadGen. 3D mesh의 quad layout 자동 생성. graphics·CAD 측 결로, AI 생성 3D mesh의 후처리 측면에서 의미는 있지만 robot/CV 측 직접 영향은 작음.",
    "2604.28115": "FreeOcc — training-free, embodied open-vocabulary occupancy prediction. 기존 학습 기반 occupancy는 large 3D annotation 필요했는데 FreeOcc는 'training-free'로 환경 일반화를 정조준. embodied/AD 측 deployment에서 즉시 가치 있어요.",
    "2604.27450": "RAY-TOLD — ray-based latent dynamics를 TDMPC와 결합해 dense dynamic obstacle avoidance. crowd robotics 측 결로, MPPI의 local minima 자리를 정조준. SLAM/navigation 라인의 deployment 결.",
    "2604.27821": "Hierarchical scene graph matching으로 prior map 기반 robot localization. open-vocab semantic SLAM(어제 RADIO-ViPE)와 한 axis 다르게 'graph 구조 매칭'을 강조한 결입니다. localization 측 deployment에서 reference.",
    "2604.28111": "GSDrive — driving policy를 3DGS environment로 multi-mode trajectory probing 통해 RL 강화. 어제 GSDrive 후보들 흐름 위에 'closed-loop 학습 환경의 substrate가 3DGS'라는 paradigm을 더 분명히 합니다. AD에서 simulation 측 변곡점.",

    # Robot Learning
    "2604.27353": "이건 분류기가 RL 버킷에 잘못 매핑한 결입니다 — 사실 사람 보행(gait) 인식 결로 surveillance 응용이에요. 무시 가능.",
    "2604.27366": "Judge-Then-Drive. VLA가 driving control에 쓰일 때 'critic이 후보 action을 평가'하는 구조를 추가해 안전성을 끌어올린 결입니다. 기존 VLA는 mapping을 직접 했는데, 여기선 'propose → judge'라는 두 단계로 risky decision을 거르는 axis. AD 측 VLA의 흥미로운 결.",
    "2604.28022": "DeepFake detection 결로 RL/RO와 무관해 분류 잡음. 무시 가능.",
    "2604.27367": "DOT-Sim. 광학 tactile sensor의 differentiable simulator로, real-to-sim physical calibration을 정확하게 매칭해 sim2real gap을 줄여요. 기존엔 tactile rendering이 black-box였는데 DOT-Sim은 학습 신호를 sim 안에서 흘릴 수 있어 imitation/RL training에 즉시 substrate. tactile 측면 인프라 결의 한 변곡점.",
    "2604.27621": "Robot Learning from Human Videos: A Survey. embodied AI의 data scaling bottleneck을 'human video 활용'으로 뚫는 라인을 systematic하게 정리한 survey예요. task-/observation-/action-oriented 세 pathway taxonomy + 데이터셋·video gen 인프라 정리까지 — 우리 랩이 manipulation을 굴린다면 reference로 즉시 가치 있는 결. survey 결이지만 한 분야의 가치 정리는 향후 인용에서 큰 비중.",
    "2604.28192": "LaST-R1. VLA에 latent CoT reasoning + RL을 결합해 LIBERO에서 99.8% 평균 성공률(거의 ceiling). 기존 VLA RL은 raw action space만 최적화했는데, LaST-R1의 LAPO는 'latent reasoning + action'을 동시에 최적화 — 즉 VLA가 'physical하게 생각하고 행동'하게 만들었어요. 실 환경 4 task에서 +44%까지 개선. 오늘 must-read 1순위.",
    "2604.26988": "Active perception을 plan execution 중에 명시적으로 트리거하는 robot planning framework. 'plan만 짜는' 게 아니라 '관찰을 적극적으로 가져와 plan을 보정'하는 결로, dynamic 환경 측 결의 표준 후보. 어제까지 long-horizon planning 흐름의 한 axis 보강.",
    "2604.27175": "Contact-rich manipulation에서 KernelSOS — kernel sum-of-squares — 로 global trajectory optimization. 기존 sampling 기반 (e.g., MPPI) 결의 local minima 한계를 'global하게 푸는' 방향으로 끌어올린 결. 이론적 깊이가 있는 manipulation 결로, theoretical control + manipulation 라인 reference.",
    "2604.27224": "Quadruped loco-manipulation에 tactile feedback을 통합. 기존 vision+proprio 만으로 부족한 contact-rich 자리를 정조준해, '몸 전체로 만지는' 시나리오에서 robust한 정책을 학습. legged robotics의 manipulation 측 확장 흐름과 같이 봐야 해요.",
    "2604.27557": "Dexterous hand의 task-driven co-design. 기존 hand 설계는 control과 분리됐는데, 이 논문은 task evaluation을 hand morphology에 직접 흘려 'function 기반 parametric 최적화'. dexterous manipulation의 hardware-software 통합 흐름의 결.",
    "2604.27667": "Tabular foundation model(테이블 형태 데이터 위 사전학습 모델)을 robot policy 학습의 exploration guidance로 쓰는 결입니다. 'tabular FM이 high-dim continuous control의 exploration을 guide할 수 있나?'라는 흥미로운 framing. RL exploration 측면 새 paradigm 후보.",
    "2604.27792": "MotuBrain — UniDiffuser + three-stream MoT 구조로 video와 action을 unified 학습. 어제 X-WAM 흐름 다음으로 'unified video-action world model' 라인이 한 결 더 등장. 50배 inference speedup으로 real-time deployment를 정조준한 점이 차별. RL/imitation/inverse dynamics를 한 모델로 묶는 시도가 community에서 점점 누적되는 신호.",
    "2604.27935": "UAV swarm trajectory를 active inference로 굴리는 결. 'free energy minimization'으로 다중 UAV가 환경 변화에 적응. 기존 combinatorial optimization 측 한계를 generative inference로 우회. UAV swarms 측면에서 흥미로운 결.",
    "2604.28156": "FlexiTac. 저비용·open-source·scalable 압전 tactile sensor + 'plug-in' 모듈. 기존 sensors는 hardware 통합이 까다로웠는데 FlexiTac은 lab democratization 측면에서 가치. DOT-Sim이 sim 측이라면 FlexiTac은 real 측 — 같은 날 두 결이 같이 나오는 게 흥미롭네요.",
    "2604.28161": "RopeDreamer. Deformable Linear Object(끈·튜브) manipulation을 위한 kinematic recurrent state space model. 기존 DLO dynamics 모델링은 mesh/finite element가 흔했는데, RopeDreamer는 latent state space로 long-horizon prediction. deformable manipulation 측 RL/imitation 인프라 결.",
    "2604.27472": "PRTS. VLA pretraining이 supervised behavior cloning에 갇혀 있다는 진단에서 출발해, primitive reasoning + tasking을 contrastive representation으로 학습. VLA 측 학습 paradigm 측면 결로, LaST-R1의 'latent reasoning' 흐름과 같이 봐야 합니다.",
    "2604.27583": "유아의 first-person sensorimotor 경험을 motion retargeting으로 humanoid에 옮기는 결입니다. dev-psych + humanoid robotics 교차 결로, embodied learning curriculum 측 reference. 데이터 측면 흥미로운 결.",

    # Autonomous Driving
    "2604.27414": "VLM 기반 driving 시스템의 cross-architecture adversarial transferability 분석. 'VLM-AD가 robust한가?'를 정조준 — 한 architecture 위 attack이 다른 architecture로 얼마나 transfer되나가 연구의 본 axis. AD 측 VLM deployment의 silent failure 자리.",
    "2604.27448": "LA-Pose. Camera pose estimation을 inverse-dynamics pretraining 측면에서 self-supervised로 풀어요. AD pretraining 측면 흥미로운 결로, 'fully-supervised 3D annotation 의존도'를 줄이는 방향성.",
    "2604.27499": "Off-road nighttime driving용 large-scale multispectral 데이터셋 + benchmark. 야간 visible-light 한계를 IR로 보완하는 'all-day' 측 결. AD에서 가장 약한 자리(야간·off-road) 데이터 결로, 향후 인용 가능성 높습니다.",
    "2604.27617": "UAV의 bridge crack 분류 — civil engineering 측 결로 AD 측 ROI는 약함. lightweight model로 real-time 추론.",
    "2604.28196": "HERMES++. Driving world model이 future scene generation만 하던 한계를 정조준해 '3D scene understanding + future geometry prediction'을 한 framework로 통합. BEV-LLM, Current-to-Future Link, Joint Geometric Optimization으로 두 task가 충돌 없이 같이 굴러가게 만들었어요. AD 측 world model의 변곡점, 오늘 must-read 2순위.",
    "2604.27118": "PALCAS. Multi-agent federated RL로 lane change advisory. 'priority-aware'하게 emergency vehicle 등을 우선 처리하는 결로, federated learning + AD 결합의 응용 결.",
    "2604.27168": "Field of Safe Motion. 기존 'field of safe travel' affordance 개념을 reachability analysis로 operationalize한 결입니다. 차량 동역학을 정확히 반영한 safety field로, AD safety의 이론적 foundation 측 reference.",
    "2604.27193": "AEB 시스템의 NHTSA FMVSS No.127 인증을 위한 GPU 가속 Monte Carlo evaluation. 산업·인증 측 결로, 'safety case 만들기' 인프라.",
    "2604.27728": "Run-time function/anomaly monitoring을 'connected dependability cage'로 묶은 결. AV 안전 인증 흐름과 같이 봐야 합니다.",
    "2604.27994": "CARLA에서 zero-shot held-out town fixed-route driving. 'town-adversarial regularization + semantic rollout'으로 unseen town 일반화. closed-loop AD eval에서 흥미로운 결.",
    "2604.28057": "Marshaling yard 측 collaborative autonomous delivery vehicle framework. 산업 응용 측 결.",

    # Foundation Models
    "2604.27122": "Text-guided part matching으로 person re-identification — fine-grained part-level 정보 활용. CV 측 결로 우리 ROI 직접 영향은 작지만 VLM의 fine-grained alignment 라인의 한 사례.",
    "2604.27375": "VeraRetouch — 사진 retouching에 reasoning을 결합한 lightweight differentiable framework. Photo editing 응용 결.",
    "2604.27389": "COHERENCE. Interleaved multimodal context에서 fine-grained image-text alignment 평가 벤치마크. 기존 MLLM 평가가 single-image 측에 치우친 한계를 정조준한 결로, evaluation infra 측면에서 가치 있는 결입니다.",
    "2604.27476": "EdgeFM. VLM의 edge inference를 위한 deterministic low-latency 시스템 결. on-device VLM 측 deployment에서 흥미로운 결.",
    "2604.27505": "Image editing에 verifier-based RL을 적용 — RLHF가 T2I generation에는 표준이지만 editing은 unexplored했던 자리를 정조준. 'editing reward'의 generality가 핵심 자리.",
    "2604.27529": "CNN의 'Spatial Funnel Hypothesis'(deep encoder가 background를 suppress한다) 가정을 adjoint inversion으로 반증. interpretability 측 흥미로운 결로, 기존 CNN 해석 prior에 도전.",
    "2604.27553": "Visual text style이 LVLM의 attribute description에 미치는 영향을 systematic 평가 — same word, different style이 모델 출력을 어떻게 바꾸는지. VLM robustness 측면 새 axis.",
    "2604.27604": "SPUR. 과학 실험 이미지 perception/understanding/reasoning 평가 벤치마크 4264개 QA. scientific VLM 응용에서 reference 결로, MMMU/MathVista 라인의 도메인 특화 자리.",
    "2604.27715": "Test-time prompt tuning(TPT)에서 calibration drift 문제를 'data-free flatness-aware prompt pretraining'으로 보정. VLM의 confidence calibration 측면.",
    "2604.27932": "Vision-language pretraining의 비용을 줄이기 위한 dynamic cluster sampling. 'long-tail balance'와 효율을 동시에 잡는 시도.",
    "2604.27968": "Climate 관련 social media video 분석 — 응용 분야 결로 ROI 직접 영향은 약함.",
    "2604.27974": "FineState-Bench. GUI agent의 fine-grained state-conditioned grounding 평가 벤치마크. GUI agent line이 한 주 내내 누적되는 흐름과 같이 봐야 합니다.",
    "2604.27975": "TransVLM. Shot transition detection을 VLM framework로 푸는 결. video understanding 측 응용.",
    "2604.28011": "Echo-α. Ultrasound interpretation을 위한 large agentic multimodal reasoning model. 기존엔 detection / interpretation이 분리됐는데 한 모델로 통합. medical VLM 측 reference.",
    "2604.28177": "AEGIS. AI-generated academic image의 forensic 분석 평가 벤치마크. 학술 출판 ethics 측 결로, '논문 그림이 AI인가?' 평가가 표준화되는 흐름.",
    "2604.27953": "Visual priming이 VLM의 cooperative behavior에 미치는 영향. multi-agent VLM scenario 측 결로 흥미롭네요.",

    # Generation
    "2604.27322": "YOSE. DiT 기반 video object removal에서 token selection으로 latency를 줄임. video diffusion 가속 라인의 한 결.",
    "2604.27361": "CasLayout. Cascaded 3D layout diffusion으로 indoor scene synthesis — global architectural constraint와 local semantic을 동시에. 3D scene generation 측 결.",
    "2604.27504": "REVIVE 3D — 2D 이미지 기반 3D generation의 'volume hollow' 문제(내부가 비어있는 어색한 결)를 inflated prior로 채워 refinement. 3D generation 측 fidelity 결.",
    "2604.27875": "AI-generated image detection을 frequency-aware semantic fusion + gated injection으로. detection 측 결.",
    "2604.27889": "Noise2Map. Remote sensing의 segmentation·change detection을 end-to-end diffusion으로. dense prediction에 diffusion 적용한 결.",
    "2604.27903": "HiMix. Generalized synthetic image detection을 hierarchical artifact-aware mixup으로. 27875와 함께 detection 라인의 한 결.",
    "2604.27958": "TripVVT. Large-scale triplet 데이터셋 + coarse-mask baseline으로 in-the-wild video virtual try-on. data + baseline 측 reference.",
    "2604.28078": "AesRM. Video aesthetics(영화 같은 색·조명) 평가 reward model. video generation의 quality 평가가 photorealism 너머로 확장되는 흐름의 결.",
    "2604.28126": "AdvDMD. Diffusion distillation에 adversarial reward를 추가해 high-quality few-step generation. distillation 라인의 한 결.",
    "2604.28134": "3D-ReGen. 2D image + 초기 3D shape에서 3D를 'regenerate'하는 unified framework. 기존 one-shot 3D generator의 controllability 한계를 정조준.",
    "2604.28169": "PhyCo. Video diffusion의 'physical consistency'(물체 drift, 충돌 시 ricochet 부정확) 문제를 controllable physical priors로. 'visual generation in the new era' 흐름과 같이 봐야 해요.",
    "2604.28185": "Visual Generation in the New Era — five-level taxonomy(Atomic / Conditional / In-Context / Agentic / World-Modeling Generation)로 visual generation의 다음 단계를 framing한 position paper. 'photorealism은 풀렸으니 다음은 spatial reasoning + persistent state + causal understanding'이라는 메시지. 한 주 내내 누적된 'world model = foundation' 흐름의 자연스러운 종합 자리.",
    "2604.27277": "BrainDINO. Brain MRI foundation model을 self-supervised로 학습. medical 측 결로 ROI 직접 영향은 약함.",
    "2604.27955": "GUI Agents with RL — 'Toward Digital Inhabitants'. GUI agent line이 SFT 한계를 넘어 RL 측으로 이동하는 결.",
    "2604.27711": "ExoActor. Exocentric video generation을 humanoid control의 substrate로 — '비디오 생성으로 humanoid를 제어'하는 흐름. world model 흐름과 같이 봐야 합니다.",

    # Efficiency/Systems
    "2604.27128": "Livestock 모니터링용 SAM 3 + DINOv3 distillation 결. application 측면 결로 ROI는 약함.",
    "2604.27178": "Plant monitoring을 knowledge distillation으로 에너지 효율화. 응용 결.",
    "2604.27247": "Hedge mapping(독일 전국 단위) earth observation 결. ROI 약함.",
    "2604.27259": "VTBench. Time series classification을 chart-based 표현으로 — multimodal framework. 흥미롭지만 우리 ROI 직접 영향은 약함.",
    "2604.27833": "Federated learning에서 prototype degradation을 noise-resilient하게 푸는 결. privacy preserving 측면.",
    "2604.27870": "Translation-invariant CNN을 parameter-efficient하게 만든 architectural 결. 1-pixel shift에 fragile한 CNN의 알려진 약점을 정조준.",
    "2604.28123": "PRISM. Multimodal RL의 SFT distribution shift 문제를 'pre-alignment via black-box on-policy distillation'으로 우회. SFT-then-RLVR 표준 recipe의 한 axis 개선이라 LMM 측 reference 가치 있어요.",
    "2604.28190": "Fréchet distance를 학습 objective로 직접 최적화 — 기존엔 평가용으로만 썼던 자리를 representation space로 끌어들임. visual generation 측 새 loss 아이디어.",
    "2604.27326": "Hyperspectral image super-resolution. application 결.",
    "2604.27383": "Glottis segmentation in nasotracheal intubation. medical 측 결.",
    "2604.28148": "ThermoMesh — passive thin-film thermoelectric mesh sensor. hardware 결로 RO 측 일부 결.",

    # Embodied AI
    "2604.27445": "CatSignal. 비언어 agent(고양이·유아 등)의 intent를 spatial context를 prior로 둔 Bayesian framework로 추정. 'context-gated Product-of-Experts'로 ambiguous case의 shortcut 실패를 줄여요. 일반 embodied intent inference의 작은 testbed지만 framework는 transfer 가능.",
    "2604.27578": "World2Minecraft. 실세계 occupancy를 Minecraft 환경으로 변환해 VLN 같은 task를 효율적으로 굴림. 100,165개 이미지 156 scene MinecraftOcc 데이터셋도 함께 공개. embodied 시뮬레이션 측 인프라 결.",
    "2604.27620": "SpaAct. VLN에서 'spatially-activated transition learning + curriculum'으로 VLM의 navigation 적응. VLN line의 한 결.",

    # Safety/Alignment
    "2604.27343": "Skin lesion 다중모달 분류 — medical 결로 robotics safety와 거리가 멀어요. 분류 잡음.",
    "2604.27364": "Hyperspectral image classification — application 결.",
    "2604.27559": "Radiology report generation의 hierarchical alignment. medical VLM 측 결.",
    "2604.27582": "PDAC vascular invasion 평가 벤치마크. medical.",
    "2604.27591": "ClipTBP. Video moment retrieval의 temporal boundary prediction. video understanding 측.",
    "2604.27654": "CT-MRI 경추 등록. medical.",
    "2604.27759": "Domain knowledge를 fuzzy logic + targeted knowledge discovery로 robust image recognition에 결합. interpretability/robustness 측 결.",
    "2604.27918": "Talking avatar generation. multimedia 결.",
    "2604.28136": "Night photography rendering의 perceptual distortion 최소화. low-level vision.",
    "2604.27357": "Circle of Willis 다중 클래스 segmentation. medical.",
    "2604.27606": "ZAYAN. Tabular remote sensing data 측 representation. RS 응용.",
    "2604.28197": "OmniRobotHome. Multi-camera platform으로 real-time multiadic(다대다) human-robot interaction. 가정용 로봇이 'dyadic → multiadic' 흐름으로 가는 단서로 흥미. HRI 측 인프라 결.",
    "2604.27508": "SASI. Sub-action semantics를 활용한 robust early action recognition for HRI. 'robot이 사람의 action을 일찍 감지'가 안전한 협업의 substrate인데 그 자리를 정조준.",
    "2604.27267": "Holistic threat modeling of LLM-enabled robotic systems. STRIDE-per-interaction을 6 boundary point에 적용해 'LLM unsafe output → physical actuation'까지의 cross-boundary attack chain 3가지를 trace한 결입니다. LLM-as-controller가 robotics에 들어오는 흐름의 silent risk를 처음으로 architectural lens로 본 결로, 우리 LLM-controlled robot 라인이 있는 랩이라면 즉시 audit 후보.",
}

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
    parts.append('<div class="meta">')
    parts.append('<div><strong>시야:</strong> 주간 2026-04-25 ~ 2026-05-01 · 오늘 배치 cs.CV/new + cs.RO/new</div>')
    parts.append('<div><strong>소스:</strong> arxiv.org /list/cs.CV/new · /list/cs.RO/new (stdlib 파서 경유)</div>')
    parts.append('<div><strong>주간 규모:</strong> cs.CV 598편 · cs.RO 187편 (union ~785편 후보)</div>')
    parts.append('<div><strong>오늘 /new:</strong> cs.CV 166 + cs.RO 52 → 218 candidates → 132 ROI 매칭 → 107편 8개 ROI 버킷 선정</div>')
    parts.append('<div><strong>델타 기준:</strong> 7일 전 동급 스냅샷(2026-04-24 — 같은 1일 /new 단위)과 비교</div>')
    parts.append('</div>')

    # 주간 동향
    parts.append('<h2>🔭 주간 동향</h2>')
    parts.append('<p>이번주 가장 두드러진 매크로 신호는 <strong>3D/Scene이 다시 살아났다</strong>는 점이에요. 7일 전 13편 → 오늘 20편으로 <span class="hot">+54%</span> 급등했고, 그 안에서 sparse-view 3DGS 결만 4편(<a href="https://arxiv.org/abs/2604.27106">RecGen</a>·<a href="https://arxiv.org/abs/2604.27422">Sparse-View 3DGS in the Wild</a>·<a href="https://arxiv.org/abs/2604.27552">Residual GS for CBCT</a>·<a href="https://arxiv.org/abs/2604.28193">Generalizable Sparse-View Recon</a>) 동시에 등장했습니다. 어제까지 \'3DGS deployment의 production cost\'였다면 오늘은 \'sparse view에서도 robust한가\'로 community focus가 이동한 모양새고, 이건 driving simulation·embodied data scaling 모두에 직접 영향을 끼치는 자리라 한동안 갈 것 같습니다.</p>')
    parts.append('<p>오늘 /new에서 제일 흥미로운 건 <strong>VLA의 reasoning 측면이 \"linguistic CoT\" → \"physical latent reasoning + RL\"로 paradigm shift</strong>하는 구체적 결이 등장했다는 점이에요. <a href="https://arxiv.org/abs/2604.28192">LaST-R1</a>이 latent CoT + LAPO(Latent-to-Action Policy Optimization)로 LIBERO에서 99.8% 평균 성공률(거의 ceiling) + 실 환경 4 task에서 +44% 개선을 보여줬고, 같은 날 <a href="https://arxiv.org/abs/2604.27792">MotuBrain</a>이 UniDiffuser + three-stream MoT로 video와 action을 unified 학습하면서 50배 inference speedup. <a href="https://arxiv.org/abs/2604.27472">PRTS</a>도 VLA pretraining의 SFT 측 한계를 contrastive primitive reasoning으로 우회. 어제 X-WAM·STARRY·World2VLM이 \"world model = substrate\"였다면, 오늘 이 셋은 그 substrate 위에서 \"reasoning을 어떻게 굴릴 것인가\"를 정조준하는 결이라, 흐름이 한 단계 더 deployment 측으로 내려왔다고 봐요.</p>')
    parts.append('<p>부상 중인 미니 토픽 두 개. 첫째, <strong>LLM-controlled robot의 architectural threat modeling</strong>이 처음 표면화. <a href="https://arxiv.org/abs/2604.27267">From Prompt to Physical Actuation</a>이 STRIDE-per-interaction을 6 boundary point에 적용해 \"prompt → unsafe physical actuation\" cross-boundary attack chain 3가지를 trace — robotics cybersecurity·adversarial perception·LLM safety가 따로 굴러왔던 결을 한 architectural lens로 통합한 첫 결. 어제 LLM Robotic Health Attendant Safety가 \"sample 측면\"이었다면 오늘은 \"architecture 측면\"으로 한 단계 위. 둘째, <strong>Driving world model의 \"understanding + generation\" 통합</strong>이 <a href="https://arxiv.org/abs/2604.28196">HERMES++</a>로 정리되는 결이 등장. 기존 driving WM이 future scene generation에 치우쳤던 한계를 BEV-LLM + Joint Geometric Optimization으로 두 task를 한 모델로 푸는 framing — AD 라인이 일주일 7→11편(<span class="hot">+57%</span>) 누적되는 흐름의 정점 결.</p>')

    # CV vs RO
    parts.append('<h2>📐 CV vs RO 대비</h2>')
    parts.append('<p>오늘 분포는 3D/Scene(20)·Robot Learning(17)·Foundation Models(16)·Generation(15)·Safety(14)·Autonomous Driving(11)·Efficiency(11)·Embodied AI(3)으로, <em>3D/Scene이 단독 1위에 올라왔고 RL이 그 뒤를 따르는</em> 모양새예요. 7일 전 대비 가장 큰 변화는 3D/Scene <span class="hot">+54%</span>(13→20)와 AD <span class="hot">+57%</span>(7→11) 두 자리 surge, 그리고 Safety <span class="cold">-48%</span>(27→14) cooling. 어제까지 Generation이 단독 톱이었다면 오늘은 \"3D/Scene + RL + AD\" 셋이 동시에 surge하면서 deployment 측 결이 community 무게중심을 잡은 모양새. RO 비중은 17 RL 중 11편이 RO 전용이고 AD 11 중 6편이 RO — 양쪽 모두 RO 비중이 60% 가까이 올라온 것도 한 주 흐름 안에서 가장 RO-heavy한 자리예요.</p>')
    parts.append('<div class="contrast">')
    parts.append('<p><strong>① 공통으로 뜨는 키워드</strong></p>')
    parts.append('<ul>')
    parts.append('<li><code>3DGS</code> — CV(<a href="https://arxiv.org/abs/2604.27422">Sparse-View in the Wild</a>·<a href="https://arxiv.org/abs/2604.27437">Softmax-GS</a>·<a href="https://arxiv.org/abs/2604.27552">Residual GS</a>·<a href="https://arxiv.org/abs/2604.28016">Faster Convergence</a>) + RO(<a href="https://arxiv.org/abs/2604.28111">GSDrive</a>) — CV는 \"sparse view + 효율\", RO는 \"RL training environment\"로 같은 기술을 다른 layer에서 활용</li>')
    parts.append('<li><code>world model + action</code> — CV(<a href="https://arxiv.org/abs/2604.28196">HERMES++</a> driving WM·<a href="https://arxiv.org/abs/2604.28185">Visual Generation taxonomy</a>) + RO(<a href="https://arxiv.org/abs/2604.27792">MotuBrain</a>·<a href="https://arxiv.org/abs/2604.28192">LaST-R1</a>·<a href="https://arxiv.org/abs/2604.27472">PRTS</a>) — 어제 \"substrate\" 흐름 위에서 오늘은 \"reasoning + action\" 측 후속</li>')
    parts.append('<li><code>tactile / contact-rich</code> — RO(<a href="https://arxiv.org/abs/2604.27367">DOT-Sim</a>·<a href="https://arxiv.org/abs/2604.27224">Tactile Quadruped</a>·<a href="https://arxiv.org/abs/2604.28156">FlexiTac</a>·<a href="https://arxiv.org/abs/2604.27175">KernelSOS contact-rich</a>) — sim 측·real 측·planning 측이 한 날 같이 등장하는 게 흥미</li>')
    parts.append('</ul>')
    parts.append('<p><strong>② CV에만 뜨는 키워드</strong></p>')
    parts.append('<ul>')
    parts.append('<li><code>AI-image forensics</code> — <a href="https://arxiv.org/abs/2604.27590">Fake3DGS</a>·<a href="https://arxiv.org/abs/2604.27875">Frequency-Aware Detection</a>·<a href="https://arxiv.org/abs/2604.27903">HiMix</a>·<a href="https://arxiv.org/abs/2604.28177">AEGIS</a> — \"AI-generated image detection\"이 한 날 4편 누적, 3DGS forensic까지 추가</li>')
    parts.append('<li><code>VLM evaluation 인프라</code> — <a href="https://arxiv.org/abs/2604.27389">COHERENCE</a>·<a href="https://arxiv.org/abs/2604.27604">SPUR</a>·<a href="https://arxiv.org/abs/2604.27974">FineState-Bench</a>·<a href="https://arxiv.org/abs/2604.27553">Visual Text Style</a> — interleaved/scientific/GUI/style 4 axis로 새 평가 벤치 등장</li>')
    parts.append('<li><code>video generation refinement</code> — <a href="https://arxiv.org/abs/2604.28078">AesRM</a>·<a href="https://arxiv.org/abs/2604.28169">PhyCo</a>·<a href="https://arxiv.org/abs/2604.28126">AdvDMD</a> — photorealism 너머 \"aesthetics·physics·distillation\"로 한 단계 위</li>')
    parts.append('</ul>')
    parts.append('<p><strong>③ RO에만 뜨는 키워드</strong></p>')
    parts.append('<ul>')
    parts.append('<li><code>tactile sensor 인프라</code> — <a href="https://arxiv.org/abs/2604.27367">DOT-Sim</a>(sim) + <a href="https://arxiv.org/abs/2604.28156">FlexiTac</a>(real) — sim/real 양쪽 인프라가 같은 날 등장하는 건 라인 성숙 신호</li>')
    parts.append('<li><code>deformable / dexterous manipulation</code> — <a href="https://arxiv.org/abs/2604.28161">RopeDreamer</a> DLO·<a href="https://arxiv.org/abs/2604.27557">Dexterous Co-Design</a>·<a href="https://arxiv.org/abs/2604.27175">KernelSOS</a> — \"hard manipulation\" 자리</li>')
    parts.append('<li><code>UAV swarm / autonomous fleet</code> — <a href="https://arxiv.org/abs/2604.27935">Active Inference UAV Swarm</a>·<a href="https://arxiv.org/abs/2604.28057">Marshaling Yard Delivery</a> — 다중 agent 측 결</li>')
    parts.append('<li><code>LLM threat modeling</code> — <a href="https://arxiv.org/abs/2604.27267">Prompt to Physical Actuation</a> — LLM-as-controller의 architectural risk를 처음으로 통합 분석</li>')
    parts.append('</ul>')
    parts.append('<p><strong>④ 같은 단어 다른 맥락</strong></p>')
    parts.append('<ul>')
    parts.append('<li><code>3DGS</code>: CV는 \'sparse view + production cost\'(렌더링 품질) / RO는 \'closed-loop RL training environment\'(GSDrive처럼 simulation substrate) — 같은 기술이 \"asset\" vs \"environment\"로 정반대 layer 활용</li>')
    parts.append('<li><code>world model</code>: CV는 \'driving scene understanding + generation 통합\'(HERMES++) / RO는 \'video-action unified 정책 학습\'(MotuBrain·LaST-R1) — \"perception + prediction\" vs \"perception + action\"</li>')
    parts.append('<li><code>safety</code>: CV는 \'AI-image forensics·OOD\' (Fake3DGS·AEGIS·HiMix) / RO는 \'physical actuation 측 architectural risk\'(<a href="https://arxiv.org/abs/2604.27267">Prompt-to-Actuation</a>·<a href="https://arxiv.org/abs/2604.27728">Dependability Cage</a>) — \"위조 검출\" vs \"행동 결과 통제\"로 정반대</li>')
    parts.append('</ul>')
    parts.append('</div>')
    parts.append('<p>오늘의 CV/RO 교집합은 <em>3DGS와 world model이 \"asset/representation\"을 넘어 \"interactive substrate\"가 되는 흐름</em>이에요. 어제까지 world model이 substrate라는 메시지였다면, 오늘은 그 substrate가 양 modality에서 다른 layer로 활용되는 구체적 결이 등장 — CV는 generation/understanding 통합 (HERMES++), RO는 action policy의 reasoning 강화 (LaST-R1·MotuBrain). \"world model\"이라는 단어 안에 \"reasoning prior · action substrate · simulation environment\" 세 axis가 모두 살아있는 단계로 볼 수 있고, 이 균형이 향후 6개월 community key word를 결정할 거라고 봅니다.</p>')

    # 인사이트
    parts.append('<h2>💡 오늘의 인사이트</h2>')
    parts.append('<div class="insight"><h3>VLA reasoning paradigm shift — \"linguistic CoT\" → \"physical latent reasoning + RL\"이 한 날 3편으로 표면화</h3><p>오늘 <a href="https://arxiv.org/abs/2604.28192">LaST-R1</a>이 latent CoT reasoning + LAPO로 LIBERO 99.8% (거의 ceiling) + 실 환경 +44% 개선을 보여주고, <a href="https://arxiv.org/abs/2604.27792">MotuBrain</a>이 UniDiffuser + 3-stream MoT로 video·action을 unified로 묶으면서 50배 speedup, <a href="https://arxiv.org/abs/2604.27472">PRTS</a>가 VLA pretraining의 SFT 한계를 contrastive primitive reasoning으로 우회 — 한 날 3편이 \"VLA의 reasoning을 어디서 어떻게 표현할 것인가\"를 동시에 정조준했어요. 어제 X-WAM·STARRY·World2VLM이 \"world model = substrate\"였다면, 오늘은 그 substrate 위에서 \"reasoning을 어떻게 굴리고 RL로 어떻게 강화할까\"가 community focus의 다음 layer가 됐다는 신호. 우리 VLA 스택이 explicit linguistic CoT에 갇혀 있다면 latent reasoning + LAPO 류 paradigm으로 audit이 시급해진 시점이에요.</p></div>')
    parts.append('<div class="insight"><h3>3D/Scene이 \"production cost\" → \"sparse view robustness\"로 focus 한 단계 이동</h3><p>일주일 13→20편(<span class="hot">+54%</span>) 급등 안에서 <a href="https://arxiv.org/abs/2604.27106">RecGen</a>(generative recon, 80% 적은 데이터로 +30%)·<a href="https://arxiv.org/abs/2604.27422">Sparse-View in the Wild</a>·<a href="https://arxiv.org/abs/2604.27552">Residual GS for CBCT</a>·<a href="https://arxiv.org/abs/2604.28193">Generalizable Sparse-View Recon</a> 4편이 모두 \"sparse view에서도 robust한가\"를 정조준. 어제까지 EnerGS·MesonGS++가 \"production cost\"였다면, 오늘은 그 cost를 \"data 측\"에서 줄이는 결로 한 단계 이동했어요. 3D/Scene 라인이 \"품질 → cost → sparse data robustness\"의 3단계로 stepwise 진화하는 모양새고, 이게 driving simulation·embodied data scaling 모두에 직접 substrate가 되니까 한동안 갈 것 같습니다.</p></div>')
    parts.append('<div class="insight"><h3>LLM-controlled robot의 \"architectural threat surface\"가 처음으로 통합된 lens로 분석됨</h3><p><a href="https://arxiv.org/abs/2604.27267">From Prompt to Physical Actuation</a>이 STRIDE-per-interaction을 LLM-enabled robot의 6 boundary point에 적용해 \"prompt → unsafe physical actuation\" cross-boundary attack chain 3가지를 trace — \"independent semantic validation 부재\"·\"cross-modal translation\"·\"unmediated provider tool use\" 세 architectural property를 silent risk로 식별. 어제 \"LLM Robotic Health Attendant Safety\"가 sample 270개 측 결이었다면, 오늘은 architecture 측 결이라 \"무엇을 audit할 것인가\"의 framework 자체를 제공해요. LLM-as-controller 라인이 있는 랩이라면 즉시 우리 시스템의 boundary diagram + STRIDE audit이 첫 follow-up.</p></div>')

    # 추천 연구주제
    parts.append('<h2>🔬 추천 연구주제</h2>')
    parts.append('<div class="topic"><h3>VLA Reasoning Atlas — Linguistic CoT vs Latent CoT vs Continuous Latent × LIBERO/CALVIN/RoboCasa</h3><p>오늘 LaST-R1(latent CoT + LAPO) · MotuBrain(unified video-action) · PRTS(contrastive primitive reasoning)이 모두 \"VLA reasoning을 어디서 표현하나\"를 다른 axis로 정조준했지만, 같은 LIBERO/CALVIN 위에서 정량 비교는 비어 있어요. \"linguistic CoT vs latent CoT vs continuous latent vs no reasoning\" 4 paradigm × 3 표준 벤치 atlas로 묶으면 향후 6주 안에 community standard 후보. 우리 랩이 VLA 인프라가 있다면 first-mover 자리고, LaST-R1의 99.8% ceiling이 진짜 ceiling인지 paradigm 비교에서 명확해질 자리예요.</p></div>')
    parts.append('<div class="topic"><h3>Sparse-View 3DGS Robustness Suite — In-the-Wild × Generalizable × Domain-Transfer atlas</h3><p>오늘 sparse-view 3DGS 4편(RecGen·In the Wild·Residual GS·Generalizable)이 모두 \"sparse view에서 robust\"를 정조준했지만, 같은 \"sparse view\" 라벨 안에서 \"in-the-wild distractor\" vs \"few training meshes\" vs \"medical ultra-sparse\" vs \"unconstrained illumination\"로 axis가 달라요. ScanNet++/Mip-NeRF 360 위에서 4 axis 통합 robustness suite를 만들면 향후 sparse-view deployment 측 reference로 즉시. driving simulation/embodied data 측 응용에서도 substrate라 paper 1편으로도 인용 모일 자리.</p></div>')
    parts.append('<div class="topic"><h3>LLM-Robot Threat Audit Framework — STRIDE × DFD × 우리 랩 LLM-controlled robot 시스템</h3><p>오늘 <a href="https://arxiv.org/abs/2604.27267">Prompt to Physical Actuation</a>이 LLM-enabled robot의 첫 architectural threat model을 정의했지만, 이를 \"실제 lab 시스템에 적용한 case study\"는 비어 있어요. 우리 랩이 LLM-controlled robot을 굴린다면 같은 STRIDE-per-interaction framework로 \"우리 시스템의 boundary 어디가 attack chain의 weak point인가\"를 audit한 case study paper가 즉시 가치. 일반 cybersecurity audit과 다른 \"physical world consequence\" 측 정량 평가 framework가 동시에 필요한 자리고, 이건 향후 1년 robotics safety 측 첫 표준이 될 가능성이 큽니다.</p></div>')

    # 회고 — 금요일이라 skip
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
    parts.append(f'<p>🔥 <span class="hot">TOP3</span>: {top3[0][0]} ({top3[0][1]}), {top3[1][0]} ({top3[1][1]}), {top3[2][0]} ({top3[2][1]}) · ❄️ <span class="cold">BOTTOM2</span>: {bot2[0][0]} ({bot2[0][1]}), {bot2[1][0]} ({bot2[1][1]}). 오늘 가장 큰 변화는 3D/Scene이 단독 1위에 올라온 것(7일 전 13편 → 오늘 20편, +54%)과 AD가 11편으로 +57% surge한 점. 반면 Safety가 14편(-48%)으로 한 주 cooling되고, Generation도 -25%로 한 주 1위 자리에서 내려와 Generation·Safety 양강 구도가 깨졌어요. Embodied AI는 3편으로 한 주 내내 가장 조용한 자리.</p>')

    # 델타 (vs 7일 전)
    parts.append('<p>📈 <strong>주간 델타(2026-04-24 → 2026-05-01, 7일 시야 — 같은 1일 /new 단위)</strong>: 🚗 Autonomous Driving <span class="hot">+57%</span> (7→11), 📦 3D/Scene <span class="hot">+54%</span> (13→20), 🏃 Embodied AI <span class="hot">+50%</span> (2→3), 🤖 Robot Learning <span class="hot">+13%</span> (15→17), ⚡ Efficiency <span class="cold">+0%</span> (11→11), 🧠 Foundation Models <span class="cold">-16%</span> (19→16), 🎨 Generation <span class="cold">-25%</span> (20→15), 🛡️ Safety/Alignment <span class="cold">-48%</span> (27→14). 가장 명확한 신호는 \"AD·3D·Embodied\" 3축이 동시에 surge한 것 — 모두 \"physical world deployment\" 측 결이라는 공통점이 있어요. 한 주 누적 패턴은 \"Generation·Safety 양강\"에서 \"deployment-heavy 3축\"으로 무게중심이 이동하는 모양새. Embodied는 base가 작아 +50%가 통계적으론 노이즈 수준이지만, AD+3D 양쪽이 50%+로 surge한 신호와 같이 보면 의미 있는 흐름.</p>')

    # 벤치마크 SOTA — 신규 SOTA 보고
    parts.append('<h2>📈 벤치마크 SOTA 추이</h2>')
    parts.append('<table style="border-collapse:collapse;width:100%;font-size:13.5px;margin:12px 0">')
    parts.append('<thead><tr style="background:#f6f8fa;border-bottom:1px solid #d0d7de"><th style="text-align:left;padding:8px">벤치마크</th><th style="text-align:left;padding:8px">메트릭</th><th style="text-align:right;padding:8px">이번주 최고</th><th style="text-align:left;padding:8px;padding-left:14px">논문</th></tr></thead>')
    parts.append('<tbody>')
    parts.append('<tr style="border-bottom:1px solid #eaeef2"><td style="padding:8px"><strong>LIBERO</strong></td><td style="padding:8px">평균 SR</td><td style="padding:8px;text-align:right;font-family:ui-monospace,monospace">99.8%</td><td style="padding:8px;padding-left:14px"><a href="https://arxiv.org/abs/2604.28192">LaST-R1</a></td></tr>')
    parts.append('<tr style="border-bottom:1px solid #eaeef2"><td style="padding:8px"><strong>real-world manipulation (4 task)</strong></td><td style="padding:8px">improvement vs warm-up</td><td style="padding:8px;text-align:right;font-family:ui-monospace,monospace">+44%</td><td style="padding:8px;padding-left:14px"><a href="https://arxiv.org/abs/2604.28192">LaST-R1</a></td></tr>')
    parts.append('<tr style="border-bottom:1px solid #eaeef2"><td style="padding:8px"><strong>SAM3D-style sparse recon</strong></td><td style="padding:8px">Geometric quality</td><td style="padding:8px;text-align:right;font-family:ui-monospace,monospace">+30.1%</td><td style="padding:8px;padding-left:14px"><a href="https://arxiv.org/abs/2604.27106">RecGen</a></td></tr>')
    parts.append('<tr><td style="padding:8px"><strong>real-time VLA inference</strong></td><td style="padding:8px">speedup</td><td style="padding:8px;text-align:right;font-family:ui-monospace,monospace">50×</td><td style="padding:8px;padding-left:14px"><a href="https://arxiv.org/abs/2604.27792">MotuBrain</a></td></tr>')
    parts.append('</tbody></table>')
    parts.append('<p>오늘은 LIBERO에서 LaST-R1이 평균 99.8%로 사실상 ceiling을 친 게 가장 큰 이벤트예요. 다만 LIBERO 자체가 실 환경의 long-tail을 충분히 반영하지 못한다는 비판이 한 주 흐름 안에 누적된 자리라, \"99.8% = solved\"보다 \"LIBERO의 ceiling이 닿았으니 다음 벤치(CALVIN·RoboCasa·실 환경)로 무게가 옮겨갈 것\"으로 해석하는 게 안전합니다. ScanNet++/Mip-NeRF 360 측 새 SOTA 보고는 잡힌 게 없어, 표는 최소 보고만.</p>')

    # 크로스오버 페어
    parts.append('<h2>🔀 크로스오버 페어</h2>')
    parts.append('<div class="crosspair"><h3>같은 \"world model\", 다른 task layer — HERMES++(CV/AD) vs MotuBrain(RO)</h3><p><a href="https://arxiv.org/abs/2604.28196">HERMES++</a>(CV/AD)이 driving world model의 \"future scene generation\" + \"3D scene understanding\"을 한 framework로 통합하고, 같은 날 <a href="https://arxiv.org/abs/2604.27792">MotuBrain</a>(RO)은 video와 action을 UniDiffuser + 3-stream MoT로 unified 학습. 둘 다 \"world model을 단일 unified framework로\"라는 같은 paradigm을 공유하지만, HERMES++는 \"perception + prediction\"이고 MotuBrain은 \"perception + action\"이라 같은 단어가 \"이해 측\" vs \"행동 측\"으로 분기. 같은 paradigm이 두 측면에서 동시 표면화하는 건 \"world model = unified substrate\"가 community 양쪽에서 설계 표준이 되는 신호.</p></div>')
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
