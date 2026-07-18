#!/usr/bin/env python3
"""Generate the 2026-W29 weekly retrospective from parser and daily RI artifacts."""
from __future__ import annotations

import html
import json
from pathlib import Path


DATE = "2026-07-18"
WEEK = "2026-W29"
WEEK_START = "2026-07-12"
WEEK_END = "2026-07-18"
LISTING_DATE = "2026-07-17"
DAILY_DATES = ["2026-07-13", "2026-07-14", "2026-07-15", "2026-07-16", "2026-07-17"]
SITE_URL = "https://gisbi-kim.github.io/arxiv-daily-summary"


def load_json(path: str | Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def esc(value) -> str:
    return html.escape(str(value or ""), quote=False)


def paper_lookup(weekly_full: dict) -> dict[str, dict]:
    out = {}
    for bucket_name, bucket in weekly_full["buckets_full"].items():
        for item in bucket["papers"]:
            p = dict(item)
            p["bucket"] = bucket_name
            out[p["arxiv_id"]] = p
    for raw_path in ["out/cv_pastweek.json", "out/ro_pastweek.json"]:
        path = Path(raw_path)
        if not path.exists():
            continue
        for item in load_json(path):
            out.setdefault(item["arxiv_id"], dict(item))
    return out


def phy(source: str, lineage: str, confidence: str = "High") -> dict:
    phylum, klass, order, genus = [x.strip() for x in lineage.split(">")]
    return {
        "source": source,
        "phylum": phylum,
        "class": klass,
        "order": order,
        "genus": genus,
        "confidence": confidence,
        "rationale": "weekly representative paper lineage assigned from the robotics/CVML phylogeny style",
    }


LINEAGES = {
    "vla": phy("ROBOTICS", "Robot Learning > Vision-Language-Action > Execution Interfaces > Runtime and Semantic Alignment"),
    "contact": phy("ROBOTICS", "Robot Manipulation > Contact-Rich Control > Tactile and Force Sensing > State Estimation"),
    "geometry": phy("ROBOTICS", "Perception and Mapping > State Estimation > SLAM and Reconstruction > Gaussian and Point-Cloud Maps"),
    "world": phy("ROBOTICS", "Simulation and World Models > World-Action Models > Closed-Loop Safety > Scenario Validity"),
    "memory": phy("ROBOTICS", "Embodied AI > Navigation and Planning > Memory and Semantic Maps > Long-Horizon Agents"),
    "trust": phy("CVML", "Foundation Models > Multimodal Learning > Trustworthy Evaluation > Evidence and Calibration"),
}

TAGS = {
    "vla": ["[평가축]", "[방법전환]", "[실사용전환]"],
    "contact": ["[경고신호]", "[데이터전환]", "[실사용전환]"],
    "geometry": ["[SLAM/Recon]", "[평가축]", "[실사용전환]"],
    "world": ["[경고신호]", "[closed-loop]", "[평가축]"],
    "memory": ["[인프라]", "[실사용전환]", "[평가축]"],
    "trust": ["[근거검증]", "[경고신호]", "[인프라]"],
}


def make_paper(by_id: dict[str, dict], arxiv_id: str, key: str, short: str) -> dict:
    p = dict(by_id.get(arxiv_id, {}))
    p.setdefault("arxiv_id", arxiv_id)
    p.setdefault("title", short)
    p.setdefault("badge", "")
    p.setdefault("bucket", "")
    p["short"] = short
    p["phylogeny"] = LINEAGES[key]
    p["importance_tags"] = TAGS[key]
    return p


def paper_url(p: dict) -> str:
    return f"https://arxiv.org/abs/{p['arxiv_id']}"


def phy_text(p: dict) -> str:
    ph = p["phylogeny"]
    return f"{ph['source']} · {ph['phylum']} > {ph['class']} > {ph['order']} > {ph['genus']}"


def phy_html(p: dict) -> str:
    ph = p["phylogeny"]
    lineage = " &gt; ".join(esc(ph[key]) for key in ["phylum", "class", "order", "genus"])
    return f"<span class='phy'>Phylogeny: <strong>{esc(ph['source'])}</strong> {lineage}</span>"


def tag_html(tags: list[str]) -> str:
    return " ".join(f"<span class='tag'>{esc(t)}</span>" for t in tags)


def paper_link(p: dict) -> str:
    badge = f" <span class='badge'>{esc(p.get('badge', ''))}</span>" if p.get("badge") else ""
    return f'<a href="{paper_url(p)}" target="_blank" rel="noopener">{esc(p["short"])}</a>{badge}<br>{phy_html(p)}'


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


def daily_summary() -> dict:
    out = {"totals": {"cv": 0, "ro": 0, "selected": 0, "total_scanned": 0}, "theses": [], "frontier": [], "strategy": []}
    for date in DAILY_DATES:
        trend = load_json(Path("trends") / f"{date}.json")
        insight = load_json(Path("insights") / f"{date}.json")
        intelligence = load_json(Path("intelligence") / f"{date}.json")
        counts = trend.get("daily_new_counts", {})
        totals = trend.get("totals", {})
        out["totals"]["cv"] += int(counts.get("cv", 0))
        out["totals"]["ro"] += int(counts.get("ro", 0))
        out["totals"]["selected"] += int(totals.get("selected", 0))
        out["totals"]["total_scanned"] += int(totals.get("total_scanned", 0))
        if insight.get("daily_thesis"):
            out["theses"].append({"date": date, "thesis": insight["daily_thesis"]})
        out["frontier"].extend({"date": date, **item} for item in intelligence.get("frontier_memory", [])[:2])
        out["strategy"].extend({"date": date, **item} for item in intelligence.get("strategy", [])[:2])
    return out


def build() -> None:
    weekly_full = load_json("out/weekly_full.json")
    snapshot = weekly_full["snapshot"]
    by_id = paper_lookup(weekly_full)
    daily = daily_summary()

    def p(arxiv_id: str, key: str, short: str) -> dict:
        return make_paper(by_id, arxiv_id, key, short)

    clusters = [
        {
            "cluster": "VLA가 action head 경쟁에서 action-facing interface와 runtime contract 검증으로 이동",
            "papers": [
                p("2607.14635", "vla", "Action QFormer"),
                p("2607.14739", "vla", "FoMoVLA"),
                p("2607.13429", "vla", "Anchor-Align VLA"),
                p("2607.13597", "vla", "Semantic Anchoring"),
                p("2607.12659", "vla", "Jetson-PI"),
                p("2607.12287", "vla", "Temporal Redundancy VLA"),
            ],
            "why": (
                "이번 주 Robot Learning은 83편으로 가장 큰 버킷이지만 핵심은 VLA를 더 크게 만드는 경쟁이 아닙니다. "
                "Action QFormer와 FoMoVLA는 action supervision이 upstream visual representation을 어떻게 다시 쓰는지 묻고, "
                "Anchor-Align과 Semantic Anchoring은 fine-tuning 중 semantic structure가 침식되는 문제를 드러냅니다. "
                "Jetson-PI와 temporal redundancy 논문은 이 논의를 onboard latency와 control-loop clock까지 내립니다. "
                "따라서 VLA 평가는 action head score보다 query interface, semantic retention, streaming delay가 실패를 어떻게 바꾸는지 분리해야 합니다."
            ),
            "confidence": "High — representation, semantic retention, streaming inference, onboard timing 신호가 같은 주에 반복",
            "lab_action": (
                "LIBERO/RoboCasa/UAV tracking에서 query interface, language-action anchoring, token reuse, latency jitter를 factorial split으로 두고 "
                "success, instruction-action contradiction, semantic retention, failure-warning lead time을 비교한다."
            ),
        },
        {
            "cluster": "Contact-rich manipulation이 vision-only chunk에서 force와 tactile state 평가로 이동",
            "papers": [
                p("2607.14236", "contact", "Never Too Late for Force"),
                p("2607.14578", "contact", "Explicit Force-Torque Proxies"),
                p("2607.14609", "contact", "Tactile Grounding"),
                p("2607.14842", "contact", "KineFuse"),
                p("2607.14728", "contact", "VQ-Touch"),
                p("2607.09218", "contact", "TACTIC"),
            ],
            "why": (
                "금요일 batch에서 force, tactile, haptic fusion 논문이 한꺼번에 올라온 것은 manipulation policy가 시각 chunk만으로는 접촉 상태를 충분히 설명하지 못한다는 신호입니다. "
                "LIFT와 force-torque proxy 논문은 action chunk 안에 force memory를 넣고, tactile grounding과 KineFuse는 occlusion 상태에서 접촉 evidence를 별도 representation으로 둡니다. "
                "VQ-Touch와 TACTIC까지 묶으면 데이터셋 수집보다 어떤 contact state가 실제 recovery를 바꾸는지 검증하는 축이 더 중요해집니다."
            ),
            "confidence": "High — force, tactile, haptic, contact-centric control 논문이 같은 contact observability 문제로 연결",
            "lab_action": (
                "folding, insertion, in-hand pose tracking에서 force memory length, tactile prediction target, haptic fusion encoder를 독립 ablation으로 두고 "
                "contact failure, recovery success, failure-warning lead time을 평가한다."
            ),
        },
        {
            "cluster": "3D/SLAM과 reconstruction이 visual fidelity에서 online geometry contract로 이동",
            "papers": [
                p("2607.15211", "geometry", "MAGiSt3R"),
                p("2607.14481", "geometry", "Immediate 3DGS"),
                p("2607.14203", "geometry", "Instant NuRec"),
                p("2607.14639", "geometry", "Image-to-Point Cloud Registration"),
                p("2607.15048", "geometry", "RoGS"),
                p("2607.12265", "geometry", "DiffRadar"),
            ],
            "why": (
                "3D/Scene은 51편으로 두껍고, 이번 주 신호는 Gaussian이나 feed-forward reconstruction이 예쁜 rendering asset을 넘어 로봇 map contract가 되는 방향입니다. "
                "MAGiSt3R와 Immediate 3DGS는 unordered/monocular input에서 바로 geometry를 만들고, Instant NuRec과 RoGS는 driving/road-surface mapping으로 내려옵니다. "
                "Image-to-point-cloud registration과 DiffRadar는 camera-LiDAR/radar alignment와 pose drift를 직접 건드립니다. "
                "이 축은 photometric score가 아니라 localization, update cost, memory footprint, dynamic-object failure를 함께 봐야 합니다."
            ),
            "confidence": "High — feed-forward reconstruction, Gaussian map, LiDAR/radar registration, road mapping 신호가 동시에 반복",
            "lab_action": (
                "같은 driving/robot camera trajectory에서 3DGS map, point-cloud registration, feed-forward reconstruction을 비교하고 "
                "localization success, update cost, dynamic-object failure, downstream navigation cost를 측정한다."
            ),
        },
        {
            "cluster": "World-action safety와 driving simulation이 imagined future에서 executable scenario validity로 이동",
            "papers": [
                p("2607.15207", "world", "BadWAM"),
                p("2607.14727", "world", "WorkDrive"),
                p("2607.14005", "world", "M4World"),
                p("2607.13028", "world", "TerraZero"),
                p("2607.14455", "world", "Model-Based Diffusion Planning"),
                p("2607.14387", "world", "Chat2Scenic"),
            ],
            "why": (
                "Generation은 69편이지만 weekly thesis는 샘플 품질보다 실행 가능한 scenario와 action alignment입니다. "
                "BadWAM은 imagined future가 맞아도 action channel이 틀릴 수 있음을 보이고, WorkDrive와 TerraZero는 roadwork/long-tail scenario를 closed-loop 실패 조건으로 재현합니다. "
                "M4World, diffusion planning, Chat2Scenic은 world model과 planner를 따로 평가하지 말고 constraint, intent, scenario validity가 실제 action을 어떻게 바꾸는지 보라는 신호입니다."
            ),
            "confidence": "Medium-High — WAM safety, driving causation, procedural simulation, constrained planning이 같은 실행 검증 축으로 연결",
            "lab_action": (
                "RoboTwin/LIBERO와 CARLA에서 visual perturbation, relation violation, roadwork cue removal, generated scenario seed를 stress split으로 만들고 "
                "imagined-future drift, action shift, collision margin, recovery behavior를 비교한다."
            ),
        },
        {
            "cluster": "Embodied memory가 complete map과 episode reset에서 just-in-time persistent state로 이동",
            "papers": [
                p("2607.14514", "memory", "VTM-Nav"),
                p("2607.14252", "memory", "MEMORA"),
                p("2607.14586", "memory", "SoftNav"),
                p("2607.13245", "memory", "JITOMA"),
                p("2607.12630", "memory", "Instance-Enriched Semantic Maps"),
                p("2607.13653", "memory", "Open-World Mobile Manipulation"),
            ],
            "why": (
                "Embodied AI는 33편으로 중간 규모지만, memory와 navigation의 research decision은 분명합니다. "
                "JITOMA는 full scene graph가 planner를 포화시킬 수 있음을 보이고, VTM-Nav와 MEMORA는 cross-episode scene/action memory를 runtime state로 올립니다. "
                "SoftNav, instance-enriched semantic maps, open-world mobile manipulation은 더 많은 memory를 쌓는 방식이 아니라 instruction에 맞게 열리고 닫히는 state growth가 중요하다는 점을 강화합니다."
            ),
            "confidence": "Medium-High — semantic map, action memory, 3D scene tokens, just-in-time graph growth 신호가 반복",
            "lab_action": (
                "ObjectNav/mobile manipulation에서 no-memory, transcript memory, visual-topological memory, scene-graph growth를 비교하고 "
                "SPL, stale-memory failure, wrong-turn recovery, hidden-dependency miss를 평가한다."
            ),
        },
        {
            "cluster": "Multimodal 신뢰성과 효율화가 headline score에서 evidence contract와 task-critical retention으로 이동",
            "papers": [
                p("2607.15241", "trust", "Beyond the Leaderboard"),
                p("2607.15216", "trust", "Symbal"),
                p("2607.14737", "trust", "GeoDetect"),
                p("2607.14935", "trust", "VideoChat3"),
                p("2607.13500", "trust", "Attention-Free Token Reduction"),
                p("2607.13481", "trust", "GPOcc++"),
            ],
            "why": (
                "Foundation Models 50편, Safety 33편, Efficiency 38편은 별개 버킷처럼 보이지만 같은 평가 질문을 공유합니다. "
                "Beyond the Leaderboard와 Symbal은 정답률보다 systematic mismatch와 evaluator contract를 묻고, GeoDetect는 geometric adversarial signal을 별도 failure family로 만듭니다. "
                "VideoChat3, token reduction, GPOcc++는 더 빠르고 큰 모델보다 어떤 visual evidence와 geometry prior가 남아야 downstream task가 유지되는지 확인해야 함을 보여줍니다."
            ),
            "confidence": "Medium — VLM reliability와 efficiency 신호가 강하지만 공통 benchmark는 아직 분산",
            "lab_action": (
                "VQA/VLN/occupancy task에서 cue removal, geometry corruption, token budget, visual-prior ablation을 함께 두고 "
                "evidence recall, calibration shift, occupancy error, downstream action delta를 비교한다."
            ),
        },
    ]

    top5 = [
        (clusters[0]["papers"][0], "VLA의 action-facing interface를 별도 진단 대상으로 세워 이번 주 VLA 축을 가장 잘 대표합니다."),
        (clusters[1]["papers"][0], "vision-only VLA chunk가 놓치는 force state를 post-training 축으로 끌어올립니다."),
        (clusters[2]["papers"][0], "feed-forward multi-agent reconstruction을 robot-usable geometry contract 쪽으로 밀어붙입니다."),
        (clusters[3]["papers"][0], "world-action model의 imagined future와 executable action이 분리될 수 있음을 직접 드러냅니다."),
        (clusters[4]["papers"][0], "cross-episode memory를 embodied navigation의 기본 평가 축으로 올립니다."),
    ]

    research_autopsy = [
        {
            "title": "Action-facing representation을 action head 밖에서 계측한다",
            "source": "2026-07-17 RI synthesis",
            "evidence": "Action QFormer, FoMoVLA, Reflex, DiMaS는 action supervision이 visual token selection과 streaming latency를 함께 바꾸는지 묻습니다.",
            "falsification": "같은 query/latency stress split에서 representation 차이가 failure family를 바꾸지 못하면 이 해석은 약해집니다.",
            "aprl_tool": "VLA 실험표에 action-facing interface stress split을 기본 열로 둡니다.",
        },
        {
            "title": "Contact state는 policy 내부 memory가 아니라 관측 가능한 평가축이다",
            "source": "2026-07-17 daily cluster",
            "evidence": "force injection, force-torque proxy, tactile grounding, KineFuse가 모두 vision-only manipulation의 숨은 상태를 겨냥합니다.",
            "falsification": "force/tactile ablation이 insertion/folding/in-hand tracking failure를 분리하지 못하면 contact observability thesis는 약합니다.",
            "aprl_tool": "force memory length와 tactile prediction target을 failure-warning lead time과 함께 봅니다.",
        },
        {
            "title": "Geometry quality는 rendering이 아니라 downstream map contract로 인정한다",
            "source": "2026-07-15 to 2026-07-17 RI frontier memory",
            "evidence": "DiffRadar, Instant NuRec, MAGiSt3R, image-to-point-cloud registration이 pose drift, throughput, map update를 직접 건드립니다.",
            "falsification": "ATE와 downstream navigation cost가 좋아지지 않으면 Gaussian/reconstruction novelty는 robot-useful map으로 보기 어렵습니다.",
            "aprl_tool": "3D/SLAM benchmark에 localization, update cost, dynamic-object failure를 동시에 넣습니다.",
        },
        {
            "title": "World model safety는 future image quality가 아니라 action alignment다",
            "source": "2026-07-17 RI decision cards",
            "evidence": "BadWAM과 WAM steering은 future prediction이 좋아도 action channel이 공격되거나 misaligned될 수 있음을 전제로 둡니다.",
            "falsification": "future/action divergence가 closed-loop failure와 상관하지 않으면 WAM safety metric으로 쓰기 어렵습니다.",
            "aprl_tool": "imagined-future drift와 action shift를 같은 rollout에서 측정합니다.",
        },
        {
            "title": "Memory는 많이 쌓는 자산이 아니라 필요한 state를 늦지 않게 여는 runtime 계약이다",
            "source": "2026-07-16 to 2026-07-17 RI synthesis",
            "evidence": "JITOMA, HRIBench, VTM-Nav, MEMORA가 complete state보다 task-relevant state growth와 persistent retrieval을 강조합니다.",
            "falsification": "persistent memory가 stale-state failure를 늘리면 memory-first 설계는 오히려 deployment risk가 됩니다.",
            "aprl_tool": "memory horizon보다 state opening latency와 false retention을 측정합니다.",
        },
    ]

    strategy_board = [
        {
            "opportunity": "Action-facing VLA interface stress suite",
            "portfolio": "Build moat",
            "why_now": "VLA papers now expose representation, streaming, semantic retention, and force state as separate failure sources.",
            "contrarian_bet": "APRL can own the failure interface rather than chase another VLA backbone.",
            "one_week_probe": "Run one LIBERO/RoboCasa task with latency jitter, query-interface ablation, and instruction paraphrase stress.",
            "four_week_build": "Reusable VLA interface stress suite with semantic-retention and failure-warning metrics.",
            "success_metric": "At least two VLA variants with equal success but different failure-warning or semantic-retention signatures.",
            "stop_condition": "If interface stress does not change failure taxonomy beyond normal random seed variance.",
            "asset_path": "Benchmark scripts, stress splits, and taxonomy of action-facing failures.",
        },
        {
            "opportunity": "Robot-usable Gaussian geometry harness",
            "portfolio": "Exploit",
            "why_now": "3DGS and feed-forward reconstruction papers are moving into road mapping, SLAM, and LiDAR registration.",
            "contrarian_bet": "Measure pose drift and navigation utility before visual quality.",
            "one_week_probe": "Compare one Gaussian map and one point-cloud baseline on a short indoor/outdoor trajectory.",
            "four_week_build": "Trajectory suite with dynamic-object corruption, update cost, and downstream navigation hooks.",
            "success_metric": "A geometry representation changes navigation or localization failure while photometric score stays ambiguous.",
            "stop_condition": "If all methods rank identically under visual quality and robot metrics.",
            "asset_path": "Robot-usable map evaluation protocol and logged trajectory pack.",
        },
        {
            "opportunity": "World-action safety divergence benchmark",
            "portfolio": "Explore",
            "why_now": "BadWAM and driving scenario papers make future/action mismatch measurable.",
            "contrarian_bet": "Safety failures can be detected as divergence between generated future and executable action, not only outcome failure.",
            "one_week_probe": "Inject one visual relation perturbation and one roadwork cue removal into existing rollout logs.",
            "four_week_build": "Closed-loop divergence benchmark across WAM, driving, and embodied agent settings.",
            "success_metric": "Future/action divergence predicts unsafe or unrecoverable behavior earlier than final task failure.",
            "stop_condition": "If divergence metrics fail to rank risky rollouts before collision or task failure.",
            "asset_path": "Stress scenarios and divergence metric implementation.",
        },
    ]

    payload = {
        "date": DATE,
        "iso_week": WEEK,
        "week_start": WEEK_START,
        "week_end": WEEK_END,
        "source_mode": "pastweek",
        "source_listing_date": LISTING_DATE,
        "source_daily_artifacts": DAILY_DATES,
        "weekly_thesis": (
            "이번 주의 핵심은 VLA, tactile manipulation, 3D/SLAM, world-action safety, embodied memory, VLM reliability가 모두 "
            "더 큰 모델보다 실패가 시작되는 interface와 state contract를 검증하는 방향으로 수렴했다는 점입니다."
        ),
        "totals": snapshot["totals"],
        "daily_totals": daily["totals"],
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
        "research_autopsy": research_autopsy,
        "strategy_board": strategy_board,
    }

    Path("weekly").mkdir(exist_ok=True)
    Path("weekly", f"{WEEK}.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    trends_payload = {
        **snapshot,
        "source_mode": "pastweek",
        "source_listing_date": LISTING_DATE,
        "source_daily_artifacts": DAILY_DATES,
        "daily_artifact_totals": daily["totals"],
    }
    Path("trends", f"{DATE}.json").write_text(json.dumps(trends_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

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

    top5_html = "".join(f"<li><strong>{paper_link(p)}</strong><p>{esc(why)}</p></li>" for p, why in top5)
    autopsy_html = "".join(
        "<article class='card'>"
        f"<h3>{esc(item['title'])}</h3>"
        f"<p><strong>Source</strong> {esc(item['source'])}</p>"
        f"<p><strong>Evidence</strong> {esc(item['evidence'])}</p>"
        f"<p><strong>Falsification frontier</strong> {esc(item['falsification'])}</p>"
        f"<p><strong>APRL tool</strong> {esc(item['aprl_tool'])}</p>"
        "</article>"
        for item in research_autopsy
    )
    strategy_html = "".join(
        "<article class='card strategy'>"
        f"<h3>{esc(item['opportunity'])} <span>{esc(item['portfolio'])}</span></h3>"
        f"<p><strong>Why now</strong> {esc(item['why_now'])}</p>"
        f"<p><strong>Contrarian bet</strong> {esc(item['contrarian_bet'])}</p>"
        f"<p><strong>1-week probe</strong> {esc(item['one_week_probe'])}</p>"
        f"<p><strong>4-week build</strong> {esc(item['four_week_build'])}</p>"
        f"<p><strong>Success metric</strong> {esc(item['success_metric'])}</p>"
        f"<p><strong>Stop condition</strong> {esc(item['stop_condition'])}</p>"
        f"<p><strong>Asset path</strong> {esc(item['asset_path'])}</p>"
        "</article>"
        for item in strategy_board
    )

    css = """
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:#f6f8fa;color:#24292f;margin:0;padding:28px 12px;line-height:1.62}
.container{max-width:1080px;margin:0 auto;background:#fff;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.06),0 1px 2px rgba(0,0,0,.04);padding:40px 48px}
h1{font-size:28px;margin:0 0 6px;color:#0d1117}h2{font-size:21px;margin:40px 0 14px;padding-bottom:8px;border-bottom:2px solid #e5e7eb}h3{font-size:16px;margin:10px 0 4px}
a{color:#0969da;text-decoration:none}a:hover{text-decoration:underline}.home{display:inline-block;padding:6px 14px;font-size:13px;color:#0969da;background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;margin:0 0 18px}
.meta{font-size:13px;color:#3b434d;padding:14px 18px;background:#f6f8fa;border-left:3px solid #7c3aed;border-radius:6px;margin:14px 0 22px}.thesis{background:#111827;color:#f8fafc;border-radius:10px;padding:18px 22px;margin:16px 0 28px;font-size:16px}.thesis strong{color:#fde68a}
.cluster-table{width:100%;table-layout:fixed;border-collapse:collapse;font-size:13px;margin:12px 0 18px}.cluster-table th,.cluster-table td{border:1px solid #d0d7de;padding:9px;vertical-align:top;overflow-wrap:anywhere;word-break:break-word}.cluster-table th{background:#f6f8fa;color:#0d1117}
.takeaway{margin:-4px 0 24px;padding:12px 16px;background:#fff8e1;border-left:3px solid #f59e0b;border-radius:6px;color:#3b434d;font-size:14px}.bucket-line{font-family:ui-monospace,SFMono-Regular,Consolas,Menlo,monospace;background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;padding:10px 14px;font-size:13px;white-space:pre-wrap}
.tag{display:inline-block;font-family:ui-monospace,SFMono-Regular,Consolas,Menlo,monospace;font-size:12px;color:#7c2d12;background:#fff7ed;border:1px solid #fed7aa;border-radius:6px;padding:1px 7px;margin:2px 3px 2px 0}.badge{display:inline-block;font-size:11px;font-weight:600;padding:1px 7px;border-radius:10px;margin-left:5px;background:#f3f4f6;color:#374151;border:1px solid #d1d5db}.phy{display:block;color:#475569;font-size:12.5px;margin-top:2px}
.card{background:#fafbfc;border:1px solid #e5e7eb;border-radius:8px;padding:14px 18px;margin:12px 0}.strategy h3 span{font-size:12px;color:#7c2d12;background:#fff7ed;border:1px solid #fed7aa;border-radius:999px;padding:2px 8px;margin-left:6px}ol li{margin:12px 0}footer{margin-top:40px;padding-top:16px;border-top:1px solid #eaeef2;font-size:12px;color:#656d76;text-align:center}
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
<div><strong>소스:</strong> arXiv cs.CV/pastweek + cs.RO/pastweek · source_mode=pastweek · /new listing_date={LISTING_DATE}</div>
<div><strong>주간 시야:</strong> {WEEK_START} ~ {WEEK_END} · committed daily artifacts {", ".join(DAILY_DATES)}</div>
<div><strong>pastweek corpus:</strong> {snapshot['totals']['total_scanned']} scanned · {snapshot['totals']['selected']} ROI selected</div>
<div><strong>daily corpus:</strong> cs.CV {daily['totals']['cv']} + cs.RO {daily['totals']['ro']} · {daily['totals']['total_scanned']} dedup · {daily['totals']['selected']} ROI</div>
</div>
<section class="thesis"><strong>주간 결론:</strong> {esc(payload['weekly_thesis'])}</section>
<h2>주간 클러스터 표</h2>
<table class="cluster-table"><thead><tr><th>Cluster</th><th>대표 논문</th><th>왜 중요?</th><th>Confidence</th><th>Lab action</th></tr></thead><tbody>
{''.join(cluster_rows)}
</tbody></table>
<p class="takeaway"><strong>이번 주의 핵심:</strong> 더 큰 VLA, 더 예쁜 3D, 더 긴 world model이 아니라, action-facing interface, contact state, online geometry, executable scenario, persistent memory를 실제 실패 조건에서 어떻게 분리해 검증할 것인가다.</p>
<h2>주간 동향</h2>
<p>이번 주 pastweek snapshot은 {snapshot['totals']['total_scanned']}편을 스캔했고 ROI {snapshot['totals']['selected']}편을 선별했습니다. {esc(bucket_line(snapshot))}. Robot Learning이 83편으로 가장 두껍고, Generation 69편, 3D/Scene 51편, Foundation Models 50편이 뒤따릅니다. 하지만 주간 thesis는 양보다 research decision입니다. VLA, tactile manipulation, 3D/SLAM, world-action safety, embodied memory, VLM reliability가 모두 같은 방향, 즉 실패가 시작되는 interface와 state contract를 따로 측정하는 쪽으로 모였습니다.</p>
<div class="bucket-line">{esc(bucket_line(snapshot))}</div>
<h2>주간 Top 5</h2>
<ol>{top5_html}</ol>
<h2>주간 논문 사고 해부</h2>
{autopsy_html}
<h2>APRL Leading Group Strategy Board</h2>
{strategy_html}
<footer>Generated from repo parser outputs and committed daily Research Intelligence artifacts. WebFetch was not used for arXiv source data. Link: {SITE_URL}/posts/{DATE}-weekly.html</footer>
</main></body></html>
"""
    Path("posts").mkdir(exist_ok=True)
    Path("posts", f"{DATE}-weekly.html").write_text(html_doc, encoding="utf-8", newline="\n")
    print(f"wrote weekly/{WEEK}.json and posts/{DATE}-weekly.html")


if __name__ == "__main__":
    build()
