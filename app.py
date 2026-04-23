import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 1. إعدادات الهوية والتخصيص
# ==========================================
LECTURER_NAME = "د. صابر الفطيسي"
INSTITUTE_NAME = "المعهد العالي للعلوم والتقنية - سوق الخميس امسيحل"
YEAR_SESSION = "العام الدراسي 2025 - 2026"
LOGO_FILE = "image_166501.jpg" 
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSs6IHWs1o90rFma8_QnUS-Yoi1gRO8X8pEfK8JcfBtNiI_90R51P0g3D9xIAlpmF3jxuGYK4yTWflN/pub?output=csv"

# توزيع الدرجات (النهايات العظمى) - يمكنك تعديلها من هنا
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
# 2. تحسين الخطوط والأحجام (CSS المطور)
# ==========================================
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    
    <style>
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, span, div {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl;
    }

    .main { background-color: #f7f9fc; }
    
    /* تكبير خط إدخال رقم القيد */
    .stTextInput > div > div > input {
        text-align: center; border: 3px solid #003366; border-radius: 15px; 
        font-size: 30px !important; font-weight: 900; height: 70px; color: #003366;
    }

    /* بطاقة النتيجة */
    .result-card {
        background: white; padding: 40px; border-radius: 30px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border-right: 15px solid #003366; text-align: right;
    }

    /* تكبير الأرقام داخل المربعات */
    .score-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 25px; }
    
    .score-item {
        background: #f0f4f8; padding: 20px; border-radius: 15px; 
        text-align: center; border: 2px solid #e1e8ed;
    }

    .score-title { font-size: 18px; color: #555; font-weight: bold; margin-bottom: 10px; }
    
    /* تنسيق الدرجة (مثلاً 15/15) */
    .score-value { 
        font-size: 32px !important; 
        color: #003366; 
        font-weight: 900; 
        letter-spacing: 1px;
    }

    /* بانر المجموع النهائي */
    .final-banner {
        background: linear-gradient(135deg, #003366 0%, #004a99 100%);
        color: white; padding: 30px; border-radius: 20px; 
        text-align: center; margin-top: 35px;
    }
    
    .total-value { font-size: 55px !important; font-weight: 900; color: #f6e09e; }
    .grade-label { font-size: 28px; font-weight: 900; color: white; margin-top: 10px; }
    
    .stButton > button {
        height: 60px; font-size: 22px !important; font-weight: bold; border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. الواجهة الرسومية
# ==========================================
col1, col2, col3 = st.columns([1,1.5,1])
with col2:
    try: st.image(LOGO_FILE, width=200)
    except: st.info("يرجى رفع الشعار image_166501.jpg")

st.markdown(f"""
    <div style="text-align:center; color:#003366;">
        <h1 style="font-size: 32px;">{INSTITUTE_NAME}</h1>
        <h2 style="color: #d4af37; font-size: 26px;">المنصة الرقمية للأستاذ {LECTURER_NAME}</h2>
    </div>
""", unsafe_allow_html=True)

student_id = st.text_input("أدخل رقم القيد للاستعلام", placeholder="رقم القيد")

if st.button("🔍 استعلام عن النتيجة"):
    if student_id:
        df = load_data()
        if df is not None:
            df['رقم_القيد'] = df['رقم_القيد'].astype(str).str.strip()
            result = df[df['رقم_القيد'] == student_id.strip()]
            
            if not result.empty:
                row = result.iloc[0]
                st.balloons()
                
                # دالة لتنسيق الدرجة بشكل (درجة/عظمى)
                def fmt(val, max_s):
                    if pd.isnull(val): return "⏳"
                    return f"{int(val)} / {max_s}"

                st.markdown(f"""
                <div class="result-card">
                    <h1 style="text-align:center; color:#333; font-size:40px; font-weight:900;">{row['اسم_الطالب']}</h1>
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
                        <div style="font-size:20px;">المجموع النهائي العام</div>
                        <div class="total-value">{fmt(row['المجموع_النهائي'], MAX_SCORES['المجموع_النهائي'])}</div>
                        <div class="grade-label">التقدير: {row['التقدير'] if pd.notnull(row['التقدير']) else '--'}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("رقم القيد غير موجود.")
    else:
        st.warning("أدخل رقم القيد أولاً.")

st.markdown(f"<div style='text-align:center; margin-top:50px; color:#888;'>جميع الحقوق محفوظة &copy; {LECTURER_NAME}</div>", unsafe_allow_html=True)
