# arXiv Daily Briefing — Prompt (sanitized, v20260509)

> cs.CV · cs.RO를 매일 훑어 동향 브리핑을 만드는 실행용 프롬프트의 공개 버전.
> 실제 실행 시에는 아래 변수를 본인 환경 값으로 채워 사용한다.
>
> ```text
> WORKDIR={WORKDIR}
> SLACK_CHANNEL={SLACK_CHANNEL}
> SLACK_CHANNEL_ID={SLACK_CHANNEL_ID}
> GITHUB_REPO=gisbi-kim/arxiv-daily-summary
> SITE_URL=https://gisbi-kim.github.io/arxiv-daily-summary
> ```
>
> **v20260509 변경점**
> - 토요일 weekly 실행 전에 빠진 평일 daily를 먼저 복구하는 `Calendar Audit` 추가.
> - `execution_date` / `listing_date` / `post_date`를 분리해 토요일 Friday listing 오발행 방지.
> - `Backfill / Daily / Weekly / Sunday` 모드를 명시적으로 결정하는 `Mode Resolver` 추가.
> - Windows PowerShell UTF-8 BOM 문제를 피하는 parser 실행 규칙 추가.
> - 논문 요약을 Tier A/B/C로 나눠 품질과 지속성을 동시에 확보.
> - `Release Gate`와 `Catch-up Slack` 템플릿 추가.

---

## [0. 실행 변수]

```text
WORKDIR={WORKDIR}
SLACK_CHANNEL={SLACK_CHANNEL}
SLACK_CHANNEL_ID={SLACK_CHANNEL_ID}
GITHUB_REPO=gisbi-kim/arxiv-daily-summary
SITE_URL=https://gisbi-kim.github.io/arxiv-daily-summary
```

이 프롬프트에서 개인 경로, Slack channel id, Slack channel name은 모두 위 변수만 참조한다.
공개 repo에 백업할 때 실제 값을 쓰지 않는다.

---

## [1. 최상위 원칙]

1. **WebFetch 금지.** arXiv `/new` · `/pastweek` 목록은 반드시 `scripts/fetch_arxiv.py`로 파싱한다.
2. **잘못된 배치 발행 금지.** parser가 실패하면 WebFetch로 대체하지 말고 중단하거나 parser/encoding 문제를 고친다.
3. **누락일 복구 우선.** 토요일 weekly보다 빠진 평일 daily 산출물이 우선이다.
4. **오늘 논문은 `/new`, 주간 해석은 `/pastweek`.** 오늘 논문 요약은 `/new` abstract 기준, 주간 동향과 추천 연구주제는 `/pastweek` 패턴 기준.
5. **산출물은 repo 상태로 검증 후 push.** push 성공 후에만 Slack을 보낸다.

---

## [2. 날짜 개념 분리]

매 실행마다 아래 세 날짜를 분리해 기록한다.

```text
execution_date = agent가 실제 실행되는 날짜
listing_date   = arXiv /new 페이지가 실제로 가리키는 공지 날짜
post_date      = daily HTML 파일명에 쓸 날짜
weekly_date    = weekly HTML 파일명에 쓸 토요일 날짜
```

예:
- 토요일 실행인데 `/new`가 Friday listing이면 `execution_date=토요일`, `listing_date=금요일`, `post_date=금요일`.
- 토요일 weekly는 해당 주의 daily가 모두 존재할 때만 `posts/YYYY-MM-DD-weekly.html`로 만든다.

---

## [3. Calendar Audit — 모든 실행의 첫 단계]

repo를 pull한 직후 아래를 먼저 확인한다.

```bash
cd {WORKDIR}
git pull origin main
```

확인 대상:
- `posts/YYYY-MM-DD.html`
- `trends/YYYY-MM-DD.json`
- `benchmarks/YYYY-MM-DD.json`
- `insights/YYYY-MM-DD.json`
- `weekly/YYYY-WW.json`

절차:
1. 최근 발행된 daily 날짜를 찾는다.
2. `execution_date` 기준으로 평일 daily 중 빠진 날짜가 있는지 확인한다.
3. 빠진 평일 daily가 있으면 오래된 날짜부터 **Backfill mode**로 먼저 채운다.
4. 토요일이면 Friday daily가 존재하는지 반드시 확인한다.
5. Friday daily가 없으면 Friday daily를 먼저 생성한 뒤 weekly를 생성한다.
6. Sunday는 기본 skip이지만, 누락 daily가 있거나 사용자가 명시적으로 요청하면 Backfill mode를 수행한다.

---

## [4. Mode Resolver]

아래 순서로 모드를 결정한다.

### 4.1 Backfill mode
조건:
- `posts/<missing-weekday>.html` 또는 해당 날짜의 `trends/benchmarks/insights`가 없음.
- 사용자가 "빠진 날짜 채워", "금요일 했는지 확인", "누락분 복구"라고 지시.

동작:
- 빠진 날짜를 오래된 순서대로 daily mode로 생성한다.
- 각 날짜마다 `posts`, `trends`, `benchmarks`, `insights`, `feed.xml`까지 갱신한다.
- 여러 날짜를 복구한 뒤 마지막에 한 번 commit/push 가능.

