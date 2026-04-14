# streamlit run app.py --server.runOnSave true
# git add .
# git commit -m "mô tả thay đổi"
# git push

import os
import re
import unicodedata
import json as pyjson
import streamlit as st
import streamlit.components.v1 as components

from textwrap import dedent
from html import escape
from google import genai
from google.genai import types

import base64

def image_to_data_uri(candidates):
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }

    for path in candidates:
        if path and os.path.exists(path):
            ext = os.path.splitext(path)[1].lower()
            mime = mime_map.get(ext, "image/png")
            try:
                with open(path, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode("utf-8")
                return f"data:{mime};base64,{encoded}"
            except Exception:
                pass

    return ""

st.set_page_config(
    page_title="LAO CAI HERITAGE AI",
    page_icon="assets/anime_teamtrangchu1.png",
    layout="wide"
)

page = st.query_params.get("page", "home")


# ChatBot
def _load_json_safe(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = pyjson.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []

def _build_chatbot_payload():
    diemden = _load_json_safe("diemden.json")
    lichtrinh = _load_json_safe("lichtrinh.json")

    places = []
    for item in diemden[:120]:
        highlights = item.get("highlights", [])
        if not isinstance(highlights, list):
            highlights = []

        places.append({
            "name": str(item.get("name", "")).strip(),
            "slug": str(item.get("slug", "")).strip(),
            "area": str(item.get("area", "")).strip(),
            "category": str(item.get("category", "")).strip(),
            "season": str(item.get("season", "")).strip(),
            "best_time": str(item.get("best_time", "")).strip(),
            "short_desc": str(item.get("short_desc", "")).strip(),
            "full_desc": str(item.get("full_desc", "")).strip(),
            "image": str(item.get("image", "")).strip(),
            "highlights": [str(x).strip() for x in highlights[:5] if str(x).strip()]
        })

    routes = []
    for item in lichtrinh[:150]:
        routes.append({
            "from": str(item.get("from", "")).strip(),
            "to": str(item.get("to", "")).strip(),
            "slug": str(item.get("slug", "")).strip(),
            "category": str(item.get("category", "")).strip(),
            "time_estimate": str(item.get("time_estimate", "")).strip(),
            "distance_km": str(item.get("distance_km", "")).strip(),
            "transport_name": str(item.get("transport_name", "")).strip(),
            "transport_price": str(item.get("transport_price", "")).strip(),
            "ticket_price": str(item.get("ticket_price", "")).strip(),
            "hotel_name": str(item.get("hotel_name", "")).strip(),
            "hotel_price": str(item.get("hotel_price", "")).strip(),
            "total_price": str(item.get("total_price", "")).strip(),
            "note": str(item.get("note", "")).strip(),
            "short_desc": str(item.get("short_desc", "")).strip()
        })

    return {
        "brand": "Lao Cai Heritage AI",
        "phone": "0346 538 917",
        "places": places,
        "routes": routes,
        "quick_questions": [
            "Sa Pa có gì đẹp?",
            "Mùa nào đi Fansipan đẹp?",
            "Gợi ý lịch trình đi Bắc Hà",
            "Chi phí tham khảo thế nào?"
        ]
    }

CHATBOT_PAYLOAD = _build_chatbot_payload()

GEMINI_MODEL = "gemini-2.5-flash"

def normalize_query_text(value: str) -> str:
    text = str(value or "").strip().lower()
    text = text.replace("đ", "d").replace("Đ", "D")
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return text

def tokenize_query(value: str) -> list[str]:
    text = normalize_query_text(value)
    return [tok for tok in re.split(r"[^a-zA-Z0-9]+", text) if len(tok) >= 2]

def score_item(fields, tokens: list[str]) -> int:
    joined = " ".join(str(x or "") for x in fields)
    norm = normalize_query_text(joined)
    score = 0

    for tok in tokens:
        if tok in norm:
            score += 3

    return score

def build_context_from_payload(question: str, payload: dict, current_page: str) -> str:
    tokens = tokenize_query(question)

    places_ranked = []
    for item in payload.get("places", []):
        fields = [
            item.get("name"),
            item.get("area"),
            item.get("category"),
            item.get("season"),
            item.get("best_time"),
            item.get("short_desc"),
            item.get("full_desc"),
            " ".join(item.get("highlights", [])) if isinstance(item.get("highlights"), list) else ""
        ]
        score = score_item(fields, tokens)

        # cộng điểm mạnh nếu user nhắc đúng tên địa điểm
        name_norm = normalize_query_text(item.get("name", ""))
        q_norm = normalize_query_text(question)
        if name_norm and name_norm in q_norm:
            score += 8

        if score > 0:
            places_ranked.append((score, item))

    routes_ranked = []
    for item in payload.get("routes", []):
        fields = [
            item.get("from"),
            item.get("to"),
            item.get("category"),
            item.get("time_estimate"),
            item.get("distance_km"),
            item.get("transport_name"),
            item.get("transport_price"),
            item.get("ticket_price"),
            item.get("hotel_name"),
            item.get("hotel_price"),
            item.get("total_price"),
            item.get("note"),
            item.get("short_desc"),
        ]
        score = score_item(fields, tokens)

        to_norm = normalize_query_text(item.get("to", ""))
        q_norm = normalize_query_text(question)
        if to_norm and to_norm in q_norm:
            score += 8

        if score > 0:
            routes_ranked.append((score, item))

    places_ranked.sort(key=lambda x: x[0], reverse=True)
    routes_ranked.sort(key=lambda x: x[0], reverse=True)

    top_places = [item for _, item in places_ranked[:5]]
    top_routes = [item for _, item in routes_ranked[:5]]

    lines = []
    lines.append(f"Trang hiện tại: {current_page}")
    lines.append(f"Tổng số địa điểm trong hệ thống: {len(payload.get('places', []))}")
    lines.append(f"Tổng số lịch trình trong hệ thống: {len(payload.get('routes', []))}")
    lines.append("")

    if top_places:
        lines.append("ĐỊA ĐIỂM LIÊN QUAN:")
        for i, p in enumerate(top_places, 1):
            highlights = p.get("highlights", [])
            if not isinstance(highlights, list):
                highlights = []

            lines.append(
                f"{i}. Tên: {p.get('name', 'Đang cập nhật')} | "
                f"Khu vực: {p.get('area', 'Đang cập nhật')} | "
                f"Loại hình: {p.get('category', 'Đang cập nhật')} | "
                f"Mùa đẹp: {p.get('season', 'Đang cập nhật')} | "
                f"Thời điểm đẹp: {p.get('best_time', 'Đang cập nhật')} | "
                f"Mô tả ngắn: {p.get('short_desc', 'Đang cập nhật')} | "
                f"Nổi bật: {', '.join(highlights[:5]) if highlights else 'Đang cập nhật'}"
            )
        lines.append("")

    if top_routes:
        lines.append("LỊCH TRÌNH LIÊN QUAN:")
        for i, r in enumerate(top_routes, 1):
            lines.append(
                f"{i}. Từ: {r.get('from', 'Đang cập nhật')} | "
                f"Đến: {r.get('to', 'Đang cập nhật')} | "
                f"Loại hình: {r.get('category', 'Đang cập nhật')} | "
                f"Thời gian: {r.get('time_estimate', 'Đang cập nhật')} | "
                f"Quãng đường: {r.get('distance_km', 'Đang cập nhật')} | "
                f"Phương tiện: {r.get('transport_name', 'Đang cập nhật')} | "
                f"Giá xe: {r.get('transport_price', 'Đang cập nhật')} | "
                f"Vé tham quan: {r.get('ticket_price', 'Đang cập nhật')} | "
                f"Khách sạn: {r.get('hotel_name', 'Đang cập nhật')} | "
                f"Giá khách sạn: {r.get('hotel_price', 'Đang cập nhật')} | "
                f"Tổng chi phí: {r.get('total_price', 'Đang cập nhật')} | "
                f"Ghi chú: {r.get('note', 'Đang cập nhật')}"
            )
        lines.append("")

    if not top_places and not top_routes:
        lines.append("Không tìm thấy mục nào khớp mạnh trong dữ liệu nội bộ.")
        lines.append("Khi trả lời, hãy nói rõ dữ liệu hệ thống chưa có thông tin đủ cụ thể.")

    return "\n".join(lines)

def build_history_text(messages: list[dict], limit: int = 8) -> str:
    recent = messages[-limit:] if messages else []
    lines = []

    for msg in recent:
        role = "Người dùng" if msg.get("role") == "user" else "Trợ lý"
        content = str(msg.get("content", "")).strip()
        if content:
            lines.append(f"{role}: {content}")

    return "\n".join(lines) if lines else "Chưa có lịch sử hội thoại."

def ask_gemini(user_message: str, payload: dict, current_page: str, messages: list[dict]) -> str:
    route_mode = route_question(user_message)

    if route_mode == "internal":
        api_key = os.environ.get("GEMINI_API_KEY", "").strip()
        if not api_key:
            return "Bạn chưa cấu hình GEMINI_API_KEY."

        try:
            client = genai.Client(api_key=api_key)

            context_text = build_context_from_payload(user_message, payload, current_page)
            history_text = build_history_text(messages, limit=8)

            prompt = f"""
DỮ LIỆU NỘI BỘ:
{context_text}

LỊCH SỬ HỘI THOẠI GẦN ĐÂY:
{history_text}

CÂU HỎI MỚI CỦA NGƯỜI DÙNG:
{user_message}
""".strip()

            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "Bạn là Lao Cai Heritage AI, trợ lý du lịch thông minh cho website giới thiệu "
                        "địa điểm, lịch trình và văn hóa Lào Cai. "
                        "Chỉ ưu tiên dữ liệu nội bộ được cung cấp trong prompt. "
                        "Không bịa thông tin. Nếu dữ liệu hệ thống chưa có, hãy nói rõ là chưa có trong hệ thống. "
                        "Trả lời bằng tiếng Việt, ngắn gọn, đúng trọng tâm, dễ hiểu. "
                        "Ưu tiên trả lời theo dạng tư vấn thực tế cho khách du lịch. "
                        "Khi phù hợp, gợi ý thêm 1 đến 2 câu hỏi tiếp theo. "
                        "Không nói rằng bạn là Gemini hay Google."
                    ),
                    temperature=0.35,
                    max_output_tokens=500,
                ),
            )

            answer = (response.text or "").strip()
            if answer:
                return answer

            return "Mình chưa tạo được câu trả lời phù hợp. Bạn hãy hỏi lại ngắn gọn hơn."

        except Exception as e:
            error_text = str(e)

            if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text.upper():
                return "Gemini đang báo hết quota hoặc vượt giới hạn tốc độ ở API key hiện tại."

            if "API key" in error_text or "api_key" in error_text.lower():
                return "API key Gemini chưa đúng hoặc chưa được cấp quyền."

            return f"Lỗi Gemini: {error_text}"

    if route_mode in ["search", "hybrid"]:
        return ask_gemini_search(
            user_message=user_message,
            payload=payload,
            current_page=current_page,
            messages=messages
        )

    return "Mình chưa xác định được kiểu câu hỏi."
    

def route_question(user_message: str) -> str:
    q = normalize_query_text(user_message)

    search_keywords = [
        "hom nay", "hien tai", "moi nhat", "gan day", "tin tuc", "thoi tiet",
        "su kien", "le hoi", "gia ve", "gio mo cua", "lich mo cua", "cap nhat",
        "nam nay", "thang nay", "tuan nay"
    ]

    external_keywords = [
        "o dau", "dia chi", "di chuyen", "duong di", "review", "danh gia",
        "an gi", "khach san nao", "quan an", "cafe", "gan", "xung quanh"
    ]

    internal_score = 0
    for item in CHATBOT_PAYLOAD.get("places", []):
        name_norm = normalize_query_text(item.get("name", ""))
        if name_norm and name_norm in q:
            internal_score += 2

    for item in CHATBOT_PAYLOAD.get("routes", []):
        to_norm = normalize_query_text(item.get("to", ""))
        if to_norm and to_norm in q:
            internal_score += 2

    if any(k in q for k in search_keywords):
        return "search"

    if any(k in q for k in external_keywords):
        return "search"

    if internal_score > 0:
        return "internal"

    return "hybrid"


def ask_gemini_search(user_message: str, payload: dict, current_page: str, messages: list[dict]) -> str:
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        return "Bạn chưa cấu hình GEMINI_API_KEY."

    try:
        client = genai.Client(api_key=api_key)

        context_text = build_context_from_payload(user_message, payload, current_page)
        history_text = build_history_text(messages, limit=8)

        prompt = f"""
DỮ LIỆU NỘI BỘ THAM KHẢO:
{context_text}

LỊCH SỬ HỘI THOẠI GẦN ĐÂY:
{history_text}

CÂU HỎI MỚI CỦA NGƯỜI DÙNG:
{user_message}

YÊU CẦU:
- Ưu tiên dữ liệu nội bộ nếu đã có.
- Nếu dữ liệu nội bộ chưa đủ hoặc câu hỏi cần thông tin mới, hãy dùng Google Search để bổ sung.
- Phân biệt rõ:
  1. Thông tin từ hệ thống
  2. Thông tin tham khảo từ web
- Không bịa chi tiết cụ thể.
""".strip()

        grounding_tool = types.Tool(
            google_search=types.GoogleSearch()
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[grounding_tool],
                system_instruction=(
                    "Bạn là Lao Cai Heritage AI, trợ lý du lịch thông minh cho website du lịch Lào Cai. "
                    "Khi có dữ liệu nội bộ trong prompt, hãy ưu tiên dùng trước. "
                    "Khi cần thông tin mới hoặc ngoài hệ thống, hãy dùng Google Search. "
                    "Trả lời bằng tiếng Việt, ngắn gọn, dễ hiểu, thực tế. "
                    "Nếu có thông tin lấy từ web, ghi rõ đó là thông tin tham khảo mới cập nhật. "
                    "Không nói rằng bạn là Gemini hay Google."
                ),
                temperature=0.35,
                max_output_tokens=700,
            ),
        )

        answer = (response.text or "").strip()
        if answer:
            return answer

        return "Mình chưa lấy được câu trả lời phù hợp từ web. Bạn hãy hỏi cụ thể hơn."

    except Exception as e:
        error_text = str(e)

        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text.upper():
            return "Gemini đang báo hết quota hoặc vượt giới hạn tốc độ ở API key hiện tại."

        if "API key" in error_text or "api_key" in error_text.lower():
            return "API key Gemini chưa đúng hoặc chưa được cấp quyền."

        return f"Lỗi Gemini Search: {error_text}"

hero_home_src = image_to_data_uri([
    "kho_anh/chinh.png",
    "kho_anh/chinh.jpg",
    "kho_anh/chinh.jpeg",
    "kho_anh/chinh.webp"
])

# CSS trang chủ
st.markdown(f"""
<style>
/* Ẩn menu mặc định streamlit cho giống web thật hơn */
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
header {{visibility: hidden;}}

/* Toàn bộ nền */
.stApp {{
    background-color: #f6f6f6;
}}

/* Giảm padding mặc định */
.block-container {{
    padding-top: 0rem;
    padding-left: 0rem;
    padding-right: 0rem;
    max-width: 100%;
}}

/* Navbar */
.navbar {{
    background: rgba(255,255,255,0.98);
    height: 72px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 60px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    width: 100%;
    z-index: 99999;
    box-sizing: border-box;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
}}

.logo {{
    display: flex;
    align-items: center;
    gap: 14px;
    text-decoration: none;
    white-space: nowrap;
}}

.logo img {{
    height: 71px;
    width: auto;
    display: block;
    object-fit: contain;
}}

.logo-text {{
    font-size: 34px;
    font-weight: 800;
    color: #1565c0;
    line-height: 1;
}}

.logo-text span {{
    color: #2e7d32;
}}

.nav-links {{
    display: flex;
    gap: 34px;
    align-items: center;
    flex-wrap: wrap;
}}

.nav-links a {{
    font-size: 18px;
    font-weight: 600;
    color: #222;
    text-decoration: none;
    position: relative;
    padding: 6px 0;
    transition: color 0.25s ease;
}}

.nav-links a:hover {{
    color: #1565c0;
}}

.nav-links a.active {{
    color: #1565c0;
}}

.nav-links a.active::after {{
    content: "";
    position: absolute;
    left: 0;
    bottom: -6px;
    width: 100%;
    height: 3px;
    border-radius: 999px;
    background: #1565c0;
}}

/* Hero */
.hero {{
    position: relative;
    min-height: 100vh;
    background-image: linear-gradient(rgba(0,0,0,0.28), rgba(0,0,0,0.28)),
                      url('{hero_home_src}');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    display: flex;
    align-items: center;
    padding: 0 80px;
    box-sizing: border-box;
    overflow: hidden;
}}

.hero-content {{
    color: white;
    max-width: 760px;
    width: 100%;
    position: relative;
    z-index: 2;
}}

.hero-title {{
    font-size: 54px;
    font-weight: 800;
    line-height: 1.15;
    margin-bottom: 16px;
}}

.hero-subtitle {{
    font-size: 22px;
    line-height: 1.6;
    opacity: 0.96;
}}

@media (max-width: 768px) {{
    .hero {{
        min-height: calc(100vh - 72px);
        padding: 0 24px;
    }}

    .hero-title {{
        font-size: 42px;
        line-height: 1.15;
    }}

    .hero-subtitle {{
        font-size: 18px;
        line-height: 1.65;
    }}
}}

.hero-content {{
    color: white;
    max-width: 700px;
    animation: heroFadeUp 1s ease-out forwards;
}}

.hero-title {{
    font-size: 54px;
    font-weight: 800;
    line-height: 1.15;
    margin-bottom: 16px;
    opacity: 0;
    transform: translateY(28px);
    animation: heroTextUp 1s ease-out forwards;
}}

.hero-subtitle {{
    font-size: 22px;
    line-height: 1.6;
    opacity: 0;
    transform: translateY(30px);
    animation: heroTextUp 1s ease-out 0.35s forwards;
}}

@keyframes heroZoom {{
    from {{
        background-size: 100%;
    }}
    to {{
        background-size: 108%;
    }}
}}

@keyframes heroTextUp {{
    from {{
        opacity: 0;
        transform: translateY(28px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

@keyframes heroFadeUp {{
    from {{
        opacity: 0.2;
    }}
    to {{
        opacity: 1;
    }}
}}

.hero-content {{
    color: white;
    max-width: 700px;
}}

.hero-title {{
    font-size: 54px;
    font-weight: 800;
    line-height: 1.15;
    margin-bottom: 16px;
}}

.hero-subtitle {{
    font-size: 22px;
    line-height: 1.6;
    opacity: 0.96;
}}       

@media (max-width: 992px) {{
    .search-wrapper {{
        margin-top: -52px;
    }}

    .search-box {{
        width: 92%;
    }}

    .search-row {{
        grid-template-columns: 1fr 1fr;
    }}
}}

@media (max-width: 640px) {{
    .search-wrapper {{
        margin-top: -36px;
    }}

    .search-box {{
        width: 94%;
        padding: 14px;
    }}

    .search-row {{
        grid-template-columns: 1fr;
    }}
}}            

.search-float {{
    position: relative;
    margin-top: -95px;  
    margin-bottom: -20px;
    z-index: 50;
}}         

/* Danh mục nhanh */
.section {{
    padding: 46px 70px 10px 70px;
}}

.quick-grid {{
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 24px;
    margin-top: 20px;
}}

.quick-card {{
    background: white;
    border-radius: 20px;
    padding: 26px 16px;
    text-align: center;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
    transition: 0.2s;
}}

.quick-card:hover {{
    transform: translateY(-4px);
}}

.quick-icon {{
    font-size: 34px;
    margin-bottom: 10px;
}}

.quick-title {{
    font-size: 18px;
    font-weight: 700;
    color: #1f2937;
}}

/* Tiêu đề section */
.section-title {{
    font-size: 34px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 8px;
}}

.section-subtitle {{
    font-size: 18px;
    color: #6b7280;
}}

/* Card địa điểm */
.place-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 26px;
    margin-top: 28px;
    margin-bottom: 60px;
}}

.place-card {{
    background: white;
    border-radius: 22px;
    overflow: hidden;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
}}

.place-image {{
    height: 220px;
    background-size: cover;
    background-position: center;
}}

.place-body {{
    padding: 18px;
}}

.place-name {{
    font-size: 22px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 10px;
}}

.place-desc {{
    color: #4b5563;
    line-height: 1.6;
    font-size: 16px;
}}

/* Footer */
.footer {{
    background: #dfeefc;
    padding: 40px 70px;
    margin-top: 30px;
}}

.footer-title {{
    font-size: 24px;
    font-weight: 800;
    margin-bottom: 14px;
    color: #0d2b4d;
}}

.footer-text {{
    font-size: 17px;
    color: #334155;
    line-height: 1.8;
}}
</style>
""", unsafe_allow_html=True)

navbar_logo_src = image_to_data_uri([
    "assets/anime_teamtrangchu1.png",
    "anime_teamtrangchu1.png",
    "assets/anime_teamtrangchu1.jpg",
    "anime_teamtrangchu1.jpg",
    "assets/anime_teamtrangchu1.jpeg",
    "anime_teamtrangchu1.jpeg",
    "assets/anime_teamtrangchu1.webp",
    "anime_teamtrangchu1.webp"
])

# Topbar
navbar_html = dedent(f"""
<div class="navbar">
    <a class="logo" href="?page=home" target="_self">
        <img src="{navbar_logo_src}" alt="Logo">
        <span class="logo-text">Lao Cai <span>Heritage AI</span></span>
    </a>
    <div class="nav-links">
        <a href="?page=home" target="_self" class="{'active' if page == 'home' else ''}">Trang chủ</a>
        <a href="?page=diemden" target="_self" class="{'active' if page in ['diemden', 'diemden_detail'] else ''}">Điểm đến</a>
        <a href="?page=lichtrinh" target="_self" class="{'active' if page in ['lichtrinh', 'lichtrinh_detail'] else ''}">Lịch trình</a>
        <a href="?page=chatbot" target="_self" class="{'active' if page == 'chatbot' else ''}">Chatbot AI</a>
        <a href="?page=gioithieu" target="_self" class="{'active' if page == 'gioithieu' else ''}">Về dự án</a>
    </div>
</div>
""")
st.markdown(navbar_html, unsafe_allow_html=True)

hero_home_src = image_to_data_uri([
    "kho_anh/trang_chu/chinh.png",
    "kho_anh/trang_chu/chinh.jpg",
    "kho_anh/trang_chu/chinh.jpeg",
    "kho_anh/trang_chu/chinh.webp"
])

