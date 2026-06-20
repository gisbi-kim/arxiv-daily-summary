#!/usr/bin/env python3
"""Generate the 2026-06-19 arXiv daily briefing artifacts from /new parser outputs."""
from __future__ import annotations

from daily_backfill_lib import build, week_start


DATE = "2026-06-19"

PROFILE = {
    "date": DATE,
    "weekday": "Fri",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Daily /new parser output",
    "benchmark_note": "Daily artifact generated from arXiv /new parser output with abstracts available.",
    "thesis": (
        "6/19 batch는 VLA와 world model을 더 크게 만드는 흐름보다, 행동에 필요한 증거가 압축, 기억, 합성, "
        "실패 예측, calibration 과정에서 살아남는지를 묻는 논문들이 중심입니다. APRL 관점에서는 모델 이름보다 "
        "evidence-to-action chain, closed-loop recovery, 그리고 deployment budget을 한 표에서 같이 보는 날입니다."
    ),
    "trend_note": (
        "Robot Learning과 Generation이 가장 큰 축이고, 두 축은 서로 분리되어 있지 않습니다. ImageWAM, SurgVista, "
        "Holo-World, EventVLA, Tri-Info 같은 논문들은 world model과 VLA를 단순 생성기나 정책이 아니라 "
        "행동 증거를 저장하고 검증하는 중간 계층으로 다룹니다. 동시에 driving, navigation, calibration, "
        "medical/surgical reliability 논문들은 평균 성능보다 long-tail, uncertainty, domain shift, sensor budget을 "
        "운영 조건으로 끌어올립니다."
    ),
    "cluster_specs": [
        {
            "title": "VLA는 action token보다 task evidence 보존 문제가 됨",
            "buckets": ["Robot Learning", "Foundation Models"],
            "ids": ["2606.19565", "2606.20092", "2606.19998", "2606.19965"],
            "needles": [
                "vision-language-action",
                "vla",
                "task-evidence",
                "visual evidence memory",
                "failure prediction",
                "perception-to-action gap",
            ],
            "why": (
                "Mix-QVLA, EventVLA, Tri-Info, ROSE를 같이 보면 VLA의 핵심 질문이 '무슨 action을 내는가'에서 "
                "'그 action을 만드는 증거가 quantization, long-horizon memory, rollout failure, task context 변화 뒤에도 "
                "남아 있는가'로 이동합니다. 이는 VLA 평가를 성공률 하나가 아니라 evidence retention과 failure warning까지 "
                "포함한 계약으로 바꾸라는 신호입니다."
            ),
            "confidence": "High",
            "confidence_note": "VLA, evidence memory, failure prediction, perception-to-action benchmark가 같은 날 직접 등장",
            "lab_action": "VLA 실험 로그에 action, supporting evidence, memory event, quantization setting, predicted failure score를 같은 row로 저장합니다.",
            "limit": 5,
        },
        {
            "title": "World model은 full video보다 intervention 가능한 state interface로 수렴",
            "buckets": ["Robot Learning", "Generation"],
            "ids": ["2606.19889", "2606.19531", "2606.20083", "2606.19495", "2606.19817"],
            "needles": [
                "world model",
                "world action model",
                "video world model",
                "action-conditioned",
                "synthetic data",
                "spatial blocking",
            ],
            "why": (
                "SurgVista, ImageWAM, Holo-World, LooseControlVideo, synthetic-data metric 논문은 world model을 "
                "미래 프레임 생성기로만 보지 않습니다. 비용이 큰 full video 대신 image editing, camera/object/weather control, "
                "surgical instrument-tissue dynamics, detector proxy metric처럼 intervention과 downstream usefulness를 "
                "직접 묻는 방향입니다."
            ),
            "confidence": "High",
            "confidence_note": "robotics, driving-style world control, synthetic-data evaluation이 모두 action-conditioned usefulness로 연결됨",
            "lab_action": "world model benchmark를 visual realism, action-relevant state error, intervention controllability, downstream policy gain으로 분해합니다.",
            "limit": 5,
        },
        {
            "title": "3D representation은 보기 좋은 geometry에서 질의 가능한 scene memory로 이동",
            "buckets": ["3D/Scene", "Robot Learning", "Efficiency/Systems", "Foundation Models"],
            "ids": ["2606.19383", "2606.19828", "2606.19915", "2606.20103", "2606.19733", "2606.19776"],
            "needles": [
                "3d scene graphs",
                "part-level object tokens",
                "3d spatial awareness",
                "lidar-camera calibration",
                "open-vocabulary 3d instance retrieval",
                "occupancy grounded",
            ],
            "why": (
                "3D Scene Graphs, 3D-PLOT-LLM, SpatialSV, LiDAR-camera calibration, QueryGaussian, Occ-VLM은 "
                "3D 표현을 reconstruction 결과물이 아니라 로봇이 질의하고 설명하고 보정할 수 있는 memory interface로 다룹니다. "
                "APRL 쪽에서는 map을 저장하는 형식보다 part, relation, occupancy, calibration uncertainty가 action에 어떻게 "
                "전달되는지를 봐야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "scene graph, part token, spatial supervision, calibration, open-vocabulary retrieval이 한 축을 이룸",
            "lab_action": "3D map/scene 실험마다 query type, part relation, calibration residual, retrieval hit, downstream action effect를 함께 기록합니다.",
            "limit": 6,
        },
        {
            "title": "Driving과 autonomy 평가는 closed-loop long-tail을 직접 생성하고 검증하려 함",
            "buckets": ["Autonomous Driving", "Generation"],
            "ids": ["2606.19641", "2606.19836", "2606.20110", "2606.20336", "2606.19687"],
            "needles": [
                "self-play",
                "end-to-end driving",
                "post-training",
                "safety-critical",
                "text-guided driving scene generation",
                "stl specifications",
                "gnss degraded",
            ],
            "why": (
                "Scaling Self-Play, World Engine, FrozenDrive, priority-ordered STL planning, route-constrained GNSS fusion은 "
                "driving/autonomy 평가가 offline imitation에서 벗어나 long-tail scenario generation, closed-loop feedback, "
                "우선순위가 있는 안전 명세, degraded localization을 직접 다루는 방향으로 가고 있음을 보여줍니다."
            ),
            "confidence": "High",
            "confidence_note": "self-play, post-training, synthetic driving scenes, formal specification, degraded navigation이 같은 실패면을 공유",
            "lab_action": "자율주행/UGV 실험에는 scenario generator, closed-loop intervention, violated STL priority, localization degradation을 별도 column으로 둡니다.",
            "limit": 5,
        },
        {
            "title": "Efficiency는 작게 만드는 문제가 아니라 spatial evidence를 잃지 않는 문제",
            "buckets": ["Efficiency/Systems", "Generation", "3D/Scene"],
            "ids": ["2606.19849", "2606.19932", "2606.20076", "2606.19483", "2606.20130", "2606.19961"],
            "needles": [
                "streaming videollms",
                "100 fps",
                "spatial-aware reduction",
                "variable-length tokenization",
                "layer-skipping",
                "self-distillation",
                "detail bottlenecks",
            ],
            "why": (
                "ViCoStream, Spatial-Aware Reduction, variable-length tokenization, LEAP, SAM3 self-distillation, RGB-to-SWIR detail bottleneck은 "
                "efficiency를 FLOPs 절감으로 끝내지 않습니다. 실시간 video LLM, visual state-space reduction, diffusion tokenizer, "
                "segmentation distillation 모두 어떤 spatial evidence가 남고 무엇이 사라지는지가 품질을 결정합니다."
            ),
            "confidence": "Medium",
            "confidence_note": "시스템/생성/segmentation 논문이 서로 다른 모델 계열이지만 공통적으로 evidence preservation을 다룸",
            "lab_action": "경량화 실험은 latency와 memory뿐 아니라 retained spatial cue, segmentation/detail loss, downstream decision delta를 함께 plot합니다.",
            "limit": 6,
        },
        {
            "title": "Reliability는 confidence 숫자보다 domain shift와 반증 증거를 분리해 보는 쪽으로 감",
            "buckets": ["Safety/Alignment", "Foundation Models", "Efficiency/Systems"],
            "ids": ["2606.19950", "2606.20032", "2606.20196", "2606.19736", "2606.20303", "2606.20161"],
            "needles": [
                "confidence calibration",
                "reliability-aware",
                "continual test-time adaptation",
                "adversarial camouflage",
                "generalization failures",
                "reliability-aware temporal",
            ],
            "why": (
                "MLLM confidence calibration, reliability-aware open-vocabulary change detection, continual test-time adaptation, physical adversarial camouflage, "
                "federated surgical AI generalization guard, video polyp reliability 논문은 reliability를 단일 confidence 값으로 보지 말라고 말합니다. "
                "어떤 domain shift인지, 어떤 반증 evidence가 있는지, adaptation이 source privacy와 충돌하는지까지 분리해야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "calibration, open-vocabulary change, CTTA, adversarial physical risk, surgical deployment guard가 reliability 축으로 직접 연결",
            "lab_action": "신뢰성 평가 row를 confidence, counter-evidence, domain-shift source, adaptation memory, physical attack exposure로 나눕니다.",
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Evidence-preserving VLA benchmark",
            "claim": "VLA 성공률과 함께 quantization, event memory, failure prediction이 action-relevant evidence를 얼마나 보존하는지 평가합니다.",
        },
        {
            "title": "World-model intervention audit",
            "claim": "video realism보다 image editing, camera/object/weather control, instrument-tissue dynamics가 downstream policy 판단을 어떻게 바꾸는지 측정합니다.",
        },
        {
            "title": "3D scene memory for robotics",
            "claim": "scene graph, part token, occupancy, calibration residual을 action/logging schema로 연결해 map representation의 실제 사용성을 평가합니다.",
        },
    ],
}


if __name__ == "__main__":
    build(PROFILE, "out/cv_new.json", "out/ro_new.json")
