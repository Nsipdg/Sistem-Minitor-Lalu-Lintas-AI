import streamlit as st
import google.generativeai as genai
import pandas as pd
import numpy as np
from PIL import Image
import io
import json
import re

# --- KONSEP PBO: INHERITANCE ---
class GeminiEngine:
    def __init__(self, key):
        # Perbaikan Konfigurasi API
        genai.configure(api_key=key)
        # Menggunakan jalur model yang lebih stabil
        self.model = genai.GenerativeModel(model_name="gemini-1.5-flash")

class QualityApp(GeminiEngine):
    def __init__(self, key):
        super().__init__(key)
        self.title = "Gemini AI Quality Analytics"

    def analyze_image(self, img_pil):
        prompt = """
        Analisis foto produk ini. Berikan jawaban HANYA dalam format JSON mentah:
        {
          "produk": "Nama Produk",
          "skor_kualitas": 85,
          "jumlah_unit": 3,
          "status": "Lolos",
          "data_tren": [80, 85, 90, 85, 88]
        }
        Jangan berikan teks tambahan.
        """
        # Memanggil generate_content dengan parameter eksplisit
        response = self.model.generate_content([prompt, img_pil])
        
        # Pembersihan JSON
        clean_json = re.sub(r'```json|```', '', response.text).strip()
        return json.loads(clean_json)

# --- KONFIGURASI ---
st.set_page_config(page_title="Vision AI Pro", layout="wide")

# MASUKKAN API KEY KAMU DI SINI
API_KEY = "MASUKKAN_API_KEY_KAMU" 

if API_KEY == "MASUKKAN_API_KEY_KAMU":
    st.error("⚠️ Masukkan API Key Gemini kamu!")
    st.stop()

app = QualityApp(API_KEY)
st.title("♊ " + app.title)

uploaded_file = st.file_uploader("Unggah foto...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    col_img, col_data = st.columns([1, 1])
    
    with col_img:
        st.image(img, caption="Foto Input", use_column_width=True)
        
    with col_data:
        with st.spinner('Gemini sedang menganalisis...'):
            try:
                res = app.analyze_image(img)
                
                st.subheader("🚀 KPI Indikator")
                k1, k2, k3 = st.columns(3)
                k1.metric("Produk", res.get('produk', '-'))
                k2.metric("Unit", f"{res.get('jumlah_unit', 0)} Pcs")
                k3.metric("Skor", f"{res.get('skor_kualitas', 0)}%")
                
                if res.get('status') == "Lolos":
                    st.success("Status: Lolos QC")
                else:
                    st.error("Status: Defect/Reject")

                st.markdown("---")
                st.write("**📈 Tren & Performa**")
                st.line_chart(res.get('data_tren', []))
                
            except Exception as e:
                st.error(f"Error Analisis: {e}")
else:
    st.info("Silakan unggah foto.")
    
