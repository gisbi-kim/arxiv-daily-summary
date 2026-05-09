#!/usr/bin/env python3
"""Regenerate prompt-style posts from committed local materials.

The original out/*.json parser outputs were not committed for older dates, so
this script treats the already-published post as the immutable paper-set
snapshot.  It does not revisit arXiv /new or /pastweek.  It only rebuilds the
HTML around the saved paper IDs, titles, bucket assignments, trends, insights,
benchmarks, and weekly JSON files that are present in the repository.
"""
from __future__ import annotations

import html
import json
import re
import sys
from collections import Counter
from datetime import date as Date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POSTS = ROOT / "posts"

BUCKETS = [
    "3D/Scene",
    "Robot Learning",
    "Autonomous Driving",
    "Foundation Models",
    "Generation",
    "Efficiency/Systems",
    "Embodied AI",
    "Safety/Alignment",
]

BUCKET_ICON = {
    "3D/Scene": "📦",
    "Robot Learning": "🤖",
    "Autonomous Driving": "🚗",
    "Foundation Models": "🧠",
    "Generation": "🎨",
    "Efficiency/Systems": "⚙️",
    "Embodied AI": "🏠",
    "Safety/Alignment": "🛡️",
}

WEEKDAY_KO = ["월", "화", "수", "목", "금", "토", "일"]

BANNED_REPLACEMENTS = [
    ("정조준", "다룹니다"),
    ("표면화", "드러남"),
    ("batch", "묶음"),
    ("Batch", "묶음"),
    ("paradigm", "평가 기준"),
    ("substrate", "기반 구조"),
    ("Substrate", "기반 구조"),
    ("catalog 단계", "정리하고 비교하는 단계"),
    ("bottleneck", "가장 큰 제약"),
    ("개별 처방", "각 문제에 맞춘 해결책"),
    ("failure mode", "실패 유형"),
    ("Failure mode", "실패 유형"),
    ("failure-management", "실패를 줄이는 설계"),
    ("audit", "점검"),
    ("Audit", "점검"),
]


def read_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def esc(value) -> str:
    return html.escape(str(value or ""), quote=False)


def clean(text: str) -> str:
    text = html.unescape(str(text or ""))
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    for old, new in BANNED_REPLACEMENTS:
        text = text.replace(old, new)
    return text


def weekday(date_str: str) -> str:
    try:
        return WEEKDAY_KO[Date.fromisoformat(date_str).weekday()]
    except ValueError:
        return ""


def badge_html(badge: str) -> str:
    label = clean(badge).upper()
    if label in {"CV/RO", "CVRO"}:
        return '<span class="badge cvro">CV/RO</span>'
    if label == "RO":
        return '<span class="badge ro">RO</span>'
    if label == "CV":
        return '<span class="badge cv">CV</span>'
    return '<span class="badge x">?</span>'


def arxiv_link(aid: str, title: str | None = None) -> str:
    label = title or aid
    return f'<a href="https://arxiv.org/abs/{esc(aid)}" target="_blank" rel="noopener">{esc(label)}</a>'


def split_blocks_by_details(source: str) -> dict[str, str]:
    blocks = {}
    for m in re.finditer(r"<details>\s*<summary>(.*?)</summary>(.*?)</details>", source, re.S):
        summary = clean(m.group(1))
        for bucket in BUCKETS:
            if bucket in summary:
                blocks[bucket] = m.group(2)
                break
    return blocks


def parse_post_snapshot(path: Path) -> dict[str, list[dict]]:
    source = path.read_text(encoding="utf-8")
    blocks = split_blocks_by_details(source)
    parsed = {bucket: [] for bucket in BUCKETS}
    if not blocks:
        # Current regenerated posts use h4.bucket sections instead of details.
        h4_re = re.compile(r"<h4[^>]*class=['\"]bucket['\"][^>]*>(.*?)</h4>(.*?)(?=<h4[^>]*class=['\"]bucket['\"]|<h2|</div></body>)", re.S)
        for m in h4_re.finditer(source):
            heading = clean(m.group(1))
            bucket = next((b for b in BUCKETS if b in heading), None)
            if not bucket:
                continue
            for chunk in re.split(r"<div class=['\"]mini-paper['\"]>", m.group(2))[1:]:
                chunk = chunk.split("</div>", 1)[0]
                link_m = re.search(r'href="https://arxiv\.org/abs/([0-9.]+)"[^>]*>(.*?)</a>', chunk, re.S)
                if not link_m:
                    continue
                badge_m = re.search(r'<span class="badge [^"]+">(.*?)</span>', chunk, re.S)
                authors_m = re.search(r"<p class=['\"]authors['\"]>(.*?)</p>", chunk, re.S)
                bullets = [clean(x) for x in re.findall(r"<li>(.*?)</li>", chunk, re.S)]
                parsed[bucket].append(
                    {
                        "arxiv_id": link_m.group(1),
                        "title": clean(link_m.group(2)),
                        "badge": clean(badge_m.group(1) if badge_m else "?"),
                        "authors": clean(authors_m.group(1) if authors_m else ""),
                        "tags": [],
                        "old_bullets": bullets,
                    }
                )
        if any(parsed.values()):
            return parsed

    if not blocks:
        # Fallback for any older post shape: bucket is unknown, but this keeps
        # the paper set from disappearing.
        links = re.findall(r'href="https://arxiv\.org/abs/([0-9.]+)"[^>]*>(.*?)</a>', source, re.S)
        seen = set()
        for aid, title in links:
            if aid in seen:
                continue
            seen.add(aid)
            parsed["Foundation Models"].append(
                {"arxiv_id": aid, "title": clean(title), "badge": "?", "authors": "", "tags": [], "old_bullets": []}
            )
        return parsed

    for bucket, block in blocks.items():
        chunks = re.split(r"<div class=['\"]mini-paper['\"]>", block)[1:]
        for chunk in chunks:
            chunk = chunk.split("</div>", 1)[0]
            link_m = re.search(r'href="https://arxiv\.org/abs/([0-9.]+)"[^>]*>(.*?)</a>', chunk, re.S)
            if not link_m:
                continue
            badge_m = re.search(r'<span class="badge [^"]+">(.*?)</span>', chunk, re.S)
            authors_m = re.search(r"<span class=['\"]why['\"]>(.*?)</span>", chunk, re.S)
            tags_m = re.search(r"<span class=['\"]tag['\"]>(.*?)</span>", chunk, re.S)
            bullets = [clean(x) for x in re.findall(r"<li>(.*?)</li>", chunk, re.S)]
            parsed[bucket].append(
                {
                    "arxiv_id": link_m.group(1),
                    "title": clean(link_m.group(2)),
                    "badge": clean(badge_m.group(1) if badge_m else "?"),
                    "authors": clean(authors_m.group(1) if authors_m else ""),
                    "tags": re.findall(r"\[([^\]]+)\]", clean(tags_m.group(1) if tags_m else "")),
                    "old_bullets": bullets,
                }
            )
    return parsed


def lower_blob(*parts: str) -> str:
    return " ".join(parts).lower()


def short_title(title: str, limit: int = 58) -> str:
    title = re.split(r"[:：]", title)[0].strip()
    return title if len(title) <= limit else title[: limit - 1].rstrip() + "…"


