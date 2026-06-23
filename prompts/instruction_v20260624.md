# arXiv Daily Briefing — Prompt (sanitized, v20260624)

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

---

## 변경점

### v20260624

- `Editorial Clarity Gate` 추가.
- 클러스터 표에서 `같은 row에 저장`, `로그에 기록`, `plot`, `follow-up`, `추가 확인` 같은 저수준 로깅/데이터프레임 문체 금지.
- `Lab action`을 저장 행위가 아니라 benchmark, ablation, stress split, failure mode, downstream metric 중심의 실험 지시로 쓰도록 강화.
- `왜 중요?` 칸이 논문명 나열이나 영어식 압축 구문으로 끝나지 않도록 4단계 해석 구조 추가.
- 나쁜 표현과 좋은 표현의 대조표를 Release Gate에 연결.
- 클러스터 표 아래에 오늘의 판세를 관통하는 한 줄 요약을 강제.
- `Geometry / SLAM / Reconstruction Watch Lens`는 유지하되, 3D/SLAM cluster의 `Lab action`도 robot-usable validity 평가로 쓰도록 보강.

### v20260516

- `Geometry / SLAM / Reconstruction Watch Lens` 추가.
- `SLAM`이라는 제목 키워드가 없어도 localization, relocalization, odometry, mapping, 3DGS map, feature field, feed-forward 3D reconstruction, LiDAR world model을 함께 묶어 해석하도록 보강.
- 3D/Scene 신호가 충분한데 상단 클러스터에 geometry/SLAM/recon 행이 없으면 명시적으로 누락 사유를 쓰도록 Release Gate 추가.

### v20260512

- `/new`의 실제 `listing_date`와 발행할 `post_date`가 다르면 daily 발행을 중단하는 hard gate 추가.
- 과거 날짜 backfill은 `/new` 재사용 금지. 반드시 `/pastweek`의 해당 날짜 섹션만 추출한다.
- `source_listing_date`, `source_mode`, `daily_new_counts.scope` 기록 의무화.
- 직전 daily와 cluster 제목·대표 논문·thesis가 과도하게 같으면 release 실패로 보는 `Editorial Uniqueness Gate` 추가.
- `scripts/validate_daily_release.py --date YYYY-MM-DD` 검증을 Release Gate에 추가.

### v20260510

- 추천/대표 논문에 robotics-paper-phylogeny와 cvml-paper-phylogeny 기준의 `Phylogeny tag`를 붙이는 규칙 추가.
- Daily/Weekly HTML, `insights`/`weekly` JSON, Release Gate에 계통도 태그 검증 추가.
- ROI 버킷·중요도 태그와 별개로 `Phylum > Class > Order > Genus` lineage를 표시해 논문의 연구 계통을 드러내도록 수정.

### v20260509

- 토요일 weekly 실행 전에 빠진 평일 daily를 먼저 복구하는 `Calendar Audit` 추가.
- `execution_date` / `listing_date` / `post_date`를 분리해 토요일 Friday listing 오발행 방지.
- `Backfill / Daily / Weekly / Sunday` 모드를 명시적으로 결정하는 `Mode Resolver` 추가.
- Windows PowerShell UTF-8 BOM 문제를 피하는 parser 실행 규칙 추가.
- 논문 요약을 Tier A/B/C로 나눠 품질과 지속성을 동시에 확보.
- `Release Gate`와 `Catch-up Slack` 템플릿 추가.

---

## [0. 실행 변수]

```text
WORKDIR={WORKDIR}
SLACK_CHANNEL={SLACK_CHANNEL}
SLACK_CHANNEL_ID={SLACK_CHANNEL_ID}
GITHUB_REPO=gisbi-kim/arxiv-daily-summary
SITE_URL=https://gisbi-kim.github.io/arxiv-daily-summary
```

이 프롬프트에서 개인 경로, Slack channel id, Slack channel name은 모두 위 변수만 참조한다. 공개 repo에 백업할 때 실제 값을 쓰지 않는다.

---

## [1. 최상위 원칙]

1. **WebFetch 금지.** arXiv `/new` · `/pastweek` 목록은 반드시 repo의 parser script로 파싱한다.
2. **잘못된 배치 발행 금지.** parser가 실패하면 WebFetch로 대체하지 말고 중단하거나 parser/encoding 문제를 고친다.
3. **누락일 복구 우선.** 토요일 weekly보다 빠진 평일 daily 산출물이 우선이다.
4. **오늘 논문은 `/new`, 주간 해석은 `/pastweek`.** 오늘 논문 요약은 `/new` abstract 기준, 주간 동향과 추천 연구주제는 `/pastweek` 패턴 기준.
5. **산출물은 repo 상태로 검증 후 push.** push 성공 후에만 Slack을 보낸다.
6. **날짜가 맞지 않으면 발행하지 않는다.** `/new`의 실제 `listing_date`와 발행하려는 `post_date`가 다르면 daily mode가 아니라 backfill mode다.
7. **클러스터 표는 템플릿이 아니다.** 직전 daily와 같은 cluster 제목을 재사용하려면 대표 논문과 `왜 중요?`가 실제로 달라야 한다. 같은 제목 4개 이상이 반복되면 미완성 산출물로 본다.
8. **클러스터 표는 리포트의 두뇌다.** 논문별 요약보다 먼저 독자가 오늘의 판세를 이해하게 만들어야 한다.
9. **저장/기록/row 중심 문체 금지.** 클러스터 표의 `Lab action`은 데이터 로깅 지시가 아니라 실험 설계 지시여야 한다.
10. **논문명 나열 금지.** `왜 중요?` 칸은 대표 논문 이름을 나열하는 칸이 아니라, 기존 관점과 새 흐름의 차이를 풀어내는 칸이다.

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

### 2.1 Date Source Contract — hard gate

Daily를 만들기 전에 arXiv 원본이 어떤 날짜를 가리키는지 반드시 확인한다.

```bash
python - <<'PY'
import re, urllib.request
for cat in ["cs.CV", "cs.RO"]:
    html = urllib.request.urlopen(
        urllib.request.Request(
            f"https://arxiv.org/list/{cat}/new",
            headers={"User-Agent": "arxiv-daily-summary helper"},
        ),
        timeout=60,
    ).read().decode("utf-8", "replace")
    h3 = re.findall(r"<h3[^>]*>(.*?)</h3>", html, re.S | re.I)[0]
    print(cat, re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h3)).strip())
PY
```

규칙:

- `post_date == /new listing_date`이면 `/new`를 사용한다.
- `post_date < /new listing_date`이면 `/new` 사용 금지. 반드시 `/pastweek`의 해당 날짜 h3 섹션만 추출하는 backfill parser를 사용한다.
- `/pastweek`에 해당 날짜 섹션이 없으면 발행하지 말고 사용자에게 “원본 listing을 repo에 저장하지 않아 복구 불가”라고 보고한다.
- `post_date > /new listing_date`이면 arXiv가 아직 올라오지 않은 것이므로 발행하지 않는다.
- `cs.CV`와 `cs.RO`의 listing date가 서로 다르면 발행하지 않는다.

`trends/YYYY-MM-DD.json`에는 아래 필드를 반드시 남긴다.

