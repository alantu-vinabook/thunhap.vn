# KẾ HOẠCH TRIỂN KHAI CHI TIẾT — HỆ THỐNG `thunhap.vn`
## Phễu Tự Hoàn Vốn (SLO) vận hành bằng AI Agents — Mục tiêu lợi nhuận & Mô hình P&L

> **Phiên bản:** 1.0 · **Ngày lập:** 09/06/2026 · **Người duyệt:** Alan Nguyễn Tú
> **Tài liệu nguồn:** *Bản Thiết Kế Chiến Lược: Hệ Thống Kinh Doanh Tự Động Bằng AI Agents*
> **Phạm vi:** Trục Front-End `thunhap.vn` (mồi 399k) → Trục Back-End `khoahoc.ai` (high-ticket 20tr)

---

## 0. TÓM TẮT ĐIỀU HÀNH (EXECUTIVE SUMMARY)

Mô hình là một **phễu tự hoàn vốn quảng cáo (Self-Liquidating Offer)**: doanh thu từ sản phẩm mồi 399.000đ ở đầu phễu bao phủ toàn bộ chi phí quảng cáo và hạ tầng, đưa **chi phí thuần để sở hữu một khách hàng tiềm năng chất lượng cao về ~0đ**. Toàn bộ lợi nhuận thực đến từ trục Back-End (gói chuyển giao hệ thống 20.000.000đ).

| Chỉ tiêu cốt lõi (trạng thái ổn định — Tháng 4+) | Giá trị mục tiêu |
| :--- | ---: |
| Doanh thu/tháng | **1.399.000.000đ** |
| Lợi nhuận ròng/tháng (theo thiết kế gốc) | **1.036.000.000đ** |
| Lợi nhuận ròng/tháng (kịch bản thận trọng có tính chi phí vận hành BE) | **~986.000.000đ** |
| Biên lợi nhuận ròng | **70–74%** |
| Chi phí sở hữu khách hàng (CAC thuần sau khi FE hoàn vốn) | **~0đ** |
| Thời gian có dòng tiền dương | **≤ 45 ngày** |

> ⚠️ **Lưu ý quan trọng về trạng thái hiện tại:** Trang `index.html` đã dựng đầy đủ giao diện phễu Front-End, mã VietQR động và 3 gói value ladder, **NHƯNG**: (1) "AI phân tích" hiện là công thức JavaScript tĩnh, *chưa* phải Gemini API; (2) toàn bộ cấu hình thanh toán/email/lead còn là placeholder; (3) chưa có backend Supabase + webhook xác nhận thanh toán + render PDF + gửi Zalo. Kế hoạch này bao gồm lộ trình lấp các khoảng trống đó.

---

## 1. MỤC TIÊU LỢI NHUẬN PHÂN KỲ (PROFIT TARGETS)

Mục tiêu 1 tỷ lợi nhuận/tháng là **trạng thái ổn định**, không phải tháng đầu. Lộ trình tăng trưởng (ramp-up) theo lượng đơn Front-End/tháng:

| Tháng | Giai đoạn | Đơn FE/tháng | Deal BE/tháng (5%) | Doanh thu | LN ròng (thận trọng) |
| :--- | :--- | ---: | ---: | ---: | ---: |
| **T1** | Setup + Soft launch | 100 | 5 | 139.900.000đ | 71.600.000đ |
| **T2** | Mở rộng kênh | 300 | 15 | 419.700.000đ | 274.800.000đ |
| **T3** | Tăng tốc | 600 | 30 | 839.400.000đ | 579.600.000đ |
| **T4** | **Đạt mục tiêu** | **1.000** | **50** | **1.399.000.000đ** | **986.000.000đ** |
| **T5** | Tối ưu CAC | 1.200 | 60 | 1.678.800.000đ | 1.189.200.000đ |
| **T6** | Bứt phá | 1.500 | 75 | 2.098.500.000đ | 1.494.000.000đ |
| | **Tổng 6 tháng** | **3.700** | **185** | **~6,58 tỷ** | **~4,60 tỷ** |

**Cột mốc tài chính:**
- **Ngày 0–15:** Hoàn thiện kỹ thuật lõi (config thật + backend + fulfillment MVP).
- **Ngày 30:** Hoàn thiện nội dung lõi + Agent 1 chạy đều, soft launch.
- **Ngày 45:** Dòng tiền dương (FE đã tự hoàn vốn ads).
- **Tháng 4:** Chạm mốc 1.000 đơn FE → lợi nhuận ~1 tỷ/tháng.
- **Tháng 6:** Ổn định + bứt phá, lợi nhuận ~1,5 tỷ/tháng.

