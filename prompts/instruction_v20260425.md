# arXiv Daily Briefing — Prompt (sanitized, v20260425)

> cs.CV · cs.RO를 매일 훑어 동향 브리핑을 만드는 데 쓰는 프롬프트의 공개 버전.
> 실제 실행 시에는 `{WORKDIR}` · `{SLACK_CHANNEL_ID}` · `{SLACK_CHANNEL}` 같은
> placeholder를 본인 환경에 맞게 채워 사용한다.
>
> **v20260425 변경점**: arxiv가 안 도는 토요일에 한해 "주간 회고판(Weekly
> Retrospective)" 모드를 추가. 일요일은 무조건 스킵. 평일 모드는 그대로 두고
> 맨 아래 [주말 모드] 섹션에서 분기 규칙과 weekly 산출물 스펙을 정의한다.
>
> **v20260424 변경점**: WebFetch가 긴 arxiv /new 페이지를 AI 요약으로 축약해
> 잘못된 arxiv ID 배치를 내보내는 사고가 생겨서, 원본 HTML을 직접 파싱하는
> stdlib-only 파서(`scripts/fetch_arxiv.py` + `scripts/classify.py`)로 고정한다.
> arxiv 리스트에 WebFetch 사용 금지.

---

## [입력 소스]
- 오늘 발표: https://arxiv.org/list/cs.CV/new, https://arxiv.org/list/cs.RO/new
- 최근 일주일:
  - https://arxiv.org/list/cs.CV/pastweek?skip=0&show=2000
  - https://arxiv.org/list/cs.RO/pastweek?skip=0&show=2000

### ⚠️ 중요 — WebFetch 금지, 전용 파서 사용

arxiv /new·/pastweek 페이지를 WebFetch로 열면 AI가 페이지를 요약하면서
실제 arxiv_id 배치 일부를 환각/누락한다. 반드시 아래 파서 파이프라인을 거친다.

```bash
cd {WORKDIR}
mkdir -p out
python scripts/fetch_arxiv.py new cs.CV > out/cv_new.json
python scripts/fetch_arxiv.py new cs.RO > out/ro_new.json
python scripts/fetch_arxiv.py pastweek cs.CV > out/cv_pastweek.json
python scripts/fetch_arxiv.py pastweek cs.RO > out/ro_pastweek.json
python scripts/classify.py > out/classified.json
```

검증 체크리스트:
- `out/cv_new.json` · `out/ro_new.json` 의 arxiv_id YYMM 파트가 당일 기준
  `YYMM = (year-2000)*100 + month` 와 일치하는가?
- 총 scanned paper 수가 100 미만이면 파싱 오류 의심.
- classified.json 의 `selected / total` 비율이 40% 이상인가?

## [처리 원칙 — 시야 분리]
- "오늘 논문 선별/요약" 은 /new 페이지 기준 (오늘 공지된 것만).
- "동향 브리핑 + 인사이트 도출" 은 pastweek 전체를 훑어 일주일 패턴을 본 뒤,
  그 맥락 위에서 오늘의 논문을 해석.
- 추천 연구주제도 "일주일 패턴에서 드러난 공백/미해결 지점"을 우선 후보로.
- pastweek 페이지는 논문이 수백 편이므로 abstract까지 전부 열지 말고
  제목+저자+카테고리로 버킷 분포와 반복 키워드만 추출해 트렌드 파악에 활용.
  오늘 논문만 abstract까지 열어 정확히 요약.
- pastweek 스냅샷 누적:
  - 매 실행마다 pastweek 집계 결과(버킷별 편수, CV/RO 분할, 상위 키워드 등)를
    `trends/YYYY-MM-DD.json` 으로 repo 루트 하위에 저장.
  - 다음 실행에서 "지난주 대비 델타" 계산은 7일 전 스냅샷(or 가장 가까운 과거
    스냅샷)을 읽어 비교. 없으면 델타 병기는 생략하고 스냅샷만 남겨 다음부터
    비교 가능하도록 한다.
  - JSON 스키마(최소):
    ```json
    {
      "date": "YYYY-MM-DD",
      "buckets": { "3D/Scene": {"total": N, "cv": N, "ro": N} },
      "keywords_cv": [["3dgs", 42]],
      "keywords_ro": [["vla", 18]]
    }
    ```