```json
{
  "source_listing_date": "YYYY-MM-DD",
  "source_mode": "new|pastweek-date-section",
  "daily_new_counts": {
    "cv": 0,
    "ro": 0,
    "scope": "new+cross; replacements excluded"
  }
}
```

`source_listing_date != date`이면 release 실패다. 단, `source_mode=pastweek-date-section`이고 `source_listing_date == date`이면 backfill로 허용한다.

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
- 사용자가 “빠진 날짜 채워”, “금요일 했는지 확인”, “누락분 복구”라고 지시.
- `/new`의 `listing_date`가 발행하려는 `post_date`보다 뒤로 넘어갔음.

동작:

- 빠진 날짜를 오래된 순서대로 backfill source로 생성한다.
- `/new`를 다시 쓰지 않는다. 반드시 `/pastweek`에서 해당 날짜 섹션만 추출한다.
- 각 날짜마다 `posts`, `trends`, `benchmarks`, `insights`, `feed.xml`까지 갱신한다.
- 여러 날짜를 복구한 뒤 마지막에 한 번 commit/push 가능.

Backfill parser 예:

```bash
python scripts/fetch_arxiv_pastweek_date.py cs.CV YYYY-MM-DD > out/cv_new.json
python scripts/fetch_arxiv_pastweek_date.py cs.RO YYYY-MM-DD > out/ro_new.json
```

주의:

- `/pastweek` backfill에는 abstract가 없을 수 있다. 이 경우 “title/subject 기반 backfill”임을 meta와 trends에 기록한다.
- `/pastweek` 날짜 섹션의 표시 편수와 `out/*_new.json` 편수가 맞지 않으면 release 실패다.

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

- 오늘 발표:
  - `https://arxiv.org/list/cs.CV/new`
  - `https://arxiv.org/list/cs.RO/new`
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

### 5.1 Windows PowerShell 주의

PowerShell 5의 `Set-Content -Encoding UTF8`은 BOM을 붙일 수 있어 `json.load(..., encoding="utf-8")`에서 깨질 수 있다.

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
2. `/new` 총 편수가 50편 미만이면 parser 오류를 의심한다.
3. `out/classified.json`의 `selected / total` 비율이 40% 이상인가.
4. arXiv id의 `YYMM` prefix가 `listing_date`의 연월과 맞는가.
5. 토요일 backfill이면 `listing_date=Friday`인지 확인하고, `post_date`를 Friday로 둔다.
6. `source_listing_date`, `source_mode`, `daily_new_counts.scope`가 trends JSON에 들어갔는가.
7. 대표 논문에 replacement, cross-list-only, duplicate가 과도하게 섞이지 않았는가.
8. parser가 실패했는데 빈 JSON으로 release하지 않았는가.

간단 검증 예:

```bash
python - <<'PY'
import json, pathlib
for p in ["out/cv_new.json", "out/ro_new.json", "out/cv_pastweek.json", "out/ro_pastweek.json", "out/classified.json"]:
    obj = json.loads(pathlib.Path(p).read_text(encoding="utf-8-sig"))
    print(p, type(obj).__name__, len(obj) if hasattr(obj, "__len__") else "n/a")
PY
```

---

## [7. ROI 버킷]

ROI 버킷은 저장/분류용이다. 상단 해석은 버킷명이 아니라 클러스터 표로 한다.

기본 버킷:

```text
3D/Scene
Robot Learning
Autonomous Driving
Foundation Models
Generation
Efficiency/Systems
Embodied AI
Safety/Alignment
```

주의:

- 버킷은 논문을 담는 서랍이지, 리포트의 결론이 아니다.
- `Generation`, `Robot Learning`, `Safety` 같은 버킷명을 그대로 클러스터 제목으로 쓰면 실패다.
- 클러스터는 버킷을 가로질러 만들어도 된다.
- 한 논문이 여러 버킷과 연결되면 가장 중요한 해석 축을 기준으로 대표 클러스터에 둔다.

---

## [8. Editorial Pipeline]

Daily/Weekly briefing은 아래 순서로 작성한다.

1. 날짜·source mode·parser 결과 확인.
2. ROI paper snapshot 확인.
3. 3D/SLAM/Reconstruction Watch Lens 별도 적용.
4. bucket별 논문 목록을 다시 훑어 2편 이상 연결되는 흐름을 찾는다.
5. 상단 클러스터 표를 먼저 만든다.
6. 클러스터 표에서 오늘의 thesis를 도출한다.
7. `주간 동향`, `오늘의 인사이트`, `추천 연구주제`, `must-read`를 클러스터 표와 일관되게 작성한다.
8. Tier A/B/C 논문 요약을 생성한다.
9. Release Gate를 통과한 뒤 HTML/JSON/feed를 저장한다.

---

## [8.1 Daily 출력 구조]

Daily HTML/Markdown의 권장 구조:

```text
# arXiv Daily Briefing — YYYY-MM-DD (Day)

소스: arXiv cs.CV/new + cs.RO/new · source_listing_date=YYYY-MM-DD · source_mode=new
주간 시야: YYYY-MM-DD ~ YYYY-MM-DD
오늘 /new: cs.CV N + cs.RO M · D dedup · R ROI papers
오늘의 결론: ...

## 오늘의 클러스터 지도
<table 또는 markdown table>

오늘의 핵심은 ...

## 주간 동향
...

## 오늘의 인사이트
...

## 추천 연구주제
...

## Must-read papers
...

## 버킷별 주요 논문
...
```

필수:

- `오늘의 클러스터 지도`는 thesis 바로 뒤에 둔다.
- 표는 최소 3행, 기본 5행을 목표로 한다.
- 5행을 만들 근거가 없으면 표 아래에 “보조 클러스터 근거 부족으로 N행만 표시”라고 적는다.
- 표 이후의 모든 섹션은 클러스터 표를 풀어쓴 것이어야 한다.

---

## [8.2 Weekly 출력 구조]

Weekly HTML/Markdown의 권장 구조:

```text
# arXiv Weekly Briefing — YYYY-WW

소스: arXiv cs.CV/pastweek + cs.RO/pastweek
주간 시야: YYYY-MM-DD ~ YYYY-MM-DD
주간 결론: ...

## 주간 클러스터 표
<table 또는 markdown table>

이번 주의 핵심은 ...

## 주간 동향
...

## 주간 Top 5
...

## 다음 주 실행안
...
```

주의:

- Weekly는 daily의 단순 합산이 아니다.
- 같은 cluster 제목을 반복하더라도 대표 논문, evidence, thesis가 달라야 한다.
- weekly에서는 하루짜리 novelty보다 반복해서 나타난 평가축, failure mode, benchmark shift를 우선한다.

---

## [8.3 클러스터 표 — 필수 스키마]

Daily와 weekly의 클러스터 표 스키마는 동일하다.

```text
| Cluster | 대표 논문 | 왜 중요? | Confidence | Lab action |
|---|---|---|---|---|
```

각 칸의 역할:

