# 환경·계정·GitHub 저장소 준비

목표: `phase-preflight.md`의 준비 카드와 설치 동의 범위 안에서 필요한 도구만 준비하고, 사용할
계정을 확인한 뒤 기본 공개 GitHub 저장소를 만든다. `helpful-tools.md`에서 고른 도움 도구도 현재
호스트 하나에만 준비한다. 웹앱이라고 해서 Supabase를, 스킬이라고 해서 Node.js나 MCP를 무조건
설치하지 않는다.

## 1. 기존 프로젝트 보호

먼저 읽기 전용으로 확인한다.

```bash
pwd
git status --short --branch
git remote -v
```

- 기존 파일·변경·원격이 있으면 재사용한다. 사용자 변경을 덮어쓰거나 정리하지 않는다.
- `adaptive`면 `execution-profiles.md`에 따라 프로젝트의 `AGENTS.md`, `CLAUDE.md`, README,
  package·runtime 설정, CI와 배포 설정을 먼저 읽는다. 기존 명령과 배포 경로가 Orange Build의
  새 프로젝트 기본값보다 우선한다.
- 기존 GitHub 저장소의 visibility는 **자동으로 바꾸지 않는다**. 현재 상태와 변경 영향을 알리고
  확인받는다.
- `SOURCE_PLAN.md`와 `PLAN.md`가 git에 들어가도 되는지 개인정보·비밀값을 먼저 살핀다. 실제 고객
  데이터, 토큰, 비밀번호가 있으면 제거하거나 예시값으로 바꾼다.
- 커밋할 때 전체 파일 일괄 stage를 하지 않는다. `git status --short`로 이번 단계가 만든 파일을 가려내고,
  `git add --` 뒤에 **정확한 경로만** 나열한다. `git diff --cached --name-only`로 기존 사용자
  변경이 섞이지 않았는지 확인한다.

## 2. 필요한 런타임만 점검·설치

`PLAN.md`와 기존 프로젝트가 요구하는 런타임을 먼저 정한다. `## 사전 준비`의 설치 목록과 사용자가
동의한 범위를 대조한다. **동의받지 않은 시스템·글로벌·프로젝트 설치를 실행하지 않는다.**

- `web_app`: 기본적으로 Node.js·npm 필요
- `ai_skill`: 스크립트가 있을 때만 그 스크립트의 Node.js 또는 Python 필요
- `automation`: 선택한 구현의 Node.js 또는 Python 필요

### Node.js

`node --version`, `npm --version`과 아래 LTS metadata를 확인한다. 숫자가 높아도 `lts`가 `null`이면
LTS가 아니다. 기존 프로젝트면 `.nvmrc`, `.node-version`, `package.json#engines`를 우선한다. 새
프로젝트와 Chrome DevTools MCP는 현재 LTS 계열을 쓴다.

```bash
node -p 'JSON.stringify({version: process.version, lts: process.release.lts || null})'
```

Node.js가 없거나 요구 버전보다 낮으면 링크만 주고 중단하지 않는다. 사전 준비에서 동의받았다면
가능한 공식 패키지 관리자로 직접 설치한다.

| 환경 | 기본 명령 |
|---|---|
| macOS + Homebrew | `brew install node` 또는 설치된 버전 관리자에서 LTS 설치 |
| Windows | `winget install OpenJS.NodeJS.LTS` |
| Linux | 설치된 `nvm`·`mise`·`asdf`가 있으면 LTS 설치, 없으면 배포판 패키지 관리자 사용 |

검증하지 않은 원격 설치 스크립트나 `sudo`를 먼저 쓰지 않는다. 관리자 암호나 터미널 재시작이
필요할 때만 사용자에게 그 한 동작을 요청한다. 설치 후 새 셸에서 `node --version && npm --version`과
LTS metadata를 다시 실행해 실제 성공을 확인한다. 버전이 여전히 요구사항에 못 미치면 다음 단계로
가지 않는다.

### 공통 CLI

- `git --version`; 없으면 OS의 공식 개발 도구 또는 패키지 관리자로 설치한다.
- `gh --version`과 `gh auth status`; 없으면 macOS는 `brew install gh`, Windows는
  `winget install --id GitHub.cli`, Linux는 배포판별 GitHub 공식 패키지 경로를 쓴다.
