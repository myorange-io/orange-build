---
name: orange-secure
description: 오렌지 빌드로 만든 Next.js + Supabase 앱의 흔한 보안 구멍을 선택한 local·shared·real_work 완료 수준에 맞춰 점검하고 고친다. 배포·공유 전이나 Supabase 보안 경고 메일을 받았을 때 사용. "보안 점검", "오렌지 보안", "Supabase 경고", "RLS 확인" 같은 요청에 사용.
---

# Orange Build — Secure

오렌지 빌드로 만든 앱의 **흔한 보안 구멍 6가지**를 빠르게 점검·수정한다. 입문자가 공유 가능한
URL을 받았을 때 대표적인 키·권한·민감정보 위험이 없는지 확인하는 단계다.

가벼운 검사 — 토큰을 거의 쓰지 않는다. 매 턴 자동 리뷰가 아니라, 사용자가 부를 때만 1회 돈다.

## 1. 사전 점검

현재 폴더가 오렌지 빌드 프로젝트가 맞는지 본다:

- `PLAN.md`·`package.json` 없음 → "오렌지 빌드 프로젝트가 아닌 것 같아요. 프로젝트 폴더에서
  실행하세요." 라고 안내하고 끝낸다.
- Supabase 사용 여부는 특정 클라이언트 파일 하나로 판단하지 않는다. `supabase/config.toml`,
  `supabase/migrations/`, Supabase SDK import, 관련 환경변수를 함께 본다.
- service-role 사용 흔적이 없으면 4번은 건너뛸 수 있다. Supabase 사용 흔적이 전혀 없을 때만
  5번(RLS)을 건너뛴다.

## 2. 6가지 점검 항목

각 항목을 순서대로 본다. **하나씩 결과를 출력하고**, 위험이 있으면 사용자에게 보여준 뒤 "고칠까요?"
한 번만 묻고 진행한다.

### 검사 1 — `.env.local`이 git에 커밋됐는지

```bash
git ls-files | grep -E '^\.env(\.|$)' || echo "OK"
```

`.env.local`·`.env`가 출력되면 **CRITICAL**. 키가 이미 git 히스토리에 들어갔다.

**고치는 법** (사용자가 OK 하면):
1. `git rm --cached .env.local .env 2>/dev/null` 로 추적에서 제외
2. `.gitignore`에 `.env*.local`·`.env` 추가 (이미 있는지 확인)
3. **사용자에게 알린다**: "이미 push 한 적이 있다면 GitHub 히스토리에 키가 남아 있어요.
   Supabase 대시보드 → Settings → API → 'Reset anon key'와 'Reset service_role key'로 키를
   새로 발급하고 `.env.local`·Vercel env에 새 키를 넣으세요. LLM API 키도 마찬가지로 재발급."

### 검사 2 — `NEXT_PUBLIC_*`에 서버 전용 키가 섞였는지

```bash
grep -E '^NEXT_PUBLIC_.*(SERVICE_ROLE|SECRET|PRIVATE)' .env.local .env 2>/dev/null || echo "OK"
```

`NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY`·`NEXT_PUBLIC_ANTHROPIC_API_KEY` 같은 게 잡히면 **CRITICAL**.
`NEXT_PUBLIC_` 접두사는 브라우저 번들에 들어간다 — service_role 키가 노출되면 RLS가 무력화된다.

**고치는 법**:
1. 해당 변수에서 `NEXT_PUBLIC_` 제거 (예: `SUPABASE_SERVICE_ROLE_KEY=...`)
2. 코드에서 이 변수를 쓰는 곳을 grep으로 찾는다:
   ```bash
   grep -rn "NEXT_PUBLIC_SUPABASE_SERVICE_ROLE\|NEXT_PUBLIC_ANTHROPIC\|NEXT_PUBLIC_OPENAI" app/ components/ lib/ 2>/dev/null
   ```
3. 클라이언트 컴포넌트(`'use client'` 있거나 `components/`)에서 쓰고 있으면 **그 호출을 서버
   라우트(`app/api/<이름>/route.ts`)로 옮긴다**.
   `../orange-start/references/phase-build.md`의 비밀값·외부 연동 원칙을 따른다.
4. Vercel env(`vercel env ls`)에도 같은 변수가 있으면 사용자에게 대시보드에서 접두사를 고치도록 안내.
5. 키가 한 번이라도 배포·노출됐다면 **반드시 재발급**.

### 검사 3 — 클라이언트 코드에 비밀 키가 하드코딩됐는지

