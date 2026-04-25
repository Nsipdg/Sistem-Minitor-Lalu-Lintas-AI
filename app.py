import streamlit as st
import requests
import pandas as pd
from PIL import Image, ImageDraw
import io

# --- KONSEP PBO: INHERITANCE ---
class BaseAI:
    def __init__(self):
        # API Key gratisan Hugging Face (Public Model)
        self.api_url = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"
        self.headers = {"Authorization": "Bearer hf_xxxx"} # Kosongkan saja, model publik biasanya open

class TrafficAI(BaseAI):
    def __init__(self):
        super().__init__()

    def query(self, image_bytes):
        # Mengirim foto ke server AI Hugging Face
        response = requests.post(self.api_url, data=image_bytes)
        return response.json()

# --- UI DASHBOARD ---
st.set_page_config(page_title="AI Traffic Pro", layout="wide")
ai_system = TrafficAI()

st.title("🚦 Smart City AI Traffic Detection")
st.caption("Deployment: GitHub + Streamlit Cloud + Hugging Face API")

uploaded_file = st.file_uploader("Pilih foto lalu lintas...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img_bytes = uploaded_file.getvalue()
    img = Image.open(io.BytesIO(img_bytes))
    
    with st.spinner('Menghubungi AI Cloud...'):
        results = ai_system.query(img_bytes)
        
        # Validasi jika hasil berupa list (berhasil deteksi)
        if isinstance(results, list):
            draw = ImageDraw.Draw(img)
            labels = [res['label'] for res in results]
            
            # Gambar kotak deteksi
            for res in results:
                box = res['box']
                # Format box: xmin, ymin, xmax, ymax
                draw.rectangle([box['xmin'], box['ymin'], box['xmax'], box['ymax']], outline="red", width=3)
            
            col1, col2 = st.columns([2, 1])
            col1.image(img, use_column_width=True)
            
            with col2:
                st.subheader("📊 Hasil Analisis")
                counts = pd.Series(labels).value_counts()
                st.write(counts)
                
                # Analisis Resiko (Poin 2 Instruksi)
                st.markdown("---")
                total_car = counts.get('car', 0)
                if total_car > 5:
                    st.error(f"⚠️ Resiko Kemacetan: TINGGI ({total_car} Mobil)")
                else:
                    st.success("✅ Resiko Kemacetan: RENDAH")
        else:
            st.warning("Server AI sedang sibuk, silakan coba lagi dalam beberapa detik.")

if uploaded_file is not None:
    # Konversi file ke format yang dimengerti AI
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)
    
    with st.spinner('AI sedang memproses foto beneran...'):
        # Panggil fungsi deteksi dari Class PBO
        result_img, counts, all_labels = ai.detect_objects(opencv_image)
        
        # Tampilkan Hasil
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.image(result_img, channels="BGR", caption="Hasil Deteksi AI Asli", use_column_width=True)
            
        with col2:
            st.subheader("📊 Analisis Objek")
            if counts:
                for obj, qnty in counts.items():
                    st.write(f"✅ **{obj.capitalize()}**: {qnty} terdeteksi")
                
                # Analisis Resiko Sederhana
                st.markdown("---")
                st.subheader("⚠️ Analisis Resiko")
                if counts.get('car', 0) > 5 or counts.get('motorcycle', 0) > 10:
                    st.warning("Potensi Kemacetan: TINGGI")
                else:
                    st.success("Potensi Kemacetan: RENDAH")
            else:
                st.info("Tidak ada objek kendaraan umum terdeteksi.")
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
