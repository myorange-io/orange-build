# 최종 검증 — 원본 기획서와 결과물을 다시 맞추기

목표: 만든 파일 수가 아니라 `SOURCE_PLAN.md`의 약속이 실제로 충족됐는지 증거로 판정한다.

시작할 때 `verification-loop.md`, `self-improvement-loop.md`, `memory-log.md`를 읽는다. TEST↔REQ 연결,
결과물 인벤토리, 증거 등급과 자동 수정·사람 결정 경계, 완료 기록의 중복 방지를 최종 판정의 공통
기준으로 사용한다.

## 1. 원본 추적 감사

`SOURCE_PLAN.md`와 `PLAN.md`를 나란히 읽는다. 원본의 다음 항목을 하나씩 세어 추적표와 대조한다.

- 핵심 기능
- 포함 범위
- 사용 흐름
- 성공 기준
- 직접 확인할 TEST의 준비·행동·기대 결과·통과 증거
- 사용할 자료·개인정보와 공개·비공개 경계
- AI 역할과 사람 확인 지점

각 항목이 하나 이상의 `REQ-*`에 연결되어야 한다. 빠진 항목을 발견하면 새 REQ로 복구하고
구현 단계로 돌아간다. 디자인 참고자료 누락, 시간 부족, 기술 난이도는 원본 삭제 근거가 아니다.

제외 범위가 원본보다 늘었다면 `가정과 결정`에 사용자의 명시적 결정과 이유가 있는지 확인한다.
없으면 완료를 중단하고 원래 범위를 구현한다.

### TEST 계약 감사

- 최신 contract v2 원본에 TEST가 있으면 `TEST-01`~`TEST-03` 정확히 세 개인지 확인한다.
- 각 TEST의 제목과 `준비`, `행동`, `기대 결과`, `통과 증거`가 원문과 일치하는지 확인한다.
- TEST마다 관련 REQ가 하나 이상 연결됐고, 모든 REQ가 TEST 또는 더 작은 보조 검증에 포함됐는지
  양방향으로 대조한다.
- TEST 항목이 없는 기존 v2 또는 v1/legacy는 원문을 바꾸거나 추가 질문하지 않고 대표 성공,
  빈 값·잘못된 값, 유형별 예외의 `derived_compat` TEST 세 개와 파생 근거가 있는지 확인한다.

누락되거나 더 쉬운 시나리오로 바뀐 TEST는 원본 계약 누락이다. 관련 REQ와 TEST를 TODO로 되돌리고
구현 단계에서 복구한다.

## 2. 증거 표 감사

각 REQ에 다음 다섯 가지가 있어야 한다.

1. 원본 근거
2. 관찰 가능한 완료 조건
3. 실제 구현 위치
4. 실행한 검증과 기대 결과
5. PASS 증거: 테스트 출력, live URL의 관찰, 실제 호출 결과 또는 run id

`구현 위치: 미정`, `NOT_RUN`, `대략 동작`, HTTP 200만 있는 항목은 PASS가 아니다. 증거가 약하면
다시 검증하거나 테스트를 보강한다.

각 REQ와 TEST의 증거에는 아래 등급 하나가 있어야 한다.

- `TESTED`: 계획한 준비와 행동을 실제 수행하고 기대 결과와 통과 증거를 관찰함
- `PARTIAL`: 일부 계층·분기 또는 대체 검증만 실행함
- `INFERRED`: 코드·설정·HTTP 상태만 보고 동작을 추론함

필수 REQ와 TEST는 `TESTED`일 때만 PASS다. `PARTIAL`, `INFERRED`, `NOT_RUN`, `BLOCKED`는 PASS 수에
포함하지 않는다. 자동화의 dry-run만 확인했다면 `DRY_RUN_PASS / PARTIAL`로 둔다.

### 제품 사실 감사

`product-truth-gate.md`에 따라 사용자 화면·AI 출력·자동화 결과에서 금액·비율·정량 효과·자격·정책·
개인정보·외부 실행 규칙을 찾는다. 각 사실에 `FACT_CONFIRMED: source | user` 근거가 있는지 확인한다.
단일 TEST의 예시, 코드 상수, 동일한 계산을 반복한 테스트만으로 실제 사업 규칙을 증명하지 않는다.

