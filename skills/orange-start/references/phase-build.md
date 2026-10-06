# 웹앱 구현 — 승인받은 IA 단계 완성하기

목표: `PLAN.md`의 현재 IA STEP을 완결 흐름으로 구현하고 선택한 `completion_level`의 환경에서
사용자가 직접 확인할 결과를 보여준다.

먼저 `ia-collaboration.md`를 읽는다. 현재 STEP이 `AWAITING_APPROVAL`이면 확인할 변화·완료 확인·
제외 범위를 보여주고 답을 기다린다. 명시적 승인 전에는 코드·설정·테스트·프로젝트 문서를 수정하지
않는다. 승인 뒤에만 `IN_PROGRESS`로 바꾸고 현재 STEP을 구현한다.

`adaptive`에서는 먼저 `execution-profiles.md`를 읽고 기존 framework, package script, test, CI와
배포 경로를 사용한다. `completion_level: local`이면 `web_delivery_target: local`로 두고 배포 계정이나
원격 저장소를 요구하지 않는다. `shared | real_work`에서 `web_delivery_target: codex_sites`면 `codex-sites.md`와 설치된
`sites-building`·`sites-hosting`을, `vercel_supabase`면 아래 Vercel 폴백을 사용한다. 기존 경로면
그 프로젝트의 production 절차로 같은 완료 증거를 만든다.

시작할 때 `verification-loop.md`와 `self-improvement-loop.md`를 읽는다. `PLAN.md`의 TEST↔REQ
연결과 결과물 인벤토리를 구현 순서의 기준으로 삼고, TEST의 기대 결과나 통과 증거를 구현 편의에
맞게 줄이지 않는다.

금액·비율·효과 수치·자격·정책·개인정보처럼 사용자에게 사실로 보이는 값에 `FACT_UNVERIFIED` 신호가
있으면 `product-truth-gate.md`를 먼저 적용한다. 확인 전에는 관련 계산과 공개 문구를 구현·배포하지
않는다. 내부의 `TEST-*`, `REQ-*`, 임시 가정, 운영자 확인 필요 문구를 사용자 화면에 노출하는 것으로
우회하지 않는다.

## 1. 현재 STEP 확인

`SOURCE_PLAN.md`와 `PLAN.md`를 읽고 `current_step`에 연결된 `REQ-*`와 TEST만 사용자 가치가 끝까지
이어지는 세로 슬라이스로 묶는다. 미래 STEP의 요구사항을 미리 포함하지 않는다.

```text
입력 또는 시작
→ 실제 처리·저장·외부 호출
→ 사용자가 확인할 결과
→ 실패했을 때의 안내
```

첫 슬라이스는 가장 작은 **완결 흐름**이어야 한다. 첫 화면만 예쁘게 만들거나 모든 화면의 빈
껍데기만 만드는 방식은 쓰지 않는다. 여러 경로가 필요하면 첫 슬라이스에 함께 포함한다.

승인 직후 `PLAN.md`의 현재 STEP을 `IN_PROGRESS`로 바꾸고 관련 REQ에 구현 예정 파일과 검증
시나리오를 채운다. 연결된 TEST의 준비·행동·기대 결과·통과 증거와 결과물 인벤토리를 다시 센다.

## 2. 기본 UI와 경로

별도 디자인 도구 없이도 읽기 쉽고 작동하는 공통 바닥선을 먼저 둔다.

- 흰색·중립 배경, 읽기 쉬운 한글 폰트, 강조색 하나, 8px 안팎 radius, 충분한 간격
- 버튼·입력·카드·표는 설치된 공통 UI 컴포넌트를 우선 사용
- 본문·목록·표는 왼쪽 정렬을 기본으로 하고, 가장 중요한 행동 하나만 시각적으로 강조
- 보라 그라데이션·과한 그림자·발광·장식 이모지·동일한 3열 카드 남발 금지
- 모바일 폭에서 가로 넘침과 잘린 버튼이 없도록 구성

`PLAN.md`의 모든 경로를 인벤토리로 만든다. 각 경로에 다음이 있어야 한다.

