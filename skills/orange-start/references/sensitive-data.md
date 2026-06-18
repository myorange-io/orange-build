# 민감정보 저장 — 최소화 먼저, 어쩔 수 없으면 암호화

개인정보보호법은 아래 4종을 **암호화해서 저장**하도록 정한다(개인정보의 안전성 확보조치 기준 고시
제7조). 클라우드(Supabase)는 '인터넷 구간'에 해당하므로, 받는다면 기본적으로 암호화 대상이다.

| 대상 | 처리 |
|------|------|
| 비밀번호 | **일방향**(복호화 불가). 직접 저장하지 말고 Supabase Auth |
| 신용카드·계좌번호 | 양방향 암호화. 가능하면 결제 대행 토큰만 |
| 주민등록번호 등 고유식별정보(여권·운전면허·외국인등록번호) | 양방향 암호화(주민번호는 무조건) |
| 바이오정보(지문·얼굴 특징 등) | 양방향 암호화 |

> 이건 법무 자문이 아니라 실무 기본값이다. 정확한 의무 범위는 개인정보보호위원회의
> **'개인정보의 안전성 확보조치 기준'** 고시를 확인한다. 이름·이메일·연락처는 이 의무 대상이 아니다
> — 과잉 암호화하지 않는다.

## 0단계 — 먼저 "안 받기"를 시도한다 (가장 안전하고 단순)

직접 짠 암호화는 입문자가 가장 틀리기 쉬운 코드다. 받지 않으면 틀릴 일도 없다.

- **비밀번호** → **Supabase Auth**(이메일/비밀번호 로그인). 비밀번호를 우리 테이블에 저장하지 않는다 —
  Auth가 해시까지 알아서 한다. `phase-build.md`의 '로그인 있음' 패턴을 그대로 쓴다.
- **카드·계좌번호** → **결제 대행(Toss Payments·Stripe)**. 결제사가 주는 **토큰**과 **끝 4자리**만
  저장한다. 카드 원번호(PAN)는 우리 DB에 두지 않는다.
- **주민번호 등 본인확인용** → **PASS/본인확인기관**으로 대체. 대부분의 앱은 주민번호 자체가 필요 없다.

여기서 다 해결되면 아래 암호화 단계는 건너뛴다.

## 1단계 — 그래도 저장해야 하면: AES 암호화 (양방향)

### 키 발급 (한 번만)

```bash
openssl rand -base64 32
```

출력값을 `.env.local`에 넣는다. **`NEXT_PUBLIC_` 접두사를 절대 붙이지 않는다**(붙이면 브라우저에
노출돼 암호화가 무의미해진다). Vercel env에도 같은 이름으로 등록한다.

```
ENCRYPTION_KEY=<openssl 출력값>
```

### `lib/crypto.ts` — 서버 전용 헬퍼

`'use client'` 모듈에서 절대 import 하지 않는다. 서버 라우트에서만 쓴다.

```ts
import crypto from 'node:crypto'

const ALGO = 'aes-256-gcm'
const KEY = Buffer.from(process.env.ENCRYPTION_KEY ?? '', 'base64') // 32바이트(AES-256)

export function encrypt(plain: string): string {
  const iv = crypto.randomBytes(12)
  const cipher = crypto.createCipheriv(ALGO, KEY, iv)
  const enc = Buffer.concat([cipher.update(plain, 'utf8'), cipher.final()])
  const tag = cipher.getAuthTag()
  return [iv, tag, enc].map((b) => b.toString('base64')).join('.')
}

export function decrypt(blob: string): string {
  const [iv, tag, enc] = blob.split('.').map((s) => Buffer.from(s, 'base64'))
  const decipher = crypto.createDecipheriv(ALGO, KEY, iv)
  decipher.setAuthTag(tag)
  return Buffer.concat([decipher.update(enc), decipher.final()]).toString('utf8')
}
```

### 테이블 — 암호문을 담을 컬럼

암호문은 `text`에 담는다. 컬럼명에 `_enc` 접미사를 붙여 "평문이 아님"을 드러낸다.

```sql
create table public.applicants (
  id uuid primary key default gen_random_uuid(),
  name text,                  -- 일반 정보: 그대로
  resident_no_enc text,       -- 주민번호 암호문 (절대 평문 아님)
  created_at timestamptz default now()
);
alter table public.applicants enable row level security;
-- 클라이언트는 RLS로 막고, 쓰기·읽기는 서버 라우트에서 service_role로 처리
```

### 서버 라우트에서만 암복호화

```ts
// app/api/applicants/route.ts  — 서버에서만 실행됨
import { encrypt, decrypt } from '@/lib/crypto'
import { createClient } from '@supabase/supabase-js'

const admin = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!, // 서버 전용 키
)

export async function POST(req: Request) {
  const { name, residentNo } = await req.json()
  await admin.from('applicants').insert({
    name,
    resident_no_enc: encrypt(residentNo), // 저장 직전 암호화
  })
  return Response.json({ ok: true })
}

export async function GET() {
  const { data } = await admin.from('applicants').select('id, name, resident_no_enc')
  // 정말 원문이 필요할 때만 decrypt 한다. 보통은 끝자리만 보여주는 걸로 충분하다.
  const rows = (data ?? []).map((r) => ({
    id: r.id,
    name: r.name,
    residentNoTail: decrypt(r.resident_no_enc).slice(-4), // 예: 뒤 4자리만 노출
  }))
  return Response.json(rows)
}
```

화면(클라이언트)은 이 라우트를 `fetch`로만 부른다 — 암호화 키도 평문도 브라우저로 내려가지 않는다.

## 1단계(비밀번호 예외) — 부득이 직접 저장한다면: 해시 (일방향)

비밀번호는 복원되면 안 되므로 양방향 암호화가 아니라 **해시**다. Supabase Auth를 못 쓰는
특수한 경우에만, `bcryptjs`로 서버 라우트에서 해시해 저장하고 로그인 시 `compare`로 검증한다.
가능하면 이 길로 가지 말고 Auth를 쓴다.

## 주의

- **키가 한 번이라도 노출됐다면**(`NEXT_PUBLIC_`로 빌드에 들어갔거나 git에 커밋됨) 새 키를 발급하고,
  기존 데이터를 옛 키로 복호화 → 새 키로 재암호화해야 한다.
- 암호화는 "저장 시 보호"일 뿐이다. RLS·서버 라우트·키 분리가 무너지면 의미가 없다 —
  배포 전 `orange-secure`로 함께 점검한다.
