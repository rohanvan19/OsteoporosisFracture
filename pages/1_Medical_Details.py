import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.title("Habits and Medical Conditions")

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

if "Parent_Fractured_Hip" not in st.session_state:
    st.session_state["Parent_Fractured_Hip"] = ""

if "Patient_Smoke" not in st.session_state:
    st.session_state["Patient_Smoke"] = ""

if "Patient_Alcohol" not in st.session_state:
    st.session_state["Patient_Alcohol"] = ""

if "Patient_Diabetes" not in st.session_state:
    st.session_state["Patient_Diabetes"] = ""

if "Patient_Arthritis" not in st.session_state:
    st.session_state["Patient_Arthritis"] = ""

#PARENT FRACTURED HIP
fracture = {"No":0,"Yes":1}
st.session_state["Parent_Fractured_Hip"] = Parent_Fractured_Hip = st.radio("Do your parents have hip fracture history ? ",fracture)

#SMOKE
smoke={"No":0,"Yes":1}
st.session_state["Patient_Smoke"] = Patient_Smoke = st.radio("Do you Smoke every week ? ",smoke)

#ALCOHOL
alcohol={"No":0,"Yes":1}
st.session_state["Patient_Alcohol"] = Patient_Alcohol = st.radio("Do you consume Alcohol every week ? ",alcohol)

#DIABETES
diabetes={"No":0,"Yes":1}
st.session_state["Patient_Diabetes"] = Patient_Diabetes = st.radio("Do you have Diabetes ? ",diabetes)

#ARTHRITIS
arthritis={"No":0,"Yes":1}
st.session_state["Patient_Arthritis"] = Patient_Arthritis = st.radio("Do you have Arthritis diasease ? ",arthritis)

submit = st.button('Submit')

if submit:
    valid_input = True
    #SMOKE
    if Patient_Smoke == 'No':
        st.write("Patient Smokes : ",Patient_Smoke)
    if Patient_Smoke == 'Yes':
        st.write("Patient Smokes : ",Patient_Smoke)

    #ALCOHOL
    if Patient_Alcohol == 'No':
        st.write("Patient consumes Alcohol : ",Patient_Alcohol)
    if Patient_Alcohol == 'Yes':
        st.write("Patient consumes Alcohol : ",Patient_Alcohol)

    #DIABETES
    if Patient_Diabetes == 'No':
        st.write("Patient has Diabetes : ",Patient_Diabetes)
    if Patient_Diabetes == 'Yes':
        st.write("Patient has Diabetes : ",Patient_Diabetes)

    #PARENT FRACTURED HIP
    if Parent_Fractured_Hip == 'No':
        st.write("Parent Hip Fracture : ",Parent_Fractured_Hip)
    if Parent_Fractured_Hip == 'Yes':
        st.write("Parent Hip Fracture : ",Parent_Fractured_Hip)

    #ARTHRITIS
    if Patient_Arthritis == 'No':
        st.write("Patient has Arthritis Disease : ",Patient_Arthritis)
    if Patient_Arthritis == 'Yes':
        st.write("Patient has Arthritis Disease : ",Patient_Arthritis)

    # Navigate to new page if inputs are valid
    if valid_input:
        st.session_state["Patient_Smoke"] = smoke[Patient_Smoke]
        st.session_state["Patient_Alcohol"] = alcohol[Patient_Alcohol]
        st.session_state["Patient_Diabetes"] = diabetes[Patient_Diabetes]
        st.session_state["Parent_Fractured_Hip"] = fracture[Parent_Fractured_Hip]
        st.session_state["Patient_Arthritis"] = arthritis[Patient_Arthritis]
        st.button(switch_page("Patient_BMD_Score"))

prev = st.button('Previous')

if prev:
    st.button(switch_page("Homepage"))