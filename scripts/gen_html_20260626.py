#!/usr/bin/env python3
"""Generate the 2026-06-26 arXiv daily briefing artifacts from /new parser outputs."""
from __future__ import annotations

from daily_backfill_lib import build, week_start


DATE = "2026-06-26"

PROFILE = {
    "date": DATE,
    "weekday": "Fri",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Daily /new parser output",
    "benchmark_note": "Daily artifact generated from arXiv /new parser output with abstracts available.",
    "thesis": (
        "6/26 batch는 VLA safety, open-data behavior cloning, world-model hallucination, 3D robot perception, "
        "traffic scenario generation, VLM grounding이 모두 '실제 실행 전에 실패를 예측하고 줄일 수 있는가'로 수렴합니다. "
        "APRL 관점에서는 policy scaling보다 diagnostic benchmark, physical feasibility, uncertainty routing, closed-loop scenario가 더 중요한 날입니다."
    ),
    "cluster_takeaway": (
        "오늘의 핵심은 더 큰 robot foundation model이 아니라, safety·world hallucination·3D perception·traffic scenario의 실패를 "
        "실행 평가 안에서 얼마나 일찍 분리해 검증할 것인가다."
    ),
    "trend_note": (
        "cs.CV/cs.RO Friday /new batch는 Robot Learning과 Generation이 특히 큽니다. ForesightSafety-VLA, PhysReflect-VLA, "
        "Hallucination in World Models, OctoSense, traffic scenario diffusion, CRISP/Inattentional Gap이 함께 나오면서 "
        "모델 능력보다 실패 진단과 근거 보존이 상단 주제로 올라왔습니다."
    ),
    "cluster_specs": [
        {
            "title": "VLA 평가가 open-data scaling에서 safety diagnosis와 physical reflection으로 이동",
            "buckets": ["Robot Learning"],
            "ids": ["2606.27079", "2606.27375", "2606.27295", "2606.27146", "2606.27268", "2606.26801", "2606.26443"],
            "needles": [
                "foresightsafety", "behavior cloning", "open data", "vla", "physical feasibility",
                "test-time scaling", "keyframe supervision", "benchmark",
            ],
            "why": (
                "VLA 성능을 더 큰 데이터와 더 높은 success rate로만 보면 실제 안전 실패를 놓칩니다. ForesightSafety-VLA, open-data behavior cloning, "
                "LA4VLA, PhysReflect-VLA, embodied test-time scaling, stage/keyframe supervision, WatchAct는 policy가 무엇을 보지 못했고 "
                "어떤 physical constraint를 어겼는지 실행 전에 진단해야 한다는 신호입니다."
            ),
            "confidence": "High",
            "confidence_note": "VLA safety benchmark, open-data scaling, physical reflection, test-time scaling, behavior-grounded benchmark가 동시에 등장",
            "lab_action": (
                "LIBERO/RoboCasa/real-robot task에서 open-data pretraining, keyframe supervision, physical-feasibility reflection, "
                "test-time scaling을 독립 변수로 두고 unsafe action, failure warning lead time, object-generalization success를 비교한다."
            ),
            "limit": 7,
        },
        {
            "title": "World model 평가가 생성 품질에서 hallucination 예측과 물리 일관성 검증으로 이동",
            "buckets": ["Generation", "Foundation Models"],
            "ids": ["2606.27326", "2606.26217", "2606.27364", "2606.26410", "2606.26916", "2606.27277", "2606.27345"],
            "needles": [
                "hallucination in world models", "world model", "mechanics", "voxel dynamics",
                "physics-awareness", "earth observation", "3d-aware video",
            ],
            "why": (
                "world model을 시각적으로 그럴듯한 미래 생성기로만 보면 planning에서 어떤 환각이 위험한지 알 수 없습니다. "
                "hallucination predictability, Fast LeWorldModel, PhysiFormer, neural voxel dynamics, PhysRAG, EO world model, RayPE는 "
                "세계 모델이 물리 상태와 공간 경로를 얼마나 일관되게 유지하는지 직접 검증해야 한다는 흐름입니다."
            ),
            "confidence": "High",
            "confidence_note": "world-model hallucination, physical simulation, voxel dynamics, physics retrieval, 3D-aware video가 같은 신뢰성 축으로 연결",
            "lab_action": (
                "navigation/planning forecast에서 object permanence, contact consistency, dynamics violation, hallucination warning을 "
                "분리된 failure condition으로 만들고 downstream planning success와 함께 평가한다."
            ),
            "limit": 7,
        },
        {
            "title": "3D robot perception이 reconstruction 결과에서 motion feasibility와 pose reliability 평가로 이동",
            "buckets": ["3D/Scene", "Safety/Alignment"],
            "ids": ["2606.27317", "2606.27071", "2606.27223", "2606.26700", "2606.26616", "2606.26863"],
            "needles": [
                "multimodal robot perception", "geometry-guided", "gaussian splatting",
                "motion feasibility", "inter-robot pose", "rolling shutter relative pose",
            ],
            "why": (
                "3D perception은 reconstruction 결과가 보기 좋은지보다 로봇이 움직일 수 있는 경로와 상대 pose를 안정적으로 줄 수 있는지가 중요합니다. "
                "OctoSense, sparse panorama reconstruction, satellite Gaussian refinement, point-cloud motion feasibility, bearing-only inter-robot pose, "
                "rolling-shutter relative pose는 geometry 표현을 task feasibility와 pose reliability로 평가하라는 신호입니다."
            ),
            "confidence": "High",
            "confidence_note": "multimodal robot perception, reconstruction, Gaussian refinement, point-cloud feasibility, pose estimation 신호가 반복됨",
            "lab_action": (
                "sparse-view reconstruction과 point-cloud feasibility pipeline을 같은 robot navigation scenes에서 비교하고 "
                "pose drift, collision-free path recall, viewpoint robustness, downstream navigation success를 함께 평가한다."
            ),
            "limit": 6,
        },
        {
            "title": "Autonomy benchmark가 trajectory planning에서 closed-loop scenario와 driver-state risk로 확장",
            "buckets": ["Autonomous Driving", "Safety/Alignment"],
            "ids": ["2606.26922", "2606.27123", "2606.26661", "2606.26413", "2606.26858", "2606.26533", "2606.26265"],
            "needles": [
                "driver-state world modeling", "traffic scenario generation", "trajectory prediction",
                "reachability guarantees", "driving experts", "openscenario", "human-aware navigation",
            ],
            "why": (
                "driving/autonomy 평가는 planner가 평균적으로 좋은 trajectory를 내는지보다 위험 상태를 closed-loop에서 재현할 수 있는지가 중요합니다. "
                "driver-state world modeling, latent traffic scenario diffusion, lane-aligned motion primitives, reachability planning, PlanRL, OSC2Runner, "
                "crowd navigation benchmark는 위험 조건을 만들고 회복 행동을 검증하는 방향으로 평가를 확장합니다."
            ),
            "confidence": "High",
            "confidence_note": "driver monitoring, scenario generation, planning guarantees, OpenSCENARIO, crowd benchmark가 같은 closed-loop risk 축을 공유",
            "lab_action": (
                "CARLA/OpenSCENARIO와 crowd-navigation suite에서 driver state, scenario diffusion seed, reachability bound, crowd density를 바꾸며 "
                "near-miss, recovery behavior, rule violation, closed-loop success를 비교한다."
            ),
            "limit": 7,
        },
        {
            "title": "VLM grounding이 더 긴 reasoning에서 task-conditioned omission과 uncertainty routing 평가로 이동",
            "buckets": ["Foundation Models", "Safety/Alignment"],
            "ids": ["2606.27128", "2606.27330", "2606.26535", "2606.26287", "2606.26387", "2606.26529"],
            "needles": [
                "vqa", "gui agents", "hallucination", "spatial intelligence", "uncertainty-aware",
                "counterfactual visual alignment", "inattentional gap",
            ],
            "why": (
                "VLM이 더 긴 reasoning을 한다는 주장만으로 실제 task 신뢰성을 설명할 수 없습니다. UAV wildfire VQA, GUI agent exploration, "
                "CRISP spatial intelligence, MoE uncertainty routing, counterfactual alignment, Inattentional Gap은 모델이 볼 수 있는 신호를 "
                "task 조건 때문에 놓치는 실패를 따로 평가해야 한다는 흐름입니다."
            ),
            "confidence": "High",
            "confidence_note": "physical VQA, GUI planning, spatial grounding, uncertainty routing, task-conditioned omission이 reliability 축을 형성",
            "lab_action": (
                "thermal/UAV, GUI, 3D spatial VQA task에서 task prompt, visual saliency, routing entropy, counterfactual alignment를 조작하고 "
                "omitted critical signal과 recovery behavior를 함께 평가한다."
            ),
            "limit": 6,
        },
        {
            "title": "효율화가 cache 재사용에서 mission-critical memory와 bandwidth 보존성 평가로 이동",
            "buckets": ["Efficiency/Systems"],
            "ids": ["2606.26398", "2606.26631", "2606.26762", "2606.26151", "2606.26559", "2606.26778"],
            "needles": [
                "compression", "v2x", "cache reuse", "streaming video", "memory-enhanced",
                "semantic delivery", "feature caching", "bandwidth",
            ],
            "why": (
                "효율화는 빨라졌다는 주장만으로 V2X, rover, streaming video, satellite network 같은 배포 환경을 통과할 수 없습니다. "
                "DinoLink, position rebinding cache reuse, ProtoKV, rover obstacle memory, semantic satellite delivery, diffusion feature caching은 "
                "bandwidth와 memory를 줄인 뒤 task-critical evidence가 남아 있는지 평가해야 한다는 흐름입니다."
            ),
            "confidence": "Medium",
            "confidence_note": "V2X compression, cache reuse, streaming memory, rover perception, satellite delivery가 배포 효율성 축으로 연결됨",
            "lab_action": (
                "V2X/rover/streaming-video benchmark에서 bandwidth, cache budget, delayed query를 단계적으로 제한하고 "
                "obstacle recall, collaborative perception accuracy, semantic delivery success, downstream decision change를 비교한다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "VLA safety diagnosis grid",
            "claim": "open-data VLA와 reflective/test-time scaling VLA를 unsafe action, failure warning, physical feasibility 기준으로 비교한다.",
        },
        {
            "title": "World-model hallucination stress suite",
            "claim": "world model의 object permanence, contact consistency, dynamics violation이 downstream planning을 언제 망가뜨리는지 평가한다.",
        },
        {
            "title": "Task-conditioned VLM omission benchmark",
            "claim": "모델이 평소 볼 수 있는 safety-critical visual signal을 task prompt 조건에서 놓치는지 thermal, GUI, 3D VQA에서 검증한다.",
        },
    ],
}


if __name__ == "__main__":
    build(PROFILE, "out/cv_20260626.json", "out/ro_20260626.json")
