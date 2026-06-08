#!/usr/bin/env python3
"""Generate 2026-06-02..04 arXiv daily backfill artifacts from date-section parser outputs."""
from __future__ import annotations

import sys

from daily_backfill_lib import build, week_start


def base_profile(date: str, weekday: str, thesis: str, trend_note: str, cluster_specs: list[dict], topics: list[dict]) -> dict:
    return {
        "date": date,
        "weekday": weekday,
        "week_start": week_start(date),
        "source_mode": "pastweek-date-section",
        "source_label": "arXiv cs.CV/pastweek date section + cs.RO/pastweek date section",
        "source_note": "Backfill parser output from arXiv /pastweek date section",
        "benchmark_note": "Backfill artifact generated from arXiv /pastweek date-section parser output; abstracts are unavailable.",
        "thesis": thesis,
        "trend_note": trend_note,
        "cluster_specs": cluster_specs,
        "research_topics": topics,
    }


PROFILES = {
    "2026-06-02": base_profile(
        "2026-06-02",
        "Tue",
        (
            "6/2 backfill은 VLA와 world model이 '크게 학습하면 된다'에서 벗어나 trust, semantic grounding, "
            "navigation memory, driving token으로 쪼개지는 날입니다. title/subject 기반 복구라 세부 claim은 보수적으로 보되, "
            "평가축과 state/action interface가 동시에 나온 신호는 강합니다."
        ),
        (
            "화요일 배치는 CV 쪽에서 3D, video, diffusion, token compression이 넓게 깔리고 RO 쪽에서 VLA, manipulation, "
            "navigation, world model이 직접 맞물립니다. 특히 RoboTrustBench, RoboSemanticBench, Safe2Drive 같은 이름이 보여주듯 "
            "모델을 키우는 것보다 어느 실패를 어떤 benchmark로 잡을지가 더 중요해졌습니다."
        ),
        [
            {
                "title": "VLA는 trust benchmark와 semantic grounding으로 평가축이 갈라짐",
                "buckets": ["Robot Learning", "Foundation Models"],
                "ids": ["2606.01600", "2606.02307", "2606.02277", "2606.02313", "2606.02486", "2606.00054"],
                "needles": ["vla", "trust", "failue-aware", "semantic grounding", "aerial navigation", "world model"],
                "why": (
                    "RoboTrustBench, FATE-VLA, RoboSemanticBench가 같은 날 보이는 것은 VLA 평가가 단순 success rate에서 trustworthiness, "
                    "failure generation, semantic grounding으로 나뉘고 있다는 신호입니다. Human-video survey와 predictive WAM도 함께 있어 "
                    "데이터 소스, action grounding, 실패 생성기를 따로 떼어 봐야 합니다."
                ),
                "confidence": "High",
                "confidence_note": "VLA benchmark, failure-aware test generation, semantic grounding 논문이 직접 연결됨",
                "lab_action": "VLA 실험표에 task success와 별도로 semantic grounding error, generated failure coverage, trust score, human-video transfer 조건을 둡니다.",
            },
            {
                "title": "Embodied navigation은 semantic-geometric map과 bad-behavior reward로 이동",
                "buckets": ["Embodied AI", "Robot Learning"],
                "ids": ["2606.02463", "2606.01788", "2606.01621", "2606.00095", "2606.01565", "2606.01036"],
                "needles": ["embodied", "navigation", "semantic", "geometric", "goal", "reward", "bad behavior"],
                "why": (
                    "MASER, PlatonicNav, Goal2Pixel, hierarchical semantic-geometric map 계열은 navigation memory를 pixel goal이나 topological map으로 "
                    "내려보내려 합니다. 여기에 reward model에는 bad behavior data가 필요하다는 position까지 붙으면서, navigation은 성공 경로만 모으는 문제가 아니라 "
                    "mistake-aware state와 reward를 같이 설계하는 문제가 됩니다."
                ),
                "confidence": "High",
                "confidence_note": "semantic map, goal grounding, bad-behavior reward 논문이 navigation 평가축으로 연결됨",
                "lab_action": "VLN/ObjectNav 로그에 map abstraction, goal-pixel grounding, instruction mistake, bad-behavior recovery tag를 추가합니다.",
            },
            {
                "title": "Geometry watch: 3D memory와 Gaussian streaming이 robot state 후보가 됨",
                "buckets": ["3D/Scene", "Generation"],
                "ids": ["2606.02510", "2606.02096", "2606.01573", "2606.00963", "2606.02436", "2606.01935"],
                "needles": ["lidar", "gaussian", "3d", "memory", "geometry", "driving world models"],
                "why": (
                    "Uncertainty-aware 4D LiDAR synthesis, real-time 3D Gaussians, voxel-Gaussian transformer, Reasmory의 3D memory는 "
                    "같은 질문으로 모입니다. 3D 표현이 렌더링 결과물이 아니라 VLM spatial reasoning, driving world model, robot state의 저장소가 될 수 있는지입니다."
                ),
                "confidence": "High",
                "confidence_note": "LiDAR synthesis, Gaussian streaming, explicit 3D memory, driving tokenizer가 한 배치에 존재",
                "lab_action": "3D 표현을 reconstruction score 외에 memory lookup accuracy, uncertainty calibration, planning-token usefulness로 비교합니다.",
            },
            {
                "title": "Driving은 safe behavior와 geometry-guided token으로 world model화됨",
                "buckets": ["Autonomous Driving", "Generation"],
                "ids": ["2606.02105", "2606.00191", "2606.01935", "2606.00857", "2606.00519", "2606.02273"],
                "needles": ["autonomous driving", "safe driving", "driving world", "trajectory", "driver", "risk"],
                "why": (
                    "Safe2Drive, multimodal action diffusion, dynamic risk horizon, anchor-based flow planning은 driving을 closed-loop action problem으로 밀고 갑니다. "
                    "Unified Driving Tokens는 representation과 geometry를 discrete token으로 묶어 world model과 planning을 같이 보려는 흐름이라, "
                    "perception benchmark만으로는 충분하지 않습니다."
                ),
                "confidence": "High",
                "confidence_note": "safe driving eval, action diffusion, risk horizon, driving token 논문이 같은 평가면에 놓임",
                "lab_action": "driving 평가에 safe-behavior checklist, risk horizon, geometry-token ablation, planning rollout divergence를 함께 기록합니다.",
            },
            {
                "title": "Long video MLLM은 retrieval, codec, token compression을 먼저 요구",
                "buckets": ["Foundation Models", "Efficiency/Systems", "Generation"],
                "ids": ["2606.02569", "2606.02564", "2606.02522", "2606.02482", "2606.02161", "2606.01790", "2606.02553"],
                "needles": ["video", "mllm", "long video", "token compression", "kv cache", "retrieve"],
                "why": (
                    "Video MLLM codec, adaptive test-time optimization, moment fidelity, multi-stream understanding, information-aware token compression과 KV cache compression이 "
                    "같이 나오면서 긴 비디오는 단순 context 확장이 아니라 무엇을 압축하고 무엇을 검색할지의 systems problem이 됩니다."
                ),
                "confidence": "Medium",
                "confidence_note": "video reasoning과 systems compression 논문이 같은 병목을 다른 층에서 다룸",
                "lab_action": "long-video 평가에서 moment fidelity, retrieval coverage, token budget, KV eviction policy를 같이 sweep합니다.",
            },
            {
                "title": "Reliability는 jailbreak, localization attack, representation alignment로 분해됨",
                "buckets": ["Safety/Alignment", "Foundation Models"],
                "ids": ["2606.02111", "2606.01892", "2606.02352", "2606.01746", "2606.02331", "2606.02276"],
                "needles": ["jailbreaking", "adversarial", "robust", "alignment", "localization", "linkage risk"],
                "why": (
                    "비디오 jailbreak, robot localization feature perturbation, driver distraction representation alignment, robustness trade-off, clinical VLM linkage risk가 "
                    "한 날에 모였습니다. reliability를 하나로 합치면 원인이 사라지므로 attack surface, data linkage, representation alignment를 따로 봐야 합니다."
                ),
                "confidence": "Medium",
                "confidence_note": "application은 다르지만 attack surface와 alignment failure가 공통 축",
                "lab_action": "신뢰성 로그를 jailbreak input, localization perturbation, linkage/privacy risk, representation drift 항목으로 분리합니다.",
            },
        ],
        [
            {"title": "VLA trust battery", "claim": "semantic grounding, failure generation, safe action, human-video transfer를 같은 VLA 모델군에 붙입니다."},
            {"title": "Navigation bad-behavior dataset", "claim": "성공 trajectory뿐 아니라 instruction mistake, wrong-goal, collision-prone recovery를 reward model 학습에 넣습니다."},
            {"title": "3D memory for planning", "claim": "3DGS/voxel/explicit memory를 VLM spatial reasoning과 driving token planning의 공통 state store로 비교합니다."},
        ],
    ),
    "2026-06-03": base_profile(
        "2026-06-03",
        "Wed",
        (
            "6/3 backfill은 geometry와 simulation이 실험 인프라 쪽으로 강하게 움직인 날입니다. 3DGS, odometry, closed-loop driving world model, "
            "VLA failure attribution, embodied memory가 모두 '보이는 장면'을 실행 가능한 testbed와 state로 바꾸려 합니다."
        ),
        (
            "수요일 배치는 3D/Scene과 Robot Learning이 균형 있게 강하고, driving에서는 closed-loop generative simulation과 uncertainty-aware planning이 같이 등장합니다. "
            "VLM 쪽은 streaming spatial intelligence와 KV eviction으로 긴 context를 운영하려고 하고, embodied AI는 reliability와 formal verification까지 언급합니다."
        ),
        [
            {
                "title": "Geometry watch: 3DGS와 odometry가 simulation-ready state로 정렬",
                "buckets": ["3D/Scene"],
                "ids": ["2606.03994", "2606.03992", "2606.03989", "2606.03909", "2606.03479", "2606.03254", "2606.02996"],
                "needles": ["3d scene", "lidar", "visual odometry", "gaussian", "streaming", "inertial odometry"],
                "why": (
                    "SimuScene, LiDAR semantic completion, PixVOD, SparseStreet, PersistGS, FreeStreamGS, MARIO가 같이 나오면서 3D는 offline reconstruction보다 "
                    "simulation-ready state, streaming input, odometry consistency를 요구받습니다. 로봇/주행 실험에 쓸 scene state라면 geometry 품질과 temporal consistency를 같이 봐야 합니다."
                ),
                "confidence": "High",
                "confidence_note": "3D scene reconstruction, LiDAR, odometry, streaming GS 논문이 직접 연결됨",
                "lab_action": "3D mapping 후보를 scene-completion IoU, odometry drift, streaming latency, sim-ready object consistency로 평가합니다.",
            },
            {
                "title": "Robot policy는 humanoid scaling과 failure attribution을 같이 요구",
                "buckets": ["Robot Learning"],
                "ids": ["2606.03985", "2606.03598", "2606.03949", "2606.03784", "2606.03556", "2606.03385"],
                "needles": ["humanoid", "vla", "failure attribution", "manipulation", "human-in-the-loop", "adversarial"],
                "why": (
                    "Humanoid-GPT와 PHASER는 데이터/경험 replay를 키우는 방향이고, embodied CoT와 Grasp-Then-Plan은 failure attribution과 계획 구조를 다시 묻습니다. "
                    "여기에 VLA adversarial patch와 human-in-the-loop RL이 붙으면 scaling만으로는 부족하고, 실패 원인을 사람·데이터·정책·perception 공격으로 나눠야 합니다."
                ),
                "confidence": "High",
                "confidence_note": "humanoid scaling, VLA replay, adversarial attack, failure attribution이 모두 robot policy 표면을 건드림",
                "lab_action": "manipulation/humanoid 실험에 failure attribution label, adversarial condition, replay source, human preference calibration을 같이 붙입니다.",
            },
            {
                "title": "Driving은 real-time generative world model과 uncertainty planning으로 이동",
                "buckets": ["Autonomous Driving"],
                "ids": ["2606.03159", "2606.02956", "2606.02979", "2606.03296", "2606.02677", "2606.03756"],
                "needles": ["closed-loop", "autonomous driving", "dataset", "uncertainty", "motion planning", "navigation functions"],
                "why": (
                    "NVIDIA OmniDreams가 real-time generative world model을 closed-loop simulation에 놓고, KITScenes와 compact perception은 데이터/모델 측을 보강합니다. "
                    "Safe action을 위한 uncertainty planning과 classical-to-modern planning survey까지 같이 있어 driving 실험은 world model, dataset, planner 보증을 한 장에서 봐야 합니다."
                ),
                "confidence": "High",
                "confidence_note": "closed-loop AV simulation, dataset, compact perception, uncertainty planning이 직접 연결됨",
                "lab_action": "closed-loop driving 평가에 generator latency, uncertainty-to-action coupling, dataset coverage, planner fallback trigger를 남깁니다.",
            },
            {
                "title": "Spatial intelligence는 streaming benchmark와 embodied memory로 구체화",
                "buckets": ["Foundation Models", "Efficiency/Systems", "Embodied AI"],
                "ids": ["2606.03890", "2606.03577", "2606.03075", "2606.03509", "2606.03374", "2606.03175", "2606.03593"],
                "needles": ["streaming spatial", "spatial reasoning", "kv", "memory", "embodied", "reliable", "formal verification"],
                "why": (
                    "OVO-S-Bench와 wide-baseline spatial reasoning은 MLLM spatial intelligence를 streaming/geometry 조건에서 묻고, TGV-KV는 text-grounded KV eviction으로 runtime을 만집니다. "
                    "EvoMemNav, eMEM, Ask When It Pays, embodied AI reliability agenda까지 이어지면 memory는 모델 내부 context가 아니라 탐색과 상호작용 비용을 줄이는 state입니다."
                ),
                "confidence": "High",
                "confidence_note": "spatial benchmark, KV eviction, embodied memory, reliability agenda가 같은 문제를 계층별로 다룸",
                "lab_action": "spatial-agent eval에 memory update cost, ask/act tradeoff, KV eviction error, formal-verification target을 분리합니다.",
            },
            {
                "title": "Generation은 one-step video, foresight, scene completion으로 평가 압력을 받음",
                "buckets": ["Generation"],
                "ids": ["2606.03972", "2606.03971", "2606.03915", "2606.03603", "2606.03243", "2606.03216"],
                "needles": ["video", "diffusion", "scene completion", "world models", "preference"],
                "why": (
                    "AAD-1과 Video-Mirai는 빠른 video generation에도 foresight가 필요하다는 쪽이고, PatchScene은 large-scale scene completion으로 3D 공간을 생성합니다. "
                    "World Models Meet Language Models와 MemoGen은 구체적 경험과 추상 reasoning을 연결하려 해, generation 평가도 temporal foresight와 reusable memory를 봐야 합니다."
                ),
                "confidence": "Medium",
                "confidence_note": "video generation, scene completion, world/language model 논문이 연결되지만 task surface는 넓음",
                "lab_action": "video/world-model 실험에 one-step latency, foresight horizon, scene-completion consistency, preference drift를 같이 둡니다.",
            },
            {
                "title": "Robustness는 multimodal adversarial safety와 feature matching으로 분산",
                "buckets": ["Safety/Alignment", "Foundation Models", "Embodied AI"],
                "ids": ["2606.03925", "2606.03713", "2606.03793", "2606.03539", "2606.03406", "2606.02603", "2606.03593"],
                "needles": ["adversarial", "robust", "safety alignment", "feature matching", "formal verification"],
                "why": (
                    "High-confidence adversarial training, MLLM robustness, multilingual multimodal safety alignment, robust feature matching, COD corruptions, embodied AI formal verification agenda가 함께 있습니다. "
                    "안전성은 모델별 score 하나보다 공격 유형, modality, corruption, verification target을 분리해 관리해야 합니다."
                ),
                "confidence": "Medium",
                "confidence_note": "robustness 논문들이 같은 failure taxonomy를 요구하지만 도메인은 분산됨",
                "lab_action": "robustness dashboard를 attack modality, corruption family, feature-match failure, formal spec coverage로 나눕니다.",
            },
        ],
        [
            {"title": "Simulation-ready scene state", "claim": "3DGS, LiDAR completion, odometry를 closed-loop sim에서 같은 state interface로 비교합니다."},
            {"title": "Robot failure attribution protocol", "claim": "VLA/manipulation failure를 perception, action decoder, replay data, human preference source로 분해합니다."},
            {"title": "Streaming spatial intelligence eval", "claim": "MLLM spatial benchmark에 memory update, KV eviction, ask-cost, formal-verification target을 붙입니다."},
        ],
    ),
    "2026-06-04": base_profile(
        "2026-06-04",
        "Thu",
        (
            "6/4 backfill은 mapping, tactile imitation, video/world-action generation, VLM statefulness가 한 번에 올라온 날입니다. "
            "복구 소스는 title/subject 기반이지만, robot policy가 실제 deployment로 가려면 uncertainty-aware map, contact-rich data, fast video generation, "
            "token/quantization budget을 같이 봐야 한다는 메시지는 뚜렷합니다."
        ),
        (
            "목요일 배치는 전날보다 총량은 작지만 주제가 조밀합니다. SLAM과 semantic reconstruction은 LLM planning verification으로 이어지고, "
            "VLA는 latent 3D priors와 tactile-language-action dataset을 만납니다. Generation 쪽은 executable manipulation, physics-informed video, infinite memory, steering control로 "
            "robot/world-action interface에 가까워졌습니다."
        ),
        [
            {
                "title": "Geometry watch: long-horizon mapping이 uncertainty-aware SLAM과 LLM verification으로 연결",
                "buckets": ["3D/Scene"],
                "ids": ["2606.05035", "2606.04853", "2606.04618", "2606.04226", "2606.04593", "2606.05124"],
                "needles": ["streaming 3d", "slam", "semantic scene reconstruction", "mapping", "gaussian", "4d reconstruction"],
                "why": (
                    "Anchor3R는 long-horizon visual mapping을 streaming 3D reconstruction으로 보고, SENTINEL은 SLAM에 'I don't know'를 넣습니다. "
                    "BPDA-GMM과 PerceptTwin은 semantic SLAM과 LLM planning verification을 연결하고, sparse dynamic camera 4D reconstruction과 geometry Gaussians까지 있어 "
                    "geometry는 planner가 신뢰할 수 있는 불확실성 포함 state여야 합니다."
                ),
                "confidence": "High",
                "confidence_note": "streaming mapping, uncertainty SLAM, semantic reconstruction, 4D/GS 논문이 같은 geometry-state 축에 있음",
                "lab_action": "mapping 실험에 transient-anchor drift, unknown-state calibration, semantic verification pass rate, geometry/appearance disentanglement를 추가합니다.",
            },
            {
                "title": "Manipulation은 3D priors, deformable imitation, tactile contact로 촘촘해짐",
                "buckets": ["Robot Learning"],
                "ids": ["2606.04436", "2606.04269", "2606.04968", "2606.04825", "2606.04708", "2606.04233"],
                "needles": ["vla", "deformable", "imitation", "tactile", "contact-rich", "benchmarking"],
                "why": (
                    "3DThinkVLA는 latent 3D priors를 VLA co-training에 넣고, Instant-Fold는 deformable object manipulation의 in-context imitation을 봅니다. "
                    "HapTile과 TransTac은 tactile/vision-language-action 데이터를 contact-rich 실행에 붙이고, manipulation benchmark 질문까지 나와 "
                    "정책 구조보다 데이터 modality와 benchmark definition을 먼저 정해야 하는 날입니다."
                ),
                "confidence": "High",
                "confidence_note": "3D priors, deformable imitation, tactile VLA data, benchmark 논문이 manipulation 표면에서 만남",
                "lab_action": "manipulation benchmark를 rigid/deformable/contact-rich로 나누고 3D prior, tactile token, UMI adaptation source를 명시합니다.",
            },
            {
                "title": "World-action generation은 executable manipulation과 navigation으로 가까워짐",
                "buckets": ["Robot Learning", "Generation", "Embodied AI", "Autonomous Driving"],
                "ids": ["2606.04811", "2606.04737", "2606.04775", "2606.04527", "2606.04907", "2606.04884"],
                "needles": ["video generation", "robot manipulation", "world-action", "infinite video", "autonomous driving", "navigation"],
                "why": (
                    "Dream.exe는 video generation model이 executable robot manipulation을 꿈꿀 수 있는지 묻고, physics-informed video generation과 activation steering은 "
                    "생성 모델을 control surface로 만지려 합니다. Echo-Infinity와 WAM-Nav, diffusion MoE driving까지 합치면 video/world generation은 보기 좋은 영상보다 "
                    "action consequence와 navigation/driving 제어 가능성이 중요합니다."
                ),
                "confidence": "High",
                "confidence_note": "executable manipulation, physics-informed video, steering, WAM navigation, driving diffusion이 action interface로 연결됨",
                "lab_action": "generation 모델 평가에 executable-action success, physics residual, steering controllability, navigation rollout consistency를 둡니다.",
            },
            {
                "title": "VLM은 stateful encoder와 modality imbalance 진단을 요구",
                "buckets": ["Foundation Models", "Efficiency/Systems"],
                "ids": ["2606.04986", "2606.04922", "2606.04773", "2606.04613", "2606.04433", "2606.04351", "2606.04434"],
                "needles": ["vision-language", "stateful", "modality imbalance", "video", "attention calibration", "benchmark"],
                "why": (
                    "Food-R1, geometry-aware distillation, motion QA, spectral diagnostics of modality imbalance, stateful visual encoders, Video2LoRA가 같이 나오면서 "
                    "VLM은 task score보다 어떤 modality가 state를 지배하는지 진단해야 합니다. Hyper-ICL의 attention calibration도 같은 문제의 runtime 조정축입니다."
                ),
                "confidence": "Medium",
                "confidence_note": "VLM task는 다양하지만 statefulness, modality imbalance, calibration이라는 공통 진단축이 있음",
                "lab_action": "VLM 평가에 modality contribution spectrum, state retention, video internalization cost, attention calibration sensitivity를 기록합니다.",
            },
            {
                "title": "Efficiency는 video compression, quantization, sparse evidence retrieval로 실제 제약을 만짐",
                "buckets": ["Efficiency/Systems"],
                "ids": ["2606.04410", "2606.04349", "2606.04373", "2606.04437", "2606.04493", "2606.04801", "2606.04920"],
                "needles": ["compression", "quantization", "sparse", "retrieval", "mamba", "fast"],
                "why": (
                    "Ultra-fast video compression, modality-aware quantization, data-free quantization, ego-guided sparse evidence retrieval, correspondence pruning, fast persistent homology가 "
                    "동시에 보입니다. 배포 가능한 multimodal/robot stack에서는 모델 선택만큼 어떤 evidence를 남기고 어떤 bit/token을 줄이는지가 실험 claim의 일부입니다."
                ),
                "confidence": "Medium",
                "confidence_note": "압축·양자화·retrieval·pruning 계열이 같은 deployment budget을 다룸",
                "lab_action": "runtime 비교표에 video bitrate, quantization error, evidence retrieval recall, correspondence-pruning failure를 함께 둡니다.",
            },
            {
                "title": "Robustness는 deepfake, medical shift, anomaly alignment로 적용면이 넓음",
                "buckets": ["Generation", "Safety/Alignment"],
                "ids": ["2606.04863", "2606.04722", "2606.04700", "2606.04427", "2606.04385", "2606.04369", "2606.04767"],
                "needles": ["deepfake", "robust", "alignment", "anomaly", "fisher", "noise"],
                "why": (
                    "IRIS-GAN deepfake detection, stroke/pose/segmentation robustness, heterogeneous foundation-model alignment, 3D anomaly detection, Fisher-information robustness가 같이 있습니다. "
                    "도메인은 넓지만 공통적으로 distribution shift와 representation alignment를 분리해야 하며, safety claim을 단일 benchmark로 요약하기 어렵습니다."
                ),
                "confidence": "Medium",
                "confidence_note": "medical, forensic, anomaly, theory 논문이 reliability taxonomy 관점에서 연결됨",
                "lab_action": "robustness 결과를 forensic shift, clinical acquisition shift, geometry alignment shift, theoretical bound 항목으로 나눠 관리합니다.",
            },
        ],
        [
            {"title": "Uncertainty-aware geometry state", "claim": "SLAM/mapping 출력에 unknown-state calibration과 LLM planning verification pass rate를 붙입니다."},
            {"title": "Contact-rich VLA data audit", "claim": "deformable, tactile, visual, UMI adaptation source가 manipulation success에 주는 영향을 같은 표로 비교합니다."},
            {"title": "World-action generation gate", "claim": "video generation을 executable manipulation, WAM navigation, driving rollout의 control metric으로 평가합니다."},
        ],
    ),
}


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in PROFILES:
        known = ", ".join(sorted(PROFILES))
        raise SystemExit(f"usage: python scripts/gen_html_20260602_04.py <date>; known: {known}")
    build(PROFILES[sys.argv[1]], "out/cv_new.json", "out/ro_new.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
