#!/usr/bin/env python3
"""Generate the 2026-06-12 arXiv daily briefing artifacts from parser outputs."""
from __future__ import annotations

from daily_backfill_lib import build, week_start


DATE = "2026-06-12"

PROFILE = {
    "date": DATE,
    "weekday": "Fri",
    "week_start": week_start(DATE),
    "source_mode": "pastweek-date-section",
    "source_label": "arXiv cs.CV/pastweek date section + cs.RO/pastweek date section",
    "source_note": "Backfill parser output from arXiv /pastweek date sections",
    "benchmark_note": "Daily artifact corrected from arXiv /pastweek date-section parser output.",
    "thesis": (
        "6/12 묶음은 새 모델 종류 하나가 튀어나온 날이라기보다 실행 인터페이스가 앞으로 나온 날입니다. "
        "world-action model, VLA control, dexterous tool use, visual agent, deployable perception이 모두 "
        "표현이 어떻게 믿을 만한 행동으로 바뀌는지를 묻고 있습니다. APRL 관점에서는 generation, spatial reasoning, "
        "robot learning을 따로 보지 말고, 세계를 예측하고, 근거를 드러내고, 로봇이나 agent가 그 근거로 실제 행동할 수 있는지를 "
        "한 평가 스택으로 묶어보는 게 좋습니다."
    ),
    "trend_note": (
        "Robot Learning과 Generation이 가장 큰 두 축이지만, 둘 다 같은 압박 지점을 가리킵니다. "
        "world-action 논문은 시각 예측을 action transfer 쪽으로 밀고 있고, VLA와 manipulation 논문은 memory, preference, "
        "spatial annotation, attack surface를 붙여 실제 궤적에서 어디가 깨지는지 보려 합니다. Systems 쪽도 커서 오늘 묶음은 "
        "순수 모델 데모보다 실전형에 가깝습니다. on-device fall detection, forest place recognition, distributed tracking, "
        "unified tokenizer가 모두 깨끗한 벤치 밖에서 무엇이 남는지를 묻고 있습니다."
    ),
    "cluster_specs": [
        {
            "title": "World-action model은 video prediction과 control 사이의 인터페이스가 되고 있음",
            "buckets": ["Robot Learning", "Autonomous Driving", "Generation", "Safety/Alignment"],
            "ids": ["2606.13674", "2606.12987", "2606.13376", "2606.13515", "2606.13679"],
            "needles": [
                "world action model",
                "world-action",
                "visual-action tokenizers",
                "av scene prediction",
                "video world modeling",
                "maskwam",
                "interleaved generation",
            ],
            "why": (
                "RepWAM, AV scene prediction용 diffusion-transformer WAM, MoVerse, MaskWAM은 같은 경계에 놓여 있습니다. "
                "video나 world를 예측하는 능력은 그 latent state를 질의하거나, mask로 고치거나, action으로 옮길 수 있을 때 의미가 커집니다. "
                "오늘 신호는 world model이 더 그럴듯한 미래 영상을 만드는 도구를 넘어, control에서 호출할 수 있는 인터페이스 계약으로 바뀌고 있다는 점입니다."
            ),
            "confidence": "High",
            "confidence_note": "WAM/world-model 제목이 robot learning, driving, generation, safety 버킷에 동시에 걸립니다.",
            "lab_action": "같은 표에 forecast 품질, mask/prompt controllability, action-token alignment, downstream policy 성공률을 함께 기록합니다.",
            "limit": 5,
        },
        {
            "title": "VLA 평가는 성공률보다 interaction failure mode로 이동",
            "buckets": ["Robot Learning", "Autonomous Driving"],
            "ids": ["2606.12706", "2606.12475", "2606.12978", "2606.12499", "2606.12603"],
            "needles": [
                "vla",
                "cot-action",
                "collaborative",
                "trajectory-level redirection attacks",
                "action-effect memory",
                "human-preference",
                "long-horizon",
            ],
            "why": (
                "VLADriveBench는 chain-of-thought가 실제 action과 맞는지를 묻고, Learning to Assist는 VLA를 implicit collaboration 쪽으로 옮깁니다. "
                "redirection attack 논문은 실패 표면을 더 노골적으로 보여줍니다. 여기에 action-effect memory와 preference-flow policy가 시간축을 붙이기 때문에, "
                "이제 benchmark는 instruction, memory, attack이 궤적 전체에서 행동을 어떻게 바꾸는지까지 봐야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "같은 날 VLA가 benchmark, collaboration, navigation, memory, attack 논문에 동시에 나타납니다.",
            "lab_action": "각 VLA run마다 language trace, intended action, executed action, intervention point, recovery behavior를 저장합니다.",
            "limit": 5,
        },
        {
            "title": "Dexterous manipulation은 grounded data와 tool-level capability로 이동",
            "buckets": ["Robot Learning", "3D/Scene"],
            "ids": ["2606.13677", "2606.12604", "2606.12728", "2606.12910", "2606.13497"],
            "needles": [
                "dexterous",
                "articulated tools",
                "egocentric human videos",
                "contact-grounded",
                "grasping",
                "spatial annotations",
                "robot demonstrations",
            ],
            "why": (
                "Mana, EgoEngine, EquiDexFlow, language-conditioned grasping, SPARC는 하나의 manipulation stack처럼 읽힙니다. "
                "human video에서 demonstration을 복구하고, contact와 SE(3) 구조를 맞춘 뒤, robot data를 대규모로 annotation하는 흐름입니다. "
                "중요한 부분은 최종 hand policy 하나가 아니라, 어떤 data interface가 tool use를 안정적으로 만들 수 있는가입니다."
            ),
            "confidence": "High",
            "confidence_note": "dexterous, grasping, egocentric demonstration, robot annotation 논문이 직접 연결됩니다.",
            "lab_action": "human-video source, contact label, object articulation, grasp success, annotation noise를 묶는 작은 audit sheet를 만듭니다.",
            "limit": 5,
        },
        {
            "title": "Visual agent는 tool, feedback, spatial self-correction이 필요",
            "buckets": ["Foundation Models", "Robot Learning"],
            "ids": ["2606.12830", "2606.13156", "2606.12886", "2606.12744", "2606.13061"],
            "needles": [
                "tool-augmented visual agents",
                "spatial reasoning",
                "visual feedback",
                "interleaved thinking",
                "prompt retrieval",
                "latent space",
                "multimodal embedding",
            ],
            "why": (
                "foundation-model 쪽 묶음은 더 큰 VLM보다 reasoning loop를 어떻게 제어하느냐에 가깝습니다. "
                "tool-augmented visual agent, iterative visual thinking, stepwise modality transition, prompt retrieval은 모두 perception을 한 번에 끝나는 판정이 아니라 "
                "모델이 더 나은 evidence를 요청하고 고칠 수 있는 상호작용 과정으로 봅니다."
            ),
            "confidence": "High",
            "confidence_note": "여러 Foundation Models 논문이 tool, feedback, modality transition, spatial correction을 직접 다룹니다.",
            "lab_action": "visual agent 평가는 evidence-request count, correction success, spatial error type, final task success를 함께 봅니다.",
            "limit": 5,
        },
        {
            "title": "Generation 논문은 controllability, memory, provenance를 최적화 중",
            "buckets": ["Generation"],
            "ids": ["2606.13035", "2606.13303", "2606.13345", "2606.12977", "2606.13366"],
            "needles": [
                "long-form video generation",
                "gated recall",
                "diffusion image editing",
                "3d scene editing",
                "fingerprinting",
                "diffusion models",
                "rate-distortion-perception",
            ],
            "why": (
                "TetherCache, DuET, JointEdit3D, diffusion fingerprinting, diffusion compression은 같은 성숙 패턴을 보여줍니다. "
                "이제 generation 품질 자체는 어느 정도 전제하고, memory를 얼마나 안정화할지, structure를 어디까지 edit할지, provenance를 어떻게 잡을지, "
                "compression과 perceptual usefulness를 어떻게 맞바꿀지를 묻고 있습니다."
            ),
            "confidence": "High",
            "confidence_note": "상위 generation 제목들이 memory, editing, fingerprinting, operational tradeoff를 강조합니다.",
            "lab_action": "FID만 보지 말고 temporal drift, edit locality, identity/provenance recovery, downstream scene-usefulness를 같이 추적합니다.",
            "limit": 5,
        },
        {
            "title": "Deployment 논문은 perception reliability를 edge와 field 문제로 만듦",
            "buckets": ["Efficiency/Systems", "3D/Scene", "Autonomous Driving"],
            "ids": ["2606.12473", "2606.13206", "2606.13127", "2606.13503", "2606.12981"],
            "needles": [
                "on-device",
                "amd kria",
                "forest",
                "depth-aware distillation",
                "distributed",
                "real-time",
                "long-term place recognition",
                "bev fusion",
            ],
            "why": (
                "오늘은 모델 이야기를 hardware와 field constraint 안으로 밀어 넣는 논문이 많습니다. "
                "AMD SOM 기반 fall prediction, forest visual place recognition, distributed real-time multi-view tracking, "
                "unstructured LiDAR place recognition, cooperative BEV fusion이 모두 그렇습니다. 여기서는 latency, sensor mix, place shift가 부가 지표가 아니라 1차 평가 항목입니다."
            ),
            "confidence": "Medium",
            "confidence_note": "도메인은 다르지만 deployment constraint와 sensor robustness라는 공통점이 있습니다.",
            "lab_action": "perception benchmark report에 hardware budget, sensor modality, location shift, recovery latency를 추가합니다.",
            "limit": 5,
        },
    ],
    "research_topics": [
        {
            "title": "World-action interface benchmark",
            "claim": "같은 robot 또는 driving episode에서 video prediction, masked world-state query, action-token transfer를 비교합니다.",
        },
        {
            "title": "Trajectory-level VLA safety audit",
            "claim": "최종 성공률만 보지 말고 instruction trace, action trace, attack/redirection point, recovery outcome을 궤적 단위로 남깁니다.",
        },
        {
            "title": "Field perception deployment sheet",
            "claim": "각 perception model마다 hardware target, sensor mix, shift condition, latency, failure recovery path를 기록합니다.",
        },
    ],
}


if __name__ == "__main__":
    build(PROFILE, "out/cv_new.json", "out/ro_new.json")
