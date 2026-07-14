# 기획서 기반 도움 도구 — 필요한 능력만 자동 준비하기

목표: 기획서의 구현·검증에 실제로 필요한 개발 능력을 찾고, 현재 호스트에 같은 능력이 없을 때만
공식 도구를 설치한다. 도구 이름이 익숙하다는 이유로 MCP를 늘리거나 Codex와 Claude Code 양쪽을
한꺼번에 설정하지 않는다.

## 1. 먼저 능력 재고 조사

설정 변경 전 현재 **이 세션을 실행 중인 호스트 하나만** 읽기 전용으로 조사한다.

```bash
# Codex에서 실행 중일 때
codex mcp list --json

# Claude Code에서 실행 중일 때
claude mcp list
```

대화에 이미 노출된 connector, computer use, in-app browser, Chrome 연동, MCP 도구도 함께 본다.
두 CLI가 컴퓨터에 모두 설치돼 있어도 현재 사용하지 않는 호스트는 변경하지 않는다.

제품명이 아니라 다음 능력으로 중복을 판정한다.

| 능력 | 충족됐다고 볼 증거 |
|---|---|
| `browser_navigation` | 실제 페이지 열기·읽기·클릭·스크린샷 성공 |
| `browser_runtime_diagnostics` | DOM과 console·network를 읽고 필요시 performance trace 실행 가능. MCP면 health·scope·격리·연결 옵션도 안전함 |
| `repeatable_e2e` | 프로젝트에서 같은 사용자 흐름을 독립 테스트로 반복 실행 가능 |
| `deployment_observability` | 선택한 Vercel team/project의 배포와 로그를 구조적으로 조회 가능 |
| `database_diagnostics` | 선택한 개발용 Supabase project의 schema·migration·advisor를 제한된 범위로 조회 가능 |

같은 이름의 MCP가 아니라도 능력의 실제 호출과 필요한 안전 설정이 확인되면 `EQUIVALENT`로 기록하고
새로 설치하지 않는다. 반대로 클릭·스크린샷만 되는 도구를 console·network 진단 능력이 있다고
간주하지 않는다. health가 실패했거나 범위가 필요 이상이고, Chrome entry에 `--autoConnect`·
`--browser-url`·비격리 profile이 있으면 `EXISTING_UNSAFE`이며 사용 가능한 동등 기능으로 세지 않는다.

## 2. 공식 allowlist와 선택 규칙

아래 후보도 `PLAN.md` 신호가 있을 때만 선택한다.

| 기획서 신호 | 부족한 능력 | 기본 후보 | 설치하지 않는 경우 |
|---|---|---|---|
| 웹앱의 라이브 오류·OAuth·네트워크·성능 진단 | `browser_runtime_diagnostics` | Chrome DevTools MCP | 같은 능력의 도구가 이미 활성·정상 |
| 다단계·권한별·모바일 흐름을 매 빌드에서 반복 검증 | `repeatable_e2e` | 프로젝트 로컬 `@playwright/test`와 Chromium | 단순 1회 확인이거나 기존 E2E가 있음 |
| 반복적인 Vercel 배포·프로젝트·로그 분석 | `deployment_observability` | Vercel 공식 remote MCP | 단순 배포만 필요해 Vercel CLI로 충분 |
| Supabase schema·RLS·migration·advisor 조회 | `database_diagnostics` | project-scoped read-only Supabase MCP | project ref 미확정, production뿐, 기존 connector가 있음 |

- GitHub 저장소 생성·push·visibility 확인은 기존 `gh`로 충분하므로 GitHub MCP를 기본 추가하지 않는다.
- Gmail·Slack·Notion을 결과물에서 쓴다는 사실만으로 해당 호스트 MCP를 설치하지 않는다. 이미 제공된
  connector를 우선하고, 없으면 구현 SDK와 OAuth만 준비한다.
- AI 스킬이나 Python 자동화에 선택적 npm MCP 하나를 쓰기 위해 Node.js를 새로 설치하지 않는다.
- `HELPFUL` 후보가 실패하거나 사용자가 건너뛰면 대체 검증을 기록하고 구현을 계속한다. 기획서상
  완료 증거를 만들 방법이 전혀 없는 `REQUIRED` 능력만 blocker다.

검토했지만 다음은 일반 선설치에서 제외한다.

- Next DevTools MCP는 Next.js 16+의 **실행 중인 로컬 dev server**를 진단할 때만 유효하다. Orange
  Build의 첫 배포 우선 흐름에서는 설치하지 않으며, 기존 Next.js 16+ 프로젝트의 로컬 runtime 오류를
  진단하기로 사용자가 선택했을 때만 같은 동의 절차에 넣는다. MCP 때문에 Next.js를 업그레이드하거나
  `npm run dev`를 기본 단계로 되돌리지 않는다.
