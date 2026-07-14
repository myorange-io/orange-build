# UI 이름·참고자료·시각 반복

목표: 사용자가 “뒤에 깔리는 어두운 것”, “잠깐 뜨는 알림”처럼 설명해도 정확한 UI 이름·동작·
접근성 의미로 번역하고, 막연한 분위기 대신 화면 근거와 작은 변경으로 웹앱을 다듬는다. 이 단계는
기능 범위를 다시 기획하거나 Stitch를 의무화하지 않는다.

## 1. 언제 읽을지

`web_app`에서 다음 중 하나일 때만 적용한다.

- 사용자가 UI 요소를 일상어로 설명해 구현 대상이 모호함
- modal·drawer·popover처럼 비슷한 패턴 중 동작 차이가 중요함
- 참고 화면·스크린샷·사이트·Stitch 결과를 구현에 반영함
- “디자인을 더 좋게” 같은 요청을 관찰 가능한 수정으로 바꿔야 함
- 기능 검증 뒤 별도의 visual QA를 수행함

UI 이름과 시각 방향이 이미 명확하면 이 단계를 보고하거나 질문하지 않는다.

## 2. Name That UI로 일상어 번역

[Name That UI](https://namethatui.com/)는 디자인 갤러리가 아니라 **UI 시각 사전**으로 사용한다.
현재 브라우저·web 도구가 있으면 사용자의 표현을 그대로 검색하고, 모양보다 trigger·placement·
blocking·dismissal·selection behavior가 맞는 항목을 고른다. 계정이나 설치는 필요 없다.

다음 형식으로 구현 언어를 고정한다.

```text
사용자 표현 → canonical UI 이름 → 핵심 동작 → semantic/accessibility primitive → 검증 상태
```

대표 번역:

| 사용자 표현 | canonical 이름 | 구분할 핵심 |
|---|---|---|
| 팝업 뒤의 어두운 반투명 층 | scrim / backdrop | modal 표면과 배경을 분리하며 뒤 상호작용을 막는가 |
| 저장 뒤 잠깐 뜨는 알림 | toast / snackbar | non-blocking status이며 자동 사라지는가 |
| 버튼 옆에 붙는 작은 설명·메뉴 | tooltip / popover / dropdown menu | hover 설명인지, rich content인지, action list인지 |
| 내용 자리 모양으로 먼저 뜨는 로딩 | skeleton | 레이아웃이 예측 가능하고 `aria-busy` 상태인가 |
| 검색하며 후보를 고르는 입력 | combobox / autocomplete | 입력과 filtered list selection이 연결되는가 |
| 항목이 없을 때 안내와 다음 행동 | empty state | 비어 있음의 이유와 1순위 행동이 보이는가 |
| 세 점 버튼 | overflow menu | 숨겨진 부가 action을 여는가 |
| 켬/끔 또는 여러 선택 | switch / checkbox / radio | 즉시 설정, 독립 선택, 단일 그룹 선택 중 무엇인가 |

사이트에 정확한 항목이 없거나 접속할 수 없으면 구현을 막지 않는다. 표준 플랫폼 용어를 근거와 함께
`INFERRED`로 기록하고 실제 동작·접근성 검증으로 보완한다. 사이트를 대량 scrape하거나 외부 이미지를
자동으로 저장소에 복사하지 않는다.

이 이름은 구현·테스트·프롬프트에 같은 단어로 쓴다. 예를 들어 `팝업`이라고 뭉뚱그리지 않고
`modal dialog + scrim`, `popover`, `toast` 중 하나를 정해 focus 이동, Escape, outside click,
background blocking 같은 acceptance check를 만든다.

## 3. 참고자료를 명세로 바꾸기

참고 화면은 그대로 복제하지 않고 증거로 분해한다. 사용자가 준 이미지·URL·Stitch 결과에서 다음을
추출한다.

1. `GOAL` — 이 화면의 한 가지 목적과 1순위 행동
2. `UI INVENTORY` — PLAN에 이미 있는 제목·입력·버튼·상태·경로
3. `LAYOUT` — grid, 영역 순서, 폭, 정렬, responsive 변화
4. `HIERARCHY` — H1→support→primary action→secondary information
5. `TYPE` — 크기·굵기·행간·밀도 관계
6. `COLOR / MATERIAL` — 배경·텍스트·강조색 하나·border·shadow
7. `CANONICAL COMPONENTS` — 2절에서 고정한 UI 이름과 동작
8. `CONSTRAINTS` — 반드시 유지할 기능·문구·데이터·접근성
9. `NEGATIVE CONSTRAINTS` — 추가하면 안 되는 기능·장식·문구·패턴

외부 참고 이미지는 라이선스와 저장 허용 여부가 불명확하면 분석용으로만 보고 commit하지 않는다.
대신 출처 URL과 추출한 토큰·구조·원칙만 `PLAN.md` 또는 `MEMORY.md`에 남긴다. 참고자료가 요구사항보다
우선하지 않으며, 참고 화면에 빠진 페이지·상태도 원본 범위에서 삭제하지 않는다.

## 4. variants가 reroll보다 먼저

전체 화면을 매번 재생성하지 않는다. 기능과 UI inventory를 잠근 뒤 한 후보에서 변수 1~2개만
바꾼다.

- 먼저 layout·hierarchy·copy를 고정한다.
- 다음 후보는 spacing, type scale, accent, card arrangement, image crop 중 1~2개만 바꾼다.
- 각 후보의 before/after를 같은 viewport·같은 데이터·같은 상태에서 캡처한다.
- `self-improvement-loop.md`의 후보 채택 게이트로 원본 기능 보존, visual acceptance check, 기존
  functional test를 비교한다.
- 더 낫다는 증거가 없거나 기능·접근성이 회귀하면 후보를 버리고 이전 기준선으로 돌아간다.

사용자가 시각 취향을 이미 정했으면 묻지 않는다. 서로 타당한 방향이 여러 개이고 결과가 크게 달라질
때만 대표 후보 2개와 차이를 보여주고 선택받는다.

## 5. functional QA와 visual QA 분리

코드가 작동하는 것과 화면이 좋은 것은 별도로 확인한다. 구현 전 `PLAN.md`의 REQ·실제 컨트롤·최종
보고에서 주장할 사용자 결과를 합쳐 작은 QA inventory를 만든다.

- functional: 입력, click, keyboard, focus, validation, 저장·재조회, 권한, 오류 복구
- visual: desktop/mobile viewport fit, hierarchy, overflow, loading·empty·error·success, dialog가 열린
  상태, 긴 텍스트·대표 데이터, focus ring

한 장의 예쁜 첫 화면만 보지 않는다. 주요 상호작용 뒤 상태와 모바일을 같은 production URL에서
확인하고, console·network 오류도 함께 본다. 시각적으로 중요한 주관 기준은 `primary CTA가 다른
행동보다 가장 먼저 보인다`처럼 관찰 문장으로 바꾼다.

## 참고한 방법

- [MengTo/Skills](https://github.com/MengTo/Skills) — specs beat vibes, screenshots as evidence,
  design-system prompt, 한 번에 1~2개 변수 반복, functional/visual QA 분리
- [Name That UI](https://namethatui.com/) — 일상어에서 표준 UI 이름·동작·접근성 primitive로 번역

외부 스킬 파일이나 스타일 코드를 복사하지 않는다. Orange Build의 기존 UI 바닥선과 선택적 Stitch
순서를 유지하면서 명세·용어·검증 패턴만 적용한다.
