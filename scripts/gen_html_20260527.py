#!/usr/bin/env python3
"""Generate the 2026-05-27 arXiv daily briefing artifacts from /pastweek date-section parser outputs."""
from __future__ import annotations

from daily_backfill_lib import build, week_start


DATE = "2026-05-27"

PROFILE = {
    "date": DATE,
    "weekday": "수",
    "week_start": week_start(DATE),
    "source_mode": "pastweek-date-section",
    "source_label": "arXiv cs.CV/pastweek 2026-05-27 section + cs.RO/pastweek 2026-05-27 section",
    "source_note": "Backfill parser output from /pastweek date section",
    "benchmark_note": "Backfill artifact generated from arXiv /pastweek date-section parser output; abstracts are not available in that source.",
    "thesis": (
        "27일 묶음은 3D geometry와 robot policy가 둘 다 '현장에 들어갈 때 무엇이 깨지는가'를 묻는 쪽으로 모였습니다. "
        "Gaussian map, sparse LiDAR, semantic mapping, FineVLA, continual VLA가 같이 나오면서, 보기 좋은 모델보다 map update, uncertainty, data correction, safety constraint를 함께 재야 하는 날입니다."
    ),
    "trend_note": (
        "논문 수는 28일 /new보다 작지만, geometry, manipulation, embodied navigation 쪽 신호가 또렷합니다. "
        "특히 3DGS map과 VLN, VLA continual learning, VR-based on-policy correction이 같은 날 나와서 robot stack의 perception-memory-action 연결을 다시 보게 합니다."
    ),
    "cluster_specs": [
        {
            "title": "Gaussian map이 VLN과 open-world semantic mapping으로 들어옴",
            "buckets": ["3D/Scene", "Embodied AI", "Robot Learning"],
            "ids": ["2605.26500", "2605.26503", "2605.26831", "2605.26576"],
            "needles": ["gaussian map", "semantic mapping", "vision-language navigation", "referring segmentation", "3d gaussian"],
            "why": (
                "27일에는 3D Gaussian이 단순한 rendering asset이 아니라 로봇이 쓰는 map과 semantic memory로 들어가는 논문들이 같이 나왔습니다. "
                "3D Gaussian Map은 VLN에서 open-set semantic grouping을 쓰고, Uncertainty-Aware Gaussian Map은 navigation에서 map confidence를 같이 보게 합니다. "
                "OSMa-Bench++와 TrackRef3D까지 묶으면, 앞으로는 예쁜 3D reconstruction보다 지도 표현이 지시문, 물체 referent, manipulation 준비에 얼마나 쓸 수 있는지가 더 중요합니다."
            ),
            "confidence": "High",
            "confidence_note": "Gaussian map, semantic mapping, VLN 관련 대표 논문 4편 연결",
            "lab_action": "3DGS map, voxel map, feature-field map을 VLN success, open-set object recall, map update cost로 비교",
        },
        {
            "title": "VLA는 fine-grained instruction과 continual data 문제로 이동",
            "buckets": ["Robot Learning", "Foundation Models", "Safety/Alignment"],
            "ids": ["2605.27284", "2605.26820", "2605.26828", "2605.26649"],
            "needles": ["finevla", "vla models", "continually", "forgetting", "instruction alignment", "imitation learning", "demonstrations"],
            "why": (
                "FineVLA는 VLA가 거친 instruction을 맞히는 수준을 넘어, 조작 가능한 세부 지시를 얼마나 잘 따르는지 묻습니다. "
                "continual learning 논문은 real-world data를 계속 넣을 때 이전 행동을 잊지 않는지 보고, keypoint imitation과 symbolic task rule 논문은 demonstration에서 무엇을 일반화할지 다시 나눕니다. "
                "즉 오늘 VLA 쪽 질문은 큰 모델 하나가 아니라, 새 데이터와 새 지시가 들어왔을 때 policy가 얼마나 안정적으로 바뀌는가입니다."
            ),
            "confidence": "High",
            "confidence_note": "VLA instruction, continual learning, demonstration generalization 논문이 직접 연결",
            "lab_action": "LIBERO/RoboCasa에서 instruction granularity, continual update step, demonstration count를 바꾼 forgetting-success table 작성",
        },
        {
            "title": "Robot data collection은 VR correction과 sim-to-real stress test로 구체화",
            "buckets": ["Robot Learning", "Embodied AI"],
            "ids": ["2605.27114", "2605.26638", "2605.26944", "2605.27046"],
            "needles": ["vr-dagger", "sim-to-real", "grasping", "dexterous", "uncertainty-guided", "thermal safety", "quadrupedal"],
            "why": (
                "VR-DAgger는 사람이 VR로 policy를 고쳐 주는 on-policy correction을 다루고, HyperSim은 manipulation에서 sim-to-real을 더 넓게 묶습니다. "
                "pose and shape estimation for grasping과 quadruped thermal safety까지 보면, 데이터 수집과 policy 보정은 더 이상 학습 전처리만이 아닙니다. "
                "실제 로봇에서는 grasp 실패, actuator heat, uncertainty가 함께 오기 때문에 correction loop 자체를 실험 protocol로 잡아야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "data correction, sim-to-real, grasping, locomotion safety 논문 4편 연결",
            "lab_action": "VR correction 횟수, sim-to-real domain gap, actuator thermal limit을 같은 manipulation/locomotion log에 기록",
        },
        {
            "title": "Navigation은 uncertainty, credibility, low-light sensing을 같이 봐야 함",
            "buckets": ["Embodied AI", "Safety/Alignment", "Autonomous Driving", "3D/Scene"],
            "ids": ["2605.26974", "2605.26710", "2605.26348", "2605.26330"],
            "needles": ["navigation", "safe", "uncertainty", "risk-sensitive", "dark", "events", "socially-compliant"],
            "why": (
                "USV navigation, socially-compliant indoor navigation, risk-sensitive planning, event-based dark navigation이 같은 날 나왔습니다. "
                "이 묶음은 path planning을 최단경로 문제가 아니라 sensor uncertainty, social rule, low-light observation까지 함께 들어오는 의사결정 문제로 봅니다. "
                "따라서 navigation benchmark도 성공률 하나보다 visibility, rule violation, risk cost를 나눠 저장해야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "safe navigation 관련 서로 다른 platform 논문 4편 연결",
            "lab_action": "ObjectNav/VLN split에 darkness, dynamic obstacle, social-distance violation, risk budget 조건을 추가",
        },
        {
            "title": "Diffusion generation은 controllability와 acceleration을 동시에 묻기 시작",
            "buckets": ["Generation", "Efficiency/Systems", "Safety/Alignment"],
            "ids": ["2605.27343", "2605.27336", "2605.27075", "2605.27003"],
            "needles": ["controllable image generation", "video generation", "diffusion transformer", "acceleration", "quantization", "adaptive routing"],
            "why": (
                "representation-conditioned diffusion은 원하는 조건을 더 잘 넣는 문제를 보고, PARE와 SoftCap은 video generation과 diffusion transformer의 비용을 줄입니다. "
                "W4A4 quantization까지 같이 보면, 생성 모델 평가는 이제 결과가 그럴듯한지만 보는 단계가 아닙니다. "
                "원하는 조건을 얼마나 잘 따르는지와 같은 시간 예산에서 얼마나 안정적으로 나오는지를 함께 봐야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "controllability, routing, budget control, quantization 논문이 같은 축으로 연결",
            "lab_action": "text/image condition fidelity, frame consistency, latency, memory footprint를 묶은 diffusion runtime grid 작성",
        },
        {
            "title": "VLM reliability는 retrieval head와 OOD, adversarial texture로 쪼개짐",
            "buckets": ["Foundation Models", "Safety/Alignment", "Efficiency/Systems"],
            "ids": ["2605.27243", "2605.26661", "2605.26501", "2605.27136"],
            "needles": ["retrieval heads", "out-of-distribution", "adversarial", "uncertainty", "vision-language"],
            "why": (
                "long-context VLM의 retrieval head가 실제 image evidence를 보는지 묻는 논문과, modality gap 기반 OOD, texture-constrained adversarial attack, token-level uncertainty 논문이 같이 나왔습니다. "
                "이 흐름은 VLM reliability를 정답률 하나로 보지 않고, 어떤 token과 visual evidence가 결정에 영향을 줬는지 확인하려는 쪽입니다. "
                "랩에서는 answer correctness와 함께 retrieval target, OOD score, token uncertainty를 같은 log에 남기는 편이 좋습니다."
            ),
            "confidence": "Medium",
            "confidence_note": "reliability 관련 논문 4편 연결, benchmark 통합은 추가 확인 필요",
            "lab_action": "VLM eval log에 retrieved image region, OOD distance, adversarial texture flag, token uncertainty를 저장",
        },
    ],
    "research_topics": [
        {
            "title": "Gaussian map for embodied navigation 비교표",
            "claim": "3DGS map, uncertainty-aware map, semantic mapping benchmark를 VLN success, open-set recall, update latency로 비교합니다.",
        },
        {
            "title": "Continual VLA forgetting stress test",
            "claim": "FineVLA와 continual VLA류를 대상으로 새 task data를 순차 주입하고 이전 instruction success가 얼마나 떨어지는지 봅니다.",
        },
        {
            "title": "Navigation uncertainty logging protocol",
            "claim": "darkness, social rule, risk budget, sensor credibility를 같은 navigation run에서 기록하는 stress split을 만듭니다.",
        },
    ],
}


if __name__ == "__main__":
    build(PROFILE, "out/cv_new.json", "out/ro_new.json")
