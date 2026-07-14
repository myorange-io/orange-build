# Stitch 시각 보정 — Orange Design에서만 선택적으로

목표: 이미 최종 검증을 마친 웹앱의 **시각 방향만** 짧게 보정한다. Stitch는 기능·페이지·데이터를
다시 기획하는 도구가 아니며, 기본 `orange-start` 구현 흐름에서는 사용하지 않는다.

## 적용 조건

- 사용자가 Stitch 사용 또는 가져온 Stitch 시안을 명시적으로 요청했다.
- production URL과 최종 검증 증거가 있다.
- 대표 화면 1개, 수정 요청 1회, 10분이 기본 상한이다. 서로 다른 화면 유형이 꼭 필요해도 3개를
  넘기지 않는다.

## 고정 목록과 프롬프트

`PLAN.md`와 라이브 화면에서 반드시 남아야 하는 제목·입력·버튼·표·상태·핵심 행동·경로를 고정한다.
`ui-language-and-references.md`를 읽어 UI 이름과 interaction을 정확히 기록한다.

```text
Visual redesign only. Do not add or remove screens, fields, actions, data,
navigation, or features. Preserve the exact UI inventory and Korean labels below.
Focus only on hierarchy, spacing, typography, color, and responsive layout.
```

이어 대표 화면의 실제 UI 목록, `DESIGN.md`의 적용 토큰, 원하는 밀도·배경·강조색을 넣는다. `modern`,
`clean` 같은 형용사만으로 요청하지 않는다. Stitch가 새 기능·문구·페이지를 제안하면 무시한다.

## 계정과 가져오기

Stitch를 열기 전 `../../orange-start/references/browser-steps.md`의 다계정 확인 게이트를 따른다.
여러 Google 계정 중 선택, 로그인, 2FA, CAPTCHA, 약관 동의는 사용자가 직접 한다. 에이전트는
프롬프트·고정 목록·가져온 결과의 비교를 돕는다.

스크린샷만 있어도 tokens와 hierarchy를 참고할 수 있다. HTML zip이 있더라도 하드코딩된 마크업 전체를
복사하지 않는다. 기존 컴포넌트와 디자인 토큰으로 색상·type·spacing·layout만 반영한다.

같은 viewport·데이터·상태에서 before/after와 functional regression을 비교한다. spacing, type,
accent, arrangement 중 1~2개 변수만 바꾸고, 더 낫다는 관찰이 없으면 기존 디자인으로 되돌린다.
