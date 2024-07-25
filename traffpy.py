import sys
import os
import pickle
import streamlit as st
import numpy as np

# Tambahkan direktori saat ini ke sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Fungsi untuk memuat model
def load_model(model_path):
    try:
        with open(model_path, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        st.error(f"File model tidak ditemukan di: {model_path}")
    except ModuleNotFoundError as e:
        st.error(f"Modul tidak ditemukan: {e}")
        st.error("Pastikan semua dependensi terinstal dengan benar.")
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca model: {e}")
    return None

# Judul web
st.title('Prediksi Traffic')

# Informasi debugging
st.write(f"Current working directory: {os.getcwd()}")
st.write(f"Python path: {sys.path}")
st.write("Installed packages:")
st.write(os.popen('pip list').read())

# Coba beberapa lokasi untuk model
model_locations = [
    os.path.join(current_dir, 'model.sav'),
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

# Input data
CarCount = st.number_input('CarCount', value=2, step=1)
BikeCount = st.number_input('BikeCount', value=120, step=1)
BusCount = st.number_input('BusCount', value=70, step=1)
TruckCount = st.number_input('TruckCount', value=20, step=1)
Total = st.number_input('Total', value=25.0, step=0.1)

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
    except Exception as e:
        st.error(f"Terjadi kesalahan saat melakukan prediksi: {e}")

# Tambahan informasi untuk debugging
st.write("\nInformasi Tambahan:")
st.write(f"Python version: {sys.version}")
try:
    import sklearn
    st.write(f"Sklearn version: {sklearn.__version__}")
except ImportError:
    st.write("Sklearn tidak terinstal")
