# Orange Build

[Orange Build App](https://build.myorange.io/)에서 만든 기획서나 대화로 정리한 아이디어를 받아 웹앱·AI 작업 스킬·자동화를 실제
작동 결과까지 구현하는 Codex·Claude Code 플러그인입니다. 기획서가 없어도 `orange-start`로 시작하면
필요한 질문을 거쳐 기획서부터 만듭니다.

## 무엇을 완성하나요

| 결과물 | 첫 작동 결과 | 완료 기준 |
|---|---|---|
| 웹앱 | 실제 production URL | 라이브 핵심 흐름, 데이터·권한·상태, build와 테스트 |
| AI 작업 스킬 | 대표 요청의 실제 출력 | 구조 검증, 긍정·비트리거, fixture, 새 컨텍스트 호출 |
| 자동화 | dry-run 결과와 run id | 중복 방지, 재시도·로그, 승인된 샘플 live-run |

`구현해줘`, `만들어줘`, `완성해줘`라고 요청하면 로컬 코드나 build에서 멈추지 않습니다. 결과물에 맞춰
commit·push와 production 배포 또는 활성화까지 진행합니다. 사용자가 `배포하지 마`, `커밋하지 마`,
`외부 발송은 하지 마`라고 제한한 경우에는 그 제한을 지키고 남은 검증을 분명히 표시합니다.

```text
기획서 가져오기 또는 아이디어 인터뷰
→ SOURCE_PLAN.md 원본 보존
→ PLAN.md 요구사항·TEST 계약
→ 필요한 설치·계정·브라우저 준비
→ 결과물별 구현과 첫 작동 결과
→ 자가 테스트·수정·재검증
→ 원본 기획서 전체 대조
→ 배포·활성화·완료 보고
```

## 시작하기

### Orange Build App 기획서가 있을 때

1. [Orange Build App](https://build.myorange.io/)에서 기획서를 완성합니다.
2. 결과 화면에서 **orange-start용 복사**를 선택합니다.
3. 새 프로젝트 폴더에서 Codex 또는 Claude Code를 엽니다.
4. 복사한 내용을 붙여넣고 `orange-start`를 호출합니다.

복사문에 `contract_version: 2`와 `deliverable_kind`가 있으면 결과물 유형을 그대로 사용합니다.
원문은 `SOURCE_PLAN.md`에 보존하고, 핵심 기능·포함 범위·사용 흐름·성공 기준·TEST를 `PLAN.md`의
`REQ-*`와 검증 증거로 연결합니다.

기존 v1 기획서와 TEST가 없는 초기 v2 기획서도 지원합니다. 필요한 호환 TEST는 이미 받은 내용에서
만들며 같은 질문을 다시 하지 않습니다. 지원 범위보다 높은 계약 버전은 추측하지 않고 플러그인
업데이트가 필요하다고 안내합니다.

### 기획서가 없을 때

새 프로젝트 폴더에서 `orange-start`만 호출하고 만들고 싶은 것을 한두 문장으로 말하세요. Orange
Build는 이미 답한 내용을 건너뛰며, 결과물 유형에 맞춰 필요한 질문만 한 번에 하나씩 진행합니다.

답변은 `SOURCE_PLAN.md`로 정리되고, 이어서 `PLAN.md`의 요구사항 추적·사전 준비·구현·검증 흐름으로
진행합니다. 아이디어가 없으면 편집 가능한 제안을 받을 수 있으며, 충분히 정했다면 “전부 건너뛰기”로
현재 정보와 명시한 가정만 사용해 시작할 수 있습니다.

## 설치

### Codex

```bash
codex plugin marketplace add myorange-io/orange-build
codex plugin add orange-build@orange-build
```

새 task에서 `$orange-start` 또는 “오렌지 빌드 시작”이라고 요청합니다.

Orange Build 교육에서는 Codex의 모델 선택기에서 **GPT-5.6**을 사용합니다. 플러그인은 모델이나 추론
수준을 자동 변경하지 않습니다. GPT-5.6에는 산출물·보호할 요구사항·완료 증거·사람이 결정할 경계만
명확히 주고, 조사 순서와 도구 선택은 맡깁니다. 탐색·테스트·로그 분석처럼 독립된 읽기 중심 작업이
둘 이상일 때만 서브에이전트를 제한적으로 병렬 사용하고, 같은 파일의 동시 수정과 배포·발송·삭제
같은 외부 변경은 한 흐름에서 순차 처리합니다.

이 방식은 OpenAI의 [Customization overview](https://learn.chatgpt.com/docs/customization/overview)와
[GPT-5.6 model guidance](https://developers.openai.com/api/docs/guides/model-guidance?model=gpt-5.6)를
따릅니다. 저장소의 지속 규칙은 작은 `AGENTS.md`에, 반복 구현 절차는 스킬과 필요한 reference에,
GitHub·브라우저·배포 같은 외부 시스템 연결은 현재 제공되는 도구나 MCP에 둡니다.

업데이트할 때는 다음을 실행한 뒤 새 task를 엽니다.

```bash
codex plugin marketplace upgrade orange-build
codex plugin add orange-build@orange-build
```

`codex plugin list`에 구형 `orange-build@personal`이 남아 있으면 같은 `orange-start`가 중복될 수
있습니다. 구형 항목만 제거합니다.

```bash
codex plugin remove orange-build@personal
```

### Claude Code

```bash
claude plugin marketplace add myorange-io/orange-build
claude plugin install orange-build@orange-build
```

새 세션에서 `/orange-start` 또는 자연어 요청으로 시작합니다.

업데이트할 때는 다음을 실행하고 Claude Code를 다시 시작합니다.

```bash
claude plugin marketplace update orange-build
claude plugin update orange-build@orange-build
```

`claude plugin list`에 같은 `orange-start`를 제공하는 구형 설치본이 있으면 그 항목만 uninstall합니다.

## 진행 방식

### 프로젝트 상태에 맞춘 실행

Orange Build는 숙련도를 묻지 않고 작업 폴더를 보고 실행 방식을 고릅니다.

- `guided`: 새 폴더 또는 기획부터 시작하는 작업입니다. 준비 카드, 설치 보조, 계정 확인, 첫 배포와
  초보자 보호장치를 적용합니다.
- `adaptive`: 코드·Git 원격·CI·배포 설정이 있는 기존 프로젝트입니다. 준비된 환경을 다시 설정하지
  않고 기존 명령·구조·배포 경로를 우선합니다.

두 방식 모두 원본 요구사항 추적과 완료 검증을 유지합니다. `orange-resume`을 호출하면 `PLAN.md`,
검증 증거, 최근 커밋을 읽고 다음 미완료 요구사항부터 이어서 진행합니다.

Codex에서는 `orange-start`와 `orange-resume`이 GPT-5.6 실행 프로필을 적용합니다. Claude Code에서는
같은 결과 계약과 사람 결정 게이트를 유지하되 현재 계정의 최신 고성능 모델을 사용합니다.

### Codex Sites 우선 배포

새 웹앱을 Codex 데스크톱·웹에서 시작하고 현재 Sites 기능과 기획서가 호환되면 **Codex Sites를
기본 배포 경로**로 사용합니다. 별도의 Vercel·Supabase 가입 없이 정적·full-stack 웹앱을 배포하고,
필요한 구조화 데이터는 D1, 업로드 파일은 R2, ChatGPT·workspace 사용자는 Sites 인증 경로로
구현합니다. Sites 내부 preview는 에이전트가 관리하며 참가자에게 주는 첫 결과는 production URL입니다.

다음 경우에는 기존 경로나 Vercel·Supabase로 자동 폴백합니다.

- 이미 작동하는 배포·DB·인증 경로가 있는 기존 프로젝트
- Claude Code 또는 Sites 관리 기능이 없는 Codex 표면
- 특정 외부 OAuth가 핵심인데 현재 Sites 지원을 확인할 수 없는 경우
- 지원되지 않는 framework·private network·database·background service가 필요한 경우
- Sites의 public beta, plan·region·workspace·quota 제한으로 실제 배포할 수 없는 경우
- 결제카드·금융 거래·의료정보·아동 대상·데이터 residency처럼 Sites 정책과 맞지 않는 경우

Sites는 디자인 시안을 고르는 단계로 사용하지 않습니다. 기본 `orange-start`에서는 디자인 picker와
Stitch를 건너뛰고 기획서대로 구현하며, 디자인 개선은 최종 검증 뒤 `orange-design`에서만 진행합니다.
Sites 방문자 접근 범위는 GitHub 저장소 공개 여부와 별개로 검증합니다. 새 GitHub 저장소의 기본
visibility는 계속 `PUBLIC`이고, Sites는 기획서에 정한 대상에게만 공개합니다.

현재 Sites는 public beta이며 플랜·지역·workspace 설정에 따라 가용성과 한도가 달라질 수 있습니다.
자세한 내용은 [OpenAI Sites 문서](https://learn.chatgpt.com/docs/sites)와
[Sites 내부 앱 사례](https://learn.chatgpt.com/use-cases/build-and-deploy-internal-apps)를 참고하세요.

### 준비·설치·계정

기획서를 읽고 필요한 도구·계정·권한·브라우저 설정만 확인합니다. Node.js, GitHub CLI, Sites,
Vercel CLI, Python, MCP와 프로젝트 package는 선택한 경로에 필요한 경우에만 정확한 변경 목록을
보여주고 한 번 동의받은 뒤 설치·등록·상태 확인까지 진행합니다.

가입·로그인·2FA·CAPTCHA·약관·결제·여러 계정 중 선택은 사용자가 직접 합니다. 그 외 저장소 생성,
프로젝트 연결, OAuth callback, 최소 권한 설정, 브라우저 이동은 현재 사용할 수 있는 도구로 최대한
도와줍니다. GitHub·Sites workspace·Vercel·Supabase·Google 등 여러 계정이 로그인된 경우에는 대상 계정과 조직을
확인한 뒤 진행합니다.

새 GitHub 저장소는 기본으로 공개로 만들고 실제 visibility를 다시 확인합니다. 기획서에 비공개가
필요하거나 개인정보·비밀값 위험이 있으면 생성 전에 공개 범위를 확인합니다.

### 구현과 검증

원본 기획서는 `SOURCE_PLAN.md`에 보존합니다. `PLAN.md`에는 각 요구사항의 완료 조건, 구현 위치,
검증 방법, 실제 증거를 기록합니다. 모든 요구사항은 TEST 또는 보조 검증에 연결되고, `TESTED`,
`PARTIAL`, `INFERRED`를 구분합니다.

웹앱은 localhost를 기본 결과로 사용하지 않습니다. Sites가 내부 preview를 사용하더라도 참가자가
관리하지 않으며, 첫 완결 흐름을 production에 배포하고 URL에서
입력→처리→결과, console·network, 저장 후 재조회, 권한·오류·모바일 상태를 확인합니다. AI 작업
스킬은 새 컨텍스트의 실제 호출을, 자동화는 fixture·dry-run·중복 방지·재시도·결과 재조회를
확인합니다.

테스트 실패, 명백한 버그, 원본에 적힌 기능·상태·출력의 누락은 자동으로 수정하고 다시 검증합니다.
한 번에 원인 하나와 변경 변수 1~2개만 다루며, 기준선보다 좋아지고 기존 요구사항과 테스트가
회귀하지 않을 때만 변경을 채택합니다. 같은 오류가 두 번 반복되면 로그·재현 조건·직전 변경을
기준으로 진단합니다.

사람의 결정이 필요한 경우에만 멈춥니다.

- 제품 범위·핵심 흐름·브랜드 방향을 바꾸는 선택
- 비용·결제·권한 확대·개인정보·공개 범위 변경
- 데이터 삭제·마이그레이션·외부 발송·live 자동화 활성화
- 여러 계정·team·organization·production 대상 중 선택
- 테스트를 약화하거나 요구사항을 미완료로 남기는 결정

기록 파일은 개발의 중심이 아니라 누락 방지 장치로 사용합니다. `SOURCE_PLAN.md`는 최초 원본을
보존하고, `AGENTS.md`·`CLAUDE.md`는 없을 때 한 번만 만듭니다. 작은 코드 수정과 테스트 반복마다
문서를 고치지 않으며, 완결 흐름이 검증됐을 때 `PLAN.md`의 상태와 증거만 한 번 갱신합니다.
`MEMORY.md`는 중요한 결정·반복 실패 해결·사람 결정·최종 검증이 있을 때만 마일스톤당 한 항목을
남기고, 평범한 설치·구현·테스트 성공은 기록하지 않습니다.

### 다른 프로젝트를 참고해 개선한 사례

Orange Build도 처음부터 완성된 플러그인이 아니었습니다. 공개된 오픈소스 프로젝트와 디자인 참고
서비스가 문제를 해결하는 방식을 살펴보고, Orange Build의 교육 목적과 실행 환경에 필요한 원칙만
다시 구성해 현재의 구현·검증·디자인 개선 흐름에 반영했습니다.

| 참고 자료 | 참고한 점 | Orange Build에 반영한 방식 | 가져오지 않은 것 |
|---|---|---|---|
| [gstack](https://github.com/garrytan/gstack) | 현재 상태를 먼저 확인하고 계획·구현·검토·테스트·배포를 연결하는 흐름 | `orange-start`가 기존 프로젝트를 진단한 뒤 결과물별 완료 게이트와 배포까지 이어가도록 구성 | gstack 코드와 runtime 의존성 |
| [Hermes Agent Self-Evolution](https://github.com/NousResearch/hermes-agent-self-evolution) | 실행 기록에서 실패 원인을 찾고 회귀를 막으며 개선하는 방식 | 실패 로그와 재현 조건을 기준으로 작은 변경을 적용하고 의미 보존·전체 테스트·사람의 중요 결정 검토를 요구 | DSPy·GEPA와 학습·최적화 구현 |
| [Microsoft SkillOpt](https://github.com/microsoft/SkillOpt) | 제한된 크기의 변경을 기준선과 비교해 채택하거나 폐기하는 방식 | 한 번에 원인 하나와 변수 1~2개만 바꾸고, 기존 요구사항과 인접 사례가 회귀하지 않을 때만 채택 | SkillOpt 패키지와 optimizer 코드 |
| [MengTo/Skills](https://github.com/MengTo/Skills) | 막연한 취향보다 명세·화면 자료·디자인 시스템을 근거로 반복하는 방식 | `orange-design`이 기능을 고정하고 참고 화면과 디자인 원칙을 바탕으로 제한된 변형안을 비교하도록 구성 | 데모 코드·컴포넌트·이미지 등 원본 에셋 |
| [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp) | 공식 브라우저 도구를 설치해 실제 화면·console·network를 확인하는 방식 | 기획서와 환경에 도움이 될 때만 설치 동의를 받고 구성한 뒤 라이브 브라우저 검증에 사용 | 프로젝트 소스 코드와 불필요한 상시 의존성 |
| [getdesign.md](https://getdesign.md/) | 프로젝트와 어울리는 우수 디자인의 구조와 원칙을 비교하는 방식 | `orange-design`이 관련 사례를 최대 두 개까지 링크로 제안하고 사용자가 고른 뒤 일반 디자인 원칙만 적용 | 사례 서비스의 코드·브랜드·화면·이미지 |
| [Name That UI](https://namethatui.com/) | 사용자의 표현을 표준 UI 컴포넌트 명칭과 동작으로 구체화하는 방식 | 모호한 UI 요구를 정확한 컴포넌트 이름·상태·접근성 요구로 바꾸어 구현 범위를 명확하게 함 | 사이트 콘텐츠의 복제·수집과 원본 에셋 |

좋은 결과물과 오픈소스를 참고해 해결 원리를 자기 프로젝트에 맞게 적용하는 것도 바이브코딩의
유효한 개선 방법입니다. 다만 실제 코드를 재사용할 때는 해당 라이선스와 저작권 고지 의무를 먼저
확인해야 합니다. 비밀정보·개인정보·브랜드 에셋·라이선스가 불분명한 코드는 복사하지 않습니다.

### 웹앱 디자인

웹앱의 기본 흐름은 기능 구현·배포·최종 검증까지입니다. 이 과정에서 디자인 시안을 만들거나 Stitch를
열지 않습니다. 완료 후 화면 디자인이 기대와 다르면 별도 `orange-design`을 호출합니다. 이 스킬은
기능·페이지·데이터·`PLAN.md`의 REQ와 TEST를 고정한 채 위계, 간격, 타이포그래피, 색상, 반응형을
개선하고 build·기능 테스트·라이브 visual QA를 다시 실행합니다.

`orange-design`은 프로젝트의 기존 `DESIGN.md`를 가장 먼저 사용합니다. 없다면 사용자가 확인한
조직 홈페이지의 공개 페이지에서 디자인 원칙을 관찰해 `DESIGN.md` 초안을 만들 수 있습니다. URL을
추측하거나 로그인·접근 제한을 우회하지 않으며, 코드·이미지·로고·카피를 복사하지 않습니다. 저장 전
추출 범위와 diff를 보여주고 사용자의 동의를 받습니다.

[getdesign.md](https://getdesign.md/)는 디자인 시스템 분석을 비교할 때 쓰는 참고 카탈로그입니다.
특정 브랜드를 복제하지 않고 layout, hierarchy, type relationship, spacing rhythm, component rule 같은
일반 원칙만 가져옵니다. UI 표현이 모호하면 [Name That UI](https://namethatui.com/)로 `scrim`,
`toast`, `combobox`처럼 정확한 컴포넌트 이름과 동작을 정합니다. 사용자가 명시적으로 요청하거나
Stitch 시안을 가져온 경우에만 `orange-design` 안에서 대표 화면을 짧게 보정할 수 있습니다.

`orange-design`은 프로젝트의 목적·사용자·핵심 행동·정보 밀도에 맞는 getdesign.md 사례를 최대 두 개
추천할 수 있습니다. 각 안에는 **getdesign.md 분석 화면 링크**와 확인된 경우 **원본 서비스 화면 링크**를
함께 보여줍니다. 사용자가 링크를 본 뒤 A/B/현재 디자인 유지 중 하나를 선택하기 전에는 코드를 바꾸지
않습니다.

## 제공 스킬

| 스킬 | 사용 시점 |
|---|---|
| `orange-start` | 기획서를 가져오거나 아이디어부터 시작해 구현·검증·배포까지 진행할 때 |
| `orange-resume` | 중단된 프로젝트의 현재 상태를 읽고 다음 요구사항부터 이어갈 때 |
| `orange-design` | 최종 검증 뒤 디자인 사례를 링크로 비교·선택하고, 기능을 보존해 디자인 시스템과 화면을 개선할 때 |
| `orange-secure` | Orange Build로 만든 Next.js·Supabase 앱의 키 노출·RLS·민감정보 위험을 점검할 때 |

`orange-secure`는 사용자가 직접 호출하는 점검 도구입니다. 각 위험을 하나씩 보여주고 수정 전에는
확인을 받습니다.

## 프로젝트에 남는 파일

- `SOURCE_PLAN.md` — App에서 가져오거나 인터뷰로 만든 원본 기획서
- `PLAN.md` — REQ ID, 완료 조건, 검증 시나리오, 증거가 있는 실행 계약
- `DESIGN.md` — 승인된 디자인 원칙과 토큰. 조직 홈페이지에서 추출한 경우에도 사용자 검토 후 저장
- `MEMORY.md` — 주요 결정, 문제와 해결 기록
- `CASE.md` — 수작업을 대신하는 결과물일 때 만드는 사례 카드

완료는 필수 REQ와 TEST가 모두 PASS이고 실제 증거가 있을 때만 선언합니다. 일부가 미검증이면
`N/M 통과`와 남은 항목을 그대로 보여줍니다. App에서 시작한 작업은 사용자가 원할 때 GitHub URL,
배포 URL, `MEMORY.md`를 App에 되돌릴 수 있으며, 파일 업로드와 참가자 회고 작성은 사용자의 명시적
동의를 받은 뒤에만 보조합니다.

## 라이선스

MIT · v2.5.0
