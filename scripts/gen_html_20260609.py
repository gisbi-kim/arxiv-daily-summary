#!/usr/bin/env python3
"""Generate the 2026-06-09 arXiv daily briefing artifacts from /new parser outputs."""
from __future__ import annotations

from daily_backfill_lib import build, week_start


DATE = "2026-06-09"

PROFILE = {
    "date": DATE,
    "weekday": "Tue",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Daily /new parser output",
    "benchmark_note": "Daily artifact generated from arXiv /new parser output with abstracts available.",
    "thesis": (
        "6/9 /new 배치는 VLA와 world-action model이 action representation, memory, uncertainty, contact sensing 쪽으로 갈라진 날입니다. "
        "동시에 geometry와 driving 쪽은 reconstruction score보다 실제 grasping, LiDAR-camera fusion, closed-loop safety로 이어지는 검증 신호가 강합니다."
    ),
    "trend_note": (
        "어제보다 총량이 크게 늘었고 Robot Learning, Foundation Models, Generation이 모두 두껍습니다. "
        "로봇 쪽에서는 VLA, WAM, tactile/contact, humanoid, teleoperation이 같은 배치에 몰렸고, "
        "CV 쪽에서는 video world model, token/memory efficiency, reliability benchmark가 같이 올라왔습니다. "
        "APRL 관점에서는 모델 크기 경쟁보다 action interface, spatial state, failure recovery, runtime budget을 같이 재는 것이 핵심입니다."
    ),
    "cluster_specs": [
        {
            "title": "VLA와 WAM은 action representation 경쟁으로 이동",
            "buckets": ["Robot Learning"],
            "ids": ["2606.07895", "2606.08530", "2606.09215", "2606.09827", "2606.09811", "2606.09630"],
            "needles": [
                "vla",
                "vision-language-action",
                "world action",
                "world model",
                "action representation",
                "action decoding",
                "memory",
                "failure recovery",
            ],
            "why": (
                "TBD-VLA, GEAR-VLA, MotionWAM, MemoryVLA++, AHA-WAM이 한꺼번에 나오면서 VLA의 병목이 backbone이 아니라 "
                "action을 어떤 latent, geometry-aware representation, temporal memory, observation-routed context로 표현하느냐로 이동합니다. "
                "ReCoVLA까지 보면 실패 후 reward를 어떻게 재구성해 recovery policy로 돌리는지도 같은 축에 들어옵니다."
            ),
            "confidence": "High",
            "confidence_note": "VLA, world-action model, memory, failure recovery 논문이 같은 Robot Learning 버킷에 밀집",
            "lab_action": "동일 manipulation split에서 action-token horizon, memory length, observation routing, failure recovery success를 같은 table로 비교합니다.",
            "limit": 5,
        },
        {
            "title": "Contact-rich manipulation은 tactile, teleoperation, degradation test가 관건",
            "buckets": ["Robot Learning"],
            "ids": ["2606.09337", "2606.08737", "2606.08341", "2606.08881", "2606.09243", "2606.08121"],
            "needles": [
                "tactile",
                "contact-rich",
                "teleoperation",
                "manipulation",
                "failure",
                "recovery",
                "grasp pressure",
                "degradation",
            ],
            "why": (
                "TORL-VLA와 Dream-Tac은 contact-rich manipulation에서 tactile signal을 policy update와 world-action model 안으로 넣습니다. "
                "EgoTactile은 egocentric video에서 grasp pressure를 학습하고, uncertainty-aware teleoperation과 SO-101 failure analysis는 "
                "사람 개입, 실패 복구, degradation 조건을 별도 실험 축으로 세워야 한다는 신호입니다."
            ),
            "confidence": "High",
            "confidence_note": "tactile, grasp pressure, teleoperation, VLA failure analysis가 같은 문제를 다른 센서와 프로토콜에서 다룸",
            "lab_action": "contact-rich task에서 tactile ablation, human intervention timing, pressure prediction error, recovery count를 로그로 남깁니다.",
            "limit": 5,
        },
        {
            "title": "Geometry watch: reconstruction이 grasping, fusion, navigation utility로 내려옴",
            "buckets": ["3D/Scene"],
            "ids": ["2606.08440", "2606.08844", "2606.08284", "2606.08729", "2606.09292", "2606.08402"],
            "needles": [
                "reconstruction",
                "grasp",
                "3d foundation",
                "fisheye",
                "lidar",
                "pose estimation",
                "odometry",
                "navigation",
                "simulator",
                "scene generation",
            ],
            "why": (
                "GraspFoM은 3D foundation prior를 reconstruction-driven grasping으로 연결하고, geometry-aware fisheye-LiDAR fusion은 "
                "low-overlap setup에서 perception robustness를 묻습니다. G2G pose estimation, IR-SIM, visual-inertial odometry까지 묶으면 "
                "3D 표현을 보기 좋은 재구성으로 끝내지 말고 grasp pose stability, sensor overlap failure, navigation benchmark로 읽어야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "grasping, LiDAR-camera fusion, pose, VIO, simulator가 모두 downstream utility를 요구",
            "lab_action": "3D method를 PSNR/Chamfer와 분리해 grasp success, low-overlap detection, pose drift, navigation latency로 재평가합니다.",
            "limit": 5,
        },
        {
            "title": "Driving은 reward, uncertainty, evidence grounding으로 닫힌 루프를 요구",
            "buckets": ["Autonomous Driving"],
            "ids": ["2606.08525", "2606.08680", "2606.08860", "2606.09350", "2606.08470", "2606.09542", "2606.09109"],
            "needles": [
                "autonomous driving",
                "reward",
                "uncertainty",
                "lidar",
                "camera",
                "work zone",
                "speed regulation",
                "accident",
                "retrieval",
                "grounding",
            ],
            "why": (
                "DriveReward와 work-zone intelligence는 driving VLM을 reward와 safety-critical regulation 쪽으로 끌고 갑니다. "
                "Distortion-aware PETR, perception jitter, LUNA-AD, accident anticipation, driving video retrieval은 sensor distortion, uncertainty, "
                "lifelong update, evidence grounding을 같이 보지 않으면 closed-loop 주행 품질을 설명하기 어렵다는 방향입니다."
            ),
            "confidence": "High",
            "confidence_note": "dataset/reward, uncertainty-aware perception, safety regulation, accident anticipation이 함께 등장",
            "lab_action": "driving benchmark에 reward provenance, uncertainty trigger, retrieval grounding, accident horizon, sensor distortion split을 추가합니다.",
            "limit": 5,
        },
        {
            "title": "Video world model은 memory와 controllability를 분리해서 봐야 함",
            "buckets": ["Generation", "Foundation Models"],
            "ids": ["2606.09803", "2606.09828", "2606.08091", "2606.08415", "2606.07687", "2606.09507", "2606.07636"],
            "needles": [
                "video world model",
                "memory",
                "agentic",
                "long video",
                "editing",
                "action-relevant",
                "camera-controllable",
                "multi-agent",
            ],
            "why": (
                "Echo-Memory와 Latent Spatial Memory는 video world model의 memory를 직접 실험 대상으로 만들고, "
                "VideoWeaver, CoVEBench, Crayotter는 긴 비디오 생성과 편집에서 instruction complexity와 workflow traceability를 묻습니다. "
                "Prisma-World와 action-relevant latent 논문은 생성 품질보다 controllable state와 action consequence를 따로 재야 한다는 쪽입니다."
            ),
            "confidence": "High",
            "confidence_note": "memory, controllability, video editing benchmark, action-relevant latent가 같은 날 강하게 겹침",
            "lab_action": "video/world-model 평가는 temporal memory retention, camera control, edit instruction depth, action consequence prediction으로 나눕니다.",
            "limit": 5,
        },
        {
            "title": "Efficiency와 reliability는 token, memory, robustness budget으로 합쳐짐",
            "buckets": ["Efficiency/Systems", "Safety/Alignment", "Foundation Models"],
            "ids": ["2606.08302", "2606.08156", "2606.07647", "2606.08063", "2606.08745", "2606.09746", "2606.07577", "2606.08708"],
            "needles": [
                "token",
                "compression",
                "pruning",
                "memory compression",
                "hallucination",
                "robust",
                "uncertainty",
                "adversarial",
                "verification",
                "policy optimization",
            ],
            "why": (
                "HACK++, RAPID, OmniMem은 token/cache/memory를 줄이는 방법을 내고, Steer Where It Matters와 PRPO는 중요한 visual token에 "
                "policy signal을 더 주려 합니다. Robust-U1, adversarial purification, hybrid robustness verification은 줄인 계산이 실제 배포에서 "
                "hallucination, corruption, spatio-temporal failure를 악화시키지 않는지 확인해야 한다는 반대편 축입니다."
            ),
            "confidence": "Medium",
            "confidence_note": "효율화와 신뢰성 논문은 application은 다르지만 token/memory budget과 failure robustness로 연결됨",
            "lab_action": "compression curve에 accuracy만 넣지 말고 hallucination rate, corruption recovery, verification pass rate, latency를 같이 올립니다.",
            "limit": 5,
        },
    ],
    "research_topics": [
        {
            "title": "Action-interface bakeoff for VLA/WAM",
            "claim": "latent action, geometry-aware action, temporal memory, state-fusion decoding을 같은 manipulation benchmark에서 비교합니다.",
        },
        {
            "title": "Geometry utility benchmark",
            "claim": "3D reconstruction 계열을 grasping, low-overlap LiDAR-camera detection, VIO drift, navigation success로 재점수화합니다.",
        },
        {
            "title": "Reliability-aware token budget",
            "claim": "token pruning과 KV compression을 hallucination, corrupted input recovery, robustness verification까지 포함한 Pareto curve로 봅니다.",
        },
    ],
}


if __name__ == "__main__":
    build(PROFILE, "out/cv_new.json", "out/ro_new.json")
