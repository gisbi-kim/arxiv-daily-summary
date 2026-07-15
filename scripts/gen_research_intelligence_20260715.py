#!/usr/bin/env python3
"""Generate the full-text Research Intelligence edition for 2026-07-15."""

from __future__ import annotations

import json
from pathlib import Path

import gen_research_intelligence_20260713 as template


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-07-15"
SLUG = f"{DATE}-research-intelligence"


DATA = {
    "date": DATE,
    "edition": "Research Intelligence",
    "source_prompt": "prompts/instruction_v20260713.md",
    "scope_note": (
        "당일 cs.CV/cs.RO /new 247편을 dedup하고 121편을 ROI로 분류했습니다. Tier A 6편은 공식 arXiv HTML 원문에서 "
        "본문·표·그림·제한점을 확인했습니다. Verified는 논문에서 직접 확인한 사실, Inference는 APRL 관점의 해석입니다."
    ),
    "executive_thesis": (
        "오늘 강한 논문들은 모델을 더 크게 만드는 대신, 로봇 시스템이 실패하는 시간·공간·평가 계약을 다시 정의합니다. "
        "Jetson-PI와 temporal-redundancy VLA는 VLA inference를 평균 latency가 아니라 action chunk가 실행될 미래 상태와 맞추는 문제로 바꾸고, "
        "TrustVLA는 backdoor 방어를 입력 정화가 아니라 clean-calibrated evidence geometry 감시로 바꿉니다. DiffRadar, PixelLoop, TerraZero, "
        "temporal benchmark audit는 각각 센서 물리, topological shortcut, procedural long-tail, 시간 채널을 평가 안으로 끌어들입니다. APRL에는 "
        "새 backbone보다 failure가 생기는 coordinate, clock, evaluator를 소유하는 것이 더 방어력 있는 연구 자산입니다."
    ),
    "decision_cards": [
        {
            "title": "판세 1 · VLA 속도는 compression 문제가 아니라 clock alignment 문제다",
            "body": (
                "Reducing Temporal Redundancy와 Jetson-PI는 모두 계산량을 줄이지만, 핵심은 단순 pruning이 아닙니다. "
                "visual token, flow step, future latent, scheduler threshold를 control-loop deadline과 묶어야 실제 task success가 유지됩니다."
            ),
            "label": "Decision",
        },
        {
            "title": "판세 2 · 보안과 평가의 단위가 output에서 evidence trace로 내려온다",
            "body": (
                "TrustVLA와 temporal benchmark audit는 최종 성공률이 같은 시스템도 내부 evidence channel이 다를 수 있음을 보여줍니다. "
                "APRL의 benchmark도 success/fail 전에 어떤 sensor, token, evaluator 계약이 결정을 만들었는지 분리해야 합니다."
            ),
            "label": "Decision",
        },
        {
            "title": "판세 3 · Geometry는 예쁜 reconstruction보다 downstream control edge다",
            "body": (
                "DiffRadar와 PixelLoop는 map을 시각 품질이 아니라 pose, shortcut, cost propagation, loop drift로 평가합니다. "
                "3D representation 연구도 robot-usable validity를 먼저 정의해야 합니다."
            ),
            "label": "Decision",
        },
    ],
    "papers": [
        {
            "rank": 1,
            "title": "Jetson-PI: Towards Onboard Real-Time Robot Control via Foresight-Aligned Asynchronous Inference",
            "arxiv_id": "2607.12659",
            "project": "https://github.com/PKU-SEC-Lab/Jetson-PI",
            "fit": "VLA deployment · onboard inference · control-loop timing",
            "status": "Tier A · 공식 arXiv HTML 확인",
            "status_quo": (
                "VLA deployment는 큰 GPU에서 latency를 줄이거나 asynchronous inference로 다음 chunk를 미리 계산하면 된다는 믿음이 강했습니다."
            ),
            "friction": (
                "Jetson Orin에서는 π0.5 inference가 약 1.4초까지 느려져 control frequency가 0.7Hz 수준으로 떨어지고, "
                "비동기 실행은 오래된 관측으로 미래 action을 예측해 perception-execution misalignment를 만듭니다 [Sec. 1][Fig. 1]."
            ),
            "hidden_premise": (
                "낮은 latency 자체보다 중요한 것은 action expert가 실제 실행 시점의 환경 latent를 보도록 만드는 것입니다 [Inference]."
            ),
            "conceptual_move": (
                "현재 observation에서 바로 다음 chunk를 만들지 않고, 이미 committed action을 조건으로 future VLM representation을 예측한 뒤 "
                "action expert가 미래 time step부터 action을 생성하게 합니다 [Sec. 4][Fig. 4]."
            ),
            "mechanism": (
                "future correction module, confidence-based scheduling, CUDA graph reuse, GPU-resident buffering, flow unrolling을 결합해 "
                "VLM 호출 빈도와 action-head 반복을 동시에 줄입니다 [Sec. 4][Table 4]."
            ),
            "evidence": [
                {
                    "trace": "Sec. 5.1 / Table 3 [Verified]",
                    "claim": "LIBERO 네 sub-dataset과 여러 inference delay에서 Jetson-PI는 VLASH보다 평균 success rate를 14.8%, RTC보다 3.9% 높였고, Δ=9에서는 VLASH 대비 45.6%p 차이가 났습니다.",
                },
                {
                    "trace": "Sec. 5.2 / Table 4 [Verified]",
                    "claim": "Jetson Orin에서 naive PyTorch 대비 control frequency가 8.66배, vla.cpp 대비 5.41배 개선됐고, graph reuse와 buffering/unrolling이 reaction time을 줄였습니다.",
                },
                {
                    "trace": "Sec. 5.3 / Fig. 7-8 [Verified]",
                    "claim": "X2-W robot의 cloth-folding task에서 Jetson Orin 배포를 실험했고, threshold sweep은 VLM 호출 빈도와 prediction error 사이 trade-off를 보여줍니다.",
                },
                {
                    "trace": "Limitations [Author claim]",
                    "claim": "저자들은 onboard compute와 bandwidth 제약이 고성능 GPU cluster와의 간극을 완전히 닫지는 못한다고 인정합니다.",
                },
            ],
            "falsification": (
                "동일 control frequency에서 stale-observation baseline이나 state-only forecast가 같은 success를 내면 future VLM latent가 아니라 scheduling/system optimization만 원인일 수 있습니다."
            ),
            "adversarial": (
                "LIBERO와 한 real task 중심이며, real robot 반복 수와 dynamic disturbance sweep이 제한적입니다. future correction error가 contact-rich task에서 누적될 위험도 남습니다."
            ),
            "thinking_tool": (
                "VLA latency를 ms 단위 최적화가 아니라 observation timestamp, committed action, future latent, control deadline의 정렬 문제로 재정의합니다."
            ),
            "transfer_boundary": (
                "예측 가능한 action chunk와 calibrated camera stream에는 강하지만, 급격한 external intervention, high-frequency force control, long-horizon replanning에는 별도 fail-safe가 필요합니다."
            ),
        },
        {
            "rank": 2,
            "title": "TrustVLA: Mechanism-Guided Inference-Time Defense Against Vision-Language-Action Backdoors",
            "arxiv_id": "2607.12571",
            "fit": "VLA security · inference-time monitor · backdoor recovery",
            "status": "Tier A · 공식 arXiv HTML 확인",
            "status_quo": (
                "VLA backdoor 방어는 입력 전체를 변형하거나 checkpoint를 고치는 classifier식 repair로 접근하기 쉽습니다."
            ),
            "friction": (
                "backdoored VLA는 clean observation에서 정상적으로 보이다가 작은 trigger가 long-horizon action sequence를 틀어도, output-only monitor는 너무 늦게 반응합니다 [Sec. 1]."
            ),
            "hidden_premise": (
                "visual trigger가 성공하려면 compact support가 hidden-state evidence geometry를 clean calibration region 밖으로 밀어내야 한다는 가설을 둡니다 [Definition 1][Inference]."
            ),
            "conceptual_move": (
                "trigger를 사전에 알지 않고, per-token per-layer Dirichlet evidence trajectory가 clean-calibrated operating region을 벗어나는지 감시한 뒤 "
                "counterfactual masking으로 causal support를 검증합니다 [Sec. 3][Fig. 2-4]."
            ),
            "mechanism": (
                "epistemic homogenization, attention rank promotion, mechanism-score drop을 연결해 detection, localization, inpainting recovery를 분리합니다. "
                "threshold는 clean calibration episodes에서 고정합니다 [Sec. 3][Appendix B]."
            ),
            "evidence": [
                {
                    "trace": "Sec. 4 / Table 1 [Verified]",
                    "claim": "OpenVLA/LIBERO main rows는 clean/triggered 각각 500 episodes로 clean success, triggered recovery, residual VLA-ASR를 분리해 보고합니다.",
                },
                {
                    "trace": "Fig. 3-4 [Verified]",
                    "claim": "BadVLA와 INFUSE 모두 triggered state에서 late-layer uncertainty compression과 trigger-neighborhood attention support가 나타나지만, attention은 causal proof가 아니라 candidate proposal로만 씁니다.",
                },
                {
                    "trace": "Appendix / Tables 18-21 [Verified]",
                    "claim": "INFUSE Stage-II clean fine-tuned checkpoints에서도 triggered detection은 500/500에 도달했고, final causal-closure recovery는 Spatial/Object/Goal/LIBERO-10에서 487/500, 487/500, 467/500, 433/500을 보였습니다.",
                },
                {
                    "trace": "Limitations / failure taxonomy [Verified]",
                    "claim": "global filter나 task object에 붙은 semantic trigger는 automatic recovery보다 fail-safe halt가 기대 동작이라고 명시합니다.",
                },
            ],
            "falsification": (
                "adaptive attacker가 clean evidence trajectory, compact support score-drop, high clean SR, high triggered ASR를 동시에 만족하면 TrustVLA의 mechanism hypothesis가 약해집니다."
            ),
            "adversarial": (
                "평가된 trigger family는 localizable visual support 중심입니다. inpainting이 task context를 훼손하는 multi-object clutter에서는 recovery 실패가 남고, 인증 방어는 아닙니다."
            ),
            "thinking_tool": (
                "보안 문제를 입력 변형 recipe가 아니라 clean-calibrated evidence geometry와 causal support localization 문제로 바꿉니다."
            ),
            "transfer_boundary": (
                "hidden-state 접근이 가능한 open VLA에는 유효하지만 closed proprietary policy, global style trigger, semantic object trigger에는 detection-only fail-safe로 낮춰야 합니다."
            ),
        },
        {
            "rank": 3,
            "title": "Reducing Temporal Redundancy for Efficient Vision-Language-Action Inference",
            "arxiv_id": "2607.12287",
            "fit": "VLA acceleration · token reuse · flow-step compression",
            "status": "Tier A · 공식 arXiv HTML 확인",
            "status_quo": (
                "VLA acceleration은 vision encoder pruning이나 lightweight architecture처럼 한 module의 계산량을 줄이는 문제로 다뤄지는 경우가 많습니다."
            ),
            "friction": (
                "실시간 manipulation에서는 visual encoding과 flow/diffusion action head가 모두 반복 계산을 만들고, 한쪽만 줄이면 병목이 다른 쪽으로 이동합니다 [Sec. 1]."
            ),
            "hidden_premise": (
                "연속 frame의 대부분 visual token과 flow velocity update는 독립 정보가 아니라 시간적으로 중복된 계산이라는 전제를 둡니다 [Fig. 1]."
            ),
            "conceptual_move": (
                "adjacent frame에서 바뀐 token만 갱신하고 나머지는 cached KV를 재사용하며, flow matching policy를 10-step에서 compact 2-step schedule로 압축합니다 [Sec. III]."
            ),
            "mechanism": (
                "첫 transformer layer의 cosine similarity로 dynamic token subset을 고르고, 같은 index를 후속 layer에 재사용합니다. action head에서는 velocity trajectory의 low-rank structure를 이용합니다 [Fig. 1-2]."
            ),
            "evidence": [
                {
                    "trace": "Table I / Sec. IV-B [Verified]",
                    "claim": "π0.5에 적용했을 때 mean success rate 93.8%를 유지하면서 sampling을 10 step에서 2 step으로 줄이고 latency를 286.9ms에서 121.2ms로 낮췄습니다.",
                },
                {
                    "trace": "Table II-III / Sec. IV-D [Verified]",
                    "claim": "TokenReuse는 ViT latency를 40.1ms에서 28.5ms로 줄였고, Efficient Policy는 Action Expert latency를 212.6ms에서 41.5ms로 줄였습니다.",
                },
                {
                    "trace": "Table IV / Fig. 5 [Verified]",
                    "claim": "real robot six tasks에서 2-step policy는 overall success 95.4% vs 97.2%로 유사했고, time-constrained SR@30s는 77.1%에서 82.3%로 올랐습니다.",
                },
                {
                    "trace": "Conclusion / Limitations [Author claim]",
                    "claim": "저자들은 짧은 horizon manipulation 중심 검증이라 long-horizon planning과 highly dynamic environment는 추가 검증이 필요하다고 둡니다.",
                },
            ],
            "falsification": (
                "dynamic scene perturbation과 contact-rich long horizon에서 token reuse가 failure를 만들거나 2-step flow가 boundary jitter를 키우면 redundancy 가설은 deployment에서 제한됩니다."
            ),
            "adversarial": (
                "주요 simulation은 A100, real-world는 RTX 4090에서 돌아갑니다. edge deployment와 sensor jitter, actuator latency가 결합된 조건은 Jetson-PI류 실험과 별도로 봐야 합니다."
            ),
            "thinking_tool": (
                "계산량을 module별로 줄이지 말고 perception token, action solver step, task deadline을 같은 latency-success Pareto surface에 올립니다."
            ),
            "transfer_boundary": (
                "slowly changing tabletop streams와 flow-based policy에는 적합하지만, fast occlusion, deformable contact, moving camera에서는 update ratio를 adaptive하게 둬야 합니다."
            ),
        },
        {
            "rank": 4,
            "title": "DiffRadar: Differentiable Physics-Aware Radar SLAM with Gaussian Fields",
            "arxiv_id": "2607.12265",
            "fit": "radar SLAM · differentiable sensor physics · Gaussian maps",
            "status": "Tier A · 공식 arXiv HTML 확인",
            "status_quo": (
                "radar SLAM은 RA/DA heatmap이나 point feature를 추출한 뒤 scan matching이나 learned odometry로 motion을 맞추는 pipeline으로 읽히기 쉽습니다."
            ),
            "friction": (
                "poor lighting/weather에서는 radar가 강하지만, scan-matching pipeline은 lateral structure 부족, dynamic clutter, loop drift에서 불안정합니다 [Sec. 7.3]."
            ),
            "hidden_premise": (
                "radar return은 image-like feature가 아니라 sensor physics와 scene structure가 함께 만든 measurement이므로, forward model을 optimization 안에 넣어야 합니다 [Inference]."
            ),
            "conceptual_move": (
                "FMCW-consistent differentiable radar renderer와 dynamic Gaussian map을 fixed-lag SLAM optimizer로 결합해 pose와 map을 jointly refine합니다 [Sec. 6-7]."
            ),
            "mechanism": (
                "각 scatterer를 position, anisotropic covariance, reflectivity를 가진 Gaussian primitive로 두고 RA/DA residual, Doppler, visibility gating을 함께 씁니다 [Sec. 6]."
            ),
            "evidence": [
                {
                    "trace": "Table 6 / Sec. 7.3 [Verified]",
                    "claim": "100m 이상 loop-closure trajectory에서 cart-mounted loop drift가 20.44m/100m에서 0.51m/100m로, ATE가 2.92m에서 0.017m로 줄었습니다.",
                },
                {
                    "trace": "Table 8 / Sec. 7.3.2 [Verified]",
                    "claim": "RDST map fidelity에서 map consistency가 43%에서 95%로 두 배 이상 상승하고 loop drift와 vertical artifact가 함께 감소했습니다.",
                },
                {
                    "trace": "Table 10 / Sec. 7.4 [Verified]",
                    "claim": "Doppler residual 제거는 translation accuracy를 크게 망치고, RA residual 제거는 translation과 orientation 모두를 악화시켜 두 measurement가 상보적임을 보입니다.",
                },
                {
                    "trace": "Limitations [Author claim]",
                    "claim": "특정 FMCW radar configuration과 calibration에 맞춰져 있으며, dense moving object 환경은 여전히 pose estimation을 흔들 수 있습니다.",
                },
            ],
            "falsification": (
                "다른 radar hardware, calibration drift, dense dynamic crowd에서 visibility-conditioned Gaussian field가 scan matching보다 안정적이지 않으면 physics-aware prior의 범위가 좁습니다."
            ),
            "adversarial": (
                "commodity radar 한 계열과 controlled stress suite 중심입니다. 카메라/LiDAR와 결합한 downstream navigation success까지 직접 닫지는 않습니다."
            ),
            "thinking_tool": (
                "sensor를 feature extractor로 보지 말고, 실패 mode를 만드는 physics를 differentiable map representation 안으로 끌어옵니다."
            ),
            "transfer_boundary": (
                "radar-only low-visibility SLAM에는 강하지만, robot task에서 map을 쓰려면 localization drift와 navigation recovery까지 함께 검증해야 합니다."
            ),
        },
        {
            "rank": 5,
            "title": "TerraZero: Procedural Driving Simulation for Zero-Demonstration Self-Play at Scale",
            "arxiv_id": "2607.13028",
            "fit": "autonomous driving · procedural simulation · self-play RL",
            "status": "Tier A · 공식 arXiv HTML 확인",
            "status_quo": (
                "자율주행 policy 학습은 logged trajectory imitation이나 reference-anchored self-play가 현실성을 보장한다는 전제에 기대기 쉽습니다."
            ),
            "friction": (
                "배포 readiness를 결정하는 dense merge, jaywalker, crash, construction 같은 long-tail interaction은 logged data에서 희귀하고 수동 scenario 작성도 불완전합니다 [Sec. 1]."
            ),
            "hidden_premise": (
                "픽셀 realism보다 object-level closed-loop throughput과 scenario configurability가 RL policy의 long-tail exposure를 결정한다는 전제입니다 [Inference]."
            ),
            "conceptual_move": (
                "C engine과 zero-copy GPU training loop로 heterogeneous agents, traffic rules, multiple dynamics, procedural road users를 조합하고, 모든 reported policy를 demonstration 없이 self-play RL로 학습합니다 [Sec. 3-5]."
            ),
            "mechanism": (
                "Waymo, nuPlan, CARLA map을 공통 binary scenario format으로 변환하고, saliency-prioritized sampling, V-trace, PopArt, reward/kinematic randomization, population play를 씁니다 [Fig. 2-4]."
            ),
            "evidence": [
                {
                    "trace": "Abstract / Table 1 [Verified]",
                    "claim": "single server-grade GPU에서 1.3M agent-steps/s, 8-GPU node에서 최대 2.8M agent-steps/s를 보고하며 heterogeneous agents와 traffic-rule enforcement를 유지합니다.",
                },
                {
                    "trace": "Sec. 6 / Tables 4-6 [Verified]",
                    "claim": "WOSAC 2023에서 Gigaflow보다 overall realism이 0.632 vs 0.619로 높고, 2024 vehicle/VRU 설정에서도 demonstration-free baseline 대비 경쟁력을 보입니다.",
                },
                {
                    "trace": "Sec. 6.5 / Fig. 6 [Verified]",
                    "claim": "nuPlan map geometry만 학습한 policy가 Waymo WOSAC protocol에서 Waymo-trained policy와 거의 같은 vehicle realism 0.732 vs 0.740, VRU realism 0.683 vs 0.683을 보였습니다.",
                },
                {
                    "trace": "Limitations [Author claim]",
                    "claim": "저자들은 visual perception pipeline과 통합해야 object-level observation과 end-to-end driving 사이 간극을 줄일 수 있다고 명시합니다.",
                },
            ],
            "falsification": (
                "object-level realism이 pixel/perception error와 결합될 때 safety gain을 잃거나, generated long-tail이 실제 logged rare case와 다른 failure를 만들면 simulator asset의 전이가 약해집니다."
            ),
            "adversarial": (
                "closed-loop interaction과 throughput은 강하지만, perception stack은 ground-truth object state에 가깝습니다. full-stack robot autonomy에는 sensor corruption과 perception latency가 빠져 있습니다."
            ),
            "thinking_tool": (
                "long-tail을 더 모으는 문제가 아니라, 어떤 scenario axes를 조합하면 policy가 스스로 harder opponent를 만들게 되는지 설계합니다."
            ),
            "transfer_boundary": (
                "object-level driving policy와 sim-agent training에는 적합하지만 camera/LiDAR perception, map conversion artifacts, human-likeness metric에는 별도 validation이 필요합니다."
            ),
        },
        {
            "rank": 6,
            "title": "What Does a Temporal Benchmark Score Measure? Decomposing Channel Use in Video VLM Evaluation",
            "arxiv_id": "2607.12304",
            "fit": "video VLM evaluation · temporal channel audit · benchmark validity",
            "status": "Tier A · 공식 arXiv HTML 확인",
            "status_quo": (
                "temporal video benchmark score는 모델이 frame order와 motion을 이해한다는 단일 지표처럼 해석됩니다."
            ),
            "friction": (
                "multi-frame gain과 frame-shuffle sensitivity는 task가 여러 frame을 필요로 하는지 말해줄 뿐, 모델이 order를 pixel sequence, timestamp, RoPE 중 무엇에서 읽는지는 말하지 않습니다 [Sec. 1]."
            ),
            "hidden_premise": (
                "같은 accuracy를 가진 두 VLM도 시간 순서를 읽는 내부 channel이 다르면 배포 failure mode가 완전히 다를 수 있습니다 [Inference]."
            ),
            "conceptual_move": (
                "visual frame order, in-context timestamp, RoPE position을 독립적으로 뒤섞고 conflict condition을 만들어 channel question을 분리합니다 [Fig. 1]."
            ),
            "mechanism": (
                "rev-corr condition에서는 pixels는 reversed event를, RoPE는 forward order를 가리키게 하고, paired reverse ground truth 또는 reversal-drop으로 모델이 어느 channel을 따르는지 봅니다 [Sec. 3.5]."
            ),
            "evidence": [
                {
                    "trace": "Sec. 4.3 / Tables 24-26 [Verified]",
                    "claim": "TempCompass conflict에서 Molmo2는 RoPE가 가리키는 forward event를, Qwen3-VL은 reversed pixels가 보이는 event를 따르는 family split을 보였습니다.",
                },
                {
                    "trace": "TVBench results [Verified]",
                    "claim": "TVBench temporal tasks에서도 Molmo의 reversal drop은 약 +0.04로 작고, Qwen-8B overall은 0.558에서 0.333으로 무너져 같은 dissociation이 반복됐습니다.",
                },
                {
                    "trace": "Probe / Table 14-16 [Verified]",
                    "claim": "shuf-corr에서 frame identity recovery gap closed는 Molmo 4B/8B/O-7B가 74%/64%/30%, Qwen 4B/8B가 17%/20%로 달라 behavioral split과 맞았습니다.",
                },
                {
                    "trace": "Limitations / Recommendations [Author claim]",
                    "claim": "test는 open models의 internals가 필요하며, diagnostic은 aggregate score 대체가 아니라 score가 무엇을 측정하는지 밝히는 audit로 제안됩니다.",
                },
            ],
            "falsification": (
                "다른 benchmark와 architecture에서 channel conflict가 aggregate score와 같은 ranking만 내면, reversal-drop의 추가 정보는 제한됩니다."
            ),
            "adversarial": (
                "open-model internal manipulation이 필요해 closed commercial systems에는 바로 적용하기 어렵고, conflict condition 자체가 out-of-distribution일 수 있습니다."
            ),
            "thinking_tool": (
                "benchmark 점수를 능력의 총량으로 보지 말고 task question과 channel question을 나누어 실패가 어느 입력 경로에서 생기는지 측정합니다."
            ),
            "transfer_boundary": (
                "video VLM과 embodied memory benchmark에는 유용하지만, robot closed-loop 평가에서는 temporal channel이 action latency와 sensor timestamp까지 포함하도록 확장해야 합니다."
            ),
        },
    ],
    "synthesis": [
        {
            "title": "Runtime research decision: action은 현재가 아니라 실행될 미래와 정렬한다",
            "links": "Jetson-PI · Reducing Temporal Redundancy · ChunkFlow",
            "facts": (
                "Jetson-PI는 future latent와 scheduling으로 control frequency를 높였고, temporal-redundancy VLA는 token reuse와 2-step policy로 latency를 줄였습니다."
            ),
            "inference": (
                "두 논문은 모두 VLA runtime을 compression recipe가 아니라 action chunk boundary와 observation timestamp를 맞추는 system identification 문제로 만듭니다."
            ),
            "decision": "APRL은 VLA benchmark에 latency, jitter, chunk boundary, failure warning lead time을 독립 변수로 넣어야 합니다.",
        },
        {
            "title": "Geometry research decision: map quality를 planning cost와 loop drift로 재정의한다",
            "links": "DiffRadar · PixelLoop · X-Lens · VistaVLA",
            "facts": (
                "DiffRadar는 radar physics-aware Gaussian map으로 loop drift를 줄였고, PixelLoop는 dense pixel-level closures로 SPL-A를 크게 높였습니다."
            ),
            "inference": (
                "3D representation의 승부는 rendering fidelity보다 robot이 localize, shortcut, recover, navigate할 때 어떤 cost를 바꾸는지에 있습니다."
            ),
            "decision": "3D/SLAM 실험은 visual metric 옆에 ATE, loop drift, costmap MAE, downstream navigation success를 기본 축으로 둡니다.",
        },
        {
            "title": "Evaluation research decision: score가 아니라 score를 만든 channel을 감사한다",
            "links": "TrustVLA · Temporal Benchmark Audit · WSI Leakage Audit",
            "facts": (
                "TrustVLA는 hidden evidence geometry를 감시하고, temporal audit는 동일 score의 모델이 서로 다른 temporal channel을 쓰는 것을 보였습니다."
            ),
            "inference": (
                "평균 success가 같아도 내부 channel, data provenance, evaluator contract가 다르면 배포 위험은 다릅니다."
            ),
            "decision": "APRL은 benchmark release마다 model failure와 evaluator/data failure를 분리하는 audit sheet를 같이 냅니다.",
        },
    ],
    "frontier_memory": [
        {
            "signal": "강화 중",
            "title": "VLA runtime이 7월 14일 latency-aware execution 흐름에서 더 구체화",
            "history": "전날 Stop-to-Decide, HUMA, runtime control-loop 논문들이 느린 reasoning과 빠른 control을 분리했습니다.",
            "read": "오늘은 Jetson-PI와 temporal-redundancy VLA가 onboard device, token reuse, solver step으로 같은 질문을 실제 deployment budget까지 내렸습니다.",
        },
        {
            "signal": "새로운 통합",
            "title": "VLA security가 backdoor trigger 위치보다 evidence geometry로 이동",
            "history": "최근 safety cluster는 confidence calibration과 evaluator contract가 중심이었습니다.",
            "read": "TrustVLA는 clean success를 보존한 채 triggered hidden-state geometry를 감시하므로, robot safety를 output metric 이전의 internal evidence contract로 확장합니다.",
        },
        {
            "signal": "강화 중",
            "title": "Robot-usable geometry가 radar, topological loop, heterogeneous camera로 확장",
            "history": "6월 말 이후 3DGS/SLAM/reconstruction watch lens가 visual fidelity보다 localization/navigation validity를 요구했습니다.",
            "read": "DiffRadar와 PixelLoop는 sensor physics와 pixel-level closure가 downstream path cost를 바꿀 때만 representation 가치가 생긴다는 신호를 강화합니다.",
        },
        {
            "signal": "긴장 관계",
            "title": "Evaluation audit가 점점 강하지만 실험비를 늘린다",
            "history": "v20260713 prompt는 Evidence Trace와 Insight Depth Gate를 release 조건으로 올렸습니다.",
            "read": "temporal channel audit와 WSI leakage audit는 benchmark 신뢰성을 높이지만, 매일 브리핑 자동화에는 원문·데이터 provenance 확인 비용이 빠르게 커집니다.",
        },
        {
            "signal": "비어 있음",
            "title": "Failure monitors와 map representations를 하나의 robot stack에서 닫는 논문은 아직 적다",
            "history": "runtime, security, geometry가 각각 강해졌지만 한 시스템에서 동시에 닫힌 증거는 드뭅니다.",
            "read": "APRL의 기회는 VLA runtime monitor, geometry map, evaluator audit를 같은 closed-loop manipulation/navigation benchmark에 묶는 데 있습니다.",
        },
    ],
    "strategy": [
        {
            "priority": "BUILD",
            "title": "Clock-Aligned VLA Deployment Harness",
            "thesis": (
                "VLA policy를 모델 정확도만이 아니라 latency, chunk boundary, future-state mismatch, failure-warning lead time으로 평가하는 edge deployment harness를 소유합니다."
            ),
            "scores": {"fit": 5, "novelty": 4, "feasibility": 5, "moat": 5, "timing": 5, "evidence": 5},
            "one_week": (
                "LIBERO/RoboCasa에서 π0.5 또는 OpenVLA wrapper에 artificial latency, jitter, chunk overlap, token reuse ratio를 주고 success, SR@30s, boundary jitter, recovery delay를 측정합니다."
            ),
            "four_week": (
                "Jetson Orin 또는 동일 전력 budget PC에서 future-state predictor, pause-and-decide, token reuse, confidence scheduler를 factorial하게 비교하는 공개 harness를 만듭니다."
            ),
            "metric": "baseline 대비 SR@30s +10%, boundary jitter -30%, failure-warning lead time ≥2 control ticks, clean success drop <3%.",
            "stop": "latency perturbation이 task outcome을 5% 미만만 바꾸거나 hardware replication에서 순위가 뒤집히면 독립 paper path를 멈춥니다.",
            "assets": [
                {"label": "Jetson-PI", "url": "https://arxiv.org/abs/2607.12659"},
                {"label": "Temporal redundancy VLA", "url": "https://arxiv.org/abs/2607.12287"},
                {"label": "ChunkFlow", "url": "https://arxiv.org/abs/2607.12992"},
            ],
        },
        {
            "priority": "EXPLOIT",
            "title": "Robot-Usable Geometry Validity Protocol",
            "thesis": (
                "3D/SLAM/map representation을 rendering score가 아니라 localization, loop drift, path cost, dynamic recovery, downstream task success로 평가하는 protocol을 만듭니다."
            ),
            "scores": {"fit": 5, "novelty": 4, "feasibility": 4, "moat": 5, "timing": 5, "evidence": 5},
            "one_week": (
                "DiffRadar/PixelLoop/X-Lens/VistaVLA의 metric을 공통 schema로 정리하고, 기존 APRL navigation logs에서 ATE, loop drift, costmap error, downstream failure를 같이 산출합니다."
            ),
            "four_week": (
                "point-cloud map, Gaussian map, feature-field map을 동일 trajectory와 dynamic-object corruption에서 비교하는 robot-usable geometry benchmark를 구현합니다."
            ),
            "metric": "visual score와 task success의 rank inversion 2건 이상 발견, corruption별 failure taxonomy precision ≥90%, public protocol 재현성 확보.",
            "stop": "map representation 차이가 downstream success보다 sensor calibration 차이에만 설명되면 paper claim을 protocol/tool note로 낮춥니다.",
            "assets": [
                {"label": "DiffRadar", "url": "https://arxiv.org/abs/2607.12265"},
                {"label": "PixelLoop", "url": "https://arxiv.org/abs/2607.12811"},
                {"label": "X-Lens", "url": "https://arxiv.org/abs/2607.12993"},
            ],
        },
        {
            "priority": "EXPLORE",
            "title": "Evidence-Channel Audit for Embodied Benchmarks",
            "thesis": (
                "robot benchmark의 success score를 data provenance, temporal channel, hidden-state monitor, evaluator contract로 분해해 model improvement와 benchmark artifact를 구별합니다."
            ),
            "scores": {"fit": 4, "novelty": 5, "feasibility": 4, "moat": 4, "timing": 5, "evidence": 5},
            "one_week": (
                "기존 VLA/VLN evaluation 300 episodes에 timestamp shuffle, instruction paraphrase, evaluator threshold sweep, clean/trigger-like patch perturbation을 적용해 score-flip table을 만듭니다."
            ),
            "four_week": (
                "TrustVLA식 clean-calibrated hidden-state monitor와 temporal channel conflict test를 결합해 closed-loop robot failure가 어느 evidence channel에서 시작되는지 분리합니다."
            ),
            "metric": "aggregate success가 같은 두 policy 사이에서 channel-specific failure difference ≥10% 발견, human audit precision ≥90%, benchmark artifact report template 완성.",
            "stop": "channel perturbation이 rollout failure를 설명하지 못하고 evaluator-only noise가 3% 미만이면 internal audit tool로만 유지합니다.",
            "assets": [
                {"label": "TrustVLA", "url": "https://arxiv.org/abs/2607.12571"},
                {"label": "Temporal benchmark audit", "url": "https://arxiv.org/abs/2607.12304"},
                {"label": "WSI leakage audit", "url": "https://arxiv.org/abs/2607.12278"},
            ],
        },
    ],
}


def main() -> None:
    template.DATE = DATE
    template.SLUG = SLUG
    template.DATA = DATA
    doc = template.build_html()
    doc = doc.replace("2026-07-13 arXiv Research Intelligence", "2026-07-15 arXiv Research Intelligence")
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
