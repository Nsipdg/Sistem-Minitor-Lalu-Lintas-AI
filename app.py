import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import requests
import json
import base64

# --- PBO: INHERITANCE ---
class AIService:
    def __init__(self, key):
        self.key = key
        # MENGGUNAKAN v1beta KARENA FLASH ADA DI SINI
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.key}"

class QualityApp(AIService):
    def __init__(self, key):
        super().__init__(key)
        self.title = "Vision QC - Jalur Beta"

    def analyze(self, img_bytes):
        img_b64 = base64.b64encode(img_bytes).decode('utf-8')
        payload = {
            "contents": [{
                "parts": [
                    {"text": "Analisis foto ini. Berikan jawaban dalam JSON mentah saja: {\"produk\": \"nama kue\", \"skor\": 95, \"unit\": 4, \"tren\": [80, 85, 95]}"},
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
            raise Exception(f"Status {res.status_code}: {res.text}")

# --- UI ---
st.set_page_config(page_title="Vision QC", layout="wide")
API_KEY = "AIzaSyB3bQLCvAb2b4tw7Gmsz-N4ZKXwfiFND30" # <--- GANTI INI

app = QualityApp(API_KEY)
st.title("🛡️ " + app.title)

uploaded_file = st.file_uploader("Upload Foto", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img_bytes = uploaded_file.getvalue()
    st.image(img_bytes, width=350)
    
    if st.button("Jalankan Analisis"):
        with st.spinner("Menghubungi Jalur Beta..."):
            try:
                data = app.analyze(img_bytes)
                c1, c2, c3 = st.columns(3)
                c1.metric("Produk", data.get('produk', '-'))
                c2.metric("Unit", f"{data.get('unit', 0)} Pcs")
                c3.metric("Skor", f"{data.get('skor', 0)}%")
                
                st.line_chart(data.get('tren', []))
                st.success("Analisis Berhasil!")
            except Exception as e:
                st.error(f"Error: {e}")
                
