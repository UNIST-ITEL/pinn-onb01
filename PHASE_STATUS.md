# PINN-ONB01 — Phase 진척 상태

**최종 갱신:** 2026-05-18 (D-시리즈 + E6-E12 보강 + 컨설팅 02 + bib 검증 완료)
**전체 진척:** Phase 1-4 완료 / Phase 5 (논문) ~99.5% — 투고 패키지 준비 완료

---

## Phase 1-4 (요약, 변동 없음)

| Phase | 산출물 | Go/No-Go |
|---|---|---|
| 1. Survey | 25 paper cards, gap matrix v5 | ✅ |
| 2. Data | 1,361 boiling pts / 82 ONB labels / 49 surfaces / 4 fluids | ✅ |
| 3. Modeling | `baseline_phaseDbal` (FiLM, 24,005 params) | ✅ |
| 4. Inverse | Hsu inverse 48 surfaces, Simpson's paradox 발견 | ✅ |

### 핵심 결과
- **RMSE 3.42 K, R² +0.44** on n=77 (Basu 대비 −53%, 냉매 −65~67%)
- Physics consistency: 8/9 PASS, 평균 |ρ|=0.90
- Ensemble UQ (K=10): coverage **98.7%**, σ_total 4.09 K (epistemic dominant)
- Hsu inverse mean r_c **3.21 μm**, 60% in [1,100] μm physical band

---

## Phase 5 — 논문 작성 (현 99%)

### Manuscript 구조 재편 완료 (2026-05-17)
사용자 피드백 "패러그래프마다 섹션타이틀 자제, 단락 연결" 반영.

| Section | 이전 | 현재 |
|---|---|---|
| §1 Introduction | 6 subsec | **0 subsec** (단일 흐름) |
| §2 Formulation | 6 subsec | **3 subsec** (Governing+BC / Hsu / Non-dim) |
| §3 Data | 6 subsec | **3 subsec** (Curation / Cards+ONB / Stats) |
| §4 Architecture | 5 subsec | **2 subsec** (Encoder+Backbone / Loss+Training) |
| §5 Results | 6 subsec + 16 \paragraph | **3 subsec + 0 \paragraph** |
| §6 Conclusions | 5 subsec | **0 subsec** (단일 흐름) |
| **합계** | 34 subsec + 16 \para | **11 subsec + 0 \para** |

기존 서브섹션 라벨은 새 헤딩에 alias로 보존 → 모든 `\ref{subsec:...}` 작동.

### 워드 카운트 (재구조화 + native-tone 후)

| Section | 단어 (`wc -w`) |
|---|---|
| 0. Abstract | 222 |
| 1. Introduction | 923 |
| 2. Formulation | 855 |
| 3. Data | 933 |
| 4. Architecture | 1,271 |
| 5. Results | 2,620 |
| 6. Conclusions | 520 |
| **본문 합계** | **7,122** (IJHMT 6,000-8,000 적합) |

### 문체 / 영어 품질
- **4:6 long:short sentence mix** 6개 섹션 일괄 적용
- **Native English tone review (B7)** 6개 섹션 — 128 발견사항 중 **127 적용** (1 DEFERRED 해결: §4 w_ONB ramp Option 2)
- 카테고리별 보고서 6개 파일 `04_analysis/native_tone_review_sec{1..6}.md`
- UK→US spelling 추가 검출: `internalised`/`artefact`/`coloured` ×2 / `summarised` → 미국식
- section-drafter agent에 영구 style constraint 등록 (`.claude/agents/section-drafter.md`)

### Frontmatter 완성
- 저자: Jaeseon Lee*, Gyuchang Kim, Eunjeong Ko, Yujin Kim (UNIST ITE Lab)
- Correspondence: JaeseonLee@unist.ac.kr, Tel +82-52-217-2342
- Highlights 5 bullets, 모두 **85자 한도 내**
- Abstract 222 단어 (목표 200-250)
- Nomenclature: Roman 28 + Greek 16 + Abbrev. 20 (Spearman ρ, ε, α_ℓ, β_ℓ, ν_ℓ, Bo, Ja, Nu_L, Ra_L, Gr_L, d_z, z_s, F(θ) 추가)

