#!/usr/bin/env python3
"""Regenerate older daily briefings from the already-published paper snapshot.

This intentionally does not revisit arxiv.org /new or /pastweek.  The paper set
comes from the existing posts/YYYY-MM-DD.html file, which is the safest
available snapshot when out/*.json was not committed.
"""
from __future__ import annotations

import ast
import html
import io
import json
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
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
EMOJI = {
    "3D/Scene": "📦",
    "Robot Learning": "🤖",
    "Autonomous Driving": "🚗",
    "Foundation Models": "🧠",
    "Generation": "🎨",
    "Efficiency/Systems": "⚡",
    "Embodied AI": "🏃",
    "Safety/Alignment": "🛡️",
}
WEEKDAY = {
    "2026-05-06": "수",
    "2026-05-07": "목",
}


def esc(s) -> str:
    return html.escape(str(s or ""), quote=False)


def clean_text(s: str) -> str:
    s = html.unescape(s or "")
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def naturalize_ko(s: str) -> str:
    """Reduce internal memo / translationese phrasing in old curated notes."""
    s = clean_text(s)
    replacements = [
        ("둘이 한 batch에 표면화한 건", "두 논문이 같은 날 나온 건"),
        ("한 batch에 표면화한 건", "같은 날 함께 나온 건"),
        ("같은 batch에 표면화", "같은 날 같이 등장"),
        ("동시 표면화", "같이 드러남"),
        ("batch에 동시", "하루치 안에 같이"),
        ("batch에", "하루치에"),
        ("batch", "하루치"),
        ("정조준하고", "직접 다루고"),
        ("정조준한", "직접 다룬"),
        ("정조준해요", "직접 다룹니다"),
        ("정조준", "직접 다룸"),
        ("표면화한", "드러난"),
        ("표면화한 자리", "흐름이 드러난 대목"),
        ("표면화한 모양", "드러난 모습"),
        ("표면화했습니다", "드러났습니다"),
        ("표면화했어요", "드러났어요"),
        ("표면화", "드러남"),
        ("실험적인 압력이 걸려 있습니다", "실험 쪽 비중이 더 큽니다"),
        ("실험적 압력이 걸려 있습니다", "실험 쪽 비중이 더 큽니다"),
        ("압력이 걸려 있습니다", "비중이 큽니다"),
        ("paradigm-defining", "흐름을 바꿀 만한"),
        ("World Model evaluation", "World Model 평가"),
        ("World Model 평가이", "World Model 평가가"),
        ("interactive bench", "interactive 벤치마크"),
        ("systematic study", "체계적 비교"),
        ("formulation-task correspondence", "문제 설정과 작업 종류의 대응 관계"),
        ("formulation이", "문제 설정이"),
        ("formulation", "문제 설정"),
        ("처음 체계적인 정리됨", "처음 체계적으로 정리됨"),
        ("단계 진입", "단계에 들어섬"),
        ("단계에 들어섬 —", "단계에 들어섰고,"),
        ("연구 흐름으로 전환", "연구 흐름으로 전환됐다는 것"),
        ("처음 정량", "처음 정량화됐다는 것"),
        ("current policy가 자기 자신과 play해 self-improvement", "현재 policy가 자기 자신과 경쟁하면서 개선되는 방식"),
        ("current policy가 자기와 play해 self-improvement", "현재 policy가 자기 자신과 경쟁하면서 개선되는 방식"),
        ("game-theoretic", "게임 이론 기반"),
        ("reframe", "다시 정의"),
        ("surge", "증가"),
        ("formal하게", "명시적으로"),
        ("formal", "명시적"),
        ("systematic", "체계적인"),
        ("paradigm 측", "연구 흐름상"),
        ("paradigm", "연구 흐름"),
        ("substrate 측", "기반 구조 쪽"),
        ("substrate", "기반 구조"),
        ("audit 대상", "점검해야 할 지점"),
        ("audit 가치", "점검 가치"),
        ("audit", "점검"),
        ("layer", "층위"),
        ("strict win", "분명히 이기는지"),
        ("reference로", "기준점으로"),
        ("reference가", "기준점이"),
        ("community standard", "커뮤니티 표준"),
        ("메타가 같은", "큰 문제의식이 같은"),
        ("메타에서", "큰 문제의식에서"),
        ("메타를", "큰 흐름을"),
        ("메타", "큰 흐름"),
        ("측 결이에요", "쪽에서 의미가 있습니다"),
        ("측 결입니다", "쪽에서 의미가 있습니다"),
        ("측 결", "쪽 관찰점"),
        ("응용 결처럼", "응용 논문처럼"),
        ("응용 결이지만", "응용 논문이지만"),
        ("응용 결", "응용 논문"),
        ("결 총집결", "논문이 몰림"),
        ("BT model 측 가정 깬", "BT 모델의 가정을 넘어서려는"),
        ("측 가정", "의 가정"),
        ("측면 첫", "측면에서 첫"),
        ("결이에요", "대목이에요"),
        ("결입니다", "대목입니다"),
        ("자리예요", "대목이에요"),
        ("자리입니다", "대목입니다"),
        ("자리.", "대목."),
        ("SR", "success rate"),
    ]
    for old, new in replacements:
        s = s.replace(old, new)
    s = re.sub(r"\breference\b", "기준점", s)
    s = re.sub(r"\bcommunity\b", "연구 커뮤니티", s)
    s = re.sub(r"\baudit\b", "점검", s)
    s = s.replace("연구 흐름으로 전환라는", "연구 흐름으로 전환됐다는")
    s = s.replace("정량화됐다는 것라는", "정량화됐다는")
    s = s.replace("평가이", "평가가")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def explain_plain(s: str) -> str:
    """Rewrite dense research shorthand into a self-contained Korean explanation."""
    text = naturalize_ko(s)
    low = text.lower()
    if (
        ("world model" in low or "wm eval" in low or "robot video wm" in low)
        and (
            "reconstruction loss" in low
            or "reconstruction/perceptual" in low
            or "reward alignment" in low
            or "reward-aligned" in low
            or "interactive" in low
        )
    ):
        return (
            "예전에는 World Model을 '미래 영상을 얼마나 그럴듯하게 복원하거나 예측하느냐'로 많이 평가했는데, "
            "이제는 '그 예측이 로봇 행동 성공에 실제로 도움이 되느냐'와 "
            "'상호작용 상황에서 계속 쓸 수 있느냐'가 더 중요해지고 있다는 뜻입니다."
        )
    if "latent action supervision" in low or "image-based vs action-based" in low:
        return (
            "VLA를 학습시킬 때 행동을 그대로 맞히게 할지, 아니면 이미지 변화 속에 숨어 있는 행동 단서를 먼저 배우게 할지의 차이를 "
            "본격적으로 비교하기 시작했다는 뜻입니다. 쉽게 말하면 '로봇에게 정답 행동을 외우게 할 것인가, "
            "장면이 어떻게 변해야 하는지를 먼저 이해하게 할 것인가'를 나눠 보기 시작한 겁니다."
        )
    if "diffusion alignment" in low and ("nash" in low or "bt" in low or "preference" in low):
        return (
            "diffusion 모델을 사람 취향에 맞추는 방식이 단순한 선호도 점수 맞추기에서 벗어나고 있다는 뜻입니다. "
            "이제는 모델이 여러 후보를 서로 비교하고 스스로 더 나은 방향을 찾게 만드는 쪽으로 평가와 학습 방식이 옮겨가고 있습니다."
        )
    if "4d world model" in low or "lovif" in low or "physcore" in low:
        return (
            "4D World Model을 볼 때 단순히 영상이 예쁜지보다, 시간에 따라 물리적으로 말이 되는지와 조건을 잘 따르는지를 "
            "함께 평가하려는 흐름입니다. 즉 '그럴듯한 동영상'이 아니라 '물리적으로 믿을 수 있는 시뮬레이션'인지 묻는 쪽으로 가고 있습니다."
        )
    if "understanding-generation gap" in low:
        return (
            "VLM이 이미지를 이해하거나 틀린 점을 지적하는 능력은 꽤 좋은데, 정작 그 이해를 바탕으로 원하는 이미지를 정확히 생성하는 데는 "
            "아직 간극이 있다는 뜻입니다. 그래서 '잘 보는 모델'을 '잘 만드는 모델'로 어떻게 연결할지가 핵심 문제가 됩니다."
        )
    return text


