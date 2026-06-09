# THIẾT LẬP KỸ THUẬT BACKEND — Agent 3 Fulfillment Engine
## Schema Supabase đầy đủ + Edge Functions (Webhook thanh toán → Gemini → PDF → Giao hàng)

> **Phiên bản:** 1.0 · **Ngày lập:** 09/06/2026 · **Người duyệt:** Alan Nguyễn Tú
> **Bổ trợ cho:** `docs/PLAYBOOK-4-AI-AGENTS.md` (Agent 3, mục 3.1–3.4)
> **Stack:** Supabase (Postgres + Edge Functions/Deno) · SePay/PayOS · Gemini API · PDF service · EmailJS/Resend · Zalo OA
> **Lưu ý:** Các đoạn code là *scaffolding khung* — biến nhạy cảm để ở Environment Variables, KHÔNG hardcode key.

---

## 0. KIẾN TRÚC TỔNG QUAN

```
Khách quét VietQR → chuyển khoản
        │
        ▼
[SePay/PayOS] ──POST webhook──► Edge Function: payment-webhook
                                      │ 1. Xác thực chữ ký/API key
                                      │ 2. Trích order_code từ nội dung CK
                                      │ 3. Khớp đơn pending + đúng số tiền
                                      │ 4. UPDATE orders.payment_status='paid'
                                      │ 5. Gọi Edge Function: fulfillment
                                      ▼
                            Edge Function: fulfillment
                                      │ a. Lấy order + lead
                                      │ b. Gemini sinh báo cáo độc bản
                                      │ c. Render HTML → PDF → Storage
                                      │ d. Gửi Email + Zalo (link PDF)
                                      │ e. UPDATE delivered_at
                                      ▼
                            Khách nhận báo cáo ≤ 120 giây
```

---

## 1. SCHEMA SUPABASE (SQL DDL)

> Chạy trong **Supabase Studio → SQL Editor**. Thứ tự: bảng → index → RLS → policy → storage.

### 1.1. Bảng `leads` (Agent 2 thu thập)

```sql
create table public.leads (
  id              uuid primary key default gen_random_uuid(),
  name            text,
  birth_year      int,
  quadrant        text check (quadrant in ('E','S','B','I','MIX')),
  income_band     text,                 -- ví dụ '10-20tr', '20-50tr'
  streams         int,                  -- số nguồn thu nhập
  blocker         text,                 -- nút thắt khách chọn
  industry        text,
  teaser_summary  text,                 -- teaser AI đã xuất
  email           text,
  phone           text,
  status          text not null default 'new'
                    check (status in ('new','engaged','converted_fe','converted_be','cold')),
  utm_source      text,
  created_at      timestamptz not null default now()
);
```

### 1.2. Bảng `orders` (đơn FE/BE)

```sql
create table public.orders (
  id               uuid primary key default gen_random_uuid(),
  order_code       text unique not null,            -- TNSP1234 / TNVIP1234
  lead_id          uuid references public.leads(id) on delete set null,
  package          text not null default 'fe_report'
                     check (package in ('fe_report','starter','sprint','mastery','be_transfer')),
  amount           int  not null,                   -- VNĐ
  customer_name    text,
  customer_email   text,
  customer_phone   text,
  payment_status   text not null default 'pending'
                     check (payment_status in ('pending','paid','failed','refunded')),
  paid_at          timestamptz,
  gemini_status    text not null default 'idle'
                     check (gemini_status in ('idle','generating','done','error')),
  pdf_url          text,
  delivered_at     timestamptz,
  bank_ref         text,                            -- mã giao dịch ngân hàng
  raw_webhook      jsonb,                           -- lưu nguyên payload để đối soát
  created_at       timestamptz not null default now()
);
```

### 1.3. Bảng `events` (nhật ký vận hành / đối soát)

```sql
create table public.events (
  id          bigint generated always as identity primary key,
  order_id    uuid references public.orders(id) on delete cascade,
  type        text not null,   -- webhook_received | payment_matched | gemini_done
                               -- | pdf_rendered | email_sent | zalo_sent | error
  detail      jsonb,
  created_at  timestamptz not null default now()
);
```

### 1.4. Index

```sql
create index idx_orders_code         on public.orders (order_code);
create index idx_orders_pay_status   on public.orders (payment_status);
create index idx_orders_email        on public.orders (customer_email);
create index idx_leads_status        on public.leads (status);
create index idx_events_order        on public.events (order_id);
```

### 1.5. RLS (Row Level Security)

> Nguyên tắc: **đóng mặc định**. Edge Functions dùng `service_role` (bỏ qua RLS). Client tĩnh chỉ được phép *chèn* lead, không đọc/sửa gì khác.

