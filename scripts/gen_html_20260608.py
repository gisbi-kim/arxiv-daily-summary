#!/usr/bin/env python3
"""Generate the 2026-06-08 arXiv daily briefing artifacts from /new parser outputs."""
from __future__ import annotations

from daily_backfill_lib import build, week_start


DATE = "2026-06-08"

PROFILE = {
    "date": DATE,
    "weekday": "Mon",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Daily /new parser output",
    "benchmark_note": "Daily artifact generated from arXiv /new parser output with abstracts available.",
    "thesis": (
        "6/8 /new 배치는 VLA와 world-model을 더 키우는 이야기보다, 실행 가능한 중간 표현을 어디에 둘지의 문제로 읽힙니다. "
        "Action decoder, symbolic state, geometry map, closed-loop simulator, long-context memory, safety diagnostic이 모두 "
        "로봇·주행 시스템의 검증 가능한 인터페이스를 요구합니다."
    ),
    "trend_note": (
        "최근 일주일 키워드는 CV 쪽에서 video, 3D, benchmark, diffusion이 강하고 RO 쪽에서 robot, manipulation, navigation, "
        "VLA, world model이 같이 뜹니다. 오늘 배치는 이 둘을 직접 잇습니다. 시각 모델은 더 긴 video/memory와 3D state를 다루고, "
        "로봇 논문은 그 state를 action token, STRIPS fact, closed-loop planning, safety filter로 내려 보내려 합니다. "
        "APRL 관점에서는 모델 성능보다 state/action interface와 failure attribution을 먼저 고정하는 편이 유리합니다."
    ),
    "cluster_specs": [
        {
            "title": "VLA가 action decoder와 data alignment 문제로 내려옴",
            "buckets": ["Robot Learning"],
            "ids": ["2606.07100", "2606.06904", "2606.07107", "2606.07383", "2606.06761", "2606.07217"],
            "needles": [
                "vision-language-action",
                "vla",
                "latent action",
                "action decoder",
                "action-token",
                "token",
                "coordinate system",
                "meta-learning",
            ],
            "why": (
                "오늘 VLA 논문들은 backbone scaling보다 action side의 병목을 더 직접 건드립니다. "
                "LARA는 인간 비디오와 로봇 action 사이 latent action alignment를 묻고, ActionMap은 single-point action decoder 대신 "
                "voxel action heatmap을 둡니다. Coarse-to-Control은 action-token planning을 넣고, RhinoVLA는 token budget을 줄여 "
                "edge deployment를 겨냥합니다. 즉 '무슨 거대 모델을 쓰나'보다 action representation, data alignment, runtime budget을 "
                "같은 표에서 비교해야 하는 배치입니다."
            ),
            "confidence": "High",
            "confidence_note": "VLA, latent action, voxel heatmap, action-token planning, edge-token budget 논문이 같은 날 직접 등장",
            "lab_action": "동일 manipulation split에서 latent-action transfer, action heatmap entropy, action-token horizon, token-pruned latency를 함께 기록합니다.",
        },
        {
            "title": "World model은 비디오 예측보다 symbolic planning과 action consequence로 재정의됨",
            "buckets": ["Robot Learning", "Embodied AI", "Generation"],
            "ids": ["2606.06832", "2606.07089", "2606.06877", "2606.07304", "2606.06618"],
            "needles": [
                "world models",
                "world action",
                "strips",
                "symbolic",
                "long-horizon",
                "embodied planning",
                "diffusion planning",
                "action-conditioned",
            ],
            "why": (
                "STRIPS-WM은 이미지에서 action-relevant propositional state를 배우고, Dreaming when Necessary는 WAM이 상황별 reasoning mode를 "
                "바꿔야 한다고 봅니다. Neuro-Symbolic planning과 CAPE는 long-horizon 계획에서 중요한 object/action consequence만 남기려 하고, "
                "ChronoForest는 offline trajectory 조각으로 long-range route를 닫힌 루프에서 합성합니다. 여기서 world model은 예쁜 rollout generator가 아니라 "
                "planner가 질의할 수 있는 사실, 효과, 불확실성을 내는 모듈입니다."
            ),
            "confidence": "High",
            "confidence_note": "STRIPS-style state, WAM reasoning, neuro-symbolic pruning, action-conditioned planning이 함께 묶임",
            "lab_action": "world-model 후보를 visual prediction score가 아니라 precondition accuracy, effect prediction, plan repair success, rollout cost로 비교합니다.",
        },
        {
            "title": "Geometry watch: reconstruction이 streaming, grasping, physical simulation의 상태 표현이 됨",
            "buckets": ["3D/Scene", "Robot Learning"],
            "ids": ["2606.06690", "2606.07179", "2606.07288", "2606.06878", "2606.07118", "2606.07233"],
            "needles": [
                "gaussian",
                "splatting",
                "mesh reconstruction",
                "point cloud",
                "6-dof grasp",
                "simulation",
                "lidar",
                "3d multi-pedestrian",
            ],
            "why": (
                "오늘의 Geometry/SLAM/Reconstruction lens는 단순 reconstruction 품질이 아니라 downstream state utility입니다. "
                "RPC-GS는 satellite RPC camera geometry를 native rendering으로 처리하고, EvoGS는 progressive 3DGS streaming 구조를 만듭니다. "
                "ExMesh는 explicit mesh topology adaptation을 다루고, cross-view grasp pose와 QuadVerse는 3D state가 grasping·quadruped simulation으로 "
                "넘어갈 때 필요한 occlusion, visual-physical alignment 문제를 드러냅니다. 3D 표현을 렌더링 품질만으로 고르면 안 되는 날입니다."
            ),
            "confidence": "High",
            "confidence_note": "GS, mesh, grasp pose, sim-to-real alignment, LiDAR tracking이 geometry state 관점에서 연결됨",
            "lab_action": "3D 표현 후보를 PSNR/Chamfer와 별도로 occlusion recovery, grasp-pose stability, sim state error, streaming latency로 평가합니다.",
            "limit": 5,
        },
        {
            "title": "Driving은 closed-loop simulation과 runtime assurance로 검증축이 이동",
            "buckets": ["Autonomous Driving", "Efficiency/Systems"],
            "ids": ["2606.07366", "2606.07338", "2606.07186", "2606.06996", "2606.07464", "2606.07170"],
            "needles": [
                "closed-loop",
                "driving simulation",
                "counterfactual",
                "runtime assurance",
                "autonomous driving",
                "trajectory optimization",
                "token compression",
                "vision-language planning",
            ],
            "why": (
                "Dash2Sim은 wild dashcam video에서 closed-loop driving sim을 만들고, VeriDrive는 vision-language planning supervision을 "
                "counterfactual하게 검증하려 합니다. Causal closed-loop simulation, mission-level runtime assurance, test-time trajectory optimization, "
                "planning-aligned token compression까지 같이 나오면서 driving 논문은 perception benchmark보다 '실행 중 무엇을 보증할 수 있나'로 이동합니다. "
                "긴 context를 넣는 것도 planner가 쓸 token만 남기는 문제로 바뀝니다."
            ),
            "confidence": "High",
            "confidence_note": "closed-loop sim, counterfactual supervision, runtime assurance, planning token compression이 직접 연결됨",
            "lab_action": "driving stack 평가에 scenario provenance, counterfactual validity, assurance trigger, planning-token retention을 한 로그로 남깁니다.",
            "limit": 5,
        },
        {
            "title": "Long-video와 3D VLM은 memory를 검색 가능한 작업 상태로 바꾸려 함",
            "buckets": ["Foundation Models", "Efficiency/Systems"],
            "ids": ["2606.06532", "2606.06891", "2606.07433", "2606.07436", "2606.07512", "2606.06991"],
            "needles": [
                "long-video",
                "structural memory",
                "spatial understanding",
                "geometry priors",
                "remember",
                "hierarchical graph memory",
                "agentic retrieval",
                "streaming video-language",
            ],
            "why": (
                "GOPAgen, Watch-Remember-Reason, MemDreamer는 긴 비디오를 단순 context 확장으로 보지 않고 structural memory, graph memory, retrieval로 나눕니다. "
                "Stream3D-VLM과 Skill-3D는 3D spatial understanding과 scene-aware skill을 연결하고, Don't Pause는 online video-language synchrony를 깨지 않으려 합니다. "
                "멀티모달 모델이 로봇에 들어가려면 memory가 hidden context가 아니라 policy와 planner가 호출할 수 있는 작업 상태여야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "long-video memory, online 3D priors, scene-aware skills, streaming synchrony 논문이 같은 방향으로 정렬됨",
            "lab_action": "비디오/3D VLM 평가에 recall horizon, spatial fact update, retrieval provenance, response-time stall을 별도 metric으로 둡니다.",
            "limit": 5,
        },
        {
            "title": "Reliability는 safe generation, forensic detection, representation editing으로 분해됨",
            "buckets": ["Generation", "Safety/Alignment", "Efficiency/Systems", "Foundation Models"],
            "ids": ["2606.06875", "2606.07311", "2606.07034", "2606.06918", "2606.06938", "2606.07451"],
            "needles": [
                "safe",
                "unsafe",
                "forensic",
                "ai-generated",
                "robustness",
                "adversarial",
                "alignment",
                "sparse autoencoders",
                "faithfulness",
            ],
            "why": (
                "안전/신뢰성 신호는 하나의 safety score로 합치기 어렵습니다. Safe in-context image generation은 unsafe information flow를 막고, "
                "CULTURESCORE는 video generation의 cultural faithfulness를 묻습니다. ForensicConcept와 DRIFT는 AI-generated image detection을 다른 representation으로 보며, "
                "CLIP counterattack과 TEVI는 VLM representation을 test-time 또는 text-conditioned editing으로 조정합니다. 즉 failure를 생성 안전성, 문화적 충실성, "
                "forensic detectability, representation alignment로 분해해야 합니다."
            ),
            "confidence": "Medium",
            "confidence_note": "서로 다른 application이지만 failure attribution과 representation steering이라는 공통 축이 있음",
            "lab_action": "신뢰성 실험 결과를 unsafe-flow, cultural-faithfulness, generator-shift, adversarial robustness, embedding-alignment 항목으로 분리 기록합니다.",
            "limit": 5,
        },
    ],
    "research_topics": [
        {
            "title": "Action-interface ablation for VLA deployment",
            "claim": "latent action, voxel heatmap, action-token planning, token compression을 같은 manipulation benchmark에서 latency와 recovery까지 함께 비교합니다.",
        },
        {
            "title": "Planner-queryable world state benchmark",
            "claim": "world model을 video prediction이 아니라 precondition/effect prediction, symbolic repair, action consequence retrieval로 평가합니다.",
        },
        {
            "title": "Geometry-as-utility evaluation",
            "claim": "3DGS, mesh, point-cloud, cross-view fusion을 downstream grasping, navigation, simulation fidelity, streaming budget 기준으로 재정렬합니다.",
        },
    ],
}


if __name__ == "__main__":
    build(PROFILE, "out/cv_new.json", "out/ro_new.json")