- Playwright MCP는 일반 코딩·회귀 검증에 기본 추가하지 않는다. 저장되는 테스트가 필요한 경우 5절의
  프로젝트 로컬 Playwright Test를 쓴다.
- GitHub MCP는 단순 저장소 작업에, shadcn MCP는 기존 CLI로 충분한 컴포넌트 설치에 기본 추가하지
  않는다. Figma·Stripe처럼 외부 데이터나 결제에 접근하는 도구는 해당 링크·결제 요구가 원본 기획에
  명시되고 기존 connector가 없을 때만 공식 도구를 별도 후보로 제시한다.

## 3. 준비 카드와 한 번의 동의

선택한 후보마다 다음을 먼저 보여준다.

```text
도움 도구 후보
- 기능: [왜 필요한 능력인지]
- 도구: [공식 이름과 고정할 버전 또는 remote URL]
- 범위: [프로젝트 package / Claude local / Codex 사용자 설정]
- 접근: [브라우저 데이터 / Vercel project / Supabase dev project]
- 영향: [다운로드·설정 파일·OAuth·재시작 여부]
- 대체: [설치하지 않을 때의 검증 방법]
```

MCP 등록도 호스트 설정을 바꾸는 설치다. `phase-preflight.md`의 시스템·글로벌·프로젝트 설치 목록에
합쳐 한 번 동의받는다. 동의 뒤에는 항목마다 다시 묻지 않고 아래 명령을 자동 실행한다. 계정 로그인,
OAuth consent, 2FA와 여러 계정 중 선택만 사용자에게 맡긴다.

Codex의 `codex mcp add`는 사용자 설정을 바꾸므로 그 범위를 명시한다. Claude Code는 기본적으로
`--scope local`을 써서 현재 프로젝트에만 둔다. 기존 동일 이름 entry는 덮어쓰거나 제거하지 않고
설정과 health를 먼저 보여준다.

기존 entry가 같은 능력을 제공하지만 아래 privacy·scope 기본값과 다르면 `EXISTING_UNSAFE`로 두고
그 entry를 사용하지 않는다. 준비 카드에 정확한 차이와 fallback을 보여준다. 재구성에 동의하면 비밀을
제외한 기존 `get` 결과를 임시 백업하고, 현재 호스트의 그 entry만 제거해 안전 설정으로 다시 등록한다.
실패하면 이번 실행에서 바꾼 entry를 제거하고 백업한 원래 설정을 복원한다. 기존 설정 재구성을 새
설치로 위장하거나 일반 설치 동의 범위에 몰래 포함하지 않는다.

## 4. Chrome DevTools MCP

Node.js LTS, npm/npx와 지원되는 최신 Chrome이 이미 필요하거나 준비될 웹앱에서만 선택한다. 먼저
공식 npm registry의 package identity와 현재 버전을 확인하고, 결과가 정상 semver일 때 그 **정확한
버전**을 `<resolved-version>`에 넣는다.

```bash
npm view chrome-devtools-mcp name version dist.integrity repository.url --json

# 현재 호스트가 Codex일 때만
codex mcp add chrome-devtools -- \
  npx -y chrome-devtools-mcp@<resolved-version> \
  --isolated --no-usage-statistics --no-performance-crux --redact-network-headers

# 현재 호스트가 Claude Code일 때만
claude mcp add --scope local chrome-devtools -- \
  npx -y chrome-devtools-mcp@<resolved-version> \
  --isolated --no-usage-statistics --no-performance-crux --redact-network-headers
```

격리 프로필을 기본으로 써서 종료 시 브라우저 데이터를 지운다. 개인 Chrome 프로필의 열린 탭에
붙는 `--autoConnect`, `--browser-url`, remote debugging은 별도 명시 동의 없이는 사용하지 않는다.
Chrome DevTools MCP는 연결한 브라우저의 내용을 읽고 수정할 수 있으므로 계정 가입·2FA용 개인 탭은
`browser-steps.md`의 기존 browser/computer 도구로 처리한다.

## 5. 반복 E2E는 프로젝트 로컬 Playwright

반복 가능한 회귀 검증이 기획서 완료 조건에 필요할 때만 프로젝트 dependency로 설치한다. 브라우저를
오래 탐색하는 별도 MCP보다 테스트 코드와 결과가 저장되는 Playwright Test를 기본으로 한다.

