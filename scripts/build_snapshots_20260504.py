#!/usr/bin/env python3
"""Generate trends / benchmarks / insights JSON snapshots for 2026-05-04 (Monday — retrospective)."""
import io, json, os, sys
from collections import Counter

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

sys.path.insert(0, 'scripts')
from classify import BUCKETS

DATE = "2026-05-04"

with io.open("out/classified.json", "r", encoding="utf-8") as f:
    cl = json.load(f)

cv_pw = json.load(io.open("out/cv_pastweek.json", encoding="utf-8"))
ro_pw = json.load(io.open("out/ro_pastweek.json", encoding="utf-8"))

def assign_bucket(p):
    text = (p.get('title','') + ' ' + p.get('abstract','')).lower()
    best = None; best_score = 0
    for name, kws in BUCKETS:
        score = sum(1 for k in kws if k in text)
        if score > best_score:
            best_score = score; best = name
    return best

bcv = Counter(); bro = Counter()
for p in cv_pw:
    b = assign_bucket(p)
    if b: bcv[b] += 1
for p in ro_pw:
    b = assign_bucket(p)
    if b: bro[b] += 1

PASTWEEK_KEYWORDS = [
    '3dgs','gaussian splat','splatting','nerf','slam','scene reconstruction',
    'diffusion','video','world model','vlm','vision-language model','vla',
    'vision-language-action','manipulation','humanoid','dexterous','navigation',
    'autonomous driving','tactile','robust','alignment','distillation','moe',
    'sparse','transformer','grounding','imitation','reinforcement learning'
]
def kw_count(papers):
    text = ' '.join((p.get('title','') + ' ' + p.get('abstract','')).lower() for p in papers)
    out = []
    for k in PASTWEEK_KEYWORDS:
        c = text.count(k)
        if c > 0: out.append([k, c])
    out.sort(key=lambda x: -x[1])
    return out

# baseline: prior Monday 2026-04-27 pastweek snapshot (week-over-week)
baseline = json.load(io.open("trends/2026-04-27.json", encoding="utf-8"))

trends = {
    "date": DATE,
    "totals": {
        "selected": cl["selected"],
        "total_scanned": cl["total"],
        "note": "Monday — fresh /new batch (cs.CV 81 new+cross + cs.RO 26 new+cross), pastweek window 2026-04-28 ~ 2026-05-04. Retrospective loop active vs 2026-04-23 insights (closest available; 04-20 not snapshotted)."
    },
    "buckets": {},
    "buckets_pastweek": {},
    "vs_7d_prior": {
        "baseline_date": "2026-04-27",
        "baseline_note": "Prior Monday pastweek snapshot — week-over-week comparison of 7-day rolling window.",
        "pastweek_buckets_delta_pct": {}
    },
    "hottest": [
        {
            "topic": "VLA latent reasoning paradigm 2주차 — pixel-free world-action models 정착",
            "evidence": ["2605.00078", "2605.00080", "2605.00412"],
            "note": "Being-H0.7가 'pixel-space prediction은 비효율적' 정조준 + Hamiltonian WM이 'physically meaningful' 측 paradigm 제안 + WM Survey가 정리. LaST-R1(지난주) 후속 결로 paradigm 단단해지는 모양새."
        },
        {
            "topic": "Autonomous Driving evaluation methodology — open vs closed-loop 격차 정량화",
            "evidence": ["2605.00066", "2605.00050"],
            "note": "NAVSIM PDM ↔ Bench2Drive 8-method 페어링 분석으로 'open-loop은 closed-loop 예측에 한계' 정량화 + 사고 reconstruction이 새 substrate."
        },
        {
            "topic": "Visual modality safety surface — VLM jailbreak 측정 가능해진 자리",
            "evidence": ["2605.00583", "2605.00326"],
            "note": "Visual cipher 40.9% ASR(Claude-Haiku-4.5)·prompt-induced score variance가 'safety = text-only training이 vision으로 전이 안 됨' 정조준."
        },
        {
            "topic": "3DGS RL-based density control 등장",
            "evidence": ["2605.00408"],
            "note": "LeGS가 heuristic density control을 RL policy로 대체 + Mip-NeRF 360/Tanks Temples/Deep Blending 3개 표준 벤치 통과. 'RL이 3DGS 학습 stack에 들어오는' 첫 결."
        }
    ],
    "cooling": [
        {
            "topic": "Tactile/Contact-rich 측은 이번주 조용 (지난주 burst)",
            "evidence": [],
            "note": "지난주 DOT-Sim·FlexiTac·KernelSOS 등 4편 burst 후 이번주 /new에는 tactile 측 결 0편 — Generation·FM은 keyword 잡음 큰 반면 hard manipulation 자리는 일시 cool."
        },
        {
            "topic": "Embodied AI 단일일 3편 — Monday 배치 치고 적음",
            "evidence": [],
            "note": "프라이데이 배치(5/1 일요일 회고 시점) 대비도 비슷한 자리, Monday 치고는 가장 조용. 한 주 더 봐야 진짜 cooling vs 일시 분포 변동 판단 가능."
        }
    ],
    "buckets_summary_note": "Generation 17편 · Efficiency 14편 · 3D/Scene 13편 · RL 12편 · AD 9편 · FM 8편 · Safety 8편 · Embodied 3편. Generation·Efficiency 양강 + 3D/RL 중간 + Embodied 단독 cold. Generation은 medical imaging·remote sensing 응용 잡음이 많아 라벨 vs substantive 결 분리 필요.",
    "keywords_cv": kw_count(cv_pw)[:20],
    "keywords_ro": kw_count(ro_pw)[:20],
    "pastweek_total": {
        "cv": len(cv_pw),
        "ro": len(ro_pw)
    }
}

