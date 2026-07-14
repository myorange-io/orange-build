# 조직 홈페이지에서 DESIGN.md 초안 만들기

목표: 조직 홈페이지가 이미 가진 시각 언어를 공개적으로 관찰해, 프로젝트의 화면을 일관되게 만들 수
있는 **검토 가능한** `DESIGN.md` 초안으로 정리한다. 홈페이지를 복제하거나 조직의 브랜드 전략을
새로 결정하지 않는다.

## 실행 전 확인

- 프로젝트에 승인된 `DESIGN.md`가 있으면 새로 추출하지 않고 그 파일을 우선한다.
- 조직 홈페이지 URL은 사용자가 제공하거나 화면에서 명시적으로 확인한 값만 사용한다. 검색 결과나
  비슷한 이름의 사이트로 추측하지 않는다.
- 공개적으로 볼 수 있는 페이지와 사용자가 접근 권한을 가진 화면만 관찰한다. 로그인·paywall·robots
  제한·접근 제어를 우회하지 않으며, 개인정보·대시보드·고객 데이터는 수집하지 않는다.
- 추출·저장 전 다음을 한 번 확인한다: "[URL]의 공개 시각 원칙을 분석해 이 프로젝트 루트에
  `DESIGN.md` 초안을 저장해도 될까요? 코드·이미지·상표 자산은 복사하지 않습니다."

## 관찰과 기록

대표적인 공개 페이지 1~3개만 보고 아래 항목을 **관찰 사실**과 **프로젝트 적용 제안**으로 나눈다.

1. 목적·톤 — 신뢰감, 정보 밀도, 친근함처럼 화면에서 확인 가능한 방향
2. color — 배경·표면·본문·보조 글자·accent·border의 역할과 대비
3. type — 서체 계열, 제목/본문 규모 관계, 굵기, 행간, 숫자/라벨 사용
4. layout — 최대 폭, grid, 여백, section rhythm, mobile에서의 우선순위 변화
5. components — button, input, card, table, navigation, dialog, feedback 상태
6. motion/material — 필요한 경우에만 전환 속도·radius·border·shadow의 강도
7. accessibility — keyboard focus, text contrast, reduced motion, touch target

브랜드 자산·카피·화면 구성·코드를 복사하지 않는다. 관찰으로 확인할 수 없는 색상 값, 폰트 파일,
반응형 규칙은 추측하지 않고 `확인 필요`로 남긴다.

## DESIGN.md 초안 형식

```md
# [조직/프로젝트] Design System

## Source
- Homepage: [확인된 URL]
- Observed: [YYYY-MM-DD]
- Scope: public pages [경로 또는 페이지 이름]
- Status: draft — user review required

## Design principles
- [관찰한 원칙 → 프로젝트 적용 방식]

## Tokens
| Role | Value or relationship | Evidence | Project use |
|---|---|---|---|
| surface | ... | ... | ... |

## Typography and layout
- ...

## Components and interaction
- [canonical component] — [appearance + keyboard/focus/dismissal rule]

## Constraints
- Preserve PLAN.md UI inventory and all functional states.
- Do not copy external code, images, logos, or brand copy.
```

저장 전 `git diff -- DESIGN.md`를 보여주고, 사용자의 기존 `DESIGN.md`는 덮어쓰지 않는다. 승인되지 않은
초안은 `DESIGN.md`로 가장하지 말고 대화에서 제안만 한다.
