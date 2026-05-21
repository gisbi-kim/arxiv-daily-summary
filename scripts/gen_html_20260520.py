#!/usr/bin/env python3
"""Generate the 2026-05-20 arXiv daily briefing artifacts from date-section backfill outputs."""
from __future__ import annotations

from daily_backfill_lib import build, week_start


DATE = "2026-05-20"

PROFILE = {
    "date": DATE,
    "weekday": "수",
    "week_start": week_start(DATE),
    "thesis": (
        "20일 배치는 3DGS가 대규모 map/reconstruction substrate로 커지는 흐름과, VLA/주행 정책이 "
        "safe alignment와 hard-negative 실행 검증으로 내려오는 흐름이 같이 보입니다. "
        "생성 쪽도 예쁜 샘플보다 multi-shot 평가, physical world model, controllable aerial video처럼 "
        "실험 가능한 제어축을 묻는 날입니다."
    ),
    "trend_note": (
        "Foundation Models와 Generation이 수량상 가장 크지만, lab 관점에서는 3DGS/SLAM 계열 geometry, "
        "risk-aware VLA, closed-loop driving validation, embodied navigation map memory를 따로 보는 편이 좋습니다."
    ),
    "cluster_specs": [
        {
            "title": "Geometry가 3DGS scale-up과 SLAM/VIO back-end를 동시에 갱신",
            "buckets": ["3D/Scene"],
            "ids": ["2605.20150", "2605.19949", "2605.19539", "2605.19556", "2605.19990", "2605.19701", "2605.19257"],
            "needles": ["gaussian", "3dgs", "splatting", "feed-forward", "reconstruction", "odometry", "slam", "pose", "lidar", "mesh"],
            "why": (
                "이번 3D/Scene 묶음은 rendering 품질 경쟁 하나로 보기 어렵습니다. TideGS와 sparse-view Gaussian은 "
                "3DGS를 대규모 scene substrate로 키우고, Trust3R/EpiDiffVO/Minimalist VIO/PRISM-SLAM은 pose, "
                "uncertainty, scale-aware inference를 다시 묻습니다. 즉 classic SLAM 문제가 Gaussian map과 "
                "feed-forward reconstruction 쪽으로 흡수되는 신호입니다."
            ),
            "confidence": "High",
            "confidence_note": "3DGS, reconstruction, VIO/SLAM 논문이 같은 날짜에 5편 이상 연결",
            "lab_action": "3DGS map, feed-forward recon, VIO/SLAM baseline을 sparse-view, update cost, scale drift, dynamic-object failure로 같은 표에서 비교",
        },
        {
            "title": "VLA는 policy 크기보다 safe alignment와 execution recovery가 병목",
            "buckets": ["Robot Learning", "Safety/Alignment"],
            "ids": ["2605.19524", "2605.19678", "2605.19580", "2605.19294", "2605.19919", "2605.19986"],
            "needles": ["vla", "safe", "alignment", "risk", "policy", "counterfactual", "manipulation", "robot", "execution", "steering"],
            "why": (
                "SafeAlign-VLA, RoVLA, PAPO-VLA, DEFLECT가 한 묶음으로 나오면 VLA를 그냥 더 크게 만드는 문제가 아닙니다. "
                "negative risk, multi-consistency, planning-aware policy optimization, delay-robust execution처럼 실제 로봇에서 "
                "틀어지는 지점을 직접 겨냥합니다. fine-grained manipulation 평가까지 붙으면서 '성공/실패' 이분법보다 "
                "어디서 실패했는지 기록하는 쪽으로 무게가 갑니다."
            ),
            "confidence": "High",
            "confidence_note": "VLA 안전/강건성/실행 보정 논문 4편 이상 연결",
            "lab_action": "LIBERO/RoboCasa에서 risk-negative data, planning-aware loss, counterfactual recovery를 같은 task family로 ablation",
        },
        {
            "title": "Driving은 preference tuning에서 hard-negative closed-loop 검증으로 이동",
            "buckets": ["Autonomous Driving", "Robot Learning", "Generation", "Safety/Alignment"],
            "ids": ["2605.20082", "2605.19771", "2605.19631", "2605.19490", "2605.19033", "2605.18895"],
            "needles": ["driving", "autonomous", "closed-loop", "hard negative", "world model", "digital twin", "traffic", "scenario", "risk"],
            "why": (
                "VL-DPO처럼 language-guided preference alignment가 나오지만, 같은 날 Hard Negatives, HEAT, hybrid digital twin, "
                "traffic simulation, adversarial scenario generation이 같이 등장했습니다. 주행 모델을 offline score로만 보는 것이 아니라 "
                "어떤 위험 장면에서 policy가 무너지는지 closed-loop로 남기려는 흐름입니다."
            ),
            "confidence": "High",
            "confidence_note": "driving policy, simulation, hard-negative, adversarial scenario가 함께 등장",
            "lab_action": "nuPlan/CARLA에서 preference-tuned policy와 hard-negative policy를 동일 위험 장면 replay board로 비교",
        },
        {
            "title": "VLM 평가는 gaze, artifact, operation CoT처럼 채점 가능한 failure log로 내려감",
            "buckets": ["Foundation Models", "Safety/Alignment", "Efficiency/Systems"],
            "ids": ["2605.20165", "2605.19859", "2605.19559", "2605.19307", "2605.18984", "2605.19027"],
            "needles": ["vlm", "mllm", "benchmark", "gaze", "cot", "robustness", "artifact", "medical", "hallucination", "visual question"],
            "why": (
                "CaMo, gaze following, EgoCoT-Bench, MetaRA, Artifact-Bench, MedFM-Robust는 모두 'VLM이 그럴듯하게 맞는가'보다 "
                "어떤 evidence와 operation에서 실패하는지 기록하려는 쪽입니다. 특히 camera motion, gaze, artifact, medical robustness처럼 "
                "평가 조건이 구체화되어서 VLM reliability를 회의용 impression이 아니라 failure log로 남길 수 있습니다."
            ),
            "confidence": "High",
            "confidence_note": "서로 다른 평가축 benchmark가 5편 이상 연결",
            "lab_action": "camera motion, gaze, generated-video artifact, medical robustness를 하나의 VLM reliability schema로 묶어 answer error와 evidence error를 분리",
        },
        {
            "title": "Generation은 multi-shot 평가와 physics/action-conditioned world model로 실험화",
            "buckets": ["Generation", "Embodied AI", "Autonomous Driving"],
            "ids": ["2605.20183", "2605.19995", "2605.19242", "2605.19728", "2605.19319", "2605.19600"],
            "needles": ["video generation", "multi-shot", "controllable", "world model", "physics", "aerial", "uav", "embodied", "image editing"],
            "why": (
                "MSAVBench와 CogOmniControl은 video generation을 보기 좋은 샘플에서 multi-shot consistency와 creative intent control로 옮깁니다. "
                "PhyWorld, Aero-World, SWEET, FlyMirage까지 보면 action-conditioned world model을 로봇/드론/embodied task에 붙이려는 방향입니다. "
                "그래서 이 묶음은 생성 모델이라기보다 simulation/evaluation substrate 후보로 읽어야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "video evaluation, controllable generation, physical world model이 동시에 등장",
            "lab_action": "multi-shot consistency, inertial-control tracking, task success, temporal drift를 분리한 world-model evaluation grid 설계",
        },
        {
            "title": "Embodied navigation은 semantic map과 observation fidelity의 역효과를 같이 묻는다",
            "buckets": ["Embodied AI", "3D/Scene", "Safety/Alignment"],
            "ids": ["2605.19634", "2605.19958", "2605.19594", "2605.19206", "2605.20072", "2605.19328"],
            "needles": ["navigation", "embodied", "semantic map", "object-goal", "dynamic cognitive map", "observation fidelity", "adversarial", "robotic agents"],
            "why": (
                "P2DNav, TravExplorer, MCNav, CLUE는 navigation을 step-by-step action보다 map, memory, cue prioritization 문제로 봅니다. "
                "여기에 observation fidelity가 오히려 문제 해결을 해칠 수 있다는 probing과 embodied adversarial benchmark가 붙어서, "
                "더 많은 시각 정보가 항상 좋은가를 따져야 하는 날입니다."
            ),
            "confidence": "Medium",
            "confidence_note": "navigation/map-memory 논문 4편과 embodied safety 신호가 연결",
            "lab_action": "ObjectNav/VLN split에 observation fidelity, semantic-map cue, adversarial instruction을 함께 넣어 failure taxonomy 작성",
        },
    ],
    "research_topics": [
        {
            "title": "Gaussian-map SLAM audit",
            "claim": "TideGS, Feed-Forward GS, PRISM-SLAM, Minimalist VIO를 같은 indoor/outdoor relocalization split에서 map size, update cost, scale drift로 비교합니다.",
        },
        {
            "title": "Risk-aware VLA recovery board",
            "claim": "SafeAlign-VLA, RoVLA, PAPO-VLA, DEFLECT를 manipulation task family별로 실패 원인과 recovery step을 기록하는 board에 올립니다.",
        },
        {
            "title": "World-model controllability grid",
            "claim": "MSAVBench, CogOmniControl, PhyWorld, Aero-World를 multi-shot consistency, action tracking, physics violation, task success 네 축으로 평가합니다.",
        },
    ],
}


if __name__ == "__main__":
    build(PROFILE, f"out/cv_{DATE}.json", f"out/ro_{DATE}.json")
