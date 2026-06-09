# PLAYBOOK VẬN HÀNH 4 AI AGENTS — HỆ THỐNG `thunhap.vn`
## Tài liệu chi tiết hóa Mục 6 của Kế Hoạch Triển Khai (Agent 1 → Agent 4)

> **Phiên bản:** 1.0 · **Ngày lập:** 09/06/2026 · **Người duyệt:** Alan Nguyễn Tú
> **Bổ trợ cho:** `docs/KE-HOACH-TRIEN-KHAI-CHI-TIET.md`
> **Mục đích:** Biến 4 Agent từ mô tả khái niệm thành quy trình vận hành cụ thể — sẵn sàng để dựng kỹ thuật và chạy thật.

---

## TỔNG QUAN LUỒNG PHỐI HỢP 4 AGENT

```
AGENT 1 (Media Factory)  →  Kéo traffic về thunhap.vn
        │
        ▼
AGENT 2 (AI Closer)      →  Chốt đơn FE 399k qua hội thoại + VietQR
        │ (webhook tiền về)
        ▼
AGENT 3 (Fulfillment)    →  Gemini sinh báo cáo độc bản → PDF → gửi ≤120s
        │
        ▼
AGENT 4 (Nurture/Upsell) →  Nuôi tệp → điều hướng khoahoc.ai (BE 20tr)
```

| Agent | Mục tiêu số liệu cốt lõi | KPI chính |
| :--- | :--- | :--- |
| 1 — Media Factory | Tạo ≥ 2.000 lượt truy cập LP/ngày (T4) | View → click bio ≥ 3% |
| 2 — AI Closer | Tỷ lệ LP → mua FE ≥ 5% | Hoàn tất hội thoại ≥ 40% |
| 3 — Fulfillment | Trả báo cáo ≤ 120 giây, hoàn tiền ≤ 3% | Tỷ lệ giao thành công 100% |
| 4 — Nurture/Upsell | Chốt FE → BE ≥ 5% | Mở email ≥ 35%, CTR ≥ 8% |

---

# AGENT 1 — AI MEDIA FACTORY (Nhà máy nội dung kéo traffic)

## 1.1. Pipeline sản xuất tự động

```
[1] Cào trend  →  [2] Gemini viết kịch bản  →  [3] 11Labs lồng tiếng
       │                                              │
       └──────────────  [4] Midjourney/Canva tạo hình ──┘
                                  │
                    [5] Ghép video (CapCut/Auto-editor)
                                  │
                    [6] Lên lịch & đăng đa kênh (Make/Metricool)
```

| Bước | Công cụ | Đầu ra |
| :--- | :--- | :--- |
| 1. Cào chủ đề viral | Gemini + Google Trends/TikTok Creative Center | 10–20 chủ đề tài chính/vận số hot/tuần |
| 2. Viết kịch bản | Gemini Pro (prompt khung bên dưới) | Kịch bản 30–60s, hook sắc |
| 3. Lồng tiếng | ElevenLabs (clone giọng chuyên gia) | File audio |
| 4. Hình ảnh | Midjourney / Canva | Ảnh nền sang trọng, b-roll |
| 5. Dựng video | CapCut template / auto-edit | Video dọc 9:16 |
| 6. Phân phối | Make/Zapier + Metricool | Đăng TikTok/Reels/Shorts theo lịch |

## 1.2. Trục nội dung (Content Pillars)

| Trục | Tỷ trọng | Mục đích | Ví dụ chủ đề |
| :--- | ---: | :--- | :--- |
| 🧠 Tư duy hệ thống & dòng tiền | 40% | Tạo "aha", định vị chuyên gia | "Vì sao cày 10 năm vẫn không giữ được tiền" |
| 💡 Vận số/định hướng tài chính cá nhân | 30% | Khơi tò mò → click chẩn đoán | "3 nhóm người dễ giàu nhất theo cấu trúc thu nhập" |
| 🤖 AI & tự động hóa kiếm tiền | 20% | Dẫn nhập trục Back-End | "Tôi để AI chốt đơn khi đang ngủ như thế nào" |
| 🏆 Bằng chứng & câu chuyện | 10% | Tạo niềm tin (social proof) | Kết quả khách, hậu trường hệ thống |

## 1.3. Công thức Hook (3 giây đầu quyết định)

1. **Nghịch lý:** "Càng chăm chỉ, bạn càng nghèo đi — đây là lý do."
2. **Tiết lộ con số:** "Top 10% người Việt cùng ngành có 3,8 nguồn thu. Bạn có mấy?"
3. **Phản đề niềm tin:** "Quên 'kiếm thêm tiền' đi. Vấn đề của bạn là CẤU TRÚC dòng tiền."
4. **Tò mò định danh:** "Gõ ngày sinh, AI nói thẳng bạn đang kẹt ở tầng thu nhập nào."

