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

# Navbar
navbar_html = dedent(f"""
<div class="navbar">
    <a class="logo" href="?page=home" target="_self">Lao Cai <span>Heritage AI</span></a>
    <div class="nav-links">
        <a href="?page=home" target="_self" class="{'active' if page == 'home' else ''}">Trang chủ</a>
        <a href="?page=diemden" target="_self" class="{'active' if page == 'diemden' else ''}">Điểm đến</a>
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
        margin: 16px auto 60px auto;
        padding: 0 4px;
        box-sizing: border-box;
        font-family: Inter, Arial, sans-serif;
    ">
        <div style="
            position: relative;
            border-radius: 26px;
            overflow: hidden;
            min-height: 240px;
            background-image:
                linear-gradient(rgba(15,23,42,0.72), rgba(15,23,42,0.72)),
                url('https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1600&auto=format&fit=crop');
            background-size: cover;
            background-position: center;
            box-shadow: 0 18px 38px rgba(15,23,42,0.12);
            border: 1px solid rgba(255,255,255,0.12);
            padding: 28px 28px 24px 28px;
            box-sizing: border-box;
        ">
            <div style="
                position:absolute;
                top:0;
                left:0;
                right:0;
                height:5px;
                background:linear-gradient(90deg, #f59e0b 0%, #fbbf24 100%);
            "></div>

            <div style="
                font-size: 24px;
                font-weight: 900;
                color: #ffffff;
                margin-bottom: 16px;
                position: relative;
                z-index: 2;
            ">
                Lưu ý trước khi đặt lịch trình
            </div>

            <div style="
                font-size: 15px;
                line-height: 1.95;
                color: rgba(255,255,255,0.95);
                position: relative;
                z-index: 2;
                max-width: 980px;
            ">
                • Giá hiển thị chỉ mang tính tham khảo tại thời điểm tra cứu.<br>
                • Lịch trình có thể thay đổi tùy điều kiện thời tiết và vận hành thực tế.<br>
                • Du khách nên xác nhận lại dịch vụ lưu trú, phương tiện và vé tham quan trước khi khởi hành.<br>
                • Nên chuẩn bị giấy tờ cá nhân và vật dụng cần thiết cho chuyến đi.<br>
                • Với mùa cao điểm, nên đặt sớm để đảm bảo chỗ và mức giá tốt hơn.
            </div>
        </div>
    </div>
    """, height=250, scrolling=False)