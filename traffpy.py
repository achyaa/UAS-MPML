import pickle
import streamlit as st
import numpy as np
import os

# Fungsi untuk memuat model
def load_model(model_path):
    try:
        with open(model_path, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        st.error(f"File model tidak ditemukan di: {model_path}")
        return None
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca model: {str(e)}")
        return None

# Coba beberapa lokasi untuk model
model_locations = [
    'model.sav',
    os.path.join(os.path.dirname(__file__), 'model.sav'),
    '/app/model.sav',  # Untuk Streamlit Cloud
    os.path.expanduser('~/model.sav')
]

traffic_model = None
for location in model_locations:
    traffic_model = load_model(location)
    if traffic_model:
        st.success(f"Model berhasil dimuat dari: {location}")
        break

if not traffic_model:
    st.error("Gagal memuat model. Aplikasi tidak dapat melanjutkan.")
    st.stop()

# Judul web
st.title('Prediksi Traffic')

# Input data
CarCount = st.number_input('CarCount', value=2, step=1)
BikeCount = st.number_input('BikeCount', value=120, step=1)
BusCount = st.number_input('BusCount', value=70, step=1)
TruckCount = st.number_input('TruckCount', value=20, step=1)
Total = st.number_input('Total', value=25.0, step=0.1)

# Membuat tombol untuk prediksi
if st.button('Prediksi'):
    try:
        # Persiapkan input
        inputs = np.array([[CarCount, BikeCount, BusCount, TruckCount, Total]])
        
        # Lakukan prediksi
        prediction = traffic_model.predict(inputs)
        
        # Tentukan situasi lalu lintas
        traffic_situations = {
            1: 'Normal',
            2: 'Low',
            3: 'High',
            4: 'Heavy'
        }
        Traffic_Situation = traffic_situations.get(prediction[0], 'Tidak Diketahui')
        
        st.success(f'Situasi Lalu Lintas: {Traffic_Situation}')
    except Exception as e:
        st.error(f"Terjadi kesalahan saat melakukan prediksi: {str(e)}")