- 확인되지 않은 사실을 제품에 넣고 면책 문구를 붙인 경우 PASS가 아니다.
- `TEST-*`, `REQ-*`, `임시 가정`, `운영자 확인 후 변경` 같은 내부 문구가 공개 UI·AI 최종 출력·외부
  메시지에 노출되면 제거하고 원래 사실을 확인한다.
- 불확실한 핵심 사실이 남으면 최적의 권장안과 대안을 제시해 한 번 묻고 관련 REQ·TEST를
  `BLOCKED · FACT_UNVERIFIED`로 둔다. 답과 무관한 검증은 계속한다.

### 결과물 인벤토리 감사

`PLAN.md`의 예상 목록·수량을 실제 결과와 같은 기준으로 다시 센다.

- 웹앱: 경로·페이지, 완결 흐름, 데이터·외부 연동, 역할별 상태
- AI 스킬: 필수 파일, scripts/references/assets, 약속한 출력, 호출 fixture
- 자동화: 트리거, 실행 파일·workflow, 입력→출력 매핑, runbook, 실행 결과·로그

예상보다 적거나 이름만 있고 동작하지 않는 항목이 있으면 관련 REQ를 다시 연다. placeholder, 빈
handler/script, 고정 성공값, no-op 점검은 **REQ와 연결된 예상 결과물 경로**에만 적용한다. 저장소의
무관한 TODO·예제·향후 작업을 이번 완료 blocker로 확대하지 않는다.

### 사전 준비 감사

- `REQUIRED` 준비 항목이 모두 `READY`다. `USER_ACTION`이 남았으면 완료가 아니라 blocker이고,
  `NOT_NEEDED`에는 기획서 근거가 있다.
- 설치한 도구는 사용자 동의 범위와 버전·import/build 증거가 있다.
- 필요한 계정·team·organization을 CLI와 브라우저에서 대조했다.
- 기획서에 필요 없는 Vercel·Supabase·Node.js·외부 계정을 습관적으로 설치·연결하지 않았다.
- `web_app`의 `web_delivery_target`이 `existing | codex_sites | vercel_supabase` 중 하나이고 판정
  이유가 있으며, 선택되지 않은 배포·DB 서비스는 설치하지 않았다.
- 비밀번호·토큰·개인 이메일을 계획·로그·커밋에 남기지 않았다.
- `HELPFUL` 도구는 기획서 신호와 부족했던 능력이 기록돼 있다. `SKIPPED`·`FAILED`면 대체 검증이
  PASS했고, 도움 도구 설치 실패만으로 결과물을 미완료로 판정하지 않았다.
- 같은 능력의 MCP·connector·프로젝트 package를 중복 설치하지 않았고 현재 세션을 실행한 호스트
  하나만 변경했다.
- 기존 MCP가 `EXISTING_UNSAFE`면 사용하지 않았고, 재구성했다면 정확한 변경 동의·원본 설정
  backup·실패 rollback 증거가 있다.
- MCP `등록 성공`, `인증 성공`, `현재 세션 실제 도구 호출 성공`을 구분했다. 등록 목록만 보고
  runtime 진단이 완료됐다고 하지 않았다.
- Chrome DevTools MCP는 격리·통계/CrUX 차단으로 등록했고, 개인 Chrome profile의 remote debugging에
  동의 없이 붙지 않았다.
- Supabase MCP는 개발·테스트 project에 `project_ref`·`read_only=true`·최소 feature로 제한했다.

## 3. 유형별 완료 게이트

### `web_app`

- production build·lint·테스트 통과
- 선택한 배포의 terminal success와 공유할 production URL
- `codex_sites`는 유효한 `.openai/hosting.json`, saved version, deployment `succeeded`, 검증 commit과
  GitHub·Sites source 일치, 계획한 Sites 접근 범위 확인
- `vercel_supabase`는 Vercel production `READY`; Supabase를 쓰면 RLS·정책·서버 전용 키 확인
- 핵심 사용자 흐름을 라이브 URL에서 처음부터 끝까지 실행
- 저장 후 재조회 또는 외부 연동 결과 재확인. Sites D1/R2를 쓰면 각 binding의 실제 왕복 증거 확인
- 로그인 없음·로그인·권한 없음 등 계획된 역할 검증
- 로딩·빈 상태·오류·성공 피드백과 모바일 핵심 흐름 확인
- `.env` 미추적, 서버 전용 키 미노출, 선택한 저장소의 authorization·접근 정책 확인
- `.openai/hosting.json`에는 Sites secret·개인정보가 없고 runtime 값은 Sites 설정에서 관리
- `PLAN.md`의 모든 경로가 실제 존재
- UI가 핵심이면 canonical component 이름에 맞는 focus·keyboard·dismissal·blocking 동작 확인
- functional QA와 visual QA를 분리해 desktop/mobile, loading·empty·error·success, 상호작용 뒤 상태 확인

