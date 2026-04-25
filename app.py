import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import io
import requests
import json
import base64

# --- KONSEP PBO: INHERITANCE ---
class GeminiEngine:
    def __init__(self, api_key):
        self.api_key = api_key
        # Menggunakan endpoint v1 yang paling stabil
        self.url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={self.api_key}"

class QualityApp(GeminiEngine):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.title = "Gemini AI Quality Analytics"

    def analyze_image(self, img_bytes):
        # Mengubah gambar ke base64 agar bisa dikirim lewat JSON
        image_base64 = base64.b64encode(img_bytes).decode('utf-8')
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": "Analisis foto produk ini. Berikan jawaban HANYA format JSON: {\"produk\": \"nama\", \"skor_kualitas\": 85, \"jumlah_unit\": 3, \"status\": \"Lolos\", \"data_tren\": [80, 85, 90, 85, 88]}"},
                    {"inline_data": {"mime_type": "image/jpeg", "data": image_base64}}
                ]
            }]
        }
        
        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.url, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            result_text = response.json()['candidates'][0]['content']['parts'][0]['text']
            # Bersihkan markdown jika ada
            clean_json = result_text.replace('```json', '').replace('```', '').strip()
            return json.loads(clean_json)
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")

# --- UI DASHBOARD ---
st.set_page_config(page_title="Vision AI Pro", layout="wide")
API_KEY = "AIzaSyB3bQLCvAb2b4tw7Gmsz-N4ZKXwfiFND30" # <--- GANTI INI

if API_KEY == "MASUKKAN_API_KEY_KAMU_DISINI":
    st.error("⚠️ Masukkan API Key Gemini kamu!")
    st.stop()

app = QualityApp(API_KEY)
st.title("♊ " + app.title)

uploaded_file = st.file_uploader("Unggah foto...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    img_bytes = uploaded_file.getvalue()
    st.image(img_bytes, caption="Foto Input", width=400)
    
    with st.spinner('Gemini sedang menganalisis...'):
        try:
            res = app.analyze_image(img_bytes)
            
            st.subheader("🚀 KPI Indikator")
            k1, k2, k3 = st.columns(3)
            k1.metric("Produk", res.get('produk', '-'))
            k2.metric("Unit", f"{res.get('jumlah_unit', 0)} Pcs")
            k3.metric("Skor", f"{res.get('skor_kualitas', 0)}%")
            
            st.markdown("---")
            st.write("**📈 Tren & Performa**")
            st.line_chart(res.get('data_tren', []))
            
        except Exception as e:
            st.error(f"Gagal: {e}")
else:
    st.info("Silakan unggah foto.")
