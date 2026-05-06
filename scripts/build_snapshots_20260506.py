#!/usr/bin/env python3
"""Generate trends / benchmarks / insights JSON snapshots for 2026-05-06 (Wednesday)."""
import io, json, os, sys
from collections import Counter

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

sys.path.insert(0, 'scripts')
from classify import BUCKETS

DATE = "2026-05-06"

with io.open("out/classified.json", "r", encoding="utf-8") as f:
    cl = json.load(f)

cv_pw = json.load(io.open("out/cv_pastweek.json", encoding="utf-8"))
ro_pw = json.load(io.open("out/ro_pastweek.json", encoding="utf-8"))


def assign_bucket(p):
    text = (p.get('title', '') + ' ' + p.get('abstract', '')).lower()
    best = None
    best_score = 0
    for name, kws in BUCKETS:
        score = sum(1 for k in kws if k in text)
        if score > best_score:
            best_score = score
            best = name
    return best


bcv = Counter()
bro = Counter()
for p in cv_pw:
    b = assign_bucket(p)
    if b:
        bcv[b] += 1
for p in ro_pw:
    b = assign_bucket(p)
    if b:
        bro[b] += 1

PASTWEEK_KEYWORDS = [
    '3dgs', 'gaussian splat', 'splatting', 'nerf', 'slam', 'scene reconstruction',
    'diffusion', 'video', 'world model', 'vlm', 'vision-language model', 'vla',
    'vision-language-action', 'manipulation', 'humanoid', 'dexterous', 'navigation',
    'autonomous driving', 'tactile', 'robust', 'alignment', 'distillation', 'moe',
    'sparse', 'transformer', 'grounding', 'imitation', 'reinforcement learning'
]


def kw_count(papers):
    text = ' '.join((p.get('title', '') + ' ' + p.get('abstract', '')).lower() for p in papers)
    out = []
    for k in PASTWEEK_KEYWORDS:
        c = text.count(k)
        if c > 0:
            out.append([k, c])
    out.sort(key=lambda x: -x[1])
    return out


# Baseline: 7-day prior pastweek snapshot (Wednesday 2026-04-29 → use 04-29's pastweek)
baseline = json.load(io.open("trends/2026-04-29.json", encoding="utf-8"))
# In 04-29 file the pastweek totals sit under `buckets` (older schema)

trends = {
    "date": DATE,
    "totals": {
        "selected": cl["selected"],
        "total_scanned": cl["total"],
        "note": "Wednesday — cs.CV 129 new+cross + cs.RO 50 new+cross dedup → 114, 90 selected to ROI buckets. Pastweek window 2026-04-30 ~ 2026-05-06."
    },
    "buckets": {},
    "buckets_pastweek": {},
    "vs_7d_prior": {
        "baseline_date": "2026-04-29",
        "baseline_note": "Same weekday(Wed) pastweek snapshot 7 days ago — week-over-week comparison of 7-day rolling window.",
        "pastweek_buckets_delta_pct": {}
    },
    "hottest": [
        {
            "topic": "World Model evaluation이 'reward alignment + interactive bench' 양축으로 동시 표면화",
            "evidence": ["2605.03821", "2605.03941", "2603.28489"],
            "note": "RoboAlign-R1이 reconstruction loss 대신 6-dim multimodal reward 정렬로 robot video WM을 post-train + iWorld-Bench가 14 representative WM에 6 task type 통합 평가 + Video Gen as WM survey가 efficiency 측 paradigm 정리 — '학습 시그널 + 평가 프로토콜' 양쪽이 한 batch에 표면화한 자리."
        },
        {
            "topic": "VLM의 'understanding-generation gap'이 처음 formal하게 정의됨",
            "evidence": ["2605.04040"],
            "note": "UniReasoner가 'unified VLM이 prompt를 verify는 잘 하지만 generation에서는 fail'한다는 내재적 모순을 새 paradigm 이름(understanding-generation gap)으로 명시화. LLM을 universal reasoner로 두고 visual draft → critique → diffusion guidance 3-step framework — visual generation이 reasoning loop 안에 들어온 자리."
        },
        {
            "topic": "Embodied AI safety가 survey-level synthesis 단계 진입",
            "evidence": ["2605.02900"],
            "note": "400+ papers 통합한 multi-level taxonomy로 embodied AI 측 perception·cognition·planning·action·interaction 5축 attack/defense 정리 — 'embodied 측 safety 결이 문헌으로 쏟아지지만 paradigm 측 통합은 없다'는 자리에 처음 메타 정리. 어제 TAIL-Safe·Online Safety Filter 결이 표면화한 그 흐름의 메타-layer."
        },
        {
            "topic": "Efficiency/Systems의 sustained surge — DiT LoRA·KV·NPU 측 결 동시 등장",
            "evidence": ["2605.03252", "2605.03680", "2605.03555", "2605.03999"],
            "note": "Ortho-Hydra(DiT LoRA orthogonal experts) + Mobile NPU denoising distillation + MILE(continual segmentation MoE) + RD-ViT(recurrent-depth ViT) — efficiency가 어제 +15% surge 후 한 batch 더 dense하게 누적, deployment-side optimization이 한 주 내내 단독 1위 흐름."
        }
    ],
    "cooling": [
        {
            "topic": "Embodied AI 버킷 '0편'으로 한 주 내내 cold trough 깊어짐",
            "evidence": [],
            "note": "어제 5편(MCB 등) → 오늘 0편으로 단숨에 dry-up. 어제 'cold bucket이지만 paradigm-level 한 편으로 흐름 흔들기 가능' 진단했는데, 오늘은 그 한 편마저 안 등장. 한 주 평균 15편 유지지만 일별 진폭이 가장 큰 자리 — 다음주 회복 여부 관찰 필요."
        },
        {
            "topic": "Autonomous Driving이 3편으로 가장 cold(전주 16편 대비 -16% 가속)",
            "evidence": [],
            "note": "AD가 어제까지 22편이었던 자리에서 오늘 단 3편 — single-day shrink로 한 주 내내 -16% trend가 더 명확. NAVSIM/Bench2Drive 기반 evaluation methodology 흐름 외에는 결이 안 도착하는 자리."
        }
    ],
    "buckets_summary_note": "Foundation Models 19편 · Generation 16편 · Efficiency 16편 · Safety 16편 · Robot Learning 11편 · 3D/Scene 9편 · Autonomous Driving 3편 · Embodied AI 0편. FM·Gen·Eff·Safety 4편 단단한 4-way + RL 11편이 'world model post-training + dexterous + cross-embodiment' 측 substantive 지속, AD/Embodied 단독 cold trough.",
    "keywords_cv": kw_count(cv_pw)[:20],
    "keywords_ro": kw_count(ro_pw)[:20],
    "pastweek_total": {
        "cv": len(cv_pw),
        "ro": len(ro_pw)
    }
}

