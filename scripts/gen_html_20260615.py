#!/usr/bin/env python3
"""Generate the 2026-06-15 arXiv daily briefing artifacts from /new parser outputs."""
from __future__ import annotations

from daily_backfill_lib import build, week_start


DATE = "2026-06-15"

PROFILE = {
    "date": DATE,
    "weekday": "Mon",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Daily /new parser output",
    "benchmark_note": "Daily artifact generated from arXiv /new parser output with abstracts available.",
    "thesis": (
        "6/15 /new 묶음은 실행 쪽 압력이 유난히 큽니다. real-time VLA distillation, 4D world-action modeling, "
        "physically grounded manipulation, multi-agent driving simulation, camera-side attack이 서로 다른 이름으로 같은 질문을 던집니다. "
        "APRL 관점에서 중요한 건 더 큰 multimodal model이 아니라, perception이 control loop 안에 들어왔을 때 state, causality, contact, recovery behavior가 "
        "끝까지 유지되는지를 보는 것입니다."
    ),
    "trend_note": (
        "Robot Learning이 가장 큰 버킷이지만 Generation과 Safety/Alignment가 강하게 얽혀 있습니다. "
        "world model은 더 이상 video predictor에 머물지 않고, VLA 논문은 latency와 physics 쪽으로 밀리고 있으며, safety 논문은 "
        "sensor-side와 planner-side failure mode를 구체적으로 보여줍니다. 그래서 오늘은 representation quality, action latency, contact evidence, "
        "adversarial exposure, mission recovery를 한 평가 행렬에 넣기 좋은 날입니다."
    ),
    "cluster_specs": [
        {
            "title": "Real-time VLA는 model capability에서 deployment contract로 이동",
            "buckets": ["Robot Learning"],
            "ids": ["2606.14010", "2606.14153", "2606.13856", "2606.13886"],
            "needles": [
                "real-time vision-language-action",
                "vla backbone",
                "vla fine-tuning",
                "physically-grounded vla",
                "distillation",
                "frozen-backbone",
            ],
            "why": (
                "RT-VLA, frozen-backbone grafting diagnostic, output-level VLA regularization, PhysVLA를 같이 보면 VLA가 단일 leaderboard 문제가 아니라 "
                "deployment contract 문제처럼 보입니다. latency, transferable encoder, fine-tuning stability, physical grounding을 따로 떼어 보지 말고 함께 점검해야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "여러 VLA 논문이 latency, backbone transfer, fine-tuning stability, physical grounding을 직접 겨냥합니다.",
            "lab_action": "모든 VLA baseline에서 latency, backbone choice, fine-tuning seed variance, physical constraint violation, task success를 같이 기록합니다.",
            "limit": 5,
        },
        {
            "title": "World-action model은 structured state interface가 되고 있음",
            "buckets": ["Robot Learning", "Generation", "Autonomous Driving"],
            "ids": ["2606.14048", "2606.13769", "2606.13817", "2606.14058", "2606.13840"],
            "needles": [
                "world action model",
                "4d world action model",
                "interaction-trace world model",
                "world model with object momentum",
                "reactive behavior world model",
                "shared world models",
            ],
            "why": (
                "WAM4D, scalable 3D interaction-trace world model, FlowMo-WM, ReactSim-Bench, multi-agent embodied driving은 같은 이동을 가리킵니다. "
                "world model이 그럴듯한 미래를 렌더링하는 장치에서, control이 질의할 수 있는 state interface로 바뀌고 있습니다."
            ),
            "confidence": "High",
            "confidence_note": "world-model 언어가 robotics, driving, simulation 논문에 동시에 나타납니다.",
            "lab_action": "state persistence, action conditioning, counterfactual query quality, model error 이후 downstream recovery를 같이 평가합니다.",
            "limit": 5,
        },
        {
            "title": "Contact-rich manipulation은 tactile evidence와 geometry evidence를 함께 요구",
            "buckets": ["Robot Learning", "3D/Scene"],
            "ids": ["2606.13877", "2606.14699", "2606.14389", "2606.14237"],
            "needles": [
                "contactworld",
                "vision-tactile",
                "contact-rich manipulation",
                "3d object articulation",
                "kinematic control",
                "object pose estimation",
                "indoor localization",
            ],
            "why": (
                "ContactWorld, Instruct-Particulate, MooMIns, BIM-Loc은 manipulation stack으로 읽기 좋습니다. "
                "contact signal, articulated object geometry, object pose, localization이 모두 실제 상호작용 중 policy가 활용하거나 잃어버릴 수 있는 evidence가 됩니다."
            ),
            "confidence": "Medium",
            "confidence_note": "논문들은 manipulation, articulation, reconstruction, localization으로 흩어져 있지만 evidence grounding 필요가 같습니다.",
            "lab_action": "tactile cue, object articulation state, pose source, localization drift, failure label을 묶는 contact audit sheet를 만듭니다.",
            "limit": 5,
        },
        {
            "title": "Autonomous driving 평가는 causal recovery와 adversarial curriculum으로 이동",
            "buckets": ["Autonomous Driving", "Safety/Alignment"],
            "ids": ["2606.14032", "2606.14438", "2606.14380", "2606.14504", "2606.14658"],
            "needles": [
                "adversarial training for safe autonomous driving",
                "causal auditing",
                "accident anticipation",
                "optical attacks",
                "acoustic adversarial attacks",
                "agentic recovery",
            ],
            "why": (
                "learnability-guided adversarial training, CADET, FLaRA, scratched-lens attack, acoustic attack을 같이 보면 평가는 평균 prediction보다 causal fault isolation에 가까워집니다. "
                "무엇이 바뀌었는지, 누가 감지했는지, planner나 autonomy stack이 어떻게 회복했는지가 핵심입니다."
            ),
            "confidence": "High",
            "confidence_note": "driving과 safety 논문이 attack, causal auditing, anticipation, recovery를 명시적으로 다룹니다.",
            "lab_action": "perturbation source, causal feature shift, planner response, recovery action, residual mission risk를 추적합니다.",
            "limit": 5,
        },
        {
            "title": "Visual reasoning 논문은 final answer보다 evidence chain을 드러냄",
            "buckets": ["Foundation Models", "Embodied AI"],
            "ids": ["2606.13870", "2606.13929", "2606.14702", "2606.14703", "2606.13878"],
            "needles": [
                "fake visual understanding",
                "visual questioner",
                "structured scripts and evidence chains",
                "gaze heads",
                "vision-language guided multi-agent exploration",
                "lifelong navigation",
            ],
            "why": (
                "Mirage Probes, Self-Evolving Visual Questioner, OmniVideo-100K, Gaze Heads, AnyGoal은 같은 진단 표면을 밀고 있습니다. "
                "최종 multimodal answer를 그대로 믿기보다, 모델이 어떤 evidence를 찾고, 어디를 보고, 무엇을 script로 만들고, 무엇을 무시했는지 보자는 흐름입니다."
            ),
            "confidence": "High",
            "confidence_note": "foundation과 embodied 논문에서 probe, question generation, evidence chain, gaze, exploration이 반복됩니다.",
            "lab_action": "VLM/agent test마다 evidence request, gaze 또는 attention target, intermediate script, final answer, correction outcome을 저장합니다.",
            "limit": 5,
        },
        {
            "title": "Efficient vision은 adaptive token과 field deployment engineering으로 이동",
            "buckets": ["Efficiency/Systems", "Generation", "Safety/Alignment"],
            "ids": ["2606.14277", "2606.13898", "2606.14631", "2606.14071", "2606.14081"],
            "needles": [
                "adaptive layer-wise visual token selection",
                "token compression",
                "distillation",
                "wildfire spread prediction",
                "geo-foundational models",
                "lightweight saliency",
            ],
            "why": (
                "adaptive token selection, HiLo-Token, event saliency distillation, wildfire prediction, geo-foundation hybrid는 오늘 묶음의 실용적인 면을 보여줍니다. "
                "efficiency는 단순히 작은 모델이 아니라, deployment constraint 아래에서 어떤 visual evidence를 남길지 고르는 문제입니다."
            ),
            "confidence": "Medium",
            "confidence_note": "token, distillation, field-risk 논문이 deployment-constrained evidence selection으로 연결됩니다.",
            "lab_action": "token budget, retained evidence type, latency, field domain shift, safety-relevant miss case를 함께 보고합니다.",
            "limit": 5,
        },
    ],
    "research_topics": [
        {
            "title": "VLA deployment contract",
            "claim": "VLA 방법을 latency, seed stability, physical grounding violation, task success가 함께 들어간 표로 비교합니다.",
        },
        {
            "title": "World-model state audit",
            "claim": "world-action model이 intervention 이후 object state, contact, recovery-relevant information을 유지하는지 테스트합니다.",
        },
        {
            "title": "Sensor-side failure recovery",
            "claim": "optical/acoustic perturbation을 causal planner auditing과 묶어 detection, attribution, recovery를 측정합니다.",
        },
    ],
}


if __name__ == "__main__":
    build(PROFILE, "out/cv_new.json", "out/ro_new.json")