def topic_title_ko(text: str) -> str:
    low = text.lower()
    if "video" in low and ("camera" in low or "controll" in low):
        return "비디오 생성은 이제 '예쁜 샘플'보다 '원하는 대로 조종되는가'를 봅니다"
    if "vla" in low and ("relation" in low or "expert" in low or "latent" in low or "structure" in low):
        return "VLA는 큰 모델 하나보다 내부 구조를 드러내는 쪽으로 갑니다"
    if "reliab" in low or "calibration" in low or "uncertainty" in low or "safety" in low:
        return "신뢰성은 부록 주제가 아니라 배포 조건이 되고 있습니다"
    if "attack surface" in low or "threat" in low or "stride" in low or "jailbreak" in low:
        return "안전성 논문은 공격 경로를 실제 시스템 경계 안에서 보기 시작했습니다"
    if "world model" in low or "4d" in low:
        return "World Model 평가는 영상 복원에서 행동에 도움 되는지로 옮겨갑니다"
    if "navigation" in low or "objectnav" in low or "vln" in low:
        return "내비게이션은 한 걸음씩 따라가기보다 전체 지도를 보고 결정하는 쪽입니다"
    if "diffusion" in low or "generation" in low:
        return "생성 모델은 품질 경쟁에서 제어와 평가 경쟁으로 이동합니다"
    if "efficien" in low or "router" in low or "token" in low:
        return "효율 논문은 계산량 절감만이 아니라 무엇을 버려도 되는지 묻고 있습니다"
    return "오늘 논문들이 같은 질문을 다른 방식으로 묻고 있습니다"


def explain_claim(text: str) -> str:
    raw = clean(text)
    low = raw.lower()
    if "vla" in low and ("relation" in low or "expert" in low or "latent" in low or "structure" in low or "supervision" in low):
        return (
            "VLA를 하나의 거대한 policy로만 보면 왜 성공하고 왜 실패하는지 설명하기가 어렵습니다. "
            "이번 흐름은 object-hand-task 관계, expert routing, latent action, verifier처럼 내부 역할을 나눠서 보는 쪽입니다. "
            "즉 모델 크기를 더 키우기 전에 어떤 구조가 어떤 작업에서 실제로 도움이 되는지 비교할 수 있는 발판이 생긴다는 뜻입니다."
        )
    if "world model" in low and ("reconstruction" in low or "reward" in low or "interactive" in low):
        return (
            "예전에는 World Model을 미래 영상을 얼마나 그럴듯하게 복원하거나 예측하느냐로 많이 평가했습니다. "
            "이제는 그 예측이 로봇 행동 성공에 실제로 도움이 되는지, 그리고 상호작용 상황에서도 계속 쓸 수 있는지를 같이 보자는 쪽으로 기준이 바뀌고 있습니다. "
            "뜻은 간단합니다. 보기 좋은 예측보다 행동을 더 잘하게 만드는 예측이 중요해졌다는 겁니다."
        )
    if "world model" in low or "4d" in low or "physical realism" in low or "physics" in low:
        return (
            "4D World Model 쪽은 이제 장면을 그럴듯하게 만드는 수준을 넘어, 시간에 따라 물리적으로 말이 되는지와 실제 상호작용에 쓸 수 있는지를 같이 묻고 있습니다. "
            "LoViF 같은 평가는 dynamics, optics, temporal consistency처럼 실패가 어디서 나는지 나눠서 보려는 시도입니다. "
            "즉 4D/World Model 연구가 데모 영상 경쟁에서 평가 프로토콜과 물리 기반 장면 표현 경쟁으로 넘어가고 있다는 뜻입니다."
        )
    if "vla" in low and ("relation" in low or "expert" in low or "latent" in low or "structure" in low):
        return (
            "VLA를 하나의 거대한 policy로만 보면 왜 성공하고 왜 실패하는지 설명하기가 어렵습니다. "
            "이번 흐름은 object-hand-task 관계, expert routing, latent action, verifier처럼 내부 역할을 나눠서 보는 쪽입니다. "
            "즉 모델 크기를 더 키우기 전에 어떤 구조가 어떤 작업에서 실제로 도움이 되는지 비교할 수 있는 발판이 생긴다는 뜻입니다."
        )
    if "video" in low and ("camera" in low or "controll" in low):
        return (
            "비디오 생성은 더 이상 한 장면이 그럴듯한지만으로는 부족해지고 있습니다. "
            "카메라 경로, 대상의 움직임, 정체성 유지, 지연시간처럼 실제 제작 도구에서 중요한 조건을 따로 재야 합니다. "
            "그래서 이 흐름은 생성 모델을 감상용 샘플러가 아니라 조작 가능한 촬영 시스템으로 바꾸려는 움직임에 가깝습니다."
        )
    if "reliab" in low or "uncertainty" in low or "calibration" in low or "contradiction" in low:
        return (
            "여기서 핵심은 모델이 답을 잘 맞히는가만 보는 게 아닙니다. "
            "증거가 부족하거나, 분포가 바뀌었거나, 문장 안에 부정 표현이 끼어 있을 때 모델이 자기 한계를 알아차리는지가 중요해졌습니다. "
            "실제 배포에서는 빠른 모델보다 언제 믿으면 안 되는지 알려주는 모델이 더 값질 수 있다는 뜻입니다."
        )
    if "routing" in low or "token" in low or "efficient" in low or "latency" in low:
        return (
            "효율화의 질문도 단순히 토큰을 얼마나 줄였느냐에서 조금 달라지고 있습니다. "
            "질문에 따라 어떤 프레임과 근거를 남겨야 하는지 고르는 문제가 되었고, 잘못 고르면 중요한 증거를 버릴 수 있습니다. "
            "그래서 계산량 절감과 실패 위험을 한 표에서 같이 봐야 할 필요성이 커지고 있습니다."
        )
    if "diffusion" in low and ("alignment" in low or "preference" in low or "self" in low or "nash" in low):
        return (
            "diffusion alignment는 외부 보상 모델이 정답을 준다고 가정하는 방식에서 조금씩 벗어나고 있습니다. "
            "이번 흐름은 self-play, self-distillation, self-editing처럼 모델이 자기 출력과 비교하거나 스스로 고치는 루프를 쓰려는 쪽입니다. "
            "그래서 중요한 질문은 성능이 올랐느냐뿐 아니라, 이런 자기참조 루프가 어떤 task에서는 안정적이고 어떤 task에서는 편향을 키우는지입니다."
        )
    if "navigation" in low or "objectnav" in low or "vln" in low:
        return (
            "내비게이션 쪽은 지시문을 한 단계씩 따라가는 policy보다, 지도 수준에서 목표와 모호성을 다시 해석하는 쪽으로 움직입니다. "
            "사용자 질문이 애매하거나 관측이 부족할 때 바로 이동하기보다 비교하고 확인하는 과정이 중요해졌습니다. "
            "로봇이 길을 찾는 문제가 점점 '어디로 갈까'뿐 아니라 '지금 이 목표를 제대로 이해했나'를 묻는 문제로 바뀌고 있습니다."
        )
    if "hallucination" in low or "evidence" in low or "grounding" in low or "clinical" in low or "unintended changes" in low:
        return (
            "VLM 쪽 신뢰성 논문은 모델이 답을 맞히는지만 보지 않고, 실제로 어떤 근거를 보고 답했는지를 더 집요하게 묻고 있습니다. "
            "차트, 의료 영상, image-to-image 변화처럼 근거가 흐려지기 쉬운 영역에서 evidence anchoring이나 hallucination 점검이 중요해졌습니다. "
            "즉 foundation model 평가가 '그럴듯한 설명'에서 '근거가 남는 설명'으로 이동하고 있다는 뜻입니다."
        )
    if "attack surface" in low or "threat" in low or "stride" in low or "jailbreak" in low:
        return (
            "안전성 논문은 이제 '모델이 나쁜 답을 하느냐'만 보지 않고, 입력·도구·제어기·로봇 행동 사이의 경계에서 공격이 어떻게 이어지는지를 봅니다. "
            "즉 텍스트 prompt 하나를 막는 문제가 아니라, 실제 시스템 안에서 위험이 어디를 타고 이동하는지 그 경로를 그려야 한다는 뜻입니다. "
            "우리 쪽에서 보면 실험을 만들 때도 단일 실패 사례보다 경계별 실패 표를 먼저 준비해야 합니다."
        )
    if raw:
        return (
            "이 흐름은 새 기술 이름을 외우라는 뜻이라기보다, 여러 논문이 같은 평가 기준과 실패 조건을 공유하기 시작했다는 신호로 읽는 게 좋습니다. "
            "그래서 다음에 볼 것은 성능 숫자 하나보다 어떤 조건에서 좋아지고, 어떤 조건에서 무너지는지입니다."
        )
    return "오늘 논문들은 성능 숫자보다 평가 조건과 실패 조건을 더 분명히 하려는 방향으로 묶입니다."


