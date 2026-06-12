# ⚙️ SETUP — Cài đặt & chạy workflow N8N

> File workflow: [`lead-magnet-multichannel.workflow.json`](./lead-magnet-multichannel.workflow.json)
> Thời gian cài đặt lần đầu: **~20–30 phút**. Sau đó mỗi lần tạo mồi chỉ tốn **1 cú bấm**.

Workflow biến **1 chủ đề** thành: Ebook PDF + bộ ảnh carousel 1080×1080 + caption riêng từng kênh → **đăng đa kênh** (FB/IG/TikTok) → **đẩy lead vào Salekit** + gửi mồi & mở đường up-sell qua Email/ZNS Zalo OA.

---

## 0. Yêu cầu

| Hạng mục | Cần gì |
|---|---|
| **n8n** | Bản Cloud hoặc self-hosted (khuyến nghị ≥ 1.6x). Workflow dùng node lõi: Form Trigger, Set, Code, HTTP Request, Split Out, Aggregate. |
| **Claude (Anthropic)** | API key `sk-ant-...` tại [platform.claude.com](https://platform.claude.com) → *API Keys*. Model dùng: `claude-opus-4-8`. |
| **Render ảnh** | Tài khoản [htmlcsstoimage.com](https://htmlcsstoimage.com) (có gói free) → lấy **User ID** + **API Key**. |
| **Render PDF** | Tài khoản [apitemplate.io](https://apitemplate.io) → **API Key**. *(Có thể thay nhà cung cấp khác, xem §5.)* |
| **Đăng feed** | Tài khoản [ayrshare.com](https://www.ayrshare.com) (kết nối sẵn FB/IG/TikTok) → **API Key**. *(Hoặc thay bằng Meta Graph API / publisher khác.)* |
| **Salekit.io** | Tài khoản [salekit.io](https://salekit.io). Lấy **API Token** trong *Cấu hình → API*. Tài liệu: [help.salekit.io](https://help.salekit.io). |

> 💡 **Không bắt buộc đủ hết ngay.** Tất cả node ngoài Claude đã đặt `On Error = Continue`, nên bạn có thể test phần tạo mồi (Claude) trước, rồi bật dần render/đăng/Salekit.

---

## 1. Import workflow

1. Mở n8n → **Workflows → Import from File** → chọn `lead-magnet-multichannel.workflow.json`.
2. Bạn sẽ thấy 15 node nối thành chuỗi + 4 sticky note hướng dẫn theo 3 giai đoạn.
3. Một số node sẽ báo *"credential not set"* — bình thường, ta tạo ở bước 2.

---

## 2. Tạo 5 credential

Vào **Credentials → New**. Tạo đúng 5 cái sau (đặt tên y hệt để node tự nhận):

| # | Loại credential | Tên (đặt y hệt) | Cấu hình |
|---|---|---|---|
| 1 | **Header Auth** | `Anthropic x-api-key` | Name = `x-api-key` · Value = `sk-ant-...` |
| 2 | **Header Auth** | `Render API (X-API-KEY)` | Name = `X-API-KEY` · Value = API key APITemplate |
| 3 | **Basic Auth** | `Image API (hcti.io)` | User = *User ID* · Password = *API key* (htmlcsstoimage) |
| 4 | **Header Auth** | `Publisher Bearer (Ayrshare)` | Name = `Authorization` · Value = `Bearer xxxxx` |
| 5 | **Header Auth** | `Salekit Token` | Name = `Token` · Value = JWT token Salekit |

Sau khi tạo, mở từng node HTTP, ở mục *Credential* chọn đúng credential tương ứng (nếu chưa tự gán).

> Node dùng credential nào:
> - **4. Claude sinh moi** → `Anthropic x-api-key`
> - **6. Render Ebook PDF** → `Render API (X-API-KEY)`
> - **8. Slide to anh** → `Image API (hcti.io)`
> - **11. Dang da kenh (Publisher)** → `Publisher Bearer (Ayrshare)`
> - **12. Salekit - Audience** + **13. Salekit - Email/ZNS nurture** → `Salekit Token`

---

## 3. Sửa node **2. Cau hinh** (trung tâm điều khiển)

Đây là node DUY NHẤT chứa biến — học viên chỉ cần sửa ở đây.

| Biến | Ý nghĩa | Gợi ý |
|---|---|---|
| `chu_de`, `avatar`, `upsell`, `brand`, `funnel_url` | Tự lấy từ form. Có giá trị mặc định nếu form để trống. | Để nguyên. |
| `ANTHROPIC_MODEL` | Model Claude | `claude-opus-4-8` (giữ nguyên) |
| `PDF_ENDPOINT` | API render PDF | Mặc định APITemplate. Đổi nếu dùng nhà khác. |
| `IMAGE_ENDPOINT` | API render ảnh | Mặc định `https://hcti.io/v1/image` |
| `PUBLISHER_URL` | API đăng feed | Mặc định Ayrshare |
| `CHANNELS_FEED` | Kênh đăng feed | `['facebook','instagram','tiktok']` — thêm `'threads'` nếu Ayrshare của bạn bật. **Zalo OA không nằm ở đây** (do Salekit lo). |
| `SALEKIT_BASE` | Gốc API Salekit | `https://api.salekit.io/api/v1` |
| `test_lead_*` | Lead test để kiểm tra Salekit | Thay bằng email/sđt thật của bạn để nhận thử. |
| `c_cream/coral/forest/sun/ink` | Màu thương hiệu | Mặc định = bảng màu thunhap.vn. |

---

## 4. Test & Go-live

1. Bấm **Test workflow** (hoặc mở URL form ở node **1. Form**), điền **Chủ đề/nỗi đau** + Avatar → Submit.
2. Theo dõi từng node sáng xanh. Kết quả mong đợi:
   - Node **5**: ra JSON (ebook + carousel + caption_kenh) + `ebook_html`.
   - Node **6/8**: ra `download_url` (PDF) và các `url` ảnh.
   - Node **11**: Ayrshare trả `id`/status đăng bài.
   - Node **12**: Salekit trả audience đã tạo. Kiểm tra trong Salekit thấy lead + tag `leadmagnet:...`.
3. **Go-live:** bật toggle **Active** (góc trên). URL form trở thành Production — gửi cho học viên/cộng tác viên dùng.

### Cách test từng phần (khuyến nghị lần đầu)
- Tạm chỉ cần credential **Anthropic** → chạy tới node 5 xem nội dung mồi đã "đã" chưa, chỉnh prompt (node 3) nếu cần.
- Thêm credential render (2,3) → kiểm tra PDF/ảnh.
- Thêm publisher (4) + Salekit (5) → bật đăng + CRM.

---

## 5. Tuỳ biến nhà cung cấp (không khoá cứng)

Workflow cố tình **không khoá cứng** nhà cung cấp — chỉ cần đổi URL ở node **2. Cau hinh** + sửa credential:

- **PDF:** APITemplate (mặc định, body `{ body: "<html>" }`, trả `download_url`). Hoặc PDFShift/Gotenberg → đổi `PDF_ENDPOINT` và body ở node **6** cho khớp.
- **Ảnh:** htmlcsstoimage (mặc định, body `{ html, css }`, trả `url`). Hoặc Bannerbear/Placid/APITemplate.
- **Đăng feed:** Ayrshare (mặc định, body `{ post, platforms, mediaUrls }`). Hoặc Meta Graph API (FB/IG) + TikTok Content Posting API → tách thành node riêng từng kênh.
- **Salekit nurture (node 13):** URL `/send/email` là **template** — hãy mở [help.salekit.io](https://help.salekit.io) đối chiếu đúng *send-email-api* hoặc *api gửi ZNS qua Zalo OA*, rồi sửa URL + body ở node **13**. Node **12 (audience/create)** đã đúng chuẩn tài liệu Salekit.

---

## 6. Nối tiếp thành phễu hoàn chỉnh (gợi ý)

Workflow này là **"động cơ tạo mồi + đăng"**. Để khép kín phễu, ghép thêm 1 workflow thứ hai **"Opt-in → Nurture → Up-sell"**:

```
[Form trên thunhap.vn / Webhook Salekit khi có lead]
        → Salekit audience/create (gắn tag)
        → Gửi ebook tự động (Email/ZNS)
        → Chuỗi nurture 3–5 chạm
        → Khi đủ điểm: mời lên VIP 1-1 (up-sell)  →  Salekit order/automation
```

Node **12 (audience/create)** chính là cầu nối giữa hai workflow. Xem chi tiết trong [`../docs/SOP-thiet-ke-ebook-lead-magnet.md`](../docs/SOP-thiet-ke-ebook-lead-magnet.md) §7.

---

## 7. Lỗi thường gặp

| Triệu chứng | Nguyên nhân & cách xử lý |
|---|---|
| Node 4 báo 401 | Sai/thiếu credential `x-api-key`. Kiểm tra Name đúng là `x-api-key`. |
| Node 5 báo *"Claude khong tra ve JSON"* | Hiếm gặp. Mở node 4 xem `content` — thường do `max_tokens` quá thấp; tăng ở node **3** (`max_tokens`). |
| Node 6/8 lỗi nhưng workflow vẫn chạy | Đúng thiết kế (`On Error = Continue`). Kiểm tra credential render. |
| `node type ... not available` khi import | n8n quá cũ. Cập nhật n8n, hoặc thay **Form Trigger** bằng **Manual Trigger + Set** (giữ nguyên các biến). |
| Đăng feed lỗi kênh nào đó | Kênh chưa kết nối trong Ayrshare, hoặc TikTok cần duyệt nội dung. Bỏ kênh đó khỏi `CHANNELS_FEED`. |

---

## 8. Regenerate workflow (cho coach)

Muốn đổi prompt/biến mặc định rồi xuất lại JSON sạch:
```bash
cd pheu-lead-magnet/n8n
python3 _build_workflow.py   # ghi đè lead-magnet-multichannel.workflow.json
```
Sửa prompt trong `_build_workflow.py` (biến `build_prompt_js`) hoặc trong [`../docs/prompts/claude-lead-magnet.prompt.md`](../docs/prompts/claude-lead-magnet.prompt.md) rồi đồng bộ.
