# UNIST-ITEL GitHub Org + Zenodo 연동 셋업 가이드

**작성일**: 2026-05-18
**대상**: PINN-ONB01 공개 release 준비 (수락 후 활성화)
**사용자 정보**:
- Email: `leejs92@gmail.com`
- ORCID: `0000-0003-1996-6086`
- 결정된 repo URL: `https://github.com/UNIST-ITEL/pinn-onb01`
- 데이터 license: CC-BY-4.0 / 코드 license: MIT

---

## 단계 0 — 전제 조건 점검

| 항목 | 확인 방법 | 필요 시 조치 |
|---|---|---|
| 개인 GitHub 계정 | <https://github.com/login> 접속 | 없다면 `leejs92@gmail.com`으로 가입 |
| 개인 GitHub 2FA 활성화 | Settings → Password and authentication | 반드시 켜기 (org 소유자는 2FA 필수 권장) |
| ORCID 확인 | <https://orcid.org/0000-0003-1996-6086> | 공개 프로필 상태 확인 |
| 공동저자 GitHub 계정 | Gyuchang Kim, Eunjeong Ko, Yujin Kim | 각자 개별 가입 필요 |
| 로컬 git config | `git config user.email` | `leejs92@gmail.com` 또는 GitHub-noreply 이메일 권장 |

---

## 단계 1 — GitHub Organization (UNIST-ITEL) 생성

### 1.1 Organization 만들기

1. <https://github.com/account/organizations/new> 접속
2. **Free plan** 선택 ("Create a free organization")
3. 입력값:
   - Organization account name: `UNIST-ITEL`
     - 만약 이미 사용 중이면 대안: `unist-itel`, `ITEL-UNIST`, `UNIST-ThermalLab`
   - Contact email: `JaeseonLee@unist.ac.kr`
   - This organization belongs to: **A business or institution** 선택
   - Business/Institution name: `Ulsan National Institute of Science and Technology (UNIST)`
4. 인증 후 "Create organization" 클릭

> **주의.** GitHub Free plan으로도 public repo 무제한, 무료 Actions 분량 충분.
> 학술 OSS 목적이라면 GitHub Teams 유료 플랜 불필요.

### 1.2 Organization 기본 설정

Organization 페이지 진입 → Settings 탭:

- **Profile**
  - Display name: `Innovative Thermal Engineering Laboratory, UNIST`
  - Description: `Pool/flow boiling, surface engineering, and physics-informed ML research at UNIST`
  - URL: `https://your-lab-website.unist.ac.kr` (있다면)
  - Location: `Ulsan, Republic of Korea`
- **Member privileges** → Base permissions: `Read` 권장 (기본 read-only)
- **Two-factor authentication** → "Require two-factor authentication for everyone" 활성화 권장
- **Repository visibility** → "Members can create public repositories" 활성화

### 1.3 멤버 초대

People → Invite member:

| 역할 | 멤버 | GitHub username | 권한 |
|---|---|---|---|
| Owner | Jaeseon Lee | _your_github_| Owner (default) |
| Member | Gyuchang Kim | _to invite_ | Member (read) |
| Member | Eunjeong Ko | _to invite_ | Member (read) |
| Member | Yujin Kim | _to invite_ | Member (read) |

> 공동저자들은 본인의 GitHub 계정으로 초대 이메일을 수락해야 함.

---

## 단계 2 — `pinn-onb01` Repo 생성

### 2.1 Repo 만들기

1. UNIST-ITEL org 페이지 → **New repository**
2. 입력값:
   - Repository name: `pinn-onb01`
   - Description: `Surface-Conditioned Physics-Informed Neural Network for Pool-Boiling ONB (IJHMT 2026)`
   - Visibility: **🔒 Private** *또는* **🌐 Public** (사용자 결정 — 본 프로젝트는 2026-05-18 부터 **Public** 으로 운영. Zenodo가 private repo를 보려면 OAuth 권한을 `repo` 전체 스코프로 재인증해야 하며, IJHMT는 single-blind이므로 public 유지가 운영상 단순함)
   - Initialize: **체크하지 않음** (로컬 repo를 push 할 예정)
3. "Create repository" 클릭

### 2.2 로컬 → 원격 push

