import pandas as pd
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "lab_test_dataset.csv")
MODEL_OUTPUT_PATH = os.path.join(BASE_DIR, "app", "model_data.joblib")

def main():
    print("Loading data...")
    if not os.path.exists(DATA_PATH):
        print(f"Error: Data file not found at {DATA_PATH}")
        return

    df = pd.read_csv(DATA_PATH)
    
    X = df["Symptoms"]
    y = df["Disease"]

    print("Training model...")
    # Create a pipeline: Text processing -> Classifier
    model = Pipeline([
        ("tfidf", TfidfVectorizer(stop_words="english")),
        ("clf", RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    model.fit(X, y)
    print("Model trained successfully.")

    # Define Disease Mapping (Tests, Costs, Reasons)
    # This acts as our "Knowledge Base" linked to the predictions
    disease_mapping = {
        "Diabetes": {
            "tests": [
                {"test_name": "HbA1c", "cost": 15.00, "reason": "Measures average blood sugar over 3 months.", "importance": "High"},
                {"test_name": "Fasting Blood Glucose", "cost": 10.00, "reason": "Checks blood sugar levels after fasting.", "importance": "High"},
                {"test_name": "Lipid Profile", "cost": 25.00, "reason": "High blood sugar often correlates with cholesterol issues.", "importance": "Medium"}
            ]
        },
        "Hypertension": {
            "tests": [
                {"test_name": "Lipid Profile", "cost": 25.00, "reason": "Checks for cholesterol levels which affect blood pressure.", "importance": "High"},
                {"test_name": "Kidney Function Test", "cost": 30.00, "reason": "High blood pressure can damage kidneys.", "importance": "Medium"},
                {"test_name": "ECG", "cost": 50.00, "reason": "Checks irregular heart rhythms caused by hypertension.", "importance": "High"}
            ]
        },
        "Anemia": {
            "tests": [
                {"test_name": "Complete Blood Count (CBC)", "cost": 12.00, "reason": "Measures red blood cell count and hemoglobin.", "importance": "High"},
                {"test_name": "Ferritin Test", "cost": 20.00, "reason": "Checks iron stores in the body.", "importance": "High"},
                {"test_name": "Vitamin B12", "cost": 25.00, "reason": "Deficiency can cause anemia.", "importance": "Medium"}
            ]
        },
        "Hypothyroidism": {
            "tests": [
                {"test_name": "TSH", "cost": 15.00, "reason": "Primary screening for thyroid function.", "importance": "High"},
                {"test_name": "Free T4", "cost": 18.00, "reason": "Measures active thyroid hormone.", "importance": "High"},
                {"test_name": "Anti-TPO Antibodies", "cost": 35.00, "reason": "Checks for autoimmune thyroid disease.", "importance": "Medium"}
            ]
        },
        "COVID-19": {
            "tests": [
                {"test_name": "RT-PCR", "cost": 50.00, "reason": "Detects active viral infection.", "importance": "High"},
                {"test_name": "CRP (C-Reactive Protein)", "cost": 15.00, "reason": "Checks for inflammation.", "importance": "Medium"},
                {"test_name": "D-Dimer", "cost": 40.00, "reason": "Checks for blood clotting risks.", "importance": "Medium"}
            ]
        },
        "Arthritis": {
             "tests": [
                {"test_name": "Rheumatoid Factor (RF)", "cost": 20.00, "reason": "Screening for rheumatoid arthritis.", "importance": "High"},
                {"test_name": "Anti-CCP", "cost": 45.00, "reason": "More specific test for rheumatoid arthritis.", "importance": "High"},
                {"test_name": "ESR", "cost": 10.00, "reason": "Measures inflammation in the body.", "importance": "Medium"}
            ]
        },
         "Pneumonia": {
             "tests": [
                {"test_name": "Chest X-Ray", "cost": 40.00, "reason": "Visualizes lung infection.", "importance": "High"},
                {"test_name": "Complete Blood Count (CBC)", "cost": 12.00, "reason": "Checks for signs of infection (white blood cells).", "importance": "High"},
                {"test_name": "Sputum Culture", "cost": 25.00, "reason": "Identifies the specific bacteria causing pneumonia.", "importance": "Medium"}
            ]
        },
        "UTI": {
             "tests": [
                {"test_name": "Urinalysis", "cost": 10.00, "reason": "Checks for bacteria and white blood cells in urine.", "importance": "High"},
                {"test_name": "Urine Culture", "cost": 25.00, "reason": "Identifies specific bacteria and effective antibiotics.", "importance": "High"}
            ]
        }
    }

    # Save Model and Data
    print(f"Saving model to {MODEL_OUTPUT_PATH}...")
    joblib.dump({"model": model, "disease_mapping": disease_mapping}, MODEL_OUTPUT_PATH)
    print("Done!")

if __name__ == "__main__":
    main()
