# -*- coding: utf-8 -*-
"""
Builder cho workflow N8N: "Phễu Lead Magnet — Claude + Salekit.io".
Chạy:  python3 _build_workflow.py
Sinh ra: lead-magnet-multichannel.workflow.json (import thẳng vào n8n).

Vì sao dùng builder thay vì viết tay JSON?
- Các node Code chứa JS dài, nhiều ký tự đặc biệt; json.dumps() sẽ escape chuẩn 100%.
- Coach/học viên có thể sửa prompt/biến tại đây rồi build lại, luôn ra JSON hợp lệ.
"""
import json

# ------------------------------------------------------------------ helpers
def node(nid, name, ntype, ver, pos, params, creds=None, extra=None):
    n = {
        "id": nid,
        "name": name,
        "type": ntype,
        "typeVersion": ver,
        "position": pos,
        "parameters": params,
    }
    if creds:
        n["credentials"] = creds
    if extra:
        n.update(extra)
    return n

def http(nid, name, pos, url, json_body_expr, auth=None, header_params=None,
         creds=None, timeout=120000, notes=None):
    params = {
        "method": "POST",
        "url": url,
        "sendBody": True,
        "specifyBody": "json",
        "jsonBody": json_body_expr,
        "options": {"timeout": timeout},
    }
    if auth:
        params["authentication"] = "genericCredentialType"
        params["genericAuthType"] = auth
    if header_params is not None:
        params["sendHeaders"] = True
        params["headerParameters"] = {"parameters": header_params}
    extra = {"onError": "continueRegularOutput"}
    if notes:
        extra["notes"] = notes
        extra["notesInFlow"] = True
    return node(nid, name, "n8n-nodes-base.httpRequest", 4.2, pos, params, creds, extra)

def sticky(nid, pos, w, h, content, color=7):
    return node(nid, "note", "n8n-nodes-base.stickyNote", 1, pos,
                {"content": content, "height": h, "width": w, "color": color})

CFG = "$('2. Cau hinh').first().json"   # short alias used in expressions

# ------------------------------------------------------------------ 1. FORM
form_params = {
    "formTitle": "Tạo sản phẩm mồi (Lead Magnet) bằng AI",
    "formDescription": "Nhập chủ đề/nỗi đau → hệ thống dùng Claude sinh Ebook + Carousel + caption, render ảnh/PDF, rồi đăng đa kênh và đẩy lead vào Salekit. Mẹo: mô tả càng cụ thể nỗi đau & avatar, mồi càng 'cắn câu'.",
    "formFields": {"values": [
        {"fieldLabel": "Chu de hoac noi dau", "fieldType": "text", "requiredField": True,
         "placeholder": "VD: Người đi làm muốn dùng AI tăng thu nhập nhưng không biết bắt đầu từ đâu"},
        {"fieldLabel": "Avatar khach hang", "fieldType": "text",
         "placeholder": "VD: Nhân viên văn phòng 25-40 tuổi, bận, muốn thu nhập 2-5 lần"},
        {"fieldLabel": "San pham up-sell", "fieldType": "text",
         "placeholder": "VD: Khoá VIP 1-1 cùng Alan Tú"},
        {"fieldLabel": "Thuong hieu", "fieldType": "text", "placeholder": "Thu Nhập AI"},
        {"fieldLabel": "Link pheu", "fieldType": "text", "placeholder": "https://thunhap.vn"},
    ]},
    "options": {},
}
n1 = node("n1", "1. Form chu de & avatar", "n8n-nodes-base.formTrigger", 2.2,
          [-360, 300], form_params, extra={"webhookId": "pheu-lead-magnet-form-01"})

# ------------------------------------------------------------------ 2. CONFIG (Set)
def asg(name, value, typ="string"):
    return {"id": "a-" + name, "name": name, "value": value, "type": typ}