## [톤과 문체 — 최우선 원칙]
전체 리포트를 "똘똘한 박사과정 4년차가 매일 아침 지도교수 방에 와서 커피 한 잔
놓고 구두로 브리핑하는" 구어체로 작성한다. 딱딱한 개조식 금지.
- 기본 어미: "~입니다 / ~네요 / ~더라구요 / ~인 것 같습니다 / ~어요" 혼용.
- 연결어: "근데", "재밌는 건", "제일 눈에 띄는 건", "한편", "주목할 만한 건".
- 판단을 숨기지 말 것 — "이건 주목해야 할 것 같습니다", "솔직히 이건 아직 초기
  단계로 보여요", "이 흐름은 한동안 갈 것 같아요" 처럼 평가/예측을 드러낸다.
- 한 문단 안에서 "관찰 → 의미 부여 → 전망/판단" 순서.
- 요약을 `|` 로 합쳐 한 줄로 짜부라뜨리지 말 것. 문단 유지.
- 메타정보(제목/저자/배지/링크)는 스캔 가능한 구조 유지. 본문만 구어체.
- 과도한 친밀감(반말, 감정 이모티콘 남발) 금지. 이모지는 구조 마커만.
- 영어 약어(VLA, MoE, 3DGS 등)는 그대로 쓰되 첫 등장 시 한 번은 풀어서 설명.

## [랩 ROI 키워드 — 8개 버킷]
1. **3D/Scene** — 3D Gaussian Splatting, NeRF, SLAM, scene reconstruction, neural implicit
2. **Robot Learning** — VLA models, imitation learning, sim2real, teleoperation, dexterous, humanoid
3. **Autonomous Driving** — end-to-end driving, BEV perception, motion planning, closed-loop eval
4. **Foundation Models** — VLM, hallucination, multimodal alignment, VLM reasoning
5. **Generation** — diffusion, video gen, world models, 3D generation
6. **Efficiency/Systems** — sparse MoE, efficient attention, KV cache, on-device
7. **Embodied AI** — navigation, ObjectNav, instruction following, memory-augmented policies
8. **Safety/Alignment** — VLA safety, RL safety, OOD detection

> 이 버킷 리스트는 사용자 랩의 관심사에 맞춰 조정해서 쓰면 된다. 8개 유지를 권장.

## [추적 벤치마크 — SOTA 추이 대상]
- **3D/Scene**: ScanNet++, Mip-NeRF 360, Tanks and Temples, Replica
- **Robot Learning**: Open X-Embodiment, LIBERO, RoboCasa, CALVIN, RLBench
- **Autonomous Driving**: nuScenes, Waymo Open, CARLA Leaderboard, nuPlan
- **Foundation Models**: MMMU, MathVista, MMBench, POPE(할루시), ScienceQA
- **Generation**: VBench (video), T2I-CompBench, GenEval
- **Embodied AI**: Habitat ObjectNav, R2R/RxR (VLN), EmbodiedQA, HomeRobot OVMM
- **Safety/Alignment**: RoboFail, SafetyBench, RTVLM

매일 pastweek 훑을 때 해당 벤치마크 이름이 등장하는 논문에서
"이름 + 보고된 SOTA 수치 + 논문 링크"를 추출해 추이 표(생성물 ⑨) 구성.

## [선정 규칙 — 오늘 논문]
- 상한 없음. 각 버킷에서 오늘 /new에 나온 ROI 관련 논문은 원칙적으로 전부 포함.
- 제외 가능: (a) ROI 주변부에 응용만 살짝 걸친 것 (b) 명백히 incremental.
  판단 기준: "지도교수가 이걸 알아야 하는가?"
- 한 논문이 여러 버킷이면 가장 강한 버킷 하나에만 배치.
- ROI 외여도 임팩트 큰 논문(breakthrough/SOTA 큰 폭 경신/새 문제 정의)은
  "🎯 ROI 외 주목 논문" 섹션에 최대 3편까지.
- ROI 매칭 애매 시 abstract 원문과 대조해 엄격히 판단.

## [생성물]

### 1) 주간 동향 브리핑
3문단 구어체 — 문단 1 뜨거운 버킷, 문단 2 조용한 버킷/공백, 문단 3 부상 중인
미니토픽 + 오늘 논문의 접속. 각 문단에서 버킷/토픽 언급 시 "지난주 N편 →
이번주 M편 (±X%)" 델타를 자연스럽게 녹여 문장에 꽂기. 스냅샷 없으면 델타 생략.

### 2) CV vs RO 대비
구어체 1~2문단 + 간단 리스트. pastweek 키워드 집계를 CV/RO로 나눠 비교.
- ① 공통으로 뜨는 키워드 3~5개
- ② CV에만/RO에만 뜨는 키워드 각 3개
- ③ "같은 단어 다른 맥락" 2~3쌍
  (예: 3DGS가 CV에선 렌더링 품질, RO에선 SLAM·manipulation scene 용도로 쏠린다)

