import streamlit as st
import xgboost as xgb
from prediction_page import show_predict_page
from EDA_page import show_EDA_page


page = st.sidebar.selectbox("Explore Or Predict", ("Predict", "Explore"))

if page == "Predict":
     show_predict_page()
else:
     show_EDA_page()