# Today bucket counts (mirror classified)
for bname, info in cl["buckets"].items():
    trends["buckets"][bname] = {
        "total": info["total"],
        "cv": info["cv"],
        "ro": info["ro"],
        "cvro": info["cvro"]
    }
order = ["3D/Scene", "Robot Learning", "Autonomous Driving", "Foundation Models",
         "Generation", "Efficiency/Systems", "Embodied AI", "Safety/Alignment"]
for bname in order:
    trends["buckets_pastweek"][bname] = {
        "total": bcv.get(bname, 0) + bro.get(bname, 0),
        "cv": bcv.get(bname, 0),
        "ro": bro.get(bname, 0)
    }

# delta vs baseline (pastweek vs 04-29's `buckets` which was pastweek)
for bname in order:
    today = trends["buckets_pastweek"][bname]["total"]
    prev = baseline.get("buckets", {}).get(bname, {}).get("total", 0)
    if prev > 0:
        pct = round((today - prev) / prev * 100)
        trends["vs_7d_prior"]["pastweek_buckets_delta_pct"][bname] = f"{'+' if pct>=0 else ''}{pct}%"
    else:
        trends["vs_7d_prior"]["pastweek_buckets_delta_pct"][bname] = "n/a"

os.makedirs("trends", exist_ok=True)
with io.open(f"trends/{DATE}.json", "w", encoding="utf-8", newline="\n") as fout:
    json.dump(trends, fout, ensure_ascii=False, indent=2)
sys.stderr.write(f"wrote trends/{DATE}.json\n")

