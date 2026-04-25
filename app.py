import streamlit as st
import google.generativeai as genai
import pandas as pd
import numpy as np
from PIL import Image
import io
import json
import re

# --- KONSEP PBO: INHERITANCE ---
class GeminiBase:
    def __init__(self, key):
        genai.configure(api_key=key)

class QualityApp(GeminiBase):
    def __init__(self, key):
        super().__init__(key)
        self.title = "AI Vision Quality Control"
        # Memaksa model menggunakan versi stabil
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def analyze(self, img_pil):
        prompt = """
        Analisis foto ini. Berikan jawaban HANYA JSON mentah:
        {"produk": "nama", "skor": 85, "unit": 3, "status": "Lolos", "tren": [80, 85, 90, 88]}
        """
        # Proses pengiriman ke AI
        response = self.model.generate_content([prompt, img_pil])
        # Membersihkan teks agar hanya JSON yang diambil
        clean_text = re.sub(r'```json|```', '', response.text).strip()
        return json.loads(clean_text)

# --- TAMPILAN DASHBOARD ---
st.set_page_config(page_title="Vision AI", layout="wide")
MY_KEY = "AIzaSyB3bQLCvAb2b4tw7Gmsz-N4ZKXwfiFND30" # <--- Tempel API Key dari foto kamu

if MY_KEY == "MASUKKAN_API_KEY_KAMU_DISINI":
    st.warning("Silakan masukkan API Key di dalam kode.")
    st.stop()

app = QualityApp(MY_KEY)
st.title("🛡️ " + app.title)

uploaded_file = st.file_uploader("Pilih foto...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, width=300)
    
    if st.button("Jalankan Analisis AI"):
        with st.spinner("Sedang memproses..."):
            try:
                res = app.analyze(img)
                
                # Menampilkan KPI (Poin 2 Instruksi)
                c1, c2, c3 = st.columns(3)
                c1.metric("Produk", res.get('produk', '-'))
                c2.metric("Jumlah", f"{res.get('unit', 0)} Unit")
                c3.metric("Kualitas", f"{res.get('skor', 0)}%")
                
                # Menampilkan Grafik Tren (Dinamis)
                st.markdown("---")
                st.subheader("📈 Tren Analisis Produk")
                st.line_chart(res.get('tren', []))
                
                st.success(f"Analisis Selesai. Status: {res.get('status')}")
            except Exception as e:
                st.error(f"Gagal: {e}. Coba Reboot App di Streamlit.")

st.caption("PBO Paradigm: Inheritance | Engine: Gemini 1.5 Flash")
