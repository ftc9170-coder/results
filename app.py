import streamlit as st
import pandas as pd

# ==========================================
# 1. الإعدادات الأساسية
# ==========================================
LECTURER_NAME = "د. صابر الفطيسي"
INSTITUTE_NAME = "المعهد العالي للعلوم والتقنية - سوق الخميس امسيحل"
YEAR_SESSION = "2025 - 2026"
LOGO_FILE = "image_166501.jpg" 
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSs6IHWs1o90rFma8_QnUS-Yoi1gRO8X8pEfK8JcfBtNiI_90R51P0g3D9xIAlpmF3jxuGYK4yTWflN/pub?output=csv"

# الدرجات العظمى المطلوبة
MAX_SCORES = {
    "عملي_نصفي": 15,
    "نظري_نصفي": 25,
    "النهائي_العملي": 15,
    "النهائي_النظري": 45,
    "المجموع_النهائي": 100
}

st.set_page_config(page_title=f"منصة {LECTURER_NAME}", page_icon="🎓", layout="centered")

@st.cache_data(ttl=60)
def load_data():
    try: return pd.read_csv(SHEET_CSV_URL)
    except: return None

# ==========================================
# 2. هندسة التنسيق والتوسيط (CSS)
# ==========================================
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    
    <style>
    /* تصفير الهوامش وتوحيد الخط */
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, span, div {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl;
        text-align: center;
    }

    /* توسيط المحتوى بالكامل في منتصف الشاشة */
    .block-container {
        padding-top: 2rem !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
    }

    /* تنسيق الشعار وضمان توسيطه */
    .stImage {
        display: flex !important;
        justify-content: center !important;
        margin-bottom: 10px !important;
    }

    /* تنسيق حقل إدخال رقم القيد */
    .stTextInput {
        width: 100% !important;
        max-width: 450px !important;
        margin: 0 auto !important;
    }
    
    .stTextInput > div > div > input {
        text-align: center !important;
        font-size: 26px !important;
        font-weight: 700 !important;
        height: 65px !important;
        border: 2px solid #003366 !important;
        border-radius: 15px !important;
        background-color: #f9f9f9 !important;
    }

    /* تنسيق زر البحث ليكون تحت الحقل مباشرة ومنتظم */
    .stButton {
        width: 100% !important;
        max-width: 450px !important;
        margin: 15px auto !important;
    }

    .stButton > button {
        width: 100% !important;
        height: 55px !important;
        background-color: #003366 !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        border-radius: 15px !important;
    }

    /* بطاقة النتيجة المنسقة */
    .result-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid #eee;
        width: 100%;
        max-width: 550px;
        margin: 20px auto;
    }

    .score-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
        margin-top: 20px;
    }

    .score-item {
        background: #f4f7fa;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #e1e8ed;
    }

    .score-title { font-size: 14px; color: #666; margin-bottom: 5px; }
    .score-value { font-size: 22px; color: #003366; font-weight: 900; }

    .final-banner {
        background: #003366;
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin-top: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. بناء الواجهة
# ==========================================

# 1. الشعار في المنتصف
try:
    st.image(LOGO_FILE, width=170)
except:
    st.info("يرجى التأكد من رفع صورة الشعار image_166501.jpg")

# 2. العناوين
st.markdown(f"""
    <h1 style="color: #003366; font-size: 26px; margin-bottom: 0;">{INSTITUTE_NAME}</h1>
    <h2 style="color: #d4af37; font-size: 22px; margin-top: 5px; font-weight: 700;">المنصة الرقمية لـ {LECTURER_NAME}</h2>
    <p style="color: #666; font-size: 15px;">نتائج مادة الكيمياء • {YEAR_SESSION}</p>
""", unsafe_allow_html=True)

# 3. حقل البحث والزر
student_id = st.text_input("", placeholder="أدخل رقم القيد هنا...", label_visibility="collapsed")
search_clicked = st.button("استعلام عن النتيجة")

# 4. معالجة النتائج
if search_clicked:
    if student_id:
        df = load_data()
        if df is not None:
            df['رقم_القيد'] = df['رقم_القيد'].astype(str).str.strip()
            result = df[df['رقم_القيد'] == student_id.strip()]
            
            if not result.empty:
                row = result.iloc[0]
                st.balloons()
                
                def fmt(val, max_s):
                    if pd.isnull(val): return "⏳"
                    return f"{int(val)} / {max_s}"

                st.markdown(f"""
                <div class="result-card">
                    <h2 style="color:#333; font-size:30px; font-weight:900; margin-bottom:5px;">{row['اسم_الطالب']}</h2>
                    <p style="color:#888; font-size:14px; margin-bottom:20px;">رقم القيد: {row['رقم_القيد']}</p>
                    <div class="score-grid">
                        <div class="score-item"><div class="score-title">عملي نصفي</div><div class="score-value">{fmt(row['عملي_نصفي'], MAX_SCORES['عملي_نصفي'])}</div></div>
                        <div class="score-item"><div class="score-title">نظري نصفي</div><div class="score-value">{fmt(row['نظري_نصفي'], MAX_SCORES['نظري_نصفي'])}</div></div>
                        <div class="score-item"><div class="score-title">النهائي العملي</div><div class="score-value">{fmt(row['النهائي_العملي'], MAX_SCORES['النهائي_العملي'])}</div></div>
                        <div class="score-item"><div class="score-title">النهائي النظري</div><div class="score-value">{fmt(row['النهائي_النظري'], MAX_SCORES['النهائي_النظري'])}</div></div>
                    </div>
                    <div class="final-banner">
                        <div style="font-size:14px; opacity:0.8;">المجموع النهائي العام</div>
                        <div style="font-size:38px; font-weight:900; color:#d4af37;">{fmt(row['المجموع_النهائي'], MAX_SCORES['المجموع_النهائي'])}</div>
                        <div style="font-size:22px; font-weight:700; margin-top:5px;">التقدير: {row['التقدير'] if pd.notnull(row['التقدير']) else '--'}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("⚠️ رقم القيد غير موجود.")
    else:
        st.warning("⚠️ يرجى إدخال رقم القيد.")

# تذييل الصفحة
st.markdown(f"<div style='margin-top:50px; color:#aaa; font-size:12px;'>جميع الحقوق محفوظة © {LECTURER_NAME}</div>", unsafe_allow_html=True)
