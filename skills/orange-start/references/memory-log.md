# 만들기 기록 — MEMORY.md 작성 규칙

`MEMORY.md`는 선택한 완료 수준의 구현 완료 증거다. 모든 IA STEP이 승인되고 필수 REQ·TEST와
`completion_level` 게이트를 통과한 뒤 최종 검증 결과를 정확히 한 번 기록한다.

## 목차

1. 기록 게이트
2. marker 하나 유지
3. 최신 App 형식
4. 안전·저장
5. Orange Build App으로 가져가기

## 1. 기록 게이트

`delivery_intent: implement`에서 다음을 모두 확인한 뒤 생성하거나 갱신한다.

- 모든 IA STEP이 `APPROVED`이고 `current_step: complete`다.
- 모든 필수 REQ와 최신 TEST 3개가 선택한 완료 수준에서 `TESTED`다.
- P0/P1과 `FACT_UNVERIFIED`가 없다.
- 결과물 유형과 `completion_level`의 실제 결과가 있다.
  - `local`: 로컬 핵심 흐름 / 현재 호스트 스킬 새 작업 호출 / 자동화 dry-run
  - `shared`: 공유 URL / 격리 설치·호출 / 공유 테스트 run
  - `real_work`: 실제 자료·계정·업무 결과와 복구 절차
- `PLAN.md` 최종 판정이 실제 증거와 일치한다.

첫 GREEN, build만 성공한 웹앱, source 경로만 지정한 스킬 실행, 선택한 수준에 못 미치는
`PARTIAL`·`INFERRED` 결과에는 완료 기록을 만들지 않는다. `plan_only`도 대상이 아니다.

## 2. marker 하나 유지

```markdown
<!-- orange-build:final-verification -->
[최종 검증 내용]
<!-- /orange-build:final-verification -->
```

- 파일이 없으면 최신 형식과 marker 블록 하나를 만든다.
- 파일이 있지만 marker가 없으면 기존 기록을 보존하고 블록 하나만 추가한다.
- marker 블록이 이미 하나 있으면 새 항목을 append하지 않고 기존 블록만 최신 결과로 갱신한다.
- 중복이면 내용을 보존해 한 블록으로 합친다.
- 완료 선언 전에 시작 marker와 종료 marker가 각각 정확히 하나인지 확인한다.

이후 디자인·보안·재검증으로 상태가 바뀌어도 두 번째 최종 검증 항목을 만들지 않는다.

## 3. 최신 App 형식

날짜는 `date +%Y-%m-%d`로 확인한다. 실제로 관찰하지 않은 commit·URL·run id를 추측하지 않는다.

```markdown
# 🍊 만들기 기록 — [결과물 이름]

## 한눈에 보기
- 무엇을: [결과물 한 문장]
- 누구를 위해: [주요 사용자]
- 핵심 흐름: [입력 → 처리 → 결과 → 사람 확인]
- 결과물 유형: [web_app / ai_skill / automation]
- 완료 수준: [local / shared / real_work]
- 도구: [실제로 사용한 주요 기술과 서비스]
- 시작: [확인 가능한 작업 시작일]
- 결과: [로컬 결과 / 배포 URL / 대표 실행 결과 / run id]

## 기록

<!-- orange-build:final-verification -->
### [YYYY-MM-DD] 최종 검증
- **최종 판정**: [완료 수준] 완료 — IA STEP [S/S] APPROVED · REQ [M/M] PASS · TEST [3/3] TESTED
- **정한 것 / 한 것**: [가장 중요한 결정과 실제 결과]
- **왜**: [그 방식과 범위를 선택한 이유]
- **확인한 결과**: [사용자가 직접 확인할 핵심 결과]
- **어떻게**: [검증 조건과 절차]
- **검증 근거**: [실제 핵심 증거 최대 3개]
- **막힌 점 / 바꾼 점**: [원인과 해결, 없으면 없음]
- **배운 것 / 다음**: [교훈과 다음 개선]
- **저장·배포**: [확인한 commit·GitHub·URL·run id와 상태, local이면 해당 없음]
- **아직 증명하지 못한 것**: [없음 또는 내용·영향]
<!-- /orange-build:final-verification -->
```

`local` 결과를 공유·실업무 성공으로 바꾸어 쓰지 않는다. 허용된 P2/P3나 사용자가 수용한 제한이
있으면 `아직 증명하지 못한 것`에 ID·영향·근거를 적는다.

과정 기록은 사용자가 요청한 경우에만 marker 앞에 추가한다. 평범한 설치·파일 생성·테스트·commit·
push·STEP 상태 전이는 중간 기록 조건이 아니다.

## 4. 안전·저장

- 비밀번호·API 키·토큰·개인 이메일·고객 원문·불필요한 개인정보를 기록하지 않는다.
- 긴 로그와 명령 전체를 복제하지 않고 핵심 증거만 요약한다.
- 파일은 256KB 이하로 유지한다.
- commit이 선택한 수준과 프로젝트 계약에 포함될 때만 `PLAN.md`, `MEMORY.md`, 코드·테스트를 같은
  최종 커밋에 담는다. 정확한 경로만 `git add --`로 지정한다.
- 구현 완료 후 marker가 정확히 하나가 아니면 완료 게이트는 FAIL이다.

## 5. Orange Build App으로 가져가기

`SOURCE_PLAN.md`의 `source`가 `orange-build-app`인 작업은 사용자가 원할 때 App의 만들기 기록으로 가져갈 수 있다. 완료
조건은 아니다.

- 업로드 전 비밀값과 불필요한 개인정보가 없는지 검사한다.
- 256KB 제한을 확인한다.
- 파일 전체가 App에 저장된다는 사실을 설명하고 명시적 프라이버시 동의를 받는다.
- 참가자 회고는 사용자가 자신의 말로 쓴 문장만 입력을 보조한다.
- 실제 절차는 `browser-steps.md`의 선택적 App 복귀 흐름을 따른다.
