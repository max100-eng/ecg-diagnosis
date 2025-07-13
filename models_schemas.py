from pydantic import BaseModel, Field
from typing import List, Optional

class ClinicalContext(BaseModel):
    patient_id: str
    age: int
    gender: str
    symptoms: List[str]
    medical_history: Optional[str] = None
    # Otros campos relevantes para el contexto clínico

class AIResponse(BaseModel):
    model_name: str
    output: dict # La estructura real dependerá del modelo
    status: str = "success"
    error_message: Optional[str] = None

class ProcessingResult(BaseModel):
    deepseek_ecg_analysis: Optional[AIResponse] = None
    gemini_image_analysis: Optional[AIResponse] = None
    medpalm_claude_reasoning: Optional[AIResponse] = None
    gpt4_synthesis: Optional[AIResponse] = None
    heatmap_data: Optional[dict] = None # Si aplica
    reconstruction_3d_data: Optional[dict] = None # Si aplica
    overall_summary: str
    warnings: List[str] = []