## 1.4. Prompt khung cho Gemini (viết kịch bản)

```
Vai trò: Bạn là copywriter chuyên video ngắn viral về tài chính cá nhân,
giọng điệu sắc bén, thẳng thắn, truyền cảm hứng (phong cách Naval + Kiyosaki).

Đầu vào: [Chủ đề trend] + [Trục nội dung] + [Insight tử huyệt của khách]

Yêu cầu đầu ra (script 30–60 giây):
1. HOOK (0–3s): 1 câu gây sốc/nghịch lý, dùng 1 trong 4 công thức hook.
2. THÂN (3–45s): 3 luận điểm ngắn, mỗi luận điểm 1 câu, có 1 con số cụ thể.
3. CTA (45–60s): điều hướng "Bấm link bio nhận chẩn đoán cấu trúc thu nhập miễn phí".
4. Kèm: 5 hashtag, 3 gợi ý cảnh quay/b-roll, mô tả giọng đọc.

Ràng buộc: không hứa hẹn làm giàu nhanh; tập trung vào tư duy & cấu trúc.
```

## 1.5. Lịch đăng (Cadence)

| Kênh | Tần suất | Khung giờ vàng (VN) |
| :--- | :--- | :--- |
| TikTok | 2–3 video/ngày | 12h, 20h, 22h |
| Reels (IG/FB) | 1–2 video/ngày | 12h, 21h |
| YouTube Shorts | 1 video/ngày | 19h–21h |

> **Mục tiêu T4:** ~150 video/tháng (organic) + ngân sách Ads mồi đẩy các video có ROAS tốt.

---

# AGENT 2 — AI CLOSER (Chatbot chốt đơn trên landing)

> **Trạng thái hiện tại:** đang là form 12 câu tĩnh. **Mục tiêu:** nâng thành chatbot hội thoại đóng vai *Trợ lý Tài chính cấp cao*, hỏi 3–5 câu tử huyệt, xuất teaser, chốt offer 399k + QR.

## 2.1. Kịch bản hội thoại (Conversation Flow)

```
[B1] CHÀO & TẠO NGỮ CẢNH
  "Chào bạn 👋 Mình là trợ lý tài chính AI của Thu Nhập AI.
   Trong 90 giây, mình sẽ chẩn đoán nhanh cấu trúc thu nhập của bạn
   đang ở tầng nào và đâu là nút thắt lớn nhất. Bắt đầu nhé?"

[B2] THU THẬP DỮ LIỆU (3–5 câu tử huyệt)
  Q1. Tên & năm sinh của bạn? (định danh + cá nhân hóa)
  Q2. Bạn đang chủ yếu ở nhóm nào: Làm công / Tự doanh / Chủ DN / Đầu tư?
  Q3. Thu nhập hiện tại mỗi tháng rơi vào khoảng nào? [các mốc]
  Q4. Bạn đang có bao nhiêu NGUỒN thu nhập? (1 / 2 / 3+)
  Q5. Nút thắt lớn nhất của bạn lúc này là gì? [chọn: hết tiền cuối tháng /
      không có thời gian / không biết bắt đầu từ đâu / sợ rủi ro]

[B3] XUẤT TEASER MIỄN PHÍ (tạo niềm tin cao độ)
  → AI phân tích nhanh, trả về 3 ý:
    • "Bạn đang ở Top ~X% người cùng ngành" (định vị)
    • "Phát hiện nút thắt #1: ..." (1 nỗi đau cụ thể có số liệu)
    • "Nếu không xử lý, 12 tháng tới bạn có thể bỏ lỡ ~Y triệu" (chi phí cơ hội)

[B4] CHỐT OFFER (399k)
  "Đây mới là phần nổi của tảng băng. Bản đồ Dòng tiền đầy đủ 45 trang —
   được Gemini biên soạn ĐỘC BẢN cho riêng [Tên] — sẽ chỉ rõ lộ trình
   90 ngày để gỡ nút thắt này.
   Phí xử lý dữ liệu hệ thống: 399.000đ. Mở khóa ngay?"
  → Hiện mã VietQR động (đã điền sẵn số tiền + cú pháp định danh).

[B5] XỬ LÝ TỪ CHỐI (Objection handling)
  • "Đắt quá" → so sánh: "Bằng 2 ly cà phê, đổi lấy lộ trình tránh mất Y triệu."
  • "Để suy nghĩ" → khan hiếm: "Ưu đãi 399k chỉ áp dụng trong phiên này."
  • "Có đáng tin không" → bảo chứng: "Hoàn tiền 100% trong 30 ngày nếu không hữu ích."
```