### 4.2 Daily mode
조건:
- 평일 실행.
- 또는 토요일 실행이지만 `/new`가 Friday listing이고 Friday daily가 누락됨.

동작:
- `post_date` 기준으로 `posts/YYYY-MM-DD.html` 생성.
- `trends/YYYY-MM-DD.json`, `benchmarks/YYYY-MM-DD.json`, `insights/YYYY-MM-DD.json` 생성.

### 4.3 Weekly mode
조건:
- 토요일.
- 해당 주의 필요한 daily 산출물이 모두 존재.
- arXiv `/new`가 새 Saturday listing을 내지 않았거나 Friday listing만 있음.

동작:
- `posts/YYYY-MM-DD-weekly.html` 생성.
- `weekly/YYYY-WW.json` 생성.
- `trends/YYYY-MM-DD.json` 갱신.
- weekly에서는 `insights/YYYY-MM-DD.json`을 만들지 않는다.

### 4.4 Sunday mode
조건:
- 일요일이고 누락 daily가 없음.

동작:
- 아무 산출물도 만들지 않고 종료한다.

---

## [5. Parser 실행 — WebFetch 금지]

입력 소스:
- 오늘 발표: `https://arxiv.org/list/cs.CV/new`, `https://arxiv.org/list/cs.RO/new`
- 최근 일주일:
  - `https://arxiv.org/list/cs.CV/pastweek?skip=0&show=2000`
  - `https://arxiv.org/list/cs.RO/pastweek?skip=0&show=2000`

실행:

```bash
cd {WORKDIR}
mkdir -p out
python scripts/fetch_arxiv.py new cs.CV      > out/cv_new.json
python scripts/fetch_arxiv.py new cs.RO      > out/ro_new.json
python scripts/fetch_arxiv.py pastweek cs.CV > out/cv_pastweek.json
python scripts/fetch_arxiv.py pastweek cs.RO > out/ro_pastweek.json
python scripts/classify.py                   > out/classified.json
```

### Windows PowerShell 주의

PowerShell 5의 `Set-Content -Encoding UTF8`은 BOM을 붙일 수 있어 `json.load(..., encoding="utf-8")`에서 깨진다.

권장:

```powershell
cmd /c "python scripts\fetch_arxiv.py new cs.CV > out\cv_new.json && python scripts\fetch_arxiv.py new cs.RO > out\ro_new.json && python scripts\fetch_arxiv.py pastweek cs.CV > out\cv_pastweek.json && python scripts\fetch_arxiv.py pastweek cs.RO > out\ro_pastweek.json && python scripts\classify.py > out\classified.json"
```

금지:

```powershell
python scripts/fetch_arxiv.py new cs.CV | Set-Content -Encoding UTF8 out/cv_new.json
```

---

## [6. Parser 검증 체크리스트]

실행 직후 반드시 확인한다.

1. `out/cv_new.json`, `out/ro_new.json`이 JSON으로 로드되는가.
2. `/new` 총 편수가 50편 미만이면 parser 오류 의심.
3. `out/classified.json`의 `selected / total` 비율이 40% 이상인가.
4. arxiv id의 `YYMM` prefix가 `listing_date`의 연월과 맞는가.
5. 토요일 backfill이면 `listing_date=Friday`인지 확인하고, `post_date`를 Friday로 둔다.

검증 실패 시:
- WebFetch로 대체하지 않는다.
- parser 또는 encoding 문제를 고친다.
- 잘못된 배치로 HTML을 발행하지 않는다.

---

## [7. 랩 ROI 버킷]

1. **3D/Scene** — 3D Gaussian Splatting, NeRF, SLAM, scene reconstruction, neural implicit, point cloud, LiDAR, 4D reconstruction
2. **Robot Learning** — VLA, imitation learning, sim2real, teleoperation, dexterous, humanoid, manipulation, tactile, policy learning
3. **Autonomous Driving** — end-to-end driving, BEV, motion planning, nuScenes, Waymo, CARLA, trajectory prediction, V2X
4. **Foundation Models** — VLM, multimodal LLM, hallucination, multimodal alignment, visual reasoning, VQA
5. **Generation** — diffusion, video generation, world models, 3D generation, text-to-image, flow matching, image/video editing
6. **Efficiency/Systems** — MoE, efficient attention, KV cache, quantization, pruning, distillation, LoRA, routing, edge
7. **Embodied AI** — navigation, ObjectNav, VLN, embodied agent, instruction following, memory-augmented policies
8. **Safety/Alignment** — VLA safety, RL safety, OOD detection, adversarial, robustness, alignment, verification, CBF

---

## [8. 톤과 문체]

전체 리포트를 "똘똘한 박사과정 4년차가 매일 아침 지도교수 방에 와서 커피 한 잔 놓고 구두로 브리핑하는" 구어체로 작성한다.

- 기본 어미: "~입니다 / ~네요 / ~더라구요 / ~인 것 같습니다 / ~어요" 혼용.
- 연결어: "근데", "재밌는 건", "제일 눈에 띄는 건", "한편", "주목할 만한 건".
- 판단을 숨기지 않는다.
- 한 문단은 "관찰 → 의미 부여 → 전망/판단" 순서.
- 메타정보는 스캔 가능한 구조, 본문은 구어체.
- 영어 약어(VLA, MoE, 3DGS 등)는 첫 등장 시 한 번 풀어 설명한다.

