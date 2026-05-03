#!/usr/bin/env python3
"""Generate trends / benchmarks / insights JSON snapshots for 2026-05-03 (Sunday)."""
import io, json, os, sys
from collections import Counter

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

sys.path.insert(0, 'scripts')
from classify import BUCKETS

DATE = "2026-05-03"

# -- load classified --
with io.open("out/classified.json", "r", encoding="utf-8") as f:
    cl = json.load(f)

# -- load pastweek for keyword snapshot --
cv_pw = json.load(io.open("out/cv_pastweek.json", encoding="utf-8"))
ro_pw = json.load(io.open("out/ro_pastweek.json", encoding="utf-8"))

# Pastweek bucket totals (mirror classify.py logic)
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

# Pastweek keywords (count over title+abstract; abstract is empty for pastweek so title dominates)
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

# ---- trends/2026-05-03.json ----
trends = {
    "date": DATE,
    "totals": {
        "selected": cl["selected"],
        "total_scanned": cl["total"],
        "note": "Sunday — same Friday May 1 batch (arxiv has no weekend listings); pastweek window rolled to 2026-04-27 ~ 2026-05-03."
    },
    "buckets": {},
    "buckets_pastweek": {},
    "vs_7d_prior": {
        "baseline_date": "2026-04-26",
        "baseline_note": "Same 1-day /new unit on previous Sunday (mirrored arxiv batch from previous week's Friday).",
        "today_buckets_delta_pct": {
            "Autonomous Driving": "+57%",
            "3D/Scene": "+54%",
            "Embodied AI": "+50%",
            "Robot Learning": "+13%",
            "Efficiency/Systems": "+0%",
            "Foundation Models": "-16%",
            "Generation": "-25%",
            "Safety/Alignment": "-48%"
        }
    },
    "hottest": [
        {
            "topic": "VLA reasoning paradigm shift — latent CoT + RL",
            "evidence": ["2604.28192", "2604.27792", "2604.27472"],
            "note": "LaST-R1 + MotuBrain + PRTS 셋이 다른 axis로 같은 paradigm 정조준; 일요일까지도 후속 ablation 결 미등장"
        },
        {
            "topic": "Sparse-View 3DGS 4-fold surge",
            "evidence": ["2604.27106", "2604.27422", "2604.27552", "2604.28193"],
            "note": "한 날에 4편이 모두 다른 'sparse' 정의로 정조준; 통합 robustness suite 자리가 비어있음"
        },
        {
            "topic": "Driving WM unified understanding+generation",
            "evidence": ["2604.28196"],
            "note": "HERMES++가 'generation-only'에서 'understanding+generation 통합'으로 paradigm shift 첫 분명한 결"
        },
        {
            "topic": "LLM-controlled robot architectural threat modeling",
            "evidence": ["2604.27267"],
            "note": "From Prompt to Physical Actuation — STRIDE-per-interaction을 LLM-enabled robot에 처음 적용한 통합 lens"
        }
    ],
    "cooling": [
        {
            "topic": "Safety/Alignment burst 종료",
            "evidence": ["2604.27343", "2604.27357", "2604.27654"],
            "note": "27→14편 -48% cooling; 안에서도 진짜 'AI safety' 결은 1~2편, 나머지는 medical/forensics 키워드 잡음"
        },
        {
            "topic": "Foundation Models 소폭 -16%",
            "evidence": [],
            "note": "지난주 양강 중 한 축이 cooling; deployment 측 결로 무게중심 이동 신호"
        }
    ],
    "buckets_summary_note": "3D/Scene 20편 단독 1위(7일 전 13→오늘 20), RL 17편(15→17), FM 16편, Generation 15편, Safety 14편(-48%), AD 11편(+57%), Eff 11편, Embodied 3편. 'deployment-heavy 3축(3D+RL+AD)' 무게중심 이동.",
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
for bname in ["3D/Scene","Robot Learning","Autonomous Driving","Foundation Models","Generation","Efficiency/Systems","Embodied AI","Safety/Alignment"]:
    trends["buckets_pastweek"][bname] = {
        "total": bcv.get(bname, 0) + bro.get(bname, 0),
        "cv": bcv.get(bname, 0),
        "ro": bro.get(bname, 0)
    }

os.makedirs("trends", exist_ok=True)
with io.open(f"trends/{DATE}.json", "w", encoding="utf-8", newline="\n") as fout:
    json.dump(trends, fout, ensure_ascii=False, indent=2)
sys.stderr.write(f"wrote trends/{DATE}.json\n")

# ---- benchmarks/2026-05-03.json ----
benchmarks = {
    "date": DATE,
    "results": [
        {
            "benchmark": "LIBERO",
            "metric": "average success rate",
            "value": 99.8,
            "value_str": "99.8%",
            "paper": "https://arxiv.org/abs/2604.28192",
            "paper_title": "LaST-R1: Reinforcing Action via Adaptive Physical Latent Reasoning for VLA Models",
            "note": "Average across LIBERO suite — task-by-task breakdown unverified; 'LIBERO solved' claim pending CALVIN/RoboCasa cross-check"
        },
        {
            "benchmark": "real-world manipulation (4 task)",
            "metric": "improvement vs warm-up",
            "value": 44.0,
            "value_str": "+44%",
            "paper": "https://arxiv.org/abs/2604.28192",
            "paper_title": "LaST-R1",
            "note": "Single-arm + dual-arm; dual-arm collaboration depth from abstract unclear"
        },
        {
            "benchmark": "SAM3D-style sparse reconstruction",
            "metric": "geometric quality",
            "value": 30.1,
            "value_str": "+30.1%",
            "paper": "https://arxiv.org/abs/2604.27106",
            "paper_title": "RecGen: Reconstruction by Generation",
            "note": "80% less training mesh; pose estimation +33.9% same paper"
        },
        {
            "benchmark": "real-time VLA inference",
            "metric": "speedup vs UniDiffuser baseline",
            "value": 50.0,
            "value_str": "50x",
            "paper": "https://arxiv.org/abs/2604.27792",
            "paper_title": "MotuBrain",
            "note": "Baseline definition (naive vs accelerated diffusion) needs verification — see risk filter"
        }
    ],
    "proposed_benchmarks": [],
    "note": "Same SOTA reports as Friday May 1 batch (Sunday's pastweek view unchanged); ScanNet++/Mip-NeRF 360 측 새 SOTA 보고는 안 잡힘."
}
os.makedirs("benchmarks", exist_ok=True)
with io.open(f"benchmarks/{DATE}.json", "w", encoding="utf-8", newline="\n") as fout:
    json.dump(benchmarks, fout, ensure_ascii=False, indent=2)
sys.stderr.write(f"wrote benchmarks/{DATE}.json\n")

# ---- insights/2026-05-03.json ----
insights = {
    "date": DATE,
    "insights": [
        {
            "title": "VLA paradigm shift: latent CoT + RL persists after weekend retrospect",
            "claim": "LaST-R1·MotuBrain·PRTS 셋이 같은 paradigm을 다른 axis로 정조준했고, 일요일까지도 직접 반박/우회 결이 안 등장 — community가 reading+digestion 시간에 들어간 모양새. 우리 랩이 latent CoT 비교 실험을 빠르게 굴리면 first-follower 자리 비어있음.",
            "papers": ["https://arxiv.org/abs/2604.28192", "https://arxiv.org/abs/2604.27792", "https://arxiv.org/abs/2604.27472"]
        },
        {
            "title": "Safety -48% cooling: 키워드 surge vs architecture-level 진짜 safety 분리",
            "claim": "Safety/Alignment 27→14편으로 cool했지만, 안에서 진짜 substantive 결은 architecture-level threat modeling 1~2편(Prompt-to-Actuation·SASI·OmniRobotHome). 나머지는 medical/forensics 잡음. 우리 랩이 safety follow할 때 키워드 surge 추적이 아니라 STRIDE/threat-model 측 결만 따로 추출하는 별도 필터 필요.",
            "papers": ["https://arxiv.org/abs/2604.27267", "https://arxiv.org/abs/2604.27508", "https://arxiv.org/abs/2604.28197"]
        },
        {
            "title": "deployment-heavy 3축(3D+AD+RL) surge가 일요일에도 변하지 않음",
            "claim": "3D/Scene +54% · AD +57% · RL +13% 3축 surge가 한 주 burst가 아니라 community 무게중심의 진짜 이동. 'physical world deployment'라는 한 narrative 위에서 일관되게 누적. 우리 랩이 perception-only 측에 무게가 있다면 이번주 안에 deployment 측 paper 1편의 audit 시급.",
            "papers": ["https://arxiv.org/abs/2604.28111", "https://arxiv.org/abs/2604.28196", "https://arxiv.org/abs/2604.28192"]
        }
    ],
    "research_topics": [
        {
            "title": "VLA Reasoning Atlas — 4 paradigm × LIBERO/CALVIN/RoboCasa",
            "claim": "linguistic CoT vs latent CoT vs continuous latent vs no reasoning 4 paradigm × 3 표준 벤치 atlas. 일요일까지 후속 ablation 결 미등장 자리라 first-mover timing이 가장 좋음. LaST-R1 99.8% LIBERO ceiling이 진짜 ceiling인지 paradigm bias인지 atlas에서 결정."
        },
        {
            "title": "Sparse-View 3DGS Robustness Suite — 4 axis 통합 벤치",
            "claim": "view 수 / illumination / data quantity / domain 4 axis × ScanNet++/Mip-NeRF 360 통합 robustness suite. 4편이 다 다른 'sparse' 정의로 정조준한 자리에서 통합 비교가 비어있음. 6주 안에 인용 모일 자리."
        },
        {
            "title": "LLM-Robot Threat Audit Framework — STRIDE × DFD case study",
            "claim": "Prompt-to-Actuation의 framework를 우리 랩 LLM-controlled robot 시스템에 적용한 case study. 'physical world consequence' 측 정량 평가 framework 동시 필요. 향후 1년 robotics safety 첫 표준 가능성."
        }
    ]
}
os.makedirs("insights", exist_ok=True)
with io.open(f"insights/{DATE}.json", "w", encoding="utf-8", newline="\n") as fout:
    json.dump(insights, fout, ensure_ascii=False, indent=2)
sys.stderr.write(f"wrote insights/{DATE}.json\n")