set_assignments = [
    asg("chu_de", "={{ $json['Chu de hoac noi dau'] }}"),
    asg("avatar", "={{ $json['Avatar khach hang'] || 'Người đi làm 25-40 tuổi, muốn dùng AI để tăng thu nhập 2-5 lần' }}"),
    asg("upsell", "={{ $json['San pham up-sell'] || 'Khoá VIP 1-1 cùng Alan Tú' }}"),
    asg("brand", "={{ $json['Thuong hieu'] || 'Thu Nhập AI' }}"),
    asg("funnel_url", "={{ $json['Link pheu'] || 'https://thunhap.vn' }}"),
    # --- Claude ---
    asg("ANTHROPIC_URL", "https://api.anthropic.com/v1/messages"),
    asg("ANTHROPIC_MODEL", "claude-opus-4-8"),
    asg("ANTHROPIC_VERSION", "2023-06-01"),
    # --- Render ---
    asg("PDF_ENDPOINT", "https://rest.apitemplate.io/v2/create-pdf-from-html"),
    asg("IMAGE_ENDPOINT", "https://hcti.io/v1/image"),
    # --- Publisher (đăng feed đa kênh) ---
    asg("PUBLISHER_URL", "https://api.ayrshare.com/api/post"),
    asg("CHANNELS_FEED", "={{ ['facebook','instagram','tiktok'] }}", "array"),
    # --- Salekit ---
    asg("SALEKIT_BASE", "https://api.salekit.io/api/v1"),
    # --- Lead test (để test kết nối Salekit; thay bằng lead thật khi chạy production) ---
    asg("test_lead_name", "Khach test"),
    asg("test_lead_email", "test@example.com"),
    asg("test_lead_phone", "0900000000"),
    # --- Màu thương hiệu (đồng bộ thunhap.vn) ---
    asg("c_cream", "#FFF8EE"),
    asg("c_coral", "#FF5B4E"),
    asg("c_forest", "#1F4B36"),
    asg("c_sun", "#FFC043"),
    asg("c_ink", "#1A1510"),
]
n2 = node("n2", "2. Cau hinh", "n8n-nodes-base.set", 3.4, [-140, 300],
          {"assignments": {"assignments": set_assignments}, "options": {}})

