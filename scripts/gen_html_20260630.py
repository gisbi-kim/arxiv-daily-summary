#!/usr/bin/env python3
"""Generate the 2026-06-30 arXiv daily briefing artifacts from /new parser outputs."""
from __future__ import annotations

from daily_backfill_lib import build, week_start


DATE = "2026-06-30"

PROFILE = {
    "date": DATE,
    "weekday": "Tue",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Daily /new parser output",
    "benchmark_note": "Daily artifact generated from arXiv /new parser output with abstracts available.",
    "thesis": (
        "6/30 batch는 대규모 submission volume 안에서 VLA, 3D Gaussian/SLAM, driving world model, "
        "VLM hallucination, edge inference가 모두 실제 deployment failure를 조기에 잡는 방향으로 모였습니다. "
        "APRL 관점에서는 low-latency action, robot-usable 3D map, closed-loop driving, grounded VLM, "
        "resource-constrained perception을 같은 실험 언어로 비교할 수 있습니다."
    ),
    "cluster_takeaway": (
        "오늘은 3D/Scene과 Generation volume이 크지만, top-level 결론은 rendering이나 생성 품질이 아닙니다. "
        "로봇이 행동하기 전에 무엇을 빠르게 보고, 어떤 map을 믿고, 어떤 world model을 거부해야 하는지를 "
        "failure-aware benchmark로 바꾸는 흐름이 강합니다."
    ),
    "trend_note": (
        "Tuesday /new는 cs.CV와 cs.RO 모두 크게 늘었고 3D/Scene, Generation, Foundation Models, "
        "Robot Learning이 두껍습니다. VCS-SLAM, Event-VLA, OpenVLA failure warning, OWMDrive, "
        "physics-grounded multi-agent world model, hallucination mitigation이 같은 release에서 나와 "
        "perception-to-action 검증 축을 더 촘촘하게 만듭니다."
    ),
    "cluster_specs": [
        {
            "title": "VLA 평가가 action latency에서 event fusion과 failure early warning으로 이동",
            "buckets": ["Robot Learning"],
            "ids": ["2606.29350", "2606.29384", "2606.29699", "2606.29267", "2606.29941", "2606.30456", "2606.30552"],
            "needles": ["vla", "robotic vlm", "failure", "event", "latency", "tactile", "chain-of-thought"],
            "why": (
                "VLA는 단순히 더 큰 model을 쓰는 문제가 아니라 action 전에 충분히 빨리 보고, 실패 신호를 빨리 잡고, "
                "touch나 event stream 같은 sensory evidence를 어떻게 합치는지의 문제로 바뀌고 있습니다. "
                "Fast Enough to Act, Event-VLA, OpenVLA failure warning, part grounding, tactile policy, real-world UR5, dense embodied CoT는 "
                "latency와 failure prediction을 같은 축에서 봐야 한다는 강한 evidence입니다."
            ),
            "confidence": "High",
            "confidence_note": "VLA latency, event fusion, visual distribution shift, tactile/real-robot evaluation paper가 동시에 나왔습니다.",
            "lab_action": (
                "UR5/LIBERO/RoboCasa task에서 token merging, event fusion, tactile cue, visual distribution shift를 "
                "ablation 변수로 두고 action latency, failure-warning lead time, unsafe action rate, task success를 비교합니다."
            ),
            "limit": 7,
        },
        {
            "title": "3D representation이 visual asset에서 localization 가능한 Gaussian-SLAM map으로 이동",
            "buckets": ["3D/Scene", "Embodied AI"],
            "ids": ["2606.29494", "2606.28371", "2606.28396", "2606.28581", "2606.28828", "2606.29374", "2606.30097"],
            "needles": ["slam", "gaussian", "localization", "radar", "satellite", "4d", "tracking"],
            "why": (
                "3D Gaussian과 reconstruction은 보기 좋은 asset을 넘어서 localization, tracking, dynamic scene reasoning에 들어가고 있습니다. "
                "VCS-SLAM, GeoISF, RadarTwin, SatSplat, Ground4D, L2D2-GS, CylindTrack은 map representation을 robot/driving sensor loop에서 "
                "pose drift와 object persistence로 평가해야 한다는 흐름입니다."
            ),
            "confidence": "High",
            "confidence_note": "SLAM, radar simulation, satellite Gaussian, 4D reconstruction, tracking paper가 geometry gate를 충족합니다.",
            "lab_action": (
                "same route에서 3DGS map, radar simulation, satellite/ground localization, 4D reconstruction baseline을 비교하고 "
                "pose drift, tracking ID switch, dynamic-object failure, downstream navigation success를 측정합니다."
            ),
            "limit": 7,
        },
        {
            "title": "Driving world model 평가가 scene generation에서 causal closed-loop risk로 이동",
            "buckets": ["Autonomous Driving", "Safety/Alignment", "Generation"],
            "ids": ["2606.28758", "2606.29020", "2606.29097", "2606.30421", "2606.28757", "2606.29115", "2606.30537"],
            "needles": ["driving", "world model", "traffic", "scenario", "causality", "multi-agent", "rollout"],
            "why": (
                "driving world model은 realistic video나 scenario text를 만드는 것만으로 충분하지 않습니다. "
                "X-Mind, physics-informed weather synthesis, TrafficAlign, OWMDrive, physics-grounded multi-agent dynamics, minimal-risk condition, "
                "rollout-retrieval lifelong driving은 scenario generator가 closed-loop risk와 causal intervention을 견디는지 봐야 한다는 묶음입니다."
            ),
            "confidence": "High",
            "confidence_note": "world-model driving, traffic scenario generation, physics benchmark, minimal-risk condition paper가 한 축으로 연결됩니다.",
            "lab_action": (
                "CARLA/OpenSCENARIO에서 weather, traffic prompt, occupancy horizon, human interaction, retrieval memory를 stress split으로 만들고 "
                "near-miss, intervention count, rule violation, recovery success를 비교합니다."
            ),
            "limit": 7,
        },
        {
            "title": "VLM reliability가 hallucination mitigation에서 grounded routing과 temporal reasoning 검증으로 이동",
            "buckets": ["Foundation Models", "Safety/Alignment"],
            "ids": ["2606.28401", "2606.28520", "2606.28551", "2606.28593", "2606.28862", "2606.28864", "2606.29805"],
            "needles": ["hallucination", "grounding", "vlm", "temporal", "test-time", "preference", "uncertainty"],
            "why": (
                "VLM reliability는 hallucination을 줄였다는 평균 점수보다 어떤 visual evidence가 answer routing을 바꾸는지가 중요합니다. "
                "preference synthesis, clinical hallucination uncertainty, DataComp-VLM, Animation2Code, detector-grounded reasoning, test-time scaling, "
                "pickup preference optimization은 grounded evidence와 temporal reasoning 실패를 분리해야 한다는 흐름입니다."
            ),
            "confidence": "High",
            "confidence_note": "hallucination, dataset curation, detector grounding, temporal reasoning, test-time scaling 신호가 강합니다.",
            "lab_action": (
                "VideoQA/VLM navigation prompt에서 counterfactual visual grounding, detector binding, temporal keyframe removal을 "
                "ablation으로 만들고 hallucination rate, answer routing change, downstream task success를 비교합니다."
            ),
            "limit": 7,
        },
        {
            "title": "Edge perception이 compression 절약에서 mission-critical evidence 보존 평가로 이동",
            "buckets": ["Efficiency/Systems", "Generation", "Robot Learning"],
            "ids": ["2606.28398", "2606.28516", "2606.29337", "2606.29360", "2606.28421", "2606.29350", "2606.30215"],
            "needles": ["edge", "resource", "quantization", "fast", "token", "compression", "sparse"],
            "why": (
                "edge deployment는 latency나 compression 수치만 줄이면 끝나는 문제가 아닙니다. "
                "semantic image transmission, CLEAR-MoE, W4A4 quantization, SAFE-DiT, edge-native T2I, low-latency robotic VLM, sparse cross-modality fusion은 "
                "resource budget을 줄일 때 task-critical evidence가 남는지 평가해야 한다는 신호입니다."
            ),
            "confidence": "Medium",
            "confidence_note": "resource-constrained transmission, MoE extraction, quantization, fast diffusion, robotic token merging이 연결됩니다.",
            "lab_action": (
                "robot perception and visual-IoT benchmark에서 bandwidth, token budget, quantization, expert count를 단계적으로 줄이고 "
                "critical-object recall, action latency, downstream decision change, failure recovery를 비교합니다."
            ),
            "limit": 7,
        },
        {
            "title": "Embodied navigation이 route success에서 world-action memory와 delayed measurement robustness로 이동",
            "buckets": ["Embodied AI", "Robot Learning"],
            "ids": ["2606.28397", "2606.29908", "2606.29934", "2606.30367", "2606.30404", "2606.29123", "2606.32222"],
            "needles": ["navigation", "world-action", "memory", "delays", "vln", "object goal", "routines"],
            "why": (
                "embodied navigation은 성공 여부보다 retrieval, world-action memory, delayed measurement, routine prediction이 "
                "실패 직전에 어떻게 작동하는지가 중요합니다. CLOSER-VLN, spatial-perceiving world action model, RoamFlow, FutureNav, HUMEMBR, aided inertial delays는 "
                "long-horizon route에서 memory와 measurement delay를 같이 평가해야 한다는 신호입니다."
            ),
            "confidence": "Medium",
            "confidence_note": "VLN, image-goal navigation, world-action model, inertial delay, routine prediction paper가 실험 후보를 만듭니다.",
            "lab_action": (
                "VLN/ObjectNav route에서 retrieval memory, world-action horizon, measurement delay, routine prior를 stress split으로 두고 "
                "route success, detour recovery, localization drift, unsafe stop을 비교합니다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "VLA early-warning benchmark",
            "claim": "token merging, event fusion, tactile cue, visual shift를 같은 robot task에서 ablation해 failure-warning lead time과 unsafe action rate를 측정합니다.",
        },
        {
            "title": "Gaussian-SLAM robot map trial",
            "claim": "3DGS, radar simulation, satellite/ground geo-localization, VCS-SLAM을 pose drift와 downstream navigation success로 비교합니다.",
        },
        {
            "title": "Closed-loop driving world-model stress suite",
            "claim": "traffic prompt, occupancy world model, human interaction, weather synthesis를 조작해 near-miss와 recovery success를 평가합니다.",
        },
    ],
}


if __name__ == "__main__":
    build(PROFILE, "out/cv_20260630.json", "out/ro_20260630.json")