- `web_delivery_target: vercel_supabase`일 때만 `vercel --version`; 없으면 `npm install -g vercel`
- `web_delivery_target: vercel_supabase`에서 Supabase가 선택됐을 때만 `supabase --version`; 없으면 macOS는 Homebrew, Windows는
  Scoop 등 공식 설치 경로를 사용한다. 프로젝트 로컬 방식이면 `npm install supabase --save-dev`와
  `npx supabase`를 쓰며 `npm install -g supabase`는 쓰지 않는다.

### Python

Python 자동화나 스킬 스크립트에만 `python3 --version`을 확인한다. 기존 `pyproject.toml`,
`.python-version`, `runtime.txt`가 있으면 그 버전을 우선한다. 없으면 유지보수 중인 안정 버전을
OS 공식 설치 경로로 설치한다. 프로젝트 의존성은 가상환경에 설치하고 시스템 Python을 덮어쓰지
않는다. 설치와 package 변경은 사전 준비에서 동의받은 범위여야 한다.

CLI 설치가 성공했는지 반드시 버전 명령으로 재확인한다. 새 npm/Python 패키지는 공식 registry에
실제로 존재하는지와 lockfile 변경을 확인하고, 설치 뒤 import·build까지 실행한다.

### 현재 호스트의 도움 도구

`helpful-tools.md`에 따라 설치 전 현재 호스트의 MCP와 프로젝트 package를 다시 조사한다. 준비 카드에
포함해 사용자가 동의한 후보만 다음처럼 처리한다.

1. `browser_runtime_diagnostics`가 부족한 웹앱만 Chrome DevTools MCP의 package identity와 현재
   버전을 공식 npm registry에서 확인하고, 그 정확한 버전으로 현재 호스트에 등록한다.
2. `repeatable_e2e`가 요구될 때만 프로젝트 로컬 `@playwright/test`와 Chromium을 설치한다.
3. Vercel·Supabase처럼 계정과 project scope가 필요한 remote MCP는 아직 broad URL로 등록하지 않고
   3단계 identity 확인 뒤 처리한다.
4. 설치 뒤 `등록`, `인증`, `현재 세션 실제 호출`을 따로 검증한다. 재시작 전에는 호출이 안 되더라도
   기존 browser·CLI 검증으로 작업을 계속하고 `HELPFUL` 도구 때문에 구현을 멈추지 않는다.

기존 동일 이름이나 같은 능력의 entry는 기본적으로 덮어쓰거나 재설치하지 않는다. 단,
`EXISTING_UNSAFE`의 정확한 재구성과 원본 설정 backup·실패 rollback에 명시적으로 동의한 경우만
그 entry를 안전 설정으로 교체한다. 새 설치가 실패하면 기존 설정을 건드리지 않고 이번 실행에서
새로 만든 entry만 제거한다. 동의 뒤에는 도구별로 재확인하지 않고 설치와 health 검증까지 자동으로
이어간다.

## 3. 계정 확인 게이트

로그인되어 있다는 사실만으로 진행하지 않는다. 실제 대상 계정과 조직을 보여준다.

계정이 없거나 인증되지 않았다면 오류를 반복하지 않는다. 왜 필요한지 설명하고
`phase-preflight.md`의 공식 가입 URL을 연 뒤, 사용자가 가입·이메일 확인·로그인·2FA를 끝내도록
한 동작만 요청한다. 연결된 browser/computer 도구가 있으면 `browser-steps.md`에 따라 나머지
페이지 이동과 비밀이 아닌 설정을 대신하고, 완료 직후 아래 identity 명령으로 재확인한다.

공식 CLI 인증은 현재 지원되는 기본 브라우저/device flow를 쓴다.

```bash
gh auth login --web       # GitHub가 미인증일 때
vercel login              # Vercel이 미인증일 때
supabase login            # 전역 CLI를 선택했을 때
npx supabase login        # 프로젝트 로컬 CLI를 선택했을 때
```

사용자가 브라우저에 표시된 device code, 위치, 요청 시각을 확인한 뒤 승인하도록 한다. 토큰을
명령 인자나 대화에 붙여넣게 하지 않는다.

```bash
gh api user --jq .login
vercel whoami                 # Vercel이 필요한 경우
vercel teams ls               # 팀 범위가 필요한 경우
supabase projects list --output json  # Supabase가 필요한 경우
```

다음처럼 대화에만 요약한다. 이메일·토큰을 파일이나 `MEMORY.md`에 저장하지 않는다.

```text
계정 확인
- GitHub: [login]
- Sites: [사용 가능 / 폴백 / 기존 project]
- Vercel: [user / team]
- Supabase: [organization / project 또는 미사용]
- Google OAuth: [확인 전 / 선택한 계정]
```

