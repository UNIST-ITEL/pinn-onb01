---
description: Phase 1.5 lab data 출처를 새로 등록 — 폴더 생성 + inventory entry + bib 추가
argument-hint: <source_name> [--doi <DOI>] [--description "<text>"]
---

# /add-lab-source — Lab 데이터 출처 등록

본 명령은 Phase 1.5 의 새 lab data 출처를 표준 위치에 등록합니다.

## 입력 (`$ARGUMENTS`)

```
<source_name>             폴더 식별자 (snake_case, 예: "lee_2023_ichmt", "inhouse_corrosion")
--doi <DOI>               (선택) 공개 논문 시 DOI
--description "<text>"    (선택) 한 줄 설명
```

## 처리 흐름

1. **폴더 생성**:
   ```
   phase1p5_inhouse_augmentation/data/raw/lab/<source_name>/
   ```

2. **빈 README 자동 생성**:
   `<source_name>/README.md` — 출처 설명, 측정 조건, 원본 파일 목록 placeholder

3. **Inventory 항목 추가**:
   `phase1p5_inhouse_augmentation/data/lab_data_inventory.md` 의 해당 출처
   섹션에 빈 양식 row 추가 (없으면 파일 생성)

4. **DOI 제공 시 bibtex-curator 호출**:
   `phase1p5_inhouse_augmentation/manuscript/references.bib` 에 entry 추가
   (CrossRef 메타데이터 자동 fetch)

5. **Surface card placeholder 생성** (선택, 단일 표면 출처 시):
   `phase1p5_inhouse_augmentation/data/surface_cards/SFC-XXX.yaml.template`
   다음 가용 ID 자동 할당

## 사용 예

```
/add-lab-source lee_2023_ichmt --doi 10.1016/j.icheatmasstransfer.2023.107072 --description "Femtosecond laser periodic ripple"
/add-lab-source inhouse_corrosion --description "Cu 부식 친수화 표면 (미공개)"
```

## 출력 보고

```
✓ 폴더: phase1p5_inhouse_augmentation/data/raw/lab/lee_2023_ichmt/
✓ README placeholder 생성
✓ Inventory 항목 추가 (lab_data_inventory.md § lee_2023_ichmt)
✓ Bib entry: @article{lee2023_ichmt, ...} (DOI 검증 완료)
다음 단계: figure-digitizer 로 raw 데이터 추출 또는 CSV 직접 import
```

## 주의사항

- `<source_name>` 은 기존 디렉토리와 충돌 시 사용자 확인 후 진행.
- DOI 미제공 시 bib entry skip (Phase 1.5 paper 작성 시 사용자가 직접 추가).
- 미공개 출처도 `inhouse_*` prefix 권장하여 식별 일관성 유지.

## 인자

$ARGUMENTS
