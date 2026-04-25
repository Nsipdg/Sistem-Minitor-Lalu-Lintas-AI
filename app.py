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
        genai.configure(api_key=key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

class QualityApp(GeminiEngine):
    def __init__(self, key):
        super().__init__(key)
        self.title = "Gemini AI Quality Analytics"

    def analyze_image(self, img_pil):
        # Prompt diperketat agar Gemini tidak salah format
        prompt = """
        Analisis foto produk ini. Berikan jawaban HANYA dalam format JSON mentah:
        {
          "produk": "Nama Produk",
          "skor_kualitas": 85,
          "jumlah_unit": 3,
          "status": "Lolos",
          "data_tren": [80, 85, 90, 85, 88]
        }
        Jangan berikan teks tambahan atau penjelasan.
        """
        response = self.model.generate_content([prompt, img_pil])
        
        # FUNGSI PEMBERSIH (Anti-Error)
        raw_text = response.text
        # Menghapus blok markdown ```json ... ``` jika ada
        clean_json = re.sub(r'```json|```', '', raw_text).strip()
        return json.loads(clean_json)

# --- KONFIGURASI ---
st.set_page_config(page_title="Vision AI Pro", layout="wide")
API_KEY = "MASUKKAN_API_KEY_KAMU_DISINI" # <--- Ganti dengan API Key kamu

if API_KEY == "MASUKKAN_API_KEY_KAMU_DISINI":
    st.error("⚠️ Masukkan API Key Gemini kamu di dalam kode!")
    st.stop()

app = QualityApp(API_KEY)
st.title("♊ " + app.title)

uploaded_file = st.file_uploader("Unggah foto produk...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    col_img, col_data = st.columns([1, 1])
    
    with col_img:
        st.image(img, caption="Foto Input", use_column_width=True)
        
    with col_data:
        with st.spinner('Gemini sedang menganalisis...'):
            try:
                res = app.analyze_image(img)
                
                st.subheader("🚀 KPI Indikator (Real AI)")
                k1, k2, k3 = st.columns(3)
                k1.metric("Produk", res['produk'])
                k2.metric("Unit", f"{res['jumlah_unit']} Pcs")
                k3.metric("Quality Score", f"{res['skor_kualitas']}%")
                
                if res['status'] == "Lolos":
                    st.success(f"Status Final: {res['status']}")
                else:
                    st.error(f"Status Final: {res['status']}")

                # SECTION GRAFIK (Hanya muncul jika analisis berhasil)
                st.markdown("---")
                c1, c2 = st.columns(2)
                with c1:
                    st.write("**📈 Tren Kualitas**")
                    st.line_chart(res['data_tren'])
                with c2:
                    st.write("**📊 Performa Produk**")
                    p_data = pd.DataFrame({
                        'Kategori': ['Lolos QC', 'Reject'],
                        'Jumlah': [res['jumlah_unit'], 0 if res['status'] == 'Lolos' else 1]
                    })
                    st.bar_chart(p_data.set_index('Kategori'))

            except Exception as e:
                st.error(f"Gagal memproses data AI. Coba klik 'X' pada foto dan unggah ulang.")
                # Tampilkan teks asli dari Gemini untuk debug jika ingin (opsional)
                # st.write(response.text)
else:
    st.info("Silakan unggah foto untuk mengaktifkan Gemini Vision.")

st.caption("PBO Paradigm: Inheritance | Engine: Google Gemini 1.5 Flash")
            
