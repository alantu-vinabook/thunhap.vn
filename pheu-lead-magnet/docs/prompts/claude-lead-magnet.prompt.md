# 🧠 Prompt sản xuất Lead Magnet (Claude `claude-opus-4-8`)

> Đây là bản tách riêng để dễ đọc & tinh chỉnh. Nó **đồng bộ** với prompt nhúng trong node **3. Build prompt Claude** của workflow (`../../n8n/_build_workflow.py` → biến `build_prompt_js`). Sửa ở đâu thì nhớ đồng bộ chỗ kia (hoặc chạy lại builder).

Workflow gọi Claude với **structured outputs** (`output_config.format`) nên đầu ra luôn là JSON đúng khuôn — các node sau parse được ngay, không cần "đoán".

---

## Tham số API (node 4)

```jsonc
{
  "model": "claude-opus-4-8",
  "max_tokens": 16000,
  "thinking": { "type": "adaptive" },
  "output_config": {
    "effort": "high",
    "format": { "type": "json_schema", "schema": { /* xem dưới */ } }
  },
  "system": "<SYSTEM PROMPT>",
  "messages": [{ "role": "user", "content": "<USER PROMPT>" }]
}
```
Header: `x-api-key: sk-ant-...`, `anthropic-version: 2023-06-01`, `content-type: application/json`.

---

## SYSTEM PROMPT

```
Bạn là chuyên gia thiết kế phễu (funnel) và copywriter direct-response người Việt,
chuyên tạo SẢN PHẨM MỒI (lead magnet) chuyển đổi cao cho coach/doanh nghiệp nhỏ.
Nguyên tắc: bám đúng nỗi đau của avatar, hứa 1 kết quả CỤ THỂ & nhanh, cho giá trị thật,
không lý thuyết suông, dùng ví dụ Việt Nam, văn phong gần gũi nhưng sắc bén.
Mọi nội dung phải dẫn người đọc về đầu phễu rồi mở đường cho up-sell một cách tự nhiên.
Trả về DUY NHẤT JSON đúng schema, viết hoàn toàn bằng tiếng Việt có dấu.
```

## USER PROMPT (các biến `${...}` lấy từ node 2. Cau hinh)

```
Hãy tạo MỘT bộ sản phẩm mồi hoàn chỉnh dựa trên thông tin sau:

- Chủ đề / nỗi đau: ${chu_de}
- Avatar khách hàng: ${avatar}
- Thương hiệu: ${brand}
- Sản phẩm/dịch vụ up-sell: ${upsell}
- Link đầu phễu (CTA): ${funnel_url}

YÊU CẦU CHI TIẾT:
1) meta: chốt lại avatar, noi_dau (1 câu), loi_hua (1 câu, kết quả cụ thể), bang_chung
   (lý do tin được), cau_noi_upsell (câu chuyển tiếp sang ${upsell}).
2) ebook (ấn phẩm số): tiêu đề giật nhưng đúng sự thật, phụ đề, lời hứa trang bìa,
   5-7 chương. Mỗi chương noi_dung_md viết bằng Markdown (dùng ## tiêu đề phụ, '- ' gạch đầu dòng,
   **in đậm**), 120-220 từ, có bước hành động làm được ngay. Kết bằng cta dẫn về ${funnel_url}.
3) carousel: 7 slide đăng mạng xã hội. Slide 1 = hook chặn ngón tay; 5 slide giá trị (mỗi slide 1 ý,
   tieu_de <= 8 từ, noi_dung <= 40 từ); slide cuối = CTA về phễu. Mỗi slide có ghi_chu_hinh_anh
   gợi ý hình. Kèm caption tổng và 8-12 hashtags tiếng Việt + tiếng Anh không dấu '#'.
4) caption_kenh: viết caption RIÊNG, đúng văn phong từng kênh: facebook (kể chuyện, có CTA),
   zalo_oa (tin nhắn chăm sóc ngắn gọn lịch sự, có link tải), tiktok (lời thoại hook 3 giây đầu),
   instagram (ngắn + emoji + hashtag), threads (đối thoại, khơi tranh luận).
Chỉ trả về JSON đúng schema, không thêm lời dẫn.
```

---

## JSON Schema (ép cấu trúc đầu ra)

```json
{
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "meta": {
      "type": "object", "additionalProperties": false,
      "properties": {
        "avatar": { "type": "string" },
        "noi_dau": { "type": "string" },
        "loi_hua": { "type": "string" },
        "bang_chung": { "type": "string" },
        "cau_noi_upsell": { "type": "string" }
      },
      "required": ["avatar","noi_dau","loi_hua","bang_chung","cau_noi_upsell"]
    },
    "ebook": {
      "type": "object", "additionalProperties": false,
      "properties": {
        "tieu_de": { "type": "string" },
        "phu_de": { "type": "string" },
        "loi_hua_trang_bia": { "type": "string" },
        "chuong": {
          "type": "array",
          "items": {
            "type": "object", "additionalProperties": false,
            "properties": { "tieu_de": { "type": "string" }, "noi_dung_md": { "type": "string" } },
            "required": ["tieu_de","noi_dung_md"]
          }
        },
        "cta": { "type": "string" }
      },
      "required": ["tieu_de","phu_de","loi_hua_trang_bia","chuong","cta"]
    },
    "carousel": {
      "type": "object", "additionalProperties": false,
      "properties": {
        "slides": {
          "type": "array",
          "items": {
            "type": "object", "additionalProperties": false,
            "properties": {
              "so_thu_tu": { "type": "integer" },
              "tieu_de": { "type": "string" },
              "noi_dung": { "type": "string" },
              "ghi_chu_hinh_anh": { "type": "string" }
            },
            "required": ["so_thu_tu","tieu_de","noi_dung","ghi_chu_hinh_anh"]
          }
        },
        "caption": { "type": "string" },
        "hashtags": { "type": "array", "items": { "type": "string" } }
      },
      "required": ["slides","caption","hashtags"]
    },
    "caption_kenh": {
      "type": "object", "additionalProperties": false,
      "properties": {
        "facebook": { "type": "string" },
        "zalo_oa": { "type": "string" },
        "tiktok": { "type": "string" },
        "instagram": { "type": "string" },
        "threads": { "type": "string" }
      },
      "required": ["facebook","zalo_oa","tiktok","instagram","threads"]
    }
  },
  "required": ["meta","ebook","carousel","caption_kenh"]
}
```

---

## Mẹo tinh chỉnh prompt (cho học viên)

- **Đổi "giọng":** sửa câu cuối SYSTEM, ví dụ thêm *"văn phong truyền cảm hứng, ít từ chuyên môn"*.
- **Đổi độ dài ebook:** sửa "5-7 chương" và "120-220 từ" trong USER.
- **Thêm ràng buộc thương hiệu:** thêm dòng *"Luôn nhắc tới phương pháp [TÊN] của ${brand}"*.
- **Đổi số slide carousel:** sửa "7 slide" (nhớ render vẫn tự động theo số slide thực tế).
- **Thêm kênh caption:** thêm key vào `caption_kenh` (schema) + yêu cầu trong USER.

> Lưu ý structured outputs: schema **không** hỗ trợ `minLength`/`maxLength`/`minimum`… nên ràng buộc độ dài đặt trong câu chữ USER prompt, không đặt trong schema.

> Model: luôn dùng `claude-opus-4-8` (mặc định). Chỉ đổi khi bạn có lý do rõ ràng.
