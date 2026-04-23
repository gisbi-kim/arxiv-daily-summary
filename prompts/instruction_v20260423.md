# arXiv Daily Briefing — Prompt (sanitized, v20260423)

> cs.CV · cs.RO를 매일 훑어 동향 브리핑을 만드는 데 쓰는 프롬프트의 공개 버전.
> 실제 실행 시에는 `{WORKDIR}` · `{SLACK_CHANNEL_ID}` · `{SLACK_CHANNEL}` 같은
> placeholder를 본인 환경에 맞게 채워 사용한다.

---

## [입력 소스]
- 오늘 발표: https://arxiv.org/list/cs.CV/new, https://arxiv.org/list/cs.RO/new
- 최근 일주일:
  - https://arxiv.org/list/cs.CV/pastweek?skip=0&show=2000
  - https://arxiv.org/list/cs.RO/pastweek?skip=0&show=2000

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
9. 커밋 + 푸시 — 존재하는 산출물만 add (mp3는 생성 성공 시에만 포함):
   ```bash
   cd {WORKDIR}
   git add posts/YYYY-MM-DD.html \
           trends/YYYY-MM-DD.json \
           benchmarks/YYYY-MM-DD.json \
           insights/YYYY-MM-DD.json \
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
