#!/usr/bin/env python3
"""Rewrite 2026-05-11/12 cluster interpretation with date-specific editorial judgment."""
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


OVERRIDES = {
    "2026-05-11": {
        "thesis": (
            "5/11은 VLA 자체보다 world model을 실제 simulator처럼 쓰려는 흐름이 더 선명합니다. "
            "Sword, ST-Gen4D, GEM, visual-feature world model 계열이 같이 나오면서, 생성 모델이 보기 좋은 샘플러가 아니라 "
            "planning과 sensor simulation에 들어갈 기반 구조가 될 수 있는지를 묻는 날입니다."
        ),
        "trend": (
            "오늘 /new는 cs.CV 184건, cs.RO 47건이고 dedupe 후 219건 중 99건이 ROI 버킷에 걸렸습니다. "
            "가장 큰 버킷은 Generation 29편, Foundation Models 16편, 3D/Scene 14편입니다. "
            "핵심은 VLA 논문 숫자보다 world model, 4D/LiDAR generation, resilient driving, adaptive token budget이 같은 날 나온 점입니다. "
            "즉 5/11은 모델 구조 경쟁보다 '실제 제어와 센서 조건에서 쓸 수 있는 생성·예측 기반'을 보는 날에 가깝습니다."
        ),
        "clusters": [
            {
                "cluster": "World model을 simulator로 쓰려는 흐름이 4D와 LiDAR까지 확장",
                "why": "Sword, ST-Gen4D, visual-feature world model, GEM은 모두 생성 모델을 단순 예쁜 영상 생성기가 아니라 다음 행동이나 센서 상황을 미리 실험하는 기반으로 보려는 논문입니다. 특히 4D spatiotemporal cognition과 LiDAR world model이 같이 나온 것은 world model 평가가 RGB 영상 품질에서 geometry, time, sensor realism 쪽으로 넓어진다는 신호입니다.",
                "confidence": "High",
                "confidence_note": "world model/4D/LiDAR 계열 대표 논문 4편 연결",
                "lab_action": "동일 driving/manipulation rollout에서 RGB 예측, LiDAR consistency, downstream control success를 분리 측정",
                "importance_tags": ["[평가축]", "[방법전환]", "[인프라]"],
                "papers_override": [
                    ("Sword: Style-Robust World Models as Simulators via Dynamic Latent Bootstrapping for VLA Policy Post-Training", "https://arxiv.org/abs/2605.07288"),
                    ("ST-Gen4D: Embedding 4D Spatiotemporal Cognition into World Model for 4D Generation", "https://arxiv.org/abs/2605.07390"),
                    ("Learning Visual Feature-Based World Models via Residual Feedback", "https://arxiv.org/abs/2605.07079"),
                    ("GEM: Generating LiDAR World Model via Deformable Mamba", "https://arxiv.org/abs/2605.07326"),
                ],
            },
            {
                "cluster": "주행 논문은 SOTA보다 foresight와 resilience 조건을 전면에 둠",
                "why": "123D, MORPH-U, See Tomorrow Act Today는 주행을 perception module 점수로만 보지 않고, 여러 modality를 묶고 미래 상황을 미리 보며 실패에 강한 motion을 만드는 문제로 봅니다. 그래서 5/11의 driving 흐름은 closed-loop benchmark 자체보다, 불확실한 상황에서 미리 판단하고 견디는 능력을 묻는 쪽입니다.",
                "confidence": "High",
                "confidence_note": "multimodal driving, resilient planning, foresight planning 논문이 같은 방향",
                "lab_action": "nuScenes/CARLA에 occlusion, delayed cue, route ambiguity를 넣고 foresight horizon별 failure rate 비교",
                "importance_tags": ["[실사용전환]", "[평가축]", "[경고신호]"],
                "papers_override": [
                    ("123D: Unifying Multi-Modal Autonomous Driving Data at Scale", "https://arxiv.org/abs/2605.08084"),
                    ("MORPH-U: Multi-Objective Resilient Motion Planning for V2X-Enabled Autonomous Driving", "https://arxiv.org/abs/2605.07370"),
                    ("See Tomorrow, Act Today: Foresight-Driven Autonomous Driving", "https://arxiv.org/abs/2605.07195"),
                    ("Predictive but Not Plannable: World Model Limits for Planning", "https://arxiv.org/abs/2605.07278"),
                ],
            },
            {
                "cluster": "Robust perception은 날씨, 추적, video reward처럼 실패 조건을 더 구체화",
                "why": "Weather-Robust Scene Semantics, TriP, Video Understanding Reward Modeling은 모두 모델이 언제 잘못 보는지를 더 구체적인 조건으로 쪼갭니다. 5/11의 reliability 흐름은 범용 safety보다 날씨 변화, tracking geometry, video reward처럼 실제 실패가 발생하는 지점을 좁혀 잡는 쪽입니다.",
                "confidence": "Medium",
                "confidence_note": "서로 다른 task지만 실패 조건을 구체화한다는 공통점",
                "lab_action": "weather shift, geometric tracking puzzle, video reward disagreement를 한 reliability board에 정리",
                "importance_tags": ["[경고신호]", "[해부분석]", "[평가축]"],
                "papers_override": [
                    ("Weather-Robust Scene Semantics with Vision-Aligned 4D Radar", "https://arxiv.org/abs/2605.07367"),
                    ("TriP: A Triangle Puzzle Approach to Robust Translation Averaging", "https://arxiv.org/abs/2605.07143"),
                    ("Video Understanding Reward Modeling: A Robust Benchmark and Performant Reward Models", "https://arxiv.org/abs/2605.07872"),
                ],
            },
            {
                "cluster": "효율화는 모든 token을 똑같이 처리하지 않는 방향으로 이동",
                "why": "Not All Tokens Need 40 Steps와 Beyond GSD-as-Token은 입력이나 token마다 필요한 계산량이 다르다는 전제를 깔고 있습니다. 이는 단순히 모델을 작게 만드는 효율화가 아니라, 어떤 token·scale·step에 계산을 더 줄지 정하는 스케줄링 문제로 바뀌고 있다는 뜻입니다.",
                "confidence": "Medium",
                "confidence_note": "token step, scale conditioning, rendering efficiency 논문이 계산 배분 문제로 연결",
                "lab_action": "diffusion step 수, visual token 수, scale encoding 방식을 고정 budget 아래에서 Pareto curve로 비교",
                "importance_tags": ["[실사용전환]", "[방법전환]", "[해부분석]"],
                "papers_override": [
                    ("Not All Tokens Need 40 Steps: Heterogeneous Step Allocation in Diffusion Transformers", "https://arxiv.org/abs/2605.06892"),
                    ("Beyond GSD-as-Token: Continuous Scale Conditioning for Remote Sensing VLMs", "https://arxiv.org/abs/2605.07562"),
                    ("Towards Photorealistic and Efficient Bokeh Rendering via Neural Rendering", "https://arxiv.org/abs/2605.07429"),
                    ("LENS: Efficient Visual Processing", "https://arxiv.org/abs/2605.07253"),
                ],
            },
            {
                "cluster": "로봇 쪽은 시각만으로 부족한 tactile·material·path context를 보강",
                "why": "AT-VLA, PathPainter, material-aware Hamiltonian risk field는 로봇이 화면만 보고 행동하는 데서 생기는 공백을 tactile, path prior, material risk 같은 추가 문맥으로 메우려는 흐름입니다. 5/11의 robot learning은 거대한 VLA 하나보다, 실제 접촉과 이동에서 빠지는 감각 정보를 어떻게 넣을지가 더 중요해 보입니다.",
                "confidence": "Medium",
                "confidence_note": "tactile injection, path transfer, material-aware risk가 보조 sensing/context 축으로 연결",
                "lab_action": "manipulation/navigation task에서 vision-only baseline에 tactile, path prior, material risk를 하나씩 추가하는 ablation",
                "importance_tags": ["[데이터전환]", "[방법전환]", "[실사용전환]"],
                "papers_override": [
                    ("AT-VLA: Adaptive Tactile Injection for Enhanced Feedback Reaction in Vision-Language-Action Models", "https://arxiv.org/abs/2605.07308"),
                    ("PathPainter: Transferring the Generalization Ability of Image Generation Models to Embodied Navigation", "https://arxiv.org/abs/2605.07496"),
                    ("Learning Material-Aware Hamiltonian Risk Fields for Safe Navigation", "https://arxiv.org/abs/2605.07038"),
                ],
            },
            {
                "cluster": "데이터와 embodiment 다양성은 benchmark의 배경 조건으로 올라옴",
                "why": "Bi3 같은 dataset 논문은 모델 성능 자체보다 어떤 문화권, 플랫폼, 사람 조건에서 데이터를 모았는지를 전면에 둡니다. 이는 embodied/navigation 평가에서도 단일 환경 성공률보다 data provenance와 embodiment diversity를 같이 봐야 한다는 신호입니다.",
                "confidence": "Low",
                "confidence_note": "신호는 있으나 대표 논문 수가 적어 후속 확인 필요",
                "lab_action": "데이터셋별 platform, user group, scene diversity, annotation protocol을 비교표로 정리",
                "importance_tags": ["[인프라]", "[데이터전환]", "[위험보류]"],
                "papers_override": [
                    ("Bi3: A Biplatform, Bicultural, Biperson Dataset", "https://arxiv.org/abs/2605.06863"),
                    ("MemCompiler: Memory Compilation for Embodied Agents", "https://arxiv.org/abs/2605.07594"),
                ],
            },
        ],
        "research_topics": [
            {"title": "World model simulator eval board", "claim": "Sword, ST-Gen4D, GEM을 같은 rollout에서 RGB, 4D geometry, LiDAR consistency, downstream success로 나눠 평가합니다."},
            {"title": "Foresight driving stress test", "claim": "123D, MORPH-U, See Tomorrow Act Today를 기반으로 occlusion과 route ambiguity에서 horizon별 판단 실패를 비교합니다."},
            {"title": "Tactile·material context ablation", "claim": "AT-VLA, PathPainter, material-aware risk field를 vision-only policy 위에 하나씩 붙여 실제로 어떤 context가 성능을 바꾸는지 확인합니다."},
        ],
    },
    "2026-05-12": {
        "thesis": (
            "5/12는 5/11보다 훨씬 더 VLA 실행 스택과 closed-loop 평가가 전면에 나온 날입니다. "
            "CoWorld-VLA, async inference, CapVector, ALAM이 내부 실행 구조를 건드리고, HiDrive와 driving world model 계열이 "
            "그 구조가 실제 주행 루프에서 버티는지를 묻습니다."
        ),
        "trend": (
            "오늘 /new는 cs.CV 399건, cs.RO 113건이고 dedupe 후 483건 중 417건이 ROI 버킷에 걸렸습니다. "
            "가장 큰 버킷은 Generation 80편, Foundation Models 76편, Efficiency/Systems 69편입니다. "
            "5/12의 핵심은 논문 수 자체보다 VLA 내부 실행 구조, driving world model, closed-loop benchmark, VLM self-verification failure가 한꺼번에 나온 점입니다."
        ),
        "clusters": [
            {
                "cluster": "VLA 실행 스택이 async, capability vector, latent transition으로 쪼개짐",
                "why": "CoWorld-VLA, asynchronous inference, CapVector, ALAM은 VLA를 하나의 큰 policy로 두지 않고 실행 경로를 나눠 봅니다. 이는 reasoning, capability transfer, latent transition, inference timing을 따로 조절할 수 있어야 실제 로봇이나 주행 시스템에서 안정적으로 쓸 수 있다는 뜻입니다.",
                "confidence": "High",
                "confidence_note": "VLA 내부 구조 관련 대표 논문 4편 연결",
                "lab_action": "같은 VLA backbone에서 async inference, capability vector, latent transition을 task family별로 ablation",
                "importance_tags": ["[해부분석]", "[방법전환]", "[실사용전환]"],
            },
            {
                "cluster": "World model은 물리 상호작용과 driving generalist 평가로 압축됨",
                "why": "Is Your Driving World Model an All-Around Player, DeformMaster, ACWM-Phys, SceneFactory는 world model이 그럴듯한 영상을 만드는지보다 물리 상호작용과 driving 상황에서 쓸 수 있는지를 묻습니다. 5/12의 world model 흐름은 5/11보다 평가 대상이 더 closed-loop와 physical interaction 쪽으로 가까워졌습니다.",
                "confidence": "High",
                "confidence_note": "driving WM, deformable object, physical interaction 논문이 직접 연결",
                "lab_action": "driving, deformable manipulation, action-conditioned video에서 physics violation과 task success를 같은 protocol로 측정",
                "importance_tags": ["[평가축]", "[표준후보]", "[경고신호]"],
            },
            {
                "cluster": "주행은 고수준 지시와 closed-loop benchmark가 중심축",
                "why": "HiDrive, VECTOR-Drive, DeepSight, DRIVE-C는 주행을 perception score가 아니라 고수준 지시, trajectory expert routing, long-horizon latent state, corruption condition에서 봅니다. 즉 5/12의 driving은 모델이 맞히는지가 아니라 실제 루프 안에서 언제 틀리는지를 묻는 날입니다.",
                "confidence": "High",
                "confidence_note": "closed-loop, expert routing, corruption dataset이 같은 driving 평가축으로 연결",
                "lab_action": "HiDrive류 high-level instruction과 DRIVE-C corruption을 결합한 closed-loop failure matrix 작성",
                "importance_tags": ["[평가축]", "[실사용전환]", "[표준후보]"],
            },
            {
                "cluster": "VLM 신뢰성은 self-verification과 over-alignment의 경계를 드러냄",
                "why": "Verification Mirage, C-CoT, When Language Overwrites Vision, Lost in Volume은 VLM이 스스로 검증하거나 언어 지시에 맞춘다고 해서 항상 더 안전해지는 것은 아니라는 점을 보여줍니다. 특히 의료와 driving처럼 틀린 확신이 위험한 도메인에서, self-verification이 어디서 깨지는지 따로 측정해야 합니다.",
                "confidence": "High",
                "confidence_note": "medical VQA, driving VLM, over-alignment, spatial VQA가 reliability boundary로 연결",
                "lab_action": "의료 VQA와 driving VLM에서 self-check answer, visual evidence, counterfactual prompt를 같이 저장하는 failure set 구축",
                "importance_tags": ["[경고신호]", "[평가축]", "[해부분석]"],
            },
            {
                "cluster": "효율화는 KV cache와 visual token pruning으로 실제 추론 경로를 줄임",
                "why": "Forcing-KV, LLaVA-UHD v4, Evading Visual Aphasia는 효율화를 파라미터 수가 아니라 추론 중 어떤 token과 cache를 남길지의 문제로 봅니다. 이는 큰 MLLM과 video diffusion을 배포하려면 정확도와 latency를 같은 그래프에서 봐야 한다는 뜻입니다.",
                "confidence": "High",
                "confidence_note": "KV cache, visual encoding, semantic token pruning이 같은 deployment bottleneck으로 연결",
                "lab_action": "MLLM/video diffusion에서 token count, cache size, latency, hallucination rate를 한 Pareto plot에 정리",
                "importance_tags": ["[실사용전환]", "[방법전환]", "[인프라]"],
            },
            {
                "cluster": "Navigation은 consistency gap과 long-horizon memory를 동시에 다룸",
                "why": "LCGNav, ConsistNav, EgoMemReason, PECMAN은 navigation이 단순한 다음 행동 선택이 아니라 목표 후보, semantic consistency, 장기 기억, multi-agent 협업을 함께 다뤄야 한다고 봅니다. 5/12의 navigation 흐름은 5/11보다 benchmark와 consistency failure가 더 분명합니다.",
                "confidence": "Medium",
                "confidence_note": "navigation benchmark와 consistency 논문이 연결되지만 표준 protocol은 아직 분산",
                "lab_action": "ObjectNav/VLN에 memory reset, ambiguous goal, semantic executive mismatch를 넣은 stress split 생성",
                "importance_tags": ["[문제정의]", "[평가축]", "[인프라]"],
            },
        ],
        "research_topics": [
            {"title": "VLA execution-stack ablation", "claim": "CoWorld-VLA, async inference, CapVector, ALAM을 같은 backbone과 task family 위에서 실행 경로별로 비교합니다."},
            {"title": "Driving world model closed-loop suite", "claim": "HiDrive, VECTOR-Drive, DeepSight, DRIVE-C를 묶어 고수준 지시와 corruption 조건의 실패 행렬을 만듭니다."},
            {"title": "VLM self-verification boundary set", "claim": "Verification Mirage, C-CoT, over-alignment 계열을 의료와 driving VLM에 적용해 self-check가 언제 실패를 강화하는지 모읍니다."},
        ],
    },
}


