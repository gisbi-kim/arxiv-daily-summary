#!/usr/bin/env python3
"""Generate the 2026-06-11 arXiv daily briefing artifacts from /new parser outputs."""
from __future__ import annotations

from daily_backfill_lib import build, week_start


DATE = "2026-06-11"

PROFILE = {
    "date": DATE,
    "weekday": "Thu",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Daily /new parser output",
    "benchmark_note": "Daily artifact generated from arXiv /new parser output with abstracts available.",
    "thesis": (
        "6/11 /new 배치는 VLA를 더 큰 모델로만 보는 흐름에서 벗어나 action manifold, asynchronous sensing, execution horizon, "
        "world-action prior처럼 실제 제어 루프에 필요한 구조를 묻는 쪽으로 강하게 기울었습니다. 동시에 4D/spatial reasoning과 "
        "3D field perception, long-video/agentic foundation model, drone/vehicle agent orchestration이 같이 올라와서 "
        "APRL 관점에서는 perception-reasoning-control을 한 테이블에서 묶어 볼 만한 날입니다."
    ),
    "trend_note": (
        "Robot Learning이 여전히 가장 크고, Foundation Models와 3D/Scene이 뒤를 받칩니다. "
        "어제의 contact/force 축이 오늘은 tactile feature alignment, blind dexterous grasping, external force estimation, "
        "bimanual benchmark로 더 구체화됐고, VLM 쪽은 4D QA, spatial data-model loop, test-time compute allocation, visual token routing처럼 "
        "비용과 근거를 동시에 묻는 방향입니다."
    ),
    "cluster_specs": [
        {
            "title": "VLA는 semantic prior보다 실행 시간축과 action geometry가 병목",
            "buckets": ["Robot Learning"],
            "ids": ["2606.11221", "2606.12105", "2606.12396", "2606.11408", "2606.12366", "2606.12299", "2606.12403"],
            "needles": [
                "vision-language-action",
                "vla",
                "action manifold",
                "gromov-wasserstein",
                "asynchronous",
                "execution horizon",
                "action expert",
                "steering",
                "world-action priors",
                "geometry-action",
            ],
            "why": (
                "LAST는 vision-language와 action manifold의 geometry alignment를 묻고, DAM-VLA는 시각, 언어, 고주파 센서가 같은 clock으로 움직인다는 "
                "가정 자체를 깹니다. Dynamic Execution Horizon, APT, World Pilot, Learning What to Say to Your VLA까지 합치면 문제는 "
                "어떤 VLM을 붙일지가 아니라 action chunk를 얼마나 실행할지, language가 어떤 행동을 끌어내는지, world-action prior가 control failure를 "
                "얼마나 줄이는지로 이동합니다."
            ),
            "confidence": "High",
            "confidence_note": "VLA, action manifold, asynchronous modality, execution horizon, steering 논문이 같은 Robot Learning 축에 집중",
            "lab_action": "동일 task에서 language paraphrase, sensor update rate, action chunk length, world-prior alignment score, recovery success를 같이 기록합니다.",
            "limit": 5,
        },
        {
            "title": "Tactile/dexterous manipulation은 센서와 morphology gap을 동시에 다룸",
            "buckets": ["Robot Learning"],
            "ids": ["2606.12069", "2606.11372", "2606.11396", "2606.11743", "2606.11767", "2606.11901", "2606.11952", "2606.12406"],
            "needles": [
                "tactile",
                "vision-tactile",
                "piezoresistive",
                "multi-finger",
                "dexterous",
                "blind grasping",
                "bimanual",
                "force",
                "torque",
                "morphology gap",
            ],
            "why": (
                "Tac-DINO와 TacCoRL은 tactile signal을 VLA/representation 안으로 넣고, HiPi와 slip-aware tactile sensor, FACTR 2는 "
                "저가/commodity hardware에서 force sensitivity를 확보하려 합니다. PLUME, Blind Dexterous Grasping, DuoBench는 multi-finger와 "
                "bimanual setup의 불확실성, morphology gap, benchmark 재현성을 한꺼번에 다룹니다."
            ),
            "confidence": "High",
            "confidence_note": "tactile feature, force estimation, blind dexterous grasping, bimanual benchmark가 같은 배치에 출현",
            "lab_action": "dexterous manipulation benchmark에 tactile patch alignment, torque-estimation error, slip onset, morphology transfer, bimanual coordination failure를 추가합니다.",
            "limit": 5,
        },
        {
            "title": "Spatial/4D VLM은 더 오래 생각하는 대신 어디에 compute를 쓸지 물음",
            "buckets": ["Foundation Models"],
            "ids": ["2606.11568", "2606.11719", "2606.11745", "2606.11792", "2606.11913", "2606.12125", "2606.12402", "2606.12412"],
            "needles": [
                "4d perception",
                "spatial reasoning",
                "causal reasoning",
                "hallucinations",
                "long video",
                "test-time compute",
                "visual token",
                "routing",
                "adaptive test-time scaling",
            ],
            "why": (
                "4DP-QA와 Ouroboros-Spatial은 VLM이 world dynamics와 spatial relation을 실제로 추론하는지 묻고, causal supervision과 MultiToP는 "
                "근거 없는 video answer를 줄이는 쪽입니다. DIRECT와 Reroute, Don't Remove는 test-time compute와 visual token을 모두 쓰는 대신 "
                "언제, 어디에 쓸지를 결정해야 한다고 말합니다."
            ),
            "confidence": "High",
            "confidence_note": "4D perception, spatial reasoning, hallucination mitigation, test-time compute allocation이 하나의 평가축으로 연결",
            "lab_action": "VLM planner 평가에서 answer accuracy 옆에 evidence frame, token budget, re-routing decision, intervention success, latency를 같이 둡니다.",
            "limit": 5,
        },
        {
            "title": "3D/field perception은 깨끗한 RGB 밖에서 geometry를 유지해야 함",
            "buckets": ["3D/Scene"],
            "ids": ["2606.11326", "2606.11563", "2606.11507", "2606.11683", "2606.11880", "2606.12189", "2606.11989", "2606.11894"],
            "needles": [
                "thermal geometry",
                "cross-modal benchmarking",
                "robotic perception",
                "natural environments",
                "bev scene mining",
                "spatial reasoning",
                "visual localization",
                "4d reconstruction",
                "rainfall",
                "gaussian splatting",
            ],
            "why": (
                "DarkVGGT는 darkness에서 thermal geometry로, Cross-Modal Benchmarking은 natural environment에서 foundation model 약점을 드러냅니다. "
                "SceneMiner와 simulated rainfall 평가는 driving log와 weather risk를 찾고, SG2Loc/DynaTok/Wild3R는 localization, 4D reconstruction, "
                "unconstrained photo collection처럼 field deployment에 가까운 geometry 문제를 묻습니다."
            ),
            "confidence": "High",
            "confidence_note": "low-light, natural environment, BEV scene mining, 4D point cloud, localization 논문이 field robustness로 묶임",
            "lab_action": "3D perception 실험을 indoor/RGB clean split에서 끝내지 말고 thermal, rain, sparse views, partial point cloud, natural field robot split으로 확장합니다.",
            "limit": 5,
        },
        {
            "title": "Video/generation은 identity보다 검증 가능한 foresight가 핵심",
            "buckets": ["Generation"],
            "ids": ["2606.11751", "2606.11838", "2606.12217", "2606.11805", "2606.11670", "2606.11783", "2606.11969"],
            "needles": [
                "temporal consistency",
                "causal memory",
                "plan-and-verify",
                "spatio-temporal scene graph",
                "world action model",
                "foresight",
                "hand-object interaction",
                "video generation",
                "motion-coherent",
            ],
            "why": (
                "AnchorEdit와 ARGUS는 multi-turn/image-video identity drift를 다루지만, Plan-and-Verify와 Making Foresight Actionable은 reward reasoning과 "
                "world-action model foresight를 실제 action으로 연결할 수 있는지 묻습니다. TextHOI-3D는 language-to-3D hand-object contact까지 가져와 "
                "generation output이 control/planning에 쓸 수 있는 구조인지 확인하게 만듭니다."
            ),
            "confidence": "High",
            "confidence_note": "temporal consistency, reward verification, WAM foresight, 3D HOI generation이 같은 generation 버킷에 공존",
            "lab_action": "video/world-model output을 visual quality가 아니라 scene-graph condition coverage, contact plausibility, action transfer, long-turn drift로 평가합니다.",
            "limit": 5,
        },
        {
            "title": "Autonomous agents는 vehicle, drone, marine, multi-robot scheduling으로 확장",
            "buckets": ["Autonomous Driving", "Efficiency/Systems"],
            "ids": ["2606.12236", "2606.12142", "2606.11687", "2606.11569", "2606.11249", "2606.12070", "2606.12306", "2606.12349"],
            "needles": [
                "autonomous driving systems",
                "aerial agents",
                "drone threat",
                "consistency models",
                "multi-agent",
                "risk-sensitive",
                "multi-robot motion planning",
                "ugv",
                "uav",
                "sea trials",
            ],
            "why": (
                "DrivingAgent와 AerialClaw는 foundation-model agent를 autonomous driving과 aerial robot workflow로 옮기고, DroneShield-AI는 sensor fusion과 "
                "swarm intent까지 포함합니다. ConsistencyPlanner, MASK, Fibration Trees, UGV-conditioned multi-UAV planning은 agentic autonomy가 "
                "LLM prompt 문제가 아니라 scheduling, risk-sensitive communication, multi-robot decomposition 문제라는 점을 보여줍니다."
            ),
            "confidence": "Medium",
            "confidence_note": "도메인은 vehicle/drone/marine으로 넓지만 agent orchestration과 planning decomposition이라는 공통 축이 있음",
            "lab_action": "agentic autonomy benchmark에 planner latency, handoff failure, communication budget, sensor-fusion evidence, multi-robot conflict rate를 추가합니다.",
            "limit": 5,
        },
    ],
    "research_topics": [
        {
            "title": "Asynchronous VLA control table",
            "claim": "VLA를 modality clock, action chunk length, world-action prior, language steering robustness로 쪼개 같은 robot task에서 비교합니다.",
        },
        {
            "title": "Tactile morphology-gap benchmark",
            "claim": "tactile patch alignment, force/torque estimation, blind grasping, dexterous hand morphology transfer를 하나의 contact-rich suite로 묶습니다.",
        },
        {
            "title": "4D/spatial planner compute audit",
            "claim": "VLM planner가 어느 frame/token/state에 test-time compute를 쓰는지 기록하고 success, hallucination, latency와 연결합니다.",
        },
    ],
}


if __name__ == "__main__":
    build(PROFILE, "out/cv_new.json", "out/ro_new.json")