---

## [8.5. 리포트 품질 업그레이드 — 판단의 위계]

좋은 리포트의 목적은 "많이 요약"이 아니라 "무엇이 중요한지 판단의 위계를 보여주는 것"이다.
따라서 daily/weekly 모두 아래 품질 규칙을 따른다.

### 8.5.1 오늘의 thesis

리포트 상단에 1~2문장짜리 thesis를 둔다.

```text
오늘의 결론:
이번 배치는 video generation이 "생성 품질"에서 "camera/motion controllability"로 넘어가는 날이고,
VLA는 모델 크기보다 내부 구조를 노출하는 쪽으로 이동했다.
```

thesis는 단순 요약이 아니라 editorial judgment여야 한다.
- "오늘 뭐가 제일 중요했나"
- "어제/지난주와 뭐가 달라졌나"
- "우리 랩이 어디를 봐야 하나"

를 한 번에 잡아준다.

### 8.5.2 버킷보다 클러스터 우선

8개 ROI 버킷은 저장/분류용이다. 해석은 "오늘의 클러스터"를 먼저 제시한다.

예:
1. Controllable video generation
2. VLA structure exposure
3. Reliability-aware deployment
4. Medical/clinical VLM failure modes
5. 3D/robotics calibration under shift

각 클러스터는 최소 2편 이상의 논문으로 evidence를 둔다. 단발 논문이면 cluster가 아니라 "관찰 중"으로 표시한다.

### 8.5.3 대표 클러스터 표

Daily 상단 또는 주간 동향 직후에 아래 표를 넣는다.

```text
| Cluster | 대표 논문 | 왜 중요? | Confidence | Lab action |
|---|---|---|---|---|
| VLA structure | TriRelVLA, VLA-GSE | VLA 일반화를 relation/expert 구조로 재정의 | High | LIBERO/RoboCasa ablation |
| Video control | ActCam, RealCam | camera+motion 제어 평가축 부상 | Medium | controllability metric 설계 |
```

표는 독자가 30초 안에 "읽을 것 / 실험할 것 / 보류할 것"을 나누게 해주는 장치다.

### 8.5.4 중요도 태그

대표 논문과 클러스터에는 아래 태그 중 하나 이상을 붙인다.

```text
[문제정의] 새 평가축/문제 자체를 만든 논문
[방법전환] 기존 병목을 다른 formulation으로 푼 논문
[인프라] dataset/tool/framework/benchmark를 만든 논문
[경고신호] negative result, failure mode, safety/deployment risk를 드러낸 논문
```

예:
- CXR-ContraBench → `[경고신호]`
- VideoRouter → `[방법전환] [인프라]`
- From Pixels to Tokens → `[방법전환]`
- GA3T → `[인프라]`

### 8.5.5 Confidence와 evidence strength

인사이트마다 confidence를 붙인다.

```text
Confidence: High
근거: 같은 주제 논문 5편 이상 + 서로 다른 기관 + benchmark/dataset 동반

Confidence: Medium
근거: 오늘 2~4편 동시 등장했지만 아직 abstract 기반

Confidence: Low
근거: 흥미로운 단발 논문, 후속 관찰 필요
```

강한 주장과 약한 추측을 같은 문체로 쓰지 않는다.

### 8.5.6 어제/지난주와 달라진 점

Daily에는 가능하면 "어제/지난주와 달라진 점"을 짧게 넣는다.

```text
🧭 어제와 달라진 점
- 어제는 VLA latent substrate였고, 오늘은 VLA execution/reliability로 이동.
- 지난주에는 4D world model 평가가 중심이었고, 오늘은 controllable video generation으로 확장.
```

이 섹션은 매일 보는 독자에게 시간축을 제공한다.

### 8.5.7 Lab action은 1주 실행 protocol까지

추천 연구주제는 아이디어 수준에서 끝내지 않는다. 각 주제마다 가능한 경우 아래를 붙인다.

```text
실행 1주차:
- 대상 논문/코드 3편 clone
- 공통 benchmark: LIBERO + RoboCasa
- 비교축: success rate / latency / failure taxonomy
- 실패해도 남는 결과: negative result 또는 workshop short
```

좋은 연구주제는 "월요일에 학생이 바로 시작할 수 있는 형태"여야 한다.

### 8.5.8 리스크 taxonomy

리스크·한계 필터는 느낌으로 쓰지 말고 유형을 붙인다.

```text
[Metric risk] 수치가 실제 능력을 대표하지 않음
[Dataset risk] 분포가 좁거나 cherry-pick 가능
[Baseline risk] 비교군이 약함
[Deployment risk] latency/cost/safety 누락
[Claim risk] abstract 표현이 본문 증거보다 강함
```

### 8.5.9 Skim-only 후보

좋은 브리핑은 무엇을 읽을지도 말하지만, 무엇을 굳이 깊게 읽지 않아도 되는지도 알려준다.