- `Cluster`: 버킷명이 아니라 해석된 흐름명.
- `대표 논문`: 한 흐름을 구성하는 evidence set. 기본 2~4편.
- `왜 중요?`: 기존 관점과 새 흐름의 차이를 독자가 다시 묻지 않아도 되게 설명.
- `Confidence`: 감이 아니라 근거 수준. 논문 수, 저자군 다양성, 평가축 반복성에 기반.
- `Lab action`: 회의에서 바로 실험 지시로 바꿀 수 있는 수준의 benchmark/ablation/stress test.

---

## [8.4 클러스터 표의 핵심 원칙]

### 8.4.1 Cluster 칸

Cluster는 버킷명이 아니라 해석된 흐름명이다.

나쁜 예:

```text
Generation
Robot Learning
Safety
3D/Scene
```

좋은 예:

```text
VLA가 few-shot adaptation에서 long-horizon execution diagnosis로 확장
3D reconstruction 평가가 visual fidelity에서 robot-usable validity로 이동
자율시스템 평가가 정적 perception score에서 재현 가능한 실패 시나리오로 이동
긴 비디오/월드모델에서 장면 간 객체·절차 기억이 핵심 병목으로 부상
경량화 연구가 latency 경쟁에서 공간 단서 보존성 평가로 이동
```

Cluster 제목 조건:

- 12~24단어 이내.
- 단순 버킷명으로 끝나지 않는다.
- “무엇에서 무엇으로 이동하는지”가 보인다.
- 논문 제목 키워드의 단순 합집합이 아니다.
- 연구자가 다음 실험 축을 떠올릴 수 있어야 한다.

### 8.4.2 대표 논문 칸

대표 논문은 evidence set이다.

규칙:

- 각 cluster는 최소 2편 이상의 논문을 가져야 한다.
- 기본 2~4편, 아주 강한 흐름이면 5편까지 가능하다.
- 제목 키워드가 우연히 겹치는 논문은 제외한다.
- 같은 단어가 있어도 문제 setting이 다르면 묶지 않는다.
- 논문 제목 뒤에는 필요하면 `[CV]`, `[RO]`, `[CV/RO]`를 붙인다.
- 대표 논문 칸에 넣은 논문은 `왜 중요?` 칸에서 실제 evidence로 작동해야 한다.

### 8.4.3 왜 중요? 칸

`왜 중요?`는 전문가의 압축 메모가 아니라 독자가 되물을 필요 없는 해석이어야 한다.

반드시 아래 4단계를 포함한다.

1. 기존 관점 또는 기존 평가 방식.
2. 오늘 논문들이 새로 드러낸 병목.
3. 대표 논문들이 공유하는 evidence.
4. 우리 랩/로봇 연구 관점에서 바뀌어야 할 평가 또는 실험 설계.

나쁜 구조:

```text
A, B, C는 operational validity로 이동합니다.
```

좋은 구조:

```text
기존 3D reconstruction은 시각적으로 얼마나 그럴듯한지에 집중했지만, 로봇은 물체가 떠 있거나 시점이 바뀌면 깨지는 scene을 그대로 사용할 수 없다. 이번 묶음은 물리적 타당성, view-change robustness, uncertainty-aware fusion을 통해 3D scene이 실제 task에 쓸 수 있는지를 묻는다. 따라서 3D/SLAM 평가는 photometric quality뿐 아니라 robot-usable validity를 별도 축으로 봐야 한다.
```

### 8.4.4 Confidence 칸

Confidence는 감이 아니라 근거 수준이다.

```text
High   = 서로 다른 논문 3편 이상, 서로 다른 저자군/기관, 같은 평가축 또는 같은 실패 조건이 반복됨.
Medium = 2~3편이 같은 방향을 보이지만 benchmark 확산이나 독립 검증은 아직 부족함.
Low    = 신호는 있으나 단발이거나 제목/abstract 기반 연결이 강하지 않음.
```

Confidence 아래에는 반드시 한 줄 근거를 붙인다.

예:

```text
High — VLA adaptation, policy efficiency, memory, failure detection 논문이 같은 날짜에 반복됨
Medium — compression, occupancy, memory distillation 신호는 연결되지만 공통 benchmark는 아직 약함
Low — 단일 논문 중심 신호라 다음 batch 확인 필요
```

### 8.4.5 Lab action 칸

`Lab action`은 “데이터를 어떻게 남길지”가 아니라 “어떤 실험을 해야 하는지”를 말한다.

형식은 아래 중 하나를 따른다.

```text
A와 B를 C 조건에서 비교해 D를 검증한다.
A를 ablation 축으로 두고 B failure mode에 미치는 영향을 평가한다.
A/B/C 조건을 stress split으로 만들어 closed-loop success와 failure warning을 함께 본다.
A metric만 보지 말고 B/C/D를 분리해 task-level 성능 변화와 연결한다.
```

가능하면 아래 요소 중 3개 이상을 포함한다.

```text
benchmark 또는 dataset
비교 대상
ablation 변수
실패 조건
평가 metric
downstream task
expected failure mode
```

---

## [8.5 Editorial Clarity Gate — 번역투·로깅체·저수준 구현어 금지]

클러스터 표는 논문 목록을 압축해 넣는 표가 아니다. 이 표는 독자가 30초 안에 아래 세 가지를 판단하게 해주는 **editorial decision map**이다.

1. 오늘 연구판에서 실제로 움직인 축이 무엇인가.
2. 그 움직임이 기존 평가·방법·실험 관습을 어떻게 바꾸는가.
3. 우리 랩은 다음 실험/제안서/벤치마크에서 무엇을 바꿔야 하는가.

따라서 클러스터 표의 문장은 **저장/기록/row/plot 중심의 데이터 처리 언어**가 아니라, **평가 설계·실패 분석·실험 전략 언어**로 써야 한다.

### 8.5.1 금지되는 문체

아래 표현은 클러스터 표, `왜 중요?`, `Lab action`, `추천 연구주제`에서 원칙적으로 금지한다.

```text
같은 row에 저장한다
같은 row로 기록한다
실험 테이블에 넣는다
로그에 저장한다
row를 분리한다
plot한다
값을 기록한다
항목을 추가한다
metric을 추가한다
follow-up한다
추가 확인한다
audit한다
정리한다
추적한다
체크한다
```

위 표현이 무조건 나쁜 것은 아니지만, arXiv Daily Briefing의 상단 클러스터 표에서는 너무 낮은 수준의 구현어다. 이 표는 “어떤 열을 만들까”가 아니라 “어떤 연구 판단을 해야 하는가”를 말해야 한다.

### 8.5.2 권장되는 연구 동사

금지 표현 대신 아래 동사를 우선 사용한다.

```text
비교한다
분리해 평가한다
ablation 축으로 둔다
failure mode로 추적한다
stress test로 만든다
benchmark split으로 설계한다
실행 안정성에 미치는 영향을 검증한다
downstream task 성능 변화로 검증한다
OOD 조건별로 나누어 평가한다
uncertainty와 task success의 관계를 분석한다
closed-loop 실패 조건으로 재현한다
```

문장의 중심은 항상 **저장 행위**가 아니라 **연구 판단**이어야 한다.

### 8.5.3 대조표 예시 — 나쁜 표현과 좋은 표현