---

## 2. MÔ HÌNH KINH TẾ ĐƠN VỊ (UNIT ECONOMICS)

Đây là "viên gạch" của toàn hệ thống — nếu mỗi đơn FE có biên đóng góp dương thì việc scale chỉ là bài toán bơm ngân sách quảng cáo.

### 2.1. Kinh tế 1 đơn Front-End (Báo cáo 399k)

| Khoản | Giá trị | Ghi chú |
| :--- | ---: | :--- |
| Giá bán FE | 399.000đ | Sản phẩm mồi (tripwire) |
| (–) CAC quảng cáo | 300.000đ | Ngân sách tối đa/đơn (TikTok/Reels/Shorts + Ads mồi) |
| (–) Phí cổng thanh toán (2%) | 7.980đ | SePay/PayOS/VietQR |
| (–) Chi phí API + hạ tầng/đơn | ~5.000đ | Gemini token + render PDF + lưu Supabase |
| **= Biên đóng góp FE/đơn** | **~86.020đ** | **DƯƠNG → phễu tự hoàn vốn ✓** |

> **Ý nghĩa:** Mỗi đơn FE không những trả hết tiền quảng cáo mà còn **dư ~86k** để nuôi hạ tầng và tích lũy. Khi đã có biên dương, mỗi đồng ngân sách ads bơm thêm đều an toàn → đòn bẩy scale gần như vô hạn (giới hạn chỉ ở khả năng hấp thụ traffic của thị trường và giá thầu ads).

### 2.2. Kinh tế 1 deal Back-End (Gói chuyển giao 20tr)

| Khoản | Giá trị | Ghi chú |
| :--- | ---: | :--- |
| Giá bán BE | 20.000.000đ | High-ticket tại `khoahoc.ai` |
| (–) Phí cổng thanh toán (2%) | 400.000đ | |
| (–) Chi phí vận hành/onboarding | ~1.000.000đ | Discovery call, tài liệu, mở khóa Hub, support |
| **= Biên đóng góp BE/deal** | **~18.600.000đ** | CAC = 0đ (đã được FE chi trả) |

### 2.3. Giá trị vòng đời & đòn bẩy phễu

- **AOV phễu (blended):** với 1.000 FE + 50 BE → doanh thu/khách FE = 1.399.000.000 / 1.000 = **1.399.000đ/khách FE**.
- **Tỷ lệ chuyển đổi FE→BE then chốt:** 5% (mục tiêu). Mỗi 1% cải thiện = +10 deal = **+200tr doanh thu/tháng**.
- **Ràng buộc năng lực:** 50 deal BE/tháng ≈ 50 Discovery Call × 45 phút ≈ **~37 giờ/tháng** — khả thi cho 1 người điều hành; trên 100 deal/tháng cần ủy quyền sales cấp cao.

---

## 3. BẢNG P&L CHI TIẾT — 3 KỊCH BẢN (TRẠNG THÁI ỔN ĐỊNH)

Tất cả tính cho **1 tháng ở trạng thái ổn định**. Các tham số thay đổi giữa 3 kịch bản: lượng đơn FE, CAC, tỷ lệ chốt BE.

### 3.1. Tham số đầu vào theo kịch bản

| Tham số | 🟡 Thận trọng | 🟢 Cơ sở (Base) | 🔴 Bứt phá |
| :--- | ---: | ---: | ---: |
| Đơn FE/tháng | 700 | 1.000 | 2.000 |
| CAC/đơn FE | 350.000đ | 300.000đ | 280.000đ |
| Tỷ lệ chốt BE | 3% | 5% | 6% |
| Deal BE/tháng | 21 | 50 | 120 |

### 3.2. P&L từng kịch bản

