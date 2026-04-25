import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2 # OpenCV untuk simulasi AI

# --- KONSEP PBO: INHERITANCE (Pewarisan) ---
class BaseDetector:
    def __init__(self, target_domain):
        self.domain = target_domain
        self.model_status = "AI Engine Active"

    def get_info(self):
        return f"Domain: {self.domain} | Status: {self.model_status}"

# Class Anak yang mewarisi Class Induk
class TrafficVisionAI(BaseDetector):
    def __init__(self):
        # Memanggil konstruktor induk
        super().__init__("Smart Traffic Monitoring")
        # Daftar kendaraan yang bisa dideteksi model ini
        self.vehicle_classes = ["Mobil", "Motor", "Bus", "Truk"]
        self.accident_classes = ["Tabrakan", "Pecah Ban", "Mogok"]

    # Fungsi AI Utama: Analisis Gambar
    def analyze_image(self, uploaded_file, confidence_threshold):
        # 1. Konversi file unggahan Streamlit ke format OpenCV
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, 1)
        original_image = Image.fromarray(cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB))
        
        # --- SIMULASI AI VISION (Di sini harusnya model AI asli) ---
        h, w, _ = opencv_image.shape
        num_vehicles = np.random.randint(5, 20) # Random jumlah kendaraan
        counts = {cls: 0 for cls in self.vehicle_classes}
        bboxes = []
        accident_detected = np.random.choice([True, False], p=[0.2, 0.8]) # 20% peluang kecelakaan

        # Membuat bbox (kotak) simulasi di atas threshold
        for _ in range(num_vehicles):
            cls = np.random.choice(self.vehicle_classes)
            conf = np.random.uniform(0.5, 0.99)
            if conf >= confidence_threshold:
                counts[cls] += 1
                x, y = np.random.randint(0, w-100), np.random.randint(0, h-100)
                bboxes.append(((x, y), (x+100, y+100), cls, conf))

        return original_image, bboxes, counts, accident_detected

    # Fungsi AI Kedua: Analisis Risiko
    def analyze_traffic_risks(self, vehicle_counts, accident_detected):
        total_vehicles = sum(vehicle_counts.values())
        risks = []
        
        # Analisis Risiko Kemacetan
        if total_vehicles > 15:
            risks.append({"Tipe": "Kemacetan", "Level": "Tinggi", "Penyebab": "Volume kendaraan melebihi kapasitas jalan."})
        elif total_vehicles > 8:
            risks.append({"Tipe": "Kemacetan", "Level": "Sedang", "Penyebab": "Volume kendaraan padat."})

        # Analisis Risiko Kecelakaan
        if accident_detected:
            accident_type = np.random.choice(self.accident_classes)
            risks.append({"Tipe": "Kecelakaan", "Level": "Kritis", "Penyebab": f"Deteksi objek insiden ({accident_type}) di badan jalan."})
        elif vehicle_counts["Motor"] > (vehicle_counts["Mobil"] * 3) and total_vehicles > 10:
             risks.append({"Tipe": "Kecelakaan", "Level": "Sedang", "Penyebab": "Rasio kendaraan roda dua terlalu tinggi (Perilaku selap-selip)."})

        return risks

# --- UI STREAMLIT DASHBOARD (Poin 3 Instruksi: Informatif & Interaktif) ---
st.set_page_config(page_title="AI Traffic Risk Detector", page_icon="🚦", layout="wide")

# Menginisialisasi Objek AI (Penerapan PBO)
traffic_ai = TrafficVisionAI()

st.title("🚦 AI Traffic Risk Detection System")
st.markdown(traffic_ai.get_info())

# Poin 3: Tata Letak yang Seimbang
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📸 Analisis Citra CCTV (AI Detection)")
    uploaded_file = st.file_uploader("Unggah foto kondisi lalu lintas...", type=["jpg", "png", "jpeg"])
    
    # Slider untuk mengatur tingkat kepercayaan AI (Interaktif)
    confidence_threshold = st.slider("Ambang Batas Kepercayaan AI (Confidence Threshold)", 0.5, 0.99, 0.85)

if uploaded_file is not None:
    # Memproses gambar dengan AI (PBO Metode)
    with st.spinner('AI sedang menganalisis resiko...'):
        image_with_bboxes, bboxes, vehicle_counts, accident_detected = traffic_ai.analyze_image(uploaded_file, confidence_threshold)
        
        # Menampilkan gambar hasil deteksi
        draw = ImageDraw.Draw(image_with_bboxes)
        for bbox in bboxes:
            start_point, end_point, cls, conf = bbox
            draw.rectangle([start_point, end_point], outline="red", width=5)
            # Menambahkan teks label kendaraan
            text = f"{cls} ({conf:.2f})"
            draw.text(start_point, text, fill="white")
        
        col1.image(image_with_bboxes, caption="Hasil Deteksi Kendaraan & Insiden", use_column_width=True)

    with col2:
        st.subheader("📊 Statistik Deteksi & Analisis Resiko")
        
        # Poin 2: Indikator Kinerja Utama (KPI)
        total_v = sum(vehicle_counts.values())
        st.metric("Total Kendaraan", f"{total_v}", delta="+10% vs Rata-rata" if total_v > 10 else "-5% vs Rata-rata")
        
        if accident_detected:
            st.error("🚨 PERINGATAN: Deteksi Insiden di Jalan Raya!")
        else:
            st.success("✅ Tidak ada insiden kritis terdeteksi.")

        # Poin 2: Grafik Perbandingan
        st.markdown("---")
        st.write("**Perbandingan Jenis Kendaraan:**")
        df_counts = pd.DataFrame(vehicle_counts.items(), columns=['Kategori', 'Jumlah'])
        st.bar_chart(df_counts.set_index('Kategori'))

        # Poin 2: Analisis Risiko AI (Sesuai ide canggih kamu)
        st.markdown("---")
        st.write("**AI Risk Analysis (Potensi Masalah):**")
        risk_list = traffic_ai.analyze_traffic_risks(vehicle_counts, accident_detected)
        
        if risk_list:
            for risk in risk_list:
                level_color = "red" if risk["Level"] == "Kritis" else "orange" if risk["Level"] == "Tinggi" else "yellow"
                st.markdown(f"""
                <div style="background-color:rgba({level_color}, 0.2); padding:10px; border-radius:5px; margin-bottom:10px;">
                    <b style="color:{level_color};">{risk['Tipe']} (Level: {risk['Level']})</b><br>
                    Penyebab: {risk['Penyebab']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Kondisi jalanan diprediksi lancar dan aman.")

else:
    st.info("Mohon unggah foto di panel kiri untuk memulai analisis AI.")
    
# Footer (Poin 3: User Friendly)
st.markdown("---")
st.caption("Peringatan: Analisis ini bersifat simulasi untuk UTS PBO dan tidak menggunakan model AI asli (simulasi OpenCV).")
