import streamlit as st
from streamlit_extras.switch_page_button import switch_page

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

st.title("Osteoporosis Questionnaire")

if "name" not in st.session_state:
    st.session_state["name"] = ""

if "Patient_Age" not in st.session_state:
    st.session_state["Patient_Age"] = ""

if "Patient_Gender" not in st.session_state:
    st.session_state["Patient_Gender"] = ""

if "Patient_Weight" not in st.session_state:
    st.session_state["Patient_Weight"] = ""

if "Patient_Height" not in st.session_state:
    st.session_state["Patient_Height"] = ""

# NAME 
name = st.text_input('Enter Full Name :', st.session_state["name"])

# AGE
def validate_age(Patient_Age):
    if Patient_Age == '':
        return False
    try:
        int(Patient_Age)
        if int(Patient_Age) >= 0 and int(Patient_Age) <= 150:
            return True
        else:
            return False
    except ValueError:
        return False

Patient_Age = st.number_input('Enter Age:', min_value=0, max_value=120, step=1)

# GENDER
gender = {"Female":0,"Male":1}
st.session_state["Patient_Gender"] = Patient_Gender = st.radio("Select gender : ",gender)

# WEIGHT
def validate_weight(Patient_Weight):
    if Patient_Weight <= 0:
        return False
    else:
        return True

Patient_Weight = st.number_input('Enter Weight (KG)', min_value=0.0, max_value=200.0, step=1.0, format="%f", value=0.0)

# HEIGHT
def validate_height(Patient_Height):
    if Patient_Height <= 0:
        return False
    else:
        return True

Patient_Height = st.number_input('Enter Height (CM)', min_value=0.0, max_value=200.0, step=1.0, format="%f", value=0.0)

submit = st.button('Submit')

if submit:
    valid_input = True
    #NAME
    if not name:
        st.error('Please enter a name')
        valid_input = False
    elif any(char.isdigit() for char in name):
        st.error('Name should not contain numbers')
        valid_input = False
    #AGE
    if not validate_age(Patient_Age):
        st.error('Please enter a valid age')
        valid_input = False
    #GENDER
    if not Patient_Gender:
        st.error('Please select a gender')
        valid_input = False
    #WEIGHT
    if not validate_weight(Patient_Weight):
        st.error('Please enter a valid weight')
        valid_input = False
    #HEIGHT
    if not validate_height(Patient_Height):
        st.error('Please enter a valid height')
        valid_input = False

    # Navigate to new page if inputs are valid
    if valid_input:
        st.session_state["name"] = name
        st.session_state["Patient_Age"] = Patient_Age
        st.session_state["Patient_Gender"] = gender[Patient_Gender]
        st.session_state["Patient_Weight"] = Patient_Weight
        st.session_state["Patient_Height"] = Patient_Height
        st.button(switch_page("Medical_Details"))