def esc(text: str) -> str:
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def rewrite_json(date: str, spec: dict) -> None:
    path = ROOT / "insights" / f"{date}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    old = data.get("clusters", [])
    for idx, override in enumerate(spec["clusters"]):
        if idx >= len(old):
            break
        clean_override = {k: v for k, v in override.items() if k != "papers_override"}
        old[idx].update(clean_override)
        if "papers_override" in override:
            old[idx]["papers"] = [
                {
                    "title": title,
                    "arxiv": url,
                    "importance_tags": override.get("importance_tags", []),
                }
                for title, url in override["papers_override"]
            ]
    data["daily_thesis"] = spec["thesis"]
    data["research_topics"] = spec.get("research_topics", data.get("research_topics", []))
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def cluster_table(data: dict) -> str:
    rows = []
    for cl in data["clusters"]:
        papers = cl.get("papers", [])
        links = []
        for p in papers[:4]:
            title = p.get("title", "")
            url = p.get("arxiv", "#")
            label = title.split(":")[0][:54]
            links.append(f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(label)}</a>')
        tags = " ".join(f"<span class='tag'>{esc(t)}</span>" for t in cl.get("importance_tags", []))
        rows.append(
            "<tr>"
            f"<td><strong>{esc(cl['cluster'])}</strong><br>{tags}</td>"
            f"<td>{', '.join(links)}</td>"
            f"<td>{esc(cl['why'])}</td>"
            f"<td><strong>{esc(cl.get('confidence','Medium'))}</strong><br><span class='small'>{esc(cl.get('confidence_note',''))}</span></td>"
            f"<td>{esc(cl.get('lab_action',''))}</td>"
            "</tr>"
        )
    return "<table class='cluster-table'><thead><tr><th>Cluster</th><th>대표 논문</th><th>왜 중요?</th><th>Confidence</th><th>Lab action</th></tr></thead><tbody>" + "\n".join(rows) + "</tbody></table>"


