# Codex Sites 웹앱 경로

읽는 조건: 결과물 유형이 `web_app`일 때만 읽는다. 이 파일은 결과물 유형을 새로 만들지 않고,
`web_app`의 구현·저장·배포 대상을 고르는 내부 실행 프로필이다.

## 1. 배포 대상 판정

`PLAN.md`의 `web_delivery_target`을 다음 값 하나로 확정한다.

- `existing`: 기존 프로젝트의 검증된 배포·데이터 경로를 그대로 사용
- `codex_sites`: Codex Sites로 구현·저장·배포
- `vercel_supabase`: Sites를 사용할 수 없거나 호환되지 않을 때의 새 웹앱 기본 폴백
- `n/a`: 웹앱이 아닌 결과물

다음 우선순위를 지킨다.

1. 기존 프로젝트에 `.openai/hosting.json`과 유효한 `project_id`가 있으면 `codex_sites`를 유지한다.
2. 그 외 `adaptive` 프로젝트에 기존 배포·DB·인증 경로가 있으면 `existing`이다. 명시적 마이그레이션
   요청 없이 Vercel·Supabase 프로젝트를 Sites로 옮기지 않는다.
3. 새 `guided` 웹앱이고 현재 표면이 ChatGPT 데스크톱·웹의 Codex이며 Sites 도구가 실제로 호출
   가능하면 아래 호환성 판정을 한다.
4. 호환되면 `codex_sites`, 아니면 `vercel_supabase`를 선택한다. 판정 가능한 내용을 사용자에게
   선택 질문으로 돌리지 않는다.
5. Claude Code, Sites 관리 기능이 없는 Codex CLI·IDE 단독 환경, Sites 비활성화·quota·권한 오류는
   `vercel_supabase`로 폴백한다.

선택한 값과 한 줄 이유를 `PLAN.md` 메타데이터와 `MEMORY.md`에 남긴다. 폴백은 원본 기능을 줄이는
근거가 아니다. 폴백에 새 가입·비용·계정 선택이 필요할 때만 기존 사람 게이트를 적용한다.

## 2. Sites 호환성

다음 조건이면 Sites를 우선한다.

- 새 프로젝트이며 지원되는 Sites starter 또는 Cloudflare Worker 호환 JavaScript/TypeScript
  결과로 만들 수 있다.
- 정적 사이트, 랜딩 페이지, 대시보드, 포털, 게임 또는 한두 개의 명확한 업무 흐름인 웹앱이다.
- 영구 구조화 데이터는 D1, 파일은 R2, 로그인은 Sign in with ChatGPT 또는 workspace identity로
  충족할 수 있다.
- 외부 API는 runtime 환경변수와 지원되는 네트워크 경계에서 호출할 수 있다.
- 기획서의 공개 범위와 Sites workspace 정책이 충돌하지 않는다.

다음 신호가 있으면 Sites를 억지로 쓰지 않고 폴백한다.

- 기존 Vercel·Supabase·다른 배포 경로가 이미 작동한다.
- Google 등 특정 외부 identity provider가 핵심인데 현재 Sites의 해당 인증 경로를 실제로 확인할
  수 없다.
- 지원되지 않는 framework, private network, 별도 database, 장기 background service 또는 hosting
  pattern이 필수다.
- PHI·결제카드·금융 거래, 13세 미만 또는 해당 지역 디지털 동의 연령 미만 대상, 데이터·inference
  residency 요구처럼 Sites 정책과 맞지 않는다. 이 경우 외부 스택을 쓰더라도 보안·법적 결정을
  사용자에게 명확히 돌린다.
- Sites가 public beta 제한, plan·region·workspace 설정, quota 또는 관리 권한 때문에 실제로
  생성·저장·배포할 수 없다.

외부 OAuth나 지원 여부가 불명확할 때 기능을 추측하지 않는다. 현재 Sites 도구 설명과 공식 문서를
확인하고, 확인되지 않으면 폴백한다.

## 3. 저장·인증 선택

`codex_sites`에서는 기획서에 필요한 것만 선언한다.

| 요구사항 | 선택 |
|---|---|
| 영구 데이터 없음 | D1·R2 모두 `null` |
| 사용자 기록·진행·설정·업무 상태 | D1 |
| 이미지·문서·영상·오디오 업로드 | R2, 검색·소유권 metadata가 있으면 D1도 사용 |
| ChatGPT 로그인 또는 workspace 사용자 | Sites가 제공하는 인증 경로와 서버 측 authorization |
| 특정 외부 OAuth | 현재 지원 확인 후 Sites 또는 `vercel_supabase` 폴백 |

