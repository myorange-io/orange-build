# Orange Build 품질 계약 — 상시 심판 없이 회귀 막기

목표: Orange Build 자체의 핵심 행동을 짧고 결정적인 계약으로 고정한다. 별도 심판 스킬이나 숫자
점수를 기본 실행 경로에 추가하지 않고, 바뀐 범위에 맞는 검증만 실행해 속도와 단순성을 지킨다.

## 1. 변하지 않아야 할 사용자 여정

| id | 반드시 관찰할 행동 | 통과 증거 |
|---|---|---|
| `no_plan_one_question` | 기획서가 없으면 7개 phase 안에서 한 번에 질문 하나와 2~3개 선택지를 제시한다. | 첫 응답에 질문 하나, 추천안이 첫 번째 |
| `latest_plan_step_approval` | 최신 기획서는 `STEP-01`의 확인할 변화·완료 확인·제외를 먼저 보여준다. | `이 단계부터 만들까요?` 뒤 구현 대기 |
| `legacy_plan_regeneration` | 구형 기획서는 직접 구현하지 않고 초기 아이디어로만 가져와 현재 구조로 다시 만든다. | 호환 TEST·표시 문자열 추론 없음 |
| `approval_before_write` | 구현 요청은 현재 STEP 승인 전 프로젝트 파일을 만들거나 고치지 않는다. | 승인 전 diff 없음 |
| `completion_level_evidence` | `local | shared | real_work` 중 사용자가 정한 수준의 실제 결과로만 완료를 판정한다. | 관련 REQ·TEST가 해당 수준에서 `TESTED` |
| `dual_host_shared_source` | Codex와 Claude Code가 같은 `skills/` 원본과 호스트별 호출·등록 경로를 사용한다. | 양쪽 manifest와 호출 smoke |

위 여섯 행동 중 하나라도 깨지면 릴리스하지 않는다. 판정은 `PASS | FAIL | EVIDENCE_MISSING`만 쓰며,
여러 항목을 하나의 숫자 점수로 뭉치지 않는다. `EVIDENCE_MISSING`은 실패를 숨기는 중간 점수가 아니라
필요한 관찰이 아직 없다는 뜻이다.

## 2. 검증 강도

| 강도 | 언제 실행하나 | 무엇을 실행하나 |
|---|---|---|
| `targeted` | 문서·fixture·validator를 수정하는 동안 | 바뀐 책임과 가장 가까운 validator, 관련 fixture |
| `release` | 버전 변경 또는 배포 후보를 만들 때 | 전체 `validate_*.py`, 네 스킬 구조 검증, Codex·Claude manifest 검증, diff 검사, 양쪽 smoke |
| `independent` | 반복 회귀, 고위험 권한·실데이터, 상충하는 증거, 품질 기준이 모호한 결과, 두 버전 비교가 있을 때만 | 구현과 분리된 사람 또는 모델이 같은 계약과 증거를 검토 |

독립 검토는 기본 완료 조건이 아니다. 위 활성화 조건이 없으면 `NOT_NEEDED`와 이유를 남기고 별도
reviewer를 호출하지 않는다. 독립 검토를 하더라도 새 점수표를 만들지 않고 같은 계약에서 빠진 행동과
근거만 찾는다.

## 3. 실행 시간 보호

- 사용자 질문마다 전체 품질 suite를 실행하지 않는다.
- 내부 검증을 위해 인터뷰 질문이나 승인 단계를 추가하지 않는다.
- 현재 입력 분기와 STEP에 필요한 reference만 읽는다.
- STEP 안에서는 가까운 결정적 검증을 실행하고, 전체 회귀는 단계 검토 또는 release 경계에서 실행한다.
- 검증 결과가 같으면 심판의 심판처럼 재귀적인 평가를 추가하지 않는다.
- 공개 진입점은 `orange-start`, `orange-resume`, `orange-design`, `orange-secure` 네 개만 유지한다.

## 4. 내부 책임 지도

공개 스킬을 늘리지 않고 reference와 validator를 한 가지 중요한 결정 단위로 나눈다.

| 책임 | 소유 reference·validator | 한 가지 결정 |
|---|---|---|
| `input_classification` | `phase-interview.md`, `phase-plan.md` | 지금 입력을 인터뷰·현재 기획·구형 재생성 중 어디로 보낼지 |
| `step_approval` | `ia-collaboration.md` | 현재 STEP을 구현해도 되는지 |
| `deliverable_routing` | `phase-build.md`, `phase-build-skill.md`, `phase-build-automation.md` | 승인된 STEP을 어떤 결과물 경로로 구현할지 |
| `evidence_verdict` | `verification-loop.md`, `phase-verify.md` | 선택한 완료 수준의 증거가 충분한지 |
| `resume_and_record` | `orange-resume`, `memory-log.md` | 어디서 재개하고 언제 최종 기록을 한 번 남길지 |
| `release_regression` | `validate_quality_contract.py`, `validate_release.py` | 여섯 사용자 여정과 공용 패키지가 유지됐는지 |

새 책임이 기존 행과 독립적으로 호출할 가치가 있고 사용자가 직접 선택해야 할 때만 공개 스킬 후보로
검토한다. 구현 편의를 위한 내부 분해만으로 공개 명령을 늘리지 않는다.

## 5. Orange Build가 만드는 AI 스킬

AI 스킬은 별도 심판을 붙이기 전에 `phase-interview.md`와 `phase-plan.md`에서 인지 과업 지도를 만들고,
그중 한 가지 인지 과업만 단일 과업 계약으로 확정한다. `phase-build-skill.md`가 그 계약 안에 정상·
비트리거·빈/깨진 입력·도구 부재·새 작업 호출 평가를 내장한다. 여러 독립 과업을 한 스킬에 묶거나
독립 검토를 상시 실행해 품질을 대신하지 않는다.
