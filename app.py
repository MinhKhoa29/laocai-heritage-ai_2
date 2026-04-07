# git add .
# git commit -m "mô tả thay đổi"
# git push

# xincahp

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

# CSS điểm đến

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

elif page == "diemden":
    destination_cards = [
        {
            "id": "den-thuong",
            "title": "Đền Thượng",
            "location": "TP. Lào Cai",
            "type": "Tâm linh",
            "desc": "Di tích tâm linh tiêu biểu của tỉnh Lào Cai.",
            "price": "Miễn phí"
        },
        {
            "id": "den-bao-ha",
            "title": "Đền Bảo Hà",
            "location": "Bảo Yên",
            "type": "Tâm linh",
            "desc": "Điểm đến văn hóa tâm linh nổi tiếng của Lào Cai.",
            "price": "Miễn phí"
        },
        {
            "id": "fansipan",
            "title": "Fansipan",
            "location": "Sa Pa",
            "type": "Thiên nhiên",
            "desc": "Nóc nhà Đông Dương với cảnh đẹp hùng vĩ.",
            "price": "750.000 đ"
        },
        {
            "id": "catcat",
            "title": "Bản Cát Cát",
            "location": "Sa Pa",
            "type": "Văn hóa",
            "desc": "Bản làng du lịch cộng đồng nổi tiếng.",
            "price": "150.000 đ"
        },
        {
            "id": "oquyho",
            "title": "Ô Quy Hồ",
            "location": "Sa Pa",
            "type": "Check-in",
            "desc": "Một trong tứ đại đỉnh đèo Việt Nam.",
            "price": "Miễn phí"
        },
        {
            "id": "cho-bac-ha",
            "title": "Chợ Bắc Hà",
            "location": "Bắc Hà",
            "type": "Văn hóa",
            "desc": "Chợ vùng cao đậm bản sắc dân tộc.",
            "price": "Miễn phí"
        },
        {
            "id": "nha-tho-da",
            "title": "Nhà thờ đá Sa Pa",
            "location": "Sa Pa",
            "type": "Kiến trúc",
            "desc": "Công trình kiến trúc cổ nổi bật giữa trung tâm Sa Pa.",
            "price": "Miễn phí"
        },
        {
            "id": "ham-rong",
            "title": "Núi Hàm Rồng",
            "location": "Sa Pa",
            "type": "Thiên nhiên",
            "desc": "Khu du lịch ngắm cảnh đẹp nhìn xuống thị trấn Sa Pa.",
            "price": "70.000 đ"
        }
    ]

    cards_html = """
    <html>
    <head>
        <style>
            * {
                box-sizing: border-box;
                font-family: Arial, sans-serif;
            }

            body {
                margin: 0;
                background: transparent;
            }

            .place-page {
                max-width: 1280px;
                margin: 0 auto;
                padding: 20px 24px 40px 24px;
            }

            .place-title {
                text-align: center;
                font-size: 36px;
                font-weight: 800;
                color: #111827;
                margin-bottom: 8px;
            }

            .place-subtitle {
                text-align: center;
                font-size: 17px;
                color: #6b7280;
                margin-bottom: 30px;
            }

            .place-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 24px;
            }

            .place-card {
                background: #ffffff;
                border-radius: 18px;
                box-shadow: 0 10px 24px rgba(0,0,0,0.08);
                padding: 18px;
                min-height: 250px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }

            .place-name {
                font-size: 24px;
                font-weight: 800;
                color: #111827;
                line-height: 1.35;
                min-height: 66px;
                margin-bottom: 10px;
            }

            .place-meta {
                font-size: 15px;
                color: #6b7280;
                line-height: 1.7;
                min-height: 28px;
                margin-bottom: 12px;
            }

            .place-desc {
                font-size: 15px;
                color: #374151;
                line-height: 1.8;
                min-height: 84px;
                margin-bottom: 14px;
            }

            .place-footer {
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 12px;
                margin-top: auto;
            }

            .place-price {
                font-size: 18px;
                font-weight: 800;
                color: #ef3b2d;
            }

            .place-btn {
                text-decoration: none;
                background: #1565c0;
                color: white;
                padding: 9px 14px;
                border-radius: 10px;
                font-size: 14px;
                font-weight: 700;
                display: inline-block;
            }

            .place-btn:hover {
                background: #0f4f9a;
            }

            @media (max-width: 1100px) {
                .place-grid {
                    grid-template-columns: repeat(2, 1fr);
                }
            }

            @media (max-width: 768px) {
                .place-grid {
                    grid-template-columns: 1fr;
                }

                .place-title {
                    font-size: 28px;
                }
            }
        </style>
    </head>
    <body>
        <div class="place-page">
            <div class="place-title">Điểm đến nổi bật</div>
            <div class="place-subtitle">
                Khám phá các di tích và khu du lịch nổi bật của Lào Cai
            </div>

            <div class="place-grid">
    """

    for item in destination_cards:
        cards_html += f"""
                <div class="place-card">
                    <div>
                        <div class="place-name">{item['title']}</div>
                        <div class="place-meta">📍 {item['location']} • {item['type']}</div>
                        <div class="place-desc">{item['desc']}</div>
                    </div>

                    <div class="place-footer">
                        <div class="place-price">{item['price']}</div>
                        <a class="place-btn" href="/?page=chitiet&place={item['id']}" target="_top">
                            Xem chi tiết
                        </a>
                    </div>
                </div>
        """

    cards_html += """
            </div>
        </div>
    </body>
    </html>
    """

    components.html(cards_html, height= 800, scrolling=False)