| 구간 | 나쁜 표현 | 좋은 표현 |
|---|---|---|
| VLA Lab action | VLA 실험 테이블에 demo count, memory horizon, action chunk length, failure score, object-generalization split을 같은 row로 저장합니다. | VLA 평가는 성공률만 보지 말고, 데모 수·메모리 길이·액션 청크 길이·실패 감지가 실행 안정성에 미치는 영향을 ablation 축으로 분리해 비교한다. |
| VLA Lab action — 더 구체적 | demo count와 failure score를 기록합니다. | LIBERO/RoboCasa에서 demo count와 memory horizon을 독립 변수로 두고, failure detector가 실제 execution failure를 얼마나 일찍 예측하는지 object-generalization split별로 평가한다. |
| 3D/SLAM Lab action | 3D/SLAM 실험에는 photometric score와 별도로 physical violation, viewpoint sweep error, uncertainty-weighted fusion, robot-task delta를 기록합니다. | 3D/SLAM 결과는 재구성 품질뿐 아니라 물리적 위반, 시점 변화에 따른 붕괴, uncertainty-aware fusion이 실제 localization/navigation 성능을 얼마나 바꾸는지 함께 평가한다. |
| Autonomy Lab action | 자율시스템 benchmark를 OOD geography, replayable scenario seed, geometry cue, prior-map uncertainty, attack trigger exposure로 나눕니다. | 자율시스템 평가는 지역 OOD, 재현 가능한 시나리오, 기하 단서 부족, prior map 오류, 공격 trigger 노출을 별도 stress split으로 구성해 closed-loop failure를 재현한다. |
| Long video / world model Lab action | world-model 평가에 frame budget, temporal distance, entity drift, camera-control error, contact consistency, procedure-step retrieval을 추가합니다. | world model은 프레임 품질만 보지 말고, 긴 시간 간격에서 객체 정체성, 카메라 제어, 접촉 일관성, 절차 기억이 유지되는지를 task-level metric으로 평가한다. |
| Reliability Lab action | 안전성 평가 row를 confidence quantile, OOD family, manipulation severity, prompt/visual trigger, runtime failure detector output으로 분리합니다. | 안전성 평가는 confidence 하나로 뭉뚱그리지 말고, OOD 유형, 조작 강도, prompt/visual trigger, 실행 중 실패 감지 신호를 별도 failure family로 나누어 보고한다. |
| Efficiency Lab action | 경량화 실험에는 latency, bandwidth, memory와 함께 retained geometry cue, occupancy false primitive, boundary error, downstream action delta를 plot합니다. | 경량화는 latency만 줄였는지가 아니라, 압축 후에도 기하 단서, occupancy 구조, 경계 정보, downstream action이 얼마나 보존되는지를 함께 비교한다. |
| 왜 중요? | A, B, C는 operational validity로 이동합니다. | 기존 3D reconstruction은 시각적으로 그럴듯한 결과에 초점을 맞췄지만, 로봇은 물체가 떠 있거나 시점이 바뀌면 무너지는 scene을 사용할 수 없다. 이번 묶음은 물리적 타당성, 시점 강건성, uncertainty-aware fusion을 통해 3D scene을 실제 task에 쓸 수 있는지 평가하려는 흐름이다. |
| 왜 중요? | Reliability는 calibration 하나가 아니라 OOD, manipulation, prompt injection을 분리해야 함. | 모델이 자신 있게 틀리는 문제와, 훈련 분포 밖에서 틀리는 문제, 입력이 조작되어 틀리는 문제는 서로 다른 실패다. 이번 묶음은 confidence calibration 하나로 안전성을 설명할 수 없고, failure family별 평가 로그가 필요하다는 신호다. |
| 제목 | Efficiency는 edge latency보다 spatial evidence 압축 계약으로 봐야 함 | 경량화 평가가 latency 경쟁에서 공간 단서 보존성 평가로 이동 |
| 제목 | Long video와 world generation은 cross-shot memory budget 문제가 됨 | 긴 비디오/월드모델에서 장면 간 객체·절차 기억이 핵심 병목으로 부상 |

### 8.5.4 영어 개념어 사용 규칙

영어 개념어는 필요할 때만 쓴다. 다만 영어 용어를 한국어 문장 안에 던져놓고 설명을 생략하면 실패다.

나쁜 예:

```text
robot-facing failure입니다.
evidence-preserving compression으로 연결됩니다.
operational validity로 이동합니다.
failure surface를 넓힙니다.
```

좋은 예:

```text
로봇 입장에서는 시각적으로 그럴듯한 장면보다, 충돌·접촉·시점 변화에서 무너지지 않는 3D 표현이 더 중요하다.
압축 후에도 localization, occupancy prediction, boundary reasoning에 필요한 공간 단서가 남아 있는지를 봐야 한다.
정적 perception score가 아니라 실제 배포 조건에서 어떤 실패가 재현되는지를 평가해야 한다.
```

영어 개념어를 쓰려면 바로 뒤에서 뜻을 풀어쓴다.

예:

```text
operational validity, 즉 로봇이 실제 시점 변화와 task execution에서 그 3D scene을 사용할 수 있는지의 문제가 중요해진다.
```

### 8.5.5 클러스터 표 최종 검수 질문

클러스터 표를 저장하기 전에 각 행마다 아래 질문에 답한다.

1. 이 행은 논문 제목 몇 개를 이어 붙인 것이 아니라, 실제 공통 연구 흐름을 말하는가?
2. `왜 중요?`를 읽으면 기존 방식과 새 흐름의 차이가 보이는가?
3. `Lab action`이 “기록한다/저장한다/plot한다”가 아니라 “비교한다/검증한다/평가한다”로 끝나는가?
4. 독자가 이 행만 보고 다음 실험 하나를 설계할 수 있는가?
5. 대표 논문이 정말 같은 흐름의 evidence인가, 아니면 제목 키워드만 우연히 겹쳤는가?
6. 너무 영어식 압축 표현으로 끝나지 않았는가?
7. `Confidence`가 감이 아니라 논문 수, 저자군 다양성, 평가축 반복성에 근거하는가?

위 질문 중 하나라도 실패하면 해당 행을 다시 쓴다.

### 8.5.6 강제 Rewrite 규칙

초안 생성 후 아래 표현이 발견되면 자동으로 rewrite한다.

| 발견된 표현 | rewrite 방향 |
|---|---|
| 같은 row에 저장 | 동일 episode/benchmark 조건에서 함께 비교 |
| 로그에 기록 | 실패 원인을 추적할 수 있도록 평가 항목으로 분리 |
| metric을 추가 | 기존 metric이 놓치는 실패 조건을 별도 평가축으로 설계 |
| plot한다 | trade-off 또는 failure curve로 분석 |
| follow-up | 구체적 논문/benchmark/ablation을 지정 |
| 추가 확인 | 무엇을 어떤 기준으로 확인할지 명시 |
| operational validity | 실제 로봇 task에서 쓸 수 있는지 |
| failure surface | 실제 배포에서 재현 가능한 실패 조건 |
| evidence-preserving compression | 압축 후에도 task에 필요한 공간 단서가 남는지 |
| memory budget | 제한된 토큰/프레임/상태 안에서 과거 정보를 얼마나 유지하는지 |
| robot-facing failure | 로봇 실행 시 실제 실패로 이어지는 조건 |

