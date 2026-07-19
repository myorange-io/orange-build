# orange-build 릴리스 규칙

버전을 올릴 때는 **반드시 아래 세 파일의 `version` 필드를 함께 수정**한다.

- `.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`
- `.codex-plugin/plugin.json`

버전이 어긋나면 Codex 또는 Claude 마켓플레이스가 옛 버전을 최신으로 인식해 사용자에게 업데이트가 노출되지 않는다. 커밋 전 `python3 scripts/validate_release.py`로 일치 여부를 확인할 것.

## 저장소 작업 규칙

- 플러그인·스킬을 바꾼 뒤 `python3 scripts/validate_release.py`와 `git diff --check`를 실행한다.
- 변경한 정확한 경로만 `git add -- <path...>`로 stage한다. `git add .`과 `git add -A`는 사용하지 않는다.
- 큰 실행 절차는 이 파일에 복제하지 않고 해당 `SKILL.md`와 `references/`에 둔다.