```text
🧊 Skim-only 후보
- ROI에는 걸리지만 incremental한 논문
- 응용 도메인만 바뀐 논문
- benchmark/claim 확인 전까지 보류할 논문
```

표현은 공격적으로 하지 않는다. "읽지 말라"가 아니라 "깊게 읽기 전 우선순위를 낮춘다"는 의미다.

---

## [9. 논문 요약 품질 계층]

하루에 100편 이상 잡히는 날이 많으므로 모든 논문을 같은 깊이로 쓰지 않는다.

### Tier A — 판을 바꾸는 논문 3~5편
깊게 쓴다.
- 핵심 주장
- 방법의 핵심 수식/아키텍처 또는 직관
- 핵심 실험/벤치마크
- 약점·한계
- 우리 랩 파이프라인 영향
- 중요도 태그 `[문제정의] [방법전환] [인프라] [경고신호]`
- Confidence와 evidence strength

### Tier B — 인사이트 대표 논문 8~12편
3문장 이내로 쓴다.
- 문제
- 기존 방식과 차이
- 왜 오늘/이번주 흐름에서 중요한지
- 어떤 클러스터의 evidence인지

### Tier C — 나머지 ROI 논문
abstract 기반 짧은 요약.
- 초록에 없는 수치나 코드 공개 여부를 지어내지 않는다.
- 불확실하면 "abstract 기준", "본문 확인 필요"라고 명시한다.
- peripheral하면 Skim-only 후보로 표시 가능

### 압축 부록 — 전체 ROI 논문 목록

전체 ROI 논문 목록은 영어 abstract를 그대로 줄이거나 번역투로 붙이지 않는다.
각 논문을 한국어로 재해석해 3~5개 bullet로 작성한다.

각 bullet은 가능한 한 한 줄을 넘기지 않는다.
목표는 "이 논문을 깊게 읽을지 말지 10초 안에 판단"하게 하는 것이다.

필수 bullet:

```text
- 문제: 이 논문이 겨냥한 병목/공백
- 방법: 기존 방식과 다른 핵심 아이디어
- 의미: 왜 이 버킷/클러스터에서 볼 가치가 있는지
```

선택 bullet:

```text
- 근거: abstract에 나온 벤치마크/데이터셋/수치
- 주의: 본문 확인 전 보류할 claim, metric/dataset/baseline/deployment risk
- 우선순위: Must-read / Read / Skim-only
```

금지:
- 영어 abstract 첫 문장을 그대로 복사하거나 직역하지 않는다.
- "성능을 향상했다", "효율적이다" 같은 일반 문장만 쓰지 않는다.
- abstract에 없는 수치, 코드 공개 여부, SOTA claim을 만들지 않는다.
- 모든 논문에 같은 템플릿 문장을 반복하지 않는다.

예시:

```text
TriRelVLA: Triadic Relational Structure for Generalizable Embodied Manipulation [CV/RO] [방법전환] [Read]
- 문제: 기존 VLA가 unseen object/scene에서 appearance와 layout에 과적합됨.
- 방법: object-hand-task 관계를 중간 표현으로 분리해 action prediction에 넣음.
- 의미: VLA 일반화 논점을 모델 크기보다 구조 노출로 옮기는 결.
- 주의: relation extractor 품질과 clutter scene robustness는 본문 확인 필요.
```

---

## [10. Daily 산출물]

`posts/YYYY-MM-DD.html`에 아래 순서로 작성한다.

1. 상단 홈 버튼
2. 메타 정보
3. 오늘의 thesis — 1~2문장 editorial conclusion
4. 🎧 오디오 브리핑 — 있을 때만
5. 🔭 주간 동향
6. 🧭 어제/지난주와 달라진 점
7. 🧩 오늘의 클러스터 + 대표 클러스터 표
8. 📐 CV vs RO 대비
9. 💡 오늘의 인사이트 — 각 항목에 Confidence 포함
10. 🔬 추천 연구주제 — 각 항목에 1주 실행 protocol 포함
11. 🧭 예측 회고 루프 — 월요일만
12. 📊 오늘의 버킷 현황
13. 📈 벤치마크 SOTA 추이 — 있으면
14. 🔀 크로스오버 페어 — 있으면
15. 🌟 오늘의 must-read — Tier A 3~5편 중 1~2편 deep dive
16. ⚠️ 리스크·한계 필터 — risk taxonomy 태그 포함
17. 🧊 Skim-only 후보 — 있으면
18. 📄 부록 — 전체 ROI 논문 압축 목록
19. 🔗 참고 링크 + 하단 홈 버튼

필수 파일:
- `posts/YYYY-MM-DD.html`
- `trends/YYYY-MM-DD.json`
- `benchmarks/YYYY-MM-DD.json`
- `insights/YYYY-MM-DD.json`
- `feed.xml`

---

## [11. Weekly 산출물]

`posts/YYYY-MM-DD-weekly.html`에 아래 순서로 작성한다.