### 8.5.7 최종 출력 톤

최종 문체는 아래와 같아야 한다.

- 연구실 PI가 학생들에게 “이걸 다음 실험에 반영하자”고 말하는 톤.
- 논문 심사자가 “이 평가축이 없으면 claim이 약하다”고 지적하는 톤.
- 과제 제안서 작성자가 “이게 왜 지금 중요한지”를 설득하는 톤.

아래 톤은 피한다.

- 번역기처럼 영어 추상어를 한국어 조사로만 연결한 문장.
- 데이터 엔지니어링 로그 설계 메모.
- arXiv 제목 키워드를 모아 붙인 자동 요약문.
- “중요합니다/필요합니다”만 반복하는 일반론.
- 독자가 다시 물어봐야 이해되는 압축 메모.

### 8.5.8 좋은 클러스터 행 예시

| Cluster | 대표 논문 | 왜 중요? | Confidence | Lab action |
|---|---|---|---|---|
| VLA가 few-shot adaptation에서 long-horizon execution diagnosis로 확장 | FOCA; PolicyTrim; MemoryVAM; VLA-FAIL | 기존 VLA 평가는 적은 데모로 새 skill을 배우는지에 초점을 맞추는 경우가 많았다. 이번 묶음은 데모 수뿐 아니라 실행 이력, 액션 청크 길이, 실패 감지가 실제 안정성을 바꾼다는 신호를 준다. 즉 VLA를 단순 action decoder가 아니라 memory와 failure monitor를 포함한 실행 시스템으로 봐야 한다. | High — VLA adaptation, policy efficiency, memory, failure detection 논문이 같은 날짜에 반복됨 | LIBERO/RoboCasa에서 demo count, memory horizon, action chunk length를 독립 ablation 축으로 두고, failure detector가 실제 execution failure를 얼마나 앞서 예측하는지 object-generalization split별로 평가한다. |
| 3D reconstruction 평가가 visual fidelity에서 robot-usable validity로 이동 | phi-Scene; G-MASt3R-SfM; Single-View Mesh Rotation; UECP | 기존 3D reconstruction은 시각적으로 얼마나 그럴듯한지에 집중했지만, 로봇은 물체가 떠 있거나 시점이 바뀌면 깨지는 scene을 그대로 사용할 수 없다. 이번 묶음은 물리적 타당성, view-change robustness, uncertainty-aware fusion을 통해 3D scene이 실제 task에 쓸 수 있는지를 묻는다. | High — physical validity, SfM pruning, robot camera rotation, uncertainty fusion 신호가 동시에 등장 | 3DGS map, point-cloud map, feature-field map을 visual localization 성공률, update cost, dynamic-object failure, downstream navigation success 기준으로 비교한다. |
| 자율시스템 평가가 정적 perception score에서 재현 가능한 실패 시나리오로 이동 | Robusto-2; BadDreamer; From Driving Videos to Simulatable Scenarios; Mirage | 자율주행/자율로봇 평가는 detection AP나 offline planning score만으로 실제 배포 실패를 설명하기 어렵다. 이번 묶음은 지역 OOD, video-to-scenario 변환, prior map 오류, backdoor trigger처럼 실제 시스템이 무너지는 조건을 benchmark 안으로 끌어들이려는 흐름이다. | High — driving, world model, LiDAR security, scenario replay 신호가 같은 deployment failure 축을 형성 | 지역 OOD, prior-map corruption, attack trigger exposure를 별도 stress split으로 만들고 closed-loop success, near-miss, recovery behavior를 함께 평가한다. |
| 긴 비디오/월드모델에서 장면 간 객체·절차 기억이 핵심 병목으로 부상 | Long Video Memory; GroundShot; UnityShots; IMAGIN-4D | 긴 비디오와 world generation에서는 프레임 하나의 품질보다, 장면이 바뀌어도 객체 정체성·카메라 경로·접촉 상태·절차 순서가 유지되는지가 더 중요하다. 이는 robot world model 평가에서도 단기 prediction보다 long-horizon consistency와 task-relevant memory를 봐야 한다는 뜻이다. | High — memory budget, entity persistence, camera control, contact consistency 논문이 같은 축으로 묶임 | frame budget과 temporal distance를 바꿔가며 entity drift, camera-control error, contact consistency, procedure-step retrieval이 downstream planning success에 미치는 영향을 평가한다. |
| 신뢰성 평가가 confidence calibration에서 failure-family diagnosis로 확장 | Quantile Calibration; PROTON; T-IMPACT; MIRAGE; VLA-FAIL | 모델이 자신 있게 틀리는 문제, OOD에서 틀리는 문제, 조작된 입력에 속는 문제, 실행 중 실패 징후를 놓치는 문제는 서로 다르다. 이번 묶음은 reliability를 하나의 confidence 숫자로 뭉뚱그리지 말고 failure family별로 나누어 평가해야 한다는 신호다. | High — calibration, OOD, manipulation, prompt/visual injection, runtime failure detection이 동시에 등장 | OOD family, manipulation severity, prompt/visual trigger, runtime failure warning을 별도 split으로 만들고, 각 조건에서 confidence와 실제 failure의 상관을 비교한다. |
| 경량화 연구가 latency 경쟁에서 공간 단서 보존성 평가로 이동 | ACE-GS; FLM-Occ; Recurrent Memory Distillation; CoVStream | 로봇 배포에서는 모델이 빠른지만으로 충분하지 않다. 압축 후에도 localization, occupancy prediction, boundary reasoning, action decision에 필요한 공간 단서가 남아 있어야 한다. 이번 묶음은 efficiency를 latency 절감이 아니라 task-relevant evidence를 얼마나 보존하는지로 봐야 한다는 흐름이다. | Medium — compression, occupancy, memory distillation, edge-cloud 신호는 연결되지만 공통 benchmark는 아직 약함 | latency, bandwidth, memory를 줄이는 조건별로 geometry cue 보존율, occupancy false primitive, boundary error, downstream action delta를 함께 비교한다. |

### 8.5.9 한 줄 요약 규칙

클러스터 표 아래에는 반드시 한 줄로 오늘의 판세를 다시 쓴다.

형식:

```text
오늘의 핵심은 [큰 주제]가 아니라, [실제 병목]을 [평가/실험/배포] 안에서 어떻게 드러내고 검증할 것인가다.
```

예:

```text
오늘의 핵심은 더 큰 VLA나 더 예쁜 3D scene이 아니라, memory, uncertainty, failure detector, physical validity, deployment efficiency를 실제 실행 평가 안에서 어떻게 분리해 검증할 것인가다.
```

이 한 줄이 표의 모든 행을 관통하지 못하면 클러스터 표를 다시 쓴다.

---

## [8.6 Editorial Uniqueness Gate]

Daily cluster는 그날 논문 집합을 다시 읽고 새로 판단해야 한다. 같은 repo 안의 직전 daily에서 제목을 가져와 채우면 안 된다.

저장 전 아래를 확인한다.

