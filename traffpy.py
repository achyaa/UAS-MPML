import pickle
import streamlit as st
import numpy as np

# Membaca model
traffic_model = pickle.load(open('model.sav', 'rb'))

# Judul web
st.title('Prediksi Traffic')

# Input data dengan contoh angka valid untuk pengujian
CarCount = st.text_input('CarCount', '2')
BikeCount = st.text_input('BikeCount', '120')
BusCount = st.text_input('BusCount', '70')
TruckCount = st.text_input('TruckCount', '20')
Total = st.text_input('Total', '25.0')

Traffic_Situation = ''

# Membuat tombol untuk prediksi
if st.button('Prediksi'):
    try:
        # Konversi input menjadi numerik
        inputs = np.array([[float(CarCount), float(BikeCount), float(BusCount), float(TruckCount), float(Total)]])
        
        # Lakukan prediksi
        prediction = traffic_model.predict(inputs)
        
        # Tentukan situasi lalu lintas berdasarkan prediksi
        if prediction[0] == 1:
            Traffic_Situation = 'Normal'
        elif prediction[0] == 2:
            Traffic_Situation = 'Low'
        elif prediction[0] == 3:
            Traffic_Situation = 'High'
        elif prediction[0] == 4:
            Traffic_Situation = 'Heavy'
        
        st.success(f'Situasi Lalu Lintas: {Traffic_Situation}')
    except ValueError:
        st.error("Pastikan semua input diisi dengan angka yang valid.")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
