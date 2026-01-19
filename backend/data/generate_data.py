
import pandas as pd
import random
import os

# Define the data mapping
# Disease -> {Symptoms, Tests}
DISEASE_DATA = {
    "Viral Fever": {
        "symptoms": ["measured high fever", "chills", "fatigue", "weakness", "headache", "body ache", "loss of appetite"],
        "tests": [
            {"test_name": "Complete Blood Count (CBC)", "cost": 500, "reason": "Check for infection markers", "importance": "High"},
            {"test_name": "Urine Routine", "cost": 400, "reason": "Screen for UTI", "importance": "Medium"}
        ]
    },
    "Dengue": {
        "symptoms": ["sudden high fever", "severe headache", "pain behind eyes", "severe joint and muscle pain", "fatigue", "nausea", "vomiting", "skin rash", "mild bleeding"],
        "tests": [
            {"test_name": "Dengue NS1 Antigen", "cost": 1200, "reason": "Detect early Dengue infection", "importance": "High"},
            {"test_name": "Complete Blood Count (CBC)", "cost": 500, "reason": "Monitor platelet count", "importance": "High"},
             {"test_name": "Dengue IgM/IgG", "cost": 1000, "reason": "Check for antibodies", "importance": "Medium"}
        ]
    },
    "Malaria": {
        "symptoms": ["fever with shaking chills", "sweating", "headache", "nausea", "vomiting", "abdominal pain", "diarrhea", "anemia", "muscle pain"],
        "tests": [
            {"test_name": "Malaria Parasite (MP) Smear", "cost": 300, "reason": "Detect malaria parasites", "importance": "High"},
            {"test_name": "Rapid Malaria Antigen Test", "cost": 600, "reason": "Quick screening for malaria", "importance": "High"},
             {"test_name": "Complete Blood Count (CBC)", "cost": 500, "reason": "Check for anemia and infection", "importance": "Medium"}
        ]
    },
    "Typhoid": {
        "symptoms": ["prolonged fever", "headache", "weakness", "fatigue", "muscle ache", "sweating", "dry cough", "loss of appetite", "weight loss", "abdominal pain", "diarrhea or constipation", "rash"],
        "tests": [
            {"test_name": "Widal Test", "cost": 400, "reason": "Screen for Typhoid antibodies", "importance": "Medium"},
            {"test_name": "Typhoid DNA PCR", "cost": 1500, "reason": "Confirm Typhoid infection", "importance": "High"},
             {"test_name": "Blood Culture", "cost": 1000, "reason": "Definitive diagnosis", "importance": "High"}
        ]
    },
    "Hypothyroidism": {
        "symptoms": ["fatigue", "increased sensitivity to cold", "constipation", "dry skin", "weight gain", "puffy face", "hoarseness", "muscle weakness", "elevated blood cholesterol", "muscle aches", "tenderness and stiffness", "pain, stiffness or swelling in your joints", "heavy or irregular menstrual periods", "thinning hair", "slowed heart rate", "depression", "impaired memory"],
        "tests": [
            {"test_name": "Thyroid Profile (T3, T4, TSH)", "cost": 800, "reason": "Check thyroid hormone levels", "importance": "High"},
            {"test_name": "Anti-TPO Antibody", "cost": 1200, "reason": "Check for autoimmune thyroiditis", "importance": "Medium"}
        ]
    },
     "Diabetes Type 2": {
        "symptoms": ["increased thirst", "frequent urination", "increased hunger", "unintended weight loss", "fatigue", "blurred vision", "slow-healing sores", "frequent infections", "numbness or tingling in the hands or feet", "areas of darkened skin"],
        "tests": [
            {"test_name": "HbA1c", "cost": 700, "reason": "Average blood sugar over 3 months", "importance": "High"},
            {"test_name": "Fasting Blood Sugar (FBS)", "cost": 200, "reason": "Immediate blood sugar check", "importance": "High"},
            {"test_name": "Post Prandial Blood Sugar (PPBS)", "cost": 200, "reason": "Sugar check after meal", "importance": "Medium"},
             {"test_name": "Lipid Profile", "cost": 800, "reason": "Check cholesterol levels", "importance": "Low"}
        ]
    },
    "Anemia": {
        "symptoms": ["fatigue", "weakness", "pale or yellowish skin", "irregular heartbeats", "shortness of breath", "dizziness or lightheadedness", "chest pain", "cold hands and feet", "headache"],
        "tests": [
            {"test_name": "Complete Blood Count (CBC)", "cost": 500, "reason": "Check Hemoglobin levels", "importance": "High"},
            {"test_name": "Iron Studies", "cost": 1500, "reason": "Check iron deficiency", "importance": "High"},
             {"test_name": "Vitamin B12", "cost": 1000, "reason": "Check B12 deficiency", "importance": "Medium"}
        ]
    },
    "Common Cold": {
         "symptoms": ["runny or stuffy nose", "sore throat", "cough", "congestion", "slight body aches", "mild headache", "sneezing", "low-grade fever", "malaise"],
         "tests": [
             {"test_name": "No Tests Required", "cost": 0, "reason": "Self-limiting viral infection", "importance": "Low"}
         ]
    }
}

def generate_symptoms_string(disease_symptoms):
    """
    Randomly select 1 to all symptoms and join them.
    """
    num_symptoms = random.randint(1, len(disease_symptoms))
    selected_symptoms = random.sample(disease_symptoms, num_symptoms)
    return ", ".join(selected_symptoms)

def generate_dataset(num_samples=1000):
    data = []
    
    for _ in range(num_samples):
        # Pick a random disease
        disease = random.choice(list(DISEASE_DATA.keys()))
        info = DISEASE_DATA[disease]
        
        # Generate varied symptoms
        symptoms_text = generate_symptoms_string(info["symptoms"])
        
        # We store the target disease. The tests are derived from the disease during inference/lookup.
        data.append({
            "symptoms": symptoms_text,
            "disease": disease
        })
        
    df = pd.DataFrame(data)
    
    output_path = os.path.join("backend", "data", "symptoms_data.csv")
    df.to_csv(output_path, index=False)
    print(f"Dataset generated at {output_path} with {num_samples} samples.")

if __name__ == "__main__":
    generate_dataset()
