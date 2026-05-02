# arxiv-daily-summary

cs.CV · cs.RO 논문을 매일 자동으로 수집·분류·요약해 HTML 브리핑 페이지를 생성하는 파이프라인.

**[→ 브리핑 보기](https://gisbi-kim.github.io/arxiv-daily-summary/)**

---

## 무슨 프로젝트인가

arXiv에 매일 올라오는 Computer Vision / Robotics 논문을 8개 관심 버킷으로 분류하고, 각 논문을 짧게 요약해 읽기 편한 HTML 페이지로 만든다. 주말에는 한 주치 트렌드를 돌아보는 Weekly 회고판을 별도로 생성한다.

Claude Code agent가 매일 자동 실행한다. 프롬프트 파일(`prompts/`)이 실행 방법과 버전 변경 이력을 담고 있다.

---

## 관심 버킷 (ROI Buckets)

| 버킷 | 주요 키워드 |
|------|------------|
| 📦 3D/Scene | 3DGS, NeRF, SLAM, point cloud, LiDAR, depth, odometry |
| 🤖 Robot Learning | VLA, imitation learning, manipulation, humanoid, sim2real |
| 🚗 Autonomous Driving | BEV, motion planning, nuScenes, trajectory prediction |
| 🧠 Foundation Models | VLM, multimodal LLM, visual reasoning, VQA |
| 🎨 Generation | diffusion, video generation, flow matching, text-to-image |
| ⚡ Efficiency/Systems | MoE, KV cache, quantization, pruning, LoRA |
| 🏃 Embodied AI | navigation, VLN, embodied agent, instruction following |
| 🛡️ Safety/Alignment | adversarial, robustness, alignment, OOD detection |

---

## 파이프라인

```
fetch_arxiv.py          arXiv /new · /pastweek HTML을 직접 파싱 → JSON
      ↓
classify.py             cs.CV + cs.RO 통합 · 중복 제거 → 버킷 분류
      ↓
gen_html_YYYYMMDD.py    요약 삽입 → posts/YYYY-MM-DD.html
      ↓
build_feed.py           feed.xml (RSS) 갱신
build_weekly.py         weekly/YYYY-Www.json 생성 (토요일)
build_weekly_html.py    posts/YYYY-MM-DD-weekly.html 생성 (토요일)
```

> **arXiv 파서를 직접 만든 이유**  
> WebFetch는 긴 arXiv 목록 페이지를 AI가 요약하면서 arxiv_id를 환각·누락하는 사고가 생겼다. stdlib만 쓴 HTML 파서(`fetch_arxiv.py`)로 고정해 ID 오류를 원천 차단한다.

---

## 저장소 구조

```
posts/          일별·주별 HTML 브리핑
trends/         일별 pastweek 버킷 분포 스냅샷 (JSON)
benchmarks/     일별 성능 지표 (JSON)
insights/       일별 인사이트 추출 결과 (JSON)
weekly/         주별 회고 데이터 (JSON)
scripts/        파이프라인 스크립트
prompts/        agent 실행 프롬프트 및 버전 이력
index.html      홈 페이지
feed.xml        RSS 피드
```

---

## 로컬 실행

```bash
mkdir -p out
python scripts/fetch_arxiv.py new cs.CV      > out/cv_new.json
python scripts/fetch_arxiv.py new cs.RO      > out/ro_new.json
python scripts/fetch_arxiv.py pastweek cs.CV > out/cv_pastweek.json
python scripts/fetch_arxiv.py pastweek cs.RO > out/ro_pastweek.json
python scripts/classify.py                   > out/classified.json
# 날짜에 맞는 gen_html 스크립트 실행
python scripts/build_feed.py
```

파싱 결과 검증 체크리스트:
- `out/cv_new.json`의 arxiv_id `YYMM` 파트가 당일 날짜와 일치하는가
- scanned 논문 수 100 미만이면 파싱 오류 의심
- `out/classified.json`의 `selected / total` 비율이 40% 이상인가
