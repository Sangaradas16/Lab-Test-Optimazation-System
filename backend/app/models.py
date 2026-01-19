from pydantic import BaseModel
from typing import List, Optional

class PatientData(BaseModel):
    age: int
    gender: str
    symptoms: List[str]
    history: Optional[str] = None
    vital_signs: Optional[dict] = None

class TestRecommendation(BaseModel):
    test_name: str
    reason: str
    cost: float
    importance: str  # High, Medium, Low

class OptimizationResult(BaseModel):
    recommended_tests: List[TestRecommendation]
    predicted_diseases: List[str]
    total_cost: float
    savings: float
    confidence_score: float
