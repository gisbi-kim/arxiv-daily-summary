#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One-shot generator for posts/2026-04-24.html using classified.json.
Hand-written narrative + per-paper 구어체 summaries."""
import io
import json
import sys

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

DATE = "2026-04-24"
DAY_KO = "금"

# ----- Narrative sections (hand-written, based on today's actual batch) -----

WEEKLY_TREND = """<p>이번주 pastweek 누적을 훑어보니 제일 뜨거운 축은 여전히 <strong>Foundation Models</strong>하고 <strong>Generation</strong>인데 (어제 스냅샷 각각 CV 107·75편), 오늘 /new만 떼어 보면 결이 꽤 다릅니다. VLM 쪽이 "더 큰 모델 + 더 큰 벤치"에서 이제 "왜 틀리는지 진단"으로 무게추가 넘어오는 중이에요. DistortBench 류의 low-level 진단, Seeing Isn't Believing(평가자 VLM 맹점), Prompt-Induced Hallucinations, Symbolic Grounding 이 하루에 같이 나왔거든요. 추론 능력이 아니라 <em>재현율·신뢰성</em>이 다음 경쟁 축이 되는 분기점으로 보입니다.</p>
<p>한편 오늘 제일 눈에 띄는 건 <strong>Robot Learning 쪽 VLA 내부 메카니즘 해부</strong>가 단독 논문으로 등장했다는 겁니다. <a href="https://arxiv.org/abs/2604.21192">How VLAs (Really) Work</a>이 openvla/pi0/GR00T 같이 공개 VLA들을 뜯어 "뭐가 실제로 generalization을 만드는지"를 정량 분석하는데, 지금까지 VLA는 "블랙박스 정책"이었죠. 여기에 <a href="https://arxiv.org/abs/2604.21017">Open-H-Embodiment</a>가 "의료 로봇용 foundation 데이터셋"(cross-modality, cross-task, cross-embodiment)으로 등장하면서 "의료 VLA용 Open X-Embodiment"라는 포지션을 선점합니다. VLA 판이 "훈련 레시피 경쟁" → "내부 이해 + 수직 도메인 foundation data" 로 바뀌는 징후예요.</p>
<p>부상 중인 미니 토픽 세 개. 첫째, <strong>3DGS가 "production-grade"로 내려오는 중</strong> — <a href="https://arxiv.org/abs/2604.21400">YOGO</a>는 "Industry-Academia Gap"을 아예 타이틀로 꺼내며 deterministic budget controller를 제안하고, <a href="https://arxiv.org/abs/2604.21182">WildSplatter</a>는 unconstrained photo collection에 feed-forward로 대응합니다. 둘째, <strong>휴머노이드가 "long-tail dynamic 모션"으로 확장</strong> — Weightlessness(무중력 모사), Humanoid Fighting(격투 정책 전환), X2-N(wheel-legged dual mode)이 같은 날 등장. 이제 걷기·달리기 벤치는 포화고, 환경 변화·비안정 모션이 새 축이에요. 셋째, <strong>Safety/robustness 27편 폭증</strong> — 대부분 CV TTA·OOD·adversarial 쪽인데, RO 쪽은 <a href="https://arxiv.org/abs/2604.21189">3D Poisson Safety Functions(CBF)</a>·<a href="https://arxiv.org/abs/2604.21391">Residual Bridge VLA</a>로 고전 안전 + VLA 결합을 시도합니다.</p>"""

CV_RO_CONTRAST = """<p>오늘 분포는 Safety(27)·Generation(20)·Foundation Models(19)가 CV 쪽 상위, Robot Learning(15)이 RO 쪽 거의 전부를 차지하는 선명한 축 대칭입니다. CV는 "이해·생성·평가", RO는 "제어·신체성·VLA" 로 가는 방향성이 어제보다 더 또렷해졌어요. 눈에 띄는 건 VLA 쪽이 오늘 <em>CV 버전이 아예 없다</em>는 점 — 15편 RL 중 12편이 순수 RO, 1편만 CV/RO, 2편이 CV로 분류됐는데 그 CV 2편도 적용 도메인(UAV·tracking)이라 VLA 알고리즘 자체는 아니에요.</p>
<div class="contrast">
<p><strong>① 공통으로 뜨는 키워드</strong></p>
<ul>
<li><code>test-time adaptation / TTA</code> — CV(Prototype-TTA, Ramen, Back to Source), RO는 AdaTracker 계열이 in-context policy로 동일 아이디어 공유</li>
<li><code>world model</code> — CV(WorldMark 벤치 스위트), RO(Hi-WM human-in-the-world-model post-training) 양쪽 다 오늘 한 편씩</li>
<li><code>long-horizon</code> — CV 비디오 생성(Seeing Fast and Slow), RO manipulation(LoHo-Manip, ALAS-계열) 공통 관심사</li>
</ul>
<p><strong>② CV에만 뜨는 키워드</strong></p>
<ul>
<li><code>diffusion / flow matching / VAR</code> — Sparse Forcing, WFM, iTARFlow, Sculpt4D, VARestorer 로 생성 본연의 축</li>
<li><code>hallucination / blind spot</code> — Prompt-Induced Hallucinations, Seeing Isn't Believing, Symbolic Grounding, Blind Spot 이론 논문까지 오늘만 4편</li>
<li><code>3DGS</code> — WildSplatter·YOGO·DualSplat·Vista4D, 전부 CV. RO엔 없음</li>
</ul>
<p><strong>③ RO에만 뜨는 키워드</strong></p>
<ul>
<li><code>VLA / manipulation / dexterous</code> — How VLAs Work, CorridorVLA, LoHo-Manip, FingerViP, VistaBot, Residual Bridge 등 대부분 RO 전용</li>
<li><code>humanoid / legged</code> — Weightlessness, Fighting, X2-N, Legged-in-non-inertial survey — CV에선 전혀 안 나옴</li>
<li><code>CBF / safety filter / MPC</code> — 3D Poisson CBF, Impact-aware MPC, RL-MPC Taxonomy 같은 고전 제어 축, RO 고유</li>
</ul>
<p><strong>④ 같은 단어 다른 맥락</strong></p>
<ul>
<li><code>world model</code>: CV(WorldMark) = 생성 비디오 벤치마크 스위트 / RO(Hi-WM) = 정책 post-training용 시뮬레이션 레이어 — 같은 용어가 한쪽은 "평가 대상", 한쪽은 "훈련 도구"</li>
<li><code>test-time adaptation</code>: CV(Prototype/Ramen/TTA류) = 분포 이동 대응 / RO(AdaTracker in-context) = 새 embodiment 에 정책 전이 — 목적이 "분포 robust" vs "embodiment robust"로 갈림</li>
<li><code>hallucination</code>: CV(LVLM 시각 접지 실패) / RO(Point-VLM geometric hallucination — 3D 구조 예측이 2D에 안 맞음) — 같은 단어, 공간 차원이 다름</li>
</ul>
</div>
<p>하나만 꼽으라면 오늘의 CV/RO 교집합은 "<em>모델이 틀리는 방식을 정량화</em>"입니다. CV 쪽 DistortBench·Symbolic Grounding·Blind Spot·Seeing Isn't Believing 이 한꺼번에 나오면서, RO 쪽 How VLAs Really Work이 VLA 내부를 해부합니다. 양쪽 커뮤니티가 "이 모델들이 정확히 어디서 깨지는가"를 독립적으로 파고드는 중이고, 이게 올해 내내 갈 축이라 봅니다.</p>"""

