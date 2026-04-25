import streamlit as st
import google.generativeai as genai
import pandas as pd
import numpy as np
from PIL import Image
import io
import json

# --- KONSEP PBO: INHERITANCE ---
class GeminiEngine:
    def __init__(self, key):
        genai.configure(api_key=key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

class QualityApp(GeminiEngine):
    def __init__(self, key):
        super().__init__(key)
        self.title = "Gemini AI Quality Analytics"

    def analyze_image(self, img_pil):
        # Prompt agar Gemini memberikan data dalam format JSON untuk grafik
        prompt = """
        Analisis foto produk ini. Berikan jawaban HANYA dalam format JSON mentah seperti ini:
        {
          "produk": "Nama Produk",
          "skor_kualitas": 85,
          "jumlah_unit": 3,
          "status": "Lolos",
          "data_tren": [80, 85, 90, 85, 88]
        }
        Jangan berikan teks tambahan selain JSON.
        """
        response = self.model.generate_content([prompt, img_pil])
        # Membersihkan teks dari markdown jika ada
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_json)

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Vision AI Pro", layout="wide")
API_KEY = "MASUKKAN_API_KEY_GEMINI_DISINI" # <--- Ganti dengan API Key kamu

if API_KEY == "MASUKKAN_API_KEY_GEMINI_DISINI":
    st.error("⚠️ Masukkan API Key Gemini kamu di dalam kode!")
    st.stop()

app = QualityApp(API_KEY)

st.title("♊ " + app.title)
st.caption("Deployment: GitHub + Streamlit + Gemini 1.5 Flash API")

# SECTION 1: UPLOAD & ANALISIS
uploaded_file = st.file_uploader("Unggah foto produk untuk dianalisis...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    
    col_img, col_data = st.columns([1, 1])
    
    with col_img:
        st.image(img, caption="Foto Input", use_column_width=True)
        
    with col_data:
        with st.spinner('Gemini sedang berpikir...'):
            try:
                res = app.analyze_image(img)
                
                # Menampilkan KPI (POIN 2 INSTRUKSI)
                st.subheader("🚀 KPI Indikator (Data AI)")
                k1, k2, k3 = st.columns(3)
                k1.metric("Produk", res['produk'])
                k2.metric("Unit", f"{res['jumlah_unit']} Pcs")
                k3.metric("Quality Score", f"{res['skor_kualitas']}%")
                
                if res['status'] == "Lolos":
                    st.success(f"Status Final: {res['status']}")
                else:
                    st.error(f"Status Final: {res['status']}")
            except Exception as e:
                st.error("Gagal menganalisis. Pastikan foto jelas atau cek API Key.")
                res = None

    # SECTION 2: GRAFIK SINKRON (POIN 2 INSTRUKSI)
    if res:
        st.markdown("---")
        st.subheader("📊 Visualisasi Data Sinkron")
        c1, c2 = st.columns(2)
        
        with c1:
            st.write("**📈 Tren Kualitas Berdasarkan Analisis**")
            # Grafik tren garis dari data JSON Gemini
            st.line_chart(res['data_tren'])
            
        with c2:
            st.write("**📊 Performa Unit Terdeteksi**")
            # Grafik batang performa produk
            p_data = pd.DataFrame({
                'Kategori': ['Lolos QC', 'Reject'],
                'Jumlah': [res['jumlah_unit'], 0 if res['status'] == 'Lolos' else 1]
            })
            st.bar_chart(p_data.set_index('Kategori'))

else:
    st.info("Silakan unggah foto untuk melihat kekuatan analisis Gemini Vision.")

st.caption("PBO Paradigm: Inheritance | Engine: Google Gemini 1.5 Flash")
