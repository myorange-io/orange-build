# 환경·계정·비공개 저장소 준비

목표: `PLAN.md`의 결과물 유형에 필요한 도구만 준비하고, 사용할 계정을 확인한 뒤 비공개 GitHub
저장소를 만든다. 웹앱이라고 해서 Supabase를, 스킬이라고 해서 Node.js를 무조건 설치하지 않는다.

## 1. 기존 프로젝트 보호

먼저 읽기 전용으로 확인한다.

```bash
pwd
git status --short --branch
git remote -v
```

- 기존 파일·변경·원격이 있으면 재사용한다. 사용자 변경을 덮어쓰거나 정리하지 않는다.
- 기존 GitHub 저장소가 공개라면 **자동으로 visibility를 바꾸지 않는다**. 현재 상태와 비공개 전환
  영향을 알리고 확인받는다.
- `SOURCE_PLAN.md`와 `PLAN.md`가 git에 들어가도 되는지 개인정보·비밀값을 먼저 살핀다. 실제 고객
  데이터, 토큰, 비밀번호가 있으면 제거하거나 예시값으로 바꾼다.
- 커밋할 때 전체 파일 일괄 stage를 하지 않는다. `git status --short`로 이번 단계가 만든 파일을 가려내고,
  `git add --` 뒤에 **정확한 경로만** 나열한다. `git diff --cached --name-only`로 기존 사용자
  변경이 섞이지 않았는지 확인한다.

## 2. 필요한 런타임만 점검·설치

`PLAN.md`와 기존 프로젝트가 요구하는 런타임을 먼저 정한다.

- `web_app`: 기본적으로 Node.js·npm 필요
- `ai_skill`: 스크립트가 있을 때만 그 스크립트의 Node.js 또는 Python 필요
- `automation`: 선택한 구현의 Node.js 또는 Python 필요

### Node.js

`node --version`과 `npm --version`을 확인한다. 기존 프로젝트면 `.nvmrc`, `.node-version`,
`package.json#engines`를 우선한다. 새 프로젝트면 현재 LTS 계열을 쓴다.

Node.js가 없거나 요구 버전보다 낮으면 링크만 주고 중단하지 않는다. 설치한다고 한 줄 알리고,
가능한 패키지 관리자로 직접 설치한다.

| 환경 | 기본 명령 |
|---|---|
| macOS + Homebrew | `brew install node` 또는 설치된 버전 관리자에서 LTS 설치 |
| Windows | `winget install OpenJS.NodeJS.LTS` |
| Linux | 설치된 `nvm`·`mise`·`asdf`가 있으면 LTS 설치, 없으면 배포판 패키지 관리자 사용 |

관리자 암호나 터미널 재시작이 필요할 때만 사용자에게 그 한 동작을 요청한다. 설치 후 새 셸에서
`node --version && npm --version`을 다시 실행해 실제 성공을 확인한다. 버전이 여전히 요구사항에
못 미치면 다음 단계로 가지 않는다.

### 공통 CLI

- `git --version`
- `gh --version`과 `gh auth status`
- 웹앱을 Vercel에 배포할 때만 `vercel --version`; 없으면 `npm install -g vercel`
- Supabase가 선택된 웹앱일 때만 `supabase --version`; 없으면 macOS는 Homebrew, Windows는
  Scoop 등 공식 설치 경로를 사용한다.

CLI 설치가 성공했는지 반드시 버전 명령으로 재확인한다.

## 3. 계정 확인 게이트

로그인되어 있다는 사실만으로 진행하지 않는다. 실제 대상 계정과 조직을 보여준다.

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

## 4. 결과물 뼈대 준비

### `web_app`

기존 앱이 없을 때만 현재 폴더를 보존하며 Next.js 앱을 만든다.

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
- `PLAN.md`가 요구할 때만 SDK를 설치한다. 데이터 저장이 없으면 Supabase를 붙이지 않는다.
- UI 컴포넌트가 필요한 앱이면 shadcn/ui를 기본 스타일로 초기화하고 필요한 컴포넌트만 추가한다.
- 기본 Next.js 홍보 화면은 제거한다. 아직 별도 `준비 중` 화면을 배포하지 않고, 구현 단계에서
  첫 완결 흐름을 만든 뒤 바로 배포한다.