if page == "home":
    # Hero
    st.markdown("""
    <div class="hero">
        <div class="hero-content">
            <div class="hero-title">Khám phá vẻ đẹp văn hóa và lịch sử Lào Cai</div>
            <div class="hero-subtitle">
                Một nền tảng du lịch thông minh giúp bạn tìm hiểu di tích,
                danh lam thắng cảnh và gợi ý hành trình phù hợp bằng AI.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    kham_pha_1 = image_to_data_uri([
        "kho_anh/trang_chu/kham_pha/1.png",
        "kho_anh/trang_chu/kham_pha/1.jpg",
        "kho_anh/trang_chu/kham_pha/1.jpeg",
        "kho_anh/trang_chu/kham_pha/1.webp"
    ])

    kham_pha_2 = image_to_data_uri([
        "kho_anh/trang_chu/kham_pha/2.png",
        "kho_anh/trang_chu/kham_pha/2.jpg",
        "kho_anh/trang_chu/kham_pha/2.jpeg",
        "kho_anh/trang_chu/kham_pha/2.webp"
    ])

    kham_pha_3 = image_to_data_uri([
        "kho_anh/trang_chu/kham_pha/3.png",
        "kho_anh/trang_chu/kham_pha/3.jpg",
        "kho_anh/trang_chu/kham_pha/3.jpeg",
        "kho_anh/trang_chu/kham_pha/3.webp"
    ])

    kham_pha_4 = image_to_data_uri([
        "kho_anh/trang_chu/kham_pha/4.png",
        "kho_anh/trang_chu/kham_pha/4.jpg",
        "kho_anh/trang_chu/kham_pha/4.jpeg",
        "kho_anh/trang_chu/kham_pha/4.webp"
    ])

    kham_pha_5 = image_to_data_uri([
        "kho_anh/trang_chu/kham_pha/5.png",
        "kho_anh/trang_chu/kham_pha/5.jpg",
        "kho_anh/trang_chu/kham_pha/5.jpeg",
        "kho_anh/trang_chu/kham_pha/5.webp"
    ])

    # Khám phá nhanh
    components.html(f"""
    <style>
    body {{
        margin: 0;
        font-family: Arial, sans-serif;
    }}

    .product-section {{
        padding: 30px 0 20px 0;
        width: 100%;
        box-sizing: border-box;
        overflow: hidden;
    }}

    .product-container {{
        width: 100%;
        max-width: 1280px;
        margin: 0 auto;
        padding: 0 24px;
        box-sizing: border-box;
    }}

    .product-header {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 24px;
        margin-bottom: 28px;
    }}

    .product-header-left {{
        flex: 1;
        min-width: 0;
    }}

    .product-title {{
        font-size: 35px;
        font-weight: 800;
        color: #1565c0;
        text-transform: uppercase;
        line-height: 1.3;
        margin-bottom: 8px;
    }}

    .product-line {{
        width: 145px;
        height: 4px;
        background: #1565c0;
        border-radius: 999px;
        margin-bottom: 18px;
    }}

    .product-desc {{
        max-width: 940px;
        font-size: 18px;
        line-height: 1.8;
        color: #1f2937;
    }}

    .arrow-box {{
        display: flex;
        gap: 14px;
        align-items: center;
        flex-shrink: 0;
        margin-top: 10px;
    }}

    .arrow-btn {{
        width: 50px;
        height: 50px;
        border: none;
        border-radius: 50%;
        background: #ffffff;
        color: #6b7280;
        font-size: 24px;
        cursor: pointer;
        box-shadow: 0 6px 18px rgba(0,0,0,0.10);
        transition: all 0.25s ease;
    }}

    .arrow-btn:hover {{
        transform: translateY(-2px);
        color: #1565c0;
        box-shadow: 0 10px 22px rgba(0,0,0,0.14);
    }}

    .arrow-btn:disabled {{
        opacity: 0.45;
        cursor: not-allowed;
        transform: none;
    }}

    /* khung ngoài */
    .carousel-wrap {{
        width: 100%;
        overflow: hidden;
        position: relative;
        padding-right: 90px; /* chừa chỗ để lộ card sau */
        box-sizing: border-box;
    }}

    /* thanh trượt */
    .carousel-track {{
        display: flex;
        gap: 18px;
        transition: transform 0.6s ease;
        will-change: transform;
    }}

    /* mỗi card */
    .product-card {{
        position: relative;
        flex: 0 0 calc((100% - 36px) / 3); /* 3 card chính */
        height: 300px;
        border-radius: 22px;
        overflow: hidden;
        background-size: cover;
        background-position: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    }}

    .product-card::after {{
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(to top, rgba(0,0,0,0.62), rgba(0,0,0,0.08));
    }}

    .product-text {{
        position: absolute;
        left: 18px;
        right: 18px;
        bottom: 16px;
        z-index: 2;
        color: #fff;
        font-size: 15px;
        font-weight: 800;
        text-transform: uppercase;
        line-height: 1.5;
        text-shadow: 0 2px 8px rgba(0,0,0,0.35);
        text-align: center;
    }}

    @media (max-width: 992px) {{
        .product-header {{
            flex-direction: column;
            align-items: flex-start;
        }}

        .carousel-wrap {{
            padding-right: 40px;
        }}

        .product-card {{
            flex: 0 0 calc((100% - 18px) / 2);
            height: 270px;
        }}
    }}

    @media (max-width: 768px) {{
        .product-container {{
            padding: 0 16px;
        }}

        .product-title {{
            font-size: 24px;
        }}

        .product-desc {{
            font-size: 16px;
            line-height: 1.7;
        }}

        .carousel-wrap {{
            padding-right: 0;
        }}

        .product-card {{
            flex: 0 0 100%;
            height: 250px;
        }}

        .arrow-btn {{
            width: 46px;
            height: 46px;
            font-size: 22px;
        }}
    }}
    </style>

    <div class="product-section">
        <div class="product-container">
            <div class="product-header">
                <div class="product-header-left">
                    <div class="product-title">KHÁM PHÁ LAO CAI HERITAGE AI</div>
                    <div class="product-line"></div>
                    <div class="product-desc">
                        Nền tảng ứng dụng trí tuệ nhân tạo giúp giới thiệu các địa danh, văn hóa, lịch sử và du lịch Lào Cai một cách trực quan, hiện đại và dễ tiếp cận.
                        Mang đến trải nghiệm khám phá thông minh, hỗ trợ tra cứu thông tin, gợi ý hành trình và kết nối người dùng với vẻ đẹp của quê hương Lào Cai.
                    </div>
                </div>

                <div class="arrow-box">
                    <button class="arrow-btn" id="prevBtn">←</button>
                    <button class="arrow-btn" id="nextBtn">→</button>
                </div>
            </div>

            <div class="carousel-wrap">
                <div class="carousel-track" id="carouselTrack"></div>
            </div>
        </div>
    </div>

    <script>
    const productData = [
        {{
            image: "{kham_pha_1}",
            text: "TIỀM NĂNG, ĐỊNH HƯỚNG PHÁT TRIỂN"
        }},
        {{
            image: "{kham_pha_2}",
            text: "Sun World Fansipan Legend"
        }},
        {{
            image: "{kham_pha_3}",
            text: "đua ngựa bắc hà"
        }},
        {{
            image: "{kham_pha_4}",
            text: "nhà thờ đá sapa"
        }},
        {{
            image: "{kham_pha_5}",
            text: "tâm linh - đền chiềng ken"
        }}
    ];

    const track = document.getElementById("carouselTrack");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");

    let currentIndex = 0;

    function buildCards() {{
        track.innerHTML = "";
        productData.forEach(item => {{
            const card = document.createElement("div");
            card.className = "product-card";
            card.style.backgroundImage = `url('${{item.image}}')`;
            card.innerHTML = `<div class="product-text">${{item.text}}</div>`;
            track.appendChild(card);
        }});
    }}

    function getVisibleCount() {{
        if (window.innerWidth <= 768) return 1;
        if (window.innerWidth <= 992) return 2;
        return 3;
    }}

    function updateCarousel() {{
        const cards = track.querySelectorAll(".product-card");
        if (!cards.length) return;

        const gap = 18;
        const cardWidth = cards[0].offsetWidth + gap;
        track.style.transform = `translateX(-${{currentIndex * cardWidth}}px)`;

        prevBtn.disabled = currentIndex === 0;
        nextBtn.disabled = currentIndex >= productData.length - getVisibleCount();
    }}

    prevBtn.addEventListener("click", () => {{
        if (currentIndex > 0) {{
            currentIndex--;
            updateCarousel();
        }}
    }});

    nextBtn.addEventListener("click", () => {{
        if (currentIndex < productData.length - getVisibleCount()) {{
            currentIndex++;
            updateCarousel();
        }}
    }});

    window.addEventListener("resize", updateCarousel);

    buildCards();
    setTimeout(updateCarousel, 100);
    </script>
    """, height=540)

    # Miền Bắc
    nb_quangninh = image_to_data_uri([
        "kho_anh/trang_chu/noi_bat/bac/quangninh.png",
        "kho_anh/trang_chu/noi_bat/bac/quangninh.jpg",
        "kho_anh/trang_chu/noi_bat/bac/quangninh.jpeg",
        "kho_anh/trang_chu/noi_bat/bac/quangninh.webp"
    ])

    nb_hagiang = image_to_data_uri([
        "kho_anh/trang_chu/noi_bat/bac/hagiang.png",
        "kho_anh/trang_chu/noi_bat/bac/hagiang.jpg",
        "kho_anh/trang_chu/noi_bat/bac/hagiang.jpeg",
        "kho_anh/trang_chu/noi_bat/bac/hagiang.webp"
    ])

    nb_laocai = image_to_data_uri([
        "kho_anh/trang_chu/noi_bat/bac/laocai.png",
        "kho_anh/trang_chu/noi_bat/bac/laocai.jpg",
        "kho_anh/trang_chu/noi_bat/bac/laocai.jpeg",
        "kho_anh/trang_chu/noi_bat/bac/laocai.webp"
    ])

    nb_ninhbinh = image_to_data_uri([
        "kho_anh/trang_chu/noi_bat/bac/ninhbinh.png",
        "kho_anh/trang_chu/noi_bat/bac/ninhbinh.jpg",
        "kho_anh/trang_chu/noi_bat/bac/ninhbinh.jpeg",
        "kho_anh/trang_chu/noi_bat/bac/ninhbinh.webp"
    ])

    nb_yenbai = image_to_data_uri([
        "kho_anh/trang_chu/noi_bat/bac/yenbai.png",
        "kho_anh/trang_chu/noi_bat/bac/yenbai.jpg",
        "kho_anh/trang_chu/noi_bat/bac/yenbai.jpeg",
        "kho_anh/trang_chu/noi_bat/bac/yenbai.webp"
    ])

    nb_sonla = image_to_data_uri([
        "kho_anh/trang_chu/noi_bat/bac/sonla.png",
        "kho_anh/trang_chu/noi_bat/bac/sonla.jpg",
        "kho_anh/trang_chu/noi_bat/bac/sonla.jpeg",
        "kho_anh/trang_chu/noi_bat/bac/sonla.webp"
    ])

    nb_caobang = image_to_data_uri([
        "kho_anh/trang_chu/noi_bat/bac/caobang.png",
        "kho_anh/trang_chu/noi_bat/bac/caobang.jpg",
        "kho_anh/trang_chu/noi_bat/bac/caobang.jpeg",
        "kho_anh/trang_chu/noi_bat/bac/caobang.webp"
    ])

    nb_haiphong = image_to_data_uri([
        "kho_anh/trang_chu/noi_bat/bac/haiphong.png",
        "kho_anh/trang_chu/noi_bat/bac/haiphong.jpg",
        "kho_anh/trang_chu/noi_bat/bac/haiphong.jpeg",
        "kho_anh/trang_chu/noi_bat/bac/haiphong.webp"
    ])

    nb_hanoi = image_to_data_uri([
        "kho_anh/trang_chu/noi_bat/bac/hanoi.png",
        "kho_anh/trang_chu/noi_bat/bac/hanoi.jpg",
        "kho_anh/trang_chu/noi_bat/bac/hanoi.jpeg",
        "kho_anh/trang_chu/noi_bat/bac/hanoi.webp"
    ])

    # Miền Trung
    nt_hue = image_to_data_uri([
        "kho_anh/trang_chu/noi_bat/trung/hue.png",
        "kho_anh/trang_chu/noi_bat/trung/hue.jpg",
        "kho_anh/trang_chu/noi_bat/trung/hue.jpeg",
        "kho_anh/trang_chu/noi_bat/trung/hue.webp"
    ])

    nt_danang = image_to_data_uri([
        "kho_anh/trang_chu/noi_bat/trung/danang.png",
        "kho_anh/trang_chu/noi_bat/trung/danang.jpg",
        "kho_anh/trang_chu/noi_bat/trung/danang.jpeg",
        "kho_anh/trang_chu/noi_bat/trung/danang.webp"
    ])

    nt_quangnam = image_to_data_uri([
        "kho_anh/trang_chu/noi_bat/trung/quangnam.png",
        "kho_anh/trang_chu/noi_bat/trung/quangnam.jpg",
        "kho_anh/trang_chu/noi_bat/trung/quangnam.jpeg",
        "kho_anh/trang_chu/noi_bat/trung/quangnam.webp"
    ])

    nt_nhatrang = image_to_data_uri([
        "kho_anh/trang_chu/noi_bat/trung/nhatrang.png",
        "kho_anh/trang_chu/noi_bat/trung/nhatrang.jpg",
        "kho_anh/trang_chu/noi_bat/trung/nhatrang.jpeg",
        "kho_anh/trang_chu/noi_bat/trung/nhatrang.webp"
    ])

    nt_phuyen = image_to_data_uri([
        "kho_anh/trang_chu/noi_bat/trung/phuyen.png",
        "kho_anh/trang_chu/noi_bat/trung/phuyen.jpg",
        "kho_anh/trang_chu/noi_bat/trung/phuyen.jpeg",
        "kho_anh/trang_chu/noi_bat/trung/phuyen.webp"
    ])

    nt_binhdinh = image_to_data_uri([
        "kho_anh/trang_chu/noi_bat/trung/binhdinh.png",
        "kho_anh/trang_chu/noi_bat/trung/binhdinh.jpg",
        "kho_anh/trang_chu/noi_bat/trung/binhdinh.jpeg",
        "kho_anh/trang_chu/noi_bat/trung/binhdinh.webp"
    ])

    nt_quangbinh = image_to_data_uri([
        "kho_anh/trang_chu/noi_bat/trung/quangbinh.png",
        "kho_anh/trang_chu/noi_bat/trung/quangbinh.jpg",
        "kho_anh/trang_chu/noi_bat/trung/quangbinh.jpeg",
        "kho_anh/trang_chu/noi_bat/trung/quangbinh.webp"
    ])

    nt_thanhhoa = image_to_data_uri([
        "kho_anh/trang_chu/noi_bat/trung/thanhhoa.png",
        "kho_anh/trang_chu/noi_bat/trung/thanhhoa.jpg",
        "kho_anh/trang_chu/noi_bat/trung/thanhhoa.jpeg",
        "kho_anh/trang_chu/noi_bat/trung/thanhhoa.webp"
    ])

    nt_nghean = image_to_data_uri([
        "kho_anh/trang_chu/noi_bat/trung/nghean.png",
        "kho_anh/trang_chu/noi_bat/trung/nghean.jpg",
        "kho_anh/trang_chu/noi_bat/trung/nghean.jpeg",
        "kho_anh/trang_chu/noi_bat/trung/nghean.webp"
    ])

    # Miền Nam
    nn_hochiminh = image_to_data_uri([
        "kho_anh/trang_chu/noi_bat/nam/hochiminh.png",
        "kho_anh/trang_chu/noi_bat/nam/hochiminh.jpg",
        "kho_anh/trang_chu/noi_bat/nam/hochiminh.jpeg",
        "kho_anh/trang_chu/noi_bat/nam/hochiminh.webp"
    ])

    nn_kiengiang = image_to_data_uri([
        "kho_anh/trang_chu/noi_bat/nam/kiengiang.png",
        "kho_anh/trang_chu/noi_bat/nam/kiengiang.jpg",
        "kho_anh/trang_chu/noi_bat/nam/kiengiang.jpeg",
        "kho_anh/trang_chu/noi_bat/nam/kiengiang.webp"
    ])

    nn_lamdong = image_to_data_uri([
        "kho_anh/trang_chu/noi_bat/nam/lamdong.png",
        "kho_anh/trang_chu/noi_bat/nam/lamdong.jpg",
        "kho_anh/trang_chu/noi_bat/nam/lamdong.jpeg",
        "kho_anh/trang_chu/noi_bat/nam/lamdong.webp"
    ])

    nn_vungtau = image_to_data_uri([
        "kho_anh/trang_chu/noi_bat/nam/vungtau.png",
        "kho_anh/trang_chu/noi_bat/nam/vungtau.jpg",
        "kho_anh/trang_chu/noi_bat/nam/vungtau.jpeg",
        "kho_anh/trang_chu/noi_bat/nam/vungtau.webp"
    ])

    nn_cantho = image_to_data_uri([
        "kho_anh/trang_chu/noi_bat/nam/cantho.png",
        "kho_anh/trang_chu/noi_bat/nam/cantho.jpg",
        "kho_anh/trang_chu/noi_bat/nam/cantho.jpeg",
        "kho_anh/trang_chu/noi_bat/nam/cantho.webp"
    ])

    nn_angiang = image_to_data_uri([
        "kho_anh/trang_chu/noi_bat/nam/angiang.png",
        "kho_anh/trang_chu/noi_bat/nam/angiang.jpg",
        "kho_anh/trang_chu/noi_bat/nam/angiang.jpeg",
        "kho_anh/trang_chu/noi_bat/nam/angiang.webp"
    ])

    nn_tiengiang = image_to_data_uri([
        "kho_anh/trang_chu/noi_bat/nam/tiengiang.png",
        "kho_anh/trang_chu/noi_bat/nam/tiengiang.jpg",
        "kho_anh/trang_chu/noi_bat/nam/tiengiang.jpeg",
        "kho_anh/trang_chu/noi_bat/nam/tiengiang.webp"
    ])

    nn_bentre = image_to_data_uri([
        "kho_anh/trang_chu/noi_bat/nam/bentre.png",
        "kho_anh/trang_chu/noi_bat/nam/bentre.jpg",
        "kho_anh/trang_chu/noi_bat/nam/bentre.jpeg",
        "kho_anh/trang_chu/noi_bat/nam/bentre.webp"
    ])

    nn_dongthap = image_to_data_uri([
        "kho_anh/trang_chu/noi_bat/nam/dongthap.png",
        "kho_anh/trang_chu/noi_bat/nam/dongthap.jpg",
        "kho_anh/trang_chu/noi_bat/nam/dongthap.jpeg",
        "kho_anh/trang_chu/noi_bat/nam/dongthap.webp"
    ])

    # Điểm đến yêu thích
    components.html(dedent(f"""
    <style>
    body {{
        margin: 0;
        font-family: Arial, sans-serif;
    }}

    .favorite-section {{
        width: 100%;
        padding: 24px 0;
        box-sizing: border-box;
    }}

    .favorite-container {{
        max-width: 1350px;
        margin: 0 auto;
        padding: 0 18px;
        box-sizing: border-box;
    }}

    .favorite-title {{
        text-align: center;
        font-size: 35px;
        font-weight: 900;
        color: #1565c0;
        text-transform: uppercase;
        margin-bottom: 8px;
        line-height: 1.3;
    }}

    .favorite-line {{
        width: 150px;
        height: 4px;
        background: #1565c0;
        border-radius: 999px;
        margin: 0 auto 18px auto;
    }}

    .favorite-desc {{
        text-align: center;
        max-width: 820px;
        margin: 0 auto 24px auto;
        font-size: 18px;
        line-height: 1.8;
        color: #374151;
    }}

    .favorite-tabs {{
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 36px;
        margin-bottom: 28px;
    }}

    .favorite-tab {{
        position: relative;
        font-size: 17px;
        font-weight: 700;
        color: #374151;
        padding-bottom: 8px;
        cursor: pointer;
        transition: 0.25s ease;
    }}

    .favorite-tab:hover {{
        color: #1565c0;
    }}

    .favorite-tab.active {{
        color: #1565c0;
    }}

    .favorite-tab.active::after {{
        content: "";
        position: absolute;
        left: 0;
        bottom: 0;
        width: 100%;
        height: 3px;
        border-radius: 999px;
        background: #1565c0;
    }}

    .favorite-grid {{
        display: grid;
        grid-template-columns: 1.35fr 1.05fr 1.05fr 1.05fr;
        grid-template-rows: 180px 180px 220px;
        gap: 10px;
    }}

    /* CARD */
    .favorite-card {{
        position: relative;
        overflow: hidden;
        border-radius: 16px;
        min-height: 180px;
        background-size: cover;
        background-position: center;
        box-shadow: 0 6px 18px rgba(0,0,0,0.08);
        isolation: isolate;
        opacity: 1;
        transform: translateY(0);
        transition: opacity 0.35s ease, transform 0.35s ease;
    }}

    .favorite-card.fade-out {{
        opacity: 0;
        transform: translateY(8px);
    }}

    .favorite-card::before {{
        content: "";
        position: absolute;
        inset: 0;
        background-image: inherit;
        background-size: cover;
        background-position: center;
        transform: scale(1);
        transition: transform 0.5s ease;
        z-index: 0;
    }}

    .favorite-overlay {{
        position: absolute;
        inset: 0;
        background: linear-gradient(to top, rgba(0,0,0,0.55), rgba(0,0,0,0.12));
        transition: 0.35s ease;
        z-index: 1;
    }}

    .favorite-content {{
        position: absolute;
        inset: 0;
        z-index: 2;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 18px;
        text-align: center;
        color: #fff;
    }}

    .favorite-name {{
        margin: 0;
        font-size: 18px;
        font-weight: 800;
        text-transform: uppercase;
        line-height: 1.3;
        transition: 0.35s ease;
    }}

    .favorite-content {{
        position: absolute;
        inset: 0;
        z-index: 2;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 18px;
        text-align: center;
        color: #fff;
    }}

    .favorite-name {{
        margin: 0;
        font-size: 18px;
        font-weight: 800;
        text-transform: uppercase;
        line-height: 1.3;
        transition: 0.35s ease;
    }}

    .favorite-info {{
        margin-top: 12px;
        max-width: 88%;
        font-size: 14px;
        line-height: 1.6;
        color: #ffffff;
        opacity: 0;
        transform: translateY(12px);
        transition: 0.35s ease;
        display: -webkit-box;
        -webkit-line-clamp: 4;
        -webkit-box-orient: vertical;
        overflow: hidden;
        text-shadow: 0 2px 8px rgba(0,0,0,0.35);
    }}

.favorite-card:hover::before {{
    transform: scale(1.08);
}}

.favorite-card:hover .favorite-overlay {{
    background: linear-gradient(to top, rgba(0,0,0,0.78), rgba(0,0,0,0.28));
}}

.favorite-card:hover .favorite-name {{
    transform: translateY(-8px);
}}

