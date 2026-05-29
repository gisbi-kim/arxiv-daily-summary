#!/usr/bin/env python3
"""Generate the 2026-05-29 arXiv daily briefing artifacts from /new parser outputs."""
from __future__ import annotations

from daily_backfill_lib import build, week_start


DATE = "2026-05-29"

PROFILE = {
    "date": DATE,
    "weekday": "금",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Daily /new parser output",
    "benchmark_note": "Daily artifact generated from arXiv /new parser output with abstracts available.",
    "thesis": (
        "29일 /new는 VLA와 video world model이 더 커지는 이야기보다, 실제로 쓰기 전에 내부 상태와 실패 조건을 "
        "어떻게 드러낼지로 중심이 옮겨간 날입니다. VLA는 state aliasing, visual reasoning, 3D spatial grounding, "
        "procedural memory, confidence까지 꺼내 보이기 시작했고, 3D/SLAM 쪽은 active mapping, LiDAR perception, "
        "point-cloud navigation처럼 robot stack에 바로 붙는 geometry evidence가 두꺼워졌습니다."
    ),
    "trend_note": (
        "Robot Learning, Generation, Foundation Models, Efficiency/Systems가 동시에 높고, 3D/Scene도 24편이라 "
        "geometry/SLAM/reconstruction watch lens를 상단에 올려야 하는 배치입니다. 오늘의 핵심은 모델 규모 경쟁보다 "
        "상태 추론, 공간 grounding, runtime budget, hallucination 검증을 같은 배포 체크리스트에 넣는 쪽입니다."
    ),
    "cluster_specs": [
        {
            "title": "VLA가 행동 전 상태, 공간, 확신을 먼저 드러내기 시작",
            "buckets": ["Robot Learning", "Efficiency/Systems", "Safety/Alignment"],
            "ids": ["2605.29577", "2605.30011", "2605.29416", "2605.29562", "2605.29605", "2605.29710"],
            "needles": [
                "vla",
                "vision-language-action",
                "state aliasing",
                "intermediate reasoning",
                "3d spatial",
                "procedural memory",
                "confidence",
            ],
            "why": (
                "오늘 VLA 묶음은 policy가 바로 action을 내는지보다, action 전에 어떤 상태를 구분하고 어떤 중간 표상을 쓰며 "
                "자기 성공 가능성을 얼마나 믿어도 되는지를 묻습니다. State aliasing 완화, VisualThink-VLA, 3DVLA, VLA-Pro, "
                "VLAConf가 같이 나오면서 VLA 평가가 success rate 하나에서 state disambiguation, spatial grounding, memory transfer, "
                "confidence calibration으로 넓어졌습니다. 그래서 실험도 model size 비교보다 같은 task family에서 내부 단서가 "
                "실패 복구와 long-horizon 안정성을 얼마나 바꾸는지 봐야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "state aliasing, visual reasoning, 3D grounding, procedural memory, confidence 논문이 직접 연결",
            "lab_action": "LIBERO/RoboCasa 계열에 state aliasing split, 3D grounding ablation, confidence calibration curve를 같은 sheet로 추가",
        },
        {
            "title": "Geometry/SLAM은 보기 좋은 3D보다 active map과 robot pose로 이동",
            "buckets": ["3D/Scene", "Efficiency/Systems", "Embodied AI"],
            "ids": ["2605.30342", "2605.29997", "2605.30111", "2605.30310", "2605.30320", "2605.29663"],
            "needles": [
                "active mapping",
                "gaussian splatting",
                "reconstruction",
                "lidar",
                "point cloud",
                "navigation",
                "geometry",
            ],
            "why": (
                "3D/Scene이 24편이고, 단순 rendering보다 robot이 쓰는 map과 pose evidence가 눈에 띕니다. Uncertainty-driven 3DGS active "
                "mapping은 어디를 더 봐야 map uncertainty가 줄어드는지를 묻고, FRUC와 City-Mesh3R은 driving/city scale reconstruction을 "
                "feed-forward와 simulation-ready mesh로 당깁니다. xModel-KD는 LiDAR 3D perception, EXACT-MPPI는 point-cloud signed distance "
                "navigation으로 이어지기 때문에, 오늘 geometry cluster는 예쁜 reconstruction이 아니라 localization, mapping, collision checking에 "
                "쓸 수 있는지로 읽어야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "active mapping, LiDAR perception, city reconstruction, point-cloud navigation 논문이 함께 존재",
            "lab_action": "3DGS map 후보를 uncertainty reduction, pose drift, collision-distance query latency, navigation success로 같은 기준에서 비교",
        },
        {
            "title": "Video world model은 생성 품질보다 causal control과 실시간 상호작용으로 압축",
            "buckets": ["Generation", "Autonomous Driving", "Robot Learning"],
            "ids": ["2605.30263", "2605.30346", "2605.30347", "2605.30090", "2605.30083", "2605.29471"],
            "needles": [
                "world model",
                "video generation",
                "causal",
                "real-time",
                "interactive",
                "kv cache",
                "driving scene",
            ],
            "why": (
                "minWM은 real-time interactive video world model을 framework로 내고, YoCausal은 video generation이 world model이라고 부를 만큼 "
                "causal하게 움직이는지를 직접 묻습니다. NeuROK는 object kinematics를 4D generation 쪽으로 연결하고, DirectorBench와 Future Forcing은 "
                "long-form generation과 KV cache policy를 평가 축으로 끌어옵니다. 즉 오늘 world model 흐름은 샘플이 그럴듯한지가 아니라, 사용자가 "
                "개입했을 때 원인과 결과가 유지되고 실시간 제어 loop에 들어갈 수 있는지로 좁혀집니다."
            ),
            "confidence": "High",
            "confidence_note": "interactive world model, causal video, 4D kinematics, long-form evaluation, KV cache 논문이 연결",
            "lab_action": "world-model eval에 intervention consistency, object kinematics error, interactive latency, cache-induced drift를 추가",
        },
        {
            "title": "Runtime은 token pruning에서 video diffusion KV cache까지 한 줄로 이어짐",
            "buckets": ["Efficiency/Systems", "Robot Learning", "Foundation Models", "Generation"],
            "ids": ["2605.29657", "2605.29662", "2605.30010", "2605.30351", "2605.30325", "2605.29505"],
            "needles": [
                "token pruning",
                "kv cache",
                "compression",
                "sparse attention",
                "edge",
                "efficient",
                "low-rank",
            ],
            "why": (
                "OccamToken과 SAFE-Pruner는 VLM/VLA에서 어떤 token을 버려도 되는지를 묻고, EarlyTom은 fast video understanding을 token compression으로 "
                "당깁니다. VideoMLA와 Veda는 minute-scale video diffusion과 distilled sparse attention까지 runtime 문제를 확장합니다. 그래서 오늘 "
                "efficiency cluster는 단순 FPS 개선이 아니라, perception, VLA manipulation, video diffusion에서 같은 budget knob가 accuracy와 safety를 "
                "어떻게 흔드는지 보는 문제입니다."
            ),
            "confidence": "High",
            "confidence_note": "VLM/VLA token pruning, fast video understanding, video diffusion cache/sparse attention 논문이 연결",
            "lab_action": "token budget sweep을 VQA accuracy, VLA manipulation success, video temporal consistency, latency Pareto curve로 동시에 기록",
        },
        {
            "title": "Multimodal reliability는 hallucination을 원인, 장면, 물리 법칙으로 쪼개기 시작",
            "buckets": ["Foundation Models", "Safety/Alignment", "Generation"],
            "ids": ["2605.29579", "2605.29881", "2605.29339", "2605.29615", "2605.30062", "2605.30231"],
            "needles": [
                "hallucination",
                "counterfactual",
                "causal reasoning",
                "visual differences",
                "physical laws",
                "geometric reasoning",
            ],
            "why": (
                "ReactBench는 multimodal hallucination을 cause-driven benchmark로 묶고, barrier-regulated steering은 VLM hallucination을 줄이는 조작 "
                "가능한 steering 문제로 봅니다. DMC-CF는 dynamic multimodal counterfactual QA, DiffSpot은 web interface의 fine-grained difference, "
                "FakeVLM-R1은 physical law CoT를 synthetic image detection으로 연결합니다. 그래서 reliability는 이제 틀렸다는 판정에서 멈추지 않고, "
                "어떤 원인 변화와 어떤 시각 단서가 답을 흔드는지 기록하는 쪽으로 가고 있습니다."
            ),
            "confidence": "High",
            "confidence_note": "hallucination benchmark, counterfactual QA, visual difference, physical-law reasoning 논문이 직접 연결",
            "lab_action": "VLM eval log에 causal factor, scene difference region, physical-rule violation, steering intervention을 함께 저장",
        },
        {
            "title": "Robot manipulation은 bimanual, contact-rich, recovery workflow가 한 묶음으로 등장",
            "buckets": ["Robot Learning", "Embodied AI", "Safety/Alignment"],
            "ids": ["2605.29298", "2605.29407", "2605.29564", "2605.30226", "2605.29378", "2605.29410"],
            "needles": [
                "bimanual",
                "failure recovery",
                "contact-rich",
                "residual adaptation",
                "manipulation",
                "docking",
            ],
            "why": (
                "MonoDuo는 한 팔 데이터로 bimanual policy를 배우고, phase-conditioned imitation learning은 deformable manipulation에서 autonomous failure "
                "recovery를 전면에 둡니다. VE2VF는 vision-enabled policy를 vision-free contact-rich manipulation으로 distill하고, BORA는 offline RL과 online "
                "residual adaptation을 real-world dexterous VLA로 연결합니다. 오늘 manipulation 묶음은 데모를 많이 모으는 문제가 아니라, contact가 바뀌고 "
                "실패가 생겼을 때 policy가 어떤 recovery path를 갖는지 기록해야 한다는 신호입니다."
            ),
            "confidence": "High",
            "confidence_note": "bimanual learning, failure recovery, contact-rich distillation, online residual adaptation 논문이 함께 존재",
            "lab_action": "manipulation benchmark에 phase label, contact sensor summary, recovery trigger, residual adaptation step을 추가",
        },
    ],
    "research_topics": [
        {
            "title": "VLA internal-state evaluation sheet",
            "claim": "state aliasing, visual reasoning, 3D grounding, memory transfer, confidence calibration을 같은 task family에서 ablation합니다.",
        },
        {
            "title": "Active 3DGS map for navigation",
            "claim": "active mapping, LiDAR perception, signed-distance navigation을 pose drift와 collision query latency로 비교합니다.",
        },
        {
            "title": "Causal video world-model stress test",
            "claim": "minWM, YoCausal, NeuROK 계열을 intervention consistency, object kinematics, real-time latency로 평가합니다.",
        },
    ],
}


if __name__ == "__main__":
    build(PROFILE, "out/cv_new.json", "out/ro_new.json")