```bash
cd "/Users/myhomemini/Library/CloudStorage/OneDrive-개인/Projects/PINN-ONB01"

# 원격 추가 (HTTPS 또는 SSH 둘 중 하나)
git remote add origin https://github.com/UNIST-ITEL/pinn-onb01.git
#  또는 SSH:
#  git remote add origin git@github.com:UNIST-ITEL/pinn-onb01.git

# 푸시
git push -u origin main

# 검증
git remote -v
```

> **HTTPS vs SSH.** SSH 권장 (passphrase 1회 입력으로 끝). SSH 셋업이 없다면
> <https://docs.github.com/en/authentication/connecting-to-github-with-ssh> 참고.

### 2.3 Repo 설정 (수락 전 단계)

Settings 탭:

| 영역 | 설정 |
|---|---|
| **General → Default branch** | `main` 확인 |
| **General → Features** | Issues ✓, Discussions ✓ (선택), Wiki ✗ (불필요) |
| **Branches → Branch protection rules** | `main` 보호: PR review 필수, "Restrict who can push to matching branches" (release 직전 적용) |
| **Collaborators and teams** | 공동저자에게 Write 권한 부여 |
| **Secrets and variables** | (아직 불필요; Zenodo 연동 후 토큰 관리 시 활용) |

---

## 단계 3 — Zenodo 계정 + ORCID 연동

### 3.1 Zenodo 가입

1. <https://zenodo.org/signup> 접속
2. **"Sign in with ORCID"** 선택 (가장 추천 — ORCID 자동 연동)
3. ORCID 계정 `0000-0003-1996-6086` 로그인 → Zenodo 권한 승인
4. 가입 완료 후 Zenodo 프로필에 ORCID가 자동으로 연결됨

### 3.2 Zenodo 프로필 보강

<https://zenodo.org/account/settings/profile/> 에서:

- Display name: `Jaeseon Lee`
- Email: `leejs92@gmail.com` 또는 `JaeseonLee@unist.ac.kr`
- Affiliations: `Ulsan National Institute of Science and Technology (UNIST)`
- ORCID: 자동으로 연결됨 (확인)

---

## 단계 4 — Zenodo ↔ GitHub 통합

### 4.1 GitHub 권한 부여

1. Zenodo 로그인 → 우측 상단 username 클릭 → **GitHub** 메뉴
   - 또는 직접: <https://zenodo.org/account/settings/github/>
2. "Sign in with GitHub" → GitHub 인증 페이지로 이동
3. **Authorize zenodo** 클릭 (Zenodo가 GitHub repo 목록 + webhook 설치 권한 획득)
4. 이후 페이지에 사용자가 소속된 GitHub org/repo 목록이 나타남

### 4.2 `UNIST-ITEL/pinn-onb01` archiving 활성화

> **중요.** Org-owned repo의 경우 **org owner 또는 admin이 third-party
> application 사용을 허용**해야 보입니다.

#### 4.2.1 Org-level OAuth 허용 (한 번만)

1. GitHub → `UNIST-ITEL` org → Settings → **Third-party access** → **OAuth app policy**
2. "Remove restrictions" 또는 Zenodo 앱 개별 승인
3. 이후 Zenodo 페이지 새로고침 → `UNIST-ITEL/pinn-onb01` 목록에 등장

#### 4.2.2 Repo archiving 토글

1. Zenodo GitHub 페이지에서 `UNIST-ITEL/pinn-onb01` 옆 토글을 **ON**
2. Zenodo가 GitHub repo에 webhook을 자동 설치 (이후 모든 Release가 자동 archive됨)
3. **첫 Release 발행 전까지는 DOI 발급 안 됨** — 이는 정상

#### 4.2.3 검증

- GitHub repo Settings → Webhooks → `zenodo.org` webhook 존재 확인
- Webhook "Recent Deliveries" 탭에서 ping 성공 응답 (200 OK) 확인

---

## 단계 5 — DOI 사전 예약 (선택, Pre-reserve)

게재 수락 전에도 Zenodo는 DOI를 "사전 예약" 할 수 있어 cover letter / proof
단계에서 참조 가능합니다.

### 5.1 Code DOI 사전 예약 (GitHub Release 발생 전)

Zenodo가 GitHub-Release 시점에 자동 발급하는 방식 외에, Zenodo에서 새 Upload를
시작하면서 미리 DOI를 reserve 할 수 있습니다. 그러나 GitHub-Zenodo 통합을 사용할
경우, **release 직후 자동 발급**이 정석입니다. 따라서:

- **권장:** code DOI는 release 직전(`v1.0-published` tag 시) 자동 발급
- 사전 예약이 꼭 필요하면 별도 "manual upload" record를 만들어 DOI reserve 후
  acceptance 직후 메타데이터만 교체 (지원되긴 함)

### 5.2 Dataset DOI 사전 예약 (권장)

데이터셋은 GitHub-Release와 무관하므로 Zenodo에서 별도 record로 등록:

1. <https://zenodo.org/uploads/new> 접속
2. **"Reserve DOI"** 버튼 클릭 → DOI placeholder 발급
3. Upload type: **Dataset**
4. 필수 메타데이터 입력:
   - Title: `PINN-ONB01 pool-boiling ONB dataset (v1.0)`
   - Authors: 4명 (ORCID 포함)
   - Description: `02_data/processed/README.md` § 1-2 요약을 붙여넣기
   - License: **Creative Commons Attribution 4.0 International (CC-BY-4.0)**
   - Keywords: `pool boiling`, `onset of nucleate boiling`, `physics-informed neural network`, `surface engineering`, `Hsu criterion`, `heat transfer`
   - Related identifiers (수락 후 추가): paper DOI를 `is supplement to`로 연결
5. **Save (draft)** — 아직 publish 하지 않음 (file 업로드는 release 시점)
6. 발급된 DOI를 `02_data/processed/README.md`, `LICENSE-DATA`, `CITATION.cff`,
   `README_PUBLIC.md`, `main.tex` 의 `XXXXXXX` placeholder에 치환

> Draft 상태에서는 DOI가 활성화되지 않지만, publish 직후 영구화됩니다.

---

## 단계 6 — 수락 후 활성화 시퀀스

게재 수락 후 다음 순서로 실행:

```bash
# 0. 작업 디렉터리
cd "/Users/myhomemini/Library/CloudStorage/OneDrive-개인/Projects/PINN-ONB01"

# 1. proof 단계에서 받은 paper DOI를 placeholder에 치환
#    (예: 10.1016/j.ijheatmasstransfer.2026.123456)
PAPER_DOI="10.1016/j.ijheatmasstransfer.2026.123456"
DATASET_DOI="10.5281/zenodo.1234567"  # Zenodo가 draft → publish 시 발급

# 위 두 DOI로 placeholder 일괄 치환
grep -rl "XXXXXXX" 02_data/processed/README.md LICENSE-DATA LICENSE-CODE \
    CITATION.cff README_PUBLIC.md 05_manuscript/main.tex 05_manuscript/supplementary/
# 검토 후 sed 또는 수동 edit

# 2. PHASE_STATUS / 변경사항 commit
git add -A
git commit -m "Insert published-paper DOI and Zenodo dataset DOI"

# 3. Repo visibility 확인 — 본 프로젝트는 2026-05-18부터 이미 public이므로
#    이 단계는 스킵. private으로 운영한 사용자만 여기서 public 전환.
#    GitHub UI: Settings → Danger Zone → Change visibility → Make public

# 4. Tag and release
git tag -a v1.0-published -m "IJHMT v1.0 published version"
git push origin v1.0-published

# 5. GitHub UI에서 Release 생성
#    Releases → Draft a new release → Tag: v1.0-published
#    Title: "PINN-ONB01 v1.0 — IJHMT published version"
#    Description: Cite paper + dataset DOIs, link to Zenodo records
#    "Publish release" 클릭
#    → Zenodo가 자동으로 archive하고 code DOI 발급

# 6. Zenodo dataset record:
#    - 데이터 ZIP (boiling_curves.csv, onb_dataset.csv, surface_cards/, digitization/)
#      업로드
#    - draft에서 publish 클릭 → dataset DOI 활성화

# 7. 두 DOI를 README에 최종 반영 후 commit & push
git add README.md CITATION.cff
git commit -m "Activate Zenodo code DOI and dataset DOI"
git push
```

---

## 단계 7 — 사후 가시성 (선택)

| 작업 | URL | 효과 |
|---|---|---|
| Papers with Code 등록 | <https://paperswithcode.com/sota> | ML 커뮤니티 노출 |
| ML4Sci 카탈로그 | <https://ml4sci.org/> | 과학 ML 그룹 노출 |
| Hugging Face Datasets | <https://huggingface.co/datasets> | 데이터셋 발견성 |
| OpenAIRE | <https://explore.openaire.eu/> | EU 공개과학 색인 |
| Google Scholar profile | Jaeseon Lee 프로필 | 인용 추적 |
| ResearchGate 게시 | (선택) | SNS 트래픽 |