- 목적과 1순위 정보
- 필수 입력·버튼·링크
- 로딩·빈 상태·오류·성공 피드백
- 권한이 없을 때의 동작
- 연결되는 다음 경로 또는 결과

디자인 참고자료가 없다는 이유로 경로나 기능을 빼지 않는다.

## 3. 데이터·인증·외부 연동

관련 REQ가 있을 때만 준비한다.

### 데이터 저장

- 데이터 모델은 화면 모양이 아니라 완료 조건에서 역산한다.
- 마이그레이션이나 스키마 파일을 저장소에 남겨 재현 가능하게 한다.
- `codex_sites`는 D1 schema·migration과 서버 측 authorization을, `vercel_supabase`의 Supabase는
  모든 public 테이블의 RLS와 로그인·역할 정책을 둔다.
- 공개 익명 입력과 비공개 관리자 조회가 함께 있으면, 클라이언트에 service-role 키를 주지 말고
  서버 라우트에서만 처리한다.
- 쓰기 성공만 확인하지 말고 **다시 조회해 같은 값이 보이는지** 검증한다.

### 인증과 권한

- 로그인 필요 여부와 역할을 `PLAN.md`대로 구현한다.
- 로그인·로그아웃·세션 없음·권한 없음 경로를 각각 확인한다.
- Sites의 Sign in with ChatGPT·workspace identity는 authorization을 서버에서 확인한다. Google
  OAuth를 쓰면 여러 계정 중 어느 계정과 OAuth 프로젝트를 사용하는지 `browser-steps.md`로 확인한다.

### 비밀값과 민감정보

- LLM·메일·service-role·OAuth secret은 서버 전용 환경변수로 둔다. `NEXT_PUBLIC_` 금지.
- 비밀번호는 직접 저장하지 않고 Auth를 사용한다.
- 주민번호·계좌·카드·바이오정보 등 암호화 의무 대상이 있으면 `sensitive-data.md`를 읽고
  대체·토큰화·암호화를 적용한다.
- `.env.local`과 실제 사용자 데이터는 commit하지 않는다.

## 4. 슬라이스 구현과 검증

슬라이스마다 다음 순서를 반복한다.

1. 관련 REQ와 TEST의 정상·빈 입력·실패 시나리오를 먼저 적는다.
2. 자동화할 수 있는 행동은 가능한 가장 작은 테스트를 먼저 추가해 의도한 이유로 실패하는
   **RED**를 확인한다.
3. UI, 서버 처리, 데이터·외부 연동을 끝까지 최소 구현해 **GREEN**으로 만든다.
4. 동작을 바꾸지 않고 중복과 불필요한 복잡성을 줄이는 **REFACTOR** 뒤 같은 테스트를 다시 실행한다.
   핵심 계산·변환은 단위 테스트, 경계 연결은 통합 테스트, 사용자 관찰은 브라우저 테스트로 둔다.
5. `package.json`의 실제 스크립트를 확인해 lint·test·production build를 실행한다.

   ```bash
   npm run lint
   npm run build
   ```

   테스트 스크립트가 있으면 함께 실행한다. 없으면 핵심 흐름에 맞는 최소 테스트를 만든 뒤 실행한다.

   사용자 대상 계산·주장이 있으면 기술 테스트와 별개로 `FACT_CONFIRMED` 근거를 확인한다. 코드가
   예시값대로 계산된다는 테스트만으로 실제 사업 규칙까지 증명했다고 보지 않는다.

6. 2~5의 수정·재검증 중에는 `PLAN.md`를 건드리지 않는다. 테스트·CI·실행 결과가 중간 증거다.
   `PLAN.md`는 IA 단계 상태 전이, 사람 결정, 실제 handoff, 최종 판정에서만 구현 위치·상태·
   `TESTED | PARTIAL | INFERRED` 증거를 한 번에 갱신한다. PASS는 명령 성공뿐 아니라 TEST의 준비와
   행동을 실제 수행해 기대 결과와 통과 증거를 관찰한 `TESTED`일 때만 쓴다. 원본 근거와 완료 조건은
   사람의 범위 변경 결정 없이는 다시 쓰지 않는다.

