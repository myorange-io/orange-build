# Orange Build

[Orange Build App](https://build.myorange.io/)의 최신 기획서와 구현 자료를 가져오거나, 기획서가 없어도
같은 구조로 새 기획서를 만든 뒤 웹앱·AI 작업 스킬·자동화를 함께 구현하는 Codex·Claude Code 공용
플러그인입니다.

Orange Build 2.6.0은 IA(Intelligence Augmentation, 지능 증강) 방식으로 작동합니다. AI가 전체를 한
번에 대신 만들지 않습니다. 사람이 작은 결과를 확인하고 다음 방향을 선택하며 자신의 판단과 실행
능력을 확장하도록 한 단계씩 진행합니다.

```text
첫 번째 작은 완성 제안
→ “이 단계부터 만들까요?”
→ 승인받은 단계만 구현
→ 화면·파일·실제 호출·테스트로 결과 확인
→ 이대로 다음 개선 / 현재 결과 수정 / 구현 방향 다시 정하기
→ 선택한 완료 수준까지 반복·검증
```

## 공용 스킬

두 호스트가 저장소의 같은 `skills/` 원본을 사용합니다. Codex용과 Claude Code용 스킬 내용을 따로
복제하지 않습니다.

| 스킬 | 용도 |
|---|---|
| `orange-start` | 최신 기획서·자료 묶음·아이디어에서 IA 기획과 구현 시작 |
| `orange-resume` | `current_step`과 승인 상태에서 정확히 재개 |
| `orange-design` | 선택한 완료 수준에서 검증된 웹앱의 기능을 보존해 디자인 개선 |
| `orange-secure` | Orange Build 웹앱의 키·RLS·민감정보 위험 점검 |

호출 표기는 호스트에 맞춰 달라도 됩니다.

| Codex | Claude Code | 공통 자연어 |
|---|---|---|
| `$orange-start` | `/orange-start` | `오렌지 빌드 시작` |
| `$orange-resume` | `/orange-resume` | `오렌지 빌드 이어서` |
| `$orange-design` | `/orange-design` | `오렌지 디자인 개선` |
| `$orange-secure` | `/orange-secure` | `오렌지 보안 점검` |

## 설치와 업데이트

Codex와 Claude Code 설치는 서로 독립적입니다. 한쪽 설치가 다른 쪽의 전제조건이 아닙니다.

### Codex

```bash
codex plugin marketplace add myorange-io/orange-build
codex plugin add orange-build@orange-build
```

업데이트:

```bash
codex plugin marketplace upgrade orange-build
codex plugin add orange-build@orange-build
```

새 task에서 `$orange-start` 또는 자연어로 시작합니다. 설치 상태는 `codex plugin list`에서 확인합니다.
구형 `orange-build@personal`이 같은 스킬을 중복 제공하면 그 구형 항목만 제거합니다.

```bash
codex plugin remove orange-build@personal
```

### Claude Code

```bash
claude plugin marketplace add myorange-io/orange-build
claude plugin install orange-build@orange-build
```

업데이트:

```bash
claude plugin marketplace update orange-build
claude plugin update orange-build@orange-build
```

새 세션에서 `/orange-start` 또는 자연어로 시작합니다. 설치 상태는
`claude plugin details orange-build@orange-build`에서 확인합니다. 같은 스킬을 제공하는 구형 설치본이
있으면 그 항목만 제거합니다.

## 세 가지 시작 경로

### 최신 App 기획서

Orange Build App의 `orange-start용 복사` 내용을 새 프로젝트에 붙여넣습니다. 현재 형식에는 다음이
있습니다.

- `source: orange-build-app`, `contract_version: 2`, canonical `deliverable_kind`
- `TEST-01`~`TEST-03`
- `함께 구현할 순서`
- 각 단계의 `확인할 변화`, `완료 확인`, `이번 단계에서 하지 않을 것`

`orange-start`는 첫 번째 작은 완성을 요약하고 `이 단계부터 만들까요?`라고 묻습니다. 동의 전에는
코드·설정·테스트·프로젝트 문서를 수정하지 않습니다.

### 구현 자료 묶음

App에서 내려받은 다음 구조를 그대로 프로젝트에 둡니다.

```text
PLAN.md
IMPLEMENTATION_REQUEST.md
MATERIALS.md
materials/
```

원본 파일과 `MATERIALS.md`를 대조해 용도, 필수 규칙, 그대로 유지할 요소, 적용 위치, 열린 질문을
분석합니다. 사용자가 분석을 확인하거나 바로잡은 뒤에만 구현에 반영합니다. 필수 파일이 없으면
임의로 대체하지 않습니다.

### 기획서 없는 아이디어

`orange-start`를 호출하고 아이디어를 한두 문장으로 말합니다. 최신 App과 같은 순서로 진행합니다.

- 7개 phase, 후속 질문을 포함해 최대 10문항
- 한 번에 질문 하나
- 선택지 2~3개, 추천안을 첫 번째에 배치
- 구조화 질문 기능이 없으면 같은 선택지를 일반 대화로 제시
- 결과물 유형과 완료 수준까지 확인

생성되는 `SOURCE_PLAN.md`에는 대상·문제, 막히는 순간, 해결 방식, 결과물 유형, 사용 흐름, 핵심 기능,
포함·제외, 자료, AI·사람 역할, 성공·실패 기준, TEST 3개, 함께 구현할 순서, 가정이 들어갑니다.

### 구형 기획서

v1 또는 `함께 구현할 순서`가 없는 초기 v2 문서는 실행 계약으로 사용하지 않습니다. 결과물 표시
문자열을 추론하거나 호환 TEST를 만들지 않고, 확인 가능한 내용만 초기 아이디어로 가져와 최신 IA
인터뷰와 구조로 다시 생성합니다.

## IA 단계 상태

`PLAN.md`에는 다음 상태가 기록됩니다.

```yaml
workflow: ia_collaborative
completion_level: local | shared | real_work
current_step: STEP-NN
```

```text
AWAITING_APPROVAL → IN_PROGRESS → AWAITING_REVIEW → APPROVED
```

- 승인 전에는 읽기 전용 조사만 합니다.
- 승인 뒤 현재 STEP 범위의 기술 선택·오류 수정·테스트는 AI가 진행합니다.
- 결과 뒤 `이대로 다음 개선`을 골라야 다음 STEP으로 이동합니다.
- `현재 결과 수정`은 같은 단계에서 다시 구현·검토합니다.
- `구현 방향 다시 정하기`는 원본을 보존하고 현재·미래 단계를 다시 승인받습니다.
- 배포·외부 발송·실데이터 변경·자동화 활성화·비용·권한 확대는 단계 승인과 별도로 실행 직전에
  확인합니다.

## 완료 수준

| 수준 | 웹앱 | AI 작업 스킬 | 자동화 |
|---|---|---|---|
| `local` | 로컬 핵심 흐름과 관련 상태 | 현재 호스트 개인 경로 등록·새 작업 호출 | dry-run·중복 방지·재시도·로그 |
| `shared` | 실제 공유 URL과 대상 접근 | 격리 또는 대상 환경 설치·호출 | 공유 테스트 환경의 샘플 실행 |
| `real_work` | 실제 자료·계정·업무 결과와 복구 | 실제 업무 자료·도구 결과와 폴백 | 실제 계정·업무 결과와 중지·복구 |

AI 스킬 개인 등록 경로는 다음과 같습니다.

- Codex: `$CODEX_HOME/skills`, 기본 `~/.codex/skills`
- Claude Code: `~/.claude/skills`

선택한 수준보다 높은 배포나 활성화를 강요하지 않습니다. 반대로 로컬 build, source 경로를 알려준
스킬 실행, dry-run만으로 `shared`나 `real_work`를 완료했다고 말하지 않습니다.

## 실행 프로필과 검증

- `guided`: 새 폴더, 아이디어 인터뷰, 새 App 기획 구현
- `adaptive`: 코드·Git 원격·CI·배포 설정이 있는 기존 프로젝트

두 프로필 모두 같은 IA 승인과 안전 게이트를 사용합니다. adaptive는 기존 `AGENTS.md`, `CLAUDE.md`,
README, package script, CI와 배포 경로를 우선합니다.

Codex 교육 환경에서는 Codex의 모델 선택기에서 **GPT-5.6**을 사용합니다. 플러그인은 모델이나 추론 수준을
자동 변경하지 않습니다. 결과물·보호할 요구사항·완료 증거·사람이 결정할 경계를 명확히 주고 조사와
도구 선택은 맡깁니다. 같은 파일의 동시 수정과 배포·발송·삭제 같은 외부 변경은 한 흐름에서 순차
처리합니다. 참고: [Customization overview](https://learn.chatgpt.com/docs/customization/overview),
[GPT-5.6 model guidance](https://developers.openai.com/api/docs/guides/model-guidance?model=gpt-5.6).

검증은 TEST와 REQ를 양방향으로 연결하고 다음 증거를 구분합니다.

- `TESTED`: 계획한 입력과 행동을 실행해 기대 결과를 관찰
- `PARTIAL`: 일부 계층·분기 또는 대체 검증만 수행
- `INFERRED`: 코드·설정·HTTP 상태만 보고 추론

필수 항목은 선택한 완료 수준에서 `TESTED`일 때만 PASS입니다. 실패·누락은 승인받은 STEP 범위에서
자동 수정하고 다시 검증합니다. 범위·비용·권한·삭제·외부 발송처럼 책임이 달라지는 선택만 사람에게
돌립니다.

## 웹앱 배포와 디자인

`local`에는 배포를 요구하지 않습니다. `shared` 또는 `real_work`에서 배포가 필요하면 기존 경로를
우선하고, 새 Codex 프로젝트에서 Sites가 실제로 사용 가능하고 기획과 호환되면 Codex Sites를
검토합니다. 미지원 기능·Claude Code·기존 배포·정책 충돌에는 기존 경로나 Vercel/Supabase를
사용합니다. 배포 직전에 대상과 공개 범위를 다시 확인합니다.

기본 `orange-start`에서는 디자인 picker와 Stitch를 열지 않습니다. 선택한 완료 수준에서 기능과
최종 검증이 끝난 뒤 디자인을 개선하려면 `orange-design`을 별도로 호출합니다. 이때 기능·페이지·
데이터·REQ·TEST는 고정합니다.

새 GitHub 저장소가 실제로 필요하면 기본 `PUBLIC`으로 제안하고 생성 직후 visibility를 확인합니다.
기획서가 비공개를 요구하거나 개인정보·비밀값 위험이 있으면 생성 전에 공개 범위를 확인합니다.
`local`에는 원격 저장소를 강요하지 않습니다.

## 프로젝트에 남는 파일

- `SOURCE_PLAN.md`: 최신 App 원본 또는 IA 인터뷰로 만든 현재 기획서
- `PLAN.md`: IA STEP·REQ·TEST·완료 수준·증거 상태판
- `MEMORY.md`: 선택한 완료 수준 검증 뒤 최신 App 형식의 최종 marker 블록 하나
- `DESIGN.md`: `orange-design`에서 승인한 원칙이 있을 때만
- `CASE.md`: 사용자가 교육 사례를 요청했을 때만

`MEMORY.md`에는 `local | shared | real_work` 중 실제로 검증한 수준을 적습니다. 재검증에서는 두 번째
최종 기록을 추가하지 않고 기존 marker 블록을 갱신합니다.

## 라이선스

MIT · v2.6.0
