import streamlit as st

from src.logger import logging
from src.exception import CustomException

from src.pipelines import Prediction_pipeline
from src.pipelines.Prediction_pipeline import Prediction_Pipeline


# Set page config
st.set_page_config(page_title="Student Marks Prediction", page_icon="🔮", layout="centered")

st.markdown(
    """
    <style>
        .main {background-color: #f4f4f4; padding: 20px; border-radius: 10px;}
        .stButton>button {background-color: #ff4b4b; color: white; font-size: 18px; border-radius: 10px; padding: 10px 20px;}
        .stButton>button:hover {background-color: #ff6b6b;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🔮 Student Marks Prediction")
st.markdown("### Enter details to get a prediction!")


# Input form
with st.form("input_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        gender = st.selectbox('Select Gender',['male','female'])
        race_ethnicity = st.selectbox('Select Race Ethnicity',['group A','group B','group C','group D','group E'])
        parental_level_of_education = st.selectbox("Select Parental Education", ["associate's degree", "bachelor's degree", "high school","master's degree","some college","some high school"])
        writing_score = st.number_input("Enter Writing Score", min_value=0, max_value=100, step=1)

    with col2:
        lunch = st.selectbox("Select Lunch", ["free/reduced", "standard"])
        test_preparation_course = st.selectbox("Select Course", ["none", "completed"])
        reading_score = st.number_input("Enter Reading Score", min_value=0, max_value=100, step=1)
        
    
    submit_button = st.form_submit_button("🔍 Predict")

    if submit_button:
        cd = Prediction_pipeline.CustomData(gender,race_ethnicity,parental_level_of_education,lunch,test_preparation_course,reading_score,writing_score)
        data = cd.get_data_as_data_frame()
        predictor = Prediction_Pipeline()
        prediction = predictor.prediction(data)
        st.success(f"✅ The Student Marks is : {prediction[0]}")
        st.balloons()
      
    


