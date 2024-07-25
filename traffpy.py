import pickle
import streamlit as st
import numpy as np
import os
import logging
import sys
import sklearn

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)

# Informasi versi
st.write(f"Python version: {sys.version}")
st.write(f"Sklearn version: {sklearn.__version__}")

# Judul web
st.title('Prediksi Traffic')

# Fungsi untuk memuat model
def load_model(path):
    try:
        with open(path, 'rb') as file:
            model = pickle.load(file)
        logging.info(f"Model berhasil dimuat dari {path}")
        return model
    except Exception as e:
        logging.error(f"Gagal memuat model dari {path}: {e}")
        return None

# Mencoba beberapa lokasi untuk model
current_directory = os.path.dirname(os.path.abspath(__file__))
model_locations = [
    os.path.join(current_directory, 'model.sav'),
    'model.sav',
    '/app/model.sav',
    os.path.expanduser('~/model.sav')
]

traffic_model = None
for path in model_locations:
    traffic_model = load_model(path)
    if traffic_model:
        st.success(f"Model berhasil dimuat dari: {path}")
        break

if not traffic_model:
    st.error("Tidak dapat menemukan atau memuat model. Aplikasi tidak dapat melanjutkan.")
    st.stop()

# Verifikasi model
if hasattr(traffic_model, 'predict'):
    st.success("Model valid dan memiliki metode predict")
else:
    st.error("Model tidak valid atau tidak memiliki metode predict")
    st.stop()

# Input data
CarCount = st.number_input('CarCount', value=2, step=1)
BikeCount = st.number_input('BikeCount', value=120, step=1)
BusCount = st.number_input('BusCount', value=70, step=1)
TruckCount = st.number_input('TruckCount', value=20, step=1)
Total = st.number_input('Total', value=25.0, step=0.1)

# Logging tipe data input
logging.info(f"Input types: {type(CarCount)}, {type(BikeCount)}, {type(BusCount)}, {type(TruckCount)}, {type(Total)}")

# Membuat tombol untuk prediksi
if st.button('Prediksi'):
    try:
        # Konversi input menjadi numerik
        inputs = np.array([[CarCount, BikeCount, BusCount, TruckCount, Total]])
        
        # Lakukan prediksi
        prediction = traffic_model.predict(inputs)
        
        # Tentukan situasi lalu lintas berdasarkan prediksi
        traffic_situations = {
            1: 'Normal',
            2: 'Low',
            3: 'High',
            4: 'Heavy'
        }
        Traffic_Situation = traffic_situations.get(prediction[0], 'Tidak Diketahui')
        
        st.success(f'Situasi Lalu Lintas: {Traffic_Situation}')
    except ValueError as ve:
        st.error(f"Kesalahan nilai input: {ve}")
        logging.error(f"ValueError: {ve}")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
        logging.error(f"Unexpected error: {e}")

# Informasi tambahan untuk debugging
st.write("Informasi Debugging:")
st.write(f"Current directory: {current_directory}")
st.write(f"Model path yang dicoba: {', '.join(model_locations)}")