# ------------------------------------------------------------------ 3. BUILD PROMPT (Code)
build_prompt_js = r"""
// Dựng request body cho Claude API (structured outputs).
// Sửa SYSTEM / USER ở đây để đổi "giọng" và công thức mồi.
const cfg = $json; // đến từ node "2. Cau hinh"

const schema = {
  type: "object", additionalProperties: false,
  properties: {
    meta: { type: "object", additionalProperties: false,
      properties: {
        avatar: { type: "string" },
        noi_dau: { type: "string" },
        loi_hua: { type: "string" },
        bang_chung: { type: "string" },
        cau_noi_upsell: { type: "string" }
      },
      required: ["avatar","noi_dau","loi_hua","bang_chung","cau_noi_upsell"] },
    ebook: { type: "object", additionalProperties: false,
      properties: {
        tieu_de: { type: "string" },
        phu_de: { type: "string" },
        loi_hua_trang_bia: { type: "string" },
        chuong: { type: "array", items: { type: "object", additionalProperties: false,
          properties: { tieu_de: { type: "string" }, noi_dung_md: { type: "string" } },
          required: ["tieu_de","noi_dung_md"] } },
        cta: { type: "string" }
      },
      required: ["tieu_de","phu_de","loi_hua_trang_bia","chuong","cta"] },
    carousel: { type: "object", additionalProperties: false,
      properties: {
        slides: { type: "array", items: { type: "object", additionalProperties: false,
          properties: {
            so_thu_tu: { type: "integer" },
            tieu_de: { type: "string" },
            noi_dung: { type: "string" },
            ghi_chu_hinh_anh: { type: "string" }
          },
          required: ["so_thu_tu","tieu_de","noi_dung","ghi_chu_hinh_anh"] } },
        caption: { type: "string" },
        hashtags: { type: "array", items: { type: "string" } }
      },
      required: ["slides","caption","hashtags"] },
    caption_kenh: { type: "object", additionalProperties: false,
      properties: {
        facebook: { type: "string" },
        zalo_oa: { type: "string" },
        tiktok: { type: "string" },
        instagram: { type: "string" },
        threads: { type: "string" }
      },
      required: ["facebook","zalo_oa","tiktok","instagram","threads"] }
  },
  required: ["meta","ebook","carousel","caption_kenh"]
};

const SYSTEM = [
  "Bạn là chuyên gia thiết kế phễu (funnel) và copywriter direct-response người Việt,",
  "chuyên tạo SẢN PHẨM MỒI (lead magnet) chuyển đổi cao cho coach/doanh nghiệp nhỏ.",
  "Nguyên tắc: bám đúng nỗi đau của avatar, hứa 1 kết quả CỤ THỂ & nhanh, cho giá trị thật,",
  "không lý thuyết suông, dùng ví dụ Việt Nam, văn phong gần gũi nhưng sắc bén.",
  "Mọi nội dung phải dẫn người đọc về đầu phễu rồi mở đường cho up-sell một cách tự nhiên.",
  "Trả về DUY NHẤT JSON đúng schema, viết hoàn toàn bằng tiếng Việt có dấu."
].join(" ");

const USER = [
  "Hãy tạo MỘT bộ sản phẩm mồi hoàn chỉnh dựa trên thông tin sau:",
  "",
  "- Chủ đề / nỗi đau: " + cfg.chu_de,
  "- Avatar khách hàng: " + cfg.avatar,
  "- Thương hiệu: " + cfg.brand,
  "- Sản phẩm/dịch vụ up-sell: " + cfg.upsell,
  "- Link đầu phễu (CTA): " + cfg.funnel_url,
  "",
  "YÊU CẦU CHI TIẾT:",
  "1) meta: chốt lại avatar, noi_dau (1 câu), loi_hua (1 câu, kết quả cụ thể), bang_chung",
  "   (lý do tin được), cau_noi_upsell (câu chuyển tiếp sang " + cfg.upsell + ").",
  "2) ebook (ấn phẩm số): tiêu đề giật nhưng đúng sự thật, phụ đề, lời hứa trang bìa,",
  "   5-7 chương. Mỗi chương noi_dung_md viết bằng Markdown (dùng ## tiêu đề phụ, '- ' gạch đầu dòng,",
  "   **in đậm**), 120-220 từ, có bước hành động làm được ngay. Kết bằng cta dẫn về " + cfg.funnel_url + ".",
  "3) carousel: 7 slide đăng mạng xã hội. Slide 1 = hook chặn ngón tay; 5 slide giá trị (mỗi slide 1 ý,",
  "   tieu_de <= 8 từ, noi_dung <= 40 từ); slide cuối = CTA về phễu. Mỗi slide có ghi_chu_hinh_anh",
  "   gợi ý hình. Kèm caption tổng và 8-12 hashtags tiếng Việt + tiếng Anh không dấu '#'.",
  "4) caption_kenh: viết caption RIÊNG, đúng văn phong từng kênh: facebook (kể chuyện, có CTA),",
  "   zalo_oa (tin nhắn chăm sóc ngắn gọn lịch sự, có link tải), tiktok (lời thoại hook 3 giây đầu),",
  "   instagram (ngắn + emoji + hashtag), threads (đối thoại, khơi tranh luận).",
  "Chỉ trả về JSON đúng schema, không thêm lời dẫn."
].join("\n");

const body = {
  model: cfg.ANTHROPIC_MODEL,
  max_tokens: 16000,
  thinking: { type: "adaptive" },
  output_config: { effort: "high", format: { type: "json_schema", schema: schema } },
  system: SYSTEM,
  messages: [{ role: "user", content: USER }]
};

return [{ json: { body } }];
""".strip("\n")
n3 = node("n3", "3. Build prompt Claude", "n8n-nodes-base.code", 2, [80, 300],
          {"jsCode": build_prompt_js})

