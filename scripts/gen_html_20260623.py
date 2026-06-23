#!/usr/bin/env python3
"""Generate the 2026-06-23 arXiv daily briefing artifacts from /new parser outputs."""
from __future__ import annotations

from daily_backfill_lib import build, week_start


DATE = "2026-06-23"

PROFILE = {
    "date": DATE,
    "weekday": "Tue",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Daily /new parser output",
    "benchmark_note": "Daily artifact generated from arXiv /new parser output with abstracts available.",
    "thesis": (
        "6/23 batch는 VLA, 3D world model, long-video memory, driving simulation, calibration/security가 모두 "
        "'실행 전에 어떤 증거를 보존하고, 실행 중 무엇을 의심할 것인가'로 모입니다. APRL 관점에서는 큰 모델보다 "
        "memory budget, geometry uncertainty, failure detector, deployable efficiency를 같은 실험 로그에 묶어야 하는 날입니다."
    ),
    "trend_note": (
        "cs.CV 358건과 cs.RO 174건이 같은 날짜에 쌓인 큰 배치입니다. Robot Learning과 Generation의 볼륨이 크지만, "
        "핵심 신호는 VLA adaptation, video/world memory, physical 3D reconstruction, autonomous-driving scenario replay, "
        "LiDAR/web-agent backdoor와 calibration처럼 실제 배포 실패를 설명하는 축으로 연결됩니다."
    ),
    "cluster_specs": [
        {
            "title": "VLA는 few-shot skill보다 memory, failure, policy length를 같이 봐야 함",
            "buckets": ["Robot Learning", "Embodied AI"],
            "ids": ["2606.20867", "2606.21493", "2606.22540", "2606.20679", "2606.21386", "2606.21496"],
            "needles": [
                "vision-language-action",
                "vla",
                "future-oriented conditioning",
                "semi-supervised",
                "policy efficiency",
                "memoryvam",
                "failure detection",
                "declarative",
                "procedural",
            ],
            "why": (
                "FOCA, Semi-Supervised VLA, PolicyTrim, MemoryVAM, VLA-FAIL, declarative/procedural decoupling은 "
                "VLA를 action decoder 하나로 보지 말라고 말합니다. 적은 demonstration, 긴 manipulation history, "
                "action chunk 길이, failure warning, skill/object generalization이 모두 실제 실행 안정성을 바꾸는 변수입니다."
            ),
            "confidence": "High",
            "confidence_note": "VLA adaptation, memory, failure detection, policy efficiency 논문이 같은 날짜에 직접 등장",
            "lab_action": "VLA 실험 테이블에 demo count, memory horizon, action chunk length, failure score, object-generalization split을 같은 row로 저장합니다.",
            "limit": 6,
        },
        {
            "title": "3D scene은 보기 좋은 mesh보다 물리, 불확실성, robot viewpoint 평가가 중요",
            "buckets": ["3D/Scene", "Autonomous Driving", "Embodied AI"],
            "ids": ["2606.21596", "2606.22856", "2606.22987", "2606.23031", "2606.23046", "2606.22756"],
            "needles": [
                "physically grounded",
                "3d scene reconstruction",
                "sfm",
                "robot camera rotation",
                "drivingvoxels",
                "uncertainty-enhanced collaborative perception",
                "multi-robot slam",
            ],
            "why": (
                "phi-Scene, G-MASt3R-SfM, single-view mesh rotation 평가, DrivingVoxels, UECP, HERCULES를 묶으면 "
                "3D 표현의 질문이 fidelity에서 operational validity로 이동합니다. floating/interpenetration, bad matching, "
                "camera rotation, dynamic driving memory growth, collaborative perception uncertainty가 모두 robot-facing failure입니다."
            ),
            "confidence": "High",
            "confidence_note": "physical validity, SfM pruning, robot camera rotation, driving reconstruction, collaborative uncertainty가 같은 축을 공유",
            "lab_action": "3D/SLAM 실험에는 photometric score와 별도로 physical violation, viewpoint sweep error, uncertainty-weighted fusion, robot-task delta를 기록합니다.",
            "limit": 6,
        },
        {
            "title": "Autonomy 평가는 video를 scenario로 되돌리고 attack surface까지 포함하려 함",
            "buckets": ["Autonomous Driving", "Safety/Alignment", "Generation"],
            "ids": ["2606.20980", "2606.21172", "2606.22617", "2606.21993", "2606.22756", "2606.23606", "2606.20752"],
            "needles": [
                "autonomous driving",
                "video world models",
                "simulatable scenarios",
                "geometry awareness",
                "heterogeneous multi-robot",
                "subsea cable",
                "lidar 3d object detection",
                "backdoor",
            ],
            "why": (
                "Robusto-2, BadDreamer, OmniSpace, D-V2S, HERCULES, subsea cable tracking, LiDAR Mirage는 autonomy 평가가 "
                "정적 perception score를 넘어 geography OOD, world-model poisoning, geometry-aware MLLM, replayable scenario, "
                "heterogeneous robot simulation, degraded prior map, clean-label LiDAR attack까지 포함해야 함을 보여줍니다."
            ),
            "confidence": "High",
            "confidence_note": "driving, multi-robot, underwater autonomy, LiDAR security가 모두 deployment failure surface를 넓힘",
            "lab_action": "자율시스템 benchmark를 OOD geography, replayable scenario seed, geometry cue, prior-map uncertainty, attack trigger exposure로 나눕니다.",
            "limit": 6,
        },
        {
            "title": "Long video와 world generation은 cross-shot memory budget 문제가 됨",
            "buckets": ["Foundation Models", "Generation", "Robot Learning", "Embodied AI"],
            "ids": ["2606.20726", "2606.20774", "2606.20799", "2606.20891", "2606.21661", "2606.23675", "2606.23256"],
            "needles": [
                "memory-budget",
                "long video",
                "camera control",
                "multi-shot",
                "point tracking",
                "memory-driven",
                "interaction generation",
                "procedural video",
            ],
            "why": (
                "long-video memory law, TriMotion, GroundShot, Go-with-the-Track, UnityShots, IMAGIN-4D, P-JEPA는 "
                "video/world generation의 병목이 frame quality만이 아니라 cross-shot entity memory, camera trajectory, "
                "reference-conditioned contact, procedure dependency를 제한된 budget에서 유지하는 문제임을 보여줍니다."
            ),
            "confidence": "High",
            "confidence_note": "memory budget, camera control, entity persistence, HOI contact, procedural dependency가 같은 memory-control 축",
            "lab_action": "world-model 평가에 frame budget, temporal distance, entity drift, camera-control error, contact consistency, procedure-step retrieval을 추가합니다.",
            "limit": 6,
        },
        {
            "title": "Reliability는 calibration 하나가 아니라 OOD, manipulation, prompt injection을 분리해야 함",
            "buckets": ["Safety/Alignment", "Foundation Models", "Robot Learning", "Autonomous Driving"],
            "ids": ["2606.21749", "2606.20752", "2606.20717", "2606.20913", "2606.22339", "2606.21386", "2606.21172"],
            "needles": [
                "confidence calibration",
                "backdoor",
                "visual prompt injection",
                "ood detection",
                "manipulation",
                "failure detection",
                "badDreamer",
            ],
            "why": (
                "Quantile adaptive calibration, LiDAR clean-label backdoor, web-agent visual prompt injection, PROTON OOD, "
                "T-IMPACT manipulation severity, VLA-FAIL, BadDreamer는 reliability를 단일 confidence 숫자로 끝내면 안 된다는 신호입니다. "
                "shift type, adversary capability, manipulated context, runtime failure sign을 분리해 로깅해야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "calibration, OOD, manipulation, web-agent injection, LiDAR/video-world-model attack이 명확히 safety 축을 형성",
            "lab_action": "안전성 평가 row를 confidence quantile, OOD family, manipulation severity, prompt/visual trigger, runtime failure detector output으로 분리합니다.",
            "limit": 6,
        },
        {
            "title": "Efficiency는 edge latency보다 spatial evidence 압축 계약으로 봐야 함",
            "buckets": ["Efficiency/Systems", "3D/Scene", "Autonomous Driving"],
            "ids": ["2606.21244", "2606.21373", "2606.21562", "2606.21947", "2606.22804", "2606.21594"],
            "needles": [
                "compact and efficient",
                "occupancy prediction",
                "observation history",
                "quantization",
                "edge-cloud",
                "texture-poor industrial parts",
                "few-shot instance segmentation",
            ],
            "why": (
                "ACE-GS, FLM-Occ, recurrent memory distillation, ScalePredictor, CoVStream, Boundary-by-Mask는 "
                "deployment efficiency를 단순 latency 절감이 아니라 어떤 geometry, occupancy, observation history, boundary evidence를 "
                "압축 후에도 남기는지의 계약으로 바꿉니다. 로봇 배포에서는 빠른 모델보다 잃은 증거를 추적하는 모델이 더 중요합니다."
            ),
            "confidence": "Medium",
            "confidence_note": "3D compression, occupancy, recurrent memory, quantization, edge-cloud, industrial segmentation이 evidence-preserving compression으로 연결",
            "lab_action": "경량화 실험에는 latency, bandwidth, memory와 함께 retained geometry cue, occupancy false primitive, boundary error, downstream action delta를 plot합니다.",
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "VLA evidence ledger",
            "claim": "VLA 실행 로그를 action, memory token, failure detector, demo scarcity, policy length로 정규화해 성공률 뒤의 failure mode를 분리합니다.",
        },
        {
            "title": "Robot-facing 3D validity suite",
            "claim": "3D scene 결과물을 photometric metric뿐 아니라 physical contact, robot camera rotation, collaborative uncertainty, task delta로 평가합니다.",
        },
        {
            "title": "Scenario-to-security autonomy benchmark",
            "claim": "driving/robot autonomy 평가에서 replayable scenario generation과 backdoor/prompt-injection exposure를 같은 closed-loop stress suite에 넣습니다.",
        },
    ],
}


if __name__ == "__main__":
    build(PROFILE, "out/cv_new.json", "out/ro_new.json")
