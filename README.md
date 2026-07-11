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

복사문에는 `contract_version`과 `deliverable_kind`가 들어 있습니다. orange-start는 이 canonical
값을 그대로 사용해 웹앱·AI 작업 스킬·자동화로 분기하고, 원문은 `SOURCE_PLAN.md`에 보존합니다.
지원하는 계약보다 새 버전이면 추측해 구현하지 않고 플러그인 업데이트를 안내합니다. 기존 v1
복사문도 표시 이름을 기준으로 계속 지원합니다.

### 기획서가 없을 때

1. 비어 있는 새 프로젝트 폴더에서 Codex 또는 Claude Code를 엽니다.
2. `orange-start`만 호출합니다.
3. 만들고 싶은 아이디어를 한두 문장으로 답합니다.
4. 한 번에 하나씩 나오는 질문에 답합니다.

orange-start는 앱과 같은 순서로 최대 7개를 묻되, 아이디어에서 이미 확인된 단계는 건너뜁니다.
결과물 유형이 정해지면 웹앱·AI 작업 스킬·자동화에 맞는 질문으로 전환하고, 답변을
`SOURCE_PLAN.md`에 정리한 뒤 기존 `PLAN.md`·REQ 추적 흐름으로 바로 이어갑니다.

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

## 준비 사항

- Git과 GitHub 계정
- Codex 또는 Claude Code
- 웹앱이면 Vercel 계정
- 데이터 저장·OAuth·외부 API는 기획서가 요구할 때만

Node.js가 필요한 결과물인데 설치되어 있지 않으면 macOS·Windows의 사용 가능한 패키지 관리자로
설치를 시도하고 버전을 재확인합니다. 스킬이나 Python 자동화에 필요하지 않다면 설치하지 않습니다.

Google 계정이 여러 개 로그인되어 있으면 OAuth 승인 전에 사용할 계정을 직접 선택하게 합니다.
GitHub 사용자, Vercel 팀, Supabase 조직도 실제 identity를 보여주고 맞는지 확인합니다.

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
남은 항목을 그대로 보여줍니다.

## 강사용 노트

- 참가자는 기획서를 복사해 붙여넣거나, 빈 폴더에서 `orange-start`만 호출해 기획부터 시작합니다.
- 웹앱 실습의 첫 피드백은 localhost가 아니라 실제 Vercel URL입니다.
- Stitch를 진행한다면 기능 토론을 멈추고 시각 위계·색·간격만 보정합니다.
- 외부 발송·삭제·결제·live 자동화는 dry-run 뒤 대상과 건수를 보여주고 승인받습니다.
- 수업 전 GitHub·Vercel·Google의 여러 계정 상태를 정리하거나, 사용할 계정을 미리 정해두면
  OAuth 실수가 줄어듭니다.

## 라이선스

MIT · v2.1.0
