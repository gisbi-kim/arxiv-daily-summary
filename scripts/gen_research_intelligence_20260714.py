#!/usr/bin/env python3
"""Generate the full-text Research Intelligence edition for 2026-07-14."""

from __future__ import annotations

import json
from pathlib import Path

import gen_research_intelligence_20260713 as template


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-07-14"
SLUG = f"{DATE}-research-intelligence"


DATA = {
    "date": DATE,
    "edition": "Research Intelligence",
    "source_prompt": "prompts/instruction_v20260713.md",
    "scope_note": (
        "당일 cs.CV/cs.RO /new 318편을 dedup하고 264편을 ROI로 분류했습니다. Tier A 6편은 공식 arXiv PDF의 본문·표·부록·제한점을 "
        "직접 읽어 작성했습니다. Verified는 논문에서 직접 확인한 사실, Inference는 APRL 관점의 해석입니다."
    ),
    "executive_thesis": (
        "오늘 최고의 논문들은 모델을 더 크게 만드는 대신, 실패가 생기는 경계에 구조를 심습니다. object slot은 장면의 경쟁 단위를, "
        "robot-centric pointmap은 관측 좌표계를, SEAMLiS는 ‘보이지 않는 동안 안전할 수 있는가’를, SensorPerch는 센서의 물리적 위치를, "
        "Stop to Decide는 decision timing을, short-answer VQA 연구는 정답 판정 계약을 바꿉니다. 핵심은 ‘구조가 좋다’가 아니라 "
        "task invariant가 있는 층에만 구조를 주고, 그 구조가 깨지는 조건을 failure taxonomy와 matched control로 증명하는 것입니다."
    ),
    "decision_cards": [
        {
            "title": "판세 1 · Capacity보다 invariant를 먼저 산다",
            "body": (
                "object slot과 robot-frame pointmap의 이득은 parameter 수가 아니라 어떤 정보가 같이 묶이고 어떤 좌표가 고정되는지에서 나옵니다. "
                "새 backbone 전에는 object identity, action frame, viewpoint를 각각 독립 축으로 고정한 matched comparison이 우선입니다."
            ),
            "label": "Decision",
        },
        {
            "title": "판세 2 · Safety state에 visibility와 latency를 넣는다",
            "body": (
                "현재 map이 안전해 보여도 센서가 이동 방향을 보지 않거나 다음 control tick 전에 braking margin을 소진하면 충돌합니다. "
                "FoV, speed, loop rate, sensor relocation time을 물리적 state로 올려야 합니다."
            ),
            "label": "Decision",
        },
        {
            "title": "판세 3 · Error pool을 곧바로 학습 데이터로 믿지 않는다",
            "body": (
                "binary success와 official score는 Near-Miss, No-Grasp, non-arrival, evaluator mismatch를 한 실패로 섞습니다. "
                "실패를 고치기 전에 model error와 measurement error를 분리하는 자동 taxonomy를 먼저 만듭니다."
            ),
            "label": "Decision",
        },
    ],
    "papers": [
        {
            "rank": 1,
            "title": "More Structure, Not More Capacity: Object-Centric Representations for Visuomotor Imitation Learning",
            "arxiv_id": "2607.09825",
            "fit": "visuomotor imitation · object-centric representation · failure diagnosis",
            "status": "Tier A · 공식 PDF 전체 확인",
            "status_quo": (
                "frozen vision encoder를 쓰는 imitation policy에서 성능을 높이려면 더 촘촘한 patch token, 더 긴 temporal window, 더 강한 fusion처럼 "
                "representation capacity를 늘려야 한다는 믿음이 강합니다."
            ),
            "friction": (
                "global feature와 dense grid는 task-relevant object와 배경을 섞고, seen initialization의 공기출현 shortcut을 정책이 쉽게 외웁니다. "
                "binary success만 보면 spatial precision과 object tracking 중 어느 병목이 남았는지도 알 수 없습니다."
            ),
            "hidden_premise": (
                "manipulation의 병목은 정보량 부족보다 patch가 object 단위로 경쟁하도록 강제되지 않은 데 있습니다. 제한된 slot capacity가 오히려 "
                "배경 통계 대신 cube, goal, arm에 표현 예산을 쓰게 할 수 있습니다."
            ),
            "conceptual_move": (
                "196 DINO patches를 camera당 7개의 SPOT object slot으로 압축하고 encoder·policy·goal·rendering을 고정한 held-out-seed probe로 "
                "token 수와 구조의 효과를 분리합니다. 이어 실패를 kinematic event로 자동 분해해 다음 연구 병목을 찾습니다."
            ),
            "mechanism": (
                "두 camera의 frozen DINO ViT-B/16+Slot Attention이 14 slots를 만들고, proprioception·2D goal·action token과 함께 8-layer causal policy가 "
                "10-step action chunk를 예측합니다. 1,000 expert demos, train seed 0–9,999, test seed ≥10,000을 사용합니다."
            ),
            "evidence": [
                {
                    "trace": "본문 Table I 상단 · matched encoder comparison [Verified]",
                    "claim": "3×300 held-out episodes에서 DINO [CLS] 32.6±1.5%, 4×4 patches 31.7±3.0%, SPOT 55.0±2.9%. 같은 policy에서 16× token 증가는 이득이 없고 object grouping은 +22.4p입니다.",
                },
                {
                    "trace": "본문 Table I 하단 · spatial grounding/resolution [Verified]",
                    "claim": "SPOT pure visual 31.0±2.8 → approximate 2D goal 55.0±2.9 → exact calibration 58.7±3.4 → 224² 68.7±4.2; privileged 3D oracle 71.7±4.1. encoder 구조만큼 goal grounding이 큽니다.",
                },
                {
                    "trace": "본문 Table II · fusion capacity probe [Verified]",
                    "claim": "goal 없는 설정에서 cross-attention은 seen train 약 60.0%로 concatenation 38.6%보다 높지만 held-out은 둘 다 31.0%. 추가 fusion capacity가 transfer되지 않습니다.",
                },
                {
                    "trace": "본문 Fig. 4–5 · automated failure taxonomy [Verified]",
                    "claim": "grounding이 좋아지며 PickCube Near-Miss는 31%→21%→2.5%로 감소하지만 No-Grasp는 남습니다. StackCube 단일 200-episode run은 144건(72%) No-Grasp, 성공 12건(6%)으로 occlusion·temporal binding을 지목합니다.",
                },
            ],
            "falsification": (
                "parameter·token·history를 맞춘 segmentation-mask 또는 shuffled-slot control이 같은 향상을 내거나, unseen texture/background에서 slot binding 없이도 성능이 유지되면 "
                "object competition이 아니라 SPOT pretraining/implicit supervision 효과일 수 있습니다."
            ),
            "adversarial": (
                "단일 ManiSkill3 domain, fixed cameras, frozen COCO-pretrained SPOT, privileged simulator 2D goal에 의존합니다. 14×14 dense baseline은 GPU memory 때문에 T=1/H=1이라 공정한 dense 반증이 아니며, "
                "best checkpoint를 200 held-out episodes로 고른 뒤 3×300을 평가합니다. sim-to-real 증거는 없습니다."
            ),
            "thinking_tool": (
                "capacity를 늘리는 대신 먼저 경쟁 단위를 설계합니다. 그 다음 성공률을 올리는 실험과 실패 종류를 바꾸는 실험을 분리해, 다음 module이 spatial grounding인지 temporal identity인지 결정합니다."
            ),
            "transfer_boundary": (
                "작은 수의 분리 가능한 rigid objects와 고정 camera에 잘 맞습니다. deformable object, dense clutter, heavy occlusion, long temporal identity에는 slot memory와 correspondence가 추가로 필요합니다."
            ),
        },
        {
            "rank": 2,
            "title": "See like a Robot: Robot-Centric Pointmaps for Vision-Language-Action Models",
            "arxiv_id": "2607.11498",
            "fit": "VLA · 3D geometry · viewpoint generalization",
            "status": "Tier A · 공식 PDF 및 supplementary 확인",
            "status_quo": (
                "VLA는 camera-frame RGB/depth를 보고 robot-base action을 예측하며, 충분한 데이터와 camera cue가 있으면 그 좌표 변환도 정책이 학습할 수 있다고 가정합니다."
            ),
            "friction": (
                "기관·camera setup이 섞인 데이터에서는 같은 물체가 viewpoint마다 다른 image coordinate를 갖지만 action은 robot frame에 남습니다. "
                "point cloud는 frame mismatch를 줄여도 pretrained 2D VLA의 H×W grid와 weight를 버립니다."
            ),
            "hidden_premise": (
                "정책이 calibration을 ‘알고’ 있는 것과 관측 자체가 action frame으로 변환돼 있는 것은 다릅니다. 3D 정보를 주는 것보다 pretraining interface를 보존한 채 action 좌표계로 미리 옮기는 것이 중요합니다."
            ),
            "conceptual_move": (
                "RGB-D pixel마다 robot-frame XYZ를 저장한 pointmap을 만들고 end-effector 기준으로 재중심화합니다. image grid를 유지해 별도 point-cloud architecture 없이 기존 SigLIP visual tokens에 element-wise로 더합니다."
            ),
            "mechanism": (
                "intrinsics·extrinsics로 depth를 robot frame에 lift하고 현재 end-effector position을 뺍니다. RGB tower에서 복제한 pointmap tower를 fine-tune하며, camera별 RGB/pointmap token을 같은 위치끼리 더해 π0.5와 SmolVLA에 입력합니다."
            ),
            "evidence": [
                {
                    "trace": "본문 Table 1 · information-matched transform ablation [Verified]",
                    "claim": "RGB 27.9%, RGB+Plücker 28.7%, +Depth 31.6%, 같은 depth/K/E로 pre-computed pointmap 34.7%. 3.1p 차이가 좌표 변환을 policy 밖에서 수행한 효과를 격리합니다.",
                },
                {
                    "trace": "본문 Table 2–3 · representation/origin ablation [Verified]",
                    "claim": "pointmap add 34.7%가 PTv3 point cloud 32.8%, pointmap concat 30.7%보다 높습니다. end-effector centering은 fixed 36.9%, randomized 36.6%로 base-centered 34.7→32.7보다 viewpoint drop이 작습니다.",
                },
                {
                    "trace": "본문 Table 4 · RoboCasa 24 tasks [Verified]",
                    "claim": "π0.5 55.3→62.9%, SmolVLA 37.2→41.4%. strongest matched camera-aware KYC 59.1%, 3D-augmented PointVLA 57.3%보다 π0.5+pointmap이 높지만, 네 prior baseline은 저자 재구현입니다.",
                },
                {
                    "trace": "본문 Table 5 · Franka seen/unseen camera [Verified]",
                    "claim": "4 tasks×condition당 15 rollouts에서 RGB π0.5 대비 pointmap은 seen 73.3→78.3(+5.0p), unseen 55.0→66.7(+11.7p). unseen에서도 절대 11.6p 하락은 남습니다.",
                },
            ],
            "falsification": (
                "extrinsic noise를 주거나 calibration을 틀리게 한 상태에서 camera-conditioned baseline이 pointmap보다 견고하고, token·encoder capacity를 맞춘 point-cloud grid가 격차를 없애면 "
                "robot-frame invariance보다 정확한 calibration과 fusion implementation이 이득의 원인일 수 있습니다."
            ),
            "adversarial": (
                "calibrated RGB-D가 train/test 모두 필요하고 camera 수·FoV 변화는 다루지 않습니다. point-cloud 비교는 한 sampling budget뿐이며 KYC·OC-VLA·GeoVLA·PointVLA는 official code 부재로 재구현했습니다. "
                "real robot은 한 Franka, 4 tasks, camera placement shift에 한정됩니다."
            ),
            "thinking_tool": (
                "학습기가 좌표 변환을 추론하게 두기 전에 관측을 action이 정의된 frame으로 옮깁니다. 동시에 pretrained model이 기대하는 topology(H×W)를 보존해 invariance와 transfer interface를 함께 설계합니다."
            ),
            "transfer_boundary": (
                "calibrated RGB-D manipulation과 end-effector-relative action에 강합니다. moving/unknown cameras, monocular-only sensing, severe depth holes, deformable scenes에는 calibration estimation과 uncertainty propagation이 필요합니다."
            ),
        },
        {
            "rank": 3,
            "title": "SEAMLiS: Visibility-Aware Safety for Perception-Limited Multi-Robot Exploration",
            "arxiv_id": "2607.09959",
            "project": "https://github.com/tkkim-robot/seamlis",
            "fit": "active perception · safety filter · decentralized exploration",
            "status": "Tier A · 공식 PDF 전체 확인",
            "status_quo": (
                "exploration planner는 frontier와 information gain을 고르고, local CBF/MPC는 현재 map의 obstacle을 피하면 된다는 모듈 분리가 일반적입니다."
            ),
            "friction": (
                "unknown space를 free로 계획하고 sensor yaw는 정보가 많은 방향을 보면, 이동 방향의 hidden obstacle이 braking이 불가능해진 뒤에야 FoV에 들어옵니다. "
                "현재 known map에 대한 collision-free는 perception-limited safety를 보장하지 않습니다."
            ),
            "hidden_premise": (
                "안전 상태에는 obstacle distance뿐 아니라 ‘critical known-free/unknown boundary를 회피 가능한 시간 안에 관측할 수 있는가’가 포함돼야 합니다. sensing direction이 control state입니다."
            ),
            "conceptual_move": (
                "upstream allocator/planner를 바꾸지 않고 execution layer에 yaw gatekeeper와 positional CBF를 붙입니다. information-seeking yaw는 future visibility certificate가 유효할 때만 허용하고 아니면 velocity-tracking yaw로 전환합니다."
            ),
            "mechanism": (
                "candidate yaw rollout이 nominal horizon에서 visibility-safe set을 유지하고 backup rollout이 terminal set에 도달하는지 검사합니다. 위치 MPC-CBF/HOCBF는 detect된 obstacle과 inter-agent separation을 처리합니다. "
                "각 robot은 local map만 갖고 pose/frontier만 비동기 공유합니다."
            ),
            "evidence": [
                {
                    "trace": "본문 Table II · 100 randomized trials/setting [Verified]",
                    "claim": "frontier와 D-CoScan-style allocator, R=1/2/3의 6개 설정에서 SEAMLiS success=1.00, collision=0.00. constant/VP는 multi-robot collision이 0.37–1.00까지 오르고 velocity tracking은 collision 0이지만 모든 설정에서 completion 0입니다.",
                },
                {
                    "trace": "본문 Sec. VII-A · deployment envelope [Verified]",
                    "claim": "기본 θFoV=70°, range=4.5m, vmax=1.5m/s, amax=2.0m/s², 0.1s tick, 5–25 hidden obstacles. unknown은 free로 계획하며 obstacle map을 robot 간 공유하지 않는 강한 partial-observability 조건입니다.",
                },
                {
                    "trace": "본문 Sec. VII-B · efficiency/safety trade [Verified]",
                    "claim": "SEAMLiS는 모든 trial을 완료하지만 unknown-region overlap violation은 0이 아닙니다(예: frontier R=3, 4.33/robot). 완전 보수 yaw의 0 violation과 달리 탐색 완료를 유지하는 절충입니다.",
                },
                {
                    "trace": "본문 Fig. 7–8 · Isaac Sim/Crazyflie [Verified, qualitative]",
                    "claim": "대표 Isaac rollout과 2-Crazyflie Vicon 실험에서 constant yaw는 late detection 후 충돌하고 SEAMLiS는 회피합니다. 다만 hardware 결과는 반복 수치 표가 아니라 대표 실행입니다.",
                },
            ],
            "falsification": (
                "FoV/range/actuation/model error를 certificate 경계 밖으로 sweep했을 때 planner-integrated visibility baseline이나 chance-constrained MPC가 같은 completion으로 더 적은 violation을 내면, "
                "execution-only gate의 독립적 이점과 보장 범위가 약해집니다."
            ),
            "adversarial": (
                "충돌 보장은 sensing range, braking feasibility, nonempty CBF admissible set, model 조건에 의존합니다. simulation은 planar dynamics와 static sampled obstacles이며 deterministic master seed를 사용합니다. "
                "hardware 증거는 2 robots의 대표 사례이고 통계적 반복·localization error·communication loss stress는 없습니다."
            ),
            "thinking_tool": (
                "‘지금 보이는 obstacle을 피한다’에서 ‘피할 시간이 남아 있을 때 반드시 보게 한다’로 safety invariant를 한 단계 앞당깁니다. planner를 갈아엎지 않고 execution contract로 위험한 자유도만 필터링합니다."
            ),
            "transfer_boundary": (
                "bounded dynamics, finite static obstacles, known FoV/range, feasible backup policy에 적합합니다. dynamic obstacles, uncertain state estimation, 3D attitude coupling, intermittent sensing에서는 robust/probabilistic certificate가 필요합니다."
            ),
        },
        {
            "rank": 4,
            "title": "SensorPerch: Sense Wherever and Whenever it Matters",
            "arxiv_id": "2607.10682",
            "fit": "reconfigurable sensing · active perception · robot systems",
            "status": "Tier A · 공식 PDF 전체 확인",
            "status_quo": (
                "active perception은 robot-mounted camera를 움직이거나 fixed infrastructure 중 좋은 view를 고르는 문제로 정의됩니다. sensor는 robot 또는 environment에 영구 결합된 자원입니다."
            ),
            "friction": (
                "robot이 workspace를 떠나면 object state를 볼 수 없고, wrist camera는 tool/arm에 가리며, task마다 top-down·lateral처럼 필요한 view가 달라 한 static third-person camera가 모두를 만족시키지 못합니다."
            ),
            "hidden_premise": (
                "viewpoint selection의 feasible set을 robot kinematics에 고정할 이유가 없습니다. sensor 자체를 manipulation 가능한 object로 만들면 perception은 fixed capability가 아니라 배치·회수·충전 가능한 resource가 됩니다."
            ),
            "conceptual_move": (
                "wireless RGB-D sensor를 robot이 detach/reattach하는 물리적 entity로 만들고, mountable surface의 candidate view를 합성·scoring해 task-optimal 위치에 부착합니다. object-coupled monitoring과 policy-coupled view reconstruction을 구분합니다."
            ),
            "mechanism": (
                "Raspberry Pi 4B, battery, 2-DoF gimbal, vacuum stand, magnetic interface로 298.7g module을 구성합니다. radiance-field scene에서 mountable regions를 찾고 novel view를 합성한 뒤 VLM 또는 policy-feature utility로 placement를 고릅니다."
            ),
            "evidence": [
                {
                    "trace": "본문 Fig. 5 · hardware reliability, 20 trials [Verified]",
                    "claim": "attachment error 0.42±0.18cm, payload 포함 weight 대비 shear >12×·pull-off 4×, RealSense streaming battery 2.25±0.17h. 물리적 sensing primitive를 정량화합니다.",
                },
                {
                    "trace": "본문 Fig. 6a · object-coupled tasks, 20 trials [Verified]",
                    "claim": "boil-over, fall, microwave fire, dropped cup, leak의 5 tasks에서 oracle에 근접한다고 보고하며 random feasible placement는 20%에 그칩니다. feasibility만으로 task utility를 대체할 수 없습니다.",
                },
                {
                    "trace": "본문 Fig. 6b · policy-coupled tasks, 20 trials [Verified]",
                    "claim": "peeling/cutting/pouring에서 약 80% success로 oracle에 근접합니다. gimbal 제거 시 peeling 약 40%, cutting 약 20%; wrist는 self-occlusion, fixed camera는 task-specific view 불일치가 병목입니다.",
                },
                {
                    "trace": "본문 Fig. 7–8 · system demonstration/latency [Verified]",
                    "claim": "3 modules 10 trials에서 object-state detection 90%, cutting 80%. one-time scene reconstruction 369.20±2.31s, detach–reattach 12.53±3.40s, streaming 약 180ms(<250ms at −65dBm)로 시간척도가 분리됩니다.",
                },
            ],
            "falsification": (
                "같은 설치·reconfiguration 예산에서 mobile robot reposition, pan-tilt camera, 다중 fixed camera가 task success와 coverage를 같거나 더 싸게 달성하거나, surface/material shift에서 attachment/view scoring이 무너지면 "
                "sensor-as-resource의 일반적 우위는 약해집니다."
            ),
            "adversarial": (
                "한 Kinova arm, lab household, 8 tasks와 제한된 attachable surfaces입니다. one-time reconstruction이 약 6분이고 relocation은 12.5초라 고속 task에는 맞지 않습니다. "
                "porous/compliant surface, robot-motion-induced occlusion, long-term dirt/leak, security·network failure는 다루지 않습니다."
            ),
            "thinking_tool": (
                "관측이 부족할 때 model을 더 강하게 만들기 전에 sensing topology 자체를 action space로 승격합니다. task가 요구하는 information을 계산한 뒤 camera를 움직이는 것이 아니라 sensor의 소유 위치를 바꿉니다."
            ),
            "transfer_boundary": (
                "초 단위 reconfiguration이 허용되고 평탄·밀폐 가능한 surface가 있는 household/inspection monitoring에 강합니다. high-speed navigation, outdoor weather, soft/porous structures, millisecond feedback control에는 다른 attachment와 planning이 필요합니다."
            ),
        },
        {
            "rank": 5,
            "title": "Stop to Decide: Latency-Aware Proprioceptive Navigation Primitives for Mapping-Free Quadruped Inspection",
            "arxiv_id": "2607.11204",
            "fit": "quadruped inspection · control latency · hybrid primitives",
            "status": "Tier A · 공식 PDF 및 protocol audit 확인",
            "status_quo": (
                "proprioceptive stair detector는 body pitch가 회복되면 summit에 도달했다고 판단하면서 계속 전진합니다. algorithmic threshold가 맞으면 loop rate는 implementation detail로 취급됩니다."
            ),
            "friction": (
                "Jetson에서 vision과 navigation을 같이 돌리면 stair loop가 약 15Hz로 내려가고, 50cm top platform보다 75cm robot이 길어 pitch recovery를 다음 tick에 읽는 사이 far edge를 넘어갑니다."
            ),
            "hidden_premise": (
                "latency의 물리적 dose는 ms가 아니라 한 decision period에 전진하는 거리 v/f입니다. sensor estimate가 맞더라도 움직이는 동안 판정하면 geometry margin보다 dose가 큰 순간 실패합니다."
            ),
            "conceptual_move": (
                "continuous detect-and-climb를 climb–settle–decide cadence로 바꿉니다. robot을 잠시 고정해 rate-limited loop가 pitch hysteresis를 평가하도록 하며, logistic dose–response로 배포 가능한 critical rate를 계산합니다."
            ),
            "mechanism": (
                "1s climb/2s stop cadence와 deep-climb-then-recovery pitch rule을 state machine에 넣습니다. built-in IMU, 4 foot forces, 3 one-dimensional ranges, line camera만으로 line following, 45°–push–45° corridor turn, stairs를 연결합니다."
            ),
            "evidence": [
                {
                    "trace": "본문 Table 8 · crossed loop-rate ablation [Verified]",
                    "claim": "continuous overshoot는 약 30/20/15Hz에서 6/15, 9/15, 7/15; cadence는 1/15, 0/15, 0/15. pooled 22/45 vs 1/45, Fisher p≈2.4×10⁻⁷; 15Hz에서는 7/15 vs 0/15입니다.",
                },
                {
                    "trace": "본문 Sec. 4.5/6.4 · pre-specified dose model [Verified]",
                    "claim": "x=v/f logistic fit은 0.30m/s에서 critical rate 약 19Hz를 제시합니다. 사전 지정 40Hz cell은 5/15=33%로 protocol-clean 43%, sensitivity 22% 예측 사이이며 저자는 양쪽 fit을 공개합니다.",
                },
                {
                    "trace": "본문 Table 7 · 55cm corridor primitive [Verified]",
                    "claim": "45°–10cm push–45°는 20/20 contact-free, in-place yaw는 14/20 success와 12/20 wall-contact. time 18.08±0.89 vs 24.08±0.89s, exit error 1.56±0.71° vs 5.64±2.50°입니다.",
                },
                {
                    "trace": "본문 Table 5 / Sec. 7.4 · integrated result and bounds [Verified]",
                    "claim": "end-to-end 18/20(90%), 77.30±4.40s. 하지만 한 course geometry·robot·operator, n=15/cell이며 loop throttling은 fixed delay라 실제 compute jitter를 재현하지 않습니다.",
                },
            ],
            "falsification": (
                "같은 throughput에서 slow continuous crawl, predictive phase compensation, higher-priority control thread가 cadence와 같은 overshoot 감소를 더 짧은 시간에 달성하거나 다른 stair geometry/platform에서 v/f dose가 failure를 설명하지 못하면 "
                "stop-to-decide의 일반성이 제한됩니다."
            ),
            "adversarial": (
                "단일 indoor competition-style course와 hand-tuned state machine이며 SLAM·absolute pose·unstructured terrain·endurance가 없습니다. arrival rule 자체는 별도 ablation하지 않았고, fixed delay는 jitter를 모델링하지 않습니다. "
                "trace label의 dwell 항이 한 operator-caught continuous overshoot를 safe로 만들었으나 pitch-only audit에서도 cadence 효과는 유지됩니다."
            ),
            "thinking_tool": (
                "latency를 software profiling 값에서 물리적 dose v/f로 변환합니다. decision confidence를 더 높이기보다 margin이 소진되기 전에 motion을 멈춰 sensing/decision time과 actuation time을 분리합니다."
            ),
            "transfer_boundary": (
                "geometry가 반복되고 pause가 가능한 structured inspection에 적합합니다. dynamic terrain, traffic flow를 막을 수 없는 navigation, momentum이 큰 platform, 매우 짧은 event에는 predictive control이나 asynchronous real-time path가 필요합니다."
            ),
        },
        {
            "rank": 6,
            "title": "What Does Your Short-Answer VQA Score Actually Measure? Evaluator-Dependent Instability in Multimodal Short-Answer Benchmarks",
            "arxiv_id": "2607.10240",
            "fit": "multimodal evaluation · evaluator reliability · benchmark contracts",
            "status": "Tier A · 공식 PDF 및 appendix 확인",
            "status_quo": (
                "short-answer VQA의 official score는 semantic ability를 직접 측정하며, exact match/ANLS가 만든 오차는 model ranking을 크게 바꾸지 않으면 사소한 noise로 간주됩니다."
            ),
            "friction": (
                "생성 모델은 맞는 뜻을 wrapper, morphology, alias, multi-span 순서가 다른 문자열로 냅니다. official error pool은 genuine visual failure와 surface-form rejection을 섞어 다음 학습 우선순위를 왜곡합니다."
            ),
            "hidden_premise": (
                "관측 점수는 semantic correctness Ssem과 evaluator compatibility κ의 합성입니다. benchmark마다 scalar/readout/identifier/multi-span contract mix가 달라 같은 1점도 같은 능력 변화를 뜻하지 않습니다."
            ),
            "conceptual_move": (
                "6 models×6 benchmarks의 official errors를 human-validated text-only semantic judge로 audit하고, answer contract별 undercount와 benign prompt/context perturbation을 분리합니다. deterministic CPU repair를 causal diagnostic으로 사용합니다."
            ),
            "mechanism": (
                "37,033 official-error items을 두 judge로 재평가하고 570-item stratified human review로 judge를 검증합니다. output-side normalization, reference-side accepted-form expansion, bidirectional repair를 166,731 open-weight rows에 적용합니다."
            ),
            "evidence": [
                {
                    "trace": "본문 Table 2 · judge validation [Verified]",
                    "claim": "570-item human review에서 precision 97.6%, recall 95.5%, Cohen κ=0.917. second text-only judge도 benchmark-level false-negative pattern을 재현해 단일 judge artifact 가능성을 줄입니다.",
                },
                {
                    "trace": "본문 Table 3 · semantic undercount [Verified]",
                    "claim": "ST-VQA official errors의 28–48%가 judge-accepted이고 open-model accuracy correction 평균 +9.2p; TextVQA +4.9p, DocVQA +2.4p. ranking이 거의 유지돼도 adjacent official gap보다 correction이 큽니다.",
                },
                {
                    "trace": "본문 Table 4–6 · contract/perturbation diagnosis [Verified]",
                    "claim": "readout·multi-span judge false-negative가 36.4%·39.2%. benign variant flip은 1.8–29.4%; context-only edit은 official −4.7p인데 canonical true score는 +0.5p로 evaluator-facing drift를 분리합니다.",
                },
                {
                    "trace": "본문 Table 7 · CPU-only contract repair [Verified]",
                    "claim": "bidirectional repair는 166,731 rows에서 +1.34p, net +2,237, 4 breaks, 32 workers 약 45s. judge false negatives의 17.44%만 복구해 mismatch의 대부분은 단순 string normalization을 넘습니다.",
                },
            ],
            "falsification": (
                "blind human re-annotation과 task-specific semantic metrics에서 judge correction이 재현되지 않거나, contract-normalized score가 downstream human utility/transfer를 더 잘 예측하지 못하면 "
                "semantic audit가 또 다른 evaluator preference를 추가했을 뿐일 수 있습니다."
            ),
            "adversarial": (
                "LLM judge도 완전한 ground truth가 아니며 taxonomy는 heuristic입니다. closed-source 결과는 benchmark별 200–500 sample이고, perturbation은 latent understanding 보존을 직접 증명하지 않습니다. "
                "text-side interface만 다루며 image/cross-modal shift와 open-ended generation은 범위 밖입니다."
            ),
            "thinking_tool": (
                "score를 능력 하나로 읽지 않고 생성 내용과 interface survival의 곱으로 분해합니다. error pool을 학습에 쓰기 전에 evaluator를 intervention해 점수가 움직이는지 확인합니다."
            ),
            "transfer_boundary": (
                "VQA, embodied QA, structured robot command처럼 reference answer와 automatic metric이 있는 task에 직접 적용됩니다. open-ended planning, preference evaluation, physical success처럼 reference string이 없는 경우에는 다른 contract audit가 필요합니다."
            ),
        },
    ],
    "synthesis": [
        {
            "title": "S1 · 구조는 많을수록 좋은 것이 아니라 invariant의 위치가 맞아야 한다",
            "links": "More Structure ↔ See like a Robot ↔ FoundationGeo",
            "facts": (
                "object slots는 patch grouping을, pointmaps는 camera-to-robot transform을, FoundationGeo는 pixel-wise metric calibration과 focal coverage를 구조화합니다. 각 논문에서 다른 구조·데이터 축이 지배합니다."
            ),
            "inference": (
                "‘structure beats scale’은 절반만 맞습니다. structure는 올바른 nuisance를 제거하고, scale은 남은 true variation을 덮을 때 보완 관계입니다. APRL은 object/frame/intrinsics를 한 번에 섞지 말고 각각의 causal gain을 분리해야 합니다."
            ),
            "decision": "VLA ablation 표의 열을 backbone size보다 object identity, coordinate frame, calibration coverage 순서로 설계합니다.",
        },
        {
            "title": "S2 · Active perception의 세 actuator는 센서, 시선, 시간이다",
            "links": "SensorPerch ↔ SEAMLiS ↔ Stop to Decide",
            "facts": (
                "SensorPerch는 센서 위치를 옮기고, SEAMLiS는 yaw를 gate하며, Stop to Decide는 robot motion을 멈춰 decision 시간을 확보합니다. 세 방법 모두 perception failure를 더 강한 recognizer 없이 줄입니다."
            ),
            "inference": (
                "우리의 active perception policy는 next view만 고를 것이 아니라 reposition / look / pause 중 가장 싼 actuator를 고르는 meta-controller가 되어야 합니다. 비용 단위는 view 수가 아니라 time-to-safe-information입니다."
            ),
            "decision": "FoV·reconfiguration time·v/f·braking margin을 같은 state에 둔 visibility-to-action benchmark를 만듭니다.",
        },
        {
            "title": "S3 · 실패 taxonomy는 분석 부록이 아니라 다음 모델의 설계도다",
            "links": "More Structure ↔ Stop to Decide ↔ Short-Answer VQA",
            "facts": (
                "binary failure 안에 Near-Miss/No-Grasp, overshoot/non-arrival, semantic error/contract mismatch가 섞여 있습니다. 각 분해 뒤에 필요한 fix가 spatial grounding, temporal tracking, cadence, evaluator repair로 달라집니다."
            ),
            "inference": (
                "top group의 moat는 최고 평균보다 failure를 재현 가능하게 이름 붙이고 자동 판정하는 protocol입니다. 그 taxonomy가 data collection과 module roadmap을 동시에 결정합니다."
            ),
            "decision": "모든 APRL benchmark에 mutually exclusive failure family와 raw trace-to-label script를 first-class artifact로 포함합니다.",
        },
        {
            "title": "S4 · Viewpoint robustness에는 representation invariance와 physical reconstruction 두 가격표가 있다",
            "links": "See like a Robot ↔ SensorPerch",
            "facts": (
                "pointmap은 calibration으로 viewpoint variation을 robot frame에서 지우고, SensorPerch는 policy가 익숙한 view를 물리적으로 다시 만듭니다. 전자는 매-frame depth/calibration, 후자는 약 12.5s relocation과 surface를 요구합니다."
            ),
            "inference": (
                "둘은 경쟁 baseline입니다. invariant representation이 싸지 않은 환경에서는 sensor relocation이, reconfiguration이 느린 환경에서는 frame alignment가 유리합니다. hybrid는 uncertainty가 높을 때만 physical view를 재구성해야 합니다."
            ),
            "decision": "camera shift 실험에서 success뿐 아니라 calibration setup cost, relocation latency, energy, recovery frequency를 같이 보고합니다.",
        },
    ],
    "frontier_memory": [
        {
            "signal": "강화 중",
            "title": "Representation → robot-usable invariant",
            "history": "6/24 interactable map → 6/29 localization drift → 6/30 localization 가능한 Gaussian-SLAM → 7/13 language-action grounding → 7/14 object/frame alignment.",
            "read": "rendering·embedding 품질보다 action에 필요한 object identity와 coordinate frame을 보존하는 연구가 계속 강화됩니다.",
        },
        {
            "signal": "새로운 통합",
            "title": "Active perception → visibility-time control",
            "history": "7/13 active multi-view diagnosis → 7/14 sensor relocation, yaw gatekeeping, stop-to-decide가 한 배치에서 결합.",
            "read": "next-best-view를 넘어 언제 보고, 어디서 보고, 보는 동안 멈출지를 함께 결정하는 연구선이 열렸습니다.",
        },
        {
            "signal": "강화 중",
            "title": "Average score → measurement contract",
            "history": "6/26 closed-loop scenario → 6/29 cooperation stress → 7/13 hidden state diagnosis → 7/14 evaluator contract·failure taxonomy.",
            "read": "benchmark는 model을 재는 수동 장치가 아니라 결과를 만드는 intervention입니다. score pipeline을 공개·ablate하는 팀이 표준을 소유합니다.",
        },
        {
            "signal": "긴장 관계",
            "title": "Structure vs scale은 거짓 양자택일",
            "history": "More Structure는 1,000 demos에서 inductive bias가 capacity를 이김. FoundationGeo는 10.2M corpus와 focal-length coverage로 metric shift를 복구.",
            "read": "shortcut을 막는 structure와 실제 deployment variation을 덮는 scale은 보완적입니다. 어떤 variation이 nuisance인지 먼저 판별해야 합니다.",
        },
        {
            "signal": "비어 있음",
            "title": "동시 복합 shift와 task-success/J",
            "history": "각 논문은 viewpoint, occlusion, latency, evaluator를 주로 따로 조작합니다.",
            "read": "camera shift+occlusion+compute jitter가 동시에 올 때의 closed-loop success, recovery latency, Joule/success는 아직 공백입니다. APRL이 소유하기 좋은 평가축입니다.",
        },
    ],
    "strategy": [
        {
            "priority": "BUILD",
            "title": "Coordinate–Time Interface Stressbench",
            "thesis": (
                "같은 policy에서 object grouping, robot-frame alignment, camera variation, loop throttling을 교차해 representation gain이 실제 control timing 아래 유지되는지 측정합니다."
            ),
            "scores": {"fit": 5, "novelty": 5, "feasibility": 4, "moat": 5, "timing": 5, "evidence": 5},
            "one_week": (
                "ManiSkill PickCube/StackCube 2 tasks에 DINO global, frozen slots, RGB-D pointmap을 붙이고 camera jitter 0/low/high와 inference delay 0/30/60ms를 교차합니다. "
                "success, Near-Miss, No-Grasp, p95 action age를 자동 로깅합니다."
            ),
            "four_week": (
                "RoboCasa 6 tasks와 Jetson hardware로 확장해 calibration noise·occlusion·jitter를 넣습니다. image-space action까지 추가하고 같은 backbone/data/compute budget에서 causal effect를 추정합니다."
            ),
            "metric": "OOD success +10p, worst-group success +8p, p95 action age 증가 ≤15%, failure classifier agreement κ≥0.8.",
            "stop": "2개 task family에서 matched RGB baseline 대비 worst-group +5p 미만이거나 calibration noise 2°/2cm에서 gain 절반 이상이 사라지면 general method build를 중단하고 diagnostic benchmark로 축소합니다.",
            "assets": [
                {"label": "More Structure paper", "url": "https://arxiv.org/abs/2607.09825"},
                {"label": "Robot-centric Pointmaps paper", "url": "https://arxiv.org/abs/2607.11498"},
                {"label": "ManiSkill", "url": "https://github.com/haosulab/ManiSkill"},
                {"label": "RoboCasa", "url": "https://github.com/robocasa/robocasa"},
            ],
        },
        {
            "priority": "EXPLOIT",
            "title": "Visibility-to-Action Safety Layer",
            "thesis": (
                "reposition sensor, rotate sensor, pause robot을 하나의 hybrid safety action set으로 두고 time-to-safe-information이 가장 짧은 선택을 합니다."
            ),
            "scores": {"fit": 5, "novelty": 5, "feasibility": 4, "moat": 5, "timing": 4, "evidence": 5},
            "one_week": (
                "SEAMLiS simulator에서 FoV 40/70/100°, range, v/f를 sweep하고 yaw gate / pause / combined policy를 비교합니다. collision, unknown-overlap, completion time으로 safety envelope를 그립니다."
            ),
            "four_week": (
                "quadruped 또는 mobile manipulator에서 fixed camera, wrist camera, relocatable third-person proxy를 붙여 task마다 look/pause/reposition을 고르는 rule-based meta-controller를 검증합니다."
            ),
            "metric": "zero collision under tested envelope, baseline 대비 completion slowdown <20%, hidden-region exposure -50%, unnecessary pause/reposition -30%.",
            "stop": "combined controller가 단순 velocity-aligned sensing보다 completion을 25% 이상 늦추거나 model mismatch에서 certificate violation이 5%를 넘으면 hardware 확장을 멈춥니다.",
            "assets": [
                {"label": "SEAMLiS paper", "url": "https://arxiv.org/abs/2607.09959"},
                {"label": "SEAMLiS code", "url": "https://github.com/tkkim-robot/seamlis"},
                {"label": "SensorPerch paper", "url": "https://arxiv.org/abs/2607.10682"},
                {"label": "Stop to Decide paper", "url": "https://arxiv.org/abs/2607.11204"},
            ],
        },
        {
            "priority": "EXPLORE",
            "title": "Embodied Evaluation Contract Autopsy",
            "thesis": (
                "robot benchmark의 binary success와 human annotation을 trace-derived failure family, semantic task completion, safety consequence로 분리해 model improvement와 evaluator repair를 구별합니다."
            ),
            "scores": {"fit": 5, "novelty": 5, "feasibility": 5, "moat": 4, "timing": 5, "evidence": 4},
            "one_week": (
                "기존 manipulation 500 episodes의 logs/video에 No-Grasp/Near-Miss/Drop/unsafe/contract-mismatch schema를 적용하고 binary success와 disagreement matrix를 만듭니다. 100건 blind human audit로 precision을 확인합니다."
            ),
            "four_week": (
                "instruction paraphrase, goal tolerance, success detector threshold, evaluator model을 factorial하게 바꿔 score flip과 downstream policy-selection flip을 분석하고 공개 reporting template을 만듭니다."
            ),
            "metric": "automatic taxonomy precision ≥95%, evaluator-induced score flip ≥5%의 재현 가능한 pocket 발견, error-driven retraining의 true failure reduction +10%.",
            "stop": "human audit에서 evaluator mismatch가 3% 미만이고 taxonomy가 next intervention의 성과를 예측하지 못하면 독립 benchmark 주장을 철회하고 내부 QA 도구로 유지합니다.",
            "assets": [
                {"label": "Short-answer VQA audit", "url": "https://arxiv.org/abs/2607.10240"},
                {"label": "3D-DefectBench", "url": "https://arxiv.org/abs/2607.10826"},
                {"label": "More Structure taxonomy", "url": "https://arxiv.org/abs/2607.09825"},
            ],
        },
    ],
}


def main() -> None:
    template.DATE = DATE
    template.SLUG = SLUG
    template.DATA = DATA
    doc = template.build_html()
    doc = doc.replace("2026-07-13 arXiv Research Intelligence", "2026-07-14 arXiv Research Intelligence")
    doc = doc.replace("<span>Tier A 5편 full-text</span>", "<span>Tier A 6편 full-text</span>")

    json_dir = ROOT / "intelligence"
    json_dir.mkdir(exist_ok=True)
    json_path = json_dir / f"{DATE}.json"
    html_path = ROOT / "posts" / f"{SLUG}.html"
    json_path.write_text(json.dumps(DATA, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    html_path.write_text(doc, encoding="utf-8")
    print(f"wrote {json_path.relative_to(ROOT)}")
    print(f"wrote {html_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
