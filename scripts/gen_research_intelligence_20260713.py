#!/usr/bin/env python3
"""Generate a separate, full-text Research Intelligence edition for 2026-07-13."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-07-13"
SLUG = f"{DATE}-research-intelligence"


DATA = {
    "date": DATE,
    "edition": "Research Intelligence",
    "source_prompt": "prompts/instruction_v20260713.md",
    "scope_note": (
        "기존 일간 브리핑을 보존한 별도 심층판입니다. Tier A 5편은 공식 arXiv PDF의 본문, 표, "
        "부록, 제한점을 읽고 작성했습니다. Verified는 논문에서 직접 확인한 사실, Inference는 APRL 관점의 해석입니다."
    ),
    "executive_thesis": (
        "오늘 가장 강한 공통 신호는 더 큰 backbone이 아니라, 모델이 실패하는 경계의 정의를 바꾸는 팀이 "
        "연구 의제를 선점한다는 것입니다. CLAP은 action의 표현 인터페이스를, BeyondSight는 actor의 존재 상태를, "
        "MultiView-Bench는 관측을 결합하는 좌표계와 평가 단위를, edge VLM 연구는 비용의 회계 단위를 바꿉니다. "
        "AnythingReality는 여러 모듈을 한 온라인 루프로 묶지만, 그 다음 승부는 렌더링 품질이 아니라 "
        "로봇이 그 map을 이용해 얼마나 정확히 판단하고 행동하는지에서 납니다."
    ),
    "decision_cards": [
        {
            "title": "판세 1 · Backbone보다 interface가 더 싼 레버리지다",
            "body": (
                "CLAP의 핵심은 별도 action expert가 아니라 자연어 prefix입니다. MultiView-Bench도 재학습보다 "
                "view별 판단과 belief aggregation으로 같은 모델을 개선합니다. 우리도 새 backbone을 만들기 전에 "
                "출력 표현, 상태 보존, 관측 분해를 독립 실험축으로 고정해야 합니다."
            ),
            "label": "Decision",
        },
        {
            "title": "판세 2 · Benchmark가 보지 못하면 model도 배우지 못한다",
            "body": (
                "BeyondSight의 temporal prior만으로는 mAPunobs가 0입니다. permanence label과 metric을 함께 넣을 때 "
                "0.249가 됩니다. 새 모듈보다 먼저 hidden state, observability gap, stale memory를 측정하는 "
                "evaluation contract를 설계하는 것이 선행되어야 합니다."
            ),
            "label": "Decision",
        },
        {
            "title": "판세 3 · 실험 예산은 입력량이 아니라 output·memory·view에 배분한다",
            "body": (
                "edge VLM의 decode 비용, MultiView-Bench의 budget-matched view selection, BeyondSight의 stale hypothesis는 "
                "모두 test-time budget을 무엇에 쓰는지가 성능과 안전을 결정함을 보여줍니다. task success당 Joule, "
                "회복당 추가 view, occlusion duration별 false persistence를 같은 표에 올려야 합니다."
            ),
            "label": "Decision",
        },
    ],
    "papers": [
        {
            "rank": 1,
            "title": "CLAP: Direct VLM-to-VLA Adaptation via Language-Action Grounding",
            "arxiv_id": "2607.08974",
            "fit": "VLA · policy representation · real-time deployment",
            "status": "Tier A · 공식 PDF 전체 확인",
            "status_quo": (
                "VLM을 VLA로 바꾸려면 action expert, 새 action vocabulary, 별도 diffusion/flow head처럼 "
                "구조적 변경이 필요하다는 믿음이 지배적입니다."
            ),
            "friction": (
                "사전학습 VLM은 자연어 분포에 맞춰져 있는데, fine-tuning에서 처음부터 숫자 action token을 내게 하면 "
                "출력 분포가 급변합니다. 구조를 복잡하게 만들수록 VLM 자체의 기여와 action head의 기여도 분리하기 어렵습니다."
            ),
            "hidden_premise": (
                "숫자 action 자체가 어려운 것이 아니라, 언어 모델이 익숙한 의미 공간에서 숫자 공간으로 넘어가는 다리가 없다는 것이 병목입니다."
            ),
            "conceptual_move": (
                "정답 action chunk를 고정 template의 자연어 설명으로 먼저 풀어 쓰고, 이어서 정확한 numeric action token을 생성합니다. "
                "자연어 prefix가 semantic plan이자 causal conditioning intermediate가 됩니다."
            ),
            "mechanism": (
                "동일 Qwen3.5 VLM backbone과 autoregressive decoder를 유지합니다. 학습 시 7-DoF action chunk에서 "
                "자연어 prefix를 자동 생성하고, 추론 시 모델이 prefix와 numeric token을 순차 출력합니다. 별도 expert, "
                "새 vocabulary, 수작업 language annotation은 필요하지 않습니다."
            ),
            "evidence": [
                {
                    "trace": "본문 Table 2 · matched 1-epoch comparison [Verified]",
                    "claim": "LIBERO 평균: 0.8B 76.1→89.6, 2B 75.9→90.8, 4B 64.2→84.9. 2B에서 +14.9p.",
                },
                {
                    "trace": "본문 Table 3 · action masking ablation [Verified]",
                    "claim": "masking은 0.8B -3.9p, 2B -1.7p, 4B +3.2p. augmentation은 보편 recipe가 아니라 capacity-dependent 변수.",
                },
                {
                    "trace": "본문 Table 4 · OOD factor split [Verified]",
                    "claim": "2B 평균은 32.9→44.0이지만 object-position relocation 성공은 거의 0. 개선이 모든 OOD family를 해결하지 못함.",
                },
                {
                    "trace": "부록 Table 6–7 · real robot / latency [Verified]",
                    "claim": "120 demos, 조건당 20 trials에서 2B ID/OOD 60/60%; 0.8B 35/10%. CLAP 2B latency 4.307s/chunk, VLA-0 0.8B 3.205s/chunk.",
                },
            ],
            "falsification": (
                "동일 action tokens와 data에서 prefix 의미를 무작위화하거나 길이만 맞춘 nonsense prefix가 같은 향상을 내면, "
                "language-action grounding이 아니라 추가 computation/sequence length 효과일 수 있습니다."
            ),
            "adversarial": (
                "4B가 2B보다 약하고 real-robot 성공률이 simulation보다 크게 낮습니다. 저자 비교표의 회색 prior work는 "
                "학습 조건이 통제되지 않았으며, 단일 VLM family·제한된 embodiment·autoregressive latency가 남습니다."
            ),
            "thinking_tool": (
                "분포가 끊기는 출력 앞에 모델이 이미 잘하는 표현으로 된 의미적 완충층을 둡니다. 새 module을 추가하기 전, "
                "pretraining distribution과 downstream output 사이의 interface mismatch부터 해부합니다."
            ),
            "transfer_boundary": (
                "자연어로 안정적으로 요약 가능한 action chunk에 강합니다. 고주파 force control, 매우 긴 horizon, "
                "언어화가 정보 손실을 만드는 reactive control에는 그대로 옮기기 어렵습니다."
            ),
        },
        {
            "rank": 2,
            "title": "BeyondSight: Object Permanence for End-to-End Autonomous Driving",
            "arxiv_id": "2607.09138",
            "project": "https://beyondsight-eccv.github.io",
            "fit": "partial observability · persistent state · planning",
            "status": "Tier A · 공식 PDF 및 부록 확인",
            "status_quo": (
                "센서 return이 없는 actor는 annotation과 metric에서 사라지고, sparse-query driving stack도 그 actor를 지웁니다. "
                "관측 가능성과 존재를 사실상 같은 변수로 취급합니다."
            ),
            "friction": (
                "nuScenes 분석에서 매 timestep 약 30% actor가 완전히 비관측입니다. temporal aggregation은 짧은 흔들림은 줄이지만, "
                "긴 occlusion 동안 actor를 학습·평가할 label과 contract가 없습니다."
            ),
            "hidden_premise": (
                "object permanence는 단순 memory module이 아니라 representation, supervision, metric 세 층이 동시에 actor existence를 보존해야 성립합니다."
            ),
            "conceptual_move": (
                "actor existence를 instantaneous observability에서 분리하고, prior–observation–posterior의 filtering-inspired query update로 바꿉니다. "
                "동시에 nuScenes-Permanence를 만들어 보이지 않는 동안도 학습·평가합니다."
            ),
            "mechanism": (
                "image-free Temporal Prior Decoder가 이전 query를 motion-conditioned hypothesis로 전파하고, Observation Decoder가 현재 image로 갱신하며, "
                "Posterior Fusion Decoder가 둘을 합칩니다. observability head와 unobservable actor loss를 추가합니다."
            ),
            "evidence": [
                {
                    "trace": "본문 Table 1–3 [Verified]",
                    "claim": "SparseDrive 대비 planning L2avg 0.61→0.54, mAP 0.415→0.427, mAPunobs 0→0.249; observable mAP은 0.415→0.421.",
                },
                {
                    "trace": "본문 Table 4 · cumulative ablation [Verified]",
                    "claim": "표준 label에서는 temporal prior를 넣어도 mAPunobs=0. Permanence label+prior 0.126, fusion 0.194, unobs supervision 0.213, full 0.249.",
                },
                {
                    "trace": "부록 Table 8 [Verified]",
                    "claim": "occlusion 0–2s→4–6s에서 TPR 0.62→0.35, FDR 0.85→0.98. headline gain 뒤에 매우 높은 false persistence가 남음.",
                },
                {
                    "trace": "부록 Table 9–10 [Verified]",
                    "claim": "annotation 932k→1.33M. 추가분은 zero-point 20%, interpolation 1%, extrapolation 9%; generated label 평균 L2 0.50m, P90 1.04m.",
                },
            ],
            "falsification": (
                "oracle privileged label 또는 multi-observer ground truth에서 adaptive tolerance를 제거했을 때 mAPunobs와 planning gain이 유지되지 않으면, "
                "일부 성과는 model permanence보다 label reconstruction/evaluation tolerance에서 왔을 수 있습니다."
            ),
            "adversarial": (
                "unobservable reference의 일부가 offline interpolation/extrapolation이며 abrupt hidden maneuver는 범위 밖입니다. "
                "4–6s FDR 0.98은 ‘기억한다’와 ‘유효하게 기억한다’가 다름을 보여줍니다. open-loop planning gain도 closed-loop safety 보장은 아닙니다."
            ),
            "thinking_tool": (
                "실패를 module 부족으로 보지 말고, benchmark가 존재 자체를 삭제하는지부터 봅니다. state variable을 "
                "존재/관측/불확실성으로 분해하고 각 상태별 metric을 설계합니다."
            ),
            "transfer_boundary": (
                "motion prior가 유효한 연속적 occlusion에 적합합니다. sudden turn, stop, scene exit, 상호작용이 강한 crowd에서는 "
                "uncertainty와 deletion policy가 없으면 위험한 phantom actor가 됩니다."
            ),
        },
        {
            "rank": 3,
            "title": "MultiView-Bench: A Diagnostic Benchmark for World-Centric Multi-View Integration in VLMs",
            "arxiv_id": "2607.08970",
            "project": "https://hantaozhangrichard.github.io/MultiView-Bench",
            "fit": "3D reasoning · diagnostic benchmark · active perception",
            "status": "Tier A · 공식 PDF 및 failure appendix 확인",
            "status_quo": (
                "VLM spatial benchmark는 single/limited view의 camera-relative 정답률을 주로 측정합니다. 높은 평균은 global coordinate frame을 "
                "여러 view에서 일관되게 구성하는 능력으로 오인될 수 있습니다."
            ),
            "friction": (
                "실제 CAD·assembly는 irregular shape를 lossless text/bounding box로 대체할 수 없고, object relation을 camera frame에서 world frame으로 옮겨야 합니다."
            ),
            "hidden_premise": (
                "3D reasoning 실패는 하나의 능력 부족이 아니라 object ID, 2D relation, axis identification, 3D translation 중 특정 atomic step의 붕괴입니다."
            ),
            "conceptual_move": (
                "visible global XYZ axes, controlled DoF, six views, procedural ground truth로 world-centric integration을 직접 stress-test하고, "
                "실패가 난 axis/view만 능동적으로 다시 관측하는 agent로 전환합니다."
            ),
            "mechanism": (
                "500개 main instances와 20 controlled variants를 생성합니다. ViewNavigator는 LLM planner가 view를 선택하고 VLM이 axis별 판단을 내리며, "
                "Dirichlet belief와 confidence gate가 evidence를 합칩니다."
            ),
            "evidence": [
                {
                    "trace": "본문 Figure 2 / 부록 Table 2 [Verified]",
                    "claim": "3D DoF=3 random chance는 3.7%. GPT-4o 2.0%, Claude 4 5.3%, Gemini 2.5 Pro 17.7%, GPT-5 49.0%.",
                },
                {
                    "trace": "본문 Section 4.2–4.3 [Verified]",
                    "claim": "주 실패는 axis direction identification. grid/color 효과는 model-specific이고, 비표준 axis rotation에서 급락해 learned convention 의존을 드러냄.",
                },
                {
                    "trace": "본문 Figure 5 · budget matched [Verified]",
                    "claim": "같은 최대 6 views/compute에서 GPT-4o 2→19%, Claude 4 5→25%, GPT-5 49→61%. 추가 budget이 아니라 structured decomposition 효과를 분리.",
                },
                {
                    "trace": "부록 F.3–F.5 [Verified]",
                    "claim": "한 번의 VLM Y-axis 오판이 belief confirmation bias로 전파되고, planner도 원하는 plane과 camera elevation을 모순되게 선택함.",
                },
            ],
            "falsification": (
                "camera calibration 또는 explicit projection matrix를 동일 budget에 제공했을 때 단순 geometry baseline이 크게 앞서면, "
                "benchmark가 일반 3D intelligence보다 이미지로 표시된 axis glyph 해석 능력을 주로 측정하는 것일 수 있습니다."
            ),
            "adversarial": (
                "scene은 clean schematic geometry와 visible axes에 의존하고 main variant당 100개뿐입니다. GPT-5의 Real World 56.7%가 DoF=3 primitive 49.0%보다 높아, "
                "‘real objects are always harder’ 서술도 model별로 성립하지 않습니다. full agent의 3–5×에는 더 많은 view와 micro-jitter가 포함됩니다."
            ),
            "thinking_tool": (
                "end score를 올리려 하지 말고 reasoning chain의 가장 약한 변환을 찾아 그 변환만 단순화·반복·belief update합니다. "
                "그리고 반드시 budget-matched control로 scaffold의 진짜 기여를 분리합니다."
            ),
            "transfer_boundary": (
                "global axes가 명시된 CAD/assembly에는 직접적입니다. 축이 보이지 않는 자연 scene, deformable objects, metric depth·occlusion이 큰 환경에는 "
                "calibration 추정과 geometry module이 추가로 필요합니다."
            ),
        },
        {
            "rank": 4,
            "title": "AnythingReality: Robust Online Gaussian Splatting SLAM for Open-Vocabulary VR Scene Exploration",
            "arxiv_id": "2607.09260",
            "fit": "online Gaussian map · VR · VLM interaction",
            "status": "Tier A · 공식 PDF 전체 확인",
            "status_quo": (
                "Gaussian reconstruction, SLAM, VR, semantic VLM은 각각 발전했지만, scan이 끝난 뒤 offline asset을 보는 식으로 분리되어 있습니다. "
                "depth tracking 품질이 나쁘면 online system 전체가 흔들립니다."
            ),
            "friction": (
                "noisy RealSense depth, Gaussian spawn explosion, host rendering과 headset latency, free-form VLM response를 한 live loop에서 동시에 다뤄야 합니다."
            ),
            "hidden_premise": (
                "새 representation 하나가 아니라, pose·map·render·language의 freshness contract와 typed interface를 맞추는 것이 deployable system의 핵심입니다."
            ),
            "conceptual_move": (
                "ORB-SLAM3 pose stream을 Gaussian-plus-SDF mapping에 결합하고, incrementally updated map을 즉시 stereo VR과 speech/VLM query에 노출합니다."
            ),
            "mechanism": (
                "TSDF confidence와 raycast depth로 Gaussian spawn을 gate하고 sliding-window optimization/pruning을 수행합니다. host에서 per-eye render 후 WebRTC로 전송하며, "
                "text router는 mark/describe/unsupported의 structured JSON만 허용합니다."
            ),
            "evidence": [
                {
                    "trace": "본문 Table 1 [Verified]",
                    "claim": "자체 4개 RealSense scene에서 Quality mode PSNR 22.69–27.72, 47.2–63.2 FPS; FPS mode 141.5–223.8 FPS. 비교법보다 자체 scene image quality가 높음.",
                },
                {
                    "trace": "본문 Section 3.1 [Author claim]",
                    "claim": "GPS-SLAM 대비 평균 Gaussian 수 47% 감소. 다만 camera 차이를 맞추기 위해 비교법 설정을 저자가 수정함.",
                },
                {
                    "trace": "본문 Section 3.2 [Verified protocol, weak evidence]",
                    "claim": "rendered view의 dominant object를 수동 판정하는 방식으로 understandable-view recognition 88%. sample 수·모델·inter-rater 정보는 본문에 없음.",
                },
                {
                    "trace": "본문 Limitation / future work [Verified]",
                    "claim": "현재 VLM은 보이는 단일 rendered image만 reasoning하며 persistent object map이 없음. annotation은 grounded object instance가 아니라 좌표+label point record.",
                },
            ],
            "falsification": (
                "PSNR/SSIM 우위가 camera-pose ATE, map consistency, headset motion-to-photon latency, downstream navigation/inspection success로 이어지지 않으면, "
                "통합은 impressive demo이지만 robot-usable map 개선은 아닙니다."
            ),
            "adversarial": (
                "자체 dataset은 6,000 frames/4 scenes이고 semantic 88% protocol이 약합니다. VR latency 숫자와 user study, pose accuracy, persistent grounding이 없습니다. "
                "‘complete system’의 강점은 integration이고, 각 component의 causal gain은 충분히 분리되지 않았습니다."
            ),
            "thinking_tool": (
                "모듈별 최고 점수보다 shared state가 언제 갱신되고 누가 소비하는지 설계합니다. freshness, schema, fallback을 interface-level invariant로 둡니다."
            ),
            "transfer_boundary": (
                "RGB-D indoor telepresence와 inspection에 적합합니다. outdoor scale, dynamic scene, high-speed robot, persistent semantics에는 pose/map consistency와 "
                "object memory 평가가 추가되어야 합니다."
            ),
        },
        {
            "rank": 5,
            "title": "Seeing is Free, Speaking is Not: Uncovering the True Energy Bottleneck in Edge VLM Inference",
            "arxiv_id": "2607.09520",
            "fit": "edge VLM · energy accounting · runtime budget",
            "status": "Tier A · 공식 PDF 및 표 확인",
            "status_quo": (
                "VLM efficiency는 visual token pruning, resolution, vision encoder FLOPs에 집중하며 시각 입력 처리가 주 에너지 병목이라고 암묵적으로 가정합니다."
            ),
            "friction": (
                "multimodal inference는 vision encoding, parallel prefill, autoregressive decode가 서로 다른 hardware regime을 갖기 때문에 FLOPs만으로 Joule을 설명할 수 없습니다."
            ),
            "hidden_premise": (
                "edge GPU가 추론 중 거의 일정 power로 포화된다면, energy 최적화는 power를 낮추는 문제가 아니라 비싼 단계의 wall-clock time을 줄이는 문제입니다."
            ),
            "conceptual_move": (
                "energy를 model power fingerprint × (prefill token cost + decode token cost + overhead)로 분해하고, 입력과 출력 token의 marginal cost를 따로 측정합니다."
            ),
            "mechanism": (
                "RTX 3070 Laptop과 Jetson Orin NX에서 5개 1B–4B quantized VLM, 4개 resolution, content complexity, long/short prompt를 llama.cpp greedy decoding으로 측정합니다."
            ),
            "evidence": [
                {
                    "trace": "본문 Figure 3–4 / Table 2 [Verified]",
                    "claim": "조건별 평균 power 변동 <5%; output token의 wall-clock cost는 input token의 11–39×. decode가 일반 조건에서 86–97% energy.",
                },
                {
                    "trace": "본문 Table 4 [Verified]",
                    "claim": "InternVL3-1B decode 87–91%. Dynamic-token Qwen2.5-VL-3B는 896²에서 prefill이 커져 decode 비율이 46%로 내려가는 resolution trap이 존재.",
                },
                {
                    "trace": "본문 Table 5 [Verified/theoretical bound]",
                    "claim": "fixed-token InternVL3-1B에서 모든 visual token 제거 상한 ≤10%, max_tokens 256→128은 약 45%, 3-token short answer는 90% 절감.",
                },
                {
                    "trace": "본문 Figure 5 / Equation 13 [Verified]",
                    "claim": "model size, Nin, Nout 및 interaction으로 1,680 runs의 universal predictor R²=0.986, MAPE=10.3%.",
                },
            ],
            "falsification": (
                "continuous VLA action decoding, batching/speculative decoding, DVFS, non-NVIDIA accelerators에서 power가 고정되지 않거나 output이 매우 짧을 때도 같은 dominance가 유지되는지 확인해야 합니다."
            ),
            "adversarial": (
                "결과는 llama.cpp, quantized 1B–4B 5개 모델, greedy decoding, 두 NVIDIA platform과 image-description prompt 중심입니다. "
                "‘모든 visual token 제거 ≤10%’는 fixed-token 조건의 상한이며 Qwen2.5-VL-3B 448²에서는 ≤28%입니다. quality trade-off도 직접 측정하지 않았습니다."
            ),
            "thinking_tool": (
                "최적화 대상의 개수를 세기 전에 stage별 hardware utilization과 marginal Joule을 측정합니다. ‘많은 token’과 ‘비싼 token’을 구분합니다."
            ),
            "transfer_boundary": (
                "긴 자연어를 생성하는 edge VLM에 강하게 적용됩니다. CLAP 같은 짧은 structured action output이나 parallel action head에는 decode dominance가 작아질 수 있어 재측정이 필요합니다."
            ),
        },
    ],
    "synthesis": [
        {
            "title": "S1 · 네 논문은 병목의 위치를 backbone 밖으로 옮긴다",
            "links": "CLAP ↔ BeyondSight ↔ MultiView-Bench ↔ Edge VLM",
            "facts": (
                "CLAP은 output prefix, BeyondSight는 persistent query와 label, MultiView는 view decomposition과 belief, energy 연구는 output budget을 바꿉니다."
            ),
            "inference": (
                "APRL이 선점할 자리는 새 거대모델보다 ‘world-action interface lab’입니다. 같은 backbone을 고정하고 표현·memory·view·budget만 바꿔 "
                "failure family별 causal gain을 보여주는 것이 더 빠르고 방어 가능한 연구선입니다."
            ),
            "decision": "다음 VLA/SLAM 실험표에 backbone row보다 interface-state-budget column을 먼저 고정합니다.",
        },
        {
            "title": "S2 · Scaffold의 효과는 budget-matched로만 인정한다",
            "links": "CLAP ↔ MultiView-Bench ↔ AnythingReality",
            "facts": (
                "CLAP은 matched backbone/epoch 표를 따로 두고, MultiView는 동일 6-view budget control을 둡니다. AnythingReality는 통합 성능은 보이지만 module별 causal ablation은 약합니다."
            ),
            "inference": (
                "agent loop, language prefix, map module의 효과는 추가 token·view·latency를 같은 예산으로 맞춰야 연구 기여가 됩니다. integration paper일수록 causal accounting이 moat가 됩니다."
            ),
            "decision": "모든 agentic baseline에 equal images, equal tokens, equal wall-clock의 3중 control을 요구합니다.",
        },
        {
            "title": "S3 · Memory는 recall이 아니라 stale-state 비용까지 측정한다",
            "links": "BeyondSight ↔ AnythingReality ↔ MultiView-Bench",
            "facts": (
                "BeyondSight 4–6s FDR은 0.98이고 AnythingReality는 persistent object memory가 없으며, MultiView agent는 한 번의 오판이 confirmation bias로 전파됩니다."
            ),
            "inference": (
                "persistent state는 보존률만 높이면 위험합니다. 기억 생성, 갱신, 삭제, uncertainty calibration을 한 protocol에서 재야 합니다."
            ),
            "decision": "APRL memory benchmark의 핵심 지표를 recall, false persistence, recovery latency, delete precision으로 정의합니다.",
        },
        {
            "title": "S4 · ‘로봇용’ 주장은 task-success당 비용으로 닫아야 한다",
            "links": "AnythingReality ↔ CLAP ↔ Edge VLM",
            "facts": (
                "AnythingReality는 PSNR/FPS와 weak semantic recognition, CLAP은 success와 chunk latency, energy 연구는 Joule을 각각 따로 측정합니다."
            ),
            "inference": (
                "이 셋을 결합하면 map quality나 VLA success 하나가 아니라 success/J, recovery/J, map-update-to-action latency가 배포 경쟁력이 됩니다."
            ),
            "decision": "향후 demo의 표준 결과표에 task success, p95 latency, Joule/decision, failure recovery를 같은 row로 둡니다.",
        },
    ],
    "frontier_memory": [
        {
            "signal": "강화 중",
            "title": "3D representation → robot-usable state",
            "history": "6/23 physical uncertainty·robot viewpoint → 6/24 interactable map → 6/29 localization drift → 6/30 localization 가능한 Gaussian-SLAM → 7/13 online map.",
            "read": "rendering metric만 앞세우는 연구의 전략 가치가 하락하고, pose·freshness·action coupling을 함께 내는 연구가 강화됩니다.",
        },
        {
            "signal": "강화 중",
            "title": "VLA scaling → grounding·adaptation·recovery",
            "history": "6/23 memory/failure/policy length → 6/25 online adaptation → 6/26 safety diagnosis → 6/30 early warning → 7/13 language-action grounding/post-training.",
            "read": "demonstration 수만 늘리는 후속작보다 어떤 failure family를 어떤 interface로 고치는지 분리한 연구가 더 설득력을 얻습니다.",
        },
        {
            "signal": "강화 중",
            "title": "평균 정확도 → hidden state와 closed-loop failure",
            "history": "6/24 risk understanding → 6/26 closed-loop scenario → 6/29 response/cooperation stress → 7/13 object permanence·multi-view diagnosis.",
            "read": "보이지 않는 actor, 보지 않은 view, 지워진 state를 benchmark가 명시하는 흐름이 뚜렷합니다.",
        },
        {
            "signal": "새로운 경고",
            "title": "Efficiency의 미측정 축: task-energy coupling",
            "history": "6/23 evidence compression → 6/26 mission-critical memory/bandwidth → 6/30 geometry 보존 → 7/13 decode energy.",
            "read": "token 절감은 반복됐지만 task success당 Joule과 recovery당 Joule은 아직 비어 있습니다. APRL이 빠르게 소유할 수 있는 평가축입니다.",
        },
    ],
    "strategy": [
        {
            "priority": "BUILD",
            "title": "Persistent World–Action Interface Benchmark",
            "thesis": (
                "강한 backbone을 고정하고 action prefix, actor memory, active view, output budget을 교체해 partial observability에서 "
                "success–latency–energy–staleness frontier를 측정합니다."
            ),
            "scores": {"fit": 5, "novelty": 5, "feasibility": 4, "moat": 5, "timing": 5, "evidence": 5},
            "one_week": (
                "LIBERO의 2–3 tasks에 CLAP-style semantic prefix/no-prefix, 1/2/4-view, short/long output budget을 얹고 "
                "success, recovery steps, p95 latency를 수집합니다. 실제 Joule이 없으면 첫 주는 GPU time을 proxy로 두되 명시합니다."
            ),
            "four_week": (
                "occlusion injection과 stale-state deletion을 추가하고 Jetson에서 Joule/decision을 측정합니다. 동일 backbone·token·view budget control을 자동 생성하는 harness로 확장합니다."
            ),
            "metric": "같은 backbone에서 OOD success +10p 또는 recovery time -20%, Joule/success 악화 ≤10%, false persistence <0.30.",
            "stop": "2개 task family에서 prefix/memory/view scaffold가 equal-budget baseline 대비 5p 미만이거나 false persistence가 0.50을 넘으면 build를 중단하고 진단 benchmark만 남깁니다.",
            "assets": [
                {"label": "CLAP paper", "url": "https://arxiv.org/abs/2607.08974"},
                {"label": "BeyondSight project", "url": "https://beyondsight-eccv.github.io"},
                {"label": "MultiView-Bench project", "url": "https://hantaozhangrichard.github.io/MultiView-Bench"},
            ],
        },
        {
            "priority": "EXPLOIT",
            "title": "Robot-Usable Gaussian Map Protocol",
            "thesis": (
                "Gaussian map을 PSNR asset이 아니라 localization, semantic query, reactive action을 같은 trajectory에서 지원하는 online state로 평가합니다."
            ),
            "scores": {"fit": 5, "novelty": 4, "feasibility": 5, "moat": 4, "timing": 5, "evidence": 4},
            "one_week": (
                "TUM-RGBD/Replica 한 scene에서 online GS baseline의 PSNR·FPS와 ATE, map update age, viewpoint query consistency를 동시에 로깅합니다. "
                "POI label을 다른 view에서 다시 찾는 최소 persistent-grounding test를 추가합니다."
            ),
            "four_week": (
                "dynamic occluder와 sensor dropout을 넣고 map freshness에 따라 navigation/inspection decision이 어떻게 무너지는지 benchmark화합니다."
            ),
            "metric": "PSNR 상위 모델과 task-success 상위 모델의 순위 역전 여부를 확인하고, map update age로 failure AUC ≥0.75를 달성.",
            "stop": "ATE·freshness·semantic consistency가 downstream action error를 예측하지 못하거나 기존 SLAM metric 대비 추가 설명력이 5% 미만이면 독립 benchmark 주장을 철회합니다.",
            "assets": [
                {"label": "AnythingReality paper", "url": "https://arxiv.org/abs/2607.09260"},
                {"label": "TUM RGB-D", "url": "https://cvg.cit.tum.de/data/datasets/rgbd-dataset"},
                {"label": "Replica dataset", "url": "https://github.com/facebookresearch/Replica-Dataset"},
            ],
        },
        {
            "priority": "EXPLORE",
            "title": "Uncertainty-Budgeted Active Perception",
            "thesis": (
                "보이지 않는 actor를 무한히 기억하지도, 모든 view를 계속 보지도 않고, belief uncertainty와 energy budget이 허용하는 만큼만 재관측합니다."
            ),
            "scores": {"fit": 5, "novelty": 5, "feasibility": 3, "moat": 5, "timing": 4, "evidence": 3},
            "one_week": (
                "MultiView-Bench에서 entropy, disagreement, elapsed-occlusion을 기준으로 next-view/stop/delete를 결정하는 비학습 policy를 만들고 fixed-six-view와 비교합니다."
            ),
            "four_week": (
                "nuScenes-Permanence의 occlusion duration과 edge energy predictor를 연결해 risk-weighted view/memory budget policy를 시뮬레이션합니다."
            ),
            "metric": "equal 6-view budget에서 accuracy +10p, calibration ECE -20%, 불필요 view -25%; stale FDR을 fixed persistence보다 절반으로 감소.",
            "stop": "active policy가 random view보다 5p 미만 개선하거나, energy 절감이 accuracy 10p 이상 손실을 만들면 exploratory note로 종료합니다.",
            "assets": [
                {"label": "MultiView-Bench paper", "url": "https://arxiv.org/abs/2607.08970"},
                {"label": "BeyondSight paper", "url": "https://arxiv.org/abs/2607.09138"},
                {"label": "Edge VLM energy paper", "url": "https://arxiv.org/abs/2607.09520"},
            ],
        },
    ],
}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def paper_links(paper: dict) -> str:
    links = [
        f'<a href="https://arxiv.org/abs/{esc(paper["arxiv_id"])}">abstract</a>',
        f'<a href="https://arxiv.org/pdf/{esc(paper["arxiv_id"])}">PDF</a>',
    ]
    if paper.get("project"):
        links.append(f'<a href="{esc(paper["project"])}">project</a>')
    return " · ".join(links)


def render_paper(paper: dict) -> str:
    evidence = "".join(
        f'<li><strong>{esc(item["trace"])}</strong><span>{esc(item["claim"])}</span></li>'
        for item in paper["evidence"]
    )
    fields = [
        ("1. 지배적 믿음", paper["status_quo"]),
        ("2. 관찰된 마찰", paper["friction"]),
        ("3. 숨은 전제", paper["hidden_premise"]),
        ("4. 개념적 이동", paper["conceptual_move"]),
        ("5. 작동 메커니즘", paper["mechanism"]),
    ]
    field_html = "".join(
        f'<div class="field"><h4>{esc(label)}</h4><p>{esc(text)}</p></div>' for label, text in fields
    )
    return f"""
