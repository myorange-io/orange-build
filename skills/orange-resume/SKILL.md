---
name: orange-resume
description: Orange Build로 진행 중인 웹앱·AI 작업 스킬·자동화 프로젝트의 PLAN.md, 검증 증거, 최근 커밋을 읽어 완료 수와 다음 미완료 요구사항을 알려주고 구현을 이어간다. "이어하기", "어디까지 했지", "계속하자", "오렌지 빌드 이어서" 같은 요청에 사용한다.
---

# Orange Build — Resume

세션이 끊긴 프로젝트를 `PLAN.md`의 요구사항 계약과 검증 증거에서 복원한다. `package.json`이나
`design/` 유무로 단계를 추측하지 않는다.

## 1. 현재 상태 읽기

다음만 읽어 빠르게 파악한다.

- `PLAN.md` 전체: 결과물 유형, REQ 상태, 진행 상황, 변경 기록, 검증 증거
- `SOURCE_PLAN.md`: PLAN 추적표에 누락 의심이 있을 때만 관련 절 확인
- `MEMORY.md`: 마지막 1~2개 항목
- `git status --short --branch`
- `git log --oneline -12`
- 결과물 증거
  - `web_app`: 기록된 production URL과 최근 배포
  - `ai_skill`: SKILL.md와 최근 validator/호출 결과
  - `automation`: 최근 dry-run/live run id와 트리거 설정

`PLAN.md`가 없으면 `orange-start`로 돌아간다. 복사한 기획서가 있으면 가져오고, 없으면 아이디어
인터뷰부터 시작할 수 있다고 안내한다.

## 2. 짧은 현황 보고

REQ 상태를 실제로 세어 다음 형식으로 보여준다.

```text
📋 [결과물 이름] · [web_app / ai_skill / automation]
   요구사항: [PASS 수]/[전체 수]
   다음: [가장 앞선 TODO/FAIL REQ와 완료 조건]
   결과: [라이브 URL / 대표 스킬 결과 / 최근 run id / 아직 없음]
   저장소: [PRIVATE 확인 / 확인 필요]
```

`MEMORY.md`의 마지막 결정이나 blocker가 있으면 한 줄 덧붙인다. 테스트가 실패했는데 체크박스만
완료인 경우 PASS 수에 넣지 않는다.

## 3. 재개 위치

- 구현 계약 미완료 → `../orange-start/references/phase-plan.md`
- 사전 준비 안내 미완료 → `../orange-start/references/phase-preflight.md`와
  `../orange-start/references/helpful-tools.md`
- 환경·저장소 미완료 또는 도움 도구 `WAITING_FOR_SCOPE` →
  `../orange-start/references/phase-connect.md`와 `../orange-start/references/helpful-tools.md`
- `web_app` REQ 미완료 → `../orange-start/references/phase-build.md`
- `ai_skill` REQ 미완료 → `../orange-start/references/phase-build-skill.md`
- `automation` REQ 미완료 → `../orange-start/references/phase-build-automation.md`
- 모든 REQ 구현, 최종 검증 미완료 → `../orange-start/references/phase-verify.md`

현황만 말하고 끝내지 않는다. 사용자가 단순 상태 조회만 요청한 것이 아니라면 해당 파일을 읽고
다음 미완료 요구사항부터 바로 이어간다.

## 4. 기록

재개 자체를 매번 기록하지 않는다. 긴 중단의 원인이나 blocker 해결처럼 나중에 가치가 있는 변화가
있을 때만 `MEMORY.md`에 덧붙인다. 코드·PLAN 상태와 같은 커밋에 저장한다.