| Hạng mục | 🟡 Thận trọng | 🟢 Cơ sở | 🔴 Bứt phá |
| :--- | ---: | ---: | ---: |
| **I. TỔNG DOANH THU** | **699.300.000đ** | **1.399.000.000đ** | **3.198.000.000đ** |
| &nbsp;&nbsp;1. Doanh thu FE | 279.300.000đ | 399.000.000đ | 798.000.000đ |
| &nbsp;&nbsp;2. Doanh thu BE | 420.000.000đ | 1.000.000.000đ | 2.400.000.000đ |
| **II. TỔNG CHI PHÍ** | **313.486.000đ** | **412.980.000đ** | **793.960.000đ** |
| &nbsp;&nbsp;1. Quảng cáo (CAC) | 245.000.000đ | 300.000.000đ | 560.000.000đ |
| &nbsp;&nbsp;2. API AI + Server | 3.500.000đ | 5.000.000đ | 10.000.000đ |
| &nbsp;&nbsp;3. Phí cổng TT (2%) | 13.986.000đ | 27.980.000đ | 63.960.000đ |
| &nbsp;&nbsp;4. Công cụ/SaaS (cố định) | 30.000.000đ | 30.000.000đ | 40.000.000đ |
| &nbsp;&nbsp;5. Vận hành BE (1tr/deal) | 21.000.000đ | 50.000.000đ | 120.000.000đ |
| **III. LỢI NHUẬN RÒNG** | **385.814.000đ** | **986.020.000đ** | **2.404.040.000đ** |
| **Biên LN ròng** | **55,2%** | **70,5%** | **75,2%** |

### 3.3. Đối chiếu với "Thiết kế gốc"

Bản chiến lược gốc tính LN ròng **1.036.000.000đ (74%)** vì **không** tách chi phí vận hành BE (50tr) và xem phí công cụ gộp khác đi. Kế hoạch này giữ con số gốc làm **mục tiêu trần**, và dùng **986tr (kịch bản Cơ sở có tính chi phí vận hành BE)** làm **mục tiêu thực tế thận trọng hơn** để dự phòng.

> **Đòn bẩy tự hoàn vốn (kịch bản Cơ sở):** Doanh thu FE 399tr > Chi phí Ads 300tr → FE tự trả hết tiền quảng cáo và **dư 99tr** nuôi hạ tầng. ⇒ Toàn bộ **1 tỷ doanh thu BE gần như là lợi nhuận sạch**.

---

## 4. DỰ PHÓNG DÒNG TIỀN 6 THÁNG (CASH FLOW RAMP)

Theo kịch bản Cơ sở, tính chi phí vận hành BE (thận trọng). Đơn vị: triệu VNĐ.

| Hạng mục | T1 | T2 | T3 | T4 | T5 | T6 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Đơn FE | 100 | 300 | 600 | 1.000 | 1.200 | 1.500 |
| Deal BE | 5 | 15 | 30 | 50 | 60 | 75 |
| **Doanh thu** | **139,9** | **419,7** | **839,4** | **1.399** | **1.678,8** | **2.098,5** |
| (–) Quảng cáo | 30 | 90 | 180 | 300 | 360 | 450 |
| (–) API/Server | 0,5 | 1,5 | 3 | 5 | 6 | 7,5 |
| (–) Phí cổng 2% | 2,8 | 8,4 | 16,8 | 28 | 33,6 | 42 |
| (–) Công cụ cố định | 30 | 30 | 30 | 30 | 30 | 30 |
| (–) Vận hành BE | 5 | 15 | 30 | 50 | 60 | 75 |
| **LN ròng tháng** | **71,6** | **274,8** | **579,6** | **986** | **1.189,2** | **1.494** |
| **LN lũy kế** | **71,6** | **346,4** | **926** | **1.912** | **3.101,2** | **4.595,2** |

**Chi phí thiết lập một lần (Giai đoạn 0):** ~**50.000.000đ** (gồm: ngân sách test ads ban đầu ~30tr, mua gói SaaS năm đầu, domain/SSL/hosting, chi phí thiết kế PDF template + Gemini prompt engineering). Khoản này được hoàn vốn ngay trong **Tháng 1**.

> **Kết luận dòng tiền:** Ngay từ Tháng 1 đã dương (~71tr) nhờ cơ chế tự hoàn vốn. Không cần vốn lưu động lớn — chỉ cần ngân sách "mồi" ban đầu để test ads trước khi FE bắt đầu tự nuôi.

---

## 5. CẤU TRÚC GIÁ & VALUE LADDER (KIẾN NGHỊ CHUẨN HÓA)

Hiện trang web có 3 gói (990k / 2,9tr / 9,9tr) nhưng **thiếu sản phẩm mồi 399k** — chính là mắt xích quan trọng nhất của mô hình SLO. Kiến nghị cấu trúc lại thành thang giá trị 5 bậc:

