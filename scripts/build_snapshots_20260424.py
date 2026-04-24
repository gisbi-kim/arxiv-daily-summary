#!/usr/bin/env python3
"""Generate trends / benchmarks / insights JSON snapshots for 2026-04-24 from classified.json."""
import io, json, os

with io.open("out/classified.json", "r", encoding="utf-8") as f:
    cl = json.load(f)

# ---- trends/2026-04-24.json ----
buckets = cl["buckets"]
trends = {
    "date": "2026-04-24",
    "totals": {
        "selected": cl["selected"],
        "total_scanned": cl["total"],
        "note": "stdlib parser (scripts/fetch_arxiv.py + scripts/classify.py); cs.CV/new + cs.RO/new listings."
    },
    "buckets": {},
    "vs_yesterday": {
        "note": "2026-04-23 대비 Safety 급증(23→27), Robot Learning 소폭 감소, 3D/Scene 유지, Generation 견조.",
        "up": ["Safety/Alignment", "Generation"],
        "down": ["Robot Learning"],
        "flat": ["3D/Scene", "Foundation Models"]
    },
    "hottest": [
        {
            "topic": "VLA 내부 이해·진단 페이즈",
            "evidence": ["2604.21192", "2604.21241", "2604.21391", "2604.21741"],
            "note": "오픈소스 VLA 해부 + spatial grounding 약점 겨냥 + post-training을 world-model 시뮬에 묶는 흐름이 한 날에 터짐"
        },
        {
            "topic": "의료 로봇 foundation dataset",
            "evidence": ["2604.21017"],
            "note": "Open-H-Embodiment가 Open X-Embodiment의 의료 버전을 표방"
        },
        {
            "topic": "VLM Blind-Spot · 체계적 실패 분석",
            "evidence": ["2604.21911", "2604.21346", "2604.21160", "2604.21395"],
            "note": "Prompt hallucination·Representational bottleneck·Geometric hallucination·이론적 blind spot이 동시 진단"
        }
    ],
    "cooling": [
        {
            "topic": "평지 humanoid locomotion (ceiling)",
            "evidence": ["2604.20990", "2604.21351", "2604.21355", "2604.21541"],
            "note": "평지 걷기는 포화, 대신 non-inertial / 무중력 / 격투 / wheel-legged 로 long-tail 분산"
        }
    ],
    "buckets_summary_note": "Safety 27편으로 1위, 그 다음 Generation 20편, Foundation Models 19편, Robot Learning 15편, 3D/Scene 13편, Efficiency/Systems 11편, Autonomous Driving 7편, Embodied AI 2편."
}
for bname, info in buckets.items():
    trends["buckets"][bname] = {
        "total": info["total"],
        "cv": info["cv"],
        "ro": info["ro"],
        "cvro": info["cvro"]
    }

with io.open("trends/2026-04-24.json", "w", encoding="utf-8", newline="\n") as f:
    json.dump(trends, f, ensure_ascii=False, indent=2)

