# streamlit run app.py --server.runOnSave true
# git add .
# git commit -m "mô tả thay đổi"
# git push

import streamlit as st
import streamlit.components.v1 as components
from textwrap import dedent

st.set_page_config(
    page_title="LAO CAI HERITAGE AI",
    page_icon="🏔️",
    layout="wide"
)

page = st.query_params.get("page", "home")

# CSS trang chủ
st.markdown("""
<style>
/* Ẩn menu mặc định streamlit cho giống web thật hơn */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Toàn bộ nền */
.stApp {
    background-color: #f6f6f6;
}

/* Giảm padding mặc định */
.block-container {
    padding-top: 0rem;
    padding-left: 0rem;
    padding-right: 0rem;
    max-width: 100%;
}

/* Topbar */
.topbar {
    background: #eaf4ff;
    height: 42px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 60px;
    font-size: 15px;
    color: #0d2b4d;
    border-bottom: 1px solid #dbe7f3;
}

/* Navbar */
.navbar {
    background: white;
    height: 72px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 60px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    position: sticky;
    top: 0;
    z-index: 999;
    box-sizing: border-box;
}

.logo {
    font-size: 34px;
    font-weight: 800;
    color: #1565c0;
    text-decoration: none;
    white-space: nowrap;
}

.logo span {
    color: #2e7d32;
}

.nav-links {
    display: flex;
    gap: 34px;
    align-items: center;
    flex-wrap: wrap;
}

.nav-links a {
    font-size: 18px;
    font-weight: 600;
    color: #222;
    text-decoration: none;
    position: relative;
    padding: 6px 0;
    transition: color 0.25s ease;
}

.nav-links a:hover {
    color: #1565c0;
}

.nav-links a.active {
    color: #1565c0;
}

.nav-links a.active::after {
    content: "";
    position: absolute;
    left: 0;
    bottom: -6px;
    width: 100%;
    height: 3px;
    border-radius: 999px;
    background: #1565c0;
}

/* Hero */
.hero {
    position: relative;
    height: 520px;
    background-image: linear-gradient(rgba(0,0,0,0.18), rgba(0,0,0,0.18)),
                      url('https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1600&auto=format&fit=crop');
    background-size: cover;
    background-position: center;
    display: flex;
    align-items: center;
    padding: 0 80px;
}

.hero-content {
    color: white;
    max-width: 700px;
}

.hero-title {
    font-size: 54px;
    font-weight: 800;
    line-height: 1.15;
    margin-bottom: 16px;
}

.hero-subtitle {
    font-size: 22px;
    line-height: 1.6;
    opacity: 0.96;
}       

.search-wrapper {
    position: relative;
    margin-top: -78px;
    z-index: 50;
    display: flex;
    justify-content: center;
}

.search-box {
    width: 86%;
    background: #ffffff;
    border-radius: 22px;
    box-shadow: 0 14px 34px rgba(0,0,0,0.16);
    padding: 14px 18px;
    box-sizing: border-box;
    border: 1px solid rgba(0,0,0,0.05);
}

.search-row {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 130px;
    gap: 14px;
    align-items: center;
}

.search-item {
    background: #f8f9fb;
    border: 1px solid #dbe3ee;
    border-radius: 14px;
    padding: 10px 14px;
    min-height: 64px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.search-label {
    font-size: 13px;
    color: #6b7280;
    margin-bottom: 6px;
    font-weight: 500;
}

.search-fake-input {
    background: #ffffff;
    border-radius: 10px;
    min-height: 38px;
    padding: 9px 12px;
    font-size: 16px;
    color: #111827;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-sizing: border-box;
}

.search-placeholder {
    color: #9ca3af;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.search-button {
    min-height: 64px;
    border-radius: 14px;
    background: #1565c0;
    color: white;
    font-size: 18px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 10px 20px rgba(21,101,192,0.22);
}

@media (max-width: 992px) {
    .search-wrapper {
        margin-top: -52px;
    }

    .search-box {
        width: 92%;
    }

    .search-row {
        grid-template-columns: 1fr 1fr;
    }
}

@media (max-width: 640px) {
    .search-wrapper {
        margin-top: -36px;
    }

    .search-box {
        width: 94%;
        padding: 14px;
    }

    .search-row {
        grid-template-columns: 1fr;
    }
}            

.search-float {
    position: relative;
    margin-top: -95px;  
    margin-bottom: -20px;
    z-index: 50;
}         

/* Danh mục nhanh */
.section {
    padding: 46px 70px 10px 70px;
}

.quick-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 24px;
    margin-top: 20px;
}

.quick-card {
    background: white;
    border-radius: 20px;
    padding: 26px 16px;
    text-align: center;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
    transition: 0.2s;
}

.quick-card:hover {
    transform: translateY(-4px);
}

.quick-icon {
    font-size: 34px;
    margin-bottom: 10px;
}

.quick-title {
    font-size: 18px;
    font-weight: 700;
    color: #1f2937;
}

/* Tiêu đề section */
.section-title {
    font-size: 34px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 8px;
}

.section-subtitle {
    font-size: 18px;
    color: #6b7280;
}

/* Card địa điểm */
.place-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 26px;
    margin-top: 28px;
    margin-bottom: 60px;
}

.place-card {
    background: white;
    border-radius: 22px;
    overflow: hidden;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
}

.place-image {
    height: 220px;
    background-size: cover;
    background-position: center;
}

.place-body {
    padding: 18px;
}

.place-name {
    font-size: 22px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 10px;
}

.place-desc {
    color: #4b5563;
    line-height: 1.6;
    font-size: 16px;
}

/* Footer */
.footer {
    background: #dfeefc;
    padding: 40px 70px;
    margin-top: 30px;
}

.footer-title {
    font-size: 24px;
    font-weight: 800;
    margin-bottom: 14px;
    color: #0d2b4d;
}

.footer-text {
    font-size: 17px;
    color: #334155;
    line-height: 1.8;
}
</style>
""", unsafe_allow_html=True)

