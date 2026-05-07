#!/usr/bin/env python3
"""Generate trends / benchmarks / insights JSON snapshots for 2026-05-07 (Thursday)."""
import io, json, os, sys
from collections import Counter

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

sys.path.insert(0, 'scripts')
from classify import BUCKETS

DATE = "2026-05-07"

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
    'sparse', 'transformer', 'grounding', 'imitation', 'reinforcement learning',
    '4d', 'latent action', 'preference', 'hallucination'
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


# Baseline: same-weekday(Thu) 7 days ago = 2026-04-30
baseline = json.load(io.open("trends/2026-04-30.json", encoding="utf-8"))

trends = {
    "date": DATE,
    "totals": {
        "selected": cl["selected"],
        "total_scanned": cl["total"],
        "note": "Thursday — cs.CV 190 new+cross + cs.RO 65 new+cross dedup → 146 unique, 123 selected to ROI buckets. Pastweek window 2026-05-01 ~ 2026-05-07."
    },
    "buckets": {},
    "buckets_pastweek": {},
    "vs_7d_prior": {
        "baseline_date": "2026-04-30",
        "baseline_note": "Same weekday(Thu) pastweek snapshot 7 days ago — week-over-week comparison of 7-day rolling window.",
        "pastweek_buckets_delta_pct": {}
    },
    "hottest": [
        {
            "topic": "VLA의 'latent action supervision' formulation이 처음 systematic 정리됨 — image-based vs action-based 구분",
            "evidence": ["2605.04678", "2605.05126", "2605.05092"],
            "note": "From Pixels to Tokens가 latent action supervision을 (i) image-based(trajectory regularization) vs (ii) action-based(target unification) 두 갈래로 정리하고, formulation-task correspondence를 처음 정량 측정 — image-based는 long-horizon reasoning + scene generalization, action-based는 motor coordination에 강함. 'discrete latent action token으로 직접 VLM 감독'이 가장 효과적. 같은 batch에 ConsisVLA-4D(spatiotemporal consistency for 4D-reasoning manipulation) + Driver-WM(driver-centric latent WM)이 동시 등장 — VLA latent substrate 측 paradigm이 한 batch에 단단해진 자리."
        },
        {
            "topic": "4D World Model 평가의 첫 표준 정착 — LoViF 2026 PhyScore challenge",
            "evidence": ["2605.05187", "2605.04527", "2605.04435", "2605.05163"],
            "note": "LoViF 2026 PhyScore가 1554 videos × 7 generative models × 26 physics-relevant categories(dynamics·optics·thermodynamics)로 4D WM의 holistic quality(Video Quality·Physical Realism·Condition-Video Alignment·Temporal Consistency)와 anomaly localization 평가를 도입. Velox(4D geometry+appearance representation) + Ground4D(off-road feedforward 4D recon) + PhysForge(physics-grounded 3D assets via VLM physical architect) 동시 등장 — 어제 iWorld-Bench(interactive WM)에 이어 4D substrate의 평가 표준이 한 주 만에 완성형 자리."
        },
        {
            "topic": "Diffusion alignment paradigm이 BT model 측 가정 깬 game-theoretic 정의로 이동",
            "evidence": ["2605.04494", "2605.05204", "2605.04647"],
            "note": "Diff-NPO가 'Bradley-Terry preference model이 human preference 복잡성을 못 잡는다'는 진단으로 diffusion alignment를 game-theoretic Nash Equilibrium으로 reframe — current policy가 자기 자신과 play해 self-improvement. 같은 batch에 D-OPSD(on-policy self-distillation for step-distilled diffusion) + ReflectDrive-2(RL-aligned self-editing for discrete diffusion driving) — 'self-play / self-distillation / self-editing'이라는 self-referential alignment paradigm이 한 batch에 3 layer 누적."
        },
        {
            "topic": "Generation 버킷이 26편으로 단독 1위 surge — TTS·flow matching·preference·outlier token 결 총집결",
            "evidence": ["2605.04461", "2605.04590", "2605.05206", "2605.04412", "2605.04494", "2605.04566"],
            "note": "Stream-T1(streaming video gen TTS) + From Diffusion to Rectified Flow(text-based seg paradigm 재정의) + Taming Outlier Tokens in DiT + DiLAST(structured 3D latents · 2D diffusion teacher · OOD style) + Diff-NPO + Open-Source Image Editing as Zero-Shot Vision Learners — Generation이 한 batch에 26편으로 다른 버킷의 1.5배. 어제 TOP3(FM·Gen·Eff)가 오늘 Gen 단독 1위로 굳어진 자리."
        }
    ],
    "cooling": [
        {
            "topic": "Embodied AI 4편 — 어제 0편 dry-up에서 미세 회복했지만 substantive는 1편(PhysForge)뿐",
            "evidence": ["2605.05163", "2605.05017"],
            "note": "어제 0편에서 4편으로 미세 회복했지만 substantive paradigm 결은 PhysForge 한 편이 사실상 전부. 나머지 3편은 underwater AUV navigation·low-thrust rendezvous·privacy position paper로 specialized. Embodied 측 'paradigm-defining paper batch 부재'가 일주일 더 이어지는 자리."
        },
        {
            "topic": "Autonomous Driving 13편 — 회복했지만 deployment-side 일색, paradigm 결 약함",
            "evidence": [],
            "note": "어제 3편 cold trough에서 13편으로 회복. 다만 substantive paradigm 결은 ReflectDrive-2(RL-aligned discrete diffusion driving) + Driver-WM(driver-centric latent WM) + CRAFT(counterfactual-to-interactive RL fine-tune) 정도. 나머지는 sensor fusion·scenario gen·mmWave beam mgmt 등 응용 결로 deployment optimization 라인이 dominant — Wayve/Tesla 등 industry-driven paradigm 흐름 약화 신호."
        }
    ],
    "buckets_summary_note": "Generation 26 · Foundation Models 18 · Efficiency/Systems 18 · 3D/Scene 15 · Safety/Alignment 15 · Robot Learning 14 · Autonomous Driving 13 · Embodied AI 4. Generation 단독 1위(다른 버킷 1.5배) + 4-way mid(FM·Eff·3D·Safety) + RO 측 RL/AD substantive layer + Embodied 4편 dry-up 지속.",
    "keywords_cv": kw_count(cv_pw)[:20],
    "keywords_ro": kw_count(ro_pw)[:20],
    "pastweek_total": {
        "cv": len(cv_pw),
        "ro": len(ro_pw)
    }
}

