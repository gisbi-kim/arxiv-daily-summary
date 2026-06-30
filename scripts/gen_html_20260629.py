#!/usr/bin/env python3
"""Generate the 2026-06-29 arXiv daily briefing artifacts from /pastweek date-section outputs."""
from __future__ import annotations

from daily_backfill_lib import build, week_start


DATE = "2026-06-29"

PROFILE = {
    "date": DATE,
    "weekday": "Mon",
    "week_start": week_start(DATE),
    "source_mode": "pastweek-date-section",
    "source_label": "arXiv cs.CV/pastweek date section + cs.RO/pastweek date section",
    "source_note": "Backfill parser output from the 2026-06-29 /pastweek date sections",
    "benchmark_note": "Backfill artifact generated from arXiv /pastweek date sections; abstracts are not available in this source.",
    "thesis": (
        "6/29 backfill은 로봇 조작, 3D map, diffusion, embodied navigation이 모두 "
        "좋은 데모를 만드는 단계에서 실제 실패 조건을 분리하는 단계로 이동했음을 보여줍니다. "
        "APRL 관점에서는 policy 재사용, Gaussian/LiDAR map, multi-agent response, VLM grounding을 "
        "각각 benchmark, ablation, stress split으로 바로 비교해야 합니다."
    ),
    "cluster_takeaway": (
        "오늘의 핵심은 모델 family가 아니라 평가 축입니다. manipulation, 3D reconstruction, "
        "multi-agent autonomy, VLM reasoning, diffusion generation이 모두 downstream success와 "
        "failure condition을 나누는 실험 단위로 재정의되고 있습니다."
    ),
    "trend_note": (
        "Monday backfill은 Robot Learning과 Generation이 가장 두껍고, 3D/Scene과 Embodied AI가 "
        "그 뒤를 받칩니다. /pastweek backfill이라 abstract는 없지만 title/subject만으로도 "
        "physics simulator, LiDAR/Gaussian map, response map, VLM shortcut, domain-gap diffusion이 "
        "동일한 검증 축으로 모이는 흐름이 분명합니다."
    ),
    "cluster_specs": [
        {
            "title": "Manipulation 평가가 policy 재사용에서 물리 시뮬레이터와 cached control 검증으로 이동",
            "buckets": ["Robot Learning"],
            "ids": ["2606.28128", "2606.28323", "2606.28133", "2606.28300", "2606.28276", "2606.27872"],
            "needles": ["physics", "dexterous", "manipulation", "cached", "scene generation", "vla"],
            "why": (
                "조작 policy를 많이 모으는 것만으로는 실제 전이 실패를 설명하기 어렵습니다. "
                "PhysisForcing, DexCompose, Translation as a Bridging Action, CacheMPC, SimFoundry, S2-VLA는 "
                "재사용 가능한 skill이 물리 제약, cached control, 자동 scene generation, long-horizon state space에서 "
                "어디서 무너지는지를 따로 평가해야 한다는 신호입니다."
            ),
            "confidence": "High",
            "confidence_note": "robot manipulation, simulator, cached MPC, VLA long-horizon 신호가 같은 평가 축으로 반복됩니다.",
            "lab_action": (
                "LIBERO/RoboCasa와 quadruped locomotion suite에서 policy reuse, physics forcing, cached MPC, "
                "scene-generation seed를 ablation 변수로 두고 collision, recovery time, task success를 비교합니다."
            ),
            "limit": 6,
        },
        {
            "title": "3D map 평가는 Gaussian 품질에서 localization drift와 LiDAR constraint로 이동",
            "buckets": ["3D/Scene"],
            "ids": ["2606.28321", "2606.28060", "2606.27729", "2606.27584", "2606.27509", "2606.27491", "2606.27811"],
            "needles": ["gaussian", "lidar", "localization", "slam", "reconstruction", "3d"],
            "why": (
                "3D 결과물을 시각적으로 잘 만드는지만 보면 로봇 map으로 쓸 수 있는지 알 수 없습니다. "
                "StructSplat, ReScene, 1-bit LiDAR localization, CoIn, Structured-Li-GS, SelectAnyTree, LXD-SLAM은 "
                "sparse view, LiDAR constraint, dense SLAM 조합에서 pose drift와 navigation validity를 함께 봐야 한다는 흐름입니다."
            ),
            "confidence": "High",
            "confidence_note": "Gaussian reconstruction, LiDAR localization, SLAM paper가 2편 이상 연결되어 geometry gate를 충족합니다.",
            "lab_action": (
                "같은 indoor/outdoor route에서 Gaussian map과 LiDAR/SLAM baseline을 sparse-view, dynamic-object, "
                "loop-closure stress split으로 나누고 localization drift와 downstream navigation success를 측정합니다."
            ),
            "limit": 7,
        },
        {
            "title": "Multi-agent autonomy가 optimal path에서 response map과 cooperation law stress test로 확장",
            "buckets": ["Autonomous Driving", "Embodied AI"],
            "ids": ["2606.27625", "2606.27495", "2606.27656", "2606.28182", "2606.27929", "2606.27962"],
            "needles": ["multi-robot", "response map", "cooperation", "closed-loop", "agentic", "planning"],
            "why": (
                "multi-robot 성능은 최단 경로 또는 asymptotic optimality만으로 끝나지 않습니다. "
                "P-ARC, AO-ARC, driver response maps, LLawCo, embodied collective intelligence, cloud-native simulation은 "
                "독립 subproblem, human response, cooperation law가 충돌할 때 어떤 policy가 안전하게 양보하는지 검증해야 함을 보여줍니다."
            ),
            "confidence": "Medium",
            "confidence_note": "motion planning, driver interaction, embodied cooperation paper가 서로 다른 실험 축을 제공합니다.",
            "lab_action": (
                "multi-agent simulator에서 agent 수, human response delay, cooperation rule violation을 stress split으로 만들고 "
                "near-miss, deadlock, recovery success, rule violation을 함께 비교합니다."
            ),
            "limit": 6,
        },
        {
            "title": "VLM reasoning 평가는 movement VQA와 shortcut decoding의 failure condition으로 이동",
            "buckets": ["Foundation Models", "Safety/Alignment"],
            "ids": ["2606.27999", "2606.27974", "2606.27947", "2606.27646", "2606.27596", "2606.28149", "2606.28077"],
            "needles": ["vqa", "multimodal", "token", "shortcut", "robust", "distribution"],
            "why": (
                "VLM이 답을 맞혔다는 결과만으로는 어떤 visual evidence를 실제로 썼는지 알기 어렵습니다. "
                "HumanMoveVQA, ProMSA, activation maps, VLM-aware meta-optics, faithful decoding, robust segmentation, TextDS는 "
                "movement, search, token activation, distribution shift 조건에서 reasoning shortcut을 분리해야 한다는 묶음입니다."
            ),
            "confidence": "Medium",
            "confidence_note": "VQA, activation map, robust representation, distribution-shift paper가 grounding failure 축으로 연결됩니다.",
            "lab_action": (
                "movement VQA와 scene-text/segmentation benchmark에서 cue removal, viewpoint shift, distribution shift를 "
                "ablation으로 만들고 omitted evidence와 answer stability를 비교합니다."
            ),
            "limit": 7,
        },
        {
            "title": "Diffusion generation이 빠른 복원에서 domain gap과 attribution 검증으로 이동",
            "buckets": ["Generation"],
            "ids": ["2606.28226", "2606.28144", "2606.28094", "2606.28092", "2606.28039", "2606.28016", "2606.27537"],
            "needles": ["diffusion", "flow", "domain gap", "attribution", "world modeling", "video"],
            "why": (
                "diffusion은 더 빠른 샘플링이나 더 그럴듯한 복원만으로 로봇 평가에 들어오기 어렵습니다. "
                "flow rectification, avatar reconstruction, one-step inpainting, denoiser attribution, cross-sensor super-resolution, "
                "TempAct, MemoBench는 생성 모델이 어떤 frequency/domain/world-state 조건에서 실패하는지 분해해야 한다는 흐름입니다."
            ),
            "confidence": "High",
            "confidence_note": "diffusion, flow matching, attribution, domain gap, world-model benchmark가 같은 검증 요구로 모입니다.",
            "lab_action": (
                "same scene에서 sensor domain, occlusion, temporal horizon, generated artifact를 stress split으로 두고 "
                "perception downstream score와 planning failure rate를 함께 평가합니다."
            ),
            "limit": 7,
        },
        {
            "title": "Embodied navigation infrastructure가 cloud simulation에서 on-device object-goal evaluation으로 이동",
            "buckets": ["Embodied AI", "Efficiency/Systems"],
            "ids": ["2606.28049", "2606.27962", "2606.27871", "2606.28182", "2606.27660", "2606.28163"],
            "needles": ["embodied", "navigation", "cloud", "on-device", "multi-view", "compression", "token"],
            "why": (
                "embodied benchmark는 고정된 offline score보다 heterogeneous view, cloud simulation, on-device navigation, token budget을 "
                "같이 움직여야 실제 배포 조건을 드러냅니다. AirGroundBench, cloud-native simulation, LocalNav, LLawCo, MVPruner, video compression은 "
                "공간 reasoning과 resource budget을 같은 실험 단위에서 봐야 한다는 신호입니다."
            ),
            "confidence": "Medium",
            "confidence_note": "embodied collaboration, simulator, on-device navigation, pruning/compression 신호가 묶입니다.",
            "lab_action": (
                "ObjectNav/VLN suite에서 viewpoint heterogeneity, compute budget, communication delay를 ablation 변수로 두고 "
                "goal success, collision, latency, memory footprint를 함께 비교합니다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Manipulation physics-transfer grid",
            "claim": "policy reuse, physics forcing, cached control, scene generation을 같은 조작 task에서 ablation해 sim-to-real failure mode를 분리합니다.",
        },
        {
            "title": "Gaussian-LiDAR map validity suite",
            "claim": "Gaussian map과 LiDAR/SLAM baseline을 localization drift, dynamic-object robustness, navigation success로 비교합니다.",
        },
        {
            "title": "Embodied resource stress benchmark",
            "claim": "on-device navigation에서 token pruning, compression, view heterogeneity를 조작해 latency와 goal success의 trade-off를 측정합니다.",
        },
    ],
}


if __name__ == "__main__":
    build(PROFILE, "out/cv_20260629.json", "out/ro_20260629.json")