def sentence_split(text: str) -> list[str]:
    text = naturalize_ko(text)
    if not text:
        return []
    parts = re.split(r"(?<=[.!?。])\s+|(?<=요\.)\s+|(?<=다\.)\s+|(?<=임\.)\s+", text)
    return [p.strip(" -—") for p in parts if p.strip(" -—")]


def first_sentence(text: str, limit: int = 230) -> str:
    parts = sentence_split(text)
    out = parts[0] if parts else clean_text(text)
    if len(out) > limit:
        out = out[: limit - 1].rstrip() + "…"
    return out


def sentence_with(text: str, keywords: list[str], default_idx: int = 0, limit: int = 230) -> str:
    parts = sentence_split(text)
    lowered = [(p, p.lower()) for p in parts]
    for p, low in lowered:
        if any(k.lower() in low for k in keywords):
            out = p
            break
    else:
        out = parts[min(default_idx, len(parts) - 1)] if parts else clean_text(text)
    if len(out) > limit:
        out = out[: limit - 1].rstrip() + "…"
    return out


def load_json(path: Path, default):
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def parse_published_post(date: str) -> dict[str, list[dict]]:
    path = ROOT / "posts" / f"{date}.html"
    raw = path.read_text(encoding="utf-8")
    if '<div class="paper">' not in raw:
        for ref in ["HEAD"] + [f"HEAD~{i}" for i in range(1, 12)]:
            try:
                candidate = subprocess.check_output(
                    ["git", "show", f"{ref}:posts/{date}.html"],
                    cwd=ROOT,
                    text=True,
                    encoding="utf-8",
                )
            except Exception:
                continue
            if '<div class="paper">' in candidate:
                raw = candidate
                break
    result = {b: [] for b in BUCKETS}
    for i, bucket in enumerate(BUCKETS):
        marker = re.search(rf"<h4[^>]*>(?:(?!</h4>).)*{re.escape(bucket)}(?:(?!</h4>).)*</h4>", raw, re.S)
        if not marker:
            continue
        start = marker.end()
        next_starts = []
        for nb in BUCKETS[i + 1 :]:
            m = re.search(rf"<h4[^>]*>(?:(?!</h4>).)*{re.escape(nb)}(?:(?!</h4>).)*</h4>", raw[start:], re.S)
            if m:
                next_starts.append(start + m.start())
        h2 = re.search(r"<h2[^>]*>🔗 참고 링크", raw[start:], re.S)
        if h2:
            next_starts.append(start + h2.start())
        end = min(next_starts) if next_starts else len(raw)
        section = raw[start:end]
        for block in re.findall(r'<div class="paper">(.*?)(?=<div class="paper">|$)', section, re.S):
            aid_m = re.search(r"https://arxiv\.org/abs/([0-9.]+)", block)
            title_m = re.search(r"<strong>(.*?)</strong>", block, re.S)
            badge_m = re.search(r'<span class="badge[^"]*">(CV/RO|CV|RO)</span>', block)
            author_m = re.search(r'<div class="paper-authors">(.*?)</div>', block, re.S)
            summary_m = re.search(r"<p>(.*?)</p>", block, re.S)
            if not aid_m:
                continue
            result[bucket].append(
                {
                    "arxiv_id": aid_m.group(1),
                    "title": clean_text(title_m.group(1) if title_m else aid_m.group(1)),
                    "badge": badge_m.group(1) if badge_m else "?",
                    "authors_line": clean_text(author_m.group(1) if author_m else "").replace("👥", "").strip(),
                    "summary": clean_text(summary_m.group(1) if summary_m else ""),
                }
            )
    return result


