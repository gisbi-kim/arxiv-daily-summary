#!/usr/bin/env python3
"""Generate the recoverable 2026-07-03..10 daily backfills."""
from __future__ import annotations

import datetime as dt
import sys

from daily_backfill_lib import build, week_start


DATES = ["2026-07-03", "2026-07-07", "2026-07-08", "2026-07-09", "2026-07-10"]

DAY_FOCUS = {
    "2026-07-03": ("world simulation, Gaussian SLAM, VLA robustness", "현실 배포를 위한 폐루프 검증"),
    "2026-07-07": ("대규모 VLA, 장기 navigation, long-tail driving", "규모 확장 뒤의 안전성과 일반화"),
    "2026-07-08": ("4D world model, visual SLAM, geometry-aware VLA", "3D 동역학과 로봇 행동의 결합"),
    "2026-07-09": ("VLA memory, multi-robot control, dense Gaussian SLAM", "기억과 협업을 포함한 폐루프 제어"),
    "2026-07-10": ("lightweight VLA, deformable SLAM, driving shift", "경량화와 분포 변화에 강한 배포"),
}


def profile(date: str) -> dict:
    signals, decision = DAY_FOCUS[date]
    weekday = dt.date.fromisoformat(date).strftime("%a")
    specs = [
        ("Geometry/SLAM", ["3D/Scene"], ["slam", "gaussian", "lidar", "geometry", "reconstruction", "mapping"],
         "3D 표현의 시각 품질만으로는 로봇 map의 유효성을 판단할 수 없습니다. 오늘 묶음은 geometry, Gaussian, LiDAR 신호를 pose drift와 downstream localization 성공률로 연결해 비교할 필요를 보여줍니다.",
         "동일 trajectory에서 dynamic-object, sparse-view, loop-closure stress split을 구성하고 pose drift, relocalization, navigation success를 공동 측정합니다."),
        ("Robot learning/VLA", ["Robot Learning"], ["vla", "robot", "manipulation", "humanoid", "world model", "policy"],
         "로봇 학습은 더 큰 policy나 더 많은 demonstration을 제시하는 단계를 넘어, 새로운 embodiment와 교란 조건에서 행동이 유지되는지를 묻고 있습니다. 대표 논문들은 perception, memory, dynamics를 실제 task success와 분리해 검증할 근거를 제공합니다.",
         "조작 및 이동 task에서 embodiment, observation delay, unseen object를 ablation하고 success, recovery time, collision을 비교합니다."),
        ("Closed-loop autonomy", ["Autonomous Driving", "Embodied AI"], ["closed-loop", "driving", "navigation", "planning", "agent", "trajectory"],
         "자율 시스템의 open-loop 정확도는 상호작용 중 누적되는 오차와 회복 능력을 가립니다. driving과 embodied navigation 논문을 함께 보면 long-tail scene, human response, horizon 증가를 폐루프 평가 축으로 묶어야 합니다.",
         "시뮬레이터에서 long-tail scene, horizon, interaction delay를 stress split으로 만들고 near-miss, goal success, recovery rate를 측정합니다."),
        ("Multimodal grounding", ["Foundation Models", "Safety/Alignment"], ["vision-language", "multimodal", "ground", "hallucination", "robust", "uncertainty"],
         "멀티모달 모델의 정답률만으로는 실제 visual evidence를 사용했는지 알 수 없습니다. grounding, hallucination, uncertainty 신호는 cue removal과 distribution shift에서 reasoning shortcut을 따로 드러내야 한다는 공통 요구로 이어집니다.",
         "VQA와 robotic instruction benchmark에서 cue removal, viewpoint shift, corrupted observation을 적용하고 answer stability와 task success를 함께 비교합니다."),
        ("Generative world models", ["Generation"], ["diffusion", "world", "video", "generation", "flow", "autoregressive"],
         "생성 모델은 샘플 품질을 넘어 action consistency와 temporal persistence를 만족해야 로봇 실험에 쓸 수 있습니다. 오늘 논문들은 diffusion, video, world representation을 downstream perception 및 planning failure와 연결할 필요를 보여줍니다.",
         "동일 scene에서 horizon, occlusion, action perturbation을 바꾸고 temporal consistency, perception score, planning failure rate를 공동 평가합니다."),
        ("Efficient deployment", ["Efficiency/Systems"], ["efficient", "compression", "pruning", "token", "lightweight", "real-time"],
         "효율화는 FLOPs 감소만으로 끝나지 않고 중요한 spatial token과 안전 관련 정보를 보존해야 합니다. 압축과 pruning 논문은 latency 이득을 robustness 및 downstream control 손실과 함께 기록해야 한다는 신호입니다.",
         "동일 모델에서 token budget, quantization, pruning ratio를 조절하고 latency, memory, OOD 성능, control success의 Pareto frontier를 비교합니다."),
    ]
    cluster_specs = []
    for name, buckets, needles, why, action in specs:
        cluster_specs.append({
            "title": f"{name}: {decision} ({date})",
            "buckets": buckets,
            "ids": [],
            "needles": needles,
            "why": why,
            "confidence": "Medium",
            "confidence_note": "해당 날짜의 title, subject, ROI bucket에서 반복된 신호를 기준으로 묶었습니다.",
            "lab_action": action,
            "limit": 6,
        })
    return {
        "date": date,
        "weekday": weekday,
        "week_start": week_start(date),
        "source_mode": "pastweek-date-section",
        "source_label": "arXiv cs.CV/pastweek date section + cs.RO/pastweek date section",
        "source_note": f"Backfill parser output from the {date} /pastweek date sections",
        "benchmark_note": "Backfill artifact generated from arXiv /pastweek date sections; abstracts are not available in this source.",
        "thesis": f"{date} 배치의 중심 신호는 {signals}입니다. APRL 관점에서는 {decision}을 공통 평가축으로 삼아 성능뿐 아니라 실패 조건과 회복 능력을 함께 비교해야 합니다.",
        "cluster_takeaway": f"오늘의 판세는 {signals}이 서로 분리된 주제가 아니라 {decision}이라는 한 가지 실험 질문으로 모인다는 점입니다.",
        "trend_note": f"title/subject 기반 backfill에서 {signals} 관련 논문이 두드러졌으며, 핵심 판단 기준은 {decision}입니다.",
        "cluster_specs": cluster_specs,
        "research_topics": [
            {"title": f"{decision} stress suite", "claim": "geometry, policy, multimodal model을 동일한 교란 조건에서 비교해 failure mode와 recovery를 분리합니다."},
            {"title": "Robot-usable geometry benchmark", "claim": "3D 표현을 rendering score가 아니라 localization drift와 navigation success로 평가합니다."},
            {"title": "Resource-aware embodied evaluation", "claim": "token budget과 latency를 조절하며 perception robustness와 control success의 trade-off를 측정합니다."},
        ],
    }


if __name__ == "__main__":
    targets = sys.argv[1:] or DATES
    for date in targets:
        compact = date.replace("-", "")
        build(profile(date), f"out/cv_{compact}.json", f"out/ro_{compact}.json")
