#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-09-23 run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260923 import RI_BY_DATE, main as build_research_intelligence


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-23"


PROFILE = {
    "date": DATE,
    "weekday": "Wed",
    "week_start": week_start(DATE),
    "source_mode": "new",
    "source_label": "arXiv cs.CV/new + cs.RO/new",
    "source_note": "Direct parser output from matching Wednesday 2026-09-23 /new listings",
    "benchmark_note": (
        "Daily artifact generated from the matching Wednesday 2026-09-23 arXiv /new listings. "
        "The parser includes abstracts; Research Intelligence records conservative abstract-only evidence traces for Tier A."
    ),
    "thesis": (
        "The 2026-09-23 batch says robot systems are being judged by the evidence variable that actually authorizes action. "
        "VLA and WAM papers separate clean scores from protocol tier, quantization recipe, action-token stability, instruction entropy, and physical-condition robustness. "
        "Manipulation papers then make contact force, compliance, surgical hierarchy, and specialist routing into explicit command authority rather than auxiliary observations. "
        "Geometry and SLAM papers move 3DGS, point clouds, RGB-D completion, and map priors toward registration, semantic structures, and interactive object state. "
        "World-model and driving papers ask whether predicted futures enter a planner through an auditable action channel, while efficiency papers test which tokens, cache states, or matcher choices can be removed without losing the evidence a robot or detector actually needs."
    ),
    "cluster_takeaway": (
        "Today's core is not bigger VLAs, prettier Gaussian maps, or faster token pruning; it is deciding which evidence can safely change a robot command, map update, or deployment budget."
    ),
    "trend_note": (
        "Wednesday /new produced 240 deduplicated non-replacement papers and 202 ROI papers. "
        "The strongest signals are traceable VLA/WAM evaluation, contact and force authority, robot-usable 3D/SLAM, action-channel world models, closed-loop driving/navigation safety, and conditional deployment budgets."
    ),
    "cluster_specs": [
        {
            "title": "VLA and WAM evaluation moves from leaderboard score to traceable deployment contracts",
            "buckets": ["Robot Learning", "Embodied AI"],
            "ids": ["2609.25562", "2609.25376", "2609.25820", "2609.26292", "2609.25636", "2609.26672"],
            "needles": [
                "vla", "wam", "benchmark", "evaluation", "closed-loop", "quantization",
                "token", "physical", "instruction", "robustness", "deployment", "traceable",
            ],
            "why": (
                "기존 robot policy 비교는 clean task score나 단일 성공률로 모델을 줄 세우기 쉬웠지만, 오늘 묶음은 그 숫자가 어떤 evidence tier에서 나온 것인지 먼저 묻는다. "
                "IndustrialVLA-Bench는 protocol-faithful 비교와 robustness/paraphrase/cost 축을 분리하고, VLAQuantBench는 quantization recipe가 closed-loop success를 크게 바꿀 수 있음을 보인다. "
                "action-tokenization 논문은 reconstruction error만으로 action representation을 고르면 rollout ranking이 뒤집힐 수 있음을 드러내고, RoboTwin-Phys와 RoboFollow는 physical parameter와 instruction entropy를 별도 실패 축으로 만든다. "
                "APRL은 VLA/WAM leaderboard를 만들 때 clean score 앞에 protocol tier, language entropy, physics sweep, compression setting, latency/memory를 같은 release gate로 둬야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Traceable VLA/WAM benchmark, quantization, action tokenization, physics-diverse benchmark, instruction-following diagnosis, and imperfect-data precision papers all expose hidden evaluation contracts.",
            "lab_action": (
                "LIBERO/RoboTwin류 manipulation suite에서 protocol tier, paraphrase pair, high-entropy instruction, mass/friction/joint sweep, action-token perturbation, quantization assignment, and latency/memory budget을 독립 ablation 축으로 두고 clean success, intent score, physical failure, recovery, and deployment cost를 함께 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Manipulation policies split command authority by force, contact, precision, and specialist timing",
            "buckets": ["Robot Learning"],
            "ids": ["2609.25785", "2609.25887", "2609.25756", "2609.26313", "2609.26467", "2609.25606", "2609.25322", "2609.25630"],
            "needles": [
                "force", "contact", "tactile", "precision", "medical", "surgical", "route",
                "specialist", "rollback", "cable", "bimanual", "grasp", "stability",
            ],
            "why": (
                "Contact-rich manipulation에서는 policy가 무엇을 보았는지보다 어떤 물리 신호가 다음 action chunk를 바꿀 권한을 갖는지가 중요하다. "
                "VisForce와 force-sensitive curriculum 논문은 current/desired force와 sub-Newton contact limit을 policy representation 안으로 끌어오고, MedVLA는 precision medical manipulation을 hierarchy와 safety constraint로 나눈다. "
                "SafeLoop와 RouteRLT는 long-horizon VLA가 위험하거나 precision-critical한 구간에서 rollback 또는 RL specialist에게 권한을 넘기는 문제를 제기한다. "
                "CableVLA, JAMB, PAKT 계열은 cable topology, bimanual geometry, physically aligned teaching처럼 접촉 상태가 바뀌는 task에서 nominal policy만으로 부족한 지점을 보여준다."
            ),
            "confidence": "High",
            "confidence_note": "Force grounding, contact-sensitive curriculum, medical hierarchy, rollback, specialist routing, cable topology, bimanual future geometry, and kinesthetic teaching point to the same authority split.",
            "lab_action": (
                "Cable routing, fragile grasping, bimanual rearrangement, surgical precision, and connector insertion tasks에서 vision-only VLA, force-conditioned policy, rollback gate, RL specialist, and physically aligned demo를 비교하고 peak force, contact violation, rollback timing, specialist handoff precision, and final success를 평가한다."
            ),
            "limit": 6,
        },
        {
            "title": "3D and SLAM shift from photorealistic maps to registration, semantics, and interactive state",
            "buckets": ["3D/Scene"],
            "ids": ["2609.25746", "2609.26315", "2609.26795", "2609.25375", "2609.25654", "2609.25966", "2609.26325", "2609.25813"],
            "needles": [
                "slam", "gaussian", "registration", "map", "semantic", "interactive",
                "scene completion", "object decomposition", "localization", "lidar", "odometry",
            ],
            "why": (
                "오늘 3D/SLAM 신호는 photorealistic reconstruction이 아니라 robot이 그 map을 언제 믿고 움직일 수 있는지로 모인다. "
                "Dual Covariance 3DGS-SLAM은 rendering covariance와 tracking covariance를 분리하고, ArborSplat은 orchard robot에 필요한 thin semantic structure를 Gaussian map 안에서 보존한다. "
                "phi-RIE는 3DGS reconstruction을 movable simulator asset과 completed background로 바꾸며, PARTE, CODA, GRIP, map-prior HD mapping은 registration, completion, 2D-3D bridge, long-term driving map prior를 각각 action substrate로 만든다. "
                "APRL geometry 평가는 PSNR이나 ATE만 보지 말고 uncertainty, semantic capacity, movable object state, relocalization, and downstream navigation/manipulation success를 함께 봐야 한다."
            ),
            "confidence": "High",
            "confidence_note": "3DGS SLAM, semantic orchard maps, interactive 3DGS conversion, plane-assisted registration, RGB-D completion, and HD map priors repeatedly connect geometry to robot-use contracts.",
            "lab_action": (
                "RGB-D/LiDAR route와 manipulation scene에서 single-covariance 3DGS, dual-covariance 3DGS, semantic Gaussian map, point-cloud registration, scene-completion map, and interactive object asset을 같은 relocalization/navigation/grasp-planning task에 넣고 tracking loss, semantic recall, object edit validity, collision checks, and task success를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "World models are judged by the action channel that consumes their futures",
            "buckets": ["Robot Learning", "Generation", "Autonomous Driving", "3D/Scene"],
            "ids": ["2609.25961", "2609.26299", "2609.26792", "2609.26458", "2609.25652", "2609.25741", "2609.26007", "2609.26314"],
            "needles": [
                "world model", "world-action", "future", "action", "simulation", "planner",
                "executable", "latent", "policy-oriented", "driving", "navigation", "tri-view",
            ],
            "why": (
                "World-model 논문들은 미래를 그리는 능력보다 그 미래가 어떤 command interface로 들어가는지를 드러낸다. "
                "PatchWAM은 continuous action을 patch로 써서 visual prediction과 action generation을 한 backbone 안에 넣고, ForeDrive는 planning-relevant latent future를 gated guidance로 사용한다. "
                "DreamStream은 policy-oriented generative simulation을, GameDirector와 CoDeR는 gameplay/code logic과 video rendering을 분리해 executable world를 만들며, Fysiverse-3D와 TriWorldBench는 3D/executable scene과 multi-view consistency를 robot evaluation으로 끌어온다. "
                "APRL은 world model을 도입할 때 visual quality가 아니라 action encoding, horizon reliability, simulation replay, and recovery metric이 실제 policy decision을 바꾸는지 먼저 검증해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Patch actions, planning-relevant futures, policy-oriented driving simulation, game/code worlds, executable 3D scenes, drone WAMs, and tri-view robot evaluation all target the action-consumption interface.",
            "lab_action": (
                "Manipulation, drone navigation, and driving-style tasks에서 action-as-patch, latent future guidance, executable simulation replay, tri-view consistency, and no-world-model baselines를 비교하고 action disagreement, horizon reliability, recovery timing, closed-loop safety margin, and task success를 함께 평가한다."
            ),
            "limit": 6,
        },
        {
            "title": "Driving and navigation benchmarks move from open-loop plausibility to closed-loop commitment",
            "buckets": ["Autonomous Driving", "Embodied AI", "Foundation Models", "Efficiency/Systems"],
            "ids": ["2609.26618", "2609.25831", "2609.25860", "2609.26084", "2609.26408", "2609.26360", "2609.25898", "2609.25942"],
            "needles": [
                "closed-loop", "driving", "navigation", "safety", "latency", "reliability",
                "commitment", "trajectory", "planning", "exploration", "formation", "calibration",
            ],
            "why": (
                "Driving/navigation 계열은 open-loop prediction이나 VLM plausibility가 실제 안전 행동을 보증하지 못한다는 쪽으로 움직인다. "
                "NavSafe-infinity는 280개 closed-loop traffic scenario와 safety taxonomy로 open-loop gain의 blind spot을 드러내고, Run-then-Walk scheduling은 progress와 safety reward의 순서를 조절한다. "
                "MatchFusion과 ForeDrive류는 spatio-temporal instance matching과 planning-relevant latent를 통해 perception/planning interface를 조정하고, UAV VLM copilot, SparseNav, floorplan-guided EQA, active perception control은 latency, instruction-conditioned sparse semantics, exploration evidence, relative-state perception이 언제 commitment로 바뀌는지 묻는다. "
                "APRL navigation 평가는 final success뿐 아니라 false commitment, detour cost, safety-margin loss, latency-induced violation, and recovery behavior를 함께 측정해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Closed-loop driving safety, GRPO scheduling, instance matching, VLM UAV latency, sparse VLN semantics, floorplan-guided exploration, active perception, and multimodal trajectory support all expose commitment failures.",
            "lab_action": (
                "NAVSIM/CARLA/ObjectNav/VLN/UAV-UGV cooperation tasks에서 open-loop policy, closed-loop rollout, VLM command latency, sparse semantic map, instance matching, and safety scheduling을 ablation하고 crashes, VRU violations, wrong commitment, detour cost, latency breach, and recovery success를 비교한다."
            ),
            "limit": 6,
        },
        {
            "title": "Deployment budgets become conditional evidence-removal tests instead of generic compression",
            "buckets": ["Efficiency/Systems", "Foundation Models", "Generation", "Robot Learning"],
            "ids": ["2609.26484", "2609.26425", "2609.25492", "2609.25635", "2609.25688", "2609.25108", "2609.25503", "2609.26590"],
            "needles": [
                "token", "pruning", "quantization", "cache", "matcher", "budget", "removability",
                "compression", "efficient", "latency", "runtime", "memory", "coding",
            ],
            "why": (
                "Efficiency 논문들은 더 작은 모델이나 낮은 latency 자체보다 어떤 evidence를 지워도 decision이 유지되는지를 묻는다. "
                "Conditional Removability는 token importance만으로 pruning safe 여부를 판단할 수 없고 representation depth와 deletion set이 조건임을 보이며, QuantWM은 world model/video generation의 2-bit KV cache가 temporal consistency를 보존해야 한다고 말한다. "
                "RGSQ, Shallow-to-Deep token pruning, MatcherCompass, image coding for machines, spike-budgeted UAV tracking, GTR은 quantization, pruning, matcher choice, machine-oriented coding, spike budget, softmax-free dense prediction을 모두 downstream evidence budget 문제로 바꾼다. "
                "APRL은 edge deployment를 latency만으로 승인하지 말고 geometry cue, action token, temporal consistency, matcher reliability, and closed-loop task delta가 보존되는지 확인해야 한다."
            ),
            "confidence": "High",
            "confidence_note": "Token removability, KV cache quantization, VLM quantization geometry, stage-wise pruning, matcher selection, machine coding, spike budgets, and recurrent dense prediction align around conditional evidence budgets.",
            "lab_action": (
                "Robot perception/control stack에서 visual token pruning, 2-bit KV cache, VLM quantization, matcher choice, image coding, spike budget, and recurrent dense backbone을 같은 downstream task에 걸고 latency, memory, geometry cue retention, correspondence failure, temporal drift, action delta, and task success를 비교한다."
            ),
            "limit": 6,
        },
    ],
    "research_topics": [
        {
            "title": "Evidence-tiered VLA/WAM ledger",
            "claim": (
                "Build one evaluation sheet where protocol tier, paraphrase entropy, physical-condition sweep, action-token stability, quantization setting, latency, and memory are release gates before model ranking."
            ),
        },
        {
            "title": "Robot-usable Gaussian map contract",
            "claim": (
                "Compare Gaussian maps by tracking covariance, semantic thin-structure recall, object editability, and navigation/manipulation success rather than rendering score alone."
            ),
        },
        {
            "title": "Contact authority ladder for manipulation",
            "claim": (
                "Rank vision, force, tactile, compliance, rollback, and specialist controllers by the stage at which each should override the next action chunk."
            ),
        },
        {
            "title": "Action-channel world-model audit",
            "claim": (
                "A world model should enter the policy only through a named action patch, latent-future gate, simulator replay, or recovery metric that can be ablated."
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
        "meaning": "Included because it supports today's evidence-contract thesis.",
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