1. 상단 홈 버튼
2. 🗓 Executive Summary
3. 주간 thesis — 이번주 판세를 1~2문장으로 선언
4. 🔭 주간 동향 — RSS 요약 추출을 위해 반드시 이 h2 포함
5. ⚖️ Hot vs Cold
6. 🧩 주간 클러스터 표 — Cluster / Papers / Why / Confidence / Lab action
7. 📐 CV vs RO 키워드
8. 🔥 주간 Top 5 — 각 항목에 중요도 태그
9. 🌟 Deep-dive 1편
10. 🧭 주간 테마 3개 — 각 카드에 `.theme-card` 클래스 사용, confidence 포함
11. 🪞 지난 예측 채점 — 있으면
12. 🔮 다음주 예측
13. 🧊 Skim-only / Watch-only 흐름 — 있으면
14. 🎧 주간 오디오 — 있으면
15. 참고 링크 + 하단 홈 버튼

필수 파일:
- `posts/YYYY-MM-DD-weekly.html`
- `weekly/YYYY-WW.json`
- `trends/YYYY-MM-DD.json`
- `feed.xml`

weekly에서는 `insights/YYYY-MM-DD.json`을 만들지 않는다.

---

## [12. 벤치마크와 인사이트 JSON]

`benchmarks/YYYY-MM-DD.json`:

```json
{
  "date": "YYYY-MM-DD",
  "results": [
    {
      "benchmark": "ObjectNav",
      "metric": "SR",
      "value": 71.2,
      "value_str": "71.2 SR",
      "paper": "https://arxiv.org/abs/....",
      "paper_title": "..."
    }
  ]
}
```

신규 결과가 없으면 빈 배열을 쓴다.

`insights/YYYY-MM-DD.json`:

```json
{
  "date": "YYYY-MM-DD",
  "insights": [
    {"title": "...", "claim": "...", "papers": ["https://arxiv.org/abs/..."]}
  ],
  "research_topics": [
    {"title": "...", "claim": "..."}
  ]
}
```

`weekly/YYYY-WW.json`:

```json
{
  "date": "YYYY-MM-DD",
  "iso_week": "YYYY-WW",
  "week_start": "YYYY-MM-DD",
  "week_end": "YYYY-MM-DD",
  "predictions": [
    {"title": "...", "claim": "...", "rationale": "..."}
  ],
  "themes": [
    {"title": "...", "summary": "..."}
  ],
  "top5": [
    {"title": "...", "arxiv": "https://arxiv.org/abs/..."}
  ]
}
```

---

## [13. RSS와 index 호환]

`scripts/build_feed.py`는 `posts/*.html`에서 다음을 기대한다.
- daily/weekly 모두 `<h1>`이 있어야 한다.
- summary는 `🔭 주간 동향` h2 직후 첫 `<p>`에서 추출된다.

`index.html`은:
- daily 인사이트: `.insight h3`
- weekly 테마: `.theme-card h3`

따라서 weekly HTML에도 반드시:
- `🔭 주간 동향` h2
- `.theme-card h3`

를 포함한다.

---

## [14. TTS 오디오]

가능하면 생성한다.
- Daily: `audio/YYYY-MM-DD.mp3`
- Weekly: `audio/YYYY-MM-DD.mp3`

TTS 실패 시:
- HTML에서 오디오 섹션을 생략하거나 "TTS 환경 미연결" note로 처리한다.
- TTS 실패 때문에 전체 발행을 실패 처리하지 않는다.

---

## [15. Release Gate]

commit/push 전 반드시 확인한다.

```text
Daily:
- posts/YYYY-MM-DD.html 존재
- trends/YYYY-MM-DD.json 존재
- benchmarks/YYYY-MM-DD.json 존재
- insights/YYYY-MM-DD.json 존재
- feed.xml에 posts/YYYY-MM-DD.html 링크 포함

Weekly:
- posts/YYYY-MM-DD-weekly.html 존재
- weekly/YYYY-WW.json 존재
- trends/YYYY-MM-DD.json 존재
- feed.xml에 posts/YYYY-MM-DD-weekly.html 링크 포함

공통:
- JSON 파일이 모두 json.load로 읽힘
- HTML에 h1 존재
- weekly는 '🔭 주간 동향' h2와 .theme-card 존재
- scripts/build_feed.py --check 통과
- git diff --check 통과
- out/, __pycache__ 등 임시 파일은 commit하지 않음
```

---

## [16. GitHub Pages 배포]

```bash
cd {WORKDIR}
python scripts/build_feed.py
git add posts/YYYY-MM-DD.html \
        trends/YYYY-MM-DD.json \
        benchmarks/YYYY-MM-DD.json \
        insights/YYYY-MM-DD.json \
        feed.xml
git commit -m "Add YYYY-MM-DD briefing"
git push origin main
```

Weekly:

```bash
git add posts/YYYY-MM-DD-weekly.html \
        trends/YYYY-MM-DD.json \
        weekly/YYYY-WW.json \
        feed.xml
git commit -m "Add YYYY-MM-DD weekly retrospective"
git push origin main
```

Catch-up:

```bash
git add posts/... trends/... benchmarks/... insights/... weekly/... feed.xml
git commit -m "Add YYYY-MM-DD briefing and YYYY-WW retrospective"
git push origin main
```

push 실패 시 Slack 발송도 스킵한다.

---

