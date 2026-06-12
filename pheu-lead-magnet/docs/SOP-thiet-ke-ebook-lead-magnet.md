# 📘 SOP — Quy trình thiết kế Ebook / Ấn phẩm số làm Lead Magnet

> **Dành cho:** Coach & học viên Khoá học "Xây dựng hệ thống thu hút khách hàng bằng AI" (Phễu) — kết hợp UNICA.
> **Mục tiêu:** Biến kiến thức của bạn thành **sản phẩm mồi** (ebook / ấn phẩm số / bộ ảnh đăng hàng loạt) khiến người lạ **tự nguyện để lại thông tin**, đổ traffic vào đầu phễu, rồi mở đường **up-sell** sản phẩm/dịch vụ phía sau.
> **Cặp đôi vận hành:** SOP này (tư duy + công thức) ⟷ Workflow N8N (`../n8n/`) tự động hoá toàn bộ khâu sản xuất & phân phối.

---

## 0. Lead Magnet là gì & vì sao nó là "trái tim" của phễu

Phễu (funnel) đơn giản là hành trình: **Người lạ → Lead → Khách hàng → Khách trung thành.**

```
   TRAFFIC (lạ)         ĐẦU PHỄU            THÂN PHỄU           ĐÁY PHỄU
   FB/IG/TikTok   →   LEAD MAGNET    →    NURTURE/CHĂM SÓC  →  BÁN & UP-SELL
   (ảnh carousel)     (ebook miễn phí)    (email/ZNS Zalo)     (khoá VIP 1-1)
        │                  │                    │                   │
   hút chú ý         đổi info lấy quà      xây niềm tin        chốt doanh thu
```

Lead Magnet là **điểm đánh đổi**: bạn cho đi một giá trị nhỏ — nhanh, cụ thể, miễn phí — để đổi lấy **thông tin liên hệ** (email/SĐT/Zalo). Mồi tốt = phễu đầy. Mồi dở = mọi thứ phía sau chết khát.

**3 tiêu chí của một mồi "cắn câu":**
1. **Cụ thể** — giải đúng 1 nỗi đau, không ôm đồm. ("7 prompt AI viết bài bán hàng" > "Tổng quan về AI").
2. **Nhanh** — người ta thấy kết quả/giá trị trong < 15 phút đọc.
3. **Dẫn lối** — kết thúc bằng bước tiếp theo tự nhiên hướng về sản phẩm trả phí.

---

## 1. Hai định dạng mồi ta sản xuất

| Định dạng | Vai trò trong phễu | Workflow tạo bằng |
|---|---|---|
| **Ebook / Ấn phẩm số (PDF)** | Quà tặng tải về để **đổi lấy info** (đầu phễu). Là "thỏi nam châm" đặt sau form opt-in. | Node 5 → 6 (HTML → PDF) |
| **Bộ ảnh Carousel (đăng hàng loạt)** | Nội dung **hút traffic mới** trên feed FB/IG/TikTok, dẫn về form tải ebook. | Node 5 → 7 → 8 (HTML → ảnh 1080×1080) |

> Hai định dạng này **đi cùng nhau**: carousel kéo người lạ → click → tải ebook (để lại info) → vào phễu. Workflow tạo **cả hai trong một lần bấm**.

---

## 2. Khung 7 bước thiết kế mồi (CORE)

Đây là quy trình tư duy. Workflow đã "đóng băng" khung này vào prompt của Claude (node 3) — nhưng học viên PHẢI hiểu để biết chỉnh.

> Nhớ bằng cụm: **A · P · P · P · C** + 2 bước hậu kỳ → **AVATAR → PAIN → PROMISE → PROOF → PACKAGE → PUBLISH → PROFIT**

| Bước | Tên | Câu hỏi cốt lõi | Đầu ra |
|---|---|---|---|
| 1 | **Avatar** | Mồi cho ai? Họ 1 ngày trông như thế nào? | Chân dung 1 dòng |
| 2 | **Pain** | Nỗi đau số 1 đang khiến họ mất ngủ là gì? | 1 câu nỗi đau |
| 3 | **Promise** | Sau khi dùng mồi, họ đạt được kết quả **cụ thể** gì, **nhanh** thế nào? | Lời hứa trang bìa |
| 4 | **Proof** | Vì sao tin được bạn? (case, con số, kinh nghiệm) | Bằng chứng |
| 5 | **Package** | Đóng gói thành ebook (5–7 chương) + carousel (7 slide) | Bản thảo |
| 6 | **Publish** | Đăng đa kênh + đặt sau form opt-in | Bài đăng + landing |
| 7 | **Profit** | Câu chuyển tiếp lên sản phẩm trả phí | Cầu nối up-sell |

