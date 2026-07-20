---
name: orange-start
description: Orange Build 앱에서 복사한 기획서를 구현하거나, 기획서 없이 호출하면 앱과 같은 질문 흐름으로 기획서부터 만든 뒤 Codex 또는 Claude Code에서 실제 결과물로 끝까지 구현·배포한다. 새 프로젝트는 guided, 기존 프로젝트는 adaptive로 진행해 준비된 환경을 반복 설명하지 않으며, 필요한 설치·가입·계정·브라우저 세팅과 도움 도구를 판정하고 웹앱·AI 작업 스킬·자동화의 요구사항 추적·첫 작동 결과·최종 검증까지 진행한다. "오렌지 빌드 시작", "이 기획서 구현해줘", "바이브코딩 이어서", "orange-start" 같은 요청에 사용한다.
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
- 원본 기획을 `SOURCE_PLAN.md`에 보존한다. 구현 편의나 디자인 참고자료의 누락을 이유로 원본 범위를
  조용히 줄이지 않는다.
- `PLAN.md`의 요구사항마다 `REQ-01` 같은 ID, 완료 조건, 검증 방법을 둔다. 증거 없이 완료로
  체크하지 않는다.
- 앱 기획서의 `TEST-01`~`TEST-03`은 `references/verification-loop.md`에 따라 해당 `REQ-*`의
  검증 계약으로 연결한다. 구형 v2 원문에 TEST가 없으면 이미 받은 내용으로 세 가지를 파생하고
  이를 묻기 위한 질문은 추가하지 않는다.
- Codex에서는 사용자가 **GPT-5.6**을 선택한 교육 환경을 전제로 한다. 모델을 바꾸는 명령이나 설정은
  실행하지 않고 `codex-gpt-5p6.md`에 따라 결과 계약, 자율 도구 사용, 안전한 병렬화와 검증 능력을
  충분히 사용한다. Claude Code에서는 현재 계정의 최신 고성능 모델을 사용한다.
- 가장 먼저 `execution-profiles.md`로 `guided | adaptive`와 완료 의도를 판정한다. 사용자의 숙련도를
  묻지 않으며, `구현해줘`는 결과물별 구현·검증·commit·push·배포 또는 활성화까지 끝내라는 뜻이다.
- 구현 전에 `phase-preflight.md`로 필요한 설치·가입·계정·브라우저 세팅을 먼저 보여준다.
  `helpful-tools.md`로 현재 호스트의 능력을 조사해 Chrome DevTools MCP 같은 도움 도구도 기획서에
  필요하고 중복이 아닐 때만 고른다. 설치는 정확한 변경 목록에 동의받은 뒤 대신하고,
  가입·본인확인만 사용자에게 요청한다.
- `web_app`이면 `codex-sites.md`로 배포 대상을 고른다. 새 guided 프로젝트를 Codex 데스크톱·웹에서
  진행하고 Sites가 호환되면 `codex_sites`를 우선하며, 기존 배포 경로·Claude Code·미지원 기능·
  Sites 비활성화에는 기존 경로나 `vercel_supabase`로 폴백한다.
- 새 GitHub 저장소는 **기본으로 공개**로 만들고 생성 직후 실제 visibility를 확인한다. 기획서에 비공개가 필요하거나 개인정보·비밀값 위험이 있으면 생성 전에 사용자와 공개 범위를 확인한다.
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

한 번에 필요한 파일만 읽는다. Codex에서 실행 중이면 먼저 `references/codex-gpt-5p6.md`를 읽고,
Claude Code에서는 건너뛴다.

1. **실행 프로필·완료 의도** — `references/execution-profiles.md`
2. **입력 경로 선택**
   - 복사한 기획서 있음 → `references/phase-plan.md`
   - 복사한 기획서 없음 → `references/phase-interview.md` → `references/phase-plan.md`
3. **기획서 기반 사전 준비** — `references/phase-preflight.md` + `references/helpful-tools.md`
   - `web_app` → `references/codex-sites.md`로 배포·저장 경로 확정
4. **환경·계정·GitHub 저장소** — `references/phase-connect.md`
5. **결과물별 구현**
   - `web_app` → `references/phase-build.md`
   - `ai_skill` → `references/phase-build-skill.md`
   - `automation` → `references/phase-build-automation.md`
6. **전체 대조 검증과 릴리스** — `references/phase-verify.md`

계획·구현·최종 검증에서 공통으로 쓰는 TEST 매핑, 결과물 수량 대조, 증거 등급은
`references/verification-loop.md`를 따른다. 구현과 검증 중 발견한 안전한 결함은
`references/self-improvement-loop.md`에 따라 묻지 않고 수정·재검증하며, 범위·비용·권한·삭제·
외부 발송처럼 중요한 결정만 사람에게 돌린다.

웹앱의 기본 구현은 기능·상태·반응형·접근성·최종 검증까지 끝낸다. 최종 검증 후 디자인이 마음에
들지 않는다는 요청이 있을 때만 별도 `orange-design`을 호출한다. 기본 `orange-start` 흐름에서
Stitch나 디자인 시안 생성 단계를 열지 않는다.

