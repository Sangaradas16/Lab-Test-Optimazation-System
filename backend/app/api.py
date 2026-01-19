from fastapi import APIRouter
from app.models import PatientData, OptimizationResult, TestRecommendation
import random
import joblib
import os

model_pipeline = None
disease_mapping = None
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model_data.joblib")

router = APIRouter()

@router.post("/analyze", response_model=OptimizationResult)
async def analyze_patient(data: PatientData):
    # Load Model (In production, load this once at startup, but for now we load here or at module level)
    # Better to load at module level if possible, but let's do it lazily or check if loaded.
    # For simplicity in this script, we'll load it here or at top level. 
    # Let's use a global variable pattern or lru_cache for better practice if we can modify imports, 
    # but to keep it simple and effective in this single file context:
    
    global model_pipeline
    global disease_mapping
    
    if model_pipeline is None:
        try:
            model_data = joblib.load(MODEL_PATH)
            model_pipeline = model_data["model"]
            disease_mapping = model_data["disease_mapping"]
        except Exception as e:
            # Fallback if model load fails (e.g. during dev)
            print(f"Error loading model: {e}")
            return OptimizationResult(
                recommended_tests=[],
                predicted_diseases=["Error loading model"],
                total_cost=0,
                savings=0,
                confidence_score=0
            )

    symptoms_text = ", ".join(data.symptoms)
    
    # Predict Disease
    # The model expects a list of strings
    predicted_disease_arr = model_pipeline.predict([symptoms_text])
    predicted_disease = predicted_disease_arr[0]
    
    # Get Confidence (probability of the predicted class)
    predicted_proba_arr = model_pipeline.predict_proba([symptoms_text])
    confidence_score = float(max(predicted_proba_arr[0])) # Take the max probability
    
    # Get Recommendations
    disease_info = disease_mapping.get(predicted_disease, {})
    raw_tests = disease_info.get("tests", [])
    
    recommended_tests = []
    for t in raw_tests:
        recommended_tests.append(TestRecommendation(
            test_name=t["test_name"],
            reason=t["reason"],
            cost=t["cost"],
            importance=t["importance"]
        ))
        
    # Calculate costs
    total_cost = sum(t.cost for t in recommended_tests)
    traditional_cost = total_cost * 2.86 # Mock savings ratio
    savings = traditional_cost - total_cost

    return OptimizationResult(
        recommended_tests=recommended_tests,
        predicted_diseases=[predicted_disease],
        total_cost=total_cost,
        savings=savings,
        confidence_score=confidence_score
    )