Trong workflow, bước 1–4 nằm ở field `meta` của JSON Claude trả về; bước 5 ở `ebook`+`carousel`; bước 6 ở `caption_kenh` + node đăng; bước 7 ở `meta.cau_noi_upsell` + node Salekit nurture.

---

## 3. Giải phẫu một EBOOK mồi (cấu trúc 5–7 chương)

Prompt đã ép Claude theo bộ khung dưới đây. Đây là "công thức vàng" — dạy học viên ghi nhớ:

1. **Trang bìa** — Tiêu đề giật (đúng sự thật) + phụ đề + lời hứa. *Không* sến, *không* hứa lố.
2. **Chương 1 — Gọi tên nỗi đau:** khiến người đọc gật gù "đúng là mình".
3. **Chương 2 — Vì sao cách cũ thất bại:** phá niềm tin sai, dọn đường cho cách mới.
4. **Chương 3–5 — Giải pháp từng bước:** mỗi chương 1 ý, có **bước hành động làm ngay** (checklist, prompt mẫu, template).
5. **Chương cuối — Bức tranh sau khi áp dụng:** vẽ tương lai + lý do nên đi tiếp cùng bạn.
6. **CTA cuối:** 1 hành động duy nhất → về đầu phễu (`funnel_url`).

**Quy tắc viết:** mỗi chương 120–220 từ, văn nói, ví dụ Việt Nam, in đậm ý chính, tránh "lý thuyết hàn lâm". (Đây chính là các ràng buộc trong prompt node 3.)

---

## 4. Giải phẫu bộ CAROUSEL (7 slide đăng hàng loạt)

| Slide | Vai trò | Nguyên tắc |
|---|---|---|
| 1 | **Hook** — chặn ngón tay | Câu gây sốc/tò mò ≤ 8 từ, nền màu nổi (coral). |
| 2–6 | **Giá trị** | Mỗi slide 1 ý, tiêu đề ≤ 8 từ, nội dung ≤ 40 từ. |
| 7 | **CTA** | "Tải trọn bộ ebook miễn phí tại…" → `funnel_url`. |

Workflow render mỗi slide thành ảnh 1080×1080 theo màu thương hiệu (node 7b + 8), kèm `caption` + `hashtags`. Sau đó node 11 đăng lên FB/IG/TikTok.

**Vì sao carousel hút traffic?** Thuật toán ưu tiên nội dung giữ người xem lâu (vuốt nhiều slide) → reach tự nhiên cao → traffic miễn phí vào đầu phễu. Đây là cách "tiếp cận tối đa nguồn traffic" mà không tốn ngân sách quảng cáo.

---

## 5. Caption riêng từng kênh (đừng copy–paste 1 nội dung)

Mỗi nền tảng có "giọng" khác nhau — prompt đã yêu cầu Claude viết riêng (`caption_kenh`):

| Kênh | Giọng | Do ai đăng |
|---|---|---|
| **Facebook** | Kể chuyện + CTA rõ | Publisher (node 11) |
| **Instagram** | Ngắn + emoji + hashtag | Publisher (node 11) |
| **TikTok** | Hook 3 giây đầu (lời thoại) | Publisher (node 11) |
| **Threads** | Đối thoại, khơi tranh luận | Publisher (bật trong `CHANNELS_FEED`) |
| **Zalo OA** | Tin chăm sóc lịch sự + link tải | **Salekit** (node 13) — kênh sở hữu |

> **Phân vai rõ:** *Feed công khai* (FB/IG/TikTok) = hút **traffic mới** → Ayrshare. *Kênh sở hữu* (Zalo OA/Email/SMS) = chăm sóc **lead đã có** + up-sell → Salekit.

---

## 6. Vì sao kết hợp Claude + N8N + Salekit (kiến trúc)

| Thành phần | Vai trò | "Cơ bắp" |
|---|---|---|
| **Claude (`claude-opus-4-8`)** | Bộ não sáng tạo: nghĩ mồi, viết ebook + carousel + caption đúng công thức phễu. | `output_config.format` ép ra JSON sạch để máy xử lý. |
| **N8N** | Dây chuyền tự động: nối Claude ↔ render ↔ đăng ↔ CRM, chạy 1 cú bấm. | Node lõi, không cần code. |
| **Salekit.io** | Trung tâm CRM & chăm sóc đa kênh sở hữu: thu lead, gắn tag, automation nurture, lên đơn up-sell. | `audience/create`, ZNS Zalo OA, Email/SMS. |

> **"Claude code" trong khoá học:** ở khâu *xây dựng* (build), coach có thể dùng **Claude Code (CLI)** để sinh/chỉnh chính workflow & prompt (regenerate qua `_build_workflow.py`). Ở khâu *vận hành* (runtime), workflow gọi **Claude API**. Cùng một bộ não, hai vai.

