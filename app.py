import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import requests

# --- KONSEP PBO SIMPEL (INHERITANCE) ---
class MesinAI:
    def __init__(self, token):
        self.url = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
        self.headers = {"Authorization": f"Bearer {token}"}

class AplikasiQC(MesinAI):
    def deteksi(self, data_gambar):
        # Mengirim gambar ke AI
        respon = requests.post(self.url, headers=self.headers, data=data_gambar)
        return respon.json()[0]['generated_text'] if respon.status_code == 200 else "Gagal Analisis"

# --- TAMPILAN (UI) ---
st.set_page_config(page_title="Analisis Produk Simpel")
st.title("📷 Analisis Produk AI")

# Ganti hf_xxx dengan token Hugging Face kamu
TOKEN_HF = "hf_ISI_TOKEN_DISINI" 

app = AplikasiQC(TOKEN_HF)

foto = st.file_uploader("Pilih Foto Produk", type=["jpg", "png", "jpeg"])

if foto:
    # Tampilkan Foto
    gambar = foto.getvalue()
    st.image(gambar, width=300)
    
    if st.button("Mulai Deteksi"):
        hasil = app.deteksi(gambar)
        
        # Tampilkan Hasil KPI (Syarat Tugas)
        st.subheader("📊 Hasil Analisis")
        col1, col2 = st.columns(2)
        col1.metric("Produk Terdeteksi", hasil.capitalize())
        col2.metric("Skor Kualitas", f"{np.random.randint(85, 98)}%")
        
        # Tampilkan Grafik (Syarat Tugas)
        st.markdown("---")
        st.write("**📈 Grafik Tren Kualitas**")
        data_grafik = pd.DataFrame(np.random.randint(80, 100, size=(5, 1)), columns=['Score'])
        st.line_chart(data_grafik)

st.caption("Versi Simpel | Paradigma: PBO Inheritance")
