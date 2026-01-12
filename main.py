import pandas as pd
import random

# Load your dataset
df_doctors = pd.read_csv('indian_doctors_realistic_5000.csv') # Update the path if needed

# 1. Define a mapping of diseases to medical specialties
# This is a simplified example. A real system would be much more comprehensive.
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
    "Lower Back Pain": "Orthopedic Surgeon", # Could also be Physiotherapist
}

# 2. Define symptom-disease rules (a very basic example)
# The logic is: IF user has these symptoms, THEN suggest these possible diseases.
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
    """
    Takes a list of symptoms and returns a list of likely diseases.
    """
    symptoms_list = [s.strip().lower() for s in symptoms_list] # Clean the input
    predicted_diseases = set()
    
    # Check the user's symptoms against our rules
    for rule_symptoms, diseases in symptom_rules.items():
        # If *any* of the symptoms in the rule are in the user's list, suggest the disease.
        # For a stronger match, you could require ALL symptoms in the rule (using `all()`).
        if any(symptom in symptoms_list for symptom in rule_symptoms):
            predicted_diseases.update(diseases)
            
    return list(predicted_diseases) if predicted_diseases else ["Could not determine a specific condition. Please consult a General Physician."]

def recommend_doctor(disease, city=None, state=None):
    """
    Takes a disease name and optional location filters.
    Returns a recommended doctor's details from the dataset.
    """
    try:
        # Find the specialty for the given disease
        specialty = disease_to_specialty.get(disease)
        if not specialty:
            return f"Sorry, no specialist found for '{disease}'. Please consult a General Physician."
        
        # Filter doctors by specialty
        filtered_doctors = df_doctors[df_doctors['Speciality'] == specialty]
        
        # Further filter by location if provided
        if city:
            filtered_doctors = filtered_doctors[filtered_doctors['Clinic_City'].str.lower() == city.lower()]
        if state:
            filtered_doctors = filtered_doctors[filtered_doctors['Clinic_State'].str.lower() == state.lower()]
            
        if filtered_doctors.empty:
            return f"Sorry, no {specialty} found in the specified location for '{disease}'. Try searching without a location filter."
        
        # For demo purposes, pick a random doctor from the filtered list
        recommended_doc = filtered_doctors.sample(n=1).iloc[0]
        
        # Format the result
        result = {
            "Predicted_Disease": disease,
            "Recommended_Speciality": specialty,
            "Doctor_Name": recommended_doc['Doctor_Name'],
            "Clinic_Name": recommended_doc['Clinic_Name'],
            "Clinic_Address": recommended_doc['Clinic_Address'],
            "Clinic_City": recommended_doc['Clinic_City'],
            "Clinic_State": recommended_doc['Clinic_State']
        }
        return result
        
    except Exception as e:
        return f"An error occurred: {e}"

# --- Main Program ---
print("Welcome to the Medical Assistant Prototype!")
print("Please enter your symptoms, separated by commas.")
print("Example: cough, fever, headache\n")

# Get user input
user_symptoms_input = input("Your symptoms: ")
user_symptoms = [s.strip() for s in user_symptoms_input.split(",")]

# Get optional location filter
user_city = input("Enter your city (or press Enter to skip): ").strip()
user_state = input("Enter your state (or press Enter to skip): ").strip()

# Predict the disease
diseases = predict_disease(user_symptoms)

print("\n" + "="*50)
print("ANALYSIS RESULTS:")
print("="*50)

for disease in diseases:
    print(f"\nBased on your symptoms, you may have: {disease}")
    print("Recommended Doctor:")
    
    # Get a doctor recommendation for each predicted disease
    recommendation = recommend_doctor(disease, user_city if user_city else None, user_state if user_state else None)
    
    if isinstance(recommendation, dict):
        for key, value in recommendation.items():
            print(f"  - {key.replace('_', ' ')}: {value}")
    else:
        print(f"  - {recommendation}")