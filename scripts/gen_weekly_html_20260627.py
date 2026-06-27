#!/usr/bin/env python3
"""Generate the 2026-06-27 weekly retrospective from parser-derived weekly_full.json."""
from __future__ import annotations

import html
import json
from pathlib import Path


DATE = "2026-06-27"
WEEK = "2026-W26"
WEEK_START = "2026-06-21"
WEEK_END = "2026-06-27"
SITE_URL = "https://gisbi-kim.github.io/arxiv-daily-summary"


def load_json(path: str):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def esc(value) -> str:
    return html.escape(str(value or ""), quote=False)


def paper_lookup(weekly_full: dict) -> dict[str, dict]:
    out = {}
    for bucket_name, bucket in weekly_full["buckets_full"].items():
        for p in bucket["papers"]:
            item = dict(p)
            item["bucket"] = bucket_name
            out[p["arxiv_id"]] = item
    return out


def make_paper(by_id: dict[str, dict], arxiv_id: str, short: str, phylogeny: dict, tags: list[str]) -> dict:
    p = dict(by_id.get(arxiv_id, {}))
    p.setdefault("arxiv_id", arxiv_id)
    p.setdefault("title", short)
    p.setdefault("bucket", "")
    p.setdefault("badge", "")
    p["short"] = short
    p["phylogeny"] = phylogeny
    p["importance_tags"] = tags
    return p


def phy(source: str, lineage: str, confidence: str = "High") -> dict:
    phylum, klass, order, genus = [x.strip() for x in lineage.split(">")]
    return {
        "source": source,
        "phylum": phylum,
        "class": klass,
        "order": order,
        "genus": genus,
        "confidence": confidence,
        "rationale": "weekly representative paper lineage assigned from the public robotics/CVML phylogeny style",
    }


def paper_url(p: dict) -> str:
    return f"https://arxiv.org/abs/{p['arxiv_id']}"


def phy_text(p: dict) -> str:
    ph = p["phylogeny"]
    return f"{ph['source']} · {ph['phylum']} > {ph['class']} > {ph['order']} > {ph['genus']}"


def phy_html(p: dict) -> str:
    ph = p["phylogeny"]
    lineage = " &gt; ".join(esc(ph[key]) for key in ["phylum", "class", "order", "genus"])
    return f"<span class='phy'>Phylogeny: <strong>{esc(ph['source'])}</strong> {lineage}</span>"


def paper_link(p: dict) -> str:
    return (
        f'<a href="{paper_url(p)}" target="_blank" rel="noopener">{esc(p["short"])}</a> '
        f"<span class='badge'>{esc(p.get('badge', ''))}</span><br>{phy_html(p)}"
    )


def paper_cell(papers: list[dict]) -> str:
    return "<br><br>".join(paper_link(p) for p in papers)


def bucket_line(snapshot: dict) -> str:
    labels = [
        ("3D", "3D/Scene"),
        ("RL", "Robot Learning"),
        ("AD", "Autonomous Driving"),
        ("FM", "Foundation Models"),
        ("Gen", "Generation"),
        ("Eff", "Efficiency/Systems"),
        ("Emb", "Embodied AI"),
        ("Safety", "Safety/Alignment"),
    ]
    return " · ".join(f"[{short}] {snapshot['buckets'][bucket]['total']}" for short, bucket in labels)


def tag_html(tags: list[str]) -> str:
    return " ".join(f"<span class='tag'>{esc(t)}</span>" for t in tags)