### Backmatter 완성
- Acknowledgements (NRF 2건 + KETEP 1건)
- CRediT author contributions (4명 역할 분담)
- Data availability statement (open-source 약속)
- Declaration of competing interests

### Cover letter (별도 PDF)
- `05_manuscript/cover_letter.tex` → `cover_letter.pdf` (2페이지, IJHMT 표준)

### Figure 품질 (E14-17 점검)
- Main figures **9개** (모두 inline `\cref{}` 인용)
- Supplementary figures **10개** + 1 table
- **모두 300 dpi** (Python PIL 검증)
- 3개 포맷 보유: PNG (preview) / PDF (compile) / EPS (publisher)
- **Figure 1 재생성** (Level 1 composite): 단일 PNG들의 중복 (a)(b)(c) 라벨 제거, 데이터 기반 새로 그림
- **Figure 7 (f) 재생성**: histogram+scatter 2-subplot 중복 제거

### Bibliography (`references.bib`)
- 28 entries 유지, bibtex-curator 정리 (B8)
- BibTeX 경고: **5건 → 1건** (잔여: `perez2018film` empty pages, AAAI online-only이므로 본질적)
- DOI 보강: 모두 이미 보유
- 인용 키 main.tex 28개 ↔ bib 28개 완전 일치

### LaTeX 빌드 (최종)

| 파일 | 페이지 | 크기 | Errors | Warnings | Box |
|---|---|---|---|---|---|
| **main.pdf** | **33** | 1.48 MB | 0 | 0 LaTeX | 1 minor (31pt overfull) |
| **supplementary.pdf** | 6 | 1.28 MB | 0 | 0 | 0 |
| **cover_letter.pdf** | 2 | 89 KB | 0 | 0 | 0 |

`\emergencystretch=5em` 추가로 overfull 2/3 해결, §2 잔여 1건은 시각상 1cm 정도로 minor.

### siunitx 콤마 처리 통일
- `group-digits=integer` 추가 → 소수부 콤마 제거 (이전 `0.100,0` → `0.1000`)
- 정수 천단위 콤마 유지 (`24,005`, `1,361`)
- Highlights/Abstract 모두 `\num{}` 통과로 통일

### 세 세대 백업 보존
- `.bak_presentence`: 첫 단문 시범 패스 전
- `.bak_pre_nativetone`: native-tone 적용 전
- `.bak_pre_restructure`: 서브섹션 재구조화 전

---

## 2026-05-18 추가 작업 (D-시리즈 + 정밀 검수)

### 컨설팅 보고서 02 반영
- §3 FC-77 제외 사유 학술적 방어 1단락 추가
- Title 변경: 사용자 결정 — 현재 유지

### 신규 인용 3건 CrossRef 검증
- `jalili2025pinn`: IJHMT 241, 126680 (2025), DOI 10.1016/j.ijheatmasstransfer.2025.126680
- `huang2024bubble`: IJMF 179, 104928 (2024) — Huang/Chang/Suh/Mudawar/Won/Kharangate
- `li2025cryogenic`: ASME J Heat Mass Transf 147(4), 041603 (2025), DOI 10.1115/1.4067339

### D11 — Reviewer Rebuttal 정식 문서
- 파일: `04_analysis/reviewer_rebuttal.md` (35 KB, 4,650 단어, 20 questions)
- Top-5 (컨설팅 01+02 식별) + Methodology 5 + Data/Validation 5 + Generalization 5
- 각 질문당 200-350 단어 학술 영어 Rebuttal + manuscript reference + action item
- 15/20 본문이 이미 강력 대응, 5건만 추가 보강 권장 (Appendix B)