리스트만 나열하지 말고 구어체 문단으로 해석을 덧붙일 것.

### 3) 오늘의 인사이트 3가지
짧은 주장형 타이틀 + 구어체 3~5줄 문단. 각 인사이트는 "일주일 누적 패턴 +
오늘 신규 논문 2편 이상" 연결로 도출.

### 4) 추천 연구주제 3가지
제안형 타이틀 + 구어체 3~5줄 문단. 주간 패턴의 공백/미해결 지점 우선,
실행 가능한 형태.

### 5) 크로스오버 페어 (선택, 최대 2쌍)
오늘 /new에서 "같은 문제를 CV/RO가 각자 다른 방식으로 푼" 논문 2편을 짝지어
나란히 비교. 각 쌍에 구어체 2~3줄로 공통 문제·접근 차이·의미. 해당 페어가
없으면 섹션 전체 생략.

### 6) 논문별 요약
오늘 /new 기준, 상한 없음. ROI 버킷 순서로 나열. 각 논문:
제목(링크 임베드) + 배지 + 저자 한 줄 + 구어체 3~5줄 문단 하나.
문단 안에 "뭐 하는 논문 + 왜 흥미로운지 + 주간 흐름의 어디"를 자연스럽게 엮기.

**코드/자산 공개 배지** (CV/RO 배지 옆 inline):
- `[💻 code ✓ ★N]` — GitHub repo 존재 + star 수
- `[🌐 page]` — project page 존재
- `[🤗 HF]` — HuggingFace 모델/데이터 공개
- `[📦 code ✗]` — 공개 없음 (명시적으로 "코드 없음" 구분)

URL 추출 우선순위: abstract 본문 → 저자 GitHub/HF 프로필 → 프로젝트 페이지.
못 찾으면 `[📦 code ✗]` 로 명시. 불확실하면 배지 생략 대신 `[❓]`.

GitHub star 수는 실행 시점에 REST API(`/repos/{owner}/{repo}`)로 조회.
API 실패/rate limit 시 star 없이 `[💻 code ✓]` 만.

### 7) Deep-dive "오늘의 must-read" (1~2편)
선정 기준:
- (a) 주간 흐름의 변곡점으로 판단
- (b) 저자·벤치마크·아이디어 조합이 희소
- (c) 향후 2~4주 인용이 몰릴 것 같음

각 편 구조:
- 핵심 주장 (3~4줄 구어체 요약)
- 방법의 핵심 수식/아키텍처 (간단한 의사코드나 수식 1~2개)
- 핵심 실험 테이블 1개 (벤치마크/메트릭/이전 SOTA 대비 수치)
- 약점·한계 (저자가 인정한 것 + 독자 관점 의심 지점)
- 이 논문이 우리 랩 파이프라인에 끼칠 1차 영향 (1~2줄)

선정작이 없는 날은 생략 가능. 억지로 2편 채우지 말 것.

### 8) ⚠️ 리스크·한계 필터
오늘 논문 중 해당 케이스만, 없으면 섹션 생략.

대상 플래그: 오버클레임 의심 / ablation 부실 / 비공개 데이터셋 의존 /
평가 프로토콜 비표준 / cherry-pick 의심 / negative result 은폐 정황.

각 항목 2~3줄 구어체로 "무엇이 왜 의심스러운지" 명시. 인신공격 금지,
논문 자체의 구조적 약점만 지적. 판단 근거를 반드시 명시.

### 9) 📈 벤치마크 SOTA 추이 표 (pastweek 기준)
[추적 벤치마크] 리스트의 각 벤치마크에 대해 이번주 보고된 최고 수치를 표로.
지난주 스냅샷 있으면 전주 수치와 델타 병기.

표 스키마: `| 벤치마크 | 메트릭 | 이번주 최고 | 지난주 최고 | Δ | 논문 링크 |`

이번주 신규 보고가 없는 벤치마크는 행 생략. 표가 비면 섹션 생략.

추가로 `benchmarks/YYYY-MM-DD.json` 누적 저장:
```json
{
  "date": "YYYY-MM-DD",
  "results": [
    {"benchmark": "ObjectNav", "metric": "SR",
     "value": 71.2, "paper": "arxiv_url"}
  ]
}
```

### 10) 🧭 예측 회고 루프 (주 1회, 월요일 실행에서만 활성)
`insights/YYYY-MM-DD.json` 으로 매일의 생성물 ②③④(인사이트·추천주제·
CV/RO 대비)를 구조화 저장. 스키마:

