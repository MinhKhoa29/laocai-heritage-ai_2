import streamlit as st
import streamlit.components.v1 as components
from textwrap import dedent

st.set_page_config(
    page_title="LAO CAI HERITAGE AI",
    page_icon="🏔️",
    layout="wide"
)

page = st.query_params.get("page", "home")
place = st.query_params.get("place", "")

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
        margin-top: 50px;
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
    """, height=200, scrolling=False)
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
        pointer-events: none;
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

    .favorite-divider {
        width: 56px;
        height: 2px;
        border-radius: 999px;
        background: rgba(255,255,255,0.95);
        margin: 12px auto 14px auto;
        opacity: 0;
        transform: translateY(10px);
        transition: 0.35s ease;
    }

    .favorite-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 10px 22px;
        background: #1565c0;
        color: white;
        border-radius: 10px;
        text-decoration: none;
        font-size: 15px;
        font-weight: 700;
        opacity: 0;
        transform: translateY(12px);
        transition: 0.35s ease;
        position: relative;
        z-index: 5;
        pointer-events: auto;
        cursor: pointer;
    }

    .favorite-card:hover::before {
        transform: scale(1.08);
    }

    .favorite-card:hover .favorite-overlay {
        background: linear-gradient(to top, rgba(0,0,0,0.72), rgba(0,0,0,0.22));
    }

    .favorite-card:hover .favorite-name {
        transform: translateY(-4px);
    }

    .favorite-card:hover .favorite-divider,
    .favorite-card:hover .favorite-button {
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
                        <div class="favorite-divider"></div>
                        <button type="button" class="favorite-button">Khám phá</button>
                    </div>
                </div>

                <div class="favorite-card card-2">
                    <div class="favorite-overlay"></div>
                    <div class="favorite-content">
                        <div class="favorite-name"></div>
                        <div class="favorite-divider"></div>
                        <button type="button" class="favorite-button">Khám phá</button>
                    </div>
                </div>

                <div class="favorite-card card-3">
                    <div class="favorite-overlay"></div>
                    <div class="favorite-content">
                        <div class="favorite-name"></div>
                        <div class="favorite-divider"></div>
                        <button type="button" class="favorite-button">Khám phá</button>
                    </div>
                </div>

                <div class="favorite-card card-4">
                    <div class="favorite-overlay"></div>
                    <div class="favorite-content">
                        <div class="favorite-name"></div>
                        <div class="favorite-divider"></div>
                        <button type="button" class="favorite-button">Khám phá</button>
                    </div>
                </div>

                <div class="favorite-card card-5">
                    <div class="favorite-overlay"></div>
                    <div class="favorite-content">
                        <div class="favorite-name"></div>
                        <div class="favorite-divider"></div>
                        <button type="button" class="favorite-button">Khám phá</button>
                    </div>
                </div>

                <div class="favorite-card card-6">
                    <div class="favorite-overlay"></div>
                    <div class="favorite-content">
                        <div class="favorite-name"></div>
                        <div class="favorite-divider"></div>
                        <button type="button" class="favorite-button">Khám phá</button>
                    </div>
                </div>

                <div class="favorite-card card-7">
                    <div class="favorite-overlay"></div>
                    <div class="favorite-content">
                        <div class="favorite-name"></div>
                        <div class="favorite-divider"></div>
                        <button type="button" class="favorite-button">Khám phá</button>
                    </div>
                </div>

                <div class="favorite-card card-8">
                    <div class="favorite-overlay"></div>
                    <div class="favorite-content">
                        <div class="favorite-name"></div>
                        <div class="favorite-divider"></div>
                        <button type="button" class="favorite-button">Khám phá</button>
                    </div>
                </div>

                <div class="favorite-card card-9">
                    <div class="favorite-overlay"></div>
                    <div class="favorite-content">
                        <div class="favorite-name"></div>
                        <div class="favorite-divider"></div>
                        <button type="button" class="favorite-button">Khám phá</button>
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
                slug: "quangninh",
                image: "https://images.unsplash.com/photo-1528127269322-539801943592?q=80&w=1200&auto=format&fit=crop"
            },
            {
                name: "Hà Giang",
                slug: "hagiang",
                image: "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?q=80&w=1200&auto=format&fit=crop"
            },
            {
                name: "Lào Cai",
                slug: "laocai",
                image: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?q=80&w=1200&auto=format&fit=crop"
            },
            {
                name: "Ninh Bình",
                slug: "ninhbinh",
                image: "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=1200&auto=format&fit=crop"
            },
            {
                name: "Yên Bái",
                slug: "yenbai",
                image: "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=1200&auto=format&fit=crop"
            },
            {
                name: "Sơn La",
                slug: "sonla",
                image: "https://images.unsplash.com/photo-1501785888041-af3ef285b470?q=80&w=1200&auto=format&fit=crop"
            },
            {
                name: "Cao Bằng",
                slug: "caobang",
                image: "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1200&auto=format&fit=crop"
            },
            {
                name: "Hải Phòng",
                slug: "haiphong",
                image: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=1200&auto=format&fit=crop"
            },
            {
                name: "Hà Nội",
                slug: "hanoi",
                image: "https://images.unsplash.com/photo-1493246507139-91e8fad9978e?q=80&w=1200&auto=format&fit=crop"
            }
        ],

        central: [
            {
                name: "Huế",
                slug: "hue",
                image: "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=1200&auto=format&fit=crop"
            },
            {
                name: "Đà Nẵng",
                slug: "danang",
                image: "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1200&auto=format&fit=crop"
            },
            {
                name: "Quảng Nam",
                slug: "quangnam",
                image: "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?q=80&w=1200&auto=format&fit=crop"
            },
            {
                name: "Nha Trang",
                slug: "nhatrang",
                image: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=1200&auto=format&fit=crop"
            },
            {
                name: "Phú Yên",
                slug: "phuyen",
                image: "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=1200&auto=format&fit=crop"
            },
            {
                name: "Bình Định",
                slug: "binhdinh",
                image: "https://images.unsplash.com/photo-1501785888041-af3ef285b470?q=80&w=1200&auto=format&fit=crop"
            },
            {
                name: "Quảng Bình",
                slug: "quangbinh",
                image: "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?q=80&w=1200&auto=format&fit=crop"
            },
            {
                name: "Thanh Hóa",
                slug: "thanhhoa",
                image: "https://images.unsplash.com/photo-1493246507139-91e8fad9978e?q=80&w=1200&auto=format&fit=crop"
            },
            {
                name: "Nghệ An",
                slug: "nghean",
                image: "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=1200&auto=format&fit=crop"
            }
        ],

        south: [
            {
                name: "TP. Hồ Chí Minh",
                slug: "hcm",
                image: "https://images.unsplash.com/photo-1583417319070-4a69db38a482?q=80&w=1200&auto=format&fit=crop"
            },
            {
                name: "Kiên Giang (Phú Quốc)",
                slug: "kiengiang",
                image: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=1200&auto=format&fit=crop"
            },
            {
                name: "Lâm Đồng (Đà Lạt)",
                slug: "lamdong",
                image: "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=1200&auto=format&fit=crop"
            },
            {
                name: "Bà Rịa - Vũng Tàu",
                slug: "vungtau",
                image: "https://images.unsplash.com/photo-1500375592092-40eb2168fd21?q=80&w=1200&auto=format&fit=crop"
            },
            {
                name: "Cần Thơ",
                slug: "cantho",
                image: "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?q=80&w=1200&auto=format&fit=crop"
            },
            {
                name: "An Giang",
                slug: "angiang",
                image: "https://images.unsplash.com/photo-1501785888041-af3ef285b470?q=80&w=1200&auto=format&fit=crop"
            },
            {
                name: "Tiền Giang",
                slug: "tiengiang",
                image: "https://images.unsplash.com/photo-1519046904884-53103b34b206?q=80&w=1200&auto=format&fit=crop"
            },
            {
                name: "Bến Tre",
                slug: "bentre",
                image: "https://images.unsplash.com/photo-1473116763249-2faaef81ccda?q=80&w=1200&auto=format&fit=crop"
            },
            {
                name: "Đồng Tháp",
                slug: "dongthap",
                image: "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1200&auto=format&fit=crop"
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
                const item = data[index];

                card.style.backgroundImage = `url('${item.image}')`;
                card.querySelector(".favorite-name").textContent = item.name;

                const btn = card.querySelector(".favorite-button");
                btn.onclick = function() {
                    window.top.location.href = `${window.top.location.pathname}?page=detail&place=${item.slug}`;
                };

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
    """), height=980, scrolling=False)

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
    190 Pasteur, Phường Xuân Hòa,<br>
    TP. Hồ Chí Minh, Việt Nam
    </div>

    <div style="margin-top:12px;font-size:16px;color:#1f2937;">
    info@vietravel.com
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
    📞 1800 646 888
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


