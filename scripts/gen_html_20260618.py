#!/usr/bin/env python3
"""Generate the 2026-06-18 arXiv daily briefing artifacts from /new parser outputs."""
from __future__ import annotations

from daily_backfill_lib import build, week_start


DATE = "2026-06-18"

PROFILE = {
    "date": DATE,
    "weekday": "Thu",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Daily /new parser output",
    "benchmark_note": "Daily artifact generated from arXiv /new parser output with abstracts available.",
    "thesis": (
        "6/18 arXiv의 핵심은 로봇이 한 장면을 보고 바로 행동하는 문제에서, 실패 기억, human egovideo, action-conditioned world model, sensor configuration까지 "
        "학습 루프 전체를 다시 설계하는 쪽으로 무게가 이동했다는 점입니다. 동시에 3D/SLAM과 VLM reliability 쪽에서는 좋은 표현을 만드는 것보다 "
        "그 표현이 domain shift, occlusion, bandwidth, uncertainty 아래서 실제로 유지되는지를 묻는 논문들이 많이 나왔습니다."
    ),
    "trend_note": (
        "Robot Learning은 오늘 31편으로 가장 크고, 단순 policy 학습보다 failure recovery, cross-embodiment video-to-action, memory-augmented world model, "
        "teleoperation correction 같은 실행 구조 논문이 두드러집니다. Foundation/Safety 쪽은 hallucination, counter-evidence, fine-grained diagnosis, "
        "uncertainty가 함께 나오며 VLM을 '답 생성기'가 아니라 evidence-budgeted decision module로 보는 흐름이 강합니다. 3D/Scene은 LiDAR place recognition, "
        "4D Gaussian, point-cloud reconstruction, event underwater SLAM처럼 geometry 표현이 downstream navigation과 reconstruction fidelity로 바로 연결됩니다."
    ),
    "cluster_specs": [
        {
            "title": "VLA가 human egovideo와 실패 로그를 행동 supervision으로 끌어오는 날",
            "buckets": ["Robot Learning"],
            "ids": ["2606.18955", "2606.19333", "2606.18328", "2606.18610", "2606.18363"],
            "needles": [
                "cross-embodiment",
                "human egovideos",
                "robot failures",
                "foundation models",
                "self-consistent video generation",
                "embodied manipulation",
            ],
            "why": (
                "Motion-Focused Latent Action, Do as I Do, Recover-Discover-Plan, SC3-Eval, Guava를 같이 보면 오늘 로봇 학습의 질문은 "
                "'데이터를 더 모은다'가 아니라 인간 비디오, 실패 episode, generated video, universal manipulation harness를 어떤 행동 단위로 바꾸느냐입니다. "
                "policy 자체보다 supervision의 형식과 평가 harness가 연구 포인트로 올라왔습니다."
            ),
            "confidence": "High",
            "confidence_note": "대표 논문들이 모두 action supervision, failure recovery, embodied manipulation 평가 축을 직접 건드립니다.",
            "lab_action": "우리 manipulation task도 성공 demo만 보지 말고 failure-to-recovery transition, human egovideo action token, generated rollout consistency를 같은 로그 schema로 저장해 비교합니다.",
            "limit": 5,
        },
        {
            "title": "World model과 memory가 persistent manipulation의 중간층으로 자리 잡음",
            "buckets": ["Robot Learning", "Generation"],
            "ids": ["2606.18960", "2606.18375", "2606.18825", "2606.18702", "2606.18478"],
            "needles": [
                "memory-augmented",
                "action-conditioned world models",
                "world foundation model",
                "robotic manipulation",
                "belief-driven world model",
                "video generation",
            ],
            "why": (
                "Mem-World와 PAIWorld가 manipulation을 persistent world model 관점에서 보고, DreamReg와 UniTemp/Data-Forcing Distillation은 생성 모델의 "
                "temporal/order control 문제를 다룹니다. 로봇에서 world model은 더 이상 예쁜 rollout 생성기가 아니라 기억, registration, action-conditioned prediction을 "
                "묶는 중간 상태 표현으로 내려오고 있습니다."
            ),
            "confidence": "High",
            "confidence_note": "robot world model과 video generation 논문이 모두 temporal consistency와 action conditioning을 공유합니다.",
            "lab_action": "월드모델 평가를 PSNR류가 아니라 object persistence, action-conditioned state error, recovery planning success, memory overwrite failure로 다시 짭니다.",
            "limit": 5,
        },
        {
            "title": "3D/SLAM은 보기 좋은 reconstruction보다 재사용 가능한 place/map 증거로 이동",
            "buckets": ["3D/Scene", "Efficiency/Systems", "Robot Learning"],
            "ids": ["2606.18583", "2606.19067", "2606.18951", "2606.18948", "2606.19156", "2606.18588"],
            "needles": [
                "LiDAR place recognition",
                "multimodal SLAM",
                "underwater SLAM",
                "LiDAR Sensors",
                "4D Hand Reconstruction",
                "3D Gaussian Splatting",
            ],
            "why": (
                "Aerial-ground LiDAR place recognition, multimodal SLAM sensor configuration, event underwater SLAM, adaptive LiDAR clustering, Hand-4DGS, Splaxel을 묶으면 "
                "오늘 geometry 흐름은 static reconstruction 성능표보다 어떤 sensor setup과 representation이 place recognition, teleoperation, large-scale map reuse로 이어지느냐입니다. "
                "특히 LiDAR/SLAM/3DGS가 서로 다른 이름으로 같은 deployment friction을 다룹니다."
            ),
            "confidence": "High",
            "confidence_note": "LiDAR, SLAM, 4DGS, distributed 3DGS가 모두 downstream 재사용성 문제로 수렴합니다.",
            "lab_action": "map/reconstruction 결과마다 relocalization success, cross-view retrieval, sensor ablation, communication budget, downstream teleop correction gain을 같이 기록합니다.",
            "limit": 6,
        },
        {
            "title": "VLM reliability는 정답률보다 counter-evidence와 fine-grained diagnosis로 이동",
            "buckets": ["Foundation Models", "Safety/Alignment"],
            "ids": ["2606.18609", "2606.19053", "2606.18441", "2606.19300", "2606.18860", "2606.18554"],
            "needles": [
                "hallucination",
                "counter-evidence",
                "fine-grained",
                "visual focus",
                "confidence is not reliability",
                "uncertainty",
                "synthetic disaster detection",
            ],
            "why": (
                "medical VLM hallucination correction, fine-grained VLM diagnosis, visual focus alignment, MC dropout reliability 재검토, adversarial uncertainty, synthetic disaster detection이 "
                "같은 날 나왔습니다. 공통점은 모델 답을 믿을지 말지를 logit confidence 하나로 보지 않고, 반증 증거, task granularity, domain shift, uncertainty calibration을 따로 보는 것입니다."
            ),
            "confidence": "High",
            "confidence_note": "VLM/Vision safety 논문들이 reliability의 하위 축을 여러 방식으로 분해합니다.",
            "lab_action": "VLM을 로봇 perception에 붙일 때 answer, evidence crop, counter-evidence, confidence, abstention, domain-shift flag를 분리 저장하는 평가 row를 만듭니다.",
            "limit": 6,
        },
        {
            "title": "Driving과 V2X는 planner 성능보다 통신, label noise, rough terrain 보정이 병목",
            "buckets": ["Autonomous Driving", "Efficiency/Systems"],
            "ids": ["2606.19258", "2606.19186", "2606.18630", "2606.18516", "2606.18824"],
            "needles": [
                "V2X",
                "bandwidth",
                "AEB",
                "path tracking",
                "motion planning",
                "pedestrian",
            ],
            "why": (
                "CABLE은 V2X에서 LMM encoding의 bandwidth 병목을, AEB annotation 논문은 delayed/false event label noise를, Koopman path tracking은 slope/pothole 보정을, "
                "CBBA+convex set planning은 dynamic cluttered allocation을 다룹니다. 오늘 driving 축은 end-to-end score보다 deploy loop 안의 통신/라벨/지형/할당 오차를 고치는 쪽입니다."
            ),
            "confidence": "Medium",
            "confidence_note": "논문 수는 적지만 병목 유형이 실제 시스템 failure mode와 직접 연결됩니다.",
            "lab_action": "자율주행/UGV 평가표에 bandwidth budget, delayed label, false event cost, terrain compensation, allocation failure를 별도 column으로 추가합니다.",
            "limit": 5,
        },
        {
            "title": "Efficiency는 작은 모델이 아니라 spatial token과 geometry redundancy를 지우는 문제",
            "buckets": ["Efficiency/Systems", "Foundation Models", "3D/Scene"],
            "ids": ["2606.18439", "2606.18681", "2606.18687", "2606.19195", "2606.18974"],
            "needles": [
                "redundancy removal",
                "token pruning",
                "distillation",
                "lightweight",
                "self-distillation",
                "spatial",
            ],
            "why": (
                "RegimeVGGT, visual token pruning, radar place distillation, Moebius, Visual-OPSD는 모두 모델을 작게 만드는 문제가 아니라 어떤 spatial evidence와 token을 남겨야 "
                "geometry/VLM reasoning이 무너지지 않는지를 묻습니다. 3D와 VLM 모두에서 redundancy removal이 deployment quality의 핵심 변수로 올라왔습니다."
            ),
            "confidence": "Medium",
            "confidence_note": "efficiency 논문들이 공통적으로 spatial preservation과 distillation을 강조합니다.",
            "lab_action": "압축 실험은 FLOPs만 쓰지 말고 spatial consistency, place-recognition recall, fine-grained reasoning score, reconstruction drift를 함께 plot합니다.",
            "limit": 5,
        },
    ],
    "research_topics": [
        {
            "title": "Failure-to-action dataset schema",
            "claim": "성공 demo 중심 데이터셋에 실패 원인, recovery skill, human egovideo alignment, generated rollout consistency를 붙여 VLA supervision 단위를 다시 정의합니다.",
        },
        {
            "title": "Reusable map evidence benchmark",
            "claim": "LiDAR place recognition, multimodal SLAM, 4DGS, event SLAM 결과를 같은 relocalization/downstream-control 지표로 묶어 '보기 좋은 map'과 '쓸 수 있는 map'을 분리합니다.",
        },
        {
            "title": "Counter-evidence VLM evaluator for robotics",
            "claim": "로봇 perception VLM이 답을 낼 때 반증 crop, uncertainty, abstention, domain-shift flag를 함께 저장해 action failure와 연결되는 reliability 지표를 만듭니다.",
        },
    ],
}


if __name__ == "__main__":
    build(PROFILE, "out/cv_new.json", "out/ro_new.json")
