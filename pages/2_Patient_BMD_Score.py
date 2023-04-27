import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.title("Bone Mineral Density (T - Score)")

import base64
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('output.png')  

if "Patient_BMD_Score" not in st.session_state:
    st.session_state["Patient_BMD_Score"] = ""

#BMD T_SCORE
def validate_tscore(Patient_BMD_Score):
    if Patient_BMD_Score == '':
        return False
    try:
        float(Patient_BMD_Score)
        return True
    except ValueError:
        return False

Patient_BMD_Score = st.number_input('Enter T-Score:', min_value=-10.0, max_value=10.0, step=1.0, format="%f", value=0.0)

submit = st.button('Submit')

if submit:
    valid_input = True
    if validate_tscore(Patient_BMD_Score):
        tscore_float = float(Patient_BMD_Score)
        st.write('Patient T-Score :', tscore_float)
    else:
        st.write('Please enter a valid T-Score.')

    # Navigate to new page if inputs are valid
    if valid_input:
        st.session_state["Patient_BMD_Score"] = Patient_BMD_Score
        st.button(switch_page("Prediction"))

prev = st.button('Previous')

if prev:
    st.button(switch_page("Medical_Details"))