<article class="autopsy-card" id="paper-{esc(paper['arxiv_id'])}">
  <div class="paper-top"><span class="rank">#{paper['rank']}</span><span class="tier">{esc(paper['status'])}</span></div>
  <h3>{esc(paper['title'])}</h3>
  <p class="fit">{esc(paper['fit'])} · {paper_links(paper)}</p>
  <div class="field-grid">{field_html}</div>
  <div class="evidence"><h4>6. 결정적 증거와 Evidence Trace</h4><ul>{evidence}</ul></div>
  <div class="critical-grid">
    <div><h4>7. Falsification frontier</h4><p>{esc(paper['falsification'])}</p></div>
    <div><h4>8. Adversarial read</h4><p>{esc(paper['adversarial'])}</p></div>
    <div class="tool"><h4>9. 훔칠 사고 도구</h4><p>{esc(paper['thinking_tool'])}</p></div>
    <div><h4>10. Transfer boundary</h4><p>{esc(paper['transfer_boundary'])}</p></div>
  </div>
</article>"""


def render_strategy(item: dict) -> str:
    score_names = {"fit": "Fit", "novelty": "Novelty", "feasibility": "Feasibility", "moat": "Moat", "timing": "Timing", "evidence": "Evidence"}
    score_html = "".join(
        f'<span>{score_names[key]} <b>{value}/5</b></span>' for key, value in item["scores"].items()
    )
    total = sum(item["scores"].values())
    assets = " · ".join(f'<a href="{esc(link["url"])}">{esc(link["label"])}</a>' for link in item["assets"])
    return f"""
