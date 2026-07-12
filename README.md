# Orange Build

> [Orange Build App](https://github.com/myorange-io/orange-build-app)에서 만든 기획서를 가져오거나,
> 앱 없이 같은 질문 흐름으로 기획서부터 작성해 웹앱·AI 작업 스킬·자동화를 실제 작동 결과까지
> 구현하는 Codex·Claude Code 교육용 플러그인.

앱에서 복사한 기획서가 있으면 이미 확인한 내용을 다시 묻지 않습니다. 기획서가 없으면 앱과 같은
7단계 질문 로직으로 필요한 내용만 물어 원본을 만들고, 어느 경로든 핵심 기능·포함 범위·사용
흐름·성공 기준을 요구사항 ID로 연결한 뒤 구현과 검증을 끝까지 이어갑니다.

## 지원 결과물

| 결과물 | 첫 번째 눈에 보이는 결과 | 완료 검증 |
|---|---|---|
| 웹앱 | 첫 작동 흐름의 Vercel URL | 라이브 핵심 흐름·데이터·권한·상태·production build |
| AI 작업 스킬 | 실제 대표 요청의 출력 | 구조 validator·긍정/비트리거·fixture·새 컨텍스트 호출 |
| 자동화 | dry-run의 대상·건수·run id | 중복 방지·재시도·로그·승인된 샘플 live-run |

새 GitHub 저장소는 기본으로 **비공개**이며, 생성 뒤 실제 visibility를 다시 확인합니다.

## 새 흐름

```text
기획서 가져오기 또는 여기서 작성
→ 원본 보존 + 요구사항 계약
→ 필요한 설치·가입·브라우저 세팅 안내
→ 결과물 유형별 구현
→ 첫 작동 결과
→ (웹앱만, 필요할 때) Stitch 시각 보정
→ 원본 기획서 전체 대조
→ 완료
```

### Stitch를 뒤로 옮긴 이유

Stitch는 기능 기획 단계가 아니라 선택적인 시각 보정 단계입니다. 웹앱의 첫 작동 URL을 먼저 본 뒤,
필요할 때만 10분 동안 대표 화면 1개를 다듬습니다. Stitch에 빠진 페이지나 기능은 구현 범위에서
삭제되지 않으며, Stitch가 추가한 기능도 자동으로 범위에 들어오지 않습니다.

## 빠른 시작

### Orange Build App 기획서가 있을 때

1. [Orange Build App](https://github.com/myorange-io/orange-build-app)에서 기획서를 완성합니다.
2. 결과 화면의 **orange-start용 복사**를 누릅니다.
3. 비어 있는 새 프로젝트 폴더를 만들고 그 폴더에서 Codex 또는 Claude Code를 엽니다.
4. 복사한 본문 전체를 붙여넣고 `orange-start`를 호출합니다.

복사문에는 `contract_version`과 `deliverable_kind`, 직접 확인할 `TEST-01`~`TEST-03`이 들어
있습니다. orange-start는 canonical 값을 그대로 사용해 웹앱·AI 작업 스킬·자동화로 분기하고,
원문은 `SOURCE_PLAN.md`에 보존합니다. 각 TEST는 `PLAN.md`의 `REQ-*`와 실제 검증 증거에 연결합니다.
지원하는 계약보다 새 버전이면 추측해 구현하지 않고 플러그인 업데이트를 안내합니다. 기존 v1
복사문과 TEST가 없던 초기 v2 복사문도 계속 지원하며, 기존 답에서 호환 TEST 3개를 추가 질문 없이
만듭니다.

### 기획서가 없을 때

1. 비어 있는 새 프로젝트 폴더에서 Codex 또는 Claude Code를 엽니다.
2. `orange-start`만 호출합니다.
3. 만들고 싶은 아이디어를 한두 문장으로 답합니다.
4. 한 번에 하나씩 나오는 질문에 답합니다.

orange-start는 앱과 같은 순서로 최대 7개를 묻되, 아이디어에서 이미 확인된 단계는 건너뜁니다.
결과물 유형이 정해지면 웹앱·AI 작업 스킬·자동화에 맞는 질문으로 전환하고, 답변을
`SOURCE_PLAN.md`에 정리한 뒤 기존 `PLAN.md`·REQ 추적 흐름으로 바로 이어갑니다. 아이디어가
떠오르지 않으면 편집 가능한 제안을 받을 수 있고, 충분히 정했다면 “전부 건너뛰기”로 현재 정보와
명시한 가정만 사용해 시작할 수 있습니다. 제안을 본 직후 건너뛰면 현재 제안을 초기 아이디어로
확정하고 이후 기획 확인 질문을 다시 열지 않습니다.

## 설치

### Codex

처음 설치할 때:

```bash
codex plugin marketplace add myorange-io/orange-build
codex plugin add orange-build@orange-build
```

새 task에서 `$orange-start` 또는 자연어로 “오렌지 빌드 시작”이라고 요청합니다.

업데이트할 때:

```bash
codex plugin marketplace upgrade orange-build
codex plugin add orange-build@orange-build
```

예전 `orange-build@personal` v1.11.1이 `codex plugin list`에 보이면, v2를 설치하기 전에 그
플러그인만 제거합니다. 두 버전이 함께 활성화되면 같은 `orange-start`가 중복 노출될 수 있습니다.

```bash
codex plugin remove orange-build@personal
```

업데이트 뒤에는 새 task를 열어야 새 스킬 정의를 읽습니다.

### Claude Code

Claude Code 안에서:

```text
/plugin marketplace add myorange-io/orange-build
/plugin install orange-build@orange-build
```

새 세션에서 `/orange-start`를 실행합니다.

이미 설치했다면 다음 순서로 업데이트합니다.

```text
/plugin marketplace update orange-build
/plugin update orange-build@orange-build
```

`/plugin list`에 구형 v1.11.1이 다른 marketplace와 함께 보이면 구형 항목만
`/plugin uninstall <구형-plugin@marketplace>`로 제거한 뒤 새 세션을 엽니다. 같은 이름의
orange-start를 두 설치본에서 동시에 활성화하지 않습니다.

## 기획서 기반 준비

orange-start는 코딩 전에 기획서를 읽고 `시작 전 준비 카드`를 먼저 보여줍니다.

- 이미 준비된 도구와 계정
- 자동 설치할 수 있지만 동의가 필요한 도구
- 기획서 검증에 도움이 되고 현재 호스트에 같은 능력이 없는 도구
- 사용자가 직접 가입·로그인·본인확인할 서비스
- computer use·in-app browser·Chrome 연동으로 대신할 프로젝트·OAuth 설정
- 비용 승인이 필요하거나 이번 기획에는 필요 없는 서비스

Node.js, GitHub CLI, Vercel CLI, Python 등은 **기획서에 필요한 것만** 골라 정확한 설치 목록과
영향을 보여준 뒤 한 번 동의받고 설치·버전 확인까지 대신합니다. GitHub·Vercel·Supabase 등 계정이
없으면 공식 가입 페이지를 열어 직접 요청합니다. 비밀번호·2FA·CAPTCHA·약관·결제·여러 계정 중
선택은 사용자가 하고, 나머지 저장소·프로젝트·OAuth·callback·최소 권한 설정은 연결된 브라우저
도구로 최대한 대신합니다.

웹앱에 console·network·performance 진단이 필요하면 Chrome DevTools MCP, 반복 E2E가 필요하면
프로젝트 로컬 Playwright Test, 반복적인 배포 로그 분석에는 Vercel MCP, Supabase schema·RLS 진단에는
project-scoped read-only Supabase MCP를 후보로 고릅니다. 현재 세션에 같은 능력이 있으면 설치하지
않고, 단순 배포에는 기존 Vercel CLI를 그대로 씁니다. 현재 실행 중인 Codex 또는 Claude Code 한쪽만
설정하며, MCP 등록 범위와 접근 데이터까지 준비 카드에 보여준 뒤 기존 설치 목록과 함께 한 번
동의받아 자동 설치·인증 확인까지 이어갑니다. 로그인·OAuth consent·2FA와 계정 선택만 사용자가 합니다.
같은 기능의 기존 MCP라도 health·scope·격리 설정이 안전하지 않으면 `EXISTING_UNSAFE`로 알리고,
정확한 재구성 동의 없이 덮어쓰거나 사용하지 않습니다.

Chrome DevTools MCP는 격리 브라우저와 사용 통계·CrUX 차단을 기본으로 하고 개인 Chrome profile에는
별도 동의 없이 연결하지 않습니다. Supabase MCP도 개발 project ref, read-only, 최소 feature가
확정되기 전에는 broad URL로 등록하지 않습니다.

Google 계정이 여러 개 로그인되어 있으면 OAuth 승인 전에 사용할 계정을 직접 선택하게 합니다.
GitHub 사용자, Vercel 팀, Supabase 조직도 CLI와 브라우저의 실제 identity를 함께 확인합니다.

## 초보자 보호장치

초보자는 AI 코드가 “거의 맞는” 상태에서 디버깅 시간이 늘고, 첫 화면을 완성으로 오인하거나,
설치 성공 여부를 판단하기 어려운 경우가 많습니다. Orange Build는 이를 줄이기 위해 다음을
기본 게이트로 둡니다.

- `SOURCE_PLAN.md`의 모든 핵심 항목을 `REQ-*`와 검증 증거에 연결
- 앱의 세 가지 TEST와 예상 페이지·파일·트리거 수를 구현 전후로 대조
- 한 번에 입력→처리→검토 가능한 작은 흐름 하나 구현
- 가능한 동작은 실패 테스트부터 만들고, lint·typecheck·test·build와 실제 URL 또는 dry-run을 검증
- `TESTED / PARTIAL / INFERRED`로 증거를 구분하고 추론만 한 항목은 완료로 세지 않음
- 같은 오류가 두 번 반복되면 재생성을 멈추고 로그·재현 조건·직전 변경 진단
- 새 패키지의 공식 registry·유지 상태·취약점·lockfile 확인
- 각 이정표에서 `만든 것 / 직접 확인할 행동 / 아직 안 된 것`을 쉬운 말로 안내

근거와 세부 대응은 플러그인의 `beginner-guardrails.md`에 출처와 함께 포함되어 있습니다.

## 명령

| 스킬 | 하는 일 |
|---|---|
| `orange-start` | 기획서를 가져오거나 여기서 작성한 뒤 유형별 구현·검증까지 진행 |
| `orange-resume` | REQ 상태와 증거를 읽어 다음 미완료 항목부터 재개 |
| `orange-secure` | Next.js·Supabase 웹앱의 키 노출·RLS·민감정보 저장 점검 |

## 결과물에 남는 파일

- `SOURCE_PLAN.md` — Orange Build App에서 가져왔거나 orange-start 인터뷰로 만든 원본
- `PLAN.md` — REQ ID·완료 조건·검증 증거가 있는 실행 계약
- `MEMORY.md` — 결정 이유와 막힌 점·해결 기록
- `CASE.md` — 수작업을 대신하는 프로젝트일 때 만드는 사례 카드

완료 판정은 `PLAN.md`의 필수 요구사항이 모두 PASS일 때만 합니다. 일부가 미검증이면 `N/M 통과`와
남은 항목, 아직 증명하지 못한 것을 그대로 보여줍니다. Orange Build App에서 시작한 작업이면
완료 뒤 GitHub·배포 URL과 `MEMORY.md`를 앱에 되돌려 학습 기록을 마무리할 수 있도록 안내합니다.
브라우저로 대신 입력하는 경우에도 MEMORY 업로드는 사용자의 명시적 동의를 받은 뒤에만 합니다.

## 강사용 노트

- 참가자는 기획서를 복사해 붙여넣거나, 빈 폴더에서 `orange-start`만 호출해 기획부터 시작합니다.
- 웹앱 실습의 첫 피드백은 localhost가 아니라 실제 Vercel URL입니다.
- Stitch를 진행한다면 기능 토론을 멈추고 시각 위계·색·간격만 보정합니다.
- 외부 발송·삭제·결제·live 자동화는 dry-run 뒤 대상과 건수를 보여주고 승인받습니다.
- 수업 전 GitHub·Vercel·Google의 여러 계정 상태를 정리하거나, 사용할 계정을 미리 정해두면
  OAuth 실수가 줄어듭니다.

## 라이선스

MIT · v2.3.0