- `.gitignore`가 `.env*`, 로컬 DB, 빌드 산출물을 제외하는지 확인한다.

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

## 5. 비공개 GitHub 저장소

새 저장소면 기술 이름 slug를 사용한다. 3단계에서 고른 GitHub 사용자 또는 조직을
`<github-owner>`로 명시한다. owner를 생략해 CLI 기본 계정에 만들지 않는다.

```bash
git init
git add -- SOURCE_PLAN.md PLAN.md MEMORY.md
# 생성한 프로젝트 파일은 git status에서 확인한 정확한 경로만 추가한다.
git diff --cached --name-only
git commit -m "기획서와 구현 계약"
gh repo create <github-owner>/<slug> --private --source=. --remote=origin --push
gh repo view --json visibility,url --jq '"\(.visibility) \(.url)"'
```

출력이 반드시 `PRIVATE`여야 한다. 새로 만든 저장소가 아니라면 `gh repo view`로 기존 visibility를
확인하고, 공개 저장소를 비공개로 바꾸기 전에는 사용자 확인을 받는다.

`PLAN.md`의 `비공개 GitHub 저장소`를 체크하고 GitHub URL을 `검증 증거`에 남긴다. visibility
확인과 체크 변경을 같은 커밋으로 push한다.

## 6. 웹앱 배포 연결

`web_app`만 실행한다. 첫 화면을 localhost에 띄우지 않고, 첫 완결 흐름을 만든 뒤 즉시
프로덕션 배포할 수 있도록 연결만 준비한다.

개인 scope면 `vercel link --yes --project <slug>`를, 팀을 골랐다면 아래처럼 팀 id/slug를 명시한다.

```bash
vercel link --yes --project <slug> --team <vercel-team-id-or-slug>
vercel git connect --yes
```

- Vercel 프로젝트 scope가 3단계에서 확인한 사용자·팀인지 확인한다.
- 비공개 GitHub 저장소를 쓰므로 Vercel GitHub App이 **그 저장소에 접근 가능**한지 확인한다.
  브라우저 작업은 `browser-steps.md`를 따른다.
- 이 단계에서는 빈 앱을 보여주기 위한 `npm run dev`를 실행하지 않는다.
- 실제 `vercel --prod`와 URL 전달은 `phase-build.md`의 첫 완결 흐름 직후 한다.

### 데이터·인증이 필요한 경우만

`PLAN.md` 요구사항에 영구 저장이 있을 때만 데이터 저장소를 연결한다. Supabase를 선택했다면:

1. Vercel/Supabase 조직과 프로젝트 이름을 먼저 확인한다.
2. 새 프로젝트 생성 또는 기존 프로젝트 사용을 `PLAN.md` 가정에 기록한다.
3. 프로젝트 URL과 publishable/anon 키만 클라이언트 환경변수로 둔다.
4. 비공개 폼 처리나 관리자 작업에 service-role이 필요하면 **서버 전용**
   `SUPABASE_SERVICE_ROLE_KEY`를 로컬·Vercel 비밀 환경변수에 저장한다. `NEXT_PUBLIC_`을 붙이지 않는다.
5. 키 값을 대화·로그·파일 출력에 노출하지 않고, `.env.local`은 커밋하지 않는다.
6. 모든 public 테이블에 RLS와 계획에 맞는 정책을 둔다.

Google OAuth 로그인이 있는 앱이면 Google 계정·OAuth 프로젝트·redirect URL 소유자가 같은지
`browser-steps.md`에 따라 확인한다.

## 7. 단계 마무리

`PLAN.md`의 `환경·계정 확인`을 체크하고, 확인한 **계정 이름이 아니라 확인 절차와 선택한 scope**,
설치한 도구, 비공개 저장소 검증을 `MEMORY.md`에 기록한다. 개인 이메일과 토큰은 기록하지 않는다.

변경된 계획·설정·체크 상태를 한 커밋에 담아 push한다.

`git status --short`에서 이번 단계가 바꾼 계획·설정 파일만 정확한 경로로 stage하고,
`git diff --cached --name-only`로 확인한 뒤 commit한다.

```bash
git commit -m "환경과 비공개 저장소 준비"
git push
```

`✅ 준비 완료 — 비공개 저장소와 실행 환경을 확인했습니다.`라고 알리고 결과물 유형에 맞는 구현
파일로 바로 이어간다.