def paper_template(paper: dict, bucket: str) -> tuple[str, str, str, str]:
    title = paper["title"]
    low = lower_blob(title, bucket, " ".join(paper.get("old_bullets", [])))
    if "vla" in low or "vision-language-action" in low or "imitation" in low:
        problem = "VLA가 훈련에서 본 상황은 잘 처리하지만, 새 물체나 새 조합에서는 왜 흔들리는지 설명하기 어렵다는 문제입니다."
        method = "논문은 관계 구조, expert 분기, latent action, 검증기처럼 policy 안쪽의 역할을 나눠 보려 합니다."
        meaning = "의미는 모델을 더 키우는 경쟁에서, 어떤 내부 구조가 일반화에 기여하는지 비교하는 경쟁으로 넘어갈 수 있다는 점입니다."
    elif "video" in low or "diffusion" in low or "generation" in bucket.lower() or "generate" in low:
        problem = "생성 결과가 보기 좋아도 사용자가 원하는 움직임, 시점, 시간 조건을 안정적으로 따르지 못하면 실제 도구로 쓰기 어렵습니다."
        method = "논문은 카메라 제어, 시간 일관성, 조건부 생성, 샘플 선택 같은 장치를 넣어 생성 과정을 더 직접 조절하려 합니다."
        meaning = "의미는 생성 모델 평가가 미적 품질에서 제어 가능성과 실패 조건으로 넓어지고 있다는 점입니다."
    elif "uncertainty" in low or "safety" in low or "calibration" in low or "contrabench" in low or "ood" in low:
        problem = "모델이 틀릴 때도 자신 있게 말하거나, 부정 표현과 분포 변화에서 근거를 잘못 읽는 문제가 있습니다."
        method = "논문은 불확실성 추정, calibration, contradiction benchmark, open-set 점검처럼 실패를 드러내는 장치를 세웁니다."
        meaning = "의미는 실제 배포에서 정확도와 함께 '언제 믿으면 안 되는가'를 측정해야 한다는 점입니다."
    elif "driving" in low or "bev" in low or "motion" in low or "trajectory" in low:
        problem = "자율주행은 인식, 예측, 계획이 따로 좋아도 닫힌 루프에서 함께 흔들릴 수 있습니다."
        method = "논문은 BEV 표현, 궤적 예측, 폐루프 평가, 센서 변환 같은 요소를 통해 실제 주행 조건에 더 가까운 검증을 시도합니다."
        meaning = "의미는 단일 perception 점수보다 계획과 행동으로 이어지는 품질을 봐야 한다는 점입니다."
    elif "navigation" in low or "objectnav" in low or "embodied" in bucket.lower():
        problem = "로봇이 지시문을 이해해도 관측이 부족하거나 목표가 애매하면 잘못된 곳으로 이동하기 쉽습니다."
        method = "논문은 지도, 메모리, 비교 판단, 목표 재해석을 넣어 바로 행동하기 전에 상황을 더 잘 정리하려 합니다."
        meaning = "의미는 embodied AI가 단순 policy 실행보다 확인과 재해석을 포함한 의사결정 문제로 가고 있다는 점입니다."
    elif "3d" in low or "nerf" in low or "gaussian" in low or "scene" in bucket.lower():
        problem = "3D 표현은 보기 좋은 재구성만으로는 부족하고, sparse view나 새 시점, downstream 작업에서 버텨야 합니다."
        method = "논문은 multi-view geometry, Gaussian/NeRF 계열 표현, semantic feature, uncertainty를 결합해 장면 표현을 더 쓰기 좋게 만듭니다."
        meaning = "의미는 3D/Scene 논문이 렌더링 품질에서 실제 활용 조건으로 평가 축을 넓히고 있다는 점입니다."
    else:
        problem = f"{bucket} 안에서 기존 평가나 사용 조건이 충분히 설명하지 못하던 부분을 다룹니다."
        method = "논문은 새 데이터셋, 학습 구조, 평가 프로토콜, 또는 효율화 장치를 통해 그 빈칸을 메우려 합니다."
        meaning = "의미는 성능 숫자만 보기보다 어떤 조건에서 효과가 나는지 확인해야 한다는 점입니다."
    caution = "읽을 때는 벤치마크가 실제 사용 조건을 잘 대표하는지, ablation이 핵심 주장과 주변 효과를 분리하는지 보면 좋습니다."
    return problem, method, meaning, caution


CORE_OVERRIDES = {
    "2605.06667": (
        "예쁜 영상을 생성하는 데서 멈추지 않고, 배우의 움직임과 카메라 궤적을 같이 지정해 새 장면으로 옮기는 방법입니다. "
        "기존 방식이 샘플 품질을 주로 봤다면, 이 논문은 사용자가 원하는 촬영 조건을 얼마나 따라가는지로 질문을 바꿉니다. "
        "그래서 비디오 생성이 감상용 데모에서 편집 가능한 촬영 시스템으로 이동한다는 신호로 볼 수 있습니다."
    ),
    "2605.05714": (
        "VLA가 훈련에서 본 task는 잘하지만 새 장면과 물체에서 약해지는 이유를 object-hand-task 관계 표현 문제로 봅니다. "
        "기존엔 큰 policy 하나가 알아서 일반화하길 기대했다면, 이 논문은 조작에 필요한 관계를 명시적으로 드러내 일반화를 돕습니다. "
        "뜻은 모델 크기보다 어떤 관계 구조를 배우게 하느냐가 더 중요해질 수 있다는 겁니다."
    ),
    "2605.05848": (
        "긴 비디오는 visual token이 너무 많아져 memory와 latency가 빠르게 커집니다. "
        "VideoRouter는 모든 프레임을 같은 방식으로 압축하지 않고, 질문에 필요한 시각 근거가 어디 있는지에 따라 routing을 달리합니다. "
        "그래서 효율화가 단순 압축이 아니라 중요한 증거를 남기는 선택 문제로 바뀝니다."
    ),
    "2605.05810": (
        "흉부 X-ray에 consolidation이 보이는데도 선택지의 'No consolidation' 같은 부정 문장에 끌리는 실패를 따로 재는 benchmark입니다. "
        "기존 VLM 평가는 정답률만 보기 쉬웠는데, 이 논문은 영상 근거와 문장 부정이 충돌할 때 생기는 위험한 실패를 분리해 봅니다. "
        "의료처럼 실수가 큰 분야에서는 모델이 무엇을 봤는지와 무엇을 잘못 읽었는지를 따로 점검해야 한다는 뜻입니다."
    ),
    "2605.05328": (
        "3D object detector가 자신감 있게 낸 점수가 실제 위험도를 반영하지 못하는 문제를 다룹니다. "
        "특히 학습 분포와 다른 환경에서는 기존 calibration이 쉽게 약해지기 때문에, query와 feature density를 이용해 confidence를 다시 보정하려 합니다. "
        "즉 3D perception은 검출만 잘하는 것보다 언제 자신의 판단을 낮춰야 하는지 아는 쪽이 중요해지고 있습니다."
    ),
}