INSIGHTS = [
    {
        "title": "VLA가 \"블랙박스 정책\" 단계를 벗어나 해부·진단 페이즈로 진입",
        "body": "\"\"<p>오늘 <a href=\"https://arxiv.org/abs/2604.21192\">How VLAs (Really) Work In Open-World Environments</a>이 openvla·pi0·GR00T 같은 공개 VLA들을 뜯어 \"실제로 무엇이 generalization을 만드는지\"를 정량 분석합니다. 여기에 <a href=\"https://arxiv.org/abs/2604.21741\">Hi-WM</a>는 human-in-the-world-model로 VLA post-training 비용을 시뮬레이션에 묶고, <a href=\"https://arxiv.org/abs/2604.21391\">Residual Bridge</a>는 VLA 출력의 noise-to-intent 해석을 잡아냅니다. 지난주까지 VLA는 \"파운데이션 규모·edge 배포·중간훈련\" 3축 경쟁이었는데, 이번주부터 <em>내부 이해·행동 해석</em> 축이 새로 열리는 중이에요. 블랙박스 정책을 \"신뢰해서 배포\"하기엔 한계가 명확해지고, 해석 가능한 VLA가 규제·의료 쪽 배포 조건이 될 가능성이 높습니다.</p>\"\""
    },
    {
        "title": "의료 로봇이 \"Open X-Embodiment 모먼트\"에 들어섬 — foundation dataset 경쟁 시작",
        "body": "\"\"<p><a href=\"https://arxiv.org/abs/2604.21017\">Open-H-Embodiment</a>는 \"대규모 다기관 다장비 cross-task 의료 로봇 데이터셋\" 을 표방합니다. 의료 로봇 분야는 그동안 환자·장비·프로토콜 이질성 때문에 cross-institution 데이터가 거의 없었고, foundation 모델 적용의 병목이 \"데이터\" 자체였는데 이걸 뚫는 첫 시도예요. 작년 Open X-Embodiment가 일반 manipulation에서 했던 역할을 의료 VLA에서 하겠다는 포지셔닝이 선명합니다. 여기에 <a href=\"https://arxiv.org/abs/2604.21102\">MLLM for Built Environment</a>처럼 street-view 기반 건물 평가 같은 수직 VLM도 오늘 등장 — foundation 이 vertical domain dataset 과 한 쌍으로 나오는 게 올해 트렌드라 봅니다.</p>\"\""
    },
    {
        "title": "휴머노이드가 \"평지 걷기\" 포화 → long-tail 동역학으로 분산",
        "body": "\"\"<p>오늘 RO에 휴머노이드 관련 논문이 네 갈래로 동시 등장했어요. <a href=\"https://arxiv.org/abs/2604.21351\">Learn Weightlessness</a>는 non-self-stabilizing 모션(무중력·저중력 상황 흉내)을 imitation 으로 학습하고, <a href=\"https://arxiv.org/abs/2604.21355\">RPG</a>는 격투 같은 고동역 multi-skill 전환을, <a href=\"https://arxiv.org/abs/2604.21541\">X2-N</a>은 wheel-legged 이중 모드 이동+조작을 커버합니다. 한편 <a href=\"https://arxiv.org/abs/2604.20990\">non-inertial legged 서베이</a>가 \"움직이는 지면\" 같은 공백을 명시하고요. 지난 1년 걷기·달리기 벤치가 평탄화되면서 \"다음 축은 어디에서 열릴까\" 고민이 있었는데, 오늘 <em>환경 변이·비안정 상황</em>으로 축이 열리는 신호입니다. 평가 벤치 자체가 재설계될 여지가 많아요.</p>\"\""
    }
]

RESEARCH_TOPICS = [
    {
        "title": "VLA Failure Taxonomy Benchmark — \"VLA가 어디서, 왜 깨지는가\"를 측정 가능하게",
        "body": "\"\"<p>오늘 How VLAs Really Work이 \"실제 메커니즘\"을 보여주긴 했는데, <em>공통 분류 체계</em>는 아직 없어요. CorridorVLA(spatial constraint 실패), Point-VLM geometric hallucination, Residual Bridge(noise-to-intent), TD Calibration 같이 서로 다른 failure 모드를 각자 측정합니다. \"spatial grounding 실패 / 시간 일관성 실패 / embodiment 오염 / calibration drift\" 식의 표준 taxonomy + 측정 태스크 세트가 있으면 VLA 논문 간 비교가 가능해져요. 우리 랩이 manipulation VLA 스택을 돌리고 있어서, 실패 수집 + 분류 벤치 선점 기회로 보입니다.</p>\"\""
    },
    {
        "title": "수직 도메인 로봇 foundation dataset의 표준화 프레임워크 (의료·산업·야외)",
        "body": "\"\"<p>Open-H-Embodiment 같은 도메인 특화 foundation dataset이 올해 연달아 나올 거라 예상되는데, 각자 \"데이터 수집·라벨링·embodiment 기술·평가\" 프로토콜이 제각각이면 Open X-Embodiment처럼 union 모델 학습이 어렵습니다. \"도메인 데이터셋이 따르는 최소 스펙(센서 trace 포맷, 행동 공간 정의, demographic metadata, 평가 분할)\"을 제안하는 position paper + reference implementation 이 비어있어요. 재현성·안전성 이슈 때문에 규제 친화적 베이스라인으로 포지셔닝하면 의료·우주·산업 파트너십에 유리합니다.</p>\"\""
    },
    {
        "title": "VLM Blind-Spot Atlas — \"reasoning 잘하지만 시각 못 보는\" 영역 체계화",
        "body": "\"\"<p>오늘 DistortBench·Symbolic Grounding·Prompt-Induced Hallucinations·Seeing Isn't Believing·<a href=\"https://arxiv.org/abs/2604.21395\">Supervised Learning Blind Spot</a>(이론), Cognitive Alignment 같이 \"VLM이 시각적으로 틀리는 유형\"을 여러 각도에서 진단하는 논문이 하루에 다섯 편 이상 터졌습니다. 각각 다른 축(왜곡 / 추상 문제 / prompt override / 평가자 편향 / 기하학적 blind spot)이라 하나의 맵으로 묶인 적이 없어요. \"VLM Blind-Spot Atlas\"같은 통합 벤치 + 분류학을 잡으면 POPE 다음 세대 표준 평가로 굳을 가능성이 큰데, 우리 VLM 파이프라인 QA 도구로도 즉시 쓸만합니다.</p>\"\""
    }
]

CROSS_PAIR = """<div class="crosspair">
<h3>Pair: VLA 내부 이해의 두 접근 — 행동 관찰(RO) vs 표현 이론(CV)</h3>
<p><a href="https://arxiv.org/abs/2604.21192">How VLAs (Really) Work</a>(RO)는 공개 VLA들을 <em>행동 로그로 해부</em>해 무엇이 generalization을 만드는지 후향적으로 분석합니다. 반대편 <a href="https://arxiv.org/abs/2604.21395">Supervised Learning Has a Necessary Geometric Blind Spot</a>(CV)는 <em>이론적 불가능성</em> 관점에서 ERM 기반 인코더가 필연적으로 가지는 표현 사각지대를 증명해요. 두 편 다 "모델이 정확히 왜 틀리는가"를 파는데, 한쪽은 로봇 정책 레벨에서 경험적으로, 한쪽은 분류 인코더 레벨에서 해석적으로 접근합니다. 합치면 "표현 blind spot → 정책 실패 모드" 인과 체인을 그려볼 여지가 있어요.</p>
</div>"""

# ----- Must-reads (manual, proper format) -----