def build() -> None:
    weekly_full = load_json("out/weekly_full.json")
    snapshot = weekly_full["snapshot"]
    by_id = paper_lookup(weekly_full)

    lineages = {
        "vla": phy("ROBOTICS", "Robot Learning > Vision-Language-Action > Safety Evaluation > Execution Diagnosis"),
        "geometry": phy("ROBOTICS", "Perception and Mapping > State Estimation > SLAM and Odometry > Gaussian and LiDAR Maps"),
        "world": phy("ROBOTICS", "Simulation and World Models > Generative Simulation > Action-Conditioned Worlds > Trust Horizons"),
        "vlm": phy("CVML", "Foundation Models > Multimodal Reasoning > Grounded Reliability > Evidence and Uncertainty"),
        "autonomy": phy("ROBOTICS", "Autonomous Systems > Closed-Loop Planning > Scenario Evaluation > Risk and Recovery"),
        "systems": phy("CVML", "Efficient ML Systems > Token and Cache Efficiency > Adaptive Inference > Memory Compression"),
    }
    tags = {
        "vla": ["[평가축]", "[실사용전환]", "[경고신호]"],
        "geometry": ["[SLAM/Recon]", "[실사용전환]", "[평가축]"],
        "world": ["[방법전환]", "[평가축]", "[위험보류]"],
        "vlm": ["[근거검증]", "[경고신호]", "[표준후보]"],
        "autonomy": ["[closed-loop]", "[실사용전환]", "[평가축]"],
        "systems": ["[인프라]", "[실사용전환]", "[효율성]"],
    }

    def p(arxiv_id: str, key: str, short: str) -> dict:
        return make_paper(by_id, arxiv_id, short, lineages[key], tags[key])

    clusters = [
        {
            "cluster": "VLA는 성능 확장에서 실행 전 safety diagnosis와 physical feasibility 검증으로 이동",
            "papers": [
                p("2606.27079", "vla", "ForesightSafety-VLA"),
                p("2606.23686", "vla", "LIBERO-Safety"),
                p("2606.25800", "vla", "ROAD-VLA"),
                p("2606.23623", "vla", "dVLA-RL"),
                p("2606.27146", "vla", "PhysReflect-VLA"),
                p("2606.26443", "vla", "WatchAct"),
            ],
            "why": (
                "이번 주 Robot Learning은 160편으로 가장 큰 로봇 버킷이며, 중심 신호는 VLA가 단순 success rate를 넘는다는 점입니다. "
                "ForesightSafety-VLA와 LIBERO-Safety는 실패를 실행 전에 예측하고, ROAD-VLA와 PhysReflect-VLA는 online adaptation과 물리 feasibility를 "
                "정책 안으로 끌어옵니다. 따라서 VLA 평가는 더 큰 데이터셋이 아니라 어떤 failure family를 먼저 드러내는지로 재구성해야 합니다."
            ),
            "confidence": "High — VLA safety benchmark, online adaptation, physical reflection, behavior-grounded benchmark가 같은 주에 반복",
            "lab_action": (
                "LIBERO/RoboCasa/real-robot task에서 safety benchmark, online self-distillation, physical reflection을 독립 변수로 두고 "
                "unsafe action, failure warning lead time, object-generalization success를 비교한다."
            ),
        },
        {
            "cluster": "Geometry/SLAM은 Gaussian map 경쟁에서 자원제약 localization과 robot-usable map 평가로 이동",
            "papers": [
                p("2606.21258", "geometry", "Spectral GS-SLAM"),
                p("2606.20424", "geometry", "LIT-GS"),
                p("2606.21527", "geometry", "LOGOS"),
                p("2606.26010", "geometry", "FAR-LIO"),
                p("2606.25386", "geometry", "Commerge"),
                p("2606.24628", "geometry", "ArtiTwinSplat"),
            ],
            "why": (
                "이번 주 3D/Scene은 68편이고, SLAM이라는 이름이 붙은 논문과 Gaussian map 논문이 함께 두껍습니다. "
                "Spectral GS-SLAM, LIT-GS, LOGOS는 Gaussian representation을 map과 segmentation substrate로 쓰고, FAR-LIO와 Commerge는 "
                "고속·자원제약 localization을 요구합니다. 핵심은 photometric quality가 아니라 로봇이 실제 환경 변화와 통신 제약 안에서 쓸 수 있는 지도인지입니다."
            ),
            "confidence": "High — Gaussian SLAM, LiDAR-inertial mapping, map merging, interactable digital twin 신호가 충분",
            "lab_action": (
                "warehouse/tunnel/driving sequence에서 Gaussian map, LiDAR-inertial map, object-SLAM map을 비교하고 "
                "localization drift, update cost, communication budget, navigation success를 함께 평가한다."
            ),
        },
        {
            "cluster": "World model은 미래 프레임 생성에서 planning에 쓸 수 있는 trust horizon 검증으로 이동",
            "papers": [
                p("2606.24101", "world", "NavWM"),
                p("2606.26025", "world", "In-Context World Modeling"),
                p("2606.24946", "world", "Conformal Orbit-Valid Trust Horizons"),
                p("2606.24945", "world", "Certified Horizons for Latent World Models"),
                p("2606.22729", "world", "Temporal Logic Guidance"),
                p("2606.27123", "world", "Closed-Loop Traffic Scenario Generation"),
            ],
            "why": (
                "Generation은 124편으로 매우 크지만, 단순 생성 품질보다 로봇이 얼마나 오래 믿고 행동할 수 있는지가 핵심입니다. "
                "NavWM과 in-context world modeling은 planning으로 연결되고, conformal/certified horizon 논문은 언제까지 예측을 믿을 수 있는지 묻습니다. "
                "traffic scenario diffusion과 temporal-logic guidance는 그 신뢰 구간을 closed-loop 실패 조건 안에서 검증하라는 신호입니다."
            ),
            "confidence": "High — navigation world model, certified horizon, temporal logic, closed-loop traffic generation이 같은 trust-horizon 축으로 연결",
            "lab_action": (
                "navigation/driving rollout에서 forecast horizon, temporal-logic constraint, scenario diffusion seed를 바꾸고 "
                "unsafe action rate, recovery behavior, closed-loop success를 함께 비교한다."
            ),
        },
        {
            "cluster": "VLM 신뢰성은 hallucination rate에서 evidence grounding과 uncertainty routing 평가로 확장",
            "papers": [
                p("2606.27326", "vlm", "Hallucination in World Models"),
                p("2606.25760", "vlm", "Computer-Use Agent Uncertainty"),
                p("2606.27128", "vlm", "FlameVQA"),
                p("2606.24115", "vlm", "Endoscopy Hallucination Benchmark"),
                p("2606.24797", "vlm", "EG-VQA"),
                p("2606.26535", "vlm", "CRISP"),
                p("2606.26529", "vlm", "The Inattentional Gap"),
            ],
            "why": (
                "Foundation Models 75편과 Safety/Alignment 44편은 별도 버킷이지만 실제로는 같은 신뢰성 질문을 공유합니다. "
                "world-model hallucination, computer-use uncertainty, thermal VQA, endoscopy hallucination, verifiable temporal VQA, CRISP, "
                "Inattentional Gap은 정답 여부보다 어떤 근거를 봤고 어떤 task 조건에서 중요한 신호를 놓쳤는지 평가해야 한다고 말합니다."
            ),
            "confidence": "High — hallucination, GUI uncertainty, physical VQA, temporal evidence, task-conditioned omission이 반복됨",
            "lab_action": (
                "medical/UAV/GUI/3D spatial VQA에서 evidence span, routing entropy, task prompt, visual saliency를 조작하고 "
                "omitted critical signal, confidence shift, correction behavior를 함께 평가한다."
            ),
        },
        {
            "cluster": "Autonomy benchmark는 perception score에서 재현 가능한 closed-loop risk와 recovery 평가로 이동",
            "papers": [
                p("2606.20980", "autonomy", "Robusto-2"),
                p("2606.27123", "autonomy", "Traffic Scenario Diffusion"),
                p("2606.20336", "autonomy", "Priority-Ordered STL Driving"),
                p("2606.26922", "autonomy", "Driver-State World Modeling"),
                p("2606.25509", "autonomy", "ASSCG"),
                p("2606.19641", "autonomy", "Scaling Self-Play for Driving"),
                p("2606.19836", "autonomy", "World Engine"),
            ],
            "why": (
                "Autonomous Driving은 41편으로 전체 최대 버킷은 아니지만 평가 방향은 선명합니다. Robusto-2, traffic scenario diffusion, STL driving, "
                "driver-state world modeling, fast-slow LLM planning, self-play, World Engine은 모두 offline score보다 재현 가능한 위험 상황과 회복 행동을 봅니다. "
                "자율시스템 평가는 이제 near-miss와 rule violation을 closed-loop에서 다시 만드는 능력이 중심입니다."
            ),
            "confidence": "High — driving risk understanding, scenario generation, formal specification, self-play, post-training 신호가 같은 배포 평가축을 형성",
            "lab_action": (
                "CARLA/OpenSCENARIO에서 city OOD, driver-state change, STL priority violation, generated scenario seed를 stress condition으로 만들고 "
                "near-miss, recovery behavior, rule violation, closed-loop success를 비교한다."
            ),
        },
        {
            "cluster": "효율화는 latency 경쟁에서 task-critical memory와 bandwidth 보존성 평가로 이동",
            "papers": [
                p("2606.24286", "systems", "AVOC"),
                p("2606.24156", "systems", "Prior-Corrected Token Reduction"),
                p("2606.26398", "systems", "DinoLink"),
                p("2606.23105", "systems", "Compression and Retrieval"),
                p("2606.25700", "systems", "Memory-Efficient Policy Libraries"),
                p("2606.20755", "systems", "UNSEEN"),
            ],
            "why": (
                "Efficiency/Systems 51편은 단순 모델 축소보다 어떤 정보를 버리지 말아야 하는지를 묻습니다. AVOC와 token reduction은 긴 multimodal 입력을 줄이고, "
                "DinoLink와 cache reuse는 V2X/visual revisiting에서 bandwidth와 memory를 다룹니다. ProtoKV와 UNSEEN은 delayed query와 sparse estimation에서 "
                "task-critical evidence가 남아야 실제 배포가 가능하다는 신호입니다."
            ),
            "confidence": "Medium-High — token compression, V2X bandwidth, cache reuse, streaming memory, sparse navigation이 같은 배포 효율성 축으로 묶임",
            "lab_action": (
                "V2X/long-video/navigation benchmark에서 token budget, cache size, bandwidth, delayed query를 제한하고 "
                "obstacle recall, semantic delivery success, spatial reasoning error, downstream decision change를 비교한다."
            ),
        },
    ]

    top5 = [
        (clusters[0]["papers"][0], "VLA safety를 실행 전 진단 문제로 명시해 이번 주 로봇 정책 흐름을 가장 잘 대표합니다."),
        (clusters[1]["papers"][0], "3D Gaussian representation이 SLAM tracking과 degeneracy robustness로 들어온 대표 신호입니다."),
        (clusters[2]["papers"][2], "world model을 언제까지 믿을 수 있는지 보증하려는 방향을 가장 선명하게 보여줍니다."),
        (clusters[3]["papers"][0], "world-model hallucination을 예측 가능한 실패로 다뤄 VLM/world reliability cluster를 지탱합니다."),
        (clusters[4]["papers"][1], "closed-loop traffic scenario를 생성해 autonomy 평가를 offline score 밖으로 밀어냅니다."),
    ]

    next_actions = [
        {
            "title": "VLA safety grid",
            "body": "LIBERO-Safety, ForesightSafety-VLA, PhysReflect-VLA를 같은 task family에 올리고 unsafe action, failure-warning lead time, physical-feasibility violation을 비교한다.",
        },
        {
            "title": "Robot-usable Gaussian map test",
            "body": "GS-SLAM, LiDAR-inertial Gaussian map, object/digital-twin map을 localization drift, map update cost, dynamic-object failure 기준으로 비교한다.",
        },
        {
            "title": "World-model trust horizon benchmark",
            "body": "NavWM류 world model에서 forecast horizon과 temporal-logic constraint를 바꾸며 planning success와 unsafe action rate를 함께 평가한다.",
        },
        {
            "title": "Grounded VLM omission audit",
            "body": "medical/UAV/GUI VQA에서 모델이 볼 수 있는 safety-critical signal을 task prompt 조건 때문에 놓치는지 evidence span과 confidence shift로 평가한다.",
        },
    ]

    payload = {
        "date": DATE,
        "iso_week": WEEK,
        "week_start": WEEK_START,
        "week_end": WEEK_END,
        "source_mode": "pastweek",
        "weekly_thesis": (
            "이번 주의 핵심은 VLA, Gaussian SLAM, world model, VLM reliability, autonomy benchmark가 모두 "
            "더 큰 모델보다 실패를 재현하고 실행 전에 검증하는 평가 설계로 이동했다는 점입니다."
        ),
        "totals": snapshot["totals"],
        "buckets": snapshot["buckets"],
        "clusters": [
            {
                "cluster": c["cluster"],
                "representative_papers": [
                    {
                        "title": p["title"],
                        "arxiv": paper_url(p),
                        "short": p["short"],
                        "importance_tags": p["importance_tags"],
                        "phylogeny": p["phylogeny"],
                    }
                    for p in c["papers"]
                ],
                "why_it_matters": c["why"],
                "confidence": c["confidence"],
                "lab_action": c["lab_action"],
            }
            for c in clusters
        ],
        "top5": [{"paper": p["title"], "arxiv": paper_url(p), "why": why, "phylogeny": phy_text(p)} for p, why in top5],
        "next_week_actions": next_actions,
    }

    Path("weekly").mkdir(exist_ok=True)
    Path("weekly", f"{WEEK}.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    cluster_rows = []
    for c in clusters:
        cluster_rows.append(
            "<tr>"
            f"<td><strong>{esc(c['cluster'])}</strong><br>{tag_html(c['papers'][0]['importance_tags'])}</td>"
            f"<td>{paper_cell(c['papers'])}</td>"
            f"<td>{esc(c['why'])}</td>"
            f"<td>{esc(c['confidence'])}</td>"
            f"<td>{esc(c['lab_action'])}</td>"
            "</tr>"
        )

    top5_html = "".join(
        f"<li><strong>{paper_link(p)}</strong><p>{esc(why)}</p></li>"
        for p, why in top5
    )
    actions_html = "".join(
        f"<div class='card'><h3>{esc(a['title'])}</h3><p>{esc(a['body'])}</p></div>"
        for a in next_actions
    )

    css = """
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:#f6f8fa;color:#24292f;margin:0;padding:28px 12px;line-height:1.62}
.container{max-width:1040px;margin:0 auto;background:#fff;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.06),0 1px 2px rgba(0,0,0,.04);padding:40px 48px}
h1{font-size:28px;margin:0 0 6px;color:#0d1117}h2{font-size:21px;margin:40px 0 14px;padding-bottom:8px;border-bottom:2px solid #e5e7eb}h3{font-size:16px;margin:10px 0 4px}
a{color:#0969da;text-decoration:none}a:hover{text-decoration:underline}.home{display:inline-block;padding:6px 14px;font-size:13px;color:#0969da;background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;margin:0 0 18px}
.meta{font-size:13px;color:#3b434d;padding:14px 18px;background:#f6f8fa;border-left:3px solid #7c3aed;border-radius:6px;margin:14px 0 22px}.thesis{background:#111827;color:#f8fafc;border-radius:10px;padding:18px 22px;margin:16px 0 28px;font-size:16px}.thesis strong{color:#fde68a}
.cluster-table{width:100%;table-layout:fixed;border-collapse:collapse;font-size:13px;margin:12px 0 18px}.cluster-table th,.cluster-table td{border:1px solid #d0d7de;padding:9px;vertical-align:top;overflow-wrap:anywhere;word-break:break-word}.cluster-table th{background:#f6f8fa;color:#0d1117}
.takeaway{margin:-4px 0 24px;padding:12px 16px;background:#fff8e1;border-left:3px solid #f59e0b;border-radius:6px;color:#3b434d;font-size:14px}.bucket-line{font-family:ui-monospace,SFMono-Regular,Consolas,Menlo,monospace;background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;padding:10px 14px;font-size:13px;white-space:pre-wrap}
.tag{display:inline-block;font-family:ui-monospace,SFMono-Regular,Consolas,Menlo,monospace;font-size:12px;color:#7c2d12;background:#fff7ed;border:1px solid #fed7aa;border-radius:6px;padding:1px 7px;margin:2px 3px 2px 0}.badge{display:inline-block;font-size:11px;font-weight:600;padding:1px 7px;border-radius:10px;margin-left:5px;background:#f3f4f6;color:#374151;border:1px solid #d1d5db}.phy{display:block;color:#475569;font-size:12.5px;margin-top:2px}
.card{background:#fafbfc;border:1px solid #e5e7eb;border-radius:8px;padding:14px 18px;margin:12px 0}ol li{margin:12px 0}footer{margin-top:40px;padding-top:16px;border-top:1px solid #eaeef2;font-size:12px;color:#656d76;text-align:center}
@media(max-width:760px){body{padding:16px 8px}.container{padding:24px 20px}.cluster-table{font-size:12.5px}}
""".strip()

    html_doc = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>arXiv Weekly Briefing - {WEEK}</title>
<style>{css}</style>
</head>
<body><main class="container">
<a class="home" href="../index.html">← Home</a>
<h1>arXiv Weekly Briefing — {WEEK}</h1>
<div class="meta">
<div><strong>소스:</strong> arXiv cs.CV/pastweek + cs.RO/pastweek · source_mode=pastweek</div>
<div><strong>주간 시야:</strong> {WEEK_START} ~ {WEEK_END}</div>
<div><strong>주간 스캔:</strong> {snapshot['totals']['total_scanned']} scanned · {snapshot['totals']['selected']} ROI selected</div>
</div>
<section class="thesis"><strong>주간 결론:</strong> {esc(payload['weekly_thesis'])}</section>
<h2>주간 클러스터 표</h2>
<table class="cluster-table"><thead><tr><th>Cluster</th><th>대표 논문</th><th>왜 중요?</th><th>Confidence</th><th>Lab action</th></tr></thead><tbody>
{''.join(cluster_rows)}
</tbody></table>
<p class="takeaway"><strong>이번 주의 핵심:</strong> 더 큰 모델 경쟁이 아니라, VLA·SLAM·world model·VLM·autonomy를 실제 실패 조건에서 어떻게 분리해 검증할 것인가다.</p>
<h2>주간 동향</h2>
<p>이번 주 pastweek snapshot은 {snapshot['totals']['total_scanned']}편을 스캔했고 ROI {snapshot['totals']['selected']}편을 선별했습니다. {esc(bucket_line(snapshot))}. Robot Learning과 Generation이 가장 두껍지만, 주간 thesis는 양보다 평가축입니다. VLA safety, Gaussian/LiDAR SLAM, world-model trust horizon, grounded VLM reliability, closed-loop autonomy가 모두 실행 전에 실패를 드러내는 실험 설계로 모입니다.</p>
<div class="bucket-line">{esc(bucket_line(snapshot))}</div>
<h2>주간 Top 5</h2>
<ol>{top5_html}</ol>
<h2>다음 주 실행안</h2>
{actions_html}
<footer>Generated from repo parser outputs. WebFetch was not used for arXiv source data. Link: {SITE_URL}/posts/{DATE}-weekly.html</footer>
</main></body></html>
"""
    Path("posts").mkdir(exist_ok=True)
    Path("posts", f"{DATE}-weekly.html").write_text(html_doc, encoding="utf-8", newline="\n")
    print(f"wrote weekly/{WEEK}.json and posts/{DATE}-weekly.html")


def tag_html(tags: list[str]) -> str:
    return " ".join(f"<span class='tag'>{esc(t)}</span>" for t in tags)


if __name__ == "__main__":
    build()