```sql
alter table public.leads  enable row level security;
alter table public.orders enable row level security;
alter table public.events enable row level security;

-- Cho phép trang tĩnh (anon) chèn lead khi khách hoàn tất chatbot
create policy "anon can insert leads"
  on public.leads for insert
  to anon
  with check (true);

-- KHÔNG tạo policy select/update/delete cho anon → mọi đọc/ghi nhạy cảm
-- đều phải đi qua Edge Function (service_role). orders & events: 0 policy public.
```

> ⚠️ Khuyến nghị an toàn hơn: thay vì để anon insert trực tiếp, dùng Edge Function `capture-lead` có rate-limit + validation. Policy trên là phương án nhanh cho giai đoạn đầu.

### 1.6. Storage bucket cho PDF

```sql
-- Tạo bucket private (chỉ truy cập qua signed URL)
insert into storage.buckets (id, name, public)
values ('reports', 'reports', false);
```

---

## 2. BIẾN MÔI TRƯỜNG (Edge Functions Secrets)

Cấu hình qua CLI: `supabase secrets set KEY=value`

| Biến | Mô tả |
| :--- | :--- |
| `SUPABASE_URL` | URL project (tự có sẵn) |
| `SUPABASE_SERVICE_ROLE_KEY` | Service role key — bỏ qua RLS (tự có sẵn) |
| `SEPAY_API_KEY` | API key SePay gửi trong header `Authorization: Apikey ...` |
| `PAYOS_CHECKSUM_KEY` | (Nếu dùng PayOS) khóa để verify HMAC chữ ký |
| `GEMINI_API_KEY` | Khóa Google AI Studio / Gemini API |
| `PDF_API_KEY` | Khóa dịch vụ HTML→PDF (PDFShift/Browserless/DocRaptor) |
| `RESEND_API_KEY` | (Khuyến nghị) gửi email qua Resend REST |
| `ZALO_OA_TOKEN` | Access token Zalo Official Account |
| `BANK_ACCOUNT_NO` | Số TK nhận để đối chiếu webhook |

---

## 3. EDGE FUNCTION: `payment-webhook` (SePay)

> File: `supabase/functions/payment-webhook/index.ts` · Deploy với cờ `--no-verify-jwt` (webhook ngoài không có JWT).

```ts
// supabase/functions/payment-webhook/index.ts
import { createClient } from "jsr:@supabase/supabase-js@2";

const supabase = createClient(
  Deno.env.get("SUPABASE_URL")!,
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
);

// SePay gửi: { transferAmount, content, referenceCode, transferType, accountNumber, ... }
Deno.serve(async (req) => {
  // 1) Xác thực: SePay gửi header  Authorization: Apikey <SEPAY_API_KEY>
  const auth = req.headers.get("authorization") ?? "";
  const expected = `Apikey ${Deno.env.get("SEPAY_API_KEY")}`;
  if (auth !== expected) {
    return new Response("Unauthorized", { status: 401 });
  }

  const payload = await req.json();

  // Chỉ xử lý tiền VÀO
  if (payload.transferType !== "in") {
    return Response.json({ ok: true, skipped: "not incoming" });
  }

  // 2) Trích order_code (TNSP1234 / TNVIP1234) từ nội dung chuyển khoản
  const match = String(payload.content ?? "").toUpperCase().match(/TN(?:SP|VIP)\d{3,}/);
  if (!match) {
    await supabase.from("events").insert({
      type: "error", detail: { reason: "no_order_code", payload },
    });
    return Response.json({ ok: false, reason: "order_code_not_found" });
  }
  const orderCode = match[0];

  // 3) Khớp đơn pending + đúng số tiền
  const { data: order } = await supabase
    .from("orders")
    .select("*")
    .eq("order_code", orderCode)
    .eq("payment_status", "pending")
    .maybeSingle();

  if (!order) {
    await supabase.from("events").insert({
      type: "error", detail: { reason: "order_not_found_or_paid", orderCode },
    });
    return Response.json({ ok: false, reason: "order_not_found" });
  }

  if (Number(payload.transferAmount) < Number(order.amount)) {
    await supabase.from("events").insert({
      order_id: order.id, type: "error",
      detail: { reason: "amount_mismatch", expected: order.amount, got: payload.transferAmount },
    });
    return Response.json({ ok: false, reason: "amount_mismatch" });
  }

  // 4) Đánh dấu đã thanh toán
  await supabase.from("orders").update({
    payment_status: "paid",
    paid_at: new Date().toISOString(),
    bank_ref: payload.referenceCode,
    raw_webhook: payload,
  }).eq("id", order.id);

  await supabase.from("events").insert({
    order_id: order.id, type: "payment_matched",
    detail: { amount: payload.transferAmount, ref: payload.referenceCode },
  });

  // 5) Kích hoạt fulfillment (fire-and-forget để trả 200 nhanh cho SePay)
  fetch(`${Deno.env.get("SUPABASE_URL")}/functions/v1/fulfillment`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")}`,
    },
    body: JSON.stringify({ order_id: order.id }),
  }).catch((e) => console.error("fulfillment trigger failed", e));

  return Response.json({ ok: true });
});
```

### 3.1. Phương án PayOS (thay thế — verify HMAC)

```ts
// PayOS gửi { data, signature }. signature = HMAC_SHA256(sorted_querystring(data), CHECKSUM_KEY)
import { createHmac } from "node:crypto";

