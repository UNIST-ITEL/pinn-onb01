# PINN-ONB01 — Post-Acceptance Public Release Checklist

**작성일**: 2026-05-18
**근거**: `05_manuscript/main.tex` § Data availability (lines 128-145)
**대상 공개 시점**: IJHMT 게재 수락 후 (proof 단계 또는 게재 직후)

---

## 결정 사항 요약

| 항목 | 결정 |
|---|---|
| 공개 시점 | **수락 후** (게재 확정 후 proof 단계에서 DOI 삽입) |
| GitHub repo | `https://github.com/UNIST-ITEL/pinn-onb01` (org 계정) |
| 데이터 license | **CC-BY-4.0** |
| 코드 license | **MIT** |
| Digitization metadata | **포함** (per-paper WebPlotDigitizer 기록) |
| 데이터 저장소 | **Zenodo** (영구 DOI) + GitHub-Zenodo 자동 연동 |

---

## Phase 0 — 제출 직후 (게재 결정 대기 중에도 진행 가능)

| # | 작업 | 담당 | 상태 |
|---|---|---|---|
| 0-1 | UNIST-ITEL GitHub organization 계정 생성 (없으면) | Jaeseon Lee | ☐ |
| 0-2 | Zenodo 계정 생성 + ORCID 연동 (0000-0003-1996-6086) | Jaeseon Lee | ☐ |
| 0-3 | Zenodo $\leftrightarrow$ GitHub 통합 설정 (Zenodo Settings → GitHub) | Jaeseon Lee | ☐ |
| 0-4 | Public repo 콘텐츠 폴더 정리 (raw PDF 제외, .bak 제외, 이미 `.gitignore` 처리) | Claude/저자 | ☐ |
| 0-5 | 공개용 README, CITATION.cff, CONTRIBUTING.md 초안 검토 | 저자 | ☐ |
| 0-6 | `requirements.txt` + `environment.yml` 버전 고정 + 테스트 | 저자 | ☐ |
| 0-7 | 데이터 패키지 README (컬럼 schema, 단위, 출처 매핑) 작성 | Claude | ☐ |
| 0-8 | Per-paper digitization metadata `tar.gz` 생성 + 검수 | 저자 | ☐ |

---

## Phase 1 — 게재 수락 직후 (DOI 발급 ≤ 1주)

| # | 작업 | 절차 |
|---|---|---|
| 1-1 | 본문 proof 단계에서 Zenodo DOI placeholder 교체 | Elsevier proof 인터페이스 |
| 1-2 | GitHub repo 공개 전환 (private → public) | Repo Settings → Change visibility |
| 1-3 | `v1.0-published` Git tag 생성 + Release 등록 | `git tag -a v1.0-published -m "..." && git push --tags` |
| 1-4 | Zenodo가 GitHub Release 자동 archive → **code DOI** 발급 확인 | Zenodo dashboard |
| 1-5 | Zenodo dataset record 별도 생성 + 데이터 ZIP 업로드 → **data DOI** 발급 | Zenodo new upload |
| 1-6 | 두 DOI를 README, CITATION.cff, LICENSE 파일에 일괄 치환 | `grep -r XXXXXXX` 후 sed |
| 1-7 | repo 최상위 `README.md` 의 IJHMT DOI / paper 인용 정보 갱신 | 직접 수정 |
| 1-8 | DOI 등록 확인 → Elsevier에 "Data citation update" 요청 (필요 시) | author proof |

---

## Phase 2 — 추가 가시성 작업 (게재 후 1개월 이내, 선택)

| # | 작업 | 효과 |
|---|---|---|
| 2-1 | **Papers with Code** 등록 (`paperswithcode.com/paper/...`) | ML 커뮤니티 노출 |
| 2-2 | **ML4Sci / Hugging Face Datasets** 카탈로그 등록 | 데이터셋 발견성↑ |
| 2-3 | **Google Dataset Search**에 schema.org/Dataset JSON-LD 메타데이터 노출 | 검색 색인 |
| 2-4 | UNIST 기관 리포지토리 (ScholarWorks) 후속 게시 | 기관 가시성 |
| 2-5 | KAIST/SNU 등 한국 비등 연구 그룹에 dataset 공유 메일 | 인용 유도 |
| 2-6 | Twitter/LinkedIn 짧은 announcement (figure-7 thumbnail) | SNS 트래픽 |