- 한 계정만 있고 서비스 간 소유자가 자연스럽게 일치하면 계속한다.
- 여러 GitHub 조직, Vercel 팀, Supabase 조직 중 대상이 모호하면 **어느 하나를 쓸지 한 번만 묻는다**.
- Google 로그인 화면에 여러 계정이 있으면 임의로 최근 계정을 고르지 않는다. OAuth 승인 전에
  `browser-steps.md`의 계정 확인 절차로 사용자가 직접 계정을 선택하게 한다.
- Supabase 프로젝트를 이름이나 `가장 최근 생성`만으로 고르지 않는다. 확인한 조직·프로젝트명·
  reference id를 함께 대조한다.

### 계정 범위가 있는 도움 도구

`PLAN.md`에서 선택했고 같은 능력이 없을 때만 `helpful-tools.md`의 정확한 명령을 실행한다.

- Vercel MCP: 단순 배포가 아니라 반복 배포·로그 분석이 필요한 경우에만, 확인한 Vercel 계정으로
  OAuth한 뒤 `https://mcp.vercel.com/<team-slug>/<project-slug>`에 제한하고 대상 team/project를 다시
  대조한다. account-wide endpoint는 넓어지는 접근을 별도 승인받은 경우만 쓴다.
- Supabase MCP: 개발·테스트 project ref가 확인된 뒤에만 `project_ref`, `read_only=true`, 필요한
  `features`가 모두 있는 URL로 등록한다. production이나 조직 전체 URL은 연결하지 않는다.
- 현재 호스트가 Codex면 Codex만, Claude Code면 Claude의 `--scope local`만 변경한다. 두 CLI가
  설치됐다는 이유로 양쪽에 등록하지 않는다.

로그인·OAuth consent·2FA·여러 계정 중 선택은 사용자가 처리하고, 등록·페이지 이동·health 확인은
에이전트가 이어서 한다. 권한 확대나 read-only 해제는 기존 설치 동의와 별개로 실행 직전에 확인한다.

## 4. 결과물 뼈대 준비

### `web_app`

`web_delivery_target`을 먼저 확인한다.

- `codex_sites`: 여기서 Next.js를 만들지 않는다. `phase-build.md`가 `codex-sites.md`와 설치된
  `sites-building`을 사용해 Sites starter와 `.openai/hosting.json`을 준비한다.
- `existing`: 기존 앱 구조를 그대로 사용한다.
- `vercel_supabase`: 기존 앱이 없을 때만 현재 폴더를 보존하며 아래 Next.js 앱을 만든다.

```bash
TMP=$(mktemp -d)
npx create-next-app@latest "$TMP/app" --typescript --tailwind --app --eslint \
  --no-src-dir --import-alias "@/*" --use-npm --skip-install --disable-git --yes
rsync -a --ignore-existing "$TMP/app/" ./
rm -rf "$TMP"
npm install
```

- 복사 전 동명 파일을 확인한다. `--ignore-existing`으로 기존 파일을 덮어쓰지 않고, `.gitignore`처럼
  양쪽 내용이 필요한 파일은 diff를 읽어 필요한 줄만 합친다. `rsync`가 없으면 파일 목록을 비교해
  동명 파일을 제외하고 명시적으로 복사한다.
- `PLAN.md`가 요구할 때만 SDK를 설치한다. `codex_sites`에는 Supabase를 붙이지 않고 D1/R2 선택을
  `codex-sites.md`에 맡긴다. 데이터 저장이 없으면 어느 DB도 붙이지 않는다.
- UI 컴포넌트가 필요한 앱이면 shadcn/ui를 기본 스타일로 초기화하고 필요한 컴포넌트만 추가한다.
- 기본 Next.js 홍보 화면은 제거한다. 아직 별도 `준비 중` 화면을 배포하지 않고, 구현 단계에서
  첫 완결 흐름을 만든 뒤 바로 배포한다.
- `.gitignore`가 `.env*`, 로컬 DB, 빌드 산출물을 제외하는지 확인한다.
- `npm install`은 사전 준비에서 동의받은 프로젝트 package 설치 범위 안에서만 실행한다.

프로젝트 지침은 두 호스트에서 같은 계약을 읽도록 `AGENTS.md`와 `CLAUDE.md`에 짧게 둔다.