.favorite-card:hover .favorite-info {{
    opacity: 1;
    transform: translateY(0);
}}

    /* vị trí từng card */
    .card-1 {{
        grid-column: 1 / 2;
        grid-row: 1 / 3;
    }}

    .card-2 {{
        grid-column: 2 / 3;
        grid-row: 1 / 2;
    }}

    .card-3 {{
        grid-column: 3 / 5;
        grid-row: 1 / 2;
    }}

    .card-4 {{
        grid-column: 2 / 3;
        grid-row: 2 / 3;
    }}

    .card-5 {{
        grid-column: 3 / 4;
        grid-row: 2 / 3;
    }}

    .card-6 {{
        grid-column: 4 / 5;
        grid-row: 2 / 4;
    }}

    .card-7 {{
        grid-column: 1 / 2;
        grid-row: 3 / 4;
    }}

    .card-8 {{
        grid-column: 2 / 3;
        grid-row: 3 / 4;
    }}

    .card-9 {{
        grid-column: 3 / 4;
        grid-row: 3 / 4;
    }}

    @media (max-width: 1100px) {{
        .favorite-grid {{
            grid-template-columns: 1fr 1fr 1fr;
            grid-template-rows: 220px 220px 220px;
        }}

        .card-1 {{ grid-column: 1 / 2; grid-row: 1 / 3; }}
        .card-2 {{ grid-column: 2 / 3; grid-row: 1 / 2; }}
        .card-3 {{ grid-column: 3 / 4; grid-row: 1 / 2; }}
        .card-4 {{ grid-column: 2 / 3; grid-row: 2 / 3; }}
        .card-5 {{ grid-column: 3 / 4; grid-row: 2 / 3; }}
        .card-6 {{ grid-column: 1 / 2; grid-row: 3 / 4; }}
        .card-7 {{ grid-column: 2 / 3; grid-row: 3 / 4; }}
        .card-8 {{ grid-column: 3 / 4; grid-row: 3 / 4; }}
        .card-9 {{ display: none; }}
    }}

    @media (max-width: 768px) {{
        .favorite-container {{
            padding: 0 14px;
        }}

        .favorite-title {{
            font-size: 26px;
        }}

        .favorite-desc {{
            font-size: 15px;
            line-height: 1.7;
        }}

        .favorite-tabs {{
            gap: 18px;
        }}

        .favorite-tab {{
            font-size: 15px;
        }}

        .favorite-grid {{
            grid-template-columns: 1fr;
            grid-template-rows: none;
        }}

        .favorite-card,
        .card-1, .card-2, .card-3, .card-4, .card-5, .card-6, .card-7, .card-8, .card-9 {{
            grid-column: auto;
            grid-row: auto;
            min-height: 250px;
        }}

        .card-9 {{
            display: block;
        }}
    }}
    </style>

    <div class="favorite-section">
        <div class="favorite-container">

            <div class="favorite-title">Điểm đến nổi bật</div>
            <div class="favorite-line"></div>

            <div class="favorite-desc">
                Các điểm đến tiêu biểu cùng những thông tin hữu ích về thiên nhiên, văn hóa, con người và các hành trình trải nghiệm nổi bật tại mỗi vùng miền.
            </div>

            <div class="favorite-tabs">
                <div class="favorite-tab active" data-region="north">Miền Bắc</div>
                <div class="favorite-tab" data-region="central">Miền Trung</div>
                <div class="favorite-tab" data-region="south">Miền Nam</div>
            </div>

            <div class="favorite-grid" id="favoriteGrid">
                <div class="favorite-card card-1">
                    <div class="favorite-overlay"></div>
                    <div class="favorite-content">
                        <div class="favorite-name"></div>
                        <div class="favorite-info"></div>
                    </div>
                </div>

                <div class="favorite-card card-2">
                    <div class="favorite-overlay"></div>
                    <div class="favorite-content">
                        <div class="favorite-name"></div>
                        <div class="favorite-info"></div>
                    </div>
                </div>

                <div class="favorite-card card-3">
                    <div class="favorite-overlay"></div>
                    <div class="favorite-content">
                        <div class="favorite-name"></div>
                        <div class="favorite-info"></div>
                    </div>
                </div>

                <div class="favorite-card card-4">
                    <div class="favorite-overlay"></div>
                    <div class="favorite-content">
                        <div class="favorite-name"></div>
                        <div class="favorite-info"></div>
                    </div>
                </div>

                <div class="favorite-card card-5">
                    <div class="favorite-overlay"></div>
                    <div class="favorite-content">
                        <div class="favorite-name"></div>
                        <div class="favorite-info"></div>
                    </div>
                </div>

                <div class="favorite-card card-6">
                    <div class="favorite-overlay"></div>
                    <div class="favorite-content">
                        <div class="favorite-name"></div>
                        <div class="favorite-info"></div>
                    </div>
                </div>

                <div class="favorite-card card-7">
                    <div class="favorite-overlay"></div>
                    <div class="favorite-content">
                        <div class="favorite-name"></div>
                        <div class="favorite-info"></div>
                    </div>
                </div>

                <div class="favorite-card card-8">
                    <div class="favorite-overlay"></div>
                    <div class="favorite-content">
                        <div class="favorite-name"></div>
                        <div class="favorite-info"></div>
                    </div>
                </div>

                <div class="favorite-card card-9">
                    <div class="favorite-overlay"></div>
                    <div class="favorite-content">
                        <div class="favorite-name"></div>
                        <div class="favorite-info"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
    const destinationData = {{
        north: [
            {{
                name: "Quảng Ninh",
                image: "{nb_quangninh}",
                info: "Nổi tiếng với Vịnh Hạ Long, Quảng Ninh là điểm đến hấp dẫn với cảnh biển đảo kỳ vĩ, thiên nhiên đặc sắc và nhiều trải nghiệm du lịch đáng nhớ."
            }},
            {{
                name: "Hà Giang",
                image: "{nb_hagiang}",
                info: "Hà Giang gây ấn tượng bởi núi non hùng vĩ, những cung đèo nổi tiếng, bản làng vùng cao và vẻ đẹp hoang sơ đậm chất miền đá."
            }},
            {{
                name: "Lào Cai",
                image: "{nb_laocai}",
                info: "Lào Cai là vùng đất hội tụ vẻ đẹp của núi rừng Tây Bắc, nổi bật với Sa Pa, Fansipan, ruộng bậc thang và bản sắc văn hóa dân tộc đặc sắc."
            }},
            {{
                name: "Ninh Bình",
                image: "{nb_ninhbinh}",
                info: "Ninh Bình thu hút du khách bởi quần thể danh thắng Tràng An, Tam Cốc, Hang Múa và khung cảnh non nước hữu tình như tranh vẽ."
            }},
            {{
                name: "Yên Bái",
                image: "{nb_yenbai}",
                info: "Yên Bái được biết đến với Mù Cang Chải, những thửa ruộng bậc thang tuyệt đẹp cùng vẻ đẹp bình dị, thơ mộng của núi rừng Tây Bắc."
            }},
            {{
                name: "Sơn La",
                image: "{nb_sonla}",
                info: "Sơn La nổi bật với Mộc Châu xanh mát, đồi chè trải dài, mùa hoa rực rỡ và không khí trong lành, dễ chịu quanh năm."
            }},
            {{
                name: "Cao Bằng",
                image: "{nb_caobang}",
                info: "Cao Bằng là vùng đất biên giới nổi tiếng với thác Bản Giốc, động Ngườm Ngao và cảnh quan thiên nhiên hùng vĩ, nguyên sơ."
            }},
            {{
                name: "Hải Phòng",
                image: "{nb_haiphong}",
                info: "Hải Phòng là thành phố cảng sôi động, hấp dẫn du khách với Cát Bà, Đồ Sơn, ẩm thực hải sản phong phú và nhịp sống trẻ trung."
            }},
            {{
                name: "Hà Nội",
                image: "{nb_hanoi}",
                info: "Hà Nội là thủ đô ngàn năm văn hiến, nổi bật với Hồ Gươm, phố cổ, Văn Miếu và sự giao thoa hài hòa giữa truyền thống với hiện đại."
            }}
        ],

        central: [
            {{
                name: "Huế",
                image: "{nt_hue}",
                info: "Huế mang vẻ đẹp trầm mặc và sâu lắng, nổi tiếng với Đại Nội, lăng tẩm triều Nguyễn, chùa Thiên Mụ và nền văn hóa giàu bản sắc."
            }},
            {{
                name: "Đà Nẵng",
                image: "{nt_danang}",
                info: "Đà Nẵng là thành phố biển hiện đại, nổi bật với cầu Rồng, biển Mỹ Khê, Bà Nà Hills và môi trường du lịch năng động, văn minh."
            }},
            {{
                name: "Quảng Nam",
                image: "{nt_quangnam}",
                info: "Quảng Nam hấp dẫn bởi phố cổ Hội An, thánh địa Mỹ Sơn, các làng nghề truyền thống và vẻ đẹp văn hóa đậm chất miền Trung."
            }},
            {{
                name: "Nha Trang",
                image: "{nt_nhatrang}",
                info: "Nha Trang là điểm đến lý tưởng với biển xanh, cát trắng, nhiều hòn đảo đẹp, hải sản phong phú và không khí nghỉ dưỡng sôi động."
            }},
            {{
                name: "Phú Yên",
                image: "{nt_phuyen}",
                info: "Phú Yên gây ấn tượng bởi vẻ đẹp hoang sơ, yên bình với Gành Đá Đĩa, Bãi Xép và khung cảnh biển trời trong trẻo, thơ mộng."
            }},
            {{
                name: "Bình Định",
                image: "{nt_binhdinh}",
                info: "Bình Định nổi tiếng với Quy Nhơn, Eo Gió, Kỳ Co cùng sự kết hợp hài hòa giữa cảnh đẹp biển trời và truyền thống võ cổ truyền."
            }},
            {{
                name: "Quảng Bình",
                image: "{nt_quangbinh}",
                info: "Quảng Bình được mệnh danh là vương quốc hang động với Phong Nha - Kẻ Bàng, thiên nhiên hùng vĩ và nhiều kỳ quan độc đáo."
            }},
            {{
                name: "Thanh Hóa",
                image: "{nt_thanhhoa}",
                info: "Thanh Hóa sở hữu nhiều điểm đến nổi bật như biển Sầm Sơn, thành nhà Hồ, suối cá Cẩm Lương và dấu ấn lịch sử lâu đời."
            }},
            {{
                name: "Nghệ An",
                image: "{nt_nghean}",
                info: "Nghệ An là vùng đất giàu truyền thống văn hóa và lịch sử, nổi bật với quê Bác, biển Cửa Lò và vẻ đẹp mộc mạc của xứ Nghệ."
            }}
        ],

        south: [
            {{
                name: "TP. Hồ Chí Minh",
                image: "{nn_hochiminh}",
                info: "TP. Hồ Chí Minh là trung tâm kinh tế sôi động bậc nhất cả nước, nổi bật với nhịp sống hiện đại, các công trình biểu tượng và sức trẻ năng động."
            }},
            {{
                name: "Kiên Giang",
                image: "{nn_kiengiang}",
                info: "Kiên Giang, đặc biệt là Phú Quốc, nổi tiếng với biển xanh, cát trắng, hoàng hôn đẹp, làng chài truyền thống và nhiều khu nghỉ dưỡng hấp dẫn."
            }},
            {{
                name: "Lâm Đồng",
                image: "{nn_lamdong}",
                info: "Lâm Đồng với thành phố Đà Lạt mang vẻ đẹp dịu dàng, thơ mộng, nổi bật bởi khí hậu mát mẻ, đồi thông, hồ nước và muôn vàn loài hoa."
            }},
            {{
                name: "Bà Rịa - Vũng Tàu",
                image: "{nn_vungtau}",
                info: "Bà Rịa - Vũng Tàu là điểm đến quen thuộc với du khách yêu biển, nổi bật với bãi tắm đẹp, hải sản ngon và không khí nghỉ dưỡng thoải mái."
            }},
            {{
                name: "Cần Thơ",
                image: "{nn_cantho}",
                info: "Cần Thơ là đô thị trung tâm của miền Tây Nam Bộ, nổi tiếng với chợ nổi Cái Răng, bến Ninh Kiều và nét văn hóa sông nước đặc trưng."
            }},
            {{
                name: "An Giang",
                image: "{nn_angiang}",
                info: "An Giang thu hút du khách với rừng tràm Trà Sư, núi Cấm, miếu Bà Chúa Xứ và vẻ đẹp giao hòa giữa thiên nhiên với văn hóa tâm linh."
            }},
            {{
                name: "Tiền Giang",
                image: "{nn_tiengiang}",
                info: "Tiền Giang hấp dẫn bởi những cù lao xanh mát, vườn trái cây trù phú, chợ nổi và trải nghiệm đậm chất miền sông nước Nam Bộ."
            }},
            {{
                name: "Bến Tre",
                image: "{nn_bentre}",
                info: "Bến Tre nổi tiếng là xứ dừa với hệ thống kênh rạch xanh mát, làng nghề truyền thống và nhịp sống miệt vườn thanh bình, gần gũi."
            }},
            {{
                name: "Đồng Tháp",
                image: "{nn_dongthap}",
                info: "Đồng Tháp ghi dấu ấn với đất sen hồng, làng hoa Sa Đéc, khu sinh thái đặc sắc và vẻ đẹp mộc mạc, yên bình của miền Tây."
            }}
        ]
    }};

    const tabs = document.querySelectorAll(".favorite-tab");
    const cards = document.querySelectorAll(".favorite-card");

    function renderRegion(regionKey) {{
        const data = destinationData[regionKey];

        cards.forEach(card => card.classList.add("fade-out"));

        setTimeout(() => {{
            cards.forEach((card, index) => {{
                card.style.backgroundImage = `url('${{data[index].image}}')`;
                card.querySelector(".favorite-name").textContent = data[index].name;
                card.querySelector(".favorite-info").textContent = data[index].info;
                card.classList.remove("fade-out");
            }});
        }}, 220);
    }}

    tabs.forEach(tab => {{
        tab.addEventListener("click", () => {{
            tabs.forEach(item => item.classList.remove("active"));
            tab.classList.add("active");
            renderRegion(tab.dataset.region);
        }});
    }});

    renderRegion("north");
    </script>
    """), height=900, scrolling=False)

    # Footer
    home_logo_src = image_to_data_uri([
        "assets/anime_teamtrangchu.png",
        "anime_teamtrangchu.png",
        "assets/anime_teamtrangchu.jpg",
        "anime_teamtrangchu.jpg",
        "assets/anime_teamtrangchu.jpeg",
        "anime_teamtrangchu.jpeg",
        "assets/anime_teamtrangchu.webp",
        "anime_teamtrangchu.webp"
    ]) or "https://dummyimage.com/400x400/f8fafc/94a3b8.png&text=LOGO"

    vitri_icon_src = image_to_data_uri([
        "assets/vitri.png", "vitri.png",
        "assets/vitri.jpg", "vitri.jpg",
        "assets/vitri.jpeg", "vitri.jpeg",
        "assets/vitri.webp", "vitri.webp"
    ])

    email_icon_src = image_to_data_uri([
        "assets/email.png", "email.png",
        "assets/email.jpg", "email.jpg",
        "assets/email.jpeg", "email.jpeg",
        "assets/email.webp", "email.webp"
    ])

    dienthoai_icon_src = image_to_data_uri([
        "assets/dienthoai.png", "dienthoai.png",
        "assets/dienthoai.jpg", "dienthoai.jpg",
        "assets/dienthoai.jpeg", "dienthoai.jpeg",
        "assets/dienthoai.webp", "dienthoai.webp"
    ])

    facebook_icon_src = image_to_data_uri([
        "assets/facebook.png", "facebook.png",
        "assets/facebook.jpg", "facebook.jpg",
        "assets/facebook.jpeg", "facebook.jpeg",
        "assets/facebook.webp", "facebook.webp"
    ])

    tiktok_icon_src = image_to_data_uri([
        "assets/tiktok.png", "tiktok.png",
        "assets/tiktok.jpg", "tiktok.jpg",
        "assets/tiktok.jpeg", "tiktok.jpeg",
        "assets/tiktok.webp", "tiktok.webp"
    ])

    youtube_icon_src = image_to_data_uri([
        "assets/youtube.png", "youtube.png",
        "assets/youtube.jpg", "youtube.jpg",
        "assets/youtube.jpeg", "youtube.jpeg",
        "assets/youtube.webp", "youtube.webp"
    ])

    zalo_icon_src = image_to_data_uri([
        "assets/zalo.png", "zalo.png",
        "assets/zalo.jpg", "zalo.jpg",
        "assets/zalo.jpeg", "zalo.jpeg",
        "assets/zalo.webp", "zalo.webp"
    ])

    facebook_icon_html = f'<img class="social-icon" src="{facebook_icon_src}" alt="Facebook">' if facebook_icon_src else "f"
    tiktok_icon_html = f'<img class="social-icon" src="{tiktok_icon_src}" alt="TikTok">' if tiktok_icon_src else "♪"
    youtube_icon_html = f'<img class="social-icon" src="{youtube_icon_src}" alt="YouTube">' if youtube_icon_src else "▶"
    zalo_icon_html = f'<img class="social-icon" src="{zalo_icon_src}" alt="Zalo">' if zalo_icon_src else "z"

    facebook_link = "https://www.facebook.com/share/1CubUJMiYU/"
    tiktok_link = "https://www.tiktok.com/@minhkhoadayyy?is_from_webapp=1&sender_device=pc"
    youtube_link = "http://www.youtube.com/@MINHKHOALT"
    zalo_link = "https://zalo.me/0346538917"

    facebook_href = escape(facebook_link, quote=True)
    tiktok_href = escape(tiktok_link, quote=True)
    youtube_href = escape(youtube_link, quote=True)
    zalo_href = escape(zalo_link, quote=True)

    vitri_icon_html = f'<img class="info-icon" src="{vitri_icon_src}" alt="Vị trí">' if vitri_icon_src else "📍"
    email_icon_html = f'<img class="info-icon" src="{email_icon_src}" alt="Email">' if email_icon_src else "✉️"
    dienthoai_icon_html = f'<img class="info-icon" src="{dienthoai_icon_src}" alt="Điện thoại">' if dienthoai_icon_src else "📞"

    project_title = "LAO CAI HERITAGE AI"
    project_subtitle = (
        "Là sản phẩm số giúp giới thiệu điểm đến, lịch trình và giá trị văn hóa "
        "Lào Cai bằng giao diện trực quan kết hợp AI."
    )

    contact_address = "Khánh Yên, Lào Cai, Việt Nam"
    contact_email = "khoagaming999@gmail.com"
    contact_phone = "0346 538 917"

    components.html(f"""
    <style>
    * {{
        box-sizing: border-box;
    }}

    html, body {{
        margin: 0;
        padding: 0;
        background: transparent;
        font-family: Inter, Arial, sans-serif;
    }}

    .about-contact-wrap {{
        max-width: 1600px;
        margin: 56px auto 28px auto;
        padding: 0 16px;
    }}

    .about-contact {{
        position: relative;
        overflow: hidden;
        border-radius: 34px;
        padding: 34px;
        background:
            radial-gradient(circle at top left, rgba(255,255,255,0.18), transparent 28%),
            linear-gradient(135deg, #6f829e 0%, #8799b3 35%, #b9c6d6 100%);
        box-shadow: 0 20px 52px rgba(15,23,42,0.16);
    }}

    .about-contact::before {{
        content: "";
        position: absolute;
        width: 320px;
        height: 320px;
        border-radius: 50%;
        background: rgba(255,255,255,0.08);
        top: -140px;
        right: -80px;
    }}

    .about-contact::after {{
        content: "";
        position: absolute;
        width: 240px;
        height: 240px;
        border-radius: 50%;
        background: rgba(255,255,255,0.06);
        bottom: -110px;
        left: -70px;
    }}

    .about-contact-grid {{
        position: relative;
        z-index: 2;
        display: grid;
        grid-template-columns: 1.08fr 0.92fr;
        gap: 34px;
        align-items: stretch;
    }}

    .about-left {{
        color: #ffffff;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}

    .brand-row {{
        display: flex;
        gap: 22px;
        align-items: center;
        margin-bottom: 22px;
    }}

    .brand-logo {{
        width: 176px;
        height: 176px;
        min-width: 176px;
        border-radius: 50%;
        overflow: hidden;
        border: 5px solid rgba(255,255,255,0.68);
        box-shadow: 0 12px 28px rgba(0,0,0,0.16);
        background: rgba(255,255,255,0.16);
    }}

    .brand-logo img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
    }}

    .brand-title {{
        font-size: 48px;
        line-height: 1.02;
        font-weight: 900;
        margin: 0 0 12px 0;
        letter-spacing: 0.01em;
        color: #ffffff;
    }}

    .brand-subtitle {{
        font-size: 18px;
        line-height: 1.82;
        color: rgba(255,255,255,0.94);
        max-width: 540px;
    }}

    .brand-line {{
        width: 190px;
        height: 4px;
        margin: 18px 0 0 0;
        border-radius: 999px;
        background: linear-gradient(90deg, rgba(255,255,255,0.92), rgba(255,255,255,0.18));
    }}

    .about-bottom {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 24px;
        margin-top: 12px;
    }}

    .info-box {{
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 24px;
        padding: 20px 22px;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
    }}
                    
    .social-row {{
        display: flex;
        flex-wrap: nowrap;
        align-items: center;
        justify-content: center;
        gap: 16px;
        margin-top: 10px;
    }}

    .info-title {{
        font-size: 27px;
        font-weight: 900;
        margin-bottom: 14px;
        color: #ffffff;            
        text-align: center;
        width: 100%;
    }}

    .info-item{{
        display:flex;
        align-items:center;
        gap:10px;
        font-size:20px;
        line-height:1.9;
        color:rgba(255,255,255,0.93);
    }}

    .info-icon{{
        width:18px;
        height:18px;
        object-fit:contain;
        display:block;
        flex-shrink:0;
    }}

    .social-row {{
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-top: 8px;
    }}

    .social-btn{{
        width:54px;
        height:54px;
        border-radius:50%;
        display:flex;
        align-items:center;
        justify-content:center;
        background:#ffffff;
        color:#253247;
        font-size:16px;
        font-weight:900;
        box-shadow:0 8px 18px rgba(0,0,0,0.12);
        overflow:hidden;
        flex-shrink:0;
        text-decoration:none;
        cursor:pointer;
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }}

    .social-btn:hover{{
        transform: translateY(-2px);
        box-shadow:0 12px 24px rgba(0,0,0,0.16);
    }}

    .social-icon{{
        width:24px;
        height:24px;
        object-fit:contain;
        display:block;
    }}

    .about-right {{
        display: flex;
        align-items: center;
    }}

    .form-card {{
        width: 100%;
        background: rgba(255,255,255,0.28);
        border: 1px solid rgba(255,255,255,0.28);
        border-radius: 30px;
        padding: 16px;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.34);
    }}

    .form-inner {{
        background: rgba(255,255,255,0.76);
        border-radius: 24px;
        padding: 18px;
    }}

    .form-row {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 14px;
        margin-bottom: 14px;
    }}

    .input,
    .textarea {{
        width: 100%;
        border: 1px solid rgba(148,163,184,0.28);
        background: rgba(255,255,255,0.94);
        border-radius: 16px;
        padding: 14px 16px;
        font-size: 15px;
        color: #0f172a;
        outline: none;
    }}

    .input::placeholder,
    .textarea::placeholder {{
        color: #94a3b8;
    }}

    .input:focus,
    .textarea:focus {{
        border-color: #8ca8c7;
        box-shadow: 0 0 0 3px rgba(140,168,199,0.14);
    }}

    .textarea {{
        min-height: 210px;
        resize: none;
        margin-bottom: 16px;
    }}

    .submit-wrap {{
        display: flex;
        justify-content: center;
    }}

    .submit-btn {{
        border: none;
        min-width: 180px;
        height: 50px;
        border-radius: 999px;
        background: linear-gradient(135deg, #d8dde6 0%, #bcc6d4 100%);
        color: #3f4b5d;
        font-size: 22px;
        font-weight: 800;
        cursor: pointer;
        box-shadow: 0 10px 22px rgba(15,23,42,0.10);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }}

    .submit-btn:hover {{
        transform: translateY(-1px);
        box-shadow: 0 14px 26px rgba(15,23,42,0.14);
    }}
                    
    .feedback-status {{
        margin-top: 12px;
        text-align: center;
        font-size: 14px;
        font-weight: 700;
        color: #475569;
        min-height: 20px;
    }}

    @media (max-width: 1100px) {{
        .about-contact-grid {{
            grid-template-columns: 1fr;
        }}

        .brand-title {{
            font-size: 42px;
        }}
    }}

    @media (max-width: 720px) {{
        .about-contact {{
            padding: 22px 18px;
            border-radius: 26px;
        }}

        .brand-row {{
            flex-direction: column;
            align-items: flex-start;
        }}

        .brand-logo {{
            width: 142px;
            height: 142px;
            min-width: 142px;
        }}

        .brand-title {{
            font-size: 34px;
        }}

        .about-bottom,
        .form-row {{
            grid-template-columns: 1fr;
        }}

        .textarea {{
            min-height: 180px;
        }}
    }}
    </style>

    <div class="about-contact-wrap">
        <div class="about-contact">
            <div class="about-contact-grid">

                <div class="about-left">
                    <div class="brand-row">
                        <div class="brand-logo">
                            <img src="{home_logo_src}" alt="Lao Cai Heritage AI">
                        </div>

                        <div>
                            <h2 class="brand-title">{escape(project_title)}</h2>
                            <div class="brand-subtitle">{escape(project_subtitle)}</div>
                            <div class="brand-line"></div>
                        </div>
                    </div>

                    <div class="about-bottom">
                        <div class="info-box">
                            <div class="info-title">Liên hệ</div>
                            <div class="info-item">{vitri_icon_html} Khánh Yên, Lào Cai, Việt Nam</div>
                            <div class="info-item">{email_icon_html} khoagaming999@gmail.com</div>
                            <div class="info-item">{dienthoai_icon_html} 0346 538 917</div>
                        </div>
                        <div class="info-box">
                            <div class="info-title">Mạng xã hội</div>
                            <div class="social-row">
                                <a class="social-btn" href="{facebook_href}" target="_blank" rel="noopener noreferrer">{facebook_icon_html}</a>
                                <a class="social-btn" href="{tiktok_href}" target="_blank" rel="noopener noreferrer">{tiktok_icon_html}</a>
                                <a class="social-btn" href="{youtube_href}" target="_blank" rel="noopener noreferrer">{youtube_icon_html}</a>
                                <a class="social-btn" href="{zalo_href}" target="_blank" rel="noopener noreferrer">{zalo_icon_html}</a>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="about-right">
                    <div class="form-card">
                        <div class="form-inner">

                            <iframe
                                id="feedback_hidden_frame"
                                name="feedback_hidden_frame"
                                style="display:none;"
                            ></iframe>

                            <form
                                id="feedback-form"
                                action="https://script.google.com/macros/s/AKfycbyqh-jHTAxvtDB4aTgA_vJfsHq9PLS_QI-AH-zH0LWVbjY0XRRsMXN7XXTJiUzdRgzbLw/exec"
                                method="POST"
                                target="feedback_hidden_frame"
                                onsubmit="return submitFeedbackForm(this);"
                            >
                                <div class="form-row">
                                    <input class="input" name="name" type="text" placeholder="Họ tên" required>
                                    <input class="input" name="email" type="email" placeholder="Gmail.com" required>
                                </div>

                                <textarea class="textarea" name="message" placeholder="Nội dung..." required></textarea>

                                <input type="hidden" name="to_email" value="khoagaming999@gmail.com">

                                <div class="submit-wrap">
                                    <button id="feedback-submit-btn" class="submit-btn" type="submit">Gửi</button>
                                </div>

                                <div id="feedback-status" class="feedback-status"></div>
                            </form>

                        </div>
                    </div>
                </div>

                <script>
                let feedbackSubmitting = false;
                let feedbackFormRef = null;

                const feedbackFrame = document.getElementById("feedback_hidden_frame");

                if (feedbackFrame) {{
                    feedbackFrame.addEventListener("load", function () {{
                        if (!feedbackSubmitting || !feedbackFormRef) {{
                            return;
                        }}

                        const status = document.getElementById("feedback-status");
                        const btn = document.getElementById("feedback-submit-btn");

                        status.textContent = "Đã gửi góp ý thành công.";
                        feedbackFormRef.reset();

                        btn.disabled = false;
                        btn.style.opacity = "1";
                        btn.style.cursor = "pointer";

                        feedbackSubmitting = false;
                        feedbackFormRef = null;
                    }});
                }}

                function submitFeedbackForm(form) {{
                    const name = (form.name.value || "").trim();
                    const email = (form.email.value || "").trim();
                    const message = (form.message.value || "").trim();

                    const status = document.getElementById("feedback-status");
                    const btn = document.getElementById("feedback-submit-btn");

                    if (!name || !email || !message) {{
                        status.textContent = "Vui lòng nhập đầy đủ thông tin.";
                        return false;
                    }}

                    status.textContent = "Đang gửi...";
                    btn.disabled = true;
                    btn.style.opacity = "0.7";
                    btn.style.cursor = "not-allowed";

                    feedbackSubmitting = true;
                    feedbackFormRef = form;
                    return true;
                }}
                </script>

            </div>
        </div>
    </div>
    """, height=640, scrolling=False)

elif page == "lichtrinh":
    import json
    import math
    import re
    import unicodedata
    from html import escape
    import streamlit.components.v1 as components

    try:
        with open("lichtrinh.json", "r", encoding="utf-8") as f:
            lichtrinh_data = json.load(f)
    except Exception as e:
        st.error(f"Lỗi đọc file lichtrinh.json: {e}")
        st.stop()

    def safe_text(value, fallback="Đang cập nhật"):
        text = str(value).strip() if value is not None else ""
        return escape(text) if text else escape(fallback)

    def normalize_text(value):
        return str(value or "").strip().lower()

    def extract_price(value):
        if value is None:
            return 0
        digits = re.findall(r"\d+", str(value).replace(".", "").replace(",", ""))
        return int("".join(digits)) if digits else 0
    
    def safe_url(value, fallback="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1600&auto=format&fit=crop"):
        text = str(value).strip() if value is not None else ""
        return escape(text if text else fallback, quote=True)

    def itinerary_image(item):
        for key in ["image", "cover", "thumbnail", "hero_image", "banner_image"]:
            value = str(item.get(key, "")).strip()
            if value:
                return value
        return "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1600&auto=format&fit=crop"

    def make_slug(item):
        raw = str(item.get("slug", "")).strip()
        if raw:
            return raw

        text = f"{item.get('from', '')} {item.get('to', '')}"
        text = text.replace("Đ", "D").replace("đ", "d")
        text = unicodedata.normalize("NFD", text)
        text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
        text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
        return text or "lich-trinh"

    destination_options = ["Tất cả"] + sorted({item.get("to", "") for item in lichtrinh_data if item.get("to")})
    category_options = ["Tất cả"] + sorted({item.get("category", "") for item in lichtrinh_data if item.get("category")})

    total_routes = len(lichtrinh_data)
    lowest_price_all = min((extract_price(item.get("total_price")) for item in lichtrinh_data), default=0)
    hero_title = "Lịch trình du lịch Lào Cai"
    hero_subtitle = "Plan your trip smarter — chọn điểm đến, phong cách du lịch & ngân sách để nhận gợi ý tối ưu."

    st.markdown("""
    <style>
    .lt-hero-section{
        position: relative;
        height: 500px;
        background:
            linear-gradient(180deg, rgba(5, 18, 38, 0.20) 0%, rgba(6, 22, 43, 0.55) 100%),
            url('https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1600&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 0 24px 140px 24px;
        overflow: hidden;
    }

    .lt-hero-section::after{
        content:"";
        position:absolute;
        inset:0;
        background: radial-gradient(circle at top, rgba(255,255,255,0.14), transparent 38%);
        pointer-events:none;
    }

    .lt-hero-inner{
        position: relative;
        z-index: 2;
        max-width: 980px;
        color: #ffffff;
    }

    .lt-hero-kicker{
        display:inline-flex;
        align-items:center;
        justify-content:center;
        padding: 10px 18px;
        border-radius: 999px;
        background: rgba(255,255,255,0.16);
        border: 1px solid rgba(255,255,255,0.28);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        font-size: 14px;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 18px;
    }

    .lt-hero-title{
        font-size: 56px;
        font-weight: 900;
        line-height: 1.1;
        margin: 0;
        text-shadow: 0 6px 22px rgba(0,0,0,0.28);
    }

    .lt-hero-desc{
        max-width: 760px;
        margin: 16px auto 0 auto;
        font-size: 18px;
        line-height: 1.75;
        color: rgba(255,255,255,0.96);
        text-shadow: 0 4px 16px rgba(0,0,0,0.24);
    }

    .lt-hero-stats{
        display: flex;
        justify-content: center;
        gap: 14px;
        flex-wrap: wrap;
        margin-top: 24px;
    }

    .lt-hero-stat{
        min-width: 168px;
        padding: 14px 18px;
        border-radius: 18px;
        background: rgba(255,255,255,0.14);
        border: 1px solid rgba(255,255,255,0.24);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        box-shadow: 0 14px 30px rgba(0,0,0,0.10);
    }

    .lt-hero-stat-value{
        font-size: 22px;
        font-weight: 900;
        color: #ffffff;
        line-height: 1.15;
    }

    .lt-hero-stat-label{
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: rgba(255,255,255,0.78);
        margin-top: 6px;
    }

    .lt-form-intro{
        text-align: center;
        margin: -190px auto 0 auto;
        position: relative;
        z-index: 10;
    }

    .lt-form-title{
        font-size: 30px;
        font-weight: 900;
        color: #0f172a;
        margin: 14px 0 8px 0;
    }

    .lt-form-subtitle{
        font-size: 16px;
        line-height: 1.7;
        color: #475569;
        margin: 0 auto;
        max-width: 760px;
    }

    div[data-testid="stForm"]{
        position: relative;
        z-index: 20;
        margin-top: -160px;
        background: #ffffff;
        border: 1px solid rgba(15, 23, 42, 0.07);
        border-radius: 15px;
        padding: 20px 24px 22px 24px;
        box-shadow: 0 24px 54px rgba(15,23,42,0.12);
    }

    div[data-testid="stForm"] [data-testid="stHorizontalBlock"]{
        align-items: flex-end !important;
        gap: 14px !important;
    }

    div[data-testid="stColumn"]{
        display: flex;
        align-items: stretch;
    }

    div[data-testid="stColumn"] > div{
        width: 100%;
    }

    div[data-testid="stSelectbox"]{
        width: 100%;
        margin-bottom: 0 !important;
    }

    div[data-testid="stSelectbox"] label{
        min-height: 22px !important;
        display: flex !important;
        align-items: center !important;
        margin-bottom: 8px !important;
        line-height: 1.2 !important;
    }

    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
    div[data-testid="stTextInput"] input{
        min-height: 52px !important;
        border-radius: 16px !important;
        border: 1px solid #dbe4ef !important;
        background: #f8fafc !important;
        box-shadow: none !important;
        font-size: 15px !important;
        display: flex !important;
        align-items: center !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }

    div[data-testid="stFormSubmitButton"]{
        width: 100%;
        display: flex;
        align-items: flex-end;
        height: 100%;
    }

    div[data-testid="stFormSubmitButton"] button{
        width: 100%;
        min-height: 46px !important;
        margin-top: 0 !important;
        border-radius: 14px !important;
    }

    div[data-testid="stFormSubmitButton"] button{
        width: 100%;
        min-height: 52px;
        border: none !important;
        border-radius: 16px !important;
        background: linear-gradient(135deg, #1565c0 0%, #2b7fd3 100%) !important;
        color: #ffffff !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        letter-spacing: 0.02em;
        box-shadow: 0 16px 28px rgba(21,101,192,0.24) !important;
    }

    div[data-testid="stFormSubmitButton"] button:hover{
        background: linear-gradient(135deg, #0f4f9a 0%, #1565c0 100%) !important;
    }
                
    .lt-form-overlap{
        height: 0;
        margin-top: -145px;
    }

    @media (max-width: 991px){
        .lt-hero-section{
            height: 390px;
            padding-bottom: 82px;
        }

        .lt-hero-title{
            font-size: 44px;
        }

        .lt-form-title{
            font-size: 26px;
        }
    }

    @media (max-width: 767px){
        .lt-hero-section{
            height: 360px;
            padding: 0 16px 74px 16px;
        }

        .lt-hero-title{
            font-size: 34px;
        }

        .lt-hero-desc{
            font-size: 15px;
        }

        .lt-hero-stat{
            min-width: calc(50% - 8px);
            padding: 12px 14px;
        }

        .lt-form-intro{
            margin-top: -72px;
        }

        .lt-form-title{
            font-size: 23px;
        }

        .lt-form-subtitle,
        .lt-summary-text{
            font-size: 15px;
        }

        div[data-testid="stForm"]{
            padding: 18px 16px 16px 16px;
            border-radius: 20px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <section class="lt-hero-section">
        <div class="lt-hero-inner">
            <h1 class="lt-hero-title">{escape(hero_title)}</h1>
            <p class="lt-hero-desc">{escape(hero_subtitle)}</p>
            <div class="lt-hero-stats">
                <div class="lt-hero-stat">
                    <div class="lt-hero-stat-value">{total_routes}</div>
                    <div class="lt-hero-stat-label">Hành trình đề xuất</div>
                </div>
                <div class="lt-hero-stat">
                    <div class="lt-hero-stat-value">{len(destination_options) - 1}</div>
                    <div class="lt-hero-stat-label">Điểm đến tiêu biểu</div>
                </div>
                <div class="lt-hero-stat">
                    <div class="lt-hero-stat-value">{lowest_price_all:,}đ</div>
                    <div class="lt-hero-stat-label">Giá tham khảo</div>
                </div>
            </div>
        </div>
    </section>
    """, unsafe_allow_html=True)

    _, center_col, _ = st.columns([0.12, 0.76, 0.12])
    with center_col:
        st.markdown('<div class="lt-form-overlap"></div>', unsafe_allow_html=True)

        with st.form("lichtrinh_filter_form", border=False):
            c1, c2, c3, c4, c5 = st.columns([1.55, 1.15, 1.15, 1.15, 0.85])

            with c1:
                destination_query = st.selectbox("Bạn muốn đến đâu?", destination_options, index=0, key="lichtrinh_destination")

            with c2:
                departure_place = st.selectbox("Nơi khởi hành", ["TP. Lào Cai"], key="lichtrinh_departure")

            with c3:
                selected_category = st.selectbox("Loại hình", category_options, index=0, key="lichtrinh_category")

            with c4:
                sort_option = st.selectbox("Sắp xếp chi phí", ["Mặc định", "Chi phí tăng dần", "Chi phí giảm dần"], index=0, key="lichtrinh_sort")

            with c5:
                st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                st.form_submit_button("Tìm tour", use_container_width=True)

        filtered_data = [
            item for item in lichtrinh_data
            if normalize_text(item.get("from")) == normalize_text(departure_place)
        ]

        if selected_category != "Tất cả":
            filtered_data = [
                item for item in filtered_data
                if normalize_text(item.get("category")) == normalize_text(selected_category)
            ]

        if destination_query != "Tất cả":
            keyword = normalize_text(destination_query)
            filtered_data = [
                item for item in filtered_data
                if keyword in normalize_text(item.get("to"))
            ]

    if sort_option == "Chi phí tăng dần":
        filtered_data = sorted(filtered_data, key=lambda x: extract_price(x.get("total_price")))
    elif sort_option == "Chi phí giảm dần":
        filtered_data = sorted(filtered_data, key=lambda x: extract_price(x.get("total_price")), reverse=True)

    result_count = len(filtered_data)
    cheapest_filtered = min((extract_price(item.get("total_price")) for item in filtered_data), default=0)

    selected_destination_label = destination_query if destination_query != "Tất cả" else "tất cả điểm đến"
    selected_category_label = selected_category if selected_category != "Tất cả" else "mọi loại hình"


    card_css = """
    <style>
    body{
        margin:0;
        background:transparent;
        font-family: Inter, Arial, sans-serif;
    }

    .lt-results-wrap{
        max-width: 1320px;
        margin: 18px auto 42px auto;
        padding: 0 4px;
        box-sizing: border-box;
    }

    .lt-grid{
        display:grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap:24px;
        box-sizing:border-box;
    }

    .lt-card{
        position:relative;
        min-height:430px;
        perspective:1600px;
    }

    .lt-card-shell{
        position:relative;
        width:100%;
        height:100%;
        min-height:430px;
        transform-style:preserve-3d;
        transition:transform 0.82s cubic-bezier(0.22, 0.7, 0.18, 1);
    }

    .lt-card:hover .lt-card-shell{
        transform:rotateY(-180deg);
    }

    .lt-card-face{
        position:absolute;
        inset:0;
        border-radius:26px;
        overflow:hidden;
        backface-visibility:hidden;
        -webkit-backface-visibility:hidden;
    }

    .lt-card-front{
        position:relative;
        background:linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
        border:1px solid #e5edf6;
        padding:24px 22px 22px 22px;
        display:flex;
        flex-direction:column;
        box-shadow:0 18px 38px rgba(15,23,42,0.08);
    }

    .lt-card-front::before{
        content:"";
        position:absolute;
        top:0;
        left:0;
        right:0;
        height:5px;
        background:linear-gradient(90deg, #1565c0 0%, #2b7fd3 52%, #43b0f1 100%);
    }

    .lt-card-back{
        transform:rotateY(180deg);
        background-size:cover;
        background-position:center;
        background-repeat:no-repeat;
        box-shadow:0 18px 38px rgba(15,23,42,0.12);
    }

    .lt-card-back::before{
        content:"";
        position:absolute;
        inset:0;
        background:linear-gradient(180deg, rgba(5,18,38,0.10) 0%, rgba(5,18,38,0.78) 100%);
    }

    .lt-back-inner{
        position:relative;
        z-index:2;
        height:100%;
        display:flex;
        flex-direction:column;
        justify-content:center;
        align-items:center;        
        padding:4px 18px 20px 18px;
        color:#ffffff;
    }

    .lt-back-badge{
        display:inline-flex;
        align-items:center;
        justify-content:center;
        align-self:flex-start;
        margin-bottom:12px;
        padding:8px 13px;
        border-radius:999px;
        background:rgba(255,255,255,0.16);
        border:1px solid rgba(255,255,255,0.28);
        font-size:13px;
        font-weight:800;
        text-transform:uppercase;
        letter-spacing:0.06em;
    }

    .lt-back-route{
        font-size:26px;
        font-weight:900;
        line-height:1.25;
        margin-bottom:10px;
        text-transform:uppercase;
        text-shadow:0 4px 14px rgba(0,0,0,0.28);
    }

    .lt-back-desc{
        font-size:15px;
        line-height:1.75;
        color:rgba(255,255,255,0.92);
        margin-bottom:18px;
        max-width:92%;
    }

    .lt-view-btn{
        display:inline-flex;
        align-items:center;
        justify-content:center;
        align-self:center;
        min-width:150px;
        height:48px;
        border:none;
        border-radius:14px;
        background:#ffffff;
        color:#0f172a;
        font-size:15px;
        font-weight:900;
        cursor:pointer;
        box-shadow:0 14px 26px rgba(0,0,0,0.18);
        transition:transform 0.2s ease, box-shadow 0.2s ease;
    }

    .lt-view-btn:hover{
        transform:translateY(-2px);
        box-shadow:0 18px 32px rgba(0,0,0,0.24);
    }

    .lt-card-top{
        display:flex;
        align-items:flex-start;
        justify-content:space-between;
        gap:14px;
        margin-bottom:18px;
    }

    .lt-route{
        font-size:20px;
        font-weight:900;
        text-transform:uppercase;
        letter-spacing:0.01em;
        line-height:1.3;
        color:#0f172a;
    }

    .lt-badge{
        display:inline-flex;
        align-items:center;
        justify-content:center;
        padding:8px 12px;
        border-radius:999px;
        background:#ecf5ff;
        color:#1565c0;
        font-size:15px;
        font-weight:800;
        text-transform:uppercase;
        letter-spacing:0.06em;
        white-space:nowrap;
        border:1px solid #cfe5ff;
    }

    .lt-info-grid{
        display:grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap:12px;
    }

    .lt-info-item{
        background:#f1f5f9;
        border:1px solid #dde6ef;
        border-radius:18px;
        padding:14px;
        min-height:88px;
        box-sizing:border-box;
        display:flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;
        text-align:center;
    }

    .lt-info-label{
        font-size:17px;
        font-weight:800;
        text-transform:uppercase;
        color:#64748b;
        margin-bottom:8px;
        text-align:center;
    }

    .lt-info-value{
        font-size:16px;
        line-height:1.6;
        font-weight:700;
        color:#0f172a;
        word-break:break-word;
        text-align:center;
    }

    .lt-hotel-box{
        margin-top:14px;
        background:linear-gradient(180deg, #fff7ed 0%, #fffaf5 100%);
        border:1px solid #fed7aa;
        border-radius:18px;
        padding:15px 16px;
    }

    .lt-hotel-title{
        font-size:12px;
        font-weight:800;
        text-transform:uppercase;
        letter-spacing:0.08em;
        color:#c2410c;
        margin-bottom:8px;
    }

    .lt-hotel-value{
        font-size:14px;
        line-height:1.7;
        font-weight:700;
        color:#7c2d12;
        word-break:break-word;
    }

    .lt-divider{
        height:1px;
        background:#e7eef6;
        margin:18px 0 16px 0;
    }

    .lt-bottom{
        display:flex;
        justify-content:space-between;
        align-items:flex-end;
        gap:12px;
        margin-top:auto;
    }

    .lt-bottom-note{
        font-size:13px;
        line-height:1.65;
        color:#64748b;
        max-width:55%;
    }

    .lt-price-block{
        text-align:right;
        flex-shrink:0;
    }

    .lt-price-caption{
        font-size:12px;
        font-weight:800;
        text-transform:uppercase;
        letter-spacing:0.08em;
        color:#64748b;
        margin-bottom:6px;
    }

    .lt-price-value{
        font-size:17px;
        font-weight:900;
        line-height:1.2;
        color:#ef4444;
        word-break:break-word;
        overflow-wrap:anywhere;
    }

    .lt-price-sub{
        font-size:13px;
        line-height:1.55;
        color:#94a3b8;
        margin-top:4px;
    }

    .lt-empty{
        background:linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
        border:1px dashed #cbd5e1;
        border-radius:26px;
        padding:42px 26px;
        text-align:center;
        color:#334155;
        box-shadow:0 14px 36px rgba(15,23,42,0.05);
    }

    .lt-empty-title{
        font-size:26px;
        font-weight:900;
        color:#0f172a;
        margin-bottom:10px;
    }

    .lt-empty-text{
        max-width:620px;
        margin:0 auto;
        font-size:16px;
        line-height:1.8;
        color:#475569;
    }

    @media (max-width: 1180px){
        .lt-grid{
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }

    @media (max-width: 760px){
        .lt-results-wrap{
            padding:0;
        }

        .lt-grid{
            grid-template-columns:1fr;
            gap:18px;
        }

        .lt-card,
        .lt-card-shell{
            min-height:420px;
        }

        .lt-card-top,
        .lt-bottom{
            flex-direction:column;
            align-items:flex-start;
        }

        .lt-route{
            font-size:17px;
        }

        .lt-info-grid{
            grid-template-columns:1fr;
        }

        .lt-bottom-note,
        .lt-price-block{
            max-width:100%;
            width:100%;
            text-align:left;
        }

        .lt-price-value{
            font-size:26px;
        }

        .lt-back-route{
            font-size:22px;
        }

        .lt-empty-title{
            font-size:22px;
        }

        .lt-empty-text{
            font-size:15px;
        }
    }
    </style>
    """

    cards_html = '<div class="lt-results-wrap">'

    if filtered_data:
        cards_html += '<div class="lt-grid">'
        for item in filtered_data:
            total_price = safe_text(item.get("total_price"), "Liên hệ")
            transport_price = safe_text(item.get("transport_price"), "Đang cập nhật")
            ticket_price = safe_text(item.get("ticket_price"), "0đ")
            hotel_name = safe_text(item.get("hotel_name"), "Đang cập nhật")
            hotel_price = safe_text(item.get("hotel_price"), "Liên hệ")
            category = safe_text(item.get("category"), "Lịch trình")
            route_text = f"{safe_text(item.get('from'))} → {safe_text(item.get('to'))}"
            cover_image = safe_url(itinerary_image(item))
            slug_value = make_slug(item)

            hover_desc = safe_text(
                item.get("note") or item.get("short_desc"),
                "Nhấn để xem chi tiết lịch trình, chi phí tham khảo và thông tin lưu trú."
            )

            cards_html += f"""
            <div class="lt-card">
                <div class="lt-card-shell">

                    <div class="lt-card-face lt-card-front">
                        <div class="lt-card-top">
                            <div class="lt-route">{route_text}</div>
                            <div class="lt-badge">{category}</div>
                        </div>

                        <div class="lt-info-grid">
                            <div class="lt-info-item">
                                <div class="lt-info-label">Quãng đường</div>
                                <div class="lt-info-value">{safe_text(item.get('distance_km'))}</div>
                            </div>
                            <div class="lt-info-item">
                                <div class="lt-info-label">Thời gian</div>
                                <div class="lt-info-value">{safe_text(item.get('time_estimate'))}</div>
                            </div>
                            <div class="lt-info-item">
                                <div class="lt-info-label">Phương tiện</div>
                                <div class="lt-info-value">{safe_text(item.get('transport_name'))}</div>
                            </div>
                            <div class="lt-info-item">
                                <div class="lt-info-label">Giá vé tham quan</div>
                                <div class="lt-info-value">{ticket_price}</div>
                            </div>
                        </div>

                        <div class="lt-hotel-box">
                            <div class="lt-hotel-title">Khách sạn / Nhà nghỉ gợi ý</div>
                            <div class="lt-hotel-value">{hotel_name} • {hotel_price}</div>
                        </div>

                        <div class="lt-divider"></div>

                        <div class="lt-bottom">
                            <div class="lt-bottom-note">
                                Giá xe tham khảo: <strong>{transport_price}</strong><br>
                                Hành trình hiển thị theo bộ lọc bạn đã chọn.
                            </div>
                            <div class="lt-price-block">
                                <div class="lt-price-caption">Giá từ / khách</div>
                                <div class="lt-price-value">{total_price}</div>
                                <div class="lt-price-sub">Đã gồm chi phí tổng quan</div>
                            </div>
                        </div>
                    </div>

                    <div class="lt-card-face lt-card-back" style="background-image:url('{cover_image}');">
                        <div class="lt-back-inner">
                            <div class="lt-back-badge">{category}</div>
                            <div class="lt-back-route">{route_text}</div>
                            <div class="lt-back-desc">{hover_desc}</div>
                            <button class="lt-view-btn" onclick="openLichTrinhDetail('{slug_value}')">
                                Xem chi tiết
                            </button>
                        </div>
                    </div>

                </div>
            </div>
            """

        cards_html += "</div>"

        cards_html += """
        <script>
        function openLichTrinhDetail(slug){
            try{
                const baseUrl = document.referrer
                    ? new URL(document.referrer)
                    : new URL(window.parent.location.href);

                baseUrl.searchParams.set("page", "lichtrinh_detail");
                baseUrl.searchParams.set("slug", slug);
                baseUrl.hash = "";

                window.open(baseUrl.toString(), "_blank", "noopener,noreferrer");
            }catch(err){
                window.open("?page=lichtrinh_detail&slug=" + encodeURIComponent(slug), "_blank", "noopener,noreferrer");
            }
        }
        </script>
        """

        rows = math.ceil(result_count / 3) if result_count else 1
        height = max(520, rows * 580)
    else:
        cards_html += """
        <div class="lt-empty">
            <div class="lt-empty-title">Chưa tìm thấy lịch trình phù hợp</div>
            <div class="lt-empty-text">
                Bộ lọc hiện tại đang khá hẹp nên chưa có dữ liệu khớp. Bạn hãy chuyển điểm đến hoặc loại hình về
                <strong>Tất cả</strong> để xem lại toàn bộ gợi ý đang có trong hệ thống.
            </div>
        </div>
        """
        height = 320

    cards_html += "</div>"
    components.html(card_css + cards_html, height=height, scrolling=False)

    # Lưu ý
    components.html("""
    <div style="
        max-width: 1320px;
        margin: 18px auto 60px auto;
        padding: 0 4px;
        box-sizing: border-box;
        font-family: Inter, Arial, sans-serif;
    ">
        <div style="
            display: grid;
            grid-template-columns: 280px 1fr;
            align-items: stretch;
            background: #ffffff;
            border: 1px solid #e5e7eb;
            box-shadow: 0 10px 28px rgba(15,23,42,0.08);
            overflow: hidden;
        ">
            <!-- Khối trái -->
            <div style="
                position: relative;
                min-height: 180px;
                background: linear-gradient(135deg, #8b0000 0%, #c1121f 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
                box-sizing: border-box;
            ">
                <div style="
                    position: relative;
                    width: 100%;
                    height: 100%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                ">
                    <div style="
                        width: 135px;
                        height: 68px;
                        border: 2px solid rgba(255,255,255,0.95);
                        color: #ffffff;
                        font-size: 25px;
                        font-weight: 800;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        transform: rotate(-6deg);
                        box-shadow: 0 10px 20px rgba(0,0,0,0.18);
                    ">
                        LƯU Ý
                    </div>

                    <div style="
                        position: absolute;
                        right: 8px;
                        bottom: 18px;
                        font-size: 54px;
                        line-height: 1;
                        filter: drop-shadow(0 6px 10px rgba(0,0,0,0.22));
                    ">
                        📢
                    </div>
                </div>
            </div>

            <!-- Khối phải -->
            <div style="
                padding: 18px 26px;
                box-sizing: border-box;
                background: #ffffff;
                min-height: 180px;
            ">
                <div style="
                    font-size: 31px;
                    font-weight: 800;
                    color: #111827;
                    line-height: 1.45;
                    margin-bottom: 10px;
                ">
                    THÔNG BÁO lưu ý khi thực hiện lịch trình du lịch Lào Cai.
                </div>

                <div style="
                    font-size: 14px;
                    color: #64748b;
                    margin-bottom: 14px;
                ">
                    Cập nhật hệ thống • Tham khảo trước khi khởi hành
                </div>

                <div style="
                    font-size: 15px;
                    color: #374151;
                    line-height: 1.9;
                    margin-bottom: 14px;
                ">
                    Giá hiển thị chỉ mang tính tham khảo tại thời điểm tra cứu. Lịch trình có thể thay đổi tùy điều kiện
                    thời tiết, tình trạng vận hành thực tế, lưu trú và phương tiện di chuyển. Du khách nên xác nhận lại
                    khách sạn, vé tham quan, phương tiện và chuẩn bị đầy đủ giấy tờ cá nhân trước chuyến đi.
                </div>

                <div style="
                    font-size: 15px;
                    color: #64748b;
                    line-height: 1.8;
                ">
                    Chuyên mục:
                    <span style="font-weight: 800; color: #111827;">Lưu ý lịch trình</span>
                </div>
            </div>
        </div>
    </div>
    """, height=230, scrolling=False)

elif page == "lichtrinh_detail":
    import os
    import json
    import re
    import base64
    import unicodedata
    from html import escape
    from string import Template
    from urllib.parse import quote_plus
    import streamlit.components.v1 as components

    try:
        with open("lichtrinh.json", "r", encoding="utf-8") as f:
            lichtrinh_data = json.load(f)
    except Exception as e:
        st.error(f"Lỗi đọc file lichtrinh.json: {e}")
        st.stop()

    def clean_text(value):
        if value is None:
            return ""
        return str(value).replace("\r\n", "\n").replace("\r", "\n").strip()

    def normalize_text(value):
        return clean_text(value).lower()

    def safe_text(value, fallback="Đang cập nhật"):
        text = clean_text(value)
        return escape(text if text else fallback)

    def safe_url(value, fallback="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1600&auto=format&fit=crop"):
        text = clean_text(value)
        return escape(text if text else fallback, quote=True)

    def make_slug(item):
        raw = clean_text(item.get("slug"))
        if raw:
            return raw

        text = f"{item.get('from', '')} {item.get('to', '')}"
        text = text.replace("Đ", "D").replace("đ", "d")
        text = unicodedata.normalize("NFD", text)
        text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
        text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
        return text or "lich-trinh"

    def get_images(route):
        fallback = "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1600&auto=format&fit=crop"
        images = []

        for key in [
            "image", "image_2", "image_3", "image_4", "image_5",
            "cover", "thumbnail", "hero_image", "banner_image"
        ]:
            val = clean_text(route.get(key))
            if val:
                images.append(val)

        for key in ["gallery", "images", "detail_images"]:
            val = route.get(key)
            if isinstance(val, list):
                for item in val:
                    item_text = clean_text(item)
                    if item_text:
                        images.append(item_text)

        unique_images = []
        seen = set()
        for img in images:
            if img not in seen:
                seen.add(img)
                unique_images.append(img)

        if not unique_images:
            unique_images = [fallback]

        while len(unique_images) < 5:
            unique_images.append(unique_images[-1])

        return [safe_url(img, fallback) for img in unique_images[:5]]

    def split_paragraphs(*values):
        results = []
        seen = set()

        for value in values:
            text = clean_text(value)
            if not text:
                continue

            parts = [p.strip() for p in text.split("\n") if p.strip()]
            if not parts:
                parts = [text]

            for part in parts:
                normalized = " ".join(part.split()).strip()
                if normalized and normalized.lower() not in seen:
                    seen.add(normalized.lower())
                    results.append(normalized)
        return results

    def build_highlights(route):
        highlights = []

        if clean_text(route.get("distance_km")):
            highlights.append(f"Quãng đường dự kiến: {clean_text(route.get('distance_km'))}.")
        if clean_text(route.get("time_estimate")):
            highlights.append(f"Thời gian di chuyển ước tính: {clean_text(route.get('time_estimate'))}.")
        if clean_text(route.get("transport_name")):
            highlights.append(f"Phương tiện gợi ý: {clean_text(route.get('transport_name'))}.")
        if clean_text(route.get("ticket_price")):
            highlights.append(f"Vé tham quan tham khảo: {clean_text(route.get('ticket_price'))}.")
        if clean_text(route.get("hotel_name")):
            highlights.append(f"Lưu trú gợi ý: {clean_text(route.get('hotel_name'))}.")
        if clean_text(route.get("note")):
            note_text = clean_text(route.get("note"))
            if len(note_text) > 140:
                note_text = note_text[:140].rsplit(" ", 1)[0] + "..."
            highlights.append(note_text)

        if not highlights:
            highlights = [
                "Lịch trình đang được cập nhật thêm điểm nổi bật.",
                "Bạn có thể xem chi phí, phương tiện và lưu trú tham khảo bên dưới."
            ]

        return highlights[:6]

    def build_map_url(route):
        for key in ["map_embed", "iframe_map", "google_map", "map_url", "location_map"]:
            raw = clean_text(route.get(key))
            if not raw:
                continue

            if raw.startswith("<iframe"):
                match = re.search(r'''src=["']([^"']+)["']''', raw)
                if match:
                    return escape(match.group(1), quote=True)

            if raw.startswith("http://") or raw.startswith("https://"):
                return escape(raw, quote=True)

        lat = clean_text(route.get("lat"))
        lng = clean_text(route.get("lng"))
        if lat and lng:
            return escape(f"https://www.google.com/maps?q={lat},{lng}&output=embed", quote=True)

        hotel_name = clean_text(route.get("hotel_name"))
        destination = clean_text(route.get("to"))
        area_query = " ".join([x for x in [hotel_name, destination, "Lào Cai"] if x]).strip()

        if not area_query:
            area_query = "Lào Cai"

        return escape(f"https://www.google.com/maps?q={quote_plus(area_query)}&output=embed", quote=True)

    slug = clean_text(st.query_params.get("slug", ""))

    selected_route = None
    for item in lichtrinh_data:
        if normalize_text(make_slug(item)) == normalize_text(slug):
            selected_route = item
            break

    if not selected_route:
        st.error("Không tìm thấy lịch trình.")
        st.stop()

    from_place = clean_text(selected_route.get("from")) or "Điểm khởi hành"
    to_place = clean_text(selected_route.get("to")) or "Điểm đến"
    route_title = f"{from_place} - {to_place}"
    category = clean_text(selected_route.get("category")) or "Lịch trình"
    route_code = clean_text(selected_route.get("code")) or clean_text(selected_route.get("tour_code")) or clean_text(selected_route.get("id")) or slug.upper()
    note_text = clean_text(selected_route.get("note")) or clean_text(selected_route.get("short_desc")) or "Lịch trình này đang được cập nhật thêm phần mô tả chi tiết."
    total_price = clean_text(selected_route.get("total_price")) or "Liên hệ"
    transport_price = clean_text(selected_route.get("transport_price")) or "Đang cập nhật"
    ticket_price = clean_text(selected_route.get("ticket_price")) or "0đ"
    transport_name = clean_text(selected_route.get("transport_name")) or "Đang cập nhật"
    distance_km = clean_text(selected_route.get("distance_km")) or "Đang cập nhật"
    time_estimate = clean_text(selected_route.get("time_estimate")) or "Đang cập nhật"
    hotel_name = clean_text(selected_route.get("hotel_name")) or "Đang cập nhật"
    hotel_price = clean_text(selected_route.get("hotel_price")) or "Liên hệ"

    paragraphs = split_paragraphs(selected_route.get("note"), selected_route.get("short_desc"))
    if not paragraphs:
        paragraphs = [
            f"Hành trình từ {from_place} đến {to_place} phù hợp cho du khách muốn khám phá vẻ đẹp địa phương một cách thuận tiện.",
            "Lịch trình hiện đang được hệ thống tổng hợp với các thông tin tham khảo về phương tiện, thời gian, chi phí và lưu trú."
        ]

    highlights = build_highlights(selected_route)
    images = get_images(selected_route)
    map_url = build_map_url(selected_route)

    highlight_html = "".join(f"<li>{escape(item)}</li>" for item in highlights)

    intro_html = "".join(
        f"<p>{escape(paragraph)}</p>"
        for paragraph in paragraphs[:3]
    )

    html_template = Template("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <style>
            * {
                box-sizing: border-box;
            }

            html, body {
                margin: 0;
                padding: 0;
                background: #eef2e6;
                font-family: Arial, sans-serif;
                color: #0f172a;
            }

            .ltd2-page {
                width: 100%;
                padding: 18px 16px 40px 16px;
                background: #eef2e6;
            }

            .ltd2-wrap {
                max-width: 1320px;
                margin: 0 auto;
            }

            .ltd2-title {
                font-size: 26px;
                line-height: 1.25;
                font-weight: 900;
                color: #0b4f8a;
                margin: 0 0 8px 0;
            }

            .ltd2-meta {
                display: flex;
                flex-wrap: wrap;
                gap: 16px;
                align-items: center;
                margin-bottom: 16px;
                color: #475569;
                font-size: 14px;
                line-height: 1.6;
            }

            .ltd2-meta strong {
                color: #0f172a;
            }

            .ltd2-gallery {
                display: grid;
                grid-template-columns: 1.55fr 1fr;
                gap: 10px;
                margin-bottom: 16px;
            }

            .ltd2-main-photo {
                min-height: 300px;
                border-radius: 10px;
                background-size: cover;
                background-position: center;
                position: relative;
                overflow: hidden;
                box-shadow: 0 12px 24px rgba(15, 23, 42, 0.10);
            }

            .ltd2-main-photo::before {
                content: "";
                position: absolute;
                inset: 0;
                background: linear-gradient(180deg, rgba(0,0,0,0.05) 0%, rgba(0,0,0,0.25) 100%);
            }

            .ltd2-main-badge {
                position: absolute;
                top: 10px;
                left: 10px;
                z-index: 2;
                background: #e53935;
                color: #ffffff;
                font-size: 12px;
                font-weight: 800;
                padding: 6px 10px;
                border-radius: 6px;
            }

            .ltd2-side-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
            }

            .ltd2-side-photo {
                min-height: 145px;
                border-radius: 10px;
                background-size: cover;
                background-position: center;
                box-shadow: 0 10px 20px rgba(15, 23, 42, 0.08);
            }

            .ltd2-top-grid {
                display: grid;
                grid-template-columns: 1.7fr 0.8fr;
                gap: 16px;
                margin-bottom: 16px;
            }

            .ltd2-bottom-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 16px;
            }

            .ltd2-card {
                background: #ffffff;
                border: 1px solid #dfe6d6;
                border-radius: 16px;
                padding: 18px;
                box-shadow: 0 10px 22px rgba(15, 23, 42, 0.06);
            }

            .ltd2-card-title {
                font-size: 18px;
                font-weight: 900;
                color: #1f2937;
                margin-bottom: 12px;
            }

            .ltd2-list {
                margin: 0;
                padding-left: 22px;
            }

            .ltd2-list li {
                margin-bottom: 9px;
                color: #475569;
                font-size: 15px;
                line-height: 1.7;
            }

            .ltd2-price-card {
                min-height: 100%;
                background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
                border: 1px solid #dbe7f3;
                border-radius: 18px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                padding: 26px 22px;
                box-shadow: 0 12px 28px rgba(15, 23, 42, 0.06);
            }

            .ltd2-price-label {
                font-size: 20px;
                font-weight: 800;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: #64748b;
                margin-bottom: 12px;
            }

            .ltd2-price-value {
                font-size: 42px;
                line-height: 1.15;
                font-weight: 900;
                color: #1565c0;
                word-break: break-word;
            }

            .ltd2-price-sub {
                margin-top: 12px;
                font-size: 14px;
                line-height: 1.75;
                color: #475569;
                max-width: 250px;
            }

            .ltd2-price-sub {
                margin-top: 10px;
                font-size: 13px;
                line-height: 1.7;
                color: #475569;
                max-width: 230px;
            }

            .ltd2-text p {
                margin: 0 0 12px 0;
                color: #374151;
                font-size: 16px;
                line-height: 1.85;
            }

            .ltd2-info-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
                margin-bottom: 14px;
            }

            .ltd2-info-item {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 12px 14px;
            }

            .ltd2-info-item span {
                display: block;
                font-size: 12px;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0.06em;
                color: #64748b;
                margin-bottom: 6px;
            }

            .ltd2-info-item strong {
                display: block;
                font-size: 14px;
                line-height: 1.7;
                color: #0f172a;
                font-weight: 800;
                word-break: break-word;
            }

            .ltd2-map {
                width: 100%;
                height: 300px;
                border: none;
                border-radius: 12px;
                overflow: hidden;
            }

            @media (max-width: 980px) {
                .ltd2-gallery,
                .ltd2-top-grid,
                .ltd2-bottom-grid {
                    grid-template-columns: 1fr;
                }

                .ltd2-side-grid {
                    grid-template-columns: 1fr 1fr;
                }
            }

            @media (max-width: 680px) {
                .ltd2-page {
                    padding: 14px 10px 28px 10px;
                }

                .ltd2-title {
                    font-size: 22px;
                }

                .ltd2-meta {
                    gap: 10px;
                    font-size: 13px;
                }

                .ltd2-side-grid,
                .ltd2-info-grid {
                    grid-template-columns: 1fr;
                }

                .ltd2-main-photo,
                .ltd2-side-photo {
                    min-height: 220px;
                }

                .ltd2-price-value {
                    font-size: 28px;
                }
            }
        </style>
    </head>
    <body>
        <div class="ltd2-page">
            <div class="ltd2-wrap">
                <h1 class="ltd2-title">$route_title</h1>

                <div class="ltd2-meta">
                    <div><strong>Loại hình:</strong> $category</div>
                    <div><strong>Khởi hành:</strong> $from_place</div>
                    <div><strong>Mã tour:</strong> $route_code</div>
                </div>

                <div class="ltd2-gallery">
                    <div class="ltd2-main-photo" style="background-image:url('$image_1');">
                        <div class="ltd2-main-badge">Lịch trình nổi bật</div>
                    </div>

                    <div class="ltd2-side-grid">
                        <div class="ltd2-side-photo" style="background-image:url('$image_2');"></div>
                        <div class="ltd2-side-photo" style="background-image:url('$image_3');"></div>
                        <div class="ltd2-side-photo" style="background-image:url('$image_4');"></div>
                        <div class="ltd2-side-photo" style="background-image:url('$image_5');"></div>
                    </div>
                </div>

                <div class="ltd2-top-grid">
                    <div class="ltd2-card">
                        <div class="ltd2-card-title">Điểm nổi bật tour</div>
                        <ul class="ltd2-list">
                            $highlight_html
                        </ul>
                    </div>

                    <div class="ltd2-card ltd2-price-card">
                        <div class="ltd2-price-label">Chi phí tham khảo</div>
                        <div class="ltd2-price-value">$total_price</div>
                        <div class="ltd2-price-sub">
                            Mức giá có thể thay đổi tùy thời điểm, phương tiện và dịch vụ lưu trú thực tế.
                        </div>
                    </div>
                </div>

                <div class="ltd2-bottom-grid">
                    <div class="ltd2-card">
                        <div class="ltd2-card-title">Giới thiệu</div>
                        <div class="ltd2-text">
                            $intro_html
                        </div>
                    </div>

                    <div class="ltd2-card">
                        <div class="ltd2-card-title">Thông tin khách sạn</div>

                        <div class="ltd2-info-grid">
                            <div class="ltd2-info-item">
                                <span>Khách sạn / nhà nghỉ</span>
                                <strong>$hotel_name</strong>
                            </div>

                            <div class="ltd2-info-item">
                                <span>Giá lưu trú</span>
                                <strong>$hotel_price</strong>
                            </div>

                            <div class="ltd2-info-item">
                                <span>Phương tiện</span>
                                <strong>$transport_name</strong>
                            </div>

                            <div class="ltd2-info-item">
                                <span>Thời gian</span>
                                <strong>$time_estimate</strong>
                            </div>

                            <div class="ltd2-info-item">
                                <span>Quãng đường</span>
                                <strong>$distance_km</strong>
                            </div>

                            <div class="ltd2-info-item">
                                <span>Vé tham quan</span>
                                <strong>$ticket_price</strong>
                            </div>

                            <div class="ltd2-info-item">
                                <span>Giá xe</span>
                                <strong>$transport_price</strong>
                            </div>

                            <div class="ltd2-info-item">
                                <span>Điểm đến</span>
                                <strong>$to_place</strong>
                            </div>
                        </div>

                        <iframe
                            class="ltd2-map"
                            src="$map_url"
                            loading="lazy"
                            referrerpolicy="no-referrer-when-downgrade">
                        </iframe>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """)

    html_output = html_template.substitute(
        route_title=escape(route_title),
        category=escape(category),
        from_place=escape(from_place),
        to_place=escape(to_place),
        route_code=escape(route_code if route_code else "Đang cập nhật"),
        image_1=images[0],
        image_2=images[1],
        image_3=images[2],
        image_4=images[3],
        image_5=images[4],
        highlight_html=highlight_html,
        total_price=escape(total_price),
        intro_html=intro_html,
        hotel_name=escape(hotel_name),
        hotel_price=escape(hotel_price),
        transport_name=escape(transport_name),
        time_estimate=escape(time_estimate),
        distance_km=escape(distance_km),
        ticket_price=escape(ticket_price),
        transport_price=escape(transport_price),
        map_url=map_url,
    )

    page_height = 1650 + max(0, len(" ".join(paragraphs)) // 400) * 220
    components.html(html_output, height=page_height, scrolling=False)

elif page == "diemden":
    import json
    import math
    from html import escape
    from urllib.parse import quote

    try:
        with open("diemden.json", "r", encoding="utf-8") as f:
            diemden_data = json.load(f)
    except Exception as e:
        st.error(f"Lỗi đọc file diemden.json: {e}")
        st.stop()

    def safe_text(value, fallback="Đang cập nhật"):
        text = str(value).strip() if value is not None else ""
        return escape(text) if text else escape(fallback)

    def safe_url(value, fallback="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1600&auto=format&fit=crop"):
        text = str(value).strip() if value is not None else ""
        return escape(text if text else fallback, quote=True)

    def normalize_text(value):
        return str(value or "").strip().lower()

    def safe_list(value):
        if isinstance(value, list):
            return [escape(str(item).strip()) for item in value if str(item).strip()]
        return []

    place_name_options = ["Tất cả địa điểm"] + sorted({item.get("name", "") for item in diemden_data if item.get("name")})
    area_options = ["Tất cả"] + sorted({item.get("area", "") for item in diemden_data if item.get("area")})
    category_options = ["Tất cả"] + sorted({item.get("category", "") for item in diemden_data if item.get("category")})
    season_options = ["Tất cả"] + sorted({item.get("season", "") for item in diemden_data if item.get("season")})

    total_places = len(diemden_data)
    total_areas = len(area_options) - 1
    total_categories = len(category_options) - 1

    hero_title = "Khám phá điểm đến nổi bật tại Lào Cai"
    hero_subtitle = "Tìm kiếm theo khu vực, loại hình và mùa đẹp để lựa chọn hành trình phù hợp với sở thích của bạn."

    diemden_hero_src = image_to_data_uri([
        "kho_anh/diem_den/chinh.jpg",
        "kho_anh/diem_den/chinh.png",
        "kho_anh/diem_den/chinh.jpeg",
        "kho_anh/diem_den/chinh.webp"
    ])

    st.markdown(f"""
    <style>
        .dd-hero-section{{
            position: relative;
            height: 500px;
            background:
                linear-gradient(180deg, rgba(7, 19, 37, 0.12) 0%, rgba(7, 19, 37, 0.22) 100%),
                url('{diemden_hero_src}');
            background-size: cover;
            background-position: center 58%;
            background-repeat: no-repeat;
            animation: ddHeroZoom 1.4s ease-out forwards;
            transform: scale(1.06);
            opacity: 0;
            overflow: hidden;
        }}

        .dd-hero-section::after{{
            content: "";
            position: absolute;
            inset: 0;
            background: rgba(255,255,255,0.04);
            animation: ddHeroFade 1.2s ease-out forwards;
        }}

        @keyframes ddHeroZoom {{
            from {{
                transform: scale(1.06);
                opacity: 0;
            }}
            to {{
                transform: scale(1);
                opacity: 1;
            }}
        }}

        @keyframes ddHeroFade {{
            from {{
                opacity: 0.35;
            }}
            to {{
                opacity: 1;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <section class="dd-hero-section"></section>
    """, unsafe_allow_html=True)

    filtered_data = list(diemden_data)
    result_count = len(filtered_data)

    st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

    vi_sao_canhdep = image_to_data_uri([
        "kho_anh/diem_den/vi_sao/canhdep.webp",
        "kho_anh/diem_den/vi_sao/canhdep.png",
        "kho_anh/diem_den/vi_sao/canhdep.jpg",
        "kho_anh/diem_den/vi_sao/canhdep.jpeg"
    ])

    vi_sao_bandia = image_to_data_uri([
        "kho_anh/diem_den/vi_sao/bandia.png",
        "kho_anh/diem_den/vi_sao/bandia.webp",
        "kho_anh/diem_den/vi_sao/bandia.jpg",
        "kho_anh/diem_den/vi_sao/bandia.jpeg"
    ])

    vi_sao_vanhoa = image_to_data_uri([
        "kho_anh/diem_den/vi_sao/vanhoa.png",
        "kho_anh/diem_den/vi_sao/vanhoa.webp",
        "kho_anh/diem_den/vi_sao/vanhoa.jpg",
        "kho_anh/diem_den/vi_sao/vanhoa.jpeg"
    ])

    vi_sao_trainghiem = image_to_data_uri([
        "kho_anh/diem_den/vi_sao/trainghiem.png",
        "kho_anh/diem_den/vi_sao/trainghiem.webp",
        "kho_anh/diem_den/vi_sao/trainghiem.jpg",
        "kho_anh/diem_den/vi_sao/trainghiem.jpeg"
    ])

    components.html(f"""
    <style>
    body{{
        margin:0;
        background:transparent;
        font-family: Inter, Arial, sans-serif;
    }}

    .dd-benefit-wrap{{
        max-width: 1320px;
        margin: 26px auto 8px auto;
        padding: 0 6px;
        box-sizing: border-box;
        text-align: center;
    }}

    .dd-benefit-title{{
        font-size: 30px;
        font-weight: 900;
        color: #111827;
        text-transform: uppercase;
        margin-bottom: 8px;
        line-height: 1.3;
    }}

    .dd-benefit-line{{
        width: 86px;
        height: 4px;
        background: #f59e0b;
        border-radius: 999px;
        margin: 0 auto 16px auto;
    }}

    .dd-benefit-desc{{
        max-width: 760px;
        margin: 0 auto 28px auto;
        font-size: 16px;
        line-height: 1.8;
        color: #4b5563;
    }}

    .dd-benefit-grid{{
        display:grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap:20px;
    }}

    .dd-benefit-card{{
        background:#ffffff;
        border:1px solid #e5edf6;
        border-radius:24px;
        padding:26px 20px;
        box-shadow:0 12px 28px rgba(15,23,42,0.06);
    }}

    .dd-benefit-icon{{
        width:72px;
        height:72px;
        margin:0 auto 16px auto;
        border-radius:50%;
        background:linear-gradient(135deg, #38bdf8 0%, #0ea5e9 100%);
        display:flex;
        align-items:center;
        justify-content:center;
        box-shadow:0 12px 24px rgba(14,165,233,0.22);
        overflow:hidden;
        padding:14px;
    }}

    .dd-benefit-icon img{{
        width:100%;
        height:100%;
        object-fit:contain;
        display:block;
    }}

    .dd-benefit-name{{
        font-size:18px;
        font-weight:800;
        color:#111827;
        margin-bottom:8px;
    }}

    .dd-benefit-text{{
        font-size:14px;
        line-height:1.75;
        color:#6b7280;
    }}

    @media (max-width: 980px){{
        .dd-benefit-grid{{
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }}
    }}

    @media (max-width: 640px){{
        .dd-benefit-wrap{{
            padding: 0 2px;
        }}

        .dd-benefit-title{{
            font-size:24px;
        }}

        .dd-benefit-grid{{
            grid-template-columns: 1fr;
        }}
    }}
    </style>

    <div class="dd-benefit-wrap">
        <div class="dd-benefit-title">VÌ SAO NÊN KHÁM PHÁ LÀO CAI CÙNG AI?</div>
        <div class="dd-benefit-line"></div>
        <div class="dd-benefit-desc">
            Khám phá Lào Cai theo cách hoàn toàn mới với trợ lý AI thông minh – giúp bạn tìm hiểu, lên lịch trình và trải nghiệm văn hóa vùng cao một cách sâu sắc, tiện lợi và cá nhân hóa.
        </div>

        <div class="dd-benefit-grid">
            <div class="dd-benefit-card">
                <div class="dd-benefit-icon"><img src="{vi_sao_canhdep}" alt="Cảnh đẹp"></div>
                <div class="dd-benefit-name">Cảnh đẹp nổi bật</div>
                <div class="dd-benefit-text">Khám phá Lào Cai qua góc nhìn trực quan với gợi ý thông minh từ AI – từ Sa Pa, Fansipan đến những điểm đến ít người biết.</div>
            </div>

            <div class="dd-benefit-card">
                <div class="dd-benefit-icon"><img src="{vi_sao_bandia}" alt="Bản địa"></div>
                <div class="dd-benefit-name">Bản sắc bản địa</div>
                <div class="dd-benefit-text">Tìm hiểu văn hóa, phong tục và đời sống của đồng bào dân tộc thông qua dữ liệu được chọn lọc và giải thích bởi AI.</div>
            </div>

            <div class="dd-benefit-card">
                <div class="dd-benefit-icon"><img src="{vi_sao_vanhoa}" alt="Văn hóa"></div>
                <div class="dd-benefit-name">Di tích - văn hóa</div>
                <div class="dd-benefit-text">NHệ thống AI cung cấp thông tin chính xác, dễ hiểu về các di tích, giúp bạn hiểu rõ giá trị lịch sử và văn hóa địa phương.</div>
            </div>

            <div class="dd-benefit-card">
                <div class="dd-benefit-icon"><img src="{vi_sao_trainghiem}" alt="Trải nghiệm"></div>
                <div class="dd-benefit-name">Trải nghiệm đa dạng</div>
                <div class="dd-benefit-text">Gợi ý lịch trình cá nhân hóa, hỗ trợ hỏi đáp nhanh chóng – giúp bạn khám phá Lào Cai thuận tiện và hiệu quả hơn bao giờ hết.</div>
            </div>
        </div>
    </div>
    """, height=500, scrolling=False)

    st.markdown(f"""
    <div style="
        max-width:1320px;
        margin: 8px auto 10px auto;
        padding: 0 8px;
        box-sizing:border-box;
    ">
        <div style="
            display:flex;
            align-items:flex-end;
            justify-content:space-between;
            gap:16px;
            flex-wrap:wrap;
        ">
            <div>
                <div style="
                    font-size:30px;
                    font-weight:900;
                    color:#111827;
                    line-height:1.2;
                    margin-bottom:6px;
                ">
                    Danh sách điểm đến
                </div>
                <div style="
                    font-size:16px;
                    color:#64748b;
                    line-height:1.7;
                ">
                    Tìm thấy <strong>{result_count}</strong> dành cho bạn.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    cards_css = """
    <style>
    body{
        margin:0;
        background:transparent;
        font-family: Inter, Arial, sans-serif;
    }

    .dd-results-wrap{
        max-width: 1320px;
        margin: 12px auto 60px auto;
        padding: 0 6px;
        box-sizing: border-box;
    }

    .dd-grid{
        display:grid;
        grid-template-columns: 1fr;
        gap:24px;
    }

    .dd-card{
        display:grid;
        grid-template-columns: 320px 1fr;
        background:#ffffff;
        border:1px solid #e5edf6;
        border-radius:26px;
        overflow:hidden;
        box-shadow:0 18px 38px rgba(15,23,42,0.08);
        min-height:260px;
    }

    .dd-card-image{
        height:100%;
        min-height:260px;
        background-size:cover;
        background-position:center;
        position:relative;
        overflow:hidden;
    }

    .dd-card-image::after{
        content:"";
        position:absolute;
        inset:0;
        background:
            linear-gradient(
                to right,
                rgba(255,255,255,0) 0%,
                rgba(255,255,255,0.10) 45%,
                rgba(255,255,255,0.42) 68%,
                rgba(255,255,255,0.78) 84%,
                #ffffff 100%
            );
    }

    .dd-card-body{
        padding:24px 26px;
        display:flex;
        flex-direction:column;
        min-width:0;
        gap:18px;
    }

    .dd-card-header{
        display:flex;
        align-items:flex-start;
        justify-content:space-between;
        gap:16px;
    }

    .dd-card-header-main{
        min-width:0;
        flex:1;
    }

    .dd-card-title{
        font-size:28px;
        font-weight:900;
        color:#0f172a;
        line-height:1.2;
        margin:0;
    }

    .dd-card-top{
        display:flex;
        gap:8px;
        flex-wrap:wrap;
        justify-content:flex-end;
        flex-shrink:0;
        max-width:40%;
    }

    .dd-badge{
        display:inline-flex;
        align-items:center;
        justify-content:center;
        padding:7px 12px;
        border-radius:999px;
        background:#ecf5ff;
        color:#1565c0;
        font-size:12px;
        font-weight:800;
        text-transform:uppercase;
        letter-spacing:0.06em;
        border:1px solid #cfe5ff;
        white-space:nowrap;
    }

    .dd-badge-alt{
        background:#fff7ed;
        color:#c2410c;
        border:1px solid #fed7aa;
    }

    .dd-card-desc{
        font-size:16px;
        line-height:1.8;
        color:#475569;
        margin-top:-4px;
    }

    .dd-divider{
        height:1px;
        background:#e8eef5;
        margin:-2px 0 0 0;
    }

    .dd-info-grid{
        display:grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap:12px;
    }

    .dd-info-card{
        background:#f8fafc;
        border:1px solid #e6edf5;
        border-radius:18px;
        padding:14px 16px;
    }

    .dd-info-label{
        font-size:12px;
        font-weight:800;
        text-transform:uppercase;
        letter-spacing:0.08em;
        color:#64748b;
        margin-bottom:6px;
    }

    .dd-info-value{
        font-size:15px;
        line-height:1.6;
        font-weight:700;
        color:#0f172a;
        word-break:break-word;
    }

    .dd-highlight-wrap{
        background:linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
        border:1px solid #edf2f7;
        border-radius:18px;
        padding:14px 16px;
    }

    .dd-highlight-title{
        font-size:12px;
        font-weight:800;
        text-transform:uppercase;
        letter-spacing:0.08em;
        color:#64748b;
        margin-bottom:10px;
    }

    .dd-chip-row{
        display:flex;
        gap:8px;
        flex-wrap:wrap;
    }

    .dd-chip{
        background:#f1f5f9;
        color:#334155;
        border-radius:999px;
        padding:8px 12px;
        font-size:13px;
        line-height:1.2;
        font-weight:700;
        border:1px solid #e2e8f0;
    }

    .dd-card-footer{
        display:flex;
        justify-content:flex-end;
        margin-top:auto;
    }

    .dd-detail-link{
        display:inline-flex;
        align-items:center;
        justify-content:center;
        min-width:148px;
        padding:12px 18px;
        border-radius:14px;
        background:linear-gradient(135deg, #1565c0 0%, #2b7fd3 100%);
        color:#ffffff !important;
        text-decoration:none !important;
        font-size:14px;
        font-weight:800;
        letter-spacing:0.02em;
        box-shadow:0 12px 24px rgba(21,101,192,0.18);
        transition:transform 0.18s ease, box-shadow 0.18s ease;
    }

    .dd-detail-link:hover{
        transform:translateY(-1px);
        box-shadow:0 16px 28px rgba(21,101,192,0.24);
    }

    .dd-empty{
        background:linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
        border:1px dashed #cbd5e1;
        border-radius:26px;
        padding:42px 26px;
        text-align:center;
        color:#334155;
        box-shadow:0 14px 36px rgba(15,23,42,0.05);
    }

    .dd-empty-title{
        font-size:26px;
        font-weight:900;
        color:#0f172a;
        margin-bottom:10px;
    }

    .dd-empty-text{
        max-width:620px;
        margin:0 auto;
        font-size:16px;
        line-height:1.8;
        color:#475569;
    }

    @media (max-width: 980px){
        .dd-card{
            grid-template-columns: 260px 1fr;
        }

        .dd-card-header{
            flex-direction:column-reverse;
            align-items:flex-start;
        }

        .dd-card-top{
            justify-content:flex-start;
            max-width:100%;
        }

        .dd-card-title{
            font-size:24px;
        }

        .dd-card-desc{
            font-size:15px;
        }
    }

    @media (max-width: 760px){
        .dd-results-wrap{
            padding: 0;
        }

        .dd-grid{
            gap:18px;
        }

        .dd-card{
            grid-template-columns: 1fr;
            border-radius:22px;
        }

        .dd-card-image{
            min-height:220px;
        }

        .dd-card-body{
            padding:20px 18px;
            gap:16px;
        }

        .dd-card-title{
            font-size:22px;
        }

        .dd-info-grid{
            grid-template-columns: 1fr;
        }

        .dd-card-footer{
            justify-content:stretch;
        }

        .dd-detail-link{
            width:100%;
        }

        .dd-empty-title{
            font-size:22px;
        }

        .dd-empty-text{
            font-size:15px;
        }
    }
    </style>
    """

    cards_html = '<div class="dd-results-wrap">'

    if filtered_data:
        cards_html += '<div class="dd-grid">'
        for item in filtered_data:
            highlights = safe_list(item.get("highlights"))[:3]
            highlights_html = "".join([f'<div class="dd-chip">{h}</div>' for h in highlights])

            slug_value = safe_text(item.get("slug"), "dang-cap-nhat")
            slug_raw = str(item.get("slug", "")).strip()
            detail_href = f"?page=diemden_detail&slug={quote(slug_raw)}"          

            cards_html += f"""
            <div class="dd-card">
                <div class="dd-card-image" style="background-image:url('{safe_url(item.get("image"))}');"></div>

                <div class="dd-card-body">
                    <div class="dd-card-header">
                        <div class="dd-card-header-main">
                            <div class="dd-card-title">{safe_text(item.get("name"))}</div>
                        </div>

                        <div class="dd-card-top">
                            <div class="dd-badge">{safe_text(item.get("area"))}</div>
                            <div class="dd-badge dd-badge-alt">{safe_text(item.get("category"))}</div>
                        </div>
                    </div>

                    <div class="dd-card-desc">
                        {safe_text(item.get("short_desc"), "Điểm đến đang được cập nhật thông tin.")}
                    </div>

                    <div class="dd-divider"></div>

                    <div class="dd-info-grid">
                        <div class="dd-info-card">
                            <div class="dd-info-label">Mùa đẹp</div>
                            <div class="dd-info-value">{safe_text(item.get("season"), "Quanh năm")}</div>
                        </div>

                        <div class="dd-info-card">
                            <div class="dd-info-label">Mã địa điểm</div>
                            <div class="dd-info-value">{slug_value}</div>
                        </div>
                    </div>

                    <div class="dd-highlight-wrap">
                        <div class="dd-highlight-title">Điểm nổi bật</div>
                        <div class="dd-chip-row">
                            {highlights_html}
                        </div>
                    </div>

                    <div class="dd-card-footer">
                        <a class="dd-detail-link"
                        href="{detail_href}"
                        target="_blank"
                        rel="noopener noreferrer"
                        onclick="window.open('{detail_href}', '_blank', 'noopener,noreferrer'); return false;">
                            Xem chi tiết
                        </a>
                    </div>
                </div>
            </div>
            """

        cards_html += "</div>"
        rows = result_count if result_count else 1
        cards_height = max(3000, result_count * 435)
    else:
        cards_html += """
        <div class="dd-empty">
            <div class="dd-empty-title">Chưa tìm thấy điểm đến phù hợp</div>
            <div class="dd-empty-text">
                Bạn hãy thử đổi từ khóa tìm kiếm hoặc chuyển bộ lọc về <strong>Tất cả</strong>
                để xem toàn bộ điểm đến đang có trong hệ thống.
            </div>
        </div>
        """
        cards_height = 320

    cards_html += "</div>"
    components.html(cards_css + cards_html, height=cards_height, scrolling=False)

elif page == "diemden_detail":
    import os
    import json
    import base64
    from html import escape
    from string import Template
    import streamlit.components.v1 as components

    try:
        with open("diemden.json", "r", encoding="utf-8") as f:
            diemden_data = json.load(f)
    except Exception as e:
        st.error(f"Lỗi đọc file diemden.json: {e}")
        st.stop()

    def clean_text(value):
        if value is None:
            return ""
        return " ".join(str(value).replace("\r", "\n").split())

    def normalize_text(value):
        return clean_text(value).lower()

    def safe_text(value, fallback="Đang cập nhật"):
        text = clean_text(value)
        return escape(text if text else fallback)

    def safe_url(value, fallback="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1600&auto=format&fit=crop"):
        text = str(value).strip() if value is not None else ""
        return escape(text if text else fallback, quote=True)
    
    DEFAULT_DETAIL_IMAGE = "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1600&auto=format&fit=crop"

    def file_to_data_uri(path):
        ext = os.path.splitext(path)[1].lower()
        mime_map = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp",
            ".gif": "image/gif",
            ".mp3": "audio/mpeg",
            ".wav": "audio/wav",
            ".ogg": "audio/ogg",
            ".m4a": "audio/mp4",
        }
        mime_type = mime_map.get(ext, "application/octet-stream")

        try:
            with open(path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
            return f"data:{mime_type};base64,{encoded}"
        except Exception:
            return ""

    def asset_to_src(value, fallback=DEFAULT_DETAIL_IMAGE):
        raw_value = str(value).strip() if value is not None else ""
        raw_fallback = str(fallback).strip() if fallback is not None else ""

        candidates = []
        if raw_value:
            candidates.append(raw_value)
        if raw_fallback:
            candidates.append(raw_fallback)

        for candidate in candidates:
            if candidate.startswith(("http://", "https://", "data:")):
                return escape(candidate, quote=True)

            if os.path.exists(candidate):
                data_uri = file_to_data_uri(candidate)
                if data_uri:
                    return data_uri

        return escape(DEFAULT_DETAIL_IMAGE, quote=True)

    def get_audio_src(place):
        candidates = []

        for key in ["audio_file", "audio", "audio_path", "thuyet_minh", "thuyetminh"]:
            val = str(place.get(key, "")).strip()
            if val:
                candidates.append(val)

        slug_value = str(place.get("slug", "")).strip()
        if slug_value:
            for ext in [".mp3", ".wav", ".m4a", ".ogg"]:
                candidates.append(os.path.join("assets", "audio", f"{slug_value}{ext}"))

        for candidate in candidates:
            if candidate.startswith(("http://", "https://", "data:")):
                return escape(candidate, quote=True)

            if os.path.exists(candidate):
                data_uri = file_to_data_uri(candidate)
                if data_uri:
                    return data_uri

        return ""

    def split_paragraphs(*values):
        results = []
        seen = set()

        for value in values:
            if value is None:
                continue
            text = str(value).replace("\r\n", "\n").replace("\r", "\n")
            parts = [p.strip() for p in text.split("\n") if p.strip()]
            if not parts and str(value).strip():
                parts = [str(value).strip()]

            for part in parts:
                normalized = " ".join(part.split()).strip()
                if normalized and normalized.lower() not in seen:
                    seen.add(normalized.lower())
                    results.append(normalized)
        return results

    def short_line(text, max_len=150):
        text = clean_text(text)
        if not text:
            return ""
        if len(text) <= max_len:
            return text
        trimmed = text[:max_len].rsplit(" ", 1)[0].strip()
        return (trimmed if trimmed else text[:max_len]).strip() + "..."

    def get_highlights(value):
        if isinstance(value, list):
            return [clean_text(x) for x in value if clean_text(x)]
        return []

    def get_images(place):
        images = []

        for key in ["image", "image_2", "image_3", "image_4", "image_5", "hero_image", "banner_image"]:
            val = place.get(key)
            if isinstance(val, str) and val.strip():
                images.append(val.strip())

        for key in ["gallery", "images", "detail_images"]:
            val = place.get(key)
            if isinstance(val, list):
                for item in val:
                    if isinstance(item, str) and item.strip():
                        images.append(item.strip())

        unique_images = []
        seen = set()
        for img in images:
            if img not in seen:
                seen.add(img)
                unique_images.append(img)

        if not unique_images:
            unique_images = [DEFAULT_DETAIL_IMAGE]

        while len(unique_images) < 8:
            unique_images.append(unique_images[-1])

        return [asset_to_src(x, DEFAULT_DETAIL_IMAGE) for x in unique_images[:8]]

    slug = str(st.query_params.get("slug", "")).strip()

    selected_place = None
    for item in diemden_data:
        if normalize_text(item.get("slug")) == normalize_text(slug):
            selected_place = item
            break

    if not selected_place:
        st.error("Không tìm thấy địa điểm.")
        st.stop()

    name_raw = clean_text(selected_place.get("name")) or "Đang cập nhật"
    area_raw = clean_text(selected_place.get("area"))
    category_raw = clean_text(selected_place.get("category"))
    season_raw = clean_text(selected_place.get("season"))
    best_time_raw = clean_text(selected_place.get("best_time"))
    short_desc_raw = clean_text(selected_place.get("short_desc"))
    full_desc_raw = str(selected_place.get("full_desc") or "").strip()
    slug_raw = clean_text(selected_place.get("slug"))

    name = escape(name_raw)
    area = safe_text(area_raw)
    category = safe_text(category_raw)
    season = safe_text(season_raw)
    best_time = safe_text(best_time_raw)
    slug_value = safe_text(slug_raw)

    paragraphs = split_paragraphs(selected_place.get("short_desc"), selected_place.get("full_desc"))
    highlights = get_highlights(selected_place.get("highlights"))

    intro_1 = paragraphs[0] if len(paragraphs) > 0 else f"{name_raw} là điểm đến đang được cập nhật nội dung chi tiết."
    intro_2 = paragraphs[1] if len(paragraphs) > 1 else (
        f"Địa điểm này thuộc khu vực {area_raw or 'Lào Cai'}, phù hợp để tham quan, khám phá và tìm hiểu giá trị địa phương."
    )

    culture_1 = paragraphs[2] if len(paragraphs) > 2 else (
        full_desc_raw if full_desc_raw else intro_1
    )
    culture_2 = paragraphs[3] if len(paragraphs) > 3 else (
        f"Thời điểm phù hợp để ghé thăm là {best_time_raw}."
        if best_time_raw else
        (f"Mùa đẹp để tham quan là {season_raw}." if season_raw else f"{name_raw} mang lại trải nghiệm khám phá giàu cảm xúc.")
    )

    standout_text = (
        f"Điểm nổi bật của {name_raw} gồm: {', '.join(highlights[:4])}."
        if highlights else
        f"{name_raw} gây ấn tượng bởi không gian, cảnh quan và trải nghiệm tham quan riêng biệt."
    )

    visit_text = (
        f"Khu vực {area_raw or 'địa phương'} phù hợp cho hành trình {category_raw.lower() if category_raw else 'tham quan'}, đặc biệt vào {best_time_raw or season_raw or 'thời điểm thích hợp trong năm'}."
    )

    hero_kicker = " • ".join([x for x in [area_raw, category_raw] if x]) or "Khám phá điểm đến"
    hero_subtitle = short_line(short_desc_raw or intro_1, 160)

    images = get_images(selected_place)
    team_image_src = asset_to_src("assets/anime_team.png", images[0])
    audio_src = get_audio_src(selected_place)

    narration_gallery = images[:]
    while len(narration_gallery) < 8:
        narration_gallery.append(narration_gallery[-1])
    narration_gallery = narration_gallery[:8]

    narration_image_1 = narration_gallery[0]
    narration_image_2 = narration_gallery[1]
    narration_image_3 = narration_gallery[2]
    narration_image_4 = narration_gallery[3]
    narration_image_5 = narration_gallery[4]
    narration_image_6 = narration_gallery[5]
    narration_image_7 = narration_gallery[6]
    narration_image_8 = narration_gallery[7]

    if audio_src:
        narration_audio_html = f"""
        <div class="ddt-audio-wrap">
            <audio controls preload="metadata" src="{audio_src}"></audio>
            <div class="ddt-audio-note">Bài thuyết minh riêng cho: {escape(name_raw)}</div>
        </div>
        """
    else:
        narration_audio_html = """
        <div class="ddt-audio-empty">
            Chưa tìm thấy file thuyết minh cho địa điểm này.
        </div>
        """
    hero_image = images[0]
    intro_image_big = images[0]
    intro_image_small = images[1]
    card_image_1 = images[2]
    card_image_2 = images[3]
    card_image_3 = images[4]
    culture_image_1 = images[1]
    culture_image_2 = images[2]
    culture_image_3 = images[3]
    standout_image_1 = images[4]
    standout_image_2 = images[5]
    standout_image_3 = images[0]
    standout_image_4 = images[2]

    if highlights:
        highlight_html = "".join(
            f'<span class="ddt-chip">{escape(item)}</span>' for item in highlights[:6]
        )
    else:
        highlight_html = '<span class="ddt-chip">Đang cập nhật</span>'

    news_titles = highlights[:5] if highlights else [
        f"Không gian nổi bật tại {name_raw}",
        f"Du khách khám phá {name_raw}",
        f"Hoạt động trải nghiệm quanh {name_raw}",
        f"Góc nhìn văn hóa tại {name_raw}",
        f"Hình ảnh ấn tượng về {name_raw}",
    ]

    while len(news_titles) < 5:
        news_titles.append(news_titles[-1])

    news_images = [images[0], images[1], images[2], images[3], images[4]]

    news_cards_html = "".join(
        f'''
        <div class="ddt-news-card">
            <div class="ddt-news-image" style="background-image:url('{news_images[i]}');"></div>
            <div class="ddt-news-caption">{escape(news_titles[i])}</div>
        </div>
        '''
        for i in range(5)
    )

    activity_title_seed = highlights[:6] if highlights else [
        f"Hoạt động nổi bật tại {name_raw}",
        f"Thông báo về {name_raw}",
        f"Cập nhật trải nghiệm tại {name_raw}",
        f"Sự kiện quanh {name_raw}",
        f"Góc nhìn mới về {name_raw}",
        f"Tin tức tham quan {name_raw}",
    ]

    while len(activity_title_seed) < 6:
        activity_title_seed.append(activity_title_seed[-1])

    activity_desc_seed = [
        short_line(culture_1, 120),
        short_line(culture_2, 120),
        short_line(intro_1, 120),
        short_line(intro_2, 120),
        short_line(standout_text, 120),
        short_line(visit_text, 120),
    ]

    activity_date_value = clean_text(selected_place.get("updated_at")) or "Đang cập nhật"

    activity_cards_html = "".join(
        f'''
        <div class="ddt-activity-card">
            <div class="ddt-activity-image" style="background-image:url('{images[i]}');"></div>
            <div class="ddt-activity-title-card">{escape(activity_title_seed[i])}</div>
            <div class="ddt-activity-desc">{escape(activity_desc_seed[i])}</div>
            <div class="ddt-activity-date">{escape(activity_date_value)}</div>
        </div>
        '''
        for i in range(6)
    )

    page_height = 7200 + max(0, len(full_desc_raw) // 600) * 240

    html_template = Template("""
    <style>
        html, body {
            margin: 0;
            padding: 0;
            background: #f3f3f3;
            font-family: "Segoe UI", Arial, sans-serif;
            color: #111827;
        }

        * {
            box-sizing: border-box;
        }

        .ddt-page {
            background: #f3f3f3;
            padding-bottom: 70px;
        }

        .ddt-wrap {
            max-width: 1320px;
            margin: 0 auto;
            padding: 0 24px;
        }
                             
        .ddt-narration-section {
            padding: 42px 0 8px 0;
        }

        .ddt-narration-box {
            background: transparent;
            border: none;
            border-radius: 0;
            padding: 28px 0;
            display: grid;
            grid-template-columns: 430px 1fr 430px;
            gap: 36px;
            align-items: center;
            box-shadow: none;
        }
                                    
        .ddt-narration-section .ddt-wrap {
            max-width: 1500px;
            padding: 0 18px;
        }

        .ddt-team-block {
            position: relative;
            min-height: 300px;
            display: flex;
            align-items: flex-end;
            justify-content: center;
        }

        .ddt-team-hello {
            position: absolute;
            top: 6px;
            left: 0;
            font-size: 46px;
            font-weight: 900;
            color: #7ed957;
            transform: rotate(-10deg);
            text-shadow: 0 4px 10px rgba(0,0,0,0.10);
            text-transform: uppercase;
        }

        .ddt-team-image {
            width: 100%;
            max-width: 420px;
            object-fit: contain;
            display: block;
            filter: drop-shadow(0 10px 18px rgba(15,23,42,0.10));
            -webkit-mask-image: linear-gradient(to bottom, rgba(0,0,0,1) 0%, rgba(0,0,0,1) 72%, rgba(0,0,0,0) 100%);
            mask-image: linear-gradient(to bottom, rgba(0,0,0,1) 0%, rgba(0,0,0,1) 72%, rgba(0,0,0,0) 100%);
        }
                             
        .ddt-narration-center {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            justify-content: center;
        }

        .ddt-narration-kicker {
            font-size: 13px;
            font-weight: 800;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: #475569;
            margin-bottom: 8px;
        }

        .ddt-narration-title {
            font-size: 60px;
            line-height: 0.95;
            margin: 0;
            color: #2f46c7;
            font-weight: 900;
            text-transform: uppercase;
        }

        .ddt-narration-subtitle {
            font-size: 22px;
            line-height: 1.4;
            font-weight: 800;
            color: #111827;
            text-transform: uppercase;
            margin-top: 5px;
            margin-left: 107px;
        }
        .ddt-narration-place {
            font-size: 16px;
            line-height: 1.7;
            color: #64748b;
            margin-top: 8px;
        }

        .ddt-audio-wrap {
            width: 100%;
            margin-top: 20px;
            background: #ffffff;
            border: 1px solid #eadcff;
            border-radius: 18px;
            padding: 14px 16px 12px 16px;
            box-shadow: 0 10px 20px rgba(168,85,247,0.08);
        }

        .ddt-audio-wrap audio {
            width: 100%;
            height: 44px;
        }

        .ddt-audio-note {
            margin-top: 8px;
            font-size: 13px;
            line-height: 1.6;
            color: #7c3aed;
            font-weight: 700;
        }

        .ddt-audio-empty {
            width: 100%;
            margin-top: 20px;
            padding: 18px 16px;
            border-radius: 18px;
            border: 1px dashed #cbd5e1;
            background: #ffffff;
            color: #64748b;
            font-size: 15px;
            line-height: 1.7;
            font-weight: 700;
        }

        .ddt-narration-collage {
            display: grid;
            grid-template-columns: 56px 84px 124px 84px 56px;
            grid-template-rows: 52px 80px 88px 80px 52px;
            gap: 10px;
            justify-content: center;
            align-content: center;
        }

        .ddt-narration-item {
            background-size: cover;
            background-position: center;
            border: 3px solid #ffffff;
            border-radius: 10px;
            box-shadow: 0 10px 20px rgba(15,23,42,0.10);
        }

        .ddt-ni-1 { grid-column: 1 / 2; grid-row: 2 / 4; }
        .ddt-ni-2 { grid-column: 2 / 3; grid-row: 1 / 3; }
        .ddt-ni-3 { grid-column: 3 / 4; grid-row: 1 / 3; }
        .ddt-ni-4 { grid-column: 4 / 5; grid-row: 1 / 3; }
        .ddt-ni-5 { grid-column: 2 / 3; grid-row: 3 / 5; }
        .ddt-ni-6 { grid-column: 3 / 5; grid-row: 3 / 4; }
        .ddt-ni-7 { grid-column: 3 / 4; grid-row: 4 / 6; }
        .ddt-ni-8 { grid-column: 5 / 6; grid-row: 2 / 4; }

        .ddt-hero {
            position: relative;
            width: 100%;
            min-height: 620px;
            border-radius: 0;
            overflow: hidden;
            background-image: url('$hero_image');
            background-size: cover;
            background-position: center;
            box-shadow: none;
        }

        .ddt-hero::before {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(180deg, rgba(0,0,0,0.18) 0%, rgba(0,0,0,0.34) 65%, rgba(0,0,0,0.42) 100%);
        }

        .ddt-hero-content {
            position: relative;
            z-index: 2;
            min-height: 560px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 32px;
            color: #ffffff;
        }

        .ddt-hero-kicker {
            font-size: 15px;
            font-weight: 800;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            margin-bottom: 16px;
        }

        .ddt-script {
            font-family: "Segoe Script", "Brush Script MT", cursive;
        }

        .ddt-hero-title {
            font-size: 72px;
            line-height: 1.05;
            font-weight: 800;
            margin: 0 0 14px 0;
            text-shadow: 0 4px 18px rgba(0,0,0,0.32);
        }

        .ddt-hero-subtitle {
            max-width: 760px;
            font-size: 19px;
            line-height: 1.7;
            font-weight: 700;
            text-transform: uppercase;
            text-shadow: 0 3px 14px rgba(0,0,0,0.28);
        }

        .ddt-section {
            position: relative;
            padding: 78px 0 10px 0;
        }

        .ddt-section::before {
            content: "";
            position: absolute;
            width: 430px;
            height: 430px;
            border: 1px solid rgba(15,23,42,0.04);
            border-radius: 50%;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            box-shadow:
                0 0 0 18px rgba(15,23,42,0.015),
                0 0 0 38px rgba(15,23,42,0.010);
            pointer-events: none;
        }

        .ddt-two-col {
            position: relative;
            z-index: 1;
            display: grid;
            grid-template-columns: 1.05fr 0.95fr;
            gap: 56px;
            align-items: center;
        }

        .ddt-two-col.reverse {
            grid-template-columns: 0.95fr 1.05fr;
        }

        .ddt-section-kicker {
            font-size: 15px;
            font-weight: 800;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: #334155;
            margin-bottom: 8px;
        }

        .ddt-section-title {
            font-size: 58px;
            line-height: 1.04;
            margin: 0 0 18px 0;
            color: #930000;
            font-weight: 800;
        }

        .ddt-text {
            font-size: 17px;
            line-height: 1.85;
            color: #374151;
            margin-bottom: 18px;
        }

        .ddt-button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 98px;
            padding: 11px 24px;
            border-radius: 999px;
            background: #f7b52a;
            color: #111827;
            text-decoration: none;
            font-size: 15px;
            font-weight: 800;
            box-shadow: 0 8px 18px rgba(247,181,42,0.24);
        }

        .ddt-meta-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 12px;
            margin: 24px 0 22px 0;
        }

        .ddt-meta-card {
            background: rgba(255,255,255,0.78);
            border: 1px solid #e8ebf0;
            border-radius: 18px;
            padding: 14px 16px;
            box-shadow: 0 10px 22px rgba(15,23,42,0.04);
        }

        .ddt-meta-label {
            font-size: 12px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #64748b;
            margin-bottom: 6px;
        }

        .ddt-meta-value {
            font-size: 16px;
            line-height: 1.6;
            font-weight: 700;
            color: #111827;
            word-break: break-word;
        }

        .ddt-chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 8px;
        }

        .ddt-chip {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 8px 13px;
            border-radius: 999px;
            background: #ffffff;
            border: 1px solid #e5e7eb;
            color: #334155;
            font-size: 13px;
            font-weight: 700;
            box-shadow: 0 6px 16px rgba(15,23,42,0.04);
        }

        .ddt-collage-left {
            position: relative;
            min-height: 520px;
        }

        .ddt-collage-left .main {
            width: 74%;
            height: 500px;
            background-size: cover;
            background-position: center;
            box-shadow: 0 16px 36px rgba(15,23,42,0.10);
        }

        .ddt-collage-left .small {
            position: absolute;
            right: 0;
            top: 110px;
            width: 40%;
            height: 290px;
            background-size: cover;
            background-position: center;
            box-shadow: 0 16px 36px rgba(15,23,42,0.12);
        }

        .ddt-card-section {
            padding: 56px 0 14px 0;
        }

        .ddt-center-heading {
            text-align: center;
            margin-bottom: 34px;
        }

        .ddt-card-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 30px;
        }

        .ddt-card {
            text-align: center;
        }

        .ddt-card-image {
            width: 100%;
            height: 310px;
            border-radius: 4px;
            background-size: cover;
            background-position: center;
            box-shadow: 0 14px 30px rgba(15,23,42,0.08);
        }

        .ddt-card-title {
            margin: 18px 0 10px 0;
            font-size: 18px;
            line-height: 1.4;
            font-weight: 900;
            color: #0f172a;
            text-transform: uppercase;
        }

        .ddt-card-desc {
            font-size: 15px;
            line-height: 1.7;
            color: #475569;
            max-width: 88%;
            margin: 0 auto 16px auto;
        }

        .ddt-mosaic-right {
            position: relative;
            min-height: 540px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            grid-template-rows: 330px 140px;
            gap: 18px;
        }

        .ddt-mosaic-right .img-a {
            grid-column: 1 / 3;
            grid-row: 1 / 2;
        }

        .ddt-mosaic-right .img-b {
            grid-column: 1 / 2;
            grid-row: 2 / 3;
        }

        .ddt-mosaic-right .img-c {
            grid-column: 2 / 3;
            grid-row: 2 / 3;
        }

        .ddt-mosaic-right .img-a,
        .ddt-mosaic-right .img-b,
        .ddt-mosaic-right .img-c {
            background-size: cover;
            background-position: center;
            border-radius: 4px;
            box-shadow: 0 14px 30px rgba(15,23,42,0.08);
        }

        .ddt-mosaic-left {
            position: relative;
            min-height: 540px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            grid-template-rows: 260px 190px 150px;
            gap: 18px;
        }

        .ddt-mosaic-left .img-a {
            grid-column: 1 / 2;
            grid-row: 1 / 3;
        }

        .ddt-mosaic-left .img-b {
            grid-column: 2 / 3;
            grid-row: 1 / 2;
        }

        .ddt-mosaic-left .img-c {
            grid-column: 1 / 2;
            grid-row: 3 / 4;
        }

        .ddt-mosaic-left .img-d {
            grid-column: 2 / 3;
            grid-row: 2 / 4;
        }

        .ddt-mosaic-left .img-a,
        .ddt-mosaic-left .img-b,
        .ddt-mosaic-left .img-c,
        .ddt-mosaic-left .img-d {
            background-size: cover;
            background-position: center;
            border-radius: 4px;
            box-shadow: 0 14px 30px rgba(15,23,42,0.08);
        }
                             
        .ddt-news-section{
            position: relative;
            margin-top: 42px;
            background: #a50000;
            padding: 48px 0 52px 0;
            overflow: hidden;
        }

        .ddt-news-section::before{
            content:"";
            position:absolute;
            width:520px;
            height:520px;
            left:50%;
            top:50%;
            transform:translate(-50%, -50%);
            border-radius:50%;
            border:1px solid rgba(255,255,255,0.08);
            box-shadow:
                0 0 0 20px rgba(255,255,255,0.035),
                0 0 0 42px rgba(255,255,255,0.02);
            pointer-events:none;
        }

        .ddt-news-head{
            position:relative;
            z-index:2;
            text-align:center;
            margin-bottom:22px;
        }

        .ddt-news-kicker{
            font-size:15px;
            font-weight:800;
            letter-spacing:0.16em;
            text-transform:uppercase;
            color:rgba(255,255,255,0.86);
            margin-bottom:8px;
        }

        .ddt-news-title{
            font-size:42px;
            line-height:1.05;
            margin:0;
            color:#ffffff;
            font-weight:800;
        }

        #tin-tuc-le-hoi .ddt-wrap{
            max-width:100%;
            padding:0;
        }

        .ddt-news-slider{
            position:relative;
            z-index:2;
            overflow:hidden;
        }

        .ddt-news-viewport{
            overflow:hidden;
            padding:0 24px;
        }

        .ddt-news-track{
            display:flex;
            gap:16px;
            transition:transform 0.5s ease;
            will-change:transform;
        }

        .ddt-news-card{
            flex:0 0 30%;
            min-width:0;
        }

        .ddt-news-image{
            width:100%;
            height:260px;
            background-size:cover;
            background-position:center;
            box-shadow:0 18px 36px rgba(0,0,0,0.14);
        }

        .ddt-news-caption{
            margin-top:14px;
            font-size:16px;
            line-height:1.6;
            font-weight:700;
            color:#ffffff;
            text-align:center;
        }

        .ddt-news-controls{
            position:relative;
            z-index:2;
            display:flex;
            justify-content:center;
            gap:14px;
            margin-top:18px;
        }
        .ddt-news-btn{
            width:42px;
            height:42px;
            border:none;
            border-radius:50%;
            background:#ffffff;
            color:#7c2d12;
            font-size:20px;
            font-weight:800;
            cursor:pointer;
            box-shadow:0 8px 18px rgba(0,0,0,0.14);
        }

        .ddt-news-btn:disabled{
            opacity:0.45;
            cursor:not-allowed;
        }
                             
        .ddt-activity-section{
            padding:72px 0 50px 0;
            background:#f3f3f3;
        }

        .ddt-activity-head{
            text-align:center;
            margin-bottom:34px;
        }

        .ddt-activity-kicker{
            font-size:15px;
            font-weight:800;
            letter-spacing:0.16em;
            text-transform:uppercase;
            color:#334155;
            margin-bottom:10px;
        }

        .ddt-activity-title{
            font-size:56px;
            line-height:1.05;
            margin:0;
            color:#930000;
            font-weight:800;
        }

        .ddt-activity-grid{
            display:grid;
            grid-template-columns:repeat(3, minmax(0, 1fr));
            gap:32px 26px;
        }

        .ddt-activity-card{
            min-width:0;
        }

        .ddt-activity-image{
            width:100%;
            height:215px;
            background-size:cover;
            background-position:center;
            margin-bottom:14px;
        }

        .ddt-activity-title-card{
            font-size:17px;
            line-height:1.45;
            font-weight:900;
            color:#111827;
            margin-bottom:10px;
            text-transform:uppercase;
        }

        .ddt-activity-desc{
            font-size:15px;
            line-height:1.7;
            color:#475569;
            margin-bottom:10px;
        }

        .ddt-activity-date{
            font-size:14px;
            font-weight:500;
            color:#64748b;
        }

        @media (max-width: 1100px) {
            .ddt-two-col,
            .ddt-two-col.reverse {
                grid-template-columns: 1fr;
                gap: 34px;
            }

            .ddt-card-grid {
                grid-template-columns: 1fr;
                gap: 24px;
            }

            .ddt-card-image {
                height: 280px;
            }

            .ddt-hero-title {
                font-size: 56px;
            }

            .ddt-section-title {
                font-size: 48px;
            }
                
            .ddt-news-title {
                font-size: 46px;
            }

            .ddt-news-card {
                flex: 0 0 44%;
            }

            .ddt-news-image {
                height: 230px;
            }
                            
            .ddt-activity-title{
                font-size:46px;
            }

            .ddt-activity-grid{
                grid-template-columns:repeat(2, minmax(0, 1fr));
            }

            .ddt-activity-image{
                height:210px;
            }
                             
            .ddt-narration-box {
                grid-template-columns: 1fr;
                gap: 22px;
            }

            .ddt-narration-center {
                align-items: center;
                text-align: center;
            }

            .ddt-team-block {
                min-height: 260px;
            }
        }

        @media (max-width: 768px) {
            .ddt-wrap {
                padding: 0 14px;
            }

            .ddt-hero {
                min-height: 420px;
                border-radius: 22px;
            }

            .ddt-hero-content {
                min-height: 420px;
                padding: 24px 18px;
            }

            .ddt-hero-title {
                font-size: 40px;
            }

            .ddt-hero-subtitle {
                font-size: 15px;
            }

            .ddt-section {
                padding: 52px 0 4px 0;
            }

            .ddt-section-title {
                font-size: 38px;
            }

            .ddt-text {
                font-size: 15px;
            }

            .ddt-meta-grid {
                grid-template-columns: 1fr;
            }

            .ddt-collage-left {
                min-height: auto;
                display: flex;
                flex-direction: column;
                gap: 16px;
            }

            .ddt-collage-left .main,
            .ddt-collage-left .small {
                position: relative;
                width: 100%;
                height: 240px;
                top: auto;
                right: auto;
            }

            .ddt-mosaic-right,
            .ddt-mosaic-left {
                min-height: auto;
                grid-template-columns: 1fr;
                grid-template-rows: none;
            }

            .ddt-mosaic-right .img-a,
            .ddt-mosaic-right .img-b,
            .ddt-mosaic-right .img-c,
            .ddt-mosaic-left .img-a,
            .ddt-mosaic-left .img-b,
            .ddt-mosaic-left .img-c,
            .ddt-mosaic-left .img-d {
                grid-column: auto;
                grid-row: auto;
                height: 220px;
            }
                             
            .ddt-news-section {
                padding: 56px 0 64px 0;
            }

            .ddt-news-title {
                font-size: 36px;
            }

            .ddt-news-card {
                flex: 0 0 86%;
            }

            .ddt-news-image {
                height: 190px;
            }

            .ddt-news-caption {
                font-size: 15px;
            }
                             
            .ddt-activity-section{
                padding:56px 0 36px 0;
            }

            .ddt-activity-title{
                font-size:36px;
            }

            .ddt-activity-grid{
                grid-template-columns:1fr;
                gap:24px;
            }

            .ddt-activity-image{
                height:220px;
            }
                             
            .ddt-narration-box {
                padding: 20px 16px;
                border-radius: 20px;
            }

            .ddt-team-hello {
                font-size: 34px;
            }

            .ddt-team-image {
                max-width: 240px;
            }

            .ddt-narration-title {
                font-size: 42px;
            }

            .ddt-narration-subtitle {
                font-size: 17px;
            }

            .ddt-narration-collage {
                grid-template-columns: repeat(3, 1fr);
                grid-template-rows: none;
            }

            .ddt-ni-1, .ddt-ni-2, .ddt-ni-3, .ddt-ni-4,
            .ddt-ni-5, .ddt-ni-6, .ddt-ni-7, .ddt-ni-8 {
                grid-column: auto;
                grid-row: auto;
                min-height: 90px;
            }
        }
    </style>

    <div class="ddt-page">
        <section class="ddt-hero">
            <div class="ddt-hero-content">
                <h1 class="ddt-hero-title ddt-script">$name</h1>
                <div class="ddt-hero-subtitle">$hero_subtitle</div>
            </div>
        </section>

        <section class="ddt-narration-section" id="thuyet-minh">
            <div class="ddt-wrap">
                <div class="ddt-narration-box">

                    <div class="ddt-team-block">
                        <img class="ddt-team-image" src="$team_image_src" alt="Đội thuyết minh" />
                    </div>

                    <div class="ddt-narration-center">
                        <div class="ddt-narration-kicker"></div>
                        <h2 class="ddt-narration-title">Thuyết minh</h2>
                        <div class="ddt-narration-subtitle">Nghe thuyết minh tại đây</div>
                        $narration_audio_html
                    </div>

                    <div class="ddt-narration-collage">
                        <div class="ddt-narration-item ddt-ni-1" style="background-image:url('$narration_image_1');"></div>
                        <div class="ddt-narration-item ddt-ni-2" style="background-image:url('$narration_image_2');"></div>
                        <div class="ddt-narration-item ddt-ni-3" style="background-image:url('$narration_image_3');"></div>
                        <div class="ddt-narration-item ddt-ni-4" style="background-image:url('$narration_image_4');"></div>
                        <div class="ddt-narration-item ddt-ni-5" style="background-image:url('$narration_image_5');"></div>
                        <div class="ddt-narration-item ddt-ni-6" style="background-image:url('$narration_image_6');"></div>
                        <div class="ddt-narration-item ddt-ni-7" style="background-image:url('$narration_image_7');"></div>
                        <div class="ddt-narration-item ddt-ni-8" style="background-image:url('$narration_image_8');"></div>
                    </div>

                </div>
            </div>
        </section>
                             
        <section class="ddt-section" id="gioi-thieu">
            <div class="ddt-wrap">
                <div class="ddt-two-col">
                    <div class="ddt-collage-left">
                        <div class="main" style="background-image:url('$intro_image_big');"></div>
                        <div class="small" style="background-image:url('$intro_image_small');"></div>
                    </div>

                    <div>
                        <div class="ddt-section-kicker">Về điểm đến</div>
                        <h2 class="ddt-section-title ddt-script">Giới thiệu</h2>

                        <div class="ddt-text">$intro_1</div>
                        <div class="ddt-text">$intro_2</div>

                        <div class="ddt-meta-grid">
                            <div class="ddt-meta-card">
                                <div class="ddt-meta-label">Khu vực</div>
                                <div class="ddt-meta-value">$area</div>
                            </div>

                            <div class="ddt-meta-card">
                                <div class="ddt-meta-label">Loại hình</div>
                                <div class="ddt-meta-value">$category</div>
                            </div>

                            <div class="ddt-meta-card">
                                <div class="ddt-meta-label">Mùa đẹp</div>
                                <div class="ddt-meta-value">$season</div>
                            </div>

                            <div class="ddt-meta-card">
                                <div class="ddt-meta-label">Mã địa điểm</div>
                                <div class="ddt-meta-value">$slug_value</div>
                            </div>
                        </div>

                        <div class="ddt-chip-row">
                            $highlight_html
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section class="ddt-card-section" id="kham-pha">
            <div class="ddt-wrap">
                <div class="ddt-center-heading">
                    <div class="ddt-section-kicker">Đầu tư</div>
                    <h2 class="ddt-section-title ddt-script">Khám phá</h2>
                </div>

                <div class="ddt-card-grid">
                    <div class="ddt-card">
                        <div class="ddt-card-image" style="background-image:url('$card_image_1');"></div>
                        <div class="ddt-card-title">Văn hóa, lịch sử</div>
                        <div class="ddt-card-desc">Tìm hiểu chiều sâu văn hóa và những nét nổi bật gắn với $name.</div>
                    </div>

                    <div class="ddt-card">
                        <div class="ddt-card-image" style="background-image:url('$card_image_2');"></div>
                        <div class="ddt-card-title">Điểm nổi bật</div>
                        <div class="ddt-card-desc">Khám phá các chi tiết giúp địa điểm này tạo dấu ấn trong hành trình tham quan.</div>
                    </div>

                    <div class="ddt-card">
                        <div class="ddt-card-image" style="background-image:url('$card_image_3');"></div>
                        <div class="ddt-card-title">Thông tin tham quan</div>
                        <div class="ddt-card-desc">Xem nhanh khu vực, thời điểm phù hợp và gợi ý trải nghiệm trước khi ghé thăm.</div>
                    </div>
                </div>
            </div>
        </section>

        <section class="ddt-section" id="van-hoa-lich-su">
            <div class="ddt-wrap">
                <div class="ddt-two-col reverse">
                    <div>
                        <div class="ddt-section-kicker">Khám phá</div>
                        <h2 class="ddt-section-title ddt-script">Văn hóa, lịch sử</h2>

                        <div class="ddt-text">$culture_1</div>
                        <div class="ddt-text">$culture_2</div>

                    </div>

                    <div class="ddt-mosaic-right">
                        <div class="img-a" style="background-image:url('$culture_image_1');"></div>
                        <div class="img-b" style="background-image:url('$culture_image_2');"></div>
                        <div class="img-c" style="background-image:url('$culture_image_3');"></div>
                    </div>
                </div>
            </div>
        </section>

        <section class="ddt-section" id="diem-noi-bat">
            <div class="ddt-wrap">
                <div class="ddt-two-col">
                    <div class="ddt-mosaic-left">
                        <div class="img-a" style="background-image:url('$standout_image_1');"></div>
                        <div class="img-b" style="background-image:url('$standout_image_2');"></div>
                        <div class="img-c" style="background-image:url('$standout_image_3');"></div>
                        <div class="img-d" style="background-image:url('$standout_image_4');"></div>
                    </div>

                    <div id="tham-quan">
                        <div class="ddt-section-kicker">Tham quan</div>
                        <h2 class="ddt-section-title ddt-script">Quần thể di tích</h2>

                        <div class="ddt-text">$standout_text</div>
                        <div class="ddt-text">$visit_text</div>

                        <div class="ddt-meta-grid">
                            <div class="ddt-meta-card">
                                <div class="ddt-meta-label">Thời điểm phù hợp</div>
                                <div class="ddt-meta-value">$best_time</div>
                            </div>

                            <div class="ddt-meta-card">
                                <div class="ddt-meta-label">Mùa tham quan</div>
                                <div class="ddt-meta-value">$season</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
                        
        <section class="ddt-news-section" id="tin-tuc-le-hoi">
            <div class="ddt-wrap">
                <div class="ddt-news-head">
                    <div class="ddt-news-kicker">Thông tin</div>
                    <h2 class="ddt-news-title ddt-script">Tin tức lễ hội</h2>
                </div>

                <div class="ddt-news-slider">
                    <div class="ddt-news-viewport">
                        <div class="ddt-news-track" id="ddtNewsTrack">
                            $news_cards_html
                        </div>
                    </div>

                    <div class="ddt-news-controls">
                        <button class="ddt-news-btn" id="ddtNewsPrev">‹</button>
                        <button class="ddt-news-btn" id="ddtNewsNext">›</button>
                    </div>
                </div>
            </div>
        </section>

        <script>
        (function () {
            const track = document.getElementById("ddtNewsTrack");
            const prevBtn = document.getElementById("ddtNewsPrev");
            const nextBtn = document.getElementById("ddtNewsNext");

            if (!track || !prevBtn || !nextBtn) return;

            let currentIndex = 0;

            function getVisibleCount() {
                if (window.innerWidth <= 768) return 1;
                if (window.innerWidth <= 1100) return 2;
                return 3;
            }

            function updateSlider() {
                const cards = track.querySelectorAll(".ddt-news-card");
                if (!cards.length) return;

                const gap = 18;
                const cardWidth = cards[0].offsetWidth + gap;
                const maxIndex = Math.max(0, cards.length - getVisibleCount());

                if (currentIndex > maxIndex) currentIndex = maxIndex;

                const peekOffset = 110;
                track.style.transform = 'translateX(-' + ((currentIndex * cardWidth) + peekOffset) + 'px)';
                prevBtn.disabled = currentIndex === 0;
                nextBtn.disabled = currentIndex >= maxIndex;
            }

            prevBtn.addEventListener("click", function () {
                if (currentIndex > 0) {
                    currentIndex--;
                    updateSlider();
                }
            });

            nextBtn.addEventListener("click", function () {
                const cards = track.querySelectorAll(".ddt-news-card");
                const maxIndex = Math.max(0, cards.length - getVisibleCount());
                if (currentIndex < maxIndex) {
                    currentIndex++;
                    updateSlider();
                }
            });

            window.addEventListener("resize", updateSlider);
            setTimeout(updateSlider, 120);
        })();
        </script>

        </div>
                             
        <section class="ddt-activity-section" id="tin-tuc-hoat-dong">
            <div class="ddt-wrap">
                <div class="ddt-activity-head">
                    <div class="ddt-activity-kicker">Thông tin</div>
                    <h2 class="ddt-activity-title ddt-script">Tin tức hoạt động</h2>
                </div>

                <div class="ddt-activity-grid">
                    $activity_cards_html
                </div>
            </div>
        </section>
    </div>
    """)

    html_output = html_template.substitute(
        hero_image=hero_image,
        hero_kicker=escape(hero_kicker),
        name=name,
        hero_subtitle=escape(hero_subtitle),
        intro_image_big=intro_image_big,
        intro_image_small=intro_image_small,
        intro_1=escape(intro_1),
        intro_2=escape(intro_2),
        area=area,
        category=category,
        season=season,
        slug_value=slug_value,
        highlight_html=highlight_html,
        card_image_1=card_image_1,
        card_image_2=card_image_2,
        card_image_3=card_image_3,
        culture_1=escape(culture_1),
        culture_2=escape(culture_2),
        culture_image_1=culture_image_1,
        culture_image_2=culture_image_2,
        culture_image_3=culture_image_3,
        standout_image_1=standout_image_1,
        standout_image_2=standout_image_2,
        standout_image_3=standout_image_3,
        standout_image_4=standout_image_4,
        standout_text=escape(standout_text),
        visit_text=escape(visit_text),
        best_time=best_time,
        news_cards_html=news_cards_html,
        activity_cards_html=activity_cards_html,

        team_image_src=team_image_src,
        narration_audio_html=narration_audio_html,
        narration_image_1=narration_image_1,
        narration_image_2=narration_image_2,
        narration_image_3=narration_image_3,
        narration_image_4=narration_image_4,
        narration_image_5=narration_image_5,
        narration_image_6=narration_image_6,
        narration_image_7=narration_image_7,
        narration_image_8=narration_image_8,
    )

    components.html(html_output, height=page_height, scrolling=False)

elif page == "chatbot":
    import base64
    from html import escape
    import streamlit.components.v1 as components

    def _image_to_data_uri(candidates):
        mime_map = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp"
        }

        for path in candidates:
            if path and os.path.exists(path):
                ext = os.path.splitext(path)[1].lower()
                mime = mime_map.get(ext, "image/png")
                try:
                    with open(path, "rb") as f:
                        encoded = base64.b64encode(f.read()).decode("utf-8")
                    return f"data:{mime};base64,{encoded}"
                except Exception:
                    pass
        return ""

    logo_src = _image_to_data_uri([
        "assets/anime_teamlogo.png",
        "anime_teamlogo.png"
    ])

    default_bot_message = (
        "Xin chào! Mình là trợ lý AI của Lao Cai Heritage AI. "
        "Bạn có thể hỏi về điểm đến, lịch trình, mùa đẹp hoặc chi phí tham khảo."
    )

    if "gemini_messages" not in st.session_state:
        st.session_state.gemini_messages = [
            {
                "role": "assistant",
                "content": default_bot_message
            }
        ]

    def send_chat_message(user_text: str):
        clean_user_text = str(user_text or "").strip()
        if not clean_user_text:
            return

        st.session_state.gemini_messages.append({
            "role": "user",
            "content": clean_user_text
        })

        answer = ask_gemini(
            user_message=clean_user_text,
            payload=CHATBOT_PAYLOAD,
            current_page=page,
            messages=st.session_state.gemini_messages[:-1]
        )

        st.session_state.gemini_messages.append({
            "role": "assistant",
            "content": answer
        })

    suggestion_questions = [
        "Sa Pa có gì đẹp?",
        "Mùa nào đi Fansipan đẹp?",
        "Gợi ý lịch trình đi Bắc Hà",
        "Chi phí đi Sa Pa 2 ngày",
        "Đền Bảo Hà có gì nổi bật?",
        "Thời tiết Lào Cai hôm nay"
    ]

    st.markdown("""
    <style>
    /* khung ngoài chatbot */
    .chatbot-page-title{
        max-width: 1420px;
        margin: 16px auto 8px auto;
        padding: 0 14px;
        box-sizing: border-box;
    }

    /* 2 khối chính */
    div[data-testid="stVerticalBlockBorderWrapper"]{
        border: 2px solid #bfeeee !important;
        border-radius: 28px !important;
        background: #ffffff !important;
        box-shadow: 0 14px 28px rgba(15,23,42,0.05) !important;
        padding: 14px 16px 16px 16px !important;
        min-height: 760px !important;
    }

    .chat-divider{
        width: 2px;
        height: 760px;
        margin: 0 auto;
        border-radius: 999px;
        background: linear-gradient(
            to bottom,
            rgba(143,231,231,0.00) 0%,
            rgba(143,231,231,0.35) 12%,
            rgba(143,231,231,0.50) 50%,
            rgba(143,231,231,0.35) 88%,
            rgba(143,231,231,0.00) 100%
        );
        filter: blur(0.6px);
        opacity: 0.65;
        box-shadow: 0 0 10px rgba(143,231,231,0.18);
    }

    .chat-left-logo-wrap{
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 290px;
        margin-bottom: 18px;
    }

    .chat-left-logo{
        width: 100%;
        max-width: 310px;
        object-fit: contain;
        display: block;
        filter: drop-shadow(0 10px 18px rgba(15,23,42,0.10));
        -webkit-mask-image: linear-gradient(
            to bottom,
            rgba(0,0,0,1) 0%,
            rgba(0,0,0,1) 72%,
            rgba(0,0,0,0.88) 82%,
            rgba(0,0,0,0.55) 90%,
            rgba(0,0,0,0.18) 96%,
            rgba(0,0,0,0) 100%
        );
        mask-image: linear-gradient(
            to bottom,
            rgba(0,0,0,1) 0%,
            rgba(0,0,0,1) 72%,
            rgba(0,0,0,0.88) 82%,
            rgba(0,0,0,0.55) 90%,
            rgba(0,0,0,0.18) 96%,
            rgba(0,0,0,0) 100%
        );
    }

    .chat-left-title{
        text-align: center;
        font-size: 16px;
        font-weight: 800;
        color: #334155;
        margin: 2px 0 16px 0;
        line-height: 1.6;
    }

    .chat-right-head{
        padding: 2px 6px 8px 6px;
        margin-bottom: 6px;
    }

    .chat-right-title{
        font-size: 34px;
        font-weight: 900;
        color: #111827;
        line-height: 1.1;
        margin-bottom: 6px;
    }

    .chat-right-subtitle{
        font-size: 15px;
        line-height: 1.8;
        color: #64748b;
    }

    .chat-bottom-note{
        margin-top: 8px;
        font-size: 13px;
        line-height: 1.6;
        color: #64748b;
        padding-left: 4px;
    }

    /* nút gợi ý bên trái */
        div[data-testid="stButton"] > button{
        width: 100%;
        min-height: 35px !important;
        border-radius: 16px !important;
        border: 1.5px solid #bfeeee !important;
        background: #ffffff !important;
        color: #4b6472 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        text-align: center !important;
        justify-content: center !important;
        padding: 0 14px !important;
        box-shadow: none !important;
        margin-bottom: 0px !important;
    }

    div[data-testid="stButton"] > button:hover{
        background: #f7ffff !important;
        border-color: #7ee4e4 !important;
        color: #334155 !important;
    }

    /* ô nhập */
    div[data-testid="stTextInput"] input{
        min-height: 36px !important;
        border-radius: 999px !important;
        border: 2px solid #111827 !important;
        background: #ffffff !important;
        color: #111827 !important;
        font-size: 17px !important;
        padding-left: 20px !important;
        padding-right: 20px !important;
        box-shadow: none !important;
    }

    div[data-testid="stTextInput"] input::placeholder{
        color: #94a3b8 !important;
    }

    @media (max-width: 992px){
        div[data-testid="stVerticalBlockBorderWrapper"]{
            min-height: auto !important;
        }

        .chat-divider{
            display: none;
        }

        .chat-right-title{
            font-size: 28px;
        }
                
    .chat-input-wrap{
    width: 100%;
    display: flex;
    justify-content: center;
    margin-top: 14px;
    margin-bottom: 6px;
}

    .chat-input-wrap > div{
        width: 92%;
        max-width: 760px;
    }

    .chat-input-wrap div[data-testid="stForm"]{
        margin: 0 !important;
        padding: 0 !important;
        background: transparent !important;
        box-shadow: none !important;
        border: none !important;
    }

    .chat-input-wrap div[data-testid="stTextInput"]{
        margin-bottom: 0 !important;
    }

    .chat-input-wrap{
        width: 100%;
        margin-top: 14px;
    }

    .chat-input-wrap div[data-testid="stForm"]{
        margin: 0 !important;
        padding: 0 !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    .chat-input-wrap div[data-testid="stForm"] > div{
        width: 100%;
    }

    .chat-input-wrap div[data-testid="stHorizontalBlock"]{
        gap: 0 !important;
        align-items: center !important;
    }

    .chat-input-wrap div[data-testid="stTextInput"]{
        margin-bottom: 0 !important;
    }

    .chat-input-wrap div[data-testid="stTextInput"] > div{
        position: relative !important;
    }

    .chat-input-wrap div[data-testid="stTextInput"] input{
        height: 68px !important;
        min-height: 68px !important;
        border-radius: 999px !important;
        border: 1.8px solid #b9d9ff !important;
        background: #f3f6fb !important;
        color: #111827 !important;
        font-size: 18px !important;
        padding-left: 34px !important;
        padding-right: 88px !important;
        box-shadow: none !important;
    }

    .chat-input-wrap div[data-testid="stTextInput"] input::placeholder{
        color: #7b8ba1 !important;
    }

    .chat-input-wrap div[data-testid="stFormSubmitButton"]{
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin-left: -64px !important;
        z-index: 5 !important;
        width: 56px !important;
        min-width: 56px !important;
    }

    .chat-input-wrap div[data-testid="stFormSubmitButton"] button{
        width: 40px !important;
        height: 40px !important;
        min-width: 40px !important;
        min-height: 40px !important;
        border-radius: 50% !important;
        border: none !important;
        background: linear-gradient(180deg, #58b8ff 0%, #339af0 100%) !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: 900 !important;
        padding: 0 !important;
        box-shadow: 0 6px 14px rgba(51,154,240,0.28) !important;
    }

    .chat-input-wrap div[data-testid="stFormSubmitButton"] button:hover{
        background: linear-gradient(180deg, #4aaeff 0%, #228be6 100%) !important;
    }

    .chat-input-wrap div[data-testid="stForm"] [data-testid="stCaptionContainer"],
    .chat-input-wrap div[data-testid="stForm"] p{
        display: none !important;
    }

    }
    </style>
    """, unsafe_allow_html=True)

    outer_left, outer_mid, outer_right = st.columns([0.02, 0.96, 0.02])

    with outer_mid:
        left_col, divider_col, right_col = st.columns([0.35, 0.02, 0.63], gap="small")

        with left_col:
            with st.container(border=False):
                if logo_src:
                    st.markdown(f"""
                    <div class="chat-left-logo-wrap">
                        <img class="chat-left-logo" src="{logo_src}" alt="anime_teamlogo">
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="chat-left-logo-wrap">
                        <div class="chat-left-title">Chưa tìm thấy ảnh anime_teamlogo.png</div>
                    </div>
                    """, unsafe_allow_html=True)

                for idx, question in enumerate(suggestion_questions):
                    if st.button(question, key=f"chat_suggest_{idx}", use_container_width=True):
                        send_chat_message(question)
                        st.rerun()

        with divider_col:
            st.markdown('<div class="chat-divider"></div>', unsafe_allow_html=True)

        with right_col:
            with st.container(border=False):
                st.markdown("""
                <div class="chat-right-head">
                    <div class="chat-right-title">Xin chào</div>
                    <div class="chat-right-subtitle">
                        Hỏi bất kì điều gì về điểm đến, lịch trình và trải nghiệm du lịch tại Lào Cai.
                    </div>
                </div>
                """, unsafe_allow_html=True)

                message_blocks = []
                for msg in st.session_state.gemini_messages[-40:]:
                    role = "user" if msg.get("role") == "user" else "assistant"
                    content = escape(str(msg.get("content", ""))).replace("\n", "<br>")
                    message_blocks.append(
                        f'<div class="msg-row {role}"><div class="msg-bubble {role}">{content}</div></div>'
                    )

                messages_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <style>
                        html, body {{
                            margin: 0;
                            padding: 0;
                            background: transparent;
                            font-family: "Segoe UI", Arial, sans-serif;
                        }}

                        .msg-wrap {{
                            height: 560px;
                            overflow-y: auto;
                            padding: 8px 4px 10px 4px;
                            box-sizing: border-box;
                            background: #f7f7f7;
                            border-radius: 22px;
                        }}

                        .msg-row {{
                            display: flex;
                            margin-bottom: 16px;
                        }}

                        .msg-row.user {{
                            justify-content: flex-end;
                        }}

                        .msg-row.assistant {{
                            justify-content: flex-start;
                        }}

                        .msg-bubble {{
                            max-width: 76%;
                            padding: 14px 18px;
                            font-size: 16px;
                            line-height: 1.75;
                            color: #111827;
                            word-break: break-word;
                            box-sizing: border-box;
                            box-shadow: 0 6px 14px rgba(15,23,42,0.04);
                        }}

                        .msg-bubble.user {{
                            background: #dddddd;
                            border-radius: 18px 18px 8px 18px;
                        }}

                        .msg-bubble.assistant {{
                            background: #e9e9e9;
                            border-radius: 18px 18px 18px 8px;
                        }}
                    </style>
                </head>
                <body>
                    <div class="msg-wrap" id="msgWrap">
                        {''.join(message_blocks)}
                    </div>

                    <script>
                        const box = document.getElementById("msgWrap");
                        if (box) {{
                            box.scrollTop = box.scrollHeight;
                        }}
                    </script>
                </body>
                </html>
                """

                components.html(messages_html, height=575, scrolling=False)

                st.markdown('<div class="chat-input-wrap">', unsafe_allow_html=True)

                with st.form("gemini_chat_main_form", clear_on_submit=True, border=False):
                    input_col, send_col = st.columns([0.94, 0.06], gap="small")

                    with input_col:
                        user_text = st.text_input(
                            "Nhập câu hỏi",
                            placeholder="Hỏi bất cứ điều gì...",
                            label_visibility="collapsed"
                        )

                    with send_col:
                        submitted = st.form_submit_button("↑", use_container_width=True)

                st.markdown('</div>', unsafe_allow_html=True)

                if submitted and user_text.strip():
                    send_chat_message(user_text.strip())
                    st.rerun()

elif page == "gioithieu":
    import json
    from html import escape
    import streamlit.components.v1 as components

    def load_json_list(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception:
            return []

    DEFAULT_IMG = "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1600&auto=format&fit=crop"

    def safe_url(value, fallback=DEFAULT_IMG):
        text = str(value).strip() if value is not None else ""
        return escape(text if text else fallback, quote=True)

    def get_image(data, idx, fallback=DEFAULT_IMG):
        try:
            value = str(data[idx].get("image", "")).strip()
            return safe_url(value if value else fallback)
        except Exception:
            return safe_url(fallback)

    diemden_data = load_json_list("diemden.json")
    lichtrinh_data = load_json_list("lichtrinh.json")

    hero_image = get_image(diemden_data, 0)
    overview_image = get_image(diemden_data, 1)
    collage_img_1 = get_image(diemden_data, 2)
    collage_img_2 = get_image(diemden_data, 3)
    service_img_1 = get_image(diemden_data, 4)
    service_img_2 = get_image(diemden_data, 5)
    service_img_3 = get_image(diemden_data, 6)
    service_img_4 = get_image(diemden_data, 7)

    total_places = len(diemden_data)
    total_routes = len(lichtrinh_data)
    total_areas = len({str(item.get("area", "")).strip() for item in diemden_data if str(item.get("area", "")).strip()})
    total_categories = len({str(item.get("category", "")).strip() for item in diemden_data if str(item.get("category", "")).strip()})

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <style>
            * {{
                box-sizing: border-box;
            }}

            html, body {{
                margin: 0;
                padding: 0;
                font-family: Inter, Arial, sans-serif;
                background: #f4f1ec;
                color: #243127;
            }}

            .gt-page {{
                width: 100%;
                padding: 28px 18px 52px 18px;
                background: linear-gradient(180deg, #f4f1ec 0%, #f7f4ef 100%);
            }}

            .gt-wrap {{
                max-width: 1360px;
                margin: 0 auto;
            }}

            /* ===== PHẦN 1 ===== */
            .gt-hero {{
                display: grid;
                grid-template-columns: 1.02fr 1.18fr;
                gap: 24px;
                align-items: center;
                margin-bottom: 22px;
            }}

            .gt-left {{
                padding: 18px 8px 18px 6px;
            }}

            .gt-kicker {{
                display: inline-flex;
                align-items: center;
                gap: 10px;
                font-size: 13px;
                font-weight: 700;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                color: #8c7b66;
                margin-bottom: 18px;
            }}

            .gt-kicker::before {{
                content: "";
                width: 26px;
                height: 2px;
                background: #b59e82;
                border-radius: 999px;
            }}

            .gt-title {{
                font-size: 62px;
                line-height: 1.03;
                font-weight: 500;
                color: #4a5a4a;
                margin: 0 0 18px 0;
                font-family: Georgia, "Times New Roman", serif;
            }}

            .gt-sub {{
                font-size: 18px;
                line-height: 1.8;
                color: #68756a;
                margin-bottom: 22px;
                max-width: 560px;
            }}

            .gt-actions {{
                display: flex;
                gap: 14px;
                flex-wrap: wrap;
            }}

            .gt-btn {{
                min-width: 178px;
                height: 48px;
                border-radius: 12px;
                border: 1.5px solid #50624f;
                background: transparent;
                color: #50624f;
                font-size: 15px;
                font-weight: 700;
                cursor: pointer;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
                transition: 0.2s ease;
            }}

            .gt-btn.primary {{
                background: #50624f;
                color: #ffffff;
                box-shadow: 0 10px 22px rgba(80, 98, 79, 0.18);
            }}

            .gt-btn:hover {{
                transform: translateY(-1px);
            }}

            .gt-image {{
                position: relative;
                min-height: 440px;
                border-radius: 0 0 0 120px;
                overflow: hidden;
                background-image: url('{hero_image}');
                background-size: cover;
                background-position: center;
                box-shadow: 0 18px 38px rgba(0,0,0,0.08);
            }}

            .gt-image::before {{
                content: "";
                position: absolute;
                inset: 0;
                background:
                    linear-gradient(to right, rgba(244,241,236,0.92) 0%, rgba(244,241,236,0.60) 18%, rgba(244,241,236,0.10) 38%, rgba(0,0,0,0.08) 100%);
            }}

            .gt-image::after {{
                content: "";
                position: absolute;
                inset: 0;
                background: linear-gradient(180deg, rgba(0,0,0,0.02) 0%, rgba(0,0,0,0.14) 100%);
            }}

            .gt-feature-bar {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 12px;
                background: #f2efea;
                border: 1px solid #e7e0d6;
                border-radius: 18px;
                padding: 14px;
                margin-bottom: 34px;
                box-shadow: 0 10px 24px rgba(35, 49, 39, 0.04);
            }}

            .gt-feature {{
                display: flex;
                gap: 14px;
                align-items: flex-start;
                padding: 10px 10px;
            }}

            .gt-feature-icon {{
                width: 42px;
                height: 42px;
                border-radius: 12px;
                background: #f8f5ef;
                border: 1px solid #e3dacd;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 20px;
                flex-shrink: 0;
                color: #8a765f;
            }}

            .gt-feature-title {{
                font-size: 16px;
                font-weight: 800;
                color: #4b5a4b;
                margin-bottom: 6px;
            }}

            .gt-feature-text {{
                font-size: 13px;
                line-height: 1.65;
                color: #7a8478;
            }}

            .gt-bottom {{
                display: grid;
                grid-template-columns: 0.82fr 1.18fr;
                gap: 26px;
                align-items: center;
                margin-bottom: 54px;
            }}

            .gt-bottom-left {{
                padding: 12px 4px;
            }}

            .gt-bottom-title {{
                font-size: 54px;
                line-height: 1.08;
                font-weight: 500;
                color: #4a5a4a;
                margin: 0 0 16px 0;
                font-family: Georgia, "Times New Roman", serif;
            }}

            .gt-bottom-text {{
                font-size: 16px;
                line-height: 1.9;
                color: #6f7a6e;
                max-width: 500px;
                margin-bottom: 24px;
            }}

            .gt-small-btn {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                min-width: 140px;
                height: 46px;
                border-radius: 12px;
                background: #50624f;
                color: white;
                font-size: 14px;
                font-weight: 800;
                border: none;
                cursor: pointer;
                box-shadow: 0 10px 22px rgba(80, 98, 79, 0.16);
            }}

            .gt-bottom-right {{
                position: relative;
                min-height: 390px;
                border-radius: 18px;
                overflow: hidden;
                background-image: url('{overview_image}');
                background-size: cover;
                background-position: center;
                box-shadow: 0 18px 38px rgba(0,0,0,0.08);
            }}

            .gt-bottom-right::before {{
                content: "";
                position: absolute;
                inset: 0;
                background: linear-gradient(180deg, rgba(255,255,255,0.10) 0%, rgba(0,0,0,0.18) 100%);
            }}

            .gt-stats {{
                position: absolute;
                left: 24px;
                right: 24px;
                bottom: 16px;
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 10px;
                background: rgba(247, 244, 238, 0.97);
                border: 1px solid rgba(227, 218, 205, 0.95);
                border-radius: 18px;
                padding: 18px 12px;
                box-shadow: 0 14px 26px rgba(0,0,0,0.08);
            }}

            .gt-stat {{
                text-align: center;
                padding: 6px 4px;
            }}

            .gt-stat-value {{
                font-size: 34px;
                line-height: 1.1;
                font-weight: 700;
                color: #4d5c4d;
                font-family: Georgia, "Times New Roman", serif;
                margin-bottom: 6px;
            }}

            .gt-stat-label {{
                font-size: 14px;
                font-weight: 700;
                color: #5c675b;
                margin-bottom: 3px;
            }}

            .gt-stat-sub {{
                font-size: 12px;
                line-height: 1.5;
                color: #7b847a;
            }}

            /* ===== PHẦN 2 - GIAO DIỆN BẠN VỪA GỬI ===== */
            .gt-story-section {{
                background: #faf8f4;
                border-radius: 22px;
                padding: 42px 34px 40px 34px;
                margin-bottom: 0;
            }}

            .gt-story-grid {{
                display: grid;
                grid-template-columns: 0.88fr 1.12fr;
                gap: 34px;
                align-items: center;
            }}

            .gt-collage-wrap {{
                position: relative;
                min-height: 320px;
                display: flex;
                align-items: center;
                justify-content: center;
            }}

            .gt-collage-circle {{
                position: absolute;
                width: 240px;
                height: 240px;
                border-radius: 50%;
                background: #ece6dd;
                left: 0;
                top: 34px;
            }}

            .gt-collage-card-1 {{
                position: relative;
                width: 250px;
                height: 160px;
                background-image: url('{collage_img_1}');
                background-size: cover;
                background-position: center;
                box-shadow: 0 18px 34px rgba(0,0,0,0.14);
                z-index: 2;
                margin-left: 34px;
            }}

            .gt-collage-card-2 {{
                position: absolute;
                width: 170px;
                height: 115px;
                background-image: url('{collage_img_2}');
                background-size: cover;
                background-position: center;
                left: 78px;
                bottom: 36px;
                box-shadow: 0 16px 30px rgba(0,0,0,0.14);
                z-index: 3;
            }}

            .gt-badge-float {{
                position: absolute;
                left: 18px;
                top: 124px;
                width: 52px;
                height: 52px;
                border-radius: 50%;
                background: #d8c84b;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #ffffff;
                font-size: 22px;
                font-weight: 900;
                z-index: 4;
                box-shadow: 0 10px 22px rgba(216,200,75,0.30);
            }}

            .gt-story-kicker {{
                font-size: 13px;
                font-weight: 700;
                letter-spacing: 0.16em;
                text-transform: uppercase;
                color: #9b8d7c;
                margin-bottom: 14px;
            }}

            .gt-story-title {{
                font-size: 42px;
                line-height: 1.1;
                font-weight: 500;
                color: #4a5a4a;
                margin: 0 0 16px 0;
                font-family: Georgia, "Times New Roman", serif;
                max-width: 520px;
            }}

            .gt-story-desc {{
                font-size: 15px;
                line-height: 1.9;
                color: #748071;
                max-width: 600px;
                margin-bottom: 22px;
            }}

            .gt-mini-features {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 16px 18px;
                margin-bottom: 22px;
            }}

            .gt-mini-item {{
                display: flex;
                gap: 12px;
                align-items: flex-start;
            }}

            .gt-mini-icon {{
                width: 34px;
                height: 34px;
                border-radius: 10px;
                background: #f2eee8;
                border: 1px solid #e6ddd1;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 17px;
                color: #7e8d6f;
                flex-shrink: 0;
            }}

            .gt-mini-title {{
                font-size: 14px;
                font-weight: 800;
                color: #4e5c4d;
                margin-bottom: 4px;
            }}

            .gt-mini-text {{
                font-size: 12px;
                line-height: 1.65;
                color: #7c857a;
            }}

            .gt-story-btn {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                min-width: 138px;
                height: 42px;
                border-radius: 10px;
                background: #d8c84b;
                color: #2f382d;
                font-size: 14px;
                font-weight: 800;
                border: none;
                cursor: pointer;
                box-shadow: 0 10px 22px rgba(216,200,75,0.22);
            }}

            /* ===== SERVICES ===== */
            .gt-services {{
                background: #ebe6de;
                margin-top: 0;
                padding: 52px 28px 40px 28px;
                border-radius: 0 0 22px 22px;
            }}

            .gt-services-head {{
                text-align: center;
                margin-bottom: 30px;
            }}

            .gt-services-kicker {{
                font-size: 12px;
                font-weight: 700;
                letter-spacing: 0.18em;
                text-transform: uppercase;
                color: #968775;
                margin-bottom: 10px;
            }}

            .gt-services-title {{
                font-size: 34px;
                line-height: 1.15;
                font-weight: 500;
                color: #4c5b4c;
                margin: 0;
                font-family: Georgia, "Times New Roman", serif;
            }}

            .gt-service-grid {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 16px;
            }}

            .gt-service-card {{
                background: #f7f4ee;
                padding: 18px 14px 14px 14px;
                min-height: 290px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                border: 1px solid #e3ddd4;
                box-shadow: 0 8px 18px rgba(0,0,0,0.04);
            }}

            .gt-service-number {{
                font-size: 12px;
                font-weight: 800;
                color: #b0a08f;
                letter-spacing: 0.10em;
                text-transform: uppercase;
                margin-bottom: 14px;
            }}

            .gt-service-name {{
                font-size: 18px;
                line-height: 1.3;
                font-weight: 800;
                color: #4f5d4f;
                margin-bottom: 10px;
                text-transform: uppercase;
            }}

            .gt-service-text {{
                font-size: 13px;
                line-height: 1.75;
                color: #7a8478;
                margin-bottom: 14px;
                min-height: 88px;
            }}

            .gt-service-image {{
                width: 100%;
                height: 95px;
                background-size: cover;
                background-position: center;
                margin-top: auto;
            }}

            @media (max-width: 1100px) {{
                .gt-hero,
                .gt-bottom,
                .gt-story-grid {{
                    grid-template-columns: 1fr;
                }}

                .gt-title {{
                    font-size: 48px;
                }}

                .gt-bottom-title {{
                    font-size: 42px;
                }}

                .gt-feature-bar {{
                    grid-template-columns: repeat(2, 1fr);
                }}

                .gt-service-grid {{
                    grid-template-columns: repeat(2, 1fr);
                }}
            }}

            @media (max-width: 720px) {{
                .gt-page {{
                    padding: 18px 10px 28px 10px;
                }}

                .gt-title {{
                    font-size: 38px;
                }}

                .gt-bottom-title,
                .gt-story-title {{
                    font-size: 34px;
                }}

                .gt-sub,
                .gt-bottom-text,
                .gt-story-desc {{
                    font-size: 15px;
                }}

                .gt-image {{
                    min-height: 300px;
                    border-radius: 0 0 0 60px;
                }}

                .gt-feature-bar,
                .gt-stats,
                .gt-mini-features,
                .gt-service-grid {{
                    grid-template-columns: 1fr;
                }}

                .gt-bottom-right {{
                    min-height: 420px;
                }}

                .gt-story-section {{
                    padding: 28px 16px 28px 16px;
                }}

                .gt-collage-wrap {{
                    min-height: 270px;
                }}

                .gt-collage-circle {{
                    width: 180px;
                    height: 180px;
                    left: 6px;
                    top: 34px;
                }}

                .gt-collage-card-1 {{
                    width: 210px;
                    height: 135px;
                    margin-left: 28px;
                }}

                .gt-collage-card-2 {{
                    width: 138px;
                    height: 92px;
                    left: 76px;
                    bottom: 42px;
                }}

                .gt-badge-float {{
                    width: 44px;
                    height: 44px;
                    left: 10px;
                    top: 112px;
                    font-size: 18px;
                }}

                .gt-services {{
                    padding: 34px 16px 24px 16px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="gt-page">
            <div class="gt-wrap">

                <section class="gt-hero">
                    <div class="gt-left">
                        <div class="gt-kicker">Dự án</div>
                        <h1 class="gt-title">LAO CAI HERITAGE AI</h1>
                        <div class="gt-sub">
                            Nền tảng giới thiệu văn hóa, lịch sử và điểm đến Lào Cai theo hướng hiện đại, trực quan và ứng dụng AI.
                            Dự án giúp người dùng tra cứu thông tin nhanh hơn, hiểu sâu hơn và có trải nghiệm khám phá thông minh hơn.
                        </div>

                        <div class="gt-actions">
                            <button class="gt-btn primary" onclick="window.parent.location.href='?page=diemden'">Khám phá điểm đến</button>
                            <button class="gt-btn" onclick="window.parent.location.href='?page=chatbot'">Xem chatbot AI</button>
                        </div>
                    </div>

                    <div class="gt-image"></div>
                </section>

                <section class="gt-feature-bar">
                    <div class="gt-feature">
                        <div class="gt-feature-icon">🌿</div>
                        <div>
                            <div class="gt-feature-title">Không gian văn hóa</div>
                            <div class="gt-feature-text">
                                Tôn vinh vẻ đẹp di sản, bản sắc địa phương và giá trị truyền thống của Lào Cai.
                            </div>
                        </div>
                    </div>

                    <div class="gt-feature">
                        <div class="gt-feature-icon">📍</div>
                        <div>
                            <div class="gt-feature-title">Dữ liệu địa phương</div>
                            <div class="gt-feature-text">
                                Kết nối thông tin về điểm đến, khu vực, mùa đẹp và nội dung giới thiệu rõ ràng.
                            </div>
                        </div>
                    </div>

                    <div class="gt-feature">
                        <div class="gt-feature-icon">🤖</div>
                        <div>
                            <div class="gt-feature-title">Trợ lý AI thông minh</div>
                            <div class="gt-feature-text">
                                Hỗ trợ hỏi đáp, tư vấn lịch trình và giải đáp nhanh các câu hỏi cơ bản cho du khách.
                            </div>
                        </div>
                    </div>

                    <div class="gt-feature">
                        <div class="gt-feature-icon">🛡️</div>
                        <div>
                            <div class="gt-feature-title">Định hướng bền vững</div>
                            <div class="gt-feature-text">
                                Ứng dụng công nghệ để quảng bá văn hóa địa phương theo hướng hiện đại và lâu dài.
                            </div>
                        </div>
                    </div>
                </section>

                <section class="gt-bottom">
                    <div class="gt-bottom-left">
                        <div class="gt-kicker">Giới thiệu dự án</div>
                        <h2 class="gt-bottom-title">Kiến tạo chuẩn mực khám phá mới</h2>
                        <div class="gt-bottom-text">
                            Lao Cai Heritage AI được xây dựng nhằm hỗ trợ giới thiệu danh lam thắng cảnh, di tích lịch sử và văn hóa
                            địa phương bằng giao diện trực quan, dễ dùng. Dự án hướng đến việc kết hợp dữ liệu số với AI để nâng cao
                            trải nghiệm tra cứu, tham khảo lịch trình và tiếp cận thông tin cho người dùng.
                        </div>

                        <button class="gt-small-btn" onclick="window.parent.location.href='?page=lichtrinh'">
                            Xem lịch trình
                        </button>
                    </div>

                    <div class="gt-bottom-right">
                        <div class="gt-stats">
                            <div class="gt-stat">
                                <div class="gt-stat-value">{total_places}+</div>
                                <div class="gt-stat-label">Điểm đến</div>
                                <div class="gt-stat-sub">Nội dung trong hệ thống</div>
                            </div>

                            <div class="gt-stat">
                                <div class="gt-stat-value">{total_routes}+</div>
                                <div class="gt-stat-label">Lịch trình</div>
                                <div class="gt-stat-sub">Gợi ý tham khảo</div>
                            </div>

                            <div class="gt-stat">
                                <div class="gt-stat-value">{total_areas}+</div>
                                <div class="gt-stat-label">Khu vực</div>
                                <div class="gt-stat-sub">Phân loại dữ liệu</div>
                            </div>

                            <div class="gt-stat">
                                <div class="gt-stat-value">{total_categories}+</div>
                                <div class="gt-stat-label">Loại hình</div>
                                <div class="gt-stat-sub">Trải nghiệm khám phá</div>
                            </div>
                        </div>
                    </div>
                </section>

                <section class="gt-story-section">
                    <div class="gt-story-grid">
                        <div class="gt-collage-wrap">
                            <div class="gt-collage-circle"></div>
                            <div class="gt-badge-float">✦</div>
                            <div class="gt-collage-card-1"></div>
                            <div class="gt-collage-card-2"></div>
                        </div>

                        <div>
                            <div class="gt-story-kicker">Giá trị cốt lõi</div>
                            <h2 class="gt-story-title">Nền tảng hỗ trợ quảng bá văn hóa và du lịch địa phương</h2>
                            <div class="gt-story-desc">
                                Dự án không chỉ dừng ở việc hiển thị thông tin, mà còn hướng tới trải nghiệm tra cứu hiện đại,
                                dễ tiếp cận và gần gũi hơn với học sinh, du khách và người dùng phổ thông. Giao diện được xây dựng
                                theo hướng trực quan, nội dung rõ ràng và có thể phát triển lâu dài.
                            </div>

                            <div class="gt-mini-features">
                                <div class="gt-mini-item">
                                    <div class="gt-mini-icon">🧭</div>
                                    <div>
                                        <div class="gt-mini-title">Định vị nội dung rõ ràng</div>
                                        <div class="gt-mini-text">Phân tách điểm đến, lịch trình và thuyết minh thành từng nhóm dễ tra cứu.</div>
                                    </div>
                                </div>

                                <div class="gt-mini-item">
                                    <div class="gt-mini-icon">📚</div>
                                    <div>
                                        <div class="gt-mini-title">Tăng giá trị học tập</div>
                                        <div class="gt-mini-text">Giúp người dùng tìm hiểu lịch sử, văn hóa và thông tin địa phương thuận tiện hơn.</div>
                                    </div>
                                </div>

                                <div class="gt-mini-item">
                                    <div class="gt-mini-icon">⚙️</div>
                                    <div>
                                        <div class="gt-mini-title">Tích hợp AI thực tế</div>
                                        <div class="gt-mini-text">Chatbot hỗ trợ hỏi đáp cơ bản, gợi ý lịch trình và trả lời theo dữ liệu hệ thống.</div>
                                    </div>
                                </div>

                                <div class="gt-mini-item">
                                    <div class="gt-mini-icon">🚀</div>
                                    <div>
                                        <div class="gt-mini-title">Dễ mở rộng về sau</div>
                                        <div class="gt-mini-text">Có thể tiếp tục bổ sung phản hồi, dữ liệu mới và các tính năng nâng cao sau này.</div>
                                    </div>
                                </div>
                            </div>

                            <button class="gt-story-btn" onclick="window.parent.location.href='?page=chatbot'">
                                Tìm hiểu thêm
                            </button>
                        </div>
                    </div>
                </section>

                <section class="gt-services">
                    <div class="gt-services-head">
                        <div class="gt-services-kicker">Tính năng</div>
                        <h2 class="gt-services-title">Các chức năng nổi bật</h2>
                    </div>

                    <div class="gt-service-grid">
                        <div class="gt-service-card">
                            <div>
                                <div class="gt-service-number">01</div>
                                <div class="gt-service-name">Giới thiệu điểm đến</div>
                                <div class="gt-service-text">
                                    Trình bày thông tin điểm đến bằng giao diện trực quan, dễ đọc và phù hợp với người dùng phổ thông.
                                </div>
                            </div>
                            <div class="gt-service-image" style="background-image:url('{service_img_1}');"></div>
                        </div>

                        <div class="gt-service-card">
                            <div>
                                <div class="gt-service-number">02</div>
                                <div class="gt-service-name">Lịch trình thông minh</div>
                                <div class="gt-service-text">
                                    Gợi ý hành trình tham khảo theo khu vực, loại hình và thông tin chi phí cơ bản trong hệ thống.
                                </div>
                            </div>
                            <div class="gt-service-image" style="background-image:url('{service_img_2}');"></div>
                        </div>

                        <div class="gt-service-card">
                            <div>
                                <div class="gt-service-number">03</div>
                                <div class="gt-service-name">Chatbot AI</div>
                                <div class="gt-service-text">
                                    Hỗ trợ đặt câu hỏi nhanh về địa điểm, mùa đẹp, lịch trình và các thông tin cần tra cứu cơ bản.
                                </div>
                            </div>
                            <div class="gt-service-image" style="background-image:url('{service_img_3}');"></div>
                        </div>

                        <div class="gt-service-card">
                            <div>
                                <div class="gt-service-number">04</div>
                                <div class="gt-service-name">Thuyết minh địa điểm</div>
                                <div class="gt-service-text">
                                    Tăng trải nghiệm khám phá bằng nội dung thuyết minh và phần trình bày sinh động ở trang chi tiết.
                                </div>
                            </div>
                            <div class="gt-service-image" style="background-image:url('{service_img_4}');"></div>
                        </div>
                    </div>
                </section>

            </div>
        </div>
    </body>
    </html>
    """

    components.html(html, height=2300, scrolling=False)