# ------------------------------------------------------------------ 4. CLAUDE (HTTP)
n4 = http(
    "n4", "4. Claude sinh moi", [300, 300],
    url="={{ %s.ANTHROPIC_URL }}" % CFG,
    json_body_expr="={{ JSON.stringify($json.body) }}",
    auth="httpHeaderAuth",
    header_params=[
        {"name": "anthropic-version", "value": "={{ %s.ANTHROPIC_VERSION }}" % CFG},
        {"name": "content-type", "value": "application/json"},
    ],
    creds={"httpHeaderAuth": {"id": "cred-anthropic", "name": "Anthropic x-api-key"}},
    timeout=300000,
    notes="Credential Header Auth: Name = x-api-key, Value = sk-ant-... (API key Anthropic)",
)

# ------------------------------------------------------------------ 5. PARSE (Code)
parse_js = r"""
// Bóc JSON Claude trả về + dựng HTML cho ebook (theo màu thương hiệu thunhap.vn).
const cfg = $('2. Cau hinh').first().json;
const r = $input.first().json;

let txt = '';
for (const b of (r.content || [])) { if (b.type === 'text') txt += b.text; }
txt = (txt || '').trim().replace(/^```(json)?/i, '').replace(/```$/,'').trim();

let data;
try { data = JSON.parse(txt); }
catch (e) { throw new Error('Claude khong tra ve JSON hop le. Raw: ' + txt.slice(0, 400)); }

function esc(s){ return String(s==null?'':s)
  .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
function inline(s){ return esc(s).replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>'); }
function mdToHtml(md){
  const lines = String(md||'').split(/\r?\n/); let html=''; let ul=false;
  for (const raw of lines){ const line = raw.trim();
    if(!line){ if(ul){html+='</ul>';ul=false;} continue; }
    if(/^- /.test(line)){ if(!ul){html+='<ul>';ul=true;} html+='<li>'+inline(line.slice(2))+'</li>'; continue; }
    if(/^### /.test(line)){ if(ul){html+='</ul>';ul=false;} html+='<h3>'+inline(line.slice(4))+'</h3>'; continue; }
    if(/^## /.test(line)){ if(ul){html+='</ul>';ul=false;} html+='<h2>'+inline(line.slice(3))+'</h2>'; continue; }
    if(ul){html+='</ul>';ul=false;}
    html += '<p>'+inline(line)+'</p>';
  }
  if(ul) html+='</ul>';
  return html;
}

const eb = data.ebook;
const chapters = (eb.chuong||[]).map((c,i) =>
  '<section class="ch"><h2><span class="num">'+(i+1)+'</span>'+esc(c.tieu_de)+'</h2>'
  + mdToHtml(c.noi_dung_md) + '</section>').join('\n');

const ebook_html =
'<!doctype html><html lang="vi"><head><meta charset="utf-8">'
+ '<style>'
+ '*{box-sizing:border-box;font-family:"DM Sans",Arial,Helvetica,sans-serif}'
+ 'body{margin:0;color:'+cfg.c_ink+';background:'+cfg.c_cream+'}'
+ '.cover{background:'+cfg.c_forest+';color:'+cfg.c_cream+';padding:90px 64px;}'
+ '.cover .badge{display:inline-block;background:'+cfg.c_sun+';color:'+cfg.c_ink+';font-weight:800;padding:6px 14px;border-radius:999px;font-size:14px;letter-spacing:.5px}'
+ '.cover h1{font-size:46px;line-height:1.1;margin:22px 0 10px;font-weight:900}'
+ '.cover h2{font-size:22px;font-weight:600;color:'+cfg.c_sun+';margin:0 0 22px}'
+ '.cover p{font-size:18px;max-width:640px;opacity:.95}'
+ '.cover .brand{margin-top:40px;font-weight:700;opacity:.9}'
+ '.wrap{padding:54px 64px}'
+ '.ch{margin-bottom:30px;page-break-inside:avoid}'
+ '.ch h2{color:'+cfg.c_forest+';font-size:26px;display:flex;align-items:center;gap:12px}'
+ '.ch h2 .num{background:'+cfg.c_coral+';color:#fff;width:38px;height:38px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:18px}'
+ '.ch h3{color:'+cfg.c_coral+';font-size:18px;margin:14px 0 6px}'
+ '.ch p{font-size:15px;line-height:1.7;margin:8px 0}'
+ '.ch li{font-size:15px;line-height:1.7}'
+ '.cta{background:'+cfg.c_coral+';color:#fff;padding:34px 64px;font-size:20px;font-weight:800;text-align:center}'
+ '.cta a{color:'+cfg.c_sun+'}'
+ '</style></head><body>'
+ '<div class="cover"><span class="badge">'+esc(cfg.brand)+'</span>'
+ '<h1>'+esc(eb.tieu_de)+'</h1><h2>'+esc(eb.phu_de)+'</h2>'
+ '<p>'+esc(eb.loi_hua_trang_bia)+'</p><div class="brand">'+esc(cfg.brand)+' • '+esc(cfg.funnel_url)+'</div></div>'
+ '<div class="wrap">'+chapters+'</div>'
+ '<div class="cta">'+inline(eb.cta)+'<br><a href="'+esc(cfg.funnel_url)+'">'+esc(cfg.funnel_url)+'</a></div>'
+ '</body></html>';

return [{ json: Object.assign({}, data, { ebook_html }) }];
""".strip("\n")
n5 = node("n5", "5. Boc tach JSON", "n8n-nodes-base.code", 2, [520, 300],
          {"jsCode": parse_js})