## 2.2. Khung System Prompt cho Agent 2

```
Vai trò: Trợ lý Tài chính cấp cao của Thu Nhập AI. Giọng điệu: chuyên nghiệp,
thấu cảm, dẫn dắt, KHÔNG spam. Mục tiêu: thu thập đủ dữ liệu chẩn đoán rồi
chốt đơn báo cáo 399k.

Quy tắc:
- Mỗi lượt chỉ hỏi 1 câu, ngắn gọn, có emoji vừa phải.
- Cá nhân hóa bằng tên khách ngay khi có.
- Sau khi đủ dữ liệu, BẮT BUỘC xuất teaser có ÍT NHẤT 1 con số cụ thể.
- Không bịa số liệu vô căn cứ; dùng dải benchmark đã cấu hình.
- Khi khách đồng ý mua → trả về JSON {action:"show_qr", amount:399000,
  code:"TNSP<4 số cuối SĐT>", customer:{...}} để hệ thống render QR.
- Tuyệt đối không hứa hẹn làm giàu nhanh hay cam kết lợi nhuận.
```

## 2.3. Dữ liệu cần lưu về Supabase (bảng `leads`)
`name, birth_year, quadrant, income_band, streams, blocker, teaser_summary, status, created_at`

---

# AGENT 3 — AI FULFILLMENT (Đóng gói & trả hàng tự động) — *Phần lõi nhất*

## 3.1. Luồng kỹ thuật (Webhook → Giao hàng ≤ 120s)

```
[1] Khách quét VietQR, chuyển khoản
[2] SePay/PayOS phát webhook  →  Edge Function (Supabase)
[3] Xác thực: số tiền + cú pháp định danh khớp đơn  →  status = "paid"
[4] Trigger gọi Gemini Pro với prompt khung + hồ sơ khách
[5] Nhận văn bản  →  module render PDF (cấu trúc 45 trang)
[6] Upload PDF lên storage  →  lấy link tải
[7] Gửi Email (EmailJS) + Zalo (Zalo OA) kèm link  →  status = "delivered"
```

**Bảng Supabase `orders`:**
`order_code, lead_id, package, amount, payment_status, gemini_status, pdf_url, delivered_at`

## 3.2. Khung Prompt sinh báo cáo (Gemini Pro)

```
Vai trò: Chuyên gia hoạch định tài chính cá nhân + cố vấn hệ thống kinh doanh,
kết hợp tư duy Kiyosaki (Cashflow Quadrant), Ramit Sethi (Rich Life),
Naval (đòn bẩy) và kế toán quản trị.

Đầu vào (hồ sơ khách từ Agent 2): tên, năm sinh, quadrant, thu nhập,
số nguồn thu, nút thắt, ngành nghề.

Nhiệm vụ: Soạn một báo cáo ĐỘC BẢN ~45 trang, văn phong sâu sắc, trôi chảy,
học thuật nhưng thực chiến, cá nhân hóa tuyệt đối (gọi tên khách xuyên suốt).

Bố cục bắt buộc (xem mục 3.3). Mỗi chương:
- Bắt đầu bằng phân tích riêng cho hồ sơ khách (không nói chung chung).
- Có ít nhất 1 con số/benchmark cụ thể.
- Kết bằng "việc cần làm" (actionable).

Ràng buộc: không hứa làm giàu nhanh; mọi khuyến nghị thực tế, có rủi ro kèm theo.
Chương cuối PHẢI có "điểm chuyển đổi tử huyệt" điều hướng sang khoahoc.ai.
```

## 3.3. Cấu trúc báo cáo PDF 45 trang (Table of Contents)

| Chương | Nội dung | Số trang |
| :--- | :--- | ---: |
| Bìa & Lời ngỏ cá nhân hóa | Tên khách, ngày lập, cam kết bảo mật | 2 |
| 1. Chẩn đoán vị trí hiện tại | Bạn đang ở tầng nào của Cashflow Quadrant | 4 |
| 2. Bản đồ dòng tiền cá nhân | Phân tích thu/chi/nợ, 3 nút thắt lớn nhất | 6 |
| 3. So sánh benchmark ngành | Top 1/10/25% — khoảng cách & chi phí cơ hội | 5 |
| 4. Rich Life Number của bạn | Mục tiêu tài chính được lượng hóa | 4 |
| 5. Lộ trình 90 ngày | Chia 3 sprint 30 ngày, mục tiêu cụ thể từng tuần | 8 |
| 6. Chiến lược đa dạng hóa nguồn thu | Gợi ý 2–3 dòng thu phù hợp hồ sơ | 6 |
| 7. Đòn bẩy AI & tự động hóa | Áp dụng công nghệ vào mô hình của khách | 5 |
| 8. Điểm chuyển đổi (Upsell) | Lý do cần "cỗ máy chuyển giao" tại khoahoc.ai | 3 |
| Phụ lục: 5 quà tặng kèm | Template, checklist, prompt mẫu | 2 |