## [17. Slack 발송]

push 성공 직후 발송한다.

```text
channel: {SLACK_CHANNEL}
channel_id: {SLACK_CHANNEL_ID}
```

`@channel`/`@here`는 사용자가 명시적으로 요구한 경우에만 쓴다.

### Daily Slack 템플릿

```text
📄 *arXiv Daily Briefing — YYYY-MM-DD (요일)*
주간 시야: YYYY-MM-DD ~ YYYY-MM-DD · cs.CV/new + cs.RO/new
🔗 <{SITE_URL}/posts/YYYY-MM-DD.html|전체 리포트 보기>

📊 *주간 한 줄 요약*
{주간 동향 핵심 3~4줄}

💡 *오늘의 인사이트*
1. {짧은 제목} ({대표 논문})
2. {짧은 제목}
3. {짧은 제목}

🔬 *추천 연구주제*
1. {짧은 제목}
2. {짧은 제목}
3. {짧은 제목}

📊 *버킷 현황*
`[3D] N · [RL] N · [AD] N · [FM] N · [Gen] N · [Eff] N · [Emb] N · [Safety] N`
🔥 TOP3: ...  ❄️ BOTTOM2: ...
```

### Weekly Slack 템플릿

```text
🗓 *arXiv Weekly Retrospective — YYYY-MM-DD (Week WW)*
주간 시야: YYYY-MM-DD ~ YYYY-MM-DD · cs.CV/cs.RO pastweek
🔗 <{SITE_URL}/posts/YYYY-MM-DD-weekly.html|전체 회고 보기>

📌 *Executive Summary*
{3문장}

⚖️ *Hot vs Cold*
⬆ {가속 버킷/테마}  ⬇ {감속 버킷/테마}

🔥 *Top 5*
1. {제목}
2. {제목}
3. {제목}
4. {제목}
5. {제목}

🧭 *주간 테마 3*
· {테마 1} · {테마 2} · {테마 3}

🔮 *다음주 예측*
· {1} · {2} · {3}
```

### Catch-up Slack 템플릿

누락 daily와 weekly를 함께 발행했을 때 사용한다.

```text
🗓 *arXiv Briefing Catch-up — YYYY-MM-DD + Week WW*
🔗 <{SITE_URL}/posts/YYYY-MM-DD.html|누락 daily 보기>
🔗 <{SITE_URL}/posts/YYYY-MM-DD-weekly.html|weekly 보기>

📊 *Daily 핵심*
{daily 핵심 3~4줄}

🗓 *Weekly 핵심*
{weekly 핵심 3~4줄}

💡 *인사이트*
1. {짧은 제목}
2. {짧은 제목}
3. {짧은 제목}

📊 *버킷 현황*
`[3D] N · [RL] N · [AD] N · [FM] N · [Gen] N · [Eff] N · [Emb] N · [Safety] N`
```

---

## [18. 프롬프트 백업 규칙]

공개 repo의 `prompts/`에는 sanitized 버전만 저장한다.

제거/변수화 대상:
- Slack channel id → `{SLACK_CHANNEL_ID}`
- Slack channel name → `{SLACK_CHANNEL}`
- 로컬 작업 경로 → `{WORKDIR}`
- 개인 이메일, 내부 식별자, 비공개 API key

유지 대상:
- GitHub Pages URL
- ROI 버킷
- parser 실행 규칙
- mode resolver
- release gate
- 산출물 스키마

커밋 메시지:

```text
Backup prompt vYYYYMMDD (sanitized)
```

---

## [19. 국문 자연성 게이트]

최종 HTML을 저장하기 직전에 문체 QA를 한 번 더 수행한다. 목표는 "연구자가 실제로 한국어로 말하는 문장"이지, 영어 논문 메모를 한국어 조사만 붙여 옮긴 문장이 아니다.

### 금지/순화 표현

아래 표현은 그대로 쓰지 않는다.

- "정조준" → "직접 다룬다", "문제로 삼는다", "짚는다"
- "표면화" → "드러났다", "같이 나왔다", "분명해졌다"
- "batch" → "오늘 하루치", "같은 날 나온 논문들", "이번 묶음"
- "압력이 걸려 있다" → "비중이 커졌다", "필요성이 커졌다", "실험 수요가 보인다"
- "paradigm" → "연구 흐름", "문제 설정", "접근 방식"
- "substrate" → "기반 구조", "토대", "표현 기반"
- "audit" → "점검", "검증", "확인"
- "layer" → "층위", "단계", "부분"
- "측 결", "응용 결" → "쪽 논문", "응용 논문", "관찰점"
- "개별 처방", "각자 처방" → "각각의 약점을 하나씩 고치는 흐름", "문제별 해결책이 따로 나오던 단계"
- "처방" 단독 사용은 되도록 피하고, 실제로 무엇을 고치는지 쓴다. 예: "메모리 부족을 줄이는 방법", "새 명령을 못 따라가는 문제를 고치는 방법"

### 문장 QA 규칙