```bash
npm install -D @playwright/test@latest
npx playwright install chromium
npx playwright --version
```

`--with-deps`는 OS package와 관리자 권한을 바꿀 수 있으므로 기존 동의에 포함되지 않았다면 실행하지
않는다. 설치 뒤 핵심 REQ 한 흐름의 테스트를 만들고 `npx playwright test`가 반복 통과해야
`repeatable_e2e`를 `READY`로 둔다.

## 6. Vercel MCP

단순 `vercel --prod` 배포에는 설치하지 않는다. 여러 배포의 상태·로그·project를 반복 분석해야 하고
기존 도구로 그 능력이 없을 때만 Vercel 공식 remote MCP를 현재 호스트에 추가한다. identity 게이트로
team과 project를 확인한 뒤 project-specific endpoint를 기본으로 쓴다.

```bash
# Codex
codex mcp add vercel --url "https://mcp.vercel.com/<team-slug>/<project-slug>"
codex mcp login vercel

# Claude Code
claude mcp add --scope local --transport http vercel \
  "https://mcp.vercel.com/<team-slug>/<project-slug>"
claude mcp login vercel
```

OAuth 전에 Beta 서비스임과 접근할 team/project를 보여준다. 로그인·consent·계정 선택 뒤
`browser-steps.md`의 identity 게이트로 실제 Vercel team을 다시 확인한다. account-wide
`https://mcp.vercel.com`은 여러 프로젝트 조회가 원본 기획에 꼭 필요할 때만 넓어지는 접근 범위를
준비 카드에서 별도 승인받아 쓴다. MCP mutation tool 호출의 사람 확인은 계속 유지한다.

## 7. Supabase MCP

Supabase **개발·테스트 프로젝트**의 reference id가 확정된 뒤에만 추가한다. production에는 연결하지
않는다. 쓰기는 migration 파일과 CLI 검증으로 수행하고 MCP는 기본적으로 project scope·read-only·
필요 feature group만 연다. `<feature-list>`는 아래에서 기획서에 필요한 것만 comma로 연결한다.

- schema·RLS·migration 조회 → `database`
- log·security/performance advisor 조회 → `debugging`
- MCP 안에서 공식 문서 검색이 완료 조건에 필요함 → `docs`

```text
https://mcp.supabase.com/mcp?project_ref=<project-ref>&read_only=true&features=<feature-list>
```

```bash
# 위 URL 전체를 따옴표로 감싼다.
codex mcp add supabase --url "<scoped-supabase-mcp-url>"
codex mcp login supabase

claude mcp add --scope local --transport http supabase "<scoped-supabase-mcp-url>"
claude mcp login supabase
```

`project_ref`, `read_only=true`, 필요한 `features` 중 하나라도 빠지면 자동 설치하지 않는다. 읽기 전용을
해제하거나 feature를 늘리는 일은 별도 권한 확대이므로 실행 직전에 다시 확인한다.

## 8. 검증·재시작·롤백

설치 전 MCP 이름·scope 목록을 저장하고, 설치 뒤 현재 호스트에서만 확인한다.

```bash
# Codex
codex mcp get <name> --json
codex mcp list --json

# Claude Code
claude mcp get <name>
claude mcp list
```

- `등록 성공`, `인증 성공`, `현재 세션에서 실제 도구 1회 호출 성공`을 따로 기록한다.
- 새 MCP가 다음 세션부터 노출되면 재시작 필요를 한 번만 안내하고, 현재 작업은 기존 browser·CLI·HTTP
  검증으로 계속한다. `HELPFUL` 도구 때문에 구현을 멈추지 않는다.
- 실패하면 원인과 수동 명령을 보여주고, **이번 실행에서 새로 만든 entry만**
  `codex mcp remove <name>` 또는 `claude mcp remove --scope local <name>`으로 제거한다.
- 기존 entry, 다른 호스트 설정, lockfile, 브라우저 프로필을 정리하거나 초기화하지 않는다.
- remote MCP OAuth 실패 시 이번 실행에서 시작한 login만 logout하고 새 entry만 제거한다.

실행 당일 명령과 보안 옵션은 공식 문서를 다시 확인한다.

- Chrome DevTools MCP: `https://github.com/ChromeDevTools/chrome-devtools-mcp`
- Playwright 설치: `https://playwright.dev/docs/intro`
- Next DevTools MCP: `https://nextjs.org/docs/app/guides/mcp`
- Vercel MCP: `https://vercel.com/docs/agent-resources/vercel-mcp`
- Supabase MCP: `https://supabase.com/docs/guides/ai-tools/mcp`