```markdown
# [결과물 이름]

Orange Build 프로젝트다. `SOURCE_PLAN.md`는 원본, `PLAN.md`는 실행 계약이다.

## 규칙
- 모든 변경은 `PLAN.md`의 REQ ID에 연결한다.
- 완료 조건을 실제로 검증하기 전 상태를 PASS로 바꾸지 않는다.
- 원본 범위를 줄이려면 사용자 결정과 이유를 `변경 기록`에 남긴다.
- 비밀값과 개인정보를 코드·로그·커밋에 남기지 않는다.
```

### `ai_skill`

아직 구현 파일을 만들지 않는다. `SOURCE_PLAN.md`, `PLAN.md`, `MEMORY.md`만 루트에 두고
`phase-build-skill.md`가 결과물 구조를 정하게 한다.

### `automation`

아직 특정 프레임워크를 만들지 않는다. 트리거와 배포 위치를 `PLAN.md`에서 확인하고
`phase-build-automation.md`가 가장 작은 실행 구조를 만들게 한다.

## 5. GitHub 저장소

Git 원격이 없는 새 저장소만 기술 이름 slug를 사용한다. 3단계에서 고른 GitHub 사용자 또는 조직을
`<github-owner>`로 명시한다. owner를 생략해 CLI 기본 계정에 만들지 않는다.

```bash
git init
git add -- SOURCE_PLAN.md PLAN.md MEMORY.md
# 생성한 프로젝트 파일은 git status에서 확인한 정확한 경로만 추가한다.
git diff --cached --name-only
git commit -m "기획서와 구현 계약"
gh repo create <github-owner>/<slug> --public --source=. --remote=origin --push
gh repo view --json visibility,url --jq '"\(.visibility) \(.url)"'
```

출력이 기본적으로 `PUBLIC`인지 확인한다. 기획서에 비공개가 필요하거나 개인정보·비밀값 위험이
있으면 생성 전에 사용자에게 확인받고 `--private`로 만든다. 새로 만든 저장소가 아니라면
`gh repo view`로 기존 visibility를 확인하며, visibility 변경은 항상 사용자 확인 후에만 한다.

`PLAN.md`의 `GitHub 저장소`를 체크하고 GitHub URL을 `검증 증거`에 남긴다. visibility
확인과 체크 변경을 같은 커밋으로 push한다.

기존 원격이 있으면 `gh repo create`를 실행하지 않는다. 현재 원격 URL·visibility·push 권한을
확인하고 그대로 사용한다.

## 6. 웹앱 배포 연결

`web_app`만 실행한다. 첫 화면을 localhost에 띄우지 않고, 첫 완결 흐름을 만든 뒤 즉시
프로덕션 배포할 수 있도록 연결만 준비한다.

`PLAN.md`의 `web_delivery_target`을 따른다.

### `existing`

기존 CI·배포·DB·인증 설정을 읽고 그대로 재사용한다. 새 Sites·Vercel·Supabase project를 만들지
않는다.

### `codex_sites`

- 현재 세션에 `create_site`, `save_site_version`, production deploy, deployment status 확인에 해당하는
  Sites 도구가 실제로 있는지 확인한다.
- 이 단계에서는 `create_site`를 호출하지 않는다. `phase-build.md`에서 첫 완결 흐름과 production
  build가 준비된 뒤 설치된 `sites-building`·`sites-hosting` 순서로 한 번만 생성·저장·배포한다.
- Sites 내부 preview를 위한 개발 서버는 Sites workflow가 관리한다. 사용자에게 실행을 맡기거나
  localhost를 첫 결과로 전달하지 않는다.
- Sites가 사용할 수 없거나 호환성 오류가 확인되면 `codex-sites.md`에 따라
  `web_delivery_target: vercel_supabase`와 이유를 기록하고 아래 준비부터 자동 재개한다.

### `vercel_supabase`

기존 배포 경로가 없는 새 프로젝트에서 개인 scope면 `vercel link --yes --project <slug>`를, 팀을
골랐다면 아래처럼 team id/slug를 명시한다.

```bash
vercel link --yes --project <slug> --team <vercel-team-id-or-slug>
vercel git connect --yes
```

- Vercel 프로젝트 scope가 3단계에서 확인한 사용자·팀인지 확인한다.
- GitHub 저장소를 쓰므로 Vercel GitHub App이 **그 저장소에 접근 가능**한지 확인한다.
  브라우저 작업은 `browser-steps.md`를 따른다.