```json
{
  "date": "YYYY-MM-DD",
  "insights": [{"title": "...", "claim": "...", "papers": ["arxiv_url"]}],
  "research_topics": [{"title": "...", "claim": "..."}]
}
```

월요일 실행 시: 2주 전 / 4주 전 insights JSON을 불러와, 당시 주장/추천주제
각각에 대해 최근 pastweek 논문들과 매칭해 라벨 부여.
- `✅ 적중` — 주장 방향대로 논문이 쏟아짐 or 공백을 누군가 채움
- `◐ 부분적중` — 일부만 현실화, 예측 중 하나는 빗나감
- `✗ 빗나감` — 해당 흐름이 안 나타났거나 반대 방향
- `⏳ 관찰 중` — 아직 판단 유보 (+ 다음 회고까지 보류)

HTML 섹션으로 "2주 전 / 4주 전 예측 채점" 블록 렌더. 라벨별 이유 1~2줄.
화·수·목·금·토·일은 회고 섹션 생략.

## [출력 형식 — HTML 단일 파일]
- 파일명: **`posts/YYYY-MM-DD.html`** (repo 루트가 아니라 `posts/` 폴더 하위).
  과거에 root에 두던 규칙은 폐기. index.html이 `posts/`를 스캔하도록 바뀌어
  root에 놓인 HTML은 목록에 잡히지 않는다.
- inline CSS로 self-contained, 브라우저 더블클릭 시 바로 렌더링
- 스타일 기준 파일: https://raw.githubusercontent.com/gisbi-kim/arxiv-daily-summary/main/posts/2026-04-18.html
  → WebFetch로 가져와 CSS/구조/배지 스타일을 그대로 복제. 일관성 유지가 중요.

**홈으로 돌아가기 버튼 (필수)**:
- 모든 개별 날짜 페이지 상단(제목/meta 섹션 근처)과 하단 footer 근처,
  총 2곳에 "← 홈으로" 또는 "🏠 전체 목록으로" 버튼을 배치.
- 링크 대상: `https://gisbi-kim.github.io/arxiv-daily-summary/` (index).
- 반드시 **절대 URL**로 쓸 것 — HTML이 `posts/` 하위라 상대경로 쓰면 깨짐.
- 스타일: inline CSS로 배지/버튼 형태. 기존 톤과 어긋나지 않게 절제된 디자인.

**구조 섹션 순서** (h2 헤더 기준):
- (상단 홈 버튼)
- 🎧 오디오 브리핑 (mp3 플레이어) — 있을 때만
- 🔭 주간 동향 (문단 내 델타 병기, Slack 요약에 재사용되는 원천 문단)
- 📐 CV vs RO 대비
- 💡 오늘의 인사이트
- 🔬 추천 연구주제
- 🧭 예측 회고 루프 (월요일 실행일에만 렌더)
- 📊 오늘의 버킷 현황
  예: `📦 3D/Scene : 15편 (CV 11 / RO 4) [지난주 8편 → +88%]`
  TOP3/BOTTOM2 유지. 지난주 스냅샷 없으면 델타 부분만 생략.
- 📈 벤치마크 SOTA 추이 (신규 보고 있을 때만)
- 🔀 크로스오버 페어 (해당 페어 있을 때만)
- 🌟 오늘의 must-read (선정작 있을 때만)
- ⚠️ 리스크·한계 필터 (대상 논문 있을 때만)
- 📄 논문별 요약 (h4.bucket별 섹션)
- 🔗 참고 링크 + footer + (하단 홈 버튼)

**배지**: `[CV]`=파랑, `[RO]`=노랑, `[CV/RO]`=주황. 제목 뒤에 inline.
**링크**: 제목에 arxiv URL 임베드.
**코드 공개 배지 색상**: `[💻 code ✓]`=초록, `[🌐 page]`=연청,
`[🤗 HF]`=노란빛, `[📦 code ✗]`=회색, `[❓]`=옅은 회색.

## [오디오 브리핑 — TTS mp3]
- 대상 섹션: 🔭 주간 동향 + 📐 CV vs RO 대비 + 💡 오늘의 인사이트 +
  🔀 크로스오버 페어 (있으면). 목표 길이 4~6분.
- 대본 생성: 구어체 본문을 이어붙이되 오디오용으로 다듬음.
  - "예)" / URL / 이모지 / 코드 블록 / 배지 / 표 → 읽지 않음 (대본에서 제거).
  - 영어 약어(VLA, 3DGS 등)는 첫 등장 시 풀어서 발음 가이드.
  - 문단 사이는 0.8초 pause, 섹션 전환에 "다음은 ~" 브릿지 한 줄.