elif page == "detail":
    province_data = {
        "quangninh": {
            "title": "Quảng Ninh",
            "subtitle": "Di sản thiên nhiên nổi bật miền Bắc",
            "hero": "https://images.unsplash.com/photo-1528127269322-539801943592?q=80&w=1600&auto=format&fit=crop",
            "intro": "Quảng Ninh nổi tiếng với Vịnh Hạ Long, cảnh quan biển đảo hùng vĩ và hệ thống du lịch nghỉ dưỡng phát triển mạnh.",
            "places": ["Vịnh Hạ Long", "Bãi Cháy", "Yên Tử"],
            "foods": ["Chả mực", "Sam biển", "Sá sùng"],
            "activities": ["Du thuyền", "Tắm biển", "Khám phá hang động"]
        },
        "hagiang": {
            "title": "Hà Giang",
            "subtitle": "Cao nguyên đá và mùa hoa vùng biên",
            "hero": "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?q=80&w=1600&auto=format&fit=crop",
            "intro": "Hà Giang hấp dẫn với đèo Mã Pí Lèng, cao nguyên đá Đồng Văn và vẻ đẹp hoang sơ đặc trưng của miền núi phía Bắc.",
            "places": ["Đồng Văn", "Mã Pí Lèng", "Cột cờ Lũng Cú"],
            "foods": ["Thắng cố", "Bánh tam giác mạch", "Cháo ấu tẩu"],
            "activities": ["Phượt đèo", "Check-in cao nguyên đá", "Ngắm mùa hoa"]
        },
        "laocai": {
            "title": "Lào Cai",
            "subtitle": "Bản sắc văn hóa và núi non Tây Bắc",
            "hero": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?q=80&w=1600&auto=format&fit=crop",
            "intro": "Lào Cai nổi bật với Sa Pa, Fansipan, chợ phiên vùng cao và bản sắc văn hóa đa dạng của các dân tộc.",
            "places": ["Sa Pa", "Fansipan", "Bắc Hà"],
            "foods": ["Thắng cố", "Lợn cắp nách", "Cá hồi Sa Pa"],
            "activities": ["Leo núi", "Tham quan bản làng", "Săn mây"]
        },
        "ninhbinh": {
            "title": "Ninh Bình",
            "subtitle": "Non nước hữu tình giữa lòng di sản",
            "hero": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=1600&auto=format&fit=crop",
            "intro": "Ninh Bình là điểm đến nổi bật với Tràng An, Tam Cốc, chùa Bái Đính và cảnh sắc núi đá vôi rất đặc trưng.",
            "places": ["Tràng An", "Tam Cốc", "Bái Đính"],
            "foods": ["Cơm cháy", "Dê núi", "Miến lươn"],
            "activities": ["Đi thuyền", "Tham quan hang động", "Leo núi"]
        },
        "yenbai": {
            "title": "Yên Bái",
            "subtitle": "Ruộng bậc thang và mùa vàng Tây Bắc",
            "hero": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=1600&auto=format&fit=crop",
            "intro": "Yên Bái nổi tiếng với Mù Cang Chải, đèo Khau Phạ và những mùa lúa chín vàng tuyệt đẹp.",
            "places": ["Mù Cang Chải", "Khau Phạ", "Suối Giàng"],
            "foods": ["Cốm Tú Lệ", "Thịt trâu gác bếp", "Xôi ngũ sắc"],
            "activities": ["Check-in ruộng bậc thang", "Trekking", "Dù lượn"]
        },
        "sonla": {
            "title": "Sơn La",
            "subtitle": "Cao nguyên xanh mát và bản làng Tây Bắc",
            "hero": "https://images.unsplash.com/photo-1501785888041-af3ef285b470?q=80&w=1600&auto=format&fit=crop",
            "intro": "Sơn La thu hút với Mộc Châu, đồi chè, rừng thông và khí hậu dễ chịu quanh năm.",
            "places": ["Mộc Châu", "Tà Xùa", "Ngọc Chiến"],
            "foods": ["Bê chao", "Sữa chua nếp cẩm", "Cá suối nướng"],
            "activities": ["Ngắm đồi chè", "Săn mây", "Tham quan bản làng"]
        },
        "caobang": {
            "title": "Cao Bằng",
            "subtitle": "Thác nước kỳ vĩ và non xanh biên giới",
            "hero": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1600&auto=format&fit=crop",
            "intro": "Cao Bằng nổi tiếng với thác Bản Giốc, động Ngườm Ngao và vẻ đẹp xanh mát của núi rừng Đông Bắc.",
            "places": ["Thác Bản Giốc", "Động Ngườm Ngao", "Pác Bó"],
            "foods": ["Bánh cuốn Cao Bằng", "Vịt quay 7 vị", "Hạt dẻ Trùng Khánh"],
            "activities": ["Tham quan thác", "Khám phá hang động", "Du lịch lịch sử"]
        },
        "haiphong": {
            "title": "Hải Phòng",
            "subtitle": "Thành phố cảng sôi động và biển đảo hấp dẫn",
            "hero": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=1600&auto=format&fit=crop",
            "intro": "Hải Phòng có Cát Bà, Đồ Sơn, ẩm thực phong phú và không khí biển đặc trưng của thành phố cảng.",
            "places": ["Cát Bà", "Đồ Sơn", "Nhà hát lớn Hải Phòng"],
            "foods": ["Bánh đa cua", "Nem cua bể", "Bún tôm"],
            "activities": ["Tắm biển", "Du thuyền", "Tham quan đảo"]
        },
        "hanoi": {
            "title": "Hà Nội",
            "subtitle": "Nghìn năm văn hiến giữa nhịp sống hiện đại",
            "hero": "https://images.unsplash.com/photo-1493246507139-91e8fad9978e?q=80&w=1600&auto=format&fit=crop",
            "intro": "Hà Nội là trung tâm văn hóa, lịch sử với Hồ Gươm, phố cổ, Văn Miếu và rất nhiều di sản kiến trúc.",
            "places": ["Hồ Gươm", "Phố cổ", "Văn Miếu"],
            "foods": ["Phở", "Bún chả", "Cốm"],
            "activities": ["Dạo phố cổ", "Tham quan di tích", "Thưởng thức ẩm thực"]
        },
        "hue": {
            "title": "Huế",
            "subtitle": "Cố đô di sản và nét trầm mặc miền Trung",
            "hero": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?q=80&w=1600&auto=format&fit=crop",
            "intro": "Huế nổi bật với Đại Nội, lăng tẩm, sông Hương và nét văn hóa cung đình rất riêng.",
            "places": ["Đại Nội", "Chùa Thiên Mụ", "Lăng Khải Định"],
            "foods": ["Bún bò Huế", "Cơm hến", "Bánh bèo"],
            "activities": ["Tham quan di tích", "Nghe ca Huế", "Du thuyền sông Hương"]
        },
        "danang": {
            "title": "Đà Nẵng",
            "subtitle": "Thành phố biển năng động miền Trung",
            "hero": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1600&auto=format&fit=crop",
            "intro": "Đà Nẵng có bãi biển đẹp, cầu Rồng, Bà Nà Hills và là cửa ngõ du lịch nổi bật miền Trung.",
            "places": ["Bà Nà Hills", "Biển Mỹ Khê", "Cầu Rồng"],
            "foods": ["Mì Quảng", "Bún chả cá", "Bánh tráng cuốn thịt heo"],
            "activities": ["Tắm biển", "Check-in cầu", "Vui chơi giải trí"]
        },
        "quangnam": {
            "title": "Quảng Nam",
            "subtitle": "Phố cổ và miền di sản duyên hải",
            "hero": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?q=80&w=1600&auto=format&fit=crop",
            "intro": "Quảng Nam nổi tiếng với Hội An, Mỹ Sơn, làng nghề truyền thống và các bãi biển đẹp.",
            "places": ["Hội An", "Mỹ Sơn", "Cù Lao Chàm"],
            "foods": ["Cao lầu", "Mì Quảng", "Bánh tổ"],
            "activities": ["Dạo phố cổ", "Thả đèn hoa đăng", "Tham quan di sản"]
        },
        "nhatrang": {
            "title": "Nha Trang",
            "subtitle": "Biển xanh, cát trắng và nghỉ dưỡng",
            "hero": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=1600&auto=format&fit=crop",
            "intro": "Nha Trang hấp dẫn với bãi biển đẹp, đảo du lịch, dịch vụ nghỉ dưỡng và giải trí biển phong phú.",
            "places": ["VinWonders", "Tháp Bà", "Hòn Mun"],
            "foods": ["Bún chả cá", "Nem nướng", "Hải sản"],
            "activities": ["Lặn biển", "Tắm biển", "Du lịch đảo"]
        },
        "phuyen": {
            "title": "Phú Yên",
            "subtitle": "Vùng biển hoang sơ và cảnh quay nổi tiếng",
            "hero": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=1600&auto=format&fit=crop",
            "intro": "Phú Yên được yêu thích với Gành Đá Đĩa, Bãi Xép và vẻ đẹp yên bình của miền biển.",
            "places": ["Gành Đá Đĩa", "Bãi Xép", "Vũng Rô"],
            "foods": ["Mắt cá ngừ đại dương", "Bánh hỏi lòng heo", "Sò huyết Ô Loan"],
            "activities": ["Check-in biển", "Ngắm bình minh", "Khám phá thiên nhiên"]
        },
        "binhdinh": {
            "title": "Bình Định",
            "subtitle": "Biển đẹp và đất võ miền Trung",
            "hero": "https://images.unsplash.com/photo-1501785888041-af3ef285b470?q=80&w=1600&auto=format&fit=crop",
            "intro": "Bình Định nổi bật với Quy Nhơn, Kỳ Co, Eo Gió và truyền thống võ cổ truyền.",
            "places": ["Kỳ Co", "Eo Gió", "Quy Nhơn"],
            "foods": ["Bún chả cá", "Bánh xèo tôm nhảy", "Nem chợ Huyện"],
            "activities": ["Tắm biển", "Check-in eo biển", "Thưởng thức hải sản"]
        },
        "quangbinh": {
            "title": "Quảng Bình",
            "subtitle": "Vương quốc hang động kỳ vĩ",
            "hero": "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?q=80&w=1600&auto=format&fit=crop",
            "intro": "Quảng Bình nổi tiếng với Phong Nha - Kẻ Bàng, hệ thống hang động lớn và thiên nhiên hoang sơ.",
            "places": ["Phong Nha", "Sơn Đoòng", "Biển Nhật Lệ"],
            "foods": ["Cháo canh", "Bánh bột lọc", "Hải sản"],
            "activities": ["Khám phá hang động", "Trekking", "Tắm biển"]
        },
        "thanhhoa": {
            "title": "Thanh Hóa",
            "subtitle": "Biển Sầm Sơn và đất cổ xứ Thanh",
            "hero": "https://images.unsplash.com/photo-1493246507139-91e8fad9978e?q=80&w=1600&auto=format&fit=crop",
            "intro": "Thanh Hóa có biển Sầm Sơn, suối cá thần Cẩm Lương và nhiều điểm di tích lịch sử lâu đời.",
            "places": ["Sầm Sơn", "Pù Luông", "Thành Nhà Hồ"],
            "foods": ["Nem chua", "Bánh răng bừa", "Chả tôm"],
            "activities": ["Tắm biển", "Trekking", "Tham quan di tích"]
        },
        "nghean": {
            "title": "Nghệ An",
            "subtitle": "Biển Cửa Lò và quê hương xứ Nghệ",
            "hero": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=1600&auto=format&fit=crop",
            "intro": "Nghệ An có Cửa Lò, quê Bác, vườn quốc gia Pù Mát và nhiều nét văn hóa đặc sắc.",
            "places": ["Cửa Lò", "Kim Liên", "Pù Mát"],
            "foods": ["Cháo lươn", "Nhút Thanh Chương", "Bánh mướt"],
            "activities": ["Tắm biển", "Du lịch lịch sử", "Khám phá sinh thái"]
        },
        "hcm": {
            "title": "TP. Hồ Chí Minh",
            "subtitle": "Trung tâm sôi động của miền Nam",
            "hero": "https://images.unsplash.com/photo-1583417319070-4a69db38a482?q=80&w=1600&auto=format&fit=crop",
            "intro": "TP. Hồ Chí Minh là trung tâm kinh tế, văn hóa và du lịch với nhiều điểm tham quan, mua sắm và ẩm thực đa dạng.",
            "places": ["Nhà thờ Đức Bà", "Bưu điện Thành phố", "Chợ Bến Thành"],
            "foods": ["Cơm tấm", "Bánh mì", "Hủ tiếu"],
            "activities": ["City tour", "Mua sắm", "Khám phá ẩm thực"]
        },
        "kiengiang": {
            "title": "Kiên Giang - Phú Quốc",
            "subtitle": "Thiên đường biển đảo phía Nam",
            "hero": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=1600&auto=format&fit=crop",
            "intro": "Kiên Giang nổi bật với Phú Quốc, biển trong xanh, resort nghỉ dưỡng và nhiều hoạt động du lịch đảo hấp dẫn.",
            "places": ["Bãi Sao", "Hòn Thơm", "Chợ đêm Phú Quốc"],
            "foods": ["Gỏi cá trích", "Bún quậy", "Nhum biển"],
            "activities": ["Lặn ngắm san hô", "Đi cáp treo", "Tắm biển"]
        },
        "lamdong": {
            "title": "Lâm Đồng - Đà Lạt",
            "subtitle": "Thành phố ngàn hoa thơ mộng",
            "hero": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=1600&auto=format&fit=crop",
            "intro": "Lâm Đồng nổi tiếng với Đà Lạt, khí hậu mát mẻ, rừng thông, hồ nước và các vườn hoa đầy màu sắc.",
            "places": ["Hồ Xuân Hương", "Langbiang", "Thung lũng Tình Yêu"],
            "foods": ["Dâu tây", "Atiso", "Mứt Đà Lạt"],
            "activities": ["Đạp xe", "Săn mây", "Check-in vườn hoa"]
        },
        "vungtau": {
            "title": "Bà Rịa - Vũng Tàu",
            "subtitle": "Biển gần và nghỉ dưỡng cuối tuần",
            "hero": "https://images.unsplash.com/photo-1500375592092-40eb2168fd21?q=80&w=1600&auto=format&fit=crop",
            "intro": "Vũng Tàu là điểm du lịch biển quen thuộc với bãi tắm đẹp, hải sản phong phú và di chuyển thuận tiện.",
            "places": ["Bãi Sau", "Tượng Chúa Kitô", "Mũi Nghinh Phong"],
            "foods": ["Bánh khọt", "Lẩu cá đuối", "Hải sản"],
            "activities": ["Tắm biển", "Ăn hải sản", "Ngắm hoàng hôn"]
        },
        "cantho": {
            "title": "Cần Thơ",
            "subtitle": "Đô thị miền Tây và chợ nổi đặc sắc",
            "hero": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?q=80&w=1600&auto=format&fit=crop",
            "intro": "Cần Thơ nổi tiếng với chợ nổi Cái Răng, bến Ninh Kiều và nét văn hóa sông nước đặc trưng miền Tây.",
            "places": ["Chợ nổi Cái Răng", "Bến Ninh Kiều", "Nhà cổ Bình Thủy"],
            "foods": ["Bánh cống", "Lẩu mắm", "Nem nướng"],
            "activities": ["Đi chợ nổi", "Du thuyền", "Khám phá miệt vườn"]
        },
        "angiang": {
            "title": "An Giang",
            "subtitle": "Miền sông nước và văn hóa tâm linh",
            "hero": "https://images.unsplash.com/photo-1501785888041-af3ef285b470?q=80&w=1600&auto=format&fit=crop",
            "intro": "An Giang có núi Sam, rừng tràm Trà Sư và nhiều điểm hành hương nổi tiếng ở miền Tây.",
            "places": ["Núi Sam", "Rừng tràm Trà Sư", "Châu Đốc"],
            "foods": ["Bún cá", "Tung lò mò", "Mắm Châu Đốc"],
            "activities": ["Du lịch sinh thái", "Hành hương", "Đi xuồng"]
        },
        "tiengiang": {
            "title": "Tiền Giang",
            "subtitle": "Sông nước miệt vườn đậm chất Nam Bộ",
            "hero": "https://images.unsplash.com/photo-1519046904884-53103b34b206?q=80&w=1600&auto=format&fit=crop",
            "intro": "Tiền Giang hấp dẫn với du lịch sông nước, cồn Thới Sơn và những vườn trái cây trĩu quả.",
            "places": ["Cồn Thới Sơn", "Chùa Vĩnh Tràng", "Chợ nổi Cái Bè"],
            "foods": ["Hủ tiếu Mỹ Tho", "Vú sữa Lò Rèn", "Bánh vá"],
            "activities": ["Đi thuyền", "Nghe đờn ca tài tử", "Tham quan miệt vườn"]
        },
        "bentre": {
            "title": "Bến Tre",
            "subtitle": "Xứ dừa thanh bình miền Tây",
            "hero": "https://images.unsplash.com/photo-1473116763249-2faaef81ccda?q=80&w=1600&auto=format&fit=crop",
            "intro": "Bến Tre nổi tiếng với vườn dừa, kênh rạch xanh mát và các sản phẩm đặc trưng từ dừa.",
            "places": ["Cồn Phụng", "Làng nghề kẹo dừa", "Sân chim Vàm Hồ"],
            "foods": ["Kẹo dừa", "Đuông dừa", "Cơm dừa"],
            "activities": ["Đi xuồng", "Tham quan làng nghề", "Du lịch sinh thái"]
        },
        "dongthap": {
            "title": "Đồng Tháp",
            "subtitle": "Mùa sen, làng hoa và đất lành miền Tây",
            "hero": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?q=80&w=1600&auto=format&fit=crop",
            "intro": "Đồng Tháp thu hút với làng hoa Sa Đéc, Vườn quốc gia Tràm Chim và mùa sen đặc trưng miền Tây.",
            "places": ["Làng hoa Sa Đéc", "Tràm Chim", "Khu du lịch Gáo Giồng"],
            "foods": ["Hủ tiếu Sa Đéc", "Cá lóc nướng trui", "Nem Lai Vung"],
            "activities": ["Ngắm sen", "Du lịch sinh thái", "Chụp ảnh làng hoa"]
        }
    }

    data = province_data.get(place)

    if data:
        detail_html = dedent(f"""
<div style="max-width:1250px;margin:0 auto 40px auto;background:#fffdf6;border-radius:24px;overflow:hidden;box-shadow:0 8px 24px rgba(0,0,0,0.08);">
    <div style="
        min-height:430px;
        background-image:linear-gradient(rgba(0,0,0,0.28), rgba(0,0,0,0.22)), url('{data["hero"]}');
        background-size:cover;
        background-position:center;
        display:flex;
        flex-direction:column;
        justify-content:center;
        align-items:center;
        text-align:center;
        color:white;
        padding:40px 20px;
    ">
        <div style="font-size:28px;font-style:italic;">Khám phá</div>
        <div style="font-size:64px;font-weight:900;line-height:1.1;">{data["title"]}</div>
        <div style="font-size:24px;margin-top:10px;">{data["subtitle"]}</div>
    </div>

    <div style="padding:38px 42px;">
        <div style="display:grid;grid-template-columns:1.1fr 1fr 1fr;gap:22px;">
            <div style="background:white;border-radius:20px;padding:22px;box-shadow:0 6px 18px rgba(0,0,0,0.08);">
                <div style="font-size:30px;font-weight:800;color:#0f766e;margin-bottom:12px;">Giới thiệu</div>
                <p style="font-size:18px;line-height:1.8;color:#374151;margin:0;">{data["intro"]}</p>
            </div>

            <div style="background:white;border-radius:20px;padding:22px;box-shadow:0 6px 18px rgba(0,0,0,0.08);">
                <div style="font-size:30px;font-weight:800;color:#0f766e;margin-bottom:12px;">Địa danh nổi bật</div>
                <ul style="margin:0;padding-left:22px;font-size:18px;line-height:1.9;color:#374151;">
                    <li>{data["places"][0]}</li>
                    <li>{data["places"][1]}</li>
                    <li>{data["places"][2]}</li>
                </ul>
            </div>

            <div style="background:white;border-radius:20px;padding:22px;box-shadow:0 6px 18px rgba(0,0,0,0.08);">
                <div style="font-size:30px;font-weight:800;color:#92400e;margin-bottom:12px;">Đặc sản</div>
                <ul style="margin:0;padding-left:22px;font-size:18px;line-height:1.9;color:#374151;">
                    <li>{data["foods"][0]}</li>
                    <li>{data["foods"][1]}</li>
                    <li>{data["foods"][2]}</li>
                </ul>
            </div>
        </div>

        <div style="margin-top:26px;background:white;border-radius:20px;padding:24px;box-shadow:0 6px 18px rgba(0,0,0,0.08);">
            <div style="font-size:32px;font-weight:800;color:#1565c0;text-align:center;margin-bottom:14px;">Hoạt động thú vị</div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:18px;">
                <div style="background:#f8fafc;border-radius:16px;padding:20px;text-align:center;font-size:22px;font-weight:700;color:#1f2937;">{data["activities"][0]}</div>
                <div style="background:#f8fafc;border-radius:16px;padding:20px;text-align:center;font-size:22px;font-weight:700;color:#1f2937;">{data["activities"][1]}</div>
                <div style="background:#f8fafc;border-radius:16px;padding:20px;text-align:center;font-size:22px;font-weight:700;color:#1f2937;">{data["activities"][2]}</div>
            </div>
        </div>

        <div style="margin-top:28px;text-align:center;">
            <a href="?page=home" target="_self" style="display:inline-block;background:#1565c0;color:white;text-decoration:none;padding:13px 26px;border-radius:12px;font-weight:800;font-size:17px;">← Quay lại trang chủ</a>
        </div>
    </div>
</div>
""")
        components.html(detail_html, height=950, scrolling=True)
    else:
        st.markdown("""
        <div style="padding:60px 20px;text-align:center;">
            <div style="font-size:34px;font-weight:800;color:#1565c0;">Chưa có dữ liệu tỉnh này</div>
            <div style="margin-top:16px;">
                <a href="?page=home" target="_self" style="
                    display:inline-block;
                    background:#1565c0;
                    color:white;
                    text-decoration:none;
                    padding:12px 22px;
                    border-radius:10px;
                    font-weight:700;
                ">← Quay lại trang chủ</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