가까운 검증이나 실제 브라우저 관찰에서 failing test, console·network 오류, 누락된 상태·경로,
저장 불일치를 찾으면 승인 질문 없이 수정하고 2~6을 반복한다. 원본 범위·비용·권한·데이터·외부
발송이 바뀌는 해결책만 사람 결정 게이트로 보낸다.

각 후보는 기준선과 같은 입력·viewport·상태로 비교한다. 목표 결함이 실제로 좋아지고 보호된 REQ·
TEST·기존 test/build가 회귀하지 않을 때만 채택한다. 동일하거나 `PARTIAL`인 후보는 버리고, 최종
후보는 수정에 직접 쓰지 않은 인접 입력이나 상태 1개도 확인한다.

### 선택한 완료 수준에서 결과 확인

`local`이면 에이전트가 로컬 실행을 관리하고 핵심 흐름을 직접 확인한다. 사용자가 개발 서버를
수동으로 관리하게 하지 않는다. `shared` 또는 `real_work`이면 production build 통과 뒤 STEP 승인과
별도로 배포 직전 확인을 받고 `web_delivery_target`을 따른다.

- `local`: localhost 또는 로컬 앱에서 입력→처리→결과와 현재 STEP의 오류·빈 상태·권한·모바일
  조건을 확인한다. production URL, 원격 저장소, 배포 계정은 완료 조건이 아니다.

- `existing`: 기존 production 절차로 배포한다.
- `codex_sites`: 디자인 picker 없이 `codex-sites.md`와 설치된 Sites workflow로 정확한 source
  commit을 저장·배포하고 deployment status `succeeded`를 확인한다. Sites가 내부 preview를 한 번
  여는 것은 허용하되 첫 결과는 production URL이다.
- `vercel_supabase`: 아래 명령으로 Vercel production에 배포한다.

```bash
git commit -m "구현: 첫 작동 흐름"
git push
vercel --prod --yes
```

commit이 선택한 수준과 프로젝트 계약에 포함된 경우에만 이번 슬라이스의 코드·테스트·설정 경로를
정확히 stage한다. 사람 결정이나 handoff로
실제로 바뀐 경우에만 `PLAN.md`를 포함한다. 이 단계에서는 `MEMORY.md` 완료 기록을 미리 만들지 않는다.
`git diff --cached --name-only`를 확인하고 기존 사용자 변경을 함께 넣지 않는다.

`shared | real_work`이면 선택한 배포 경로가 반환한 URL을 보여주고 다음을 확인한다.

- 배포 상태가 Sites `succeeded`, Vercel `READY` 또는 기존 공급자의 terminal success이고 루트 및
  관련 경로가 2xx/예상 redirect를 반환한다.
- 연결된 브라우저 도구가 있으면 URL에서 실제 입력→처리→결과 흐름을 수행한다.
- 브라우저 도구가 없으면 API·HTTP 테스트를 실행하고, 시각 확인이 필요한 마지막 한 단계만
  사용자에게 요청한다.
- 저장 기능이면 배포 환경에서 생성 후 다시 조회한다.
- 실패 입력이면 사용자에게 이해 가능한 오류가 보인다.

브라우저에서는 화면이 보인다는 사실만 확인하지 않는다. 선택한 실행 환경에서 사용자 트리거·입력
→ 실제 network 요청 → 서버 처리·데이터 변화·외부 호출 → 응답 → 사용자에게 보이는 결과를 끝까지
연결한다. 관련 console 오류와 실패한 network 요청이 없는지 확인하고 저장 기능은 재조회 증거까지
남긴다. 일부 경계만 확인했으면 `PARTIAL`, 코드나 HTTP 상태로 추론했으면 `INFERRED`이며 TEST PASS가
아니다.

현재 STEP 결과가 준비되면 `PLAN.md`를 `AWAITING_REVIEW`로 바꾸고 사용자에게 보여준다.

