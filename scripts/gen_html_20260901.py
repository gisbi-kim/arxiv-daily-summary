#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-09-01 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260901 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-01"


PROFILE = {
    "date": DATE,
    "weekday": "Tue",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching 2026-09-01 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching 2026-09-01 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "The 2026-09-01 batch is about release contracts for robot perception and autonomy. "
        "Geometry papers no longer stop at plausible reconstruction: dense geo-registration, dynamic Gaussian SLAM, transparent-object depth, ordered 3D grounding, and single-plane microrobot navigation all ask whether the recovered state can still support action. "
        "VLA and autonomous-driving papers show that demonstrations, rare traffic rules, stream samples, oracle labels, static infrastructure memory, and driving memory can harm deployment when they are accepted without an eligibility test. "
        "Tactile and dexterous world-model papers move embodiment toward contact-state data infrastructure, while VLM and safety papers make evidence retrieval, tool revision, nuisance filtering, and attack calibration explicit gates before a model answer or robot command is trusted."
    ),
    "cluster_takeaway": (
        "Today's core is not a bigger model or cleaner reconstruction, but whether metric state, contact evidence, memory, and nuisance-aware alarms decide when a robot may act or adapt."
    ),
    "trend_note": (
        "Tuesday /new produced 386 deduplicated non-replacement papers and 311 ROI papers. "
        "Generation and Foundation Models are large buckets, but the APRL signal is the convergence of metric geometry, evidence-eligible VLA updates, tactile/contact infrastructure, persistent navigation memory, and deployment gates that distinguish nuisance shift from real failure."
    ),
    "cluster_specs": [
        {
            "title": "Metric geometry moves from plausible reconstruction to action-state release evidence",
            "buckets": ["3D/Scene", "Embodied AI"],
            "ids": ["2608.28891", "2608.28895", "2608.29003", "2608.29881", "2608.30451", "2608.30220"],
            "needles": [
                "geo-registration", "drone", "satellite", "reconstruction", "slam", "gaussian",
                "monocular geometry", "optically challenging", "3d visual grounding", "fluoroscopy",
                "microrobot", "depth", "metric",
            ],
            "why": (
                "기존 3D 평가는 reconstructed view가 그럴듯한지나 이미지 하나의 위치가 맞는지에 기대는 경우가 많았다. "
                "SkyReg는 drone image의 각 pixel을 satellite map 좌표로 묻고, ReconSplat과 RoSe-SLAM은 Gaussian scene이 observed view 밖과 dynamic object 아래에서도 geometry를 유지해야 한다고 본다. "
                "OptiGeo, SeqAlign3DVG, VISTA는 투명/반사 장면, 순서가 있는 3D grounding, single-plane fluoroscopy처럼 로봇이 실제로 잃는 metric state를 평가축으로 만든다. "
                "따라서 APRL geometry 평가는 visual fidelity가 아니라 route reuse, grasp error, relocalization, depth recovery가 실제 action을 바꾸는지로 봐야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Six independent papers expose dense map coordinates, unobserved-view reconstruction, dynamic SLAM, optical depth failure, temporal 3D grounding, and missing-depth microrobot navigation.",
            "lab_action": (
                "Drone-satellite, dynamic indoor, transparent-object, ordered 3D grounding, and fluoroscopy navigation cases에서 geo-registration, Gaussian SLAM, feed-forward reconstruction, monocular depth, and digital-twin recovery를 metric error, relocalization success, grasp delta, route deviation, depth-recovery failure로 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "VLA and driving updates move from imitation score to evidence-eligible behavior change",
            "buckets": ["Robot Learning", "Autonomous Driving"],
            "ids": ["2608.30122", "2608.28656", "2608.28672", "2608.28673", "2608.31029", "2608.30657"],
            "needles": [
                "vla driving", "traffic-rule", "multi-trajectory", "active learning", "continuous",
                "cloud-based oracle", "driving on memory", "infrastructure occupancy", "static-to-dynamic",
            ],
            "why": (
                "기존 imitation이나 adaptation은 높은 trajectory score, 많은 stream sample, 또는 cloud oracle label을 곧바로 더 좋은 policy update로 취급하기 쉽다. "
                "Multi-trajectory VLA driving은 high-scoring trajectory가 GRPO를 오히려 안전하지 않은 방향으로 밀 수 있음을 말하고, RedLight-VLA는 평균 loss에서 묻히는 red-light braking과 launching을 별도 supervision으로 키운다. "
                "FrameScope, AdaptAV, InfraOcc, Driving on Memory는 어떤 frame, oracle correction, roadside static scaffold, memory variable이 정책을 바꿀 자격이 있는지 묻는다. "
                "APRL은 final driving score 전에 update 후보가 rare rule, feasible trajectory, dynamic event, memory evidence를 실제로 담았는지 검증해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Driving VLA, traffic-rule grounding, stream valuation, cloud adaptation, infrastructure occupancy, and memory-based planning all expose update eligibility.",
            "lab_action": (
                "Intersection, highway memory, roadside infrastructure, and manipulation transfer episodes에서 candidate trajectory score, red-light state, stream novelty, oracle disagreement, static scaffold, memory horizon을 독립 변수로 두고 unsafe update rejection, rule violation, recovery timing, closed-loop score를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Embodied learning shifts from vision-only imitation to tactile contact-state infrastructure",
            "buckets": ["Robot Learning"],
            "ids": ["2608.28664", "2608.29601", "2608.30237", "2608.29242", "2608.29396", "2608.30368", "2608.30506"],
            "needles": [
                "haptic", "tactile", "touch", "dexterous", "contact", "palpation",
                "world model", "sensor", "manipulation", "visuo-tactile",
            ],
            "why": (
                "로봇 manipulation을 vision-language policy로만 읽으면 실제 contact가 바뀌는 순간을 설명하지 못한다. "
                "Haptic Foundation Models와 N0-Foundation은 touch sensing, tactile UMI, visuo-tactile data, standardized evaluation을 foundation asset으로 묶고, Motus2와 AnyWorld는 manipulation world model을 policy, simulator, evaluator loop와 cross-embodiment experience로 확장한다. "
                "Sliding palpation, SpectraTac, tactile anomaly detection은 작은 표면 결함이나 subsurface vessel처럼 vision-only evidence가 약한 실패를 contact trace로 분리한다. "
                "APRL은 tactile sensor 하나를 추가하는 문제가 아니라 contact-state labels, visual aliases, digital-twin variants, recovery traces를 같이 축적해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Haptic foundation models, tactile data infrastructure, dexterous world models, cross-embodiment videos, palpation twins, and compact tactile sensors form one contact asset axis.",
            "lab_action": (
                "Transparent, deformable, slippery, subsurface, and sub-centimetre manipulation cases에서 vision-only VLA, tactile representation, dexterous world-model feedback, digital-twin tactile labels, compact sensor readout을 contact-state disambiguation, slip prediction, recovery success, inspection error로 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Navigation agents move from episodic routes to persistent memory and delayed-sensor correction",
            "buckets": ["Embodied AI"],
            "ids": ["2608.29114", "2608.30396", "2608.30935", "2608.29315", "2608.29514", "2608.30471"],
            "needles": [
                "lifelong", "navigation", "memory", "visual terrain", "foundation models",
                "spatial intelligence", "exploration", "inertial", "delay", "horizon",
            ],
            "why": (
                "Navigation success를 single episode route score로만 보면 이전 관측, sensor delay, semantic waypoint, and foundation-model scaffold가 실패를 어떻게 늦추거나 고치는지 보이지 않는다. "
                "CGFM-Nav는 graph-field memory로 object relation과 continuous exploration을 함께 다루고, LightNav-0와 foundation-model scaffolding은 VLM spatial priors를 action으로 끌어내려 한다. "
                "SGE, Galilean sliding-window filtering, HorizonNet은 image-space waypoint, delayed inertial correction, panoramic horizon cues처럼 long-horizon route의 다른 약한 고리를 노출한다. "
                "APRL navigation 평가는 SR/SPL 대신 revisit recovery, delay-compensated pose, semantic waypoint value, and memory corruption sensitivity를 분리해야 한다."
            ),
            "confidence": "Medium-High",
            "confidence_note": "Navigation memory, foundation-model scaffolding, semantic exploration, delayed inertial estimation, and terrain horizon cues share the same persistent-state question.",
            "lab_action": (
                "Indoor ObjectNav, outdoor USV, unstructured ground-vehicle, and delayed-inertial routes에서 graph memory, VLM spatial prior, semantic waypoint, horizon cue, delay estimator를 ablation하고 revisit recovery, route deviation, false target acceptance, relocalization time을 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "VLM reasoning shifts from global tokens to state-conditioned evidence acquisition",
            "buckets": ["Foundation Models"],
            "ids": ["2608.28666", "2608.28698", "2608.28701", "2608.29374", "2608.29395", "2608.28691"],
            "needles": [
                "structured video prompting", "state-conditioned", "evidence", "topology",
                "self-correction", "reliability-gated", "wearable", "private attribute", "retrieval",
            ],
            "why": (
                "VLM이 정답을 맞히는 것과 어떤 visual evidence를 가져와서 그 정답을 허가했는지는 다른 문제다. "
                "Structured Video Prompting은 space/time anchor로 video evidence를 정리하고, State-Conditioned Visual Evidence Retrieval은 decoding state마다 필요한 local cue를 다시 고른다. "
                "TopoAgent, ReVISE, GATE, wearable VLM privacy는 topology consistency, tool-output verification, reliability-gated evidence fusion, private attribute leakage를 통해 evidence acquisition이 answer fluency보다 중요하다는 점을 보여준다. "
                "APRL은 robot VLM agent에서 cue order, retrieved crop, tool inconsistency, privacy-sensitive token, and final action permission을 함께 평가해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Six papers independently target video evidence structure, document-state retrieval, topology reasoning, tool revision, reliability-gated fusion, and egocentric privacy.",
            "lab_action": (
                "Long-video QA, document/diagram parsing, household robot VLM, wearable assistance, and tool-using perception episodes에서 cue order, crop retrieval, topology constraint, tool disagreement, privacy mask를 바꿔 evidence hit rate, wrong-evidence right-answer, unsafe action permission, private-attribute leakage를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Deployment reliability moves from average accuracy to nuisance-aware release gates",
            "buckets": ["Efficiency/Systems", "Safety/Alignment", "Autonomous Driving", "Generation"],
            "ids": ["2608.28684", "2608.29187", "2608.29112", "2608.29113", "2608.28685", "2608.28778", "2608.29510"],
            "needles": [
                "rate-distortion", "occupancy", "nuisance", "distribution shift", "gram",
                "compression", "calibration attack", "adversarial", "robust", "deployment",
            ],
            "why": (
                "배포 reliability를 average accuracy나 compression ratio로 보면 실제 failure source가 sensor, representation, nuisance, or attack 중 무엇인지 모른다. "
                "Distributed segmentation과 OPUS-V2는 low-bitrate feature and sparse-to-dense occupancy가 downstream dense perception을 어떻게 바꾸는지 묻고, NFAD와 GramLoop는 distribution shift 아래 nuisance filtering과 spatial relation 보존을 분리한다. "
                "compression-robust deepfake negative result, AV calibration attack, ARMOR aerial defense는 benchmark 평균이 deployment alarm을 대신할 수 없음을 보여준다. "
                "APRL은 compressed feature, calibration drift, nuisance variation, adversarial patch를 release gate로 나누어 실제 robot action이 바뀌는 조건만 남겨야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Efficiency, dense occupancy, anomaly detection, frozen-backbone replay, negative deepfake robustness, AV calibration attack, and aerial patch defense converge on deployment gates.",
            "lab_action": (
                "Industrial inspection, AV perception, aerial detection, event/semantic segmentation, and occupancy prediction에서 bitrate, sparse-to-dense conversion, nuisance shift, Gram consistency, calibration drift, physical patch를 stress split으로 만들고 false alarm, missed defect, occupancy action delta, unsafe calibration acceptance를 비교한다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Metric-state release gate for robot geometry",
            "claim": (
                "Build a shared test where geo-registration, Gaussian SLAM, monocular depth, 3D grounding, and microrobot tracking are ranked by route, grasp, and relocalization decisions rather than visual quality alone."
            ),
        },
        {
            "title": "Evidence-eligible VLA update protocol",
            "claim": (
                "Use paired driving and manipulation episodes to decide whether trajectory score, rare rule evidence, stream value, oracle disagreement, or memory state is allowed to update a policy."
            ),
        },
        {
            "title": "Contact-state asset for embodied learning",
            "claim": (
                "Collect visual aliases with tactile/contact labels so tactile foundation models and dexterous world models are evaluated by failures that vision-only policies cannot distinguish."
            ),
        },
        {
            "title": "State-conditioned evidence harness for robot VLMs",
            "claim": (
                "Measure which cue, crop, topology constraint, tool revision, or privacy mask changes a robot VLM decision before the agent is allowed to act."
            ),
        },
    ],
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def all_papers(classified: dict) -> list[dict]:
    rows = []
    for bucket, info in classified.get("buckets", {}).items():
        for paper in info.get("papers", []):
            q = dict(paper)
            q["bucket"] = bucket
            rows.append(q)
    return rows


def abstract_card(paper: dict, ri_lookup: dict) -> dict:
    text = " ".join(str(paper.get("abstract", "")).split())
    return {
        "arxiv_id": paper.get("arxiv_id"),
        "title": paper.get("title"),
        "bucket": paper.get("bucket"),
        "reading_depth": ri_lookup.get(paper.get("arxiv_id"), "abstract-only"),
        "problem": text[:360],
        "method": "See Research Intelligence edition for abstract evidence trace and falsification note.",
        "meaning": "Included because it supports today's release-contract thesis.",
    }


def enrich_insights() -> None:
    insights_path = ROOT / "insights" / f"{DATE}.json"
    trends = load_json(ROOT / "trends" / f"{DATE}.json")
    insights = load_json(insights_path)
    classified = load_json(ROOT / "out" / "classified.json")
    papers = all_papers(classified)
    by_id = {p["arxiv_id"]: p for p in papers}
    ri = RI_BY_DATE[DATE]
    ri_ids = [paper["arxiv_id"] for paper in ri["papers"]]
    ri_lookup = {paper["arxiv_id"]: paper["status"] for paper in ri["papers"]}

    insights["source_listing_date"] = trends["source_listing_date"]
    insights["source_mode"] = trends["source_mode"]
    insights["daily_new_counts"] = trends["daily_new_counts"]
    insights["paper_autopsies"] = [abstract_card(by_id[pid], ri_lookup) for pid in ri_ids if pid in by_id]
    insights["frontier_memory"] = ri["frontier_memory"]
    insights["strategy_board"] = ri["strategy"]
    insights["tiering_note"] = (
        "Research Intelligence uses repository parser abstracts for selected Tier A papers. "
        "No figure/table/full-text claims are asserted in this conservative automation run."
    )
    insights["research_intelligence"] = {
        "html": f"posts/{DATE}-research-intelligence.html",
        "json": f"intelligence/{DATE}.json",
        "source_prompt": ri["source_prompt"],
    }
    write_json(insights_path, insights)


def add_ri_callout() -> None:
    post_path = ROOT / "posts" / f"{DATE}.html"
    doc = post_path.read_text(encoding="utf-8")
    if "ri-callout" in doc:
        return
    doc = doc.replace(
        ".thesis strong{color:#fef08a}",
        ".thesis strong{color:#fef08a}.ri-callout{display:flex;justify-content:space-between;gap:16px;align-items:center;margin:-12px 0 28px;padding:14px 18px;border:1px solid #67e8f9;border-radius:10px;background:#ecfeff;color:#164e63}.ri-callout a{font-weight:750;white-space:nowrap}@media(max-width:760px){.ri-callout{align-items:flex-start;flex-direction:column}}",
    )
    ri = RI_BY_DATE[DATE]
    ri_callout = (
        f"<section class=\"ri-callout\"><span><strong>Today's Research Intelligence</strong> "
        f"Tier A {len(ri['papers'])} papers are conservative abstract-only cards with evidence traces, "
        f"adversarial reads, frontier memory, and APRL strategy board.</span>"
        f"<a href=\"{DATE}-research-intelligence.html\">Open Research Intelligence</a></section>"
    )
    doc = re.sub(r"</section>\n(<h2>.*?</h2>)", f"</section>\n{ri_callout}\n\\1", doc, count=1, flags=re.S)
    post_path.write_text(doc, encoding="utf-8", newline="\n")


def main() -> int:
    build(PROFILE, "out/cv_new.json", "out/ro_new.json")
    build_research_intelligence()
    enrich_insights()
    add_ri_callout()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