### `ai_skill`

- SKILL.md 구조 validator 통과
- 폴더명·frontmatter 이름·참조 파일 일치
- 긍정 트리거 3개에서 기대한 스킬 사용과 출력 확인
- 비트리거 2개에서 부적절한 개입 없음
- 정상·빈/깨진 입력 fixture 통과
- 새 컨텍스트의 대표 실제 호출 결과 확인
- 추가 스크립트의 성공·실패 exit와 출력 검증

### `automation`

- fixture 테스트와 dry-run 통과
- 같은 입력 2회에서 중복 결과 없음
- 일시 오류의 제한 재시도와 영구 오류의 즉시 실패 확인
- run id와 읽음·성공·건너뜀·실패 건수 로그 확인
- 트리거, 최소 권한, 중지·복구·수동 재실행 문서 확인
- 외부 쓰기가 있으면 사용자 승인 후 샘플 1건 live 결과 재조회

외부 쓰기 승인이 없어 dry-run만 통과했다면 `DRY_RUN_PASS`로 두고 최종 live 검증을 남은 일로
명시한다.

## 4. 독립 완료 리뷰

가능하면 구현에 참여하지 않은 서브에이전트나 reviewer에게 `SOURCE_PLAN.md`, `PLAN.md`, 구현과
증거를 주고 아래 다섯 축을 독립적으로 확인하게 한다. 사용할 수 없으면 같은 체크리스트로 구현
점검과 분리된 self-review를 수행한다. 리뷰 과정 설명은 문서에 복제하지 않고 최종 결함과 판정만
남긴다.

1. 원본 범위가 REQ·TEST·결과물 인벤토리에 모두 연결됐는가
2. 정상·빈 값·오류·권한·재실행 경계가 정확한가
3. 불필요한 복잡성·중복·의존성이 없는가
4. 비밀값·개인정보·권한·외부 변경이 안전한가
5. 증거가 완료 주장을 실제로 뒷받침하는가

발견 사항을 `P0`~`P3`로 기록한다. P0/P1이 하나라도 있으면 관련 REQ와 TEST를 TODO/FAIL로 다시
열고 구현 단계로 돌아가 자동 수정·재검증한다. P2/P3도 원본 범위 안에서 안전하게 고칠 수 있으면
해결한다. 제품 범위·비용·권한·삭제·외부 발송처럼 사람 결정이 필요한 항목만 영향과 선택지를
`아직 증명하지 못한 것` 또는 다음 버전에 남긴다.

## 5. 저장소와 릴리스 확인

```bash
gh repo view --json visibility,url --jq '"\(.visibility) \(.url)"'
git status --short
git log -5 --oneline
```

- 새 GitHub 저장소의 기본 visibility는 `PUBLIC`이어야 한다. 기획서에 비공개가 필요하거나 개인정보·비밀값 위험으로 `PRIVATE`를 선택했다면 사용자 확인과 이유가 `가정과 결정`에 있어야 한다. 기존 저장소는 확인한 visibility와 사용자 결정이 일치해야 한다.
- Sites 방문자 접근 범위는 GitHub visibility와 별도로 확인한다. 새 Site는 검토 중 제한된 접근을
  유지하고, 기획서에 확정된 대상과 안전 검토가 있을 때만 그 범위로 공개한다.
- 비밀값·실데이터·불필요한 빌드 산출물이 추적되지 않아야 한다.
- 코드·테스트·PLAN 상태가 서로 다른 커밋으로 어긋났으면 하나의 최종 정리 커밋으로 맞춘다.

## 6. 정직한 완료 판정

필수 REQ 수와 PASS 수, 원본·파생 TEST 수와 `TESTED` 수를 각각 센다.

`delivery_intent`가 `implement_and_release`면 로컬 구현·build만으로 완료하지 않는다. 웹앱은 실제
production URL, AI 스킬은 commit·push와 계획된 설치 대상의 새 컨텍스트 호출, 자동화는 승인된
live-run·트리거·결과 재조회가 있어야 한다. 사용자 권한이나 외부 장애가 남으면 한 동작을 요청하고
해결 뒤 같은 완료 게이트로 자동 재개한다.