# ------------------------------------------------------------------ 6. EBOOK -> PDF (HTTP)
n6 = http(
    "n6", "6. Render Ebook PDF", [740, 300],
    url="={{ %s.PDF_ENDPOINT }}" % CFG,
    json_body_expr="={{ JSON.stringify({ body: $json.ebook_html, css: '', settings: { paper_size: 'A4', orientation: '1', margin_top: '12', margin_bottom: '12' } }) }}",
    auth="httpHeaderAuth",
    creds={"httpHeaderAuth": {"id": "cred-render", "name": "Render API (X-API-KEY)"}},
    timeout=180000,
    notes="Mac dinh = APITemplate.io (create-pdf-from-html). Credential Header Auth: Name = X-API-KEY, Value = API key APITemplate. Doi PDF_ENDPOINT o node Cau hinh neu dung nha cung cap khac.",
)

# ------------------------------------------------------------------ 6b. GOM DU LIEU (Code)
gom_js = r"""
// Gắn link PDF ebook trở lại gói dữ liệu (vì node HTTP đã thay $json).
const pkg = $('5. Boc tach JSON').first().json;
const pdf = $input.first().json || {};
const ebook_pdf_url =
  pdf.download_url || pdf.url ||
  (pdf.data && (pdf.data.download_url || pdf.data.url)) || '';
return [{ json: Object.assign({}, pkg, { ebook_pdf_url }) }];
""".strip("\n")
n6b = node("n6b", "6b. Gom du lieu", "n8n-nodes-base.code", 2, [960, 300],
           {"jsCode": gom_js})

# ------------------------------------------------------------------ 7. SPLIT slides
n7 = node("n7", "7. Tach slide carousel", "n8n-nodes-base.splitOut", 1, [1180, 300],
          {"fieldToSplitOut": "carousel.slides", "include": "allOtherFields", "options": {}})

