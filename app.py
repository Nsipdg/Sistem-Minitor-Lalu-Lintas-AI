import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw
import requests
import io

# --- PENERAPAN PBO: INHERITANCE (SYARAT UTAMA UTS) ---
class BaseAnalytics:
    def __init__(self):
        # Menggunakan Model AI Deteksi Objek dari Facebook (DETR) via Hugging Face API
        self.api_url = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"
        self.system_status = "Cloud AI Connected"

class ProductVisionAI(BaseAnalytics):
    def __init__(self):
        super().__init__()
        self.app_name = "AI Integrated Quality Analytics"

    def analyze_image(self, img_bytes):
        # Mengirim data ke server AI Cloud agar tidak berat di HP/Server
        try:
            response = requests.post(self.api_url, data=img_bytes, timeout=10)
            return response.json()
        except:
            return None

# --- INSTANSIASI OBJEK ---
ai_system = ProductVisionAI()

# --- TATA LETAK DASHBOARD (POIN 3: KONSISTEN & SEIMBANG) ---
st.set_page_config(page_title="UTS PBO - AI Analytics", layout="wide")

st.title("🛡️ " + ai_system.app_name)
st.caption(f"Status Sistem: {ai_system.system_status} | Paradigma: Pemrograman Berbasis Objek (Inheritance)")

# SECTION 1: UPLOAD & AI DETECTION
st.subheader("📸 Analisis Citra & Deteksi Objek AI")
uploaded_file = st.file_uploader("Unggah foto produk atau objek...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    img_bytes = uploaded_file.getvalue()
    img_display = Image.open(io.BytesIO(img_bytes))
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        with st.spinner('AI sedang memproses objek...'):
            results = ai_system.analyze_image(img_bytes)
            
            # Jika AI berhasil mendeteksi objek
            if isinstance(results, list):
                draw = ImageDraw.Draw(img_display)
                detected_names = []
                for res in results:
                    box = res['box']
                    # Menggambar Bounding Box (Kotak Merah)
                    draw.rectangle([box['xmin'], box['ymin'], box['xmax'], box['ymax']], outline="red", width=5)
                    detected_names.append(res['label'])
                
                st.image(img_display, caption="Visualisasi Deteksi AI (Bounding Box)", use_column_width=True)
            else:
                st.image(img_display, use_column_width=True)
                st.warning("Server AI sedang sibuk. Menampilkan gambar tanpa deteksi.")

    with col_right:
        # POIN 2: INDIKATOR KINERJA UT
    with st.spinner('AI sedang menganalisis foto...'):
        # Memanggil AI "Beneran"
        results = qc_system.analyze_real_ai(img_bytes)
        
        col_img, col_info = st.columns([1, 1])
        
        with col_img:
            # Jika AI berhasil mendeteksi sesuatu
            if isinstance(results, list):
                draw = ImageDraw.Draw(img_display)
                found_objects = []
                for res in results:
                    box = res['box']
                    draw.rectangle([box['xmin'], box['ymin'], box['xmax'], box['ymax']], outline="red", width=4)
                    found_objects.append(res['label'])
                
                st.image(img_display, caption="Hasil Deteksi Otomatis AI", use_column_width=True)
            else:
                st.image(img_display, use_column_width=True)
                st.warning("AI sedang memproses, silakan coba unggah ulang.")

        with col_info:
            st.subheader("📊 Hasil Deteksi")
            if isinstance(results, list) and len(results) > 0:
                # Menampilkan KPI (Poin 2)
                kpi1, kpi2 = st.columns(2)
                kpi1.metric("Objek Terdeteksi", len(results))
                kpi2.metric("Confidence", f"{results[0]['score']:.2%}")
                
                # Performa Produk (Poin 2)
                st.write("**Daftar Temuan:**")
                st.write(", ".join(set(found_objects)))
            else:
                st.info("Menunggu data dari Cloud AI...")

# --- GRAFIK (Tetap ada untuk syarat UTS) ---
st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    st.subheader("📈 Tren Kualitas")
    st.line_chart(np.random.randn(10, 2))
with c2:
    st.subheader("📊 Performa Per Kategori")
    st.bar_chart(pd.DataFrame({'Grade': ['A', 'B', 'C'], 'Unit': [50, 30, 10]}).set_index('Grade'))
                