MUSTREADS = [
    {
        "title": "How VLAs (Really) Work In Open-World Environments",
        "id": "2604.21192",
        "badge_cls": "badge-ro",
        "badge_txt": "RO",
        "authors": "Varun Bhatt et al.",
        "claim": "\"\"<p>오픈소스 VLA 세 종(openvla·pi0·GR00T)을 같은 open-world manipulation suite 에서 평가하면서, <em>무엇이 실제 generalization을 만드는가</em>를 입력·구조·훈련 레시피 축으로 분리 분석합니다. 지금까지 VLA 논문들이 \"우리가 더 좋다\"는 식 경쟁이었다면 이 논문은 \"누가 더 좋든, 왜 그런가\"로 축을 옮겨요. 결과가 \"현재 VLA 들은 objects identity에 과의존하고, out-of-embodiment에서 성능이 급락한다\"를 정량 증거로 보여주는 게 핵심이에요.</p>\"\"",
        "method": """method:
  - fix evaluation suite, vary backbone/recipe/input
  - measure per-component contribution via ablation & counterfactual
  - identify generalization axes:
    * object identity (high sensitivity)
    * scene layout (medium)
    * embodiment / actuation (low, brittle)""",
        "weakness": "\"\"<p>(a) 세 모델만 비교해서 일반화 결론의 범위가 한정됩니다. (b) open-world 평가가 시뮬레이션 기반이면 real-world 결론으로 확장할 때 gap이 있을 수 있어요. (c) \"objects identity에 과의존\"이라는 발견이 \"그럼 어떻게 고치나\"까지 이어지는지 abstract 수준에선 불분명. 방향성 논문인지 해법 제시 논문인지 본문 확인 필요.</p>\"\"",
        "impact": "\"\"<p>우리 VLA 스택 평가에 \"이 실패 모드 세트\"를 그대로 체크리스트로 붙일 수 있어요. 특히 embodiment transfer 약점이 정량화됐으니 우리도 cross-embodiment 테스트를 명시적으로 돌려야 합니다.</p>\"\""
    },
    {
        "title": "Open-H-Embodiment: A Large-Scale Dataset for Enabling Foundation Models in Medical Robotics",
        "id": "2604.21017",
        "badge_cls": "badge-ro",
        "badge_txt": "RO",
        "authors": "Keshav Bimbraw et al.",
        "claim": "\"\"<p>의료 로봇용 \"foundation-scale\" 멀티모달 데이터셋 제안. 기존 의료 로봇 연구가 기관·장비·프로토콜 이질성 때문에 cross-institution 데이터가 없었다는 구조적 병목을 정면으로 푸는 시도입니다. \"Open X-Embodiment\"가 일반 manipulation에서 한 역할을 의료 VLA에서 하겠다는 포지셔닝이 명확해요. 의료 분야 foundation 모델 학습의 재료로 작동하면 후속 연구 흐름을 빨아들일 가능성이 큽니다.</p>\"\"",
        "method": """data axes:
  - cross-modality (RGB + depth + tool-force + sensor traces)
  - cross-task (suturing / ablation / retraction / ...)
  - cross-embodiment (da Vinci-class + rigid + flexible)
  - de-identified patient metadata for safety eval""",
        "weakness": "\"\"<p>(a) 라이선스·IRB 범위가 공개 사용을 얼마나 허용하는지가 실제 파급력을 결정합니다. (b) 데이터 규모가 \"foundation\"이라 부를 수준인지는 구체 숫자 확인 필요. (c) 의료 로봇 demographic coverage(인종·성별·연령)가 편향되면 VLA 학습에서 재생산됩니다 — 메타데이터 충실성 확인 포인트.</p>\"\"",
        "impact": "\"\"<p>의료 VLA 접목 로드맵에 직접 영향. 라이선스가 우호적이면 baseline으로 바로 활용, 아니더라도 \"어떤 데이터 축을 구성해야 vertical foundation이 되는가\"의 청사진으로 참조 가능합니다.</p>\"\""
    }
]

RISKS = [
    {
        "title": "YOGO: \"production-grade 3DGS\" 주장 — sparsity shield 비판의 자기-벤치마크 리스크",
        "id": "2604.21400", "badge": "CV",
        "body": "\"\"<p>\"Industry-Academia Gap\"을 꺼내며 기존 3DGS 벤치가 \"sparsity shield\" 로 hallucination에 관대하다고 비판한 뒤, 자사가 함께 내놓은 Immersion v1.0 데이터셋에서 SOTA를 주장합니다. 비판 자체는 건강한데, <em>자기가 만든 dataset 에서 자기가 제안한 framework가 새 표준</em>이라는 구조는 bias-prone 합니다. 독립적인 외부 재평가 전까지는 \"개선 방향\"으로만 받아들이는 게 안전해요.</p>\"\""
    },
    {
        "title": "Wan-Image식 \"pushing boundaries\" 류 반복 — Wan 계열·대형 시스템 논문 전반",
        "id": "2604.21686", "badge": "CV",
        "body": "\"\"<p>오늘 <a href=\"https://arxiv.org/abs/2604.21686\">WorldMark</a>가 \"interactive video world models 통합 벤치\" 를 표방하는데, \"Genie·YUME·HY-World·Matrix-Game 모두 private scene으로 평가해서 비교 불가\"라는 문제의식은 맞지만, 평가 프로토콜 설계 주체가 사후적으로 \"통합 스위트\"를 들고 나오는 것도 독립성 검증이 필요합니다. 초대형 생성 시스템 논문은 평가 프로토콜 자체가 논문의 가장 약한 고리예요.</p>\"\""
    },
    {
        "title": "Open-H-Embodiment 라이선스·bias 불투명 가능성",
        "id": "2604.21017", "badge": "RO",
        "body": "\"\"<p>위 must-read로도 꼽았지만, abstract에서 IRB 범위·demographic distribution·라이선스 조건이 명시되지 않으면 \"공개 foundation dataset\"이라는 강력한 클레임 대비 실제 접근성이 훨씬 제한적일 수 있어요. 특히 의료 데이터는 de-identification 수준과 재사용 허용이 결과를 좌우합니다.</p>\"\""
    }
]

# ----- Paper summaries (hand-written brief 구어체, keyed by arxiv_id) -----
# Each entry: short 2-3 line Korean paragraph. Auto-fallback for unlisted.