# ------------------------------------------------------------------ 7b. DUNG HTML SLIDE (Code, per item)
slide_html_js = r"""
// Với mỗi slide -> tạo HTML/CSS khung 1080x1080 để render thành ảnh.
const cfg = $('2. Cau hinh').first().json;
function esc(s){ return String(s==null?'':s)
  .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

return $input.all().map(it => {
  const s = it.json;
  const isFirst = Number(s.so_thu_tu) === 1;
  const css =
    'body{margin:0}'
  + '.slide{width:1080px;height:1080px;box-sizing:border-box;padding:90px;'
  +   'background:' + (isFirst ? cfg.c_coral : cfg.c_cream) + ';'
  +   'color:' + (isFirst ? '#ffffff' : cfg.c_ink) + ';'
  +   'font-family:"DM Sans",Arial,sans-serif;display:flex;flex-direction:column;justify-content:center;position:relative}'
  + '.tag{position:absolute;top:70px;left:90px;font-weight:800;letter-spacing:1px;'
  +   'background:' + (isFirst ? cfg.c_sun : cfg.c_forest) + ';color:' + (isFirst ? cfg.c_ink : '#fff') + ';padding:10px 22px;border-radius:999px;font-size:26px}'
  + '.no{position:absolute;top:70px;right:90px;font-size:30px;font-weight:800;opacity:.7}'
  + '.h{font-size:' + (isFirst ? '88px' : '64px') + ';font-weight:900;line-height:1.05;margin:0 0 28px}'
  + '.b{font-size:40px;line-height:1.45;font-weight:500;max-width:880px}'
  + '.foot{position:absolute;bottom:70px;left:90px;font-weight:700;font-size:28px;'
  +   'color:' + (isFirst ? '#fff' : cfg.c_coral) + '}';
  const html =
    '<div class="slide"><span class="tag">' + esc(cfg.brand) + '</span>'
  + '<span class="no">' + esc(s.so_thu_tu) + '/' + ($input.all().length) + '</span>'
  + '<div class="h">' + esc(s.tieu_de) + '</div>'
  + '<div class="b">' + esc(s.noi_dung) + '</div>'
  + '<div class="foot">' + esc(cfg.funnel_url) + '</div></div>';
  return { json: Object.assign({}, s, { slide_html: html, slide_css: css }) };
});
""".strip("\n")
n7b = node("n7b", "7b. Dung HTML slide", "n8n-nodes-base.code", 2, [1400, 300],
           {"jsCode": slide_html_js})

# ------------------------------------------------------------------ 8. SLIDE -> ANH (HTTP hcti.io)
n8 = http(
    "n8", "8. Slide to anh", [1620, 300],
    url="={{ %s.IMAGE_ENDPOINT }}" % CFG,
    json_body_expr="={{ JSON.stringify({ html: $json.slide_html, css: $json.slide_css, google_fonts: 'DM Sans', viewport_width: 1080, viewport_height: 1080 }) }}",
    auth="httpBasicAuth",
    creds={"httpBasicAuth": {"id": "cred-hcti", "name": "Image API (hcti.io)"}},
    timeout=120000,
    notes="Mac dinh = htmlcsstoimage.com. Credential Basic Auth: User = User ID, Password = API key. Tra ve { url }.",
)

# ------------------------------------------------------------------ 9. AGGREGATE images
n9 = node("n9", "9. Gom anh", "n8n-nodes-base.aggregate", 1, [1840, 300],
          {"aggregate": "aggregateIndividualFields",
           "fieldsToAggregate": {"fieldToAggregate": [
               {"fieldToAggregate": "url", "renameField": True, "outputFieldName": "image_urls"}]},
           "options": {}})

