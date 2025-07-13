from fastapi import APIRouter, File, UploadFile, Form, Depends, HTTPException, status
from typing import Optional, List
from models.schemas import ClinicalContext, ProcessingResult
from services.ai_orchestrator import AIOrchestrator
from services.storage_service import StorageService
from utils.security import get_current_user # Para autenticación

router = APIRouter()
orchestrator = AIOrchestrator()
storage_service = StorageService()

@router.post("/process_clinical_data", response_model=ProcessingResult)
async def process_clinical_data_endpoint(
    ecg_file: Optional[UploadFile] = File(None, description="Archivo de ECG"),
    image_file: Optional[UploadFile] = File(None, description="Archivo de imagen médica"),
    clinical_context_json: str = Form(..., description="Contexto clínico en formato JSON"),
    current_user: dict = Depends(get_current_user) # Protege el endpoint
):
    """
    Recibe archivos médicos y contexto clínico, los procesa con IA y devuelve los resultados.
    """
    if not ecg_file and not image_file:
        raise HTTPException(status_code=400, detail="Al menos un archivo (ECG o imagen) es requerido.")

    try:
        # 1. Parsear el contexto clínico
        clinical_context = ClinicalContext.parse_raw(clinical_context_json)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid clinical context JSON: {e}")

    ecg_file_path = None
    image_file_path = None

    # 2. Subir archivos a un almacenamiento seguro
    # En producción, estos archivos serían anonimizados/pseudoanonimizados antes de ser subidos.
    # El path devuelto es una referencia interna o URL segura.
    if ecg_file:
        filename = f"ecg_{clinical_context.patient_id}_{ecg_file.filename}"
        ecg_file_path = await storage_service.upload_file(await ecg_file.read(), filename)

    if image_file:
        filename = f"image_{clinical_context.patient_id}_{image_file.filename}"
        image_file_path = await storage_service.upload_file(await image_file.read(), filename)

    # 3. Orquestar el procesamiento con IA
    try:
        processing_result = await orchestrator.process_medical_data(
            ecg_file_path=ecg_file_path,
            image_file_path=image_file_path,
            clinical_context=clinical_context
        )
        return processing_result
    except Exception as e:
        # Log del error y devolver un mensaje genérico al cliente por seguridad
        print(f"Error durante el procesamiento: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error processing clinical data.")

@router.post("/token")
async def login_for_access_token(user_id: str = Form(...)):
    """
    Endpoint para generar un token de acceso.
    En una aplicación real, esto implicaría verificar credenciales de usuario.
    """
    # Esto es un placeholder. En un sistema real, verificarías usuario/contraseña
    # y si son válidos, crearías el token.
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user_id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}