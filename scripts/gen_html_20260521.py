#!/usr/bin/env python3
"""Generate the 2026-05-21 arXiv daily briefing artifacts from date-section backfill outputs."""
from __future__ import annotations

from daily_backfill_lib import build, week_start


DATE = "2026-05-21"

PROFILE = {
    "date": DATE,
    "weekday": "목",
    "week_start": week_start(DATE),
    "thesis": (
        "21일은 generation이 압도적으로 많지만, 더 중요한 결은 long-video drift, 3D/multi-view memory, "
        "driving VLA grounding, Gaussian-field control이 서로 붙기 시작했다는 점입니다. VLM 쪽도 hallucination을 "
        "막는다고 말하는 수준을 넘어 evidence benchmark와 medical/road grounding처럼 실패 로그를 남기는 쪽으로 내려왔습니다."
    ),
    "trend_note": (
        "Generation이 29편으로 가장 크고 Foundation Models도 19편입니다. 다만 robotics 관점에서는 Driving VLA, "
        "LiDAR/SLAM/Gaussian active perception, tactile/contact-rich manipulation, risk-aware planning을 별도로 읽어야 합니다."
    ),
    "cluster_specs": [
        {
            "title": "Geometry가 closed-loop driving sim과 Gaussian-field control로 붙음",
            "buckets": ["3D/Scene", "Autonomous Driving", "Safety/Alignment"],
            "ids": ["2605.21032", "2605.21150", "2605.20752", "2605.20566", "2605.20484", "2605.21007"],
            "needles": ["4d scene", "reconstruction", "closed-loop", "lidar", "odometry", "gaussian", "slam", "3d point", "active perception", "control barrier"],
            "why": (
                "이날 geometry 신호는 단순한 3D 복원보다 closed-loop simulation과 control substrate 쪽이 강합니다. "
                "4D scene reconstruction for driving simulation, EllipseLIO, GaussianDream, 3DGS field control, GNSS-denied SLAM이 "
                "같이 나오면서 map이 rendering asset이 아니라 주행/로봇 제어가 기대는 상태 표현으로 이동합니다."
            ),
            "confidence": "High",
            "confidence_note": "driving simulation, LIO/SLAM, Gaussian manipulation/control 논문이 함께 연결",
            "lab_action": "4D scene sim, LiDAR-inertial odometry, Gaussian-field active perception을 closed-loop planning failure 기준으로 비교",
        },
        {
            "title": "Driving VLA는 language interface보다 action grounding과 fog stress가 병목",
            "buckets": ["Robot Learning", "Autonomous Driving", "Foundation Models"],
            "ids": ["2605.21273", "2605.21061", "2605.21446", "2605.21414", "2605.20774", "2605.21139"],
            "needles": ["driving vla", "vla", "meta-action", "inverse kinematics", "fog", "point-action", "real-world evaluation", "foresee"],
            "why": (
                "DriveMA와 Grounding Driving VLA는 language interface를 action unit과 inverse kinematics로 다시 묻습니다. "
                "Lost in Fog와 VLA-REPLICA가 붙으면 문제는 말 잘하는 driving agent가 아니라 센서 perturbation과 real-world benchmark에서 "
                "같은 instruction이 실제 제어로 안정적으로 내려가느냐입니다."
            ),
            "confidence": "High",
            "confidence_note": "driving VLA, stress perturbation, real-world VLA benchmark가 같은 날짜에 등장",
            "lab_action": "driving VLA를 clear/fog sensor split, one-step meta-action, inverse-kinematics grounding으로 나눠 closed-loop SR과 intervention rate를 측정",
        },
        {
            "title": "Generation은 long-video drift와 3D/multi-view memory를 동시에 줄이려는 날",
            "buckets": ["Generation", "3D/Scene", "Efficiency/Systems"],
            "ids": ["2605.21472", "2605.21466", "2605.21042", "2605.21028", "2605.20910", "2605.20476", "2605.21121"],
            "needles": ["stream3d", "streaming", "video", "long video", "drift", "multi-view", "3d generation", "memory", "diffusion", "autoregressive"],
            "why": (
                "Stream3D, StreamGVE, Dynamic Video Generation, DySink, FlowLong, Goodbye Drift가 같이 나오면 핵심은 샘플 품질이 아닙니다. "
                "긴 영상에서 시간이 흐를수록 무너지는 drift를 줄이고, multi-view/3D memory를 유지하며, 편집과 생성을 streaming으로 가져가려는 흐름입니다. "
                "video generation이 짧은 clip demo에서 long-horizon controllability 문제로 옮겨간 셈입니다."
            ),
            "confidence": "High",
            "confidence_note": "long-video, streaming editing, multi-view 3D generation 논문 5편 이상 연결",
            "lab_action": "long-video benchmark에서 temporal drift, view consistency, edit latency, memory footprint를 분리한 평가표를 만듭니다",
        },
        {
            "title": "VLM reliability는 hallucination 완화보다 evidence-grounded benchmark로 정착",
            "buckets": ["Foundation Models", "Safety/Alignment"],
            "ids": ["2605.21479", "2605.21443", "2605.21300", "2605.20965", "2605.20772", "2605.20676", "2605.20469"],
            "needles": ["vqabench", "glitch", "hallucination", "visual evidence", "medical", "evidence", "benchmark", "content rating", "road-damage"],
            "why": (
                "WikiVQABench, TempGlitch, object hallucination 완화, inter-layer visual attention discrepancy, VIHD, VISTAQA, HalluCXR는 "
                "모두 VLM 답변을 evidence와 함께 검증하려는 흐름입니다. 특히 knowledge grounding, temporal glitch, medical VQA, pixel-level evidence가 "
                "나뉘어 나와서 '환각 줄임'이라는 한 문장 claim을 task별 failure log로 쪼갤 수 있습니다."
            ),
            "confidence": "High",
            "confidence_note": "hallucination/evidence benchmark가 서로 다른 domain에서 반복",
            "lab_action": "knowledge VQA, gameplay temporal glitch, medical VQA, road grounding을 같은 evidence-required VLM evaluation schema로 통합",
        },
        {
            "title": "Robot manipulation은 humanoid scale-up과 tactile/contact-rich benchmark로 이동",
            "buckets": ["Robot Learning", "Embodied AI"],
            "ids": ["2605.20373", "2605.21429", "2605.21330", "2605.21133", "2605.20894", "2605.20433", "2605.20392"],
            "needles": ["humanoid", "manipulation", "tactile", "contact-rich", "visuo-haptic", "mobile manipulation", "dexterous", "loco-manipulation"],
            "why": (
                "SUGAR, Robot Tactile Olympiad, dexterous in-hand manipulation, whole-body manipulation, Mobile UMI, visuo-haptic imitation, tactile MPC는 "
                "로봇 조작을 단순 pick-and-place에서 몸 전체, 촉각, 접촉-rich feedback으로 확장합니다. VLA가 상위 interface를 맡더라도 "
                "실제 성공은 tactile/contact state와 embodiment scale-up에서 갈릴 가능성이 큽니다."
            ),
            "confidence": "High",
            "confidence_note": "humanoid, tactile, contact-rich manipulation 신호가 독립적으로 반복",
            "lab_action": "RoboCasa/LIBERO류 task에 tactile-only, vision-only, visuo-haptic policy를 같은 contact-rich split으로 비교",
        },
        {
            "title": "Risk-aware planning은 uncertainty field와 barrier-control 양쪽에서 올라옴",
            "buckets": ["Autonomous Driving", "Safety/Alignment", "Efficiency/Systems"],
            "ids": ["2605.21309", "2605.21406", "2605.21257", "2605.21138", "2605.20301", "2605.20728"],
            "needles": ["uncertainty", "risk", "motion planning", "barrier", "safety-critical", "robust", "ood", "cooperative", "3d object detection"],
            "why": (
                "Hyper-V2X, MC-Risk, differentiable CVaR barrier functions, smoothed implicit contact dynamics, Co-Fusion4D, geometry-sensitive OOD가 "
                "같은 날 나온 것은 risk를 사후 점수로 보는 대신 planning/control 안에 넣으려는 신호입니다. perception uncertainty와 barrier-based control을 "
                "분리해서 보지 않고, 둘이 같은 closed-loop safety budget을 두고 경쟁한다고 봐야 합니다."
            ),
            "confidence": "Medium",
            "confidence_note": "driving risk field와 robotics control safety 논문이 같은 방향을 보임",
            "lab_action": "BEV uncertainty, risk field, CVaR barrier, contact safety controller를 같은 near-miss / intervention metric으로 비교",
        },
    ],
    "research_topics": [
        {
            "title": "Driving VLA grounding stress suite",
            "claim": "DriveMA, Grounding Driving VLA, Lost in Fog, VLA-REPLICA를 fog/clear split과 inverse-kinematics grounding split에서 같은 closed-loop metric으로 비교합니다.",
        },
        {
            "title": "Long-video generation drift board",
            "claim": "Stream3D, StreamGVE, DySink, FlowLong, Goodbye Drift를 view consistency, identity drift, edit latency, memory footprint 네 축으로 평가합니다.",
        },
        {
            "title": "Evidence-required VLM reliability schema",
            "claim": "WikiVQABench, TempGlitch, VIHD, VISTAQA, HalluCXR를 answer-only score와 evidence-localization score로 분리해 하나의 failure log로 묶습니다.",
        },
    ],
}


if __name__ == "__main__":
    build(PROFILE, f"out/cv_{DATE}.json", f"out/ro_{DATE}.json")