# ------------------------------------------------------------------ 10. BUILD PHAN PHOI (Code)
dist_js = r"""
// Lắp payload cho: (a) đăng feed đa kênh, (b) Salekit audience, (c) Salekit nurture/up-sell.
const cfg = $('2. Cau hinh').first().json;
const pkg = $('5. Boc tach JSON').first().json;
const ebook_pdf_url = ($('6b. Gom du lieu').first().json.ebook_pdf_url) || '';
const image_urls = ($input.first().json.image_urls) || [];

const car = pkg.carousel || {};
const meta = pkg.meta || {};
const hashtags = (car.hashtags || []).join(' ');
const caption = (car.caption || '') + '\n\n👉 Tải ấn phẩm miễn phí: ' + cfg.funnel_url + '\n\n' + hashtags;

// (a) Publisher hợp nhất (mặc định Ayrshare): đăng carousel ảnh lên feed các kênh.
const ayrshare = {
  post: caption,
  platforms: cfg.CHANNELS_FEED,
  mediaUrls: image_urls
};

// (b) Salekit — tạo/cập nhật audience + gắn tag chiến dịch (kích hoạt automation chăm sóc).
const tag = ('leadmagnet:' + (pkg.ebook && pkg.ebook.tieu_de ? pkg.ebook.tieu_de : cfg.chu_de)).slice(0, 60);
const salekit_audience = {
  full_name: cfg.test_lead_name,
  email: cfg.test_lead_email,
  phone: cfg.test_lead_phone,
  tag: tag
};

// (c) Salekit — gửi mồi + mở đường up-sell qua Email/ZNS (đổi endpoint/body theo tài liệu Salekit của bạn).
const noi_dung_email =
  'Chào bạn,\n\nCảm ơn bạn đã quan tâm tới "' + (pkg.ebook ? pkg.ebook.tieu_de : '') + '".\n'
  + 'Tải ấn phẩm tại đây: ' + (ebook_pdf_url || cfg.funnel_url) + '\n\n'
  + (meta.cau_noi_upsell || '') + '\n'
  + 'Tìm hiểu thêm: ' + cfg.funnel_url + '\n\n— ' + cfg.brand;
const salekit_email = {
  to: cfg.test_lead_email,
  subject: (pkg.ebook ? pkg.ebook.tieu_de : 'Quà tặng từ ' + cfg.brand),
  content: noi_dung_email
};

return [{ json: {
  ayrshare,
  salekit_audience,
  salekit_email,
  ebook_pdf_url,
  image_urls,
  caption_kenh: pkg.caption_kenh || {}
} }];
""".strip("\n")
n10 = node("n10", "10. Build phan phoi", "n8n-nodes-base.code", 2, [2060, 300],
           {"jsCode": dist_js})

# ------------------------------------------------------------------ 11. PUBLISHER (HTTP)
n11 = http(
    "n11", "11. Dang da kenh (Publisher)", [2280, 300],
    url="={{ %s.PUBLISHER_URL }}" % CFG,
    json_body_expr="={{ JSON.stringify($json.ayrshare) }}",
    auth="httpHeaderAuth",
    creds={"httpHeaderAuth": {"id": "cred-publisher", "name": "Publisher Bearer (Ayrshare)"}},
    timeout=180000,
    notes="Mac dinh = Ayrshare (dang feed FB/IG/TikTok/Threads). Credential Header Auth: Name = Authorization, Value = Bearer <API key>. Zalo OA do Salekit lo (node 13).",
)

# ------------------------------------------------------------------ 12. SALEKIT AUDIENCE (HTTP)
n12 = http(
    "n12", "12. Salekit - Audience", [2500, 300],
    url="={{ %s.SALEKIT_BASE }}/audience/create" % CFG,
    json_body_expr="={{ JSON.stringify($('10. Build phan phoi').first().json.salekit_audience) }}",
    auth="httpHeaderAuth",
    creds={"httpHeaderAuth": {"id": "cred-salekit", "name": "Salekit Token"}},
    timeout=60000,
    notes="Salekit Audience API. Credential Header Auth: Name = Token, Value = JWT token Salekit (Cau hinh > API). Tao/cap nhat lead + gan tag de kich hoat automation cham soc.",
)

# ------------------------------------------------------------------ 13. SALEKIT NURTURE (HTTP)
n13 = http(
    "n13", "13. Salekit - Email/ZNS nurture", [2720, 300],
    url="={{ %s.SALEKIT_BASE }}/send/email" % CFG,
    json_body_expr="={{ JSON.stringify($('10. Build phan phoi').first().json.salekit_email) }}",
    auth="httpHeaderAuth",
    creds={"httpHeaderAuth": {"id": "cred-salekit", "name": "Salekit Token"}},
    timeout=60000,
    notes="TEMPLATE: xac nhan URL + body theo tai lieu Salekit (send-email-api / api-gui-tin-nhan-zns-qua-zalooa). Giao moi + mo duong up-sell tren kenh so huu.",
)