# Topbar
topbar_html = dedent("""
<div class="topbar">
    <div>📞 0346 538 917 — Trợ lý du lịch Lào Cai</div>
    <div>🌏 Văn hóa • Lịch sử • Danh lam thắng cảnh</div>
</div>
""")
st.markdown(topbar_html, unsafe_allow_html=True)

# Topbar
navbar_html = dedent(f"""
<div class="navbar">
    <a class="logo" href="?page=home" target="_self">Lao Cai <span>Heritage AI</span></a>
    <div class="nav-links">
        <a href="?page=home" target="_self" class="{'active' if page == 'home' else ''}">Trang chủ</a>
        <a href="?page=diemden" target="_self" class="{'active' if page in ['diemden', 'diemden_detail'] else ''}">Điểm đến</a>
        <a href="?page=ai" target="_self" class="{'active' if page == 'ai' else ''}">Trợ lý AI</a>
        <a href="?page=lichtrinh" target="_self" class="{'active' if page == 'lichtrinh' else ''}">Lịch trình</a>
        <a href="?page=lienhe" target="_self" class="{'active' if page == 'lienhe' else ''}">Liên hệ</a>
    </div>
</div>
""")
st.markdown(navbar_html, unsafe_allow_html=True)

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

    # Search box nổi
    st.markdown('<div class="search-float">', unsafe_allow_html=True)
    components.html("""
    <style>
    .search-wrapper {
        position: relative;
        margin-top: 30px;
        z-index: 10;
        display: flex;
        justify-content: center;
        padding: 0 0 10px 0;
    }

    .search-box {
        width: 82%;
        background: white;
        border-radius: 22px;
        box-shadow: 0 12px 28px rgba(0,0,0,0.14);
        padding: 22px 26px;
        box-sizing: border-box;
    }

    .search-row {
        display: grid;
        grid-template-columns: 2fr 1fr 1fr 140px;
        gap: 16px;
        align-items: stretch;
    }

    .search-item {
        background: #f8f9fb;
        border-radius: 14px;
        padding: 12px 16px;
        border: 1px solid #e2e7ef;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-sizing: border-box;
    }

    .search-label {
        font-size: 13px;
        color: #6b7280;
        margin-bottom: 6px;
        font-weight: 500;
    }

    .search-input,
    .search-select {
        width: 100%;
        border: none;
        outline: none;
        background: white;
        font-size: 16px;
        font-weight: 500;
        color: #111827;
        padding: 8px 10px;
        border-radius: 8px;
        box-sizing: border-box;
    }

    .search-input::placeholder {
        color: #9ca3af;
    }

    .search-input:focus,
    .search-select:focus {
        outline: 1px solid #1565c0;
    }

    .search-button {
        background: #1565c0;
        color: white;
        border-radius: 14px;
        font-size: 18px;
        font-weight: 700;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        min-height: 100%;
        transition: 0.25s ease;
    }

    .search-button:hover {
        background: #0f4f9a;
    }

    @media (max-width: 992px) {
        .search-row {
            grid-template-columns: 1fr 1fr;
        }

        .search-button {
            min-height: 56px;
        }
    }

    @media (max-width: 640px) {
        .search-box {
            width: 92%;
            padding: 18px;
        }

        .search-row {
            grid-template-columns: 1fr;
        }
    }
    </style>

    <div class="search-wrapper">
        <div class="search-box">
            <div class="search-row">

                <div class="search-item">
                    <div class="search-label">Bạn muốn khám phá gì?</div>
                    <input class="search-input" type="text" placeholder="Đền Thượng, Fansipan, Đền Bảo Hà..." />
                </div>

                <div class="search-item">
                    <div class="search-label">Loại hình</div>
                    <select class="search-select">
                        <option>Tâm linh</option>
                        <option>Check-in</option>
                        <option>Sinh thái</option>
                        <option>Văn hóa</option>
                    </select>
                </div>

                <div class="search-item">
                    <div class="search-label">Thời gian</div>
                    <select class="search-select">
                        <option>1 ngày</option>
                        <option>2 ngày</option>
                        <option>3 ngày</option>
                    </select>
                </div>

                <div class="search-button">Tìm kiếm</div>

            </div>
        </div>
    </div>
    """, height=170, scrolling=False)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Khám phá nhanh
    components.html("""
    <style>
    body {
        margin: 0;
        font-family: Arial, sans-serif;
    }

    .product-section {
        padding: 30px 0 20px 0;
        width: 100%;
        box-sizing: border-box;
        overflow: hidden;
    }

    .product-container {
        width: 100%;
        max-width: 1280px;
        margin: 0 auto;
        padding: 0 24px;
        box-sizing: border-box;
    }

    .product-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 24px;
        margin-bottom: 28px;
    }

    .product-header-left {
        flex: 1;
        min-width: 0;
    }

    .product-title {
        font-size: 28px;
        font-weight: 800;
        color: #1565c0;
        text-transform: uppercase;
        line-height: 1.3;
        margin-bottom: 8px;
    }

    .product-line {
        width: 145px;
        height: 4px;
        background: #1565c0;
        border-radius: 999px;
        margin-bottom: 18px;
    }

    .product-desc {
        max-width: 760px;
        font-size: 18px;
        line-height: 1.8;
        color: #1f2937;
    }

    .arrow-box {
        display: flex;
        gap: 14px;
        align-items: center;
        flex-shrink: 0;
        margin-top: 10px;
    }

    .arrow-btn {
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
    }

    .arrow-btn:hover {
        transform: translateY(-2px);
        color: #1565c0;
        box-shadow: 0 10px 22px rgba(0,0,0,0.14);
    }

    .arrow-btn:disabled {
        opacity: 0.45;
        cursor: not-allowed;
        transform: none;
    }

    /* khung ngoài */
    .carousel-wrap {
        width: 100%;
        overflow: hidden;
        position: relative;
        padding-right: 90px; /* chừa chỗ để lộ card sau */
        box-sizing: border-box;
    }

    /* thanh trượt */
    .carousel-track {
        display: flex;
        gap: 18px;
        transition: transform 0.6s ease;
        will-change: transform;
    }

    /* mỗi card */
    .product-card {
        position: relative;
        flex: 0 0 calc((100% - 36px) / 3); /* 3 card chính */
        height: 300px;
        border-radius: 22px;
        overflow: hidden;
        background-size: cover;
        background-position: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    }

    .product-card::after {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(to top, rgba(0,0,0,0.62), rgba(0,0,0,0.08));
    }

    .product-text {
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
    }

    @media (max-width: 992px) {
        .product-header {
            flex-direction: column;
            align-items: flex-start;
        }

        .carousel-wrap {
            padding-right: 40px;
        }

        .product-card {
            flex: 0 0 calc((100% - 18px) / 2);
            height: 270px;
        }
    }

    @media (max-width: 768px) {
        .product-container {
            padding: 0 16px;
        }

        .product-title {
            font-size: 24px;
        }

        .product-desc {
            font-size: 16px;
            line-height: 1.7;
        }

        .carousel-wrap {
            padding-right: 0;
        }

        .product-card {
            flex: 0 0 100%;
            height: 250px;
        }

        .arrow-btn {
            width: 46px;
            height: 46px;
            font-size: 22px;
        }
    }
    </style>

    <div class="product-section">
        <div class="product-container">
            <div class="product-header">
                <div class="product-header-left">
                    <div class="product-title">Khám phá sản phẩm Vietravel</div>
                    <div class="product-line"></div>
                    <div class="product-desc">
                        Hãy tận hưởng trải nghiệm du lịch chuyên nghiệp, mang lại cho bạn những khoảnh khắc tuyệt vời
                        và nâng tầm cuộc sống. Chúng tôi cam kết mang đến những chuyến đi đáng nhớ, giúp bạn khám phá
                        thế giới theo cách hoàn hảo nhất.
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
        {
            image: "https://images.unsplash.com/photo-1499856871958-5b9627545d1a?q=80&w=1200&auto=format&fit=crop",
            text: "Kỳ nghỉ mùa xuân châu Âu cùng gia đình"
        },
        {
            image: "https://images.unsplash.com/photo-1522383225653-ed111181a951?q=80&w=1200&auto=format&fit=crop",
            text: "Hòa cùng sắc hoa anh đào khắp thế giới"
        },
        {
            image: "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?q=80&w=1200&auto=format&fit=crop",
            text: "Tour lễ 30/4 giá tốt cho gia đình"
        },
        {
            image: "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1200&auto=format&fit=crop",
            text: "Tự hào nét Việt - ưu đãi kích cầu du lịch nội địa"
        },
        {
            image: "https://images.unsplash.com/photo-1506929562872-bb421503ef21?q=80&w=1200&auto=format&fit=crop",
            text: "Tour mới - hành trình độc đáo"
        }
    ];

    const track = document.getElementById("carouselTrack");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");

    let currentIndex = 0;

    function buildCards() {
        track.innerHTML = "";
        productData.forEach(item => {
            const card = document.createElement("div");
            card.className = "product-card";
            card.style.backgroundImage = `url('${item.image}')`;
            card.innerHTML = `<div class="product-text">${item.text}</div>`;
            track.appendChild(card);
        });
    }

    function getVisibleCount() {
        if (window.innerWidth <= 768) return 1;
        if (window.innerWidth <= 992) return 2;
        return 3;
    }

    function updateCarousel() {
        const cards = track.querySelectorAll(".product-card");
        if (!cards.length) return;

        const gap = 18;
        const cardWidth = cards[0].offsetWidth + gap;
        track.style.transform = `translateX(-${currentIndex * cardWidth}px)`;

        prevBtn.disabled = currentIndex === 0;
        nextBtn.disabled = currentIndex >= productData.length - getVisibleCount();
    }

    prevBtn.addEventListener("click", () => {
        if (currentIndex > 0) {
            currentIndex--;
            updateCarousel();
        }
    });

    nextBtn.addEventListener("click", () => {
        if (currentIndex < productData.length - getVisibleCount()) {
            currentIndex++;
            updateCarousel();
        }
    });

    window.addEventListener("resize", updateCarousel);

    buildCards();
    setTimeout(updateCarousel, 100);
    </script>
    """, height=540)
                    
    # Điểm đến yêu thích
    components.html(dedent("""
    <style>
    body {
        margin: 0;
        font-family: Arial, sans-serif;
    }

    .favorite-section {
        width: 100%;
        padding: 24px 0;
        box-sizing: border-box;
    }

    .favorite-container {
        max-width: 1350px;
        margin: 0 auto;
        padding: 0 18px;
        box-sizing: border-box;
    }

    .favorite-title {
        text-align: center;
        font-size: 34px;
        font-weight: 900;
        color: #1565c0;
        text-transform: uppercase;
        margin-bottom: 8px;
        line-height: 1.3;
    }

    .favorite-line {
        width: 150px;
        height: 4px;
        background: #1565c0;
        border-radius: 999px;
        margin: 0 auto 18px auto;
    }

    .favorite-desc {
        text-align: center;
        max-width: 820px;
        margin: 0 auto 24px auto;
        font-size: 18px;
        line-height: 1.8;
        color: #374151;
    }

    .favorite-tabs {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 36px;
        margin-bottom: 28px;
    }

    .favorite-tab {
        position: relative;
        font-size: 17px;
        font-weight: 700;
        color: #374151;
        padding-bottom: 8px;
        cursor: pointer;
        transition: 0.25s ease;
    }

    .favorite-tab:hover {
        color: #1565c0;
    }

    .favorite-tab.active {
        color: #1565c0;
    }

    .favorite-tab.active::after {
        content: "";
        position: absolute;
        left: 0;
        bottom: 0;
        width: 100%;
        height: 3px;
        border-radius: 999px;
        background: #1565c0;
    }

    .favorite-grid {
        display: grid;
        grid-template-columns: 1.35fr 1.05fr 1.05fr 1.05fr;
        grid-template-rows: 180px 180px 220px;
        gap: 10px;
    }

    /* CARD */
    .favorite-card {
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
    }

    .favorite-card.fade-out {
        opacity: 0;
        transform: translateY(8px);
    }

    .favorite-card::before {
        content: "";
        position: absolute;
        inset: 0;
        background-image: inherit;
        background-size: cover;
        background-position: center;
        transform: scale(1);
        transition: transform 0.5s ease;
        z-index: 0;
    }

    .favorite-overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(to top, rgba(0,0,0,0.55), rgba(0,0,0,0.12));
        transition: 0.35s ease;
        z-index: 1;
    }

    .favorite-content {
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
    }

    .favorite-name {
        margin: 0;
        font-size: 18px;
        font-weight: 800;
        text-transform: uppercase;
        line-height: 1.3;
        transition: 0.35s ease;
    }

    .favorite-content {
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
    }

    .favorite-name {
        margin: 0;
        font-size: 18px;
        font-weight: 800;
        text-transform: uppercase;
        line-height: 1.3;
        transition: 0.35s ease;
    }

    .favorite-info {
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
    }

.favorite-card:hover::before {
    transform: scale(1.08);
}

.favorite-card:hover .favorite-overlay {
    background: linear-gradient(to top, rgba(0,0,0,0.78), rgba(0,0,0,0.28));
}

.favorite-card:hover .favorite-name {
    transform: translateY(-8px);
}

.favorite-card:hover .favorite-info {
    opacity: 1;
    transform: translateY(0);
}

    /* vị trí từng card */
    .card-1 {
        grid-column: 1 / 2;
        grid-row: 1 / 3;
    }

    .card-2 {
        grid-column: 2 / 3;
        grid-row: 1 / 2;
    }

    .card-3 {
        grid-column: 3 / 5;
        grid-row: 1 / 2;
    }

    .card-4 {
        grid-column: 2 / 3;
        grid-row: 2 / 3;
    }

    .card-5 {
        grid-column: 3 / 4;
        grid-row: 2 / 3;
    }

    .card-6 {
        grid-column: 4 / 5;
        grid-row: 2 / 4;
    }

    .card-7 {
        grid-column: 1 / 2;
        grid-row: 3 / 4;
    }

    .card-8 {
        grid-column: 2 / 3;
        grid-row: 3 / 4;
    }

    .card-9 {
        grid-column: 3 / 4;
        grid-row: 3 / 4;
    }

    @media (max-width: 1100px) {
        .favorite-grid {
            grid-template-columns: 1fr 1fr 1fr;
            grid-template-rows: 220px 220px 220px;
        }

        .card-1 { grid-column: 1 / 2; grid-row: 1 / 3; }
        .card-2 { grid-column: 2 / 3; grid-row: 1 / 2; }
        .card-3 { grid-column: 3 / 4; grid-row: 1 / 2; }
        .card-4 { grid-column: 2 / 3; grid-row: 2 / 3; }
        .card-5 { grid-column: 3 / 4; grid-row: 2 / 3; }
        .card-6 { grid-column: 1 / 2; grid-row: 3 / 4; }
        .card-7 { grid-column: 2 / 3; grid-row: 3 / 4; }
        .card-8 { grid-column: 3 / 4; grid-row: 3 / 4; }
        .card-9 { display: none; }
    }

    @media (max-width: 768px) {
        .favorite-container {
            padding: 0 14px;
        }

        .favorite-title {
            font-size: 26px;
        }

        .favorite-desc {
            font-size: 15px;
            line-height: 1.7;
        }

        .favorite-tabs {
            gap: 18px;
        }

        .favorite-tab {
            font-size: 15px;
        }

        .favorite-grid {
            grid-template-columns: 1fr;
            grid-template-rows: none;
        }

        .favorite-card,
        .card-1, .card-2, .card-3, .card-4, .card-5, .card-6, .card-7, .card-8, .card-9 {
            grid-column: auto;
            grid-row: auto;
            min-height: 250px;
        }

        .card-9 {
            display: block;
        }
    }
    </style>

    <div class="favorite-section">
        <div class="favorite-container">

            <div class="favorite-title">Điểm đến yêu thích</div>
            <div class="favorite-line"></div>

            <div class="favorite-desc">
                Chọn một khu vực nổi bật để khám phá danh lam thắng cảnh,
                văn hóa đặc trưng và những hành trình hấp dẫn trên khắp Việt Nam.
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
    const destinationData = {
        north: [
            {
                name: "Quảng Ninh",
                image: "https://images.unsplash.com/photo-1528127269322-539801943592?q=80&w=1200&auto=format&fit=crop",
                info: "Nổi tiếng với Vịnh Hạ Long, di sản thiên nhiên thế giới với cảnh biển đảo tuyệt đẹp."
            },
            {
                name: "Hà Giang",
                image: "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?q=80&w=1200&auto=format&fit=crop",
                info: "Vùng cao nguyên đá hùng vĩ, nổi bật với đèo Mã Pí Lèng, cột cờ Lũng Cú và mùa hoa tam giác mạch."
            },
            {
                name: "Lào Cai",
                image: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?q=80&w=1200&auto=format&fit=crop",
                info: "Cửa ngõ Tây Bắc, nổi tiếng với Sa Pa, Fansipan, ruộng bậc thang và bản sắc văn hóa dân tộc đặc sắc."
            },
            {
                name: "Ninh Bình",
                image: "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=1200&auto=format&fit=crop",
                info: "Nổi bật với Tràng An, Tam Cốc, Hang Múa và quần thể danh thắng non nước hữu tình."
            },
            {
                name: "Yên Bái",
                image: "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=1200&auto=format&fit=crop",
                info: "Được biết đến với Mù Cang Chải, ruộng bậc thang vàng óng và vẻ đẹp núi rừng Tây Bắc."
            },
            {
                name: "Sơn La",
                image: "https://images.unsplash.com/photo-1501785888041-af3ef285b470?q=80&w=1200&auto=format&fit=crop",
                info: "Có Mộc Châu thơ mộng, đồi chè xanh mướt, mùa hoa mận và khí hậu mát mẻ quanh năm."
            },
            {
                name: "Cao Bằng",
                image: "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1200&auto=format&fit=crop",
                info: "Nổi tiếng với thác Bản Giốc, động Ngườm Ngao và cảnh sắc núi non biên giới hùng vĩ."
            },
            {
                name: "Hải Phòng",
                image: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=1200&auto=format&fit=crop",
                info: "Thành phố cảng sôi động, nổi bật với Cát Bà, Đồ Sơn và nhiều món hải sản hấp dẫn."
            },
            {
                name: "Hà Nội",
                image: "https://images.unsplash.com/photo-1493246507139-91e8fad9978e?q=80&w=1200&auto=format&fit=crop",
                info: "Thủ đô nghìn năm văn hiến với Hồ Gươm, phố cổ, Văn Miếu và nhiều giá trị lịch sử lâu đời."
            }
        ],

        central: [
            {
                name: "Huế",
                image: "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=1200&auto=format&fit=crop",
                info: "Cố đô nổi tiếng với Đại Nội, lăng tẩm triều Nguyễn, chùa Thiên Mụ và nét văn hóa trầm mặc."
            },
            {
                name: "Đà Nẵng",
                image: "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1200&auto=format&fit=crop",
                info: "Thành phố biển hiện đại với Bà Nà Hills, cầu Rồng, biển Mỹ Khê và nhiều điểm check-in hấp dẫn."
            },
            {
                name: "Quảng Nam",
                image: "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?q=80&w=1200&auto=format&fit=crop",
                info: "Nổi bật với phố cổ Hội An, thánh địa Mỹ Sơn và những làng nghề truyền thống đậm bản sắc."
            },
            {
                name: "Nha Trang",
                image: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=1200&auto=format&fit=crop",
                info: "Thiên đường biển xanh với bãi cát đẹp, đảo hấp dẫn, hải sản phong phú và nhiều hoạt động nghỉ dưỡng."
            },
            {
                name: "Phú Yên",
                image: "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=1200&auto=format&fit=crop",
                info: "Gây ấn tượng với Gành Đá Đĩa, Bãi Xép, biển trời hoang sơ và khung cảnh yên bình."
            },
            {
                name: "Bình Định",
                image: "https://images.unsplash.com/photo-1501785888041-af3ef285b470?q=80&w=1200&auto=format&fit=crop",
                info: "Nổi tiếng với Quy Nhơn, Eo Gió, Kỳ Co và sự kết hợp giữa biển đẹp với văn hóa võ cổ truyền."
            },
            {
                name: "Quảng Bình",
                image: "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?q=80&w=1200&auto=format&fit=crop",
                info: "Là quê hương của Phong Nha - Kẻ Bàng, hệ thống hang động kỳ vĩ và thiên nhiên hoang sơ."
            },
            {
                name: "Thanh Hóa",
                image: "https://images.unsplash.com/photo-1493246507139-91e8fad9978e?q=80&w=1200&auto=format&fit=crop",
                info: "Sở hữu biển Sầm Sơn, suối cá Cẩm Lương, thành nhà Hồ và nhiều dấu ấn lịch sử đặc sắc."
            },
            {
                name: "Nghệ An",
                image: "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=1200&auto=format&fit=crop",
                info: "Vùng đất giàu truyền thống với quê Bác, biển Cửa Lò, vườn quốc gia Pù Mát và nhiều giá trị văn hóa."
            }
        ],

        south: [
            {
                name: "TP. Hồ Chí Minh",
                image: "https://images.unsplash.com/photo-1583417319070-4a69db38a482?q=80&w=1200&auto=format&fit=crop",
                info: "Trung tâm kinh tế sôi động với chợ Bến Thành, nhà thờ Đức Bà, phố đi bộ và nhịp sống hiện đại."
            },
            {
                name: "Kiên Giang (Phú Quốc)",
                image: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=1200&auto=format&fit=crop",
                info: "Thiên đường biển đảo với bãi biển trong xanh, hoàng hôn đẹp, làng chài và khu nghỉ dưỡng nổi tiếng."
            },
            {
                name: "Lâm Đồng (Đà Lạt)",
                image: "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=1200&auto=format&fit=crop",
                info: "Thành phố ngàn hoa với khí hậu mát mẻ, hồ Xuân Hương, đồi thông và nhiều điểm săn mây thơ mộng."
            },
            {
                name: "Bà Rịa - Vũng Tàu",
                image: "https://images.unsplash.com/photo-1500375592092-40eb2168fd21?q=80&w=1200&auto=format&fit=crop",
                info: "Điểm đến biển gần gũi với bãi Sau, tượng Chúa Kitô, hải sản ngon và không khí nghỉ dưỡng cuối tuần."
            },
            {
                name: "Cần Thơ",
                image: "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?q=80&w=1200&auto=format&fit=crop",
                info: "Thủ phủ miền Tây nổi tiếng với chợ nổi Cái Răng, bến Ninh Kiều và nét văn hóa sông nước đặc trưng."
            },
            {
                name: "An Giang",
                image: "https://images.unsplash.com/photo-1501785888041-af3ef285b470?q=80&w=1200&auto=format&fit=crop",
                info: "Nổi bật với rừng tràm Trà Sư, núi Cấm, miếu Bà Chúa Xứ và cảnh sắc miền biên giới đặc biệt."
            },
            {
                name: "Tiền Giang",
                image: "https://images.unsplash.com/photo-1519046904884-53103b34b206?q=80&w=1200&auto=format&fit=crop",
                info: "Hấp dẫn với chợ nổi, cù lao Thới Sơn, miệt vườn trái cây và những trải nghiệm sông nước dân dã."
            },
            {
                name: "Bến Tre",
                image: "https://images.unsplash.com/photo-1473116763249-2faaef81ccda?q=80&w=1200&auto=format&fit=crop",
                info: "Xứ dừa nổi tiếng với kênh rạch xanh mát, làng nghề truyền thống và nhịp sống miệt vườn yên bình."
            },
            {
                name: "Đồng Tháp",
                image: "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1200&auto=format&fit=crop",
                info: "Nổi bật với Đồng Tháp Mười, làng hoa Sa Đéc, khu du lịch sinh thái và vẻ đẹp miền Tây mộc mạc."
            }
        ]
    };

    const tabs = document.querySelectorAll(".favorite-tab");
    const cards = document.querySelectorAll(".favorite-card");

    function renderRegion(regionKey) {
        const data = destinationData[regionKey];

        cards.forEach(card => card.classList.add("fade-out"));

        setTimeout(() => {
            cards.forEach((card, index) => {
                card.style.backgroundImage = `url('${data[index].image}')`;
                card.querySelector(".favorite-name").textContent = data[index].name;
                card.querySelector(".favorite-info").textContent = data[index].info;
                card.classList.remove("fade-out");
            });
        }, 220);
    }

    tabs.forEach(tab => {
        tab.addEventListener("click", () => {
            tabs.forEach(item => item.classList.remove("active"));
            tab.classList.add("active");
            renderRegion(tab.dataset.region);
        });
    });

    renderRegion("north");
    </script>
    """), height=900, scrolling=False)

    # Footer
    st.markdown(dedent("""
    <div style="
    background:#dceaf7;
    padding:45px 80px;
    margin-top:50px;
    ">
    <div style="
    display:grid;
    grid-template-columns: 1.2fr 1fr 1fr 1fr;
    gap:40px;
    align-items:start;
    ">

    <div>
    <div style="font-size:26px;font-weight:800;margin-bottom:18px;color:#111827;">
    Liên hệ
    </div>

    <div style="line-height:1.8;font-size:16px;color:#1f2937;">
    Thôn...., xã Khánh Yên,<br>
    tỉnh Lào Cai, Việt Nam
    </div>

    <div style="margin-top:12px;font-size:16px;color:#1f2937;">
    khoagaming999@gmail.com
    </div>

    <div style="margin-top:18px;font-size:22px;">
    📷 📘 💬 🎵 💬
    </div>

    <div style="
    margin-top:18px;
    background:#e41e10;
    color:white;
    padding:12px 18px;
    border-radius:10px;
    display:inline-block;
    font-weight:700;
    font-size:16px;
    ">
    📞 0346 538 197
    </div>

    <div style="margin-top:10px;font-size:15px;color:#1f2937;">
    Tổng đài miễn phí 24/7
    </div>
    </div>

    <div>
    <div style="font-size:22px;font-weight:700;margin-bottom:14px;color:#111827;">
    Thông tin
    </div>
    <div style="line-height:2;color:#1f2937;">
    <div>Khảo sát visa</div>
    <div>Tin tức</div>
    <div>Sitemap</div>
    <div>Trợ giúp</div>
    </div>
    </div>

    <div>
    <div style="font-size:22px;font-weight:700;margin-bottom:14px;color:#111827;">
    Dịch vụ
    </div>
    <div style="line-height:2;color:#1f2937;">
    <div>Tour</div>
    <div>Khách sạn</div>
    <div>Vé máy bay</div>
    <div>Combo du lịch</div>
    </div>
    </div>

    <div>
    <div style="font-size:22px;font-weight:700;margin-bottom:14px;color:#111827;">
    Chấp nhận thanh toán
    </div>

    <div style="
    display:flex;
    flex-wrap:wrap;
    gap:12px;
    font-size:18px;
    font-weight:700;
    color:#334155;
    ">
    <div style="background:white;padding:10px 14px;border-radius:10px;">VISA</div>
    <div style="background:white;padding:10px 14px;border-radius:10px;">Mastercard</div>
    <div style="background:white;padding:10px 14px;border-radius:10px;">VNPAY</div>
    <div style="background:white;padding:10px 14px;border-radius:10px;">JCB</div>
    <div style="background:white;padding:10px 14px;border-radius:10px;">ShopeePay</div>
    <div style="background:white;padding:10px 14px;border-radius:10px;">MSB</div>
    <div style="background:white;padding:10px 14px;border-radius:10px;">123Pay</div>
    <div style="background:white;padding:10px 14px;border-radius:10px;">MoMo</div>
    </div>
    </div>

    </div>
    </div>
    """), unsafe_allow_html=True)

