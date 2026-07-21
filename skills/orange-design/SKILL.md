---
name: orange-design
description: 구현과 최종 검증을 마친 웹앱의 디자인이 기대와 다를 때, 기능·페이지·데이터·요구사항을 보존하면서 디자인 시스템과 화면의 위계·간격·타이포그래피·색상·반응형 품질을 개선한다. 프로젝트 성격에 맞는 getdesign.md 사례를 링크와 함께 추천하고, "디자인을 다듬어줘", "화면이 마음에 안 들어", "어울리는 디자인을 추천해줘", "Stitch로 시안 보정", "조직 홈페이지 디자인을 반영해" 같은 요청에 사용한다.
---

# Orange Design

이미 작동하고 최종 검증까지 마친 `web_app`의 디자인을 안전하게 개선한다. 기능 구현이나 범위
재협상이 아니라, 현재 사용자 흐름과 `PLAN.md`의 REQ·TEST를 고정한 뒤 디자인 시스템을 만들고
작은 후보를 증거로 비교하는 후속 단계다.

## 시작 조건과 경계

- `PLAN.md`의 모든 필수 REQ와 TEST가 `PASS`이고 `phase-verify.md`의 최종 검증이 끝난 `web_app`에만
  적용한다. 구현·검증이 덜 끝났다면 먼저 `orange-start` 또는 `orange-resume`으로 돌려보낸다.
- 사용자에게 무엇이 마음에 들지 않는지 한 문장으로 받고, 라이브 URL·대표 화면·target viewport를
  확인한다. 이미 명확한 불만이 있으면 취향 질문을 반복하지 않는다.
- 기능·페이지·경로·데이터 모델·권한·문구의 의미·REQ·TEST는 고정이다. 디자인 개선 중 기능 누락을
  발견하면 디자인으로 덮지 말고 `PLAN.md`의 결함으로 기록해 구현 흐름으로 돌린다.
- 한 번에 spacing, type scale, color, hierarchy, component treatment, responsive layout 중 1~2개
  변수만 바꾼다. 기존보다 낫다는 관찰과 기능 회귀가 없을 때만 채택한다.
- 외부 사이트·Stitch·getdesign.md는 디자인 근거이지 구현 범위를 정하는 명세가 아니다. 외부 코드,
  이미지, 상표 자산을 복사하거나 로그인·접근 제한을 우회하지 않는다.

## 실행 순서

1. `PLAN.md`, `SOURCE_PLAN.md`, 마지막 검증 증거, production URL, 현재 컴포넌트·토큰을 읽어
   **고정 UI inventory**를 만든다. 반드시 남아야 하는 경로·제목·입력·버튼·상태·핵심 행동을 목록화한다.
2. 프로젝트 루트의 `DESIGN.md`를 먼저 찾는다. 있으면 그것을 우선 디자인 시스템으로 사용한다.
3. 없고 사용자가 조직 홈페이지 URL을 확인해 주면 `references/design-system-extraction.md`를 읽는다.
   공개 페이지에서 관찰한 원칙만으로 `DESIGN.md` 초안을 만들고, 저장 전 범위와 diff를 사용자에게
   보여준다. URL을 추측하거나 조직의 브랜드를 독단적으로 재정의하지 않는다.
4. 조직 디자인 시스템이 없거나 다른 방향을 비교해야 하면 `references/getdesign.md`와
   `references/design-recommendations.md`를 읽는다. 프로젝트 성격에 맞는 getdesign.md 사례를 최대
   두 개 제안하고, 사용자가 링크에서 화면을 본 뒤 고르기 전에는 디자인 방향을 구현하지 않는다.
5. `references/ui-language-and-references.md`로 모호한 UI 표현을 canonical component와
   accessibility 행동으로 번역하고 visual acceptance check를 관찰 문장으로 만든다.
6. 사용자가 Stitch를 명시적으로 원하거나 시안을 이미 가져온 경우에만
   `references/stitch-design.md`를 읽는다. 이 스킬 밖의 기본 구현 흐름에서는 Stitch를 열지 않는다.
7. 기존 컴포넌트와 디자인 토큰으로 후보를 구현한다. production build·관련 테스트·라이브 URL의
   functional/visual QA를 모두 통과한 후보만 채택해 재배포한다.

## 디자인 시스템 우선순위

1. 프로젝트에 이미 있는 승인된 `DESIGN.md`
2. 사용자가 확인하고 추출에 동의한 조직 홈페이지의 공개 디자인 원칙
3. 사용자가 제공한 브랜드 가이드·참고 화면
4. getdesign.md의 분석 카탈로그에서 얻은 비브랜드 일반 원칙
5. 현재 제품의 검증된 기본 스타일

상위 근거와 하위 근거가 충돌하면 상위를 따른다. 여러 방향이 모두 타당하고 브랜드 방향이 크게
달라질 때만 최대 두 개의 대표 후보와 차이를 보여 사람의 선택을 받는다.

## getdesign.md 추천안 제시

`references/design-recommendations.md`를 따른다. 추천안은 최소한 아래를 포함한다.

- 프로젝트와 맞는 이유 및 적용할 화면·컴포넌트
- getdesign.md의 **분석 화면 링크**와 확인 가능한 경우 원본 서비스의 **공식 화면 링크**
- 그대로 복제하지 않고 가져올 일반 원칙과 적용하지 않을 브랜드 고유 요소
- 기능·데이터·문구·경로를 변경하지 않는다는 고정 조건

사용자가 어느 링크도 고르지 않으면 현재 디자인 시스템을 유지한다. 카탈로그·원본 링크에 접근할 수
없거나 실제 화면을 확인하지 못했으면 특정 사례를 추천하는 척하지 않고, 검색 링크 또는 사용자가
제공한 참고 화면으로 전환한다.

## 구현과 검증

- 하드코딩한 시안 HTML 전체를 붙여넣지 않는다. 기존 layout·semantic HTML·컴포넌트 구조를 유지하며
  CSS variables, theme tokens, typography scale, spacing, responsive rules로 반영한다.
- 같은 production URL, viewport, 데이터, 로그인 상태에서 before/after를 비교한다. desktop·mobile,
  loading·empty·error·success, dialog·focus 상태와 긴 텍스트를 함께 본다.
- 입력→처리→결과, keyboard·focus·dismissal, console·network 오류, 기존 테스트를 다시 확인한다.
  기능 회귀·접근성 후퇴·`PARTIAL` 증거면 변경을 되돌린다.
- 채택한 모든 시각 수정마다 `MEMORY.md`를 바꾸지 않는다. 디자인 개선 전체를 실제 URL에서 최종
  검증한 뒤 `../orange-start/references/memory-log.md`의 기존 최종 검증 marker 블록을 한 번 갱신한다.
  블록이 없는 기존 프로젝트면 하나를 만들되 두 번째 최종 검증 항목을 append하지 않는다. 별도 디자인
  과정 항목은 사용자가 과정 기록 유지를 요청한 경우에만 남긴다.
  `DESIGN.md`를 새로 저장했다면 출처 URL·관찰일·적용 범위를 명시하고 비밀값·개인 계정 정보는 넣지
  않는다.

## 완료 보고

```text
✅ 디자인 개선 완료 — [production URL]
변경: [위계/간격/타이포그래피 등]
보존: [고정한 핵심 흐름과 기능]
검증: [build·test·라이브 functional/visual QA]
디자인 시스템: [기존 DESIGN.md / 조직 홈페이지 초안 / 선택한 getdesign.md 참고]
```