- REQ와 TEST가 모두 PASS이고 P0/P1 없음: `PLAN.md`의 `최종 판정`을 한 번 갱신하고 `MEMORY.md`를
  생성해 최종 검증 marker 블록을 정확히 하나 기록한 뒤 완료
- 일부 `FAIL | NOT_RUN | PARTIAL | INFERRED`: 완료라 하지 말고 REQ `N/M 통과`, TEST `T/K`와 남은 ID를
  보여준 뒤 고칠 수 있는 항목은 질문 없이 계속 수정·재검증
- 사용자 권한·외부 서비스 상태만 남음: blocker와 사용자가 해야 할 정확한 한 동작을 제시

최종 보고에 `아직 증명하지 못한 것` 한 줄을 두고 `TESTED`가 아닌 항목, 미해결 P2/P3, 외부 권한
때문에 남은 live 검증을 적는다. 없으면 `없음`이라고 쓴다.

최종 판정에서 `PLAN.md`의 요구사항·TEST·인벤토리·결과를 한 번에 맞춘다. 완료 판정이라면 사용자
요청 여부와 관계없이 `memory-log.md` 형식으로 `MEMORY.md`를 생성하고 실제 최종 검증 결과를 기록한다.
시작 marker와 종료 marker가 각각 정확히 하나인지 세며, 기존 블록이 있으면 append하지 않고 같은
블록을 갱신한다. `PLAN.md`, `MEMORY.md`, 코드·테스트를 같은 최종 커밋에 담아 push한다. 최종
검증에서 바꾼 정확한 경로만 `git add --`로 stage하고 cached 목록을 확인한다.

```bash
git commit -m "검증: 원본 기획서 요구사항 완료"
git push
```

## 7. Orange Build App으로 결과 돌려보내기

`SOURCE_PLAN.md` 메타데이터의 `source`가 정확히 `orange-build-app`일 때만, 완료 뒤 아래 복귀
흐름을 제안한다. `PLAN.md`와 값이 다르면 원본을 기준으로 삼고 드리프트를 기록한다. 원래 앱 페이지
URL을 기획서에서 추측하지 않는다. 연결된 브라우저에 해당 페이지가 열려 있으면 그 탭을 사용하고,
없으면 사용자에게 원래 기획서 페이지를 열어 달라는 한 동작만 요청한다.

1. 사용자가 원하면 권한을 받은 뒤 브라우저에서 GitHub URL을 결과 링크 입력란에 채운다. 실제
   운영 배포 URL이 있는 결과물만 라이브 URL도 채우며, `ai_skill`·`automation`에 없는 URL을
   꾸며내지 않는다. 제출 전 계정·workspace와 입력할 URL을 사용자에게 보여준다.
2. 앱의 만들기 기록으로 `MEMORY.md`를 가져오려면 파일 전체가 앱에 업로드·저장될 수 있음을 먼저
   설명하고 **명시적 동의**를 받는다. 동의 전에는 파일 선택·업로드·개인정보 동의 체크를 대신하지
   않는다.
3. 참가자 회고는 사용자가 직접 쓴 한 문장 이상이어야 한다. 대신 꾸며내지 않고, 사용자가 제공한
   문장을 원하면 입력만 보조한다.

`source`가 `orange-build-app`이 아닌 모든 작업 또는 앱 복귀를 원하지 않는 경우 이 단계는
건너뛰며 완료 판정에 영향을 주지 않는다.

## 8. 최종 전달 형식

```text
✅ Orange Build 완료 — M/M 요구사항 PASS · T/K TEST TESTED
- 결과: [라이브 URL / 대표 스킬 호출 결과 / 자동화 run id]
- 저장: [GitHub URL · PUBLIC / 승인된 PRIVATE · 배포/활성화 상태]
- 검증: [핵심 검증 최대 3개]
- 기록: MEMORY.md 최종 검증 1건
- 아직 증명하지 못한 것: [없음 / TEST·REQ·P2/P3와 이유]
```

사용자가 바로 결과를 확인할 수 있는 링크나 호출 예를 먼저 준다. 과정 설명보다 결과와 검증을
앞세운다. AI 수정 목록, 후보 채택 수, 내부 명령, 다음 버전 목록은 사용자가 요청했거나 중요한
P0/P1·범위 변경이 있었을 때만 덧붙인다.