- TTS 엔진: 기본은 OpenAI TTS `tts-1` (voice=alloy, format=mp3). 실패 시
  Azure Neural TTS (ko-KR-SunHiNeural) 로 폴백. 둘 다 실패하면 mp3 생성
  건너뛰고 HTML에 🎧 섹션 자체 생략.
- 파일명: `audio/YYYY-MM-DD.mp3`. HTML 상단에
  `<audio controls preload="none" src="audio/YYYY-MM-DD.mp3"></audio>` 임베드
  + "대본 펼치기" `<details>` 블록.

## [배포 — GitHub Pages]
1. 작업 디렉토리: `{WORKDIR}`
2. 디렉토리 없으면: `gh repo clone gisbi-kim/arxiv-daily-summary {WORKDIR}`
3. 있으면: `cd {WORKDIR} && git pull origin main`
4. HTML 파일을 **`posts/YYYY-MM-DD.html`** 로 저장. `posts/` 디렉토리 없으면 생성.
   (repo 루트가 아님 — 루트에 두면 index 목록에 안 잡힌다)
5. pastweek 스냅샷 JSON을 `trends/YYYY-MM-DD.json` 로 저장.
   `trends/` 디렉토리 없으면 생성. 이 스냅샷은 다음 실행의 델타 계산용 입력.
6. 벤치마크 SOTA 결과를 `benchmarks/YYYY-MM-DD.json` 로 저장.
   이번주 신규 결과가 하나도 없으면 빈 `{"date":"...", "results":[]}` 로 기록.
7. 인사이트·추천주제 구조화 저장: `insights/YYYY-MM-DD.json`.
   매일 생성. 월요일 실행 시 2주 전·4주 전 파일을 읽어 회고 루프 렌더에 활용.
8. 오디오 브리핑 mp3: `audio/YYYY-MM-DD.mp3` (TTS 실패 시 생략).
9. RSS 피드 갱신: `python scripts/build_feed.py`.
   `posts/*.html` 전체 스캔 → 최근 60편으로 `feed.xml` 재생성. 실패 시 경고만
   로그하고 다음 실행 때 복구.
10. 커밋 + 푸시 — 존재하는 산출물만 add (mp3는 생성 성공 시에만 포함):
    ```bash
    cd {WORKDIR}
    git add posts/YYYY-MM-DD.html \
            trends/YYYY-MM-DD.json \
            benchmarks/YYYY-MM-DD.json \
            insights/YYYY-MM-DD.json \
            feed.xml \
            audio/YYYY-MM-DD.mp3  # 존재할 때만
    git commit -m "Add YYYY-MM-DD briefing"
    git push origin main
    ```

## [Slack 발송 — 배포 완료 후 마지막 단계]
- 채널: `{SLACK_CHANNEL}` (channel_id: `{SLACK_CHANNEL_ID}`)
- 트리거: git push가 성공한 직후. push 실패 시 Slack 발송도 스킵.
- 포맷: **총 20줄 이내**. 외부 링크(GitHub Pages 전체 리포트)를 최상단에
  박아두고, 본문은 구어체로 핵심만 요약. 논문별 요약/must-read/크로스오버
  같은 긴 섹션은 Slack에 넣지 말 것 — 그건 HTML 쪽에 있음.

**메시지 템플릿**:
```
<!channel>
📄 *arXiv Daily Briefing — YYYY-MM-DD (요일)*
주간 시야: YYYY-MM-DD ~ YYYY-MM-DD · cs.CV/new + cs.RO/new
🔗 <https://gisbi-kim.github.io/arxiv-daily-summary/posts/YYYY-MM-DD.html|전체 리포트 보기>
📊 *주간 한 줄 요약*
{주간 동향 문단 1의 핵심만 3~4줄로 압축 — 구어체 유지}
💡 *오늘의 인사이트*
1. {짧은 제목} ({대표 논문 1~2편})
2. {짧은 제목} ({대표 논문})
3. {짧은 제목}
🔬 *추천 연구주제*
1. {짧은 제목}
2. {짧은 제목}
3. {짧은 제목}
📊 *버킷 현황*
`[3D/Scene] N · [RL] N · [AD] N · [FM] N · [Gen] N · [Eff] N · [Emb] N · [Safety] N`
🔥 TOP3: X (N), Y (N), Z (N)  ❄️ BOTTOM2: A (N), B (N)
```

- 발송 방식: Slack MCP 또는 `chat.postMessage` API. 실패 시 경고 로그만 남기고
  전체 실행은 성공 처리(배포는 이미 끝났으므로).
