#!/usr/bin/env python3
"""Generate the 2026-08-12 Research Intelligence edition."""

from __future__ import annotations

import json
from pathlib import Path

from gen_research_intelligence_20260811 import build_html


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PROMPT = "prompts/instruction_v20260713.md"


RI_BY_DATE = {
    "2026-08-12": {
        "date": "2026-08-12",
        "edition": "Research Intelligence",
        "source_prompt": SOURCE_PROMPT,
        "source_mode": "new",
        "scope_note": (
            "Daily edition from matching Wednesday /new listings: 148 non-replacement cs.CV rows, "
            "40 cs.RO rows, 180 deduplicated papers, and 151 ROI papers. Tier A cards are conservative "
            "abstract-only autopsies from the repository parser output; no figure/table claims are asserted."
        ),
        "executive_thesis": (
            "The August 12 batch turns yesterday's action-interface question into a harder release gate: which "
            "evidence is trusted enough to update a policy, map, cache, memory, or safety claim? Embodied Semantic "
            "3DGS, Surgical WAM, FACT, VIScore, Gated VLA-Cache, DriveVLA-M0, estimator spectral analysis, AD2-Bench, "
            "and Dual Stress all move from final score reporting toward introspective evidence contracts. APRL should "
            "treat this as a mandate to own stress benchmarks where update, reject, cache, retrieve, and intervene "
            "decisions are measured before aggregate success."
        ),
        "decision_cards": [
            {
                "label": "Decision",
                "title": "World models must expose why an action changes",
                "body": (
                    "Surgical WAM, FACT, VIScore, and 4D-WAM all ask whether latent prediction helps only when it "
                    "is tied to planning success, task progress, or 4D consistency rather than plausible video."
                ),
            },
            {
                "label": "Decision",
                "title": "Robotics evidence now needs a reject option",
                "body": (
                    "Estimator spectral analysis, protection levels, Dual Stress, and PBD-AG all treat robot memory "
                    "or safety as a decision about when evidence is unreliable enough to stop or inspect."
                ),
            },
            {
                "label": "Decision",
                "title": "VLA deployment is becoming an adversarial systems problem",
                "body": (
                    "DURA attacks, Gated VLA-Cache, Lost in Reconstruction, UniProbe, and SafeCap show that action "
                    "tokens, cache reuse, semantic action latents, and safety captions can all become failure interfaces."
                ),
            },
        ],
        "papers": [
            {
                "rank": 1,
                "title": "Embodied Multimodal Grounding for Open-Vocabulary Mobile Manipulation via Semantic 3D Gaussian Splatting",
                "arxiv_id": "2608.10756",
                "fit": "Semantic 3DGS - open-vocabulary grounding - mobile manipulation",
                "status": "Tier A - abstract-only",
                "status_quo": "Open-vocabulary manipulation is often split across language localization, mapping, base placement, and action generation modules.",
                "friction": "A mobile manipulator can ground the right object but still fail if the 3D scene, reachability, and action prior do not agree before execution.",
                "hidden_premise": "Semantic 3DGS can act as a shared interface only if active sensing, obstacle reasoning, base positioning, and action conditioning consume compatible scene evidence.",
                "conceptual_move": "Use a task-driven local Semantic-3DGS as the common grounding substrate, then inject 3D semantic cues into late action-expert blocks to preserve pretrained action priors.",
                "mechanism": "The abstract links active multi-view Semantic-3DGS, reachability-aware base positioning, and a diffusion-based VLA policy.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper states that language, visual observations, 3D scene structure, and action feasibility must be aligned before execution."},
                    {"trace": "[Abstract]", "claim": "It uses task-driven local Semantic-3DGS across active sensing, 3D localization, obstacle reasoning, base preparation, and action conditioning."},
                    {"trace": "[Inference]", "claim": "APRL should test whether a semantic 3D map changes base pose, target choice, or final action under distractor and reachability stress."},
                ],
                "falsification": "If the 3D semantic map improves language grounding but not action success under reachability conflicts, it is a perception aid rather than an execution interface.",
                "adversarial": "Few-shot household trials may hide failures under clutter, transparent objects, or base-placement limits; the map-action path needs counterfactual distractors.",
                "thinking_tool": "Treat semantic maps as action contracts: every map update should be tied to a reachable manipulation decision.",
                "transfer_boundary": "Strong for mobile manipulation with active sensing; weaker for fixed-arm tasks where workspace geometry is already known.",
            },
            {
                "rank": 2,
                "title": "Surgical WAM: A World-Action Model for Data-Efficient Surgical Robot Learning",
                "arxiv_id": "2608.11204",
                "fit": "surgical world-action model - action-scarce learning - closed-loop control",
                "status": "Tier A - abstract-only",
                "status_quo": "Surgical robot learning is bottlenecked by expensive video-kinematics demonstrations, while endoscopic video is comparatively abundant.",
                "friction": "Surgical world models are often used for simulation or evaluation without proving that video dynamics improve closed-loop manipulation.",
                "hidden_premise": "Action-free endoscopic video can pretrain a dynamics representation that remains useful when only a small action-labeled set is available.",
                "conceptual_move": "Ask whether a world-action model can convert abundant action-free video into data-efficient surgical control under a fixed demonstration budget.",
                "mechanism": "The abstract frames Surgical WAM around world modeling of surgical scenes and closed-loop manipulation policies.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper identifies synchronized surgical video-kinematics trajectories as costly and scarce."},
                    {"trace": "[Abstract]", "claim": "It asks whether action-free video pretraining improves closed-loop surgical manipulation under a fixed action-labeled budget."},
                    {"trace": "[Inference]", "claim": "APRL should evaluate whether action-free robot video helps contact timing, bimanual coordination, and recovery, not only future-frame quality."},
                ],
                "falsification": "If video pretraining improves visual prediction but not contact-rich closed-loop success, the world model learned surgical appearance rather than control state.",
                "adversarial": "Surgical video distribution may be narrow; cross-instrument, tissue, and camera-motion splits are needed before claiming data efficiency.",
                "thinking_tool": "Measure world-model usefulness by the labeled-action budget it saves at the same failure profile.",
                "transfer_boundary": "Direct for surgical and contact-rich manipulation; weaker for tasks where abundant video lacks controllable state change.",
            },
            {
                "rank": 3,
                "title": "FACT: Failure-Aware Causal Training for World-Action Models",
                "arxiv_id": "2608.10232",
                "fit": "failure-aware WAM - causal action conditioning - task progress",
                "status": "Tier A - abstract-only",
                "status_quo": "Many world-action models learn mostly from successful demonstrations and treat bad actions as data to discard.",
                "friction": "A controller cannot know which action to avoid if the world model never learns the future consequence of failure actions.",
                "hidden_premise": "Failed rollouts can supervise causal action consequences if the model predicts future video and task progress conditioned on executed action.",
                "conceptual_move": "Turn bad actions into valid future targets so failure evidence shapes both future prediction and action generation.",
                "mechanism": "The abstract describes a causal WAM that conditions future video and task-progress prediction on executed actions.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper states that WAMs trained on successful demonstrations have little reason to predict bad-action consequences."},
                    {"trace": "[Abstract]", "claim": "It uses failure rollouts to supervise action-conditioned future prediction and progress estimation."},
                    {"trace": "[Inference]", "claim": "APRL should label failures as causal interventions, not merely negative episodes."},
                ],
                "falsification": "If failure-aware progress prediction does not change action selection under near-miss states, it is a diagnostic auxiliary loss rather than a control mechanism.",
                "adversarial": "The approach may overfit known failure modes; test unseen failure families and ambiguous recovery states.",
                "thinking_tool": "Use failed actions as controlled counterfactuals for what the robot should not do next.",
                "transfer_boundary": "Strong for datasets with recoverable failure rollouts; weaker when failure labels are sparse or unsafe to collect.",
            },
            {
                "rank": 4,
                "title": "Hidden in Plain Sight: Diffusion-Based Unrestricted Robotic Attacks on Vision-Language-Action Models",
                "arxiv_id": "2608.10393",
                "fit": "VLA adversarial robustness - natural patch attack - action steering",
                "status": "Tier A - abstract-only",
                "status_quo": "VLA robustness work often inherits pixel-perturbation threat models that are visible or require white-box access.",
                "friction": "Physical robots can be steered by natural-looking objects or patches that fit the scene and avoid easy detection.",
                "hidden_premise": "A diffusion prior can search visually plausible patches while using only action outputs in the black-box setting.",
                "conceptual_move": "Move VLA attack evaluation from imperceptible image noise to deployable unrestricted visual interventions.",
                "mechanism": "The abstract says DURA optimizes along a pretrained diffusion latent trajectory to generate natural patches that steer robot actions.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper targets visually natural adversarial patches for VLA models."},
                    {"trace": "[Abstract]", "claim": "It supports black-box attack settings that require only predicted actions from the victim model."},
                    {"trace": "[Inference]", "claim": "APRL should test VLA policies with scene-plausible distractors and monitor action-token drift before contact."},
                ],
                "falsification": "If attacks fail under viewpoint changes, lighting changes, or object interaction, the threat is less physical than the abstract suggests.",
                "adversarial": "Defense evaluation needs human-plausible placement constraints and closed-loop recovery, not only target-action success.",
                "thinking_tool": "Robotic adversarial examples should be evaluated as objects in the task scene, not just pixels in the camera frame.",
                "transfer_boundary": "Direct for camera-based VLA manipulation; less direct for state-estimator-heavy controllers with explicit geometry checks.",
            },
            {
                "rank": 5,
                "title": "Neural Introspection Gating for Adaptive KV-Cache Reuse in Vision-Language-Action Models",
                "arxiv_id": "2608.10824",
                "fit": "VLA runtime cache - uncertainty gating - real-time control",
                "status": "Tier A - abstract-only",
                "status_quo": "VLA cache reuse can reduce compute by reusing visually static tokens, but observation similarity alone does not know when the action is uncertain.",
                "friction": "A reused cache can be safe for redundant frames yet harmful near decision boundaries where a small visual change alters the action token.",
                "hidden_premise": "The logit margin between top action tokens is a useful zero-cost introspection signal for cache invalidation.",
                "conceptual_move": "Let the model's own action uncertainty decide when to recompute visual KV states instead of relying only on image-space heuristics.",
                "mechanism": "The abstract describes Gated VLA-Cache, which invalidates cache when the action-token margin falls below a threshold.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper identifies repeated visual-token KV computation as a real-time control cost."},
                    {"trace": "[Abstract]", "claim": "It monitors the top-two action-token logit margin and triggers full recompute when confidence drops."},
                    {"trace": "[Inference]", "claim": "APRL should compare cache savings against the first action decision that changes under occlusion, contact, or motion blur."},
                ],
                "falsification": "If logit margins are poorly calibrated under distribution shift, cache invalidation may occur too late for safe control.",
                "adversarial": "A visually static but semantically changed scene can preserve cache similarity; evaluate with object swaps and delayed contact cues.",
                "thinking_tool": "Every deployment optimization needs a model-internal stop condition tied to action risk.",
                "transfer_boundary": "Strong for autoregressive VLA policies; weaker for controllers that do not expose action-token margins.",
            },
            {
                "rank": 6,
                "title": "VIScore: Diagnosing Planning-Relevant Quality in Latent World Models",
                "arxiv_id": "2608.11174",
                "fit": "latent world model quality - planning relevance - OOD success",
                "status": "Tier A - abstract-only",
                "status_quo": "Latent world-model regularization often optimizes representation geometry without directly testing planning success.",
                "friction": "A latent space can look stable or information-rich while failing to support OOD planning.",
                "hidden_premise": "Planning-relevant latent quality can be diagnosed by metrics that correlate with success rather than generic SSL properties.",
                "conceptual_move": "Separate latent distribution targets that help self-supervised learning from properties that actually improve world-model planning.",
                "mechanism": "The abstract compares SIGReg and VISReg, then motivates VIScore to connect latent-space factors with planning success.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper states that latent-space property and successful planning remain disconnected."},
                    {"trace": "[Abstract]", "claim": "It finds one regularization style helps SSL while another improves planning success on OOD datasets."},
                    {"trace": "[Inference]", "claim": "APRL should score world-model latents by downstream plan recovery under OOD shifts."},
                ],
                "falsification": "If VIScore correlates only within the tested environment family, it may measure dataset fit rather than planning-relevant structure.",
                "adversarial": "A latent metric can become another proxy; closed-loop plan success and intervention tests should remain the authority.",
                "thinking_tool": "Reject representation metrics that cannot predict a planning decision.",
                "transfer_boundary": "Strong for latent world-model planning; less direct for purely discriminative perception models.",
            },
            {
                "rank": 7,
                "title": "When Your State Estimator Has Lost The Plot: Detecting Estimator Failures Via Spectral Analysis",
                "arxiv_id": "2608.10623",
                "fit": "state-estimator introspection - spectral health - aerial robot odometry",
                "status": "Tier A - abstract-only",
                "status_quo": "Estimator confidence is often represented by covariance or learned quality measures that can be overconfident under OOD noise.",
                "friction": "Robots need to know that visual-inertial, LiDAR-inertial, or radar-inertial odometry has degraded before unsafe control decisions accumulate.",
                "hidden_premise": "Recent velocity-estimate frequency content contains sensor-agnostic signatures of estimator failure.",
                "conceptual_move": "Diagnose estimator health from spectral power distribution rather than relying only on estimator-reported uncertainty.",
                "mechanism": "The abstract proposes frequency-domain analysis of recent velocity estimates and evaluates it on aerial robot data across multiple odometry modalities.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper names sensor aliasing and OOD noise as causes of estimator degradation or failure."},
                    {"trace": "[Abstract]", "claim": "It evaluates visual-inertial, LiDAR-inertial, and radar-inertial odometry failures using outdoor flight data."},
                    {"trace": "[Inference]", "claim": "APRL should record estimator-health spectra next to map-update and controller-handoff decisions."},
                ],
                "falsification": "If spectral signatures lag behind actual pose divergence, the method may confirm failure but not prevent it.",
                "adversarial": "Frequency cues may be platform- or controller-dependent; transfer should be tested across speed, terrain, and sensor suites.",
                "thinking_tool": "Treat state estimation as a monitored subsystem with its own failure-warning signal.",
                "transfer_boundary": "Strong for mobile robots with velocity streams; weaker for static perception or low-rate manipulation.",
            },
            {
                "rank": 8,
                "title": "Evidence-Grounded Trustworthy Multimodal Reasoning and Evaluation Benchmark in Complex Urban Scenes",
                "arxiv_id": "2608.10954",
                "fit": "urban scene reasoning - evidence chain benchmark - trustworthy MLLM",
                "status": "Tier A - abstract-only",
                "status_quo": "Many multimodal benchmarks score final answers without diagnosing whether the model acquired the right visual evidence.",
                "friction": "Complex adverse urban scenes encourage implicit inference, making a correct-looking answer unreliable for safety-critical autonomy.",
                "hidden_premise": "Trustworthy multimodal reasoning depends on an observable chain of evidence that can be decomposed and evaluated.",
                "conceptual_move": "Use hierarchical visual diagnosis and Chain of Evidence evaluation rather than outcome-only scoring.",
                "mechanism": "The abstract introduces AD2-Bench and decomposes reasoning through a structured Chain of Evidence.",
                "evidence": [
                    {"trace": "[Abstract]", "claim": "The paper says MLLM reliability deteriorates under complex scenes and adverse conditions."},
                    {"trace": "[Abstract]", "claim": "It criticizes outcome-oriented benchmarks for failing to diagnose reasoning-process failures."},
                    {"trace": "[Inference]", "claim": "APRL should require evidence-chain traces before trusting language explanations in driving or navigation."},
                ],
                "falsification": "If Chain of Evidence quality does not predict intervention success or failure recovery, it may improve explanation quality without improving autonomy.",
                "adversarial": "Benchmarks must include occlusion, weather, and rare hazard splits so evidence grounding is not reduced to caption completeness.",
                "thinking_tool": "Grade the evidence path, not only the final multimodal answer.",
                "transfer_boundary": "Strong for driving and urban autonomy; less direct for low-level manipulation unless evidence chains are tied to action authority.",
            },
        ],
        "synthesis": [
            {
                "title": "World-action learning now has to consume failure evidence",
                "links": "Surgical WAM - FACT - VIScore - 4D-WAM",
                "facts": "The papers link video/world-model learning to fixed action-label budgets, failed rollouts, planning-relevant latent metrics, and 4D consistency.",
                "inference": "APRL should stop accepting future prediction as a proxy unless it predicts when an action should change or be rejected.",
            },
            {
                "title": "Runtime optimizations need explicit invalidation signals",
                "links": "Gated VLA-Cache - estimator spectral analysis - protection levels - Dual Stress",
                "facts": "Cache reuse, state estimation, pose integrity, and MPC monitoring all expose internal signals that can trigger recompute, reject, or warning decisions.",
                "inference": "A deployable robotics system needs stop conditions for every shortcut it takes to run faster or longer.",
            },
            {
                "title": "Evidence-grounded reasoning is crossing from VLMs into robot memory",
                "links": "AD2-Bench - TAR-Bench - AECNav - PBD-AG - Semantic 3DGS grounding",
                "facts": "Urban reasoning, traffic anomaly, object navigation, service-robot graphs, and 3D semantic grounding all separate evidence acquisition from final decision.",
                "inference": "The stronger benchmark is one where removing or corrupting evidence changes the robot decision in a measurable way.",
            },
        ],
        "frontier_memory": [
            {"label": "Strengthening", "history": "August 11 emphasized evidence-controlled action interfaces.", "body": "August 12 strengthens the same axis with explicit failure-aware WAMs, cache invalidation, estimator health, and evidence-chain benchmarks."},
            {"label": "New signal", "history": "Recent editions discussed geometry as map and localization substrate.", "body": "Today adds semantic 3DGS as a shared execution interface for open-vocabulary mobile manipulation rather than a rendering artifact."},
            {"label": "Missing axis", "history": "Prior VLA notes focused on action routing and adaptation.", "body": "The current batch still leaves multi-robot manipulation and real contact-rich failure collection under-specified; APRL can own that data asset."},
        ],
        "strategy": [
            {
                "priority": "Build moat",
                "title": "Failure-conditioned world-action benchmark",
                "thesis": "Build a robot replay suite where successful and failed actions supervise future prediction, progress estimation, and recovery decisions.",
                "scores": {"fit": 5, "novelty": 5, "feasibility": 4, "moat": 5, "timing": 5, "evidence": 5},
                "one_week": "Convert one manipulation or surgical-style dataset into success/failure action clips with progress labels and near-miss tags.",
                "four_week": "Compare vanilla WAM, FACT-style failure conditioning, and video-only pretraining under the same action-label budget.",
                "success": "Failure-conditioned prediction changes the selected action before task-level failure in at least two failure families.",
                "stop": "Failure labels improve offline prediction but do not alter recovery or success ranking.",
                "asset": "Failure rollouts, progress labels, counterfactual action clips, and recovery-decision tables.",
            },
            {
                "priority": "Explore",
                "title": "Introspective deployment shortcut controller",
                "thesis": "Unify cache invalidation, estimator-health warning, protection-level bound, and MPC dual stress as stop conditions for fast robot deployment.",
                "scores": {"fit": 5, "novelty": 4, "feasibility": 4, "moat": 4, "timing": 5, "evidence": 4},
                "one_week": "Instrument one navigation or VLA replay with action-token margin, estimator spectral score, pose bound, and safety multiplier traces.",
                "four_week": "Run stress tests where each shortcut is allowed or rejected, then measure latency, warning lead time, and downstream action error.",
                "success": "At least one introspection signal prevents a harmful shortcut before a standard metric flags failure.",
                "stop": "Signals are redundant with confidence or arrive after the unsafe action has already been chosen.",
                "asset": "Synchronized introspection traces, rejection labels, latency-risk curves, and intervention policies.",
            },
            {
                "priority": "Build moat",
                "title": "Evidence-chain robot memory protocol",
                "thesis": "Make semantic 3D maps, object-navigation beliefs, and urban-scene reasoning prove which evidence supports each action or map update.",
                "scores": {"fit": 5, "novelty": 5, "feasibility": 3, "moat": 5, "timing": 4, "evidence": 5},
                "one_week": "Create paired scenes with target distractors, corrupted evidence regions, and reachability conflicts for map-to-action grounding.",
                "four_week": "Evaluate Semantic 3DGS grounding, AECNav-style evidence consolidation, and AD2/TAR-style reasoning traces by action change under evidence removal.",
                "success": "Evidence-chain quality predicts target choice, base placement, or hazard response better than final answer accuracy.",
                "stop": "Evidence traces improve explanation readability but do not predict control or navigation decisions.",
                "asset": "Evidence-corrupted scenes, 3D semantic maps, belief traces, target support labels, and action-change metrics.",
            },
        ],
    }
}


def main() -> int:
    (ROOT / "intelligence").mkdir(exist_ok=True)
    (ROOT / "posts").mkdir(exist_ok=True)
    for date, data in RI_BY_DATE.items():
        (ROOT / "intelligence" / f"{date}.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (ROOT / "posts" / f"{date}-research-intelligence.html").write_text(
            build_html(data),
            encoding="utf-8",
            newline="\n",
        )
        print(f"wrote intelligence/{date}.json and posts/{date}-research-intelligence.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