```bash
grep -rE 'sk_live_|sk-ant-|sk-proj-|service_role|eyJ[A-Za-z0-9_-]{20,}' app/ components/ lib/ 2>/dev/null | grep -v 'process.env' || echo "OK"
```

매치가 나오면 사용자에게 보여준다. JWT(`eyJ...`)나 `sk_live_`·`sk-ant-` 같은 키 패턴이 코드에
직접 박혀 있으면 **CRITICAL**. 빌드 결과물에 그대로 들어간다.

**고치는 법**:
1. 해당 값을 `.env.local`로 옮기고 `process.env.<NAME>`으로 참조
2. 노출된 키는 **재발급** (검사 1과 같은 절차)

### 검사 4 — service_role 키가 클라이언트 컴포넌트에서 쓰이는지

`lib/supabase.ts`가 있으면 그 내용을 본다. `createClient`에 `SERVICE_ROLE`이 들어가 있으면서
파일 상단에 `'use client'`가 없어도, `app/` 하위 클라이언트 컴포넌트(`'use client'` 선언 + 이 모듈
import)에서 쓰이고 있는지 확인:

```bash
grep -rln "from.*lib/supabase" app/ components/ 2>/dev/null | xargs grep -l "'use client'" 2>/dev/null || echo "OK"
```

클라이언트 컴포넌트에서 import 하고 있고 그 모듈이 service_role을 쓴다면 **CRITICAL**. 클라이언트용
Supabase 클라이언트(`lib/supabase.ts` — anon 키)와 서버용(`lib/supabase-admin.ts` — service_role)을
분리한다.

**고치는 법**: `lib/supabase-admin.ts`를 새로 만들고 service_role 클라이언트는 거기에 둔다. 서버
라우트에서만 import 한다. 클라이언트에는 anon/publishable 키만 둔다.

### 검사 5 — Supabase 테이블에 RLS가 켜져 있는지

`supabase/` 아래의 모든 마이그레이션·SQL 파일을 재귀적으로 본다:

```bash
find supabase -type f -name '*.sql' -print 2>/dev/null
```

각 SQL 파일에서 `create table public.<이름>` 다음에 `alter table public.<이름> enable row level security`가
있는지 확인. 빠진 테이블이 있으면 **CRITICAL** (Supabase가 보낸 경고 메일의 원인).
SQL 파일이 없지만 Supabase 사용 흔적이 있으면 `OK`가 아니라 **확인 불가**다. 연결된 프로젝트의
실제 테이블 설정을 CLI나 대시보드에서 확인한다.

**고치는 법**:
1. 빠진 테이블마다 SQL 파일에 다음을 추가:
   ```sql
   alter table public.<테이블> enable row level security;
   ```
2. `PLAN.md`의 로그인·역할 완료 조건에 따라 최소 정책을 추가한다. 공개 익명 입력과 비공개
   관리자 조회를 혼동하지 말고, 정책을 만들기 어렵다는 이유로 RLS를 끄지 않는다.
3. 새 SQL을 Supabase에 적용:
   ```bash
   supabase db query --linked --file supabase/<파일>.sql
   ```
4. **이미 RLS 없이 배포된 상태라면 라이브 DB에도 같은 SQL을 적용해야 한다** — Supabase 대시보드
   SQL Editor에 붙여넣고 실행.

### 검사 6 — 법상 암호화 의무 대상이 평문으로 저장되는지

개인정보보호법은 **비밀번호 · 신용카드/계좌번호 · 주민등록번호 등 고유식별정보 · 바이오정보**를
암호화해 저장하도록 정한다(안전성 확보조치 기준 고시 제7조). 이게 평문으로 들어가 있는지 본다.

`supabase/` 폴더의 SQL에서 의무 대상으로 보이는 컬럼명을 찾되, 이미 암호화/해시된 표식
(`_enc`·`_hash`)이 붙은 건 제외한다:

```bash
find supabase -type f -name '*.sql' -exec grep -niE \
  'resident|jumin|주민|ssn|rrn|passport|여권|license|면허|card|카드|account|계좌|bank|biometric|fingerprint|지문|생체|password|passwd|비밀번호' {} + 2>/dev/null \
  | grep -viE '_enc|_hash|password_hash' || echo "NO_NAME_MATCH"
```

매치가 나오면 사용자에게 보여준다. 평문(`text`)으로 그대로 저장되고 있으면 **CRITICAL**(법 위반
소지). 코드에서 그 필드를 암호화 없이 insert 하는지도 같이 본다:

```bash
grep -rniE 'resident|주민|card|카드|account|계좌|password|비밀번호' app/ lib/ 2>/dev/null \
  | grep -viE 'encrypt|hash|crypto|auth' || echo "OK"
```