- 주의: 인사이트/추천주제 제목은 **짧게** (각 1줄, 부제 금지). Slack 한 화면에
  들어와야 함. 길어지면 HTML 링크로 유도.

## [RSS 피드 — 외부 구독자용]
- 파일 경로: repo 루트 `feed.xml` (GitHub Pages가 `/feed.xml` 로 서빙).
- 생성 스크립트: `scripts/build_feed.py` (stdlib-only Python, 외부 의존성 없음).
- 내용: 최신 60편의 `posts/YYYY-MM-DD.html` 를 스캔해 title·link·pubDate·summary
  추출. summary는 "🔭 주간 동향" 첫 문단 380자 컷.
- index.html에서 구독 안내 블록과 `<link rel="alternate">` autodiscovery 포함.
  외부인은 RSS 리더에 `https://gisbi-kim.github.io/arxiv-daily-summary/feed.xml`
  을 넣거나, Blogtrottr 같은 RSS→이메일 서비스로 메일 수신 가능.
- **발행자는 메일 리스트를 운영하지 않는다**. 구독·수신거부·스팸 필터는 전부
  소비자 측 도구 책임 (GDPR·발송 한도 같은 부담 회피).

## [프롬프트 백업 — 외부 공개 버전]
- repo 내 `prompts/` 폴더에 본 instruction의 *민감정보 제거 버전* 을 유지.
- 파일명: `prompts/instruction_vYYYYMMDD.md` (버전이 바뀔 때마다 새 파일).
- 제거 대상:
  - Slack channel_id → `{SLACK_CHANNEL_ID}`
  - Slack channel name → `{SLACK_CHANNEL}`
  - 로컬 작업 경로 → `{WORKDIR}`
  - 개인 Dropbox 경로·이메일·랩 내부 식별자
- 유지 대상: GitHub URL(public), ROI 키워드, 처리/톤/출력 스펙, 벤치마크 리스트 등
  기술 내용. 이건 다른 연구자도 참고 가치 있는 오픈 콘텐츠.
- 커밋 메시지: `Backup prompt vYYYYMMDD (sanitized)`.

---

## [주말 모드 — Weekly Retrospective]

### [실행 분기]
실행 시점에 아래 순서로 분기 판정한다. 평일 모드 입력 소스 fetch 전에 결정.

1. 요일이 **일요일이면** → 즉시 종료. 어떤 산출물도 만들지 않는다.
2. 요일이 **토요일이면** → arxiv `/new` 페이지 HTML을 받아 `Showing new listings for`
   다음 토큰을 본다.
   - 토큰이 `Friday` 이거나 비어 있으면 → **주말 모드**로 진입 (이 섹션 따름)
   - 토큰이 `Saturday`로 새 listing이 떴으면 → 평일 모드로 정상 실행, 주말 모드는
     다음주 토요일로 미룸 (이 케이스는 매우 드묾)
3. 그 외 요일 → 평일 모드 (이 문서의 위 섹션들).

### [원칙 — 두 독자 분리]
- **교수 모드 (페이지 상단)**: 30초 안에 끝나는 요약. ①②③ 까지가 교수용.
- **박사과정 모드 (페이지 본문)**: 다음주 손 움직일 거리. ⑤⑥⑨ 가 박사과정 핵심.
- 평일과 다른 점: 토요일 독자는 시간 여유가 있다. HTML 본문 길이 상한 없음 —
  표·SVG mini-chart·deep-dive 모두 풀로 풀어쓴다. **다만 Slack 메시지는 25줄 컷
  유지**. 본문 풍부함은 HTML 링크로 유도한다.
- 특정 논문을 줄거리 요약하는 톤 금지. 일주일 흐름을 박사+교수급 사전지식으로
  **해석**하는 톤. 논문은 evidence·footnote로만 인용.

### [데이터 소스]
- `trends/YYYY-MM-DD.json` — 최근 28일치 (4주 이동평균용). 없는 날은 0 처리.
- `insights/YYYY-MM-DD.json` — 최근 7일치 (주간 테마 클러스터링).
- `benchmarks/YYYY-MM-DD.json` — 최근 7일치 (위클리 SOTA 리더보드).
- `out/cv_pastweek.json` · `out/ro_pastweek.json` — 평일 모드와 동일하게 fetch
  (제목·저자·primary_cat 만 사용, abstract는 메인 deep-dive 1편에 한해 열기).