elif page == "lichtrinh":
    import json
    import math
    import re
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
        overflow:hidden;
        background:linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
        border:1px solid #e5edf6;
        border-radius:26px;
        padding:24px 22px 22px 22px;
        min-height:408px;
        display:flex;
        flex-direction:column;
        box-shadow:0 18px 38px rgba(15,23,42,0.08);
    }

    .lt-card::before{
        content:"";
        position:absolute;
        top:0;
        left:0;
        right:0;
        height:5px;
        background:linear-gradient(90deg, #1565c0 0%, #2b7fd3 52%, #43b0f1 100%);
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
        background:#f8fafc;
        border:1px solid #edf2f7;
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
        letter-spacing:0em;
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
        word-break: break-word;
        overflow-wrap: anywhere;
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
            padding: 0;
        }

        .lt-grid{
            grid-template-columns: 1fr;
            gap:18px;
        }

        .lt-card{
            min-height:auto;
            padding:22px 18px 20px 18px;
            border-radius:22px;
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
            grid-template-columns: 1fr;
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

            cards_html += f"""
            <div class="lt-card">
                <div class="lt-card-top">
                    <div class="lt-route">{safe_text(item.get('from'))} → {safe_text(item.get('to'))}</div>
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
            """
        cards_html += '</div>'
        rows = math.ceil(result_count / 3) if result_count else 1
        height = max(500, rows * 580)
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

    cards_html += '</div>'
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

    st.markdown("""
    <style>
        .dd-hero-section{
        position: relative;
        height: 420px;
        background:
            linear-gradient(180deg, rgba(7, 19, 37, 0.08) 0%, rgba(7, 19, 37, 0.18) 100%),
            url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=1600&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <section class="dd-hero-section"></section>
    """, unsafe_allow_html=True)

    filtered_data = list(diemden_data)
    result_count = len(filtered_data)

    st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

    components.html("""
    <style>
    body{
        margin:0;
        background:transparent;
        font-family: Inter, Arial, sans-serif;
    }

    .dd-benefit-wrap{
        max-width: 1320px;
        margin: 26px auto 8px auto;
        padding: 0 6px;
        box-sizing: border-box;
        text-align: center;
    }

    .dd-benefit-title{
        font-size: 30px;
        font-weight: 900;
        color: #111827;
        text-transform: uppercase;
        margin-bottom: 8px;
        line-height: 1.3;
    }

    .dd-benefit-line{
        width: 86px;
        height: 4px;
        background: #f59e0b;
        border-radius: 999px;
        margin: 0 auto 16px auto;
    }

    .dd-benefit-desc{
        max-width: 760px;
        margin: 0 auto 28px auto;
        font-size: 16px;
        line-height: 1.8;
        color: #4b5563;
    }

    .dd-benefit-grid{
        display:grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap:20px;
    }

    .dd-benefit-card{
        background:#ffffff;
        border:1px solid #e5edf6;
        border-radius:24px;
        padding:26px 20px;
        box-shadow:0 12px 28px rgba(15,23,42,0.06);
    }

    .dd-benefit-icon{
        width:72px;
        height:72px;
        margin:0 auto 16px auto;
        border-radius:50%;
        background:linear-gradient(135deg, #38bdf8 0%, #0ea5e9 100%);
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:30px;
        color:#ffffff;
        box-shadow:0 12px 24px rgba(14,165,233,0.22);
    }

    .dd-benefit-name{
        font-size:18px;
        font-weight:800;
        color:#111827;
        margin-bottom:8px;
    }

    .dd-benefit-text{
        font-size:14px;
        line-height:1.75;
        color:#6b7280;
    }

    @media (max-width: 980px){
        .dd-benefit-grid{
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }

    @media (max-width: 640px){
        .dd-benefit-wrap{
            padding: 0 2px;
        }

        .dd-benefit-title{
            font-size:24px;
        }

        .dd-benefit-grid{
            grid-template-columns: 1fr;
        }
    }
    </style>

    <div class="dd-benefit-wrap">
        <div class="dd-benefit-title">Vì sao nên khám phá?</div>
        <div class="dd-benefit-line"></div>
        <div class="dd-benefit-desc">
            Từ cảnh đẹp thiên nhiên, bản làng nguyên sơ đến chợ phiên và di tích lịch sử,
            Lào Cai mang đến trải nghiệm đa dạng và đậm bản sắc vùng cao.
        </div>

        <div class="dd-benefit-grid">
            <div class="dd-benefit-card">
                <div class="dd-benefit-icon">🏞️</div>
                <div class="dd-benefit-name">Cảnh đẹp nổi bật</div>
                <div class="dd-benefit-text">Săn mây, đèo cao, ruộng bậc thang và nhiều điểm check-in giàu cảm xúc.</div>
            </div>

            <div class="dd-benefit-card">
                <div class="dd-benefit-icon">🏡</div>
                <div class="dd-benefit-name">Bản sắc bản địa</div>
                <div class="dd-benefit-text">Khám phá đời sống, nghề thủ công và nhịp sống yên bình của đồng bào vùng cao.</div>
            </div>

            <div class="dd-benefit-card">
                <div class="dd-benefit-icon">🏯</div>
                <div class="dd-benefit-name">Di tích - văn hóa</div>
                <div class="dd-benefit-text">Nhà thờ cổ, dinh thự, chợ phiên và những không gian lưu giữ giá trị lịch sử.</div>
            </div>

            <div class="dd-benefit-card">
                <div class="dd-benefit-icon">🥾</div>
                <div class="dd-benefit-name">Trải nghiệm đa dạng</div>
                <div class="dd-benefit-text">Trekking, nghỉ dưỡng, săn ảnh, khám phá ẩm thực và hòa mình vào thiên nhiên.</div>
            </div>
        </div>
    </div>
    """, height=430, scrolling=False)

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
                    Tìm thấy <strong>{result_count}</strong> điểm đến phù hợp với bộ lọc hiện tại.
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
        cards_height = max(360, rows * 375)
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
    import json
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
        fallback = "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1600&auto=format&fit=crop"
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
            unique_images = [fallback]

        while len(unique_images) < 6:
            unique_images.append(unique_images[-1])

        return [safe_url(x, fallback) for x in unique_images[:6]]

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

    page_height = 3200 + max(0, len(full_desc_raw) // 500) * 160

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
        }
    </style>

    <div class="ddt-page">
        <section class="ddt-hero">
            <div class="ddt-hero-content">
                <h1 class="ddt-hero-title ddt-script">$name</h1>
                <div class="ddt-hero-subtitle">$hero_subtitle</div>
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
                             
        <section class="ddt-section" id="quan-the-di-tich-cuoi">
            <div class="ddt-wrap">
                <div class="ddt-two-col">
                    <div class="ddt-mosaic-left">
                        <div class="img-a" style="background-image:url('$standout_image_1');"></div>
                        <div class="img-b" style="background-image:url('$standout_image_2');"></div>
                        <div class="img-c" style="background-image:url('$standout_image_3');"></div>
                        <div class="img-d" style="background-image:url('$standout_image_4');"></div>
                    </div>

                    <div>
                        <div class="ddt-section-kicker">Tham quan</div>
                        <h2 class="ddt-section-title ddt-script">Quần thể di tích</h2>

                        <div class="ddt-text">$standout_text</div>
                        <div class="ddt-text">$visit_text</div>
                    </div>
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
        best_time=best_time
    )

    components.html(html_output, height=page_height, scrolling=False)