#!/usr/bin/env python3
"""Generate the 2026-05-23 weekly retrospective from parser-derived data."""
from __future__ import annotations

import html
import json
from pathlib import Path


DATE = "2026-05-23"
WEEK = "2026-W21"
WEEK_START = "2026-05-17"
WEEK_END = "2026-05-23"
SITE_URL = "https://gisbi-kim.github.io/arxiv-daily-summary"
PROMPT = "prompts/instruction_v20260516.md"


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
    for bucket_name, bucket in weekly_full["buckets_full"].items():
        for p in bucket["papers"]:
            item = dict(p)
            item["bucket"] = bucket_name
            out[p["arxiv_id"]] = item
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
        f'{esc(lineage)} <span>{esc(ph["confidence"])}</span></div>'
    )


def paper_cell(papers: list[dict]) -> str:
    rows = []
    for p in papers:
        rows.append(link(p, p.get("short") or p["title"]) + phy_html(p))
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
        "vla": phy("ROBOTICS", "Embodied Intelligence > Vision-Language-Action Models > Runtime Verification > Preemptive Rollout Safety"),
        "world": phy("CVML", "Generative Modeling > Video and World Models > Controllable Generation > Motion and Reasoning Control"),
        "geometry": phy("ROBOTICS", "Robot Perception > Mapping and Reconstruction > Neural and Gaussian Maps > Feed-Forward 3D Geometry"),
        "trust": phy("CVML", "Trustworthy ML > Robustness and Alignment > Evidence Grounding > Medical and Driving Reliability"),
        "systems": phy("CVML", "Efficient ML Systems > Token and Cache Efficiency > Adaptive Inference > World Memory Compression"),
        "driving": phy("ROBOTICS", "Autonomous Driving > Closed-Loop Planning > Adverse Condition Robustness > Sensor and Policy Adaptation"),
    }

    tags_by_key = {
        "vla": ["[실사용전환]", "[검증축]", "[로봇정책]"],
        "world": ["[평가축]", "[방법전환]", "[표준후보]"],
        "geometry": ["[SLAM/Recon]", "[지도표현]", "[실사용전환]"],
        "trust": ["[경고신호]", "[근거검증]", "[배포신뢰성]"],
        "systems": ["[인프라]", "[메모리]", "[속도/비용]"],
        "driving": ["[악조건]", "[closed-loop]", "[데이터셋]"],
    }

    def p(arxiv_id: str, key: str, short: str | None = None) -> dict:
        item = make_paper(by_id, arxiv_id)
        item["short"] = short or item["title"].split(":")[0]
        item["phylogeny"] = lineages[key]
        item["importance_tags"] = tags_by_key[key]
        return item

    clusters = [
        {
            "cluster": "VLA는 데모 성공률보다 런타임 검증과 실행 구조를 묻는 쪽으로 이동",
            "papers": [
                p("2605.22446", "vla", "Pre-VLA"),
                p("2605.21854", "vla", "CrossVLA"),
                p("2605.22812", "vla", "GesVLA"),
                p("2605.21061", "vla", "Grounding Driving VLA"),
            ],
            "why": "Robot Learning은 84편으로 지난주보다 작지만, VLA 신호는 더 구체적입니다. Pre-VLA는 rollout 전에 실패를 검증하려 하고, CrossVLA는 post-training과 inference를 함께 다루며, GesVLA와 driving VLA 계열은 입력 양식과 행동 표현을 나눠 봅니다. 이제 질문은 'VLA가 되는가'가 아니라 어떤 내부 표현과 검증 루프가 실제 로봇 실행을 망치지 않는가입니다.",
            "confidence": "High — VLA, runtime verification, action representation 논문이 같은 주에 반복",
            "lab_action": "LIBERO/RoboCasa와 driving VLA split에서 runtime verification, intent/action representation, inference optimization을 같은 실패 유형표로 비교",
        },
        {
            "cluster": "Video/world model은 보기 좋은 샘플보다 움직임·시간·추론 통제성으로 재편",
            "papers": [
                p("2605.22818", "world", "MotiMotion"),
                p("2605.22570", "world", "VGenST-Bench"),
                p("2605.22344", "world", "Bernini"),
                p("2605.22050", "world", "Broken Memories"),
            ],
            "why": "Generation은 149편으로 가장 큰 버킷입니다. 그런데 핵심은 양이 아니라 평가축입니다. motion-controlled generation, spatio-temporal reasoning benchmark, latent semantic planning, memorization failure가 같이 나오면서 video generation을 단순 품질이 아니라 원하는 움직임을 안정적으로 만들고 오래 유지하며 추론에 쓸 수 있는지로 보려는 흐름이 강해졌습니다.",
            "confidence": "High — Generation 최대 버킷 안에서 controllability, temporal reasoning, memory failure가 동시에 관측",
            "lab_action": "camera/motion command, entity consistency, temporal reasoning, memorization failure를 분리한 video-world-model 평가표 작성",
        },
        {
            "cluster": "Geometry/SLAM 신호는 3DGS 지도, feed-forward 복원, 4D 주행 시뮬레이션으로 분산",
            "papers": [
                p("2605.22020", "geometry", "ForeSplat"),
                p("2605.21032", "geometry", "Physically Consistent 4D Scene Reconstruction"),
                p("2605.22013", "geometry", "PointLLM-R"),
                p("2605.22342", "geometry", "4D-GSW"),
            ],
            "why": "3D/Scene은 72편으로 여전히 두껍습니다. SLAM이라는 제목이 앞에 붙은 논문보다 feed-forward 3DGS, point-cloud reasoning, 4D reconstruction, closed-loop driving simulation 안에 geometry 문제가 숨어 있습니다. 그래서 이번 주의 geometry lens는 reconstruction 품질보다 로봇과 주행 시스템이 쓸 수 있는 지도/장면 표현을 얼마나 빨리 만들고 업데이트할 수 있는가에 가깝습니다.",
            "confidence": "High — prompt의 Geometry/SLAM/Reconstruction watch lens에 해당하는 신호가 충분",
            "lab_action": "ForeSplat, 4D scene reconstruction, point-cloud reasoning을 relocalization/update-cost/dynamic-scene-failure 기준으로 재분류",
        },
        {
            "cluster": "VLM 신뢰성은 의료·주행 근거 위치와 보이는/안 보이는 취약성 검증으로 이동",
            "papers": [
                p("2605.22414", "trust", "Ophthalmic VQA Evidence"),
                p("2605.22273", "trust", "Visible-Infrared VLM Vulnerability"),
                p("2605.22185", "trust", "Safety-Critical Driving Video Analysis"),
                p("2605.22080", "trust", "JMed48k"),
            ],
            "why": "Foundation Models와 Safety/Alignment를 따로 세면 각각 88편, 61편이지만 실제로는 같은 문제를 보고 있습니다. 의료 VQA는 병변 근거 위치를, visible-infrared VLM은 cross-task adversarial 취약성을, driving video analysis는 안전 critical 판단을 묻습니다. 정답률보다 '어떤 근거를 보고 틀렸는가'를 남기는 평가가 더 중요해졌습니다.",
            "confidence": "High — medical, visible-infrared, driving safety가 모두 evidence/reliability 축으로 연결",
            "lab_action": "VQA와 driving video QA에 evidence localization, counterfactual perturbation, confidence calibration failure를 같은 dashboard로 기록",
        },
        {
            "cluster": "효율화는 모델 축소가 아니라 world memory, KV cache, video diffusion 토큰 예산 문제로 구체화",
            "papers": [
                p("2605.22718", "systems", "WorldKV"),
                p("2605.22269", "systems", "MuKV"),
                p("2605.22015", "systems", "ORBIS"),
                p("2605.20891", "systems", "HDMoE"),
            ],
            "why": "Efficiency/Systems는 61편입니다. WorldKV와 MuKV는 긴 video/world memory를 어떻게 압축하고 다시 꺼낼지 묻고, ORBIS는 video diffusion에서 어떤 토큰을 줄일지 다룹니다. 즉 효율화는 작은 모델 경쟁이 아니라 실제 multimodal/video 추론 경로에서 무엇을 기억하고 무엇을 버릴지의 설계 문제가 됐습니다.",
            "confidence": "High — KV cache, world memory, token reduction이 여러 응용에서 반복",
            "lab_action": "long-video QA, VLA rollout memory, video diffusion에서 cache size, latency, accuracy drop Pareto curve를 같은 축으로 비교",
        },
        {
            "cluster": "자율주행은 악조건 센서 변환과 closed-loop 판단 실패를 함께 보기 시작",
            "papers": [
                p("2605.22809", "driving", "Sensor2Sensor"),
                p("2605.22018", "driving", "FRED"),
                p("2605.21139", "driving", "Distill to Think, Foresee to Act"),
                p("2605.20390", "driving", "STELLAR"),
            ],
            "why": "Autonomous Driving은 37편으로 크지는 않지만 명확합니다. flooded road dataset, cross-embodiment sensor conversion, cognitive-physical RL, 3D perception scaling이 함께 나오면서 단순 perception 점수보다 악조건에서 센서/정책이 어떻게 무너지는지 확인하려는 흐름이 보입니다.",
            "confidence": "Medium-High — 버킷 수는 중간이지만 adverse condition과 closed-loop 신호가 선명",
            "lab_action": "FRED류 악조건에서 sensor conversion, BEV uncertainty, policy failure를 route-level closed-loop stress test로 묶기",
        },
    ]

    top5 = [
        (clusters[0]["papers"][0], "VLA를 실제 배포하기 전에 rollout 실패를 미리 잡자는 흐름을 가장 직접적으로 보여줍니다."),
        (clusters[1]["papers"][0], "video generation이 motion control과 visual reasoning을 함께 요구받는 방향으로 이동했다는 대표 신호입니다."),
        (clusters[2]["papers"][0], "feed-forward 3DGS가 SLAM/reconstruction lens와 만나는 지점이라 robotics 쪽 후속 읽기가 큽니다."),
        (clusters[4]["papers"][0], "world memory와 KV cache 문제가 VLM/VLA 장기 실행의 실제 병목으로 올라왔다는 신호입니다."),
        (clusters[5]["papers"][1], "악조건 도로 데이터셋이 driving VLA와 closed-loop 평가에 바로 연결될 수 있어 실험 가치가 큽니다."),
    ]

    themes = [
        {
            "title": "VLA는 '잘한다'보다 '언제 망가지는지 미리 아는가'로 질문이 바뀝니다",
            "summary": "Pre-VLA, CrossVLA, GesVLA, Grounding Driving VLA가 같은 주에 나온 점은 VLA가 단순 모델 크기 경쟁에서 벗어나 runtime verification, representation, inference optimization 경쟁으로 넘어간다는 뜻입니다. 우리 쪽에서는 VLA baseline을 볼 때 success rate 옆에 실패 예측, latency, action representation 항목을 같이 놓아야 합니다.",
            "confidence": "High",
        },
        {
            "title": "World/video generation은 장면 생성보다 조종 가능한 시뮬레이터에 가까워집니다",
            "summary": "MotiMotion, VGenST-Bench, Bernini는 모두 영상이 그럴듯한지를 넘어서 움직임, 시간, semantic plan을 어떻게 제어할지를 묻습니다. 이 흐름은 robotics simulation이나 driving world model과 직접 이어질 가능성이 큽니다.",
            "confidence": "High",
        },
        {
            "title": "Geometry/SLAM은 제목보다 기능으로 추적해야 합니다",
            "summary": "이번 주 geometry 논문들은 SLAM이라는 단어를 항상 앞세우지 않습니다. 대신 feed-forward 3DGS, physically consistent 4D reconstruction, point-cloud reasoning처럼 지도 표현과 재현 가능한 장면 상태를 만드는 기능으로 나타납니다. 그래서 SLAM/recon watch는 키워드 검색보다 기능별 분류가 더 중요합니다.",
            "confidence": "High",
        },
    ]

    predictions = [
        {
            "title": "다음 주 VLA 논문은 runtime verification 또는 latency 항목을 더 자주 보고할 것",
            "claim": "Pre-VLA와 CrossVLA가 같은 주에 나온 만큼, 다음 묶음에서는 VLA success rate만이 아니라 실패 예측, speculative inference, action representation latency가 표에 같이 들어갈 가능성이 큽니다.",
            "hit_condition": "다음 주 VLA 논문 중 runtime/latency/verification을 명시적으로 포함한 논문이 2편 이상이면 적중입니다.",
            "miss_condition": "VLA 논문이 계속 task success만 보고하고 실행 비용과 실패 예측을 빼면 빗나감입니다.",
        },
        {
            "title": "3DGS는 rendering 품질보다 driving/robotics 장면 표현으로 더 많이 연결될 것",
            "claim": "ForeSplat과 physically consistent 4D reconstruction이 나온 만큼, feed-forward 3DGS와 dynamic scene reconstruction이 localization, simulation, policy evaluation으로 붙는 흐름을 더 볼 가능성이 큽니다.",
            "hit_condition": "3DGS/4D reconstruction 논문이 driving simulation, relocalization, robot scene representation 중 하나와 연결되면 적중입니다.",
            "miss_condition": "3DGS가 editing/rendering 품질 개선으로만 반복되면 빗나감입니다.",
        },
        {
            "title": "긴 video/VLM 평가는 memory compression과 evidence grounding을 같이 물을 것",
            "claim": "WorldKV, MuKV, Ophthalmic VQA evidence, driving video safety가 함께 나온 주라 다음 주에는 memory를 줄이는 기술과 근거를 잃지 않는 평가가 같은 논문 안에서 만날 가능성이 큽니다.",
            "hit_condition": "long-video/VLM 논문이 cache/memory 압축과 evidence localization 또는 factuality를 함께 평가하면 적중입니다.",
            "miss_condition": "압축 논문과 신뢰성 논문이 완전히 분리돼 나오면 빗나감입니다.",
        },
    ]

    next_actions = [
        {
            "title": "VLA runtime failure board",
            "action": "Pre-VLA, CrossVLA, GesVLA, Grounding Driving VLA를 success, failure prediction, latency, action representation으로 정리",
            "expected_output": "1-page matrix for VLA runtime risks",
        },
        {
            "title": "Geometry/SLAM hidden-signal board",
            "action": "ForeSplat, 4D scene reconstruction, PointLLM-R, 4D-GSW를 SLAM/recon 기능 관점으로 재태깅",
            "expected_output": "geometry watch table with map type, update path, robotics relevance",
        },
        {
            "title": "World memory and evidence metric grid",
            "action": "WorldKV, MuKV, Ophthalmic VQA, driving video safety를 memory budget과 evidence retention 축으로 비교",
            "expected_output": "metric grid for long-video/VLM reliability",
        },
    ]

    weekly_json = {
        "date": DATE,
        "iso_week": WEEK,
        "week_start": WEEK_START,
        "week_end": WEEK_END,
        "weekly_thesis": "이번 주는 Generation이 149편으로 가장 크지만, 실제 변화는 video/world model, VLA, 3D geometry가 모두 '실행 전에 무엇을 검증하고 어떤 표현을 남길 것인가'로 내려온 점입니다. VLA는 runtime verification으로, 3D/SLAM은 feed-forward 3DGS와 4D scene으로, VLM 신뢰성은 evidence grounding과 memory compression으로 재배치됐습니다.",
        "hot_vs_cold": {
            "hot": [
                {"cluster": "Generation", "why": "149편으로 최대 버킷이며 motion control, temporal reasoning, world-model memory가 함께 두꺼워졌습니다."},
                {"cluster": "Foundation Models", "why": "88편이고 medical VQA, receipt reasoning, visible-infrared vulnerability처럼 평가/근거 축이 선명합니다."},
                {"cluster": "Robot Learning", "why": "84편이지만 VLA runtime verification과 driving VLA가 직접적으로 나왔습니다."},
            ],
            "cold": [
                {"cluster": "Embodied AI", "why": "28편으로 가장 작고 VLN/abstention 신호는 있지만 아직 주간 thesis의 중심은 아닙니다."}
            ],
        },
        "clusters": clusters,
        "top5": [{"title": paper["title"], "arxiv": f"https://arxiv.org/abs/{paper['arxiv_id']}", "why": why, "phylogeny": paper["phylogeny"]} for paper, why in top5],
        "themes": themes,
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
        f.write("\n")

    bucket_text = bucket_line(snapshot)
    sorted_buckets = sorted(snapshot["buckets"].items(), key=lambda item: item[1]["total"], reverse=True)
    bucket_rows = "".join(
        f'<div class="bucket"><span>{esc(name)}</span><b>{info["total"]}</b>'
        f'<small>CV {info["cv"]} · RO {info["ro"]} · CV/RO {info["cvro"]}</small></div>'
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
<h1>arXiv Weekly Retrospective — {DATE} (Week 21)</h1>
<p class="subtitle">{WEEK_START} ~ {WEEK_END} · cs.CV/cs.RO pastweek · prompt {PROMPT}</p>
<div class="meta">
<div><strong>소스:</strong> arxiv.org cs.CV/cs.RO pastweek · stdlib parser</div>
<div><strong>주간 스캔:</strong> {snapshot["totals"]["total_scanned"]} dedup · ROI {snapshot["totals"]["selected"]}</div>
<div><strong>버킷:</strong> {esc(bucket_text)}</div>
</div>
<div class="thesis"><strong>주간 결론:</strong> 이번 주는 Generation이 {snapshot["buckets"]["Generation"]["total"]}편으로 가장 크지만, 실제 변화는 video/world model, VLA, 3D geometry가 모두 "실행 전에 무엇을 검증하고 어떤 표현을 남길 것인가"로 내려온 점입니다. VLA는 runtime verification으로, 3D/SLAM은 feed-forward 3DGS와 4D scene으로, VLM 신뢰성은 evidence grounding과 memory compression으로 재배치됐습니다.</div>

<h2>주간 클러스터 표</h2>
<table class="cluster-table"><thead><tr><th>Cluster</th><th>대표 논문</th><th>왜 중요?</th><th>Confidence</th><th>Lab action</th></tr></thead><tbody>
{''.join(cluster_rows)}
</tbody></table>

<h2>주간 동향</h2>
<p>이번 주 pastweek는 {snapshot["totals"]["total_scanned"]}편을 dedupe해서 봤고, 그중 {snapshot["totals"]["selected"]}편이 ROI 버킷에 걸렸습니다. 가장 큰 버킷은 Generation {snapshot["buckets"]["Generation"]["total"]}편, Foundation Models {snapshot["buckets"]["Foundation Models"]["total"]}편, Robot Learning {snapshot["buckets"]["Robot Learning"]["total"]}편입니다. 숫자만 보면 생성 계열이 압도적이지만, 실제 판세는 생성 모델이 motion control, memory, evidence, closed-loop 실행과 붙으면서 Robot Learning, 3D/Scene, Safety/Alignment까지 같이 흔드는 쪽입니다.</p>
<div class="buckets">{bucket_rows}</div>

<h2>Hot vs Cold</h2>
<div class="grid">
<div class="card"><h3>Hot</h3><p><strong>Generation</strong>은 149편으로 가장 컸고, motion-controlled video와 world-model memory가 동시에 두꺼워졌습니다. <strong>Foundation Models</strong>는 88편으로 clinical/evidence reasoning이 강했고, <strong>Robot Learning</strong>은 VLA runtime verification 신호가 분명했습니다.</p></div>
<div class="card"><h3>Cold</h3><p><strong>Embodied AI</strong>는 28편으로 가장 작습니다. 다만 AwareVLN, abstention benchmark, world-ego modeling처럼 navigation과 embodied reliability 신호가 남아 있어 다음 주 관찰 후보로는 유지합니다.</p></div>
</div>

<h2>주간 Top 5</h2>
<ol class="top5">{top5_html}</ol>

<h2>Weekly deep-dive</h2>
<div class="card">
<h3>{link(top5[0][0])}</h3>
<p>Pre-VLA를 대표 논문으로 고른 이유는 VLA가 더 커졌기 때문이 아닙니다. 이 논문은 VLA와 world-model rollout을 실제 실행 전에 검증하려는 문제를 정면으로 둡니다. 즉 다음 경쟁은 새로운 policy 하나가 아니라, policy가 망가지기 전에 어떤 신호로 멈추고 수정할 수 있는가에 가깝습니다.</p>
<p>우리 쪽에서는 이 흐름을 VLA 안전성 논문으로만 읽으면 좁습니다. runtime verification, speculative inference, action representation, driving VLA가 같은 주에 나왔다는 점은 VLA 평가표에 success rate만 넣는 방식이 곧 부족해진다는 뜻입니다.</p>
{phy_html(top5[0][0])}
</div>

<h2>주간 테마 3</h2>
{themes_html}

<h2>다음주 예측</h2>
{predictions_html}

<h2>다음 주 1주 실행안</h2>
{actions_html}

<h2>Skim-only / Watch-only</h2>
<div class="note">Embodied AI navigation은 편수가 작지만 AwareVLN, Yes-Man Syndrome, ESI-Bench처럼 self-awareness, abstention, perception-action loop 신호가 있습니다. 다음 주에 이 흐름이 VLA runtime verification과 붙으면 독립 클러스터로 올릴 만합니다.</div>

<h2>주간 오디오</h2>
<div class="note">TTS 환경은 이번 실행에 연결하지 않았습니다. 프롬프트 규칙에 따라 오디오 실패 또는 미연결은 발행 실패로 처리하지 않았습니다.</div>

<footer>Generated from parser outputs · prompt {PROMPT} · WebFetch not used</footer>
</div></body></html>
"""

    Path("posts").mkdir(exist_ok=True)
    with open(f"posts/{DATE}-weekly.html", "w", encoding="utf-8", newline="\n") as f:
        f.write(html_doc)
    print(f"wrote posts/{DATE}-weekly.html")
    print(f"wrote weekly/{WEEK}.json")


if __name__ == "__main__":
    build()
