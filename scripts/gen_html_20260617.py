#!/usr/bin/env python3
"""Generate the 2026-06-17 arXiv daily briefing artifacts from /new parser outputs."""
from __future__ import annotations

from daily_backfill_lib import build, week_start


DATE = "2026-06-17"

PROFILE = {
    "date": DATE,
    "weekday": "Wed",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Daily /new parser output",
    "benchmark_note": "Daily artifact generated from arXiv /new parser output with abstracts available.",
    "thesis": (
        "6/17 /new에서 제일 뚜렷한 흐름은 더 큰 모델 하나를 내는 것보다, 실행에 쓰이는 증거를 어떻게 만들고 관리할 것인가입니다. "
        "VLA는 human egocentric video, 4D hand-object engine, geometry memory, multimodal sensor call로 행동 인터페이스를 넓히고, "
        "driving과 navigation은 HD map, judge, simulator, active perception을 실제 평가 도구로 묶으려 합니다. "
        "그래서 오늘 묶음은 생성 모델, VLM, 로봇 학습을 따로 보는 것보다, 어떤 증거가 policy와 world model의 다음 행동을 바꾸는지 보는 쪽이 중요합니다."
    ),
    "trend_note": (
        "Robot Learning과 Generation, Foundation Models가 모두 두껍지만 같은 이야기를 반복하지는 않습니다. "
        "로봇 쪽은 웹 비디오와 사람 시점 데이터를 action signal로 바꾸는 문제를 밀고 있고, driving 쪽은 map과 VLM judge를 평가 루프 안으로 넣고 있습니다. "
        "한편 VLM reliability 논문들은 attention, script, logical fault, OOD를 따로 다루지만 공통적으로 '모델이 무엇을 봤다고 믿어도 되는가'를 다시 묻고 있습니다. "
        "3D/Scene도 단순 reconstruction보다 simulation, SLAM, navigation에서 바로 쓸 수 있는 map representation 쪽으로 힘이 실립니다."
    ),
    "cluster_specs": [
        {
            "title": "VLA는 웹 비디오를 행동 데이터로 바꾸는 쪽으로 감",
            "buckets": ["Robot Learning"],
            "ids": ["2606.17200", "2606.17256", "2606.17385", "2606.17598", "2606.17846"],
            "needles": [
                "egocentric human",
                "video-to-action",
                "action-image",
                "multimodal sensing",
                "robotic manipulation foundation",
                "alignment unlocks scale",
            ],
            "why": (
                "ACE-Ego-0, CAIP, EgoInfinity, MuseVLA, Qwen-RobotManip을 같이 보면 VLA의 병목이 policy head 하나가 아니라 행동 supervision을 어디서 얻느냐로 옮겨갑니다. "
                "웹 비디오, hand-object reconstruction, sensor token, heterogeneous manipulation data를 action learning에 붙이려는 시도가 동시에 나오고 있어서, "
                "앞으로는 데이터 출처와 action interface를 분리해서 평가하기 어렵습니다."
            ),
            "confidence": "High",
            "confidence_note": "대표 논문들이 모두 human/robot data alignment와 action supervision을 직접 다룹니다.",
            "lab_action": "같은 manipulation task에서 egocentric pretraining, paired action-image pretraining, sensor-token call, aligned robot data를 하나씩 빼며 success와 recovery를 봅니다.",
            "limit": 5,
        },
        {
            "title": "조작 planning은 memory와 uncertainty gate를 같이 필요로 함",
            "buckets": ["Robot Learning", "Embodied AI"],
            "ids": ["2606.17463", "2606.17480", "2606.17408", "2606.17446", "2606.17309", "2606.17073"],
            "needles": [
                "latent memory",
                "governed memory",
                "source prior",
                "automatic annotation",
                "abstention-aware",
                "robot ontology",
            ],
            "why": (
                "WeaveLA, GeneralVLA-2, LeaP, AnnotateAnything, APOLLO를 묶으면 조작 정책이 점점 '지금 본 장면에서 바로 action을 뽑는 문제'를 넘어서고 있습니다. "
                "subtask 사이에 무엇을 넘길지, memory 품질과 geometry 근거를 어떻게 관리할지, 모르면 언제 LLM assistance나 abstention을 부를지를 정해야 합니다. "
                "즉 manipulation stack의 핵심 변수가 action generator보다 memory hand-off와 uncertainty gate가 되는 모습입니다."
            ),
            "confidence": "High",
            "confidence_note": "memory, source prior, annotation, abstention 논문이 같은 manipulation planning 루프를 보완합니다.",
            "lab_action": "long-horizon task를 subtask event 단위로 쪼개고 memory write, source prior, abstention trigger, 3D asset annotation의 실패 기여도를 따로 기록합니다.",
            "limit": 5,
        },
        {
            "title": "Driving 평가는 perception score보다 실행 가능한 judge와 map을 요구함",
            "buckets": ["Autonomous Driving", "Foundation Models", "3D/Scene", "Embodied AI"],
            "ids": ["2606.17362", "2606.17080", "2606.17082", "2606.17386", "2606.17536", "2606.17630"],
            "needles": [
                "driving evaluation",
                "HD-Map",
                "trajectory planning",
                "end-to-end driving",
                "driving video generation",
                "active perception planning",
            ],
            "why": (
                "DriveJudge, HRDX, ParkingTransformer, TerraTransfer, OmniDrive, FLAP은 driving을 단순 perception benchmark로 닫지 않습니다. "
                "지도는 더 큰 vector HD-map과 aerial alignment를 요구하고, planner는 language/trajectory/history를 함께 쓰며, world model은 multi-view geometry를 latent token에서 맞추려 합니다. "
                "결국 좋은 driving 모델인지 묻는 기준도 rule-grounded judge, map quality, closed-loop rollout, active perception failure를 같이 봐야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "평가 agent, HD map, planning, simulation, active perception 논문이 같은 closed-loop 축에 걸립니다.",
            "lab_action": "driving 실험표에 open-loop score만 두지 말고 rule invocation, map error, collision recovery, unseen FOV risk, simulated-to-real transfer gap을 같이 둡니다.",
            "limit": 5,
        },
        {
            "title": "Geometry는 보기 좋은 3D보다 쓸 수 있는 map으로 이동함",
            "buckets": ["3D/Scene", "Efficiency/Systems", "Autonomous Driving", "Robot Learning"],
            "ids": ["2606.17935", "2606.17520", "2606.17534", "2606.17340", "2606.17722", "2606.18153"],
            "needles": [
                "Gaussian Splatting",
                "embodied-simulation",
                "SLAM",
                "image-guided navigation",
                "pansharpening",
                "tree reconstruction",
            ],
            "why": (
                "MoonSplat, GASE, RICH-SLAM, endoscopic navigation representation, GSPan을 같이 보면 3D/Scene 논문들의 질문이 렌더링 품질에서 deployment map으로 옮겨갑니다. "
                "camera pose drift, radar sparsity, simulator construction, medical navigation correspondence처럼 실제 시스템이 틀어지는 지점을 map representation이 견뎌야 합니다. "
                "그래서 3DGS나 SLAM 결과도 이제는 보기 좋은 mesh가 아니라 planner와 simulator가 다시 사용할 수 있는 증거인지 확인해야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "3DGS, SLAM, navigation representation, simulation reconstruction이 모두 geometry-to-execution 문제를 건드립니다.",
            "lab_action": "map 후보마다 pose drift, relocalization success, simulator rebuild time, downstream navigation score, failure-case visualization을 같은 표에 넣습니다.",
            "limit": 5,
        },
        {
            "title": "VLM reliability는 attention이 아니라 증거 일관성을 물음",
            "buckets": ["Foundation Models", "Safety/Alignment", "Robot Learning"],
            "ids": ["2606.17188", "2606.17389", "2606.17410", "2606.17433", "2606.17539", "2606.17309", "2606.17477", "2606.17540"],
            "needles": [
                "script consistency",
                "spatial attention",
                "attention alignment",
                "logical fault",
                "spatial reasoning",
                "abstention",
                "Out-Of-Distribution",
                "adversarial robustness",
            ],
            "why": (
                "PuMVR, VLM Reliability Probe, human attention alignment, LADBench, SR-REAL, APOLLO, dynamic OOD detection을 같이 보면 믿을 만함은 attention map 하나로 끝나지 않습니다. "
                "같은 이미지를 다른 script로 물었을 때 흔들리는지, 인간 gaze와 맞는지, logical fault를 단계적으로 찾는지, 모를 때 멈추는지를 함께 봐야 합니다. "
                "로봇이나 driving에 VLM을 붙일수록 reliability 평가는 정답률보다 evidence consistency와 abstention behavior로 내려와야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "script, attention, logical reasoning, OOD, abstention 논문이 같은 reliability 평가 문제로 모입니다.",
            "lab_action": "VLM eval row에 answer, visual evidence, script/language variant, abstain flag, OOD shift, human-attention overlap을 함께 저장합니다.",
            "limit": 5,
        },
        {
            "title": "Video와 world model은 생성 품질보다 제어 손잡이를 늘림",
            "buckets": ["Generation", "Efficiency/Systems", "Autonomous Driving", "Safety/Alignment"],
            "ids": ["2606.17257", "2606.17310", "2606.17298", "2606.17742", "2606.17730", "2606.17590", "2606.17675"],
            "needles": [
                "safety alignment",
                "camera-controlled",
                "digital twins",
                "4D fMRI",
                "action-aware memory",
                "video tokenization",
                "fast U-Net",
            ],
            "why": (
                "REINS, SierpinskiCam, OR3, BrainWorld, ActWorld, TivTok을 보면 video/world model 쪽도 '더 그럴듯한 샘플'만 묻지 않습니다. "
                "unsafe generation을 inference-time steering으로 막고, camera path와 action memory를 직접 넣고, long video token을 재사용하며, digital twin으로 retrieval을 reasoning 문제로 바꿉니다. "
                "생성 모델을 로봇이나 수술, driving에 붙이려면 품질 점수보다 어떤 제어 손잡이가 있고 실패를 어디서 멈출 수 있는지가 더 중요해집니다."
            ),
            "confidence": "High",
            "confidence_note": "safety steering, camera control, action memory, token reuse, digital twin retrieval이 같은 controllability 축입니다.",
            "lab_action": "video/world model 평가에 camera deviation, unsafe prompt steering, action-conditioned consistency, token reuse latency, retrieval reasoning success를 같이 넣습니다.",
            "limit": 5,
        },
    ],
    "research_topics": [
        {
            "title": "Egocentric-to-action pretraining audit",
            "claim": "사람 시점 비디오, hand-object 4D engine, robot trajectory, sensor token을 같은 VLA backbone에 넣고 어떤 supervision이 실제 action success를 바꾸는지 비교합니다.",
        },
        {
            "title": "Executable map and driving judge suite",
            "claim": "HD map, 3DGS/SLAM map, rule-grounded VLM judge, active perception planner를 하나의 closed-loop driving benchmark에 묶어 open-loop score와 다른 실패를 찾습니다.",
        },
        {
            "title": "Evidence-budgeted VLM/VLA reliability",
            "claim": "VLM/VLA가 답하기 전에 어떤 crop, memory, script variant, sensor call, abstention trigger를 썼는지 기록해 reliability를 행동 가능한 evidence budget으로 봅니다.",
        },
    ],
}


if __name__ == "__main__":
    build(PROFILE, "out/cv_new.json", "out/ro_new.json")
