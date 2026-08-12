# 최신 기획서를 IA 실행 계약으로 바꾸기

목표: 최신 App 복사문, 구현 자료 묶음, 또는 로컬 IA 인터뷰 결과를 원본으로 보존하고
`workflow: ia_collaborative`인 `PLAN.md` 계약으로 바꾼다. 구현 요청이면 첫 STEP 승인 전에는
프로젝트 파일을 수정하지 않는다.

## 목차

1. 인정하는 입력
2. 최신 구조 판정과 구형 전환
3. 자료 묶음 확인
4. REQ·TEST·STEP 연결
5. PLAN.md 형식
6. 첫 승인 전 게이트

## 1. 인정하는 입력

다음 순서로 찾는다.

1. 현재 메시지나 파일의 최신 App 복사문 또는 `IMPLEMENTATION_REQUEST.md`
   - `아래 기획서를 바탕으로 실제로 동작하는 결과물을 참가자와 함께 단계적으로 구현하세요.`
   - `## 협력 구현 원칙`
   - `## 기획서 메타데이터`
   - `## 원본 기획서`
2. 구현 자료 묶음
   - `PLAN.md`
   - `IMPLEMENTATION_REQUEST.md`
   - `MATERIALS.md`
   - 필요한 경우 `materials/` 원본
3. `phase-interview.md`가 만든 현재 로컬 기획서
   - `source: orange-start-interview | orange-start-regenerated`
   - `interview_contract_version: 2`
   - `## 함께 구현할 순서`
4. 위 입력이 없으면 `phase-interview.md`로 돌아간다.

App의 `contract_version: 2`와 `deliverable_kind`는 canonical 메타데이터다. 지원 버전보다 높은 값은
추측하지 않고 원문을 보존한 뒤 플러그인 업데이트가 필요하다고 안내한다. v2인데 canonical 값이
`web_app | ai_skill | automation` 밖이면 손상된 복사본으로 보고 다시 복사하도록 한다.

구현 자료 묶음에서는 `IMPLEMENTATION_REQUEST.md`가 협력 구현 지시, 묶음의 `PLAN.md`가 원본 기획,
`MATERIALS.md`와 `materials/`가 자료 계약이다. 이 파일들을 Orange Build 실행용 `PLAN.md` 하나로
덮어써 의미를 잃지 않도록, 원본 기획은 `SOURCE_PLAN.md`에 보존하고 실행 상태판만 새 `PLAN.md`로
만든다.

## 2. 최신 구조 판정과 구형 전환

`contract_version: 2`만으로 현재 구조라고 판정하지 않는다. 아래가 모두 있어야 최신 IA 기획서다.

- `deliverable_kind` canonical 값
- `## 직접 확인할 3가지`와 정확히 `TEST-01`~`TEST-03`
- `## 함께 구현할 순서`
- `### 첫 번째 작은 완성 · ...`
- 각 단계의 `확인할 변화`, `완료 확인`, `이번 단계에서 하지 않을 것`

위 구조가 없고 `바로 시작할 순서`, 표시 문자열 추론, TEST 없는 초기 v2 같은 구형 형태만 있으면
직접 구현하지 않는다. 구형 문서는 계약이 아니라 `legacy_seed` 초기 아이디어다.

1. 대상·문제·막힌 순간·입력·결과·자료처럼 확인 가능한 내용만 추출한다.
2. 구형 결과물 표시 문자열과 TEST·구현 순서는 버린다.
3. `phase-interview.md`의 7개 phase covered 판정을 다시 수행한다.
4. 빠진 내용은 최대 10문항 안에서 한 번에 하나씩 확인한다.
5. 최신 구조의 새 기획서를 만든다.

구형 문서에서 호환 TEST를 파생하거나 유형을 표시 문자열로 추론하지 않는다. 새 기획서의 TEST와
결과물 유형은 현재 인터뷰 답과 명시된 가정에서 생성한다.

## 3. 자료 묶음 확인

`MATERIALS.md`가 있으면 원본 `materials/` 파일을 먼저 열고 파일별로 다음을 대조한다.

