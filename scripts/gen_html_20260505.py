#!/usr/bin/env python3
"""Generate the 2026-05-05 (Tue) arXiv daily briefing HTML."""
import io
import json
import os
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

DATE = "2026-05-05"
WEEKDAY = "화"
PASTWEEK_START = "2026-04-29"
PASTWEEK_END = "2026-05-05"

CLASSIFIED = json.load(open("out/classified.json", encoding="utf-8"))
PASTWEEK = json.load(open("out/pastweek_full.json", encoding="utf-8"))

# Manually authored commentary per paper (for headline papers).
# For non-headlined papers, we auto-generate a generic constructive 2-line summary
# from title + abstract first sentences using a simple rule-based approach.

PAPER_SUMMARIES = {
    # ============== 3D/Scene ==============
    "2605.01171": "Mesh를 입력으로 받아 'CAD 프로그램(Sketch + Extrude)'으로 직접 변환하는 hybrid optimization framework예요. 기존 mesh-to-CAD가 단순 sketch-extrude나 편집 어려운 mesh/Brep만 다뤘다면, CADFit은 incremental fitting + validation으로 복잡한 parametric construction sequence까지 복원합니다. CAD 자동 reverse engineering이 design/manufacturing 라인에서 작동 가능 영역을 한 단계 넓힌 자리.",
    "2605.01234": "방송 영상 monocular video 140시간을 4D reconstruction으로 풀어낸 table tennis 데이터셋이에요. 카메라 보정 + 3D 공 위치 + 회전 + 시간 segmentation + 3D human mesh를 한 패키지로 묶었고, 'sport-specific 4D recon pipeline + spin estimation'으로 정조준한 데이터 측 결입니다. Robot learning 측 sport video 데이터로의 다리가 분명히 열리는 자리.",
    "2605.01320": "Octree 기반 LiDAR 점군 압축이 causal multi-stage context 때문에 decoding latency가 크다는 진단에서, post-causal entropy modeling으로 backbone과 probability prediction을 분리한 PACE를 제안합니다. 한 모델이 multiple performance-latency trade-off에 적응 가능 — AD/로봇 측 large-scale LiDAR pipeline의 inference cost 측면에 직접 영향이에요.",
    "2605.01365": "Open-vocabulary 3D affordance detection에서 MLLM token이 sequential dependency만 잡고 spatial neighborhood를 못 잡는 문제를 voxel-token fusion으로 풀었어요. 'autoregressive token이 spatially impoverished'라는 진단이 분명한 결인데, 향후 3D affordance 라인의 표준 보강책으로 자리잡을 가능성이 있습니다.",
    "2605.01450": "ToFu/TEMPEH류 multi-view face mesh 학습이 'registered training data'에 의존하는 문제를 풀려고, registration 없이 dense semantic correspondence를 학습하는 MOCHI를 제안. multi-view face capture 라인의 self-supervision 결로 의미 — 향후 medical/avatar 측면 적용 가능성.",
    "2605.01466": "Sparse point cloud → image plane projection이 'cross-modal entropy collapse' 일으킨다는 진단에서, hard projection을 differentiable Gaussian splatting으로 대체. 'point cloud completion에서 multi-modal connection이 왜 약한가'를 처음 이론적으로 정리한 자리예요.",
    "2605.01498": "2D Visual Query Localization을 3D 공간으로 확장한 첫 결 — 3DVQL benchmark(2002 시퀀스, 170K frame)와 method baseline 동시 제안. Embodied AI · AR 라인의 'query하면 3D 위치 반환' 표준 task 후보 자리예요.",
    "2605.01736": "3D Gaussian + language description을 한 단위로 묶은 multi-scale GLMap. ObjectNav/InstNav/SQA에서 zero-shot 작동하고, 'large model interface가 native하게 붙는 3DGS map'이라는 점이 paradigm 측면 의미 강해요. Embodied navigation에서 '3DGS as memory substrate'가 두 번째 표면화한 자리.",
    "2605.01746": "Lateral face image(측면 사진) 한 장으로 3DMM regression — orthodontics 측 cephalometric landmark 자동화로 X-ray 노출 줄이는 임상 응용. ROI 주변부지만 3DMM 학습 paradigm 측면 'profile-specific' subcomponent 추가가 흥미.",
    "2605.01852": "Dual-Pixel sensor의 defocus blur로 SfM 측 scale ambiguity를 해소하는 첫 결. 'reference object 없이도 절대 scale 복원' 가능 — 3D reconstruction 라인의 calibration overhead 줄이는 새 substrate예요.",
    "2605.01995": "AD에서 3DGS로 'rare safety scenario synthetic editing' 가능성을 industrial fidelity 기준으로 평가한 결. 어제 GSDrive(driving sim용 3DGS)와 같은 'AD evaluation infra' 흐름의 직접 후속이에요.",
    "2605.02098": "Spherical crop 대신 Gaussian/exponential/linear crop을 비교한 분석 paper — large-scale 3D scene processing의 default heuristic을 다시 보는 자리. 결과로 'Gaussian이 더 나은 context preservation'을 정량 보고.",
    "2605.02201": "Airborne LiDAR forest inventory에서 sparse + noisy 점군을 voxel-CNN U-Net으로 super-resolve. 응용 측 결이지만 'point cloud SR + denoising 동시 처리'라는 substrate 측면 일반화 가능성이 있어요.",
    "2605.02357": "Point cloud feature aggregation에서 channel-level relation을 attentive aggregation에 활용 + neighborhood-homogeneity constraint 추가. 'coarse-grained metric loses info in deep layer'라는 진단이 깔끔한 결입니다.",
    "2605.02784": "Human Mesh Recovery + 3DGS avatar를 closed loop로 묶은 결. ViT-based HMR이 2D view에 overfit하고 GS avatar가 pose-appearance를 분리해서 새 pose 일반화 못 하는 문제를 동시 풀어요. Avatar 라인의 'recovery + render'가 한 stack에 들어온 자리.",
    "2605.02759": "Pedestrian motion forecasting을 social-aware GNN으로 직접 factor graph optimization에 통합한 dynamic SLAM. 'rigid constant-velocity heuristic 대신 generative GNN prior' — social navigation 라인의 SLAM 표준 후보예요.",
    "2605.00879": "LiDAR for rehabilitation의 종합 survey — 응용 측 결이지만 'LiDAR가 camera/wearable 대비 privacy + comfort 양면에서 유리'한 medical 측 활용 정리. ROI 주변부지만 LiDAR 활용 layer가 한 단계 넓어진 자리.",
    "2605.01232": "3DGS-based imitation learning demo synthesis가 'sampling-based planner로 expert trajectory에서 deviation' 한다는 문제를 'principled approach'로 해결. Contact-rich/shape-sensitive task에서 demo 품질 보존 — IL 데이터 측면 substrate 결이에요.",
    "2605.01340": "회전 mmWave radar로 agricultural UAV 지형 인식. Fixed FoV + LiDAR-targeted method가 농업 환경에서 깨지는 문제를 'rotating mmWave + sparse-data terrain extraction'으로 풀었어요. 응용 측 결이지만 sparse radar terrain 라인 표준 후보.",
    "2605.01773": "FMCW radar의 fundamental measurement noise를 first principle로 모델링 + aided inertial navigation의 reliable estimator 도출. '4D radar 활용의 한계' 자체를 정량화한 분석 paper로 의미가 있어요.",
    "2605.02227": "글로벌 metric SLAM 대신 'pose-aware topological graph of RGB-D keyframes'로 환경 변화 robust하게. CROSS representation은 'data association degrade' 자리에 직접 처방 — long-term autonomy 측면 한 결.",
    "2605.02528": "DRL navigation policy의 environment overfit 문제를 procedural map generator(sparse·maze·graph·WFC) 4종 비교로 정리. 'generator 종류가 generalization에 끼치는 영향'을 처음 systematic하게 cross-evaluate한 자리.",
    "2605.02809": "LiDAR로 teach + radar로 repeat하는 cross-modal Teach-and-Repeat navigation 시스템. Weather degradation·structural change·ephemeral dynamics 3축에 동시 robust한 첫 결로 long-term autonomy 측 의미.",
    # ============== Robot Learning ==============
    "2605.00880": "End-to-end AD(VLA류 + modular 양쪽)이 Transformer backbone에서 동일 vulnerability를 공유한다는 진단에서, gray-box adversarial flow matching으로 imperceptible perturbation을 one-step 생성. 'AD safety' 측면의 첫 cross-paradigm vulnerability 정량화 — VLA가 AD에 깔리는 시점 적절한 timing이에요.",
    "2605.00884": "Onboard aerial guidance 측 dual-rate VLA inference framework. semantic understanding은 느린 rate로, control은 빠른 rate로 분리해 UAV 측 latency 제약 대응. VLA가 AD/UAV deployment에 들어갈 때 latency-aware architecture 표준 후보예요.",
    "2605.01638": "Unified social media deepfake detection benchmark (Omni-Fake) — 응용 측 결이지만 multimodal deepfake 측면 통합 평가 자리가 비어있던 자리에서 의미 있는 baseline.",
    "2605.01666": "Onset-anchored partial HOI event를 supervisory control로 다루는 IMPACT-HOI. Embodied event understanding 라인에서 'partial event + supervisory framework' 첫 정조준 결이에요.",
    "2605.02291": "Game engine synthetic dataset의 sim2real appearance gap을 hybrid approach로 닫는 결. 'sim2real gap이 학습 성능 측면 cap이다'는 진단이 깔끔하고, synthetic data 측 표준 보강책이 될 가능성.",
    "2605.02757": "VLA data 증강을 위해 simulation video를 efficient하게 'realistic' 측으로 transfer하는 결. Sim2Real 측면의 video-level transfer가 VLA infra(어제 LWD·Lucid-XR 흐름) 라인의 한 결로 자연스럽게 들어와요.",
    "2605.01448": "Cross-task generalization을 'atomic skill-action pair'를 중간 표현으로 두고, decompose-then-recompose로 푸는 framework. In-context learning이 low-level trajectory만 줘서 superficial imitation으로 degenerate한다는 진단이 정확하고, skill reasoning 측 paradigm 후보예요.",
    "2605.02223": "Speech inpainting forensics(원본 vs 합성 구분) 데이터셋·메트릭 첫 표준화. ROI 주변부 응용 결.",
    "2605.02667": "Monocular depth metric grounding을 factor graph로 푸는 AnchorD. 'monocular depth이 metric 측 anchor 부재'라는 문제 직접 해결로 SLAM/odometry 측 의미.",
    "2605.02699": "Equivariant neural-augmented object dynamics를 few interaction에서 학습. Manipulation 측 'symmetry-aware dynamics learning'이 sample efficiency 크게 올리는 결로, dexterous 라인 후보.",
    "2605.00963": "Multimodal perception + language grounding + control의 ablation study — 응용 측 결이지만 HRI 라인의 ablation 자리 첫 정리.",
    "2605.01191": "VLA에 'sentinel' module을 붙여 실시간 execution status를 모니터링하고, 필요 시에만 dynamic reasoning + error recovery 트리거. 모든 step에서 reasoning 안 돌리니까 latency overhead가 적고, 44 task × 2.6M transition 학습 데이터를 자동 생성하는 SECL pipeline까지 같이 — 'metacognitive VLA'라는 새 layer가 표면화한 자리예요.",
    "2605.01194": "VLA에 'cognitive clutch' 측 uncertainty-based test-time compute를 도입. Reflexive 실행에서 deliberation phase로 dynamic transition + Relative Action Critic으로 candidate action 비교 — 'absolute value estimation의 instability'를 'relative pairwise comparison'으로 우회한 게 핵심. VLA에 '느린 사고' layer를 처음으로 systematic하게 도입한 결입니다.",
    "2605.01195": "Imitation learning policy의 'safe set'을 Lipschitz Q-value로 학습 — 'visibility·recognizability·graspability' 3 short-term criterion으로 long-term safety score 매핑. flow-matching·diffusion policy의 compounding drift 문제를 'safe set 안에서만 deploy'로 처방하는 새 IL safety 표준 후보.",
    "2605.01201": "IL policy의 'execution guarantee'를 정의 — policy-agnostic safety measure로 'minor run-time change에 대해서도 maximum task success 보장' 영역을 식별. 'Task success only' 패러다임에 'safety 의무 + run-time robustness' layer를 처음 systematic하게 추가한 결이에요.",
    "2605.01227": "Quadrupedal locomotion에 intrinsic dynamics head를 도입 — 'dynamics-aware control'이 별도 model 없이 single network 안에 통합. Locomotion 측 architecture 결.",
    "2605.01289": "Underactuated blimp의 center-of-mass recovery를 bi-level RL로 — 'ill-conditioned underactuated control' 측 흥미로운 결이지만 ROI 주변부.",
    "2605.01427": "Humanoid 측 task-agnostic proprioception-only whole-body wrench estimation — 'sixth sense'라는 metaphor로 force sensing 없이 whole-body force estimate. Humanoid 라인 sensing 측 결.",
    "2605.01434": "Dexterous hand의 sensor readout을 shift-register multiplexing으로 high-speed scalable화 — hardware 측 결이지만 dexterous 라인 sensor latency 측 표준 보강책 후보.",
    "2605.01518": "Humanoid 측 visual object goal pushing with force-adaptive control. 'visual goal + force adaptation' 결합으로 contact-rich pushing 처리 — humanoid manipulation 라인의 한 결.",
    "2605.01529": "End-user demonstration의 'good-in-bad' 부분을 sift through하는 IL 결. 'demonstration quality variance'가 학습 성능에 끼치는 영향 직접 처방 — 데이터 측 결로 의미.",
    "2605.01544": "IL의 data quality measurement metric 자체를 정의 + 효율 측정. 'demo quality measurement'가 정량화 안 되어 있던 자리에서 첫 표준 후보예요.",
    "2605.01581": "3D diffusion policy의 frequency-aware right-sizing — 'diffusion policy가 task에 따라 over/under-parameterized'라는 진단으로 architecture를 task-specific 조정. visuomotor diffusion 측면 efficiency 결.",
    "2605.01772": "VLA 측 long-horizon task에서 anticipation model이 future subgoal을 adaptive하게 recursively 생성. 'fixed granularity subtask'가 varying complexity에 안 맞는다는 진단이 정확하고, hierarchical VLA 측 표준 후보. 어제 IVLR(95.5%)과 같은 'long-horizon VLA' 라인의 한 결.",
    "2605.01948": "Phone 한 대로 VLA 측 teleoperation system 구현 — hardware-agnostic + low-cost로 'VLA data collection scaling'의 큰 병목을 푸는 결. 어제 LWD/Lucid-XR과 같은 'VLA infra race' 흐름의 직접 후속.",
    "2605.02037": "Soft grasping + low-cost architecture를 VLA-integrated 형태로. 'VLA hardware'가 expensive system에 묶여 있다는 진단을 직접 처방 — MolmoAct2의 'open data + low-cost platform' 라인과 timing 일치.",
    "2605.02135": "Heterogeneous object manipulation을 multi-primitive로 — desk organization이라는 일상 task가 'manipulating heterogeneous'의 첫 정조준 자리. 응용 측 결이지만 task definition이 흥미.",
    "2605.02147": "Sampling-based MPC(MPPI/CEM)의 'mode-averaging' 문제를 entropy-regularized optimal transport로 푼 OT-MPC. 'information-theoretic objective가 control geometry를 무시한다'는 진단이 정확하고, Sinkhorn으로 closed-form gradient-free update — robotic control 라인의 새 substrate 후보예요.",
    "2605.02306": "Bayesian filtering을 natural gradient로 — geometry-aware 측 dynamical system filter. Filter 측 결.",
    "2605.02347": "Visuo-haptic shape completion + grasping을 simultaneously — 'shape complete first, then grasp' 분리에서 동시 처리로. Manipulation 측 결.",
    "2605.02361": "Stochastic nonlinear system의 Signal Temporal Logic spec 만족 motion planning을 feedback formulation으로 — formal method 측 결로 safety 라인과도 연결.",
    "2605.02370": "Hook 기반 aerial transportation 측 robust adaptive predictive control — UAV 응용 결.",
    "2605.02410": "Impedance-driven anisotropic guidance field로 shared autonomy assist. HRI/teleoperation 측 결.",
    "2605.02487": "Dynamic environment의 visibility-aware mobile grasping. Grasping 측 새 substrate.",
    "2605.02513": "Multi-terrain exoskeleton의 adaptive gait generation을 constrained kernelized movement primitive로. 응용 측 결.",
    "2605.02529": "Sim-to-real RL control의 robustness evaluation framework. 'sim2real evaluation'이 dispersed인 자리에서 표준 후보.",
    "2605.02600": "LLM/VLM을 직접 controller가 아닌 'cost designer'로 두고 MPPI 측 cost function을 합성, 동시에 VLM이 mass·friction 같은 physical parameter prior를 주고 online system identification으로 refine. 'LLM+symbolic+adaptive control' 모듈 framework로, contact-rich manipulation 측면 LLM 활용의 새 layer.",
    "2605.02739": "Dual-system VLA에서 VLM backbone을 매 step 호출하는 cost를 'feature delta prediction'으로 회피. 4 LIBERO suite + 24 RoboCasa kitchen + ALOHA에서 95-100% 성능 retention + 1.65-1.73× speedup. GR00T-N1.6과 π0.5 두 architecture에 동시 적용 — 'VLA inference 비용'의 표준 보강책 후보 자리예요.",
    "2605.02881": "Frontier VLA가 closed model이고 open-weight는 expensive hardware에 묶여 있고 reasoning policy는 latency overhead가 크다는 5가지 진단을 동시 처방한 fully open VLA. MolmoER VLM(3.3M sample) + 720h bimanual teleoperation dataset + OpenFAST action tokenizer까지 묶음. '실제 deployment' 기준 fully open VLA의 표준 후보 자리예요.",
    "2605.01096": "Mini Wheelbot에 Infoprop Dyna로 'minute 단위 racing 학습' — sample-efficient model-based RL 측면 결로 robot RL 라인의 한 결.",
    "2605.01170": "Skin-like conformal sensor의 real-time shape mapping — sensor hardware 측 결로 dexterous/HRI 라인 sensing 측 표준 후보.",
    "2605.01663": "Offline RL 측 expressive flow policy + distributional critic의 high cost 문제를 'single flow iteration + single Gaussian sample'로 단순화한 FAN. SOTA 유지하면서 training/inference cost 크게 줄임 — efficient offline RL 측 직접 처방 결이에요.",
    "2605.01978": "Control Lyapunov Function-guided RL의 stability 측 정량 분석. Formal method × RL 측 결.",
    "2605.02538": "Robotic affection 측 AI-based haptic interaction 가능성 — 응용 측 결이지만 'social robot' 라인의 결.",
    # ============== Autonomous Driving ==============
    "2605.00907": "LLM/MLLM이 transportation task(regulation QA·traffic management·engineering review·driving scene reasoning)에 활용되는데 이를 'role-task-knowledge taxonomy'로 837 item 묶어 첫 표준 평가 — text·image·point cloud 다루는 multimodal AD 측 진단 평가 표준의 첫 결. 어제 NAVSIM/Bench2Drive correlation paper와 같은 'AD evaluation methodology' 흐름의 직접 후속이에요.",
    "2605.01081": "Adverse condition 하에서 AD perception을 simulated-and-real data augmentation으로 향상 — sim2real 측면 'WILD SAM'이라는 통합 substrate.",
    "2605.01277": "CNN 기반 multi-in-multi-out 구조로 efficient spatiotemporal prediction. AD/perception 측 결.",
    "2605.01393": "Motion forecasting의 'opaque latent query → latent collapse' 문제를 'motion bank(physically realizable trajectory의 contrastive embedding space)'에서 explicit retrieval로 풀어요. Anchor Retrieval Layer + Dual-Level Gated Cross-Attention + Straight-Through Gumbel-Softmax로 differentiable end-to-end 유지 — 'interpretable motion forecasting' 측면의 첫 systematic 결.",
    "2605.01478": "LiDAR-only HD Map construction with intensity enhancement(online knowledge distillation). HD Map 측 효율 결.",
    "2605.01517": "Vector animation의 rendering-aware sparse state modeling — AD 측면보단 vector graphic 결.",
    "2605.01888": "V2X cooperative perception의 channel-aware adaptive feature fusion(AFFormer). V2X 측 결.",
    "2605.01901": "Behavior-grounded lane representation을 multi-task traffic digital twin에 적용. AD digital twin 측 결.",
    "2605.01916": "Infrared·Visible image fusion의 intrinsic evolving auxiliary prior 활용. 응용 결이지만 multimodal fusion paradigm 측면 의미.",
    "2605.01924": "2D + 3D 객체를 multi-camera로 simultaneously detect하는 SimPB++. AD 측 detection 표준 후보.",
    "2605.02284": "Open-set object detection을 negative-aware framework로 — 'unknown object 처리' 표준 보강책.",
    "2605.02563": "Embedded driver monitoring system 측 multi-task NN low-latency 구현. 응용 결.",
    "2605.02762": "Map prior가 mapping과 planning을 공통으로 encoding하는 unified encoder. 'map과 plan을 분리하지 말자' 측 paradigm 결.",
    "2605.01949": "Sonar-GPS fusion으로 turbid shallow water의 seabed mapping — Autonomous Surface Vehicle 측 흥미로운 응용.",
    "2605.01485": "Cut-in gap acceptance가 autonomous vehicle vs human driver에 따라 어떻게 다른지 Waymo data로 분석 — 'AV-human interaction' 측면 정량 결로 의미.",
    "2605.01516": "Dynamics distillation으로 efficient + transferable control learning. Knowledge distillation × control 측 결.",
    "2605.01731": "Vehicle platoon의 lateral string stability를 formal한 정의 + analysis — formal method 측 platooning 결.",
    "2605.01860": "Belief space의 trajectory tree optimization — model predictive control × belief planning 측 결.",
    "2605.01996": "Multi-agent motion planning의 kinematically feasible 최적화. 응용 측 결.",
    "2605.02301": "UAV의 self-attention + goal-aware anchor planner SAGA — UAV planning 측 결.",
    "2605.02716": "Trailer-truck transport 측 sensor fusion + motion planning parking assistance. 응용 결.",
    "2605.01787": "UAV의 zero-shot safe + time-efficient navigation을 potential-based reward shaping + control barrier function으로. 응용 결이지만 safety × RL × UAV 결합 결.",
    # ============== Foundation Models ==============
    "2605.00891": "이미지·비디오의 'any segmentation'을 단일 모델로 — SAM 라인의 unified extension. 응용 측 결이지만 segmentation foundation 측 표준 후보.",
    "2605.00893": "Histopathology image captioning의 hallucination을 retrieval-guided generation으로 mitigate. 'safer captioning' 측면 응용 결.",
    "2605.00906": "Generalized Category Discovery의 domain shift 측면을 vision → vision-language model로 확장. GCD × VLM 측면 결.",
    "2605.01024": "MLLM의 emotion recognition 측 'Video Contribution Collapse(VCC)' 현상 발견 + Conflict-aware Head-level Attention Steering(CHASE)로 처방. 'modality preference + token redundancy'가 video evidence를 무력화한다는 진단이 정확하고, inference-time intervention만으로 retraining 없이 fix.",
    "2605.01266": "NSCLC 측 zero-shot segmentation VLM의 prompt alignment를 clinical factor 기준으로 분석. 응용 측 결.",
    "2605.01284": "RAG의 pixel-level visual attribution을 'chain of evidence' 형태로 — iterative retrieval에서 어떤 픽셀이 어떤 결정에 기여했는지 추적. Visual RAG 측면 interpretability 결.",
    "2605.01324": "Video MLLM의 'perceptual shortcut' 문제를 causal-inspired debiasing으로 — 'shortcut feature' 측 정조준 결.",
    "2605.01325": "VLM model selection을 Gromov-Wasserstein distance로 — 'model 사이 거리'를 distribution-level로 정의한 흥미로운 결.",
    "2605.01345": "VLM의 perceptual bandwidth bottleneck(넓은 FoV vs fine detail trade-off)을 sequential Bayesian optimal experimental design으로 형식화. greedy sampling부터 look-ahead planning까지 임의 알고리즘에 적용 가능한 training-free framework — 어제 'active perception VLM' 흐름의 첫 formal foundation이에요.",
    "2605.01391": "Video interaction의 spatio-temporal analysis benchmark VISTA — 응용 측 결.",
    "2605.01496": "SF20K Competition 2025 결과 정리 — survey/competition 결.",
    "2605.01506": "See/Hear/Feel을 한 encoder로 처리하는 OmniEncoder — multimodal foundation 측 통합 결.",
    "2605.01512": "Surveillance video의 rare traffic event를 two-pass zero-shot temporal-spatial grounding. 응용 측 결.",
    "2605.01520": "VLM의 mutual information-guided RL — 'MI guide RL'이라는 새 학습 substrate 결.",
    "2605.01657": "VLM이 정적 초기 frame에 묶이는 video reasoning 측 한계를 'CoT 안에서 frame을 actively interleave'하는 Act2See로 해소. SFT로 얻은 emergent active perception capability이 새 SOTA — 어제 active perception 흐름의 핵심 결이에요. 같은 저자의 Video Active Perception(VAP)과 같은 paradigm.",
    "2605.01662": "Long-form video QA에서 frame sampling을 'active perception'으로 — text-conditioned video gen model을 prior로 두고 keyframe selection을 information acquisition으로 본 VAP. EgoSchema·NExT-QA·ActivityNet-QA·IntentQA·CLEVRER 5 bench에서 SOTA + frame efficiency 5.6× — 'active perception VLM'이라는 paradigm의 직접 instantiation이에요.",
    "2605.01733": "VLM hallucination을 training-free caption steering으로 — inference-time intervention 측 결.",
    "2605.01779": "CT clinical reporting의 agentic workflow MedScribe — 응용 측 결.",
    "2605.01882": "Dense chart의 fine-grained visual focus-driven reasoning — Chart-FR1. 응용 결.",
    "2605.01911": "Surgical VQA에서 VLM이 정말 image를 보는지 SurgCheck로 진단 — 'shortcut vs real visual grounding' 측면 결.",
    "2605.01925": "CAD design 측 LLM 데이터셋·framework CADFS — 응용 결.",
    "2605.02130": "'Where things are' vs 'what they are for'의 spatial-functional intelligence benchmarking. VLM의 functional understanding 측면 결.",
    "2605.02206": "Multimodal machine unlearning의 metric unreliability 분석 — 'unlearning이 정말 일어났는가' 측 진단 결.",
    "2605.02376": "Medical report 측 graph-augmented topological internalization with dual-stream classifier. 응용 결.",
    "2605.02378": "Multimodal in-context learning의 inductive-deductive reasoning 강화. ICL 측 결.",
    "2605.02604": "Source-free domain adaptation을 source model 없이 from scratch로 — 'do we really need source model' 흐름의 결.",
    "2605.02623": "'Generalized moment retrieval' 측 benchmark + model — moment retrieval 측면 결.",
    "2605.02630": "GUI grounding의 uncertainty-aware active visual search AutoFocus — Agent × UI 측 결.",
    "2605.02720": "Ophthalmology VLM 측 PubMed-Ophtha open resource — domain-specific data 측 결.",
    "2605.02730": "Visual grounded reasoning 측 perceptual flow network — 응용 결.",
    "2605.02834": "Domain-specific action recognition 측 large-scale dataset VideoNet — 데이터 측 결.",
    "2605.02892": "Personalized image completion 측 album-guided reasoning + retrieval AlbumFill — 응용 결.",
    "2605.00873": "T2V evaluation 측 'implausible scenario' benchmark BRITE — 'reliable + interpretable T2V evaluation' 측면 결.",
    "2605.00876": "Grounded agentic zero-shot evaluation GAZE — VLM의 evaluation tooling 측 결.",
    "2605.00877": "Ocean foundation model용 large-scale multimodal corpus OceanPile — domain-specific 측 결.",
    "2605.01219": "Audio-visual quality assessment 측 multimodal confidence modeling. 응용 결.",
    "2605.01402": "Distributional awareness를 RL로 MLLM에 주입 — 'long-tail imbalance' 측면 결.",
    "2605.01766": "MLLM hallucination을 inference-time relevance propagation으로 mitigate. Hallucination mitigation 측 결.",
    "2605.02525": "Indoor mobile robot 측 VLM-integrated semantic autonomy framework — VLM × robotics 측 결.",
    # ============== Generation ==============
    "2605.00874": "Video generative model의 'adult content' 측면 latent space probing — generation safety 측 결.",
    "2605.00878": "Image defogging의 fourth-order telegraph PDE + physical haze model. 응용 결.",
    "2605.00883": "Face swapping survey + new benchmark — 응용 결.",
    "2605.00902": "Whole-slide foundation model의 image retrieval 측 TCGA validation. 응용 결.",
    "2605.00913": "Imperfect medical data 측 manifold-consistent spatio-temporal network. 응용 결.",
    "2605.01113": "T2I diffusion에서 NSFW generation 방어 'Disciplined Diffusion'. Generation safety 측 결.",
    "2605.01135": "Image editing용 synthetic data with scribble + text — 데이터 측 결.",
    "2605.01185": "Magnitude MR image에서 phase map synthesis를 conditional score diffusion으로. 응용 결.",
    "2605.01220": "Visual implicit autoregressive modeling — autoregressive image gen 측 결.",
    "2605.01296": "Virtual try-on 측 SIFT-based geometric correspondence supervision SIFT-VTON. 응용 결.",
    "2605.01331": "Invertible image hiding 측 zero-shot interpretable steganalysis. 응용 결.",
    "2605.01382": "혈관(vessels) sparse representation learning. 응용 결.",
    "2605.01459": "SRGAN-CKAN: Chebyshev-KAN 기반 super-resolution. SR 측 결.",
    "2605.01468": "Long-tailed learning의 decision boundary-aware generation. Long-tail 측 결.",
    "2605.01479": "Diffusion model watermark을 compressed sensing으로 forgery-resistant — generation IP 측 결.",
    "2605.01480": "MMDiT 측 training-free image editing의 per-category attention routing AttnRouter. Editing 측 결.",
    "2605.01510": "One-step diffusion 기반 lightning-fast subject-driven personalization SwiftPie. Efficiency × generation 결.",
    "2605.01568": "Image enhancement 측 deep stochastic process unification. 응용 결.",
    "2605.01653": "Diffusion 측 'bottlenecked activation control interface' SteeringDiffusion — generation control 측 결.",
    "2605.01725": "Autoregressive video generation의 motion-aware caching. Efficiency × video gen 결.",
    "2605.01743": "Text-to-3D의 manifold-order consistency MOC-3D — 3D gen 측 결.",
    "2605.01761": "T2V model의 jailbreak 방어 측 trajectory-level safety mediation TrajShield. T2V safety 측 결.",
    "2605.01799": "Embodied AI 측 4D world model — monocular video를 임의 novel view로 합성. multi-view paired data scarcity·spatiotemporal consistency·manipulation hallucination 3 challenge를 3D-aware compositional pipeline + adaptive noise injection으로 동시 처방. 'embodied world model이 2D representation에 묶여있다'는 진단이 정확하고, multi-view embodied substrate의 첫 generalist 결이에요.",
    "2605.01815": "Cross-domain adversarial augmentation으로 medical/handwriting GAN 안정화. 응용 결.",
    "2605.01848": "DADD: Disentangled Anatomy-Disease Diffusion으로 ulcerative colitis progression 제어. 응용 결.",
    "2605.01896": "Multimodal world model의 decoupled representation alignment 'divide and conquer'. WM 측 결.",
    "2605.02134": "Predictive latent으로 video generation. Latent video gen 측 결.",
    "2605.02152": "Diffusion image editing의 training-free acceleration via semantic locking SpecEdit. Efficiency × editing 결.",
    "2605.02169": "Privacy-aware multi-camera surveillance 측 heterogeneous model fusion. 응용 결.",
    "2605.02417": "Flow-based image editing의 step-level accurate inversion DirectEdit. Editing 측 결.",
    "2605.02438": "Open-set supervised anomaly detection 측 mixture prototype flow matching. 응용 결.",
    "2605.02464": "Single-image HDR reconstruction 측 exposure-aware one-step generative ExpoCM. 응용 결.",
    "2605.02521": "VA-driven affective image editing MooD. 응용 결.",
    "2605.02567": "AI-generated image detection 측 in-the-wild data automated collection. 응용 결.",
    "2605.02575": "Spatial + angular super-resolution을 self-supervised로 — 응용 결.",
    "2605.02583": "Latent diffusion의 stylistic attribute control. Editing 측 결.",
    "2605.02589": "OCT image에서 representation learning. 응용 결.",
    "2605.02746": "NSCLC histology의 virtual scanning 측 synthetic 데이터 활용 결. 응용 결.",
    "2605.02767": "TOC-SR: image super-resolution 측 task-optimal compact diffusion. SR 측 결.",
    "2605.02772": "Vision Transformer의 linearization을 test-time training으로. Efficiency × ViT 결.",
    "2605.00826": "Text-to-video retrieval의 'performance plateau'를 systematic하게 분석. 응용 결.",
    "2605.00881": "Coupled fourth-order telegraph diffusion으로 grayscale-indicator 활용 image processing. 응용 결.",
    "2605.00925": "Spatial biology와 clinical histology를 'Haiku'로 link — biomedical 응용 결.",
    "2605.00935": "Diffusion model의 'shadow timestep embedding' 통한 information injection — 측면 watermark/forensics 결.",
    "2605.00941": "Flow matching의 'Divergence is Uncertainty' closed-form posterior covariance. 이론 측 결.",
    "2605.00972": "Weather/climate data의 visual analytics workflow. 응용 결.",
    "2605.01098": "Convolutional image filter로 free adversarial example 만드는 결. Adversarial × 효율 결.",
    "2605.01467": "Quaternion nonlinear transform-induced nuclear norm 활용 low-rank tensor completion. 이론 결.",
    "2605.01869": "Parametric memory network로 token communication evolution. Architecture 측 결.",
    "2605.02222": "Orbit-space particle flow matching 기반 generative modeling. 이론 결.",
    "2605.02743": "Sensor-based human activity recognition 측 triple spectral fusion. 응용 결.",
    "2605.00943": "Social robot agent 측 'Agentic and Relationship Intelligence' framework ARIS. HRI 측 결.",
    "2605.01477": "Action Agent: agentic video generation × flow-constrained diffusion. Generation × agent 결.",
    "2605.02710": "Tensegrity crutch의 ground reaction force 향상. Hardware 결.",
    # ============== Efficiency/Systems ==============
    "2605.00887": "Medical image의 contrastive learning에 dynamic sparse attention 도입 — 학습/inference 40% 빠르고 진단 정확도 향상. Sparse attention × contrastive 측면 결.",
    "2605.00888": "Selective correlation knowledge distillation으로 GRF estimation. 응용 결.",
    "2605.00894": "Pathology tumor segmentation 측 nested U-Net + DINO foundation encoder. 응용 결.",
    "2605.00899": "Semantic dataset comparison을 latent diff로 millions scale에 — large-scale dataset analysis 측 결.",
    "2605.01236": "Unified image restoration 측 degradation-aware adaptive context gating. Restoration 측 결.",
    "2605.01330": "ViT의 'outlier decay' 통한 quantization-friendly training (Colinearity Decay). Quantization × ViT 결.",
    "2605.01355": "Cross-architecture knowledge distillation으로 leaf disease classification 효율화. 응용 결.",
    "2605.01563": "Multi-dataset cross-domain knowledge distillation 측 unified medical segmentation. 응용 결.",
    "2605.01742": "ViT의 architecture × token × bitwidth multi-axis joint optimization for semiconductor. 응용 + efficiency 결.",
    "2605.01829": "Brain MRI foundation 측 geometric prior-guided sparse autoencoder GeoSAE. 응용 결.",
    "2605.01858": "Streaming video understanding 측 'Decouple and Cache' KV cache 구성. KV cache × video 측 결.",
    "2605.01929": "Video diffusion model의 data-free LoRA transferability 분석. LoRA × video 결.",
    "2605.02137": "Fusion-Latent for optical reconstruction + flood area segmentation FLoRA. 응용 결.",
    "2605.02184": "Pansharpening 측 region-aware fusion network RAFNet. 응용 결.",
    "2605.02198": "Remote sensing image SR 측 lightweight diffusion SlimDiffSR. 응용 결.",
    "2605.02212": "NTIRE 2026 efficient low-light enhancement challenge 결과. Challenge 결과 결.",
    "2605.02258": "Vision foundation model의 spectral gap을 lightweight adapter로 메우는 SpectraDINO. 응용 결.",
    "2605.02262": "VLM 측 mixed-precision KV cache quantization을 window-level similarity 기반으로 (WindowQuant). KV quant × VLM 측 결.",
    "2605.02275": "LiDAR perception 측 edge DNN의 precision-performance trade-off EdgeLPR. Edge × LiDAR 측 결.",
    "2605.02380": "Real-time crack segmentation 측 uncertainty-guided affine prompting UnGAP. 응용 결.",
    "2605.02444": "Lightweight state-space MoE × cross-scale gating bridge M⁴Fuse. SSM × MoE 측 결.",
    "2605.02614": "Prostate pathology 측 long-term archived sample 활용 end-to-end model validation. 응용 결.",
    "2605.02616": "Salient object detection 측 SAMv2 기반 adapter-guided global-local feature decoding. 응용 결.",
    "2605.02641": "DiT-MoE 활용 unified multimodal model Mamoda2.5. MoE × DiT × multimodal 측 결.",
    "2605.02764": "Semantic segmentation 측 'focus on hard regions' efficient FoR-Net. 응용 결.",
    "2605.02794": "Edge-efficient image restoration 측 transformer → SSM distillation. SSM × distillation 결.",
    "2605.02814": "Identity-structure asymmetric conditioning으로 reference-aware face restoration IConFace. 응용 결.",
    "2605.02849": "Ultra-low-bit-rate video compression 측 conditional controlled diffusion + active sampling. Efficiency × video gen 결.",
    "2605.02866": "Rural road extraction 측 Laplacian frequency interaction network. 응용 결.",
    "2605.00905": "Diagram QA 측 reasoning-level attribution review framework DIAGRAMS. 응용 결.",
    "2605.01238": "Sensor-based momentary engagement assessment dataset EduGage. 데이터 측 결.",
    "2605.01409": "Health video의 interactive multi-turn retrieval. 응용 결.",
    "2605.01548": "ECG biometrics 측 reproducible benchmarking framework ECG-biometrics-bench. 응용 결.",
    "2605.01935": "Vision Mamba의 algorithm-hardware co-design 측 FPGA inference ViM-Q. Hardware × SSM 결.",
    "2605.02862": "Robotic navigation 측 semantic risk-aware heuristic planning. Navigation × safety 결.",
    "2605.01928": "Non-differentiable network를 optimal transport로 학습. 이론 측 결.",
    # ============== Embodied AI ==============
    "2605.01668": "Procedural activity video의 dense temporal annotation을 'correction-driven' framework로 — uncertainty-aware boundary scribble + cost-aware query planning + structured propagation으로 future human-machine collaboration 개선. Embodied annotation 측 결.",
    "2605.01700": "Zero-shot ObjectNav에서 episodic observation을 lifelong하게 누적하는 RAG framework. Topo-polar trajectory representation으로 spatial layout + semantic context 압축, hierarchical chunking + coarse-to-fine retrieval. Internet-scale text가 아닌 'embodied 3D experience'를 reasoning에 직접 주입한 결로 paradigm 측면 의미.",
    "2605.02054": "Visual pose estimation 측 dual quaternion 기반 6-DOF tracking + observability analysis. P_n_P solver의 noise·outlier·measurement dropout 한계를 동시 처방.",
    "2605.01371": "MLLM-driven UAV agent 측 search and rescue 첫 표준 benchmark — Unreal Engine 5 + AirSim + GIS 기반 4 high-fidelity environment. UAV × MLLM agent 측면 evaluation 표준 후보.",
    "2605.02192": "Robot navigation DRL의 'collision = entire episode reset' 관행에 정면 도전. Multi-Collision reset Budget(MCB)으로 local termination과 global reset을 분리 — agent가 같은 episode 안에서 어려운 obstacle config을 retry. Early-stage exploration 가속 + success rate/efficiency 향상 — methodology 측 첫 정조준 결이에요.",
    # ============== Safety/Alignment ==============
    "2605.00886": "Selective attention으로 robust infrared small target detection. 응용 결.",
    "2605.00904": "Transformer fluence map prediction의 clinical perturbation robustness. 응용 결.",
    "2605.00911": "OCR robustness 측 RAG benchmark — 'good OCR is not enough' 측면 결.",
    "2605.01217": "Reversible privacy defense for face recognition 측 asymmetric invertible threat. Face privacy × adversarial 결.",
    "2605.01283": "Plant leaf disease 측 strong pre-trained base model. 응용 결.",
    "2605.01346": "CHASE: ambiguity-aware selective prediction 측 competing hypotheses. Selective prediction 측 결.",
    "2605.01483": "Industrial robot 측 VQA 측 결. 응용 결.",
    "2605.01519": "Hybrid convolution + attention stochastic 측 certified vs empirical adversarial robustness 비교. 이론 측 결.",
    "2605.01552": "Single-image motion blur에서 robust fundamental matrix estimation. 응용 결.",
    "2605.01659": "Self-supervised RL 기반 video summarization TRIMMER. 응용 결.",
    "2605.01718": "Dual-branch robust unlearnable example. Privacy × adversarial 결.",
    "2605.01720": "25개 sign language 측 SignVerse-2M 데이터셋 — 응용 결.",
    "2605.01741": "3D dental CBCT 측 adaptive texture-aware masking SSL. 응용 결.",
    "2605.01759": "PointCSP: point cloud SSL 측 cross-sample semantic propagation + stability preservation. 응용 결.",
    "2605.01876": "Markerless GRF estimation 측 multimodal benchmark BadmintonGRF. 데이터 결.",
    "2605.02126": "Ultrasound VLM의 contrastive alignment. 응용 결.",
    "2605.02207": "Resource-constrained pneumonia screening 측 multimodal learning MultiSense-Pneumo. 응용 결.",
    "2605.02288": "Protocol-grounded 3D layout generation을 lab safety constraint 기준으로 — household scene gen이 functional semantics를 무시한다는 진단을 '실험실'에서 정조준. LabForge → LabGen → LabTouchstone 3 component로 'safe + executable lab simulator'의 첫 표준 후보. 자동화 실험실 시대의 sim infra 라인.",
    "2605.02439": "Anomaly-preference image generation 측 결. 응용 결.",
    "2605.02580": "Open-set panoptic segmentation 측 hyperbolic embedding Hyp2Former. 응용 결.",
    "2605.02586": "Source-free cross-subject fMRI decoding StableMind. 응용 결.",
    "2605.02638": "Cross-view referring 측 view-aware cross-modal semantic ViewSAM. 응용 결.",
    "2605.02714": "Volumetric + planar imaging 통합 ophthalmology foundation OphMAE. 응용 결.",
    "2605.02752": "Text-guided class-agnostic counting의 semantic grounding 'does it really count' 진단. 응용 결.",
    "2605.00869": "WiFi fall detection의 cross-domain robustness. 응용 결.",
    "2605.00872": "Fetal hemodynamics 측 maternal hypertension multi-view hierarchical learning. 응용 결.",
    "2605.00897": "Semantic communication protocol SPAT. 응용 결.",
    "2605.00923": "Cranial synthetic CT generation 측 multitask learning. 응용 결.",
    "2605.01063": "OOD detection의 angle-adaptive universal scorer GEODE. OOD detection 측 결.",
    "2605.01298": "Learning-free clean label backdoor attack 'Checkerboard'. Backdoor 측 결.",
    "2605.02007": "CAM 기반 explainability method 비교 framework. 응용 결.",
    "2605.02544": "Dual-classifier GBDT pipeline으로 'human-like routine error' vs 'high-risk non-human misclass'를 분리, post-hoc safety 처방. ISIC 2018에서 dangerous error -34.1%, SICAPv2 -12.57% — retraining 없이 safety가 substantially 개선된다는 결로 'post-hoc safety' 라인의 표준 후보.",
    "2605.02708": "Robot control 측 temporally consistent 6D pose estimation. 응용 결.",
    "2605.01051": "Temporal logic 측 value function — optimal policy + safety filter. Formal × RL 측 결.",
    "2605.01069": "Deformable object manipulation 측 horizon-agnostic neural operator 기반 online safety filter. Manipulation × safety 결.",
    "2605.01432": "UAV 측 evidence-based landing site selection + vision-based landing. UAV × safety 응용 결.",
    "2605.01501": "Distributed area partitioning + base station situation awareness algorithm. 응용 결.",
    "2605.02537": "Indoor scene generation 측 zone-graph paradigm으로 'spatial semantics orchestration' Orchestrating Spatial Semantics. 응용 결.",
}


