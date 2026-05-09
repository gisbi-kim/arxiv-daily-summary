#!/usr/bin/env python3
"""Generate a quality-upgraded comparison version of the 2026-05-08 briefing."""
from __future__ import annotations

import html
import io
import json
import os
import re
import sys

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

DATE = "2026-05-08"
OUT = "posts/2026-05-08.html"

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


def esc(s) -> str:
    return html.escape(str(s), quote=False)


def load(path: str):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def clean(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def link(aid: str, label: str | None = None) -> str:
    return f'<a href="https://arxiv.org/abs/{aid}" target="_blank" rel="noopener">{esc(label or aid)}</a>'


def short_abs(p, n=1, limit=260) -> str:
    text = clean(p.get("abstract", ""))
    if not text:
        return "abstract가 비어 있어 제목 기준으로만 판단 필요."
    parts = re.split(r"(?<=[.!?])\s+", text)
    out = " ".join(parts[:n])
    if len(out) > limit:
        out = out[: limit - 1].rstrip() + "…"
    return out


def priority_for(aid: str, bucket: str, p) -> str:
    if aid in {"2605.06667", "2605.05714", "2605.05848", "2605.05810", "2605.05328"}:
        return "Must-read"
    text = (p.get("title", "") + " " + p.get("abstract", "")).lower()
    strong = [
        "benchmark", "dataset", "world model", "vla", "vision-language-action",
        "calibration", "uncertainty", "real-time", "routing", "navigation",
        "gaussian", "diffusion", "safety", "ood", "backdoor"
    ]
    if sum(k in text for k in strong) >= 2:
        return "Read"
    if bucket in {"Generation", "Efficiency/Systems", "Safety/Alignment"} and sum(k in text for k in strong) >= 1:
        return "Read"
    return "Skim-only"


def tag_for(bucket: str, p) -> str:
    text = (p.get("title", "") + " " + p.get("abstract", "")).lower()
    tags = []
    if any(k in text for k in ["benchmark", "dataset", "framework", "infrastructure", "toolkit", "platform"]):
        tags.append("인프라")
    if any(k in text for k in ["failure", "risk", "safety", "uncertainty", "calibration", "ood", "adversarial", "backdoor", "robust"]):
        tags.append("경고신호")
    if any(k in text for k in ["new", "reformulat", "towards", "rethinking", "what makes", "when to trust", "why"]):
        tags.append("문제정의")
    if any(k in text for k in ["adaptive", "routing", "decomposition", "distillation", "flow matching", "diffusion", "experts", "relational", "token"]):
        tags.append("방법전환")
    if not tags:
        if bucket in {"3D/Scene", "Embodied AI"}:
            tags.append("인프라")
        else:
            tags.append("방법전환")
    return " ".join(f"[{t}]" for t in tags[:2])


def joined_text(p) -> str:
    return (p.get("title", "") + " " + p.get("abstract", "")).lower()


def is_video_generation(text: str) -> bool:
    return any(
        k in text
        for k in [
            "video generation",
            "video-to-video",
            "image-to-video",
            "text-to-video",
            "i2v",
            "camera-controlled",
            "video diffusion",
            "long video generation",
        ]
    )


def is_3d_scene_text(text: str) -> bool:
    return any(
        k in text
        for k in [
            "3d",
            "gaussian",
            "splat",
            "lidar",
            "cad",
            "reconstruction",
            "visual localisation",
            "visual localization",
            "novel view",
            "terrain traversability",
        ]
    )


def issue_bullet(bucket: str, p) -> str:
    text = joined_text(p)
    if "vla" in text or "vision-language-action" in text:
        return "VLA가 unseen scene/object나 robot control task에서 일반화·실행 안정성을 잃는 병목을 겨냥."
    if is_video_generation(text):
        return "video generation이 quality 중심 평가에서 camera/motion 제어와 긴 시퀀스 안정성으로 넘어가는 병목을 겨냥."
    if bucket == "3D/Scene" and is_3d_scene_text(text):
        return "3D scene 표현이 sparse view, semantic consistency, geometry fidelity, deployment shift에서 흔들리는 문제를 겨냥."
    if "uncertainty" in text or "calibration" in text:
        return "distribution shift에서 모델 confidence가 실제 위험도를 제대로 반영하지 못하는 문제를 겨냥."
    if "benchmark" in text:
        return "기존 평가가 특정 failure mode나 도메인 난점을 충분히 분리하지 못하는 공백을 겨냥."
    if "dataset" in text:
        return "해당 도메인에서 real-world·multi-modal·cross-view 데이터가 부족한 공백을 메우려는 논문."
    if "navigation" in text or "objectnav" in text or "vln" in text:
        return "navigation을 step-by-step reactive policy로만 풀 때 생기는 누적 오류와 ambiguity를 겨냥."
    if "diffusion" in text or "flow matching" in text:
        return "생성 모델의 sampling 비용, 제어성, few-step 품질 저하 중 하나를 핵심 병목으로 잡음."
    if "medical" in text or "clinical" in text or "x-ray" in text or "retinal" in text:
        return "의료 VLM/vision 모델이 benchmark와 실제 임상 조건 사이에서 깨지는 지점을 겨냥."
    if is_3d_scene_text(text):
        return "3D scene 표현이나 multi-view sensing이 sparse capture와 실제 배치 조건에서 흔들리는 문제를 겨냥."
    if bucket == "Efficiency/Systems":
        return "모델 성능보다 latency, memory, token budget, edge deployment가 병목이 되는 구간을 겨냥."
    if bucket == "Safety/Alignment":
        return "모델이 배포 조건에서 공격·분포 변화·misalignment에 취약해지는 지점을 겨냥."
    return f"{bucket} 버킷 안에서 기존 접근이 놓친 구체적 실패 조건이나 응용 공백을 겨냥."


def method_bullet(p) -> str:
    text = joined_text(p)
    if "triadic" in text or "relational" in text:
        return "object·hand·task 같은 관계 구조를 중간 표현으로 꺼내 action이나 reasoning에 직접 연결."
    if "expert" in text or "routing" in text or "router" in text:
        return "고정 압축/단일 adapter 대신 expert나 router가 입력·query별로 계산 경로를 나누게 함."
    if "camera" in text and "control" in text:
        return "pose/depth/camera 조건을 생성 과정에 넣어 frame별 시점과 motion을 함께 제어."
    if is_3d_scene_text(text):
        return "multi-view geometry나 3D 표현에 memory, semantic feature, surface constraint, novel-view synthesis 요소를 결합."
    if "uncertainty" in text or "calibration" in text:
        return "feature/query density나 uncertainty signal을 이용해 confidence와 regression 신뢰도를 다시 보정."
    if "benchmark" in text:
        return "특정 failure mode를 드러내는 질문/프로토콜/데이터 분할을 새로 구성해 모델을 압박."
    if "dataset" in text:
        return "새 센서 조합·도메인·viewpoint를 포함한 데이터셋을 만들어 기존 평가 범위를 넓힘."
    if "diffusion" in text or "flow matching" in text or "bridge" in text:
        return "diffusion/bridge/flow 계열 생성 과정을 조건부 제어, distillation, sampling 개선 쪽으로 재구성."
    if "navigation" in text or "map" in text:
        return "egocentric step policy 대신 map, factor graph, goal label, comparative judgment를 planning에 사용."
    if "distillation" in text:
        return "teacher signal이나 self-distillation으로 큰 모델 지식을 더 가볍거나 안정적인 표현에 옮김."
    if "low-rank" in text or "quantization" in text or "compression" in text:
        return "low-rank, quantization, compression-friendly 설계로 계산량과 메모리 병목을 줄임."
    return "기존 pipeline의 한 단계를 분리하거나 새 intermediate representation을 넣어 병목을 직접 조정."


def meaning_bullet(bucket: str, p) -> str:
    text = joined_text(p)
    if "vla" in text or "vision-language-action" in text:
        return "VLA 논점을 모델 크기 경쟁에서 구조·실행 신뢰도·fine-tuning recipe 비교로 옮기는 evidence."
    if is_video_generation(text):
        return "video generation을 예쁜 샘플 생성이 아니라, 원하는 카메라 움직임과 장면 변화를 안정적으로 조종하는 시스템으로 봐야 한다는 근거."
    if bucket == "3D/Scene" and is_3d_scene_text(text):
        return "3D/Scene 흐름에서 표현 품질보다 실제 capture 조건과 downstream 사용성을 같이 봐야 한다는 근거."
    if "uncertainty" in text or "calibration" in text or "ood" in text:
        return "reliability-aware deployment cluster의 근거로, 안전을 후처리가 아니라 pipeline 설계 문제로 만든다."
    if "benchmark" in text:
        return "당장 방법보다 평가축 자체를 넓히는 가치가 커서 후속 논문들의 reference가 될 수 있음."
    if "dataset" in text:
        return "새 데이터 기반을 제공하므로 당장 SOTA보다 다음 실험의 출발점으로 의미가 큼."
    if bucket == "Generation":
        return "Generation 버킷의 양적 증가를 실제 제어성·효율성·world-model 기반 구조 문제로 해석하게 해주는 근거."
    if bucket == "Efficiency/Systems":
        return "큰 모델을 실제로 굴릴 때 필요한 routing·compression·edge execution 논점에 직접 연결."
    if bucket == "Safety/Alignment":
        return "성능 향상보다 실패 양상을 드러내고 배포 전에 점검할 지점을 알려주는 가치가 더 큰 후보."
    if bucket == "Embodied AI":
        return "navigation/embodied agent를 단순 policy가 아니라 map·memory·interaction 문제로 재정의하는 데 기여."
    return f"{bucket} 흐름 안에서 대표 논문보다는 보조 evidence로 읽는 것이 적절."


def caution_bullet(p, priority: str) -> str:
    text = (p.get("title", "") + " " + p.get("abstract", "")).lower()
    if "benchmark" in text or "dataset" in text:
        return "주의: 데이터 구성, split, baseline coverage를 본문에서 확인 전까지 일반화 claim은 보류."
    if "real-time" in text or "edge" in text or "latency" in text:
        return "주의: latency·memory 수치가 실제 deployment 환경에서 측정됐는지 확인 필요."
    if "sota" in text or "state-of-the-art" in text:
        return "주의: SOTA claim은 metric 선택과 baseline 강도에 민감하므로 표를 직접 확인해야 함."
    if priority == "Skim-only":
        return "주의: ROI에는 걸리지만 오늘 핵심 클러스터와의 연결은 약해 우선순위는 낮음."
    return "주의: abstract 기반 판단이므로 핵심 ablation과 failure case는 본문 확인 필요."


def appendix_bullets(p, bucket: str) -> list[str]:
    pr = priority_for(p["arxiv_id"], bucket, p)
    bullets = [
        f"문제: {issue_bullet(bucket, p)}",
        f"방법: {method_bullet(p)}",
        f"의미: {meaning_bullet(bucket, p)}",
    ]
    # Add one selective evidence/caution/priority bullet to keep 4 bullets per paper.
    bullets.append(caution_bullet(p, pr))
    bullets.append(f"우선순위: {pr}.")
    return bullets


def badge(b: str) -> str:
    cls = {"CV": "cv", "RO": "ro", "CV/RO": "cvro"}.get(b, "x")
    return f'<span class="badge {cls}">{esc(b)}</span>'


def paper_map(classified):
    out = {}
    bucket_of = {}
    for b, info in classified["buckets"].items():
        for p in info["papers"]:
            out[p["arxiv_id"]] = p
            bucket_of[p["arxiv_id"]] = b
    return out, bucket_of


def authors(p):
    a = p.get("authors", [])
    if not a:
        return p.get("first_author", "")
    return ", ".join(a[:3]) + (" et al." if len(a) > 3 else "")


def main():
    cl = load("out/classified.json")
    cv = load("out/cv_new.json")
    ro = load("out/ro_new.json")
    pm, bucket_of = paper_map(cl)

    clusters = [
        {
            "name": "Controllable video generation",
            "tag": "[문제정의] [방법전환]",
            "papers": ["2605.06667", "2605.06051", "2605.06509"],
            "why": "예전에는 생성된 영상이 얼마나 그럴듯하고 예쁜지를 주로 봤다면, 이제는 원하는 카메라 경로와 움직임을 얼마나 안정적으로 조종할 수 있는지가 중요해졌습니다.",
            "confidence": "High",
            "evidence": "오늘 3편 + pastweek video generation 12회 이상 + 서로 다른 제어축",
            "lab": "카메라 경로 오차 / 대상 정체성 흔들림 / 지연시간 metric grid 설계",
        },
        {
            "name": "VLA structure exposure",
            "tag": "[방법전환]",
            "papers": ["2605.05714", "2605.06175", "2605.06222", "2605.04678"],
            "why": "VLA를 더 키우기보다 relation, expert, latent action, WAM verifier로 내부 구조를 노출.",
            "confidence": "High",
            "evidence": "오늘 3편 + 주간 핵심 From Pixels to Tokens와 직접 연결",
            "lab": "LIBERO/RoboCasa에서 relation/expert/verifier ablation",
        },
        {
            "name": "Reliability-aware deployment",
            "tag": "[경고신호] [인프라]",
            "papers": ["2605.05328", "2605.05810", "2605.05848", "2605.05215"],
            "why": "calibration, contradiction, routing, open-set discovery가 한 방향으로 수렴.",
            "confidence": "High",
            "evidence": "3개 이상 도메인에서 같은 failure-management 질문 등장",
            "lab": "효율을 위해 routing을 넣을 때 calibration/contradiction failure가 커지는지 점검",
        },
        {
            "name": "Navigation as map-level decision",
            "tag": "[문제정의] [인프라]",
            "papers": ["2605.06317", "2605.06223", "2605.05960"],
            "why": "VLN/ObjectNav가 step-by-step policy보다 top-down/global/ambiguous-query planning으로 이동.",
            "confidence": "Medium",
            "evidence": "오늘 3편이지만 대부분 abstract 기반, benchmark 확산은 아직 관찰 필요",
            "lab": "R2R-TopDown과 ObjectNav ambiguity set을 묶은 navigation stress test",
        },
        {
            "name": "3D/robotics calibration under shift",
            "tag": "[경고신호] [인프라]",
            "papers": ["2605.05328", "2605.06478", "2605.05897"],
            "why": "3D perception은 이제 reconstruction보다 uncertainty, cross-view dataset, V2X deployment가 병목.",
            "confidence": "Medium",
            "evidence": "3D/Scene 12편 중 deployment/data/calibration 결이 상위에 위치",
            "lab": "GA3T + Query2Uncertainty 스타일 shift calibration protocol",
        },
    ]

    tier_a = [
        ("2605.06667", "[문제정의] [방법전환]", "video generation을 원하는 카메라와 움직임을 조종하는 제작 도구로 재정의"),
        ("2605.05714", "[방법전환]", "VLA 일반화를 object-hand-task relation으로 재정의"),
        ("2605.05848", "[인프라] [방법전환]", "long-video VLM의 token budget을 query-aware routing 문제로 바꿈"),
        ("2605.05810", "[경고신호] [인프라]", "medical VLM의 negated-option attraction을 독립 failure mode로 벤치마크화"),
        ("2605.05328", "[경고신호] [방법전환]", "distribution shift에서 3D detector confidence calibration을 다시 묻는 결"),
    ]

    skim = [
        ("2605.05402", "도시 CCTV/urban design 응용은 흥미롭지만 ROI 핵심 방법론 전환은 약함"),
        ("2605.05875", "cephalopod-inspired robot은 특이하지만 랩 ROI 일반화성은 낮음"),
        ("2605.06042", "flapping-wing MAV tracking은 응용 특화성이 강해 skim 우선"),
        ("2605.06380", "decision-region topology는 이론적으로 흥미롭지만 오늘 클러스터와는 약하게 연결"),
        ("2605.05367", "sign-language avatar는 asset 응용 가치가 있으나 오늘 핵심 흐름과는 주변부"),
    ]

    bucket_lines = []
    for b, info in cl["buckets"].items():
        bucket_lines.append(
            f"{EMOJI.get(b,'')} {b:<20}: {info['total']:>2}편 (CV {info['cv']:>2} / RO {info['ro']:>2} / CV-RO {info['cvro']})"
        )

    css = """
*,*::before,*::after{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif;background:#f6f7f9;color:#1f2328;line-height:1.72;font-size:15px;padding:32px 16px;word-break:keep-all}
.container{max-width:980px;margin:0 auto;background:#fff;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.06),0 1px 2px rgba(0,0,0,.04);padding:40px 48px}
h1{font-size:28px;margin:0 0 6px;color:#0d1117}h2{font-size:21px;margin:40px 0 14px;padding-bottom:8px;border-bottom:2px solid #e5e7eb}h3{font-size:17px;margin:18px 0 8px}p{margin:0 0 14px}a{color:#0969da;text-decoration:none}
.home{display:inline-block;padding:6px 14px;font-size:13px;color:#0969da;background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;text-decoration:none;margin:0 0 18px}
.meta{font-size:13px;color:#3b434d;padding:14px 18px;background:#f6f8fa;border-left:3px solid #0969da;border-radius:6px;margin:14px 0 22px}.meta div{margin:2px 0}
.thesis{background:#0f172a;color:#f8fafc;border-radius:10px;padding:18px 22px;margin:16px 0 28px;font-size:16px}.thesis strong{color:#fef08a}
.cluster-table{width:100%;border-collapse:collapse;font-size:13px;margin:12px 0 18px}.cluster-table th,.cluster-table td{border:1px solid #d0d7de;padding:9px;vertical-align:top}.cluster-table th{background:#f6f8fa;color:#0d1117}.tag{font-family:ui-monospace,monospace;color:#7c2d12;font-size:12px}
.conf{font-weight:700}.conf.High{color:#15803d}.conf.Medium{color:#a16207}.conf.Low{color:#b91c1c}
.card{background:#fafbfc;border:1px solid #e5e7eb;border-radius:8px;padding:14px 18px;margin:12px 0}.card h3{margin-top:0}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}.paper-card{border-left:4px solid #0ea5e9}.risk{border-left:4px solid #ef4444;background:#fef2f2}.topic{border-left:4px solid #22c55e;background:#f0fdf4}.skim{border-left:4px solid #94a3b8;background:#f8fafc}
.bucket-line{font-family:ui-monospace,SFMono-Regular,Consolas,Menlo,monospace;background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;padding:10px 14px;font-size:13px;white-space:pre;overflow-x:auto}
.badge{display:inline-block;font-size:11px;font-weight:600;padding:1px 8px;border-radius:10px;margin-left:6px;vertical-align:middle;font-family:ui-monospace,monospace}.cv{background:#ddf4ff;color:#0550ae;border:1px solid #54aeff}.ro{background:#fff8c5;color:#7a4e00;border:1px solid #d4a72c}.cvro{background:#ffe5d9;color:#9a3412;border:1px solid #f59e0b}.x{background:#f3f4f6;color:#6b7280;border:1px solid #d1d5db}
details{border:1px solid #e5e7eb;border-radius:8px;padding:12px 14px;margin:10px 0;background:#fff}summary{cursor:pointer;font-weight:700;color:#334155}.mini-paper{padding:12px 0;border-top:1px solid #edf2f7}.mini-paper:first-of-type{border-top:none}.mini-paper ul{margin:7px 0 0;padding-left:20px}.mini-paper li{margin:3px 0;line-height:1.55}.why{display:block;color:#475569;font-size:13.5px;margin-top:4px}
footer{margin-top:40px;padding-top:16px;border-top:1px solid #eaeef2;font-size:12px;color:#656d76;text-align:center}
@media(max-width:760px){.container{padding:24px 20px}.grid{grid-template-columns:1fr}.cluster-table{font-size:12.5px}}
"""

    cluster_rows = []
    for c in clusters:
        papers = ", ".join(link(aid, pm[aid]["title"].split(":")[0]) if aid in pm else aid for aid in c["papers"])
        cluster_rows.append(
            f"<tr><td><strong>{esc(c['name'])}</strong><br><span class='tag'>{esc(c['tag'])}</span></td>"
            f"<td>{papers}</td><td>{esc(c['why'])}</td>"
            f"<td><span class='conf {c['confidence']}'>{c['confidence']}</span><br><span class='why'>{esc(c['evidence'])}</span></td>"
            f"<td>{esc(c['lab'])}</td></tr>"
        )

    tier_a_html = []
    for aid, tag, why in tier_a:
        p = pm[aid]
        tier_a_html.append(
            f"<div class='card paper-card'><h3>{link(aid, p['title'])} {badge(p.get('badge','?'))}</h3>"
            f"<p><span class='tag'>{esc(tag)}</span></p>"
            f"<p><strong>왜 A급인가:</strong> {esc(why)}.</p>"
            f"<p><strong>핵심:</strong> {esc(short_abs(p, 2, 520))}</p>"
            f"<p><strong>읽을 때 볼 것:</strong> metric이 실제 deployment 능력을 대표하는지, ablation이 핵심 claim을 분리하는지 확인.</p>"
            f"</div>"
        )

    appendix = []
    for b, info in cl["buckets"].items():
        rows = [f"<details><summary>{EMOJI.get(b,'')} {esc(b)} · {info['total']}편</summary>"]
        for p in info["papers"]:
            aid = p["arxiv_id"]
            pr = priority_for(aid, b, p)
            tag = tag_for(b, p)
            bullets = "".join(f"<li>{esc(x)}</li>" for x in appendix_bullets(p, b))
            rows.append(
                f"<div class='mini-paper'><strong>{link(aid, p['title'])}</strong> {badge(p.get('badge','?'))} "
                f"<span class='tag'>{esc(tag)} [{esc(pr)}]</span>"
                f"<span class='why'>{esc(authors(p))}</span><ul>{bullets}</ul></div>"
            )
        rows.append("</details>")
        appendix.append("\n".join(rows))

    html_doc = f"""<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>arXiv Daily Briefing — {DATE}</title><style>{css}</style></head><body><div class="container">
<a class="home" href="https://gisbi-kim.github.io/arxiv-daily-summary/">← 전체 목록으로</a>
<h1>📄 arXiv Daily Briefing — {DATE} (금)</h1>
<div class="meta">
<div><strong>소스:</strong> stdlib parser · cs.CV/new {len(cv)}편 + cs.RO/new {len(ro)}편 → {cl['total']} dedup → {cl['selected']} ROI 선정</div>
<div><strong>구성:</strong> thesis · cluster table · confidence · lab action · risk taxonomy · skim-only · 압축 부록</div>
</div>

<div class="thesis"><strong>오늘의 결론:</strong> 금요일 배치는 Generation이 36편으로 가장 두꺼웠지만, 진짜 변화는 “영상을 얼마나 예쁘게 만드느냐”가 아니라 <strong>원하는 카메라 움직임과 장면 변화를 얼마나 안정적으로 조종하느냐</strong>로 평가 기준이 옮겨가는 데 있습니다. 동시에 VLA는 더 큰 end-to-end policy 하나로 밀어붙이기보다, 관계 구조·전문가 모듈·검증기를 밖으로 드러내서 어디서 실패하는지 보려는 방향으로 가고 있습니다. reliability도 이제 안전 부록이 아니라 배포 파이프라인의 기본층으로 들어왔습니다.</div>

<h2>🧩 오늘의 클러스터 지도</h2>
<table class="cluster-table"><thead><tr><th>Cluster</th><th>대표 논문</th><th>왜 중요?</th><th>Confidence</th><th>Lab action</th></tr></thead><tbody>
{''.join(cluster_rows)}
</tbody></table>

<h2>🔭 주간 동향</h2>
<p>이번 리포트에서는 결론의 위계를 먼저 세웁니다. <strong>Generation 36편</strong>은 단순히 양이 많은 버킷이 아니라 ActCam·RealCam·FreeSpec으로 이어지는 “조종 가능한 video generation” 클러스터입니다. 여기서 중요한 건 FID류 품질 점수보다, 원하는 카메라 궤적을 따라가는지, 대상의 정체성이 흔들리지 않는지, 실시간으로 쓸 만큼 지연시간이 낮은지 같은 새 평가축이에요.</p>
<p>두 번째로 <strong>Robot Learning 19편</strong>은 VLA 구조 노출 쪽으로 읽어야 합니다. TriRelVLA는 relation을, VLA-GSE는 expert routing을, When to Trust Imagination은 WAM rollout의 신뢰도를 꺼냅니다. 같은 문제를 세 표현으로 찌르는 셈이라 confidence를 High로 둬도 괜찮아 보입니다.</p>
<p>세 번째로 <strong>Efficiency 27편·Safety 24편·Foundation Models 21편</strong>은 하나의 deployment cluster로 묶입니다. VideoRouter는 계산 예산을, Query2Uncertainty는 confidence를, CXR-ContraBench는 medical VLM contradiction을 다룹니다. 모델이 더 똑똑해지는 것보다 “언제 믿고, 언제 계산하고, 언제 의심할지”가 오늘 더 중요한 질문입니다.</p>

<h2>🧭 어제/지난주와 달라진 점</h2>
<div class="card"><p><strong>어제까지의 흐름:</strong> 4D world model을 어떻게 평가할지, VLA가 행동 단서를 어떤 형태로 배울지, VLA 내부 구조를 어떻게 나눌지가 중심이었습니다.</p><p><strong>오늘의 이동:</strong> 그 논의가 실제 사용 조건으로 내려왔습니다. video는 카메라 제어와 지연시간으로, VLA는 관계 구조·전문가 모듈·검증기로, VLM은 contradiction benchmark와 uncertainty로 이어집니다.</p></div>

<h2>🌟 Tier A — 판을 바꾸는 논문 5편</h2>
{''.join(tier_a_html)}

<h2>💡 인사이트와 Confidence</h2>
<div class="card"><h3>1. 조종 가능한 video generation은 새 평가축을 요구한다 <span class="conf High">High</span></h3><p>ActCam과 RealCam은 둘 다 video generation을 창작용 조작 시스템으로 봅니다. 다음 벤치는 “보기 좋은 영상인가”만 묻지 말고, 카메라 경로를 얼마나 정확히 따르는지, 대상 정체성이 얼마나 유지되는지, 지연시간이 실제 사용 가능한지까지 분리해서 봐야 합니다.</p></div>
<div class="card"><h3>2. VLA 일반화의 다음 축은 모델 크기가 아니라 구조 노출이다 <span class="conf High">High</span></h3><p>TriRelVLA, VLA-GSE, When to Trust Imagination, From Pixels to Tokens가 같은 주제의 서로 다른 층을 찌릅니다. relation, expert, latent action, verifier를 한 matrix에서 비교하는 follow-up 가치가 큽니다.</p></div>
<div class="card"><h3>3. Reliability와 efficiency는 한 파이프라인에서 봐야 한다 <span class="conf Medium">Medium</span></h3><p>VideoRouter와 CXR-ContraBench를 같이 보면 계산을 아끼는 routing이 negation/contradiction failure를 악화시킬 가능성도 열립니다. 이 연결은 아직 직접 논문은 아니지만, 실험 질문으로는 꽤 날카롭습니다.</p></div>

<h2>🔬 추천 연구주제 — 1주 실행 protocol 포함</h2>
<div class="card topic"><h3>Camera-Control Stress Test</h3><p><strong>실행 1주차:</strong> ActCam·RealCam 계열 데모/코드를 모으고, 동일 source video에 대해 카메라 경로 5종, actor motion 5종을 grid로 평가합니다. 비교축은 카메라 궤적 오차, 대상 정체성 흔들림, geometry consistency, 지연시간입니다. 실패해도 “제어 가능성 metric proposal” workshop short가 남습니다.</p></div>
<div class="card topic"><h3>VLA Structure Ablation Matrix</h3><p><strong>실행 1주차:</strong> LIBERO/RoboCasa에서 relation graph(TriRelVLA), expert routing(VLA-GSE), WAM verifier를 독립 축으로 두고 success rate·latency·failure taxonomy를 비교합니다. 핵심은 어느 구조가 어떤 task family에서만 이기는지 Pareto를 그리는 겁니다.</p></div>
<div class="card topic"><h3>Reliability-Aware Routing 점검</h3><p><strong>실행 1주차:</strong> VideoRouter류 query-adaptive compression을 medical VLM negation benchmark(CXR-ContraBench 스타일)에 얹어 봅니다. token budget을 줄일수록 contradiction failure가 늘어나는지 측정하면 효율-안전 trade-off가 바로 보입니다.</p></div>

<h2>⚠️ 리스크·한계 필터</h2>
<div class="card risk"><h3>[Metric risk] Camera-control claims</h3><p>ActCam/RealCam의 “control”이 실제 카메라 경로 오차와 대상 정체성 유지 정도를 따로 측정하지 않으면, 단순히 보기 좋은 데모를 제어가 잘 된 결과로 착각할 수 있습니다.</p></div>
<div class="card risk"><h3>[Dataset risk] VLA relation/expert 일반화</h3><p>TriRelVLA/VLA-GSE gain이 특정 simulator나 relation extractor에 묶이면 real-world generalization claim은 약해집니다. unseen object보다 unseen relation composition을 봐야 합니다.</p></div>
<div class="card risk"><h3>[Deployment risk] Efficient routing</h3><p>VideoRouter는 latency/memory를 줄이지만, query가 애매하거나 evidence가 sparse할 때 중요한 frame을 버리는 failure가 생길 수 있습니다. reliability benchmark와 함께 평가해야 합니다.</p></div>

<h2>🧊 Skim-only 후보</h2>
{''.join(f'<div class="card skim"><p>{link(aid, pm[aid]["title"]) if aid in pm else esc(aid)}<span class="why">{esc(reason)}</span></p></div>' for aid, reason in skim)}

<h2>📊 버킷 현황</h2>
<div class="bucket-line">{esc(chr(10).join(bucket_lines))}</div>

<h2>📄 부록 — 전체 ROI 논문 압축 목록</h2>
<p>coverage는 유지하되, 본문 판단 구조를 해치지 않도록 전체 논문을 압축 부록으로 내립니다.</p>
{''.join(appendix)}

<a class="home" href="https://gisbi-kim.github.io/arxiv-daily-summary/">🏠 전체 목록으로</a>
<footer>Generated {DATE} · quality-upgraded briefing · parser-grounded · WebFetch 미사용</footer>
</div></body></html>
"""

    os.makedirs("posts", exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(html_doc)
    sys.stderr.write(f"wrote {OUT}\n")


if __name__ == "__main__":
    main()