function verifyPayOS(data: Record<string, unknown>, signature: string): boolean {
  const sorted = Object.keys(data).sort()
    .map((k) => `${k}=${data[k]}`).join("&");
  const expected = createHmac("sha256", Deno.env.get("PAYOS_CHECKSUM_KEY")!)
    .update(sorted).digest("hex");
  return expected === signature;
}
// Sau khi verify ok → cùng logic khớp order_code & cập nhật như trên.
```

---

## 4. EDGE FUNCTION: `fulfillment` (Gemini → PDF → Giao hàng)

> File: `supabase/functions/fulfillment/index.ts`

```ts
// supabase/functions/fulfillment/index.ts
import { createClient } from "jsr:@supabase/supabase-js@2";

const supabase = createClient(
  Deno.env.get("SUPABASE_URL")!,
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
);

Deno.serve(async (req) => {
  const { order_id } = await req.json();

  // a) Lấy đơn + hồ sơ lead
  const { data: order } = await supabase
    .from("orders").select("*, leads(*)").eq("id", order_id).single();
  if (!order || order.payment_status !== "paid") {
    return Response.json({ ok: false, reason: "order_not_paid" });
  }

  await supabase.from("orders").update({ gemini_status: "generating" }).eq("id", order_id);

  try {
    // b) Gọi Gemini sinh báo cáo độc bản
    const reportText = await generateReport(order.leads, order);
    await supabase.from("events").insert({ order_id, type: "gemini_done" });

    // c) Render HTML → PDF → upload Storage
    const pdfBytes = await renderPdf(reportText, order);
    const path = `${order.order_code}.pdf`;
    await supabase.storage.from("reports").upload(path, pdfBytes, {
      contentType: "application/pdf", upsert: true,
    });
    const { data: signed } = await supabase.storage
      .from("reports").createSignedUrl(path, 60 * 60 * 24 * 30); // link 30 ngày
    const pdfUrl = signed!.signedUrl;
    await supabase.from("orders").update({
      gemini_status: "done", pdf_url: pdfUrl,
    }).eq("id", order_id);
    await supabase.from("events").insert({ order_id, type: "pdf_rendered" });

    // d) Gửi Email + Zalo
    await sendEmail(order, pdfUrl);
    await sendZalo(order, pdfUrl);

    // e) Đánh dấu đã giao
    await supabase.from("orders").update({
      delivered_at: new Date().toISOString(),
    }).eq("id", order_id);

    return Response.json({ ok: true, pdfUrl });
  } catch (e) {
    await supabase.from("orders").update({ gemini_status: "error" }).eq("id", order_id);
    await supabase.from("events").insert({
      order_id, type: "error", detail: { message: String(e) },
    });
    return Response.json({ ok: false, error: String(e) }, { status: 500 });
  }
});

// ---- Gemini ----
async function generateReport(lead: any, order: any): Promise<string> {
  const prompt = buildReportPrompt(lead, order); // dùng prompt khung ở Playbook mục 3.2
  const res = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key=${Deno.env.get("GEMINI_API_KEY")}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] }),
    },
  );
  const json = await res.json();
  return json.candidates?.[0]?.content?.parts?.[0]?.text ?? "";
}

function buildReportPrompt(lead: any, order: any): string {
  return `Bạn là chuyên gia hoạch định tài chính cá nhân (Kiyosaki/Ramit/Naval).
Soạn báo cáo ĐỘC BẢN ~45 trang cho khách: ${lead?.name}, sinh ${lead?.birth_year},
nhóm ${lead?.quadrant}, thu nhập ${lead?.income_band}, ${lead?.streams} nguồn thu,
nút thắt: ${lead?.blocker}. Bố cục 10 chương theo Playbook. Cá nhân hóa tuyệt đối,
mỗi chương có số liệu cụ thể + việc cần làm. Chương cuối điều hướng khoahoc.ai.
Xuất Markdown để render PDF.`;
}