> **한계**: 이건 컬럼·변수 **이름 기반 휴리스틱**이라 완벽하지 않다 — 이름이 다르면 놓칠 수 있다.
> 사용자에게 "이름으로 추정한 것이라, 민감정보를 직접 저장한다면 꼭 확인하라"고 알린다.

**고치는 법** (사용자가 OK 하면) — `../orange-start/references/sensitive-data.md`를 따른다:
1. **먼저 "안 받기"를 검토**한다 — 비밀번호는 **Supabase Auth**, 카드·계좌는 **결제 대행 토큰**,
   본인확인용 주민번호는 **PASS/본인확인기관**으로 대체할 수 있는지. 대체가 가장 안전하다.
2. 그래도 저장이 필요하면: 비밀번호는 **일방향 해시**, 그 외는 **AES 양방향 암호화**(`lib/crypto.ts`).
   컬럼명에 `_enc` 접미사를 붙이고, 암복호화는 **서버 라우트에서만**, `ENCRYPTION_KEY`는 서버 전용
   (`NEXT_PUBLIC_` 금지)으로 둔다.
3. **이미 평문으로 배포·저장된 데이터가 있다면**, 기존 행을 암호화로 마이그레이션해야 한다 —
   라이브 DB의 평문은 그대로 두면 위험이 남는다고 사용자에게 분명히 알린다.

## 3. 최종 보고

6가지 검사를 다 끝낸 뒤 한 줄 요약을 출력한다:

- 전부 OK: `✅ 6개 휴리스틱에서 문제를 찾지 못했습니다 — 실제 권한·데이터 설정도 최종 확인하세요.`
- 수정함: `✅ 보안 문제 N건을 수정했습니다. 선택한 완료 수준의 로컬 결과 또는 라이브 URL을 다시 확인해 보세요.`
- 사용자가 수정을 거부함: `⚠️  CRITICAL N건이 남아 있습니다. 공유 전에 꼭 고치세요.`

보안 수정을 구현하고 최종 검증까지 마쳤다면 `../orange-start/references/memory-log.md`의 기존 최종
검증 marker 블록을 현재 결과로 한 번 갱신한다. 블록이 없는 기존 프로젝트면 하나를 만들고, 새
`최종 검증` 항목을 append해 중복시키지 않는다. 사용자가 과정 기록을 요청했고 실제 취약점 수정이나
수용한 잔여 위험이 다음 판단에 필요할 때만 별도 `보안 점검` 항목을 한 개 덧붙인다. 기록할 때는
점검한 항목 / 결과 / 수정한 것과 **어떻게 고쳤는지** / 남은 위험과 **그렇게 판단한 근거**를 구체적으로
적는다. 날짜는 `date +%Y-%m-%d`로 얻는다. 예:

```markdown
### [YYYY-MM-DD] 보안 점검
- **점검 항목**: .env git 커밋 여부 · NEXT_PUBLIC 키 노출 · 하드코딩 비밀 키 ·
  service_role 클라이언트 사용 · RLS 활성화 · 민감정보 평문 저장(법상 암호화 의무 대상)
- **결과**: CRITICAL 1건 발견·수정. `.env.local`이 git에 커밋돼 있었다 →
  `git rm --cached .env.local` 후 `.gitignore`에 `.env*` 추가, 커밋.
- **남은 위험**: 한 번 커밋돼 노출됐던 anon 키는 git 히스토리에 남아 있다 →
  Supabase 대시보드에서 키 재발급이 안전하다고 사용자에게 안내함.
- **배운 것**: anon 키는 공개돼도 RLS가 막아 주지만, 히스토리에 남는 건 별개 문제다.
```

수정 사항이 있었으면 이번 보안 수정 파일과 최종 검증 marker를 갱신한 `MEMORY.md`의 정확한 경로만 stage하고 cached 목록을
확인한 뒤 커밋한다:
```bash
git commit -m "보안: 점검 결과 반영" && git push
```

## 원칙

- **한 번에 한 검사**, 결과를 보여주고 사용자가 OK 한 뒤 다음으로. 자동으로 6건을 한꺼번에 고치지
  않는다 — 입문자는 무엇이 바뀌었는지 알아야 한다.
- **재발급이 필요한 상황은 명확히 말한다.** 키가 git이나 브라우저에 한 번이라도 노출됐다면 코드만
  고치는 건 충분하지 않다.
- **공식 보안 도구를 대체하지 않는다.** 더 깊은 검사가 필요하면 현재 호스트의 공식 보안 검사나
  CI secret scanner를 함께 사용하도록 안내한다.
