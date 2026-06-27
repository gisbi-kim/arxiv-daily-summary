#!/usr/bin/env python3
"""Generate the 2026-06-24 arXiv daily briefing artifacts from /pastweek date-section parser outputs."""
from __future__ import annotations

from daily_backfill_lib import build, week_start


DATE = "2026-06-24"

PROFILE = {
    "date": DATE,
    "weekday": "Wed",
    "week_start": week_start(DATE),
    "source_mode": "pastweek-date-section",
    "source_label": "arXiv cs.CV/pastweek date section + cs.RO/pastweek date section",
    "source_note": "Backfill parser output from the 2026-06-24 /pastweek date sections",
    "benchmark_note": "Backfill artifact generated from arXiv /pastweek date-section parser output; paper-level summaries are title/subject based.",
    "thesis": (
        "6/24 backfill은 3DGS/SLAM, VLA, VLM evidence, navigation world model, autonomous-driving risk가 모두 "
        "실제 시스템에서 어떤 증거가 유지되고 어떤 조건에서 무너지는지 묻는 방향으로 모입니다. APRL 관점에서는 "
        "보기 좋은 생성 결과보다 지도 일관성, 실행 안정성, 물리 제약, 근거 기반 추론을 같은 평가판에 올려야 합니다."
    ),
    "cluster_takeaway": (
        "오늘의 핵심은 더 큰 생성 모델이 아니라, 3D 지도와 VLA가 실제 로봇 실행에 필요한 증거를 "
        "어떤 benchmark 조건에서 유지하는지 분리해 검증할 것인가다."
    ),
    "trend_note": (
        "6/24는 /pastweek date-section backfill이라 abstract가 없는 title/subject 기반 복구입니다. 그래도 "
        "3DGS-SLAM, geometry-guided VLA, VLM hallucination/evidence benchmark, navigation world model, token compression이 "
        "한 날짜 안에서 반복되어 상단 해석 축을 만들 만큼의 신호가 있습니다."
    ),
    "cluster_specs": [
        {
            "title": "3D 표현 평가가 렌더링 품질에서 상호작용 가능한 지도와 일관성 검증으로 이동",
            "buckets": ["3D/Scene"],
            "ids": ["2606.24628", "2606.24489", "2606.24796", "2606.24876", "2606.24829", "2606.24144"],
            "needles": [
                "digital twin", "gaussian splatting", "multi-robot slam", "3dgs-slam",
                "feedforward", "3d consistency", "style transfer",
            ],
            "why": (
                "기존 3D 생성과 reconstruction은 보기 좋은 mesh나 novel view 품질에 머무르기 쉬웠지만, "
                "이 묶음은 RGB-D digital twin, object-based multi-robot SLAM, pruning-aware 3DGS-SLAM, "
                "feedforward splatting, text-to-video 3D consistency를 함께 요구합니다. 즉 3D 표현은 렌더링 결과물이 아니라 "
                "로봇이 움직이며 수정하고 검증할 수 있는 지도 후보인지 봐야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "3DGS, multi-robot SLAM, feedforward geometry, 3D consistency benchmark가 같은 날짜에 반복됨",
            "lab_action": (
                "RGB-D Gaussian twin, object-SLAM map, feedforward splat을 같은 실내 장면에서 비교하고 "
                "localization 성공률, map update cost, viewpoint change 붕괴, manipulation query 성공률을 함께 평가한다."
            ),
            "limit": 6,
        },
        {
            "title": "VLA와 robot policy가 imitation 성공률에서 geometry-aware 실행 진단으로 확장",
            "buckets": ["Robot Learning", "Embodied AI"],
            "ids": ["2606.24472", "2606.24448", "2606.24884", "2606.24552", "2606.24742", "2606.24403"],
            "needles": [
                "vla", "geometry-guided", "synthetic robot videos", "skill acquisition",
                "simulator-in-the-loop", "world value", "imitation", "manipulation modes",
            ],
            "why": (
                "기존 imitation learning은 demonstration을 더 모아 task success를 올리는 방식으로 읽히기 쉬웠습니다. "
                "이번 묶음은 geometric inductive bias, synthetic robot video adaptation, self-guided VLA skill acquisition, "
                "simulator-in-the-loop cloth refinement, world value model을 통해 정책이 어떤 장면 증거와 물리 feedback을 "
                "사용하는지 묻습니다. 따라서 VLA 평가는 성공률 뒤의 geometry evidence와 refinement loop를 분리해야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "VLA, synthetic adaptation, simulator refinement, world-value policy 신호가 모두 robot execution 축을 공유",
            "lab_action": (
                "LIBERO/RoboCasa와 cloth manipulation task에서 geometry bias, synthetic-video pretraining, simulator refinement를 "
                "독립 ablation 축으로 두고 object-generalization, contact failure, rollout recovery를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "VLM 평가는 답변 정확도에서 근거 사용과 물리 세계 교란을 분리하는 쪽으로 이동",
            "buckets": ["Foundation Models", "Safety/Alignment"],
            "ids": ["2606.24115", "2606.24797", "2606.24335", "2606.23892", "2606.24539", "2606.24292"],
            "needles": [
                "hallucination", "verifiable", "grounded temporal evidence", "evidence use",
                "red-teaming", "physical-world", "geometric reasoning", "correcting perception",
            ],
            "why": (
                "VLM 평가는 오래도록 answer accuracy나 hallucination rate로 요약됐지만, 로봇과 의료 장면에서는 어떤 시각 근거를 "
                "사용했는지와 물리 세계 교란에 어떻게 반응하는지가 더 중요합니다. endoscopy hallucination, grounded temporal VQA, "
                "evidence-use probing, physical-world red teaming, point localization reasoning은 같은 답이라도 근거 경로가 다르면 "
                "신뢰성이 달라진다는 신호입니다."
            ),
            "confidence": "High",
            "confidence_note": "hallucination, verifiable VQA, evidence probing, physical-world red teaming이 같은 reliability 축을 형성",
            "lab_action": (
                "VLM 평가를 grounded evidence span, physical perturbation, pointing localization, perception correction 조건으로 나누고 "
                "정답률뿐 아니라 근거 불일치와 confidence 변화가 task decision을 어떻게 바꾸는지 평가한다."
            ),
            "limit": 6,
        },
        {
            "title": "Navigation world model이 예쁜 예측보다 planning에 필요한 counterfactual 제어를 요구",
            "buckets": ["Generation", "Robot Learning"],
            "ids": ["2606.24101", "2606.24208", "2606.24152", "2606.24256", "2606.24548", "2606.24888"],
            "needles": [
                "navigation world model", "physics", "diffusion", "robot control",
                "counterfactual", "world modeling evaluation", "DiffusionBench",
            ],
            "why": (
                "world model은 프레임을 그럴듯하게 만드는 모델로 보이면 로봇 planning에서 쓸 수 있는지 판단하기 어렵습니다. "
                "NavWM, physics-grounded generative policy, counterfactual controllability, world modeling evaluation, causal T2I benchmark, "
                "DiffusionBench는 생성 모델이 action 후보와 반사실 조건을 바꾸었을 때 결과가 일관되게 변하는지를 묻습니다."
            ),
            "confidence": "High",
            "confidence_note": "navigation, robot control, counterfactual control, diffusion evaluation 논문이 같은 planning-usefulness 질문으로 연결됨",
            "lab_action": (
                "navigation/world-model benchmark에서 goal change, obstacle insertion, physics-constraint violation을 stress condition으로 만들고 "
                "predicted scene consistency와 downstream planning success를 함께 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Autonomy 평가는 BEV 인식에서 위험 이해와 지도 융합의 실패 조건으로 이동",
            "buckets": ["Autonomous Driving"],
            "ids": ["2606.24759", "2606.24051", "2606.24784", "2606.24353", "2606.24301", "2606.24203"],
            "needles": [
                "risk understanding", "autonomous driving", "bev", "hd map", "3d-aware",
                "vehicle generation", "intent-sharing", "v2x",
            ],
            "why": (
                "자율주행 평가는 BEV segmentation이나 detection score만으로 실제 위험 이해를 설명하기 어렵습니다. "
                "UniDrive, DriveStack-VLA, AerialFusionMapNet, open-vocabulary BEV segmentation, 3D vehicle generation, V2X intent sharing은 "
                "지도와 언어 grounding이 위험 판단, 협조 기동, 장면 생성에 어떻게 들어가는지 따로 검증해야 한다는 신호입니다."
            ),
            "confidence": "Medium",
            "confidence_note": "driving risk, BEV grounding, HD map fusion, V2X intent sharing 신호가 연결되지만 공통 benchmark는 아직 약함",
            "lab_action": (
                "nuScenes/CARLA 기반 평가에서 aerial map fusion, open-vocabulary BEV constraint, V2X intent availability를 독립 변수로 두고 "
                "risk explanation, near-miss, maneuver coordination 성공률을 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "경량화 연구가 토큰 절감에서 시간 근거와 geometry cue 보존성 평가로 이동",
            "buckets": ["Efficiency/Systems"],
            "ids": ["2606.24286", "2606.24156", "2606.24165", "2606.24330", "2606.24464", "2606.24557"],
            "needles": [
                "token compression", "token reduction", "token pruning", "distillation",
                "dense matching", "geometry-aware", "gradient regulation",
            ],
            "why": (
                "경량화는 latency를 줄였다는 주장만으로 로봇 적용 가능성을 보장하지 못합니다. hour-level audio-video compression, "
                "MLLM token reduction, spectral token pruning, rotation-equivariant dense matching distillation, geometry-aware video segmentation은 "
                "압축 후에도 시간 근거와 geometry cue가 남는지 평가해야 한다는 흐름입니다."
            ),
            "confidence": "Medium",
            "confidence_note": "token compression, pruning, distillation, geometry-aware segmentation이 같은 evidence-preservation 질문으로 묶임",
            "lab_action": (
                "긴 비디오와 dense matching task에서 token budget을 단계적으로 줄이며 temporal retrieval, geometric matching error, "
                "segmentation boundary loss, downstream decision delta를 함께 비교한다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Geometry-usable 3D map evaluation",
            "claim": "3DGS와 object-SLAM 결과를 같은 장면에서 재구성 품질, localization, update cost, robot query success로 분리해 비교한다.",
        },
        {
            "title": "VLA geometry evidence ablation",
            "claim": "synthetic video adaptation과 geometric bias가 contact-rich manipulation 실패를 얼마나 줄이는지 object-generalization split에서 검증한다.",
        },
        {
            "title": "Grounded VLM failure family",
            "claim": "VLM hallucination을 정답률이 아니라 evidence span, physical perturbation, pointing error별 failure family로 나누어 평가한다.",
        },
    ],
}


if __name__ == "__main__":
    build(PROFILE, "out/cv_20260624.json", "out/ro_20260624.json")
