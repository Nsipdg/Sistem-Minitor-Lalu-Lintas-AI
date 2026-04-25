import streamlit as st
import google.generativeai as genai
import pandas as pd
import numpy as np
from PIL import Image
import io
import json
import re

# --- KONSEP PBO: INHERITANCE (SYARAT UTS) ---
class GeminiEngine:
    def __init__(self, key):
        # Mengonfigurasi Gemini dengan Key
        genai.configure(api_key=key)
        # Menggunakan model Flash agar cepat
        self.model = genai.GenerativeModel('gemini-1.5-flash')

class QualityApp(GeminiEngine):
    def __init__(self, key):
        super().__init__(key)
        self.title = "Gemini AI Quality Analytics"

    def analyze_image(self, img_pil):
        # PROMPT GALAK (Memaksa Gemini memberikan JSON meskipun bingung)
        prompt = """
        Analisis foto produk ini sebagai inspektur QC.
        Berikan jawaban HANYA DALAM BENTUK JSON mentah, jangan beri teks penjelasan apapun.
        Jika kamu bingung, tebak saja angkanya berdasarkan apa yang terlihat paling mirip.
        
        Format JSON yang WAJIB kamu ikuti:
        {
          "produk": "Sebutkan nama objek paling dominan (misal: Kue Dadar)",
          "skor_kualitas": 80,
          "jumlah_unit": 3,
          "status": "Lolos",
          "data_tren": [70, 75, 80, 78, 82]
        }
        """
        
        # Memanggil Gemini Vision
        response = self.model.generate_content([prompt, img_pil])
        
        # MEMBERSIHKAN FORMAT MARKDOWN (```json ... ```)
        raw_text = response.text
        clean_json_text = re.sub(r'```json|```', '', raw_text).strip()
        
        # MENGUBAH TEKS MENJADI OBJEK JSON (DIKEMBALIKAN KE UI)
        return json.loads(clean_json_text)

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Vision AI Pro", layout="wide")
API_KEY = "AIzaSyB3bQLCvAb2b4tw7Gmsz-N4ZKXwfiFND30" # <--- JANGAN LUPA GANTI INI

# Cek apakah API Key masih pakai tulisan contoh
if API_KEY == "MASUKKAN_API_KEY_KAMU_DISINI":
    st.error("⚠️ Masukkan API Key Gemini kamu di dalam kode!")
    st.stop()

# Membuat objek aplikasi (PBO)
app = QualityApp(API_KEY)
st.title("♊ " + app.title)
st.caption("Deployment: GitHub + Streamlit + Gemini 1.5 Flash (Image Understanding)")

# SECTION 1: UPLOAD & ANALISIS
uploaded_file = st.file_uploader("Unggah foto produk untuk dianalisis...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Membuka file gambar
    img = Image.open(uploaded_file)
    
    col_img, col_data = st.columns([1, 1])
    
    with col_img:
        st.image(img, caption="Foto Input", use_column_width=True)
        
    with col_data:
        with st.spinner('Gemini sedang menganalisis foto...'):
            try:
                # Memanggil fungsi analisis dari objek app
                res = app.analyze_image(img)
                
                # Menampilkan KPI (POIN 2 INSTRUKSI)
                st.subheader("🚀 KPI Indikator (Real AI)")
                k1, k2, k3 = st.columns(3)
                k1.metric("Produk", res.get('produk', 'Tidak Diketahui'))
                k2.metric("Unit", f"{res.get('jumlah_unit', 0)} Pcs")
                k3.metric("Quality Score", f"{res.get('skor_kualitas', 0)}%")
                
                # Menampilkan Status Lolos/Gagal
                final_status = res.get('status', 'Gagal')
                if final_status == "Lolos":
                    st.success(f"Status Final: {final_status}")
                else:
                    st.error(f"Status Final: {final_status}")

                # SECTION 2: GRAFIK SINKRON (POIN 2 INSTRUKSI)
                st.markdown("---")
                c1, c2 = st.columns(2)
                
                with c1:
                    st.write("**📈 Tren Kualitas Berdasarkan Analisis**")
                    # Mengambil data tren dari hasil Gemini
                    st.line_chart(res.get('data_tren', [0,0,0,0,0]))
                    
                with c2:
                    st.write("**📊 Performa Unit Terdeteksi**")
                    # Grafik batang performa produk
                    p_data = pd.DataFrame({
                        'Kategori': ['Lolos QC', 'Reject'],
                        'Jumlah': [res.get('jumlah_unit', 0), 0 if final_status == 'Lolos' else 1]
                    })
                    st.bar_chart(p_data.set_index('Kategori'))
                    
                st.success("Grafik di atas sinkron sepenuhnya dengan analisis Gemini terhadap foto.")

            except json.JSONDecodeError:
                # Ini terjadi jika Gemini menjawab pakai teks penjelasan, bukan JSON mentah
                st.error("Gagal membaca data AI. Gemini memberikan jawaban bukan format JSON. Coba unggah ulang fotonya.")
                # st.write(response.text) # Aktifkan untuk debug
            except Exception as e:
                # Pesan error umum (misal API key mati)
                st.error(f"Gagal menganalisis. Cek API Key atau pastikan foto jelas. Error: {e}")
                res = None

else:
    # Pesan panduan jika belum ada foto
    st.info("Silakan unggah foto untuk melihat kekuatan analisis Gemini Vision secara real-time.")

# FOOTER INFORMATIF (POIN 3 INSTRUKSI)
st.markdown("---")
st.caption("Dibuat untuk UTS PBO | Paradigma: Inheritance | Engine: Google Gemini 1.5 Flash")