## 단계 완료 보고

`guided`는 주요 이정표가 실제로 끝났을 때만 다음 형식으로 짧게 알린다.

```text
✅ [단계] 완료 — [확인한 증거]
다음: [바로 이어서 할 일]
```

`adaptive`는 시작 요약, 실제 사용자 동작이 필요한 blocker, 첫 작동 결과, 최종 결과만 알리고
내부 단계별 완료 보고는 생략한다.

사용량이나 시간이 부족하면 현재 파일과 체크리스트를 같은 커밋에 저장하고, 다음에
`orange-resume`을 호출하면 이어갈 수 있다고 알린다.

## 공통 원칙

- **원본이 약속이다** — 핵심 기능·포함 범위·사용 흐름·성공 기준을 모두 요구사항에 매핑한다.
- **작동 흐름 단위** — 화면이나 파일 하나가 아니라 입력→처리→검토 가능한 결과가 이어지는
  세로 슬라이스를 끝낸다.
- **첫 결과를 빨리** — 웹앱은 localhost를 사용자 결과로 주지 않고 첫 슬라이스를 프로덕션에 배포해
  URL을 준다. Sites가 내부 HMR preview를 한 번 열어도 사용자가 실행·관리하게 하지 않는다. 스킬은
  실제 호출 결과, 자동화는 dry-run 기록을 먼저 보여준다.
- **단순한 구현, 완전한 범위** — 코드는 단순하게 만들되 계획된 기능이나 실패 처리를 생략하지 않는다.
- **초보자 보호장치** — 계획과 구현 때 `references/beginner-guardrails.md`를 적용한다. 같은 오류가
  두 번 반복되면 새 코드 생성을 멈추고 로그·재현 조건·직전 변경부터 진단한다.
- **자가 개선이 기본** — 첫 GREEN이나 첫 배포를 완성으로 보지 않는다. 테스트·실제 결과·원본 대조에서
  발견한 버그와 누락은 AI가 자동으로 고치고 같은 증거를 다시 확인한다. 선택의 책임이 필요한
  항목만 `references/self-improvement-loop.md`의 사람 결정 게이트로 보낸다.
- **마일스톤 저장** — 작은 수정·테스트 반복 중에는 코드와 테스트에 집중한다. 완결 흐름 하나가
  실제 검증됐을 때만 코드·테스트와 `PLAN.md` 상태를 한 커밋에 담는다. `MEMORY.md`는 중요한 결정·
  반복 실패 해결·사람 결정·최종 검증이 실제로 있을 때만 같은 커밋에 포함한다.
- **호스트 중립** — Codex에서는 현재 도구와 `AGENTS.md`, Claude Code에서는 현재 도구와
  `CLAUDE.md`를 사용한다. 두 파일은 없을 때 최초 1회만 만들고, 기존 파일이나 이미 만든 계약을
  작업마다 다시 쓰지 않는다. 특정 호스트 전용 명령이 없으면 자연어 호출로 폴백한다.
- **브라우저는 가능한 만큼 대신** — computer use, in-app browser, Chrome 연동 등 현재 연결된
  도구로 가입 페이지 이동과 프로젝트·OAuth 설정을 대신한다. 비밀번호·2단계 인증·CAPTCHA·약관·
  여러 계정 중 선택은 사용자가 한다. `references/browser-steps.md`를 따른다.
- **도움 도구는 능력 기준** — 현재 세션에 같은 능력이 있으면 새 MCP를 설치하지 않는다. 부족한
  능력만 현재 호스트 하나에 제안하고, 한 번 동의받은 뒤 등록·인증·health 확인까지 자동 진행한다.
- **오류는 복구 가능하게** — 문제가 생긴 항목에만 `references/troubleshooting.md`를 읽고, 쉬운
  원인 설명과 한 번에 하나의 수정·검증을 제공한다.
- **기록은 예외만** — 평범한 설치·수정·테스트 성공과 `PLAN.md`·git에 이미 있는 사실은
  `MEMORY.md`에 반복하지 않는다. 나중에 다시 판단하거나 수업에서 배울 가치가 있는 결정·막힌 점·
  해결만 `references/memory-log.md`에 따라 마일스톤당 최대 한 항목으로 남긴다.
- **완료를 과장하지 않기** — 필수 요구사항이 하나라도 FAIL/미검증이면 `완성`이라 하지 않고
  `N/M 통과`와 남은 일을 밝힌 뒤 계속 고친다.
- **눈으로 보이는 증거까지** — 테스트 명령의 종료 코드만 보지 않고, 입력이 처리 경계를 지나
  사용자가 보는 결과가 되는지 확인한다. 추론만 한 항목은 통과로 세지 않는다.
- **기존 프로젝트 우선** — `adaptive`에서는 기존 지침·검증 명령·CI·배포 설정을 먼저 사용한다.
  기존 원격과 배포 경로가 있으면 새 저장소나 Sites·Vercel 프로젝트를 만들지 않는다.
