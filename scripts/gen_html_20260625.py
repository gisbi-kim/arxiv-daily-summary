#!/usr/bin/env python3
"""Generate the 2026-06-25 arXiv daily briefing artifacts from /pastweek date-section parser outputs."""
from __future__ import annotations

from daily_backfill_lib import build, week_start


DATE = "2026-06-25"

PROFILE = {
    "date": DATE,
    "weekday": "Thu",
    "week_start": week_start(DATE),
    "source_mode": "pastweek-date-section",
    "source_label": "arXiv cs.CV/pastweek date section + cs.RO/pastweek date section",
    "source_note": "Backfill parser output from the 2026-06-25 /pastweek date sections",
    "benchmark_note": "Backfill artifact generated from arXiv /pastweek date-section parser output; paper-level summaries are title/subject based.",
    "thesis": (
        "6/25 backfill은 LiDAR/SLAM, VLA online adaptation, tactile/manipulation, VLM uncertainty, navigation memory가 "
        "모두 배포 조건에서 어떤 실패를 재현할 수 있는지로 모입니다. APRL 관점에서는 새 모델 이름보다 "
        "map merge, self-distillation, tactile benchmark, GUI/egocentric uncertainty를 실제 실험 변수로 분리해야 합니다."
    ),
    "cluster_takeaway": (
        "오늘의 핵심은 모델 계열을 늘리는 것이 아니라, localization·VLA·tactile·navigation에서 배포 실패를 "
        "재현 가능한 benchmark 조건으로 어떻게 드러내고 검증할 것인가다."
    ),
    "trend_note": (
        "6/25는 /pastweek date-section backfill입니다. title/subject만으로도 LiDAR-inertial odometry와 multi-robot map merging, "
        "ROAD/WOLF/Reflective VLA, tactile benchmark, computer-use agent uncertainty, embodied navigation memory가 강하게 반복됩니다."
    ),
    "cluster_specs": [
        {
            "title": "SLAM이 단일 map 품질에서 고속·자원제약·multi-robot localization 검증으로 이동",
            "buckets": ["3D/Scene"],
            "ids": ["2606.26010", "2606.25386", "2606.25796", "2606.25699", "2606.25953", "2606.26046"],
            "needles": [
                "lidar-inertial odometry", "map merging", "localization", "slam",
                "active slam", "degeneracy", "multi-robot",
            ],
            "why": (
                "기존 SLAM 평가는 trajectory error와 map quality 중심으로 끝나는 경우가 많았습니다. 이번 묶음은 high-speed LIO, "
                "resource-constrained map merging, magnetometer-inertial-LiDAR fusion, degeneracy-aware LIVO, object SLAM, active SLAM을 통해 "
                "지도 품질이 실제 속도, 통신 제약, 퇴화 환경, 탐사 정책 안에서 유지되는지 묻습니다."
            ),
            "confidence": "High",
            "confidence_note": "LiDAR-inertial odometry, map merging, fusion localization, active/object SLAM 논문이 독립적으로 반복됨",
            "lab_action": (
                "tunnel/corridor/warehouse sequence에서 LIO, map-merging SLAM, active SLAM을 비교하고 localization drift, "
                "communication budget, loop-closure recovery, downstream navigation success를 함께 평가한다."
            ),
            "limit": 6,
        },
        {
            "title": "VLA 학습이 offline imitation에서 online adaptation과 consequence-aware 실행으로 이동",
            "buckets": ["Robot Learning"],
            "ids": ["2606.25800", "2606.25591", "2606.25215", "2606.25985", "2606.26006", "2606.26095"],
            "needles": [
                "vla", "online adaptation", "self-distillation", "humanoid", "consequences",
                "delay-aware", "reinforcement fine-tuning", "action priors",
            ],
            "why": (
                "VLA를 dataset으로 한 번 학습한 policy로만 보면 실제 배포 조건의 지연, embodiment 차이, 결과 반성, fine-tuning 안정성을 놓칩니다. "
                "ROAD-VLA, WOLF-VLA, Reflective VLA, Action ControlNet, FORCE, cross-embodiment action priors는 "
                "실행 중 적응과 consequence modeling이 generalization의 핵심 변수라는 신호입니다."
            ),
            "confidence": "High",
            "confidence_note": "online adaptation, humanoid VLA, consequence reflection, delay adapter, RL fine-tuning이 같은 실행 안정성 축을 형성",
            "lab_action": (
                "humanoid/mobile manipulation suite에서 self-distillation, consequence context, delay adapter, value-calibrated warm-up을 "
                "독립 변수로 두고 unseen object, control delay, embodiment transfer 실패를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Manipulation 평가는 시각 성공률에서 tactile·force·depth 신뢰성을 함께 묻는 쪽으로 이동",
            "buckets": ["Robot Learning"],
            "ids": ["2606.25877", "2606.25886", "2606.25503", "2606.25939", "2606.25295", "2606.26093"],
            "needles": [
                "tactile", "sensor", "depth reliability", "non-lambertian",
                "deformable", "grasp", "forceful manipulation", "semg",
            ],
            "why": (
                "manipulation 성공률만 보면 contact-rich task에서 무엇이 실패했는지 분리하기 어렵습니다. TacVerse, 3D-printable tactile dataset, "
                "non-Lambertian depth reliability, DeformGen, dynamic mobile manipulation, ForceBand는 시각 depth, tactile signal, force cue, "
                "deformable topology가 서로 다른 실패 원인임을 드러냅니다."
            ),
            "confidence": "High",
            "confidence_note": "tactile benchmark, depth reliability, deformable augmentation, forceful manipulation 신호가 모두 contact-rich 평가축을 공유",
            "lab_action": (
                "transparent/reflective object와 deformable cloth task에서 RGB-D, tactile, force/sEMG 입력을 ablation 축으로 두고 "
                "grasp stability, slip onset, topology-change recovery, mobile manipulation success를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "VLM/GUI agent 평가는 정답 생성에서 불확실성·시각 교란·지연 비용 분리로 이동",
            "buckets": ["Foundation Models", "Safety/Alignment"],
            "ids": ["2606.25760", "2606.25160", "2606.25066", "2606.26041", "2606.25343", "2606.25212"],
            "needles": [
                "uncertainty", "computer-use agents", "low-latency", "egocentric",
                "visual search", "ocr-reasoning", "document retrieval", "vlm-seeded",
            ],
            "why": (
                "VLM과 GUI agent를 답을 맞히는 모델로만 보면 실제 상호작용에서 언제 멈추고 언제 다시 봐야 하는지 알 수 없습니다. "
                "computer-use uncertainty, low-latency egocentric VLM, visual-search reaction tokens, OCR robustness, invoice retrieval, VLM-seeded simulation은 "
                "정답과 지연, 시각 교란, 불확실성을 함께 평가해야 한다는 흐름입니다."
            ),
            "confidence": "Medium",
            "confidence_note": "agent uncertainty, egocentric latency, OCR/document robustness가 같은 interaction reliability 축으로 묶임",
            "lab_action": (
                "GUI/AR/egocentric task에서 visual perturbation, document homogeneity, response budget을 바꿔가며 "
                "uncertainty calibration, correction behavior, task completion latency를 함께 평가한다."
            ),
            "limit": 6,
        },
        {
            "title": "World model은 물리 법칙을 그리는 데서 planning horizon을 보증하는 쪽으로 이동",
            "buckets": ["Generation", "Robot Learning"],
            "ids": ["2606.26025", "2606.24946", "2606.24945", "2606.26017", "2606.25754", "2606.25473"],
            "needles": [
                "world modeling", "robotic control", "conformal", "trust horizons",
                "conservation laws", "diffusion planning", "robotic polishing", "streaming video",
            ],
            "why": (
                "world model이 장면을 잘 예측해도 planning에 쓸 수 있는 horizon을 모르면 로봇 제어에서는 위험합니다. "
                "in-context world modeling, conformal trust horizons, conservation-law certification, grid-guided diffusion planning, "
                "stage-aware polishing policy는 예측 품질보다 언제까지 믿고 행동할 수 있는지를 평가하라는 신호입니다."
            ),
            "confidence": "High",
            "confidence_note": "robot control, conformal horizon, conservation law, diffusion planning이 같은 trust-horizon 질문으로 연결",
            "lab_action": (
                "manipulation과 navigation rollout에서 model horizon, physical-law violation, stage transition을 독립 변수로 두고 "
                "closed-loop success, recovery behavior, unsafe action rate를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Embodied navigation이 경로 계획에서 crowd intention과 scene-graph memory 평가로 이동",
            "buckets": ["Embodied AI"],
            "ids": ["2606.25504", "2606.26047", "2606.25206", "2606.25497", "2606.25119", "2606.25880"],
            "needles": [
                "navigation", "crowds", "intention-aware", "long-horizon", "memory",
                "scene graph", "surveillance", "spatial-semantic", "embodied visual tracking",
            ],
            "why": (
                "VLN/ObjectNav 평가는 shortest path나 success rate만으로 사회적 navigation 실패를 설명하기 어렵습니다. "
                "GROVE, crowd intention representation, RAVEN memory, SAGE-Nav scene graph, surveillance-assisted ObjectNav, spatial-semantic prompts는 "
                "로봇이 사람 의도와 장면 기억을 얼마나 유지하는지 평가해야 한다는 흐름입니다."
            ),
            "confidence": "High",
            "confidence_note": "crowd simulation, intention-aware navigation, long-horizon memory, scene graph planning 논문이 같은 embodied 평가축을 형성",
            "lab_action": (
                "Habitat/real-crowd style benchmark에서 crowd density, surveillance availability, scene-graph memory length를 바꿔가며 "
                "collision, detour cost, target recall, instruction-following success를 비교한다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Resource-constrained SLAM stress suite",
            "claim": "LiDAR-inertial SLAM과 map merging을 tunnel, high-speed, low-bandwidth 조건에서 같은 navigation success 기준으로 비교한다.",
        },
        {
            "title": "Consequence-aware VLA adaptation",
            "claim": "Reflective context와 online self-distillation이 unseen object와 control delay 조건에서 실제 실패를 얼마나 줄이는지 검증한다.",
        },
        {
            "title": "Contact-rich manipulation sensor ablation",
            "claim": "vision, tactile, force/sEMG 입력을 분리해 deformable manipulation과 non-Lambertian object handling의 실패 원인을 평가한다.",
        },
    ],
}


if __name__ == "__main__":
    build(PROFILE, "out/cv_20260625.json", "out/ro_20260625.json")
