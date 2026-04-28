#!/usr/bin/env python3
"""Generate posts/2026-04-28.html from out/classified.json"""
import json, html, io, os, sys

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

DATE = "2026-04-28"
WEEKDAY = "화"
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

# Per-paper Korean summaries (구어체, 핵심만 짧게)
SUMMARIES = {
# === 3D/Scene ===
'2604.22826': "Surface mesh를 token-level dense embedding으로 변환하는 self-supervised 3D foundation model. CAD 도메인 특화지만 'mesh가 직접 입력으로 들어가는' 라인의 결로, 산업 BIM·역공학 파이프라인에 곧장 들어갑니다. Pretraining 규모(61K mesh)는 도메인치곤 충분.",
'2604.22827': "mmWave radar로 사람 mesh 재구성하는 dual-radar 데이터셋 + generalization 벤치. 비침습 sensing 라인 결로, 카메라가 못 들어가는 환경(병원·집·노약자 케어)에 영향. Configuration shift 평가가 들어간 게 healthy.",
'2604.22865': "Single-image animatable head avatar를 feed-forward로 — test-time optimization 없이 한 번에. AR/VR avatar production 인프라에 직접 영향, 기존 NeRF/3DGS 기반 head reconstruction의 'minutes per avatar' 한계를 끊는 결.",
'2604.22883': "Brain MRI를 point cloud로 변환해 neuro-anatomically aware encoding. 3D CNN 대비 lightweight하면서 Alzheimer 진단 정확도 유지를 노립니다. 의료 영상이 voxel 대신 point cloud로 가는 흐름의 한 사례.",
'2604.23095': "실내 안전 인프라(소화기·비상구) 위치를 3D semantic segmentation으로 자동 매핑 — 첫 응답자 시나리오가 motivating. Public-safety 도메인이 '실외 GPS 인프라'에 대응되는 'indoor spatial intelligence' 라인을 새로 정의.",
'2604.23551': "Underwater 3DGS에 caustics·flickering·attenuation·backscattering 같은 spatiotemporal degradation을 명시적으로 모델링. '기존 3DGS는 깨끗한 air 환경 가정'이라는 한계를 한 단계 끊는 결로, 해양 inspection 응용에 직접 영향.",
'2604.23604': "3D LiDAR 도메인의 anomaly segmentation — known class와 unseen object를 명시적으로 구별. 자율주행 perception에서 OOD 처리가 의외로 비어있던 자리를 메우는 결입니다. CV/RO 양쪽 카테고리에 동시 등록.",
'2604.23704': "Multi-camera bundle adjustment에서 feature redundancy를 pose-only geometric constraint로 정리. SfM/3DGS 파이프라인 backend의 효율 결로, large-scale reconstruction 사람들에게 곧장 가치 있어요.",
'2604.23803': "Egocentric 비디오의 dynamic 3DGS — rapid camera motion + scene dynamic이 동시 발생하는 가장 어려운 setting을 정조준한 평가 자료. AR/robotic vision 측 baseline 정리에 도움.",
'2604.24053': "Low-light 환경 360° 3DGS. 노이즈 amplification + view-dependent photometric inconsistency를 multi-scale explicit prior로 풀어요. 야간 자율주행·실내 dim-light 측 응용에 들어갈 수 있는 결.",
'2604.24169': "Custom CUDA operator 의존도를 없앤 portable point cloud transformer. AMD/embedded 같은 비-NVIDIA 환경 deployment 라인의 결로, edge robotics에 직접 영향.",
'2604.24187': "Multivariate Gaussian NeRF로 wide field-of-view 초음파 재구성. Convex probe의 diverging acoustic beam이라는 도메인 특수성에 NeRF 표현이 자연스럽게 fit. 의료 영상 inverse problem에 NeRF 도메인 확장.",
'2604.24311': "건물 스캔에서 자동 BIM 생성하는 hybrid scan-to-BIM 파이프라인. IFC 호환 출력이라 산업 표준에 직접 들어가요. 학술 결보다 deployment-ready 측면이 강한 인프라 결입니다.",
'2604.24370': "Multispectral 항공 LiDAR 데이터셋(나무 종 분류용). Boreal 생태계 모니터링 응용 결로, biodiversity 측 데이터 인프라 자료. ROI 주변부긴 한데 LiDAR 데이터셋으로 분류기에 잡혔어요.",
'2604.24479': "B-Rep/mesh 데이터셋이 CAD의 'parametric construction history'를 제거해버린다는 진단에서 출발 — agentic synthesis로 million-scale interpretable CAD program을 real CAD data 없이 생성. CAD generation 라인의 데이터 인프라 결.",
'2604.24586': "Single image → 1-step point cloud generation via mean flows. Diffusion-based reconstructor의 'many denoising step' 비용 문제를 mean flow 한 번으로 끊는 결로, on-device 3D 응용에 가치.",
'2604.23675': "Diffuse optical tomography(DOT) reconstruction에 Gaussian splatting을 사용. 의료 영상의 inverse problem에 GS 표현이 들어가는 흐름의 결로, 'GS는 rendering 전용'이라는 통념을 넘어가는 사례.",
'2604.24415': "Markerless 3D pose data에 phase-separated complex Hilbert PCA로 글로벌 phase를 측정. Sports motion 분석 응용 결로, kinematic-sequence 분석 측 정량 도구 라인에서 niche이지만 명확한 위치.",
'2604.23033': "Radar-Inertial Odometry용 equivariant filter — extrinsic calibration 정확도와 disturbance robustness를 동시에 다룸. RIO 라인의 EKF 한계를 끊는 결로, all-weather 자율주행/UGV 측 odometry에 영향.",
'2604.24033': "High-speed maneuver용 event-based SLAM 벤치마크. Event camera가 microsecond 해상도로 빠른 동작에 강점인데, 표준 평가 setup이 부재했던 자리를 정리하는 인프라 결입니다.",
'2604.24449': "Image-based tactile sensor에서 'physical-contact'를 latent arithmetic으로 분리하는 SPLIT. Tactile 데이터 생성/증강의 기초 결로, contact-rich manipulation 라인의 데이터 부족 문제를 latent space에서 우회합니다.",
'2604.24628': "트랙터-탑재 stereo + LiDAR 데이터셋, real baling 작업에서 windrow 검출. 농업 자동화 측 인프라 자료로, '오픈 데이터셋이 부재해 progress가 막혀있다'는 motivating이 healthy합니다.",
'2604.24674': "Off-road radar odometry — urban planar setting에서 잘 되던 radar 기법이 비포장에서 망가진다는 진단부터. 'radar는 weather robust' 클레임의 실제 한계를 정량화하는 결.",
'2604.24707': "RGB-D VSLAM에서 doorway/passage를 명시적으로 구조 요소로 다루는 passage-aware mapping. 실내 navigation 응용 결로 'door가 SLAM에서 underexplored'라는 직관적 motivating이 좋아요.",

# === Robot Learning ===
'2604.23387': "Event camera로 동적 객체의 6-DoF pose tracking — motion blur·sensor noise·low-light 한계를 keypoint-based로 정조준. Manipulation의 'object pose가 fast-moving일 때 망가진다'는 패턴을 event sensor로 우회.",
'2604.24426': "AI 비디오 조작 검출용 spatial+spectral+temporal multi-domain 프레임워크. Robot learning 버킷에 분류됐지만 실제론 deepfake 검출 결 — keyword 매칭 결과 범위 외라 incremental.",
'2604.24622': "Flow-based VLA의 'multi-step inference 부담' 한계를 coarse-to-fine action 생성으로 줄이는 CF-VLA. VLA inference latency 라인의 대표 결로, edge deployment 측에 직접 가치.",
'2604.23121': "Low-data demonstration으로 VLA를 post-training하면 새 instruction에 반응을 멈추는 'lock-in' 현상을 진단하고 처방. VLA practitioner라면 반드시 봐야 할 failure mode 분석. 오늘자 must-read에서 자세히.",
'2604.22911': "Humanoid recovery policy를 contact-aware end-to-end로. Disturbance에서 회복하는 능력을 contact event 인식 + 모드 switching으로 구현. Humanoid의 'fall recovery'가 학습 가능 목표로 굳어가는 흐름.",
'2604.23000': "Behavioral cloning 데이터 quality를 smoothness-driven metric으로 측정 — operator skill 차이로 trajectory quality가 들쭉날쭉한 real-world dataset의 silent killer를 정조준. BC 데이터 큐레이션의 표준 도구가 될 수 있는 결.",
'2604.23001': "VLA 다음 진보는 architecture가 아니라 'data infrastructure에서 온다'는 강한 클레임의 survey. Open-X 이후 데이터 엔진 라인 정리로, 우리 manipulation 스택의 데이터 파이프라인 재정비에 reference로 들어옵니다. 오늘자 must-read에서 자세히.",
'2604.23039': "Hierarchical QP로 control barrier function을 풀어 physical human-robot interaction의 safety를 보장. 재활 로봇용 결로, CBF 라인이 hierarchical 구조와 결합되는 흐름.",
'2604.23249': "Human video → robot action transfer를 unified tool-target affordance로 풀기. Affordance가 인간/로봇 embodiment gap을 잇는 표준 인터페이스로 굳어가는 흐름의 또 다른 결.",
'2604.23272': "VLA에 vision 외 physical sensory(force/tactile)를 modular하게 통합. 기존 VLA의 'vision-only' 한계를 sensor-side에서 끊는 결로, contact-rich manipulation에 직접 영향.",
'2604.23360': "LfD에 failure awareness를 명시적으로 추가 — demonstration이 successful behavior에만 치우쳐 unsafe state coverage가 부족한 한계를 정조준. Safe robot navigation 라인의 데이터 측 보강.",
'2604.23570': "Real-world human task의 large-scale egocentric dataset EgoLive. Teleoperation/UMI 같은 기존 데이터 수집 방식의 한계를 우회 — 인간 일상 활동을 그대로 학습 신호로 끌어옵니다. VLA 데이터 인프라 라인의 새 자원.",
'2604.23609': "Visual + tactile reactive policy via tube diffusion — contact uncertainty와 external disturbance에 적응. Tactile feedback이 imitation learning에 흡수되는 흐름의 정량 사례.",
'2604.23620': "Manipulation을 'coarse relocation(move) + contact-critical interaction(operate)' 두 phase로 명시 분리한 VLA. 어제 LoHo-Manip 같은 phasing 결과의 연장선으로, behavior decomposition 라인이 굳어갑니다.",
'2604.23648': "Direction-aware convex free-region으로 unknown/cluttered 환경 navigation. Convex region 확장 시 'surrounding obstacle만 본다'는 한계를 direction prior로 보정하는 결로, mobile robot navigation 측 결.",
'2604.23702': "Humanoid가 ground reaction force를 인식하면서 조용히 걷는 physics-informed RL. 'Quiet walk'이 의외로 사용자 경험·하드웨어 마모 양쪽에 영향 — niche지만 deployment-aware 결입니다.",
'2604.23761': "Wheeled-legged 로봇의 high-dynamic reflexive 회피. Wheel 효율 + leg 적응성 결합 platform이 fast-moving obstacle을 reactive하게 피하는 라인의 결.",
'2604.24018': "Sim-to-real performance evaluation을 'betting' 프레임으로 — real-world 실험을 최소화하면서 알고리즘 비교/디자인 결정을 가능케 하는 통계 도구. Real eval 인프라 자체에 대한 결로 흥미로워요.",
'2604.24086': "Cloud-based VLA navigation의 network jitter/latency 문제를 plug-and-play edge adapter로 보정 — async inference로 latency hide. VLA deployment의 system-side 결.",
'2604.24182': "Layer Mixture-of-Experts로 VLA의 generalization 강화 + catastrophic forgetting 완화. End-to-end fine-tuning의 단점을 architectural 측에서 우회하는 결로, 어제 'VLA 분해+모듈화' 흐름의 직접 후속.",
'2604.24681': "Human video에서 'intention prior'를 hierarchical하게 추출 → VLA 학습 신호로 사용. 어제 GazeVLA(intent proxy)와 같은 라인의 또 다른 처방이라, 'human intent transfer' 라인이 한 주 단위로 분기점에 진입.",
'2604.23073': "VLA를 RL로 fine-tune하는 lightweight 방법 — VLA 자체를 reward model로 bootstrap하는 RL Token. Pre-trained VLA의 'out of the box' 능력을 RL post-training으로 정밀화하는 라인의 결.",
'2604.22852': "V2V semantic coordination — cloud LLM의 round-trip delay와 edge 단독의 occlusion 약점을 협력으로 우회. AD에서 V2X가 latency-constrained 환경에서 의미 있게 작동하는 결로, V2X 라인 결.",
'2604.22102': "Dynamic rope manipulation을 wiggle로 sysID 후 zero-shot 실행. 어제까지 '데이터 수집'에 매달려있던 흐름과 달리 '물리 prior로 모든 걸 푼다'는 정반대 접근이라 흥미로워요.",
'2604.22104': "비대칭 2-link 로봇이 platform 위에서 joint를 흔들면 undulatory locomotion이 발생한다는 dynamic coupling 분석. 학습보다 mechanism으로 푸는 고전 control 결.",
'2604.22235': "공장 production 환경에서 수 시간 단위로 굴러간 learning-augmented manipulation 보고서. Lab demo와 deployment 사이 갭을 정량화하는 reference 자료로, industrial 측 사람들에게 가치 있어요.",
'2604.22251': "Variable impedance MPC가 first-order actuator dynamics 하에서 'physically realizable 보다 큰 feasibility set'을 갖는 formulation error를 지적. Legged locomotion 제어 이론의 silent bug 명시화.",
'2604.22363': "가정 환경 deformable object manipulation 시뮬레이터 LeHome. Open-X-Embodiment가 한 일을 deformable 도메인에서 시뮬 인프라부터 다시 깔겠다는 포지셔닝.",
'2604.22526': "Calibration-free magnetic localization — information-theoretic geometry 최적화 + physics-aware learning. 의료 인터벤션용 occlusion-free guidance 응용으로 sim2real gap 정조준.",

# === Autonomous Driving ===
'2604.22824': "악천후 자율주행 segmentation을 dual teacher-student weight-sharing + class-aware semi-supervised로 풀기. 'AD perception은 청명한 day에서만 잘된다'는 고질병 정조준 결.",
'2604.22835': "End-to-end autonomous parking을 위한 structured simulation dataset ParkingScenes. Niche지만 parking은 production AV가 막상 막히는 자리라 응용 가치가 높아요.",
'2604.22856': "YOLOv8n에 Ghost Module + CBAM + Deformable Conv 조합으로 vehicle detection 강화. Incremental engineering 결이지만 ITS 측 응용에 즉시 들어갈 수 있어요.",
'2604.22872': "Resource-constrained AV에서 lane following + traffic sign 인식. Embedded platform deployment 결로, low-cost AV 라인 결.",
'2604.23018': "Web-scale 3D asset이 metric scale·pivot·forward axis가 제각각이라 deployment 안 된다는 진단으로 'spatially+semantically aligned' 10K dataset을 출시. Embodied AI 시뮬레이션 측 데이터 큐레이션 결입니다.",
'2604.23019': "UAV 이미지의 tropical tree species 분류 — close-up과 UAV 해상도 사이 representation gap을 정조준. Remote sensing 측 결이지만 'scale gap'이라는 일반 문제 자체가 흥미로워요.",
'2604.23247': "Avatar fingerprinting(누가 driving 하는지 검증)을 micro-expression-aware로 — frame 간 feature differencing이 핵심. Face reenactment 인증 라인 결로, deepfake defense 응용.",
'2604.23532': "Emotion-conditioned 짧은 호라이즌 human pose forecasting. 기존 trajectory 모델이 geometric cue에만 매달려 emotional signal을 무시한다는 진단에서 출발.",
'2604.23685': "Low-light scene text recognition. AV·smart surveillance 응용에서 'illumination이 망가지면 OCR이 망가진다'는 silent killer를 정조준한 결.",
'2604.23728': "Pedestrian intention prediction을 energy-based spatiotemporal interaction-aware로. 기존 모델이 단일 axis에만 매달리는 한계를 multi-modal 합성으로 우회.",
'2604.24044': "Camera-radar fusion에 contrastive learning + LiDAR-augmented pretraining. 'LiDAR가 너무 비싸다'와 'radar는 sparse하다' 사이의 cost-effective 자리를 노리는 결.",
'2604.24119': "Driving scene topology reasoning을 hierarchical centerline 표현으로 cyclic하게. MLP 기반 topology head의 한계를 끊는 결로, HD map 자동 생성 측에 영향.",
'2604.24353': "HSV 변환 camera 이미지를 attention-based rasterized encoding으로 HD map 위상 추정. HD map 라인의 cost-down 결로, AV deployment 측 가치.",
'2604.24419': "발전도상국 도시 CCTV의 BMD-45 vehicle detection 데이터셋. 기존 벤치가 highly organized highway 위주라는 한계를 정조준 — global ITS 측 데이터 인프라.",
'2604.24616': "도로변 인프라 + 차량 통신으로 road crack 검출. V2X가 'safety-critical 차원'을 넘어 'maintenance' 측에 적용되는 흐름의 결.",
'2604.22973': "Multi-agent trajectory prediction을 late fusion으로 — occlusion·sensing 한계 robustness 정조준. Trajectory forecasting 라인의 collaborative perception 결.",
'2604.23513': "고-conflict mixed-traffic에서 LLM-based interactive decision-making. 기존 AV가 overly conservative하다는 진단에서 출발해 LLM이 negotiation을 돕게 함. AV의 'social intelligence' 라인 결.",
'2604.23960': "Multi-robot motion planning을 SIMD 병렬화로 milliseconds 단위로 가속. VAMP 프레임워크 확장으로, 큰 swarm scenario에 직접 영향.",
'2604.24064': "Tractor-semitrailer 같은 articulated commercial vehicle용 MPCC trajectory planning. Passenger car에 잘 맞던 MPCC가 articulated 차량엔 안 맞는 한계 정조준.",
'2604.24242': "Mobility scooter 기반 ROS2 self-driving 연구 플랫폼 OpenPodcar2. Open-source AV 인프라로 학계 reproducibility에 기여.",
'2604.24295': "'Projected attainable speed space' 라는 instantaneous driving efficiency 메트릭 — 보수적 yielding을 정량 평가. AV deployment의 social acceptance 측 결.",
'2604.24384': "Pedestrian이 AV를 상대로 'chicken' 게임을 한다는 freezing-robot 문제 분석. Yield-always design choice의 사회적 부작용을 정량화하는 결.",
'2604.24606': "Trailer 시스템의 reverse parking을 hybrid A* 기반으로 — multi-body 시스템의 unintuitive control 문제 정조준.",
'2604.22815': "Classical vehicle dynamics의 흔한 misconception을 mechanical framework로 명시적으로 반박. AV 학계가 고전 control 가정을 무비판 차용하는 패턴에 대한 검증 자료.",
'2604.22068': "CARLA에서 실제 사고의 topology를 그대로 재구성해 AV evaluation에 사용. 기존 합성 conflict가 abstract만 잡던 한계를 끊는 결로, AV eval 인프라가 'real accident 모양'으로 옮겨가는 흐름.",

# === Foundation Models ===
'2604.22805': "AR 시스템의 privacy 위험을 semantic context-aware로 검출. 기존 framework가 visual content의 의미를 모르는 한계를 정조준 — AR/MR deployment의 audit-가능 측 결.",
'2604.22822': "VLM의 object hallucination을 perceptual error vs reasoning error로 분리해 attribute하는 DO-Bench. 기존 벤치는 aggregate accuracy만 보던 한계를 진단 축으로 분해. Hallucination 진단 인프라의 한 단계.",
'2604.22823': "Heterogeneous multimodal pretraining을 post-alignment model merging으로 — pivot-based 결합. 단일 model로 합치는 비용을 줄이는 라인 결입니다.",
'2604.22829': "VLM이 진동하는 dynamic gauge(아날로그 계기판)를 못 읽는다는 정직한 negative result. Industrial robotics 응용에서 VLM이 막상 production에 못 들어가는 자리를 정조준.",
'2604.22851': "VLM의 'ego-motion physics 이해'를 진단하는 EgoDyn-Bench. 자율주행 reasoning에서 'high-level 추론은 잘 하는데 underlying physics는 모른다'는 silent killer 측정.",
'2604.22855': "Remote sensing image captioning 평가에서 manual reference text 의존이 model을 'human annotation style 흉내'로 내모는 한계 정조준. Caption 평가 메트릭 자체에 대한 결입니다.",
'2604.22875': "VLM이 sketch/annotation으로 reasoning을 표현할 수 있게 — text-only 응답의 'verifiability 부재' 한계 우회. Modal output 확장이라는 흐름의 결.",
'2604.22884': "MLLM의 small object understanding 공백을 SOU 벤치로 정량화. 'MLLM이 큰 객체엔 강하지만 작은 객체엔 blank'라는 명백한 실패 모드를 측정.",
'2604.22989': "의료 multimodal foundation model을 unified generative pretraining으로 — CLIP-LLaVA 분리 학습이 만드는 projection 왜곡 정조준. CheXmix가 medical MLLM의 표준 처방 후보.",
'2604.23079': "Diabetic retinopathy grading을 CNN+Transformer로 풀고 explainable하게. 의료 영상 모델의 '왜 그렇게 판단했나' 측면을 명시화 — clinical adoption 측에 가치.",
'2604.23145': "VideoQA에서 implicit multi-step reasoning을 modular framework로 explicit하게 분해. 어제 SpaMEM/CodeGraphVLP의 long-horizon 진단/처방 흐름과 같은 라인.",
'2604.23195': "Analog circuit retrieval에 cross-modal representation. SPICE netlist·schematic·functional description 사이의 heterogeneous matching이 niche지만 명확한 산업 응용.",
'2604.23276': "PDF visual element parsing을 lightweight production-ready로. Multimodal RAG 인프라의 silent bottleneck 결.",
'2604.23282': "Text-based person anomaly search에 cascade pose-semantic gap 보정. Surveillance 측 결이지만 'pose-aware retrieval'의 일반 패턴 가치.",
'2604.23344': "Open-vocabulary object detection에서 hierarchical consistency + unbiased objectness. VLM이 'language prior로 hallucinate' 하는 OVD의 silent killer 정조준.",
'2604.23348': "Emotion transition을 multimodal로 이해/예측하는 EmoTrans 벤치. Social robot/HCI 측 결로 'static emotion만 보던 한계' 정조준.",
'2604.23407': "VLM이 푸쉬업을 못 센다는 PushupBench — frontier 모델조차 42% 정확도. 'recognize what'은 잘 해도 'count how many'에는 무력한 명백한 실패 모드를 정량 입증.",
'2604.23665': "CLIP을 hyperbolic geometry로 parameter-efficient하게 adapt. Hyperbolic representation 라인의 또 다른 사례, hierarchical 데이터 측 가치.",
'2604.23724': "Expressway 비디오에서 far-field anomaly detection을 zoom-in reason-out으로. VLM이 멀리 있는 작은 객체를 못 보는 한계를 활성 zoom으로 우회.",
'2604.23729': "OOD label set이 fixed면 미리 못 본 OOD에 망가진다는 한계를 dynamic prototype evolution으로 보정. OOD detection의 'closed-set assumption' 정조준.",
'2604.23788': "Multi-figure painting의 micro-interaction을 evidence-centric으로 탐색. VLM이 'figure 사이의 미세한 시선·gesture·spatial 관계'를 못 잡는 한계 정조준 — 예술 도메인이지만 social reasoning 일반 가치.",
'2604.23813': "Shredded document fragments에서 의미 복원 — 'pristine document만 평가'하던 VRDU 벤치 외연 확장. Document AI의 robustness 측 결.",
'2604.23860': "Egocentric video의 audio hallucination 측정 — sound가 visual occlusion 시 critical cue인데 audio-visual model이 hallucinate. Audio modality에서도 hallucination을 명시화.",
'2604.23909': "Video → audio assistive feedback을 motion-aware로 적응. 시각 장애인용 navigation aid 결로, cognitive overload 정조준.",
'2604.23935': "Audio-driven video object segmentation 챌린지 결. ASR-SaSaSa2VA 시스템 — niche 챌린지지만 audio-visual fusion 디자인 측 reference.",
'2604.23996': "MoE-VLM의 expert routing을 modality-guided soft하게. Hand-crafted/modality-agnostic routing의 한계 정조준 — efficiency 측 결.",
'2604.24029': "Species identification에 retrieval-augmented multimodal — 알려진 종 인식 + 알 수 없는 종 발견을 통합. Biodiversity 도메인의 'open-world recognition' 결.",
'2604.24036': "Crowded scene에서 occluded/small object grounding 강화. 어제 grounding 라인의 robustness 측 보강.",
'2604.24123': "Versatile video codec용 feature-distance-based generic quality metric. UHD/HDR 시대의 평가 측 결.",
'2604.24191': "Audio-visual deliberative reasoning을 deep nested deduction으로. 기존 sequential/parallel rollout의 한계를 nested 구조로 우회 — long-horizon reasoning 라인의 또 다른 결.",
'2604.24300': "VLM 3D 평가의 'modern setting에서 systematic invalidity'를 정조준 — point cloud 기반 QA가 VLM에 unfair하다는 진단. ReVSI는 spatial intelligence 평가 인프라 결.",
'2604.24339': "Low-level visual cue + visual feedback으로 VLM reasoning 강화. RL 기반 VLM의 'low-level 정보 부재' 한계 정조준.",
'2604.24346': "작은 open-weight VLM의 sycophancy(아첨) + hallucination 정량화. VLM-as-evaluator 라인의 신뢰성 silent killer 측정.",
'2604.24396': "Object hallucination을 positive-and-negative decoding으로 — training-free intervention. Adaptive grounding이 hallucination mitigation의 inference-time 표준이 될 수 있어요.",
'2604.24441': "GUI agent용 multi-modal functionality understanding 벤치 AutoGUI-v2. 'reactive matching → predictive mental model' 전환 측정으로, agentic AI 라인의 평가 인프라.",
'2604.24583': "Perception-centric process reward model로 VLM RLVR 강화 — outcome-level supervision의 'reasoning chain 진단 부재' 한계 정조준.",
'2604.24602': "Modality-specific corruption 하의 VLM TTA를 majorization-guided로. Entropy-based TTA가 unreliable modality에서 망가지는 silent killer 결.",
'2604.24696': "Neuroimaging agentic AI — sMRI/fMRI/dMRI/EEG 다 modal pipeline을 자동화. 의료 영상 워크플로우 자동화 측 결.",
'2604.24763': "Pixel embedding이 vision encoder를 이긴다는 unified MLLM Tuna-2. End-to-end pixel-from-scratch 학습이 understanding+generation 양쪽에서 SOTA를 노리는 결로, vision encoder 의존도가 흔들리는 신호.",
'2604.22774': "VLM이 학생 글씨를 'fix'하면서 over-correction 하는 패턴 진단. Educational AI 측 결로 'helpful AI가 학습을 망친다'는 dual-use risk 측정.",
'2604.23701': "농업 pest 진단을 training-free explainable framework로. 의료 영상 explainability 라인이 농업으로 이식되는 결.",

# === Generation ===
'2604.22828': "World-scale 3D generation MetaEarth3D — bounded 환경 한계를 넘어 spatially scalable. 기존 3D generation이 'object/room 규모'에 갇혀있던 한계 정조준, embodied AI 시뮬레이션·게임 인프라에 영향.",
'2604.22832': "Imaging phenomics + perturbation의 multiscale representation learning — drug discovery에서 transcriptomics 비용을 우회하는 결. Industrial pharmacology 응용.",
'2604.22836': "Sa2VA + agent 역할 분담의 Ref-VOS 챌린지 보고서. Agent loop가 segmentation hypothesis를 accept/revise/refine — 챌린지 결이지만 agentic 디자인 패턴 가치.",
'2604.22847': "Minecraft 환경의 voxel-resolution dataset Dream-Cubed + cube-based generative model. Embodied AI 시뮬 환경의 procedural generation 인프라.",
'2604.22850': "Few-shot diffusion으로 신제품 도입 시 visual inspection 가속. Industrial supervised 결인데 NPI 단계의 정확한 motivating이 healthy.",
'2604.22868': "Image editing model에서 visual planning을 정량 진단 — verbal-only 추론의 한계 측정. Editing 라인의 진단 측 결.",
'2604.22942': "3D Variable-Step DDPM으로 의료 modality translation 가속. Medical diffusion 효율 라인 결.",
'2604.22990': "Subtle visual anomaly(헤어라인 균열)의 active learning을 generative + symbolic으로. Industrial inspection 데이터 큐레이션 결.",
'2604.23010': "In-the-wild 데이터로 GenAssets — 3D asset latent-space generation. AV multi-sensor simulation 인프라로, 'asset 다양성 + realism 동시'를 노리는 결.",
'2604.23264': "Text-to-motion을 hierarchical flow matching으로. 어제 PoseFM과 같이 flow matching이 motion 도메인으로 확산하는 흐름.",
'2604.23325': "Talking head에 emotion-aware spatial refinement + temporal coherence. 기존 'simple emotion label' 한계 정조준 — production talking head 측 결.",
'2604.23481': "Spatial transcriptomics를 nuclei segmentation의 manual annotation 대안으로 사용. 의료 영상의 annotation cost 우회 결.",
'2604.23508': "Burst image super-resolution에 generative prior 추가. Mobile camera 측 응용에 직접 영향.",
'2604.23536': "Diffusion CFG에 zigzag trajectory를 zero-cost로 — 기존 CFG가 instantaneous gradient만 보고 manifold 곡률을 무시하는 한계 정조준. T2I 측 무료 점심.",
'2604.23540': "Initial Gaussian noise가 layout의 structural seed라는 직관 — semantic spherical alignment를 oracle로 빠르게. 어제 noise-as-prior 라인의 또 다른 사례.",
'2604.23574': "Image-to-video에 depth-aware physics layered animation. 기존 I2V의 '2D planar motion 한계' + physics 결합 라인.",
'2604.23584': "MRAG 시스템의 사람 얼굴 익명화를 identity-decoupled로. RAG의 privacy silent killer 결.",
'2604.23586': "Talking audio-video joint generation을 autoregressive diffusion으로. 'pervasive attention' 대신 high-level 의미와 low-level 디테일 분리 — joint AV generation 라인 결.",
'2604.23612': "PDE-based image despeckling 비교 연구 — niche이지만 PDE 측 측면 가치.",
'2604.23636': "Source-free TTA를 discriminator-guided adaptive diffusion으로. 'image corruption(blur·weather·digital artifact)' shift 정조준.",
'2604.23651': "In-bed pose estimation을 geometry-conditioned diffusion으로. Blanket occlusion 데이터 부족을 generative augmentation으로 우회 — 의료 측 응용.",
'2604.23688': "초상권 보호용 protective perturbation이 real-world image transformation에 망가지는지 검증 — 실제 production deployment의 silent failure 측정. Privacy attack 측 결.",
'2604.23709': "Single image dehazing의 zero-inference diffusion prior decoupling. CNN의 prior 한계와 diffusion 비용 사이 절충 결.",
'2604.23763': "Mask-free local editing에 region-aware adapter — DiT의 'global instruction은 잘 따르나 local edit이 leak'한다는 silent failure 정조준. Production 도구 후보.",
'2604.23789': "Multi-shot subject-to-video 챌린지 데이터셋 MuSS — 영화적 narrative logic + spatiotemporal coherence를 단일 시야로 측정. Cinematic AI 측 결.",
'2604.23814': "Extreme viewing angle license plate 인식의 recoverability mapping. ATM/CCTV opportunistic sensing 응용.",
'2604.23858': "Video latent의 inter-frame redundancy를 training-free pruning으로. Video diffusion 측 효율 결로 traditional codec 직관 + AI 결합.",
'2604.24136': "One-step diffusion으로 real-world super-resolution. Restoration vs generation manifold를 잇는 결로, perception-distortion trade-off 정조준.",
'2604.24146': "3D chest CT 분석을 explainable anomaly-aware foundation model로. 의료 volumetric AI의 'scan-level prediction 한계' 정조준.",
'2604.24193': "Container loss at sea를 CV로 조기 검출. 해운 industry 응용 결로, 'maritime AI'가 점점 늘어가는 신호.",
'2604.24407': "Banner relighting을 training-free illumination translation으로. Personalized ads 라인의 production 결.",
'2604.24459': "Layout-aware text rendering 데이터셋 TextGround4M. T2I의 'text rendering이 망가진다' 라인의 데이터 측 보강.",
'2604.24493': "Cross-attention guided identity-conditional diffusion으로 face swapping. Identity preservation 측 결, dual-use risk 동시.",
'2604.24575': "Diffusion 모델을 segmentation learner로 직접 사용 — denoising trajectory가 spatial prior를 encode. T2I diffusion이 perception backbone으로 활용되는 흐름의 표준 결.",
'2604.24625': "Image editing CoT의 granularity/generalization을 meta-CoT로 향상. Unified understanding/generation 결의 fine-tuning 측 결.",
'2604.24719': "Source-free + few-shot medical segmentation에 diffusion-based prompt-free SAM2. SAM의 'natural-image bias' 한계 정조준.",
'2604.24764': "Text-to-video generation에 3D constraint를 RL로 강화한 World-R1. Video gen의 geometric inconsistency를 architecture 변경 없이 RL post-training으로 해결.",
'2604.22894': "Pediatric PET의 CT-free attenuation correction. 의료 영상의 radiation dose 절감 측 결로, generalization 정조준.",
'2604.22905': "Whole-body PET registration의 voxel-wise spatially-varying regularization. 의료 영상 measurement 측 결.",
'2604.23016': "AI image의 digitally signed content-encoding watermark. 'AI image trust' 라인의 cryptographic 측 결로 watermark 라인의 또 다른 진영.",
'2604.23380': "Online RL이 denoising generative model에 'easier than you think' — V-GRPO. Denoising RL의 intractable likelihood 문제를 우회. Diffusion alignment 측의 surprising 결.",
'2604.24047': "Maximum mean discrepancy를 kernelised functional Bregman으로 일반화. 통계 ML 측 이론 결로 ROI 주변부.",
'2604.24351': "Controllable diffusion을 unified plugin framework로 — backbone-specific isolation을 끊어요. Production 측 가치.",
'2604.24487': "Score-based diffusion으로 robotic path following의 guiding vector field 생성. Diffusion이 control 라인에 흡수되는 흐름.",

# === Efficiency/Systems ===
'2604.22808': "Long video diffusion transformer의 quadratic self-attention을 frequency-domain attention + adaptive spectral routing으로 우회. Video gen의 long-sequence 효율 측 핵심 결.",
'2604.22825': "3D SAM을 lesion segmentation으로 transfer할 때 self-gated prompting. 의료 측 SAM 응용 결.",
'2604.22834': "Browser 기반 microcontroller TinyML 비전 학습. \\$15-40 USD 기기에서 end-to-end 학습/배포 — 교육·embedded 라인 결.",
'2604.22839': "Skeleton-based PES + few-shot — 체육 분야 fine-grained event spotting 측 결.",
'2604.22846': "Pathology foundation model의 fragmented tile-level representation을 unified slide-level로 통합. 의료 측 다중 foundation model 결합 결.",
'2604.22857': "Additive manufacturing surface crack을 IoT-enhanced CNN으로. Industrial 측 incremental.",
'2604.22885': "Federated cross-modal retrieval에 missing modality + non-IID 동시 처리. FL+CMR의 silent challenge 정조준.",
'2604.23094': "Portrait relighting에 hybrid domain knowledge fusion — synthetic + OLAT + real을 결합. Production 측 도메인 갭 결.",
'2604.23268': "Hexadeca-Bayer sensor용 multi-frame super-resolution. CIS 도메인 특화 efficient 결.",
'2604.23271': "WBC 분류의 hierarchical ensemble — domain shift robustness 정조준. Clinical deployment 측 결.",
'2604.23314': "SAM의 noisy prompt에 saliency-guided distillation. Medical SAM 측 'prompt가 부정확하면 망가진다'는 silent killer 결.",
'2604.23320': "Kolmogorov-Arnold convolutional network. KAN이 classification에 응용되는 라인의 결로 — 'CNN 다음 후보'에 대한 또 한 신호. 결과는 ablation 봐야 판단.",
'2604.23375': "Medical image의 hierarchical spatio-channel clustering으로 model compression. CNN 압축 라인의 의료 측 보강.",
'2604.23415': "RGB와 optical flow에 다른 backbone을 쓰는 heterogeneous two-stream. 'same backbone for both'라는 통념 정조준.",
'2604.23426': "Non-IID FL의 privacy + communication efficiency를 adaptive 양쪽으로. FL 시스템 측 결.",
'2604.23442': "UAV-based weed detection을 edge device deployment 정조준. Agricultural AI deployment 측 결.",
'2604.23632': "Real-time joint AV avatar generation에 asynchronous dual-stream. Talking head streaming 측 결로 latency 정조준.",
'2604.23899': "Mammographic lesion segmentation을 lightweight model로. 의료 측 incremental.",
'2604.23941': "GUI element grounding을 lightweight하게 — mobile phone deployment 정조준. Agentic AI on-device 측 결.",
'2604.23950': "VLM의 attention-based token pruning을 rethink — naive pruning이 reasoning을 망가뜨린다는 진단. LearnPruner는 pruning이 'attention만 보면 안 된다'는 silent finding을 정조준.",
'2604.24149': "Remote sensing image dehazing을 unified로. 'sequential pipeline 한계' 정조준.",
'2604.24167': "Implicit neural representation의 high-dimensional projection을 PEPS로 효율화. INR 측 코어 결.",
'2604.22939': "LLM의 self knowledge re-expression — fully local task adaptation. NTP의 sequential 한계를 intrinsic knowledge로 우회.",
'2604.23012': "Thumb-sized microcontroller에서 vision training + deployment + inference 전부. 가격 \\$15-40 USD — TinyML extreme 결.",
'2604.23166': "Satellite foundation model로 wealth monitoring. Social policy 응용으로 'survey 비용 우회' 결.",
'2604.23372': "Sparse fluid observation을 physics-informed temporal U-Net으로 보간. Scientific computing 측 결.",
'2604.23798': "Linear-scan attention ELSA — exact softmax 보존 + memory light. ViT 측 attention 효율 결.",
'2604.24000': "Wavelet neural network로 Poisson image reconstruction. Image inverse problem 측 결.",
'2604.24393': "Self-supervised ReLU network의 piecewise-linear region complexity 분석. 이론 측 결.",
'2604.23074': "UAV multirotor가 tilting platform에 toggleable adhesion으로 착륙. Maritime UAV 라인 결.",
'2604.23327': "Mobile robotics active perception의 efficient beam search. 정보획득 + 이동 비용 동시 최적화 결.",
'2604.23693': "Heterogeneous multi-robot collaborative exploration을 decentralized로. 멀티 로봇 협력 측 결.",
'2604.24447': "VLA를 다양한 XPU(GPU/NPU/edge) 환경에서 characterize. 'desktop GPU evaluation의 한계' 정조준 — VLA deployment의 hardware reality 정량화. 우리 deployment 라인이라면 reference.",
'2604.24661': "Visual RL의 dynamic perturbation robustness를 agent-centric으로. RL 측 robustness 결.",
'2604.23402': "Robotic touch design에 'otherness' 라는 새 quality 제안. HRI 사회적 측면의 디자인 철학 결.",

# === Embodied AI ===
'2604.23432': "Spherical camera의 pose variation 하 depth estimation 벤치 Sphere-Depth. Robotic navigation 측 360° 측 결.",
'2604.24235': "Vision-based hand tracking으로 surgical 환경 touchless image interaction. Sterility + workflow continuity 측 응용 결.",
'2604.23970': "Floor plan image → structured retrievable knowledge로 LLM agent를 통해 변환. BLV(시각장애인) navigation 측 결로, 'per-building 인프라 비용' 우회.",
'2604.22896': "Magnetic indoor localization을 CNN regression + rotation invariance로. GNSS-denied 환경 측 결.",
'2604.23580': "3D scene physics-aware symbolic simulation 벤치 PhysCodeBench. LLM이 physics 묘사를 executable simulation으로 변환하는 능력 측정 — embodied AI 측 데이터 인프라.",
'2604.24391': "VLN 모델의 token caching을 frequency-guided adaptive로. VLN의 'high computational overhead' 정조준 — embodied agent의 deployment 측 결.",

# === Safety/Alignment ===
'2604.22837': "Long occlusion·fast motion·viewpoint change 하의 SAM-tracker fragility를 dense memory + selective update로 보강. PVUW MOSE 챌린지 결로 video tracking robustness 측 결.",
'2604.22841': "Face image quality assessment에 attention-based interpretable 모델. 'multiple forward pass + backprop' 비용 우회 — face recognition 측 결.",
'2604.22853': "Fast Adversarial Training의 'fair comparison 부재' 정조준 벤치 FastAT. Adversarial robustness 라인 인프라 결.",
'2604.22899': "RGB+3D 산업 anomaly detection의 ambiguous cross-modal alignment 보정. Industrial QC 측 결.",
'2604.23105': "AD object detection에 transferable physical-world adversarial patch. AV safety 측 위협 정량화 — 어제 TriPatch와 같은 라인의 또 다른 결. Risk 섹션 참고.",
'2604.23125': "Long-tailed + high-noise label에서 robust visual recognition. 'imperfect text guidance' 활용으로 noise-image mismatch 정조준.",
'2604.23274': "Semi-supervised medical image segmentation에 generative dual-distribution alignment. Annotation 비용 우회.",
'2604.23335': "Knee osteoarthritis grading을 hierarchical semi+self-supervised fusion으로. 의료 측 annotation 부족 결.",
'2604.23452': "ViT가 'classification만 학습'했어도 spatial structure를 어떻게 encode하는지 layerwise probing. Transfer learning 이론 결로, 'spatial supervision 없이도 spatial 정보를 얻는다'는 흥미로운 진단.",
'2604.23655': "Low-light + underwater video enhancement에 visual state-space model. SSM의 vision 응용 측 결.",
'2604.23662': "Solar PV 결함 분류 데이터셋 SolarFCD. Energy 측 응용 데이터 인프라.",
'2604.23670': "DINO를 many-to-many association으로 zero-shot deployment. DINO feature의 generalization 한계 정조준.",
'2604.23706': "Ulcerative colitis Nancy index의 weakly supervised 채점 — foundation model이 의료 grading을 자동화하는 사례.",
'2604.23718': "Caries DETR + tooth structure prior + lesion-aware loss. Dental imaging 측 결.",
'2604.23839': "Fetal ultrasound nuchal translucency 측정의 ROI-aware refinement. 'global metric이 clinical fidelity의 unreliable proxy'라는 진단이 healthy.",
'2604.23875': "Medical image classification의 label noise를 risk-aware로. Clinical risk 정조준 결.",
'2604.23957': "Layered audio-visual anti-tampering watermarking. Deepfake 검출 + localization 측 결.",
'2604.23977': "Low-resource biomedical classification을 multi-view synergistic + VL로. 의료 도메인 데이터 부족 결.",
'2604.23982': "Histopathology multimodal MIL의 hierarchical prototype-based domain prior. 디지털 병리 측 결.",
'2604.24023': "Real-world commercial design 프로젝트 평가 벤치 ServImage. Image gen이 academic vs paid production 갭 측정.",
'2604.24024': "Multi-projector calibration을 embedded camera로 — sequential pattern projection의 scalability 한계 정조준.",
'2604.24109': "Medical image segmentation의 annotation efficiency를 SemiSAM-O1으로 push. Foundation model + SSL 결합 결.",
'2604.24125': "Object-level + scene-level label 통합 open-vocabulary segmentation. RS 측 결.",
'2604.24163': "NTIRE 2026 deepfake detection robustness 챌린지 보고서. Image degradation 하의 deepfake 검출 측 인프라.",
'2604.24171': "Visual text generation의 text-accuracy vs aesthetic trade-off를 Pareto-optimal curriculum alignment로. T2I rendering 측 결.",
'2604.24230': "Skull-base meningioma의 volumetric response 예측을 radiomics+clinical로. Stereotactic radiosurgery 측 결.",
'2604.24234': "Laser powder bed fusion in-situ inspection의 graph-augmented segmentation. Additive manufacturing 측 결.",
'2604.24328': "Monocular depth에 algebraic group + ring 구조를 학습 가능 파라미터로. 'Euclidean grid generic regression' 한계 정조준.",
'2604.24331': "Affordable wearable stereo eye-tracking 플랫폼. HCI 측 인프라 결.",
'2604.24492': "Spaceborne edge AI용 deployment-aligned low-precision NAS. Edge accelerator 측 결로 hardware-aware design.",
'2604.24524': "SPECT MPI + CTA registration을 point cloud로. 의료 multimodal fusion 결.",
'2604.24543': "RGB-T crowd counting에 reliability-aware crowd anchor. Cross-modal feature fusion 측 robustness 결.",
'2604.24642': "CLIP의 360° panoramic 이해 정량 — 'pretrain은 perspective image, 평가는 360° generation'이라는 evaluator 갭 정조준.",
'2604.22904': "Hepatobiliary phase liver MRI 합성 — prolonged post-contrast delay 우회. 의료 측 결.",
'2604.24236': "Biofouling 환경의 dissolved oxygen 측정에 deep learning. 해양 모니터링 측 응용.",
'2604.23179': "Multi-agent informative sensing으로 dynamic indoor 모니터링. Mobile robot team coordination 측 결.",
'2604.23696': "Wrist-mounted F/T sensor의 non-contact force compensation. Haptic-enabled robotic surgery 측 deployment 결.",
'2604.23775': "VLA safety의 threats·challenges·evaluations·mechanisms를 unified survey로. RedVLA 같은 개별 시도들이 systematic mapping을 받는 시점 — 우리 manipulation 스택의 safety roadmap 작성에 reference. 오늘자 must-read에서 자세히.",
'2604.23863': "Safety value-constrained MPC로 performance + safety co-optimization. State/input constraint 하의 MPC 측 결.",
'2604.24188': "임의 material pair의 friction coefficient를 proxy interaction으로 일반화. Robotics + digital fabrication 측 결로 'pairwise testing의 quadratic 비용' 정조준.",
'2604.24518': "Sliding mode control로 moving obstacle avoidance + trajectory tracking. Mobile robot control 측 결.",
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
    parts.append('<div><strong>시야:</strong> 주간 2026-04-22 ~ 2026-04-28 · 오늘 배치 cs.CV/new + cs.RO/new</div>')
    parts.append('<div><strong>소스:</strong> arxiv.org /list/cs.CV/new · /list/cs.RO/new (stdlib 파서 경유)</div>')
    parts.append('<div><strong>주간 규모:</strong> cs.CV ~640편 · cs.RO ~204편 (union ~844편)</div>')
    parts.append('<div><strong>오늘 /new:</strong> cs.CV 366 + cs.RO 97 (cross 포함) → 295 unique → 238편 8개 ROI 버킷 선정</div>')
    parts.append('<div><strong>델타 기준:</strong> 5일 전 스냅샷(2026-04-23)과 비교 (7일 전 스냅샷 부재로 가장 가까운 과거 사용)</div>')
    parts.append('</div>')

    # 주간 동향
    parts.append('<h2>🔭 주간 동향</h2>')
    parts.append('<p>이번주 pastweek 누적의 가장 큰 신호는 <strong>Autonomous Driving</strong>이 13편 → 32편으로 <span class="hot">+146%</span> 폭증했다는 점이에요. 어제까지 \'AD가 perception 단독 결을 줄이고 큰 모델 안으로 흡수된다\'고 보던 흐름이 이번주 다시 반전 — V2X coordination(SwarmDrive), 4D occupancy directing(OccDirector, 어제 결), end-to-end parking(ParkingScenes), pedestrian intention prediction(ESIA), trajectory planning + LLM negotiation 같은 결들이 동시에 쌓이면서 AD가 \'단순 perception\'에서 \'social-aware decision\'으로 무게중심이 옮겨가는 모양새입니다. 한편 <strong>Efficiency/Systems</strong>가 28→40편(<span class="hot">+43%</span>), <strong>Safety/Alignment</strong>가 31→39편(<span class="hot">+26%</span>) 늘어난 것도 \'production-deployment\' 라인이 함께 굵어진다는 신호로 봅니다. 반대로 <strong>Foundation Models</strong>가 112→52편(<span class="cold">-54%</span>), <strong>Embodied AI</strong>가 30→15편(<span class="cold">-50%</span>) 빠진 건 어제 폭증한 후의 자연스러운 호흡 같아요 — 다만 두 버킷이 동시에 절반으로 빠진 건 우연이 아니라, 어제 한 날에 몰렸던 신규 결들이 한꺼번에 빠지는 패턴이라 평균 회귀로 보는 게 맞아 보입니다.</p>')
    parts.append('<p>오늘 /new에서 제일 눈에 띄는 건 <strong>VLA 라인이 \'문제 정의\' 단계에 진입했다는 신호 셋</strong>이에요. 어제 \'memory·intent·safety\' 세 축 동시 점화를 짚었는데, 오늘은 <a href="https://arxiv.org/abs/2604.23121">Lock-in</a>(low-data post-training 후 instruction-following이 멈춘다는 새 failure mode), <a href="https://arxiv.org/abs/2604.23001">VLA Data Survey</a>(architecture가 아니라 data infrastructure가 진짜 bottleneck이라는 강한 클레임), <a href="https://arxiv.org/abs/2604.23775">VLA Safety Survey</a>(threats·evaluations·mechanisms 통합 매핑)가 같은 날 등장했습니다. 어제는 \'각자 다른 axis에 처방\'이었다면 오늘은 \'communities-wide 진단/매핑\' 단계 — VLA 분야가 한 분기 안에 sub-disciplines가 분기점에 들어가는 패턴이 명확해요. 솔직히 이건 한동안 갈 것 같습니다.</p>')
    parts.append('<p>부상 중인 미니 토픽 두 개. 첫째, <strong>Diffusion이 perception backbone으로 본격 흡수</strong>되는 흐름 — <a href="https://arxiv.org/abs/2604.24575">Diffusion as Generalist Segmentation Learner</a>가 denoising trajectory를 segmentation prior로 직접 사용하고, <a href="https://arxiv.org/abs/2604.23380">V-GRPO</a>가 \'denoising RL은 생각보다 쉽다\'는 surprising 결을 내놨습니다. Generation 인프라가 perception/RL post-training 양쪽에 동시에 흘러드는 패턴이에요. 둘째, <strong>VLM이 못 푸는 작은 실패 모드 정량화</strong>가 catalogue 단계 — <a href="https://arxiv.org/abs/2604.23407">PushupBench</a>(VLM이 푸쉬업 카운트를 못 함, frontier 42%), <a href="https://arxiv.org/abs/2604.22829">Dynamic Gauges</a>(진동하는 계기판을 못 읽음), <a href="https://arxiv.org/abs/2604.22884">Small Object Understanding</a>(SOU 자체가 blank), <a href="https://arxiv.org/abs/2604.24300">ReVSI</a>(VLM 3D 평가 자체가 systematically invalid)가 한 날에 나란히 등장. \'어디서 깨지는가\'를 명시화하는 단계라, hallucination/POPE가 한 일을 다른 axis에서 반복하는 패턴이 보입니다.</p>')

    # CV vs RO
    parts.append('<h2>📐 CV vs RO 대비</h2>')
    parts.append('<p>오늘 분포는 Generation(44)·Foundation Models(41)·Safety(41)·Efficiency(35)·AD(25)·3D/Scene(24)·Robot Learning(22)·Embodied AI(6)으로, <em>CV 중심 버킷이 상위 4개를 모두 차지</em>합니다. Foundation Models는 RO 0/CV 40으로 여전히 \'VLM 신규는 CV 영역\' 패턴이 일관되고, Robot Learning은 RO 18/CV 2/CV-RO 2로 거의 RO 전용. 어제 3D/Scene이 1위였는데 오늘은 Generation/FM이 뒤쪽에서 다시 올라오면서 매일 1위 버킷이 바뀌는 \'rolling rotation\' 패턴이 보여요. AD는 25편으로 4위에 안착하면서 이번주 누적 +146% 라는 거시 흐름과 일관됩니다.</p>')
    parts.append('<div class="contrast">')
    parts.append('<p><strong>① 공통으로 뜨는 키워드</strong></p>')
    parts.append('<ul>')
    parts.append('<li><code>VLA</code> — CV(CF-VLA, M²-VLA Layer-MoE), RO(VLA Survey, Lock-in, Modular Sensor, AsyncShield, RL Token, MoT-HRA, VLA Safety) — 한 날 9편 이상이 동시 등장, VLA가 한 주 단위 dominant 토픽임을 재확인</li>')
    parts.append('<li><code>diffusion as backbone</code> — CV(Generalist Segmentation Learner, Adaptive TTA, Geometry-conditioned in-bed, V-GRPO RL), RO(Score Vector Field) — diffusion이 generation 외 perception/control 라인에 흡수</li>')
    parts.append('<li><code>foundation model 측정</code> — CV(DO-Bench, EgoDyn-Bench, PushupBench, ReVSI, Audio Hallucination), RO(VLA Survey, VLA Safety) — 양쪽 모두 \'어디서 깨지나\' 진단 단계</li>')
    parts.append('</ul>')
    parts.append('<p><strong>② CV에만 뜨는 키워드</strong></p>')
    parts.append('<ul>')
    parts.append('<li><code>3DGS / NeRF</code> — Spatiotemporal Degradation 3DGS, Light\'em Up few-shot low-light 3DGS, GS-DOT(의료), Multivariate Gaussian NeRF — RO쪽에 SLAM 한정 결만, CV 본연 라인 일관 유지</li>')
    parts.append('<li><code>token pruning / efficient attention</code> — FreqFormer, ELSA exact linear-scan, LearnPruner — VLM/Video diffusion 효율 라인 모두 CV 표지</li>')
    parts.append('<li><code>medical imaging</code> — 오늘 Safety/Alignment 41편 중 절반 이상이 의료 — CV 모델 deployment의 가장 큰 industry segment가 의료라는 사실이 분포로 드러남</li>')
    parts.append('</ul>')
    parts.append('<p><strong>③ RO에만 뜨는 키워드</strong></p>')
    parts.append('<ul>')
    parts.append('<li><code>humanoid / legged</code> — RecoverFormer(humanoid recovery), QuietWalk(GRF-aware), Wheeled-legged reflexive evasion, False Feasibility VI-MPC — locomotion control RO 전용 축</li>')
    parts.append('<li><code>safety control / CBF / MPC</code> — Hierarchical QP CBF, Safety Value MPC, Sliding Mode Control, ATRS — 고전 control + 학습 결합 RO 고유 결</li>')
    parts.append('<li><code>VLA inference deployment</code> — XPU characterization, AsyncShield edge adapter, FreqCache VLN — VLA가 \'학습 cost\' 다음 \'inference cost\' 단계로 진입한 신호</li>')
    parts.append('</ul>')
    parts.append('<p><strong>④ 같은 단어 다른 맥락</strong></p>')
    parts.append('<ul>')
    parts.append('<li><code>data infrastructure</code>: CV(MetaEarth3D world-scale, Dream-Cubed Minecraft voxel, AmaraSpatial-10K) / RO(VLA Survey, EgoLive, LeHome deformable) — CV는 \'생성용\' RO는 \'학습용\' 데이터 — 같은 단어가 정반대 용도</li>')
    parts.append('<li><code>safety</code>: CV(TriPatch AD detection 패치, Risk-Aware label noise, FastAT bench) / RO(VLA Safety Survey, Hierarchical QP CBF, Safety MPC) — \'시각 모델 robustness\' vs \'physical actuation 보장\'</li>')
    parts.append('<li><code>memory / context</code>: CV(Audio Hallucination, EgoDyn-Bench ego-motion grounding) / RO(Lock-in low-data fine-tuning) — CV는 \'평가\'·RO는 \'failure mode 명명\'</li>')
    parts.append('</ul>')
    parts.append('</div>')
    parts.append('<p>오늘의 CV/RO 교집합은 \'<em>VLM/VLA가 어디서 깨지는가\'를 systematic mapping</em>하는 단계입니다. CV쪽 PushupBench·DO-Bench·ReVSI가 vision 모델의 누락된 능력을 명시화하고, RO쪽 Lock-in·VLA Safety Survey가 VLA 모델의 미래 failure mode를 통합 매핑해요. 어제까지 \'각 axis에 처방\'이었다면 오늘은 \'전체 분야가 무엇이 무너질 수 있는지\'를 동시에 정리하는 단계 — community가 maturity를 한 단계 올리는 신호로 봅니다.</p>')

    # 인사이트
    parts.append('<h2>💡 오늘의 인사이트</h2>')
    parts.append('<div class="insight"><h3>VLA 분야가 \'failure mode catalog\' 단계로 진입 — Lock-in·Safety Survey·Data Survey가 한 날 동시 등장</h3><p>어제까지 \'memory·intent·safety\'에 각자 처방이 나왔다면, 오늘은 <a href="https://arxiv.org/abs/2604.23121">Lock-in</a>이 \'low-data post-training 후 instruction-following이 멈추는\' 새 failure mode를 명명하고, <a href="https://arxiv.org/abs/2604.23775">VLA Safety</a>가 threats·challenges·evaluations·mechanisms를 통합 매핑하며, <a href="https://arxiv.org/abs/2604.23001">VLA Data Survey</a>가 \'architecture 진보가 아니라 data infrastructure가 진짜 bottleneck\'이라는 강한 클레임을 내놨습니다. 한 날에 셋이 동시에 등장하는 건 우연이 아니라, VLA community가 \'개별 시도들의 catalog\' 단계에 진입했다는 신호. 우리 manipulation 스택을 짤 때도 \'어디에 들어갈지\'에서 \'어떤 failure mode를 회피할지\'로 사고 프레임이 옮겨가야 할 시점입니다.</p></div>')
    parts.append('<div class="insight"><h3>Diffusion이 generation을 떠나 perception/control backbone으로 흡수되는 흐름이 본격화</h3><p>오늘 <a href="https://arxiv.org/abs/2604.24575">Diffusion as Generalist Segmentation Learner</a>가 denoising trajectory의 spatial prior를 segmentation에 직접 사용하고, <a href="https://arxiv.org/abs/2604.23380">V-GRPO</a>는 \'denoising generative model의 online RL이 생각보다 쉽다\'는 surprising 결을 내놓고, <a href="https://arxiv.org/abs/2604.24487">Score-Induced Guiding Vector Field</a>가 robotic path following에 score-based diffusion을 사용합니다. 어제 dWorldEval(diffusion → policy 평가), OccDirector(diffusion → AD scenario directing) 라인의 직접 후속이고, \'diffusion = generation\' 1차 정의가 빠르게 무너지고 있어요. 다음 4~6주 동안 generative와 discriminative의 경계 자체가 재정의될 가능성이 큽니다.</p></div>')
    parts.append('<div class="insight"><h3>VLM의 \'못 하는 것\' 카탈로그 정량화 — POPE 패턴이 새 axis로 반복 재현</h3><p><a href="https://arxiv.org/abs/2604.23407">PushupBench</a>(counting 42%), <a href="https://arxiv.org/abs/2604.22829">Dynamic Gauges</a>(진동 계기판 읽기 실패), <a href="https://arxiv.org/abs/2604.22884">Small Object Understanding</a>(blank), <a href="https://arxiv.org/abs/2604.24300">ReVSI</a>(VLM 3D 평가 자체가 invalid), <a href="https://arxiv.org/abs/2604.24346">SycoPhantasy</a>(VLM evaluator의 sycophancy)가 같은 날 동시 등장. POPE가 hallucination에 한 일을 \'counting\'·\'temporal vibration\'·\'small object\'·\'spatial reasoning\'·\'evaluator bias\' 다섯 axis에서 동시에 반복하는 패턴이에요. 다음 단계는 이걸 통합 \'VLM Failure Atlas\'로 묶는 paper일 가능성이 높고, 우리가 그 자리를 선점할 수 있는 좋은 기회입니다.</p></div>')

    # 추천 연구주제
    parts.append('<h2>🔬 추천 연구주제</h2>')
    parts.append('<div class="topic"><h3>VLM Failure Atlas — VLM의 시계열 failure mode를 단일 벤치로 통합</h3><p>오늘 PushupBench·Dynamic Gauges·SOU·ReVSI·SycoPhantasy가 흩어진 axis에 각자 벤치를 출시했는데, 통합 프레임이 비어 있어요. \'counting·temporal vibration·small object·spatial reasoning·evaluator bias\' 5축으로 표준 진단 task를 묶어 reproducible eval suite를 만들면, POPE가 hallucination에 한 일을 더 큰 scope에서 반복할 수 있습니다. 우리 랩이 VLM evaluation 인프라를 갖췄다면 빠르게 출판 가능한 자리고, 4~6주 안에 \'first-mover\' 위치를 잡을 수 있어요.</p></div>')
    parts.append('<div class="topic"><h3>VLA Lock-in 정량화 + 회복 메커니즘 — low-data post-training의 silent killer 정조준</h3><p>오늘 Lock-in 페이퍼가 \'low-data post-training 후 instruction-following이 멈추는\' 현상을 처음 명명했지만, 정량 다이얼(데이터 양 vs lock-in 강도, instruction diversity 영향, 회복 가능성 측정)이 비어 있어요. 우리 랩이 VLA fine-tuning 데이터를 갖고 있다면 \'lock-in scaling law\' + \'recovery mechanism (replay·diverse instruction warmup·KL anchor)\' 비교를 빠르게 measure할 수 있습니다. VLA practitioner라면 실용적으로 가장 즉각적 가치 있는 자리.</p></div>')
    parts.append('<div class="topic"><h3>Diffusion Backbone Audit — generation/perception/control 통합 학습이 실제로 효율적인가</h3><p>오늘 Diffusion-as-Segmentation, V-GRPO, Score Vector Field 같이 diffusion이 perception/control로 흡수되는 사례가 동시 등장했지만, \'단일 diffusion backbone이 multiple downstream task를 동시 수행\'하는 multi-task transfer benchmark는 아직 없어요. Generation backbone을 perception/control로 transfer할 때 효율 vs accuracy trade-off를 systematic하게 측정하는 결이 비어 있어, generative AI 인프라를 운영하는 랩이라면 빠르게 출판할 수 있는 자리입니다. 4~6주 안에 community standard로 굳을 가능성이 큰 첫 결이 나올 만한 자리.</p></div>')

    # 회고 — 자료 부족 안내 (오늘은 화요일이라 회고 섹션 자체 생략)
    # 월요일이 아니므로 retro 섹션은 skip

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
    parts.append(f'<p>🔥 <span class="hot">TOP3</span>: {top3[0][0]} ({top3[0][1]}), {top3[1][0]} ({top3[1][1]}), {top3[2][0]} ({top3[2][1]}) · ❄️ <span class="cold">BOTTOM2</span>: {bot2[0][0]} ({bot2[0][1]}), {bot2[1][0]} ({bot2[1][1]}). 어제 3D/Scene이 1위였는데 오늘은 Generation·FM·Safety가 동시 41~44편으로 상위 3개를 모두 차지하면서 \'CV 전 분야 광폭 분포\'로 회복. 어제 폭증했던 3D/Scene이 24편으로 안정화된 게 자연스러운 호흡으로 보이고, Robot Learning이 22편으로 안정 유지된 것도 VLA 라인이 한 주 내내 가속해온 결과예요.</p>')

    # 델타 (vs 2026-04-23, 5일 전)
    parts.append('<p>📈 <strong>주간 델타(2026-04-23 → 2026-04-28, 5일 시야)</strong>: 🚗 Autonomous Driving <span class="hot">+146%</span> (13→32), ⚡ Efficiency <span class="hot">+43%</span> (28→40), 🛡️ Safety/Alignment <span class="hot">+26%</span> (31→39), 📦 3D/Scene <span class="hot">+20%</span> (40→48), 🤖 Robot Learning <span class="hot">+10%</span> (58→64), 🎨 Generation <span class="cold">-9%</span> (79→72), 🏃 Embodied AI <span class="cold">-50%</span> (30→15), 🧠 Foundation Models <span class="cold">-54%</span> (112→52). AD 폭증(+146%)이 가장 큰 매크로 신호 — 4D occupancy directing, V2X coordination, end-to-end parking, social-aware decision까지 한 주 동안 다층 결들이 쌓이면서 \'AD = perception 단독\'에서 \'AD = decision-making\'으로 분야 정의 자체가 옮겨가는 인상이에요. FM·Embodied AI 동시 -50%대 빠짐은 어제 한 날 폭증의 mean-reversion으로 보입니다.</p>')

    # 벤치마크 SOTA 추이
    parts.append('<h2>📈 벤치마크 SOTA 추이</h2>')
    parts.append('<p>이번주 추적 벤치마크(ScanNet++·LIBERO·nuScenes·MMMU·VBench 등) 신규 SOTA 업데이트는 표 단위 새로 잡힌 게 없습니다. 오늘 결 중 <a href="https://arxiv.org/abs/2604.23001">VLA Survey</a>가 LIBERO/CALVIN/RLBench 누적 분석 자료를 제공하긴 하나 새 SOTA 보고는 아니고, <a href="https://arxiv.org/abs/2604.24300">ReVSI</a>는 VLM 3D 평가 표준 자체를 흔드는 결이라 추적 리스트의 \'기존 점수\' 의미를 재정의할 가능성이 있습니다. 다음주 LIBERO/MMMU 측 결과 누적되면 표 갱신할게요.</p>')

    # 크로스오버 페어
    parts.append('<h2>🔀 크로스오버 페어</h2>')
    parts.append('<div class="crosspair"><h3>VLM/VLA의 \'못 하는 것\'을 정량화 — Counting(CV) vs Lock-in(RO)</h3><p><a href="https://arxiv.org/abs/2604.23407">PushupBench</a>(CV)는 frontier VLM이 푸쉬업을 42%만 카운트한다는 명백한 실패 모드를 정량화합니다. 같은 날 <a href="https://arxiv.org/abs/2604.23121">Lock-in</a>(RO)은 low-data post-training 후 VLA가 새 instruction에 반응을 멈추는 \'lock-in\' 현상을 처음 명명. 양쪽 모두 \'프론티어 모델이 사람 눈에는 너무나 당연해 보이는 일에서 망가진다\'를 정조준한 결인데, CV쪽은 \'evaluation 측\' RO쪽은 \'training dynamics 측\'에서 접근. 두 편 같이 읽으면 \'foundation model이 어디서 깨지나\'의 진단 그림이 한층 선명해집니다.</p></div>')
    parts.append('<div class="crosspair"><h3>Data Infrastructure as Bottleneck — World-scale Generation(CV) vs VLA Data Survey(RO)</h3><p><a href="https://arxiv.org/abs/2604.22828">MetaEarth3D</a>(CV)는 \'기존 3D generation이 bounded 환경에 갇혀있다\'며 spatially scalable world-scale generation을 시도. 같은 날 <a href="https://arxiv.org/abs/2604.23001">VLA Survey</a>(RO)는 \'VLA의 진짜 bottleneck은 architecture가 아니라 data infrastructure\'라는 강한 클레임. 둘 다 \'모델보다 데이터/공간 인프라가 한계\'라는 같은 문제 인식을 공유하지만, CV는 \'생성용 데이터 인프라\' RO는 \'학습용 데이터 인프라\' 측을 정조준. 같은 진단이 두 community에서 동시 표면화하는 건 \'데이터 인프라\'가 향후 6개월 양쪽 공통 키워드가 될 신호로 봅니다.</p></div>')

    # Must-read
    parts.append('<h2>🌟 오늘의 must-read</h2>')
    parts.append('<div class="mustread">')
    parts.append('<h3>① Breaking Lock-In: Preserving Steerability under Low-Data VLA Post-Training <span class="badge badge-cvro">CV/RO</span></h3>')
    parts.append('<p><a href="https://arxiv.org/abs/2604.23121">arxiv:2604.23121</a> · Suning Huang et al.</p>')
    parts.append('<div class="section-title">핵심 주장</div>')
    parts.append('<p>VLA model을 small demonstration dataset으로 post-training 하면 새 instruction에 반응을 멈추고 post-training 시 본 행동만 반복하는 silent failure를 처음 명명 — \'lock-in\'. 기존엔 post-training이 마냥 잘 되는 줄 알았는데 사실은 모델이 \'instruction-following\' 능력 자체를 잃어버리는 거였어요. Steerability(새 명령에 따라 행동을 바꾸는 능력)를 metric으로 명시화하고, low-data regime에서 lock-in을 회복시키는 처방을 제안. VLA practitioner라면 본인 fine-tuning 파이프라인에 곧장 영향이 있는 진단입니다.</p>')
    parts.append('<div class="section-title">방법의 핵심 (직관)</div>')
    parts.append('<pre># Diagnosis: standard post-training causes lock-in\nfor demo_batch in small_dataset:\n    loss = behavior_clone(vla, demo_batch)  # tightens to demo behaviors\n    # Side effect: language conditioning gradient -> 0\n    # Result: model executes demos but ignores new prompts\n\n# Prescription: explicit steerability preservation\nfor demo_batch, instruction_diverse_batch in zip(...):\n    bc_loss = behavior_clone(vla, demo_batch)\n    steer_loss = preserve_instruction_response(vla, instruction_diverse_batch)\n    loss = bc_loss + alpha * steer_loss   # keeps language path alive</pre>')
    parts.append('<div class="section-title">약점·한계</div>')
    parts.append('<p>(a) \'low-data\' 정의가 task-dependent라 일반화된 threshold가 없어 본문에서 정량 cutoff 검증 필요. (b) Lock-in 회복 처방이 instruction-diverse data를 별도 요구하면 post-training의 cost-down 동기 자체가 약해질 수 있음. (c) 어떤 instruction class가 lock-in 영향을 가장 받는지(spatial vs temporal vs object name) 분해 ablation이 abstract만으론 안 보입니다. (d) Lock-in이 \'post-training 가능성 자체에 대한 회의\'로 연결될 수 있는데 그 보다 적극적인 \'fine-tuning이 항상 도움\'이라는 통념을 어느 정도까지 무너뜨리는지 정량 데이터 필요.</p>')
    parts.append('<div class="section-title">랩 파이프라인 영향</div>')
    parts.append('<p>우리가 VLA를 small demonstration로 fine-tune 하는 워크플로우라면 즉시 audit 필요한 결입니다. 특히 medical/long-task 시나리오에서 \'demo 100~500개로 fine-tune\' 패턴이 흔한데 lock-in이 silent하게 일어나면 deployment 단계에서 backfire. Fine-tuning 후 instruction-following holdout test를 standard practice로 들여놓는 게 맞습니다.</p>')
    parts.append('</div>')

    parts.append('<div class="mustread">')
    parts.append('<h3>② Vision-Language-Action Safety: Threats, Challenges, Evaluations, and Mechanisms <span class="badge badge-ro">RO</span></h3>')
    parts.append('<p><a href="https://arxiv.org/abs/2604.23775">arxiv:2604.23775</a> · Qi Li et al.</p>')
    parts.append('<div class="section-title">핵심 주장</div>')
    parts.append('<p>VLA safety의 4축(threats·challenges·evaluations·mechanisms)을 systematic하게 매핑한 첫 통합 survey. 어제 RedVLA(physical red teaming)와 그 전 결들이 개별 처방이었다면, 이 논문은 \'VLA가 physical actuation 가능 multimodal LLM\'이라는 본질에서 새로 등장하는 safety class 자체를 정의합니다 — irreversible physical consequences, multimodal attack surface, embodied feedback loop. 우리 manipulation 스택의 safety roadmap을 짤 때 reference framework로 곧장 들어옵니다.</p>')
    parts.append('<div class="section-title">방법의 핵심 (axis 매핑)</div>')
    parts.append('<pre>VLA Safety Axis = {\n  Threats:     adversarial input(visual/language/action),\n               jailbreak, distribution shift, sim2real gap\n  Challenges:  irreversible action, multimodal coupling,\n               embodiment-specific risk, real-time constraint\n  Evaluations: physical red teaming, benchmark suite,\n               formal verification, sim-only vs hardware\n  Mechanisms:  CBF/MPC safety filters, RL-based shielding,\n               alignment training, runtime monitoring\n}</pre>')
    parts.append('<div class="section-title">약점·한계</div>')
    parts.append('<p>(a) Survey이므로 새 method가 아닌 기존 결의 통합 — original contribution을 기대하면 실망할 수 있어요. (b) \'embodied multimodal LLM에서 새로 등장하는 safety class\' 정의가 abstraction 수준이 높아, 실제 처방으로 내려가는 단계에서 LLM safety 라인의 결과 단순 imports될 위험. (c) 4축 매핑의 axis가 mutually exclusive인지(예: threat vs challenge 경계) 본문에서 명확하지 않으면 frame이 약해질 수 있어요. (d) 평가/메커니즘 측 SOTA recommendation이 빠르게 outdated될 수 있다는 survey 특성.</p>')
    parts.append('<div class="section-title">랩 파이프라인 영향</div>')
    parts.append('<p>VLA 기반 manipulation 스택을 굴리는 랩이라면 safety roadmap의 starting framework로 채택할 가치가 큽니다. 특히 deployment 직전 \'어떤 threat을 어떤 evaluation으로 측정하고 어떤 mechanism으로 막을지\' decision tree로 활용 가능. 의료·산업 deployment 측이라면 4축 모두 cover하는 audit checklist를 만드는 데 곧장 reference로 사용.</p>')
    parts.append('</div>')

    # 리스크 필터
    parts.append('<h2>⚠️ 리스크·한계 필터</h2>')
    parts.append('<div class="risk"><h3>Transferable Physical-World Adversarial Patches — \'physical-world\' 클레임의 lab vs 야외 갭</h3><p><a href="https://arxiv.org/abs/2604.23105">Transferable Physical-World Adversarial Patches Against Object Detection</a>가 multi-stage AD detection 파이프라인 동시 교란 + appearance robustness를 클레임. 어제 TriPatch와 동일 라인의 결이지만, \'physical-world\' 단어가 실세계 다양 조명·각도·거리·운동에서 평균 성공률을 낮추는 게 이 라인 고질병이에요. 통제된 lab vs 야외 다양 시나리오 효과 차가 abstract만으론 안 잡혀, weather/distance/motion ablation 표 정독 전엔 \'production AV 위협\' 강한 클레임은 보류.</p></div>')
    parts.append('<div class="risk"><h3>VLA Survey의 \'data infrastructure가 진짜 bottleneck\' 클레임 — 검증 가능한 prediction인가</h3><p><a href="https://arxiv.org/abs/2604.23001">VLA Survey</a>의 \'architecture가 아니라 data infrastructure가 진짜 bottleneck\'이라는 클레임은 강력하지만 검증 가능 prediction으로 분해되지 않으면 narrative에 그칠 위험. 예컨대 \'데이터 양 N배 vs architecture 개선 X% 시 어느 쪽이 더 큰 SOTA gain\' 같은 정량 비교가 없으면 시각이 healthy해도 행동 가이드로는 약합니다. Survey 본문에서 retrospective 정량 비교가 충분히 보고되는지 확인 필요.</p></div>')
    parts.append('<div class="risk"><h3>PushupBench·Dynamic Gauges 류 \'failure mode\' 벤치 — single-task 스코어가 frontier 차이를 가르나</h3><p><a href="https://arxiv.org/abs/2604.23407">PushupBench</a>(VLM이 푸쉬업 42% 카운트), <a href="https://arxiv.org/abs/2604.22829">Dynamic Gauges</a>(진동 계기판 읽기 실패) 같은 single-task failure 벤치는 진단 가치는 있지만, frontier VLM 사이의 \'어느 모델이 진짜 더 나은가\'를 single-task로 결정하면 cherry-pick 인센티브가 작용합니다. 향후 evaluators가 이 single-task 벤치를 frontier 비교에 쓰지 않도록 \'배경 진단\'으로만 사용하는 게 안전 — 통합 atlas로 묶기 전엔 \'X 모델이 Y 모델보다 낫다\' 강한 결론은 보류.</p></div>')
    parts.append('<div class="risk"><h3>Tuna-2의 \'Pixel Embeddings Beat Vision Encoders\' 클레임 — fair comparison인가</h3><p><a href="https://arxiv.org/abs/2604.24763">Tuna-2</a>가 \'pixel embedding이 vision encoder를 이긴다\'는 강한 클레임을 unified MLLM 측에서. End-to-end pixel-from-scratch가 가능하다는 결 자체는 흥미롭지만, vision encoder 경쟁자가 같은 학습 token budget·compute로 비교됐는지가 핵심. End-to-end 측이 더 큰 compute로 학습됐으면 \'win\' 클레임은 fair comparison이 아닐 수 있어요. 본문의 compute-matched ablation 테이블 정독 전엔 \'vision encoder 시대 끝\' 강한 결론은 잠정 보류가 안전.</p></div>')

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