## 3.4. Quy chuẩn thiết kế PDF
- Font tinh tế (Fraunces tiêu đề / DM Sans nội dung — đồng bộ brand web).
- Lề thoáng, có mục lục, header/footer thương hiệu, watermark độc bản (mã đơn).
- Xuất A4 dọc, nhúng tên khách ở footer mỗi trang (chống chia sẻ trái phép).

---

# AGENT 4 — AI NURTURE & UPSELL (Nuôi tệp & nâng giá trị vòng đời)

## 4.1. Phân loại tệp khách (Segmentation trong Supabase)

| Phân khúc | Tiêu chí | Hành động ưu tiên |
| :--- | :--- | :--- |
| 🌱 FE mới mua | Vừa nhận báo cáo 399k | Chuỗi welcome 5 ngày + gieo mầm BE |
| 🔥 Nóng (engaged) | Mở email > 2 lần / click link khoahoc.ai | Mời đặt Discovery Call ngay |
| 😴 Nguội | Không tương tác > 30 ngày | Bản tin tái kích hoạt + case study |
| 👑 Khách BE | Đã mua gói 20tr | Onboarding + chăm sóc giữ chân + referral |

## 4.2. Chuỗi Welcome sau mua FE (5 email/Zalo)

| Ngày | Nội dung | Mục tiêu |
| :--- | :--- | :--- |
| D0 | Gửi báo cáo + hướng dẫn đọc | Giao hàng, tạo "wow" |
| D1 | "3 trang quan trọng nhất trong báo cáo của bạn" | Tăng tiêu thụ nội dung |
| D3 | Case study: người cùng hồ sơ đã bứt phá thế nào | Tạo khát vọng |
| D5 | "Tự xây mất 1–2 năm — hoặc nhận chuyển giao sẵn" → CTA khoahoc.ai | Gieo mầm Upsell |
| D7 | Mời đặt Discovery Call (Calendly) — ưu đãi có hạn | Chốt chuyển trục BE |

## 4.3. Bản tin hàng tháng (Monthly Newsletter)
- Cập nhật "vận số tài chính" cá nhân hóa theo phân khúc.
- 1 insight chiến lược + 1 case study + 1 CTA mềm về khoahoc.ai.
- Mục tiêu: tỷ lệ mở ≥ 35%, CTR ≥ 8%.

## 4.4. Trigger Upsell tự động → `khoahoc.ai`
```
NẾU (khách click link khoahoc.ai ≥ 1 lần) HOẶC (mở email D5/D7)
  → gắn tag "BE-hot"
  → tự gửi lời mời đặt Discovery Call qua Zalo
  → tạo lịch Calendly + email tài liệu chuẩn bị trước call
NẾU (đặt lịch thành công)
  → nhắc lịch tự động (trước 24h & 1h)
```

---

## PHỤ LỤC: TRẠNG THÁI TRIỂN KHAI & ĐỘ ƯU TIÊN

| Agent | Độ ưu tiên | Phụ thuộc | Giai đoạn (theo roadmap) |
| :--- | :--- | :--- | :--- |
| Agent 3 — Fulfillment | 🔴 Cao nhất | Supabase + webhook + Gemini + PDF | Giai đoạn 0 (Tuần 1–2) |
| Agent 2 — AI Closer | 🟠 Cao | Gemini + Lovable; có thể giữ form tạm | Giai đoạn 2 (Tháng 2–3) |
| Agent 1 — Media Factory | 🟠 Cao | Gemini/11Labs/Midjourney + Make | Giai đoạn 1 (Tuần 3–4) |
| Agent 4 — Nurture/Upsell | 🟡 TB | Supabase + Email/Zalo + khoahoc.ai | Giai đoạn 2 (Tháng 2–3) |

> **Khuyến nghị thứ tự dựng:** Agent 3 (để giao hàng tự động được trước) → Agent 1 (kéo traffic) → Agent 2 (tăng tỷ lệ chốt) → Agent 4 (vắt giá trị vòng đời sang BE).

---

*Tài liệu này chi tiết hóa Mục 6 của Kế Hoạch Triển Khai. Mọi kịch bản/prompt là bản nháp khung — sẽ tinh chỉnh theo dữ liệu hội thoại & chất lượng báo cáo thực tế.*
