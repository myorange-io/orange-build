---
name: orange-start
description: Orange Build 앱에서 복사한 기획서를 구현하거나, 기획서 없이 호출하면 앱과 같은 질문 흐름으로 기획서부터 만든 뒤 Codex 또는 Claude Code에서 실제 결과물로 끝까지 구현한다. 기획서에서 필요한 설치·가입·계정·브라우저 세팅과 Chrome DevTools MCP 같은 도움 도구를 먼저 판정하고, 동의받은 설치와 설정을 최대한 대신하며, 웹앱·AI 작업 스킬·자동화의 요구사항 추적·첫 작동 결과·최종 검증까지 진행한다. "오렌지 빌드 시작", "이 기획서 구현해줘", "바이브코딩 이어서", "orange-start" 같은 요청에 사용한다.
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
- 앱 기획서의 `TEST-01`~`TEST-03`은 `references/verification-loop.md`에 따라 해당 `REQ-*`의
  검증 계약으로 연결한다. 구형 v2 원문에 TEST가 없으면 이미 받은 내용으로 세 가지를 파생하고
  이를 묻기 위한 질문은 추가하지 않는다.
- 특정 모델이나 모델 변경 명령을 권하지 않는다. Codex·Claude Code에서 사용자가 현재 선택한
  모델과 호스트 기본값을 그대로 사용한다.
- 구현 전에 `phase-preflight.md`로 필요한 설치·가입·계정·브라우저 세팅을 먼저 보여준다.
  `helpful-tools.md`로 현재 호스트의 능력을 조사해 Chrome DevTools MCP 같은 도움 도구도 기획서에
  필요하고 중복이 아닐 때만 고른다. 설치는 정확한 변경 목록에 동의받은 뒤 대신하고,
  가입·본인확인만 사용자에게 요청한다.
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
| 구현 계약 완료, 사전 준비 미확인 | `references/phase-preflight.md`로 준비 카드·설치 동의 |
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
2. **기획서 기반 사전 준비** — `references/phase-preflight.md` + `references/helpful-tools.md`
3. **환경·계정·비공개 저장소** — `references/phase-connect.md`
4. **결과물별 구현**
   - `web_app` → `references/phase-build.md`
   - `ai_skill` → `references/phase-build-skill.md`
   - `automation` → `references/phase-build-automation.md`
5. **전체 대조 검증** — `references/phase-verify.md`

계획·구현·최종 검증에서 공통으로 쓰는 TEST 매핑, 결과물 수량 대조, 증거 등급은
`references/verification-loop.md`를 따른다.

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
- **초보자 보호장치** — 계획과 구현 때 `references/beginner-guardrails.md`를 적용한다. 같은 오류가
  두 번 반복되면 새 코드 생성을 멈추고 로그·재현 조건·직전 변경부터 진단한다.
- **원자적 저장** — 코드·테스트·`PLAN.md` 체크 상태·`MEMORY.md`를 한 커밋에 담은 뒤 push한다.
- **호스트 중립** — Codex에서는 현재 도구와 `AGENTS.md`, Claude Code에서는 현재 도구와
  `CLAUDE.md`를 사용한다. 특정 호스트 전용 명령이 없으면 자연어 호출로 폴백한다.
- **브라우저는 가능한 만큼 대신** — computer use, in-app browser, Chrome 연동 등 현재 연결된
  도구로 가입 페이지 이동과 프로젝트·OAuth 설정을 대신한다. 비밀번호·2단계 인증·CAPTCHA·약관·
  여러 계정 중 선택은 사용자가 한다. `references/browser-steps.md`를 따른다.
- **도움 도구는 능력 기준** — 현재 세션에 같은 능력이 있으면 새 MCP를 설치하지 않는다. 부족한
  능력만 현재 호스트 하나에 제안하고, 한 번 동의받은 뒤 등록·인증·health 확인까지 자동 진행한다.
- **오류는 복구 가능하게** — 문제가 생긴 항목에만 `references/troubleshooting.md`를 읽고, 쉬운
  원인 설명과 한 번에 하나의 수정·검증을 제공한다.
- **기록** — 단계별 결정·막힌 점·해결을 `MEMORY.md`에 남긴다. 형식은
  `references/memory-log.md`를 따른다.
- **완료를 과장하지 않기** — 필수 요구사항이 하나라도 FAIL/미검증이면 `완성`이라 하지 않고
  `N/M 통과`와 남은 일을 밝힌 뒤 계속 고친다.
- **눈으로 보이는 증거까지** — 테스트 명령의 종료 코드만 보지 않고, 입력이 처리 경계를 지나
  사용자가 보는 결과가 되는지 확인한다. 추론만 한 항목은 통과로 세지 않는다.
