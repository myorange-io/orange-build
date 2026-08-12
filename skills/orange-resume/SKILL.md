---
name: orange-resume
description: Orange Build IA 프로젝트의 PLAN.md에서 completion_level, current_step과 승인 상태를 읽고 정확한 지점부터 이어간다. 웹앱·AI 작업 스킬·자동화의 실제 파일과 검증 증거를 대조하며, 승인 전 수정하지 않고 결과 검토 뒤 다음 개선을 진행한다. "이어하기", "어디까지 했지", "계속하자", "오렌지 빌드 이어서" 같은 요청에 사용한다.
---

# Orange Build — Resume

세션이 끊긴 프로젝트를 요구사항 수가 아니라 현재 IA 단계와 사람의 승인 상태에서 복원한다.
`package.json`이나 폴더 이름으로 진행 단계를 추측하지 않는다.

Codex에서 실행 중이면 `../orange-start/references/codex-gpt-5p6.md`를 읽는다. Claude Code에서는 현재
고성능 모델로 같은 계약을 적용한다. 이어서 반드시
`../orange-start/references/ia-collaboration.md`를 읽는다.

## 1. 현재 상태 읽기

다음만 먼저 확인한다.

- `PLAN.md`: `workflow`, `deliverable_kind`, `execution_profile`, `delivery_intent`,
  `completion_level`, `current_step`, 단계 상태, REQ·TEST, 최종 판정. `ai_skill`이면 `skill_scope`,
  `atomicity`, 한 문장 책임과 내장 평가 상태도 확인
- `SOURCE_PLAN.md`: 현재 STEP이나 원본 추적 누락이 의심될 때 관련 절만 확인
- `MEMORY.md`: 있으면 최종 검증 marker 수와 기록된 완료 수준
- `git status --short --branch`, `git log --oneline -12`
- 현재 결과물 증거
  - `web_app`: 선택한 수준의 로컬 실행 또는 공유 URL·실업무 결과
  - `ai_skill`: SKILL.md, 호스트별 등록 경로와 최근 새 작업 호출
  - `automation`: dry-run·공유 테스트·실제 run id와 결과 재조회

`PLAN.md`가 없으면 `orange-start`로 돌아간다. 최신 App 입력이나 자료 묶음이 있으면 가져오고,
없으면 아이디어부터 기획할 수 있다고 안내한다. `workflow: ia_collaborative`가 없거나 구형 `바로
시작할 순서`만 있으면 직접 구현하지 않고 초기 아이디어로 재기획한다.

## 2. 실제 상태 대조

`PLAN.md` 상태를 맹신하지 않는다. 최근 코드·테스트·결과가 앞서거나 뒤처졌다면 읽기 전용으로
대조한다. 승인 기록이 없다고 코드 존재를 승인으로 추정하지 않는다. 사용자 소유 변경은 되돌리지
않고, 상태 불일치를 짧게 알린 뒤 안전한 재개 지점을 고른다.

```text
📋 [결과물 이름] · [deliverable_kind] · [completion_level]
   현재: [STEP-NN · 상태]
   확인: REQ [PASS/전체] · TEST [TESTED/전체]
   결과: [로컬 결과 / URL / 스킬 호출 / run id / 아직 없음]
   다음: [승인 요청 / 구현 / 결과 검토 / 최종 검증]
```

`PARTIAL`, `INFERRED`, 실패, `FACT_UNVERIFIED`는 PASS 수에 넣지 않는다.

## 3. 상태별 재개

- `AWAITING_APPROVAL`: 현재 단계의 확인할 변화·완료 확인·제외 범위를 보여주고
  `이 단계부터 만들까요?`라고 묻는다. 단 `ai_skill`의 `atomicity: WAITING_USER`면 서로 독립적인
  인지 과업 2~3개와 추천안을 먼저 하나만 확인한다. 답을 기다리며 프로젝트 파일을 수정하지 않는다.
- `IN_PROGRESS`: 승인된 범위를 실제 파일·테스트와 대조하고 구현을 이어간다.
- `AWAITING_REVIEW`: 관찰 가능한 결과와 검증을 다시 보여주고 `이대로 다음 개선 / 현재 결과 수정 /
  구현 방향 다시 정하기` 중 하나를 받는다.
- `APPROVED`: 다음 STEP이 있으면 그 단계를 `current_step`으로 정해 승인부터 시작한다. 없으면 선택한
  `completion_level`의 최종 검증으로 간다.
- `current_step: complete`: 최종 검증과 `MEMORY.md` marker를 대조하고 남은 것만 수행한다.

구현 route는 다음과 같다.

- 기획 계약 재생성 → `../orange-start/references/phase-plan.md`
- 준비·연결 → `phase-preflight.md`, `helpful-tools.md`, `phase-connect.md`
- `web_app` → `phase-build.md`
- `ai_skill` → `phase-build-skill.md`
- `automation` → `phase-build-automation.md`
- 모든 단계 승인 → `verification-loop.md`, `phase-verify.md`
- 선택한 완료 수준 PASS, marker 없음 → `memory-log.md`

`ai_skill`인데 `skill_scope: atomic` 또는 `atomicity: CONFIRMED`가 없으면 과거 승인만으로 구현을
재개하지 않는다. `phase-plan.md`에서 원본을 보존한 채 인지 과업 지도와 단일 과업 계약을 보강하고
현재 STEP 승인으로 돌아간다.

다음 항목이 `FACT_UNVERIFIED`이면 `../orange-start/references/product-truth-gate.md`로 현재 근거,
권장안과 대안의 영향을 보여주고 값 하나를 확인한다. 확인 전에는 관련 공개 문구·계산·외부 실행을
완료로 처리하지 않는다.

사용자가 상태 조회만 요청한 것이 아니면 현황 보고 뒤 해당 지점부터 계속한다. 다만 현재 단계 승인과
배포·외부 발송·실데이터 변경·자동화 활성화의 실행 직전 확인은 생략하지 않는다.

## 4. 호스트와 완료 수준

AI 스킬은 현재 호스트에 맞는 개인 경로를 확인한다.

- Codex: `$CODEX_HOME/skills`, 기본 `~/.codex/skills`; `$스킬이름` 또는 자연어 호출
- Claude Code: `~/.claude/skills`; `/스킬이름` 또는 자연어 호출

`local`이면 현재 호스트의 새 작업 호출 또는 로컬 핵심 흐름·dry-run에서 검증한다. `shared`이면 공유
URL·격리 설치·공유 테스트 환경, `real_work`이면 실제 자료·계정·업무 결과와 복구 절차가 필요하다.
낮은 수준의 증거로 높은 수준을 완료 처리하지 않는다.

## 5. 기록

단계 상태 전이, 중요한 사람 결정, 실제 blocker handoff, 최종 판정에서만 `PLAN.md`를 갱신한다.
평범한 수정과 테스트마다 문서를 고치지 않는다. 선택한 완료 수준을 검증한 뒤
`memory-log.md`의 최종 검증 marker 블록을 정확히 하나 생성하거나 갱신한다. 기존 블록이 있으면
append하지 않는다.