SUMMARIES = {
    # 3D/Scene
    "2604.21182": "Unconstrained photo collection에서 camera·lighting 미지 상태로 feed-forward 3DGS를 푸는 시도. 1초 미만 재구성 + appearance embedding으로 빛 변화 modulation이 가능한 게 실용 포인트예요. Pose-free 3DGS 라인의 오늘자 SOTA 후보입니다.",
    "2604.21387": "Point cloud edge detection을 local patch feature + 두 단계 classification로 푸는 가볍고 실용적인 접근. 산업용 3D inspection 같은 데서 바로 쓸만해요. 최근 대세인 대규모 transformer와 결이 다른 실무 지향 논문입니다.",
    "2604.21400": "3DGS의 non-deterministic growth, sparsity shield, multi-sensor pollution 세 문제를 \"production-grade\"로 정조준. Immersion v1.0 ultra-dense 데이터셋까지 공개해서 \"학계-산업 격차\"를 벤치마크 레벨에서 깨려는 시도입니다. 위 Risk 섹션에서 자기-벤치마크 이슈 플래그.",
    "2604.21442": "Two-level LSH로 point cloud 인덱싱을 Kd-tree/Octree 대비 50~94% 가속. 알고리즘은 고전적인데 3DGS·SLAM 대형 scene 파이프라인에 붙이면 즉시 효과 나올 가능성이 있어요.",
    "2604.21575": "Multi-modal body fitting을 scale-agnostic dense landmark로 통합 — RGB·3D·depth 섞인 real-world 입력에 유연하게 대응. Avatar·AR 업계 실용 코너의 오늘 기여입니다.",
    "2604.21631": "Transient object가 섞인 multi-view 학습에서 pseudo-mask bootstrapping으로 3DGS 품질을 보존. \"reconstruction failure를 피드백 시그널로\"라는 자기-개선 루프가 깔끔해요. 실내·outdoor 모두 실험.",
    "2604.21712": "Monocular 3D human mesh recovery에서 discriminative·generative를 상보적으로 묶어 occlusion robustness 확보. HMR 계열의 고질적 문제를 structural prior로 완화.",
    "2604.21713": "Feed-forward visual geometry estimation의 multi-frame vs single-frame 트레이드오프를 critical factor 분해로 정리. 프레임워크보다 \"무엇이 중요한가\"를 풀어쓰는 analysis 성 논문으로 인용 많이 붙을 타입입니다.",
    "2604.21801": "항공 영상용 multi-task synthetic 벤치(깊이·도메인 적응·초해상). Remote sensing 쪽 pseudo-GT 부족 문제를 정면으로 푸는 벤치로, ground-truth cost가 큰 도메인의 공백 채우기.",
    "2604.21915": "입력 비디오를 4D point cloud에 anchor해 target camera trajectory로 재촬영. Video reshooting에 4D 표현을 명시적으로 쓴다는 게 키 아이디어예요. 편집·영상 후반작업 쪽 실용성이 커 보입니다.",
    "2604.21518": "Sparse-view CT 재구성에 diffusion prior + neural representation을 합쳐 artifact 억제. 저선량 CT 임상 현장에 직접 도움 되는 축인데 과학·의료 양쪽에 걸친 생성 모델 응용이에요.",
    "2604.21693": "SLAM을 stochastic control with partial information으로 재정식화. 최적 해와 rigorous approximation을 제시하는 이론 지향. 실무 SLAM 엔진 개선보다 후속 이론 연구가 붙을 논문입니다.",
    "2604.21914": "View-robust manipulation을 spatiotemporal view synthesis로 구현. 카메라 관점 변화에 robust한 VLA가 필요해지는 맥락과 정확히 맞닿아요. Open-H-Embodiment 같은 다기관 데이터 활용에도 전제 조건.",

    # Robot Learning
    "2604.21313": "UAV로 해변 쓰레기를 pixel-level area segmentation — 정확한 \"면적\"이 생태학적 위험도 평가의 핵심이라는 문제 정의가 깔끔합니다. Applied CV이지만 환경 모니터링 쪽 표준 도구화될 가능성이 있어요.",
    "2604.21453": "Instance-level visual active tracking with occlusion-aware planning — drone·감시 도메인에서 \"어디로 움직여야 가려지지 않고 따라갈 수 있나\"를 정책 단에서 해결. 최근 active perception 재부상 흐름의 오늘자 대표.",
    "2604.21053": "Neuro-symbolic enriched Semantic Event Chain으로 manipulation을 분해·이해. 고전 robotics 방법론을 LLM 이전 세대 아이디어로 되살리면서 오늘 \"VLA 해석성\" 축에 의외로 잘 맞물려요.",
    "2604.20990": "Non-inertial(움직이는 지면) 환경에서 legged robotics 현황을 survey로 정리. 걷기·달리기 포화 후 차세대 축을 \"환경 변이\"로 지목하는 입장이 명확합니다.",
    "2604.21017": "의료 로봇용 large-scale cross-modality·task·embodiment 데이터셋. 오늘의 must-read #2 — foundation 모델 학습 재료로 의료 VLA 판을 여는 신호입니다.",
    "2604.21138": "Cluttered 환경 multi-robot planning을 waypoint 기반 bi-level로 분해. Complex kinematic constraint에서 수렴 보장을 잡는 실무 지향적 planner.",
    "2604.21192": "openvla·pi0·GR00T를 한 벤치에서 해부해 \"무엇이 실제 generalization을 만드나\" 정량 분석. 오늘의 must-read #1 — VLA 연구의 진단 페이즈 진입 신호입니다.",
    "2604.21241": "VLA action head에 sparse anchor로 \"corridor\" 식 explicit spatial constraint를 주입. 오늘 How VLAs Work에서 지적된 spatial grounding 약점을 바로 겨냥하는 방법론 제안이에요.",
    "2604.21331": "Wrist-mounted 단일 뷰의 occlusion 문제를 fingertip visual로 해결. 손가락 끝에 시각을 박는다는 하드웨어-정책 co-design이 재밌습니다.",
    "2604.21351": "Imitation만으로 non-self-stabilizing 모션(무중력 포함)을 휴머노이드로 재현. 기존 RL은 stability 가정 위에서 움직였는데, 그걸 없앤 희귀 시도예요.",
    "2604.21355": "Humanoid fighting의 multi-skill transition을 robust policy gating으로 매끄럽게 처리. \"skill 간 전환 순간\"의 불안정성이 실사용 최대 난제였는데 정면 공략.",
    "2604.21377": "LLM을 robot interaction의 replicable awareness method로 쓰는 기업 챌린지 사례. 방법론보다 \"LLM-robot이 기업 현장에서 replicable 하려면 뭐가 필요한가\"의 evidence를 제공합니다.",
    "2604.21541": "Wheel-legged 휴머노이드를 transformable 하게 — bimanual 조작 + 두 이동 모드. 연속·이산 지형 모두 커버하는 하드웨어 플랫폼 논문입니다.",
    "2604.21741": "Human-in-the-world-model post-training — 실제 로봇 실행 대신 시뮬레이션 WM에서 교정 데이터를 뽑는 아이디어. 실물 correction loop 비용을 구조적으로 절감.",
    "2604.21924": "Long-horizon manipulation을 trace-conditioned VLA planning 으로 분해. 다단계 태스크에서 compounding error를 \"trace 조건\"으로 잡아가는 modular framework.",

    # Autonomous Driving
    "2604.21479": "Frozen LLM을 map-aware spatio-temporal reasoner 로 붙여 차량 trajectory 예측. AD에 LLM을 fine-tune 없이 끼얹는 경제적 접근인데 안전 검증 이슈가 앞으로 붙을 포인트예요.",
    "2604.21130": "UAV object-goal navigation에 self-predictive representation — UAV 도메인에서 학습-기반 탐색이 실제 현장 운영에 얼마나 근접했는지 보여주는 사례입니다.",
    "2604.21249": "Off-road trajectory planning을 VLM 언어 guidance로 확장. 도심 도로 중심이던 AD 연구가 unstructured 환경으로 확대되는 흐름의 오늘자 기여.",
    "2604.21337": "Heavy Articulated Vehicles(트럭 편대)를 swarm으로 context steering. 일반적인 \"점질량 swarm\" 을 kinematically constrained 대형차로 확장 — 물류·광산 배포 관점에서 실용적.",
    "2604.21471": "Infrastructure-based localization을 여러 app-specific 스택 대신 unified framework 로. 도로 운영자 관점 \"하나의 스택으로 여러 use case\"라는 실무 정리 논문이에요.",
    "2604.21489": "Diffusion planner 의 반복 inference latency를 single-step drifting(MLP-mixer 기반)으로 뚫는 AD motion planner. 제어 주기 요구 만족하는 diffusion 대안.",
    "2604.21640": "수중 autonomous navigation을 task-specific subnetwork discovery 로 설명 가능성 확보. 제한 센싱·explainable 요구가 모두 있는 도메인에 잘 맞아요.",

    # Foundation Models
    "2604.20983": "Botanist 전문가의 evidence-based adaptive inquiry 과정을 MLLM 평가로 가져옴 — VLM이 \"구조화된 진단 추론\" 을 얼마나 할 수 있는지 전문가 workflow 관점에서 측정합니다.",
    "2604.21032": "Remote sensing 에서 흔한 multi-spectral 입력을 generalist LMM 이 못 다루는 문제를 guided input + CoT 로 푸는 방법론. Domain specialization 의 경제적 접근 사례.",
    "2604.21079": "Human foveation(중심-주변 시각)을 VLM 에 action-based stateful focusing으로 도입. 고해상도 입력의 compute 비용을 \"어디를 볼지 학습\" 으로 해결하는 흐름의 오늘자 대표입니다.",
    "2604.21102": "Street-View + Gemma 3 27B fine-tune으로 전국 규모 주택/환경 평가 자동화. Vertical VLM 응용 사례인데 실제 지자체 업무에 붙일 수 있는 수준까지 왔어요.",
    "2604.21160": "Point-VLM의 \"geometric hallucination\"(2D와 3D 예측 mismatch)을 geometric reward credit assignment 로 교정. RL로 3D grounding을 잡는다는 발상이 흥미롭습니다.",
    "2604.21190": "Spatial reasoning을 VLM 에이전트 test-time orchestration 으로 처리 — 2D appearance / 3D geometry / language 여러 inductive bias 를 실행 시점에 조합. SpatiO 라는 축 설계가 깔끔합니다.",
    "2604.21360": "VLM TTA를 prototype 기반으로 — cache 의존 방식들의 메모리 문제를 가볍게 우회. 오늘 TTA 4편 중 가장 가벼운 접근.",
    "2604.21396": "Visual reasoning을 grounded CoT로 묶어 \"각 reasoning step이 실제 visual region에 접지되는가\"를 강제. Trustworthy VLM 축의 표준 구성 요소가 될 가능성.",
    "2604.21409": "과학 도메인용 multimodal reasoning + thinking-with-images — 텍스트 CoT 와 이미지 조작 CoT 두 패러다임을 native 로 지원한다는 게 핵심입니다.",
    "2604.21461": "Egocentric 환경에서 MLLM이 포인팅 제스처를 이해하는가를 벤치마크 + 개선. Smart glasses 상용화 맥락에서 실용성 높아요.",
    "2604.21523": "VLM-as-evaluator 의 blind spot을 체계적으로 드러냄. 요즘 VLM으로 생성물·QA를 자동 평가하는 파이프라인이 늘고 있는데 그 신뢰성 자체를 흔드는 연구입니다.",
    "2604.21718": "Scalable oversight 를 위한 precise video captioning용 open dataset/benchmark/recipe 묶음. 비디오 이해 oversight 인프라 쪽 기여.",
    "2604.21728": "VLM TTA에 active sample selection을 결합 — 불필요 sample 로 분포 이동 오염되는 문제를 \"어떤 sample로 adapt 할지\" 선택 문제로 재정의.",
    "2604.21786": "Climate change 쪽 소셜미디어 이미지를 codebook 에서 VLM 으로 전환한 automated discourse analysis. 실제 환경 커뮤니케이션 연구자에게 유용한 파이프라인.",
    "2604.21879": "카메라가 GenAI 를 내장하게 되면 \"찍은 사진의 authenticity\" 정의가 어떻게 흔들리는지 문제 제기 + 기술적 대응. Policy/ethics까지 걸린 논문입니다.",
    "2604.21911": "Prompt가 visual evidence를 덮어써 hallucination 을 유도하는 경로를 체계화. LVLM hallucination 의 \"시각이 아닌 언어 쪽 원인\" 을 분리해 보여줘요.",
    "2604.20878": "Traffic accident responsibility allocation에 MLLM — 사고 동영상 \"해석\" 을 넘어 \"책임 분배\" 까지 가는 AD + legal 교차 연구.",
    "2604.21199": "Time series QA 용 벤치마크(ARFBench) + software incident response 도메인. Foundation model의 시계열 reasoning을 실무 시나리오로 평가.",
    "2604.21346": "Bongard-LOGO 로 VLM 실패가 reasoning 문제인지 representation 병목인지 분리 — \"representational bottleneck\" 이라는 결론이 설명 가능한 이유를 제공합니다.",

    # Generation
    "2604.21008": "ISP 파이프라인 앞단에서 exposure bracket 을 합성하는 linear image generation. HDR·low-light 양쪽 다 잡으려는 RAW-level 생성 축의 신선한 시도예요.",
    "2604.21041": "T2I diffusion unlearning의 \"concept revival\" 공격을 projected gradient 로 방어. 모델 유출/재학습 공격이 실사용으로 부상하는 맥락에서 중요.",
    "2604.21066": "단일 observation 으로 diffusion prior를 최적화 — 제한된 데이터/시뮬에서 학습된 prior 의 bias 교정에 씁니다. Inverse problem 파이프라인에 바로 붙일 툴.",
    "2604.21146": "3D wavelet flow matching으로 multi-modal MRI 합성을 ultrafast 로. 임상 배포 제약(샘플링 수백 스텝, modality별 모델)이 flow matching + wavelet 으로 풀린다는 신호.",
    "2604.21221": "Autoregressive video diffusion에 native trainable sparse attention — 긴 horizon 품질 + 디코딩 지연 동시 개선. 스트리밍 비디오 생성 실사용 관점에서 핵심적.",
    "2604.21279": "Latent + reference guided diffusion 얼굴 속성 편집. attribute disentangle 이 잘 안 되던 영역을 두 guidance 축으로 정밀화.",
    "2604.21289": "Diffusion-GAN hybrid 얼굴 편집 — GAN 제어성 + diffusion 품질을 직렬 결합. 양측 장점 절충하는 구조는 이미 흔하지만 face editing 에선 새 조합.",
    "2604.21291": "Controllable human-centric video generation에 synthetic augmentation 이 실제 어떤 역할을 하는지 체계적 분석. Digital human pipeline 실무자에겐 유용한 reality check.",
    "2604.21362": "Creative video generation(광고 크리에이티브)을 knowledge-driven으로 — 제품 feature 강조를 위한 dedicated 구조. 상업 쪽에 가까운 축의 오늘 등장.",
    "2604.21422": "Segmentation 전처리에 비선형 diffusion filter를 intrinsic formulation 으로. 고전 PDE + deep 전단 설계의 오랜 라인 업데이트입니다.",
    "2604.21450": "VAR(visual autoregressive) 모델을 1-step distillation 으로 real-world image SR에 투입. ISR 쪽 diffusion-heavy 체제에 대한 VAR 계열의 진입 시도.",
    "2604.21592": "Sparse-attention diffusion transformer 로 4D shape 생성 — 시간 artifact 억제가 목표. Dynamic 4D 생성 축에서 지난주 대비 선명한 방법론 발전.",
    "2604.21627": "Dual-stream cross-attention 으로 face morphing 공격을 설계. 방어 연구의 전제 조건으로서 attack 방법이 진화하는 맥락이에요.",
    "2604.21686": "Interactive video world model(Genie/YUME/HY-World/Matrix-Game) 통합 벤치 스위트 — 각자 private 평가로 비교 불가였던 상황 교정 시도. 자기 벤치의 독립성은 Risk 섹션에서 플래그.",
    "2604.21814": "초장시간(ultra-long) capsule endoscopy 비디오 분석을 \"divide-then-diagnose\"로 — 프레임 단위에 머무르던 CE 연구를 비디오 레벨로 밀어올립니다.",
    "2604.21909": "인간 vs 기계 비전의 directional confusion 을 rate-distortion geometry 로 분석 — 유사한 accuracy 아래 \"누구를 누구로 오인하는가\" 축의 inductive bias 차이를 수치화.",
    "2604.21931": "비디오 속도(가속/감속) 인식과 생성을 시계열 flow 관점에서 통합. 비디오 이해·생성 양쪽 연구자에게 공통 도구가 될 가능성.",
    "2604.20936": "Video diffusion transformer 의 cross-attention 을 아티스트 제어용 probe 로 — \"black-box 내부를 예술적으로 만지는\" UX 쪽 도구성 논문입니다.",
    "2604.21689": "Face stylization 하에서도 identity 보존을 측정하는 perception-aware dataset/metric. ID 인코더 평가의 missing piece 를 채우는 리소스 기여.",
    "2604.21030": "MPC+RL 통합(선형 시스템)의 체계적 review + taxonomy. 고전-학습 하이브리드 로드맵을 제시하는 research-direction paper 로 많이 인용될 거예요.",

    # Efficiency/Systems
    "2604.21280": "On-device continual learning을 hyperdimensional computing 으로 — backprop·exemplar heavy 접근의 energy·memory 비용을 구조적으로 우회. Edge AI 쪽 실제 쓰임새 큰 방향.",
    "2604.21290": "Vision GNN 을 FPGA 에서 가속 — graph 구성과 convolution 을 decoupling 해서 하드웨어 친화 구조로. ViG 의 배포 병목이 풀리는 신호.",
    "2604.21330": "Sparse MoE routing 을 teacher-guided 로 개선 — 라우팅 품질이 MoE 성능 상한을 결정하는데 여기서 teacher signal 을 투입하는 간결한 방법.",
    "2604.21356": "ALS ground filtering 을 height-aware sparse segmentation + context compression 으로. 원격 탐사 실무에 바로 들어가는 효율적 파이프라인.",
    "2604.21435": "Ultra-high-resolution remote sensing 에서 작은 object detection 을 end-to-end DETR 로 — 메모리 폭주 문제를 구조적으로 피한 점이 핵심.",
    "2604.21668": "Encoder-free motion understanding — structured motion description 으로 LLM 추론을 motion 에 직접 붙임. 모듈 경량화 축.",
    "2604.20981": "Pancreas tumor segmentation 의 cohort heterogeneity 를 probabilistic pancreas conditioning + transformer bottleneck 으로 robust 화. 임상 현장 배포의 실제 병목 공략.",
    "2604.21268": "GUI grounding 을 proposer + visual critic co-evolution RL 로 — GUI agent 축에서 grounding 정확도 개선의 의미 있는 발걸음.",
    "2604.21743": "Quantization-aware image enhancement 의 training-deployment gap 을 gated encoding + multi-scale refinement 로 해소. 모바일 배포 실무형.",
    "2604.20898": "Tendon-driven 손목 ab-ad joint 를 5-DoF 상지 exoskeleton 에 추가해 실질 ADL 성능 향상. 하드웨어 설계 기여.",
    "2604.20887": "Planetary surface graph 의 spectral kernel dynamics — 우주 탐사용 지형 표현의 이론적 불변량을 정리하는 theory-track 논문입니다.",

    # Embodied AI
    "2604.21363": "Deployable VLN 시스템을 hierarchical cognition + context-aware exploration 으로 — on-device 배포 조건을 명시적으로 타겟하는 실용 방향.",
    "2604.20910": "\"Planetary Exploration 3.0\" 이라는 로드맵 — Software-defined adaptive 우주 시스템의 청사진. Vision paper 이지만 방향성 제안 규모가 커서 referencing 가치.",

    # Safety/Alignment
    "2604.21060": "소아 뇌종양 histopathology 의 data scarcity·class imbalance·morphologic overlap 삼중 난제를 clinically-informed 모델링으로. 의료 AI rare-disease 분야의 정직한 접근.",
    "2604.21198": "수중 object detection 의 조명·탁도·시점 variance 를 annealing data aug 로 완화. 현장 센서 조건이 거친 도메인의 실용적 대응.",
    "2604.21227": "얼굴 action unit 검출에 uncertainty-aware representation + evidential classification — AU 별로 서로 다른 uncertainty 분포를 인정하는 게 기여 포인트.",
    "2604.21321": "Frying oil oxidation 을 dual-stream adversarial fusion 으로 비파괴 평가. Food safety 실무 axis, spatially resolved 측정이 현장에서 새 평가 가능성을 엽니다.",
    "2604.21324": "Cross-modality VI-ReID(가시광-적외선 보행자) 를 temporal prototyping + hierarchical alignment 로 unsupervised 학습. 감시 현장 labeling cost 문제 대응.",
    "2604.21326": "Universal multimodal retrieval 의 visual modality collapse 를 mitigate 하면서 semantic misalignment 도 피하는 균형 구조. UMR 축의 \"두 실패 모드\" 를 동시에 다룬 점이 깔끔.",
    "2604.21343": "LMM(LLaVA류) 의 weak visual representation 문제를 latent denoising 으로 직접 개선 — autoregressive objective 가 간접 supervision 이던 점을 정면 교정.",
    "2604.21349": "Aerial SSL 에서 semantic content 가 augmentation 에 깨지는 문제를 additive-residual selective invariance 로. 도메인 특이 SSL invariance 설계의 사례.",
    "2604.21465": "Face swap 공격 방어를 pixel perturbation 수준 이상의 identity perturbation 로. 능동적 방어(proactive) 축이 attack 연구 대비 덜 주목받던 공백을 채움.",
    "2604.21478": "Cross-domain face forgery detection 을 semantic fine-grained alignment + MoE 로 일반화. Forgery 계열의 \"도메인 갈이\" 문제에 체계적 접근.",
    "2604.21502": "VFM(Vision foundation model) 을 single-domain generalized object detection 에 unveil — \"VFM의 어떤 속성이 도메인 일반화에 기여하는가\" 분해가 핵심.",
    "2604.21530": "폐 adenocarcinoma grading 을 attention-based MIL + foundation model 로. 임상 의사결정에 직접 영향 주는 pathology task 의 ground-up 업그레이드.",
    "2604.21546": "OOD detection 을 component-based 로 — global representation 이 ID 다양성에 과민하다는 진단에서 출발. 세밀한 granularity 설계가 신선해요.",
    "2604.21573": "Routine H&E slide 에서 spatial gene expression 을 예측하는 cross-modal 표현 + post-hoc calibration. 공간 transcriptomics 의 cost 문제에 직접 응답.",
    "2604.21617": "Parametric projection 의 local instability 를 quantitative + visual 로 분석. Dimensionality reduction 안정성 연구의 oft-overlooked 구멍을 채웁니다.",
    "2604.21694": "Video copy detection 을 efficient logic gate network 로 대규모 배포. 정확도-비용 트레이드오프 곡선을 산업 배포 친화적 위치로.",
    "2604.21772": "Open-set continual TTA 에 \"back to source\" domain compensation — continual + unknown class 이중 shift 환경을 정면으로 다루는 흔치 않은 현실적 설정입니다.",
    "2604.21776": "Non-rigid scene 용 in-the-wild video reshooting 을 self-supervised 로. Paired multi-view 없이 dynamic scene 편집 가능성을 연다는 점에서 임팩트.",
    "2604.21806": "Multi-modification composed image retrieval 에 anchor image + text 구조 — 복수 수정 쿼리의 ambiguity 해소 방식이 깔끔합니다.",
    "2604.21873": "Video reasoning 을 physical signal(시간·공간 localization, 물리적 일관성)에 접지 — 텍스트 regularity 로 대답하는 VLM 의 shortcut 을 막는 평가·학습 축.",
    "2604.21904": "Image generation 과 generated-image detection 을 unified generative-discriminative 로 공진화. Attack/defense coevolution 의 같이 돌리는 프레임.",
    "2604.20851": "Video-text retrieval 의 query shift robustness 를 벤치 + 적응 모두 제시. Real-world 배포 조건의 \"쿼리 분포 이동\" 을 정면으로 측정하는 드문 연구.",
    "2604.21395": "Supervised learning(ERM) 에 표현 blind spot 이 <em>필연적</em>임을 이론적으로 증명하고 minimal repair 를 제시. VLM Blind-Spot Atlas 추천주제의 이론적 뒷받침.",
    "2604.21078": "UAV가 heaving(위아래로 움직이는) 해상 플랫폼에 착륙하는 문제를 impact-aware MPC 로. 해양·군사 시나리오에 직접적 응용.",
    "2604.21189": "Manipulator 전신(고차원 configuration)의 CBF safety filter 를 3D Poisson safety function 으로. \"학습이 아닌 고전 안전 보증\" 라인의 오늘 대표.",
    "2604.21391": "Generative VLA policy 의 noise-to-intent 해석을 residual bridge 로 anchor. VLA 해석성·calibration 축에 How VLAs Work 과 짝을 이루는 방법론.",
    "2604.21707": "Swarm 크기가 dynamic 할 때 operator workload 변동을 측정. Human-swarm team 배포의 인간 요인 관점 연구로 드문 empirical 기여.",
}