# ---- benchmarks/2026-04-24.json ----
benchmarks = {
    "date": "2026-04-24",
    "results": [],
    "proposed_benchmarks": [
        {
            "name": "Immersion v1.0",
            "paper": "2604.21400",
            "paper_title": "YOGO: You Only Gaussian Once",
            "domain": "3DGS indoor ultra-dense",
            "what": "Ultra-dense viewpoint indoor dataset designed to break the 'sparsity shield' in current 3DGS benchmarks.",
            "risk_note": "Proposer = evaluator, 자기-벤치마크 위험 있음"
        },
        {
            "name": "WorldMark",
            "paper": "2604.21686",
            "paper_title": "WorldMark: Interactive Video World Model Benchmark Suite",
            "domain": "Interactive video world models (Genie / YUME / HY-World / Matrix-Game 등)",
            "what": "Previously each system evaluated on private scenes → unified suite for cross-comparison.",
            "risk_note": "프로토콜 설계 주체의 독립성 확인 필요"
        },
        {
            "name": "VLA Open-World Eval (How VLAs Really Work)",
            "paper": "2604.21192",
            "paper_title": "How VLAs (Really) Work In Open-World Environments",
            "domain": "Open-world manipulation VLA",
            "what": "Fixed eval suite to compare openvla·pi0·GR00T under matched conditions; identifies which factors actually produce generalization.",
            "risk_note": "시뮬 기반, real-world gap 있음"
        }
    ],
    "notable_datasets": [
        {
            "name": "Open-H-Embodiment",
            "paper": "2604.21017",
            "what": "Cross-modality / cross-task / cross-embodiment 의료 로봇 foundation-scale 데이터셋",
            "risk_note": "IRB 범위·라이선스·demographic coverage 공개 필요"
        }
    ],
    "note": "오늘 표준 벤치(ScanNet / LIBERO / nuScenes / MMMU / VBench 등)에서 새 SOTA 수치 보고 없음. 대신 '새 벤치마크·새 데이터셋 제안' 흐름이 강함."
}

with io.open("benchmarks/2026-04-24.json", "w", encoding="utf-8", newline="\n") as f:
    json.dump(benchmarks, f, ensure_ascii=False, indent=2)

# ---- insights/2026-04-24.json ----
insights = {
    "date": "2026-04-24",
    "insights": [
        {
            "title": "VLA가 블랙박스 정책 단계를 벗어나 해부·진단 페이즈로 진입",
            "claim": "오픈소스 VLA(openvla·pi0·GR00T)의 generalization 메커니즘을 정량 분해하는 How VLAs Really Work, spatial grounding 약점을 겨냥한 CorridorVLA(2604.21241), 행동 노이즈를 intent로 해석하는 Residual Bridge(2604.21391), post-training을 world-model 시뮬에 묶는 Hi-WM(2604.21741)이 같은 날 함께 등장. 블랙박스로 배포하기엔 한계가 선명해지는 전환 신호.",
            "papers": [
                "https://arxiv.org/abs/2604.21192",
                "https://arxiv.org/abs/2604.21241",
                "https://arxiv.org/abs/2604.21391",
                "https://arxiv.org/abs/2604.21741"
            ]
        },
        {
            "title": "의료 로봇이 Open X-Embodiment 모먼트에 진입 — vertical foundation dataset 경쟁 시작",
            "claim": "Open-H-Embodiment가 cross-institution·cross-embodiment 의료 로봇 데이터셋을 표방하며 foundation 모델 학습의 구조적 병목을 정면으로 품. MLLM for Built Environment(2604.21102) 같은 수직 도메인 VLM도 동시 등장 — foundation이 vertical domain dataset과 짝을 이루는 올해 흐름.",
            "papers": [
                "https://arxiv.org/abs/2604.21017",
                "https://arxiv.org/abs/2604.21102"
            ]
        },
        {
            "title": "휴머노이드 평지 걷기 포화 → long-tail 동역학으로 분산",
            "claim": "non-inertial legged survey(2604.20990), 무중력 motion learning(2604.21351), multi-skill humanoid fighting(2604.21355), wheel-legged dual-mode(2604.21541)이 하루에 동시에 등장. 다음 축이 '환경 변이·비안정 상황'으로 열리는 신호 — 벤치마크 재설계 여지가 큼.",
            "papers": [
                "https://arxiv.org/abs/2604.20990",
                "https://arxiv.org/abs/2604.21351",
                "https://arxiv.org/abs/2604.21355",
                "https://arxiv.org/abs/2604.21541"
            ]
        }
    ]
}

with io.open("insights/2026-04-24.json", "w", encoding="utf-8", newline="\n") as f:
    json.dump(insights, f, ensure_ascii=False, indent=2)

print("wrote trends / benchmarks / insights 2026-04-24.json")
