---
name: orange-resume
description: Orange Build로 진행 중인 웹앱·AI 작업 스킬·자동화 프로젝트의 PLAN.md, 검증 증거, 최근 커밋을 읽어 완료 수와 다음 미완료 요구사항을 알려주고 구현을 이어간다. "이어하기", "어디까지 했지", "계속하자", "오렌지 빌드 이어서" 같은 요청에 사용한다.
---

# Orange Build — Resume

세션이 끊긴 프로젝트를 `PLAN.md`의 요구사항 계약과 검증 증거에서 복원한다. `package.json`이나
`design/` 유무로 단계를 추측하지 않는다.

Codex에서 실행 중이면 `../orange-start/references/codex-gpt-5p6.md`를 먼저 읽어 GPT-5.6 실행
프로필을 복원한다. Claude Code에서는 이 파일을 건너뛰고 현재 고성능 모델로 같은 완료 계약을
적용한다.

## 1. 현재 상태 읽기

다음만 읽어 빠르게 파악한다.

- `PLAN.md` 전체: `deliverable_kind`, `execution_profile`, `delivery_intent`, REQ·TEST 계약, 최종 판정,
  `web_delivery_target`, 결과물 수량, 가정과 결정
- `SOURCE_PLAN.md`: PLAN 추적표에 누락 의심이 있을 때만 관련 절 확인
- `MEMORY.md`: 있으면 마지막 1~2개 항목과 최종 검증 marker 수
- `git status --short --branch`
- `git log --oneline -12`
- 결과물 증거
  - `web_app`: 기록된 production URL과 최근 배포
  - `ai_skill`: SKILL.md와 최근 validator/호출 결과
  - `automation`: 최근 dry-run/live run id와 트리거 설정

`PLAN.md`가 중간 구현마다 갱신된다고 가정하지 않는다. 최근 commit·코드·테스트·배포 결과가 PLAN의
상태보다 앞서 있으면 가장 가까운 검증을 다시 실행해 실제 상태를 판정하고 계속한다. 실제 blocker로
다시 중단하거나 최종 판정에 도달하기 전에는 이 판정을 문서에 전사하지 않는다.

`PLAN.md`가 없으면 `orange-start`로 돌아간다. 복사한 기획서가 있으면 가져오고, 없으면 아이디어
인터뷰부터 시작할 수 있다고 안내한다.

## 2. 짧은 현황 보고

REQ 상태를 실제로 세어 다음 형식으로 보여준다.

```text
📋 [결과물 이름] · [web_app / ai_skill / automation]
   상태: REQ [PASS 수]/[전체 수] · TEST [TESTED 수]/[전체 수]
   다음: [가장 앞선 TODO/FAIL REQ 또는 최종 검증]
   결과: [URL / 대표 스킬 결과 / run id / 아직 없음]
```

`MEMORY.md` 또는 `PLAN.md`의 마지막 중요 blocker가 있으면 필요할 때만 한 줄 덧붙인다. 테스트가 실패했거나 증거가
`PARTIAL`/`INFERRED`인데 체크박스만 완료인 경우 PASS 수나 TESTED 수에 넣지 않는다.

## 3. 재개 위치

아래 구현·검증 파일과 함께 `../orange-start/references/verification-loop.md`의 TEST↔REQ 매핑,
증거 등급, 결과물 수량 대조와 `../orange-start/references/self-improvement-loop.md`의 자동 수정·
사람 결정 경계를 다시 적용한다.

최종 검증이 끝난 웹앱에서 사용자가 디자인 개선을 명시적으로 요청한 경우에만 `orange-design`으로
전환한다. 미완료 REQ를 디자인 변경으로 처리하지 않는다.

- 구현 계약 미완료 → `../orange-start/references/phase-plan.md`
- 사전 준비 안내 미완료 → `../orange-start/references/phase-preflight.md`와
  `../orange-start/references/helpful-tools.md`
- 환경·저장소 미완료 또는 도움 도구 `WAITING_FOR_SCOPE` →
  `../orange-start/references/phase-connect.md`와 `../orange-start/references/helpful-tools.md`
- `web_app` REQ 미완료 → `../orange-start/references/phase-build.md`
- `ai_skill` REQ 미완료 → `../orange-start/references/phase-build-skill.md`
- `automation` REQ 미완료 → `../orange-start/references/phase-build-automation.md`
- 모든 REQ 구현, 최종 검증 미완료 → `../orange-start/references/phase-verify.md`
- 최종 검증 PASS, `MEMORY.md` 없음 또는 최종 검증 marker가 정확히 하나가 아님 →
  `../orange-start/references/memory-log.md`로 생성·중복 정리 후 최종 commit·push

현황만 말하고 끝내지 않는다. 사용자가 단순 상태 조회만 요청한 것이 아니라면 해당 파일을 읽고
다음 미완료 요구사항부터 바로 이어간다. `implement_and_release`면 로컬 구현 이후에도 결과물별
배포·활성화와 원격 push 완료 조건까지 계속한다. 실패·누락이 원본 범위 안의 안전한 수정이면
질문하지 않고 고쳐 같은 검증을 다시 실행한다.

다음 항목이 `FACT_UNVERIFIED`로 막혀 있으면 `../orange-start/references/product-truth-gate.md`를 읽고
확인이 필요한 값, 현재 근거, 최적의 권장안, 다른 선택의 영향을 함께 보여준 뒤 답 하나를 받는다.
확인되지 않은 값을 예시나 기존 코드 상수로 대신하지 않는다.

`web_delivery_target: codex_sites`면 구현·배포 전에
`../orange-start/references/codex-sites.md`를 함께 읽는다. `existing`이나 `vercel_supabase`를 Sites로
바꾸거나 기존 Sites 프로젝트를 다른 공급자로 옮기지 않는다.

## 4. 기록

재개 자체와 평범한 blocker 해결은 기록하지 않는다. 과정 기록은 사용자가 요청한 경우에만 추가한다.
하지만 구현 완료 판정에는 `memory-log.md`의 최종 검증 marker 블록이 정확히 하나 있어야 하며,
재검증에서는 같은 블록을 갱신한다. 실제 blocker handoff나 최종 판정만 `PLAN.md`에 한 번 갱신한다.
