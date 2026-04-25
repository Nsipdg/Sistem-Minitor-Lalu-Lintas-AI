import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw
import requests
import io

# --- PENERAPAN PBO (INHERITANCE) ---
class BaseAnalytics:
    def __init__(self):
        # Menggunakan model deteksi objek dari Facebook (DETR)
        self.api_url = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"
        self.headers = {"Authorization": "Bearer hf_xxxx"} # Bisa dikosongkan untuk model publik tertentu

class QualityAI(BaseAnalytics):
    def __init__(self):
        super().__init__()
        self.system_name = "VisionQC - AI Detector"

    def analyze_real_ai(self, image_bytes):
        # Mengirim foto ke Server AI Hugging Face
        response = requests.post(self.api_url, data=image_bytes)
        return response.json()

# --- INTERFACE UTAMA ---
st.set_page_config(page_title="AI Product QC", layout="wide")
qc_system = QualityAI()

st.title("🛡️ " + qc_system.system_name)

uploaded_file = st.file_uploader("Unggah foto untuk dianalisis AI...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    img_bytes = uploaded_file.getvalue()
    img_display = Image.open(io.BytesIO(img_bytes))
    
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
                