def render_trends(date_str: str, trends: dict, papers: dict[str, list[dict]]) -> str:
    bucket_counts = trends.get("buckets") or {
        b: {"total": len(ps), "cv": sum(p["badge"] == "CV" for p in ps), "ro": sum(p["badge"] == "RO" for p in ps), "cvro": sum("RO" in p["badge"] and "CV" in p["badge"] for p in ps)}
        for b, ps in papers.items()
    }
    top = sorted(bucket_counts.items(), key=lambda kv: kv[1].get("total", 0), reverse=True)[:3]
    bottom = sorted(bucket_counts.items(), key=lambda kv: kv[1].get("total", 0))[:2]
    hot_name = top[0][0] if top else "Generation"
    hot_count = top[0][1].get("total", 0) if top else 0
    hot_claim = ""
    if trends.get("hottest"):
        hot_claim = explain_claim(trends["hottest"][0].get("note") or trends["hottest"][0].get("topic", ""))
    else:
        hot_claim = explain_claim(hot_name)
    p1 = (
        f"{date_str} 묶음에서 제일 두꺼운 축은 {hot_name}이고, 저장된 스냅샷 기준 {hot_count}편이 잡혔습니다. "
        f"{hot_claim}"
    )
    quiet = ", ".join(f"{name} {meta.get('total', 0)}편" for name, meta in bottom)
    p2 = (
        f"반대로 조용한 쪽은 {quiet}입니다. 조용하다는 말이 덜 중요하다는 뜻은 아니고, 이번 묶음에서는 큰 방법론 경쟁보다 "
        "평가셋, 실패 사례, 작은 적용처처럼 다음 주제를 준비하는 재료가 더 많았다는 뜻에 가깝습니다. "
        "그래서 여기서는 숫자 자체보다 어떤 공백이 남았는지를 보는 게 더 유익합니다."
    )
    examples = []
    for b, ps in papers.items():
        for p in ps[:2]:
            examples.append(short_title(p["title"]))
        if len(examples) >= 4:
            break
    p3 = (
        "오늘 논문들을 주간 흐름 위에 올려놓으면, 개별 SOTA보다 평가 기준과 실패 조건을 다시 짜는 논문들이 더 눈에 띕니다. "
        f"예를 들면 {', '.join(examples[:3])} 같은 논문들은 새 모델 하나를 소개하는 데서 끝나지 않고, "
        "무엇을 성공으로 볼지와 무엇을 위험 신호로 볼지를 같이 묻습니다."
    )
    return f"<p>{esc(p1)}</p><p>{esc(p2)}</p><p>{esc(p3)}</p>"


def render_cv_ro(trends: dict) -> str:
    cv = [k for k, _ in trends.get("keywords_cv", [])[:8]]
    ro = [k for k, _ in trends.get("keywords_ro", [])[:8]]
    common = [x for x in cv if x in set(ro)][:5]
    cv_only = [x for x in cv if x not in set(common)][:3]
    ro_only = [x for x in ro if x not in set(common)][:3]
    p = (
        "CV 쪽은 표현, 생성, 벤치마크를 통해 모델이 무엇을 보고 있는지 더 잘 재려는 논문이 많고, "
        "RO 쪽은 그 표현이 실제 행동과 배포 조건에서 버티는지를 묻는 논문이 많습니다. "
        "같은 단어가 나와도 맥락이 조금 다릅니다. 예를 들어 3D는 CV에서는 렌더링과 재구성 품질에 가깝고, "
        "RO에서는 조작이나 내비게이션에 쓸 장면 이해에 더 가깝습니다."
    )
    items = [
        f"<li><strong>공통으로 뜨는 단어:</strong> {esc(', '.join(common) or 'video, 3D, VLA, robustness 계열')}</li>",
        f"<li><strong>CV 쪽에 더 강한 단어:</strong> {esc(', '.join(cv_only) or 'generation, diffusion, benchmark')}</li>",
        f"<li><strong>RO 쪽에 더 강한 단어:</strong> {esc(', '.join(ro_only) or 'manipulation, navigation, policy')}</li>",
        "<li><strong>같은 단어 다른 맥락:</strong> diffusion은 CV에서는 생성 품질과 제어, RO에서는 planning이나 policy 개선 쪽으로 읽힙니다.</li>",
    ]
    return f"<p>{esc(p)}</p><ul>{''.join(items)}</ul>"


def cluster_name(text: str) -> str:
    low = text.lower()
    if "video" in low and ("camera" in low or "controll" in low):
        return "Controllable video generation"
    if "vla" in low and ("relation" in low or "expert" in low or "latent" in low or "structure" in low):
        return "VLA structure exposure"
    if "reliab" in low or "uncertainty" in low or "calibration" in low or "contradiction" in low:
        return "Reliability-aware deployment"
    if "navigation" in low or "objectnav" in low or "vln" in low:
        return "Navigation as map-level decision"
    if "world model" in low or "4d" in low:
        return "World Model evaluation shift"
    if "diffusion" in low or "generation" in low:
        return "Generation under stronger control"
    if "efficien" in low or "routing" in low or "token" in low:
        return "Efficient evidence routing"
    return short_title(clean(text), 42)


def cluster_tags(text: str) -> list[str]:
    low = text.lower()
    tags = []
    if any(x in low for x in ["benchmark", "dataset", "evaluation", "eval"]):
        tags.append("평가축")
    if any(x in low for x in ["structure", "relation", "latent", "expert", "routing", "architecture"]):
        tags.append("방법전환")
    if any(x in low for x in ["safety", "reliab", "uncertainty", "calibration", "contradiction", "threat"]):
        tags.append("경고신호")
    if any(x in low for x in ["infrastructure", "data", "system", "deployment", "efficient"]):
        tags.append("인프라")
    if not tags:
        tags.append("문제정의")
    return tags[:2]


def lab_action_for(text: str) -> str:
    low = text.lower()
    if "video" in low and ("camera" in low or "controll" in low):
        return "카메라 경로 오차, 대상 정체성 유지, 지연시간을 분리한 metric grid 설계"
    if "vla" in low and ("relation" in low or "expert" in low or "latent" in low or "structure" in low):
        return "LIBERO/RoboCasa에서 relation, expert, latent action, verifier를 같은 표로 ablation"
    if "reliab" in low or "uncertainty" in low or "calibration" in low or "contradiction" in low:
        return "효율을 높일 때 calibration이나 contradiction 실패가 커지는지 같이 점검"
    if "navigation" in low or "objectnav" in low or "vln" in low:
        return "R2R/ObjectNav에 ambiguous-query와 map-level planning stress test 추가"
    if "world model" in low or "4d" in low:
        return "영상 복원 점수와 robot success rate를 같은 rollout에서 비교"
    if "3d" in low or "lidar" in low:
        return "view shift와 sensor shift를 나눠 calibration protocol 작성"
    return "대표 논문 2~3편을 같은 입력, 같은 실패 기준, 같은 ablation 표로 재비교"


def evidence_ids_from_obj(obj: dict) -> list[str]:
    ids = []
    for key in ["papers", "evidence"]:
        for value in obj.get(key, []) or []:
            m = re.search(r"([0-9]{4}\.[0-9]{4,5})", str(value))
            if m and m.group(1) not in ids:
                ids.append(m.group(1))
    return ids