---

## 공개 패키지 디렉터리 구조 (목표)

```
github.com/UNIST-ITEL/pinn-onb01/
├── README.md                  # 공개용 (현재 README_PUBLIC.md → 게재 후 이동)
├── LICENSE-CODE               # MIT (이미 생성됨)
├── LICENSE-DATA               # CC-BY-4.0 (이미 생성됨)
├── CITATION.cff               # 게재 후 DOI 삽입
├── CONTRIBUTING.md            # 기여 가이드
├── .gitignore                 # raw PDF, .bak, *.zip 제외 (현재 상태 유지)
├── requirements.txt           # PyTorch 2.x, DeepXDE, CoolProp, etc.
├── environment.yml            # conda 환경
├── Makefile                   # make train / make figures / make hpo
│
├── 02_data/
│   ├── processed/
│   │   ├── README.md          # 컬럼 schema + 단위 + 출처 매핑
│   │   ├── boiling_curves.csv     # 1361 × 14
│   │   ├── onb_dataset.csv        # 82 × 12
│   │   └── surface_cards/         # 49 × YAML
│   └── raw/
│       └── digitization/      # per-paper WebPlotDigitizer .tar.gz
│
├── 03_model/
│   ├── src/                   # PyTorch + DeepXDE 소스
│   ├── configs/               # YAML hyperparameters
│   └── checkpoints/
│       └── ensemble_k10/      # deep ensemble K=10 (또는 Zenodo로)
│
├── 04_analysis/
│   ├── scripts/               # figure / table 재현 코드
│   ├── notebooks/             # Jupyter notebooks
│   └── figures/               # PNG 출력
│
└── 05_manuscript/
    └── (제외 — Elsevier 저작권)
```

### Zenodo Dataset record (별도 DOI)

```
PINN-ONB01-dataset-v1.0.zip
├── README.md
├── LICENSE                    # CC-BY-4.0
├── boiling_curves.csv
├── onb_dataset.csv
├── surface_cards/             # 49 YAML
├── digitization/              # per-paper WPD metadata
└── checksums.sha256
```

---

## Manuscript proof 단계 체크리스트

| # | 작업 |
|---|---|
| M-1 | `main.tex` Data availability 섹션의 Zenodo DOI placeholder 교체 (이미 plain prose로 작성됨, 발급된 DOI로 lightly edit) |
| M-2 | `references.bib`에 dataset 인용 항목 추가 (선택) |
| M-3 | Supplementary `supplementary.tex`에서도 동일한 DOI 참조 정합성 확인 |
| M-4 | Highlights, Abstract에 GitHub URL이 들어갈 필요 없음 (Data availability에만 있음) |

---

## 책임자 / 액션

| 액션 | 담당자 |
|---|---|
| GitHub org 생성·관리 | Jaeseon Lee |
| Zenodo 업로드 | Jaeseon Lee |
| Code packaging / Makefile | Gyuchang Kim |
| Dataset README / digitization metadata | Eunjeong Ko |
| Notebook 정리 | Yujin Kim |
| 본문 DOI 삽입 (proof) | Jaeseon Lee |

---

## 위험 관리

| 위험 | 대응 |
|---|---|
| Reviewer가 게재 전 데이터/코드 검토 요구 (편집자 권한으로 가능) | private repo의 read-only collaborator 초대 또는 Zenodo "restricted access" record로 대응 |
| 원본 figure 저작권 침해 우려 | raw PDF는 절대 redistribute 하지 않음, digitization metadata는 자체 생성물이므로 안전 |
| Zenodo 파일 크기 한도 (record당 50 GB) 초과 | 현 추정 ≤ 200 MB이므로 여유 충분 |
| GitHub Action / CI 비용 | 학술 repo는 GitHub Free org 충분 |

---

## 참고 자료

- Elsevier Research Data 가이드: https://www.elsevier.com/authors/tools-and-resources/research-data
- Zenodo $\leftrightarrow$ GitHub 통합: https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content
- CITATION.cff 스펙: https://citation-file-format.github.io/
- CC-BY-4.0: https://creativecommons.org/licenses/by/4.0/
- MIT License: https://opensource.org/license/mit/
