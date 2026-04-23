import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 1. إعدادات الهوية البصرية (تخصيص د. صابر)
# ==========================================
LECTURER_NAME = "د. صابر الفطيسي"
INSTITUTE_NAME = "المعهد العالي للعلوم والتقنية - سوق الخميس امسيحل"
YEAR_SESSION = "العام الدراسي 2025 - 2026"
# رابط شعار المعهد (تم وضعه كرمز تعبيري مؤقتاً، يمكنك استبداله برابط الصورة المرفوعة)
LOGO_URL = "https://raw.githubusercontent.com/ftc9170-coder/repo/master/image_166501.jpg" 

# رابط ملف جوجل شيت الخاص بك
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSs6IHWs1o90rFma8_QnUS-Yoi1gRO8X8pEfK8JcfBtNiI_90R51P0g3D9xIAlpmF3jxuGYK4yTWflN/pub?output=csv"

st.set_page_config(
    page_title=f"منصة {LECTURER_NAME}",
    page_icon="🎓",
    layout="centered"
)

@st.cache_data(ttl=60)
def load_data():
    try:
        return pd.read_csv(SHEET_CSV_URL)
    except:
        return None

# ==========================================
# 2. تصميم الواجهة (CSS)
# ==========================================
st.markdown(f"""
    <style>
    .main {{ background-color: #f4f7f9; }}
    .stTextInput > div > div > input {{
        text-align: center; border: 2px solid #003366; border-radius: 12px; font-size: 20px;
    }}
    .result-card {{
        background: white; padding: 30px; border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border-top: 10px solid #003366; direction: rtl; text-align: right;
    }}
    .institute-header {{
        text-align: center; color: #003366; margin-bottom: 20px;
    }}
    .score-grid {{
        display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 20px;
    }}
    .score-item {{
        background: #f8f9fa; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #eee;
    }}
    .final-banner {{
        background: #003366; color: white; padding: 20px; border-radius: 15px; text-align: center; margin-top: 25px;
    }}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. عرض الشعار والعناوين
# ==========================================
col1, col2, col3 = st.columns([1,2,1])
with col2:
    # عرض الشعار
    st.image("image_166501.jpg", width=150) # تأكد من رفع صورة الشعار بنفس الاسم في GitHub

st.markdown(f"""
    <div class="institute-header">
        <h2 style="margin-bottom:0;">{INSTITUTE_NAME}</h2>
        <h3 style="color: #d4af37; margin-top:5px;">المنصة الرقمية للنتائج</h3>
        <p style="font-size: 18px;"><b>بإشراف: {LECTURER_NAME}</b></p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 4. منطق البحث
# ==========================================
st.markdown("---")
student_id = st.text_input("أدخل رقم القيد للاستعلام عن نتيجتك", placeholder="مثال: 2026100")

if st.button("عرض النتيجة"):
    if student_id:
        df = load_data()
        if df is not None:
            df['رقم_القيد'] = df['رقم_القيد'].astype(str)
            result = df[df['رقم_القيد'] == student_id.strip()]
            
            if not result.empty:
                row = result.iloc[0]
                st.balloons()
                
                st.markdown(f"""
                <div class="result-card">
                    <h2 style="text-align:center;">الطالب: {row['اسم_الطالب']}</h2>
                    <hr>
                    <div class="score-grid">
                        <div class="score-item"><b>عملي نصفي</b><br>{row['عملي_نصفي']}</div>
                        <div class="score-item"><b>نظري نصفي</b><br>{row['نظري_نصفي']}</div>
                        <div class="score-item"><b>النهائي العملي</b><br>{row['النهائي_العملي'] if pd.notnull(row['النهائي_العملي']) else '⏳'}</div>
                        <div class="score-item"><b>النهائي النظري</b><br>{row['النهائي_النظري'] if pd.notnull(row['النهائي_النظري']) else '⏳'}</div>
                    </div>
                    <div class="final-banner">
                        <div style="font-size:14px; opacity:0.8;">المجموع النهائي</div>
                        <div style="font-size:32px; font-weight:bold;">{row['المجموع_النهائي'] if pd.notnull(row['المجموع_النهائي']) else 'قيد الرصد'}</div>
                        <div style="font-size:20px; margin-top:10px; color:#d4af37;">التقدير: {row['التقدير'] if pd.notnull(row['التقدير']) else '--'}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("رقم القيد غير موجود. يرجى التأكد من الرقم والمحاولة مرة أخرى.")
    else:
        st.warning("يرجى إدخال رقم القيد أولاً.")

# ==========================================
# 5. التذييل والمشاركة
# ==========================================
st.markdown(f"""
    <br><br>
    <div style="text-align:center; color:#666; font-size:12px;">
        <p>جميع الحقوق محفوظة © {LECTURER_NAME} - {YEAR_SESSION}</p>
        <p>{INSTITUTE_NAME}</p>
    </div>
""", unsafe_allow_html=True)