### D12 — Supplementary HPO 표 (§S5)
- Optuna TPE 30 trials (21 성공 / 9 가지치기), 3.1시간 M1 CPU
- Top-5 trials 표 (rank/trial#/val_RMSE/test_RMSE/4 weights)
- Importance: hidden_dim 0.30 > lr_Adam 0.22 > w_data 0.21 > d_z 0.17 > w_ONB 0.07

### D13 — Supplementary Phase progression 표 (§S6)
- A(concat) 6.20 → B(FiLM) 5.50 → C/C-A/C-D 7-8.6 → D 7.04 → **Dbal 3.42** → E 9.50
- Over-regularization 민감도 입증

### D14 — Author info
- Jaeseon Lee ORCID **0000-0003-1996-6086** main.tex frontmatter 추가
- 공저자 3명 ORCID: TBD (submission portal 입력 시 수집)

### D15 — Graphical Abstract
- `05_manuscript/figures/graphical_abstract.{png,pdf,eps}` 16×5.5 cm, 300 dpi
- 3-패널: 데이터셋 / 아키텍처 / Forward parity headline

### E6-E9 무결성 점검 (모두 통과)
- E6 표 캡션 위치: 10/10 above tabular ✅
- E7 cross-ref: 0 undefined, 0 broken ✅
- E8 nomenclature: K (Zuber), p_r (reduced pressure) 추가 (현재 Roman 34 + Greek 17 + Abbrev 20)
- E9 인용 매핑: 31/31 완전 매칭 ✅

### E12 LanguageTool grammar 패스
- 6,811 단어 본문 분석, 30 issues, 3 actionable 수정:
  - §1: "consequences including" → "consequences that include"
  - §4: "checkpoint so" → "checkpoint, so"
  - §5.2: "(best classical, Basu et al.)" → "(the best classical correlation, ...)"

### 투고 패키지 (`05_manuscript/SUBMISSION/`)
- main.pdf (36p), supplementary.pdf (7p), cover_letter.pdf (2p), graphical_abstract.pdf
- figures_pdf/ (9 figures, fig01-fig09 본문 번호 일치)
- ZIP 3.7 MB

---

## 남은 작업 (Optional, 외부 단계)

| 항목 | 시간 | 효과 |
|---|---|---|
| Reviewer Appendix B 5건 본문 사전 보강 (Q1/Q4/Q6/Q9/Q11) | 1시간 | 사전 방어 |
| Native-speaker / professional editing service | 외주 | 영문 자연스러움 |
| Co-author / 지도교수 검토 | 외부 | 학술 review |
| §2 잔여 overfull 31pt fine-tune | 30분 | cosmetic |
| 백업 파일 정리 (3 세대) | 사용자 결정 | 리포 정리 |
| 누적 변경분 git commit (D-시리즈 이후) | 5분 | 버전 관리 |
| Git tag `v1.0-submitted` | 5분 | submission 시점 마커 |
| Git remote(GitHub) push | 사용자 | 외부 백업/공유 |
| 데이터셋 Zenodo/OSF DOI 발급 | 사용자 | open-source 약속 실행 |
| 공저자 ORCID 수집 | 사용자 | submission portal 메타데이터 |
| IJHMT submission portal 업로드 | 사용자 | 최종 |

---

## 빠른 빌드 명령

```bash
cd /Users/myhomemini/Library/CloudStorage/OneDrive-개인/Projects/PINN-ONB01/05_manuscript
export PATH="/Library/TeX/texbin:$PATH"

# 본문
latexmk -pdf main.tex

# Supplementary
cd supplementary && latexmk -pdf supplementary.tex && cd ..

# Cover letter
pdflatex cover_letter.tex

# Figure 재생성 (필요시)
python ../04_analysis/scripts/compose_figures.py
python ../04_analysis/scripts/compose_composites.py
```

## 핵심 자료 위치

```
01_survey/paper_database.md           # 25 paper cards
01_survey/gap_matrix.md
02_data/processed/onb_dataset.csv     # 82 ONB
02_data/processed/boiling_curves.csv  # 1,361 pts + r_c_um 컬럼
02_data/surface_cards/_index.md       # 49 surfaces
03_model/checkpoints/baseline_phaseDbal/  # 최종 모델 (RMSE 3.42 K)
03_model/checkpoints/ensemble_phaseDbal/  # K=10 (coverage 98.7%)
03_model/configs/baseline_phaseDbal.yaml
04_analysis/native_tone_review_sec{1..6}.md  # 128 발견 + 적용 기록
04_analysis/scripts/compose_composites.py
05_manuscript/main.tex                 # elsarticle, 33 pages
05_manuscript/cover_letter.tex         # 2 pages
05_manuscript/sections/                # 6 body sections + abstract/highlights/nomenclature
05_manuscript/references.bib           # 28 entries
05_manuscript/figures/                 # 22 단일 + 2 composite, 300 dpi
05_manuscript/supplementary/
  supplementary.tex                    # 10 supp figs + 1 supp table
```
