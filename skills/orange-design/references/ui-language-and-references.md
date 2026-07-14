# UI 이름·참고자료·시각 반복

목표: 모호한 사용자 표현을 정확한 UI 이름·동작·접근성 의미로 번역하고, 화면 참고자료를 작은 디자인
변경의 근거로 쓴다. 기능 범위를 다시 기획하지 않는다.

## Name That UI로 일상어 번역

[Name That UI](https://namethatui.com/)를 시각 사전으로 사용한다. 모양보다 trigger, placement,
blocking, dismissal, selection behavior가 맞는 항목을 고른다.

```text
사용자 표현 → canonical UI 이름 → 핵심 동작 → semantic/accessibility primitive → 검증 상태
```

| 사용자 표현 | canonical UI 이름 | 구분할 핵심 |
|---|---|---|
| 팝업 뒤의 어두운 반투명 층 | scrim / backdrop | modal과 분리되고 뒤 상호작용을 막는가 |
| 저장 뒤 잠깐 뜨는 알림 | toast / snackbar | non-blocking status이며 자동 사라지는가 |
| 버튼 옆 설명·메뉴 | tooltip / popover / dropdown menu | 설명, rich content, action list 중 무엇인가 |
| 내용 자리 모양 로딩 | skeleton | 예측 가능한 레이아웃과 `aria-busy`가 있는가 |
| 검색하며 후보 선택 | combobox / autocomplete | 입력과 filtered list selection이 연결되는가 |
| 항목 없음 안내 | empty state | 이유와 1순위 행동이 보이는가 |

사이트에 항목이 없거나 접속할 수 없으면 표준 플랫폼 용어를 근거와 함께 `INFERRED`로 기록하고,
실제 동작·접근성 검증으로 보완한다. 사이트를 대량 scrape하거나 외부 이미지를 자동 저장하지 않는다.

## 참고자료를 명세로 바꾸기

참고 화면·스크린샷·사이트·Stitch 결과는 그대로 복제하지 않고 다음으로 분해한다.

1. `GOAL` — 화면의 한 가지 목적과 1순위 행동
2. `UI INVENTORY` — PLAN에 이미 있는 제목·입력·버튼·상태·경로
3. `LAYOUT` / `HIERARCHY` — 폭·정렬·반응형 순서와 정보 우선순위
4. `TYPE` / `COLOR / MATERIAL` — 관계와 역할, 과도하지 않은 재료감
5. `CANONICAL COMPONENTS` — 위 표의 UI 이름과 interaction
6. `CONSTRAINTS` / `NEGATIVE CONSTRAINTS` — 유지할 기능과 추가하면 안 되는 것

## variants가 reroll보다 먼저

기능과 UI inventory를 잠근 뒤 한 후보에서 1~2개 변수만 바꾼다. before/after를 같은 viewport·데이터·
상태에서 캡처하고, 시각 기준과 기존 functional test가 모두 통과한 후보만 채택한다. 더 낫다는 증거가
없거나 기능·접근성이 회귀하면 이전 기준선으로 돌아간다.

## functional QA와 visual QA 분리

- functional: 입력, click, keyboard, focus, validation, 저장·재조회, 권한, 오류 복구
- visual: desktop/mobile fit, hierarchy, overflow, loading·empty·error·success, dialog, 긴 텍스트,
  focus ring

한 장의 예쁜 첫 화면만 보지 않는다. 주요 상호작용 뒤 상태와 모바일을 production URL에서 확인하고,
console·network 오류도 함께 본다.

## 참고한 방법

- [MengTo/Skills](https://github.com/MengTo/Skills) — specs beat vibes, screenshots as evidence,
  design-system prompt, 한 번에 1~2개 변수 반복, functional/visual QA 분리
- [Name That UI](https://namethatui.com/) — 일상어에서 표준 UI 이름·동작·접근성 primitive로 번역
