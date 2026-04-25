import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import io
import requests
import json
import base64

# --- PBO: INHERITANCE ---
class AIService:
    def __init__(self, key):
        self.key = key
        # Jalur v1 resmi untuk model gemini-1.5-flash
        self.url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={self.key}"

class QualityApp(AIService):
    def __init__(self, key):
        super().__init__(key)
        self.title = "Vision QC - Gemini Flash"

    def analyze(self, img_bytes):
        img_b64 = base64.b64encode(img_bytes).decode('utf-8')
        payload = {
            "contents": [{
                "parts": [
                    {"text": "Berikan analisis produk dalam JSON mentah saja: {\"produk\": \"kue\", \"skor\": 90, \"unit\": 4, \"tren\": [80, 85, 90]}"},
                    {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
                ]
            }]
        }
        res = requests.post(self.url, json=payload)
        if res.status_code == 200:
            text = res.json()['candidates'][0]['content']['parts'][0]['text']
            clean = text.replace('```json', '').replace('```', '').strip()
            return json.loads(clean)
        else:
            raise Exception(f"Error {res.status_code}: {res.text}")

# --- UI ---
st.set_page_config(page_title="Vision QC", layout="wide")
API_KEY = "AIzaSyB3bQLCvAb2b4tw7Gmsz-N4ZKXwfiFND30" # <--- ISI DISINI

app = QualityApp(API_KEY)
st.title("🛡️ " + app.title)

uploaded_file = st.file_uploader("Upload Foto", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img_bytes = uploaded_file.getvalue()
    st.image(img_bytes, width=300)
    
    if st.button("Jalankan Analisis"):
        with st.spinner("Menghubungi Gemini v1..."):
            try:
                data = app.analyze(img_bytes)
                c1, c2, c3 = st.columns(3)
                c1.metric("Produk", data['produk'])
                c2.metric("Unit", f"{data['unit']} Pcs")
                c3.metric("Skor", f"{data['skor']}%")
                
                st.line_chart(data['tren'])
                st.success("Berhasil menggunakan Jalur v1!")
            except Exception as e:
                st.error(f"Gagal lagi? Coba cek kuota API Key: {e}")
                