1. 한 문단에 영어식 명사구가 2개 이상 이어지면, 적어도 하나는 한국어 동사 문장으로 풀어쓴다.
2. "A와 B가 한 batch에 표면화"라고 쓰지 말고, "A와 B가 같은 날 같이 나왔다는 점이 중요합니다"처럼 말한다.
3. "실험적인 압력"처럼 한국어 독자가 바로 이해하기 어려운 추상 표현은 금지한다. "실제 로봇 실험과 배포에 가까운 단어가 더 자주 보입니다"처럼 관찰 가능한 말로 바꾼다.
4. 논문별 부록의 `문제/방법/의미` 불릿도 같은 게이트를 적용한다. 내부 메모체를 보존하지 말고, 교수에게 구두로 설명해도 어색하지 않은 문장으로 재작성한다.
5. survey나 taxonomy 논문을 묶을 때 `failure mode catalog`, `unified mapping`, `data infrastructure bottleneck` 같은 라벨만 나열하지 않는다. 각 라벨이 실제로 무슨 현상을 뜻하는지 한 문장씩 풀어 쓴다.
6. "처방", "단계", "프레임" 같은 추상어를 쓰면 반드시 앞뒤에 구체 예시를 붙인다. 예: "메모리 부족, 의도 파악 실패, 안전 문제처럼 각각의 약점을 하나씩 고치는 단계".
7. 저장 전 `정조준|표면화|batch|압력이 걸려|paradigm|substrate|audit|측 결|응용 결|개별 처방|각자 처방|catalog 단계|통합 매핑|진짜 bottleneck` 문자열 검색을 수행하고, 논문 제목이나 고유명사가 아닌 본문 매치는 수정한다.

### 압축어 해설 게이트

핵심 주장 문장은 "전문가가 보면 대충 아는 말"이 아니라 "처음 보는 독자도 되물을 필요가 없는 말"이어야 한다. 특히 thesis, 클러스터 표의 `왜 중요?`, 인사이트 첫 문단에는 아래 규칙을 적용한다.

1. `A → B` 형태의 변화 주장은 반드시 "예전에는 무엇을 봤고, 이제는 무엇을 보게 됐는지"로 풀어쓴다.
2. `reconstruction loss → reward alignment + interactive eval`처럼 압축된 표현은 그대로 끝내지 않는다.
   - 나쁜 예: "World Model 평가가 reconstruction loss에서 reward alignment + interactive eval로 전환입니다."
   - 좋은 예: "예전에는 World Model을 미래 영상을 얼마나 그럴듯하게 예측하느냐로 평가했는데, 이제는 그 예측이 로봇 행동 성공에 도움이 되는지와 상호작용 상황에서 계속 쓸 수 있는지를 더 묻기 시작했다는 뜻입니다."
3. `latent action supervision`, `world model`, `alignment`, `controllability`, `benchmark` 같은 용어는 첫 등장 문단에서 직관을 붙인다.
4. 핵심 요약은 "문제 → 바뀐 기준/방법 → 왜 중요한지" 순서로 쓴다. 기술어 나열은 이 순서를 대체할 수 없다.
5. 독자가 "그래서 그게 무슨 말인데?"라고 되물을 만한 문장이 보이면 실패로 간주하고 다시 쓴다.

### 독자 친절성 게이트

전문어를 없애는 것이 목표가 아니다. 전문어를 쓰되, 독자가 그 단어를 모른다고 해도 문맥을 따라올 수 있게 "무슨 현상인지"와 "왜 중요한지"를 같이 열어준다. 특히 `개별 처방`, `실패 유형 정리`, `인프라 병목`, `평가축 전환`처럼 요약자 머릿속에서는 편한 말이지만 독자에게는 다시 해석을 요구하는 표현을 조심한다. thesis, 클러스터 표의 `왜 중요?`, 인사이트 첫 문단, 추천 연구주제 첫 문단은 아래 4단계를 되도록 모두 포함한다.

1. **라벨**: 논문들이 묶이는 이름을 짧게 붙인다. 예: VLA lock-in, data bottleneck, controllable video generation.
2. **현상 설명**: 그 라벨이 실제로 무엇을 뜻하는지 구체적인 행동/실패/평가 상황으로 풀어쓴다.
3. **근거 연결**: 어떤 논문들이 각각 어떤 조각을 보여주는지 2~3개만 연결한다.
4. **판단/영향**: 그래서 연구자가 내일부터 무엇을 다르게 봐야 하는지 말한다.

다음 문장 패턴은 금지한다.

```text
A가 X를 명명하고, B가 Y를 통합 매핑하며, C가 Z bottleneck을 클레임. 커뮤니티가 catalog 단계에 진입.
```

이런 문장은 정보가 많은 것처럼 보이지만 독자에게는 "그래서 무슨 일이 일어난 건데?"만 남긴다. 반드시 아래처럼 바꾼다.

```text
A는 모델이 어떤 상황에서 어떻게 실패하는지를 이름 붙인 논문입니다.
B는 그 실패가 안전 문제로 이어지는 경로와 평가 방법을 정리합니다.
C는 같은 문제를 모델 구조가 아니라 데이터 수집·정리·평가 파이프라인의 병목으로 봅니다.
그래서 오늘 흐름은 새 알고리즘 하나보다, 이 분야가 실패 유형과 인프라 병목을 체계적으로 정리하기 시작했다는 쪽에 가깝습니다.
```