def insight_cards(data: dict) -> str:
    cards = []
    for cl in data["clusters"][:4]:
        p = cl.get("papers", [{}])[0]
        title = p.get("title", "")
        url = p.get("arxiv", "#")
        cards.append(
            "<div class='card insight'>"
            f"<h3>{esc(cl['cluster'])}</h3>"
            f"<p>{esc(cl['why'])}</p>"
            f"<p><strong>대표:</strong> <a href=\"{esc(url)}\" target=\"_blank\" rel=\"noopener\">{esc(title)}</a></p>"
            "</div>"
        )
    return "".join(cards)


def topic_cards(data: dict) -> str:
    cards = []
    for topic in data.get("research_topics", [])[:3]:
        cards.append(
            "<div class='card topic'>"
            f"<h3>{esc(topic.get('title', ''))}</h3>"
            f"<p>{esc(topic.get('claim', ''))}</p>"
            "</div>"
        )
    return "".join(cards)


def rewrite_html(date: str, spec: dict) -> None:
    insight_data = json.loads((ROOT / "insights" / f"{date}.json").read_text(encoding="utf-8"))
    path = ROOT / "posts" / f"{date}.html"
    source = path.read_text(encoding="utf-8")
    source = re.sub(
        r'(<div class="thesis"><strong>오늘의 결론:</strong> ).*?(</div>)',
        lambda m: m.group(1) + esc(spec["thesis"]) + m.group(2),
        source,
        flags=re.S,
    )
    source = re.sub(
        r"(<h2>🧩 오늘의 클러스터 지도</h2>).*?(<h2>🔭 주간 동향</h2>)",
        lambda m: m.group(1) + cluster_table(insight_data) + m.group(2),
        source,
        flags=re.S,
    )
    source = re.sub(
        r"(<h2>🔭 주간 동향</h2><p>).*?(</p>\s*<div class=\"bucket-line\">)",
        lambda m: m.group(1) + esc(spec["trend"]) + m.group(2),
        source,
        flags=re.S,
    )
    source = re.sub(
        r"(<h2>💡 오늘의 인사이트</h2>).*?(<h2>🔬 추천 연구주제</h2>)",
        lambda m: m.group(1) + insight_cards(insight_data) + m.group(2),
        source,
        flags=re.S,
    )
    source = re.sub(
        r"(<h2>🔬 추천 연구주제</h2>).*?(<h2>📌 must-read</h2>)",
        lambda m: m.group(1) + topic_cards(insight_data) + m.group(2),
        source,
        flags=re.S,
    )
    path.write_text(source, encoding="utf-8", newline="\n")


def main() -> int:
    for date, spec in OVERRIDES.items():
        rewrite_json(date, spec)
        rewrite_html(date, spec)
        print(f"rewrote {date}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