- 용도
- 자료 설명
- 반드시 반영할 내용
- 그대로 유지할 항목
- 적용 위치
- 확인할 점

자료가 누락되거나 분석할 수 없거나 원본과 `MATERIALS.md`가 충돌하면 임의 대체하지 않는다. 가장
중요한 열린 질문 하나를 선택지 2~3개로 먼저 묻는다. 사용자가 분석을 확인하거나 바로잡은 뒤에만
REQ와 STEP에 반영한다. `반드시 반영할 자료`에 적힌 파일을 찾을 수 없으면 요청하고, 필수 자료가
아닌 참고 자료는 영향과 가정을 표시한 뒤 진행할 수 있다.

## 4. REQ·TEST·STEP 연결

원본의 다음 항목을 빠짐없이 읽는다.

- 대상·문제와 가장 막히는 순간
- 해결 방식과 결과물 유형
- 사용 흐름과 핵심 기능
- 첫 구현 포함·제외 범위
- 사용할 자료와 반드시 반영할 자료
- AI 역할과 사람 확인 지점
- 성공 기준·실패 신호·완료 수준
- `TEST-01`~`TEST-03`
- `함께 구현할 순서`와 가정

각 포함 범위와 핵심 행동에 `REQ-01`부터 ID를 붙인다. 완료 조건은 사용자가 관찰할 수 있게 쓰고,
각 REQ를 하나 이상의 TEST 또는 보조 검증에 연결한다. TEST의 제목·준비·행동·기대 결과·통과 증거는
뜻을 줄이거나 HTTP 상태 같은 약한 증거로 바꾸지 않는다.

각 구현 단계를 `STEP-01`부터 옮긴다. STEP 표에는 원본 단계 이름, 확인할 변화, 완료 확인, 제외,
연결 REQ·TEST, 상태를 둔다. 처음에는 모든 단계가 `AWAITING_APPROVAL`이고 `current_step`은
`STEP-01`이다. 미래 STEP도 표에는 보이지만 `current_step`과 일치하지 않으면 실행할 수 없다.

결과물 유형별 설계는 필요한 내용만 보강한다.

- `web_app`: 경로·입력·출력·데이터 변화·역할·로딩·빈 상태·오류·성공·모바일
- `ai_skill`: 긍정 트리거 3개·비트리거 2개·입출력·빈 입력·도구 부재·공용 파일·호스트별 등록
- `automation`: 트리거·계정·입출력 매핑·dry-run·중복 키·재시도·로그·중지·복구·외부 승인

제품 사실이 확인되지 않았으면 `product-truth-gate.md`에 따라 관련 REQ를
`BLOCKED · FACT_UNVERIFIED`로 둔다. 단일 예시값을 일반 규칙으로 만들지 않는다.

## 5. PLAN.md 형식