- `posts/YYYY-MM-DD.html` 최근 5–6일치 — Top5/Deep-dive 후보 풀.
- `weekly/YYYY-WW.json` — 지난주 토요일에 만든 예측 채점용 (없으면 회고 섹션 생략).

### [산출물 — 9개 섹션]

**🗓 ① Executive Summary (교수용 30초)**
3문장 구어체. (a) 이번주 한 줄 핵심, (b) 가장 변한 것, (c) 가장 안 변한 것.
번호·이모지·표 없이 3문장 그대로.

**⚖️ ② Hot vs Cold (4주 이동평균)**
버킷 8개에 대해 4주 이동평균 trend 라인 (inline SVG mini-chart 또는 텍스트 sparkline).
가속 버킷 ⬆ / 감속 버킷 ⬇ 각 2–3개 + 정체 버킷 1–2개. 각 버킷 옆에 1줄 해석.
"왜 가속/감속하는가"의 가설을 박사+교수 시각으로. 단순 카운트 나열 금지.

**🔥 ③ 주간 Top 5 논문**
최근 5–6일치 평일 must-read 풀 + 박사+교수 사전지식으로 재선정. 5편.
각 편: 제목 (arxiv 링크) + 1줄 배지 + "왜 이 주의 핵심인가" 1줄. 총 5줄.
요약 풀 문장 금지 — "왜 핵심"만.

**🌟 ④ Deep-dive 1편**
③ Top5 중 가장 변곡점 1편. 평일 ⑦과 같은 5단 구조 (핵심 주장 / 방법 핵심 /
실험 표 1개 / 약점·한계 / 우리 랩 영향). 평일보다 약점·한계 절을 더 길게 — 토요일
독자는 비판적으로 읽을 시간 있음.

**📈 ⑤ SOTA 위클리 리더보드 (박사과정 핵심)**
`benchmarks/` 7일치 합쳐 이번주 SOTA를 갱신한 모든 (벤치마크, 메트릭) 행 표로.
컬럼: `벤치마크 / 메트릭 / 이번주 최고 / 지난주 최고 / Δ / 갱신 논문 / 코드 공개`.
Δ가 +/- 부호로 명시. 이번주 갱신 0건이면 섹션 통째 생략.

**🧪 ⑥ 재현 가능 키트 (박사과정 ROI 끝판왕)**
이번주 논문 중 **코드 + 데이터 둘 다** 공개된 것만. GitHub stars 내림차순 정렬, 최대 10편.
표 컬럼: `논문 / 핵심 contribution 1줄 / repo 링크 / ★ stars / 데이터셋 / 환경 (Docker?
requirements.txt 만? 등)`. "월요일 git clone 후보" 라벨. 박사과정이 다음주 시작점으로
삼을 자료. 재현성 평가는 abstract + repo README 1줄로 빠르게 (없는 정보는 "?" 표시).

**🧭 ⑦ 주간 테마 3개 (메타 흐름)**
`insights/` 7일치 + `research_topics/` 7일치를 박사+교수 시각으로 클러스터링.
개별 논문이 아닌 "이번주 메타 흐름" 3개. 각 테마: 1줄 제목 + 3–4줄 구어체 해석.
"평일 ②③의 단발 관찰을 7일 누적으로 메타화" 한 결과물. 논문은 각주 형태로만 1–2개 인용.

**🪞 ⑧ 회고 + 🔮 예측**
- **회고**: 지난주 토요일(`weekly/YYYY-(WW-1).json`)에 만든 예측 3개에 ✅◐✗⏳ 라벨.
  각 1–2줄 이유. 첫 실행이라 지난주 파일이 없으면 회고는 생략하고 예측만.
- **예측**: 이번주 흐름을 보고 다음주 예상 3개. 각 1줄 제목 + 2–3줄 근거.
  이건 다음주 토요일에 채점됨. `weekly/YYYY-WW.json` 에 구조화 저장.

**🎓 ⑨ 트렌드 해설 코너 (박사+교수급 시각)**
*특정 논문 줄거리 요약 금지. 흐름을 historical context와 함께 해석한다.*

- **메인 1편 — 6단 구조**:
  1. 🔍 무엇이 부상했나 (1줄 관찰)
  2. 🧠 그게 뭔지 (개념 정의 + 분야 역사상 위치 — 이전 5–10년 흐름의 어디)
  3. ⚙️ 왜 지금 (직전에 어떤 한계가 풀려서 가능해졌나)
  4. 🪞 재포장인가, 새로운가 (비판적 시각 — "사실 X년 Y의 변형 + Z 끼얹은 것" 같은 평가)
  5. 🔭 6–12개월 뒤 (어디까지 갈지, 어디서 막힐지)
  6. 🎯 우리 분야 시사점 (교수: 펀딩·방향 / 박사: 손 댈 지점)