- 이 단계에서는 빈 앱을 보여주기 위한 `npm run dev`를 실행하지 않는다.
- 실제 `vercel --prod`와 URL 전달은 `phase-build.md`의 첫 완결 흐름 직후 한다.

### 데이터·인증이 필요한 경우만

`PLAN.md` 요구사항에 영구 저장이 있을 때만 데이터 저장소를 연결한다.

- `codex_sites`: D1/R2 logical binding, schema·migration, runtime secret은 `codex-sites.md`와
  `sites-building`에서 준비한다. 별도 Supabase project를 만들지 않는다.
- `existing`: 기존 저장소와 인증 경계를 유지한다.
- `vercel_supabase`: Supabase를 선택했다면 아래를 따른다.

  1. Vercel/Supabase 조직과 프로젝트 이름을 먼저 확인한다.
  2. 새 프로젝트 생성 또는 기존 프로젝트 사용을 `PLAN.md` 가정에 기록한다.
  3. 프로젝트 URL과 publishable/anon 키만 클라이언트 환경변수로 둔다.
  4. 비공개 폼 처리나 관리자 작업에 service-role이 필요하면 **서버 전용**
     `SUPABASE_SERVICE_ROLE_KEY`를 로컬·Vercel 비밀 환경변수에 저장한다. `NEXT_PUBLIC_`을 붙이지 않는다.
  5. 키 값을 대화·로그·파일 출력에 노출하지 않고, `.env.local`은 커밋하지 않는다.
  6. 모든 public 테이블에 RLS와 계획에 맞는 정책을 둔다.

Google OAuth 로그인이 있는 앱이면 Google 계정·OAuth 프로젝트·redirect URL 소유자가 같은지
`browser-steps.md`에 따라 확인한다.

## 7. 준비 완료 게이트와 단계 마무리

다음을 실제로 확인하기 전 구현으로 넘어가거나 `준비 완료`라고 하지 않는다.

- 필요한 도구의 실제 버전·LTS metadata와 프로젝트 요구 버전이 맞는다.
- 모든 `REQUIRED` 준비 항목이 `READY`이고, `NOT_NEEDED`에는 제외 근거가 있다.
- CLI와 브라우저의 user/team/organization이 선택한 대상과 일치한다.
- 필요한 저장소·프로젝트·OAuth 연결이 존재하고 최소 권한이다.
- `web_app`의 `web_delivery_target`과 한 줄 판정 이유가 기록돼 있고 `pending`이 아니다.
- 비밀값은 안전한 환경변수 저장소에 있고 대화·로그·커밋에는 없다.
- 유료·외부 영향 작업은 별도 승인을 받았거나 아직 실행하지 않았다.
- 필요 없는 서비스는 설치·가입·연결하지 않았다.
- `REQUIRED` 도움 능력은 `READY` 또는 안전 설정과 실제 호출이 확인된 `EQUIVALENT`다.
- `HELPFUL` 후보가 `SKIPPED`·`FAILED`면 대체 검증 방법이 기록돼 있다. `WAITING_FOR_SCOPE`는
  안전한 scope로 설치했거나 `SKIPPED`로 정리됐다.
- `EXISTING_UNSAFE` entry는 사용하지 않았고, 정확한 동의로 안전하게 재구성해 `READY`로 바꾸거나
  대체 검증과 함께 `SKIPPED`로 정리했다.

`PLAN.md`의 `사전 준비 안내`와 `환경·계정 확인`을 체크하고, 확인한 **계정 이름이 아니라 확인
절차와 선택한 scope**, 설치 동의 범위, 설치한 도구, 도움 도구의 `READY | EQUIVALENT | SKIPPED`
상태와 실제 호출 또는 대체 검증, GitHub 저장소 visibility 검증을 `MEMORY.md`에 기록한다. 개인 이메일과 토큰은
기록하지 않는다.

변경된 계획·설정·체크 상태를 한 커밋에 담아 push한다.

`git status --short`에서 이번 단계가 바꾼 계획·설정 파일만 정확한 경로로 stage하고,
`git diff --cached --name-only`로 확인한 뒤 commit한다.

```bash
git commit -m "환경과 GitHub 저장소 준비"
git push
```

`guided`면 `✅ 준비 완료 — GitHub 저장소와 실행 환경을 확인했습니다.`라고 알린다. `adaptive`면
사용자 동작이나 변경분이 없을 때 내부 보고를 생략한다. 두 프로필 모두 결과물 유형에 맞는 구현
파일로 바로 이어간다.