1. 직전 daily의 `insights/YYYY-MM-DD.json`과 오늘 `clusters[].cluster`를 비교한다.
2. cluster 제목이 4개 이상 완전히 같으면 release 실패다.
3. 제목이 3개 이하로 같더라도, 같은 제목의 대표 논문 arXiv id가 50% 이상 다르면 제목을 더 구체적으로 바꾼다.
4. `왜 중요?` 문장에 “오늘/이번 묶음/5월 N일”의 구체적 evidence가 없어도 실패다.
5. `대표 논문` 칸은 cluster 설명에 언급한 논문과 실제 링크가 일치해야 한다.
6. `추천 연구주제`는 cluster 제목을 그대로 반복하지 말고, 그날 대표 논문에서 바로 이어지는 실험 단위로 쓴다.

예:

- 5/11에 `Sword`, `ST-Gen4D`, `GEM`이 대표면 cluster는 `World model을 simulator로 쓰려는 흐름이 4D와 LiDAR까지 확장`처럼 쓴다.
- 5/12에 `CoWorld-VLA`, `CapVector`, `ALAM`이 대표면 cluster는 `VLA 실행 스택이 async, capability vector, latent transition으로 쪼개짐`처럼 쓴다.
- 둘 다 “VLA가 내부 역할을 나누는 쪽으로 이동”이라고 쓰면 실패다.

---

## [8.7 Geometry / SLAM / Reconstruction Watch Lens]

`3D/Scene` 버킷은 단순 보관용으로 두면 안 된다. 매일 클러스터 표를 만들기 전에 `3D/Scene` 논문을 별도로 다시 훑고, classic SLAM 제목이 줄어들어도 아래 신호가 2편 이상 있으면 독립 클러스터 후보로 승격한다.

추적할 신호:

- SLAM, visual-inertial SLAM, LiDAR-inertial odometry, odometry, relocalization, localization, geo-localization
- 2D-3D correspondence, pose estimation, calibration, bundle adjustment, dynamic object removal, static mapping
- Gaussian Splatting을 map, feature field, localization substrate, dynamic scene representation으로 쓰는 논문
- feed-forward 3D reconstruction, VGGT류 visual geometry model, sparse-view reconstruction, multi-view reconstruction
- LiDAR world model, synthetic LiDAR sensing, 4D reconstruction, scene change detection, dynamic scene reconstruction

중요한 해석 규칙:

1. `SLAM`이라는 단어가 제목에 없어도 pose, map, correspondence, localization, reconstruction, dynamic scene representation 문제를 풀면 `SLAM/recon signal`로 묶어 본다.
2. 3DGS 논문을 전부 rendering 품질 경쟁으로만 읽지 않는다. map representation, localization feature, dynamic scene state, robot/driving scene prior로 쓰이면 robotics geometry 흐름으로 해석한다.
3. feed-forward 3D reconstruction은 단순 reconstruction 속도 개선이 아니라, SfM/MVS/SLAM식 iterative geometry가 foundation geometry model로 흡수되는 신호인지 확인한다.
4. world model 논문 중 LiDAR, 4D geometry, scene flow, physical consistency, downstream control을 다루는 논문은 Generation 버킷에 있어도 geometry/SLAM/recon 후보로 cross-check한다.

상단 클러스터 예시:

- `Classic SLAM이 Gaussian map과 feature-field localization으로 재포장되는 중`
- `Reconstruction이 offline optimization에서 feed-forward geometry foundation model로 이동`
- `Mapping이 static point cloud에서 dynamic 4D/Gaussian scene representation으로 확장`
- `Localization이 cross-view, synthetic LiDAR, 2D-3D correspondence retrieval로 다시 등장`
- `3DGS가 rendering asset에서 robot/driving map representation으로 넘어가는 중`
- `3D reconstruction 평가가 visual fidelity에서 robot-usable validity로 이동`

클러스터 표 작성 규칙:

- Daily에서 `3D/Scene`이 10편 이상이거나, `SLAM/localization/odometry/reconstruction/Gaussian/LiDAR/depth/calibration/pose` 관련 논문이 2편 이상이면 geometry/SLAM/recon 후보를 반드시 검토한다.
- 위 조건을 만족하는데 최종 클러스터 표에 geometry/SLAM/recon 행을 넣지 않는다면, `주간 동향` 또는 표 아래에 “3D/Scene은 많았지만 상단 클러스터로 올리지 않은 이유”를 1문장으로 적는다.
- 이 행은 반드시 최소 2편 이상의 대표 논문을 가진다. 단일 SLAM 논문만 있으면 `Watch-only`로 내리고, 대신 3DGS localization, feed-forward reconstruction, LiDAR world model과 묶을 수 있는지 다시 본다.
- `Lab action`은 “논문 추적”이 아니라 바로 실행 가능한 형태로 쓴다.

좋은 `Lab action` 예:

```text
3DGS map, point-cloud map, feature-field map을 visual localization 성공률, update cost, dynamic-object failure, downstream navigation success 기준으로 비교한다.
VGGT류 feed-forward recon과 COLMAP/MVS baseline을 sparse-view, latency, scale drift, robot camera rotation robustness로 비교한다.
LiDAR world model과 static map baseline을 scene-change detection, localization drift, closed-loop recovery 기준으로 평가한다.
```

---

## [8.8 중요도 태그]

대표 논문과 클러스터에는 아래 태그 중 하나 이상을 붙인다. 단, 화면에서 한 논문/클러스터에 붙이는 태그는 핵심 2~3개로 제한한다.

```text
[문제정의] 새 문제나 연구 질문 자체를 세운 논문
[평가축] metric, benchmark protocol, failure condition처럼 성능을 재는 기준을 바꾼 논문
[방법전환] 기존 병목을 다른 formulation으로 푼 논문
[인프라] dataset/tool/framework/benchmark를 만든 논문
[경고신호] negative result, failure mode, safety/deployment risk를 드러낸 논문
[통합정리] survey/review/taxonomy/map처럼 흩어진 흐름을 한 장의 지도로 묶는 논문
[스케일업] 모델·데이터·embodiment·실험 규모를 키워 새 현상이나 한계를 보려는 논문
[실사용전환] latency, real-time, on-device, hardware, closed-loop, field deployment를 겨냥한 논문
[데이터전환] 병목을 모델 구조보다 데이터 수집·정제·합성·라벨링 방식에서 찾는 논문
[해부분석] 모델 내부 표현, mechanism, ablation, probing으로 왜 되는지/왜 실패하는지 뜯어보는 논문
[표준후보] 후속 논문들이 계속 쓸 만한 task, metric, protocol, dataset, benchmark를 제안하는 논문
[위험보류] 아이디어는 흥미롭지만 baseline, split, ablation, 데이터 공개성 때문에 claim 확인이 필요한 논문
```

태그 사용 원칙:

- 태그는 장식이 아니라 “왜 봐야 하는가”를 압축하는 표식이다.
- 한 논문에 태그를 너무 많이 붙이지 않는다.
- `위험보류`는 비난이 아니라 claim 확인 필요성을 표시하는 태그다.
- `평가축`, `경고신호`, `실사용전환`은 APRL 관점에서 우선순위를 높게 둔다.