| Bậc | Sản phẩm | Giá | Vai trò | Vị trí bán |
| :--- | :--- | ---: | :--- | :--- |
| **0** | Báo cáo Bản đồ Dòng tiền (PDF cá nhân hóa) | **399.000đ** | 🪝 Tripwire / SLO — *mắt xích còn thiếu* | `thunhap.vn` (sau quiz) |
| 1 | Income Starter | 990.000đ | Order bump / nâng cấp ngay | Trang pricing |
| 2 | Income Sprint ⭐ | 2.900.000đ | Gói chủ lực mid-tier | Trang pricing |
| 3 | Income Mastery | 9.900.000đ | Premium mid-tier | Trang pricing |
| **4** | **Gói Chuyển Giao Hệ Thống AI** | **20.000.000đ** | 👑 High-ticket — Profit Center | `khoahoc.ai` (qua Discovery Call) |

> **Hành động cần làm:** Thêm bậc 0 (399k) làm offer chính trên `thunhap.vn`, đặt các gói 990k–9,9tr làm upsell/order-bump trên màn pricing, và điều hướng bậc 4 (20tr) sang `khoahoc.ai` qua Calendly (SOP-04/05).

---

## 6. KIẾN TRÚC KỸ THUẬT & 4 AI AGENTS (TRẠNG THÁI CẦN ĐẠT)

| Agent | Chức năng | Công nghệ | Trạng thái hiện tại |
| :--- | :--- | :--- | :--- |
| **Agent 1 — AI Media Factory** | Cào trend → Gemini viết kịch bản → 11Labs lồng tiếng → Midjourney tạo hình → tự đăng đa kênh | Gemini, 11Labs, Midjourney, Make/Zapier | ❌ Chưa có |
| **Agent 2 — AI Closer** | Chatbot hội thoại trên landing, hỏi tử huyệt, xuất teaser, chốt offer 399k + QR | Lovable + Gemini | ⚠️ Đang là form 12 câu tĩnh |
| **Agent 3 — AI Fulfillment** | Webhook tiền về → Gemini sinh báo cáo độc bản → render PDF → gửi Email/Zalo ≤120s | SePay/PayOS, Supabase, Gemini, PDF engine, Zalo OA | ❌ Chưa có (phần lõi nhất) |
| **Agent 4 — AI Nurture & Upsell** | Phân loại tệp, bản tin hàng tháng, điều hướng lên `khoahoc.ai` | Supabase, Email/Zalo automation | ❌ Chưa có |

---

## 7. LỘ TRÌNH TRIỂN KHAI THEO TUẦN (ROADMAP)

### 🔧 GIAI ĐOẠN 0 — Nền móng "ra tiền được" (Tuần 1–2)
*Mục tiêu: trang bán được hàng thật, fulfillment bán-tự-động.*
- [ ] Điền cấu hình thật: TK ngân hàng, EmailJS (info@thunhap.vn), Lead endpoint (Google Sheet/Supabase).
- [ ] Thêm sản phẩm mồi **399k** vào phễu; chuẩn hóa value ladder.
- [ ] Dựng Supabase: bảng `leads`, `orders`, trạng thái thanh toán.
- [ ] Tích hợp webhook **SePay/PayOS** → cập nhật trạng thái "Đã thanh toán".
- [ ] **Fulfillment MVP:** gọi Gemini API sinh báo cáo + render PDF + gửi Email tự động.
- [ ] Soft launch nội bộ (10–20 đơn test).

### 📈 GIAI ĐOẠN 1 — Bật vòi traffic (Tuần 3–4)
*Mục tiêu: T1 đạt ~100 đơn FE.*
- [ ] Dựng pipeline **Agent 1** (AI Media Factory) — quy trình bán tự động trước, tự động sau.
- [ ] Lên lịch nội dung đều đặn TikTok/Reels/Shorts.
- [ ] Test ads mồi với ngân sách nhỏ (~30tr), đo CAC & ROAS.
- [ ] Tích hợp gửi **Zalo** kèm link PDF (hoàn thiện SOP-03).

### 🚀 GIAI ĐOẠN 2 — Tối ưu chuyển đổi & dựng Back-End (Tháng 2–3)
*Mục tiêu: T3 đạt ~600 đơn FE, mở trục BE.*
- [ ] Nâng cấp **Agent 2** thành chatbot Closer hội thoại (thay form tĩnh).
- [ ] A/B test landing, headline, offer, giá.
- [ ] Dựng `khoahoc.ai`: VSL + Calendly + sales page gói 20tr.
- [ ] **Agent 4:** bản tin hàng tháng + kịch bản upsell tự động.

