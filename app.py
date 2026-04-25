import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- PENERAPAN PBO (Inheritance) ---
class SistemAI:
    def __init__(self, nama_sistem):
        self.nama = nama_sistem
    
    def status_sistem(self):
        return f"Sistem {self.nama} berjalan optimal."

class TrafficMonitor(SistemAI):
    def __init__(self):
        super().__init__("Smart Traffic Vision")
        self.kategori = ["Mobil", "Motor", "Bus", "Truk"]

    def hitung_performa(self, confidence):
        # Simulasi data berdasarkan akurasi yang dipilih
        data = {
            'Kategori': self.kategori,
            'Akurasi (%)': [confidence * 0.98, confidence * 0.92, confidence * 0.88, confidence * 0.90]
        }
        return pd.DataFrame(data)

# --- UI STREAMLIT ---
st.set_page_config(page_title="AI Traffic Monitor", layout="wide")
monitor = TrafficMonitor()

st.title("🚦 Dashboard Analisis Lalu Lintas AI")
st.info(monitor.status_sistem())

# Sidebar untuk Interaktivitas (Poin 3 instruksi)
st.sidebar.header("Konfigurasi")
confidence = st.sidebar.slider("Patokan Akurasi AI (%)", 50, 100, 85)

# 1. KPI Metrics (Poin 2 instruksi)
col1, col2, col3 = st.columns(3)
col1.metric("Total Kendaraan", "2,450", "+15%")
col2.metric("Akurasi Rata-rata", f"{confidence}%")
col3.metric("Status Kepadatan", "Padat")

# 2. Grafik Tren / Time Series (Poin 2 instruksi)
st.subheader("📈 Tren Volume Kendaraan (Time Series)")
data_tren = pd.DataFrame(
    np.random.randn(20, 2),
    columns=['Arah Masuk', 'Arah Keluar']
)
st.area_chart(data_tren)

# 3. Grafik Perbandingan Performa (Poin 2 instruksi)
st.subheader("📊 Perbandingan Akurasi per Kategori")
df_performa = monitor.hitung_performa(confidence)
fig = px.bar(df_performa, x='Kategori', y='Akurasi (%)', color='Kategori', text_auto='.2f')
st.plotly_chart(fig)

st.caption("Data disimulasikan untuk keperluan demonstrasi sistem monitoring cerdas.")
