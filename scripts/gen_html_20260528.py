#!/usr/bin/env python3
"""Generate the 2026-05-28 arXiv daily briefing artifacts from /new parser outputs."""
from __future__ import annotations

from daily_backfill_lib import build, week_start


DATE = "2026-05-28"

PROFILE = {
    "date": DATE,
    "weekday": "목",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Daily /new parser output",
    "benchmark_note": "Daily artifact generated from arXiv /new parser output with abstracts available.",
    "thesis": (
        "28일 /new는 robot policy와 world model이 실제 배포 조건 쪽으로 더 가까워진 날입니다. "
        "VLA attack, VLA quantization, factory-floor deployment, robot-policy-from-video, What-If World, Con-DSO가 같이 나오면서, 이제는 성능표보다 안전한 입력, 지연시간, pose consistency, closed-loop simulator를 함께 봐야 합니다."
    ),
    "trend_note": (
        "ROI 선별 비율이 높고 Robot Learning, Generation, Foundation Models, Safety/Alignment가 동시에 큽니다. "
        "특히 3D/Scene도 15편이라 geometry/SLAM/reconstruction을 상단 클러스터로 올렸고, VLA와 world model은 실제 robot deployment failure와 직접 연결됩니다."
    ),
    "cluster_specs": [
        {
            "title": "VLA가 배포와 공격, quantization 문제로 내려옴",
            "buckets": ["Robot Learning", "Safety/Alignment", "Efficiency/Systems"],
            "ids": ["2605.28083", "2605.28803", "2605.27461", "2605.27817"],
            "needles": ["vla", "vision-language-action", "hijack", "quantization", "factory-floor", "robot policies", "deployment"],
            "why": (
                "28일 VLA 논문들은 모델을 더 크게 만드는 이야기보다 실제 현장에서 어디가 깨지는지를 더 많이 보여줍니다. "
                "VLA-Hijack은 visual proprioception patch가 action을 흔들 수 있음을 보이고, Ω-QVLA는 per-step scaling으로 quantized VLA를 버티게 하려 합니다. "
                "factory-floor deployment case와 video model을 robot policy로 바꾸는 논문까지 묶으면, 이제 VLA 평가는 success rate와 함께 attack surface, latency, failure workflow를 같이 기록해야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "VLA attack, quantization, deployment, video-policy 논문 4편 직접 연결",
            "lab_action": "OpenVLA 계열에서 patch attack, W4A quantization, factory task latency, recovery workflow를 같은 benchmark sheet에 기록",
        },
        {
            "title": "World model은 what-if causal benchmark와 closed-loop robot simulator로 이동",
            "buckets": ["Generation", "Robot Learning", "Autonomous Driving"],
            "ids": ["2605.27589", "2605.27491", "2605.27884", "2605.27697"],
            "needles": ["world model", "closed-loop", "simulator", "traffic movie", "diffusion", "motion planning", "embodied scenarios"],
            "why": (
                "What-If World는 world model이 단순히 미래 영상을 그럴듯하게 만드는지보다, 조건을 바꿨을 때 causal behavior가 맞는지를 묻습니다. "
                "GE-Sim 2.0은 manipulation용 closed-loop video simulator를 제시하고, traffic movie prediction과 multi-robot diffusion planning은 world model을 control stack 안으로 끌어옵니다. "
                "따라서 28일의 world model은 샘플 품질보다 counterfactual consistency, closed-loop action success, downstream planning utility가 핵심입니다."
            ),
            "confidence": "High",
            "confidence_note": "causal benchmark, robot simulator, traffic prediction, motion planning 논문 연결",
            "lab_action": "What-if intervention, closed-loop rollout success, planner collision rate를 world-model evaluation grid로 묶기",
        },
        {
            "title": "Geometry/SLAM은 direct odometry와 pose-depth scale consistency로 다시 등장",
            "buckets": ["3D/Scene", "Embodied AI", "Autonomous Driving"],
            "ids": ["2605.27952", "2605.28477", "2605.28125", "2605.28237"],
            "needles": ["odometry", "pose-depth", "3d reconstruction", "navigation", "nerf", "final-meters", "pose"],
            "why": (
                "Con-DSO는 RGB-D direct sparse odometry에 short-horizon consistency prior를 넣고, SA4Depth는 monocular depth에서 pose-depth scale alignment를 다룹니다. "
                "CLEAR-NeRF의 unbounded scene reconstruction과 POINav의 real-world final-meters navigation까지 같이 보면, 28일 geometry 흐름은 rendering보다 pose consistency와 navigation endpoint reliability에 가깝습니다. "
                "즉 SLAM이라는 단어가 적어도, map과 pose가 downstream robot behavior를 얼마나 안정시키는지가 다시 핵심 질문으로 올라왔습니다."
            ),
            "confidence": "High",
            "confidence_note": "odometry, pose-depth scale, reconstruction, final-meter navigation 논문 4편 연결",
            "lab_action": "Con-DSO, monocular depth, NeRF recon, POINav를 pose drift, scale error, final-meter arrival success로 비교",
        },
        {
            "title": "Embodied navigation은 language-action translation과 deployment safety를 같이 봄",
            "buckets": ["Embodied AI", "Robot Learning", "Safety/Alignment"],
            "ids": ["2605.27582", "2605.28097", "2605.28110", "2605.28330"],
            "needles": ["embodied navigation", "language-vision-robot", "deploy", "safety-critical", "mobile robot", "chance-constrained"],
            "why": (
                "Uni-LaViRA는 language, vision, robot action 사이 번역을 navigation 문제로 묶고, ICAN-Deploy는 safety-critical embodied agent 배포를 다룹니다. "
                "STR Robot과 chance-constrained MPPI까지 보면, navigation은 더 이상 instruction following만이 아니라 실제 platform identity, deployment canary, collision uncertainty까지 포함합니다. "
                "그래서 benchmark도 route success와 함께 deployment rollback, dynamic-object prediction, state uncertainty를 기록해야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "navigation, deployment safety, mobile robot, uncertainty planning 논문 연결",
            "lab_action": "VLN/ObjectNav run에 canary deployment flag, collision prediction uncertainty, rollback trigger를 추가",
        },
        {
            "title": "Multimodal safety는 hallucination, jailbreak, perturbation을 한 평가판에 올려야 함",
            "buckets": ["Foundation Models", "Safety/Alignment", "Robot Learning"],
            "ids": ["2605.27595", "2605.27932", "2605.27927", "2605.28459"],
            "needles": ["hallucination", "jailbreak", "safety", "visual perturbation", "multimodal", "manipulation detection"],
            "why": (
                "agricultural MLLM hallucination, think-with-image jailbreak robustness, structure-guided perturbation neutralization이 같은 날 나왔습니다. "
                "REVEAL 같은 manipulation detection까지 함께 보면, multimodal reliability는 틀린 답을 줄이는 문제만이 아니라 어떤 visual perturbation과 safety prompt가 실패를 만드는지 찾는 문제입니다. "
                "랩에서는 answer accuracy보다 hallucination type, jailbreak condition, visual attack region을 함께 남기는 평가판이 필요합니다."
            ),
            "confidence": "High",
            "confidence_note": "hallucination, jailbreak, perturbation, manipulation detection 논문 연결",
            "lab_action": "VLM/VLA safety eval에 visual patch, safety prompt, hallucination label, manipulation evidence region을 같이 저장",
        },
        {
            "title": "Generation은 controllable creation과 fairness, interpretability까지 넓어짐",
            "buckets": ["Generation", "Foundation Models", "Efficiency/Systems", "Safety/Alignment"],
            "ids": ["2605.28091", "2605.27891", "2605.28036", "2605.27813"],
            "needles": ["text-to-image evaluation", "video generation", "fairness", "diffusion models", "sparse autoencoders", "interpreting diffusion"],
            "why": (
                "Qwen-Image-Bench는 text-to-image를 단순 생성에서 creation 평가로 넓히고, SmartDirector는 narrative pacing을 조건으로 video generation을 제어하려 합니다. "
                "fairness across guidance scales와 diffusion interpretability 논문까지 보면, 28일 generation 흐름은 '잘 그린다'보다 무엇을 조종할 수 있고 어떤 bias와 내부 feature가 따라오는지를 보는 쪽입니다. "
                "생성 모델 평가도 prompt fidelity, narrative control, fairness drift, latent feature interpretability를 함께 봐야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "generation benchmark, controllable video, fairness, diffusion interpretation 논문 연결",
            "lab_action": "image/video generation 비교에서 prompt fidelity, pacing control, group fairness, latent SAE feature stability를 한 표로 정리",
        },
    ],
    "research_topics": [
        {
            "title": "VLA deployment safety matrix",
            "claim": "VLA-Hijack, Ω-QVLA, factory-floor VLA, video-to-policy 논문을 attack, quantization, latency, recovery workflow 축으로 비교합니다.",
        },
        {
            "title": "Closed-loop world-model evaluation",
            "claim": "What-If World와 GE-Sim 2.0을 counterfactual consistency, robot action success, simulator drift로 같이 평가합니다.",
        },
        {
            "title": "Pose-consistent navigation stress test",
            "claim": "Con-DSO, SA4Depth, CLEAR-NeRF, POINav를 pose drift, scale alignment, final-meter arrival success로 묶어 봅니다.",
        },
    ],
}


if __name__ == "__main__":
    build(PROFILE, "out/cv_new.json", "out/ro_new.json")
