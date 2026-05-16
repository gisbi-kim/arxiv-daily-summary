#!/usr/bin/env python3
"""Generate the 2026-05-16 weekly retrospective from parser-derived data."""
from __future__ import annotations

import html
import json
from pathlib import Path


DATE = "2026-05-16"
WEEK = "2026-W20"
WEEK_START = "2026-05-10"
WEEK_END = "2026-05-16"
SITE_URL = "https://gisbi-kim.github.io/arxiv-daily-summary"


def load_json(path: str):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def esc(value) -> str:
    return html.escape(str(value), quote=False)


def link(paper: dict, short: str | None = None) -> str:
    title = short or paper["title"]
    return (
        f'<a href="https://arxiv.org/abs/{paper["arxiv_id"]}" '
        f'target="_blank" rel="noopener">{esc(title)}</a>'
    )


def paper_lookup(weekly_full: dict) -> dict[str, dict]:
    out = {}
    for bucket in weekly_full["buckets_full"].values():
        for p in bucket["papers"]:
            out[p["arxiv_id"]] = p
    return out


def make_paper(by_id: dict[str, dict], arxiv_id: str, title: str | None = None) -> dict:
    p = dict(by_id.get(arxiv_id, {}))
    p.setdefault("arxiv_id", arxiv_id)
    p.setdefault("title", title or arxiv_id)
    p.setdefault("bucket", "")
    p.setdefault("badge", "")
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


def phy_html(item: dict) -> str:
    ph = item["phylogeny"]
    lineage = f'{ph["phylum"]} > {ph["class"]} > {ph["order"]} > {ph["genus"]}'
    return (
        f'<div class="phy">Phylogeny: <strong>{ph["source"]}</strong> '
        f'{lineage} <span>{ph["confidence"]}</span></div>'
    )


def paper_cell(papers: list[dict]) -> str:
    rows = []
    for p in papers:
        rows.append(
            f'{link(p, p.get("short") or p["title"])}'
            f'{phy_html(p)}'
        )
    return "<br>".join(rows)


def bucket_line(snapshot: dict) -> str:
    order = [
        ("3D", "3D/Scene"),
        ("RL", "Robot Learning"),
        ("AD", "Autonomous Driving"),
        ("FM", "Foundation Models"),
        ("Gen", "Generation"),
        ("Eff", "Efficiency/Systems"),
        ("Emb", "Embodied AI"),
        ("Safety", "Safety/Alignment"),
    ]
    return " · ".join(f"[{short}] {snapshot['buckets'][name]['total']}" for short, name in order)


