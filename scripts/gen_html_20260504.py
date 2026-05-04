#!/usr/bin/env python3
"""Generate posts/2026-05-04.html (Monday — fresh batch + retrospective loop active)."""
import json, html, io, os, sys

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

DATE = "2026-05-04"
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
.retro{background:#eef2ff;border:1px solid #c7d2fe;border-radius:8px;padding:14px 18px;margin:12px 0}
.retro h3{margin:0 0 6px 0;font-size:15px;color:#3730a3}
.retro .label-hit{color:#15803d;font-weight:700}
.retro .label-partial{color:#a16207;font-weight:700}
.retro .label-miss{color:#b91c1c;font-weight:700}
.retro .label-pending{color:#0369a1;font-weight:700}
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

# Per-paper summary (구어체 3~5줄, 원칙 1·2 따름)
SUMMARIES = {
    # 3D/Scene
    '2605.00052': "Hybrid-capture(드론+지상) 3DGS는 minority view에서 1-3 dB 저하되는 게 표준 문제였는데, 이 논문은 'GradNorm·preconditioning·gradient surgery 다 시도해도 결국 2-view per step rendering이라는 가장 단순한 구조 변화가 이긴다'고 정리했어요. 30K iterations 표준 학습 stack에 가장 작은 변경으로 가장 큰 효과가 나는 자리라, 향후 multi-modal capture 라인의 default 학습 lever로 정착할 가능성이 큽니다.",
    '2605.00147': "비협조적 우주 물체(non-cooperative space object)의 3D mesh를 단일 이미지에서 복원하는 파이프라인. 도메인 자체가 좁지만 우주 rendezvous·debris removal 측에서 즉시 가치 있는 자리.",
    '2605.00219': "VkSplat이 처음으로 fully-Vulkan 기반 3DGS 학습 스택을 만들었고 CUDA+PyTorch 대비 3.3× 속도 + VRAM 33% 절감 + cross-vendor GPU 호환을 한 번에 챙겼어요. 'CUDA monoculture'에서 벗어나는 첫 분명한 결로, AMD/Intel GPU에서도 3DGS 학습이 표준 가능해진 자리. infrastructure 측 확장에 가장 큰 영향을 미칠 결입니다.",
    '2605.00242': "mmWave 비디오에서 self-supervised로 human pose를 학습 — RGB 의존 없이 mmWave radar로 pose 인식하는 흐름의 한 결.",
    '2605.00345': "Pose-Aware Diffusion(PAD)이 'canonical 만들고 회전' 2단계를 버리고 monocular depth를 unprojection한 partial point cloud를 직접 anchor로 박아 observation space에서 generation. pose ambiguity가 자연스럽게 해소되는 구조라, text-to-3D 측에서 pose 정렬 측면 표준 후보가 될 자리예요.",
    '2605.00408': "LeGS는 3DGS의 heuristic density control을 RL policy로 통째로 대체했고, sensitivity-grounded reward로 각 Gaussian의 marginal contribution을 정량화하는 게 핵심. O(N²) → O(N) closed-form 단순화로 학습 비용도 챙겼고 Mip-NeRF 360 + Tanks Temples + Deep Blending 3개 표준 벤치 동시 통과 — 'RL이 3DGS 내부 학습 stack에 처음 들어온' 결로 향후 6개월 standard 가능성.",
    '2605.00498': "GOR-IS는 3D 객체 제거(object removal)를 'intrinsic space'에서 처리해 global lighting + non-Lambertian view-dependent 표면까지 일관성 있게 inpainting. 3DGS editing line의 한 결로, asset/시뮬 파이프라인에서 즉시 가치.",
    '2605.00517': "PhysiGen이 collision-aware physical constraint를 high-fidelity human-human interaction generation에 통합 — pose 측 generation에 physics 측 constraint가 first-class로 들어가는 흐름의 한 결.",
    '2605.00562': "Depth + 3D sphere cloud를 활용한 privacy-preserving visual localization. SLAM/AR 측에서 'image 자체를 server에 안 보내고도' localization하는 라인의 한 결.",
    '2605.00569': "2D-SuGaR가 SfM 의존이 큰 2DGS의 약점을 monocular depth/normal prior로 안정화 — sparse-view·challenging input에서 표면 reconstruction 정확도가 분명히 좋아지는 자리. 지난주 sparse-view 3DGS 4편 burst의 후속 결로 surface reconstruction 측 결이 추가됩니다.",
    '2605.00177': "FieryGS가 3DGS pipeline 안에 physics-based combustion simulation을 통합 — 'real scene + 물리적으로 정확한 fire effect'를 한 framework에서. CFD 수동 작업을 우회하는 결로 시뮬레이션·VFX 측에서 즉시 가치.",
    '2605.00634': "공중-지상 LiDAR cross-source pose registration을 height-stratified 방식으로 — 위성/드론 LiDAR와 지상 LiDAR 정렬 측면 첫 분명한 결.",
    '2605.00397': "MiniVLA-Nav v1이 language-conditioned robot navigation 측 multi-scene simulation 데이터셋 — VLA 학습 스택용 인프라 측 결로, RL 측 fleet-scale 학습과 짝을 이룹니다.",

    # Robot Learning
    '2605.00078': "기존 VLA가 'pixel-space future frame prediction'으로 reasoning을 보강했지만 그게 비싸고 control과 무관한 시각 디테일까지 학습한다는 진단에서 출발해요. Being-H0.7은 latent query를 perception-action 사이에 끼워 넣어 future frame을 안 만들고도 future-aware reasoning을 챙기는 구조 — training only posterior branch가 future obs를 보고 prior branch를 align하는 dual-branch 학습이 핵심. LaST-R1·MotuBrain의 'latent CoT + RL' paradigm을 'world-action' 측에서 정조준한 결로, 2주 연속 같은 흐름이 누적되는 자리예요.",
    '2605.00080': "World Model for Robot Learning Survey — pixel-based vs latent vs JEPA-style 분류, policy/sim/eval/data-gen 측면 활용 정리, navigation·driving까지 cross-domain 정리. 2주 연속 'pixel-free latent WM' 흐름이 본격화되는 시점에 등장한 정리 paper라 timing이 적절합니다.",
    '2605.00244': "Lucid-XR가 XR 헤드셋에 직접 돌아가는 web-based physics sim(vuer) + human-to-robot pose retargeting + physics-guided video generation을 통합한 generative data engine. zero-shot policy transfer를 입증 — 'data engine' 측 인프라 paper로 fleet-scale RL과 함께 보면 학습 스택의 양 끝 결입니다.",
    '2605.00307': "Compliant gripper에 RGB-D wrist camera로 visual force estimation — model-based 접근으로 end-to-end deep learning의 brittleness 회피. tactile sensor 없이도 force sensing 가능해지는 자리로, gripper 측 cost-down에 직접 영향.",
    '2605.00475': "MSACT가 fine bimanual manipulation 측에서 ACT의 low-latency·data efficiency와 voxel-based의 spatial consistency를 multistage spatial alignment로 합쳤어요. low-latency + stable visual localization 동시 달성 — bimanual fine manipulation 측 표준 후보.",
    '2605.00159': "E²DT는 Decision Transformer의 uniform replay 비효율을 k-DPP sampling으로 해결 — RL replay 측 결로 long-horizon manipulation 학습 efficiency 직접 영향.",
    '2605.00261': "Legged locomotion에서 epistemic uncertainty를 task-conditioned costmap으로 출력 — single learned model이 in-distribution과 OOD 구간을 구분하게 만들어 highly unstructured terrain에서 robust footstep planning 가능. quadruped/humanoid line의 robust locomotion 측 결.",
    '2605.00321': "Embodied Interpretability — VLA가 spurious correlation에 의존하는지 정량화하는 ISS(interventional masking) + NMR(nuisance ratio) 도입. 'interpretability를 distribution shift 진단 도구로' 정조준한 결이라 VLA generalization 측 audit framework 후보.",
    '2605.00384': "PrefMoE가 preference-based RL의 'heterogeneous/conflicting annotator' 문제를 single reward 대신 MoE reward로 해결 — RLHF/preference 측 reward learning 표준에 영향 가능.",
    '2605.00416': "LWD(Learning While Deploying)가 16 dual-arm robot fleet × 8 real-world manipulation task에서 offline-to-online RL로 pretrained VLA를 continual post-training. DIVL + QAM 조합으로 sparse fleet reward에서 안정적 학습 — VLA 인프라 측 large-scale 결로 'fleet-scale RL이 표준 가능' 첫 분명한 자리.",
    '2605.00471': "Stereo multistage spatial attention으로 mobile manipulation의 visual scale variation 해결 — 4 task real-world 평가, mobile platform용 closed-loop 결.",
    '2605.00623': "EnergyFlow가 diffusion-based policy의 score function이 expert soft Q-function의 gradient를 회복한다는 걸 증명 — adversarial 없이 reward extraction. inverse RL 측 결인데 generative action modeling line에 직접 substrate가 됩니다.",
    '2605.00438': "IVLR(Interleaved Vision-Language Reasoning)가 textual subgoal과 visual keyframe을 번갈아 짠 trace를 single multimodal transformer가 self-generate해 closed-loop action에 conditioning. 95.5% long-horizon 성공률 — Being-H0.7과 짝을 이루는 'latent reasoning' line의 한 결입니다.",

    # Autonomous Driving
    '2605.00051': "사고 anticipation용 generative data augmentation — 사고 데이터 부족 문제를 generative로 우회하는 결.",
    '2605.00291': "End-to-end + decision-aware multi-scale attention으로 explainable AD 정조준 — explainability 측 결.",
    '2605.00296': "Vegetation pixel classification — vision transformer로 농업/원격 측 결, AD 라벨이지만 substantive AD 결은 아님.",
    '2605.00362': "Time-series + complex motion modeling 결합한 robust motion prediction — AD 측 motion forecasting 결.",
    '2605.00595': "V2X object-level fusion으로 robust 3D object detection — V2X 측 결.",
    '2605.00781': "Map2World가 segment map(임의 모양·scale) 조건으로 3D world generation — grid layout 의존 회피 + scale consistency 챙김. driving simulation·immersive content 양 측면 인프라 결로 GSDrive와 결합 가능.",
    '2605.00050': "공개된 NHTSA 사고 보고서(텍스트)에서 physically grounded 사고 reconstruction — 6,217 case CISS-REC 데이터셋. 'public report → quantitative reconstruction'이라는 새 substrate 정의로 AD safety analysis·시뮬용 데이터 측면 직접 가치.",
    '2605.00066': "NAVSIM v2의 safety-aware open-loop metric이 closed-loop driving score를 예측하는지 15-method × 8 paired data 분석. 결론: NAVSIM PDM이 strong positive but non-monotonic + ranking inversion 존재 — open-loop metric만으로 closed-loop validation은 부족. AD evaluation methodology의 첫 정량적 정리로 community standard에 큰 영향.",
    '2605.00556': "Behaviour ↔ Perception linking으로 partially automated driving의 'meaningful human control' 평가 — human-machine interface 측 결.",

    # Foundation Models
    '2605.00323': "VLM hallucination을 online self-calibration으로 — test-time adaptation 측 결로 hallucination 측면 새 정조준.",
    '2605.00434': "LIMSSR이 LLM-driven sequence-to-score reasoning으로 training-time incomplete multimodal observation 처리 — 학습 데이터 결손 측 결.",
    '2605.00444': "MACF는 long video understanding의 perception budget 한계를 multi-agent latent communication protocol로 해결 — 각 agent가 segment를 compact token으로 인코딩하고 central coordinator가 합침. 'agent-native latent comm'이 textual intermediate 의존 회피의 첫 결로, long-video 측 표준 후보.",
    '2605.00480': "VLM을 weak annotator로 active learning에 — annotation cost 측 결.",
    '2605.00591': "Intrinsic Gradient Suppression으로 label-noise 상황에서 VLM prompt tuning robust화 — 학습 안정화 측 결.",
    '2605.00809': "ViT를 generative language-image pre-training에 — generative + ViT 결합 측 새 결.",
    '2605.00814': "Persistent Visual Memory로 LVLM의 deep generation 측 perception sustaining — long context generation 측 결.",
    '2605.00326': "Zero-shot binary VLM safety classification에서 prompt-induced score variance 측정 — 'prompt 변화에 safety score가 얼마나 민감한가'를 정조준한 결로 visual modality safety line의 한 결.",

    # Generation
    '2605.00273': "Diffusion model이 다중 객체 generation을 언제 학습하는가 — training dynamics 측 결.",
    '2605.00310': "Large-scale remote sensing super-resolution 벤치마킹 — 응용 측 결.",
    '2605.00367': "Sentinel-2 super-resolution을 flow matching으로 — 위성 영상 측 결.",
    '2605.00503': "End-to-end autoregressive image generation을 1D semantic tokenizer로 — 'AR diffusion 대체' 라인의 한 결.",
    '2605.00526': "IdentiFace가 multi-modal iterative diffusion으로 식별 가능한 suspect face generation — 법의학 측 결.",
    '2605.00548': "Training-free low-frequency noise manipulation으로 color-based conditional generation — controllable diffusion 측 결.",
    '2605.00630': "AI-generated video detection을 cross-modal temporal artifact로 — forensics 측 결.",
    '2605.00658': "UniVidX가 diffusion prior로 versatile video generation framework 통합 — multi-task video gen 측 결.",
    '2605.00664': "InpaintSLat이 structured 3D latent를 noise optimization으로 inpainting — 3D editing 측 결.",
    '2605.00707': "PhysEdit가 physics-consistent region-aware image editing을 spatio-temporal restoration으로 — 'physics-consistent editing' 측 결.",
    '2605.00718': "Coarse-to-fine osteoarthritis representation을 noisy hierarchical label에서 — 의료 영상 측 결, 'generation' 라벨이지만 분류 결.",
    '2605.00825': "Posterior augmented flow matching — flow matching 학습 안정화 측 이론 결.",
    '2605.00250': "Information-geometric adaptive sampling으로 graph diffusion — graph generation 측 결.",
    '2605.00358': "LLM parameter target construction의 backward spreading vs forward replay — LLM 학습 측 결, 'generation' 라벨이지만 LLM 측.",
    '2605.00510': "Scale-aware adversarial analysis — multiscale complex system에서 generative AI 진단 도구.",
    '2605.00793': "Real clinical low dose liver CT denoising — 의료 영상 측 결.",
    '2605.00412': "Hamiltonian World Models가 'video-gen vs 3D-scene vs JEPA-latent' 3 갈래 WM이 모두 'physically reliable + action-controllable + long-horizon stable'을 보장 못 한다는 진단에서 출발해요. observation을 structured latent phase space로 인코딩하고 Hamiltonian-inspired dynamics(control + dissipation + residual)로 진화시킨 후 디코딩 — physics-grounded substrate가 핵심. Being-H0.7과 같은 날 'pixel-free latent' 라인의 다른 측면 결로 paradigm shift 단단해지는 자리.",

    # Efficiency/Systems
    '2605.00146': "Spiking neural network로 frame+event-based real-time object detection on edge neuromorphic — 'event camera + SNN + edge' 측면 결.",
    '2605.00271': "REALM이 RGB와 event stream을 같은 latent manifold로 정렬 — cross-modal perception 표준 후보.",
    '2605.00392': "RTPrune이 'Reading-Twice' 패턴으로 DeepSeek-OCR token pruning — OCR-specific efficiency 측 결.",
    '2605.00405': "BOLT가 cooperative perception에서 preparation-free online lightweight adaptation — 'pre-deployment training 없이 deploy' 측 결.",
    '2605.00578': "Federated distillation으로 whole slide image 처리 — Gaussian-mixture feature alignment + curriculum 결합. 의료 영상 측 federated 결.",
    '2605.00605': "Faithful extreme image rescaling via learnable reversible transformation — image rescaling 측 결.",
    '2605.00789': "LVLM KV cache 경량화 — long-context VLM 측 efficiency 결, deployment 측에 직접 영향.",
    '2605.00799': "GMGaze가 MoE 기반 context-aware gaze estimation을 CLIP + multiscale transformer로 — gaze 측 결.",
    '2605.00140': "ARHQ(Activation Residual Hessian Quantization)가 low-bit LLM quantization 측 새 방식 — 양자화 라인의 한 결.",
    '2605.00174': "DPU + GPU 동시 활용해 split CNN inference — accelerator 측 결.",
    '2605.00461': "Dictionary unfolding network + gradient-adaptive fidelity로 transferable multi-task — 학습 측 결.",
    '2605.00527': "High-rate Lissajous confocal laser endomicroscopy multi-frame restoration — 의료 영상 측 결.",
    '2605.00642': "GUI grounding을 on-policy self-distillation으로 — GUI agent 측 결.",
    '2605.00536': "Tempus가 Versal AI Edge SoC용 temporally scalable resource-invariant GEMM streaming framework — edge AI hardware 측 결.",

    # Embodied AI
    '2605.00080': "World Model for Robot Learning Survey — 같은 paper, Embodied 측에서도 정리. (실제 ground truth는 RL 라인이지만 분류기에서 Embodied로 잡힘).",
    '2605.00059': "Dynamic-TD3가 dynamic obstacle trajectory prediction과 결합된 UAV path planning — TD3 응용 측 결.",
    '2605.00121': "Predictive spatio-temporal scene graph로 semi-static scene(객체가 cyclic하게 움직이는 환경) 모델링 — 'mug가 cupboard ↔ countertop ↔ sink 사이클' 같은 패턴 학습. embodied agent의 long-term memory 측 결.",

    # Safety/Alignment
    '2605.00350': "CURE-OOD가 survival prediction에서 OOD detection 벤치마킹 — 의료 OOD 측 결.",
    '2605.00401': "SIMON이 saliency-aware integrative multi-view object-centric neural decoding — neuro-decoding 측 결, 'safety' 라벨이지만 substantive safety 결은 아님.",
    '2605.00448': "Compressed CT에서 feature attention style transfer로 학습 — 의료 영상 측 결.",
    '2605.00474': "Local → Global → Mechanistic interpretation framework — interpretability 측 결.",
    '2605.00583': "VLM의 visual modality가 underexplored attack surface임을 정조준 — 4가지 visual jailbreak(visual cipher, object substitution, text-in-image swap, visual analogy puzzle)으로 6 frontier VLM 평가. visual cipher가 Claude-Haiku-4.5에서 40.9% ASR(같은 textual cipher 10.7% 대비 4배). 'text-based safety training이 visual modality로 자동 일반화 안 됨'을 첫 정량화 — visual-first safety paradigm의 분명한 첫 결.",
    '2605.00632': "BlenderRAG가 retrieval-augmented code synthesis로 high-fidelity 3D object generation — Blender Python API 활용 측 결, 'safety' 라벨이지만 generation 측.",
    '2605.00684': "Static + dynamic graph alignment로 temporal video grounding — 'safety' 라벨이지만 video understanding 측 결.",
    '2605.00719': "Reward-guided self-reinforcement로 unpaired image deraining — image enhancement 측 결.",
}

def esc(s): return html.escape(s or '', quote=True)

def badge_html(p):
    b = p.get('badge','')
    cls = {'CV':'badge-cv','RO':'badge-ro','CV/RO':'badge-cvro'}.get(b,'badge-cv')
    return f'<span class="badge {cls}">{esc(b)}</span>'

def summary_for(arxiv_id, title):
    s = SUMMARIES.get(arxiv_id)
    if s: return s
    return "오늘 /new 등록 결로, abstract 정독 전엔 정확한 평가가 어려워 본문 확인 권장합니다."

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

    parts.append('<div class="note-banner">📌 <strong>Monday note</strong> · 주말 후 첫 평일 배치라서 새 announcement가 들어왔어요. 오늘 /new는 cs.CV 81편(new+cross) + cs.RO 26편(new+cross) = 107편 candidate → 84편 ROI 매칭. 또 월요일 실행이라 <strong>예측 회고 루프</strong>가 활성화되어 2주 전(2026-04-23) 인사이트 채점이 들어갑니다(2026-04-20은 snapshotting 시작 전이라 04-23으로 대체). 4주 전 회고는 다음주(05-11)부터 첫 가능.</div>')

    parts.append('<div class="meta">')
    parts.append('<div><strong>시야:</strong> 주간 2026-04-28 ~ 2026-05-04 · 오늘 배치 cs.CV/new + cs.RO/new (Monday 5/4 listing)</div>')
    parts.append('<div><strong>소스:</strong> arxiv.org /list/cs.CV/new · /list/cs.RO/new (stdlib 파서 경유)</div>')
    parts.append('<div><strong>주간 규모:</strong> cs.CV 613편 · cs.RO 183편 (union ~796편 후보)</div>')
    parts.append('<div><strong>오늘 /new:</strong> cs.CV 146 + cs.RO 39 → 185 candidates → 104 ROI 매칭 → 84편 8개 ROI 버킷 선정</div>')
    parts.append('<div><strong>델타 기준:</strong> 7일 전 동급 pastweek 스냅샷(2026-04-27 — 같은 7일 rolling 단위)과 비교</div>')
    parts.append('</div>')

    # 주간 동향
    parts.append('<h2>🔭 주간 동향</h2>')
    parts.append('<p>이번주 가장 단단한 흐름은 <strong>VLA latent reasoning paradigm이 2주차에 들어선 것</strong>입니다. 지난주 LaST-R1·MotuBrain·PRTS가 \"latent CoT + RL\" 정조준한 자리에서, 이번주는 <a href="https://arxiv.org/abs/2605.00078">Being-H0.7</a>(latent world-action without future frame) + <a href="https://arxiv.org/abs/2605.00412">Hamiltonian World Models</a>(physics-grounded latent dynamics) + <a href="https://arxiv.org/abs/2605.00438">IVLR</a>(95.5% long-horizon)이 나란히 등장. 한 주만에 같은 paradigm이 다른 axis로 누적되는 건 burst가 아니라 <em>community standard 정착</em>의 분명한 신호고, 동시에 <a href="https://arxiv.org/abs/2605.00080">World Model Survey</a>가 정리 paper로 timing 맞춰 등장한 게 의미 깊습니다. 우리 랩이 VLA에서 future frame prediction을 substrate로 쓰고 있다면 paradigm 선회 시점.</p>')
    parts.append('<p>두 번째로 두드러지는 건 <strong>Autonomous Driving 측이 pastweek 기준 +267% 폭발</strong>한 것이에요(33편 vs 7일 전 9편). 단순 surge가 아니라 \"evaluation methodology\"라는 분명한 축이 잡힌 게 흥미로운데, <a href="https://arxiv.org/abs/2605.00066">NAVSIM ↔ Bench2Drive correlation 분석</a>이 \"open-loop metric만으로는 closed-loop 예측 불충분, ranking inversion 존재\"를 처음으로 정량화했어요. 같은 날 <a href="https://arxiv.org/abs/2605.00050">CISS-REC</a>(공개 사고 보고서 → physically grounded reconstruction)과 <a href="https://arxiv.org/abs/2605.00781">Map2World</a>(segment map → 3D driving sim asset)가 같이 등장 — community가 \"AD를 evaluation·data·sim 인프라 측에서 다시 짜는\" 흐름이 분명해졌습니다.</p>')
    parts.append('<p>한편 <strong>Safety/Alignment 측은 pastweek -27%로 한 주 더 cooling</strong>했지만, 그 안에서 <a href="https://arxiv.org/abs/2605.00583">Visual Modality Jailbreak</a> 한 편이 \"text-based safety training은 visual modality로 자동 일반화 안 됨\"을 첫 정량화한 게 가장 중요해요. Claude-Haiku-4.5에서 visual cipher 40.9% vs textual cipher 10.7% — 4배 격차로 \"visual modality는 first-class attack surface\"라는 paradigm shift의 분명한 첫 결입니다. Foundation Models가 -64%·Embodied -59%로 가장 cool했고, Efficiency/Systems가 +100%로 분명히 hot — \"deployment-heavy 라인(AD + Eff + 3D)\"으로 무게중심 이동이 한 주 더 단단해진 자리입니다.</p>')

    # CV vs RO
    parts.append('<h2>📐 CV vs RO 대비</h2>')
    parts.append('<p>오늘 분포는 Generation(17)·Efficiency(14)·3D/Scene(13)·RL(12)·AD(9)·FM(8)·Safety(8)·Embodied(3) — Generation·Efficiency 양강 + 3D/RL 중간 + Embodied 단독 cold. pastweek 시야에선 CV 613편 / RO 183편(3.4:1)로 CV 압도적인데, 오늘 batch에서 RL의 RO 비중이 8/12(67%) + AD의 RO 비중 2/9(22%) + Embodied의 RO 비중 2/3(67%) — \"deployment 라인은 RO 측이 주도\"하는 패턴이 한 주 내내 반복되는 자리예요. CV는 substrate(generation·efficiency)·RO는 closed-loop activation이라는 노동 분업.</p>')
    parts.append('<div class="contrast">')
    parts.append('<p><strong>① 공통으로 뜨는 키워드</strong></p>')
    parts.append('<ul>')
    parts.append('<li><code>3DGS</code> — CV(<a href="https://arxiv.org/abs/2605.00408">LeGS</a>·<a href="https://arxiv.org/abs/2605.00219">VkSplat</a>·<a href="https://arxiv.org/abs/2605.00569">2D-SuGaR</a>·<a href="https://arxiv.org/abs/2605.00498">GOR-IS</a>·<a href="https://arxiv.org/abs/2605.00177">FieryGS</a>) + RO(<a href="https://arxiv.org/abs/2605.00781">Map2World</a>) — CV는 \"학습 stack/edit/physics integration\", RO는 \"3D world simulation asset\". 한 주 내내 두 layer 통합 결은 안 등장.</li>')
    parts.append('<li><code>VLA + reasoning</code> — RO(<a href="https://arxiv.org/abs/2605.00078">Being-H0.7</a>·<a href="https://arxiv.org/abs/2605.00438">IVLR</a>·<a href="https://arxiv.org/abs/2605.00321">Embodied Interpretability</a>) + RO/VLA infra(<a href="https://arxiv.org/abs/2605.00416">LWD</a>·<a href="https://arxiv.org/abs/2605.00244">Lucid-XR</a>·<a href="https://arxiv.org/abs/2605.00475">MSACT</a>) — 알고리즘 측 + 인프라 측이 같은 batch에 동시 등장. 2주 전 \"인프라 race\" 예측이 표면화한 자리.</li>')
    parts.append('<li><code>world model</code> — CV(<a href="https://arxiv.org/abs/2605.00412">Hamiltonian WM</a>) + RO(<a href="https://arxiv.org/abs/2605.00078">Being-H0.7</a>·<a href="https://arxiv.org/abs/2605.00080">WM Survey</a>) — \"pixel-free latent\" 흐름이 두 진영에서 동시 정조준.</li>')
    parts.append('</ul>')
    parts.append('<p><strong>② CV에만 뜨는 키워드</strong></p>')
    parts.append('<ul>')
    parts.append('<li><code>medical/clinical imaging</code> — <a href="https://arxiv.org/abs/2605.00718">osteoarthritis</a>·<a href="https://arxiv.org/abs/2605.00350">CURE-OOD survival</a>·<a href="https://arxiv.org/abs/2605.00578">whole slide image FedDistill</a>·<a href="https://arxiv.org/abs/2605.00793">low-dose liver CT</a>·<a href="https://arxiv.org/abs/2605.00527">Lissajous CLE</a> — 한 날 5편 + Safety/Generation 잡음의 핵심 자리.</li>')
    parts.append('<li><code>VLM evaluation/safety classifier</code> — <a href="https://arxiv.org/abs/2605.00323">Online Self-Calibration</a>·<a href="https://arxiv.org/abs/2605.00326">Prompt Variance Safety</a>·<a href="https://arxiv.org/abs/2605.00583">Visual Jailbreak</a> — \"VLM의 prompt 측 sensitivity\" 측 결이 한 날 3편.</li>')
    parts.append('<li><code>edge accelerator / quantization</code> — <a href="https://arxiv.org/abs/2605.00146">SNN edge</a>·<a href="https://arxiv.org/abs/2605.00140">ARHQ</a>·<a href="https://arxiv.org/abs/2605.00174">DPU+GPU split</a>·<a href="https://arxiv.org/abs/2605.00536">Tempus Versal</a> — Eff/Systems +100% 폭발의 핵심 자리.</li>')
    parts.append('</ul>')
    parts.append('<p><strong>③ RO에만 뜨는 키워드</strong></p>')
    parts.append('<ul>')
    parts.append('<li><code>fleet-scale RL infrastructure</code> — <a href="https://arxiv.org/abs/2605.00416">LWD</a>(16 dual-arm fleet) — \"VLA를 fleet에서 continual post-training\" 첫 large-scale 결.</li>')
    parts.append('<li><code>preference / inverse RL</code> — <a href="https://arxiv.org/abs/2605.00384">PrefMoE</a>·<a href="https://arxiv.org/abs/2605.00623">EnergyFlow</a> — RLHF/preference 측면 reward learning 라인.</li>')
    parts.append('<li><code>UAV / autonomous fleet</code> — <a href="https://arxiv.org/abs/2605.00059">Dynamic-TD3 UAV path</a> — UAV/fleet 라인은 한 주 내내 RO 단독 자리.</li>')
    parts.append('<li><code>open-loop ↔ closed-loop bridge</code> — <a href="https://arxiv.org/abs/2605.00066">NAVSIM/Bench2Drive correlation</a>·<a href="https://arxiv.org/abs/2605.00556">Behaviour-Perception linking</a> — AD evaluation methodology 측면이 RO 진영에서 정조준.</li>')
    parts.append('</ul>')
    parts.append('<p><strong>④ 같은 단어 다른 맥락</strong></p>')
    parts.append('<ul>')
    parts.append('<li><code>3DGS</code>: CV는 \'학습 stack/RL density control/physics integration\'(LeGS·FieryGS) / RO는 \'3D world simulation substrate\'(Map2World, GSDrive 지난주) — \"asset 만들기\" vs \"environment 만들기\"로 layer 자체가 정반대.</li>')
    parts.append('<li><code>safety</code>: CV는 \'medical OOD·visual jailbreak·prompt sensitivity\'(CURE-OOD·Visual Jailbreak·Prompt Variance) / RO는 \'physical actuation 측 architectural risk\'(지난주 Prompt-to-Actuation) — \"인지 측 bias 검출\" vs \"행동 측 architectural fail\"로 정반대 layer.</li>')
    parts.append('<li><code>RL</code>: CV는 \'학습 stack 내부 정책(LeGS density control, BOLT online adaptation)\' / RO는 \'fleet-scale post-training (LWD), reward learning(PrefMoE, EnergyFlow)\' — \"학습 효율 도구\" vs \"deployment 학습 substrate\".</li>')
    parts.append('</ul>')
    parts.append('</div>')
    parts.append('<p>지난주에 본 \"같은 단어 다른 맥락\"이 이번주 거의 좁혀지지 않은 게 분명해요. 특히 <em>RL이라는 한 단어가 \"3DGS density control\"부터 \"fleet-scale VLA post-training\"까지 layer가 5단 이상 다른 자리</em>라, 우리 랩이 \"RL 측 follow\"한다면 어느 layer 결인지 분명히 분리해서 보지 않으면 substantive vs 키워드 매칭이 섞이는 자리예요. 이게 향후 6개월 우리 랩이 RL 측 audit할 때 첫 분리 기준이어야 할 것 같습니다.</p>')

    # 인사이트
    parts.append('<h2>💡 오늘의 인사이트</h2>')
    parts.append('<div class="insight"><h3>VLA paradigm shift 2주차 — \'pixel-free latent world-action models\'이 community standard로 굳는 중</h3><p>지난주 LaST-R1·MotuBrain·PRTS 셋이 \"latent CoT + RL\" 정조준한 후 <em>한 주만에</em> <a href="https://arxiv.org/abs/2605.00078">Being-H0.7</a>(latent world-action without future frame) + <a href="https://arxiv.org/abs/2605.00412">Hamiltonian WM</a>(physics-grounded latent dynamics) + <a href="https://arxiv.org/abs/2605.00438">IVLR</a>(95.5% long-horizon)이 나란히 등장. \"pixel-space prediction은 비효율적이고 control과 무관한 visual detail까지 학습한다\"는 같은 진단을 다른 axis로 정조준 — 2주 연속 같은 paradigm이 누적되는 건 burst가 아니라 <em>community standard 정착</em>의 분명한 신호. 같은 날 World Model Survey까지 등장한 게 timing의 마침표 역할이에요. 우리 랩이 VLA에서 future frame prediction을 substrate로 쓰고 있다면 paradigm 선회 시점.</p></div>')
    parts.append('<div class="insight"><h3>VLM Safety가 \'text 부수 효과\'에서 \'visual modality first-class attack surface\'로 paradigm 전환</h3><p><a href="https://arxiv.org/abs/2605.00583">Visual Modality Jailbreak</a> 논문이 4가지 visual attack(visual cipher·object substitution·text-in-image swap·visual analogy puzzle)을 6 frontier VLM에 측정 — visual cipher가 Claude-Haiku-4.5에서 40.9% ASR, 같은 textual cipher 10.7%의 4배 격차. \"text-based safety training은 visual modality로 자동 일반화 안 됨\"을 첫 정량화. 한 주 전에 \"safety 라벨 잡음 vs architecture-level 결 분리해야 한다\"고 본 자리에서, 이번주는 <em>visual modality 자체가 첫 번째 attack surface라는 paradigm shift</em>가 직접 등장. 우리 랩이 VLM safety follow한다면 visual-first attack 측정 framework가 곧 표준 될 자리.</p></div>')
    parts.append('<div class="insight"><h3>Autonomous Driving evaluation methodology — \'open-loop ↔ closed-loop\' 격차의 첫 정량화</h3><p><a href="https://arxiv.org/abs/2605.00066">NAVSIM ↔ Bench2Drive Correlation Study</a>가 8 paired methods에서 \"NAVSIM PDM은 strong positive correlation but non-monotonic + 분명한 ranking inversion\" 정량화. EP(Ego Progress)가 가장 강한 단일 predictor 발견(safety-critical NC보다 큼). 한 주 전에 본 \"driving WM unified understanding+generation\" 흐름과 함께 보면 community가 \"open-loop benchmark 의존\"에서 \"closed-loop 표준 통과 의무\"로 무게중심 이동 — 우리 랩이 AD 평가 protocol 설계할 때 NAVSIM-only 검증으로는 신뢰성 보장 어려움. CISS-REC의 \"public report → reconstruction\"도 같은 \"AD를 인프라 측에서 다시 짜는\" 흐름의 한 결.</p></div>')

    # 추천 연구주제
    parts.append('<h2>🔬 추천 연구주제</h2>')
    parts.append('<div class="topic"><h3>Pixel-Free VLA World-Action Bench — Latent vs Pixel Substrate Atlas</h3><p>Being-H0.7·Hamiltonian WM·LaST-R1·IVLR가 모두 \"pixel-free\" 측을 정조준했지만 \"같은 task에서 latent vs pixel substrate를 head-to-head 비교\"한 결은 비어 있어요. LIBERO·CALVIN·RoboCasa × {pixel rollout WM, latent WAM, Hamiltonian latent} 3 paradigm × 3 표준 벤치 atlas로 묶으면 향후 6주 안에 community standard 후보. <em>첫 mover 자리가 가장 비어있는 timing</em>이에요 — paradigm 굳어가는 자리니 비교 paper 1편이 즉시 가치. 우리 VLA 인프라가 있다면 이번주 sprint 시작 적절.</p></div>')
    parts.append('<div class="topic"><h3>Visual-First VLM Safety Bench — Cross-Modal Attack Surface Atlas</h3><p>Visual cipher·object substitution·text-in-image swap·visual analogy puzzle 4가지 visual attack을 frontier VLM 6개에 측정한 첫 결을 atlas로 확장 — open VLM(LLaVA·Qwen-VL)까지 포함해 <em>\"text safety vs visual safety 격차\"를 model 별로 측정한 standard bench</em>. 향후 VLM safety 평가의 첫 표준 가능성. 우리 랩이 VLM eval 인프라 있다면 즉시 sprint 가치 있는 자리.</p></div>')
    parts.append('<div class="topic"><h3>Closed-Loop AD Evaluation Methodology Audit — NAVSIM/Bench2Drive 외 3rd suite 정착 가능성 평가</h3><p>NAVSIM ↔ Bench2Drive correlation 결과가 \"ranking inversion\" 정량화한 자리에서, NAVSIM·Bench2Drive 외 CARLA Leaderboard·nuPlan과의 4-way correlation 측정이 다음 단계. 어떤 metric이 4-suite cross-validation에서 살아남는가가 community가 합의할 closed-loop 표준의 첫 조건 — 우리 랩이 AD 측 평가 인프라 있다면 6주 audit 가치 있는 자리예요.</p></div>')

    # 예측 회고 루프 (월요일만)
    parts.append('<h2>🧭 예측 회고 루프</h2>')
    parts.append('<p>이번주는 월요일 실행이라 회고가 활성화돼요. <strong>2주 전(2026-04-23 — 2026-04-20은 snapshotting 시작 전이라 가장 가까운 04-23으로 대체, delta 11일)</strong>의 인사이트·추천주제를 채점합니다. <strong>4주 전(2026-04-06)</strong>은 snapshotting이 아직 시작 안 된 시점이라 회고 불가 — 다음주(05-11)부터 첫 가능.</p>')

    parts.append('<div class="retro"><h3>2주 전 인사이트 채점</h3>')
    parts.append('<ul>')
    parts.append('<li><span class="label-hit">✅ 적중</span> · <em>"World model 평가가 픽셀 품질에서 embodied 성공률로 이동"</em> — 오늘 <a href="https://arxiv.org/abs/2605.00078">Being-H0.7</a>가 \"pixel-space prediction이 비효율적 substrate\"라며 latent world-action으로 직접 선회. <a href="https://arxiv.org/abs/2605.00080">WM Survey</a> + <a href="https://arxiv.org/abs/2605.00412">Hamiltonian WM</a>까지 모두 \"pixel-quality vs embodied success\" 경계를 명시적으로 인용. 2주 전 예측 방향 그대로 community 결이 쏟아진 자리 — 가장 강한 적중.</li>')
    parts.append('<li><span class="label-hit">✅ 적중</span> · <em>"VLA가 알고리즘 경쟁에서 훈련 스택·표현 통일의 인프라 경쟁으로 국면 전환"</em> — <a href="https://arxiv.org/abs/2605.00416">LWD</a>(fleet-scale RL infra) + <a href="https://arxiv.org/abs/2605.00244">Lucid-XR</a>(XR data engine) + <a href="https://arxiv.org/abs/2605.00475">MSACT</a>(low-latency 인프라) + <a href="https://arxiv.org/abs/2605.00159">E²DT</a>(efficient DT replay)가 한 날 4편 — 인프라 측 paper 비중이 알고리즘 측 대비 분명히 우세해진 자리. 2주 전 예측 그대로 \"infrastructure race\" 표면화.</li>')
    parts.append('<li><span class="label-partial">◐ 부분적중</span> · <em>"Safety 버킷이 얇은 만큼 \'human-aware\'·\'hierarchical robust\' 같은 새 포지셔닝이 뚫리는 중"</em> — Safety는 분명히 새 포지션이 등장했지만 \"human-aware\"·\"hierarchical robust\" 측은 아니고, <a href="https://arxiv.org/abs/2605.00583">visual modality first-class attack surface</a>(jailbreak·prompt variance·embodied interpretability)로 분기. <em>방향 자체는 맞췄지만 구체적 포지션 키워드는 빗나간 자리.</em></li>')
    parts.append('</ul></div>')

    parts.append('<div class="retro"><h3>2주 전 추천 연구주제 채점</h3>')
    parts.append('<ul>')
    parts.append('<li><span class="label-pending">⏳ 관찰 중</span> · <em>"VLA Foundry 위에 safety head를 plug-in으로 얹기"</em> — VLA Foundry 후속 결은 안 나타났고 \"safety head plug-in\" 자체 시도도 없음. jailbreak 측 결만 등장 — 제안 자리는 여전히 비어있어 관찰 보류.</li>')
    parts.append('<li><span class="label-miss">✗ 빗나감</span> · <em>"Mask 수준 world model을 cross-embodiment RoboWM-Bench로 확장"</em> — RoboWM-Bench 후속 결 없고, World Model 측은 \"pixel-free latent\" 방향으로 분기 — Mask WM 측 cross-embodiment 확장 자리는 비어있는 채로 paradigm 자체가 바뀌어버림. 제안 시점에는 합리적 방향이었지만 paradigm shift가 더 빨랐던 자리.</li>')
    parts.append('<li><span class="label-pending">⏳ 관찰 중</span> · <em>"Language-driven 3DGS editing을 로봇 시뮬 asset 파이프라인에 결합"</em> — GSDrive(driving sim용 3DGS env)가 가장 가까운 결이지만 \"language-driven editing\" 측면은 아니고 \"closed-loop RL substrate\"로 분기 — 제안 자리는 여전히 비어있음.</li>')
    parts.append('</ul></div>')

    parts.append('<p>채점 요약: 인사이트 ✅ 2건 ◐ 1건 — 정확도 측면 강하게 검증된 회차. \"World model paradigm 이동\"·\"VLA 인프라 race\" 두 매크로 흐름은 정확히 예측 방향대로 강화. Safety는 \"새 포지션이 뚫린다\"는 메타 방향은 맞췄지만 구체 키워드는 빗나감 — 다음 회차에서는 메타 vs 구체 분리해서 점수 매기는 게 안전. 추천 연구주제는 ⏳ 2건 ✗ 1건 — 제안 자리가 비어있는 건 \"우리만 채울 자리\" 측면 여전히 의미 있고, ✗ 1건은 paradigm shift 속도가 더 빨랐던 case.</p>')

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
    parts.append(f'<p>🔥 <span class="hot">TOP3</span>: {top3[0][0]} ({top3[0][1]}), {top3[1][0]} ({top3[1][1]}), {top3[2][0]} ({top3[2][1]}) · ❄️ <span class="cold">BOTTOM2</span>: {bot2[0][0]} ({bot2[0][1]}), {bot2[1][0]} ({bot2[1][1]}). Generation 17편이 단독 1위지만 의료/원격 응용 잡음이 5+편이라 substantive 결은 ~12편으로 줄여 봐야 정확. Efficiency 14편 대부분이 edge accelerator·quantization 측에 dense — \"deployment\" narrative와 일치. Embodied AI 3편으로 한 주 내내 가장 조용한 자리.</p>')

    # 델타
    parts.append('<p>📈 <strong>주간 델타(2026-04-27 → 2026-05-04, 7일 rolling pastweek 단위)</strong>: 🚗 Autonomous Driving <span class="hot">+267%</span> (9→33), ⚡ Efficiency/Systems <span class="hot">+100%</span> (22→44), 📦 3D/Scene <span class="hot">+15%</span> (46→53), 🤖 Robot Learning <span class="cold">-10%</span> (71→64), 🛡️ Safety/Alignment <span class="cold">-27%</span> (51→37), 🎨 Generation <span class="cold">-38%</span> (105→65), 🏃 Embodied AI <span class="cold">-59%</span> (32→13), 🧠 Foundation Models <span class="cold">-64%</span> (111→40). <em>가장 분명한 신호는 AD·Efficiency·3D 3축 동시 surge</em> — 모두 \"physical world deployment\" 측 결이라는 공통점. 한 주 누적 패턴은 \"FM·Generation 양강\"에서 \"deployment-heavy 3축\"으로 무게중심 이동이 한 주 더 단단해졌어요.</p>')

    # 벤치마크 SOTA
    parts.append('<h2>📈 벤치마크 SOTA 추이</h2>')
    parts.append('<table style="border-collapse:collapse;width:100%;font-size:13.5px;margin:12px 0">')
    parts.append('<thead><tr style="background:#f6f8fa;border-bottom:1px solid #d0d7de"><th style="text-align:left;padding:8px">벤치마크</th><th style="text-align:left;padding:8px">메트릭</th><th style="text-align:right;padding:8px">이번주 최고</th><th style="text-align:left;padding:8px;padding-left:14px">논문</th></tr></thead>')
    parts.append('<tbody>')
    parts.append('<tr style="border-bottom:1px solid #eaeef2"><td style="padding:8px"><strong>Mip-NeRF 360 + Tanks Temples + Deep Blending</strong></td><td style="padding:8px">PSNR/SSIM (3 datasets)</td><td style="padding:8px;text-align:right;font-family:ui-monospace,monospace">SOTA across 3</td><td style="padding:8px;padding-left:14px"><a href="https://arxiv.org/abs/2605.00408">LeGS</a></td></tr>')
    parts.append('<tr style="border-bottom:1px solid #eaeef2"><td style="padding:8px"><strong>long-horizon manipulation (sim)</strong></td><td style="padding:8px">average SR</td><td style="padding:8px;text-align:right;font-family:ui-monospace,monospace">95.5%</td><td style="padding:8px;padding-left:14px"><a href="https://arxiv.org/abs/2605.00438">IVLR</a></td></tr>')
    parts.append('<tr style="border-bottom:1px solid #eaeef2"><td style="padding:8px"><strong>fleet manipulation (16 dual-arm × 8 task)</strong></td><td style="padding:8px">single generalist policy uplift</td><td style="padding:8px;text-align:right;font-family:ui-monospace,monospace">improves ✓</td><td style="padding:8px;padding-left:14px"><a href="https://arxiv.org/abs/2605.00416">LWD</a></td></tr>')
    parts.append('<tr style="border-bottom:1px solid #eaeef2"><td style="padding:8px"><strong>Claude-Haiku-4.5 visual cipher</strong></td><td style="padding:8px">Attack Success Rate</td><td style="padding:8px;text-align:right;font-family:ui-monospace,monospace">40.9%</td><td style="padding:8px;padding-left:14px"><a href="https://arxiv.org/abs/2605.00583">Visual Jailbreak</a></td></tr>')
    parts.append('<tr><td style="padding:8px"><strong>Vulkan 3DGS training</strong></td><td style="padding:8px">speed/VRAM vs CUDA+PyTorch</td><td style="padding:8px;text-align:right;font-family:ui-monospace,monospace">3.3× / -33%</td><td style="padding:8px;padding-left:14px"><a href="https://arxiv.org/abs/2605.00219">VkSplat</a></td></tr>')
    parts.append('</tbody></table>')
    parts.append('<p>5건의 substantive SOTA 보고가 한 batch에 등장 — 3D/RL/Safety/Eff 4 라인이 동시에 hot. LeGS의 \"3DGS density control을 RL로\"가 가장 paradigm 측 의미 강하고, LWD의 \"16 dual-arm fleet\"이 fleet-scale RL의 첫 large-scale 결, Visual Jailbreak가 \"frontier VLM 측 visual attack\" 첫 측정 — 모두 향후 6개월 standard 후보 자리.</p>')

    # 크로스오버 페어
    parts.append('<h2>🔀 크로스오버 페어</h2>')
    parts.append('<div class="crosspair"><h3>같은 \"latent world model\", 다른 substrate — Being-H0.7(RO/VLA) vs Hamiltonian WM(CV/RO)</h3><p><a href="https://arxiv.org/abs/2605.00078">Being-H0.7</a>(RO)이 dual-branch posterior alignment로 future obs를 latent에 distill하는 학습 측 substrate를 정조준하고, 같은 날 <a href="https://arxiv.org/abs/2605.00412">Hamiltonian WM</a>(CV/RO)는 latent을 structured phase space로 짜고 Hamiltonian dynamics(control + dissipation + residual)로 진화시키는 구조 측 substrate를 정조준. 둘 다 \"pixel-free latent WM\"이라는 같은 paradigm을 공유하지만, Being-H0.7는 \"학습 알고리즘으로 latent을 의미 있게\"이고 Hamiltonian WM는 \"latent의 구조 자체를 physics-grounded로\"라 substrate definition이 정반대. 두 결을 동시에 굴리면 \"learned latent vs structured latent\" 측 비교가 가능해져요 — 이건 향후 6주 paradigm 정착의 가장 분명한 비교 자리.</p></div>')
    parts.append('<div class="crosspair"><h3>같은 \"3DGS + RL\", 다른 layer — LeGS(CV) vs LWD(RO)</h3><p><a href="https://arxiv.org/abs/2605.00408">LeGS</a>(CV)가 3DGS 학습 stack 내부의 density control을 RL policy로 대체해 \"학습 stack 안에 RL 도입\"이라는 새 layer를 열었고, 같은 날 <a href="https://arxiv.org/abs/2605.00416">LWD</a>(RO)는 16 dual-arm 로봇 fleet을 RL로 continual post-training — \"deployment 측 RL 인프라\"의 첫 large-scale 결. RL이라는 한 단어가 \"학습 stack 내부 정책\"부터 \"fleet 단위 deployment\"까지 layer가 정반대인 자리에 동시 등장. \"RL이 어디에 도입되는가\"라는 질문 자체가 community 안에서 폭발적으로 확장 중인 신호로, 향후 6개월 RL의 활용 layer 자체가 표준 분류 대상이 될 자리예요.</p></div>')

    # Must-read
    parts.append('<h2>🌟 오늘의 must-read</h2>')

    # ① Being-H0.7
    parts.append('<div class="mustread">')
    parts.append('<h3>① Being-H0.7: A Latent World-Action Model from Egocentric Videos <span class="badge badge-cvro">CV/RO</span></h3>')
    parts.append('<p><a href="https://arxiv.org/abs/2605.00078">arxiv:2605.00078</a> · 저자 Hao Luo et al. · abstract 기반</p>')
    parts.append('<div class="section-title">핵심 주장</div>')
    parts.append('<p>기존 VLA가 sparse action supervision으로 학습되다 보니 dynamics·contact·task progress의 진짜 표현 대신 shortcut mapping을 배우는 문제가 있었고, 최근 \"future frame을 video rollout으로 예측해 representation 강화\" 흐름은 pixel-space 자체가 비싸고 control과 무관한 visual detail까지 학습하는 indirect substrate라는 진단에서 출발해요. Being-H0.7은 future frame을 만들지 <em>않고도</em> future-aware reasoning을 챙기는 latent world-action model — perception과 action 사이에 learnable latent query를 삽입하고, training-only posterior branch가 future obs로 latent을 채우면서 deployable prior branch와 align하는 dual-branch 설계가 핵심. 즉 \"future를 본 latent\"과 \"현재만 본 latent\"이 같아지도록 학습해서, 배포 시 prior branch만으로도 future-aware하게 reasoning. LaST-R1·MotuBrain 결과의 \"latent CoT + RL\" paradigm을 \"world-action\" 측에서 정조준한 결입니다.</p>')
    parts.append('<div class="section-title">방법의 핵심 (직관)</div>')
    parts.append('<pre># 기존 \"future frame WM\" VLA\nfuture_frame = decoder(wm(s_t, a_t))   # pixel rollout\na_t = policy(s_t, future_frame)         # 비싼 substrate\n# 한계: pixel 정확도가 control 정확도와 무관\n\n# Being-H0.7: pixel-free latent WAM\nq_latent = learnable_queries           # 학습 가능 query\n# Training: dual branch\nz_prior = prior_branch(s_t, q_latent)              # current 만\nz_post  = posterior_branch(s_t, q_latent, s_{t+k}) # future obs로 채움\nloss = action_loss + lambda * ||z_prior - z_post||^2\n# Deployment: prior branch만으로 future-aware reasoning\na_t = action_head(s_t, z_prior)</pre>')
    parts.append('<div class="section-title">약점·한계</div>')
    parts.append('<p>(a) Posterior branch alignment는 future obs가 deterministic하게 \"하나로 결정\"되는 자리에 강한데, contact-rich/stochastic dynamics에서는 posterior 자체가 multi-modal이라 alignment가 oversimplified될 risk — abstract엔 stochastic posterior 처리 ablation이 안 보임. (b) \"latent reasoning interface\"가 학습 데이터의 task 분포를 외워서 reasoning처럼 보이는 \"shortcut latent\" 가능성도 — true generalization vs distribution memorization 분리 측 ablation이 본문 정독 필수. (c) Egocentric video에 특화된 학습이라 third-person 데이터로의 transfer 측면 한계가 본문에서 명시적이어야 의미. (d) LaST-R1과의 paradigm 비교 측 정량 결과가 abstract엔 약함 — 두 결이 같은 LIBERO suite에서 head-to-head 비교 안 되어 있으면 \"누가 더 나은 latent\"인지 community가 판단 못 하는 자리.</p>')
    parts.append('<div class="section-title">랩 파이프라인 영향</div>')
    parts.append('<p>VLA + future prediction 측 인프라를 굴리는 랩이라면 즉각 paradigm 비교 후보. 우리 VLA가 pixel-space WM에 의존한다면 Being-H0.7 류 latent WAM으로 audit이 첫 단계 — 학습 시간·컴퓨트 측 직접 영향. 특히 한 주만에 LaST-R1·Hamiltonian WM·IVLR이 같은 \"pixel-free latent\" 측에 누적된 자리라 paradigm은 거의 굳었다고 봐도 무방, follow 시점이 늦어지면 비용 큰 자리예요. 이번주 sprint로 LaST-R1 vs Being-H0.7의 LIBERO head-to-head를 굴리는 게 가장 효율적인 follow-up.</p>')
    parts.append('</div>')

    # ② Hamiltonian World Models
    parts.append('<div class="mustread">')
    parts.append('<h3>② Physically Native World Models: A Hamiltonian Perspective on Generative World Modeling <span class="badge badge-cv">CV</span></h3>')
    parts.append('<p><a href="https://arxiv.org/abs/2605.00412">arxiv:2605.00412</a> · 저자 Anonymous · abstract 기반</p>')
    parts.append('<div class="section-title">핵심 주장</div>')
    parts.append('<p>현재 world model 연구가 \"2D video-generative(visual future synthesis)\" + \"3D scene-centric(spatial reconstruction)\" + \"JEPA-like latent(abstract predictive)\" 3 갈래로 부분 분리되어 발전 중인데, 셋 다 \"physically reliable + action-controllable + long-horizon stable\"을 보장 못 한다는 진단에서 출발해요. Hamiltonian World Models의 핵심은 observation을 structured latent <em>phase space</em>(coordinate + momentum)로 인코딩하고, control + dissipation + residual term을 가진 Hamiltonian dynamics로 latent state를 진화시킨 후 디코딩 — physics-grounded substrate가 \"이 latent dynamics는 에너지 보존·dissipation 같은 물리 법칙을 만족해야 한다\"는 inductive bias를 강제. 결과적으로 future가 \"realistic\"하기만 한 게 아니라 \"physically meaningful + action-useful\"하게 됩니다. Being-H0.7과 같은 날 \"pixel-free latent WM\" 라인의 다른 측면 결로, paradigm shift가 단단해지는 자리.</p>')
    parts.append('<div class="section-title">방법의 핵심 (직관)</div>')
    parts.append('<pre># 기존 latent WM (JEPA류)\nz_{t+1} = f_theta(z_t, a_t)   # 임의 latent\n# 한계: latent dynamics가 임의라 physics 위반 가능\n\n# Hamiltonian WM\nq, p = encoder(o_t)                       # phase space (좌표+운동량)\nH = H_phi(q, p)                            # 학습 Hamiltonian\ndq/dt =  partial H / partial p             # Hamilton equations\ndp/dt = -partial H / partial q + u(a_t) - D(q,p) + R(q,p)\n# u: control input, D: dissipation, R: residual\nq_{t+1}, p_{t+1} = integrate(...)\no_{t+1} = decoder(q_{t+1}, p_{t+1})\n# loss = recon + dynamics + physics consistency</pre>')
    parts.append('<div class="section-title">약점·한계</div>')
    parts.append('<p>(a) Hamiltonian inductive bias는 closed-system + smooth dynamics에서 잘 맞지만, contact·friction·rigid impact 같은 non-smooth dynamics에서는 \"residual term\"이 너무 크게 떠서 Hamiltonian 구조의 의미가 약해질 risk — manipulation·legged locomotion 측에서 ablation이 결정적. (b) Phase space 인코딩의 dimension 결정·학습 안정성 측 측면 abstract만으론 안 보임 — high-dim observation에서 phase space dimension scaling 측 정량 결과가 본문 필수. (c) \"Long-horizon stable\"이 강한 클레임인데 비교 baseline의 horizon 길이·정착 metric이 abstract엔 약함. (d) Action-controllable 측면이 \"control input u(a_t)\"의 단순 더하기로 모델링되어, complex action(VLA 측 multi-step action chunk)에 직접 적용 가능한지 측면 한계.</p>')
    parts.append('<div class="section-title">랩 파이프라인 영향</div>')
    parts.append('<p>World model 측 인프라를 굴리는 랩이라면 architecture 비교 후보. 특히 \"latent dynamics에 inductive bias를 어떻게 넣을 것인가\"라는 질문이 community standard로 정착하는 자리라, JEPA·video diffusion·Hamiltonian 3 paradigm 중 어느 측면이 우리 task에 맞는지 audit이 첫 follow-up. Being-H0.7과 같은 \"learned latent\"과 Hamiltonian WM의 \"structured latent\"이 head-to-head 비교 자리가 비어있는 게 향후 6주 가장 빠른 차별화 자리예요.</p>')
    parts.append('</div>')

    # 리스크 필터
    parts.append('<h2>⚠️ 리스크·한계 필터</h2>')
    parts.append('<div class="risk"><h3>Visual Jailbreak \"40.9% ASR\" — frontier model 측 reproducibility + alignment 업데이트 race 측면 의심</h3><p><a href="https://arxiv.org/abs/2605.00583">Visual Modality Jailbreak</a>의 Claude-Haiku-4.5 40.9% ASR이 강한 클레임이지만, frontier closed-model의 safety alignment는 weekly cadence로 업데이트되는 자리라 \"논문 제출 시점 vs 발행 시점\" 사이에 이미 mitigation이 들어갔을 가능성이 높아요. 6 frontier VLM에 대한 \"ASR 측정 일자\"가 본문에 정확히 명시되어야 reproducibility 의미. 또한 \"visual cipher\"의 정확한 prompt format이 model 측 system prompt setting에 sensitive할 가능성 — 같은 attack을 같은 model에 다른 일자에 굴리면 다른 결과가 나올 risk. \"40.9% ceiling\"이라 단정 보류, model-mitigation timeline 동기화한 측정이 follow-up.</p></div>')
    parts.append('<div class="risk"><h3>LeGS \"3 dataset SOTA\" — heuristic 대비 RL 학습 비용·variance 측 trade-off 의심</h3><p><a href="https://arxiv.org/abs/2605.00408">LeGS</a>가 Mip-NeRF 360 + Tanks Temples + Deep Blending 3개 표준 벤치 동시 통과한 게 강한 클레임이지만, RL 기반 density control은 \"학습 시간·variance\" 측면 heuristic 대비 cost가 크게 증가할 risk. O(N²) → O(N) closed-form 단순화로 reward 계산은 챙겼지만, RL 학습 자체의 wall-clock + variance + reward shaping sensitivity 측 정량 비교가 본문에서 필수. \"SOTA\"이지만 학습 비용이 10× 든다면 production 측에서는 의미 약함 — heuristic 대비 \"학습 시간 vs 품질\" Pareto 측 표 정독 필수.</p></div>')
    parts.append('<div class="risk"><h3>LWD \"single generalist policy improves\" — fleet RL 측 cherry-pick + safety 측 의심</h3><p><a href="https://arxiv.org/abs/2605.00416">LWD</a>가 16 dual-arm robot fleet × 8 task에서 single generalist policy가 \"improves\"한다고 하지만, 어떤 task에서 얼마나 improve했는지 abstract만으론 약하고 \"all 8 task에서 improve\"인지 \"평균만\"인지 결정적. fleet 학습은 \"한 robot의 hard failure가 fleet 전체 정책을 덮는\" silent failure가 흔한 자리 — task 별 SR 변화 + per-robot variance 측 정량 비교 필수. 또한 fleet RL 측 \"실시간 safety guarantee\" 측면이 abstract엔 약함 — autonomous rollout 중 hardware damage 측 incident 통계가 본문에서 정직하게 정리되어야 deployment 측면 신뢰성 의미.</p></div>')
    parts.append('<div class="risk"><h3>IVLR \"95.5% long-horizon SR\" — pseudo-supervision의 trace 품질 측 의심</h3><p><a href="https://arxiv.org/abs/2605.00438">IVLR</a>의 95.5% long-horizon SR가 강한 결인데, training trace가 \"VLM이 자동 captioning한 pseudo-supervision\"이라 trace 자체의 품질에 SR가 의존. VLM caption quality가 task에 따라 large variance인 자리라, \"VLM이 잘 captioning한 task에서는 95.5%·VLM이 잘 못한 task에서는 silent failure\"인 분포가 가능. specific benchmark suite(LIBERO-Long? CALVIN?) 측 명시 + 가장 어려운 individual task의 absolute SR + trace quality 측 ablation 정독 필수.</p></div>')

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
