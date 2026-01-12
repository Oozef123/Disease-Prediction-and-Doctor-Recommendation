# streamlit_app.py
import streamlit as st
import pandas as pd
import random

# Load dataset
df_doctors = pd.read_csv("indian_doctors_realistic_5000.csv")

# --- Disease & Symptom Mapping ---
disease_to_specialty = {
    "Common Cold": "General Physician",
    "Flu (Influenza)": "General Physician",
    "Migraine": "Neurologist",
    "Tension Headache": "Neurologist",
    "Sinusitis": "ENT Specialist",
    "Allergic Rhinitis (Hay Fever)": "ENT Specialist",
    "Conjunctivitis (Pink Eye)": "Ophthalmologist",
    "Cataracts": "Ophthalmologist",
    "Acne": "Dermatologist",
    "Eczema": "Dermatologist",
    "Psoriasis": "Dermatologist",
    "Hypertension (High BP)": "Cardiologist",
    "Coronary Artery Disease": "Cardiologist",
    "Asthma": "Pulmonologist",
    "Bronchitis": "Pulmonologist",
    "Pneumonia": "Pulmonologist",
    "Gastroenteritis": "Gastroenterologist",
    "Irritable Bowel Syndrome (IBS)": "Gastroenterologist",
    "Urinary Tract Infection (UTI)": "Urologist",
    "Kidney Stones": "Urologist",
    "Arthritis": "Orthopedic Surgeon",
    "Diabetes": "Endocrinologist",
    "Thyroid Disorder": "Endocrinologist",
    "Anxiety Disorder": "Psychiatrist",
    "Depression": "Psychiatrist",
    "Lower Back Pain": "Orthopedic Surgeon",
}

symptom_rules = {
    ("cough", "fever", "runny nose"): ["Common Cold", "Flu (Influenza)"],
    ("high fever", "body ache", "fatigue", "cough"): ["Flu (Influenza)"],
    ("severe headache", "nausea", "sensitivity to light"): ["Migraine"],
    ("headache", "pressure behind eyes", "stuffy nose"): ["Sinusitis"],
    ("sneezing", "itchy eyes", "runny nose"): ["Allergic Rhinitis (Hay Fever)"],
    ("red eyes", "itchy eyes", "discharge"): ["Conjunctivitis (Pink Eye)"],
    ("chest pain", "shortness of breath"): ["Coronary Artery Disease"],
    ("wheezing", "shortness of breath", "cough"): ["Asthma"],
    ("abdominal pain", "diarrhea", "nausea"): ["Gastroenteritis"],
    ("frequent urination", "burning sensation urination"): ["Urinary Tract Infection (UTI)"],
    ("joint pain", "swelling", "stiffness"): ["Arthritis"],
    ("excessive thirst", "frequent urination", "fatigue"): ["Diabetes"],
    ("persistent sadness", "loss of interest", "fatigue"): ["Depression"],
    ("skin rash", "dry skin", "itching"): ["Eczema", "Psoriasis"],
}

def predict_disease(symptoms_list):
    symptoms_list = [s.strip().lower() for s in symptoms_list]
    predicted_diseases = set()
    for rule_symptoms, diseases in symptom_rules.items():
        if any(symptom in symptoms_list for symptom in rule_symptoms):
            predicted_diseases.update(diseases)
    return list(predicted_diseases) if predicted_diseases else ["Could not determine a specific condition. Please consult a General Physician."]

def recommend_doctor(disease, city=None, state=None):
    specialty = disease_to_specialty.get(disease)
    if not specialty:
        return None
    filtered = df_doctors[df_doctors['Speciality'] == specialty]
    if city:
        filtered = filtered[filtered['Clinic_City'].str.lower() == city.lower()]
    if state:
        filtered = filtered[filtered['Clinic_State'].str.lower() == state.lower()]
    if filtered.empty:
        return None
    return filtered.sample(n=1).iloc[0]

# --- Streamlit UI ---
st.set_page_config(page_title="AI Medical Assistant", page_icon="🩺", layout="centered")
st.title("🩺 AI Medical Assistant")
st.markdown("Enter your symptoms below to get possible conditions and recommended doctors.")

# Input UI
user_symptoms = st.text_input("Enter symptoms (comma-separated):", placeholder="e.g. cough, fever, headache")
col1, col2 = st.columns(2)
user_city = col1.text_input("City (optional)")
user_state = col2.text_input("State (optional)")

if st.button("Analyze"):
    if not user_symptoms.strip():
        st.warning("Please enter at least one symptom.")
    else:
        symptoms = [s.strip() for s in user_symptoms.split(",")]
        diseases = predict_disease(symptoms)

        for disease in diseases:
            st.subheader(f"🧾 Possible Condition: **{disease}**")
            doctor = recommend_doctor(disease, user_city, user_state)
            if doctor is not None:
                st.success(f"👨‍⚕️ Recommended {disease_to_specialty.get(disease)}:")
                st.write(f"**Doctor:** {doctor['Doctor_Name']}")
                st.write(f"**Clinic:** {doctor['Clinic_Name']}")
                st.write(f"**Address:** {doctor['Clinic_Address']}, {doctor['Clinic_City']}, {doctor['Clinic_State']}")
            else:
                st.info(f"No doctors found for **{disease}** in this location. Try removing city/state filters.")