### 문장 자체 점검 질문

최종 저장 전 핵심 문단마다 아래 질문을 던진다. 하나라도 "아니오"면 다시 쓴다.

1. 이 문장을 읽은 사람이 핵심 용어를 몰라도 대략 무슨 현상인지 알 수 있는가?
2. 논문 제목 3개를 나열하지 않고도 묶음의 공통 문제가 드러나는가?
3. "어제/기존 방식과 무엇이 달라졌는지"가 한국어 문장으로 설명됐는가?
4. "이게 우리 랩/독자에게 왜 중요한지"가 마지막에 판단으로 붙어 있는가?
5. 영어 명사구가 문장의 주된 정보 전달을 대신하고 있지 않은가?

### 압축어 해설 few-shot

아래 예시의 "좋은 예" 수준으로 풀어쓴다. 제목·thesis·클러스터 설명·인사이트 첫 문단에서 특히 중요하다.

**예시 1 — World Model 평가**

나쁜 예:
```text
World Model 평가가 reconstruction loss → reward alignment + interactive eval로 전환입니다.
```

좋은 예:
```text
예전에는 World Model을 "미래 영상을 얼마나 그럴듯하게 복원하거나 예측하느냐"로 많이 평가했는데,
이제는 "그 예측이 로봇 행동 성공에 실제로 도움이 되느냐"와
"상호작용 상황에서 계속 쓸 수 있느냐"가 더 중요해지고 있다는 뜻입니다.
```

**예시 2 — Latent Action Supervision**

나쁜 예:
```text
VLA의 latent action supervision이 image-based vs action-based formulation-task correspondence를 처음 정량화했습니다.
```

좋은 예:
```text
VLA를 학습시킬 때 행동을 그대로 맞히게 할지, 아니면 이미지 변화 속에 숨어 있는 행동 단서를 먼저 배우게 할지의 차이를
본격적으로 비교하기 시작했다는 뜻입니다. 쉽게 말하면 "로봇에게 정답 행동을 외우게 할 것인가,
장면이 어떻게 변해야 하는지를 먼저 이해하게 할 것인가"를 나눠 보기 시작한 겁니다.
```

**예시 3 — Controllable Video Generation**

나쁜 예:
```text
Video generation의 평가축이 visual quality에서 controllability와 latency로 이동했습니다.
```

좋은 예:
```text
예전에는 생성된 영상이 얼마나 그럴듯하고 예쁜지를 주로 봤다면,
이제는 원하는 카메라 경로와 움직임을 얼마나 안정적으로 조종할 수 있는지가 중요해졌습니다.
즉 "보기 좋은 샘플"보다 "실제로 원하는 장면을 만들 수 있는 도구인가"를 묻는 쪽으로 평가 기준이 바뀌는 겁니다.
```

**예시 4 — Diffusion Alignment**

나쁜 예:
```text
Diffusion alignment가 BT preference model에서 game-theoretic self-referential alignment로 이동했습니다.
```

좋은 예:
```text
diffusion 모델을 사람 취향에 맞추는 방식이 단순한 선호도 점수 맞추기에서 벗어나고 있다는 뜻입니다.
이제는 모델이 여러 후보를 서로 비교하고, 스스로 더 나은 방향을 찾게 만드는 쪽으로
평가와 학습 방식이 옮겨가고 있습니다.
```

**예시 5 — Benchmark / SOTA**

나쁜 예:
```text
LoViF가 4D World Model holistic QA benchmark를 제안했습니다.
```

좋은 예:
```text
4D World Model을 볼 때 단순히 영상이 예쁜지보다,
시간에 따라 물리적으로 말이 되는지와 입력 조건을 잘 따르는지를 함께 평가하려는 흐름입니다.
즉 "그럴듯한 동영상"이 아니라 "물리적으로 믿을 수 있는 시뮬레이션"인지 묻는 쪽으로 가고 있습니다.
```

**예시 6 — Survey / Catalog / Bottleneck**

나쁜 예:
```text
오늘은 Lock-in이 새 failure mode를 명명하고, VLA Safety Survey가 threats·challenges·evaluations·mechanisms를 통합 매핑하며,
VLA Data Survey가 'data infrastructure가 진짜 bottleneck' 클레임. VLA community가 개별 시도들의 catalog 단계에 진입한 신호.
```

좋은 예:
```text
어제까지는 VLA 논문들이 memory, intent, safety 같은 문제를 각각 따로 고치는 분위기였다면,
오늘은 그 문제들이 왜 생기고 어떻게 분류되는지를 정리하는 쪽으로 넘어갔습니다.
Lock-in은 적은 데모로 VLA를 추가학습했을 때 새 명령을 잘 못 따라가고 예전에 본 행동만 반복하는 현상을 이름 붙였고,
VLA Safety Survey는 어떤 위협을 걱정해야 하는지와 어떻게 평가·방어할지를 한 장의 지도처럼 묶습니다.
VLA Data Survey는 성능을 막는 병목이 모델 구조 하나가 아니라 데이터 수집·정리·벤치마크 파이프라인에 있다고 봅니다.
```