```text
✅ STEP 결과 — [로컬 주소 또는 공유 URL]
[무엇을 입력해 어떤 결과까지 확인했는지]
```

이어서 `이대로 다음 개선 / 현재 결과 수정 / 구현 방향 다시 정하기` 중 하나를 받고 기다린다.
현재 결과 승인은 배포·외부 변경 승인과 별개다.

### 이후 슬라이스

현재 결과를 승인받은 뒤에만 다음 STEP의 승인 질문으로 이동한다. 같은 방식으로
구현→lint/test/build→선택한 수준의 실제 확인을 반복한다. 원격 저장과 배포는 `shared | real_work`에서
계약에 필요할 때만 수행한다.

## 5. 웹앱 자체 점검

사용자에게 완성이라고 말하기 전에 전체 경로를 한 번 훑는다.

- [ ] `PLAN.md`의 모든 웹 경로가 실제로 존재하고 서로 연결된다.
- [ ] 핵심 흐름을 선택한 완료 수준의 환경에서 처음부터 끝까지 실행했다.
- [ ] 저장 후 재조회, 로그인 역할, 외부 연동이 계획대로 동작한다.
- [ ] 로딩·빈 상태·오류·성공 피드백이 있다.
- [ ] 모바일 폭에서도 핵심 행동이 가능하다.
- [ ] Sites는 서버 authorization·D1/R2 binding·runtime secret을, Supabase는 RLS·정책·서버 전용
      키를 확인했다.
- [ ] `git ls-files`에 `.env`·토큰·실데이터가 없다.
- [ ] `npm run build`와 관련 테스트가 통과한다.
- [ ] `shared | real_work`이면 선택한 production 배포가 terminal success이고 정확한 URL이 있다.
- [ ] `codex_sites`면 saved version·검증 commit·Sites source·GitHub origin이 일치하고 D1/R2 왕복
      검증과 방문자 접근 범위를 확인했다.
- [ ] 결과물 인벤토리의 예상 목록·수량과 실제 경로·흐름·연동·역할별 상태 수량이 일치한다.
- [ ] REQ와 연결된 예상 결과물 경로에서 placeholder, 빈 handler, 고정 성공값, no-op이 없다.
- [ ] 현재 STEP에 연결된 TEST의 준비·행동을 선택한 환경에서 수행하고 `TESTED` 증거를 남겼다.
- [ ] UI가 핵심이면 desktop/mobile 및 상호작용 뒤 상태에서 기능·접근성·가독성을 확인했다.

여기서 발견한 누락은 REQ 상태를 TODO/FAIL로 되돌리고 자동으로 고친 뒤 전체 점검을 다시 실행한다.
화면이 200을 반환한다는 것만으로
기능을 PASS 처리하지 않는다. 저장소 전체의 무관한 TODO·예제 placeholder까지 이번 결과물의
blocker로 확장하지 않고, 점검 범위는 REQ와 결과물 인벤토리에 연결된 경로로 제한한다.

## 6. 구현 단계 마무리

모든 STEP이 사용자에게 승인됐으면 중간 체크박스를 만들지 않고 `README.md`에 한 줄 소개, 실행·배포 방법,
필요한 환경변수 **이름만** 적는다. 실제 값은 적지 않는다.

사용자가 과정 기록을 요청했다면 `memory-log.md`의 선택 중간 항목을 남길 수 있다. 사용자가 교육용
사례 카드를 요청했을 때만 `case-card.md`를 따라 `CASE.md`를 만든다. 필수 `MEMORY.md` 최종 검증
블록은 아직 만들지 않고 전체 완료 판정 직후 생성한다.

아직 `완성`이라고 하지 말고 `phase-verify.md`로 이어가 선택한 완료 수준에서 원본 약속을 전체 대조한다.

최종 검증을 마친 뒤 사용자가 디자인 개선을 원하면 `orange-design`으로 전환한다. 이때도 `PLAN.md`의
기능·페이지·데이터·TEST는 디자인 변경의 대상이 아니다.