---

## [8.9 Phylogeny tag]

추천/대표 논문에는 robotics-paper-phylogeny 또는 cvml-paper-phylogeny 기준의 lineage를 붙인다.

형식:

```text
Phylogeny: ROBOTICS · Perception and Mapping > State Estimation > SLAM and Odometry > Geometry Maps
Phylogeny: CVML · Foundation Models > Multimodal Learning > Vision-Language Models > Reasoning and Reliability
```

어느 논문에 붙이나:

- Daily `오늘의 클러스터 지도`의 대표 논문
- Daily `오늘의 인사이트`에서 언급한 대표 논문
- Daily `추천 연구주제`의 근거 논문
- Daily Tier A / must-read / deep-dive 논문
- Weekly `주간 클러스터 표`의 대표 논문
- Weekly `주간 Top 5`
- Weekly deep-dive와 다음 주 실행안의 근거 논문

압축 부록의 Tier B/C 논문에는 가능하면 붙인다. 너무 많은 경우 Tier A/B 우선으로 붙이고, 나머지는 JSON 필드에만 넣어도 된다.

---

## [9. 논문 요약 Tier]

### 9.1 Tier A — Must-read / deep-dive 논문

조건:

- 오늘 클러스터를 대표하는 핵심 evidence.
- APRL 연구주제와 직접 연결.
- benchmark, metric, failure mode, deployment implication이 분명함.
- 후속 실험으로 바로 이어질 수 있음.

작성 방식:

```text
문제: 이 논문이 겨냥한 병목/공백
방법: 기존 방식과 다른 핵심 아이디어
의미: 왜 오늘/이번주 흐름에서 중요한지
APRL action: 우리 랩 실험/제안서/벤치마크에서 어떻게 쓸지
Phylogeny: ...
```

금지:

- 초록에 없는 수치, 코드 공개 여부, dataset 공개 여부를 지어내지 않는다.
- “SOTA 달성” 같은 표현은 abstract에 근거가 없으면 쓰지 않는다.
- 제목만 보고 과도하게 로봇 응용을 단정하지 않는다.

### 9.2 Tier B — 인사이트 대표 논문 8~12편

3문장 이내로 쓴다.

포함 요소:

- 문제
- 기존 방식과 차이
- 왜 오늘/이번주 흐름에서 중요한지
- 어떤 클러스터의 evidence인지
- 어느 계통도 lineage에 속하는지

### 9.3 Tier C — 나머지 ROI 논문

abstract 기반 짧은 요약.

필수 bullet:

```text
- 문제: 이 논문이 겨냥한 병목/공백
- 방법: 기존 방식과 다른 핵심 아이디어
- 의미: 왜 이 버킷/클러스터에서 볼 가치가 있는지
```

주의:

- abstract에 없는 디테일을 지어내지 않는다.
- 제목 키워드만 보고 잘못된 버킷에 넣지 않는다.
- 너무 약한 논문은 “watch-only”로 낮춰도 된다.

---

## [10. 오늘의 인사이트]

`오늘의 인사이트`는 클러스터 표를 풀어쓴 3~5개 문단이다.

규칙:

- 각 인사이트는 클러스터 표의 한 행과 연결되어야 한다.
- 문단 첫 문장은 결론형으로 쓴다.
- 둘째 문장은 대표 evidence를 설명한다.
- 셋째 문장은 APRL 관점에서 실험/제안서/리뷰에 어떻게 반영할지 쓴다.
- 클러스터 표와 같은 표현을 그대로 반복하지 않는다.

좋은 구조:

```text
VLA 평가는 단순 success rate에서 실행 진단으로 이동하고 있다. FOCA, PolicyTrim, MemoryVAM, VLA-FAIL은 각각 demo scarcity, policy efficiency, memory, failure detection을 건드리지만, 공통적으로는 long-horizon execution stability를 설명하려는 흐름이다. 우리 실험에서는 success/fail만 보고 끝내지 말고 memory horizon과 failure warning이 실제 실패 직전 어떻게 변하는지 분리해 봐야 한다.
```

---

## [11. 추천 연구주제]

추천 연구주제는 클러스터 제목을 바꿔 쓴 것이 아니다. 그날 논문에서 바로 이어지는 실험 단위여야 한다.

형식:

```text
### 연구주제명
한 줄 요약.

- 근거 논문: A, B, C
- 핵심 질문: ...
- 실험 설계: benchmark/dataset, baseline, ablation, metric
- 기대 결과: 어떤 failure mode나 trade-off를 드러낼 수 있는가
```

좋은 예:

```text
### VLA execution diagnosis grid
VLA 성공률 뒤에 숨어 있는 demo scarcity, memory horizon, action chunk length, failure warning의 상호작용을 분리한다.

- 근거 논문: FOCA, PolicyTrim, MemoryVAM, VLA-FAIL
- 핵심 질문: failure detector가 실제 실행 실패를 얼마나 앞서 예측하는가?
- 실험 설계: LIBERO/RoboCasa task family에서 demo count, memory horizon, action chunk length를 독립 ablation 축으로 둔다.
- 기대 결과: 성공률이 같아도 실패 전조와 object-generalization 안정성이 다른 모델을 구분할 수 있다.
```

금지:

- “추가 확인”으로 끝내지 않는다.
- “metric 설계”라고만 쓰지 않는다.
- 대표 논문 제목을 다시 나열하는 것으로 끝내지 않는다.

---

## [12. Must-read 선정 규칙]

Must-read는 오늘 나온 논문 중 “읽을 가치가 있는 논문”이 아니라, **리포트의 thesis를 지탱하는 논문**이다.

우선순위:

1. 오늘 클러스터의 중심 evidence.
2. 평가축, benchmark, failure condition을 바꾸는 논문.
3. robotics deployment와 직접 연결되는 논문.
4. geometry/SLAM/reconstruction watch lens에 걸리는 논문.
5. 위험하지만 claim 확인이 필요한 논문.

각 must-read에는 아래를 붙인다.

```text
논문 제목 [중요도 태그]
왜 읽어야 하는지 1문장
어떤 클러스터의 evidence인지
Phylogeny tag
```

---

## [13. Weekly 작성 규칙]

Weekly는 daily의 합산이 아니다. 아래 질문에 답해야 한다.

1. 이번 주에 반복해서 등장한 평가축은 무엇인가?
2. 단발 novelty가 아니라 trend로 볼 수 있는 것은 무엇인가?
3. 어떤 failure mode가 여러 버킷에서 반복되었는가?
4. 어떤 benchmark/protocol이 표준 후보로 보이는가?
5. APRL이 다음 주 바로 해볼 수 있는 실험은 무엇인가?

Weekly cluster는 daily cluster를 그대로 복사하면 안 된다. 같은 흐름이라도 더 넓은 주간 thesis로 다시 써야 한다.

나쁜 예:

```text
VLA가 내부 역할을 나누는 쪽으로 이동
```

좋은 예:

```text
이번 주 VLA 흐름은 구조 분해를 넘어 실행 중 실패 진단과 memory-aware evaluation으로 확장
```

---

## [14. HTML/JSON 산출물]

Daily mode 산출물:

