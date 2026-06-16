#!/usr/bin/env python3
"""Generate the 2026-06-16 arXiv daily briefing artifacts from /new parser outputs."""
from __future__ import annotations

from daily_backfill_lib import build, week_start


DATE = "2026-06-16"

PROFILE = {
    "date": DATE,
    "weekday": "Tue",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Daily /new parser output",
    "benchmark_note": "Daily artifact generated from arXiv /new parser output with abstracts available.",
    "thesis": (
        "6/16 /new 묶음은 모델을 크게 만드는 얘기보다, 실행 중 어디에 개입하고 무엇을 남길지를 묻는 쪽이 더 강합니다. "
        "VLA는 action token, latent reasoning, retrieval, tactile feedback으로 잘게 나뉘고, world model은 driving, navigation, manipulation에서 "
        "closed-loop 평가 장치가 되고 있습니다. 그래서 오늘 APRL 관점의 핵심은 representation 하나를 고르는 게 아니라, control loop 안에서 "
        "semantic intent, geometry, contact, compute budget, safety evidence를 어느 지점에 연결할지 보는 것입니다."
    ),
    "trend_note": (
        "Robot Learning이 75편으로 가장 크고 Generation, Foundation Models, Efficiency/Systems도 모두 50편 안팎입니다. "
        "VLA와 world model 논문이 많지만, 같은 이야기를 반복하기보다 action interface, latent future, geometry map, tactile cue, "
        "visual evidence budget을 각각 다른 병목으로 보여줍니다. 특히 3D/Scene 31편 안에는 SLAM, LiDAR calibration, visual odometry, "
        "3DGS compression이 같이 있어서, 보기 좋은 scene representation보다 robot이나 simulator가 실제로 쓸 수 있는 map representation을 "
        "따로 봐야 합니다."
    ),
    "cluster_specs": [
        {
            "title": "VLA는 언어 추론보다 action interface를 줄이는 쪽으로 감",
            "buckets": ["Robot Learning", "Efficiency/Systems"],
            "ids": ["2606.15099", "2606.14752", "2606.15021", "2606.15285", "2606.15631", "2606.17043"],
            "needles": [
                "latent reasoning",
                "early exit",
                "action tokenizer",
                "action token intervention",
                "semantic-action decoupling",
                "retrieve",
                "online rl fine-tuning",
            ],
            "why": (
                "AVA-VLA, X-Tokenizer, Token Steering, asynchronous semantic-action decoupling, retrieval-augmented VLA를 같이 보면 "
                "VLA의 병목은 더 긴 chain-of-thought가 아니라 action으로 넘어가는 좁은 인터페이스입니다. 모델이 무엇을 말했는지보다 "
                "어떤 latent/action token을 언제 멈추고, 바꾸고, 재사용하는지가 실험 변수로 올라오고 있습니다."
            ),
            "confidence": "High",
            "confidence_note": "VLA 논문 여러 편이 action token, latent reasoning, retrieval, low-latency control을 직접 다룹니다.",
            "lab_action": "VLA baseline마다 action-token entropy, early-exit 위치, retrieval hit, semantic-action latency, task success를 같은 log로 남깁니다.",
            "limit": 5,
        },
        {
            "title": "World model은 video generator보다 closed-loop 평가 장치에 가까워짐",
            "buckets": ["Robot Learning", "Generation", "Autonomous Driving", "Safety/Alignment", "Efficiency/Systems"],
            "ids": ["2606.15869", "2606.15341", "2606.16274", "2606.17030", "2606.16533", "2606.15594", "2606.16286"],
            "needles": [
                "world action model",
                "causal world models",
                "long-horizon planning",
                "embodied world modeling",
                "physical ai",
                "latent world model control",
                "flowmpc",
            ],
            "why": (
                "Metis, CausalDrive, GraphWorld, Qwen-RobotWorld, Kairos, Pixels to Proofs를 같이 보면 world model은 예쁜 미래 영상을 만드는 장치에서 "
                "정책을 닫힌 루프에서 시험하고 조정하는 장치로 이동합니다. 중요한 질문도 렌더링 품질 하나가 아니라, future state가 action, safety bound, "
                "navigation query에 얼마나 쓸 수 있는 형태로 남는지입니다."
            ),
            "confidence": "High",
            "confidence_note": "driving, embodied world model, safe MPC, robot policy planning 논문이 같은 closed-loop 사용처를 가리킵니다.",
            "lab_action": "world-model 평가에 rollout realism, action-conditioned state error, planning improvement, constraint violation, recovery success를 같이 넣습니다.",
            "limit": 5,
        },
        {
            "title": "Geometry와 SLAM은 예쁜 map보다 실행 가능한 map으로 압축됨",
            "buckets": ["3D/Scene", "Autonomous Driving", "Generation"],
            "ids": ["2606.16474", "2606.15491", "2606.15010", "2606.15287", "2606.16278", "2606.16232", "2606.16881", "2606.16935"],
            "needles": [
                "visual odometry",
                "slam",
                "lidar-camera",
                "place recognition",
                "3d gaussian splatting driving",
                "polytope coverings",
                "scene graph matching",
                "semantic mapping",
            ],
            "why": (
                "MVOFormer, FD-SLAM, LV-Calib, G2IA, RealityBridge, PolyMerge, SGM-SLAM은 모두 geometry를 downstream execution에 맞게 바꾸는 논문입니다. "
                "오늘 3D/Scene 신호가 큰 이유는 reconstruction 자체보다, map이 localization, collision avoidance, driving simulation, multi-robot SLAM에서 "
                "바로 쓸 수 있는 제약과 confidence를 가져야 한다는 압력이 커졌기 때문입니다."
            ),
            "confidence": "High",
            "confidence_note": "visual odometry, radar-inertial SLAM, LiDAR-camera calibration, 3DGS driving simulation이 모두 같은 geometry-to-control 흐름입니다.",
            "lab_action": "map representation을 pose drift, obstacle over-approximation, semantic confidence, simulator transfer gap, planning latency로 비교합니다.",
            "limit": 5,
        },
        {
            "title": "Contact-rich manipulation은 tactile cue를 steering signal로 끌어들임",
            "buckets": ["Robot Learning", "3D/Scene"],
            "ids": ["2606.14981", "2606.14862", "2606.15133", "2606.15909", "2606.16370", "2606.17055", "2606.15516", "2606.16436"],
            "needles": [
                "vision and touch",
                "tactile robot policies",
                "dexterous hand-object interaction",
                "tactile-language",
                "tactile glove",
                "tactile-reactive",
                "force-position interface",
                "monocular human videos",
            ],
            "why": (
                "ViTaL, TacStyle, DragMesh-2, GeoTLM, ART-Glove, T-Rex를 같이 보면 contact-rich manipulation에서 vision은 충분하지 않습니다. "
                "정책이 실패하는 지점은 대개 손가락이 어디를 보고 있는지가 아니라, 접촉 방향, 힘, 미끄러짐, 사용자 선호가 action 수정 신호로 들어오느냐에 있습니다."
            ),
            "confidence": "High",
            "confidence_note": "tactile policy, tactile-language reasoning, tactile glove, dexterous transfer 논문이 같은 contact-feedback 병목을 보여줍니다.",
            "lab_action": "manipulation task마다 visual progress, tactile residual, force-position calibration, intervention timing, recovery action을 함께 기록합니다.",
            "limit": 5,
        },
        {
            "title": "Visual reliability는 abstain보다 evidence를 다시 사는 문제",
            "buckets": ["Foundation Models", "Safety/Alignment", "Embodied AI"],
            "ids": ["2606.16667", "2606.16586", "2606.15782", "2606.14740", "2606.15651", "2606.15202", "2606.15608", "2606.14783", "2606.16898"],
            "needles": [
                "conformal evidence acquisition",
                "local visual cue search",
                "retrieval-augmented reliability",
                "explainability",
                "self-questioning",
                "human gaze",
                "adversarial robustness",
                "privacy boundary",
                "robust refusal",
            ],
            "why": (
                "Budgeted Conformal Evidence Acquisition, LOCUS, reliability-aware retrieval, GridVQA-X, self-questioning VLM, gaze comparison을 같이 보면 "
                "신뢰성 문제는 단순히 모르면 abstain하는 쪽으로 끝나지 않습니다. 모델이 어떤 evidence를 더 봐야 하는지, 어디를 다시 crop해야 하는지, "
                "언제 judge score를 믿지 말아야 하는지를 비용과 함께 정해야 합니다."
            ),
            "confidence": "High",
            "confidence_note": "hallucination, explainability, local cue search, adversarial judge, embodied refusal 논문이 evidence acquisition 문제로 모입니다.",
            "lab_action": "VLM 평가에 answer, abstain 여부, 추가 evidence request, crop/search target, judge robustness, final groundedness를 같은 row로 저장합니다.",
            "limit": 5,
        },
        {
            "title": "Edge perception은 token budget과 safety gate를 함께 가져감",
            "buckets": ["Efficiency/Systems", "Robot Learning", "Foundation Models", "Safety/Alignment"],
            "ids": ["2606.14716", "2606.14782", "2606.16067", "2606.15346", "2606.16253", "2606.14773", "2606.16353"],
            "needles": [
                "model switching",
                "kv cache compression",
                "token selection",
                "input-adaptive",
                "image compression",
                "bandwidth-constrained",
                "streaming video model",
            ],
            "why": (
                "RAMS, BACON, Stepwise Token Selection, Dyna-Pruner, SPARC, Double-Helix Vision, SelectStream은 모두 compute를 줄이는 논문이지만 "
                "단순한 속도 경쟁으로 읽으면 핵심을 놓칩니다. 어떤 visual token을 버릴지, 언제 큰 detector로 바꿀지, VLA에 어떤 image bits를 남길지가 "
                "safety-relevant evidence를 잃지 않는 문제와 바로 연결됩니다."
            ),
            "confidence": "Medium",
            "confidence_note": "edge switching, KV cache, token pruning, VLA image compression, streaming memory가 같은 budgeted-evidence 축에 있습니다.",
            "lab_action": "latency, retained-token type, VRU 또는 task-critical miss, bandwidth, downstream policy drop을 같이 보는 deployment table을 만듭니다.",
            "limit": 5,
        },
    ],
    "research_topics": [
        {
            "title": "Action-interface ablation for VLAs",
            "claim": "같은 VLA task에서 action tokenizer, latent reasoning, early exit, retrieval, teleoperation blending을 하나씩 바꿔 latency와 success를 같이 봅니다.",
        },
        {
            "title": "Executable map benchmark",
            "claim": "3DGS, SLAM, LiDAR-camera calibration, semantic map을 pose drift와 collision-avoidance success 기준으로 같은 navigation stack에 넣어 비교합니다.",
        },
        {
            "title": "Evidence-budgeted reliability",
            "claim": "VLM이나 world model이 틀릴 때 abstain만 기록하지 말고, 추가 crop, retrieval, memory, tactile cue가 성능을 얼마나 되살리는지 측정합니다.",
        },
    ],
}


if __name__ == "__main__":
    build(PROFILE, "out/cv_new.json", "out/ro_new.json")
