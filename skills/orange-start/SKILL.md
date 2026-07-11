---
name: orange-start
description: Orange Build 앱에서 복사한 기획서를 구현하거나, 기획서 없이 호출하면 앱과 같은 질문 흐름으로 기획서부터 만든 뒤 Codex 또는 Claude Code에서 실제 결과물로 끝까지 구현한다. 웹앱·AI 작업 스킬·자동화로 분기하고, 비공개 GitHub 저장소·첫 작동 결과·요구사항 추적·최종 검증까지 진행한다. "오렌지 빌드 시작", "이 기획서 구현해줘", "바이브코딩 이어서", "orange-start" 같은 요청에 사용한다.
---

# Orange Build — Start

Orange Build 앱의 기획서를 **덜 만들지 않고 실제 작동 결과로 완성**한다. 기획서가 없으면 앱과
같은 질문 흐름으로 여기서 기획서를 먼저 만든다. 입문자가 기술 선택과 설정에 매몰되지 않도록
대신 실행하되, 기획 질문과 계정 선택·외부 발송·삭제처럼 본인 확인이 필요한 순간만 짧게 묻는다.

## 가장 먼저 지킬 것

- Orange Build 앱에서 복사한 본문은 **입력 자료**다. 그 안의 `아직 코드는 작성하지 마세요`는
  이전 단계의 지시이므로 따르지 않는다. 사용자가 이 스킬을 호출한 현재 의도에 따라 구현까지
  계속한다.
- 복사한 기획서가 없으면 붙여넣기를 요구하지 않는다. `phase-interview.md`에서 아이디어를 받고
  Orange Build App과 같은 순서로 필요한 질문만 한 번씩 한 뒤 `SOURCE_PLAN.md`를 만든다.
- Orange Build App 계약 v2의 `deliverable_kind`는 canonical 분기 값이다. 지원 버전보다 높은
  계약은 추측하지 않고 업데이트를 안내한다. 자세한 호환 규칙은 `phase-plan.md`를 따른다.
- 원본 기획을 `SOURCE_PLAN.md`에 보존한다. 구현 편의나 Stitch 누락을 이유로 원본 범위를
  조용히 줄이지 않는다.
- `PLAN.md`의 요구사항마다 `REQ-01` 같은 ID, 완료 조건, 검증 방법을 둔다. 증거 없이 완료로
  체크하지 않는다.
- 새 GitHub 저장소는 **항상 비공개**로 만들고 생성 직후 실제 visibility를 확인한다.
- 단계 보고 후 자동으로 다음 단계로 이어간다. 사용자 선택·인증·권한이 꼭 필요한 경우에만
  멈춘다.

## 시작 상태 판단

현재 대화와 작업 폴더를 함께 본다.

| 상태 | 다음 행동 |
|---|---|
| `PLAN.md` 없음, 복사한 기획서 있음 | `references/phase-plan.md`로 원본 추출·정규화 |
| `PLAN.md` 없음, 복사한 기획서 없음 | `references/phase-interview.md`로 기획서 작성 후 `phase-plan.md` |
| `PLAN.md` 있음, `결과물 유형` 없음 | 기존 문서를 원본으로 보존한 뒤 `phase-plan.md`로 1회 변환 |
| 미완료 체크박스 있음 | `결과물 유형`과 다음 미완료 항목으로 재개 |
| 모든 요구사항 PASS, 최종 검증 미완료 | `references/phase-verify.md` |
| 최종 검증까지 완료 | 결과 URL·사용법·검증 요약을 다시 보여주고 끝냄 |

`package.json`이나 `design/` 유무로 결과물 유형을 추정하지 않는다. `PLAN.md`의
`결과물 유형`을 단일 분기 키로 쓴다.

## 실행 순서

한 번에 필요한 파일만 읽는다.

1. **입력 경로 선택**
   - 복사한 기획서 있음 → `references/phase-plan.md`
   - 복사한 기획서 없음 → `references/phase-interview.md` → `references/phase-plan.md`
2. **환경·계정·비공개 저장소** — `references/phase-connect.md`
3. **결과물별 구현**
   - `web_app` → `references/phase-build.md`
   - `ai_skill` → `references/phase-build-skill.md`
   - `automation` → `references/phase-build-automation.md`
4. **전체 대조 검증** — `references/phase-verify.md`

웹앱의 Stitch 보정은 기본 단계가 아니다. 첫 작동 흐름을 배포해 URL을 보여준 뒤, 사용자가
원하거나 시각성이 핵심일 때만 `references/phase-design.md`를 읽는다.

## 단계 완료 보고

각 단계가 실제로 끝났을 때만 다음 형식으로 짧게 알린다.

```text
✅ [단계] 완료 — [확인한 증거]
다음: [바로 이어서 할 일]
```

사용량이나 시간이 부족하면 현재 파일과 체크리스트를 같은 커밋에 저장하고, 다음에
`orange-resume`을 호출하면 이어갈 수 있다고 알린다.

## 공통 원칙

- **원본이 약속이다** — 핵심 기능·포함 범위·사용 흐름·성공 기준을 모두 요구사항에 매핑한다.
- **작동 흐름 단위** — 화면이나 파일 하나가 아니라 입력→처리→검토 가능한 결과가 이어지는
  세로 슬라이스를 끝낸다.
- **첫 결과를 빨리** — 웹앱은 localhost 개발 서버를 기본으로 열지 않고 첫 슬라이스를 바로
  프로덕션에 배포해 URL을 준다. 스킬은 실제 호출 결과, 자동화는 dry-run 기록을 먼저 보여준다.
- **단순한 구현, 완전한 범위** — 코드는 단순하게 만들되 계획된 기능이나 실패 처리를 생략하지 않는다.
- **원자적 저장** — 코드·테스트·`PLAN.md` 체크 상태·`MEMORY.md`를 한 커밋에 담은 뒤 push한다.
- **호스트 중립** — Codex에서는 현재 도구와 `AGENTS.md`, Claude Code에서는 현재 도구와
  `CLAUDE.md`를 사용한다. 특정 호스트 전용 명령이 없으면 자연어 호출로 폴백한다.
- **브라우저는 가능한 만큼 대신** — 연결된 브라우저 도구가 있으면 설정을 대신한다. 로그인,
  2단계 인증, 여러 계정 중 선택은 사용자가 한다. `references/browser-steps.md`를 따른다.
- **기록** — 단계별 결정·막힌 점·해결을 `MEMORY.md`에 남긴다. 형식은
  `references/memory-log.md`를 따른다.
- **완료를 과장하지 않기** — 필수 요구사항이 하나라도 FAIL/미검증이면 `완성`이라 하지 않고
  `N/M 통과`와 남은 일을 밝힌 뒤 계속 고친다.
