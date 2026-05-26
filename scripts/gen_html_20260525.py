#!/usr/bin/env python3
"""Generate the 2026-05-25 arXiv daily briefing artifacts from /pastweek date-section outputs."""
from __future__ import annotations

from daily_backfill_lib import build, week_start


DATE = "2026-05-25"

PROFILE = {
    "date": DATE,
    "weekday": "월",
    "week_start": week_start(DATE),
    "source_mode": "pastweek-date-section",
    "source_label": "arXiv cs.CV/pastweek date section + cs.RO/pastweek date section",
    "source_note": "Daily backfill from arXiv /pastweek date section",
    "benchmark_note": "Daily artifact backfilled from arXiv /pastweek date section; abstracts are unavailable in this source.",
    "thesis": (
        "25일 배치는 video/world generation과 robot execution이 같은 방향으로 붙은 날입니다. "
        "Geo-Align, LaMo, GEM-4D, ChainFlow-VLA가 보여주듯 생성 모델은 보기 좋은 영상보다 metric geometry, physical realism, action planning을 묻고, "
        "3D reconstruction과 navigation benchmark는 이 표현이 실제 long-horizon state를 유지하는지 확인하는 쪽으로 이동했습니다."
    ),
    "trend_note": (
        "수량상 Generation과 Robot Learning이 가장 크고 3D/Scene, Foundation Models가 뒤따릅니다. "
        "주요 신호는 video prior, VLA planning, 4D/3D Gaussian, visual grounding benchmark가 같은 날짜에 겹친다는 점입니다."
    ),
    "cluster_specs": [
        {
            "title": "Video generation은 geometry reward와 physical motion prior로 내려옴",
            "buckets": ["Generation", "Robot Learning", "3D/Scene"],
            "ids": ["2605.23903", "2605.23878", "2605.22882", "2605.23610", "2605.23902"],
            "needles": ["video generation", "metric geometry", "motion priors", "physical realism", "world model", "entity-centric memory", "latent decoding"],
            "why": (
                "Geo-Align과 LaMo는 video generation을 aesthetic score가 아니라 geometry reward와 physical motion prior로 맞추려 합니다. "
                "GEM-4D와 EM-Vid까지 보면 생성 모델의 병목은 한 장면을 잘 만드는 것이 아니라 motion, entity memory, robot manipulation state가 오래 유지되는지입니다. "
                "따라서 video/world model 평가는 temporal drift와 task-conditioned geometry consistency를 같이 봐야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "video generation, geometry reward, robot world-model 제목 신호가 직접 연결",
            "lab_action": "video generation 후보를 temporal drift, geometry consistency, manipulation rollout success 기준으로 나눠 평가",
        },
        {
            "title": "VLA와 imitation learning은 causal flow와 데이터 instrumentation으로 수렴",
            "buckets": ["Robot Learning", "Embodied AI", "Foundation Models"],
            "ids": ["2605.23270", "2605.23847", "2605.23762", "2605.23863", "2605.23263"],
            "needles": ["vla", "causal flow", "imitation learning", "retargeting", "humanoid", "reinforcement learning", "embodied agents"],
            "why": (
                "ChainFlow-VLA는 VLM/VLA planning을 causal flow로 보고, clothes-hanger insertion과 humanoid retargeting 논문은 policy 성능을 데이터 수집 구조와 motion transfer 품질로 끌고 갑니다. "
                "strawberry harvesting처럼 sim-to-real 작업까지 붙으면 로봇 학습의 핵심은 policy head보다 demonstration instrumentation, causal plan structure, domain transfer입니다. "
                "VLA 실험은 task success만 보지 말고 causal step failure와 demonstration coverage를 같이 기록해야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "VLA planning, imitation dataset, humanoid/harvesting sim-to-real 논문이 같은 배치에 존재",
            "lab_action": "long-horizon manipulation에서 causal planner, imitation data instrumentation, retargeting quality를 ablation 축으로 분리",
        },
        {
            "title": "3D/4D reconstruction은 streaming, generative prior, calibration까지 확장",
            "buckets": ["3D/Scene", "Robot Learning", "Autonomous Driving"],
            "ids": ["2605.23889", "2605.23888", "2605.23672", "2605.23602", "2605.23580"],
            "needles": ["3d reconstruction", "4d gaussian", "gaussian splatting", "streaming", "multi-view", "calibration", "lidar", "camera"],
            "why": (
                "HorizonStream, GenRecon, RiGS, GlowGS는 3D/4D scene representation을 streaming, generative prior, semantic feature learning으로 확장합니다. "
                "online LiDAR-camera calibration까지 같이 보면 이 배치의 3D는 rendering 품질보다 실시간 update, sensor calibration, dynamic scene 유지 비용이 중요합니다. "
                "로봇/주행 관점에서는 reconstruction benchmark를 pose availability와 online calibration 조건별로 쪼개야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "streaming reconstruction, 4D Gaussian, calibration 논문이 반복",
            "lab_action": "dynamic-scene split에서 3DGS, streaming reconstruction, online calibration의 latency와 drift를 비교",
        },
        {
            "title": "VLM 평가는 visual search, grounding, hallucination control로 분해",
            "buckets": ["Foundation Models", "Safety/Alignment", "Embodied AI", "Autonomous Driving"],
            "ids": ["2605.23883", "2605.23655", "2605.23629", "2605.23559", "2605.23344", "2605.23176"],
            "needles": ["visual grounding", "multimodal llm", "vlm", "hallucination", "visual search", "diagnostic trajectories", "spatiotemporal intelligence"],
            "why": (
                "PGT와 CVSearch는 VLM이 어디를 보고 답하는지 묻고, DDX-TRACE와 PathNavigate는 medical trajectory에서 scan/memory 구조를 봅니다. "
                "CHASD와 DRIVESPATIAL까지 붙으면 VLM reliability는 final answer 점수보다 search path, grounding evidence, hallucination suppression으로 나뉩니다. "
                "실험 설계는 정답률과 함께 evidence path와 spatiotemporal grounding 실패를 따로 저장해야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "grounding, visual search, hallucination, spatiotemporal benchmark 신호가 연결",
            "lab_action": "VLM evaluation log를 answer, search path, grounding evidence, hallucination flag로 분리 저장",
        },
        {
            "title": "Driving과 motion planning은 geometry fidelity와 formal verification을 요구",
            "buckets": ["Autonomous Driving", "Safety/Alignment", "3D/Scene", "Robot Learning"],
            "ids": ["2605.23327", "2605.23240", "2605.22991", "2605.23203", "2605.23192"],
            "needles": ["lane detection", "motion planning", "formal verification", "homographies", "occlusion-aware", "keyframe", "task-space"],
            "why": (
                "GFSR는 lane detection의 geometric fidelity를, STL motion planning과 verified task-space planning은 planner constraint를 전면에 세웁니다. "
                "homography verification과 occlusion-aware keyframe selection까지 보면 perception과 planning 모두에서 '그럴듯함'보다 증명 가능한 geometry와 constraint satisfaction이 중요합니다. "
                "driving/robot safety 실험은 visual quality와 별도로 formal constraint violation을 기록해야 합니다."
            ),
            "confidence": "Medium",
            "confidence_note": "driving perception, formal planning, verification 논문이 같은 안전 축으로 묶임",
            "lab_action": "lane/planning benchmark에 geometric fidelity, constraint violation, occlusion failure case를 별도 metric으로 추가",
        },
        {
            "title": "Efficiency는 token compression과 dataset distillation로 배포 예산을 줄임",
            "buckets": ["Efficiency/Systems", "Generation", "Foundation Models"],
            "ids": ["2605.23482", "2605.23451", "2605.23245", "2605.23323", "2605.23183"],
            "needles": ["distillation", "token compression", "sparse attention", "image compression", "mixture of experts", "efficient", "one-step diffusion"],
            "why": (
                "dataset distillation, compact token compression, sparse attention, entropy-free image compression이 동시에 나오면서 효율화는 단순 pruning보다 data, token, regional attention budget을 함께 줄이는 방향입니다. "
                "one-step diffusion과 video insertion까지 고려하면 latency를 줄일 때 생성 품질뿐 아니라 regional consistency와 downstream VLM/robot evidence가 유지되는지 봐야 합니다. "
                "배포 곡선은 memory, latency, visual fidelity, task evidence preservation을 함께 놓아야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "distillation, token compression, sparse attention 논문이 다수 등장",
            "lab_action": "compression ratio별로 latency, fidelity, downstream grounding score를 같은 Pareto curve에 기록",
        },
    ],
    "research_topics": [
        {
            "title": "Geometry-aware video world model evaluation",
            "claim": "Geo-Align, LaMo, GEM-4D, EM-Vid를 temporal drift, metric geometry consistency, manipulation rollout success로 비교합니다.",
        },
        {
            "title": "Causal VLA data instrumentation",
            "claim": "ChainFlow-VLA와 imitation-learning datasets를 step-level failure, demonstration coverage, retargeting quality로 ablation합니다.",
        },
        {
            "title": "Evidence-path VLM benchmark",
            "claim": "PGT, CVSearch, DRIVESPATIAL을 answer score와 visual search path, grounding evidence score로 분리 평가합니다.",
        },
    ],
}


if __name__ == "__main__":
    build(PROFILE, "out/cv_new.json", "out/ro_new.json")