- **사이드 2편 — 3단 압축**:
  관찰(🔍) / 왜 지금(⚙️) / 전망(🔭) 3단만. 메인의 인접 토픽 2개. 각 2문단 분량.

- 논문 인용은 "예: 이번주 ABC, DEF가 그 사례" 정도로만. 주체는 trend.

**🎧 ⑩ 주간 오디오 (10–15분)**
대본 = ① + ② + ③ + ⑦ + ⑨-메인. 평일(4–6분)보다 길게.
TTS·폴백 규칙은 평일과 동일. 파일명 `audio/YYYY-MM-DD.mp3`.

### [HTML 출력 형식]
- 파일명: `posts/YYYY-MM-DD-weekly.html` (`-weekly` suffix 필수). 평일 파일과
  같은 폴더에 두되, suffix로 인덱스에서 배지로 구분 가능하게.
- 상단 배너: `🗓 Weekly Retrospective · Week WW · YYYY-MM-DD ~ YYYY-MM-DD`
  (실제 주차 + 7일 범위). 배경색을 평일과 다르게 (옅은 보라/오렌지 톤 등) 시각적 구분.
- 홈으로 돌아가기 버튼: 평일과 동일하게 상하단 2곳, 절대 URL.
- 스타일은 `posts/2026-04-18.html` CSS 베이스 유지 — 새 weekly 전용 클래스 추가
  (예: `.weekly-banner`, `.exec-summary`, `.hot-cold-grid`).

### [부수 산출물]
- `weekly/YYYY-WW.json` — 다음주 회고 입력. 스키마:
  ```json
  {
    "date": "YYYY-MM-DD",
    "iso_week": "YYYY-WW",
    "predictions": [
      {"title": "...", "claim": "...", "rationale": "..."}
    ],
    "themes": [{"title": "...", "summary": "..."}],
    "top5": [{"title": "...", "arxiv": "..."}]
  }
  ```
- `trends/YYYY-MM-DD.json` 은 weekly 모드에서도 평일과 동일하게 갱신
  (pastweek 스냅샷이 끊기지 않도록).
- `insights/YYYY-MM-DD.json` 은 weekly 모드에서는 만들지 않는다 (테마는 weekly에 들어감).

### [Slack 메시지 — Weekly 전용 템플릿]
- 25줄 컷 유지. 본문은 페이지 링크로 유도.
- 템플릿:

  ```
  <!channel>
  🗓 *arXiv Weekly Retrospective — YYYY-MM-DD (Week WW)*
  주간 시야: YYYY-MM-DD ~ YYYY-MM-DD · cs.CV/cs.RO pastweek
  🔗 <https://gisbi-kim.github.io/arxiv-daily-summary/posts/YYYY-MM-DD-weekly.html|전체 회고 보기>

  📌 *Executive Summary*
  {① 3문장 그대로 — 교수용 30초}

  ⚖️ *Hot vs Cold*
  ⬆ {가속 버킷 2–3개}  ⬇ {감속 버킷 1–2개}

  🔥 *Top 5*
  1. {제목 짧게}
  2. {제목 짧게}
  ...

  🧭 *주간 테마 3*
  · {테마 1 제목} · {테마 2 제목} · {테마 3 제목}

  🔮 *다음주 예측*
  · {1} · {2} · {3}
  ```

- 발송 트리거: 평일과 동일 (push 성공 직후). push 실패 시 Slack 스킵.

### [실행 순서 — 토요일 weekly 모드]
1. 분기 판정 (위 [실행 분기]).
2. `git pull origin main`.
3. pastweek fetch (cv·ro). `out/cv_pastweek.json` · `out/ro_pastweek.json`.
4. `trends/`·`insights/`·`benchmarks/` 최근 28/7/7일치 로드.
5. `weekly/YYYY-(WW-1).json` 로드 (회고용, 없으면 skip).
6. 9개 섹션 생성 → `posts/YYYY-MM-DD-weekly.html`.
7. `weekly/YYYY-WW.json` 저장 (다음주 회고 입력).
8. `trends/YYYY-MM-DD.json` 갱신 (스냅샷 누적).
9. TTS → `audio/YYYY-MM-DD.mp3` (실패 시 ⑩ 섹션 자체 생략).
10. RSS 피드 재생성 (`scripts/build_feed.py`).
11. git add → commit `Add YYYY-MM-DD weekly retrospective` → push.
12. Slack 발송 (push 성공 시).
