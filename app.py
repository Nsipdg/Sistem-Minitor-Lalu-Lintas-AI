import streamlit as st
import pandas as pd
import numpy as np

# --- KONSEP PBO: INHERITANCE ---
class BaseSystem:
    def __init__(self):
        self.status = "Aktif"
        self.name = "Smart Traffic AI"

class TrafficApp(BaseSystem):
    def __init__(self):
        super().__init__()
        self.categories = ["Mobil", "Motor", "Bus", "Truk"]

    def calculate_risk(self, volume):
        if volume > 15:
            return "Tinggi", "🚨 Resiko Kemacetan Kritis"
        elif volume > 8:
            return "Sedang", "⚠️ Potensi Kemacetan"
        else:
            return "Rendah", "✅ Arus Lancar"

# --- INTERFACE ---
st.set_page_config(page_title="UTS PBO - Traffic AI", layout="wide")
app = TrafficApp()

st.title("🚦 " + app.name)
st.write(f"Status Sistem: **{app.status}**")

# Poin 2: Indikator Utama (KPI)
st.subheader("📊 Monitoring Real-time")
col1, col2, col3 = st.columns(3)

# Input Interaktif (Pengganti Foto Sementara agar Cepat)
volume = st.slider("Simulasi Volume Kendaraan (CCTV)", 0, 30, 10)
risk_level, risk_msg = app.calculate_risk(volume)

col1.metric("Total Kendaraan", volume)
col2.metric("Level Resiko", risk_level)
col3.metric("Akurasi Sensor", "98.2%")

# Poin 2: Analisis Resiko (Ide Canggih Kamu)
st.markdown("---")
if risk_level == "Tinggi":
    st.error(risk_msg)
elif risk_level == "Sedang":
    st.warning(risk_msg)
else:
    st.success(risk_msg)

# Poin 2: Grafik Tren (Time Series)
st.subheader("📈 Tren Kepadatan (24 Jam)")
chart_data = pd.DataFrame(
    np.random.randn(24, 2),
    columns=['Arus Masuk', 'Arus Keluar']
)
st.line_chart(chart_data)

# Poin 2: Grafik Perbandingan
st.subheader("📊 Distribusi Jenis Kendaraan")
dist_data = pd.DataFrame({
    'Kategori': app.categories,
    'Jumlah': [np.random.randint(1,10) for _ in range(4)]
})
st.bar_chart(dist_data.set_index('Kategori'))