```text
posts/YYYY-MM-DD.html
trends/YYYY-MM-DD.json
benchmarks/YYYY-MM-DD.json
insights/YYYY-MM-DD.json
feed.xml
```

Weekly mode 산출물:

```text
posts/YYYY-MM-DD-weekly.html
weekly/YYYY-WW.json
trends/YYYY-MM-DD.json
feed.xml
```

각 JSON에는 최소한 아래 정보를 포함한다.

```json
{
  "date": "YYYY-MM-DD",
  "source_listing_date": "YYYY-MM-DD",
  "source_mode": "new|pastweek-date-section",
  "daily_new_counts": {
    "cv": 0,
    "ro": 0,
    "scope": "new+cross; replacements excluded"
  },
  "clusters": [
    {
      "cluster": "...",
      "representative_papers": ["..."],
      "why_it_matters": "...",
      "confidence": "High|Medium|Low",
      "confidence_rationale": "...",
      "lab_action": "..."
    }
  ]
}
```

---

## [15. Release Gate]

release 전에 반드시 아래를 확인한다.

### 15.1 Source/date gate

- `post_date == source_listing_date`인가?
- backfill이면 `source_mode=pastweek-date-section`인가?
- `/new`와 `/pastweek`를 잘못 섞지 않았는가?
- `cs.CV`와 `cs.RO` listing date가 일치하는가?
- daily_new_counts가 실제 parser 결과와 맞는가?

### 15.2 File gate

- `posts/YYYY-MM-DD.html` 또는 weekly HTML이 생성되었는가?
- `trends/YYYY-MM-DD.json`이 생성되었는가?
- daily라면 `benchmarks/YYYY-MM-DD.json`, `insights/YYYY-MM-DD.json`이 생성되었는가?
- `feed.xml`이 갱신되었는가?
- HTML에 `Cluster`, `대표 논문`, `왜 중요?`, `Confidence`, `Lab action`이 실제로 들어 있는가?

### 15.3 Cluster gate

- 클러스터 표가 thesis 바로 뒤에 있는가?
- daily는 기본 5행, 최소 3행 이상인가?
- 각 행의 대표 논문이 최소 2편 이상인가?
- `왜 중요?`가 기존 관점과 새 흐름의 차이를 설명하는가?
- `Lab action`이 바로 실험 지시로 바뀔 수 있는가?
- Confidence에 근거가 붙어 있는가?
- 직전 daily와 cluster 제목이 과도하게 반복되지 않는가?

### 15.4 Editorial Clarity gate

아래 조건 중 하나라도 만족하면 release 실패다.

1. `Lab action`에 `같은 row`, `저장`, `기록`, `plot`, `추가 확인`, `follow-up`, `metric 설계`만 있고 구체적 benchmark·ablation·failure condition이 없다.
2. `왜 중요?`가 논문명 나열로 시작하고, 기존 관점과 새 관점의 차이를 설명하지 않는다.
3. Cluster 제목이 `Generation`, `Robot Learning`, `Safety`, `3D/Scene` 같은 버킷명으로 끝난다.
4. 영어 개념어가 2개 이상 연속으로 나오는데 한국어 해설이 없다.
5. `Lab action`이 실제 회의에서 학생에게 줄 수 있는 실험 지시로 바뀌지 않는다.
6. `왜 중요?`와 `Lab action`이 서로 연결되지 않는다.
7. 클러스터 표가 전체 리포트의 결론과 연결되지 않고, 별도 장식 표처럼 보인다.

### 15.5 Geometry gate

- `3D/Scene`이 10편 이상이거나 SLAM/localization/odometry/reconstruction/Gaussian/LiDAR/depth/calibration/pose 관련 논문이 2편 이상이면 geometry/SLAM/recon 후보를 검토했는가?
- 조건을 만족하는데 상단 클러스터에 geometry/SLAM/recon 행이 없다면 누락 사유를 1문장으로 적었는가?
- geometry/SLAM/recon 행의 `Lab action`이 robot-usable validity 평가로 쓰였는가?

### 15.6 Phylogeny gate

- 대표 논문과 must-read에 Phylogeny tag가 붙어 있는가?
- robotics/cvml lineage가 논문의 실제 문제 setting과 맞는가?
- 애매한 경우에는 `Phylogeny: tentative`로 두고 과도하게 단정하지 않는다.

### 15.7 Script validation

가능하면 아래 검증을 수행한다.

```bash
python scripts/validate_daily_release.py --date YYYY-MM-DD
```

실패하면 release하지 않는다. validator가 아직 Editorial Clarity Gate를 구현하지 않았다면, 사람이 위 체크리스트를 수동으로 적용한다.

---

## [16. Slack 발행]

Slack은 repo push 성공 후에만 보낸다.

Daily Slack 템플릿:

```text
arXiv Daily Briefing — YYYY-MM-DD
소스: cs.CV/new + cs.RO/new, source_listing_date=YYYY-MM-DD
오늘 /new: cs.CV N + cs.RO M · D dedup · R ROI papers

오늘의 결론: ...

Top clusters
1. ...
2. ...
3. ...

Link: {SITE_URL}/posts/YYYY-MM-DD.html
```

Weekly Slack 템플릿:

```text
arXiv Weekly Briefing — YYYY-WW
주간 시야: YYYY-MM-DD ~ YYYY-MM-DD

이번 주의 결론: ...

Top clusters
1. ...
2. ...
3. ...

Link: {SITE_URL}/posts/YYYY-MM-DD-weekly.html
```

Catch-up Slack 템플릿:

```text
arXiv Daily Briefing catch-up
누락된 YYYY-MM-DD daily를 backfill mode로 복구했습니다.
source_mode=pastweek-date-section

Link: {SITE_URL}/posts/YYYY-MM-DD.html
```

---

## [17. 최종 실행 요약]

매 실행 종료 시 사용자에게 아래를 보고한다.

```text
완료:
- mode: Daily|Weekly|Backfill|Sunday skip
- date: YYYY-MM-DD
- source_listing_date: YYYY-MM-DD
- source_mode: new|pastweek-date-section
- generated files: ...
- cluster rows: N
- geometry/SLAM/recon reviewed: yes|no, reason
- editorial clarity gate: pass|fail
- pushed: yes|no
- Slack sent: yes|no
```

실패 시에는 다음을 보고한다.

```text
실패 원인:
- source/date mismatch | parser failure | cluster gate failure | editorial clarity gate failure | geometry gate failure | validation failure

수정해야 할 것:
- ...
```

---

## [18. 최종 기억]

이 프롬프트의 핵심은 “논문을 많이 요약하는 것”이 아니다.

핵심은 아래다.

```text
오늘 나온 논문들을 통해 연구판의 이동 방향을 잡고,
그 이동이 우리 랩의 평가축·실험 설계·제안서 논리에 어떤 변화를 요구하는지 보여준다.
```

따라서 클러스터 표에서 가장 중요한 동사는 `저장한다`가 아니라 `검증한다`, `비교한다`, `분리해 평가한다`, `stress test로 만든다`이다.

오늘의 핵심 한 줄이 이 기준을 통과하지 못하면 release하지 않는다.
