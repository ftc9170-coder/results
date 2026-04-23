import streamlit as st
import pandas as pd

# 1. إعدادات الهوية البصرية للمنصة
st.set_page_config(page_title="منصة نتائج مادة الكيمياء", page_icon="🎓", layout="centered")

# رابط الـ CSV الخاص بك الذي أرسلته
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSs6IHWs1o90rFma8_QnUS-Yoi1gRO8X8pEfK8JcfBtNiI_90R51P0g3D9xIAlpmF3jxuGYK4yTWflN/pub?output=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        # قراءة البيانات مع التأكد من معالجة القيم الفارغة
        return pd.read_csv(SHEET_CSV_URL)
    except Exception as e:
        return None

# 2. تصميم الواجهة الاحترافية (CSS)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTextInput > div > div > input { text-align: center; border: 2px solid #1a73e8; border-radius: 12px; font-size: 22px; }
    .result-card {
        background-color: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border-top: 8px solid #1a73e8;
        direction: rtl;
        text-align: right;
    }
    .grid-container { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 15px; }
    .grid-item { background: #f1f3f4; padding: 10px; border-radius: 8px; text-align: center; border: 1px solid #dee2e6; }
    .final-score { font-size: 24px; color: #1a73e8; font-weight: bold; text-align: center; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. العنوان
st.title("🎓 بوابة استعلام نتائج الطلاب")
st.info("أدخل رقم القيد الخاص بك للاطلاع على درجات الامتحانات.")

# 4. منطقة البحث
student_id = st.text_input("رقم القيد", placeholder="مثلاً: 2026001")

if st.button("استعلام عن النتيجة"):
    if student_id:
        df = load_data()
        
        if df is not None:
            # تحويل رقم القيد لنص للمطابقة الصحيحة
            df['رقم_القيد'] = df['رقم_القيد'].astype(str)
            result = df[df['رقم_القيد'] == student_id.strip()]
            
            if not result.empty:
                row = result.iloc[0]
                st.balloons()
                
                # عرض النتائج
                st.markdown(f"""
                <div class="result-card">
                    <h2 style='text-align: center; color: #333;'>{row['اسم_الطالب']}</h2>
                    <p style='text-align: center; color: #666;'>رقم القيد: {row['رقم_القيد']}</p>
                    <hr>
                    <div class="grid-container">
                        <div class="grid-item"><b>عملي نصفي</b><br>{row['عملي_نصفي']}</div>
                        <div class="grid-item"><b>نظري نصفي</b><br>{row['نظري_نصفي']}</div>
                        <div class="grid-item"><b>النهائي العملي</b><br>{row['النهائي_العملي'] if pd.notnull(row['النهائي_العملي']) else '⏳'}</div>
                        <div class="grid-item"><b>النهائي النظري</b><br>{row['النهائي_النظري'] if pd.notnull(row['النهائي_النظري']) else '⏳'}</div>
                    </div>
                    <div class="final-score">
                        المجموع النهائي: {row['المجموع_النهائي'] if pd.notnull(row['المجموع_النهائي']) else 'قيد الرصد'}
                    </div>
                    <h3 style='text-align: center; color: #28a745;'>التقدير: {row['التقدير'] if pd.notnull(row['التقدير']) else '--'}</h3>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("رقم القيد غير موجود. يرجى التأكد من الرقم أو مراجعة أستاذ المادة.")
        else:
            st.error("عذراً، تعذر الاتصال بملف البيانات حالياً.")
    else:
        st.warning("يرجى إدخال رقم القيد أولاً.")

# 5. أزرار المشاركة والتذييل
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"""
    <div style="text-align:center;">
        <p>📢 شارك المنصة مع زملائك:</p>
        <a href="https://www.facebook.com/sharer/sharer.php?u=https://dr-results.streamlit.app" target="_blank" style="margin:5px; text-decoration:none; padding:10px 20px; background:#3b5998; color:white; border-radius:5px;">فيسبوك</a>
        <a href="https://api.whatsapp.com/send?text=رابط نتائج مادة الكيمياء: https://dr-results.streamlit.app" target="_blank" style="margin:5px; text-decoration:none; padding:10px 20px; background:#25d366; color:white; border-radius:5px;">واتساب</a>
    </div>
    <hr>
    <p style='text-align:center; color:grey; font-size: 12px;'>تم التطوير بواسطة مكتب المحاضر © 2026</p>
""", unsafe_allow_html=True)
