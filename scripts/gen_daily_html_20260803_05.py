#!/usr/bin/env python3
"""Generate daily briefing artifacts for the 2026-08-03..05 catch-up run."""

from __future__ import annotations

import json
import re
from pathlib import Path

from daily_backfill_lib import build, week_start
from gen_research_intelligence_20260803_05 import RI_BY_DATE


ROOT = Path(__file__).resolve().parents[1]


PROFILES = {
    "2026-08-03": {
        "date": "2026-08-03",
        "weekday": "Mon",
        "week_start": week_start("2026-08-03"),
        "source_mode": "pastweek-date-section",
        "source_label": "arXiv cs.CV/pastweek + cs.RO/pastweek date section",
        "source_note": "Backfilled from the matching 2026-08-03 arXiv /pastweek date sections",
        "benchmark_note": (
            "Daily artifact generated from the 2026-08-03 /pastweek date sections. "
            "Daily paper cards are title/subject based; Research Intelligence records official arXiv abstract/HTML evidence for Tier A."
        ),
        "thesis": (
            "The August 3 backfill says that robot policies are no longer failing only because they lack scale; "
            "they fail because temporal critic state, camera geometry, action-relevant futures, and sparse moving-object geometry are untyped. "
            "WCM, RayViT, ST-WAM, and CorrelationFlow point to the same operating model: before APRL collects more demonstrations, "
            "it should expose the hidden state channel that the next action actually depends on."
        ),
        "cluster_takeaway": "The useful signal is typed state for policy repair, not another undifferentiated VLA scaling run.",
        "trend_note": (
            "The small Monday corpus still has 15 robot-learning papers and 10 3D/Scene papers. The strong thread is interface repair: "
            "critic history, camera rays, semantic-temporal WAM state, LiDAR flow geometry, and attention-head hallucination signals."
        ),
        "cluster_specs": [
            {
                "title": "VLA repair moves from action heads to critic and safety state",
                "buckets": ["Robot Learning", "Generation", "Safety/Alignment"],
                "ids": ["2607.29613", "2607.29596", "2607.28993", "2607.29169", "2607.29569"],
                "needles": ["critic", "vla", "world action", "safety", "barrier", "temporal", "fibonacci", "consistency"],
                "why": (
                    "WCM makes the critic history-aware, FibVLA changes temporal sampling, ST-WAM asks whether future state survives visual shift, "
                    "ActFovea safeguards visual-action consistency at runtime, and barrier-enhanced flow matching adds an explicit safety layer. "
                    "The shared decision is to type the state that makes a VLA update trustworthy."
                ),
                "confidence": "High",
                "confidence_note": "Multiple VLA papers independently expose critic, temporal, WAM, and safety-state variables.",
                "lab_action": "Run one VLA with critic-history, temporal sampling, visual-shift WAM, and runtime safety gates toggled separately under the same manipulation tasks.",
                "limit": 5,
            },
            {
                "title": "Viewpoint robustness becomes a camera-geometry interface problem",
                "buckets": ["Robot Learning", "3D/Scene"],
                "ids": ["2607.29622", "2607.29037", "2607.29237", "2607.29136", "2607.28994"],
                "needles": ["ray", "viewpoint", "camera", "geometry", "point cloud", "reconstruction", "lidar"],
                "why": (
                    "RayViT injects camera-ray structure into imitation learning, GO-PRE chooses views by predictive rendering entropy, "
                    "CorrelationFlow keeps a geometric LiDAR baseline, and point-cloud model papers ask what 3D evidence remains usable after compression or transfer. "
                    "The common evaluation axis is whether geometry survives viewpoint change."
                ),
                "confidence": "High",
                "confidence_note": "Robot and 3D papers both target view, ray, point, and flow evidence.",
                "lab_action": "Compare RGB-only, ray-conditioned, and point/flow-conditioned policies under fixed camera-shift, sparse-object, and active-view stress splits.",
                "limit": 5,
            },
            {
                "title": "Contact-rich manipulation needs phase, stiffness, and tactile variables",
                "buckets": ["Robot Learning"],
                "ids": ["2607.29567", "2607.29285", "2607.29271", "2607.29231", "2607.29102", "2607.29625"],
                "needles": ["contact", "tactile", "stiffness", "teleoperation", "transparent", "phase", "humanoid"],
                "why": (
                    "TransGraspNet, TRACT, MDIR, TacPrint, VSTaI, and humanoid mass-balancing papers all make physical interaction variables explicit. "
                    "They do not ask whether a policy succeeds on average; they ask which phase, stiffness, mass, or contact cue makes the action valid."
                ),
                "confidence": "Medium-High",
                "confidence_note": "The evidence is concentrated in robotics but spans labware, action chunks, teleoperation, and tactile devices.",
                "lab_action": "Compare contact-rich policies across phase labels, force/stiffness cues, tactile availability, object material, and recovery success.",
                "limit": 6,
            },
            {
                "title": "VLM reliability shifts toward evidence routing and prior calibration",
                "buckets": ["Foundation Models", "Safety/Alignment"],
                "ids": ["2607.29638", "2607.29412", "2607.29240", "2607.28969", "2607.28640", "2607.29445"],
                "needles": ["evidence", "hallucination", "prior", "safety", "token", "thermal", "trigger", "routing"],
                "why": (
                    "HierDoc routes page-region evidence, Role-Break diagnoses hallucination through attention-head roles, selective prior calibration handles commonsense conflict, "
                    "SafeNexus steers safety neurons, TokenSwap probes modality gaps, and thermal triggers expose sensor-specific attacks. "
                    "The common issue is whether visual evidence or a prior is steering the answer."
                ),
                "confidence": "High",
                "confidence_note": "Evidence routing, hallucination, prior conflict, and safety steering appear in separate VLM papers.",
                "lab_action": "Stress one robot VLM prompt by varying evidence region, prior conflict, attention-role anomaly, kept tokens, and final action outcome.",
                "limit": 6,
            },
            {
                "title": "Autonomy planning distills intent and outcome instead of perception score",
                "buckets": ["Autonomous Driving", "Embodied AI"],
                "ids": ["2607.29517", "2607.29052", "2607.29031", "2607.29011", "2607.29600", "2607.29009"],
                "needles": ["driving", "outcome", "intent", "stage", "navigation", "collaboration", "reachability"],
                "why": (
                    "STAGE personalizes action generation, outcome-guided distillation targets driving reasoning, Auto-JEPA models continuous intent, "
                    "DART handles reachability-gated vehicle jumps, and VLN/multi-robot papers add memory and collaboration. "
                    "The planning signal is moving from perception score to intent, outcome, and recoverable reachability."
                ),
                "confidence": "Medium",
                "confidence_note": "The cluster is smaller but ties driving, VLN, and multi-robot planning around outcome-conditioned state.",
                "lab_action": "Evaluate one navigation stack by intent error, reachable recovery, memory handoff, and outcome-guided correction rather than route success alone.",
                "limit": 6,
            },
        ],
        "research_topics": [
            {"title": "Typed-state VLA audit", "claim": "Ablate critic history, camera rays, WAM future state, and safety gates under identical policy and task conditions."},
            {"title": "Contact-phase failure grid", "claim": "Label each manipulation failure by phase, stiffness, tactile cue, and recovery action before adding new demonstrations."},
            {"title": "Evidence-prior VLM ablation", "claim": "Separate visual evidence, commonsense prior, token compression, and safety-neuron steering in robot VLM decisions."},
        ],
    },
    "2026-08-04": {
        "date": "2026-08-04",
        "weekday": "Tue",
        "week_start": week_start("2026-08-04"),
        "source_mode": "pastweek-date-section",
        "source_label": "arXiv cs.CV/pastweek + cs.RO/pastweek date section",
        "source_note": "Backfilled from the matching 2026-08-04 arXiv /pastweek date sections",
        "benchmark_note": (
            "Daily artifact generated from the large 2026-08-04 /pastweek date sections. "
            "Daily paper cards are title/subject based; Research Intelligence records official arXiv abstract/HTML evidence for Tier A."
        ),
        "thesis": (
            "The August 4 backlog is a state-validity stress test. Contact-rich VLAs expose precision, force, tactile, and trajectory-prior failures; "
            "world models are evaluated by reactivity and navigation usefulness; and VLM compression moves from fewer tokens to preserved evidence messages. "
            "For APRL, this points to a single benchmark family: when execution state, visual evidence, or map geometry goes stale, the robot must know which state to refresh."
        ),
        "cluster_takeaway": "The large Tuesday corpus turns contact, memory, geometry, and compression into one state-validity problem.",
        "trend_note": (
            "Tuesday has unusually high volume: 431 deduplicated papers and 194 ROI papers. The dominant robotics signals are contact-rich VLA failure diagnosis, "
            "world-action models for navigation/manipulation, geometry as driving-test substrate, and evidence-preserving VLM compression."
        ),
        "cluster_specs": [
            {
                "title": "Contact-rich VLAs expose where physical state enters policy",
                "buckets": ["Robot Learning"],
                "ids": ["2608.01452", "2608.01402", "2608.02326", "2608.01824", "2608.01102", "2608.00547", "2608.02497"],
                "needles": ["contact", "vla", "dynamic", "tactile", "force", "execution", "state", "manipulation"],
                "why": (
                    "DynamicManip, the VLA contact-failure diagnosis paper, ChainVLA, ReTouch, CAAT, visuo-tactile WAM, and semantic re-binding all ask where physical state enters a policy. "
                    "The shared decision is to stop treating contact failure as a scalar success-rate drop and label the state channel that failed."
                ),
                "confidence": "High",
                "confidence_note": "The Tuesday robotics bucket has many independent contact, tactile, and VLA-state papers.",
                "lab_action": "Replay contact-rich failures with labels for precision error, force/tactile cue, execution-state age, replan boundary, and corrective action.",
                "limit": 7,
            },
            {
                "title": "World models are judged by reactivity and navigation effect",
                "buckets": ["Generation", "Robot Learning", "Embodied AI"],
                "ids": ["2608.02603", "2608.02428", "2608.01397", "2608.00793", "2608.00635", "2608.01221", "2608.01127"],
                "needles": ["world", "reactivity", "navigation", "wam", "dynamic", "flow", "diffusion"],
                "why": (
                    "WorldExam asks whether generated worlds react, DF3 and FlowPilot bring world modeling into navigation, SG-WAM and DynamicWAM bind WAMs to policy space, "
                    "EndoWAM grounds endoscopic navigation, and MiniWorld targets video world-model training. "
                    "The common test is no longer visual plausibility; it is whether the proxy changes navigation or manipulation decisions."
                ),
                "confidence": "High",
                "confidence_note": "World-model papers span benchmarks, navigation, WAMs, and training systems.",
                "lab_action": "Compare each WAM's predicted reactive state against the chosen action, real rollout result, and failure family under shifted dynamics.",
                "limit": 7,
            },
            {
                "title": "Geometry and SLAM become calibration and driving-test substrate",
                "buckets": ["3D/Scene", "Autonomous Driving", "Foundation Models"],
                "ids": ["2608.02309", "2608.01914", "2608.01761", "2608.02177", "2608.02145", "2608.02206", "2608.01338", "2608.00518"],
                "needles": ["calibration", "slam", "3d", "gaussian", "driving", "bev", "spatial", "grounding"],
                "why": (
                    "CalibBEV, CHOW-SLAM, DecoupleGS, GSRAIN, UniqueSplat, CLEAR, Driver2Map, and 3D visual grounding papers treat geometry as an evaluation substrate, not only a rendering artifact. "
                    "The decision is to measure whether calibration, map representation, or sparse-view reconstruction changes downstream driving and robot grounding."
                ),
                "confidence": "High",
                "confidence_note": "The geometry count is large and includes SLAM, calibration, Gaussians, driving tests, and spatial grounding.",
                "lab_action": "Compare map/calibration variants by localization drift, BEV decision error, dynamic-object failure, and downstream control recovery.",
                "limit": 8,
            },
            {
                "title": "VLM compression must preserve grounded evidence, not just tokens",
                "buckets": ["Foundation Models", "Efficiency/Systems"],
                "ids": ["2608.02134", "2608.01985", "2608.01979", "2608.01644", "2608.01185", "2608.00345", "2608.00077"],
                "needles": ["token", "compression", "evidence", "coreset", "pruning", "3d", "ocr", "faithful"],
                "why": (
                    "Messages Not Tokens, DiffPrune, ET-Prune, CRAFT, 3DZip, ORCA, and spatial-provenance pruning all ask what evidence survives visual compression. "
                    "For robot VLMs, the useful metric is whether task-critical visual evidence remains actionable after pruning."
                ),
                "confidence": "High",
                "confidence_note": "Several independent compression papers explicitly discuss evidence, token pruning, and spatial provenance.",
                "lab_action": "Run fixed-compute VLM decisions with token count, preserved evidence region, spatial provenance, answer, and robot action effect recorded together.",
                "limit": 7,
            },
            {
                "title": "Embodied replanning shifts from route search to memory budget",
                "buckets": ["Embodied AI", "Efficiency/Systems"],
                "ids": ["2608.01690", "2608.01428", "2608.00613", "2608.00527", "2608.00970", "2608.01456"],
                "needles": ["replanning", "embodied", "memory", "navigation", "protocol", "spatial", "topological"],
                "why": (
                    "ProtoAct, budgeted replanning, DynamicEnvPlan, SSTG-Nav, FreqNav, and long-horizon memory compression all separate semantic progress from local execution cost. "
                    "The shared issue is when an embodied agent should spend memory or replanning budget."
                ),
                "confidence": "Medium-High",
                "confidence_note": "The embodied papers share memory, replanning, and reusable spatial state even across different platforms.",
                "lab_action": "Evaluate embodied agents by progress-state error, replan trigger timing, memory compression loss, and recovery success after wrong-local-step events.",
                "limit": 6,
            },
            {
                "title": "Agent and VLA safety moves toward physical attention hijacking",
                "buckets": ["Safety/Alignment", "Robot Learning", "Foundation Models"],
                "ids": ["2608.02018", "2608.01028", "2608.00975", "2608.00068", "2608.02137", "2608.01258"],
                "needles": ["adversarial", "safety", "hijacking", "attack", "monitor", "benchmark", "agent"],
                "why": (
                    "Invisible Ink, VLAGuard, MonitorVLM-v2, SafeBuild-Bench, cross-task VLM attacks, and generated-image detection benchmarks show safety risk shifting from text-only jailbreaks to task-embedded visual and physical triggers. "
                    "A robot safety benchmark should therefore include where the unsafe goal enters the perception-action loop."
                ),
                "confidence": "Medium",
                "confidence_note": "The safety papers span agents, VLMs, construction, and VLA physical attention.",
                "lab_action": "Inject legitimate-looking visual, wireless, and task-goal triggers into a VLA scenario, then compare attention target, safety monitor state, and action deviation.",
                "limit": 6,
            },
        ],
        "research_topics": [
            {"title": "Contact-rich execution-state benchmark", "claim": "Separate precision, force, tactile, memory, and replanning failures in the same manipulation suite."},
            {"title": "Reactive world-model audit", "claim": "Evaluate WAMs by real decision change and failure prediction, not visual plausibility."},
            {"title": "Evidence-preserving token compression", "claim": "Measure whether pruned VLM tokens preserve the exact visual evidence needed for robot action."},
        ],
    },
    "2026-08-05": {
        "date": "2026-08-05",
        "weekday": "Wed",
        "week_start": week_start("2026-08-05"),
        "source_mode": "new",
        "source_label": "arXiv cs.CV/new + cs.RO/new",
        "source_note": "Direct parser output from matching 2026-08-05 /new listings",
        "benchmark_note": (
            "Daily artifact generated from the matching 2026-08-05 arXiv /new listings. "
            "The parser includes abstracts; Research Intelligence records official arXiv abstract/HTML evidence for Tier A."
        ),
        "thesis": (
            "The August 5 batch asks when an agent should trust, refresh, or discard internal state. Quo Vadis broadens world models into feedback proxies, "
            "SLAMFormer-infinity removes fixed-distance assumptions from map memory, Continue or Replan turns action horizons into a learned validity decision, "
            "and DRIFT attacks the denoising trajectory before the final VLA action. APRL should build a state-validity benchmark that couples map memory, "
            "replanning, proprioception, and physical attention attacks."
        ),
        "cluster_takeaway": "Today's useful signal is state validity across world models, SLAM, VLA execution, and safety.",
        "trend_note": (
            "The Wednesday /new listing is dense: 190 deduplicated papers and 161 ROI papers. The important thread is not volume; it is that world proxies, "
            "unbounded SLAM memory, adaptive action chunks, proprioceptive state, and adversarial denoising all expose when internal state becomes stale."
        ),
        "cluster_specs": [
            {
                "title": "World models become feedback proxies for action decisions",
                "buckets": ["Generation", "Robot Learning", "Autonomous Driving"],
                "ids": ["2608.02713", "2608.03211", "2608.03701", "2607.26657", "2608.02990", "2608.03084", "2608.02958"],
                "needles": ["world", "wam", "feedback", "action", "video", "driving", "latent", "reasoning"],
                "why": (
                    "Quo Vadis reframes world models as agent feedback proxies, CrossScope and LiLa-WAM specialize WAMs for surgical or manipulation state, "
                    "Enfold and EmbodiedVAE compress embodied predictive representations, SUV treats future driving scene understanding as video generation, and ValueFormer adds causal value labels. "
                    "The shared question is what internal proxy changes the next action."
                ),
                "confidence": "High",
                "confidence_note": "World-model papers appear across Generation, Robot Learning, and Driving with explicit action or value links.",
                "lab_action": "Classify each world proxy by feedback type, state variable, action it changes, real rollout metric, and stop condition when proxy and reality diverge.",
                "limit": 7,
            },
            {
                "title": "VLA execution horizons become learned state-validity tests",
                "buckets": ["Robot Learning", "Embodied AI"],
                "ids": ["2608.03483", "2608.03052", "2608.02958", "2608.03563", "2608.03753", "2608.03116", "2608.02653"],
                "needles": ["replan", "proprioceptive", "value", "target", "long-horizon", "contact", "locomotion"],
                "why": (
                    "Continue or Replan learns when a chunk is stale, the proprioception paper asks how VLA state should enter, ValueFormer adds stage-aware value labels, "
                    "Unified Visuomotor Targets supervises beyond physical actions, GORDON decomposes long-horizon rewards, and contact/locomotion papers expose where execution state fails. "
                    "The action policy is becoming an online validity monitor."
                ),
                "confidence": "High",
                "confidence_note": "Several robotics papers directly target horizon, state input, value, reward, and contact validity.",
                "lab_action": "Ablate chunk age, continuation probability, proprioception window, stage value, and reward decomposition against failure onset in one VLA manipulation suite.",
                "limit": 7,
            },
            {
                "title": "SLAM and 3D grounding need unbounded memory plus calibration checks",
                "buckets": ["3D/Scene", "Foundation Models"],
                "ids": ["2608.03429", "2608.03296", "2608.03423", "2608.02883", "2608.03109", "2608.03279", "2608.02980"],
                "needles": ["slam", "calibration", "registration", "3d", "grounding", "feature", "skeleton", "quality"],
                "why": (
                    "SLAMFormer-infinity changes the memory coordinate problem, PLS-Calib binds event cameras and odometry under ground constraints, SGFormer and point-cloud registration handle local matching, "
                    "plant-root phenotyping and 3DGS assessment expose downstream structure/quality, and Qwen-3D pushes 3D VLM spatial understanding. "
                    "Geometry is valuable only when map memory and calibration remain valid."
                ),
                "confidence": "High",
                "confidence_note": "3D/Scene has explicit SLAM, calibration, registration, 3D grounding, and 3D quality assessment papers.",
                "lab_action": "Run map-memory stress with sequence length, calibration perturbation, local-feature failure, 3D quality score, and downstream localization or grounding success.",
                "limit": 7,
            },
            {
                "title": "VLM evidence scheduling replaces bigger context windows",
                "buckets": ["Foundation Models", "Efficiency/Systems"],
                "ids": ["2608.03918", "2608.03083", "2608.03112", "2608.03580", "2608.03471", "2608.03631", "2608.02833"],
                "needles": ["evidence", "token", "pruning", "scheduling", "grounding", "visual", "efficient", "look"],
                "why": (
                    "Adaptive visual evidence scheduling, global spatio-temporal token pruning, two-stage visual token pruning, SlimVLM, Hi-Token, SEER, and CURV all ask where the model should look and what evidence survives. "
                    "The hidden comparison is between larger context and better evidence allocation."
                ),
                "confidence": "High",
                "confidence_note": "Multiple papers independently target evidence schedules, token pruning, coordinate tokens, and grounded reasoning.",
                "lab_action": "For one robot VLM task, compare full context, scheduled evidence, token-pruned evidence, and coordinate-token grounding by action-level error.",
                "limit": 7,
            },
            {
                "title": "Safety shifts to denoising attacks and fail-passive physical systems",
                "buckets": ["Robot Learning", "Safety/Alignment", "Autonomous Driving", "Embodied AI"],
                "ids": ["2608.03207", "2608.03231", "2608.02809", "2608.02806", "2608.02811", "2608.02886", "2608.03060"],
                "needles": ["attack", "safety", "fail", "barrier", "monitor", "patch", "certified", "passive"],
                "why": (
                    "DRIFT attacks flow-matching VLA denoising, structure-aware fine-tuning defends against physical attention hijacking, fail-passive humanoid work asks for certified safety gaps, "
                    "object-removal attacks target video perception, monitoring under uncertainty adds runtime checks, and barrier/passive guidance papers make safety constraints explicit. "
                    "Safety is moving into the physical perception-action trajectory."
                ),
                "confidence": "High",
                "confidence_note": "Robot, video, monitoring, and control papers converge on physical failure and attack surfaces.",
                "lab_action": "Inject patch, object-removal, stale-monitor, and barrier-constraint failures into one robot scenario, then compare denoising drift, monitor alarm, and recovery action.",
                "limit": 7,
            },
            {
                "title": "Edge robot deployment becomes a memory and budget audit",
                "buckets": ["Robot Learning", "Efficiency/Systems", "Autonomous Driving"],
                "ids": ["2608.03938", "2608.03682", "2608.03051", "2608.03034", "2608.03924", "2608.03490", "2608.03159"],
                "needles": ["edge", "budget", "jetson", "cloud", "gpu", "efficient", "distillation", "planning"],
                "why": (
                    "Bimanual manipulation under an 8 GB Jetson budget, PhyAI edge/cloud rollouts, CUDA MPC, adaptive planning budgets, ETA, lightweight 3D detection, and trajectory distillation papers all make resource constraints operational. "
                    "The right deployment metric is not latency alone but whether memory, sensing, and compute budgets preserve task success."
                ),
                "confidence": "Medium-High",
                "confidence_note": "The papers span edge bimanual control, cloud-edge physical AI, MPC, embodied planning, and model distillation.",
                "lab_action": "Compare task success across memory budget, sensor-copy path, quantization level, planning budget, and recovery latency on an embedded robot target.",
                "limit": 7,
            },
        ],
        "research_topics": [
            {"title": "State-validity robot benchmark", "claim": "Cross stale map memory, stale action chunks, proprioceptive history loss, and physical attention attacks in one replay suite."},
            {"title": "World-proxy feedback taxonomy", "claim": "Classify WAMs and world proxies by the feedback channel that changes action choice and the stop condition when it fails."},
            {"title": "Evidence-scheduled robot VLM", "claim": "Compare full-context VLMs against scheduled and pruned evidence using action-level error, not answer accuracy alone."},
        ],
    },
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
    if not text:
        text = "Backfill source is title/subject only; use official arXiv abstract or HTML before making mechanism claims."
    return {
        "arxiv_id": paper.get("arxiv_id"),
        "title": paper.get("title"),
        "bucket": paper.get("bucket"),
        "reading_depth": ri_lookup.get(paper.get("arxiv_id"), "title-subject" if not paper.get("abstract") else "abstract-only"),
        "problem": text[:360],
        "method": "See Research Intelligence edition for the evidence trace and falsification note.",
        "meaning": "Included because it supports the day's cluster thesis and APRL strategy board.",
    }


def enrich_daily(date: str) -> None:
    insights_path = ROOT / "insights" / f"{date}.json"
    trends = load_json(ROOT / "trends" / f"{date}.json")
    insights = load_json(insights_path)
    classified = load_json(ROOT / "out" / "classified.json")
    papers = all_papers(classified)
    by_id = {p["arxiv_id"]: p for p in papers}
    ri = RI_BY_DATE[date]
    ri_ids = [paper["arxiv_id"] for paper in ri["papers"]]
    ri_lookup = {paper["arxiv_id"]: paper["status"] for paper in ri["papers"]}

    insights["source_listing_date"] = trends["source_listing_date"]
    insights["source_mode"] = trends["source_mode"]
    insights["daily_new_counts"] = trends["daily_new_counts"]
    insights["paper_autopsies"] = [abstract_card(by_id[pid], ri_lookup) for pid in ri_ids if pid in by_id]
    insights["frontier_memory"] = ri["frontier_memory"]
    insights["strategy_board"] = ri["strategy"]
    insights["tiering_note"] = (
        "Research Intelligence uses official arXiv abstract pages and available official HTML headings for selected Tier A papers. "
        "Backfill daily cards remain conservative when /pastweek omitted abstracts."
    )
    insights["research_intelligence"] = {
        "html": f"posts/{date}-research-intelligence.html",
        "json": f"intelligence/{date}.json",
        "source_prompt": ri["source_prompt"],
    }
    write_json(insights_path, insights)

    post_path = ROOT / "posts" / f"{date}.html"
    doc = post_path.read_text(encoding="utf-8")
    if "ri-callout" not in doc:
        doc = doc.replace(
            ".thesis strong{color:#fef08a}",
            ".thesis strong{color:#fef08a}.ri-callout{display:flex;justify-content:space-between;gap:16px;align-items:center;margin:-12px 0 28px;padding:14px 18px;border:1px solid #67e8f9;border-radius:10px;background:#ecfeff;color:#164e63}.ri-callout a{font-weight:750;white-space:nowrap}@media(max-width:760px){.ri-callout{align-items:flex-start;flex-direction:column}}",
        )
        ri_callout = (
            f"<section class=\"ri-callout\"><span><strong>Today's Research Intelligence</strong> "
            f"{len(ri['papers'])} Tier A candidates include official arXiv abstract/HTML evidence traces, adversarial reads, "
            f"frontier memory, and APRL strategy board.</span>"
            f"<a href=\"{date}-research-intelligence.html\">Open Research Intelligence</a></section>"
        )
        doc = re.sub(r"</section>\n(<h2>.*?</h2>)", f"</section>\n{ri_callout}\n\\1", doc, count=1, flags=re.S)
        post_path.write_text(doc, encoding="utf-8", newline="\n")


def main() -> int:
    sources = {
        "2026-08-03": ("out/cv_new_20260803.json", "out/ro_new_20260803.json"),
        "2026-08-04": ("out/cv_new_20260804.json", "out/ro_new_20260804.json"),
        "2026-08-05": ("out/cv_new_20260805.json", "out/ro_new_20260805.json"),
    }
    for date, profile in PROFILES.items():
        build(profile, *sources[date])
        enrich_daily(date)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
