import streamlit as st
import pandas as pd

# ==========================================
# 1. إعدادات الهوية والتخصيص
# ==========================================
LECTURER_NAME = "د. صابر الفطيسي"
INSTITUTE_NAME = "المعهد العالي للعلوم والتقنية - سوق الخميس امسيحل"
YEAR_SESSION = "2025 - 2026"
LOGO_FILE = "image_166501.jpg" 
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSs6IHWs1o90rFma8_QnUS-Yoi1gRO8X8pEfK8JcfBtNiI_90R51P0g3D9xIAlpmF3jxuGYK4yTWflN/pub?output=csv"

# توزيع الدرجات العظمى الجديد
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
# 2. تصميم الواجهة (CSS المطور للتنسيق)
# ==========================================
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    
    <style>
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, span, div {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl;
        text-align: center;
    }

    .main { background-color: #ffffff; }

    /* تنسيق الحاوية الرئيسية للشعار والعناوين */
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-bottom: 40px;
    }

    /* تنسيق مربع إدخال رقم القيد ليكون غير مقصوص */
    .stTextInput > div > div > input {
        text-align: center; 
        border: 2px solid #003366 !important; 
        border-radius: 12px !important; 
        font-size: 24px !important; 
        font-weight: 700 !important; 
        height: 65px !important; 
        padding: 0 15px !important;
        width: 100%;
    }

    /* بطاقة النتيجة الفخمة */
    .result-card {
        background: #ffffff; 
        padding: 30px; 
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        border: 1px solid #eee;
        margin-top: 20px;
        width: 100%;
    }

    .score-grid { 
        display: grid; 
        grid-template-columns: 1fr 1fr; 
        gap: 15px; 
        margin-top: 25px; 
    }
    
    .score-item {
        background: #f8fafd; 
        padding: 15px; 
        border-radius: 12px; 
        border: 1px solid #e1e8ed;
    }

    .score-title { font-size: 14px; color: #555; margin-bottom: 5px; }
    .score-value { font-size: 22px; color: #003366; font-weight: 900; }

    /* بانر المجموع */
    .final-banner {
        background: #003366;
        color: #ffffff; 
        padding: 20px; 
        border-radius: 15px; 
        margin-top: 25px;
    }
    
    .total-value { font-size: 38px; font-weight: 900; color: #d4af37; }
    .grade-label { font-size: 22px; font-weight: 700; margin-top: 5px; }
    
    /* زر البحث */
    .stButton > button {
        width: 100% !important;
        height: 55px !important; 
        font-size: 20px !important; 
        font-weight: 700 !important; 
        border-radius: 12px !important;
        background-color: #003366 !important;
        color: white !important;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. عرض الشعار والعناوين (توسيط كامل)
# ==========================================
st.markdown('<div class="header-container">', unsafe_allow_html=True)
try:
    # استخدام columns مع الفراغات لضمان التوسيط الحقيقي للشعار
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.image(LOGO_FILE, width=160)
except:
    pass

st.markdown(f"""
    <h2 style="color: #003366; font-size: 24px; margin-top: 15px; font-weight: 900;">{INSTITUTE_NAME}</h2>
    <h3 style="color: #d4af37; font-size: 20px; margin-top: 0; font-weight: 700;">المنصة الرقمية لـ {LECTURER_NAME}</h3>
    <p style="color: #666; font-size: 14px;">نتائج مادة الكيمياء • {YEAR_SESSION}</p>
    </div>
""", unsafe_allow_html=True)

# منطقة الاستعلام
student_id = st.text_input("", placeholder="أدخل رقم القيد هنا للاستعلام", label_visibility="collapsed")

if st.button("استعلام عن النتيجة"):
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
                    <h2 style="color:#333; font-size:28px; font-weight:900; margin-bottom:10px;">{row['اسم_الطالب']}</h2>
                    <p style="color:#888; font-size:14px;">رقم القيد: {row['رقم_القيد']}</p>
                    <div class="score-grid">
                        <div class="score-item">
                            <div class="score-title">عملي نصفي</div>
                            <div class="score-value">{fmt(row['عملي_نصفي'], MAX_SCORES['عملي_نصفي'])}</div>
                        </div>
                        <div class="score-item">
                            <div class="score-title">نظري نصفي</div>
                            <div class="score-value">{fmt(row['نظري_نصفي'], MAX_SCORES['نظري_نصفي'])}</div>
                        </div>
                        <div class="score-item">
                            <div class="score-title">النهائي العملي</div>
                            <div class="score-value">{fmt(row['النهائي_العملي'], MAX_SCORES['النهائي_العملي'])}</div>
                        </div>
                        <div class="score-item">
                            <div class="score-title">النهائي النظري</div>
                            <div class="score-value">{fmt(row['النهائي_النظري'], MAX_SCORES['النهائي_النظري'])}</div>
                        </div>
                    </div>
                    <div class="final-banner">
                        <div style="font-size:14px; opacity:0.8;">المجموع النهائي</div>
                        <div class="total-value">{fmt(row['المجموع_النهائي'], MAX_SCORES['المجموع_النهائي'])}</div>
                        <div class="grade-label">التقدير: {row['التقدير'] if pd.notnull(row['التقدير']) else '--'}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("عذراً، رقم القيد غير مسجل في المنظومة.")
    else:
        st.warning("يرجى كتابة رقم القيد أولاً.")

st.markdown(f"<div style='text-align:center; margin-top:50px; color:#aaa; font-size:12px;'>جميع الحقوق محفوظة © {LECTURER_NAME}</div>", unsafe_allow_html=True)
