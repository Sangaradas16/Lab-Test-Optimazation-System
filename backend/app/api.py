from fastapi import APIRouter
from app.models import PatientData, OptimizationResult, TestRecommendation
import random

router = APIRouter()

@router.post("/analyze", response_model=OptimizationResult)
async def analyze_patient(data: PatientData):
    # Mock Logic for Initial Prototype
    # In a real scenario, this would call the ML model
    
    symptoms_str = ", ".join(data.symptoms).lower()
    
    recommended_tests = []
    predicted_diseases = []
    
    # Basic Rule-based Mocking
    if "fever" in symptoms_str:
        predicted_diseases.append("Viral Fever")
        predicted_diseases.append("Dengue")
        recommended_tests.append(TestRecommendation(
            test_name="Complete Blood Count (CBC)",
            reason="To check for infection markers and platelet count.",
            cost=500.0,
            importance="High"
        ))
        recommended_tests.append(TestRecommendation(
            test_name="Urine Routine",
            reason="To screen for urinary tract infections common with fever.",
            cost=400.0,
            importance="Medium"
        ))
        if "joint pain" in symptoms_str:
            predicted_diseases.append("Chikungunya")
            recommended_tests.append(TestRecommendation(
                test_name="Dengue NS1 Antigen",
                reason="Specific test for Dengue fever given joint pain.",
                cost=1200.0,
                importance="High"
            ))

    if "fatigue" in symptoms_str:
        recommended_tests.append(TestRecommendation(
            test_name="Thyroid Profile",
            reason="Fatigue is a common symptom of Thyroid issues.",
            cost=800.0,
            importance="Medium"
        ))
        recommended_tests.append(TestRecommendation(
            test_name="Vitamin B12 & D",
            reason="Deficiencies can cause chronic fatigue.",
            cost=1500.0,
            importance="Low"
        ))

    # Calculate costs
    total_cost = sum(t.cost for t in recommended_tests)
    # Mock savings comparison (vs traditional approach)
    traditional_cost = total_cost * 2.86 # Approx 65% savings logic 
    savings = traditional_cost - total_cost

    return OptimizationResult(
        recommended_tests=recommended_tests,
        predicted_diseases=predicted_diseases,
        total_cost=total_cost,
        savings=savings,
        confidence_score=0.85
    )
