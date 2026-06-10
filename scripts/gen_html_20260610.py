#!/usr/bin/env python3
"""Generate the 2026-06-10 arXiv daily briefing artifacts from /new parser outputs."""
from __future__ import annotations

from daily_backfill_lib import build, week_start


DATE = "2026-06-10"

PROFILE = {
    "date": DATE,
    "weekday": "Wed",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Daily /new parser output",
    "benchmark_note": "Daily artifact generated from arXiv /new parser output with abstracts available.",
    "thesis": (
        "6/10 /new 배치는 로봇 쪽에서 VLA/WAM의 실시간 제어, 계층 오케스트레이션, 검증, 접촉-힘 모델링이 한 번에 몰린 날입니다. "
        "CV 쪽에서는 video world model이 시간 편집, causal/autoregressive memory, 물리 일관성 benchmark로 내려오고, 3D는 digital twin과 "
        "manipulation trajectory, driving future prediction으로 실제 downstream utility를 묻는 흐름이 강합니다."
    ),
    "trend_note": (
        "Robot Learning이 가장 큰 버킷이고, Efficiency/Systems와 Generation이 뒤를 받칩니다. "
        "오늘은 새 backbone 하나보다 action interface, memory horizon, contact/force sensing, token budget, test-time verification처럼 "
        "실험에서 바로 ablation 축으로 바꿀 수 있는 논문들이 많습니다. APRL 관점에서는 VLA를 더 크게 만드는 쪽보다 "
        "occlusion, physical fault, contact transition, runtime pruning, closed-loop planner stability를 같은 evaluation table에 얹는 편이 유리합니다."
    ),
    "cluster_specs": [
        {
            "title": "VLA/WAM은 backbone 경쟁에서 제어 인터페이스 경쟁으로 이동",
            "buckets": ["Robot Learning"],
            "ids": ["2606.10040", "2606.10180", "2606.10267", "2606.10363", "2606.10305", "2606.10568", "2606.10862"],
            "needles": [
                "world-action model",
                "wam",
                "vision-language-action",
                "vla",
                "flow control",
                "hierarchical",
                "memory",
                "verification",
                "occlusion",
                "reward model",
            ],
            "why": (
                "Efficient-WAM, HiMem-WAM, Flow Control, Hi-VLA orchestration, VeriSpace, LIBERO-Occ가 같은 방향을 가리킵니다. "
                "핵심은 언어-비전 입력을 더 잘 넣는 것이 아니라, 미래 상상 비용을 낮추고, subgoal을 어떻게 쪼개고, 부분 관측과 action 후보를 "
                "test-time에 어떻게 검증할지입니다. VLA evaluation을 success rate 하나로 두면 중요한 실패 양상이 사라집니다."
            ),
            "confidence": "High",
            "confidence_note": "VLA, WAM, memory, verification, occlusion 논문이 Robot Learning 버킷에 다수 집중",
            "lab_action": "동일 manipulation split에서 action latency, memory length, occlusion severity, subgoal error, verifier rejection rate를 한 표로 묶어 비교합니다.",
            "limit": 5,
        },
        {
            "title": "Dexterous/contact-rich manipulation은 데이터 표현과 힘 예측이 병목",
            "buckets": ["Robot Learning"],
            "ids": ["2606.10614", "2606.10683", "2606.10818", "2606.11184", "2606.10244", "2606.10743", "2606.10899", "2606.10229"],
            "needles": [
                "dexterous",
                "hand",
                "tokenizer",
                "forceful",
                "force-guided",
                "tactile",
                "contact-rich",
                "bimanual",
                "demonstration",
                "trajectory transfer",
            ],
            "why": (
                "Dexterous Point Policy와 UniDexTok은 손 embodiment 차이를 representation 문제로 보고, IMPACT와 TacForeSight는 접촉/힘의 dynamics를 "
                "policy 내부에 넣으려 합니다. YUBI, HOWTransfer, MV-Actor까지 합치면 데이터 수집 장치, human video transfer, multi-view semantics가 "
                "같은 병목을 다른 쪽에서 누르는 배치입니다."
            ),
            "confidence": "High",
            "confidence_note": "dexterous hand, forceful manipulation, tactile world model, data interface 논문이 같은 날 동시 출현",
            "lab_action": "dexterous task마다 state tokenizer, tactile/force channel, human-to-robot transfer source, contact transition failure를 로그 필드로 고정합니다.",
            "limit": 5,
        },
        {
            "title": "Video world model은 시간, memory, 물리 일관성 benchmark로 내려옴",
            "buckets": ["Generation", "3D/Scene"],
            "ids": ["2606.10135", "2606.10183", "2606.10620", "2606.10671", "2606.11187", "2606.11129", "2606.11188"],
            "needles": [
                "video world model",
                "autoregressive",
                "time editable",
                "spatiotemporal",
                "memory",
                "causal",
                "worldolympiad",
                "physical faithfulness",
                "interaction fidelity",
            ],
            "why": (
                "BiWM, Making Time Editable, ImageTime, FadeMem, Next Forcing은 video generation을 예쁜 clip 생성보다 시간 제어와 memory 유지 문제로 바꿉니다. "
                "WorldOlympiad는 physical faithfulness, geometric consistency, interaction fidelity를 묻기 때문에 robotics/world-model 평가와 직접 연결됩니다."
            ),
            "confidence": "High",
            "confidence_note": "Generation 버킷의 autoregressive video 흐름과 3D/Scene의 world-model benchmark가 맞물림",
            "lab_action": "world model demo를 FVD/CLIP score가 아니라 time edit, long-horizon drift, geometry consistency, action consequence prediction으로 나눠 평가합니다.",
            "limit": 5,
        },
        {
            "title": "3D/Scene은 reconstruction 품질보다 운영 가능한 geometry로 이동",
            "buckets": ["3D/Scene"],
            "ids": ["2606.09882", "2606.09967", "2606.10019", "2606.10478", "2606.10541", "2606.10645", "2606.10656", "2606.10442"],
            "needles": [
                "digital twin",
                "3d gaussian",
                "point cloud registration",
                "vlm code synthesis",
                "lidar",
                "manipulation trajectory",
                "autonomous driving",
                "occupancy mapping",
                "submap",
            ],
            "why": (
                "WHU-Infra3D와 ABot-Earth는 대규모 3D environment를 만들고, Generalized-CVO와 GRAR, occupancy mapping은 실제 센서 오류와 정합을 다룹니다. "
                "ManiSplat과 Envision4D는 3D representation을 manipulation trajectory와 driving future prediction에 연결합니다. 3D가 rendering artifact를 넘어 "
                "로봇/주행 downstream metric으로 평가받기 시작한 신호입니다."
            ),
            "confidence": "High",
            "confidence_note": "dataset, point registration, LiDAR artifact, manipulation trajectory, driving 4D prediction이 한 버킷에 공존",
            "lab_action": "3D method를 Chamfer/PSNR에서 끊지 말고 registration latency, artifact rejection, trajectory feasibility, future-scene collision risk까지 같이 봅니다.",
            "limit": 5,
        },
        {
            "title": "Driving/planning은 uncertainty, cost tuning, history stability를 분리해야 함",
            "buckets": ["Autonomous Driving"],
            "ids": ["2606.09958", "2606.10688", "2606.10732", "2606.10733", "2606.10856", "2606.10974", "2606.10986", "2606.11019"],
            "needles": [
                "uncertainty-aware",
                "mixed traffic",
                "counterfactual",
                "mpc",
                "adaptive velocity",
                "exposure-time",
                "cost optimization",
                "diffusion forcing",
                "history",
            ],
            "why": (
                "mixed traffic uncertainty, counterfactual relevance, Formula Student MPC/velocity planning, ECU exposure-time alignment, language-driven cost tuning, "
                "Diffusion Forcing Planner가 모두 closed-loop 안정성의 다른 파트를 겨냥합니다. perception score만 높이는 대신 어떤 객체를 무시해도 되는지, "
                "cost를 누가 조정하는지, history conditioning이 trajectory 흔들림을 얼마나 줄이는지가 핵심입니다."
            ),
            "confidence": "High",
            "confidence_note": "motion planning, relevance modeling, MPC, ECU timing, cost tuning, temporal consistency가 명확히 연결",
            "lab_action": "driving benchmark에 relevance false-negative, cost parameter drift, history annealing ablation, exposure-time mismatch, closed-loop comfort/safety를 추가합니다.",
            "limit": 5,
        },
        {
            "title": "Runtime과 reliability는 token pruning, contamination, hallucination을 함께 봐야 함",
            "buckets": ["Efficiency/Systems", "Safety/Alignment", "Foundation Models"],
            "ids": ["2605.29662", "2606.10533", "2606.10651", "2606.10198", "2606.10400", "2606.10066", "2606.10309", "2606.10571"],
            "needles": [
                "token pruning",
                "efficient",
                "long-video",
                "agentic",
                "hallucination",
                "calibration",
                "textual prior",
                "contamination",
                "robustness",
                "adversarial",
            ],
            "why": (
                "SAFE-Pruner와 audio-visual token pruning은 실시간 VLA/MLLM inference 예산을 줄이려 하고, Kwai Keye-VL-2.0은 long-video/agentic intelligence를 키웁니다. "
                "동시에 contamination audit, textual-prior benchmark, hallucination selective prediction, adversarial transferability가 reliability 하한을 묻습니다. "
                "큰 모델을 빠르게 만드는 실험과 틀릴 때 멈추는 실험을 분리하면 배포 리스크를 과소평가하게 됩니다."
            ),
            "confidence": "Medium",
            "confidence_note": "응용 도메인은 흩어져 있지만 token budget과 reliability floor라는 공통 평가축이 선명함",
            "lab_action": "latency/throughput curve 옆에 contamination split, abstention calibration, hallucination rate, adversarial/post-processing robustness를 붙입니다.",
            "limit": 5,
        },
    ],
    "research_topics": [
        {
            "title": "Occlusion-to-verification VLA benchmark",
            "claim": "LIBERO-Occ류 occlusion split에 subgoal planning, WAM memory, test-time action verification을 얹어 failure source를 분해합니다.",
        },
        {
            "title": "Contact-aware dexterous tokenizer study",
            "claim": "dexterous hand tokenizer와 tactile/force world model을 같은 task에서 비교해 representation, contact transition, recovery success의 tradeoff를 봅니다.",
        },
        {
            "title": "World-model temporal fidelity table",
            "claim": "video WAM/4D scene generation을 time edit, memory budget, physical consistency, downstream planning success로 같은 표에 올립니다.",
        },
    ],
}


if __name__ == "__main__":
    build(PROFILE, "out/cv_new.json", "out/ro_new.json")