# Today bucket counts
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

# delta vs baseline (Thu pastweek vs 04-30 Thu pastweek)
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

# benchmarks — Thursday
benchmarks = {
    "date": DATE,
    "results": [
        {
            "benchmark": "LoViF 2026 PhyScore Challenge (1554 videos, 7 WM, 26 categories)",
            "metric": "Holistic 4D WM QA: Video Quality + Physical Realism + Condition-Video Alignment + Temporal Consistency + anomaly localization",
            "value_str": "first holistic 4D WM QA challenge with physics-relevant categories (dynamics/optics/thermodynamics)",
            "paper": "https://arxiv.org/abs/2605.05187",
            "paper_title": "LoViF 2026: First Challenge on Holistic Quality Assessment for 4D World Model (PhyScore)",
            "note": "1,554 videos × 7 representative WM × 26 categories(physics dynamics·optics·thermodynamics + creative content). 3 tracks(text-2D, image-to-4D, video-to-4D). Composite eval = TimeStamp_IOU + SRCC/PLCC. Trained human annotation + auto QC. iWorld-Bench(interaction)와 LoViF(physics)의 4D WM eval 양축이 한 주 만에 정착."
        },
        {
            "benchmark": "ConsisVLA-4D on robotic manipulation (multi-view 4D reasoning)",
            "metric": "Manipulation success uplift via spatiotemporal consistency (CV-Aligner + CO-Fuser + CS-Thinker)",
            "value_str": "+21.6% and +41.5% improvement (two evaluation regimes)",
            "paper": "https://arxiv.org/abs/2605.05126",
            "paper_title": "ConsisVLA-4D: Advancing Spatiotemporal Consistency in Efficient 3D-Perception and 4D-Reasoning for Robotic Manipulation",
            "note": "VLA의 2D→action 측 spatial/temporal 한계(extra sensor + future-frame prediction이 instruction-grounded scene 측 alignment 결여)를 cross-view consistency + cross-object consistency + cross-scene consistency 3축으로 처방. Latent compact representation으로 'extra sensor 없이' 측 efficiency. From Pixels to Tokens(image-based latent action) line의 4D extension."
        },
        {
            "benchmark": "ELVIS on DeepMind Control Suite (14 visual tasks)",
            "metric": "Long-horizon visual MPC success vs TD-MPC2/DreamerV3",
            "value_str": "SOTA across 14 tasks + zero-shot real-world transfer",
            "paper": "https://arxiv.org/abs/2605.04709",
            "paper_title": "ELVIS: Ensemble-Calibrated Latent Imagination for Long-Horizon Visual MPC",
            "note": "Dreamer-style RSSM + GMM-MPPI(unimodal MPPI 대신 multimodal hypothesis 유지) + ensemble UCB λ-return으로 'compounding model error in deep imagination' 처방. Zero-shot real-world sand-spraying task에 transfer까지 보고. RoboAlign-R1(reward-aligned WM)·Dream-MPC(gradient-based latent MPC) 라인의 long-horizon visual control 측 결."
        },
        {
            "benchmark": "Q2RL on D4RL + robomimic (manipulation, contact-rich, high-precision)",
            "metric": "Offline-to-online success rate / time-to-convergence",
            "value_str": "100% SR on pipe assembly+kitting · 3.75× improvement vs BC · 1-2 hours on-robot",
            "paper": "https://arxiv.org/abs/2605.05172",
            "paper_title": "When Life Gives You BC, Make Q-functions: Extracting Q-values from Behavior Cloning for On-Robot RL",
            "note": "BC policy에서 Q-function을 'few interaction step'으로 추출 + Q-Gating으로 BC/RL action switching → 'distribution mismatch로 good action 잃는' offline→online 전환 측 표준 문제 처방. On-robot 1-2시간 학습으로 contact-rich manipulation 100% SR. From Pixels to Tokens(VLA latent action)·ConsisVLA-4D(4D consistency) 라인의 'offline-to-online' 측 결."
        },
        {
            "benchmark": "PhysForge / PhysDB (150,000 assets · 4-tier physical annotation)",
            "metric": "Physics-grounded 3D asset gen with VLM 'physical architect' planner",
            "value_str": "first large-scale physically-annotated 3D asset dataset for embodied AI",
            "paper": "https://arxiv.org/abs/2605.05163",
            "paper_title": "PhysForge: Generating Physics-Grounded 3D Assets for Interactive Virtual World",
            "note": "VLM이 hierarchical physical blueprint(material/functional/kinematic constraint) plan → physics-grounded diffusion model이 KineVoxel Injection(KVI)으로 geometry + kinematic param 동시 합성. Embodied AI 측 'static geometry → functional/kinematic asset' paradigm 전환의 첫 large-scale dataset 자리."
        },
        {
            "benchmark": "Real-world dermatology MLLM benchmark-to-bedside gap",
            "metric": "Top-3 diagnostic accuracy (real-world consultation cohort 5811 cases / 46405 images)",
            "value_str": "public bench 26.55-42.25% → real-world image-only 1.50-13.35% (open) / 24.65% (GPT-4.1)",
            "paper": "https://arxiv.org/abs/2605.04098",
            "paper_title": "Are Multimodal LLMs Ready for Clinical Dermatology? A Real-World Evaluation",
            "note": "어제 DALPHIN(pathology multicentric bench) 라인의 dermatology 측 결. Public bench 대비 real-world에서 top-3 acc가 GPT-4.1조차 ~42% → ~25%로 declined. 'benchmark performance가 real-world capability를 substantially overestimate'한다는 정량 결과 — clinical FM의 deployment readiness 측 negative result."
        }
    ],
    "proposed_benchmarks": [
        {
            "name": "LoViF 2026 PhyScore",
            "paper": "https://arxiv.org/abs/2605.05187",
            "note": "1554 videos × 7 WM × 26 physics-relevant categories — 4D WM의 holistic quality + anomaly localization 표준 후보. iWorld-Bench와 함께 4D WM eval 양축."
        },
        {
            "name": "PhysDB",
            "paper": "https://arxiv.org/abs/2605.05163",
            "note": "150K assets × 4-tier physical annotation — embodied AI interactive asset generation의 첫 large-scale data substrate."
        }
    ],
    "note": "Thursday batch — 6 substantive bench reports. 가장 paradigm 측 의미 강한 결은 LoViF 2026 PhyScore(4D WM holistic quality 첫 표준) + ConsisVLA-4D(VLA 4D consistency uplift +21.6/+41.5%) + Q2RL(BC→on-robot RL 1-2h SR 100%). 어제 RobotWorldBench/iWorld-Bench(WM eval reward+interaction)에 이어 4D WM eval 표준이 한 주 만에 완성된 자리."
}
os.makedirs("benchmarks", exist_ok=True)
with io.open(f"benchmarks/{DATE}.json", "w", encoding="utf-8", newline="\n") as fout:
    json.dump(benchmarks, fout, ensure_ascii=False, indent=2)
