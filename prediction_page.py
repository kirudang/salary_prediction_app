import streamlit as st
import pickle
import numpy as np
import xgboost as xgb
from PIL import Image


def load_model():
    with open('./models/Saved_model.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

# Load model and encoders saved
data = load_model()
xgb = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]
le_employment = data["le_employment"]
le_gender = data["le_gender"]




def show_predict_page():
    st.title("**:blue[Software Engineer Developer Salary Prediction Application]**")
    # Display the image
    st.image('c:/Users/Kirudang/Desktop/Salary_prediction/images/Salary.jpg')


    countries = ( 'United States of America', 
                'Germany',
                'United Kingdom of Great Britain and Northern Ireland',
                'India',
                'Brazil',
                'Canada',
                'France',
                'Poland',
                'Spain',
                'Netherlands',
                'Italy',
                'Australia',
                'Sweden',
                'Russian Federation',
                'Turkey',
                'Others'
    )

    education = (
        "Less than a Bachelors",
        "Bachelor’s degree",
        "Master’s degree",
        "Higher education(PhD, Doctoral degrees,...)",
    )

    employment = ("Full-time Employment",
                  "Part-time Employment",
                  "Independent Contractor",
                  "I prefer not to say / Others"
    )

    gender = ("Man", "Woman", "Others")


    
    Country = st.selectbox("**:blue[Country:]**", countries)
    Education = st.selectbox("**:blue[Education Level:]**", education)
    Employment = st.selectbox("**:blue[Type of Employment:]**", employment)
    Year_of_Experience = st.slider("**:blue[Years of Professional Working Experience:]**", 0, 51, 3)
    Gender = st.selectbox("**:blue[Gender:]**", gender)


    ok = st.button("Calculate Salary")
    if ok:
        X = np.array([[Country, Education, Employment, Year_of_Experience, Gender]])
        X[:, 0] = le_country.transform(X[:,0])
        X[:, 1] = le_education.transform(X[:,1])
        X[:, 2] = le_employment.transform(X[:,2])
        X[:, 4] = le_gender.transform(X[:,4])
 
        X = X.astype(float)

        salary = xgb.predict(X)
        st.subheader(f"The estimated salary with above information is **:blue[${salary[0]:,.2f}]**.")