# benchmarks — Wednesday
benchmarks = {
    "date": DATE,
    "results": [
        {
            "benchmark": "RobotWorldBench (10K video-instruction pairs)",
            "metric": "6-dim reward (instruction follow / manipulation / physics / etc.)",
            "value_str": "first reward-aligned WM bench introduced",
            "paper": "https://arxiv.org/abs/2605.03821",
            "paper_title": "RoboAlign-R1: Distilled Multimodal Reward Alignment for Robot Video World Models",
            "note": "10,000 annotated pairs from 4 robot data sources + 6-dim teacher judge → distilled student reward. Sliding Window Re-encoding for long-horizon drift. Quantitative SR vs baseline WM(no reward align) needs body read."
        },
        {
            "benchmark": "iWorld-Bench (interactive WM, 14 models, 6 task types)",
            "metric": "interaction ability (distance / memory / trajectory)",
            "value_str": "first unified interactive WM benchmark",
            "paper": "https://arxiv.org/abs/2605.03941",
            "paper_title": "A Benchmark for Interactive World Models with a Unified Action Generation Framework",
            "note": "330k clips → 2.1k high-quality samples + 4.9k action gen test samples. 14 representative WM evaluated. Public leaderboard."
        },
        {
            "benchmark": "VideoMME breadth (93-query)",
            "metric": "follow-up latency reduction (cache reuse)",
            "value_str": "14.90-35.92× faster (Qwen2.5-VL-7B-4bit, frozen)",
            "paper": "https://arxiv.org/abs/2605.03351",
            "paper_title": "VLMaxxing through FrameMogging: Training-Free Anti-Recomputation for Video VLMs",
            "note": "Adaptive same-video follow-up reuse preserves correctness on 93-query VideoMME breadth + 50-turn repeated-question schedules. First cold query unchanged; win on subsequent reuse."
        },
        {
            "benchmark": "OGBench (long-horizon: locomotion/manipulation/pixel)",
            "metric": "compositional plan success (multimodal regimes)",
            "value_str": "consistently outperforms compositional diffusion baselines",
            "paper": "https://arxiv.org/abs/2605.03075",
            "paper_title": "Refining Compositional Diffusion for Reliable Long-Horizon Planning",
            "note": "Training-free guidance using self-reconstruction error as log-density proxy + overlap consistency. Mode-averaging mitigated. Numerical SR vs baselines requires body read."
        },
        {
            "benchmark": "VideoMME / temporal grounding (open VLM eval)",
            "metric": "training-time MLLM-aided alignment improvement",
            "value_str": "MASRA improves over query-moment matching baselines",
            "paper": "https://arxiv.org/abs/2605.03398",
            "paper_title": "MASRA: MLLM-Assisted Semantic-Relational Consistent Alignment for Video Temporal Grounding",
            "note": "Training-time MLLM textual priors(event-level + relational) for VTG — orthogonal to inference-time active-perception line."
        }
    ],
    "proposed_benchmarks": [
        {
            "name": "RobotWorldBench",
            "paper": "https://arxiv.org/abs/2605.03821",
            "note": "10K video-instruction pairs · 6-dim reward axis · 4 robot data sources — robot WM 측 reward-aligned eval의 첫 표준 후보."
        },
        {
            "name": "iWorld-Bench",
            "paper": "https://arxiv.org/abs/2605.03941",
            "note": "Interactive WM 측 14-model leaderboard + 6-task action gen — physical interaction capability eval 표준 후보."
        }
    ],
    "note": "Wednesday batch — 5 substantive bench/SOTA reports. 가장 paradigm 측 의미 강한 결은 RobotWorldBench(robot video WM의 reward alignment eval) + iWorld-Bench(interactive WM의 unified action eval). 둘이 같은 batch에 등장한 건 'WM eval이 reconstruction loss → reward + interaction'으로 paradigm 전환 분명한 신호."
}
os.makedirs("benchmarks", exist_ok=True)
with io.open(f"benchmarks/{DATE}.json", "w", encoding="utf-8", newline="\n") as fout:
    json.dump(benchmarks, fout, ensure_ascii=False, indent=2)
sys.stderr.write(f"wrote benchmarks/{DATE}.json\n")