---

## 검증 체크리스트

### Org/Repo 생성 후

- [ ] `https://github.com/UNIST-ITEL` 페이지 접속 가능
- [ ] 4명 멤버 모두 초대 수락 완료
- [ ] `https://github.com/UNIST-ITEL/pinn-onb01` 페이지 접속 (본 프로젝트는 public 운영)
- [ ] 로컬 git log와 원격 commit 일치 (`git log origin/main`)

### Zenodo 통합 후

- [ ] Zenodo 프로필에 ORCID `0000-0003-1996-6086` 연결됨
- [ ] Zenodo GitHub 페이지에 `UNIST-ITEL/pinn-onb01` 가시
- [ ] Repo Settings → Webhooks → zenodo webhook 활성 (Recent Delivery 200 OK)
- [ ] Dataset draft record DOI 사전 예약 완료 (Zenodo "DOI" 필드 확인)

### Release 직후

- [ ] GitHub Release `v1.0-published` 발행
- [ ] Zenodo "Recent Uploads" 에 code archive 자동 생성
- [ ] Code DOI 발급 (`10.5281/zenodo.XXXXXXX`)
- [ ] Dataset DOI 활성화 (`10.5281/zenodo.YYYYYYY`)
- [ ] 두 DOI가 README, CITATION.cff, LICENSE 파일에 반영됨
- [ ] Repo public 상태 유지 (또는 private 운영 시 여기서 전환)

---

## 자주 발생하는 이슈

| 증상 | 원인 / 조치 |
|---|---|
| Zenodo에서 org repo가 안 보임 | Org Settings → Third-party access에서 Zenodo OAuth 미허용. 위 § 4.2.1 참조 |
| Repo가 public 인데 webhook 응답이 401 | Zenodo 토큰 만료. Zenodo Settings → GitHub → 재인증 |
| `v1.0-published` tag 만 push, release UI에서 안 보임 | tag만 만들고 GitHub Release 객체를 안 만든 경우. Releases → "Draft a new release" → 기존 tag 선택 |
| Release 발행했으나 Zenodo archive 안 됨 | 1-2분 지연 가능. 그래도 안 되면 webhook recent delivery 확인 |
| Dataset draft에 file 업로드 후 DOI가 안 바뀜 | Draft DOI는 publish 전까지 reserved 상태로 동일 유지. publish 후 영구화 |
| ORCID record 자동 업데이트 안 됨 | Zenodo publish 시 ORCID 동기화는 24시간 이내. ORCID Settings에서 "Trusted Parties" 에 Zenodo 추가 확인 |
| Org-owned repo에 GitHub Free의 Action 분량 한계 | Public repo는 무료 무제한, Private repo만 분량 제한. 현재 release 후 public 으로 전환되므로 무관 |

---

## 외부 참고 자료

- **GitHub-Zenodo 공식 가이드**: <https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content>
- **Zenodo Help**: <https://help.zenodo.org/>
- **Making Your Code Citable** (GitHub Skills): <https://docs.github.com/en/repositories/archiving-a-github-repository>
- **Choose a License**: <https://choosealicense.com/>
- **Citation File Format (.cff) Spec**: <https://citation-file-format.github.io/>
- **DataCite DOI 검색**: <https://search.datacite.org/> (발급 후 검증용)
- **OpenAIRE 공개 데이터셋 가이드라인**: <https://www.openaire.eu/how-to-make-your-research-data-fair>

---

## 본 가이드의 위치 / 책임자

- **본 문서**: `SETUP_GITHUB_ZENODO_GUIDE.md` (repo root)
- **연관 문서**:
  - `RELEASE_CHECKLIST.md` — Phase 0/1/2 release timeline
  - `02_data/processed/README.md` — dataset citation 형식
  - `LICENSE-CODE` / `LICENSE-DATA` — 라이선스 전문
  - `CITATION.cff` — 기계 가독 인용 메타데이터
- **책임자**: Jaeseon Lee `<JaeseonLee@unist.ac.kr>` (Org Owner, Zenodo 계정 소유자)