def build():
    weekly_full = load_json("out/weekly_full.json")
    snapshot = weekly_full["snapshot"]
    by_id = paper_lookup(weekly_full)

    lineages = {
        "geometry": phy("ROBOTICS", "Robot Perception > Mapping and Reconstruction > Neural and Gaussian Maps > Relocalizable 3D Scene Geometry"),
        "vla": phy("ROBOTICS", "Embodied Intelligence > Vision-Language-Action Models > Policy Structure > Latent Action and Runtime Execution"),
        "world": phy("CVML", "Generative Modeling > Video and World Models > Controllable Generation > Geometry-Aware Interactive Video"),
        "driving": phy("ROBOTICS", "Autonomous Driving > Closed-Loop Planning > Value and Policy Evaluation > Scenario-Level Driving Decisions"),
        "trust": phy("CVML", "Trustworthy ML > Robustness and Alignment > Hallucination and Verification > Deployment Reliability"),
        "systems": phy("CVML", "Efficient ML Systems > Token and Cache Efficiency > Adaptive Inference > Video and Multimodal Acceleration"),
    }

    def p(arxiv_id: str, key: str, short: str | None = None) -> dict:
        item = make_paper(by_id, arxiv_id)
        item["short"] = short or item["title"].split(":")[0]
        item["phylogeny"] = lineages[key]
        item["importance_tags"] = {
            "geometry": ["[방법전환]", "[실사용전환]", "[해부분석]"],
            "vla": ["[방법전환]", "[해부분석]", "[실사용전환]"],
            "world": ["[평가축]", "[방법전환]", "[표준후보]"],
            "driving": ["[평가축]", "[실사용전환]", "[위험보류]"],
            "trust": ["[경고신호]", "[평가축]", "[해부분석]"],
            "systems": ["[실사용전환]", "[인프라]", "[방법전환]"],
        }[key]
        return item

    clusters = [
        {
            "cluster": "SLAM/recon은 3DGS, relocalization, LiDAR world model 안으로 재배치",
            "papers": [
                p("2605.14135", "geometry", "PanoPlane"),
                p("2605.10760", "geometry", "MAGS-SLAM"),
                p("2605.07741", "geometry", "Hierarchical 3D Global Relocalization"),
                p("2605.07326", "geometry", "GEM"),
            ],
            "why": "이번 주 3D/Scene은 단순히 장면을 예쁘게 복원하는 묶음이 아닙니다. PanoPlane은 sparse-view indoor 3DGS를, MAGS-SLAM은 multi-agent Gaussian Splatting SLAM을, relocalization 논문과 GEM은 LiDAR 기반 위치 추정과 world model을 다룹니다. 즉 classic SLAM의 pose, map, correspondence 문제가 3DGS 지도, relocalization descriptor, LiDAR world model이라는 이름으로 다시 나타난 주입니다.",
            "confidence": "High — 3D/Scene 77편 중 geometry/SLAM/recon 신호가 여러 하위군으로 반복",
            "lab_action": "3DGS map, LiDAR descriptor map, feed-forward geometry map을 같은 relocalization split에서 성공률, update cost, dynamic-object failure로 비교",
        },
        {
            "cluster": "VLA는 큰 policy 하나보다 내부 역할과 실행 지연을 나누는 쪽으로 이동",
            "papers": [
                p("2605.14950", "vla", "Evo-Depth"),
                p("2605.13778", "vla", "Realtime-VLA FLASH"),
                p("2605.14712", "vla", "IntentVLA"),
                p("2605.13403", "vla", "RotVLA"),
            ],
            "why": "Robot Learning 103편 안에서 VLA 계열은 더 큰 모델 하나를 밀어붙이는 흐름만 보이지 않습니다. depth-enhanced VLA, speculative inference, short-horizon intent, rotational latent action처럼 perception, inference latency, intent, action representation을 따로 떼어 보는 논문이 같이 나왔습니다. 그래서 다음 비교는 모델 크기가 아니라 어떤 내부 역할 분리가 어떤 task family에서 실제로 도움이 되는지입니다.",
            "confidence": "High — CV/RO cross-list VLA 논문이 같은 주에 여럿 등장",
            "lab_action": "LIBERO/RoboCasa에서 depth, intent, rotational latent action, speculative inference를 같은 task family로 ablation",
        },
        {
            "cluster": "Video/world model은 샘플 품질보다 조종 가능성과 물리 일관성을 묻기 시작",
            "papers": [
                p("2605.15199", "world", "EntityBench"),
                p("2605.15182", "world", "Warp-as-History"),
                p("2605.15178", "world", "SANA-WM"),
                p("2605.15185", "world", "Geometric-Consistency VWM Eval"),
            ],
            "why": "Generation이 160편으로 가장 컸지만, 핵심은 양이 아니라 평가 질문의 변화입니다. long-range multi-shot consistency, camera-controlled video, minute-scale world model, geometric consistency 평가가 같이 나오면서 보기 좋은 영상보다 원하는 시점과 움직임을 안정적으로 만들고 물리적으로 말이 되는지를 묻는 쪽으로 이동했습니다.",
            "confidence": "High — generation 최대 버킷 안에서 controllability와 world-model 평가 논문이 동시에 관측",
            "lab_action": "camera path error, entity consistency, geometry violation, latency를 분리한 video/world-model evaluation grid 작성",
        },
        {
            "cluster": "자율주행은 perception 점수보다 closed-loop 가치와 직접 제어를 검증",
            "papers": [
                p("2605.15120", "driving", "CLOVER"),
                p("2605.14832", "driving", "Direct Control with Flow Matching"),
                p("2605.14201", "driving", "MAPLE"),
                p("2605.10564", "driving", "DeepSight"),
            ],
            "why": "Autonomous Driving은 38편으로 최대 버킷은 아니지만, closed-loop value estimation, direct control policy, latent multi-agent play, long-horizon world modeling이 같이 나온 점이 중요합니다. lane이나 BEV 점수만 따로 올리는 문제보다 실제 주행 루프에서 어떤 판단이 안전하고 쓸 만한지 확인하려는 주간 흐름입니다.",
            "confidence": "High — planning, policy, world model, value estimation이 같은 closed-loop 축으로 연결",
            "lab_action": "nuPlan/CARLA에서 route change, perception corruption, high-level instruction failure를 넣은 closed-loop stress test 구성",
        },
        {
            "cluster": "VLM 신뢰성은 정답률보다 기억, 환각, 근거 검증의 경계로 이동",
            "papers": [
                p("2605.14906", "trust", "MemLens"),
                p("2605.14966", "trust", "MHSA"),
                p("2605.12571", "trust", "VideoSEAL"),
                p("2605.13813", "trust", "JANUS"),
            ],
            "why": "Foundation Models 78편과 Safety/Alignment 52편이 따로 보이지만 실제로는 같은 문제를 보고 있습니다. 장기 기억, hallucination 완화, long-video evidence misalignment, distribution shift triage가 같이 나오면서 모델이 맞히는지보다 어떤 근거를 놓치고 언제 자신 있게 틀리는지를 기록하는 방향으로 움직였습니다.",
            "confidence": "High — memory, hallucination, evidence, distribution shift가 서로 다른 응용에서 반복",
            "lab_action": "medical VQA와 long-video QA에 counterfactual perturbation, evidence localization, confidence calibration failure를 같은 dashboard로 기록",
        },
        {
            "cluster": "효율화는 작은 모델보다 token, cache, sparse attention 제어로 구체화",
            "papers": [
                p("2605.14877", "systems", "HeatKV"),
                p("2605.14513", "systems", "HASTE"),
                p("2605.14191", "systems", "CoReDiT"),
                p("2605.14278", "systems", "KVPO"),
            ],
            "why": "Efficiency/Systems 67편은 파라미터를 줄이는 이야기에 머물지 않습니다. KV-cache compression, adaptive sparse attention, token pruning, KV semantic exploration처럼 실제 추론 경로에서 무엇을 버리고 남길지를 다룹니다. 즉 배포 가능한 multimodal/video model을 만들 때 latency와 품질 손실을 같은 표에서 봐야 한다는 신호입니다.",
            "confidence": "High — video diffusion과 multimodal autoregressive inference 모두에서 같은 비용 문제가 반복",
            "lab_action": "video diffusion, VLM, tracking에서 token budget, cache size, latency, accuracy drop을 한 Pareto curve로 비교",
        },
    ]

    top5 = [
        (clusters[0]["papers"][1], "SLAM과 3DGS가 분리된 주제가 아니라 같은 map representation 문제로 붙기 시작했다는 점을 가장 선명하게 보여줍니다."),
        (clusters[1]["papers"][1], "VLA를 실제 로봇 루프에 넣을 때 inference latency가 병목이 된다는 문제를 정면으로 다룹니다."),
        (clusters[2]["papers"][2], "world model을 minute-scale로 밀어 올리려는 시도라서 generation과 robot simulation 사이의 접점이 큽니다."),
        (clusters[3]["papers"][0], "end-to-end driving planning을 closed-loop value estimation과 ranking 문제로 다시 묶는 논문입니다."),
        (clusters[4]["papers"][0], "multimodal long-term memory가 VLM 신뢰성의 핵심 병목으로 올라왔다는 신호입니다."),
    ]

    themes = [
        {
            "title": "Geometry는 SLAM 제목 밖으로 흩어졌지만, 지도 표현 문제는 더 커졌습니다",
            "summary": "3D/Scene 77편 안에서 Gaussian Splatting, LiDAR world model, relocalization, odometry가 따로 나온 것처럼 보이지만, 실제 질문은 같습니다. 로봇이나 주행 시스템이 쓸 수 있는 지도 표현을 어떻게 만들고, 어떻게 갱신하며, 실패 조건을 어떻게 재는지가 이번 주 3D 축의 핵심입니다.",
            "confidence": "High",
        },
        {
            "title": "VLA는 모델 크기보다 실행 구조 경쟁으로 넘어갑니다",
            "summary": "Evo-Depth, Realtime-VLA FLASH, IntentVLA, RotVLA가 보여준 건 VLA가 하나의 거대한 policy로는 설명과 배포가 어렵다는 점입니다. 다음 주에는 latent action, intent, depth, speculative inference를 같은 benchmark에서 나란히 비교하는 논문이 더 중요해질 가능성이 큽니다.",
            "confidence": "High",
        },
        {
            "title": "Generation과 reliability는 분리된 트랙이 아니라 배포 전 조건이 됩니다",
            "summary": "Generation은 160편으로 가장 컸고, reliability와 efficiency도 각각 52편, 67편으로 두껍습니다. 이제 좋은 샘플을 만드는 것만으로는 부족하고, 조종 가능성, latency, memory, evidence alignment가 같이 들어와야 실제 도구로 볼 수 있습니다.",
            "confidence": "High",
        },
    ]

    prediction_review = [
        {
            "title": "VLA structure ablation이 3편 이상 이어진다",
            "label": "✅",
            "reason": "Evo-Depth, Realtime-VLA FLASH, IntentVLA, RotVLA, Guide-Think-Act가 모두 VLA 내부 역할이나 실행 구조를 건드렸습니다.",
        },
        {
            "title": "controllable video generation 평가가 camera path fidelity로 분리된다",
            "label": "✅",
            "reason": "Warp-as-History, Geometric-Consistency VWM Eval, EntityBench가 long-range consistency와 camera/geometry control을 분리해서 다뤘습니다.",
        },
        {
            "title": "reliability-aware routing과 medical/3D calibration이 같은 주 안에서 만난다",
            "label": "◐",
            "reason": "reliability 흐름은 강했지만 medical, long-video, VLM memory 쪽이 더 두꺼웠고 3D calibration은 독립 흐름으로는 상대적으로 약했습니다.",
        },
    ]

    predictions = [
        {
            "title": "3DGS map과 relocalization을 직접 비교하는 논문이 늘어날 것",
            "claim": "SLAM이라는 제목은 적어도, 3DGS map, LiDAR descriptor, feed-forward geometry를 같은 localization benchmark에서 비교하는 논문이 더 나올 가능성이 큽니다.",
            "hit_condition": "다음 주 /new 또는 pastweek에서 3DGS map + localization/relocalization/odometry를 함께 다루는 논문이 2편 이상 나오면 적중입니다.",
            "miss_condition": "3DGS가 rendering/editing 품질 쪽으로만 남고 robot/localization 연결이 사라지면 빗나감입니다.",
        },
        {
            "title": "VLA latency와 내부 표현 ablation이 같은 표로 묶일 것",
            "claim": "Realtime-VLA FLASH가 보여준 병목 때문에 VLA 논문이 success rate만이 아니라 latency, chunk length, action representation을 같이 보고할 가능성이 큽니다.",
            "hit_condition": "VLA 논문 중 latency 또는 runtime inference와 action/intent representation ablation을 같이 둔 논문이 나오면 적중입니다.",
            "miss_condition": "계속 benchmark success만 보고하고 runtime 분석이 빠지면 빗나감입니다.",
        },
        {
            "title": "world model 평가는 geometry consistency와 action success를 같이 물을 것",
            "claim": "SANA-WM, EntityBench, Geometric-Consistency VWM Eval이 같은 주에 나온 만큼, 다음 비교는 샘플 품질보다 geometry violation과 downstream action usefulness로 옮겨갈 가능성이 큽니다.",
            "hit_condition": "video/world-model 논문이 geometry consistency, camera path error, action success 중 2개 이상을 함께 평가하면 적중입니다.",
            "miss_condition": "FVD나 visual preference 중심 평가만 반복되면 빗나감입니다.",
        },
    ]

    next_actions = [
        {
            "title": "Geometry map representation board",
            "action": "MAGS-SLAM, PanoPlane, relocalization, LiDAR world model을 같은 표에 놓고 map update cost와 localization failure를 정리",
            "expected_output": "1-page comparison table with map type, update path, relocalization metric, dynamic-scene failure",
        },
        {
            "title": "VLA runtime ablation table",
            "action": "Realtime-VLA FLASH, IntentVLA, RotVLA, Evo-Depth의 latency/action-representation 차이를 LIBERO/RoboCasa 기준으로 정리",
            "expected_output": "ablation matrix: representation, latency, task family, reported failure mode",
        },
        {
            "title": "World model evaluation grid",
            "action": "SANA-WM, EntityBench, Warp-as-History, Geometric-Consistency VWM Eval의 평가축을 camera, geometry, entity, latency로 분해",
            "expected_output": "metric grid for choosing follow-up papers and reproducible benchmarks",
        },
    ]

    weekly_json = {
        "date": DATE,
        "iso_week": WEEK,
        "week_start": WEEK_START,
        "week_end": WEEK_END,
        "weekly_thesis": "이번 주는 VLA와 world model이 커진 주이지만, 더 중요한 변화는 실행 가능한 표현으로 내려온 점입니다. SLAM/recon은 3DGS와 relocalization 안으로, VLA는 latent action과 runtime inference 안으로, video generation은 geometry consistency와 controllability 안으로 재배치됐습니다.",
        "hot_vs_cold": {
            "hot": [
                {"cluster": "Generation", "why": "160편으로 최대 버킷이며 controllable video/world-model 평가가 두껍습니다."},
                {"cluster": "Robot Learning", "why": "103편으로 VLA 내부 구조와 execution stack 논문이 반복됩니다."},
                {"cluster": "3D/Scene", "why": "77편이며 SLAM/recon 신호가 3DGS와 LiDAR world model로 확산됐습니다."},
            ],
            "cold": [
                {"cluster": "Embodied AI", "why": "32편으로 상대적으로 작고 navigation 계열은 아직 독립 파도라기보다 watch-only에 가깝습니다."}
            ],
        },
        "clusters": clusters,
        "top5": [{"title": paper["title"], "arxiv": f"https://arxiv.org/abs/{paper['arxiv_id']}", "why": why, "phylogeny": paper["phylogeny"]} for paper, why in top5],
        "themes": themes,
        "prediction_review": prediction_review,
        "predictions": predictions,
        "next_week_actions": next_actions,
        "phylogeny_tags": [
            {
                "paper": f"https://arxiv.org/abs/{paper['arxiv_id']}",
                "source": paper["phylogeny"]["source"],
                "lineage": f'{paper["phylogeny"]["phylum"]} > {paper["phylogeny"]["class"]} > {paper["phylogeny"]["order"]} > {paper["phylogeny"]["genus"]}',
            }
            for cluster in clusters
            for paper in cluster["papers"]
        ],
        "buckets_summary": {name: data["total"] for name, data in snapshot["buckets"].items()},
    }

    Path("weekly").mkdir(exist_ok=True)
    with open(f"weekly/{WEEK}.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(weekly_json, f, ensure_ascii=False, indent=2)

    bucket_text = bucket_line(snapshot)
    sorted_buckets = sorted(snapshot["buckets"].items(), key=lambda item: item[1]["total"], reverse=True)
    bucket_rows = "".join(
        f'<div class="bucket"><span>{esc(name)}</span><b>{info["total"]}</b><small>CV {info["cv"]} · RO {info["ro"]} · CV/RO {info["cvro"]}</small></div>'
        for name, info in sorted_buckets
    )

    cluster_rows = []
    for cluster in clusters:
        tags = " ".join(f'<span class="tag">{esc(tag)}</span>' for tag in cluster["papers"][0]["importance_tags"])
        cluster_rows.append(
            "<tr>"
            f'<td><strong>{esc(cluster["cluster"])}</strong><br>{tags}</td>'
            f"<td>{paper_cell(cluster['papers'])}</td>"
            f'<td>{esc(cluster["why"])}</td>'
            f'<td><strong>{esc(cluster["confidence"].split(" — ")[0])}</strong><br><span class="small">{esc(cluster["confidence"])}</span></td>'
            f'<td>{esc(cluster["lab_action"])}</td>'
            "</tr>"
        )

    top5_html = "".join(
        f'<li>{link(paper)}<p>{esc(why)}</p>{phy_html(paper)}</li>'
        for paper, why in top5
    )
    themes_html = "".join(
        f'<div class="theme-card"><h3>{esc(t["title"])}</h3><p>{esc(t["summary"])}</p><p class="small">Confidence: {esc(t["confidence"])}</p></div>'
        for t in themes
    )
    review_html = "".join(
        f'<div class="card"><h3>{esc(r["label"])} {esc(r["title"])}</h3><p>{esc(r["reason"])}</p></div>'
        for r in prediction_review
    )
    predictions_html = "".join(
        f'<div class="card"><h3>{esc(pred["title"])}</h3><p>{esc(pred["claim"])}</p><p class="small">적중: {esc(pred["hit_condition"])}</p><p class="small">빗나감: {esc(pred["miss_condition"])}</p></div>'
        for pred in predictions
    )
    actions_html = "".join(
        f'<div class="card"><h3>{esc(item["title"])}</h3><p>{esc(item["action"])}</p><p class="small">Output: {esc(item["expected_output"])}</p></div>'
        for item in next_actions
    )

    css = """
*,*::before,*::after{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif;background:#f6f7f9;color:#1f2328;line-height:1.72;font-size:15px;padding:32px 16px;word-break:keep-all}
.container{max-width:1080px;margin:0 auto;background:#fff;border-radius:10px;box-shadow:0 1px 3px rgba(0,0,0,.06);padding:36px 44px 52px}
a{color:#0969da;text-decoration:none}a:hover{text-decoration:underline}
.home-button{display:inline-block;padding:7px 13px;background:#f3f4f6;color:#374151;border:1px solid #d1d5db;border-radius:7px;font-size:13px;margin:0 0 18px}
h1{font-size:29px;margin:0 0 6px;color:#0d1117}
h2{font-size:21px;margin:40px 0 14px;padding-bottom:8px;border-bottom:2px solid #e5e7eb;color:#0d1117}
h3{font-size:17px;margin:0 0 8px;color:#0d1117}
p{margin:0 0 14px}.subtitle{margin:0 0 22px;color:#656d76;font-size:14px}
.meta{font-size:13px;color:#3b434d;padding:14px 18px;background:#f6f8fa;border-left:3px solid #f97316;border-radius:6px;margin:14px 0 24px}
.thesis{background:#f0f9ff;border:1px solid #bae6fd;border-radius:10px;padding:18px 22px;color:#0c4a6e;font-size:15.5px}
.buckets{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin:14px 0}.bucket{border:1px solid #e5e7eb;border-radius:8px;padding:10px 12px;background:#fafbfc}.bucket span{display:block;font-weight:700}.bucket b{font-size:22px}.bucket small{display:block;color:#656d76;font-size:12px}
.cluster-table{width:100%;border-collapse:collapse;font-size:13.5px}.cluster-table th,.cluster-table td{border:1px solid #d1d5db;padding:9px 10px;text-align:left;vertical-align:top}.cluster-table th{background:#f3f4f6;color:#0d1117}.cluster-table td:nth-child(3){min-width:280px}
.tag{display:inline-block;margin:4px 4px 0 0;padding:1px 7px;border-radius:10px;background:#fff7ed;border:1px solid #fed7aa;color:#9a3412;font-size:12px}
.phy{margin:3px 0 7px;color:#475569;font-size:12.2px;line-height:1.45}.phy span{color:#166534}
.small{font-size:12.5px;color:#656d76}
.top5{counter-reset:item;padding:0;list-style:none}.top5 li{counter-increment:item;position:relative;margin:9px 0;padding:14px 16px 14px 52px;border:1px solid #e5e7eb;border-radius:8px;background:#fafbfc}.top5 li::before{content:counter(item);position:absolute;left:14px;top:14px;width:26px;height:26px;border-radius:50%;background:#0d1117;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700}.top5 p{margin:5px 0;color:#3b434d}
.theme-card,.card{border:1px solid #e5e7eb;border-radius:8px;background:#fafbfc;padding:15px 18px;margin:10px 0}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.note{background:#fff7ed;border:1px solid #fed7aa;border-radius:7px;padding:11px 14px;color:#7c2d12;font-size:13px}
footer{margin-top:42px;padding-top:16px;border-top:1px solid #e5e7eb;color:#656d76;font-size:13px}
@media(max-width:820px){.container{padding:24px 18px}.buckets,.grid{grid-template-columns:1fr}.cluster-table{font-size:12.5px;display:block;overflow-x:auto;white-space:normal}}
"""

    html_doc = f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>arXiv Weekly Retrospective — {DATE}</title><style>{css}</style></head>
<body><div class="container">
<a class="home-button" href="{SITE_URL}/">← Home</a>
<h1>🗓 arXiv Weekly Retrospective — {DATE} (Week 20)</h1>
<p class="subtitle">{WEEK_START} ~ {WEEK_END} · cs.CV/cs.RO pastweek · prompt prompts/instruction_v20260516.md</p>
<div class="meta">
<div><strong>소스:</strong> arxiv.org cs.CV/cs.RO pastweek · stdlib parser</div>
<div><strong>주간 스캔:</strong> {snapshot["totals"]["total_scanned"]} dedup · ROI {snapshot["totals"]["selected"]}</div>
<div><strong>버킷:</strong> {esc(bucket_text)}</div>
</div>
<div class="thesis"><strong>주간 결론:</strong> 이번 주는 VLA와 world model이 커진 주이지만, 더 중요한 변화는 실행 가능한 표현으로 내려온 점입니다. SLAM/recon은 3DGS와 relocalization 안으로, VLA는 latent action과 runtime inference 안으로, video generation은 geometry consistency와 controllability 안으로 재배치됐습니다.</div>

<h2>🧩 주간 클러스터 표</h2>
<table class="cluster-table"><thead><tr><th>Cluster</th><th>대표 논문</th><th>왜 중요?</th><th>Confidence</th><th>Lab action</th></tr></thead><tbody>
{''.join(cluster_rows)}
</tbody></table>

<h2>🔭 주간 동향</h2>
<p>이번 주 pastweek는 {snapshot["totals"]["total_scanned"]}편을 dedupe해서 봤고, 그중 {snapshot["totals"]["selected"]}편이 ROI 버킷에 걸렸습니다. 가장 큰 버킷은 Generation {snapshot["buckets"]["Generation"]["total"]}편, Robot Learning {snapshot["buckets"]["Robot Learning"]["total"]}편, Foundation Models {snapshot["buckets"]["Foundation Models"]["total"]}편입니다. 숫자만 보면 생성 계열이 압도적이지만, 실제 판세는 생성 모델이 조종 가능성, 물리 일관성, closed-loop 실행으로 내려오면서 Robot Learning, 3D/Scene, Safety/Alignment와 엮이는 쪽입니다.</p>
<div class="buckets">{bucket_rows}</div>

<h2>🔥 Hot vs Cold</h2>
<div class="grid">
<div class="card"><h3>Hot</h3><p><strong>Generation</strong>은 160편으로 가장 컸고, camera-controlled video와 world model 평가가 동시에 두꺼워졌습니다. <strong>Robot Learning</strong>은 VLA 내부 구조와 runtime inference로, <strong>3D/Scene</strong>은 3DGS/SLAM/relocalization으로 뚜렷한 읽을거리를 만들었습니다.</p></div>
<div class="card"><h3>Cold</h3><p><strong>Embodied AI</strong>는 32편으로 상대적으로 작습니다. 다만 VLN, ObjectNav, tool-aligned VLA가 완전히 식은 것은 아니고, 아직 독립 주간 thesis라기보다 다음 주 관찰 후보에 가깝습니다.</p></div>
</div>

<h2>📌 주간 Top 5</h2>
<ol class="top5">{top5_html}</ol>

<h2>🌟 Weekly deep-dive</h2>
<div class="card">
<h3>{link(top5[0][0])}</h3>
<p>MAGS-SLAM을 주간 대표로 고른 이유는 이름 그대로 SLAM이라서가 아닙니다. 이번 주에는 PanoPlane, relocalization, LiDAR world model, Gaussian Splatting 계열이 따로 흩어져 나왔는데, 이 논문은 그 조각들이 결국 map representation과 update 문제로 모인다는 점을 가장 직접적으로 보여줍니다.</p>
<p>예전에는 SLAM이 pose graph, feature matching, map update라는 명확한 파이프라인 이름으로 보였다면, 이제는 3DGS map, LiDAR world model, descriptor-space retrieval처럼 다른 이름으로 나타납니다. 그래서 우리 랩 입장에서는 "SLAM 논문이 적다"가 아니라 "지도 표현이 어디로 이동했는가"를 추적해야 합니다.</p>
{phy_html(top5[0][0])}
</div>

<h2>🧭 주간 테마 3</h2>
{themes_html}

<h2>🪞 지난 예측 채점</h2>
{review_html}

<h2>🔮 다음주 예측</h2>
{predictions_html}

<h2>🧪 다음 주 1주 실행안</h2>
{actions_html}

<h2>🧊 Skim-only / Watch-only</h2>
<div class="note">Embodied AI navigation은 아직 편수는 작지만, What Limits Vision-and-Language Navigation?, ConsistNav, SleepWalk처럼 instruction ambiguity와 action consistency를 건드리는 논문이 이어졌습니다. 다음 주에 VLN/ObjectNav가 uncertainty나 re-query 행동과 직접 묶이면 독립 클러스터로 올릴 만합니다.</div>

<h2>🎧 주간 오디오</h2>
<div class="note">TTS 환경은 이번 실행에 연결하지 않았습니다. 프롬프트 규칙에 따라 오디오 실패 또는 미연결은 발행 실패로 처리하지 않았습니다.</div>

<footer>Generated from parser outputs · prompt prompts/instruction_v20260516.md · WebFetch not used</footer>
</div></body></html>
"""

    Path("posts").mkdir(exist_ok=True)
    with open(f"posts/{DATE}-weekly.html", "w", encoding="utf-8", newline="\n") as f:
        f.write(html_doc)
    print(f"wrote posts/{DATE}-weekly.html")
    print(f"wrote weekly/{WEEK}.json")


if __name__ == "__main__":
    build()
