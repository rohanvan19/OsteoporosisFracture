import streamlit as st
import pandas as pd
import numpy as np
import pickle
import mysql.connector
from streamlit_extras.switch_page_button import switch_page

# Create a connection to the database / Create a cursor object and execute a SQL query to create a table
try:
    conn = mysql.connector.connect(
        user='root',
        password='rohanvan',
        host='localhost',
        database='osteoporosis_dataset'
    )
    cursor = conn.cursor()
    create_table_query = """
        CREATE TABLE IF NOT EXISTS patient_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            age INT,
            gender INT,
            weight FLOAT,
            height FLOAT,
            smoke INT,
            alcohol INT,
            diabetes INT,
            parentfracture INT,
            arthritis INT,
            bmdscore FLOAT,
            prediction VARCHAR(50)
        )
    """
    cursor.execute(create_table_query)
except mysql.connector.Error as error:
    print("Failed to connect to database: {}".format(error))

patient_data = {
    "name" : "",
    "age" : "",
    "gender" : "",
    "weight" : "",
    "height" : "",
    "smoke" : "",
    "alcohol" : "",
    "diabetes" : "",
    "parentfracture" : "",
    "arthritis" : "",
    "bmdscore" : "",
}

#BACKGROUND IMAGE
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

# Define the available models
models = {
    'Logistic Regression': 'logistic_regression.pkl',
    'K-Nearest Neighbor': 'K_nearest_neighbor.pkl',
    'Support Vector Machine': 'support_vector_machine.pkl'
}

# Add a dropdown for the user to choose a model
selected_model = st.selectbox('Select a model for prediction', list(models.keys()))

# Load the selected model
with open(models[selected_model], 'rb') as f:
    model = pickle.load(f)
    # Enable probability estimates for SVM classifiers
    if 'SVM' in selected_model:
        model.probability = True

# model = pickle.load(open("logistic_regression.pkl", "rb"))

st.title("Osteoporosis Prediction")

#DISPLAYING VALUES
st.write("**Patient Name** : ", st.session_state["name"])
st.write("**Patient Gender** : ", st.session_state["Patient_Gender"])
st.write("**Patient Age** : ", st.session_state["Patient_Age"]," years")
st.write("**Patient Weight** : ", st.session_state["Patient_Weight"]," Kg")
st.write("**Patient Height** : ", st.session_state["Patient_Height"]," Cm")
st.write("**Parent Fractured Hip** : ", st.session_state["Parent_Fractured_Hip"])
st.write("**Patient Smokes** : ", st.session_state["Patient_Smoke"])
st.write("**Patient Consumes Alcohol** : ", st.session_state["Patient_Alcohol"])
st.write("**Patient Has Diabetes** : ", st.session_state["Patient_Diabetes"])
st.write("**Patient Has Arthritis Disease** : ", st.session_state["Patient_Arthritis"])
st.write("**Patient BMD Score** : ", st.session_state["Patient_BMD_Score"])

#STORING VALUES IN DATABASE
patient_data["name"] = st.session_state["name"]
patient_data["age"] = st.session_state["Patient_Age"]
patient_data["gender"] = st.session_state["Patient_Gender"]
patient_data["weight"] = st.session_state["Patient_Weight"]
patient_data["height"] = st.session_state["Patient_Height"]
patient_data["smoke"] = st.session_state["Patient_Smoke"]
patient_data["alcohol"] = st.session_state["Patient_Alcohol"]
patient_data["diabetes"] = st.session_state["Patient_Diabetes"]
patient_data["parentfracture"] = st.session_state["Parent_Fractured_Hip"]
patient_data["arthritis"] = st.session_state["Patient_Arthritis"]
patient_data["bmdscore"] = st.session_state["Patient_BMD_Score"]

def predict_result():
    gender_input = st.session_state["Patient_Gender"]
    age_input = st.session_state["Patient_Age"]
    weight_input = st.session_state["Patient_Weight"]
    height_input = st.session_state["Patient_Height"]
    fracture_input = st.session_state["Parent_Fractured_Hip"]
    smoke_input = st.session_state["Patient_Smoke"]
    alcohol_input = st.session_state["Patient_Alcohol"]
    diabetes_input = st.session_state["Patient_Diabetes"]
    arthritis_input = st.session_state["Patient_Arthritis"]
    bmd_input = st.session_state["Patient_BMD_Score"]

    #LR
    to_predict = np.array([gender_input,age_input,weight_input,height_input,fracture_input,smoke_input,alcohol_input,diabetes_input,arthritis_input,bmd_input]).reshape(1,-1)
    pred = model.predict(to_predict)[0]
    pred_prob = model.predict_proba(to_predict)[0]

    insert_query = """
        INSERT INTO patient_data (name, age, gender, weight, height, smoke, alcohol, diabetes, parentfracture, arthritis, bmdscore, prediction)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        patient_data["name"],
        patient_data["age"],
        patient_data["gender"],
        patient_data["weight"],
        patient_data["height"],
        patient_data["smoke"],
        patient_data["alcohol"],
        patient_data["diabetes"],
        patient_data["parentfracture"],
        patient_data["arthritis"],
        patient_data["bmdscore"],
        pred
    )
    cursor.execute(insert_query, values)
    conn.commit()
    print("Inserted values:", values)
    print("Input values stored in database!")

    return pred, pred_prob

but1 = st.container()

# Display exit button
but2 = st.button("Exit")
if but2:
    st.session_state["name"] = ""
    st.session_state["Patient_Gender"] = 0
    st.session_state["Patient_Age"] = 0
    st.session_state["Patient_Weight"] = 0.0
    st.session_state["Patient_Height"] = 0.0
    st.session_state["Parent_Fractured_Hip"] = 0
    st.session_state["Patient_Smoke"] = 0
    st.session_state["Patient_Alcohol"] = 0
    st.session_state["Patient_Diabetes"] = 0
    st.session_state["Patient_Arthritis"] = 0
    st.session_state["Patient_BMD_Score"] = 0.0
    st.button(switch_page("Homepage"))

with but1:
    pred = st.button('Predict', type="primary")

if pred:
    predictions = predict_result()
    prediction_type = {
        "Low": "bones are predicted to be in good condition (Normal)",
        "Moderate": "bones are predicted to be weaker than normal. (Moderate risk) of developing Osteoporosis ",
        "High": "bones are predicted to be weak and fragile, which involves (High risk) of developing Osteoporosis",
    }
    pred, pred_prob = predictions
    pred_score = round(pred_prob.max() * 100, 2)
    op = prediction_type[pred]
    st.success('Patient '+op+' with the prediction score of '+str(pred_score)+' %.')

    # Close the cursor and the database connection
    cursor.close()
    conn.close()
else:
    pass

# st.write("Risk Level Prediction Key:")
# st.write("- Normal: Your bones are in good condition and you are at a s.")
# st.write("- Moderate (Osteopeniac): Your bones are weaker than normal, but not to the level of Osteoporosis. You are at a moderate risk of developing Osteoporosis.")
# st.write("- High (Osteoporotic): Your bones are weak and fragile, which puts you at a high risk of developing Osteoporosis.")
