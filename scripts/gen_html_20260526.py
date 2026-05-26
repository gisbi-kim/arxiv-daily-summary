#!/usr/bin/env python3
"""Generate the 2026-05-26 arXiv daily briefing artifacts from /new parser outputs."""
from __future__ import annotations

from daily_backfill_lib import build, week_start


DATE = "2026-05-26"

PROFILE = {
    "date": DATE,
    "weekday": "화",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Daily /new parser output",
    "benchmark_note": "Daily artifact generated from arXiv /new parser output with abstracts available.",
    "thesis": (
        "26일 배치는 world model, VLA, 3D scene understanding이 대규모로 쏟아진 날입니다. "
        "Nano World Models, SparseWorld, DexSIM, QuoVLA, EgoProx가 보여주듯 핵심 질문은 모델 크기보다 future prediction, action quantization, sparse scene memory, 3D proximity reasoning을 "
        "실제 robot/driving runtime 안에 어떻게 넣느냐입니다."
    ),
    "trend_note": (
        "Generation, Foundation Models, Efficiency/Systems가 가장 크지만 Robot Learning과 3D/Scene도 두껍습니다. "
        "특히 world model, VLA quantization, cooperative driving, 3DGS/physical scene understanding이 서로 분리되지 않고 같은 runtime budget 문제로 연결됩니다."
    ),
    "cluster_specs": [
        {
            "title": "World model은 future video prediction에서 driving sparse scene까지 확장",
            "buckets": ["Generation", "Autonomous Driving", "Robot Learning", "Embodied AI"],
            "ids": ["2605.23993", "2605.24354", "2605.24892", "2605.24630", "2605.24578", "2605.23992"],
            "needles": ["world model", "future video prediction", "sparse scene", "predictive world", "causal video diffusion", "group actions"],
            "why": (
                "Nano World Models는 future video prediction을 최소 구현으로 끌어내리고, SparseWorld와 X-Foresight는 driving/robot action forecasting으로 연결합니다. "
                "DexSIM의 real-time dexterous simulation과 World Models as Group Actions까지 보면 world model은 영상 생성 모듈이 아니라 action-conditioned state transition layer가 됩니다. "
                "따라서 평가도 FVD류 품질보다 action success, sparse scene memory, rollout stability를 같이 봐야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "world model, predictive action, sparse driving scene 신호가 여러 버킷에 걸쳐 등장",
            "lab_action": "world model 후보를 future prediction, sparse scene update, action-conditioned rollout success로 같은 protocol에 올림",
        },
        {
            "title": "VLA는 quantization, quotient space, geometric foundation model로 구조화",
            "buckets": ["Robot Learning", "Efficiency/Systems", "3D/Scene", "Foundation Models"],
            "ids": ["2605.24011", "2605.24890", "2605.24642", "2605.24892", "2605.24630"],
            "needles": ["vision-language-action", "vla", "action-guided quantization", "quotient space", "geometric foundation", "vision-action", "robotic inference"],
            "why": (
                "ActQuant는 VLA를 sub-4-bit action-guided quantization 대상으로 만들고, QuoVLA는 action space 구조를 quotient space로 봅니다. "
                "geometric foundation model이 VLA에 주는 영향과 X-Foresight의 vision-action causal forecasting까지 합치면, 오늘의 VLA 흐름은 더 큰 policy보다 action representation, geometry prior, inference budget입니다. "
                "로봇 실험은 VLA accuracy와 함께 quantization error, geometry prior ablation, action rollout failure를 같이 기록해야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "VLA quantization, quotient/action space, geometric prior 논문이 직접 연결",
            "lab_action": "VLA benchmark에서 bit-width, action-space parameterization, geometry-prior on/off를 long-horizon success와 latency로 비교",
        },
        {
            "title": "3D scene은 physical world modeling과 Gaussian synthesis 사이로 이동",
            "buckets": ["3D/Scene", "Generation", "Embodied AI", "Efficiency/Systems"],
            "ids": ["2605.24321", "2605.24304", "2605.24114", "2605.24074", "2605.25059", "2605.24243"],
            "needles": ["3d scene", "physical world modeling", "3dgs", "gaussian splatting", "depth estimation", "semantic occupancy", "3d semantic segmentation"],
            "why": (
                "Unified 3D Scene Understanding Through Physical World Modeling은 scene understanding을 physics-aware representation으로 밀고, ArtSplat과 COSY는 3DGS synthesis/editing을 세분화합니다. "
                "WideDepth, VEOcc, GIBLy까지 보면 depth, occupancy, semantic segmentation이 모두 physical scene state를 더 싸고 안정적으로 추정하는 문제로 묶입니다. "
                "평가는 rendering fidelity만이 아니라 physical plausibility, occupancy consistency, lightweight segmentation 성능을 함께 봐야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "physical world modeling, 3DGS, depth/occupancy/segmentation 논문이 함께 등장",
            "lab_action": "3DGS/occupancy/depth 모델을 physical plausibility, online update cost, downstream navigation utility로 비교",
        },
        {
            "title": "VLM reliability는 hallucination gating과 egocentric 3D reasoning으로 이동",
            "buckets": ["Foundation Models", "Safety/Alignment", "Embodied AI", "3D/Scene"],
            "ids": ["2605.24024", "2605.24456", "2605.23997", "2605.24159", "2605.24020"],
            "needles": ["hallucinations", "vision-language", "visual-grounded reasoning", "egocentric", "3d proximity", "conversational assistance", "visual and linguistic"],
            "why": (
                "causal route gating은 LVLM hallucination을 내부 경로 제어 문제로 보고, EgoProx는 egocentric 3D proximity reasoning을 계층적으로 평가합니다. "
                "IVR-R1의 visual-grounded reasoning과 EchoVQA 같은 domain assistant까지 보면 reliability는 일반 QA 점수보다 grounding route, spatial proximity, expert interaction failure로 나뉩니다. "
                "VLM 평가는 hallucination flag와 함께 3D evidence localization, route attribution, human-assistance context를 저장해야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "hallucination gating, visual-grounded reasoning, egocentric 3D benchmark가 연결",
            "lab_action": "VLM logs에 causal route, 3D proximity evidence, final answer confidence를 같이 기록",
        },
        {
            "title": "Driving은 cooperative V2X, language nudge, safety prediction을 한 stack으로 묶음",
            "buckets": ["Autonomous Driving", "Safety/Alignment", "Generation", "3D/Scene"],
            "ids": ["2605.24098", "2605.24354", "2605.24531", "2605.24040", "2605.24014"],
            "needles": ["autonomous driving", "cooperative", "v2x", "end-to-end driving", "safety prediction", "semantic segmentation", "sparse scene"],
            "why": (
                "D2-V2X는 cooperative reasoning을, SparseWorld는 sparse scene world model을, NudgeVAD는 language-nudged driving을 전면에 둡니다. "
                "cycling safety prediction과 heterogeneous UAV segmentation까지 같이 보면 autonomous stack은 perception, language cue, cooperative sensing, safety prediction을 따로 최적화하기 어렵습니다. "
                "driving benchmark는 cooperative availability, language cue sensitivity, safety intervention rate를 같이 측정해야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "V2X, sparse-world driving, language-nudged driving, safety prediction 논문이 같은 날짜에 존재",
            "lab_action": "closed-loop driving split에서 V2X on/off, language cue perturbation, sparse-scene memory를 intervention rate로 비교",
        },
        {
            "title": "Efficiency는 quantization, feature coding, lightweight geometry로 runtime을 압축",
            "buckets": ["Efficiency/Systems", "Robot Learning", "Foundation Models", "3D/Scene"],
            "ids": ["2605.24019", "2605.24025", "2605.24011", "2605.24243", "2605.24044"],
            "needles": ["quantization", "feature coding", "lightweight", "compression", "scheduling", "robotic inference", "gradient-hessian"],
            "why": (
                "MGVQ와 large model feature coding은 representation을 줄이고, ActQuant는 VLA action space를 직접 압축합니다. "
                "GIBLy의 lightweight 3D segmentation과 RED의 robotic inference scheduling까지 붙으면 efficiency는 모델 파일 크기 문제가 아니라 perception-action loop의 latency budget입니다. "
                "실사용 전환은 accuracy drop뿐 아니라 scheduler stability, action latency, geometry quality를 한 Pareto curve에 놓아야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "quantization, feature coding, lightweight geometry, robotic scheduling 신호가 반복",
            "lab_action": "robot runtime에서 quantization ratio, scheduler delay, geometry quality, policy success를 동시에 기록",
        },
    ],
    "research_topics": [
        {
            "title": "Action-conditioned world-model benchmark",
            "claim": "Nano World Models, SparseWorld, X-Foresight, DexSIM을 future prediction, sparse scene memory, action success로 비교합니다.",
        },
        {
            "title": "Compressed VLA runtime curve",
            "claim": "ActQuant, QuoVLA, geometric-foundation VLA variants를 bit-width, action-space structure, geometry prior 기준으로 ablation합니다.",
        },
        {
            "title": "3D evidence reliability log",
            "claim": "EgoProx, hallucination gating, IVR-R1을 3D proximity evidence, route attribution, final-answer correctness로 분리 평가합니다.",
        },
    ],
}


if __name__ == "__main__":
    build(PROFILE, "out/cv_new.json", "out/ro_new.json")