def load_curated_summaries(date: str) -> dict[str, str]:
    script = ROOT / "scripts" / f"gen_html_{date.replace('-', '')}.py"
    if not script.exists():
        return {}
    tree = ast.parse(script.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            names = [t.id for t in node.targets if isinstance(t, ast.Name)]
            if "PAPER_SUMMARIES" in names:
                return ast.literal_eval(node.value)
    return {}


def arxiv_api(ids: list[str]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for i in range(0, len(ids), 50):
        batch = ids[i : i + 50]
        query = urllib.parse.urlencode({"id_list": ",".join(batch)})
        url = f"https://export.arxiv.org/api/query?{query}"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "arxiv-daily-summary-regenerator/1.0"},
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                xml = resp.read()
        except Exception as e:
            print(f"[warn] arXiv API batch failed ({batch[0]}..): {e}")
            continue
        root = ET.fromstring(xml)
        ns = {"a": "http://www.w3.org/2005/Atom"}
        for entry in root.findall("a:entry", ns):
            id_text = entry.findtext("a:id", default="", namespaces=ns)
            aid = id_text.rstrip("/").split("/")[-1]
            title = clean_text(entry.findtext("a:title", default="", namespaces=ns))
            abstract = clean_text(entry.findtext("a:summary", default="", namespaces=ns))
            authors = [clean_text(a.findtext("a:name", default="", namespaces=ns)) for a in entry.findall("a:author", ns)]
            out[aid] = {"title": title, "abstract": abstract, "authors": [a for a in authors if a]}
        time.sleep(0.2)
    return out


def merge_metadata(papers_by_bucket: dict[str, list[dict]], curated: dict[str, str], meta: dict[str, dict]) -> None:
    for papers in papers_by_bucket.values():
        for p in papers:
            aid = p["arxiv_id"]
            m = meta.get(aid, {})
            if m.get("title"):
                p["title"] = m["title"]
            if m.get("authors"):
                p["authors"] = m["authors"]
                p["authors_line"] = ", ".join(m["authors"][:3]) + (" et al." if len(m["authors"]) > 3 else "")
            else:
                p["authors"] = [p.get("authors_line", "").replace(" et al.", "")]
            p["abstract"] = m.get("abstract", "")
            if curated.get(aid):
                p["summary"] = curated[aid]


def ids_from_insights(insights: dict, trends: dict, benchmarks: dict) -> set[str]:
    ids: set[str] = set()
    for obj in insights.get("insights", []) + trends.get("hottest", []) + trends.get("cooling", []):
        for url in obj.get("papers", []) if "papers" in obj else obj.get("evidence", []):
            m = re.search(r"([0-9]{4}\.[0-9]{4,5})", str(url))
            if m:
                ids.add(m.group(1))
    for r in benchmarks.get("results", []):
        m = re.search(r"([0-9]{4}\.[0-9]{4,5})", str(r.get("paper", "")))
        if m:
            ids.add(m.group(1))
    return ids


def priority_for(p: dict, bucket: str, important_ids: set[str]) -> str:
    aid = p["arxiv_id"]
    text = f"{p.get('title','')} {p.get('summary','')} {p.get('abstract','')}".lower()
    if aid in important_ids:
        return "Must-read"
    strong = ["benchmark", "dataset", "sota", "state-of-the-art", "paradigm", "world model", "vla", "safety", "uncertainty", "calibration", "diffusion", "4d", "3dgs"]
    if sum(k in text for k in strong) >= 2:
        return "Read"
    if bucket in {"Generation", "Efficiency/Systems", "Safety/Alignment", "Robot Learning"} and sum(k in text for k in strong) >= 1:
        return "Read"
    return "Skim-only"


def tag_for(p: dict, bucket: str) -> str:
    text = f"{p.get('title','')} {p.get('summary','')} {p.get('abstract','')}".lower()
    tags = []
    if any(k in text for k in ["benchmark", "dataset", "leaderboard", "survey", "atlas"]):
        tags.append("인프라")
    if any(k in text for k in ["failure", "risk", "safety", "uncertainty", "calibration", "ood", "attack", "robust", "bias"]):
        tags.append("경고신호")
    if any(k in text for k in ["gap", "reframe", "reformulat", "paradigm", "towards", "why", "what makes"]):
        tags.append("문제정의")
    if any(k in text for k in ["routing", "distillation", "flow", "diffusion", "expert", "lora", "token", "latent", "reward", "alignment"]):
        tags.append("방법전환")
    if not tags:
        tags.append("인프라" if bucket in {"3D/Scene", "Embodied AI"} else "방법전환")
    return " ".join(f"[{t}]" for t in tags[:2])


def appendix_bullets(p: dict, bucket: str, priority: str) -> list[str]:
    text = p.get("summary") or p.get("abstract") or p.get("title", "")
    title = p.get("title", "")
    issue = sentence_with(
        text,
        ["문제", "한계", "fail", "gap", "mismatch", "bottleneck", "부재", "진단", "shift", "bias", "직접 다룸", "다룬"],
        0,
    )
    method = sentence_with(
        text,
        ["도입", "제안", "처방", "framework", "model", "benchmark", "dataset", "reframe", "alignment", "distillation", "token", "latent", "reward"],
        1,
    )
    meaning = sentence_with(
        text,
        ["paradigm", "표준", "후보", "흐름", "자리", "가치", "audit", "reference", "community", "후속"],
        max(0, len(sentence_split(text)) - 1),
    )
    if issue == method and p.get("abstract"):
        method = sentence_with(p["abstract"], ["we propose", "we introduce", "method", "framework", "model"], 0)
    if issue == method:
        low = f"{title} {text}".lower()
        if any(k in low for k in ["benchmark", "dataset", "leaderboard"]):
            method = "저자들은 failure mode가 드러나도록 데이터 구성, 평가 프로토콜, 비교 축을 새로 잡았습니다."
        elif any(k in low for k in ["4d", "3d", "gaussian", "splat", "reconstruction"]):
            method = "저자들은 3D/4D 표현, geometry prior, multi-view signal을 결합해 기존 재구성 과정을 보강했습니다."
        elif any(k in low for k in ["vla", "robot", "manipulation", "policy", "control"]):
            method = "저자들은 policy가 바로 action을 내기보다 latent/action/reward 구조를 분리해 학습과 실행을 안정화합니다."
        elif any(k in low for k in ["diffusion", "flow", "generation", "video"]):
            method = "저자들은 diffusion·flow·generation 과정에 조건부 제어, distillation, reward feedback 중 하나를 새 조정 축으로 넣었습니다."
        else:
            method = "저자들은 기존 처리 과정의 병목을 분리하고, 중간 표현이나 평가축을 추가해 그 병목을 직접 조정합니다."
    if meaning in {issue, method} and bucket:
        meaning = f"{bucket} 흐름 안에서는 단독 성능보다 오늘 하루치 논문에서 반복해서 보이는 신호를 보강하는 근거로 읽는 게 맞습니다."
    bullets = [
        f"문제: {issue}",
        f"방법: {method}",
        f"의미: {meaning}",
    ]
    if priority == "Skim-only":
        bullets.append("주의: ROI에는 걸리지만 오늘 핵심 묶음과의 연결은 약해서 우선순위는 낮게 둡니다.")
    elif any(k in f"{title} {text}".lower() for k in ["benchmark", "dataset", "sota", "state-of-the-art"]):
        bullets.append("주의: 데이터 split, baseline 강도, metric 정의를 본문에서 확인하기 전까지 일반화 claim은 보류합니다.")
    else:
        bullets.append("주의: abstract와 기존 요약 기반 재해석이므로 핵심 ablation과 failure case는 본문 확인이 필요합니다.")
    bullets.append(f"우선순위: {priority}.")
    return bullets


def badge_html(b: str) -> str:
    cls = {"CV": "cv", "RO": "ro", "CV/RO": "cvro"}.get(b, "x")
    return f'<span class="badge {cls}">{esc(b)}</span>'


def link(aid: str, label: str | None = None) -> str:
    return f'<a href="https://arxiv.org/abs/{aid}" target="_blank" rel="noopener">{esc(label or aid)}</a>'


def paper_label(aid: str, all_papers: dict[str, dict]) -> str:
    title = all_papers.get(aid, {}).get("title", aid)
    short = re.split(r"[:：]", title)[0]
    return short[:48] + ("…" if len(short) > 48 else "")


def render_cluster_table(trends: dict, insights: dict, all_papers: dict[str, dict]) -> str:
    rows = []
    topics = trends.get("hottest", [])[:4]
    if not topics:
        topics = [{"topic": x.get("title", ""), "note": x.get("claim", ""), "evidence": [u.split("/")[-1] for u in x.get("papers", [])]} for x in insights.get("insights", [])[:4]]
    for item in topics:
        ids = []
        for x in item.get("evidence", []) or item.get("papers", []):
            m = re.search(r"([0-9]{4}\.[0-9]{4,5})", str(x))
            if m:
                ids.append(m.group(1))
        reps = ", ".join(link(aid, paper_label(aid, all_papers)) for aid in ids[:4]) or "관련 논문 없음"
        note = item.get("note") or item.get("claim") or ""
        conf = "High" if len(ids) >= 2 else "Medium"
        lab = "평가축·baseline·failure case를 먼저 표로 고정"
        topic = naturalize_ko(item.get("topic", ""))
        why = explain_plain(item.get("note") or item.get("claim") or item.get("topic", ""))
        rows.append(
            "<tr>"
            f"<td><strong>{esc(topic)}</strong></td>"
            f"<td>{reps}</td>"
            f"<td>{esc(why)}</td>"
            f"<td><span class='conf {conf}'>{conf}</span></td>"
            f"<td>{esc(lab)}</td>"
            "</tr>"
        )
    return "<table class='cluster-table'><thead><tr><th>Cluster</th><th>대표 논문</th><th>왜 중요?</th><th>Confidence</th><th>Lab action</th></tr></thead><tbody>" + "\n".join(rows) + "</tbody></table>"


def render_trends(trends: dict) -> str:
    buckets = trends.get("buckets", {})
    past = trends.get("buckets_pastweek", {})
    delta = trends.get("vs_7d_prior", {}).get("pastweek_buckets_delta_pct", {})
    top_today = sorted(buckets.items(), key=lambda kv: kv[1].get("total", 0), reverse=True)[:3]
    hot = trends.get("hottest", [])
    cool = trends.get("cooling", [])
    p1 = "오늘 단일 배치에서는 " + ", ".join(f"{k} {v.get('total',0)}편" for k, v in top_today) + "이 제일 두꺼웠습니다. "
    if hot:
        p1 += f"근데 숫자보다 중요한 건 {naturalize_ko(hot[0]['topic'])} 쪽이에요. {explain_plain(hot[0].get('note') or hot[0].get('topic',''))}"
    p2 = "주간 rolling window로 보면 "
    if past:
        top_past = sorted(past.items(), key=lambda kv: kv[1].get("total", 0), reverse=True)[:3]
        p2 += ", ".join(f"{k} {v.get('total',0)}편" + (f" ({delta.get(k)})" if delta.get(k) else "") for k, v in top_past)
        p2 += "이 상위권입니다. "
    if cool:
        p2 += f"반대로 조용한 쪽은 {naturalize_ko(cool[0]['topic'])}인데, 이건 완전히 비었다기보다 다음 묶음에서 다시 올라올 수 있는 흔들림으로 보는 게 맞겠습니다."
    p3 = "오늘 논문들을 그 맥락 위에 놓으면, 개별 SOTA보다 평가 프로토콜·latent 기반 구조·배포 안정성처럼 실험판 자체를 다시 짜는 논문들이 더 중요해 보여요. "
    if len(hot) > 1:
        p3 += f"특히 {naturalize_ko(hot[1]['topic'])} 흐름은 후속 2~4주 동안 기준점으로 남을 가능성이 큽니다."
    return f"<p>{esc(p1)}</p><p>{esc(p2)}</p><p>{esc(p3)}</p>"


def render_cv_ro(trends: dict) -> str:
    cv = trends.get("keywords_cv", [])[:5]
    ro = trends.get("keywords_ro", [])[:5]
    common = [x for x, _ in cv if x in {y for y, _ in ro}]
    cv_only = [x for x, _ in cv if x not in common][:3]
    ro_only = [x for x, _ in ro if x not in common][:3]
    p = "CV와 RO를 나눠 보면, CV는 여전히 video·diffusion·VLM 쪽 어휘가 두껍고 RO는 manipulation·navigation·robustness처럼 실제 로봇 실험과 배포에 가까운 단어가 더 자주 보입니다. "
    p += "재밌는 건 공통 키워드라도 CV에서는 표현·생성·평가 문제로, RO에서는 policy·control·deployment 문제로 번역된다는 점이에요."
    rows = [
        f"<li><strong>공통으로 뜨는 단어:</strong> {esc(', '.join(common) or 'robust / video 계열')}</li>",
        f"<li><strong>CV 쪽 편향:</strong> {esc(', '.join(cv_only) or 'video, diffusion, transformer')}</li>",
        f"<li><strong>RO 쪽 편향:</strong> {esc(', '.join(ro_only) or 'manipulation, navigation, vla')}</li>",
        "<li><strong>같은 단어 다른 맥락:</strong> diffusion은 CV에선 generation·distillation, RO에선 planning·policy improvement 쪽으로 읽힙니다.</li>",
    ]
    return f"<p>{esc(p)}</p><ul>{''.join(rows)}</ul>"


def render_insights(insights: dict, all_papers: dict[str, dict]) -> str:
    cards = []
    for obj in insights.get("insights", []):
        links = []
        for u in obj.get("papers", []):
            aid = u.rstrip("/").split("/")[-1]
            links.append(link(aid, paper_label(aid, all_papers)))
        cards.append(f"<div class='card'><h3>{esc(naturalize_ko(obj.get('title','')))}</h3><p>{esc(explain_plain(obj.get('claim') or obj.get('title','')))}</p><p class='small'>{' · '.join(links)}</p></div>")
    return "\n".join(cards)


def render_topics(insights: dict) -> str:
    cards = []
    for obj in insights.get("research_topics", []):
        cards.append(f"<div class='card topic'><h3>{esc(naturalize_ko(obj.get('title','')))}</h3><p>{esc(naturalize_ko(obj.get('claim','')))}</p></div>")
    return "\n".join(cards)


def render_benchmarks(benchmarks: dict) -> str:
    rows = []
    for r in benchmarks.get("results", []):
        paper = r.get("paper", "")
        aid = paper.rstrip("/").split("/")[-1] if paper else ""
        rows.append(
            "<tr>"
            f"<td>{esc(naturalize_ko(r.get('benchmark','')))}</td>"
            f"<td>{esc(naturalize_ko(r.get('metric') or r.get('value_str','')))}</td>"
            f"<td>{esc(naturalize_ko(r.get('value') or r.get('value_str','')))}</td>"
            f"<td>{link(aid, r.get('paper_title') or aid) if aid else ''}</td>"
            "</tr>"
        )
    if not rows:
        return ""
    return "<table class='cluster-table'><thead><tr><th>벤치마크</th><th>메트릭</th><th>이번주 보고</th><th>논문</th></tr></thead><tbody>" + "\n".join(rows) + "</tbody></table>"


def render_bucket_status(trends: dict) -> str:
    lines = []
    delta = trends.get("vs_7d_prior", {}).get("pastweek_buckets_delta_pct", {})
    for b in BUCKETS:
        v = trends.get("buckets", {}).get(b, {})
        extra = f" · 지난주 대비 {delta[b]}" if b in delta else ""
        lines.append(f"{EMOJI[b]} {b:<20}: {v.get('total',0):>3}편 (CV {v.get('cv',0):>2} / RO {v.get('ro',0):>2} / CV-RO {v.get('cvro',0):>1}){extra}")
    return "<div class='bucket-line'>" + esc("\n".join(lines)) + "</div>"


def render_appendix(papers_by_bucket: dict[str, list[dict]], important_ids: set[str]) -> str:
    chunks = []
    for b in BUCKETS:
        papers = papers_by_bucket.get(b, [])
        chunks.append(f"<details><summary>{EMOJI[b]} {esc(b)} · {len(papers)}편</summary>")
        if not papers:
            chunks.append("<p class='small'>오늘 하루치에는 ROI와 맞는 논문이 없습니다.</p>")
        for p in papers:
            pr = priority_for(p, b, important_ids)
            tag = tag_for(p, b)
            bullets = "".join(f"<li>{esc(x)}</li>" for x in appendix_bullets(p, b, pr))
            chunks.append(
                f"<div class='mini-paper'><strong>{link(p['arxiv_id'], p['title'])}</strong> {badge_html(p.get('badge','?'))} "
                f"<span class='tag'>{esc(tag)} [{esc(pr)}]</span>"
                f"<span class='why'>{esc(p.get('authors_line',''))}</span><ul>{bullets}</ul></div>"
            )
        chunks.append("</details>")
    return "\n".join(chunks)


def render_skim(papers_by_bucket: dict[str, list[dict]], important_ids: set[str]) -> str:
    skims = []
    for b, papers in papers_by_bucket.items():
        for p in papers:
            if priority_for(p, b, important_ids) == "Skim-only":
                skims.append((b, p))
    items = []
    for b, p in skims[:12]:
        items.append(f"<li>{EMOJI[b]} {link(p['arxiv_id'], p['title'])} <span class='small'>({esc(b)})</span></li>")
    return "<ul>" + "".join(items) + "</ul>" if items else "<p class='small'>오늘은 별도 skim-only 후보를 두지 않았습니다.</p>"


def page(date: str) -> str:
    papers_by_bucket = parse_published_post(date)
    curated = load_curated_summaries(date)
    ids = [p["arxiv_id"] for papers in papers_by_bucket.values() for p in papers]
    meta = arxiv_api(ids)
    merge_metadata(papers_by_bucket, curated, meta)
    trends = load_json(ROOT / "trends" / f"{date}.json", {})
    insights = load_json(ROOT / "insights" / f"{date}.json", {})
    benchmarks = load_json(ROOT / "benchmarks" / f"{date}.json", {})
    important_ids = ids_from_insights(insights, trends, benchmarks)
    all_papers = {p["arxiv_id"]: p for papers in papers_by_bucket.values() for p in papers}

    total = sum(len(v) for v in papers_by_bucket.values())
    top_bucket = max(trends.get("buckets", {"": {"total": 0}}).items(), key=lambda kv: kv[1].get("total", 0))[0]
    first_insight = (insights.get("insights") or [{}])[0]
    thesis_phrase = explain_plain(first_insight.get("claim") or first_insight.get("title", "평가축과 배포 조건이 동시에 바뀌는 흐름"))
    thesis = (
        f"{date} 배치에서 가장 두꺼운 버킷은 {top_bucket}입니다. 그래도 진짜 포인트는 "
        f"{thesis_phrase} "
        "기존 리포트에 실렸던 논문 집합을 고정한 채 다시 읽어보면, 개별 논문을 길게 나열하기보다 "
        "어떤 클러스터가 다음 실험 설계를 바꾸는지 먼저 보는 편이 훨씬 선명합니다."
    )
    css = """
body{margin:0;background:#f6f8fa;color:#24292f;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Noto Sans KR",Arial,sans-serif;line-height:1.65}
.container{max-width:1060px;margin:0 auto;background:#fff;min-height:100vh;padding:44px 56px;box-sizing:border-box}
a{color:#0969da;text-decoration:none}a:hover{text-decoration:underline}
h1{font-size:28px;margin:0 0 6px;color:#0d1117}h2{font-size:21px;margin:40px 0 14px;padding-bottom:8px;border-bottom:1px solid #d8dee4;color:#0d1117}h3{font-size:16px;margin:0 0 8px;color:#111827}
.meta{color:#57606a;font-size:14px;margin-bottom:22px}.home{display:inline-block;margin-bottom:18px;padding:7px 12px;border:1px solid #d0d7de;border-radius:6px;background:#f6f8fa;color:#24292f;font-weight:600}
.thesis{background:#f0f7ff;border-left:4px solid #0969da;border-radius:8px;padding:16px 18px;margin:20px 0 24px}
.cluster-table{width:100%;border-collapse:collapse;font-size:13.5px}.cluster-table th{background:#f6f8fa;text-align:left;padding:9px;border-bottom:1px solid #d0d7de}.cluster-table td{padding:9px;border-bottom:1px solid #eaeef2;vertical-align:top}
.conf{font-weight:700;padding:2px 8px;border-radius:999px;font-size:12px}.High{background:#dcfce7;color:#166534}.Medium{background:#fef9c3;color:#854d0e}
.card{border:1px solid #d8dee4;border-radius:8px;padding:14px 16px;margin:12px 0;background:#fff}.topic{border-left:4px solid #22c55e;background:#f0fdf4}
.small,.why{display:block;color:#57606a;font-size:13.5px;margin-top:4px}.tag{display:inline-block;margin-left:6px;color:#475569;font-size:12px}
.bucket-line{font-family:ui-monospace,SFMono-Regular,Consolas,Menlo,monospace;background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;padding:10px 14px;font-size:13px;white-space:pre;overflow-x:auto}
.badge{display:inline-block;font-size:11px;font-weight:700;padding:1px 8px;border-radius:10px;margin-left:6px;vertical-align:middle;font-family:ui-monospace,monospace}.cv{background:#ddf4ff;color:#0550ae;border:1px solid #54aeff}.ro{background:#fff8c5;color:#7a4e00;border:1px solid #d4a72c}.cvro{background:#ffe5d9;color:#9a3412;border:1px solid #f59e0b}.x{background:#f3f4f6;color:#6b7280;border:1px solid #d1d5db}
details{border:1px solid #e5e7eb;border-radius:8px;padding:12px 14px;margin:10px 0;background:#fff}summary{cursor:pointer;font-weight:700;color:#334155}.mini-paper{padding:12px 0;border-top:1px solid #edf2f7}.mini-paper:first-of-type{border-top:none}.mini-paper ul{margin:7px 0 0;padding-left:20px}.mini-paper li{margin:3px 0;line-height:1.55}
footer{margin-top:40px;padding-top:16px;border-top:1px solid #eaeef2;font-size:12px;color:#656d76;text-align:center}
@media(max-width:760px){.container{padding:24px 20px}.cluster-table{font-size:12.5px}}
"""
    bench_html = render_benchmarks(benchmarks)
    return f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>arXiv Daily Briefing — {date}</title><style>{css}</style></head><body><div class="container">
<a class="home" href="https://gisbi-kim.github.io/arxiv-daily-summary/">← 전체 목록으로</a>
<h1>📄 arXiv Daily Briefing — {date} ({WEEKDAY.get(date,'')})</h1>
<div class="meta">
<div><strong>복원 방식:</strong> 기존 공식 HTML의 그날 논문 ID 스냅샷 + 당시 생성 스크립트의 curated commentary + arXiv API metadata 보강</div>
<div><strong>주의:</strong> 현재 /new 페이지를 다시 긁지 않았습니다. 논문 집합은 {date} 리포트에 이미 실렸던 {total}편으로 고정했습니다.</div>
</div>
<div class="thesis"><strong>오늘의 결론:</strong> {esc(thesis)}</div>

<h2>🧩 오늘의 클러스터 지도</h2>
{render_cluster_table(trends, insights, all_papers)}

<h2>🔭 주간 동향</h2>
{render_trends(trends)}

<h2>📐 CV vs RO 대비</h2>
{render_cv_ro(trends)}

<h2>💡 오늘의 인사이트</h2>
{render_insights(insights, all_papers)}

<h2>🔬 추천 연구주제</h2>
{render_topics(insights)}

<h2>📊 오늘의 버킷 현황</h2>
{render_bucket_status(trends)}

{f"<h2>📈 벤치마크 SOTA/평가축 추이</h2>{bench_html}" if bench_html else ""}

<h2>🧊 Skim-only 후보</h2>
{render_skim(papers_by_bucket, important_ids)}

<h2>📄 부록 — 전체 ROI 논문 압축 목록</h2>
<p>기존 리포트의 coverage는 유지하되, 각 논문을 영어 abstract 직역이 아니라 한국어 판단 불릿으로 다시 압축했습니다.</p>
{render_appendix(papers_by_bucket, important_ids)}

<h2>🔗 참고 링크</h2>
<ul>
<li><a href="https://arxiv.org/list/cs.CV/new">cs.CV/new</a></li>
<li><a href="https://arxiv.org/list/cs.RO/new">cs.RO/new</a></li>
<li><a href="https://gisbi-kim.github.io/arxiv-daily-summary/">전체 목록</a></li>
</ul>
<footer>Generated from the published {date} snapshot. <a class="home" href="https://gisbi-kim.github.io/arxiv-daily-summary/">← 전체 목록으로</a></footer>
</div></body></html>
"""


def main(argv: list[str]) -> int:
    dates = argv[1:] or ["2026-05-06", "2026-05-07"]
    for date in dates:
        out = ROOT / "posts" / f"{date}.html"
        html_text = page(date)
        out.write_text(html_text, encoding="utf-8", newline="\n")
        print(f"wrote {out} ({len(html_text)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