- 브라우저 저장소는 기기 로컬 선호나 임시 draft에만 쓴다. 제품 데이터의 source of truth로 쓰지 않는다.
- `.openai/hosting.json`에는 `project_id`, 논리적 `d1`, `r2` binding만 둔다. 토큰·이메일·환경변수 값을
  넣지 않는다.
- D1 schema와 migration을 소스에 남기고, runtime query는 prepared statement와 서버 측 권한 확인을
  사용한다.
- Sites runtime secret은 Sites 설정에서 관리한다. 로컬 `.env`에는 키 이름만 맞추고 실제 값을
  commit하지 않는다.

## 4. Orange Build 안에서 Sites 실행

`codex_sites`가 확정되면 현재 설치된 Sites의 `sites-building`과 `sites-hosting`을 사용한다.

- `SOURCE_PLAN.md`, `PLAN.md`의 REQ·TEST·결과물 인벤토리를 Sites workflow의 제품 계약으로 넘긴다.
- Orange Build 사용자는 기본 구현에서 별도 디자인 선택을 원하지 않는 것으로 이미 결정했다.
  **디자인 picker 없이** 현재 PLAN과 기본 UI 원칙으로 진행한다. Stitch나 시안 비교를 열지 않는다.
- Sites가 내부 구현·HMR 확인을 위해 개발 서버와 in-app preview를 열 수는 있다. 이를 사용자에게
  실행시키거나 localhost를 첫 결과로 전달하지 않는다. 사용자에게 주는 첫 결과는 production URL이다.
- 기획서에서 이미 답한 audience·purpose·behavior·data 질문을 다시 묻지 않는다.
- 새 Site는 생성 직후 제한된 접근으로 검토한다. 기획서에 공개 대상이 이미 명확하면 안전 검토 뒤
  그 범위로 공개하고, 불명확하면 private deployment를 유지한다. GitHub 저장소 `PUBLIC` 기본값과
  Sites 방문 권한은 별도다.
- `create_site`는 같은 프로젝트에서 한 번만 호출하고 반환한 `project_id`를 그대로 보존한다.
- 검증된 정확한 commit을 GitHub `origin`과 Sites source repository 양쪽에 보낸다. Sites credential은
  URL·Git 설정·로그에 저장하지 않고 per-command 인증으로만 사용한다. Sites source repository가
  공개 GitHub 저장소 증거를 대신하지 않는다.
- source를 바꾼 뒤에는 새 version을 저장하고 그 version만 배포한다. 배포 상태가 terminal success가
  될 때까지 확인한다.

Sites 생성·배포가 호환성 또는 beta 제약으로 실패하면 같은 호출을 무한 반복하지 않는다. 정확한
오류를 기록하고 `vercel_supabase`로 전환해 `phase-connect.md`의 폴백 준비부터 자동 재개한다.

## 5. Sites 완료 게이트

아래가 모두 있어야 `codex_sites` 웹앱을 완료로 판정한다.

- production build와 관련 테스트 통과
- `.openai/hosting.json`의 유효한 `project_id`와 필요한 D1/R2 binding
- D1 schema 변경 시 생성·검토한 migration
- 검증한 commit과 연결된 saved version
- deployment status `succeeded`와 정확한 production URL
- production URL에서 핵심 입력→처리→결과 흐름 `TESTED`
- D1 쓰기 후 재조회, R2 업로드 후 조회·권한 확인 등 사용한 저장소의 왕복 증거
- 로그인 없음·로그인·권한 없음 등 계획된 Sites 인증·authorization 경계
- 계획한 방문자 범위에서 접근 가능하고 더 넓은 범위에서는 노출되지 않는지 확인
- runtime secret 미노출, `.env` 미추적, `.openai/hosting.json`에 secret 없음
- public GitHub 저장소와 Sites source repository가 같은 검증 commit을 가리키는 증거

HTTP 200, `create_site` 성공, version 저장 또는 URL 생성 중 하나만으로 완료라고 하지 않는다.

## 공식 기준

- [OpenAI Sites documentation](https://learn.chatgpt.com/docs/sites)
- [Build and deploy internal apps with Sites](https://learn.chatgpt.com/use-cases/build-and-deploy-internal-apps)