### 🏆 GIAI ĐOẠN 3 — Scale & bứt phá (Tháng 4–6)
*Mục tiêu: T4 đạt 1.000 đơn, lợi nhuận ~1 tỷ; T6 bứt phá.*
- [ ] Tăng ngân sách ads theo biên đóng góp dương, tối ưu CAC.
- [ ] Mở rộng kênh traffic + kích hoạt `somenh.vn`.
- [ ] Tự động hóa hoàn toàn 4 Agents, giảm can thiệp thủ công về tối thiểu.
- [ ] Đóng gói "Hub chuyển giao" cho khách BE (prompt gốc, source Lovable, cấu trúc Supabase).

---

## 8. KPI & BẢNG ĐIỀU KHIỂN (DASHBOARD)

| Nhóm | Chỉ số | Mục tiêu | Ngưỡng cảnh báo |
| :--- | :--- | ---: | :--- |
| Traffic | Lượt truy cập landing/ngày | ≥ 2.000 (T4) | < 1.000 |
| Chuyển đổi | Tỷ lệ LP → mua FE | ≥ 5% | < 2% |
| Quảng cáo | CAC/đơn FE | ≤ 300.000đ | > 399.000đ (mất self-liquidating) |
| Quảng cáo | ROAS phễu | ≥ 4,5x | < 2x |
| Back-End | Tỷ lệ chốt FE → BE | ≥ 5% | < 3% |
| Tài chính | Biên LN ròng | ≥ 70% | < 50% |
| Chất lượng | Tỷ lệ hoàn tiền | ≤ 3% | > 8% |
| Vận hành | Thời gian trả báo cáo | ≤ 120 giây | > 10 phút |

---

## 9. PHÂN TÍCH RỦI RO & DỰ PHÒNG

| Rủi ro | Mức độ | Phương án dự phòng |
| :--- | :--- | :--- |
| Tài khoản ads bị khóa (TikTok/Meta) | 🔴 Cao | Đa dạng kênh + dự phòng nhiều BM; đẩy mạnh organic từ Agent 1 |
| Cổng thanh toán giữ tiền/khóa TK | 🟠 TB | Dùng song song SePay + PayOS; xác minh doanh nghiệp đầy đủ |
| Chi phí/chất lượng Gemini không ổn định | 🟠 TB | Cache prompt, giới hạn token, fallback model; QA mẫu báo cáo |
| Tỷ lệ chốt BE thấp hơn 5% | 🟠 TB | Kịch bản thận trọng (3%) vẫn LN ~386tr/tháng; tăng nurture Agent 4 |
| Năng lực Discovery Call (>100 deal) | 🟡 Thấp | Ủy quyền sales cấp cao; ghi VSL chốt thay một phần |
| Hoàn tiền/chargeback cao | 🟡 Thấp | Đảm bảo chất lượng PDF; chính sách hoàn tiền rõ ràng 30 ngày |
| Phụ thuộc nền tảng (Lovable/Make) | 🟡 Thấp | Tài liệu hóa kiến trúc; có phương án export/migrate |

---

## 10. GIẢ ĐỊNH & GHI CHÚ

1. CAC 300k/đơn là **ngân sách trần**; thực tế kỳ vọng thấp hơn nhờ traffic organic từ Agent 1 (chưa tính vào doanh thu để giữ thận trọng).
2. Tỷ lệ chốt BE 5% áp dụng cho khách FE; có độ trễ 2–4 tuần giữa mua FE và chốt BE (mô hình giả định cùng tháng để đơn giản hóa — thực tế dòng tiền BE trễ hơn FE khoảng 1 tháng ở giai đoạn đầu).
3. Chi phí vận hành BE 1tr/deal là ước tính thận trọng cho onboarding + support; bản thiết kế gốc đặt = 0.
4. Doanh thu từ các gói mid-tier (990k/2,9tr/9,9tr) **chưa** được cộng vào mô hình — đây là **dư địa tăng AOV** (upside) chưa khai thác.
5. Mọi con số là dự phóng, cần hiệu chỉnh theo dữ liệu thực 30 ngày đầu.

---

*Tài liệu này là bản kế hoạch sống — sẽ được cập nhật theo dữ liệu vận hành thực tế sau mỗi chu kỳ 30 ngày.*