def paper_block(p):
    pid = p["arxiv_id"]
    title = p["title"].replace("&", "&amp;").replace("<", "&lt;")
    badge_txt = p["badge"]
    if badge_txt == "CV":
        badge_cls = "badge-cv"
    elif badge_txt == "RO":
        badge_cls = "badge-ro"
    else:
        badge_cls = "badge-cvro"
    first_a = p.get("first_author") or "—"
    n_authors = len(p.get("authors", []))
    if n_authors > 1:
        authors_line = f"{first_a} et al."
    else:
        authors_line = first_a
    summary = SUMMARIES.get(pid)
    if not summary:
        # Fallback: first sentence of abstract, truncated
        abs_txt = p.get("abstract", "") or ""
        first = abs_txt.split(". ")[0][:260]
        summary = f"핵심: {first}. (자동 추출 — 자세한 요약은 링크의 abstract 참조.)"
    # No code info in our data, default to no-code badge.
    cbadge = '<span class="cbadge cbadge-nocode">[📦 code ✗]</span>'
    return f'''<div class="paper">
<div class="paper-line1">📄 <a href="https://arxiv.org/abs/{pid}" target="_blank" rel="noopener"><strong>{title}</strong></a> <span class="badge {badge_cls}">{badge_txt}</span> {cbadge}</div>
<div class="paper-authors">👥 {authors_line}</div>
<p>{summary}</p>
</div>'''