<article class="strategy-card">
  <div class="strategy-head"><span class="priority {esc(item['priority'].lower())}">{esc(item['priority'])}</span><span class="total">총점 {total}/30</span></div>
  <h3>{esc(item['title'])}</h3><p class="thesis">{esc(item['thesis'])}</p>
  <div class="scores">{score_html}</div>
  <div class="strategy-grid">
    <div><h4>1주 probe</h4><p>{esc(item['one_week'])}</p></div>
    <div><h4>4주 build</h4><p>{esc(item['four_week'])}</p></div>
    <div><h4>Success metric</h4><p>{esc(item['metric'])}</p></div>
    <div><h4>Stop condition</h4><p>{esc(item['stop'])}</p></div>
  </div>
  <p class="assets"><strong>Paper / asset path</strong> · {assets}</p>
</article>"""


def build_html() -> str:
    decisions = "".join(
        f'<article class="theme-card"><span>{esc(item["label"])}</span><h3>{esc(item["title"])}</h3><p>{esc(item["body"])}</p></article>'
        for item in DATA["decision_cards"]
    )
    papers = "".join(render_paper(paper) for paper in DATA["papers"])
    synthesis = "".join(
        f'''<article class="synthesis-card"><h3>{esc(item["title"])}</h3><p class="links">{esc(item["links"])}</p>
        <p><strong>논문 사실</strong> · {esc(item["facts"])}</p><p><strong>APRL inference</strong> · {esc(item["inference"])}</p>
        <p class="decision"><strong>결정</strong> · {esc(item["decision"])}</p></article>'''
        for item in DATA["synthesis"]
    )
    memory = "".join(
        f'''<article class="memory-card"><span>{esc(item["signal"])}</span><h3>{esc(item["title"])}</h3>
        <p class="history">{esc(item["history"])}</p><p>{esc(item["read"])}</p></article>'''
        for item in DATA["frontier_memory"]
    )
    strategies = "".join(render_strategy(item) for item in DATA["strategy"])
    return f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="2026-07-13 arXiv Research Intelligence: full-text paper autopsies, cross-paper decisions, frontier memory, and APRL strategy board.">
<title>arXiv Research Intelligence — {DATE}</title>
<style>
:root{{--ink:#17202a;--muted:#667085;--line:#d8dee8;--navy:#15263f;--blue:#2563eb;--cyan:#0891b2;--amber:#d97706;--green:#087f5b;--red:#b42318;--paper:#f8fafc;--lav:#f5f3ff}}
*{{box-sizing:border-box}}body{{margin:0;background:#eef2f7;color:var(--ink);font:15px/1.72 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
a{{color:#075bb5;text-decoration:none}}a:hover{{text-decoration:underline}}.wrap{{max-width:1120px;margin:0 auto;background:#fff;min-height:100vh;box-shadow:0 0 40px #b9c2cf66}}
header{{padding:52px 64px 44px;background:linear-gradient(135deg,#10233f 0%,#173d5c 55%,#0d6672 100%);color:white}}
.eyebrow{{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#a5f3fc;font-weight:800}}h1{{font-size:42px;line-height:1.12;margin:10px 0 14px;letter-spacing:-.04em}}header p{{max-width:860px;color:#dbeafe;margin:0}}
.meta{{display:flex;gap:10px;flex-wrap:wrap;margin-top:22px}}.meta span,.meta a{{font-size:12px;border:1px solid #ffffff44;border-radius:999px;padding:5px 11px;color:#fff;background:#ffffff12}}
main{{padding:38px 64px 70px}}h2{{font-size:26px;margin:48px 0 18px;letter-spacing:-.025em;color:var(--navy);border-bottom:2px solid #dbe8f5;padding-bottom:8px}}h3{{line-height:1.35;letter-spacing:-.02em}}h4{{margin:0 0 5px;color:#29435f;font-size:13px}}p{{margin:5px 0 0}}.lead{{font-size:18px;line-height:1.75;color:#24364b;padding:20px 24px;background:#eff8ff;border-left:5px solid var(--cyan);border-radius:0 12px 12px 0}}
.scope{{font-size:13px;color:var(--muted);margin:12px 0 0}}.decision-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}.theme-card{{border:1px solid #c9d8e8;border-radius:14px;padding:18px;background:linear-gradient(180deg,#fff,#f7fbff)}}.theme-card>span{{font-size:11px;font-weight:800;color:var(--cyan);text-transform:uppercase;letter-spacing:.1em}}.theme-card h3{{font-size:17px;margin:7px 0}}.theme-card p{{font-size:14px;color:#40546a}}
.autopsy-card{{border:1px solid var(--line);border-radius:18px;padding:26px;margin:18px 0 26px;background:#fff;box-shadow:0 8px 24px #1d29390a}}.paper-top{{display:flex;justify-content:space-between;gap:10px}}.rank{{font-size:28px;font-weight:900;color:#b7c4d4}}.tier{{font-size:11px;font-weight:750;border-radius:999px;padding:5px 10px;color:#075985;background:#e0f2fe;align-self:center}}.autopsy-card h3{{font-size:23px;margin:6px 0}}.fit{{color:var(--muted);font-size:13px;margin-bottom:18px}}.field-grid{{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--line);border:1px solid var(--line);border-radius:12px;overflow:hidden}}.field{{background:#fff;padding:15px 17px}}.field p,.critical-grid p{{font-size:14px;color:#34475c}}.evidence{{margin:16px 0;padding:16px 18px;background:#f8fafc;border-radius:12px;border:1px solid #e4e7ec}}.evidence ul{{margin:8px 0 0;padding-left:20px}}.evidence li{{margin:8px 0}}.evidence strong{{display:block;font-size:12px;color:#075985}}.evidence span{{font-size:14px}}.critical-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}.critical-grid>div{{border:1px solid #e4e7ec;border-radius:12px;padding:15px 17px;background:#fff}}.critical-grid .tool{{background:#fff9e8;border-color:#f3ce71}}.critical-grid .tool h4{{color:#92400e}}
.synthesis-grid,.memory-grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}.synthesis-card,.memory-card{{border:1px solid var(--line);border-radius:14px;padding:18px}}.synthesis-card h3,.memory-card h3{{font-size:17px;margin:0 0 7px}}.synthesis-card p,.memory-card p{{font-size:14px;color:#3c5065}}.links{{color:var(--cyan)!important;font-weight:750}}.decision{{margin-top:10px!important;padding:9px 11px;background:#ecfdf3;border-radius:8px;color:#07613f!important}}.memory-card>span{{font-size:11px;font-weight:800;padding:3px 8px;background:#ede9fe;color:#5b21b6;border-radius:999px}}.memory-card .history{{color:#64748b;font-size:12px}}
.strategy-card{{border:1px solid #cfd8e4;border-radius:18px;padding:24px;margin:16px 0;background:linear-gradient(145deg,#fff,#fafcff)}}.strategy-head{{display:flex;justify-content:space-between}}.priority{{font-size:11px;font-weight:900;letter-spacing:.12em;border-radius:999px;padding:5px 10px}}.priority.build{{background:#dcfce7;color:#166534}}.priority.exploit{{background:#dbeafe;color:#1d4ed8}}.priority.explore{{background:#fef3c7;color:#92400e}}.total{{font-weight:850;color:#475569}}.strategy-card h3{{font-size:22px;margin:10px 0 4px}}.thesis{{font-size:15px;color:#34475c}}.scores{{display:flex;gap:8px;flex-wrap:wrap;margin:15px 0}}.scores span{{font-size:11px;background:#eef2f6;padding:4px 8px;border-radius:6px}}.strategy-grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}.strategy-grid>div{{border-top:1px solid #dce3ea;padding:12px 8px}}.strategy-grid p{{font-size:14px;color:#40546a}}.assets{{font-size:13px;margin-top:12px;padding:10px 12px;background:#f4f7fa;border-radius:8px}}
.method-note{{margin-top:48px;padding:16px 18px;border:1px dashed #aab7c4;border-radius:12px;color:#596b7e;font-size:13px}}footer{{padding:25px 64px;background:#10233f;color:#c7d2e0;font-size:12px}}footer a{{color:#a5f3fc}}
@media(max-width:800px){{header,main,footer{{padding-left:24px;padding-right:24px}}h1{{font-size:32px}}.decision-grid,.field-grid,.critical-grid,.synthesis-grid,.memory-grid,.strategy-grid{{grid-template-columns:1fr}}}}
@media print{{body{{background:#fff}}.wrap{{box-shadow:none}}a{{color:inherit}}}}
</style></head><body><div class="wrap">
<header><div class="eyebrow">APRL · ARXIV RESEARCH INTELLIGENCE</div><h1>{DATE} 심층판</h1>
<p>논문들의 결론을 요약하는 대신, 문제를 보는 방식·숨은 전제·결정적 실험·실패 경계를 역설계합니다.</p>
<div class="meta"><span>Tier A 5편 full-text</span><span>Evidence Trace 포함</span><span>Frontier memory 4주</span><span>Strategy Board 3건</span><a href="{DATE}.html">기존 오늘자 브리핑 ↗</a><a href="../">아카이브 ↗</a></div></header>
<main>
<h2>🔭 주간 동향을 넘어: 오늘의 판단</h2><p class="lead">{esc(DATA['executive_thesis'])}</p><p class="scope">{esc(DATA['scope_note'])}</p>
<div class="decision-grid">{decisions}</div>
<h2>🧠 Paper Reasoning Autopsy</h2>{papers}
<h2>🔗 Cross-paper decision synthesis</h2><div class="synthesis-grid">{synthesis}</div>
<h2>🛰 Frontier memory · 최근 4주</h2><div class="memory-grid">{memory}</div>
<h2>🚀 Leading Group Strategy Board</h2>{strategies}
<div class="method-note"><strong>작성 규칙</strong> · 공식 arXiv PDF의 본문·표·부록을 Tier A evidence로 사용했습니다. 논문 수치와 저자 한계는 Verified/Author claim으로 표시하고, APRL의 전략적 연결은 inference로 분리했습니다. 활성 프롬프트: <a href="../{esc(DATA['source_prompt'])}">{esc(DATA['source_prompt'])}</a>. 구조화 원본: <a href="../intelligence/{DATE}.json">intelligence/{DATE}.json</a>.</div>
</main><footer>Generated as a separate Research Intelligence edition. Existing daily post remains unchanged. · <a href="https://github.com/gisbi-kim/arxiv-daily-summary">GitHub repository</a></footer>
</div></body></html>"""


def main() -> None:
    json_dir = ROOT / "intelligence"
    json_dir.mkdir(exist_ok=True)
    json_path = json_dir / f"{DATE}.json"
    html_path = ROOT / "posts" / f"{SLUG}.html"
    json_path.write_text(json.dumps(DATA, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    html_path.write_text(build_html(), encoding="utf-8")
    print(f"wrote {json_path.relative_to(ROOT)}")
    print(f"wrote {html_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