def fallback_cluster_specs(id_map: dict[str, tuple[str, dict]]) -> list[dict]:
    candidates = [
        {
            "name": "Navigation as map-level decision",
            "keywords": ["navone", "navigation", "objectnav", "label map", "ambiguous user queries", "top-down maps"],
            "exclude": ["mri", "slice navigation", "image pretraining", "underwater"],
            "why": (
                "VLN/ObjectNav가 지시문을 한 단계씩 따라가는 문제에서, 전체 지도와 애매한 목표를 함께 판단하는 문제로 이동하고 있습니다. "
                "즉 로봇이 바로 움직이기보다, 현재 목표가 무엇인지와 어느 후보가 더 맞는지를 먼저 비교해야 한다는 뜻입니다."
            ),
            "confidence": "Medium",
            "confidence_note": "navigation 관련 논문 2편 이상 연결, benchmark 확산은 추가 확인 필요",
            "lab_action": "R2R/ObjectNav에 ambiguous-query와 top-down map planning stress test를 묶어 평가",
            "tags": ["문제정의", "인프라"],
        },
        {
            "name": "Evidence-aware VLM reliability",
            "keywords": ["hallucination", "evidence-aware", "keyframe anchoring", "clinical dermatology", "unintended changes", "diffcap-bench", "grounding video-llms"],
            "why": (
                "VLM 평가는 이제 정답률이나 그럴듯한 설명만으로 부족해지고 있습니다. "
                "의료, 차트, image-to-image 변화처럼 근거가 흐려지기 쉬운 작업에서는 모델이 어떤 시각 근거를 붙잡고 답했는지까지 확인해야 합니다."
            ),
            "confidence": "Medium",
            "confidence_note": "foundation/safety 쪽에서 evidence·hallucination·clinical robustness 논문이 함께 등장",
            "lab_action": "VTAgent/CAST/DiffCap-Bench류를 묶어 evidence anchoring 실패 사례 표 만들기",
            "tags": ["경고신호", "평가축"],
        },
        {
            "name": "Efficient physical grounding systems",
            "keywords": ["grounding video-llms", "physical reality", "sparse attention", "temporal structure", "efficient test-time adaptation", "lightweight"],
            "why": (
                "효율 논문도 단순히 모델을 작게 만드는 데서 끝나지 않고, 물리적 단서나 시간 구조를 잃지 않으면서 계산을 줄이는 방향으로 가고 있습니다. "
                "즉 빠른 모델을 만들되, 실제 장면을 이해하는 데 필요한 근거를 버리지 않는지가 핵심 평가축이 됩니다."
            ),
            "confidence": "Medium",
            "confidence_note": "Efficiency/Systems 안에서 physical grounding·sparse attention·temporal adaptation 신호가 반복",
            "lab_action": "token/attention 절감 전후로 physical grounding과 temporal consistency가 얼마나 깨지는지 비교",
            "tags": ["인프라", "방법전환"],
        },
        {
            "name": "3D/robotics calibration under shift",
            "keywords": ["query2uncertainty", "ga3t", "roadside lidar", "distribution shift", "traversability", "novel view synthesis"],
            "why": (
                "3D perception은 재구성 품질만으로는 부족하고, 센서 위치나 환경이 바뀌었을 때 confidence가 얼마나 믿을 만한지가 중요해지고 있습니다. "
                "그래서 3D/Scene 흐름도 렌더링 품질에서 deployment shift와 calibration을 같이 보는 쪽으로 넓어집니다."
            ),
            "confidence": "Medium",
            "confidence_note": "3D/Scene 안에서 uncertainty·V2X·traversability 논문이 함께 등장",
            "lab_action": "GA3T와 Query2Uncertainty 스타일 shift calibration protocol을 같은 표로 정리",
            "tags": ["경고신호", "인프라"],
        },
    ]
    specs = []
    for spec in candidates:
        scored_ids = []
        for aid, (_, paper) in id_map.items():
            blob = lower_blob(aid, paper.get("title", ""), paper.get("authors", ""))
            if any(k in blob for k in spec.get("exclude", [])):
                continue
            score = sum(1 for k in spec["keywords"] if k in blob)
            if score:
                scored_ids.append((score, aid))
        scored_ids.sort(key=lambda x: (-x[0], x[1]))
        ids = [aid for _, aid in scored_ids]
        if len(ids) >= 2:
            enriched = dict(spec)
            enriched["ids"] = ids[:4]
            specs.append(enriched)
    return specs


def render_cluster_map(trends: dict, insights: dict, id_map: dict[str, tuple[str, dict]], papers: dict[str, list[dict]]) -> str:
    raw_rows = []
    for obj in insights.get("insights", []):
        raw_rows.append((f"{obj.get('title','')} {obj.get('claim','')}", evidence_ids_from_obj(obj), obj.get("claim", "")))
    for obj in trends.get("hottest", []):
        raw_rows.append((f"{obj.get('topic','')} {obj.get('note','')}", evidence_ids_from_obj(obj), obj.get("note", "")))

    rows = []
    seen = set()
    for text, ids, claim in raw_rows:
        name = cluster_name(text)
        if name in seen:
            continue
        seen.add(name)
        if not ids:
            for bucket in sorted(papers, key=lambda b: len(papers[b]), reverse=True):
                ids = [p["arxiv_id"] for p in papers[bucket][:3]]
                break
        links = []
        for aid in ids[:4]:
            if aid in id_map:
                links.append(arxiv_link(aid, short_title(id_map[aid][1]["title"], 34)))
            else:
                links.append(arxiv_link(aid, aid))
        confidence = "High" if len(ids) >= 2 else "Medium"
        why = explain_claim(claim or text)
        tags = " ".join(f"<span class='tag'>[{esc(tag)}]</span>" for tag in cluster_tags(text))
        rows.append(
            "<tr>"
            f"<td><strong>{esc(name)}</strong><br>{tags}</td>"
            f"<td>{', '.join(links) or '대표 논문 추출 없음'}</td>"
            f"<td>{esc(why)}</td>"
            f"<td><strong class='conf {confidence}'>{confidence}</strong><br><span class='small'>{esc('대표 논문 ' + str(len(ids)) + '편 이상 연결' if ids else '근거 논문 추가 확인 필요')}</span></td>"
            f"<td>{esc(lab_action_for(text))}</td>"
            "</tr>"
        )
        if len(rows) >= 5:
            break
    if len(rows) < 5:
        for spec in fallback_cluster_specs(id_map):
            if spec["name"] in seen:
                continue
            links = []
            for aid in spec["ids"]:
                if aid in id_map:
                    links.append(arxiv_link(aid, short_title(id_map[aid][1]["title"], 34)))
            tags = " ".join(f"<span class='tag'>[{esc(tag)}]</span>" for tag in spec["tags"])
            rows.append(
                "<tr>"
                f"<td><strong>{esc(spec['name'])}</strong><br>{tags}</td>"
                f"<td>{', '.join(links)}</td>"
                f"<td>{esc(spec['why'])}</td>"
                f"<td><strong class='conf {esc(spec['confidence'])}'>{esc(spec['confidence'])}</strong><br><span class='small'>{esc(spec['confidence_note'])}</span></td>"
                f"<td>{esc(spec['lab_action'])}</td>"
                "</tr>"
            )
            seen.add(spec["name"])
            if len(rows) >= 5:
                break
    if not rows:
        return "<p>저장된 인사이트/트렌드 자료가 부족해 클러스터 표를 만들지 못했습니다.</p>"
    return (
        "<table class='cluster-table'><thead><tr>"
        "<th>Cluster</th><th>대표 논문</th><th>왜 중요?</th><th>Confidence</th><th>Lab action</th>"
        "</tr></thead><tbody>"
        + "\n".join(rows)
        + "</tbody></table>"
    )