for bname, info in cl["buckets"].items():
    trends["buckets"][bname] = {
        "total": info["total"],
        "cv": info["cv"],
        "ro": info["ro"],
        "cvro": info["cvro"]
    }
order = ["3D/Scene","Robot Learning","Autonomous Driving","Foundation Models","Generation","Efficiency/Systems","Embodied AI","Safety/Alignment"]
for bname in order:
    trends["buckets_pastweek"][bname] = {
        "total": bcv.get(bname, 0) + bro.get(bname, 0),
        "cv": bcv.get(bname, 0),
        "ro": bro.get(bname, 0)
    }

# delta vs baseline (pastweek vs pastweek)
for bname in order:
    today = trends["buckets_pastweek"][bname]["total"]
    prev = baseline["buckets"].get(bname, {}).get("total", 0)
    if prev > 0:
        pct = round((today - prev) / prev * 100)
        trends["vs_7d_prior"]["pastweek_buckets_delta_pct"][bname] = f"{'+' if pct>=0 else ''}{pct}%"
    else:
        trends["vs_7d_prior"]["pastweek_buckets_delta_pct"][bname] = "n/a"

os.makedirs("trends", exist_ok=True)
with io.open(f"trends/{DATE}.json", "w", encoding="utf-8", newline="\n") as fout:
    json.dump(trends, fout, ensure_ascii=False, indent=2)
sys.stderr.write(f"wrote trends/{DATE}.json\n")

# benchmarks
benchmarks = {
    "date": DATE,
    "results": [
        {
            "benchmark": "Mip-NeRF 360 + Tanks & Temples + Deep Blending",
            "metric": "PSNR/SSIM (3 datasets aggregate)",
            "value_str": "SOTA across 3",
            "paper": "https://arxiv.org/abs/2605.00408",
            "paper_title": "LeGS: Beyond Heuristics — Learnable Density Control for 3DGS via RL",
            "note": "Reward function for density control via RL — claim covers all 3 standard 3DGS benches; per-scene breakdown unverified from abstract."
        },
        {
            "benchmark": "long-horizon manipulation (sim)",
            "metric": "average success rate",
            "value": 95.5,
            "value_str": "95.5%",
            "paper": "https://arxiv.org/abs/2605.00438",
            "paper_title": "IVLR: Interleaved Vision-Language Reasoning Traces",
            "note": "Avg across simulated long-horizon benches; specific suite (LIBERO-Long?) needs verification — see risk filter"
        },
        {
            "benchmark": "fleet manipulation (16 dual-arm robots, 8 tasks)",
            "metric": "single generalist policy uplift",
            "value_str": "improves vs pretrained baseline",
            "paper": "https://arxiv.org/abs/2605.00416",
            "paper_title": "LWD: Learning While Deploying — Fleet-Scale RL for VLA",
            "note": "Real-world 16-robot fleet, 8 tasks incl. semantic grocery + 3-5min long-horizon; abstract uplift quantification ambiguous"
        },
        {
            "benchmark": "Claude-Haiku-4.5 visual cipher attack",
            "metric": "Attack Success Rate",
            "value": 40.9,
            "value_str": "40.9%",
            "paper": "https://arxiv.org/abs/2605.00583",
            "paper_title": "Jailbreaking VLMs through the Visual Modality",
            "note": "vs 10.7% for equivalent textual cipher — cross-modality safety gap quantified for the first time on frontier VLMs"
        },
        {
            "benchmark": "Vulkan 3DGS training (cross-vendor GPU)",
            "metric": "speed/VRAM vs CUDA+PyTorch",
            "value_str": "3.3× speed, -33% VRAM",
            "paper": "https://arxiv.org/abs/2605.00219",
            "paper_title": "VkSplat: High-Performance 3DGS in Vulkan",
            "note": "First fully-Vulkan 3DGS training pipeline — cross-vendor GPU compatibility(AMD/Intel/NVIDIA)"
        }
    ],
    "proposed_benchmarks": [],
    "note": "Monday batch — 5 substantive SOTA reports across 3D/RL/Safety/Eff. ScanNet++/Mip-NeRF 360 측 새 SOTA 분명히 등장(LeGS), VLA fleet RL 측 LWD 첫 large-scale 결, VLM safety 측 frontier-model attack 측정 첫 결."
}
os.makedirs("benchmarks", exist_ok=True)
with io.open(f"benchmarks/{DATE}.json", "w", encoding="utf-8", newline="\n") as fout:
    json.dump(benchmarks, fout, ensure_ascii=False, indent=2)