# insights — Wednesday
insights = {
    "date": DATE,
    "insights": [
        {
            "title": "World Model 평가가 'reconstruction loss → reward alignment + interactive eval' paradigm으로 전환",
            "claim": "RoboAlign-R1이 robot video WM을 'reward-aligned post-training + Sliding Window Re-encoding'으로 정조준하고, 같은 날 iWorld-Bench가 'interactive WM 14-model + 6-task action gen' 통합 eval을 도입 — 둘이 한 batch에 표면화한 건 'WM eval이 reconstruction/perceptual similarity 측 low-level에서 reward + interaction 측 capability-aligned로' paradigm 전환 분명한 신호. 동시에 Video Gen as WM survey가 efficiency 측 paradigm 정리 — 학습 시그널·평가 프로토콜·efficiency 3축이 한 날 통합 표면화. 우리 랩이 WM follow한다면 'pixel reconstruction'을 default substrate로 두는 setup 자체가 paradigm 측 audit 대상.",
            "papers": ["https://arxiv.org/abs/2605.03821", "https://arxiv.org/abs/2605.03941", "https://arxiv.org/abs/2603.28489"]
        },
        {
            "title": "VLM의 'understanding-generation gap'이 첫 formal 정의 단계 진입",
            "claim": "UniReasoner가 'unified VLM이 prompt를 verify(understand)는 잘 하지만 prompt-faithful generation은 fail'한다는 내재적 모순을 새 paradigm 이름(understanding-generation gap)으로 명시화하고, LLM을 universal reasoner로 두는 3-step framework(visual draft → self-critique → diffusion guidance)를 처음 systematic하게 정조준. 어제 'active perception'·'long-horizon VLA'에서 본 'sequential acquisition' 메타가 visual generation에 직접 들어온 자리 — 'verifying capability를 generation guidance로 변환한다'는 paradigm은 향후 6주 image gen 측 표준 후보. 우리 랩이 T2I generation 측면 follow한다면 understanding-generation 격차 측정 자체가 새 audit 대상.",
            "papers": ["https://arxiv.org/abs/2605.04040"]
        },
        {
            "title": "Embodied AI safety가 'paper burst → survey synthesis' 단계 진입 + 일별 진폭 최대",
            "claim": "Embodied AI Safety Survey가 400+ papers 통합한 multi-level taxonomy로 perception/cognition/planning/action/interaction 5축 attack/defense 정리 — 어제 TAIL-Safe·Online Safety Filter 등 결이 일주일 burst 한 자리에서 'paper 단계 → meta-synthesis' 단계로 진입한 분명한 신호. 동시에 Embodied AI 버킷이 0편 dry-up — 어제 5편이 paradigm 흔들었지만 오늘은 0편으로 일별 진폭 가장 큰 자리. 'cold bucket의 substrate-level 정리는 survey가 마무리하고 다음 paper batch로 넘어가는 자리'라는 패턴이 표면화한 자리예요.",
            "papers": ["https://arxiv.org/abs/2605.02900"]
        }
    ],
    "research_topics": [
        {
            "title": "Robot WM Reward-Alignment Atlas — 6-dim reward 축에서 SR-vs-WM-quality Pareto 첫 측정",
            "claim": "RoboAlign-R1이 6-dim reward(instruction following, manipulation success, physical plausibility 등)를 도입한 자리에서 다음 단계는 'reward 축이 SR로 transfer되는 정도' 정량화. RobotWorldBench(10K 쌍) × {RoboAlign-R1, baseline reconstruction WM, perceptual similarity WM} 3 paradigm × {LIBERO, RoboCasa, OGBench} 3 IL/RL bench 조합으로 'reward dimension별 SR transfer Pareto' atlas. 'WM이 정확히 어디서 robot decision-making을 돕는가' 측면 첫 정량 결과 — 향후 6주 community standard 후보. 우리 랩이 robot WM follow한다면 즉시 sprint 가치."
        },
        {
            "title": "Understanding-Generation Gap의 cross-modality 측정 표준 — VLM·VLA·VLN에서 동일 격차 측정",
            "claim": "UniReasoner가 T2I image gen에서 격차를 정의한 자리에서 다음 단계는 'VLM이 verify는 잘 하지만 generate/act는 못 한다'는 격차가 다른 modality에서도 보이는지 측정. {T2I generation, VLA action prediction, VLN navigation prediction} × {GPT-4V, Gemini, LLaVA-OV, MolmoER} matrix로 'verifying SR vs generating SR' 격차 atlas. 격차가 modality-invariant라면 paradigm 측 의미 강하고 'critique-then-generate' 메타가 universal solution이 될 가능성. 우리 랩이 multimodal 인프라 굴린다면 즉시 audit 가치."
        },
        {
            "title": "Cross-Embodiment Video Editing의 IL pipeline 통합 — 'human video → robot policy' end-to-end 측정",
            "claim": "Bridging the Embodiment Gap이 disentangled cross-embodiment video editing을 정조준한 자리에서 다음 단계는 '편집된 robot video가 정말 IL training data로 작동하는지' end-to-end 측정. {human video → editor → robot video → IL policy → real robot SR} pipeline에서 vanilla teleop data 대비 SR 격차 측정 — 'video editing as data engine'이 정말 작동하는가 question에 첫 정량 답. 어제 BifrostUMI(robot-free demo)와 같이 보면 'data democratization' 측 두 갈래(human video editing vs sparse keypoint UMI)가 동시 정착. 우리 랩이 humanoid IL 굴린다면 6주 audit 가치."
        }
    ],
    "retrospective": {
        "active": False,
        "note": "수요일 실행 — 회고는 월요일 실행에서만 활성화. 다음 회고는 2026-05-11(월) 예정."
    }
}

os.makedirs("insights", exist_ok=True)
with io.open(f"insights/{DATE}.json", "w", encoding="utf-8", newline="\n") as fout:
    json.dump(insights, fout, ensure_ascii=False, indent=2)
sys.stderr.write(f"wrote insights/{DATE}.json\n")

print(f"wrote trends/{DATE}.json, benchmarks/{DATE}.json, insights/{DATE}.json")