def important_ids(insights: dict, trends: dict, papers: dict[str, list[dict]]) -> list[str]:
    ids = []
    for obj in insights.get("insights", []):
        for url in obj.get("papers", []):
            m = re.search(r"([0-9]{4}\.[0-9]{4,5})", url)
            if m and m.group(1) not in ids:
                ids.append(m.group(1))
    for obj in trends.get("hottest", []):
        for ev in obj.get("evidence", []):
            m = re.search(r"([0-9]{4}\.[0-9]{4,5})", str(ev))
            if m and m.group(1) not in ids:
                ids.append(m.group(1))
    for bucket in sorted(papers, key=lambda b: len(papers[b]), reverse=True):
        for p in papers[bucket][:1]:
            if p["arxiv_id"] not in ids:
                ids.append(p["arxiv_id"])
    return ids[:5]


def paper_by_id(papers: dict[str, list[dict]]) -> dict[str, tuple[str, dict]]:
    out = {}
    for bucket, ps in papers.items():
        for p in ps:
            out[p["arxiv_id"]] = (bucket, p)
    return out


def render_insights(insights: dict, id_map: dict[str, tuple[str, dict]]) -> str:
    cards = []
    items = insights.get("insights", [])[:3]
    if not items:
        return "<p>저장된 인사이트 JSON이 없어, 오늘 논문별 요약과 버킷 현황을 중심으로 읽으면 됩니다.</p>"
    for obj in items:
        title = topic_title_ko(obj.get("title", "") + " " + obj.get("claim", ""))
        claim = explain_claim(obj.get("claim", ""))
        links = []
        for url in obj.get("papers", [])[:4]:
            aid = url.rstrip("/").split("/")[-1]
            if aid in id_map:
                links.append(arxiv_link(aid, short_title(id_map[aid][1]["title"])))
            else:
                links.append(arxiv_link(aid, aid))
        cards.append(f"<div class='card'><h3>{esc(title)}</h3><p>{esc(claim)}</p><p class='small'>{' · '.join(links)}</p></div>")
    return "\n".join(cards)


def render_topics(insights: dict) -> str:
    cards = []
    for obj in insights.get("research_topics", [])[:3]:
        title = topic_title_ko(obj.get("title", "") + " " + obj.get("claim", ""))
        claim = explain_claim(obj.get("claim", ""))
        cards.append(f"<div class='card topic'><h3>{esc(title)}</h3><p>{esc(claim)}</p></div>")
    if not cards:
        cards.append("<p>저장된 추천 연구주제 JSON이 없어 이번 재생성에서는 별도 주제 제안을 생략했습니다.</p>")
    return "\n".join(cards)


def render_bucket_status(trends: dict, papers: dict[str, list[dict]]) -> str:
    rows = []
    counts = trends.get("buckets") or {}
    for bucket in BUCKETS:
        meta = counts.get(bucket) or Counter(p["badge"] for p in papers.get(bucket, []))
        total = meta.get("total", len(papers.get(bucket, []))) if isinstance(meta, dict) else len(papers.get(bucket, []))
        cv = meta.get("cv", 0) if isinstance(meta, dict) else meta.get("CV", 0)
        ro = meta.get("ro", 0) if isinstance(meta, dict) else meta.get("RO", 0)
        cvro = meta.get("cvro", 0) if isinstance(meta, dict) else meta.get("CV/RO", 0)
        rows.append(f"{BUCKET_ICON[bucket]} {bucket:<20}: {total:>3}편 (CV {cv:>2} / RO {ro:>2} / CV-RO {cvro:>1})")
    return "<div class='bucket-line'>" + esc("\n".join(rows)) + "</div>"


def render_benchmarks(benchmarks: dict) -> str:
    rows = []
    for r in benchmarks.get("results", []):
        paper = str(r.get("paper", ""))
        aid = paper.rstrip("/").split("/")[-1] if paper else ""
        rows.append(
            "<tr>"
            f"<td>{esc(r.get('benchmark', ''))}</td>"
            f"<td>{esc(r.get('metric') or r.get('value_str') or '')}</td>"
            f"<td>{esc(r.get('value') or r.get('value_str') or '')}</td>"
            "<td></td><td></td>"
            f"<td>{arxiv_link(aid, aid) if aid else ''}</td>"
            "</tr>"
        )
    if not rows:
        return ""
    return (
        "<h2>📈 벤치마크 SOTA 추이</h2>"
        "<table class='cluster-table'><thead><tr><th>벤치마크</th><th>메트릭</th><th>이번주 최고</th><th>지난주 최고</th><th>Δ</th><th>논문 링크</th></tr></thead><tbody>"
        + "\n".join(rows)
        + "</tbody></table>"
    )


def render_must_read(ids: list[str], id_map: dict[str, tuple[str, dict]]) -> str:
    cards = []
    for aid in ids[:2]:
        if aid not in id_map:
            continue
        bucket, p = id_map[aid]
        problem, method, meaning, caution = paper_template(p, bucket)
        core = CORE_OVERRIDES.get(aid) or f"{problem} {method} {meaning}"
        cards.append(
            "<div class='paper-card'>"
            f"<h3>{arxiv_link(aid, p['title'])} {badge_html(p.get('badge', '?'))}</h3>"
            f"<p><strong>핵심 주장:</strong> {esc(core)}</p>"
            "<pre><code>입력/상황 x → 핵심 구조 z를 분리하거나 보정 → 행동·생성·평가 결과 y를 다시 측정</code></pre>"
            "<table class='mini-table'><thead><tr><th>확인할 축</th><th>왜 중요한가</th></tr></thead><tbody>"
            f"<tr><td>평가 조건</td><td>{esc(meaning)}</td></tr>"
            f"<tr><td>한계</td><td>{esc(caution)}</td></tr>"
            "</tbody></table>"
            f"<p><strong>우리 랩 영향:</strong> 바로 새 모델을 붙이기보다, 같은 입력에서 실패 조건을 나누어 재는 평가표를 먼저 만들 가치가 있습니다.</p>"
            "</div>"
        )
    return "\n".join(cards)


def render_paper_summaries(papers: dict[str, list[dict]], important: set[str]) -> str:
    chunks = []
    for bucket in BUCKETS:
        ps = papers.get(bucket, [])
        if not ps:
            continue
        chunks.append(f"<h4 class='bucket'>{BUCKET_ICON[bucket]} {esc(bucket)} · {len(ps)}편</h4>")
        for p in ps:
            problem, method, meaning, caution = paper_template(p, bucket)
            pr = "Must-read" if p["arxiv_id"] in important else ("Read" if len(ps) <= 20 else "Skim")
            core = CORE_OVERRIDES.get(p["arxiv_id"]) or f"{problem} {method} {meaning}"
            chunks.append(
                "<div class='mini-paper'>"
                f"<h3>{arxiv_link(p['arxiv_id'], p['title'])} {badge_html(p.get('badge', '?'))} <span class='priority'>{esc(pr)}</span></h3>"
                f"<p class='authors'>{esc(p.get('authors', ''))}</p>"
                f"<p>{esc(core)}</p>"
                "<ul>"
                f"<li><strong>문제:</strong> {esc(problem)}</li>"
                f"<li><strong>방법:</strong> {esc(method)}</li>"
                f"<li><strong>의미:</strong> {esc(meaning)}</li>"
                f"<li><strong>읽을 때 볼 것:</strong> {esc(caution)}</li>"
                "</ul>"
                "</div>"
            )
    return "\n".join(chunks)


def render_risks(important: list[str], id_map: dict[str, tuple[str, dict]]) -> str:
    risks = []
    for aid in important[:3]:
        if aid not in id_map:
            continue
        bucket, p = id_map[aid]
        _, _, meaning, caution = paper_template(p, bucket)
        risks.append(
            f"<div class='risk'><h3>{arxiv_link(aid, short_title(p['title']))}</h3>"
            f"<p>{esc(caution)} 특히 {esc(meaning)}라는 주장은 데이터 split, 비교 baseline, 실패 사례가 충분히 열려 있을 때 더 믿을 수 있습니다.</p></div>"
        )
    return "\n".join(risks)