sys.stderr.write(f"wrote benchmarks/{DATE}.json\n")

# insights — Monday angle, with retrospective context
insights = {
    "date": DATE,
    "insights": [
        {
            "title": "VLA paradigm shift 2주차 — 'pixel-free latent world-action models'이 community standard로 굳는 중",
            "claim": "지난주 LaST-R1·MotuBrain·PRTS 셋이 'latent CoT + RL'을 정조준한 후 1주만에 Being-H0.7(latent world-action without future frame) + Hamiltonian WM(physics-grounded latent dynamics) + IVLR(95.5% long-horizon)이 나란히 등장. 'pixel-space prediction은 비효율적이고 우회 substrate'라는 같은 진단을 다른 axis로 정조준 — 2주 연속 같은 paradigm이 누적되는 건 burst가 아니라 community standard 정착의 분명한 신호. 우리 랩이 VLA에서 future frame prediction을 substrate로 쓰고 있다면 paradigm 선회 시점.",
            "papers": ["https://arxiv.org/abs/2605.00078", "https://arxiv.org/abs/2605.00080", "https://arxiv.org/abs/2605.00412", "https://arxiv.org/abs/2605.00438"]
        },
        {
            "title": "VLM Safety가 'text 부수 효과'에서 'visual modality first-class attack surface'로 paradigm 전환",
            "claim": "Visual cipher 40.9% ASR(Claude-Haiku-4.5) vs textual cipher 10.7% — 4배 격차로 'text-based safety training은 visual modality로 자동 일반화 안 됨' 정량화. 한 주 전에 우리가 'safety 라벨 잡음 vs architecture-level 결 분리해야 한다'고 본 자리에서, 이번주는 'visual modality 자체가 첫 번째 attack surface' 측 paradigm shift가 직접 등장 — 'human-aware'·'hierarchical robust' 류 텍스트 측 alignment만으로는 불충분. 우리 랩이 VLM 측 safety follow한다면 visual-first attack 측정 framework이 곧 표준 될 자리.",
            "papers": ["https://arxiv.org/abs/2605.00583", "https://arxiv.org/abs/2605.00326", "https://arxiv.org/abs/2605.00321"]
        },
        {
            "title": "Autonomous Driving evaluation methodology — 'open-loop ↔ closed-loop' 격차의 첫 정량화",
            "claim": "Open-Loop vs Closed-Loop Cross-Benchmark Correlation 논문이 NAVSIM PDM ↔ Bench2Drive 8 methods 페어링으로 'NAVSIM PDM은 강한 양 correlation but non-monotonic + ranking inversion' 정량화. EP(Ego Progress)가 가장 강한 단일 predictor 발견. 한 주 전에 본 'driving WM unified understanding+generation' 흐름과 함께 보면 community가 'open-loop benchmark 의존'에서 'closed-loop 표준 통과 의무'로 무게중심 이동. 우리 랩이 AD 평가 protocol 설계할 때 NAVSIM-only 검증으로는 신뢰성 보장 어려움.",
            "papers": ["https://arxiv.org/abs/2605.00066", "https://arxiv.org/abs/2605.00050"]
        }
    ],
    "research_topics": [
        {
            "title": "Pixel-Free VLA World-Action Bench — Latent vs Pixel Substrate Atlas",
            "claim": "Being-H0.7·Hamiltonian WM·LaST-R1·IVLR가 모두 'pixel-free' 측을 정조준했지만 '같은 task에서 latent vs pixel substrate를 head-to-head 비교'한 결은 비어 있어요. LIBERO·CALVIN·RoboCasa × {pixel rollout WM, latent WAM, Hamiltonian latent} 3 paradigm × 3 표준 벤치 atlas로 묶으면 향후 6주 안에 community standard 후보. 첫 mover 자리가 가장 비어있는 timing — paradigm 굳어가는 자리니 비교 paper 1편이 즉시 가치."
        },
        {
            "title": "Visual-First VLM Safety Bench — Cross-Modal Attack Surface Atlas",
            "claim": "Visual cipher·object substitution·text-in-image swap·visual analogy puzzle 4가지 visual attack을 frontier VLM 6개에 측정한 첫 결을 atlas로 확장 — open VLM(LLaVA·Qwen-VL)까지 포함해 'text safety vs visual safety 격차'를 model 별로 측정한 standard bench. 향후 VLM safety 평가의 첫 표준 가능성. 우리 랩이 VLM eval 인프라 있다면 즉시 sprint 가치."
        },
        {
            "title": "Closed-Loop AD Evaluation Methodology Audit — NAVSIM/Bench2Drive 외 3rd suite 정착 가능성 평가",
            "claim": "Open-Loop vs Closed-Loop 논문이 'ranking inversion' 정량화한 자리에서, NAVSIM·Bench2Drive 외 CARLA Leaderboard·nuPlan과의 4-way correlation 측정이 다음 단계. 어떤 metric이 4-suite cross-validation에서 살아남는가가 community가 합의할 closed-loop 표준의 첫 조건 — 우리 랩이 AD 측 평가 인프라 있다면 6주 audit 가치."
        }
    ],
    "retrospective": {
        "active": True,
        "two_weeks_ago": {
            "source_date": "2026-04-23",
            "note": "2026-04-20 insights 미존재(snapshotting 시작 전), 가장 가까운 04-23 사용 (delta 11일).",
            "predictions_scored": [
                {
                    "label": "✅ 적중",
                    "original": "World model 평가가 픽셀 품질에서 embodied 성공률로 이동",
                    "evidence": "오늘 Being-H0.7가 'pixel-space prediction이 비효율적 substrate'라며 latent world-action으로 직접 선회. 같은 날 World Model for Robot Learning Survey + Hamiltonian WM 모두 'pixel-quality vs embodied success' 경계를 명시적으로 인용. 2주 전 예측 방향 그대로 community 결이 쏟아진 자리 — 가장 강한 적중."
                },
                {
                    "label": "✅ 적중",
                    "original": "VLA가 알고리즘 경쟁에서 훈련 스택·표현 통일의 인프라 경쟁으로 국면 전환",
                    "evidence": "LWD(fleet-scale RL infra for VLA)·Lucid-XR(XR data engine)·MSACT(low-latency 만이프 인프라)·E²DT(efficient DT replay infra)가 한 날 4편 — 인프라 측 paper 비중이 알고리즘 측 대비 분명히 우세해진 자리. 2주 전 예측 그대로 'infrastructure race' 표면화."
                },
                {
                    "label": "◐ 부분적중",
                    "original": "Safety 버킷이 얇은 만큼 'human-aware'·'hierarchical robust' 같은 새 포지셔닝이 뚫리는 중",
                    "evidence": "Safety는 분명히 새 포지션이 등장했지만 'human-aware'·'hierarchical robust' 측은 아니고, 'visual modality first-class attack surface'(jailbreak·prompt variance·embodied interpretability)로 분기. 방향 자체는 맞췄지만 구체적 포지션 키워드는 빗나간 자리."
                }
            ]
        },
        "four_weeks_ago": {
            "source_date": "n/a",
            "note": "2026-04-06 insights 미존재(snapshotting 시작 전). 4주 회고 다음주(2026-05-11)부터 첫 가능."
        },
        "two_weeks_topics_scored": [
            {
                "label": "⏳ 관찰 중",
                "original": "VLA Foundry 위에 safety head를 plug-in으로 얹기",
                "evidence": "VLA Foundry 후속 결은 안 나타났지만 'safety head plug-in' 자체는 직접 시도가 없고, jailbreak 측 결만 등장 — 제안 자리가 여전히 비어있어 관찰 보류."
            },
            {
                "label": "✗ 빗나감",
                "original": "Mask 수준 world model을 cross-embodiment RoboWM-Bench로 확장",
                "evidence": "RoboWM-Bench 후속 결 없고, World Model 측은 'pixel-free latent' 방향으로 분기 — Mask WM 측 cross-embodiment 확장 자리는 비어있는 채로 paradigm 자체가 바뀌어버림."
            },
            {
                "label": "⏳ 관찰 중",
                "original": "Language-driven 3DGS editing을 로봇 시뮬 asset 파이프라인에 결합",
                "evidence": "GSDrive(driving sim용 3DGS env)가 가장 가까운 결이지만 'language-driven editing' 측면은 아니고 'closed-loop RL substrate'로 분기 — 제안 자리는 여전히 비어있음."
            }
        ]
    }
}

os.makedirs("insights", exist_ok=True)
with io.open(f"insights/{DATE}.json", "w", encoding="utf-8", newline="\n") as fout:
    json.dump(insights, fout, ensure_ascii=False, indent=2)
sys.stderr.write(f"wrote insights/{DATE}.json\n")