```markdown
# [결과물 이름]

> [한 줄 소개]

## 메타데이터
- source: orange-build-app | orange-start-interview | orange-start-regenerated
- source_contract: 2 | local-ia
- contract_version: 2
- deliverable_kind: web_app | ai_skill | automation
- workflow: ia_collaborative
- completion_level: local | shared | real_work
- current_step: STEP-NN | complete
- execution_profile: guided | adaptive
- delivery_intent: implement | plan_only | verify_only
- web_delivery_target: local | pending | existing | codex_sites | vercel_supabase | n/a
- host: codex | claude_code
- slug: ascii-kebab-case

## IA 단계
| STEP | 단계 | 확인할 변화 | 완료 확인 | 이번 단계에서 하지 않을 것 | 연결 REQ·TEST | 상태·증거 |
|---|---|---|---|---|---|---|
| STEP-01 | [첫 번째 작은 완성] | [...] | [...] | [...] | REQ-01 · TEST-01 | AWAITING_APPROVAL · NOT_RUN |
| STEP-02 | [다음 개선] | [...] | [...] | [...] | REQ-02 · TEST-03 | AWAITING_APPROVAL · NOT_RUN |

## 요구사항 계약
| REQ | 원본 근거 | 관찰 가능한 완료 조건 | 검증 | 구현 위치 | 상태·증거 |
|---|---|---|---|---|---|
| REQ-01 | [SOURCE_PLAN 절·짧은 문구] | [사용자가 보는 결과] | TEST-01 | - | TODO · NOT_RUN |

## 결과물 인벤토리
| 종류 | 예상 목록·수량 | 실제 목록·수량 | 상태 |
|---|---|---|---|
| [경로·흐름 / 스킬 파일·출력 / 트리거·runbook] | [목록] · N | - | TODO |

## 검증 시나리오 계약
| TEST | 준비·행동 | 기대 결과·통과 증거 | 연결 REQ·STEP | 상태·실제 증거 |
|---|---|---|---|---|
| TEST-01 | [준비] → [행동] | [기대 결과] · [증거] | REQ-01 · STEP-01 | NOT_RUN |

## 유형별 설계
[화면·데이터 / 스킬 입출력·등록 / 자동화 연결·재시도]

## 자료 계약
| 파일 | 용도 | 필수 규칙·그대로 유지 | 적용 위치 | 열린 질문·상태 |
|---|---|---|---|---|
| [없음 또는 파일] | [...] | [...] | [...] | CONFIRMED / WAITING_USER |

## 사전 준비
| 미해결 항목 | 영향·scope | 상태 |
|---|---|---|
| [없음 / 설치·가입·계정·권한] | [...] | MISSING / USER_ACTION / INSTALL_APPROVED |

## 가정과 결정
- [완료 수준, 중요한 가정·사람 결정·blocker. 없으면 없음]

## 최종 판정
- IA 단계: [APPROVED 수]/[전체] · 현재 [STEP-NN · 상태]
- REQ: 0/N PASS · TEST: 0/3 TESTED · P0/P1: 미검토
- 완료 수준: [local/shared/real_work] · 결과: [미정]
- 아직 증명하지 못한 것: 검증 전
```

`TESTED | PARTIAL | INFERRED | NOT_RUN | FAIL | BLOCKED`를 구분한다. 단계 상태는
`AWAITING_APPROVAL | IN_PROGRESS | AWAITING_REVIEW | APPROVED`만 쓴다.

## 6. 첫 승인 전 게이트

구현 요청에서는 위 `SOURCE_PLAN.md`와 `PLAN.md` 내용을 먼저 작업 메모에서 완성하고, STEP-01을
대화에 보여준다. 사용자가 `이 단계부터 만들까요?`에 동의하기 전에는 다음을 하지 않는다.

- `SOURCE_PLAN.md`, `PLAN.md`, 코드, 설정, 테스트 등 프로젝트 파일 생성·수정
- package 설치, 저장소 생성, commit·push, 배포·외부 연결
- STEP 상태를 `IN_PROGRESS`로 변경

읽기 전용 폴더 조사와 기획 요약만 허용한다. 동의하면 `SOURCE_PLAN.md`와 `PLAN.md`를 처음 저장하고
STEP-01을 `IN_PROGRESS`로 바꾼 뒤 사전 준비와 구현을 시작한다. `plan_only` 요청은 기획 파일 생성 자체를 사용자가 요청한 것이므로
파일을 저장하고 `STEP-01 · AWAITING_APPROVAL` 상태에서 끝낸다.

계약 게이트는 다음을 확인한다.

- 최신 구조 또는 로컬 IA 구조이며 구형 호환 추론이 아니다.
- 모든 원본 범위가 REQ에, 모든 REQ가 TEST 또는 보조 검증에 연결됐다.
- 정확히 세 TEST와 한 개 이상의 STEP이 있다.
- `workflow`, `completion_level`, `current_step`, 단계 상태가 있다.
- 자료 분석이 사용자 확인과 일치하거나 열린 질문이 명시됐다.
- 첫 STEP이 기술 작업이 아니라 관찰 가능한 작은 완성이다.
- 구현 요청이면 승인 전에 프로젝트 파일이 바뀌지 않았다.

승인 후에는 `ia-collaboration.md`와 결과물별 구현 reference로 간다.