sys.stderr.write(f"wrote benchmarks/{DATE}.json\n")

# insights — Thursday
insights = {
    "date": DATE,
    "insights": [
        {
            "title": "VLA의 'latent action supervision'이 systematic study 단계 진입 — image-based vs action-based formulation-task correspondence 처음 정량",
            "claim": "From Pixels to Tokens가 latent action supervision을 (i) image-based(trajectory regularization) vs (ii) action-based(target space unification) 두 갈래로 정리하고, 4 representative integration strategy를 unified VLA baseline 위에서 비교. 'image-based latent action은 long-horizon reasoning + scene-level generalization에, action-based latent action은 complex motor coordination에' 강하다는 formulation-task correspondence를 처음 정량 측정 + 'discrete latent action token으로 VLM 직접 supervision'이 가장 효과적이라는 결론. 같은 batch에 ConsisVLA-4D(4D-reasoning robotic manipulation, +21.6/+41.5% uplift) + Driver-WM(driver-centric latent WM)이 동시 표면화 — 어제까지의 'pixel-free latent WAM' 흐름이 오늘 'latent action supervision systematic study' 단계로 한 layer 더 깊어진 자리. 우리 랩이 VLA infra를 굴린다면 즉시 audit 가치 — 'image-based vs action-based vs hybrid' 측 task별 성능 mapping이 새 표준 후보.",
            "papers": ["https://arxiv.org/abs/2605.04678", "https://arxiv.org/abs/2605.05126", "https://arxiv.org/abs/2605.05092"]
        },
        {
            "title": "4D World Model 평가가 한 주 만에 'interaction(iWorld) + physics(LoViF)' 양축으로 정착",
            "claim": "어제 iWorld-Bench가 14 representative WM × 6 task type interaction eval로 첫 표준을 도입한 자리에서, 오늘 LoViF 2026 PhyScore가 1554 videos × 7 WM × 26 physics-relevant categories(dynamics/optics/thermodynamics)로 holistic quality(VQ + Physical Realism + Condition-Video Alignment + Temporal Consistency) + anomaly localization 평가를 도입 — '4D WM eval = interaction + physics' 양축이 한 주 만에 완성된 자리예요. 동시 batch에 Velox(4D geometry+appearance latent), Ground4D(off-road feedforward 4D), PhysForge(physics-grounded 3D asset, 150K dataset)가 등장 — 평가뿐 아니라 representation/data substrate까지 4D paradigm이 한 주 만에 단단해진 신호. 우리 랩이 4D WM follow한다면 LoViF + iWorld-Bench 양축에서 우리 모델 위치 정립이 향후 6주 sprint 우선순위.",
            "papers": ["https://arxiv.org/abs/2605.05187", "https://arxiv.org/abs/2605.04527", "https://arxiv.org/abs/2605.04435", "https://arxiv.org/abs/2605.05163"]
        },
        {
            "title": "Diffusion alignment paradigm이 BT model 측 가정 깬 'self-referential' 메타로 이동 — Nash equilibrium · self-distillation · self-editing 동시 표면화",
            "claim": "Diff-NPO가 'BT model이 human preference 복잡성을 못 잡는다'는 진단으로 diffusion alignment를 game-theoretic Nash equilibrium으로 reframe — 'current policy가 자기와 play해 self-improvement'라는 self-referential alignment. 같은 batch에 D-OPSD(on-policy self-distillation for step-distilled diffusion) + ReflectDrive-2(RL-aligned self-editing for discrete diffusion driving) 동시 등장 — 'self-play / self-distillation / self-editing'이라는 self-referential alignment paradigm 3-layer가 한 batch에 누적. 어제 RoboAlign-R1(reward distillation), 그제 Latent Bridge(VLM call 절감)와 함께 보면 'alignment의 reward signal을 외부 모델에서 self loop로 옮기는' 메타가 한 주 더 단단해진 자리. T2I/diffusion 인프라 follow한다면 'self-X' 기법의 task별 효과 격차 측정이 즉시 audit 가치.",
            "papers": ["https://arxiv.org/abs/2605.04494", "https://arxiv.org/abs/2605.05204", "https://arxiv.org/abs/2605.04647"]
        }
    ],
    "research_topics": [
        {
            "title": "Latent Action Supervision Atlas — image-based vs action-based vs hybrid의 task별 SR Pareto",
            "claim": "From Pixels to Tokens가 'image-based latent action은 long-horizon에, action-based는 motor coord에' 강하다는 formulation-task correspondence를 처음 측정한 자리에서 다음 단계는 hybrid 측 양축 통합 효과 정량. {image-only, action-only, image+action joint, discrete-token VLM-direct} 4 paradigm × {LIBERO, RoboCasa, OGBench, Open-X-Embodiment} 4 bench × {short-horizon manip, long-horizon nav, dexterous, contact-rich} 4 task family로 'formulation × task family' SR atlas. 'discrete latent action token이 가장 효과적'이라는 paper 결론을 다른 task family에서 verify + hybrid가 image-only 대비 어디서 strict win인가 측정 — 향후 6주 VLA training 측 community standard 후보. 우리 랩이 VLA infra 굴린다면 즉시 sprint 가치."
        },
        {
            "title": "4D WM Eval Coverage Matrix — LoViF × iWorld × RobotWorldBench 3-bench 위에서 동일 모델 cross-eval",
            "claim": "한 주 만에 4D WM eval이 LoViF 2026(physics holistic) + iWorld-Bench(interaction unified action) + RobotWorldBench(robot reward alignment) 3축으로 정착한 자리에서 다음 단계는 'same model을 3 bench에 동시 evaluate해 score correlation 측정' — physics quality와 interaction ability와 reward alignment가 같은 axis인지 orthogonal인지 처음 정량. {OpenSora-X, Cosmos-2, Veo-3, MovieGen, Sora-3, plus open-source baseline 5} × {LoViF + iWorld + RobotWorldBench} 3-bench 행렬. 격차 패턴이 'large vs small' 또는 'closed vs open' 같은 known axis와 어떻게 align되는지 정량 — 'WM이 어디서 무엇을 잘하는가' 측 첫 통합 결과. 4D WM follow하는 랩이라면 6주 audit 우선."
        },
        {
            "title": "Self-Referential Diffusion Alignment의 task-family transfer — Nash · self-distill · self-edit의 task별 best-fit Pareto",
            "claim": "Diff-NPO(Nash equilibrium) + D-OPSD(on-policy self-distillation) + ReflectDrive-2(self-editing)가 한 batch에 3 layer self-referential alignment를 표면화한 자리에서 다음 단계는 'task family별 best-fit 측정'. {T2I (T2I-CompBench, GenEval), video gen (VBench), driving (CARLA closed-loop), manipulation (LIBERO), seg (DiCLIP-style)} 5 task family × {Nash-NPO, self-distill, self-edit, baseline DPO} 4 method matrix로 'self-referential 메타가 어디서 BT-model 측 가정을 strict win'하는가 정량. 격차 패턴이 'preference dimensionality' 또는 'reward signal noise level'과 align되는지 분석 — diffusion alignment 측 community standard 후보. T2I/T2V follow하는 랩이라면 6주 sprint 가치."
        }
    ],
    "retrospective": {
        "active": False,
        "note": "목요일 실행 — 회고는 월요일 실행에서만 활성화. 다음 회고는 2026-05-11(월) 예정."
    }
}

os.makedirs("insights", exist_ok=True)
with io.open(f"insights/{DATE}.json", "w", encoding="utf-8", newline="\n") as fout:
    json.dump(insights, fout, ensure_ascii=False, indent=2)
sys.stderr.write(f"wrote insights/{DATE}.json\n")

print(f"wrote trends/{DATE}.json, benchmarks/{DATE}.json, insights/{DATE}.json")
