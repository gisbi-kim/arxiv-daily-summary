#!/usr/bin/env python3
"""Generate the 2026-07-13 daily briefing from matching arXiv /new listings."""
from __future__ import annotations

from daily_backfill_lib import build, week_start

DATE = "2026-07-13"

PROFILE = {
    "date": DATE,
    "weekday": "Mon",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from the matching 2026-07-13 /new listings",
    "benchmark_note": "Daily artifact generated from matching arXiv /new listings with abstracts.",
    "thesis": (
        "7월 13일 배치는 VLA post-training, robot-usable Gaussian map, long-tail driving, "
        "multi-view VLM diagnosis가 모두 평균 성능보다 실패 조건과 실행 비용을 드러내는 방향으로 이동했음을 보여줍니다. "
        "APRL 관점에서는 grounding, memory, dynamic scene, compute budget을 독립 stress axis로 두는 평가 설계가 핵심입니다."
    ),
    "cluster_takeaway": (
        "오늘의 판세는 더 큰 모델이 아니라 실제 행동에 필요한 grounding, map validity, object permanence, "
        "long-tail coverage, energy budget을 같은 downstream metric으로 연결하는 것입니다."
    ),
    "trend_note": (
        "Robot Learning과 Safety/Alignment가 가장 두껍고 Generation, Foundation Models가 그 뒤를 받칩니다. "
        "VLA adaptation, Gaussian control map, long-tail driving, multi-view reasoning, edge energy가 배포 검증 축으로 모입니다."
    ),
    "cluster_specs": [
        {
            "title": "VLA가 imitation 규모 경쟁에서 language-action grounding과 actor-critic post-training으로 이동",
            "buckets": ["Robot Learning"],
            "ids": ["2607.08974", "2607.09590", "2607.08877", "2607.09336"],
            "needles": ["vla", "action", "robot policy", "reinforcement", "human-in-the-loop"],
            "why": (
                "CLAP, PAC-ACT, FlowDAgger, shortcut trajectory planning은 demonstration을 더 모으는 것만으로 행동 일반화가 해결되지 않음을 보여줍니다. "
                "language-action grounding, post-training critic, human correction, trajectory shortcut이 서로 다른 failure family를 다루므로 "
                "같은 task에서 데이터 규모와 adaptation mechanism의 기여를 분리해야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "VLA grounding, actor-critic post-training, human adaptation, offline RL 신호가 반복됩니다.",
            "lab_action": (
                "LIBERO/RoboCasa에서 instruction paraphrase, unseen object, delayed correction, action-chunk length를 ablation하고 "
                "task success, recovery time, unsafe action, intervention count를 비교합니다."
            ),
            "limit": 6,
        },
        {
            "title": "Gaussian scene representation이 reconstruction asset에서 reactive control과 online SLAM map으로 이동",
            "buckets": ["3D/Scene"],
            "ids": ["2607.09260", "2607.08948", "2607.08808", "2607.09125", "2607.09503"],
            "needles": ["gaussian", "slam", "reconstruction", "geometry", "overlap"],
            "why": (
                "AnythingReality, SplatCtrl, StereoSplat+, 4D human-scene reconstruction, VGGT overlap probing은 3D 결과물을 보기 좋은 모델로만 평가할 수 없음을 보여줍니다. "
                "online update, perception-action coupling, low-overlap geometry가 실제 localization과 control을 좌우하므로 robot-usable map validity가 중심 평가가 되어야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "online GS-SLAM, reactive control, stereo reconstruction, overlap diagnosis가 같은 geometry gate를 충족합니다.",
            "lab_action": (
                "동일 dynamic trajectory에서 Gaussian SLAM, feed-forward reconstruction, geometry foundation baseline을 비교하고 "
                "pose drift, map update latency, collision, downstream task success를 공동 측정합니다."
            ),
            "limit": 6,
        },
        {
            "title": "Driving perception이 frame accuracy에서 object permanence와 generative long-tail coverage로 이동",
            "buckets": ["Autonomous Driving", "Safety/Alignment"],
            "ids": ["2607.09138", "2607.09655", "2607.09629", "2607.09428"],
            "needles": ["driving", "long-tail", "radar", "occupancy", "scenario"],
            "why": (
                "BeyondSight, OpenLongTail, 4DR360, multimodal scenario search는 한 프레임의 detection score가 가려온 occlusion과 rare-scene 실패를 직접 겨냥합니다. "
                "object permanence, radar-camera state reasoning, 생성된 long-tail data를 폐루프 위험과 연결해야 실제 일반화 여부를 판단할 수 있습니다."
            ),
            "confidence": "High",
            "confidence_note": "object permanence, 4D occupancy, long-tail generation, scenario retrieval 신호가 명확합니다.",
            "lab_action": (
                "CARLA/nuScenes에서 occlusion duration, radar dropout, rare interaction, generated-scene ratio를 조절하고 "
                "track continuity, occupancy error, near-miss, recovery success를 비교합니다."
            ),
            "limit": 6,
        },
        {
            "title": "VLM reasoning 평가가 single-view 정답률에서 world-centric multi-view integration 진단으로 이동",
            "buckets": ["Foundation Models", "Safety/Alignment"],
            "ids": ["2607.08970", "2607.09068", "2607.09654", "2607.09562"],
            "needles": ["multiview", "map", "vision-language", "reasoning", "medical"],
            "why": (
                "MultiView-Bench, OmniMapBench, decade-scale visual-cognitive error 분석, TCLA는 VLM 평균 정확도가 어떤 공간 관계와 domain cue를 놓치는지 설명하지 못함을 보여줍니다. "
                "view aggregation, map structure, metadata shift를 분리해 evidence grounding과 calibration failure를 진단해야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "multi-view integration, map reasoning, error taxonomy, domain adaptation 신호가 반복됩니다.",
            "lab_action": (
                "multi-view/map/medical VQA에서 view order, missing view, structural cue, metadata shift를 ablation하고 "
                "answer consistency, evidence recall, calibration error를 비교합니다."
            ),
            "limit": 6,
        },
        {
            "title": "World model이 action-conditioned generation에서 causal bias와 multi-robot coordination 검증으로 이동",
            "buckets": ["Generation"],
            "ids": ["2607.09185", "2607.09587", "2607.08942", "2607.09193"],
            "needles": ["world model", "diffusion", "action", "robot", "causal"],
            "why": (
                "causally debiased latent action model, CoDiMAD, adaptive MPPI, YeTI는 생성 품질보다 action consistency와 disturbance robustness를 묻습니다. "
                "embodied world model과 diffusion coordination은 잘 보이는 샘플이 아니라 control failure를 줄이는지로 검증해야 합니다."
            ),
            "confidence": "Medium-High",
            "confidence_note": "action-conditioned world model, diffusion coordination, disturbance estimation이 downstream control 축으로 연결됩니다.",
            "lab_action": (
                "multi-robot/navigation rollout에서 latent-action bias, communication dropout, disturbance covariance, horizon을 조작하고 "
                "coordination success, collision, forecast consistency를 비교합니다."
            ),
            "limit": 6,
        },
        {
            "title": "Efficient multimodal inference가 token count에서 geometry 보존과 edge energy 병목으로 이동",
            "buckets": ["Efficiency/Systems"],
            "ids": ["2607.09080", "2607.09520", "2607.09029", "2607.09225"],
            "needles": ["compression", "energy", "efficient", "geometry", "structure-from-motion"],
            "why": (
                "GeoTrace, edge VLM energy 분석, MOSAIC, Glob3R은 계산량 축소만으로 배포 효율성을 설명할 수 없음을 보여줍니다. "
                "trajectory geometry와 global structure를 보존하면서 실제 병목인 decoding energy를 줄여야 downstream spatial reasoning이 유지됩니다."
            ),
            "confidence": "High",
            "confidence_note": "trajectory token compression, edge energy, heterogeneous composition, global geometry가 같은 배포 질문으로 모입니다.",
            "lab_action": (
                "video/VLM/3D pipeline에서 token budget, decoder frequency, model composition을 조절하고 "
                "energy, latency, trajectory error, downstream decision accuracy의 Pareto frontier를 비교합니다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {"title": "Grounded VLA post-training grid", "claim": "language-action grounding, actor-critic post-training, human correction을 같은 task에서 ablation해 recovery mechanism을 분리합니다."},
        {"title": "Robot-usable Gaussian map suite", "claim": "online GS-SLAM과 reconstruction model을 pose drift, update latency, reactive-control success로 비교합니다."},
        {"title": "Long-tail permanence benchmark", "claim": "occlusion과 rare-scene generation을 결합해 object permanence가 폐루프 위험을 얼마나 줄이는지 측정합니다."},
    ],
}


if __name__ == "__main__":
    build(PROFILE, "out/cv_new.json", "out/ro_new.json")