// ---- PDF (qua dịch vụ HTML→PDF, ví dụ PDFShift) ----
async function renderPdf(markdown: string, order: any): Promise<Uint8Array> {
  const html = wrapHtmlTemplate(markdown, order); // chèn brand, footer mã đơn (chống share)
  const res = await fetch("https://api.pdfshift.io/v3/convert/pdf", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Basic ${btoa("api:" + Deno.env.get("PDF_API_KEY"))}`,
    },
    body: JSON.stringify({ source: html, format: "A4", margin: "20mm" }),
  });
  return new Uint8Array(await res.arrayBuffer());
}

function wrapHtmlTemplate(md: string, order: any): string {
  // TODO: chuyển markdown→HTML + CSS brand (Fraunces/DM Sans), watermark order_code mỗi trang
  return `<html><body style="font-family:'DM Sans'">${md}</body></html>`;
}

// ---- Email (Resend REST) ----
async function sendEmail(order: any, pdfUrl: string) {
  if (!order.customer_email) return;
  await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${Deno.env.get("RESEND_API_KEY")}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from: "Thu Nhập AI <info@thunhap.vn>",
      to: order.customer_email,
      subject: "📊 Báo cáo Bản đồ Dòng tiền của bạn đã sẵn sàng",
      html: `Chào ${order.customer_name},<br>Báo cáo độc bản của bạn:
             <a href="${pdfUrl}">Tải PDF</a> (mã đơn ${order.order_code}).`,
    }),
  });
  await supabase.from("events").insert({ order_id: order.id, type: "email_sent" });
}

// ---- Zalo OA ----
async function sendZalo(order: any, pdfUrl: string) {
  if (!order.customer_phone) return;
  // Zalo OA: gửi tin tư vấn / ZNS template kèm link tải
  await fetch("https://openapi.zalo.me/v3.0/oa/message/cs", {
    method: "POST",
    headers: {
      "access_token": Deno.env.get("ZALO_OA_TOKEN")!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      recipient: { user_id: order.zalo_user_id }, // cần map SĐT→user_id khi khách follow OA
      message: { text: `Báo cáo của bạn đã sẵn sàng: ${pdfUrl}` },
    }),
  });
  await supabase.from("events").insert({ order_id: order.id, type: "zalo_sent" });
}
```

---

## 5. TÍCH HỢP VỚI TRANG TĨNH `index.html`

Hiện trang tạo `order_code` ở client (`generateTransferCode()` → `TNSP<4 số cuối>`). Cần đồng bộ:

1. **Khi khách bấm "Thanh toán":** gọi 1 Edge Function `create-order` (hoặc insert qua RPC) để tạo bản ghi `orders` với `payment_status='pending'`, `order_code`, `amount`. → Đảm bảo webhook có đơn để khớp.
2. **Mã VietQR:** giữ nguyên `buildVietQRUrl()`, nhưng `addInfo` PHẢI là `order_code` để webhook trích đúng.
3. **Màn xác nhận:** poll `orders` theo `order_code` (qua Edge Function `check-status`) để hiện "Đã nhận thanh toán → đang gửi báo cáo".

> ⚠️ Rủi ro trùng mã: `TNSP<4 số cuối SĐT>` có thể trùng giữa 2 khách. **Khuyến nghị** đổi sang `TNSP` + 6 ký tự ngẫu nhiên (base36) để đảm bảo duy nhất, lưu ngay khi tạo đơn.

---

## 6. CHECKLIST TRIỂN KHAI (Giai đoạn 0)

- [ ] Tạo project Supabase, chạy SQL mục 1 (bảng + index + RLS + bucket).
- [ ] `supabase secrets set` đủ các biến mục 2.
- [ ] Deploy `payment-webhook` (`--no-verify-jwt`) + `fulfillment`.
- [ ] Đăng ký SePay, trỏ webhook URL về `payment-webhook`, set API key.
- [ ] Hoàn thiện `buildReportPrompt` + `wrapHtmlTemplate` (CSS brand + watermark).
- [ ] Thêm Edge Function `create-order` + nối vào `submitOrder()` của `index.html`.
- [ ] Đổi `order_code` sang dạng ngẫu nhiên 6 ký tự (chống trùng).
- [ ] Test end-to-end: chuyển khoản thật 399k → nhận PDF qua Email/Zalo ≤120s.
- [ ] Bật cảnh báo lỗi (query bảng `events` type='error').

---

*Tài liệu này chi tiết hóa kỹ thuật cho Agent 3 (Playbook mục 3). Code là khung tham khảo — cần review bảo mật (rate-limit, idempotency webhook, retry Gemini) trước khi chạy production.*
