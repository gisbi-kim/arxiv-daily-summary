#!/usr/bin/env python3
"""Generate the full-text Research Intelligence edition for 2026-07-17."""

from __future__ import annotations

import json
from pathlib import Path

import gen_research_intelligence_20260713 as template


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-07-17"
SLUG = f"{DATE}-research-intelligence"


DATA = {
    "date": DATE,
    "edition": "Research Intelligence",
    "source_prompt": "prompts/instruction_v20260713.md",
    "scope_note": (
        "당일 cs.CV/cs.RO /new 257건을 파싱했고 replacement를 제외한 dedup 165건 중 139건을 ROI로 분류했습니다. "
        "Tier A 6편은 공식 arXiv HTML 본문, 섹션, 그림, 표를 확인해 작성했습니다. Verified는 논문에서 직접 확인한 "
        "사실이고, Inference와 APRL hypothesis는 편집자의 연구 판단으로 분리했습니다."
    ),
    "executive_thesis": (
        "오늘의 강한 신호는 로봇 foundation model을 더 크게 만드는 쪽이 아니라, 행동을 내보내기 직전에 어떤 "
        "표현과 상태가 실제 제어 실패를 만든다는 점을 계측하는 쪽입니다. Action QFormer는 action supervision이 "
        "상속된 multimodal representation을 어떻게 재배선하는지 묻고, LIFT와 RoboTTT는 force memory와 장기 "
        "visuomotor context가 action chunk 내부에서 언제 필요해지는지 보여줍니다. BadWAM은 world-action model의 "
        "상상 미래가 멀쩡해도 closed-loop action은 망가질 수 있음을 드러내고, G2SR과 VTM-Nav는 3D/scene memory가 "
        "visual fidelity보다 online geometry와 cross-episode retrieval 계약으로 이동하고 있음을 보여줍니다. "
        "APRL에는 하나의 평균 성공률보다 action-facing interface, contact state, long-context memory, simulator/geometry "
        "validity를 같은 closed-loop harness에서 나누어 보는 자산이 더 방어적인 포지션입니다."
    ),
    "decision_cards": [
        {
            "title": "VLA action head가 아니라 action-facing interface를 진단한다",
            "body": (
                "Action QFormer와 RoboTTT는 action prediction 앞단의 query, context, fast weights가 실제 행동 안정성을 "
                "결정한다고 봅니다. APRL 실험은 backbone 크기보다 instruction-conditioned visual extraction, long-context "
                "retrieval, streaming latency가 실패를 어떻게 바꾸는지 분리해야 합니다."
            ),
            "label": "Decision",
        },
        {
            "title": "contact-rich manipulation은 vision-only chunk로 닫히지 않는다",
            "body": (
                "LIFT는 최근 force를 causal memory로 넣어 chunk 내부 행동을 수정하고, tactile/force proxy 논문들은 "
                "접촉 상태가 vision과 kinematics만으로는 약하게 관측된다고 봅니다. force/tactile state를 별도 ablation 축으로 "
                "두지 않으면 contact 실패의 원인을 policy capacity로 오해하기 쉽습니다."
            ),
            "label": "Decision",
        },
        {
            "title": "world-action model의 imagined future는 안전 신호가 아니다",
            "body": (
                "BadWAM은 predicted future가 깨끗해 보여도 action channel이 공격될 수 있음을 보입니다. world model이나 "
                "simulator를 안전 장치로 쓰려면 imagined future, action shift, closed-loop success를 서로 다른 failure family로 "
                "평가해야 합니다."
            ),
            "label": "Decision",
        },
    ],
    "papers": [
        {
            "rank": 1,
            "title": "Action QFormer: Structured Representation Shaping under Action Supervision in Vision-Language-Action Models",
            "arxiv_id": "2607.14635",
            "fit": "VLA action interface - representation shaping - closed-loop sim-to-real",
            "status": "Tier A - official arXiv HTML verified",
            "status_quo": (
                "VLA에서 action supervision은 downstream head를 학습시키는 목적 함수이고, 상속된 image/instruction "
                "representation은 대체로 그대로 action head에 넘겨도 된다고 보기 쉽습니다."
            ),
            "friction": (
                "논문은 direct-fusion baseline이 inherited multimodal representation을 바로 action-facing representation으로 "
                "섞는 구조라고 놓고, gradient blocking과 query interface를 통해 action loss가 upstream token을 어떻게 다시 쓰는지 "
                "분리해 봅니다."
            ),
            "hidden_premise": (
                "action generation의 병목은 action head 용량만이 아니라, instruction이 어떤 visual evidence를 뽑아 action-facing "
                "state로 넘기는 interface 설계입니다."
            ),
            "conceptual_move": (
                "Action QFormer는 learnable query를 instruction representation에 조건화하고, query output을 통해 action-relevant "
                "visual information만 선택적으로 추출해 downstream action generation을 조건화합니다."
            ),
            "mechanism": (
                "Figure 1은 direct-fusion baseline과 stop-gradient diagnostic을 제시하고, Figure 2는 instruction-conditioned query가 "
                "visual information을 선택적으로 추출하는 Action QFormer interface를 설명합니다."
            ),
            "evidence": [
                {
                    "trace": "Figure 1 [Verified]",
                    "claim": "image-side와 instruction-side representation을 바로 융합하는 baseline과 gradient-routing diagnostic을 제시합니다.",
                },
                {
                    "trace": "Figure 2 [Verified]",
                    "claim": "learnable queries가 instruction representation에 조건화되어 action-relevant visual information을 추출하는 구조를 보여줍니다.",
                },
                {
                    "trace": "Section IV [Verified]",
                    "claim": "zero-shot sim-to-real closed-loop experiment와 fixed-instruction action generation을 별도 실험 축으로 둡니다.",
                },
                {
                    "trace": "Section V [Verified]",
                    "claim": "action-facing directional distinction, upstream token rewriting, attention stability를 mechanistic analysis로 다룹니다.",
                },
            ],
            "falsification": (
                "동일한 visual/action evidence에서 단순 larger adapter나 direct-fusion plus regularization이 같은 closed-loop 안정성과 "
                "attention stability를 만들면 query interface 자체의 설명력은 약해집니다."
            ),
            "adversarial": (
                "mechanistic 분석은 설득력이 있지만, 실제 robot contact, occlusion, streaming inference 조건에서는 attention stability가 "
                "execution stability로 바로 이어진다고 단정하기 어렵습니다."
            ),
            "thinking_tool": (
                "VLA 개선을 action head 교체로 보지 말고, instruction이 어떤 visual token을 action-facing state로 통과시키는지 보는 "
                "interface 진단으로 바꿉니다."
            ),
            "transfer_boundary": (
                "language-conditioned visual selection이 중요한 task에는 강하지만, force-dominant contact recovery나 fast reflex control에서는 "
                "visual query보다 proprioceptive/tactile state가 먼저 필요할 수 있습니다."
            ),
        },
        {
            "rank": 2,
            "title": "Never Too Late for Force: Accelerating VLA Post-Training with Reactive Force Injection",
            "arxiv_id": "2607.14236",
            "fit": "VLA post-training - force memory - contact-rich manipulation",
            "status": "Tier A - official arXiv HTML verified",
            "status_quo": (
                "pretrained VLA는 vision과 language로 충분한 manipulation prior를 갖고 있고, post-training은 주로 더 많은 "
                "visual demonstration으로 성능을 올리는 과정이라고 보기 쉽습니다."
            ),
            "friction": (
                "논문은 접촉 상태에서 occlusion, depth ambiguity, 작은 force error가 offline demonstration distribution 밖으로 "
                "실행을 밀어낸다고 봅니다."
            ),
            "hidden_premise": (
                "contact-rich manipulation에서는 action chunk를 한 번 생성하고 끝내는 것이 아니라, 최근 force history로 chunk 내부 "
                "행동을 계속 수정할 수 있어야 합니다."
            ),
            "conceptual_move": (
                "LIFT는 pretrained VLA의 vision-language stack을 유지하면서 reactive action expert를 추가하고, causal force memory를 "
                "cross attention으로 주입합니다."
            ),
            "mechanism": (
                "Figure 1과 Figure 2는 force encoder, reactive branch, zero-initialized cross attention, copied action expert를 통해 "
                "기존 prior를 보존하면서 force-conditioned action update를 가능하게 하는 구조를 보여줍니다."
            ),
            "evidence": [
                {
                    "trace": "Figure 1 [Verified]",
                    "claim": "recent force를 causal force memory로 encoding하고 within-chunk action update에 쓰는 LIFT overview를 제시합니다.",
                },
                {
                    "trace": "Figure 2 [Verified]",
                    "claim": "pretrained vision-language stack을 유지한 채 reactive action expert와 force-injected cross attention을 graft합니다.",
                },
                {
                    "trace": "Table 1 [Verified]",
                    "claim": "PaliGemma 기반 pi0.5 backbone, force input dimension, causal GRU force encoder, zero-initialized attention 등 architecture hyperparameter를 명시합니다.",
                },
                {
                    "trace": "Section 4 [Verified]",
                    "claim": "towel folding, book insertion, Hanoi ring placement에서 force, reactivity, original VLA generalization, online data 효과를 질문별로 평가합니다.",
                },
            ],
            "falsification": (
                "동일 online correction data에서 visual-only DAgger가 contact tasks를 같은 속도로 따라잡거나, single-frame force가 causal "
                "memory와 같은 성능을 내면 reactive force memory 가설은 약해집니다."
            ),
            "adversarial": (
                "force sensor와 latency alignment가 잘 갖춰진 setting에 의존합니다. 더 거친 gripper, tactile-only 손, mobile manipulation에서는 "
                "force channel의 신뢰도와 timing이 다를 수 있습니다."
            ),
            "thinking_tool": (
                "VLA post-training을 demonstration 추가가 아니라, hidden contact state를 어느 시점에 action chunk로 다시 주입할지 정하는 "
                "reactive interface 설계로 봅니다."
            ),
            "transfer_boundary": (
                "접촉이 병목인 insertion/folding에는 직접적이지만, target search나 open-space navigation처럼 visual state가 대부분인 task에는 "
                "force injection이 주된 bottleneck이 아닐 수 있습니다."
            ),
        },
        {
            "rank": 3,
            "title": "RoboTTT: Context Scaling for Robot Policies",
            "arxiv_id": "2607.15275",
            "fit": "long-context robot policy - test-time training - one-shot imitation",
            "status": "Tier A - official arXiv HTML verified",
            "status_quo": (
                "robot foundation model은 현재 observation이나 짧은 history만 보아도 충분하고, 긴 context는 inference latency와 "
                "state aliasing 때문에 제한적이라고 보기 쉽습니다."
            ),
            "friction": (
                "논문은 multi-stage assembly와 long-horizon task에서 visually similar stage가 state aliasing을 만들고, short-history policy가 "
                "wrong component selection이나 skipped stage로 실패한다고 봅니다."
            ),
            "hidden_premise": (
                "long-horizon robot skill의 핵심은 단순 recurrent memory가 아니라, history를 빠른 model update로 질의해 현재 action에 "
                "반영하는 방법입니다."
            ),
            "conceptual_move": (
                "RoboTTT는 DiT action head에 TTT layer를 추가해 timestep 내부 attention과 timestep 간 fast-weight update를 분리하고, "
                "8K timestep context를 latency 증가 없이 다루려 합니다."
            ),
            "mechanism": (
                "Figure 1은 8K timestep context와 one-shot in-context imitation을, Figure 2는 TTT layer, sequence flow-matching loss, "
                "fast weight inference를 보여줍니다."
            ),
            "evidence": [
                {
                    "trace": "Figure 1 [Verified]",
                    "claim": "RoboTTT가 8K timestep context를 다루며 human video demonstration 기반 one-shot imitation과 on-the-fly improvement를 목표로 함을 제시합니다.",
                },
                {
                    "trace": "Figure 2 [Verified]",
                    "claim": "attention은 timestep 내부를, TTT layer는 timestep across-context를 처리하는 architecture와 inference flow를 보여줍니다.",
                },
                {
                    "trace": "Table 1 [Verified]",
                    "claim": "dexterous long-horizon tasks에서 RoboTTT의 평균 task completion score와 fully successful trial 수를 baseline과 비교합니다.",
                },
                {
                    "trace": "Table 2 [Verified]",
                    "claim": "unseen configuration의 Circuit task에서 human video in-context demonstration을 조건으로 one-shot imitation을 평가합니다.",
                },
            ],
            "falsification": (
                "task progress cue를 명시 state token으로 제공한 짧은-context baseline이 같은 performance를 내면, 8K context보다 state abstraction이 "
                "핵심일 수 있습니다."
            ),
            "adversarial": (
                "long-context가 늘수록 spurious history retrieval과 demonstration leakage 위험도 커집니다. human video domain shift나 wrong history가 "
                "들어왔을 때 실패 양상을 따로 봐야 합니다."
            ),
            "thinking_tool": (
                "robot memory를 hidden recurrent state가 아니라, rollout 중 빠르게 갱신되는 test-time model로 봅니다."
            ),
            "transfer_boundary": (
                "반복 조립과 long-horizon manipulation에는 강하지만, safety-critical reflex나 high-rate locomotion처럼 millisecond feedback이 "
                "필요한 task에서는 TTT update가 느릴 수 있습니다."
            ),
        },
        {
            "rank": 4,
            "title": "BadWAM: When World-Action Models Dream Right but Act Wrong",
            "arxiv_id": "2607.15207",
            "fit": "world-action model safety - adversarial closed-loop control - imagination preservation",
            "status": "Tier A - official arXiv HTML verified",
            "status_quo": (
                "world-action model은 미래를 함께 예측하므로 action을 감시할 수 있고, imagined future가 안정적이면 행동도 안전하다고 "
                "보기 쉽습니다."
            ),
            "friction": (
                "논문은 failed episodes가 큰 action shift를 보이지만 predicted-future shift는 성공/실패 사이에서 겹칠 수 있음을 Figure 1로 "
                "동기화합니다."
            ),
            "hidden_premise": (
                "world model의 future prediction과 action channel은 같은 safety signal이 아닙니다. 둘 사이의 alignment가 공격 대상이 될 수 있습니다."
            ),
            "conceptual_move": (
                "BadWAM은 frozen WAM에 query-based online search로 작은 visual perturbation을 넣고, action prediction pathway를 망가뜨리면서 "
                "future prediction drift는 작게 유지하는 attack을 구성합니다."
            ),
            "mechanism": (
                "Figure 2는 action-only attack이 특정 action horizon/channel을 구조적으로 흔든다는 점을, Figure 3은 action disruption과 "
                "imagination preservation을 함께 최적화하는 pipeline을 보여줍니다."
            ),
            "evidence": [
                {
                    "trace": "Figure 1 [Verified]",
                    "claim": "action shift와 predicted-future shift가 실패를 다르게 설명할 수 있음을 보여 attack target을 world-action alignment로 설정합니다.",
                },
                {
                    "trace": "Figure 2 [Verified]",
                    "claim": "action-only attack이 uniform noise가 아니라 action channel과 horizon 일부를 구조적으로 바꾼다고 보고합니다.",
                },
                {
                    "trace": "Table 1 [Verified]",
                    "claim": "LIBERO와 RobotWin에서 action-only 및 imagination-preserving attacks가 closed-loop task success를 크게 낮춘다고 보고합니다.",
                },
                {
                    "trace": "Table 2 [Verified]",
                    "claim": "한 WAM variant에서 최적화한 perturbation이 다른 WAM variant로 transfer될 수 있음을 평가합니다.",
                },
            ],
            "falsification": (
                "adaptive detector가 action shift와 future drift를 함께 보았을 때 공격을 안정적으로 잡거나, physical perturbation에서 효과가 "
                "사라지면 실전 위험은 줄어듭니다."
            ),
            "adversarial": (
                "black-box visual perturbation setting이 실제 센서 노이즈와 얼마나 맞는지, 그리고 closed-loop recovery controller가 있는 시스템에서도 "
                "같은 취약성이 유지되는지 별도 검증이 필요합니다."
            ),
            "thinking_tool": (
                "world model safety를 imagined future quality로 보지 말고, future/action channel의 alignment failure family로 나눕니다."
            ),
            "transfer_boundary": (
                "WAM 기반 embodied control에는 직접적이지만, explicit model predictive controller나 verified safety layer가 강하게 개입하는 시스템에는 "
                "그대로 적용하기 어렵습니다."
            ),
        },
        {
            "rank": 5,
            "title": "G2SR: Geometric Methods for Fast and Memory-Efficient Gaussian-based Surface Reconstruction",
            "arxiv_id": "2607.14470",
            "fit": "Gaussian surface reconstruction - multi-view geometry - online robot maps",
            "status": "Tier A - official arXiv HTML verified",
            "status_quo": (
                "3D Gaussian surface reconstruction은 end-to-end network가 few-view ambiguity를 통째로 해결하고, rendering fidelity를 "
                "높이는 방향으로 발전한다고 보기 쉽습니다."
            ),
            "friction": (
                "논문은 monolithic end-to-end GS가 compute와 memory를 많이 쓰고 across-scene generalization이 약하다고 놓습니다. 모바일 로봇에는 "
                "빠르고 작고 기하적으로 정확한 재구성이 필요합니다."
            ),
            "hidden_premise": (
                "few-view surface reconstruction의 ill-posed 부분과 well-posed geometry 부분을 나누면, robot online map에 더 맞는 계산 계약을 "
                "만들 수 있습니다."
            ),
            "conceptual_move": (
                "G2SR은 neural frontend가 2D Gaussian splat detection과 cross-view tracking만 맡고, analytic backend가 multi-view geometry로 "
                "3D splat triangulation을 풉니다."
            ),
            "mechanism": (
                "Figure 1은 monolithic GS와 geometry-decoupled G2SR의 차이를, Figure 2는 lightweight network, optical-flow sigma-point "
                "warping, Gauss-Newton triangulation pipeline을 보여줍니다."
            ),
            "evidence": [
                {
                    "trace": "Figure 1 [Verified]",
                    "claim": "2-3 posed RGB images에서 prior end-to-end methods와 달리 2D neural frontend와 analytic 3D backend를 분리하는 framing을 제시합니다.",
                },
                {
                    "trace": "Figure 2 [Verified]",
                    "claim": "2D Gaussian splat detection, affine correspondence tracking, squared Hellinger distance 기반 triangulation pipeline을 설명합니다.",
                },
                {
                    "trace": "Section IV-B [Verified]",
                    "claim": "memory와 throughput을 별도 실험 축으로 두어 online reconstruction 요구를 평가합니다.",
                },
                {
                    "trace": "Section IV-C [Verified]",
                    "claim": "depth estimation, mesh reconstruction, camera geometry robustness를 geometric accuracy 실험으로 분리합니다.",
                },
            ],
            "falsification": (
                "더 작은 end-to-end model이 같은 memory/throughput budget에서 camera geometry 변화에 더 강하면, analytic decomposition의 이점은 "
                "약해집니다."
            ),
            "adversarial": (
                "few posed RGB setting에 강하지만 dynamic objects, rolling shutter, uncalibrated mobile capture에서는 correspondence와 triangulation "
                "오차가 robot map failure로 번질 수 있습니다."
            ),
            "thinking_tool": (
                "3DGS를 visual asset이 아니라, online robot map이 감당할 memory, latency, geometry robustness 계약으로 읽습니다."
            ),
            "transfer_boundary": (
                "few-view static surface reconstruction에는 직접적이지만, semantic map update나 dynamic scene reasoning은 별도 layer가 필요합니다."
            ),
        },
        {
            "rank": 6,
            "title": "VTM-Nav: Hierarchical Visual-Topological Memory for Cross-Episode Object-Goal Navigation",
            "arxiv_id": "2607.14514",
            "fit": "ObjectNav - cross-episode memory - visual-topological retrieval",
            "status": "Tier A - official arXiv HTML verified",
            "status_quo": (
                "Object-goal navigation benchmark는 episode가 끝나면 scene-specific state를 reset하고, 한 episode 안에서의 exploration과 "
                "reasoning만 평가해도 충분하다고 보는 관습이 있습니다."
            ),
            "friction": (
                "논문은 실제 반복 방문 환경에서는 이전 episode의 room connectivity, object viewpoints, target routes가 남아 있어야 하는데, 표준 "
                "protocol은 agent가 매번 처음 보는 scene처럼 행동하게 만든다고 봅니다."
            ),
            "hidden_premise": (
                "embodied memory의 핵심은 모든 observation을 쌓는 것이 아니라, room-level topology와 room-conditioned object evidence를 "
                "cross-episode로 유지하고 target에 맞게 회수하는 것입니다."
            ),
            "conceptual_move": (
                "VTM-Nav는 scene-scoped hierarchical Visual-Topological Memory를 만들고, semantic/topological/spatial consistency로 localization한 "
                "observation을 memory update와 action selection에 연결합니다."
            ),
            "mechanism": (
                "Figure 1은 episode-isolated protocol과 cross-episode ObjectNav의 차이를, Figure 2는 visual-topological memory update와 "
                "target-conditioned retrieval pipeline을 보여줍니다."
            ),
            "evidence": [
                {
                    "trace": "Figure 1 [Verified]",
                    "claim": "standard protocol이 scene knowledge를 버리는 반면 VTM-Nav는 room topology와 object experience를 scene-scoped memory로 축적한다고 제시합니다.",
                },
                {
                    "trace": "Figure 2 [Verified]",
                    "claim": "RGB-D observation, target category, pose, previous action을 structured semantic evidence와 hierarchical memory update로 연결합니다.",
                },
                {
                    "trace": "Section 4.4 [Verified]",
                    "claim": "Ablation Study를 별도 섹션으로 두어 memory components의 기여를 평가합니다.",
                },
                {
                    "trace": "Section 4.5 [Verified]",
                    "claim": "Cross-Episode Progression Analysis를 통해 반복 방문에서 성능 변화가 어떻게 생기는지 봅니다.",
                },
            ],
            "falsification": (
                "strong VLM exploration policy가 memory 없이도 같은 scene 재방문에서 비슷한 path efficiency와 success를 만들면, scene-scoped "
                "memory의 독립 기여는 줄어듭니다."
            ),
            "adversarial": (
                "반복 방문 환경에서는 stale memory가 위험할 수 있습니다. 동적 object relocation이나 closed doors가 많으면 old evidence가 오히려 "
                "navigation failure를 만들 수 있습니다."
            ),
            "thinking_tool": (
                "navigation memory를 episode transcript가 아니라, target-conditioned retrieval이 가능한 room topology asset으로 봅니다."
            ),
            "transfer_boundary": (
                "반복 방문 indoor ObjectNav에는 강하지만, one-shot disaster response나 rapidly changing outdoor scene에는 stale evidence handling이 "
                "먼저 필요합니다."
            ),
        },
    ],
    "synthesis": [
        {
            "title": "Representation decision: action supervision이 어디까지 upstream을 다시 쓰는지 본다",
            "links": "Action QFormer - FoMoVLA - Reflex - DiMaS",
            "facts": (
                "Action QFormer는 action-facing interface를 query-based로 분리하고, Reflex와 DiMaS는 streaming control과 representation steering을 "
                "VLA 제어 문제로 다룹니다."
            ),
            "inference": (
                "APRL VLA run에는 action head score뿐 아니라 visual token selection, instruction-action consistency, control latency를 같은 "
                "failure family로 둬야 합니다."
            ),
            "decision": "VLA 실험마다 action-facing interface stress split을 포함합니다.",
        },
        {
            "title": "State decision: contact와 long context는 policy 내부 상태로 승격된다",
            "links": "LIFT - tactile grounding - RoboTTT - VTM-Nav",
            "facts": (
                "LIFT는 force memory를 chunk 내부 update로 넣고, RoboTTT는 8K timestep context를 fast weights로 다루며, VTM-Nav는 scene memory를 "
                "episode 밖으로 확장합니다."
            ),
            "inference": (
                "robot memory는 하나가 아니라 contact-state memory, visuomotor context, scene-topological memory로 나누어 평가해야 합니다."
            ),
            "decision": "memory length가 아니라 어떤 state가 어떤 실패를 줄이는지 factorial ablation으로 봅니다.",
        },
        {
            "title": "Safety decision: imagined future와 executable action을 분리한다",
            "links": "BadWAM - WAM steering - SafeRelBench - WorkDrive",
            "facts": (
                "BadWAM은 future prediction이 안정적이어도 action channel이 공격될 수 있음을 보이고, SafeRelBench와 WorkDrive는 embodied/spatial "
                "reasoning의 process-level failure를 benchmark로 묻습니다."
            ),
            "inference": (
                "world model 기반 안전성은 generated future 품질이 아니라 action shift, relation violation, closed-loop recovery를 함께 봐야 합니다."
            ),
            "decision": "world-action model 평가에 imagination/action divergence metric을 넣습니다.",
        },
    ],
    "frontier_memory": [
        {
            "signal": "강화 중",
            "title": "VLA runtime/fine-tuning 축이 action-facing representation 진단으로 세분화",
            "history": "지난 4주 동안 VLA runtime, semantic retention, simulator validity가 반복되었습니다.",
            "read": "오늘은 Action QFormer, LIFT, RoboTTT가 각각 query interface, force memory, long-context update라는 구체적 제어 지점을 제시합니다.",
        },
        {
            "signal": "강화 중",
            "title": "3D/SLAM 신호가 Gaussian visual fidelity에서 online geometry contract로 이동",
            "history": "최근 3DGS와 reconstruction 논문은 계속 많았지만 rendering 품질 중심으로 보이는 경우가 많았습니다.",
            "read": "G2SR, Instant NuRec, MAGiSt3R, image-to-point cloud registration은 memory/throughput/pose robustness를 robot/driving map 조건으로 끌어옵니다.",
        },
        {
            "signal": "새로운 통합",
            "title": "world-action safety와 VLA perturbation이 같은 closed-loop failure family로 합쳐짐",
            "history": "이전 batch는 benchmark 검증과 model robustness를 따로 다뤘습니다.",
            "read": "BadWAM과 illumination attack, SafeRelBench, WorkDrive는 perception score보다 executable behavior가 언제 틀어지는지를 묻습니다.",
        },
        {
            "signal": "비어 있음",
            "title": "contact, long-context, scene memory를 한 robot task 안에서 함께 나눈 표준은 아직 부족",
            "history": "각 축은 강하지만 통합 evaluation harness는 드뭅니다.",
            "read": "APRL은 force/tactile state, long context, cross-episode memory, 3D map validity를 같은 manipulation-navigation suite로 묶을 수 있습니다.",
        },
    ],
    "strategy": [
        {
            "priority": "BUILD",
            "title": "Action-Facing Interface Stress Bench",
            "thesis": (
                "VLA를 backbone별로 비교하기 전에, instruction-conditioned visual extraction, representation steering, streaming inference가 "
                "실제 closed-loop failure를 어떻게 바꾸는지 계측합니다."
            ),
            "scores": {"fit": 5, "novelty": 4, "feasibility": 5, "moat": 5, "timing": 5, "evidence": 5},
            "one_week": (
                "LIBERO/RoboCasa subset에서 direct-fusion, query interface, steering, streaming inference variant를 같은 OOD object와 "
                "latency perturbation 조건에 둡니다."
            ),
            "four_week": (
                "OpenVLA/pi0 계열 wrapper에 visual-token selection, instruction-action contradiction, control latency, recovery success를 "
                "함께 내는 dashboard를 붙입니다."
            ),
            "metric": "OOD success +10p, latency-induced failure -20%, instruction-action contradiction -40%, ID success drop <3p.",
            "stop": "interface metric이 closed-loop failure와 2개 task family 이상에서 연결되지 않으면 representation probe로 범위를 축소합니다.",
            "assets": [
                {"label": "Action QFormer", "url": "https://arxiv.org/abs/2607.14635"},
                {"label": "FoMoVLA", "url": "https://arxiv.org/abs/2607.14739"},
                {"label": "Reflex", "url": "https://arxiv.org/abs/2607.14695"},
            ],
        },
        {
            "priority": "EXPLOIT",
            "title": "Contact-State VLA Evaluation Harness",
            "thesis": (
                "contact-rich manipulation에서는 vision-only success보다 force/tactile/proprioceptive state가 action chunk를 언제 수정하는지가 "
                "핵심 연구 자산입니다."
            ),
            "scores": {"fit": 5, "novelty": 4, "feasibility": 4, "moat": 5, "timing": 5, "evidence": 5},
            "one_week": (
                "folding, insertion, in-hand tracking task에서 force memory length, tactile prediction target, haptic fusion encoder를 "
                "독립 변수로 둡니다."
            ),
            "four_week": (
                "vision-only, force-injected, tactile-grounded, haptic-fusion policies를 같은 contact perturbation suite에서 비교하고 "
                "failure-warning lead time과 recovery behavior를 평가합니다."
            ),
            "metric": "contact failure -25%, recovery success +15p, force/tactile ablation effect size, unseen object success drop <5p.",
            "stop": "force/tactile state가 vision-only baseline 대비 contact failure를 줄이지 못하면 sensor investment를 보류합니다.",
            "assets": [
                {"label": "LIFT", "url": "https://arxiv.org/abs/2607.14236"},
                {"label": "Tactile Grounding", "url": "https://arxiv.org/abs/2607.14609"},
                {"label": "KineFuse", "url": "https://arxiv.org/abs/2607.14842"},
            ],
        },
        {
            "priority": "EXPLORE",
            "title": "Robot-Usable Geometry and Memory Protocol",
            "thesis": (
                "3DGS, feed-forward reconstruction, ObjectNav memory를 따로 보지 않고, robot이 실제로 map을 재사용할 수 있는지의 "
                "latency, update, stale-memory failure로 묶습니다."
            ),
            "scores": {"fit": 5, "novelty": 5, "feasibility": 3, "moat": 5, "timing": 4, "evidence": 4},
            "one_week": (
                "G2SR/Instant NuRec류 reconstruction output과 VTM-style topological memory를 ObjectNav/localization mini-suite에 연결합니다."
            ),
            "four_week": (
                "3DGS map, point-cloud registration, visual-topological memory를 같은 repeated-scene task에서 비교하고 stale memory, pose drift, "
                "navigation recovery를 분리합니다."
            ),
            "metric": "localization success +10p, update cost -30%, stale-memory failure family, navigation SPL improvement.",
            "stop": "visual-topological memory가 geometry update보다 큰 효과를 내거나 반대일 때, 약한 축을 paper appendix로 낮춥니다.",
            "assets": [
                {"label": "G2SR", "url": "https://arxiv.org/abs/2607.14470"},
                {"label": "Instant NuRec", "url": "https://arxiv.org/abs/2607.14203"},
                {"label": "VTM-Nav", "url": "https://arxiv.org/abs/2607.14514"},
            ],
        },
    ],
}


def main() -> None:
    template.DATE = DATE
    template.SLUG = SLUG
    template.DATA = DATA
    doc = template.build_html()
    doc = doc.replace("2026-07-13 arXiv Research Intelligence", "2026-07-17 arXiv Research Intelligence")
    doc = doc.replace("<span>Tier A 5편 full-text</span>", "<span>Tier A 6편 full-text</span>")

    json_dir = ROOT / "intelligence"
    json_dir.mkdir(exist_ok=True)
    json_path = json_dir / f"{DATE}.json"
    html_path = ROOT / "posts" / f"{SLUG}.html"
    json_path.write_text(json.dumps(DATA, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    html_path.write_text(doc, encoding="utf-8")
    print(f"wrote {json_path.relative_to(ROOT)}")
    print(f"wrote {html_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
