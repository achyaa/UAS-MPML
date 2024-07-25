import pickle
import streamlit as st
import numpy as np

# Membaca model
traffic_model = pickle.load(open('model.sav','rb'))

# Judul web
st.title('Prediksi Traffic')