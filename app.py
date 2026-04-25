import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw
import requests
import io

# --- KONSEP PBO (INHERITANCE) - MEMENUHI SYARAT UTS ---
class BaseAI:
    def __init__(self):
        # Menggunakan Model Cloud AI yang Handal dari Facebook (DETR)
        self.api_url = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"
        # Gunakan API Key Publik (Limited) atau kosongi. Ini sering berhasil tanpa key.
        self.headers = {} 

class QualityApp(BaseAI):
    def __init__(self):
        super().__init__()
        self.title = "Analisis Citra Produk & Quality Control"

    def detect_real_ai(self, img_bytes):
        # Mengirim foto ke server Cloud AI untuk diproses
        try:
            # timeout dinaikkan jadi 20 detik agar server AI tidak timeout saat bangun
            response = requests.post(self.api_url, data=img_bytes, timeout=20)
            return response.json()
        except:
            return None

# --- INISIALISASI OBJEK ---
app = QualityApp()

# --- INTERFACE UTAMA (Sangat Interaktif & Seimbang) ---
st.set_page_config(page_title="VisionQC AI Pro", layout="wide", page_icon="📷")
st.title("🛡️ " + app.title)
st.caption("Paradigma: PBO Inheritance | Deployment: GitHub + Streamlit + Cloud AI API")

# BAGIAN 1: INPUT FOTO
st.subheader("📸 Analisis Citra QC (Unggah Foto)")
uploaded_file = st.file_uploader("Pilih foto produk (JPG/PNG)...", type=["jpg", "png", "jpeg"])

# LOGIKA UTAMA: JIKA ADA FOTO DIUNGGAH
if uploaded_file is not None:
    img_data = uploaded_file.getvalue()
    display_img = Image.open(io.BytesIO(img_data))
    
    # Tampilan Tata Letak Kiri (Gambar) dan Kanan (KPI)
    col_img, col_kpi = st.columns([2, 1])
    
    with st.spinner('Menghubungi Cloud AI (Mungkin butuh waktu jika ' 'sedang Cold Start)...'):
        results = app.detect_real_ai(img_data)
        
        with col_img:
            # Mengecek apakah hasil AI valid (Berhasil Deteksi)
            if isinstance(results, list) and len(results) > 0:
                draw = ImageDraw.Draw(display_img)
                found_labels = []
                for res in results:
                    b = res['box']
                    # Menggambar kotak deteksi (Bounding Box)
                    draw.rectangle([b['xmin'], b['ymin'], b['xmax'], b['ymax']], outline="red", width=5)
                    found_labels.append(res['label'])
                
                # Tampilkan Gambar Hasil Deteksi
                st.image(display_img, caption=f"Hasil Deteksi Otomatis AI (Total: {len(results)} Objek)", use_column_width=True)
            else:
                st.image(display_img, use_column_width=True)
                st.info("⚠️ AI tidak mendeteksi objek produk yang valid atau server AI sedang sibuk. Mohon unggah ulang dalam 10-15 detik (waktu 'Cold Start').")

        with col_kpi:
            st.markdown("### 📊 Indikator Kinerja (KPI)")
            # POIN 2: KPI METRICS (Dinamis Sesuai Hasil AI)
            if isinstance(results, list) and len(results) > 0:
                score = results[0]['score']
                total_obj = len(results)
                st.metric("Total Produk Terdeteksi", f"{total_obj} Unit")
                st.metric("Skor Kepercayaan AI", f"{score:.1%}")
                
                st.write("**Daftar Kategori Produk:**")
                # Menampilkan daftar kategori unik yang ditemukan
                st.write(", ".join(set(found_labels)))
            else:
                st.metric("Total Produk Terdeteksi", "0 Unit")
                st.metric("Skor Kepercayaan AI", "0.0%")
                st.info("Menunggu data dari hasil analisis AI...")

    # SECTION 2: GRAFIK (WAJIB ADA & SINKRON DENGAN FOTO)
    if isinstance(results, list) and len(results) > 0:
        st.markdown("---")
        st.subheader("🔍 Analisis Data Sinkron Berdasarkan Foto")
        col_grafik1, col_grafik2 = st.columns(2)

        with col_grafik1:
            # POIN 2: TREN GARIS (Dinamis: Tren Confidence Score)
            st.write("**Tren Skor Kepercayaan per Objek**")
            # Mengambil skor confidence dari semua objek
            scores_data = pd.DataFrame({'Skor': [res['score'] for res in results]})
            # Menampilkan tren kepercayaan untuk membuktikan sinkronisasi
            st.line_chart(scores_data)

        with col_grafik2:
            # POIN 2: PERFORMA (Dinamis: Perbandingan Jumlah per Kategori)
            st.write("**Performa Produk per Kategori**")
            # Menghitung jumlah per kategori yang ditemukan
            counts = pd.Series(found_labels).value_counts()
            # Menampilkan grafik batang untuk performa kategori
            st.bar_chart(counts)
            
        st.success("Grafik di atas sinkron sepenuhnya dengan objek yang ditemukan AI di foto.")
    else:
        st.warning("Unggah foto produk untuk melihat visualisasi data sinkron.")

else:
    # Menampilkan pesan panduan saat belum ada foto
    st.info("Mohon unggah foto produk di panel atas untuk melihat hasil analisis AI dan visualisasi data.")

# FOOTER INFORMATIF (POIN 3 INSTRUKSI: USER FRIENDLY)
st.markdown("---")
st.caption(f"App: VisionQC v1.0 | PBO Paradigma: {QualityApp.__mro__[-2]} Inheritance | Cloud AI API: Detr-ResNet-50")