def render_daily(date_str: str, source_name: str | None = None) -> str:
    source_name = source_name or f"{date_str}.html"
    source_path = POSTS / source_name
    papers = parse_post_snapshot(source_path)
    trends = read_json(ROOT / "trends" / f"{date_str}.json", {})
    insights = read_json(ROOT / "insights" / f"{date_str}.json", {})
    benchmarks = read_json(ROOT / "benchmarks" / f"{date_str}.json", {"results": []})
    id_map = paper_by_id(papers)
    total = sum(len(x) for x in papers.values())
    imp = important_ids(insights, trends, papers)
    imp_set = set(imp)
    top_bucket = max(papers, key=lambda b: len(papers[b])) if total else "Generation"
    thesis = (
        f"{date_str} 재생성본은 저장된 논문 스냅샷 {total}편을 기준으로 다시 읽었습니다. "
        f"가장 두꺼운 축은 {top_bucket}이지만, 핵심은 숫자 자체보다 평가 기준이 더 구체적으로 바뀌고 있다는 점입니다. "
        "새 모델이 무엇을 잘하는지뿐 아니라 언제 실패하고, 그 실패가 실제 배포에서 어떤 의미인지까지 같이 설명하도록 문장을 다시 정리했습니다."
    )
    bench_html = render_benchmarks(benchmarks)
    must = render_must_read(imp, id_map)
    risks = render_risks(imp, id_map)
    return f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>arXiv Daily Briefing — {date_str}</title><style>{CSS}</style></head><body><div class="container">