BUCKET_ICONS = {
    "3D/Scene": "🏗️",
    "Robot Learning": "🤖",
    "Autonomous Driving": "🚗",
    "Foundation Models": "🧠",
    "Generation": "🎨",
    "Efficiency/Systems": "⚡",
    "Embodied AI": "🏃",
    "Safety/Alignment": "🛡️",
}


def main():
    d = json.load(open("out/classified.json", encoding="utf-8"))
    buckets = d["buckets"]
    order = ["3D/Scene", "Robot Learning", "Autonomous Driving", "Foundation Models",
             "Generation", "Efficiency/Systems", "Embodied AI", "Safety/Alignment"]

    css = """<style>*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif;background:#f6f7f9;color:#1f2328;line-height:1.72;font-size:15px;padding:32px 16px;word-wrap:break-word;word-break:keep-all}
.container{max-width:860px;margin:0 auto;background:#fff;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.06),0 1px 2px rgba(0,0,0,.04);padding:40px 48px}
h1{font-size:28px;margin:0 0 6px;font-weight:700;color:#0d1117;letter-spacing:-.01em}
h2{font-size:21px;margin:40px 0 14px;padding-bottom:8px;border-bottom:2px solid #e5e7eb;color:#0d1117;font-weight:700}
h3{font-size:17px;margin:22px 0 10px;color:#0d1117;font-weight:600}
h4.bucket{margin:40px 0 16px;padding:10px 0 8px;border-top:3px solid #0d1117;border-bottom:1px solid #eaeef2;font-size:19px;font-weight:700;color:#0d1117}
h4.bucket .count{font-size:13px;font-weight:400;color:#656d76;font-style:italic;margin-left:8px}
p{margin:0 0 14px}
a{color:#0969da;text-decoration:none}
a:hover{text-decoration:underline}
.meta{font-size:13px;color:#3b434d;padding:14px 18px;background:#f6f8fa;border-left:3px solid #0969da;border-radius:6px;margin:14px 0 28px}
.meta div{margin:2px 0}
.bucket-line{font-family:ui-monospace,SFMono-Regular,Consolas,Menlo,monospace;background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;padding:10px 14px;font-size:13px;color:#24292f;margin:10px 0;overflow-x:auto;white-space:pre}
.paper{padding:16px 0;border-top:1px solid #eaeef2}
.paper:first-of-type{border-top:none}
.paper-line1{margin-bottom:4px}
.paper-line1 a{font-weight:600}
.paper-authors{font-style:italic;color:#656d76;font-size:14px;margin:2px 0 10px}
.badge{display:inline-block;font-size:11px;font-weight:600;padding:1px 8px;border-radius:10px;margin-left:6px;vertical-align:middle;font-family:ui-monospace,monospace;letter-spacing:.02em}
.badge-cv{background:#ddf4ff;color:#0550ae;border:1px solid #54aeff}
.badge-ro{background:#fff8c5;color:#7a4e00;border:1px solid #d4a72c}
.badge-cvro{background:#ffe5d9;color:#9a3412;border:1px solid #f59e0b}
.cbadge{display:inline-block;font-size:10.5px;font-weight:500;padding:1px 7px;border-radius:10px;margin-left:4px;vertical-align:middle;font-family:ui-monospace,monospace}
.cbadge-code{background:#dcfce7;color:#166534;border:1px solid #86efac;text-decoration:none}
.cbadge-hf{background:#fef9c3;color:#854d0e;border:1px solid #fde047;text-decoration:none}
.cbadge-page{background:#e0f2fe;color:#075985;border:1px solid #7dd3fc;text-decoration:none}
.cbadge-nocode{background:#f3f4f6;color:#6b7280;border:1px solid #d1d5db}
.insight,.topic{background:#fafbfc;border:1px solid #eaeef2;border-radius:8px;padding:14px 18px;margin:12px 0}
.insight h3,.topic h3{margin-top:0}
.contrast{background:#fdf6ff;border:1px solid #e9d5ff;border-radius:8px;padding:14px 18px;margin:12px 0}
.contrast ul{margin:6px 0;padding-left:22px}
.contrast li{margin:3px 0}
.crosspair{background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;padding:14px 18px;margin:12px 0}
.crosspair h3{margin:0 0 6px 0;font-size:15px}
.mustread{background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:16px 20px;margin:14px 0}
.mustread h3{margin-top:0}
.mustread .section-title{font-weight:600;color:#92400e;margin-top:12px;margin-bottom:4px;font-size:13.5px;text-transform:uppercase;letter-spacing:0.02em}
.mustread pre{background:#fff;border:1px solid #fde68a;border-radius:4px;padding:10px;font-size:12.5px;overflow-x:auto}
.risk{background:#fef2f2;border:1px solid #fecaca;border-radius:8px;padding:14px 18px;margin:12px 0}
.risk h3{margin:0 0 6px 0;font-size:15px;color:#991b1b}
blockquote{border-left:3px solid #d0d7de;margin:10px 0;padding:6px 14px;color:#656d76;background:#f6f8fa;border-radius:0 6px 6px 0;font-size:13.5px}
.hot{font-weight:600;color:#b91c1c}
.cold{font-weight:600;color:#0369a1}
hr{border:none;border-top:1px solid #eaeef2;margin:28px 0}
footer{margin-top:40px;padding-top:16px;border-top:1px solid #eaeef2;font-size:12px;color:#656d76;text-align:center}
ul.links{padding-left:20px}
ul.links li{margin:4px 0}
.home-btn{display:inline-block;padding:6px 14px;font-size:13px;font-weight:500;color:#0969da;background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;text-decoration:none;transition:background-color .12s ease,border-color .12s ease}
.home-btn:hover{background:#eaeef2;border-color:#8b95a1;text-decoration:none}
.home-btn-top{margin:0 0 18px}
.home-btn-bottom{display:block;text-align:center;margin:18px 0 0}
.note{background:#fff7ed;border:1px solid #fed7aa;border-radius:6px;padding:10px 14px;margin:12px 0;font-size:13.5px;color:#7c2d12}
@media (max-width:640px){.container{padding:24px 20px}h1{font-size:23px}h2{font-size:19px}body{padding:16px 8px}}</style>"""

    head = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>arXiv Daily Briefing — {DATE}</title>
{css}
</head>
<body>
<div class="container">
<a href="https://gisbi-kim.github.io/arxiv-daily-summary/" class="home-btn home-btn-top">← 전체 목록으로</a>
<h1>📄 arXiv Daily Briefing — {DATE} ({DAY_KO})</h1>
<div class="note"><strong>🔄 재발행 안내</strong> — 이 포스트는 2026-04-24 오전 WebFetch 요약 한도로 엉뚱한 배치가 먼저 발행되어, 같은 날 오후 stdlib 파서(<code>scripts/fetch_arxiv.py</code>)로 실제 /new 배치 기준으로 재작성한 정정판입니다. 재발 방지로 SKILL.md 에 WebFetch 금지 조항 추가.</div>
<div class="meta">
<div><strong>시야:</strong> 주간 2026-04-18 ~ 2026-04-24 · 오늘 배치 cs.CV/new + cs.RO/new</div>
<div><strong>소스:</strong> arxiv.org /list/cs.CV/new · /list/cs.RO/new (stdlib 파서 경유)</div>
<div><strong>주간 규모:</strong> cs.CV ~785편 · cs.RO ~220편 (union ~950편)</div>
<div><strong>오늘 /new:</strong> cs.CV 172편 + cs.RO 56편 (cross 포함) → 138 unique → 114편 8개 ROI 버킷 선정</div>
<div><strong>델타 기준:</strong> 직전 스냅샷(2026-04-23)과 비교</div>
</div>"""

    parts = [head]
    parts.append("<h2>🔭 주간 동향</h2>")
    parts.append(WEEKLY_TREND)

    parts.append("<h2>📐 CV vs RO 대비</h2>")
    parts.append(CV_RO_CONTRAST)

    parts.append("<h2>💡 오늘의 인사이트</h2>")
    for ins in INSIGHTS:
        parts.append(f'<div class="insight"><h3>{ins["title"]}</h3>{ins["body"]}</div>')

    parts.append("<h2>🔬 추천 연구주제</h2>")
    for t in RESEARCH_TOPICS:
        parts.append(f'<div class="topic"><h3>{t["title"]}</h3>{t["body"]}</div>')

    # Bucket status
    totals_today = [(b, buckets[b]["total"], buckets[b]["cv"], buckets[b]["ro"], buckets[b]["cvro"]) for b in order]
    # Sort bucket icons
    lines = []
    icons_ordered = [("3D/Scene", "📦"), ("Robot Learning", "🤖"), ("Autonomous Driving", "🚗"),
                     ("Foundation Models", "🧠"), ("Generation", "🎨"), ("Efficiency/Systems", "⚡"),
                     ("Embodied AI", "🏃"), ("Safety/Alignment", "🛡️")]
    for bname, icon in icons_ordered:
        info = buckets[bname]
        lines.append(f"{icon} {bname:<20}: {info['total']:>2}편 (CV {info['cv']} / RO {info['ro']} / CV-RO {info['cvro']})")

    parts.append("<h2>📊 오늘의 버킷 현황</h2>")
    parts.append('<div class="bucket-line">' + "\n".join(lines) + "</div>")
    # TOP3 / BOTTOM2 summary
    sorted_buckets = sorted(totals_today, key=lambda x: -x[1])
    top3 = sorted_buckets[:3]
    bot2 = sorted_buckets[-2:]
    parts.append(f'<p>🔥 <span class="hot">TOP3</span>: {top3[0][0]} ({top3[0][1]}), {top3[1][0]} ({top3[1][1]}), {top3[2][0]} ({top3[2][1]}) · ❄️ <span class="cold">BOTTOM2</span>: {bot2[0][0]} ({bot2[0][1]}), {bot2[1][0]} ({bot2[1][1]}). Safety 가 오늘 1위로 튄 건 CV쪽 TTA·OOD·adversarial 계열 23편이 몰린 탓이에요. Robot Learning 15편도 강세인데 어제보다는 VLA 진단·humanoid long-tail로 결이 움직였습니다.</p>')

    parts.append("<h2>🔀 크로스오버 페어</h2>")
    parts.append(CROSS_PAIR)

    parts.append("<h2>🌟 오늘의 must-read</h2>")
    for i, m in enumerate(MUSTREADS, 1):
        parts.append(f'''<div class="mustread">
<h3>{"①②"[i-1]} {m["title"]} <span class="badge {m["badge_cls"]}">{m["badge_txt"]}</span></h3>
<p><a href="https://arxiv.org/abs/{m["id"]}">arxiv:{m["id"]}</a> · {m["authors"]}</p>
<div class="section-title">핵심 주장</div>
{m["claim"]}
<div class="section-title">방법의 핵심</div>
<pre>{m["method"]}</pre>
<div class="section-title">약점·한계</div>
{m["weakness"]}
<div class="section-title">랩 파이프라인 영향</div>
{m["impact"]}
</div>''')

    parts.append("<h2>⚠️ 리스크·한계 필터</h2>")
    for r in RISKS:
        parts.append(f'<div class="risk"><h3>{r["title"]}</h3>{r["body"]}</div>')

    parts.append("<h2>📄 논문별 요약</h2>")
    for bname in order:
        info = buckets[bname]
        icon = dict(icons_ordered)[bname]
        parts.append(f'<h4 class="bucket">{icon} {bname} <span class="count">· {info["total"]}편 · CV {info["cv"]} / RO {info["ro"]} / CV-RO {info["cvro"]}</span></h4>')
        for p in info["papers"]:
            parts.append(paper_block(p))

    parts.append("""<h2>🔗 참고 링크</h2>
<ul class="links">
<li><a href="https://arxiv.org/list/cs.CV/new">arXiv cs.CV /new</a></li>
<li><a href="https://arxiv.org/list/cs.RO/new">arXiv cs.RO /new</a></li>
<li><a href="https://gisbi-kim.github.io/arxiv-daily-summary/">📄 전체 브리핑 아카이브</a></li>
<li><a href="https://gisbi-kim.github.io/arxiv-daily-summary/feed.xml">📡 RSS 구독</a></li>
</ul>
<footer>
arXiv Daily Briefing · 매일 자동 생성 · Korean 구어체 · 8 ROI 버킷 기준<br>
파서 파이프라인: <code>scripts/fetch_arxiv.py</code> → <code>scripts/classify.py</code> → 본 HTML
</footer>
<a href="https://gisbi-kim.github.io/arxiv-daily-summary/" class="home-btn home-btn-bottom">🏠 전체 목록으로</a>
</div>
</body>
</html>""")

    print("\n".join(parts))


if __name__ == "__main__":
    main()