---

## 7. Khép kín phễu: từ mồi tới up-sell

Workflow trong gói là **động cơ tạo mồi + đăng**. Phễu hoàn chỉnh ghép thêm nhánh nurture (xây bằng N8N + Salekit):

```
CAROUSEL (FB/IG/TikTok)  ──click──▶  Landing thunhap.vn (form opt-in)
                                          │ để lại email/SĐT
                                          ▼
                         Salekit  audience/create  (gắn tag chiến dịch)   ◀── node 12
                                          │ kích hoạt automation
                                          ▼
                         Gửi EBOOK tự động (Email/ZNS Zalo OA)            ◀── node 13
                                          │
                                          ▼
                         Chuỗi NURTURE 3–5 chạm (giá trị → niềm tin)
                                          │ đủ điểm quan tâm
                                          ▼
                         UP-SELL: mời lên "Khoá VIP 1-1"  (cau_noi_upsell)
                                          │
                                          ▼
                         Salekit order / chốt đơn  →  doanh thu
```

**Cầu nối kỹ thuật:** node 12 (`audience/create`) đẩy lead vào Salekit kèm `tag = leadmagnet:<tiêu đề ebook>` → Salekit tự chạy kịch bản automation tương ứng. Coach dựng kịch bản nurture/up-sell ngay trong giao diện Salekit (segment theo tag).

**Thang giá trị (Value Ladder) gợi ý cho thunhap.vn:**
`Ebook miễn phí` → `Mini-course/Bài test Thu Nhập AI` → `Khoá Phễu (UNICA)` → `VIP 1-1 với Alan Tú`.

---

## 8. Bản đồ sang các buổi học (gắn với UNICA)

| Buổi | Nội dung dạy | Thực hành trên workflow |
|---|---|---|
| **B1 — Tư duy phễu & mồi** | §0–§2 SOP: phễu, 3 tiêu chí mồi, khung A·P·P·P·C | Vẽ avatar + nỗi đau của chính học viên |
| **B2 — Sản xuất mồi bằng AI** | §3–§4: giải phẫu ebook & carousel | Bấm form → đọc JSON Claude → chỉnh prompt node 3 |
| **B3 — Render & thương hiệu hoá** | Thiết kế nhất quán, màu, font | Cấu hình render PDF/ảnh, đổi màu node 2 |
| **B4 — Đăng đa kênh** | §5: caption từng kênh, lịch đăng | Bật publisher, đăng thử FB/IG/TikTok |
| **B5 — CRM & Nurture (Salekit)** | §7: tag, automation, kênh sở hữu | Nối node 12/13, dựng kịch bản Salekit |
| **B6 — Up-sell & Value Ladder** | §7: thang giá trị, câu chuyển tiếp | Thiết kế offer VIP 1-1, đo lường |

---

## 9. Chỉ số đo lường (KPI phễu)

| Tầng | Chỉ số | Mục tiêu khởi điểm |
|---|---|---|
| Traffic | Reach/lượt xem carousel mỗi tuần | Tăng đều theo tần suất đăng |
| Đầu phễu | **Tỷ lệ opt-in** (xem trang → để lại info) | 20–40% |
| Thân phễu | Tỷ lệ mở Email/ZNS, tỷ lệ click | Email mở > 30%, ZNS đọc cao |
| Đáy phễu | **Tỷ lệ lên VIP** (lead → khách trả phí) | 1–5% tuỳ offer |

> Đo bằng tag + trạng thái trong Salekit; với traffic feed dùng số liệu Ayrshare/nền tảng.

---

## 10. Checklist trước khi đăng (in dán tường)

- [ ] Mồi giải đúng **1** nỗi đau cụ thể của avatar?
- [ ] Lời hứa có **kết quả + thời gian** rõ ràng, không hứa lố?
- [ ] Ebook có **bước hành động làm ngay** ở mỗi chương?
- [ ] Slide 1 carousel có **hook chặn ngón tay**?
- [ ] **CTA** ở cả ebook lẫn slide cuối đều trỏ về `funnel_url`?
- [ ] Có **câu chuyển tiếp up-sell** tự nhiên (không lộ liễu)?
- [ ] Lead sẽ rơi vào **đúng tag/automation** trong Salekit?

---

### Phụ lục — Prompt sản xuất mồi
Toàn văn prompt (system + user) Claude dùng để sinh mồi nằm ở [`prompts/claude-lead-magnet.prompt.md`](./prompts/claude-lead-magnet.prompt.md). Đây cũng là phần học viên được phép tinh chỉnh nhiều nhất để "ra chất" riêng.