<a class="home" href="https://gisbi-kim.github.io/arxiv-daily-summary/">← 홈으로</a>
<h1>📄 arXiv Daily Briefing — {date_str} ({weekday(date_str)})</h1>
<div class="meta"><div><strong>재생성 방식:</strong> repo에 저장된 {esc(source_name)} 논문 스냅샷 + trends/insights/benchmarks JSON 기반</div><div><strong>주의:</strong> 과거 날짜의 원본 out/*.json은 repo에 없어, 논문 집합은 저장된 HTML에서 고정했습니다. arXiv /new·/pastweek는 다시 긁지 않았습니다.</div></div>
<div class="thesis"><strong>오늘의 결론:</strong> {esc(thesis)}</div>

<h2>🧩 오늘의 클러스터 지도</h2>
{render_cluster_map(trends, insights, id_map, papers)}

<h2>🔭 주간 동향</h2>
{render_trends(date_str, trends, papers)}

<h2>📐 CV vs RO 대비</h2>
{render_cv_ro(trends)}

<h2>💡 오늘의 인사이트</h2>
{render_insights(insights, id_map)}

<h2>🔬 추천 연구주제</h2>
{render_topics(insights)}

<h2>📊 오늘의 버킷 현황</h2>
{render_bucket_status(trends, papers)}

{bench_html}

{f"<h2>🌟 오늘의 must-read</h2>{must}" if must else ""}

{f"<h2>⚠️ 리스크·한계 필터</h2>{risks}" if risks else ""}

<h2>📄 논문별 요약</h2>
{render_paper_summaries(papers, imp_set)}

<h2>🔗 참고 링크</h2>
<ul><li><a href="https://arxiv.org/list/cs.CV/new">cs.CV/new</a></li><li><a href="https://arxiv.org/list/cs.RO/new">cs.RO/new</a></li><li><a href="https://gisbi-kim.github.io/arxiv-daily-summary/">전체 목록</a></li></ul>
<footer>Regenerated from committed local materials. <a class="home" href="https://gisbi-kim.github.io/arxiv-daily-summary/">← 홈으로</a></footer>
</div></body></html>
"""


def render_weekly(path: Path) -> str:
    data = read_json(path, {})
    date_str = data.get("date") or path.stem
    title = f"arXiv Weekly Briefing — {date_str}"
    themes = data.get("themes", [])
    preds = data.get("predictions", [])
    top5 = data.get("top5", [])
    buckets = data.get("buckets_summary", {})
    theme_html = "\n".join(
        f"<div class='card'><h3>{esc(topic_title_ko(t.get('title','') + ' ' + t.get('summary','')))}</h3><p>{esc(explain_claim(t.get('summary') or t.get('title','')))}</p></div>"
        for t in themes[:5]
    )
    pred_html = "\n".join(
        f"<div class='card topic'><h3>{esc(clean(p.get('title','')))}</h3><p>{esc(explain_claim(p.get('claim','')))}</p><p class='small'>{esc(clean(p.get('rationale','')))}</p></div>"
        for p in preds[:5]
    )
    top_items = []
    for x in top5[:8]:
        url = str(x.get("arxiv") or x.get("paper") or "")
        aid_m = re.search(r"([0-9]{4}\.[0-9]{4,5})", url)
        aid = str(x.get("arxiv_id") or (aid_m.group(1) if aid_m else "")).strip()
        title_x = clean(x.get("title", ""))
        top_items.append(f"<li>{arxiv_link(aid, title_x) if aid else esc(title_x)}</li>")
    top_html = "\n".join(top_items)
    bucket_lines = []
    if isinstance(buckets, dict):
        for k, v in buckets.items():
            if isinstance(v, dict):
                bucket_lines.append(f"{k}: {v.get('total', v.get('count', 0))}편")
            else:
                bucket_lines.append(f"{k}: {v}편")
    return f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><style>{CSS}</style></head><body><div class="container">
<a class="home" href="https://gisbi-kim.github.io/arxiv-daily-summary/">← 홈으로</a>
<h1>📄 arXiv Weekly Briefing — {esc(date_str)} ({weekday(date_str)})</h1>
<div class="meta"><div><strong>주간 시야:</strong> {esc(data.get('week_start',''))} ~ {esc(data.get('week_end',''))}</div><div><strong>재생성 방식:</strong> repo에 저장된 {esc(path.name)} 기반</div></div>
<div class="thesis"><strong>이번 주 결론:</strong> 이번 주 요약은 기술 이름을 길게 나열하기보다, 어떤 평가 기준과 실패 조건이 새로 중요해졌는지를 중심으로 다시 썼습니다. 독자가 다시 묻지 않도록 각 주장 뒤에는 그 말이 실제로 뜻하는 바를 한 문장 더 붙였습니다.</div>
<h2>🔭 주간 동향</h2>{theme_html or '<p>저장된 주간 theme 자료가 없습니다.</p>'}
<h2>💡 다음 주 예측</h2>{pred_html or '<p>저장된 예측 자료가 없습니다.</p>'}
<h2>🌟 주간 핵심 논문</h2><ul>{top_html}</ul>
<h2>📊 버킷 현황</h2><div class="bucket-line">{esc(chr(10).join(bucket_lines) or '저장된 버킷 요약 없음')}</div>
<h2>🔗 참고 링크</h2><ul><li><a href="https://gisbi-kim.github.io/arxiv-daily-summary/">전체 목록</a></li></ul>
<footer>Regenerated from committed local materials. <a class="home" href="https://gisbi-kim.github.io/arxiv-daily-summary/">← 홈으로</a></footer>
</div></body></html>
"""


def render_weekly_from_post(path: Path) -> str:
    source = path.read_text(encoding="utf-8")
    date_m = re.search(r"(20[0-9]{2}-[0-9]{2}-[0-9]{2})", path.name)
    date_str = date_m.group(1) if date_m else path.stem
    links = []
    seen = set()
    for aid, title in re.findall(r'href="https://arxiv\.org/abs/([0-9.]+)"[^>]*>(.*?)</a>', source, re.S):
        if aid in seen:
            continue
        seen.add(aid)
        links.append((aid, clean(title)))
    headings = [clean(x) for x in re.findall(r"<h[23][^>]*>(.*?)</h[23]>", source, re.S)]
    themes = [h for h in headings if h and "참고" not in h and "링크" not in h][:5]
    theme_html = "\n".join(
        f"<div class='card'><h3>{esc(topic_title_ko(t))}</h3><p>{esc(explain_claim(t))}</p></div>"
        for t in themes
    )
    top_html = "\n".join(f"<li>{arxiv_link(aid, title)}</li>" for aid, title in links[:12])
    return f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>arXiv Weekly Briefing — {date_str}</title><style>{CSS}</style></head><body><div class="container">
<a class="home" href="https://gisbi-kim.github.io/arxiv-daily-summary/">← 홈으로</a>
<h1>📄 arXiv Weekly Briefing — {date_str} ({weekday(date_str)})</h1>
<div class="meta"><div><strong>재생성 방식:</strong> repo에 저장된 {esc(path.name)} HTML에서 제목과 논문 링크를 스냅샷으로 추출</div><div><strong>주의:</strong> 해당 주간의 별도 weekly JSON은 repo에 없어, 기존 weekly HTML을 원천 재료로 고정했습니다.</div></div>
<div class="thesis"><strong>이번 주 결론:</strong> 이 주간 회고는 남아 있는 HTML 스냅샷만으로 다시 만들었습니다. 그래서 새 논문을 추가로 찾지는 않고, 기존에 공개됐던 논문 링크와 주제 제목을 기준으로 문장을 더 설명적으로 풀었습니다.</div>
<h2>🔭 주간 동향</h2>{theme_html or '<p>기존 HTML에서 추출 가능한 주간 제목이 많지 않아, 아래 핵심 논문 목록 중심으로 읽으면 됩니다.</p>'}
<h2>🌟 주간 핵심 논문</h2><ul>{top_html}</ul>
<h2>🔗 참고 링크</h2><ul><li><a href="https://gisbi-kim.github.io/arxiv-daily-summary/">전체 목록</a></li></ul>
<footer>Regenerated from committed local materials. <a class="home" href="https://gisbi-kim.github.io/arxiv-daily-summary/">← 홈으로</a></footer>
</div></body></html>
"""


CSS = r"""
*,*::before,*::after{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif;background:#f6f7f9;color:#1f2328;line-height:1.72;font-size:15px;padding:32px 16px;word-break:keep-all}
.container{max-width:980px;margin:0 auto;background:#fff;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.06),0 1px 2px rgba(0,0,0,.04);padding:40px 48px}
h1{font-size:28px;margin:0 0 6px;color:#0d1117}h2{font-size:21px;margin:40px 0 14px;padding-bottom:8px;border-bottom:2px solid #e5e7eb}h3{font-size:17px;margin:18px 0 8px}h4.bucket{font-size:18px;margin:28px 0 10px;color:#0f172a}p{margin:0 0 14px}a{color:#0969da;text-decoration:none}a:hover{text-decoration:underline}
.home{display:inline-block;padding:6px 14px;font-size:13px;color:#0969da;background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;text-decoration:none;margin:0 0 18px}
.meta{font-size:13px;color:#3b434d;padding:14px 18px;background:#f6f8fa;border-left:3px solid #0969da;border-radius:6px;margin:14px 0 22px}.meta div{margin:2px 0}
.thesis{background:#0f172a;color:#f8fafc;border-radius:10px;padding:18px 22px;margin:16px 0 28px;font-size:16px}.thesis strong{color:#fef08a}
.card,.paper-card,.risk{background:#fafbfc;border:1px solid #e5e7eb;border-radius:8px;padding:14px 18px;margin:12px 0}.paper-card{border-left:4px solid #0ea5e9}.risk{border-left:4px solid #ef4444;background:#fef2f2}.topic{border-left:4px solid #22c55e;background:#f0fdf4}
.cluster-table,.mini-table{width:100%;border-collapse:collapse;font-size:13px;margin:12px 0 18px}.cluster-table th,.cluster-table td,.mini-table th,.mini-table td{border:1px solid #d0d7de;padding:9px;vertical-align:top}.cluster-table th,.mini-table th{background:#f6f8fa;color:#0d1117}
.bucket-line{font-family:ui-monospace,SFMono-Regular,Consolas,Menlo,monospace;background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;padding:10px 14px;font-size:13px;white-space:pre;overflow-x:auto}
.badge{display:inline-block;font-size:11px;font-weight:600;padding:1px 8px;border-radius:10px;margin-left:6px;vertical-align:middle;font-family:ui-monospace,monospace}.cv{background:#ddf4ff;color:#0550ae;border:1px solid #54aeff}.ro{background:#fff8c5;color:#7a4e00;border:1px solid #d4a72c}.cvro{background:#ffe5d9;color:#9a3412;border:1px solid #f59e0b}.x{background:#f3f4f6;color:#6b7280;border:1px solid #d1d5db}
.mini-paper{padding:14px 0;border-top:1px solid #edf2f7}.mini-paper:first-of-type{border-top:none}.mini-paper h3{margin:0 0 4px}.mini-paper ul{margin:7px 0 0;padding-left:20px}.mini-paper li{margin:3px 0;line-height:1.55}.authors,.small{display:block;color:#475569;font-size:13.5px;margin-top:4px}.priority{font-size:12px;color:#7c2d12;margin-left:6px}
pre{background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;padding:10px;overflow-x:auto;font-size:13px}
footer{margin-top:40px;padding-top:16px;border-top:1px solid #eaeef2;font-size:12px;color:#656d76;text-align:center}
@media(max-width:760px){body{padding:16px 8px}.container{padding:24px 20px}.cluster-table{font-size:12.5px}}
"""


def daily_dates() -> list[str]:
    dates = []
    for path in sorted(POSTS.glob("2026-??-??.html")):
        dates.append(path.stem)
    return dates


def main(argv: list[str]) -> int:
    args = argv[1:]
    if args:
        dates = [x for x in args if not x.endswith("-weekly")]
    else:
        dates = daily_dates()
    for date_str in dates:
        out = POSTS / f"{date_str}.html"
        out.write_text(render_daily(date_str), encoding="utf-8", newline="\n")
        print(f"wrote {out}")

    # Keep the visible v2 comparison URL alive, regenerated from the same 2026-05-08 material.
    if (POSTS / "2026-05-08.html").exists():
        (POSTS / "2026-05-08-quality-v2.html").write_text(
            render_daily("2026-05-08", "2026-05-08.html"), encoding="utf-8", newline="\n"
        )
        print("wrote posts/2026-05-08-quality-v2.html")

    for weekly_path in sorted((ROOT / "weekly").glob("*.json")):
        data = read_json(weekly_path, {})
        date_str = data.get("date")
        if date_str:
            out = POSTS / f"{date_str}-weekly.html"
            out.write_text(render_weekly(weekly_path), encoding="utf-8", newline="\n")
            print(f"wrote {out}")
    for weekly_post in sorted(POSTS.glob("2026-??-??-weekly.html")):
        m = re.search(r"(20[0-9]{2}-[0-9]{2}-[0-9]{2})-weekly", weekly_post.name)
        date_str = m.group(1) if m else ""
        if (ROOT / "weekly" / f"{Date.fromisoformat(date_str).isocalendar().year}-W{Date.fromisoformat(date_str).isocalendar().week:02d}.json").exists():
            continue
        weekly_post.write_text(render_weekly_from_post(weekly_post), encoding="utf-8", newline="\n")
        print(f"wrote {weekly_post}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
