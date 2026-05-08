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

## [9. 논문 요약 품질 계층]

하루에 100편 이상 잡히는 날이 많으므로 모든 논문을 같은 깊이로 쓰지 않는다.

### Tier A — must-read 1~2편
깊게 쓴다.
- 핵심 주장
- 방법의 핵심 수식/아키텍처 또는 직관
- 핵심 실험/벤치마크
- 약점·한계
- 우리 랩 파이프라인 영향

### Tier B — 인사이트 대표 논문 8~12편
3문장 이내로 쓴다.
- 문제
- 기존 방식과 차이
- 왜 오늘/이번주 흐름에서 중요한지

### Tier C — 나머지 ROI 논문
abstract 기반 짧은 요약.
- 초록에 없는 수치나 코드 공개 여부를 지어내지 않는다.
- 불확실하면 "abstract 기준", "본문 확인 필요"라고 명시한다.

---

## [10. Daily 산출물]

`posts/YYYY-MM-DD.html`에 아래 순서로 작성한다.

1. 상단 홈 버튼
2. 메타 정보
3. 🎧 오디오 브리핑 — 있을 때만
4. 🔭 주간 동향
5. 📐 CV vs RO 대비
6. 💡 오늘의 인사이트
7. 🔬 추천 연구주제
8. 🧭 예측 회고 루프 — 월요일만
9. 📊 오늘의 버킷 현황
10. 📈 벤치마크 SOTA 추이 — 있으면
11. 🔀 크로스오버 페어 — 있으면
12. 🌟 오늘의 must-read
13. ⚠️ 리스크·한계 필터 — 있으면
14. 📄 논문별 요약
15. 🔗 참고 링크 + 하단 홈 버튼

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
3. 🔭 주간 동향 — RSS 요약 추출을 위해 반드시 이 h2 포함
4. ⚖️ Hot vs Cold
5. 📐 CV vs RO 키워드
6. 🔥 주간 Top 5
7. 🌟 Deep-dive 1편
8. 🧭 주간 테마 3개 — 각 카드에 `.theme-card` 클래스 사용
9. 🪞 지난 예측 채점 — 있으면
10. 🔮 다음주 예측
11. 🎧 주간 오디오 — 있으면
12. 참고 링크 + 하단 홈 버튼

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
