
import pandas as pd
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

# Import the dictionary to save it with the model for lookup
# (This assumes generate_data.py is in backend/data/ and this script is in backend/)
# We'll just redefine it or import it. Importing is better but relative imports can be tricky in scripts.
# For simplicity and robustness, I will just redefine the mapping logic or load it if I can.
# Actually, the API needs the mapping of Disease -> Tests.
# So I should save that mapping as well.

DISEASE_DATA = {
    "Viral Fever": {
        "tests": [
            {"test_name": "Complete Blood Count (CBC)", "cost": 500, "reason": "Check for infection markers", "importance": "High"},
            {"test_name": "Urine Routine", "cost": 400, "reason": "Screen for UTI", "importance": "Medium"}
        ]
    },
    "Dengue": {
        "tests": [
            {"test_name": "Dengue NS1 Antigen", "cost": 1200, "reason": "Detect early Dengue infection", "importance": "High"},
            {"test_name": "Complete Blood Count (CBC)", "cost": 500, "reason": "Monitor platelet count", "importance": "High"},
             {"test_name": "Dengue IgM/IgG", "cost": 1000, "reason": "Check for antibodies", "importance": "Medium"}
        ]
    },
    "Malaria": {
        "tests": [
            {"test_name": "Malaria Parasite (MP) Smear", "cost": 300, "reason": "Detect malaria parasites", "importance": "High"},
            {"test_name": "Rapid Malaria Antigen Test", "cost": 600, "reason": "Quick screening for malaria", "importance": "High"},
             {"test_name": "Complete Blood Count (CBC)", "cost": 500, "reason": "Check for anemia and infection", "importance": "Medium"}
        ]
    },
    "Typhoid": {
        "tests": [
            {"test_name": "Widal Test", "cost": 400, "reason": "Screen for Typhoid antibodies", "importance": "Medium"},
            {"test_name": "Typhoid DNA PCR", "cost": 1500, "reason": "Confirm Typhoid infection", "importance": "High"},
             {"test_name": "Blood Culture", "cost": 1000, "reason": "Definitive diagnosis", "importance": "High"}
        ]
    },
    "Hypothyroidism": {
        "tests": [
            {"test_name": "Thyroid Profile (T3, T4, TSH)", "cost": 800, "reason": "Check thyroid hormone levels", "importance": "High"},
            {"test_name": "Anti-TPO Antibody", "cost": 1200, "reason": "Check for autoimmune thyroiditis", "importance": "Medium"}
        ]
    },
     "Diabetes Type 2": {
        "tests": [
            {"test_name": "HbA1c", "cost": 700, "reason": "Average blood sugar over 3 months", "importance": "High"},
            {"test_name": "Fasting Blood Sugar (FBS)", "cost": 200, "reason": "Immediate blood sugar check", "importance": "High"},
            {"test_name": "Post Prandial Blood Sugar (PPBS)", "cost": 200, "reason": "Sugar check after meal", "importance": "Medium"},
             {"test_name": "Lipid Profile", "cost": 800, "reason": "Check cholesterol levels", "importance": "Low"}
        ]
    },
    "Anemia": {
        "tests": [
            {"test_name": "Complete Blood Count (CBC)", "cost": 500, "reason": "Check Hemoglobin levels", "importance": "High"},
            {"test_name": "Iron Studies", "cost": 1500, "reason": "Check iron deficiency", "importance": "High"},
             {"test_name": "Vitamin B12", "cost": 1000, "reason": "Check B12 deficiency", "importance": "Medium"}
        ]
    },
    "Common Cold": {
         "tests": [
             {"test_name": "No Tests Required", "cost": 0, "reason": "Self-limiting viral infection", "importance": "Low"}
         ]
    }
}

def train():
    # Load data
    data_path = os.path.join("backend", "data", "symptoms_data.csv")
    df = pd.read_csv(data_path)
    
    X = df['symptoms']
    y = df['disease']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create Pipeline
    # 1. TF-IDF to convert text to numbers
    # 2. Random Forest to classify
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english')),
        ('clf', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    # Train
    print("Training model...")
    pipeline.fit(X_train, y_train)
    
    # Evaluate
    score = pipeline.score(X_test, y_test)
    print(f"Model Accuracy: {score:.2f}")
    
    # Save Model and Metadata
    model_data = {
        "model": pipeline,
        "disease_mapping": DISEASE_DATA
    }
    
    output_path = os.path.join("backend", "app", "model_data.joblib")
    joblib.dump(model_data, output_path)
    print(f"Model saved to {output_path}")

if __name__ == "__main__":
    train()
