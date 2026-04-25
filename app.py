import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw
import requests
import io

# --- KONSEP PBO (INHERITANCE) ---
class BaseSystem:
    def __init__(self):
        self.api_url = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"
        self.status = "System Online"

class QualityApp(BaseSystem):
    def __init__(self):
        super().__init__()
        self.title = "AI Integrated Quality Analytics"

    def run_ai(self, img_bytes):
        try:
            # Mengirim data ke Cloud AI
            resp = requests.post(self.api_url, data=img_bytes, timeout=10)
            return resp.json()
        except:
            return None

# --- INISIALISASI ---
app = QualityApp()

# --- UI DASHBOARD ---
st.set_page_config(page_title="UTS PBO Analytics", layout="wide")
st.title("🛡️ " + app.title)
st.caption(f"Status: {app.status} | Paradigma: PBO Inheritance")

# BAGIAN 1: UPLOAD FOTO & AI
st.subheader("📸 Analisis Citra Produk")
uploaded_file = st.file_uploader("Pilih foto produk...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    img_data = uploaded_file.getvalue()
    display_img = Image.open(io.BytesIO(img_data))
    
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        with st.spinner('Menghubungi Cloud AI...'):
            results = app.run_ai(img_data)
            
            if isinstance(results, list):
                draw = ImageDraw.Draw(display_img)
                for res in results:
                    b = res['box']
                    draw.rectangle([b['xmin'], b['ymin'], b['xmax'], b['ymax']], outline="red", width=5)
                st.image(display_img, caption="Hasil Deteksi AI", use_column_width=True)
            else:
                st.image(display_img, use_column_width=True)
                st.info("AI sedang melakukan pemanasan (cold start), coba unggah ulang.")

    with col_b:
        st.write("### 🚀 KPI Indikator")
        obj_count = len(results) if isinstance(results, list) else 0
        conf = results[0]['score'] if obj_count > 0 else 0
        
        st.metric("Objek Terdeteksi", f"{obj_count} Unit")
        st.metric("Confidence", f"{conf:.1%}")

# BAGIAN 2: GRAFIK TREN & PERFORMA
st.markdown("---")
c1, c2 = st.columns(2)

with c1:
    st.subheader("📈 Tren Kualitas (7 Hari)")
    t_data = pd.DataFrame(np.random.randn(7, 1), columns=['Akurasi'])
    st.line_chart(t_data)

with c2:
    st.subheader("📊 Performa per Kategori")
    p_data = pd.DataFrame({'Grade': ['A', 'B', 'Defect'], 'Unit': [50, 20, 5]})
    st.bar_chart(p_data.set_index('Grade'))

st.caption("UTS Pemrograman Berbasis Objek - Arsitektur Cloud AI")
              
