---
description: 논문(PDF/DOI/URL/arXiv ID)을 받아 paper-card-extractor로 카드 생성 후 paper_database.md에 추가
argument-hint: <PDF 경로 | DOI | URL | arXiv ID>
---

# /add-paper — 논문 카드 추가

본 명령은 **paper-card-extractor** 서브에이전트를 호출하여 입력 논문을 표준화된 카드 형식으로 추출하고 `01_survey/paper_database.md`에 append합니다.

## 입력 (`$ARGUMENTS`)

다음 중 하나:
- **로컬 PDF 경로**: 예) `01_survey/pdfs/HSU_JHT_1962_NucleationCavity.pdf`
- **DOI**: 예) `10.1016/j.ijheatmasstransfer.2011.06.001`
- **arXiv ID**: 예) `1907.04502` 또는 `arXiv:1907.04502`
- **URL**: 예) `https://doi.org/10.1115/1.4050542`

여러 입력은 공백·콤마로 구분하여 한 번에 처리할 수 있습니다 (각각 별도 카드로 추가).

## 처리 흐름

1. **입력 분기**:
   - PDF 경로 → `Read` 또는 `02_data/scripts/pdf_text.py`로 본문 추출
   - DOI/URL → `WebFetch`로 메타데이터 + abstract 가져오기
   - arXiv ID → `https://arxiv.org/pdf/{ID}.pdf`에서 `curl`로 다운로드 후 `01_survey/pdfs/`에 저장 → 본문 추출

2. **PDF 명명 규칙** (다운로드 시 적용):
   `{1저자성 대문자}_{저널약어}_{연도}_{핵심키워드}.pdf`
   예: `LU_SIAM_2021_DeepXDE.pdf`, `RAISSI_JCP_2019_PINN.pdf`, `BETZ_IJHMT_2013_Superbiphilic.pdf`

3. **paper-card-extractor 호출**: `.claude/agents/paper-card-extractor.md`의 카드 형식·작업 절차 그대로 따름.

4. **카드 추가 위치**: `01_survey/paper_database.md` 파일 끝의 "## 누적 카드" 섹션. 카드 사이 빈 줄 1개.

5. **(선택) 갭 매트릭스 갱신 트리거**: 새 카드가 5편 이상 누적되면 `gap-matrix-mapper` 에이전트 호출 권장 (자동 호출하지 않음 — 사용자 확인 필요).

## 사용 예

```
/add-paper 01_survey/pdfs/HSU_JHT_1962_NucleationCavity.pdf
/add-paper 10.1016/j.ijheatmasstransfer.2011.06.001
/add-paper arXiv:1907.04502
/add-paper 10.1063/1.4791682, arXiv:1211.1602
```

## 카드 작성 후 보고 형식

각 카드마다 한 줄로 보고:
```
추가됨: [제목] — 분류: [상관식/표면개질/PINN/...], 활용도: [직접 비교/방법론 참조/데이터 참조]
```

여러 논문 처리 시 마지막에 합계와 누적 카드 수도 보고:
```
이번 추가: 3편 · 누적 카드: 14편 · 다음 권장: gap-matrix-mapper 갱신
```

## 주의사항

- 페이월 차단 시 (Wiley/ASME/Elsevier 403) — abstract 기반 카드만 작성하고 PDF 미확보 명시. 사용자에게 UNIST 기관 접속 또는 직접 PDF 업로드 권장.
- 추측 금지 — 본문에 명시되지 않은 항목은 "명시 없음"으로 표기.
- 사용자 입력이 모호하거나 검색을 요구하면 `survey-search` 에이전트로 위임 (본 명령은 카드 작성 전용).

## 인자

$ARGUMENTS