# ------------------------------------------------------------------ STICKY NOTES
s1 = sticky("s1", [-380, 80], 760, 170,
            "## 🎯 GIAI ĐOẠN 1 — TẠO MỒI BẰNG CLAUDE\n"
            "Form nhập chủ đề/avatar → **Cấu hình** (sửa biến tại đây) → dựng prompt → "
            "**Claude (claude-opus-4-8)** sinh JSON (ebook + carousel + caption) → bóc tách + dựng HTML.\n"
            "👉 Trước khi chạy: tạo credential **Header Auth** `x-api-key` cho Claude. Xem `SETUP.md`.",
            color=4)
s2 = sticky("s2", [720, 80], 1100, 170,
            "## 🖼️ GIAI ĐOẠN 2 — RENDER ẤN PHẨM\n"
            "Ebook → **PDF** (APITemplate.io). Carousel → tách từng slide → dựng HTML → **ảnh 1080×1080** (htmlcsstoimage.com) → gom mảng ảnh.\n"
            "👉 Cần 2 credential: *Render API (X-API-KEY)* và *Image API (hcti.io – Basic Auth)*. "
            "Có thể đổi nhà cung cấp ở node **2. Cau hinh**.",
            color=5)
s3 = sticky("s3", [2040, 80], 900, 200,
            "## 📣 GIAI ĐOẠN 3 — ĐĂNG ĐA KÊNH & ĐẨY VÀO PHỄU\n"
            "**Publisher** (Ayrshare) đăng carousel lên FB/IG/TikTok để hút traffic mới vào đầu phễu.\n"
            "**Salekit**: tạo audience + gắn tag (kích hoạt automation) → gửi mồi + mở đường **up-sell** "
            "qua Email/ZNS Zalo OA (kênh sở hữu).\n"
            "👉 Credential: *Publisher Bearer* và *Salekit Token*.",
            color=3)
s0 = sticky("s0", [-380, -180], 1400, 230,
            "# 🚀 PHỄU LEAD MAGNET — Claude + Salekit.io  (Khoá học Phễu)\n"
            "Một cú bấm: **nhập chủ đề → ra Ebook + bộ ảnh carousel + caption → đăng đa kênh → lead vào CRM + up-sell.**\n\n"
            "**Thứ tự cài đặt (xem `SETUP.md`):** 1) Import workflow  2) Tạo 5 credential  3) Sửa node **2. Cau hinh**  "
            "4) Bấm *Test workflow* và điền form  5) Go-live.\n"
            "**Mẹo dạy học:** mỗi giai đoạn = 1 buổi học. Học viên chỉ sửa node **2. Cau hinh** và prompt ở node **3**.",
            color=6)

# ------------------------------------------------------------------ CONNECTIONS
def conn(src, dst):
    return {src: {"main": [[{"node": dst, "type": "main", "index": 0}]]}}

connections = {}
chain = [n1, n2, n3, n4, n5, n6, n6b, n7, n7b, n8, n9, n10, n11, n12, n13]
for a, b in zip(chain, chain[1:]):
    connections[a["name"]] = {"main": [[{"node": b["name"], "type": "main", "index": 0}]]}

workflow = {
    "name": "Phễu Lead Magnet — Claude + Salekit.io",
    "nodes": [s0, s1, s2, s3, n1, n2, n3, n4, n5, n6, n6b, n7, n7b, n8, n9, n10, n11, n12, n13],
    "connections": connections,
    "active": False,
    "settings": {"executionOrder": "v1"},
    "pinData": {},
    "meta": {"templateCredsSetupCompleted": False},
    "tags": [],
}

out = "lead-magnet-multichannel.workflow.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(workflow, f, ensure_ascii=False, indent=2)

# tự kiểm tra hợp lệ
with open(out, encoding="utf-8") as f:
    json.load(f)
print("OK ->", out, "| nodes:", len(workflow["nodes"]), "| connections:", len(connections))
