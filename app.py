import streamlit as st
import pandas as pd
import pickle

with open("model.pkl",'rb') as f:
    model = pickle.load(f)

def main():
    st.title("Insurance Premium Prediction 🛡️")
    st.write("Please provide the following information:")

    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False
        st.session_state.horizontal = False

    col1, col2 = st.beta_columns(2)
    col1_r, col2_r = st.beta_columns(2)

    with col1:
        st.header("Personal Information")
        age = st.number_input("Age", min_value=0, max_value=100, value=36)
        bmi = st.number_input("BMI", min_value=0, max_value=100, value=22)
        no_oth_claims = st.number_input("Number of Other Claims", min_value=0, value=0)
        covid_h_claims = st.number_input("Number of COVID-19 Hospitalization Claims", min_value=0, value=0)

    with col2:
        st.header("Claims Information")
        no_mat_claims = st.number_input("Number of Maternity Claims", min_value=0, value=0)
        no_crit_claims = st.number_input("Number of Critical Illness Claims", min_value=0, value=0)
        no_chro_claims = st.number_input("Number of Chronic Illness Claims", min_value=0, value=0)

    with col1_r:
        st.header("Gender and Relationship")
        gender_options = ['Male', 'Female']
        selected_gender = st.radio("Gender", gender_options)
        st.write("Relationship:")
        relation_employee = st.checkbox("Employee", value=True)
        relation_spouse = st.checkbox("Spouse")

    with col2_r:
        st.header("Marital Status and Risk Profile")
        marital_status_single = st.checkbox("Single", value=True)
        marital_status_married = st.checkbox("Married")
        is_high_risk_prof_yes = st.checkbox("Yes")
        is_high_risk_prof_no = st.checkbox("No", value=True)

    st.header("Nationality")
    with st.beta_container():
        nationality_options = ['AFC', 'EC', 'ISC', 'NEA', 'SEA', 'USC']
        selected_nationality = st.radio("Select nationality", nationality_options, key="nationality")

    if st.button("Submit"):
        data = {
            'Age': age,
            'BMI': bmi,
            'No_Mat_Claims': no_mat_claims,
            'No_Crit_Claims': no_crit_claims,
            'No_Chro_Claims': no_chro_claims,
            'No_Oth_Claims': no_oth_claims,
            'Covid_H_Claims': covid_h_claims,
            'Gender_male': selected_gender == 'Male',
            'Gender_female': selected_gender == 'Female',
            'Relation_employee': relation_employee,
            'Relation_spouse': relation_spouse,
            'Nationality_AFC': selected_nationality == 'AFC',
            'Nationality_EC': selected_nationality == 'EC',
            'Nationality_ISC': selected_nationality == 'ISC',
            'Nationality_NEA': selected_nationality == 'NEA',
            'Nationality_SEA': selected_nationality == 'SEA',
            'Nationality_USC': selected_nationality == 'USC',
            'Marital_Status_single': marital_status_single,
            'Marital_Status_married': marital_status_married,
            'Is_High_Risk_Prof_yes': is_high_risk_prof_yes,
            'Is_High_Risk_Prof_no': is_high_risk_prof_no
        }
        if data['Gender_male'] == True:
            data['Gender_male'] =1
        else:
            data['Gender_male'] = 0

        if data['Marital_Status_single'] == True:
            data['Marital_Status_single'] = 1
        else:
            data['Marital_Status_single'] = 0

        if data['Is_High_Risk_Prof_yes'] == True:
            data['Is_High_Risk_Prof_yes'] = 1
        else:
            data['Is_High_Risk_Prof_yes'] = 0

        data.pop("Is_High_Risk_Prof_no")
        data.pop("Marital_Status_married")
        # data.pop("Gender_male")
        data.pop("Gender_female")
        # Convert data to DataFrame
        df = pd.DataFrame(data, index=[0])
        print(df)
        # Perform further processing or prediction using the data
        prediction = model.predict(df)  # Replace ml_model with your actual ML model

        # st.write("Prediction:", prediction)  # Display the prediction result

        error_style = """
            <style>
            .error-message {
                padding: 1rem;
                background-color: green;
                color: white;
                border-radius: 0.5rem;
                font-weight: bold;
                font-size: 1.2rem;
            }
            </style>
        """

        # Display the error message
        st.markdown(error_style, unsafe_allow_html=True)
        st.markdown('<div class="error-message">The Expect Value Of Premuim Will Be:- ' + str(prediction[0]) + "</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()