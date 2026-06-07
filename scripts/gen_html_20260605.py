#!/usr/bin/env python3
"""Generate the 2026-06-05 arXiv daily briefing artifacts from /new parser outputs."""
from __future__ import annotations

from daily_backfill_lib import build, week_start


DATE = "2026-06-05"

PROFILE = {
    "date": DATE,
    "weekday": "Fri",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Daily /new parser output",
    "benchmark_note": "Daily artifact generated from arXiv /new parser output with abstracts available.",
    "thesis": (
        "6/5 /new 배치는 단일 대표 모델보다 실행 표면이 더 중요합니다. VLA action generation, "
        "휴머노이드와 dexterous manipulation, geometry-grounded navigation, video/world-model evaluation, "
        "safety-critical driving이 모두 로봇 스택에 바로 붙일 수 있는 검증 항목으로 나타났습니다."
    ),
    "trend_note": (
        "가장 강한 신호는 Robot Learning과 Generation이 동시에 넓게 퍼졌고, 3D/Scene, Foundation Models, "
        "Efficiency/Systems, Safety/Alignment가 그 위에 evidence gate와 runtime gate를 제공한다는 점입니다. "
        "APRL 관점에서는 affordance grounding, spatial memory, trajectory risk, token/cache budget, "
        "OOD와 safety failure mode를 한 장의 평가표에 묶어야 하는 배치로 읽는 편이 맞습니다."
    ),
    "cluster_specs": [
        {
            "title": "VLA와 robot policy가 더 단순한 action interface로 이동",
            "buckets": ["Robot Learning", "Efficiency/Systems"],
            "ids": ["2606.05737", "2606.06155", "2606.05254", "2606.06194"],
            "needles": [
                "vision-language-action",
                "vla",
                "world action model",
                "affordance",
                "egocentric",
                "one-step action",
            ],
            "why": (
                "이 묶음의 VLA 논문들은 로봇 policy 실행을 더 단순한 action-generation interface로 압축해도 "
                "실제 grounding을 잃지 않을 수 있는지를 묻습니다. One-step action generation, affordance-conditioned "
                "action, world-action distillation, egocentric active-perception pretraining은 모두 같은 질문을 다른 "
                "각도에서 찌릅니다. 로봇이 행동을 확정하기 전에 정말 필요한 중간 표현이 무엇인지 확인해야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "VLA, affordance, world-action, egocentric pretraining 논문이 직접 연결됨",
            "lab_action": "같은 manipulation split에서 action-token budget, affordance hit rate, recovery rate, policy latency를 함께 기록합니다.",
        },
        {
            "title": "Manipulation이 bimanual cloth, dexterous grasping, symbolic recovery로 확장",
            "buckets": ["Robot Learning", "Embodied AI"],
            "ids": ["2606.06292", "2606.05407", "2606.05248", "2606.05873", "2606.06040"],
            "needles": [
                "bimanual",
                "cloth",
                "dexterous",
                "grasping",
                "symbolic planning",
                "humanoid",
                "vine robots",
            ],
            "why": (
                "이 manipulation 묶음은 단순한 demonstration-data 배치가 아닙니다. Bimanual cloth perception을 위한 "
                "synthetic data, diffusion-policy dexterous grasping, symbolic planning과 residual operator learning, "
                "humanoid ladder climbing, fast vine-robot hardware가 한꺼번에 나옵니다. 따라서 구조를 어디에 넣을지, "
                "즉 perception label, policy prior, symbolic recovery logic, platform-specific mechanics 중 무엇이 "
                "실패 복구에 실질적으로 기여하는지 비교하기 좋습니다."
            ),
            "confidence": "High",
            "confidence_note": "여러 manipulation 및 embodied hardware 논문이 contact-rich execution으로 연결됨",
            "lab_action": "contact-rich task마다 phase label, recovery trigger, synthetic-data source, hardware-specific failure tag를 남깁니다.",
        },
        {
            "title": "Geometry와 navigation은 시각 장식이 아니라 grounded state가 됨",
            "buckets": ["3D/Scene", "Embodied AI", "Autonomous Driving"],
            "ids": ["2606.05506", "2606.05774", "2606.05833", "2606.05975", "2606.06312", "2606.05372"],
            "needles": [
                "navigation",
                "geometric",
                "grounded",
                "spatial",
                "3d functionality",
                "geo-localization",
                "distance functions",
            ],
            "why": (
                "오늘의 Geometry/SLAM/Reconstruction watch lens에 해당하는 묶음입니다. Privileged sensor contrast를 "
                "쓰는 PointGoal navigation, grounded driving transformer, video-derived geometric representation, "
                "open-vocabulary 3D functionality segmentation, cross-view geo-localization, navigation vector-field "
                "distance function은 모두 같은 요구를 가리킵니다. Spatial state는 예쁜 scene representation으로 렌더링되는 "
                "것에서 끝나면 안 되고, policy가 질의할 수 있는 상태로 남아야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "navigation, grounded driving, spatial MLLM, functionality segmentation, geo-localization 논문이 함께 존재",
            "lab_action": "map을 localization error, traversability/functionality query accuracy, downstream navigation success로 평가합니다.",
        },
        {
            "title": "Video와 world-model 평가는 control, memory, preference로 이동",
            "buckets": ["Generation", "Autonomous Driving", "Foundation Models"],
            "ids": ["2606.05665", "2606.05677", "2606.06423", "2606.05259", "2606.05399", "2606.05478"],
            "needles": [
                "video-to-video",
                "video understanding",
                "spatial memory",
                "scenario generation",
                "flow matching",
                "human preference",
            ],
            "why": (
                "이 generation 묶음이 유용한 이유는 image quality만 보지 않고 controllability에 평가 압력을 걸기 때문입니다. "
                "V2V-Bench, long-horizon spatial memory, safety-critical traffic scenario generation, knowledge-intensive "
                "video understanding, flow matching 기반 physics learning, preference prediction은 world-model 연구가 "
                "visual realism뿐 아니라 intervention consistency, 기억된 spatial fact, risk coverage를 함께 보고해야 한다고 말합니다."
            ),
            "confidence": "High",
            "confidence_note": "video generation, spatial memory, risk scenario generation, physics learning 논문이 같은 방향으로 정렬됨",
            "lab_action": "world-model eval에 intervention consistency, spatial recall, preference prediction, risk-scenario diversity를 추가합니다.",
        },
        {
            "title": "Efficiency 논문들은 multimodal system 안의 runtime knob를 드러냄",
            "buckets": ["Efficiency/Systems", "Foundation Models", "Generation"],
            "ids": ["2606.05703", "2606.05624", "2606.05489", "2606.05826", "2606.05758", "2606.05535"],
            "needles": [
                "fast",
                "kv",
                "index optimization",
                "adapter",
                "noise-aware",
                "efficient",
                "decoding",
            ],
            "why": (
                "Efficiency 신호는 retrieval, generation, representation learning, control 전반에 흩어져 있습니다. "
                "Fast autoregressive image decoding, motion control을 위한 K/V injection, ANN index optimization, "
                "residual-flow adapter, noise-aware visual representation learning은 같은 nominal model에서도 결과를 바꿀 수 있는 "
                "runtime knob입니다. 따라서 systems choice를 부가 설정이 아니라 scientific claim의 일부로 기록해야 합니다."
            ),
            "confidence": "Medium",
            "confidence_note": "application surface는 다르지만 runtime 또는 parameter-efficiency 압력이 공통으로 나타남",
            "lab_action": "method 비교 전에 latency, memory, retrieval recall, control fidelity, accuracy를 하나의 Pareto table로 보고합니다.",
        },
        {
            "title": "Reliability와 safety는 OOD, representation steering, traffic risk로 분해됨",
            "buckets": ["Safety/Alignment", "Foundation Models", "Autonomous Driving", "Generation"],
            "ids": ["2606.05536", "2606.05290", "2606.06423", "2606.06074", "2606.06219", "2606.05576"],
            "needles": [
                "ood",
                "safety",
                "risk",
                "crash",
                "adaptive routing",
                "evidence-grounded",
                "safe visual generation",
            ],
            "why": (
                "이 배치에서 reliability는 하나의 metric이 아닙니다. Fine-grained OOD detection, safe visual generation을 위한 "
                "cross-model steering, crash data, end-to-end driving의 cognition-aware routing, risk-flow traffic scenario, "
                "evidence-grounded VQA는 서로 다른 실패 원인을 분리합니다. 로봇과 driving 연구에서는 failure가 distribution shift, "
                "routing, scenario coverage, unsupported visual evidence 중 어디에서 왔는지 명시해야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "OOD, safety steering, crash/risk data, adaptive routing, evidence-grounding 논문이 직접 포함됨",
            "lab_action": "aggregate score 전에 각 failure에 OOD source, routing decision, scenario-risk class, evidence support tag를 붙입니다.",
        },
    ],
    "research_topics": [
        {
            "title": "Affordance-conditioned VLA action budget",
            "claim": "같은 manipulation task에서 one-step action, affordance grounding, world-action distillation을 비교합니다.",
        },
        {
            "title": "Geometry-as-state navigation eval",
            "claim": "geometric representation이 localization, traversability, functionality query, policy success를 실제로 개선하는지 측정합니다.",
        },
        {
            "title": "Risk-aware world-model benchmark",
            "claim": "video-to-video quality, spatial recall, intervention consistency, safety-critical scenario diversity를 한 평가로 묶습니다.",
        },
    ],
}


if __name__ == "__main__":
    build(PROFILE, "out/cv_new.json", "out/ro_new.json")
