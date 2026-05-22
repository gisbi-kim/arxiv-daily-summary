#!/usr/bin/env python3
"""Generate the 2026-05-22 arXiv daily briefing artifacts from /new parser outputs."""
from __future__ import annotations

from daily_backfill_lib import build, week_start


DATE = "2026-05-22"

PROFILE = {
    "date": DATE,
    "weekday": "금",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Daily /new parser output",
    "benchmark_note": "Daily artifact generated from arXiv /new parser output with abstracts available.",
    "thesis": (
        "22일 배치는 Foundation Models가 39편으로 가장 크지만, 실제로는 VLM evidence grounding, "
        "VLA runtime verification, Gaussian/4D geometry, world-model memory가 한꺼번에 실험 가능한 형태로 내려온 날입니다. "
        "특히 Pre-VLA, GeoWeaver, WorldKV, no-pose 4D Gaussian류는 모델을 키우기보다 실패를 검증하고 기억과 geometry를 어떻게 유지할지 묻습니다."
    ),
    "trend_note": (
        "수량상 Foundation Models, Generation, Safety/Alignment, Efficiency/Systems가 크고 Embodied AI는 작습니다. "
        "하지만 robot/lab 관점에서는 VLA verification, 3D Gaussian map, driving risk map, video/world memory compression을 따로 보아야 합니다."
    ),
    "cluster_specs": [
        {
            "title": "Geometry는 no-pose 4D Gaussian과 cross-sensor driving map으로 재배치",
            "buckets": ["3D/Scene", "Autonomous Driving", "Foundation Models", "Efficiency/Systems"],
            "ids": ["2605.22020", "2605.22069", "2605.22190", "2605.22420", "2605.22809", "2605.21863"],
            "needles": ["gaussian", "splatting", "4d", "unposed", "urban scene", "sensor2sensor", "odometry", "scene reconstruction", "3d grounded"],
            "why": (
                "ForeSplat, TWINGS, no-pose 4D dynamic Gaussians가 같이 나오면서 3DGS는 더 이상 예쁜 rendering만의 문제가 아닙니다. "
                "Diffusion-guided urban reconstruction, Sensor2Sensor, OCELOT까지 붙으면 scene representation이 driving/robot sensing stack과 직접 연결됩니다. "
                "즉 pose, map, sensor conversion, dynamic 4D state를 같은 geometry substrate로 봐야 하는 날입니다."
            ),
            "confidence": "High",
            "confidence_note": "Gaussian/4D reconstruction, sensor conversion, odometry 신호가 5편 이상 연결",
            "lab_action": "no-pose 4D Gaussian, feed-forward 3DGS, cross-sensor conversion, odometry baseline을 visual localization과 dynamic-scene update cost로 비교",
        },
        {
            "title": "VLA는 post-training보다 runtime verification과 out-of-vision memory가 병목",
            "buckets": ["Robot Learning", "Autonomous Driving", "Safety/Alignment"],
            "ids": ["2605.21854", "2605.22089", "2605.22446", "2605.21862", "2605.22283", "2605.22812"],
            "needles": ["vla", "vision-language-action", "runtime verification", "world-model rollout", "scene beliefs", "spatial memory", "gesture-aware", "latent visual"],
            "why": (
                "CrossVLA와 LVDrive가 VLA post-training/representation을 다루는 사이, Pre-VLA는 runtime verification을 전면에 세웁니다. "
                "EvoScene-VLA와 Spatial Memory for Out-of-Vision Manipulation까지 보면 병목은 action decoder가 현재 보이지 않는 state와 rollout failure를 어떻게 다루느냐입니다. "
                "VLA를 더 크게 만드는 것보다 실행 전 검증, memory, scene belief update가 실험 축으로 올라왔습니다."
            ),
            "confidence": "High",
            "confidence_note": "VLA post-training, runtime verification, spatial memory 논문이 같은 날짜에 등장",
            "lab_action": "LIBERO/RoboCasa에서 VLA policy를 memory-off, runtime-verifier-off, scene-belief-off 조건으로 나눠 long-horizon failure를 비교",
        },
        {
            "title": "VLM reliability는 continuous-thought ablation에서 3D evidence grounding까지 확장",
            "buckets": ["Foundation Models", "Safety/Alignment", "3D/Scene"],
            "ids": ["2605.21625", "2605.21642", "2605.21788", "2605.21796", "2605.22013", "2605.22558", "2605.21973"],
            "needles": ["vlm", "mllm", "spatio-temporal", "continuous thought", "3d visual grounding", "scene graph", "geometric evidence", "evidence-driven", "temporal grounding"],
            "why": (
                "Flat-Pack Bench와 Ablate-to-Validate는 VLM reasoning claim을 직접 뜯어보는 쪽이고, SceneGraphGrounder, MM-Conv, PointLLM-R, GeoWeaver는 3D 구조와 evidence를 붙입니다. "
                "Foresee-to-Ground까지 보면 VLM reliability가 '답이 맞나'에서 '어떤 visual evidence를 근거로 시간/공간 reasoning을 했나'로 이동합니다. "
                "이건 VLM 평가를 text-only reasoning score가 아니라 grounding audit으로 바꾸는 흐름입니다."
            ),
            "confidence": "High",
            "confidence_note": "spatio-temporal benchmark, 3D grounding, evidence-driven reasoning이 동시에 등장",
            "lab_action": "Flat-Pack, 3D dialogue grounding, PointLLM-R, GeoWeaver를 evidence localization score와 final answer score로 분리 평가",
        },
        {
            "title": "World model은 simulation-ready asset과 reproducible memory platform으로 내려옴",
            "buckets": ["Generation", "Robot Learning", "Foundation Models", "Efficiency/Systems"],
            "ids": ["2605.21572", "2605.21800", "2605.22718", "2605.22570", "2605.22344", "2605.22818"],
            "needles": ["world model", "simulation-ready", "physical 3d generation", "world memory", "video generation", "active video synthesis", "latent semantic planning", "motion-controlled"],
            "why": (
                "PhysX-Omni는 simulation-ready physical 3D generation을, stable-worldmodel은 reproducible evaluation platform을, WorldKV는 world memory retrieval/compression을 제시합니다. "
                "VGenST-Bench, Bernini, MotiMotion까지 붙으면 world model은 데모 영상 생성이 아니라 asset, memory, benchmark, planning을 묶는 실험 플랫폼으로 내려옵니다. "
                "후속 실험은 '그럴듯한가'보다 action/world memory가 task success로 이어지는지 봐야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "simulation asset, reproducible platform, world memory, video reasoning benchmark가 연결",
            "lab_action": "stable-worldmodel 위에서 PhysX-Omni asset, WorldKV memory, VGenST active synthesis를 task success와 memory footprint로 비교",
        },
        {
            "title": "Driving은 risk map, latent communication, semantic safety arbitration으로 안전 예산을 쪼갬",
            "buckets": ["Autonomous Driving", "Robot Learning", "Safety/Alignment", "3D/Scene"],
            "ids": ["2605.22018", "2605.22504", "2605.22189", "2605.22456", "2605.22600", "2605.22578"],
            "needles": ["driving", "risk map", "collaborative", "latent communication", "semantic safety", "motion planning", "online mapping", "flooded road", "uncertainty"],
            "why": (
                "FRED처럼 flooded-road dataset이 나오고, LACO는 collaborative driving communication을, unified risk map과 Steins;Gate Drive는 planning 안의 safety arbitration을 다룹니다. "
                "Branch-stochastic MPC와 online mapping metric까지 보면 driving은 perception 점수보다 위험 정보가 communication, map, planner에 어떻게 배분되는지가 핵심입니다. "
                "안전 예산을 하나의 metric으로 뭉개지 말고, risk map과 semantic arbitration, motion uncertainty로 쪼개야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "driving dataset, communication, risk map, planner uncertainty가 연결",
            "lab_action": "flood/low-visibility split에서 collaborative latent communication, risk-map planner, semantic arbitration을 near-miss와 intervention rate로 비교",
        },
        {
            "title": "Efficiency는 diffusion/video를 줄여도 temporal evidence가 남는지 묻는다",
            "buckets": ["Efficiency/Systems", "Generation", "Foundation Models"],
            "ids": ["2605.22015", "2605.22269", "2605.22011", "2605.21573", "2605.21907", "2605.22678"],
            "needles": ["token reduction", "video diffusion", "kv cache", "training efficiency", "sparse", "swift sampling", "temporal", "compression", "acceleration"],
            "why": (
                "ORBIS와 token reduction for diffusion, MuKV, Lens, sparse test-time diffusion, Swift Sampling은 모두 runtime budget을 줄이려는 논문입니다. "
                "근데 오늘의 차이는 그냥 빠르게 만드는 게 아니라 video/diffusion/VLM에서 temporal evidence와 output similarity가 유지되는지를 같이 묻는다는 점입니다. "
                "배포 관점에서는 latency와 memory를 줄이면서 reasoning evidence가 사라지지 않는지를 같은 Pareto curve에 올려야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "video diffusion acceleration, KV compression, token reduction 논문이 반복",
            "lab_action": "video VLM과 diffusion generator에서 token/KV budget, latency, temporal grounding score, output similarity를 같은 Pareto curve로 기록",
        },
    ],
    "research_topics": [
        {
            "title": "VLA runtime verification ablation",
            "claim": "CrossVLA, Pre-VLA, EvoScene-VLA, Spatial Memory VLA를 같은 long-horizon manipulation split에서 verifier, scene belief, memory component별로 끕니다.",
        },
        {
            "title": "Evidence-grounded VLM evaluation",
            "claim": "Flat-Pack Bench, SceneGraphGrounder, PointLLM-R, GeoWeaver를 answer score와 visual evidence localization score로 분리합니다.",
        },
        {
            "title": "World-memory deployment curve",
            "claim": "WorldKV, ORBIS, MuKV, VGenST-Bench를 memory footprint, latency, temporal consistency, action success 기준으로 비교합니다.",
        },
    ],
}


if __name__ == "__main__":
    build(PROFILE, "out/cv_new.json", "out/ro_new.json")