def html_escape(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;").replace("'", "&#39;"))


def auto_summary(p):
    """Fallback summary for papers without curated commentary."""
    title = p.get("title", "")
    abs_ = p.get("abstract", "")
    first_sent = abs_.split(". ")[0][:200]
    return f"{first_sent}. (자동 요약 — 본문 정독 권장)"


def badge_html(badge):
    if badge == "CV":
        return '<span class="badge badge-cv">CV</span>'
    elif badge == "RO":
        return '<span class="badge badge-ro">RO</span>'
    elif badge == "CV/RO":
        return '<span class="badge badge-cvro">CV/RO</span>'
    return f'<span class="badge">{html_escape(badge)}</span>'


def render_paper(p):
    aid = p["arxiv_id"]
    title = html_escape(p["title"])
    badge = badge_html(p["badge"])
    author = html_escape(p.get("first_author", "")) or "(unknown)"
    summary = PAPER_SUMMARIES.get(aid) or auto_summary(p)
    summary = html_escape(summary).replace("&#39;", "'")
    # cbadge default = nocode
    cbadge = '<span class="cbadge cbadge-nocode">[📦 code ✗]</span>'
    return (
        f'<div class="paper"><div class="paper-line1">📄 '
        f'<a href="https://arxiv.org/abs/{aid}" target="_blank" rel="noopener">'
        f'<strong>{title}</strong></a> {badge} {cbadge}</div>'
        f'<div class="paper-authors">👥 {author} et al.</div>'
        f'<p>{summary}</p></div>'
    )


# ----- Header CSS / shell -----
HEAD = '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>arXiv Daily Briefing — 2026-05-05</title>
<style>*,*::before,*::after{box-sizing:border-box}
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
@media (max-width:640px){.container{padding:24px 20px}h1{font-size:23px}h2{font-size:19px}body{padding:16px 8px}}</style>
</head>
<body>
<div class="container">
<a href="https://gisbi-kim.github.io/arxiv-daily-summary/" class="home-btn home-btn-top">← 전체 목록으로</a>
<h1>📄 arXiv Daily Briefing — 2026-05-05 (화)</h1>
<div class="meta">
<div><strong>시야:</strong> 주간 2026-04-29 ~ 2026-05-05 · 오늘 배치 cs.CV/new + cs.RO/new (Tuesday 5/5 listing)</div>
<div><strong>소스:</strong> arxiv.org /list/cs.CV/new · /list/cs.RO/new (stdlib 파서 경유)</div>
<div><strong>주간 규모:</strong> cs.CV 631편 · cs.RO 205편 (union 760편 후보)</div>
<div><strong>오늘 /new:</strong> cs.CV 390 + cs.RO 132 → 522 candidates → 329 dedupe → 261편 8개 ROI 버킷 선정</div>
<div><strong>델타 기준:</strong> 7일 전 동급 pastweek 스냅샷(2026-04-28 — 같은 7일 rolling 단위)과 비교</div>
</div>
'''

# ----- Body sections (manually authored) -----
BODY = '''
<h2>🔭 주간 동향</h2>
<p>이번주 가장 분명한 흐름은 <strong>VLA가 'monitoring·safety·test-time compute'라는 새 layer로 급격히 확장</strong>한 것이에요. 어제까지가 "pixel-free latent world-action"이라는 substrate 측 paradigm shift였다면, 오늘은 그 위에 얹는 운영 layer가 한 번에 표면화한 자리 — <a href="https://arxiv.org/abs/2605.01191">Sentinel-VLA</a>(metacognitive monitoring + on-demand reasoning) + <a href="https://arxiv.org/abs/2605.01194">VLA-ATTC</a>(adaptive test-time compute + Relative Action Critic) + <a href="https://arxiv.org/abs/2605.01195">TAIL-Safe</a>(IL safety set via Lipschitz Q) + <a href="https://arxiv.org/abs/2605.01201">To Do or Not To Do</a>(execution guarantee) + <a href="https://arxiv.org/abs/2605.02739">Latent Bridge</a>(VLM call 50-75% 절감 + 95-100% retention) + <a href="https://arxiv.org/abs/2605.01772">Anticipation-VLA</a>(adaptive subgoal) + <a href="https://arxiv.org/abs/2605.02881">MolmoAct2</a>(fully open VLA) — 한 batch에 7편 이상이 같은 "VLA를 deploy 가능하게 만들기" 결로 누적된 건 단순 burst가 아니에요. 어제 본 "infrastructure race" 예측이 정확히 한 단계 더 구체화된 자리고, 'VLA monitoring/safety/efficiency가 새 표준 column으로 굳는' 분명한 신호입니다.</p>
<p>두 번째로 두드러지는 건 <strong>'Active Perception VLM'이라는 micro-paradigm이 정착 단계로 진입</strong>한 거예요. <a href="https://arxiv.org/abs/2605.01657">Act2See</a>(SFT로 emergent active frame interleaving) + <a href="https://arxiv.org/abs/2605.01662">VAP</a>(같은 저자 그룹의 training-free 5.6× frame efficiency) + <a href="https://arxiv.org/abs/2605.01345">Active Reasoning VLM via S-BOED</a>(sequential Bayesian optimal experimental design)이 한 날 나란히 등장 — 셋 다 "VLM이 frame을 actively select/generate하는 게 video reasoning의 새 substrate"라는 같은 진단. 특히 S-BOED 결이 "active perception을 formal optimization framework로" 묶었다는 점이 paradigm 측면 의미가 강합니다. 어제 IVLR(95.5% long-horizon)·Being-H0.7와 함께 보면 '모델이 stage-by-stage로 시야를 넓히는' 흐름이 VLA·VLM 양쪽에서 동시 표면화 — '한 번에 다 보지 말고 순차적으로 acquire하라'는 메타 paradigm.</p>
<p>한편 <strong>Embodied AI 버킷이 5편으로 한 주 내내 가장 cold한 자리에 머물렀고</strong>(pastweek 15편으로 동률, 어제 3편), 여기서 등장한 <a href="https://arxiv.org/abs/2605.02192">"Do We Really Need Immediate Resets?"</a>가 한 편으로 흐름을 흔들 수 있는 자리예요. "Collision = entire episode reset"이라는 navigation DRL 수십 년 관행에 정면 도전 — Multi-Collision Budget으로 "어려운 obstacle config을 같은 episode 안에서 retry" 가능하게. 단순 응용 결이 아니라 <em>methodology-level convention 흔들기</em>라 향후 navigation RL training framework가 표준 변경될 가능성. 동시에 Generation +6%, Efficiency +15%, Safety -8%, FM -31% — 어제까지 "deployment-heavy 라인(AD+Eff+3D)" 무게중심 이동 결이 한 주 더 단단해진 자리(Eff +15%·FM -31%·Generation +6%로 'VLM 거대화에서 Generation·Efficiency 효율화로').</p>

<h2>📐 CV vs RO 대비</h2>
<p>오늘 분포는 Generation(54)·Robot Learning(44)·Foundation Models(39)·Safety(38)·Efficiency(36)·3D/Scene(23)·AD(22)·Embodied(5) — Generation·RL·FM·Safety 4편 vs 작은 버킷 4편의 단단한 5/3 분리. pastweek 시야에선 CV 631편 / RO 205편(3.1:1)로 CV 우세는 유지인데, RL의 RO 비중 34/44(77%) + Embodied RO 비중 2/5(40%) + AD RO 비중 8/22(36%) — "deployment-heavy 라인은 RO가 주도"하는 한 주 패턴이 오늘도 그대로. CV는 substrate(Generation·Efficiency·FM)·RO는 closed-loop activation이라는 노동 분업이 한 주 내내 안 깨짐.</p>
<div class="contrast">
<p><strong>① 공통으로 뜨는 키워드</strong></p>
<ul>
<li><code>VLA + monitoring/safety</code> — RO(<a href="https://arxiv.org/abs/2605.01191">Sentinel-VLA</a>·<a href="https://arxiv.org/abs/2605.01194">VLA-ATTC</a>·<a href="https://arxiv.org/abs/2605.01195">TAIL-Safe</a>·<a href="https://arxiv.org/abs/2605.01201">To Do or Not</a>·<a href="https://arxiv.org/abs/2605.01069">Online Safety Filter</a>) + CV(<a href="https://arxiv.org/abs/2605.00880">Adversarial Flow Matching on E2E AD</a>) — VLA monitoring/safety 결이 양쪽에서 동시 등장. 어제 "infrastructure race" 흐름의 직접 후속.</li>
<li><code>Active perception</code> — CV(<a href="https://arxiv.org/abs/2605.01657">Act2See</a>·<a href="https://arxiv.org/abs/2605.01662">VAP</a>·<a href="https://arxiv.org/abs/2605.01345">S-BOED VLM</a>) + RO(<a href="https://arxiv.org/abs/2605.02192">MCB Reset</a>·<a href="https://arxiv.org/abs/2605.02487">Visibility-Aware Mobile Grasping</a>) — "한 번에 다 보지 말고 actively acquire"라는 메타가 VLM·로봇 navigation 양쪽에서 동시.</li>
<li><code>3DGS as scene/world substrate</code> — CV(<a href="https://arxiv.org/abs/2605.01736">GLMap</a>·<a href="https://arxiv.org/abs/2605.01995">3DGS in AD synthetic edit</a>·<a href="https://arxiv.org/abs/2605.02784">HumanSplatHMR</a>) + RO(<a href="https://arxiv.org/abs/2605.01232">3DGS demo synthesis for IL</a>) — 4 layer(scene memory + AD edit + avatar + IL demo)에 동시 사용.</li>
</ul>
<p><strong>② CV에만 뜨는 키워드</strong></p>
<ul>
<li><code>medical/clinical imaging</code> — <a href="https://arxiv.org/abs/2605.00893">Histopathology RAG</a>·<a href="https://arxiv.org/abs/2605.01266">NSCLC zero-shot seg</a>·<a href="https://arxiv.org/abs/2605.01911">SurgCheck</a>·<a href="https://arxiv.org/abs/2605.02720">PubMed-Ophtha</a>·<a href="https://arxiv.org/abs/2605.02544">Targeted Error Correction</a> 등 한 날 7+편 — Generation·FM·Safety의 잡음 절반 가까이가 medical imaging 측 응용. 한 주 내내 CV의 'application long tail' 메인 자리.</li>
<li><code>active video reasoning</code> — <a href="https://arxiv.org/abs/2605.01657">Act2See</a>·<a href="https://arxiv.org/abs/2605.01662">VAP</a>·<a href="https://arxiv.org/abs/2605.01345">S-BOED</a> — VLM의 frame selection 측면이 한 날 3편 등장한 micro-burst. Long-form video QA의 '5.6× frame efficiency' 결이 community standard 후보.</li>
<li><code>4D world model + multi-view consistency</code> — <a href="https://arxiv.org/abs/2605.01799">Embody4D</a>·<a href="https://arxiv.org/abs/2605.01896">Decoupled Multimodal WM</a> — 어제 Hamiltonian WM·Being-H0.7 라인이 '4D + multi-view' 측으로 한 단계 확장.</li>
</ul>
<p><strong>③ RO에만 뜨는 키워드</strong></p>
<ul>
<li><code>VLA test-time compute / metacognition</code> — <a href="https://arxiv.org/abs/2605.01191">Sentinel-VLA</a>·<a href="https://arxiv.org/abs/2605.01194">VLA-ATTC</a> — VLA에 'cognitive clutch' 또는 'sentinel module'을 붙여 "느린 사고 선택적 활성화" 측면이 RO 단독 자리. 어제 latent reasoning paradigm의 직접 후속이지만 layer가 분명히 다른 새 결.</li>
<li><code>IL safety verification</code> — <a href="https://arxiv.org/abs/2605.01195">TAIL-Safe</a>·<a href="https://arxiv.org/abs/2605.01201">To Do or Not To Do</a>·<a href="https://arxiv.org/abs/2605.01069">Online Safety Filter</a> — 같은 저자(Riad Ahmed) 결 2편이 한 날 나란히 등장 + 별도 결까지 — IL safety 측 'safe set / execution guarantee' paradigm이 단숨에 표면화한 자리.</li>
<li><code>open VLA + cheap teleoperation infra</code> — <a href="https://arxiv.org/abs/2605.02881">MolmoAct2</a>·<a href="https://arxiv.org/abs/2605.01948">Phone2Act</a>·<a href="https://arxiv.org/abs/2605.02037">VILAS</a> — "frontier VLA가 closed + expensive hardware에 묶여 있다"는 진단을 정조준한 oprn-source 측 결. 어제 LWD(16 dual-arm fleet)와 함께 'VLA infra democratization' 흐름의 한 주차 정점.</li>
<li><code>cross-modal navigation (LiDAR teach + radar repeat)</code> — <a href="https://arxiv.org/abs/2605.02809">LTR²</a>·<a href="https://arxiv.org/abs/2605.01773">4D Radar limit analysis</a> — long-term autonomy 측 sensor robust 라인 RO 단독 자리.</li>
</ul>
<p><strong>④ 같은 단어 다른 맥락</strong></p>
<ul>
<li><code>active perception</code>: CV는 'frame selection/generation'(Act2See·VAP·S-BOED) — 정적 video의 어디를 보느냐 / RO는 'collision retry, visibility-aware grasping'(MCB·Visibility Mobile Grasping) — 물리적 작용 어디에서 시도하느냐. "데이터 acquisition 측 active"와 "action 측 active"는 layer가 정반대.</li>
<li><code>safety</code>: CV는 'medical OOD·post-hoc error correction·hallucination mitigation'(Targeted Error Correction·CHASE·Relevance Propagation) — 인지 측 bias 검출 / RO는 'execution guarantee, safe set, safety filter'(TAIL-Safe·To Do or Not·Online Safety Filter) — 행동 측 architectural guarantee. 어제까지의 '인지 측 vs 행동 측' 분리가 오늘 더 단단해졌어요.</li>
<li><code>VLA</code>: CV에선 'VLA = E2E AD attack surface'(Adversarial Flow Matching) / RO에선 'VLA = monitoring/safety/test-time compute layer'(Sentinel-VLA·VLA-ATTC·MolmoAct2). 같은 단어가 한쪽에선 'attack target', 한쪽에선 'deploy operation' — layer가 정반대인 자리에 동시 존재.</li>
</ul>
</div>
<p>지난주 "RL이라는 한 단어가 5단 layer로 다른 자리에 동시 등장"이라고 본 패턴이 이번주 'VLA'·'safety'·'active'에서 동일 문법으로 반복 — <em>한 단어가 paradigm shift 단계에서 layer 분화를 거치는 게 standard pattern이 됐다</em>는 메타 관찰입니다. 우리 랩이 어떤 키워드를 추적하든, 'layer가 어디인가'를 분리해서 보지 않으면 같은 단어의 다른 결을 한 줄로 묶어 분석하는 substantive vs nominal 매칭이 섞이는 자리예요.</p>

<h2>💡 오늘의 인사이트</h2>
<div class="insight"><h3>VLA paradigm shift 3주차 — 'monitoring + safety + test-time compute' 운영 layer가 한 batch에 표면화</h3><p>어제까지가 "pixel-free latent" substrate 측 paradigm shift였다면, 오늘은 그 위에 얹는 <em>운영 layer</em>가 한 번에 표면화한 자리예요. <a href="https://arxiv.org/abs/2605.01191">Sentinel-VLA</a>(metacognitive on-demand reasoning) + <a href="https://arxiv.org/abs/2605.01194">VLA-ATTC</a>(test-time compute via Relative Action Critic) + <a href="https://arxiv.org/abs/2605.01195">TAIL-Safe</a>(Lipschitz Q safe set) + <a href="https://arxiv.org/abs/2605.01201">To Do or Not To Do</a>(execution guarantee) + <a href="https://arxiv.org/abs/2605.02739">Latent Bridge</a>(VLM call 50-75% 절감) + <a href="https://arxiv.org/abs/2605.01772">Anticipation-VLA</a>(adaptive subgoal) + <a href="https://arxiv.org/abs/2605.02881">MolmoAct2</a>(fully open) — 한 날 7+편이 같은 "VLA를 deploy 가능하게" 결로 누적. 단순 burst가 아니라 <em>"학습 paradigm은 정착 → 운영 layer 표준화"</em> 단계로 community가 진입한 분명한 신호고, 우리 랩이 VLA follow한다면 substrate 결만 보지 말고 monitoring/test-time compute/safety set 3축 분리해서 audit해야 할 시점.</p></div>
<div class="insight"><h3>Active Perception VLM이 'formal framework + emergent capability' 양쪽에서 동시 정착</h3><p><a href="https://arxiv.org/abs/2605.01345">Active Reasoning VLM via S-BOED</a>가 active perception을 sequential Bayesian optimal experimental design으로 <em>formal하게 정의</em>하고, 같은 날 <a href="https://arxiv.org/abs/2605.01657">Act2See</a>(SFT로 emergent active frame interleaving) + <a href="https://arxiv.org/abs/2605.01662">VAP</a>(training-free 5.6× frame efficiency)이 <em>practical instantiation</em>으로 등장 — formal framework + practical method가 한 날 나란히 표면화한 건 paradigm 측면 가장 강한 정착 신호 중 하나예요. 어제까지 "long-horizon VLA"가 IVLR 95.5%로 임계 통과한 자리에서, 오늘은 VLM의 long-form video reasoning이 같은 'sequential acquisition' 메타로 통합되는 자리. 우리 랩이 VLM 측 inference 인프라 굴린다면 active perception 측면 추가가 cost-quality Pareto 측면 즉시 가치.</p></div>
<div class="insight"><h3>Robot Navigation DRL의 'collision = episode end' 수십 년 관행에 첫 정조준 도전</h3><p><a href="https://arxiv.org/abs/2605.02192">Multi-Collision reset Budget</a>이 single collision으로 episode 전체 reset하는 standard convention 자체에 정면 도전 — local termination과 global reset을 분리, 같은 episode 안에서 어려운 obstacle config을 retry. Embodied AI 버킷이 한 주 내내 5-15편으로 cold한 자리에서 한 편이 흐름 흔들 수 있는 케이스인데, methodology-level convention 흔들기라 단순 응용 결이 아니에요. "collision penalty가 exploration을 reverse-block"한다는 진단이 정확하고, 향후 navigation RL training framework가 표준 변경될 가능성. <em>한 편이 paradigm-level 보강책</em>이라는 건 cold bucket에서 자주 일어나지 않는 변화 — 우리 랩이 navigation RL infra 굴린다면 이번 결을 default budget heuristic에 즉시 반영 가치.</p></div>

<h2>🔬 추천 연구주제</h2>
<div class="topic"><h3>VLA Monitoring/TestTime/Safety Atlas — 3축 head-to-head benchmark</h3><p>Sentinel-VLA(monitoring)·VLA-ATTC(test-time compute)·TAIL-Safe(safety set) 3축이 같은 LIBERO·RoboCasa 상에서 head-to-head로 비교된 적이 없어요. 같은 backbone + 같은 task에서 'monitoring overhead vs safety guarantee vs test-time compute Pareto' atlas로 묶으면 향후 6주 안에 community가 합의할 'VLA 운영 layer' 표준 후보 자리. 어제 "infra race" 예측이 정확히 표면화한 자리에서, 비교 paper 1편이 즉시 가치 — 우리 랩이 VLA infra 굴린다면 이번주 sprint 시작 적절.</p></div>
<div class="topic"><h3>Active Perception VLM의 'cost-quality Pareto + formal characterization' 통합</h3><p>S-BOED가 formal framework, Act2See/VAP이 practical instantiation으로 등장한 자리에서 다음 단계는 "S-BOED 측 formal optimum vs Act2See/VAP 측 emergent behavior가 같은 video QA에서 어디까지 align하는가" 측정. EgoSchema·NExT-QA·ActivityNet-QA·IntentQA 4 bench × {S-BOED greedy, S-BOED look-ahead, Act2See SFT, VAP training-free} 4 method × frame budget {1, 4, 16, 64}로 4D Pareto atlas — '활성 perception의 optimal vs heuristic 격차'를 정량화한 첫 결이 곧 community standard. 우리 랩이 VLM 측 frame budget 튜닝 인프라 있다면 즉시 sprint 가치.</p></div>
<div class="topic"><h3>Navigation RL Training Convention Audit — collision/reset budget의 cross-platform Pareto</h3><p>MCB가 "collision = episode reset" convention 자체에 도전한 자리에서 다음 단계는 "어떤 reset budget이 어떤 environment에서 optimal한가" 정량화. Habitat·iGibson·Issac Lab 3 platform × {budget 0(standard)·1·3·∞} × {indoor home·warehouse·outdoor terrain} 3 environment로 cross-Pareto. '단순 응용 결이 아닌 methodology-level convention 변경'이 한 paper로 시작된 자리라, 실증 audit 1편이 곧 default training framework 표준 — 우리 랩이 navigation RL 굴린다면 6주 audit 가치.</p></div>

<h2>📊 오늘의 버킷 현황</h2>
<div class="bucket-line">📦 3D/Scene            : 23편 (CV 14 / RO  7 / CV-RO 2)
🤖 Robot Learning      : 44편 (CV  5 / RO 34 / CV-RO 5)
🚗 Autonomous Driving  : 22편 (CV 13 / RO  8 / CV-RO 1)
🧠 Foundation Models   : 39편 (CV 38 / RO  1 / CV-RO 0)
🎨 Generation          : 54편 (CV 51 / RO  3 / CV-RO 0)
⚡ Efficiency/Systems  : 36편 (CV 33 / RO  2 / CV-RO 1)
🏃 Embodied AI         :  5편 (CV  2 / RO  2 / CV-RO 1)
🛡️ Safety/Alignment    : 38편 (CV 31 / RO  5 / CV-RO 2)</div>
<p>🔥 <span class="hot">TOP3</span>: Generation (54), Robot Learning (44), Foundation Models (39) · ❄️ <span class="cold">BOTTOM2</span>: Autonomous Driving (22), Embodied AI (5). Generation 54편이 단독 1위지만 의료·응용 잡음 ~25편 빼면 substantive ~30편으로 줄여 봐야 정확. RL 44편은 'VLA monitoring/safety/test-time compute'에 dense하게 몰린 게 분명한 결이라 substantive 비중이 한 주 평균 대비 크게 높아요. Embodied AI 5편으로 한 주 내내 가장 cold하지만 그 안에서 MCB 한 편이 paradigm-level 흔들기.</p>
<p>📈 <strong>주간 델타(2026-04-28 → 2026-05-05, 7일 rolling pastweek 단위)</strong>: ⚡ Efficiency/Systems <span class="hot">+15%</span> (40→46), 🎨 Generation <span class="hot">+6%</span> (72→76), 🏃 Embodied AI <span class="cold">0%</span> (15→15), 📦 3D/Scene <span class="cold">-2%</span> (48→47), 🤖 Robot Learning <span class="cold">-6%</span> (64→60), 🛡️ Safety/Alignment <span class="cold">-8%</span> (39→36), 🚗 Autonomous Driving <span class="cold">-16%</span> (32→27), 🧠 Foundation Models <span class="cold">-31%</span> (52→36). <em>가장 분명한 신호는 FM의 -31% cooling이 한 주 더 가속</em> — 어제까지 -64% surge cool에서 추가 수렴(이번주 평균이 한 주 전 평균 대비 더 낮음). 동시에 Efficiency +15%·Generation +6%로 'foundation model 거대화에서 efficient generation infra로' 무게중심 이동이 한 주 더 단단해졌어요.</p>

<h2>📈 벤치마크 SOTA 추이</h2>
<table style="border-collapse:collapse;width:100%;font-size:13.5px;margin:12px 0">
<thead><tr style="background:#f6f8fa;border-bottom:1px solid #d0d7de"><th style="text-align:left;padding:8px">벤치마크</th><th style="text-align:left;padding:8px">메트릭</th><th style="text-align:right;padding:8px">이번주 최고</th><th style="text-align:left;padding:8px;padding-left:14px">논문</th></tr></thead>
<tbody>
<tr style="border-bottom:1px solid #eaeef2"><td style="padding:8px"><strong>LIBERO 4 suites + RoboCasa 24 + ALOHA</strong></td><td style="padding:8px">retention vs full VLM call</td><td style="padding:8px;text-align:right;font-family:ui-monospace,monospace">95-100% / 50-75% call ↓</td><td style="padding:8px;padding-left:14px"><a href="https://arxiv.org/abs/2605.02739">Latent Bridge</a></td></tr>
<tr style="border-bottom:1px solid #eaeef2"><td style="padding:8px"><strong>EgoSchema/NExT-QA/ActivityNet-QA/IntentQA/CLEVRER</strong></td><td style="padding:8px">zero-shot SOTA + frame eff</td><td style="padding:8px;text-align:right;font-family:ui-monospace,monospace">SOTA / 5.6× efficiency</td><td style="padding:8px;padding-left:14px"><a href="https://arxiv.org/abs/2605.01662">VAP</a></td></tr>
<tr style="border-bottom:1px solid #eaeef2"><td style="padding:8px"><strong>BimanualYAM (720h teleop)</strong></td><td style="padding:8px">largest open bimanual data</td><td style="padding:8px;text-align:right;font-family:ui-monospace,monospace">720h ✓</td><td style="padding:8px;padding-left:14px"><a href="https://arxiv.org/abs/2605.02881">MolmoAct2</a></td></tr>
<tr style="border-bottom:1px solid #eaeef2"><td style="padding:8px"><strong>ISIC 2018 (skin lesion)</strong></td><td style="padding:8px">non-human error reduction</td><td style="padding:8px;text-align:right;font-family:ui-monospace,monospace">-34.1%</td><td style="padding:8px;padding-left:14px"><a href="https://arxiv.org/abs/2605.02544">Targeted Error Correction</a></td></tr>
<tr><td style="padding:8px"><strong>navigation DRL (multi-platform)</strong></td><td style="padding:8px">SR/efficiency vs single-collision baseline</td><td style="padding:8px;text-align:right;font-family:ui-monospace,monospace">improves ✓</td><td style="padding:8px;padding-left:14px"><a href="https://arxiv.org/abs/2605.02192">MCB Reset</a></td></tr>
</tbody></table>
<p>5건의 substantive SOTA 보고가 한 batch에 등장 — Latent Bridge의 'VLM call 50-75% ↓ + 95-100% retention'이 가장 paradigm 측 의미 강하고(VLA inference cost의 표준 보강책 후보), VAP의 '5.6× frame efficiency'가 active perception 라인의 첫 정량 기준점, MolmoAct2의 '720h open bimanual'이 community의 open VLA 표준 데이터 후보. 모두 향후 6개월 standard 후보 자리.</p>

<h2>🔀 크로스오버 페어</h2>
<div class="crosspair"><h3>같은 "VLA를 deploy 가능하게", 다른 layer — Sentinel-VLA(RO) vs Adversarial Flow Matching(CV)</h3><p><a href="https://arxiv.org/abs/2605.01191">Sentinel-VLA</a>(RO)이 VLA에 metacognitive sentinel을 붙여 'execution status를 monitoring하고 필요할 때만 reasoning 활성화'하는 <em>operational layer</em>를 정조준하고, 같은 날 <a href="https://arxiv.org/abs/2605.00880">Adversarial Flow Matching</a>(CV)는 E2E AD VLA의 Transformer backbone vulnerability를 imperceptible perturbation으로 exploit하는 <em>attack surface</em>를 정조준. 둘 다 "VLA를 deploy 가능하게"라는 같은 메타에서 출발하지만, Sentinel-VLA는 "deploy 운영 측 monitoring 추가"이고 AFM은 "deploy 측 vulnerability 노출"이라 layer가 정반대. 동시에 굴리면 'monitoring layer가 attack을 어디까지 detect하는가' 측정 가능 — 향후 6주 VLA safety의 가장 분명한 비교 자리예요.</p></div>
<div class="crosspair"><h3>같은 "active perception", 다른 layer — Act2See/VAP(CV) vs MCB Reset(RO)</h3><p><a href="https://arxiv.org/abs/2605.01657">Act2See</a>·<a href="https://arxiv.org/abs/2605.01662">VAP</a>(CV)는 VLM이 video frame을 actively select/generate하는 <em>perception 측 active acquisition</em>을 정조준하고, 같은 날 <a href="https://arxiv.org/abs/2605.02192">MCB Reset</a>(RO)는 navigation agent가 collision 후에도 같은 episode 안에서 retry하는 <em>action 측 active retry</em>를 정조준. 'active'라는 한 단어가 한쪽에선 "정적 video의 어디를 보느냐"·한쪽에선 "물리 action을 어디서 시도하느냐"로 layer가 정반대. 두 layer가 같은 'sequential decision-making' 메타를 공유한다는 점은 community가 향후 'active CV + active RO를 통합한 reasoning loop'를 표준으로 묶을 가능성을 시사 — 우리 랩이 VLA × video 둘 다 follow한다면 통합 audit 시점.</p></div>

<h2>🌟 오늘의 must-read</h2>
<div class="mustread">
<h3>① Sentinel-VLA: A Metacognitive VLA Model with Active Status Monitoring for Dynamic Reasoning and Error Recovery <span class="badge badge-ro">RO</span></h3>
<p><a href="https://arxiv.org/abs/2605.01191">arxiv:2605.01191</a> · 저자 Wenhao Li et al. · abstract 기반</p>
<div class="section-title">핵심 주장</div>
<p>현재 VLA가 reasoning 능력 부족·status monitoring 부재·self-correction 어려움 3축 한계를 동시에 갖고 있다는 진단에서 출발해요. Sentinel-VLA는 VLA에 'sentinel module'을 붙여 실시간 execution status를 monitoring하고, <em>필요할 때만</em> dynamic reasoning 또는 error recovery를 trigger — 모든 step에서 reasoning 안 돌리니 latency overhead가 작고, 동시에 robust decision-making 챙김. 더 의미가 깊은 건 함께 제안한 SECL(Self-Evolving Continual Learning) — VLA가 자기 capability boundary를 식별하고 새 데이터를 자동 수집해 확장. 어제 IVLR(95.5%)·Being-H0.7가 "long-horizon VLA"의 substrate 측 paradigm shift 결이었다면, Sentinel-VLA는 그 위에 얹는 <em>"VLA가 자기 상태를 알고, 자기 데이터를 모은다"</em>는 새 운영 layer를 처음 systematic하게 정조준한 자리예요.</p>
<div class="section-title">방법의 핵심 (직관)</div>
<pre># 기존 VLA: 매 step 같은 reasoning 비용
a_t = vla(obs_t, lang)            # always-on reasoning, expensive

# Sentinel-VLA: 선택적 reasoning + monitoring
status_t = sentinel(obs_t, hist)  # 항상 켜진 가벼운 monitor
if status_t.needs_reasoning():    # initial planning OR error detected
    a_t = vla.deliberate(obs_t, lang, reasoning=True)
    if status_t.is_error:
        a_t = vla.recover(obs_t, lang, error=status_t)
else:
    a_t = vla.reflexive(obs_t, lang)  # 빠른 instinctive policy
# Self-Evolving Continual Learning
if status_t.boundary_detected():  # 능력 한계 인식
    auto_collect_data(task_id)     # 자동 데이터 수집
    schedule_orthogonal_finetune()</pre>
<div class="section-title">핵심 실험 (abstract 기반)</div>
<p>학습 데이터 측면: 44 task × 2.6M+ transition을 자동 생성·annotation pipeline으로 수집. SECL이 capability boundary 식별 + auto data collection 하니, 'VLA가 자기 학습 사이클을 굴린다'는 closed loop가 처음 시연된 자리. Orthogonal Continual Learning으로 catastrophic forgetting도 mitigation — 정량 SR 수치는 abstract엔 약하지만 'paradigm-level 도입 자체'가 매크로 의미.</p>
<div class="section-title">약점·한계</div>
<p>(a) Sentinel module이 'always-on light monitor'라지만 실제 inference cost overhead가 abstract에 정량화 안 됐음 — VLA 측 latency는 critical metric인데 sentinel이 추가 비용 만든 만큼이 비교 baseline 대비 표시 필요. (b) 'Self-Evolving Continual Learning' 측면 SECL이 자동 데이터 수집 후 capability가 "정말 확장됐는가" vs "기존 task에 fit한 데이터로 surface improvement했는가" 구분이 ablation 필수 — auto-collected data 측 quality variance 측 정직한 보고 필요. (c) 44 task가 어떤 분포인지 abstract엔 약함 — manipulation·navigation·long-horizon mix가 어떻게 분포됐는지에 따라 결과 의미가 크게 달라요. (d) Sentinel module 자체의 false-trigger rate(reasoning 안 필요한데 trigger한 비율) 측 정량 결과가 본문 정독 필수 — false-trigger가 높으면 latency 절감 의미 약화.</p>
<div class="section-title">랩 파이프라인 영향</div>
<p>VLA 인프라를 굴리는 랩이라면 즉각 paradigm 검토 후보. 특히 우리 랩이 어제까지 'pixel-free latent WAM'을 follow하기로 했다면, 그 위에 'metacognitive monitoring layer'가 동시에 표면화한 자리라 두 layer를 같이 evaluate해야 정확. Sentinel-VLA의 'on-demand reasoning'은 VLA-ATTC의 'cognitive clutch'와 paradigm 자체가 거의 같은데 layer 결이 달라서, 두 결을 동시 굴리면 'monitor만 vs monitor + ATTC' Pareto 측정 가능. 이번주 sprint로 이 비교가 가장 효율적인 follow-up이에요.</p>
</div>
<div class="mustread">
<h3>② MolmoAct2: Action Reasoning Models for Real-world Deployment <span class="badge badge-ro">RO</span></h3>
<p><a href="https://arxiv.org/abs/2605.02881">arxiv:2605.02881</a> · 저자 Haoquan Fang et al. · abstract 기반</p>
<div class="section-title">핵심 주장</div>
<p>현재 VLA가 deployment 기준 5축에서 동시 부족하다는 진단에서 출발 — (1) frontier 모델은 closed source, (2) open-weight 대안은 expensive hardware tied, (3) reasoning-augmented policy는 latency overhead prohibitive, (4) fine-tuned success rate가 dependable use threshold 미달, (5) 데이터 측 bimanual·affordable platform 데이터 부재. MolmoAct2는 5축을 동시 처방한 fully open VLA: <em>(a) MolmoER VLM backbone</em>(spatial·embodied reasoning 특화, 3.3M sample · specialize-then-rehearse 학습) + <em>(b) 3 dataset 공개</em>(BimanualYAM 720h teleoperated bimanual = 가장 큰 open bimanual data + Franka DROID quality-filtered + SO100/101 subset = 저-중 비용 platform 다양성) + <em>(c) OpenFAST</em>(open-weight·open-data action tokenizer · 5 embodiment 수백만 trajectory). 어제 LWD(16 dual-arm fleet)가 'fleet-scale VLA infra'였다면, MolmoAct2는 'fully open + low-cost platform' 측 보강책으로 community-level democratization의 가장 분명한 결입니다.</p>
<div class="section-title">방법의 핵심 (직관)</div>
<pre># 기존 frontier VLA: 5 closed knob
[ closed source · expensive hardware · slow reasoning · low SR · narrow data ]

# MolmoAct2 stack
MolmoER  = VLM_backbone(corpus=3.3M, recipe="specialize-then-rehearse")
OpenFAST = action_tokenizer(traj=millions, embodiments=5)
data     = BimanualYAM(720h) ∪ Franka_filt ∪ SO100/101_filt
policy   = action_reasoning(MolmoER, OpenFAST, data)
# 모든 component fully open: weight + data + tokenizer</pre>
<div class="section-title">핵심 실험 (abstract 기반)</div>
<p>5축 동시 advance — predecessor MolmoAct 대비 spatial·embodied reasoning 향상(MolmoER), bimanual data scale 720h(이전 SOTA 대비 가장 큼), low-cost platform 적용 가능성(SO100/101 subset), action tokenizer 일반화(5 embodiment). 정량 SR vs frontier closed 모델 비교는 본문 정독 필수지만 'fully open' 자체가 community 측 가치 — 어제 'VLA infra race'가 표면화한 자리에서 democratization 측 strongest 결이에요.</p>
<div class="section-title">약점·한계</div>
<p>(a) BimanualYAM 720h의 task 분포가 abstract엔 약함 — 단순 pick-place 720h vs 다양한 long-horizon 720h는 데이터 측면 의미가 크게 달라요. Task distribution + difficulty histogram 본문 필수. (b) "Specialize-then-rehearse" recipe가 catastrophic forgetting을 어떻게 처리하는지 ablation 필요 — 특히 spatial reasoning과 embodied reasoning이 conflict할 때 trade-off 측 정량 결과. (c) OpenFAST가 "5 embodiment 일반화"를 주장하지만 cross-embodiment transfer 측 정량 결과가 abstract엔 약함 — embodiment-specific action space의 alignment 어떻게 처리했는지 정독 필수. (d) Frontier closed model(예: Gemini-Robotics·GR00T-N1.6)과의 head-to-head SR 비교가 abstract엔 약함 — 'fully open이지만 frontier 대비 X% gap'이 정확히 정량화돼야 community 채택 의미. (e) 720h teleop 데이터의 variance/quality control 측 정직한 보고 필요 — fleet 학습 측 'silent failure'와 같은 risk.</p>
<div class="section-title">랩 파이프라인 영향</div>
<p>VLA 인프라를 굴리는 랩이라면 즉시 baseline 후보 — 특히 '데이터·tokenizer·VLM backbone 셋 다 open'이라 우리 랩 측 customization이 다른 frontier 대비 압도적으로 자유로워요. 어제 LWD의 fleet-scale post-training과 MolmoAct2의 community-level democratization을 같이 보면 'VLA infra가 두 갈래(fleet 측 + community 측)로 동시 정착'하는 자리. 우리가 한 갈래 follow한다면 다른 갈래 audit이 필수 — 이번주 sprint로 MolmoAct2 baseline 위에 Sentinel-VLA monitoring layer 얹어보는 게 가장 효율적인 follow-up. 720h BimanualYAM 데이터는 우리 bimanual 측 학습에 즉시 가치.</p>
</div>

<h2>⚠️ 리스크·한계 필터</h2>
<div class="risk"><h3>Latent Bridge "VLM call 50-75% ↓, 95-100% retention" — feature delta가 underrepresented dynamic regime에서 silent fail 측 의심</h3><p><a href="https://arxiv.org/abs/2605.02739">Latent Bridge</a>의 '95-100% retention with 50-75% VLM call reduction'이 강한 클레임이지만, feature delta prediction은 'temporally redundant feature'에 한정해 잘 작동하는 자리예요. Contact-rich/high-dynamic phase(grasping moment of contact, manipulation의 transition)에서 feature delta가 단숨에 크게 변하는 자리에선 prediction error가 culmulative하게 증가하는 silent failure가 가능. abstract의 'across 4 LIBERO + 24 RoboCasa kitchen + ALOHA'가 평균값으로 95-100%일 가능성이 높고, dynamic phase 측 worst-case retention rate가 본문에서 정직하게 정리돼야 deployment 측면 신뢰성 의미. 또한 'task-agnostic DAgger pipeline'이 정확히 어디까지 일반화되는지(unseen embodiment? unseen task class?)도 정독 필수.</p></div>
<div class="risk"><h3>VAP "5.6× frame efficiency" + 5 bench SOTA — 'training-free' claim의 model dependency 측 의심</h3><p><a href="https://arxiv.org/abs/2605.01662">VAP</a>가 training-free라며 5 bench(EgoSchema·NExT-QA·ActivityNet-QA·IntentQA·CLEVRER)에서 SOTA + 5.6× frame efficiency 클레임 — 강한 결이지만 'training-free'라는 게 'model-agnostic'을 의미하지 않아요. abstract는 GPT-4o·Gemini 1.5 Pro·LLaVA-OV 비교를 언급하는데, VAP의 'lightweight text-conditioned video gen model을 prior로 사용'이 어떤 backbone에서 training-free이고 어떤 backbone에서 fine-tune 필요한지 본문 정독 필수. '5.6× frame efficiency'도 frames per question 측면이라 'reasoning에 진짜 필요한 frame'을 더 많이 보냐 vs '단순히 frame 수를 줄여 비용 절감'이냐 분리 측면 ablation 필요. 또한 EgoSchema/NExT-QA 측 일부 task는 cherry-pick 위험이 있는 자리라 'all 5 bench에서 동시 SOTA'인지 확인 필수.</p></div>
<div class="risk"><h3>MolmoAct2 "fully open" + frontier 비교 누락 측 의심</h3><p><a href="https://arxiv.org/abs/2605.02881">MolmoAct2</a>가 fully open VLA 측 democratization 주장이 강한데, abstract에서 frontier closed model(Gemini-Robotics·GR00T-N1.6·π0.5)과의 head-to-head SR 정량 비교가 약해요. '5축 동시 advance'를 predecessor MolmoAct 대비로만 측정했을 가능성이 있고, frontier 대비 'fully open이지만 X% gap' 측면이 본문에 정확히 명시 안 되면 community 채택의 의미가 추상적이 됩니다. 또한 BimanualYAM 720h data의 task distribution이 narrow하면 (예: 단순 pick-place 위주) "open"의 가치가 약화 — task histogram + difficulty stratified analysis가 본문 필수. fully open 자체는 paradigm 측면 가치 강하지만, '정량 SR 비교 자리에 cherry-pick이 끼어들 수 있다'는 risk 인지하고 정독 필요.</p></div>
<div class="risk"><h3>Sentinel-VLA "auto-collected 2.6M transition" — pseudo-supervision quality 측 의심</h3><p><a href="https://arxiv.org/abs/2605.01191">Sentinel-VLA</a>의 '44 task × 2.6M transition을 자동 생성·annotation'이 SECL의 closed-loop self-evolution 핵심인데, 자동 annotation pipeline 자체의 quality assurance 측 정직한 보고가 abstract엔 약해요. Auto-collected data가 'capability boundary 안에 있는 task만 수집' → 'training data가 이미 풀 수 있는 task로 saturate' → 'evaluation에서 SR 향상은 보이지만 generalization 측면은 정체' 패턴이 흔한 자리. SECL 측 'orthogonal continual learning'이 catastrophic forgetting 방어를 명시적으로 측정해도, 'auto-data가 정말 새 capability를 추가했는가' vs 'surface fit'을 구분하는 ablation이 본문 정독 필수예요.</p></div>
'''

# ----- Generate per-bucket paper sections -----
EMOJI_MAP = {
    "3D/Scene": "📦",
    "Robot Learning": "🤖",
    "Autonomous Driving": "🚗",
    "Foundation Models": "🧠",
    "Generation": "🎨",
    "Efficiency/Systems": "⚡",
    "Embodied AI": "🏃",
    "Safety/Alignment": "🛡️",
}


def render_buckets(d):
    out = ['<h2>📄 논문별 요약</h2>']
    for bname, b in d["buckets"].items():
        emoji = EMOJI_MAP.get(bname, "📄")
        cv = b["cv"]; ro = b["ro"]; cvro = b["cvro"]; total = b["total"]
        out.append(
            f'<h4 class="bucket">{emoji} {html_escape(bname)} '
            f'<span class="count">· {total}편 · CV {cv} / RO {ro} / CV-RO {cvro}</span></h4>'
        )
        for p in b["papers"]:
            out.append(render_paper(p))
    return "\n".join(out)


FOOTER = '''
<h2>🔗 참고 링크</h2>
<ul class="links">
<li><a href="https://arxiv.org/list/cs.CV/new">arxiv.org/list/cs.CV/new</a></li>
<li><a href="https://arxiv.org/list/cs.RO/new">arxiv.org/list/cs.RO/new</a></li>
<li><a href="https://arxiv.org/list/cs.CV/pastweek">cs.CV/pastweek</a> · <a href="https://arxiv.org/list/cs.RO/pastweek">cs.RO/pastweek</a></li>
<li><a href="https://gisbi-kim.github.io/arxiv-daily-summary/">📚 전체 브리핑 아카이브</a></li>
<li><a href="https://gisbi-kim.github.io/arxiv-daily-summary/feed.xml">📡 RSS feed</a></li>
</ul>
<a href="https://gisbi-kim.github.io/arxiv-daily-summary/" class="home-btn home-btn-bottom">🏠 전체 목록으로</a>
<footer>Generated 2026-05-05 · stdlib parser → classify.py → curated commentary · arXiv Daily Briefing</footer>
</div>
</body>
</html>
'''


def main():
    pieces = [HEAD, BODY, render_buckets(CLASSIFIED), FOOTER]
    html = "\n".join(pieces)
    os.makedirs("posts", exist_ok=True)
    with open(f"posts/{DATE}.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote posts/{DATE}.html ({len(html)} chars)")


if __name__ == "__main__":
    main()
