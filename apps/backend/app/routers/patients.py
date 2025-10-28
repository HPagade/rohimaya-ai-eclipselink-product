"""
Patients Router
Handles patient management
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()


@router.post("/")
async def create_patient(db: Session = Depends(get_db)):
    """
    Create a new patient
    """
    return {"message": "Create patient - to be implemented"}


@router.get("/")
async def get_patients(db: Session = Depends(get_db)):
    """
    Get all patients for current user's facility
    """
    return {"message": "Get patients - to be implemented"}


@router.get("/{patient_id}")
async def get_patient(patient_id: int, db: Session = Depends(get_db)):
    """
    Get specific patient by ID
    """
    return {"message": f"Get patient {patient_id} - to be implemented"}


@router.put("/{patient_id}")
async def update_patient(patient_id: int, db: Session = Depends(get_db)):
    """
    Update patient information
    """
    return {"message": f"Update patient {patient_id} - to be implemented"}


@router.delete("/{patient_id}")
async def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    """
    Delete patient (soft delete for HIPAA compliance)
    """
    return {"message": f"Delete patient {patient_id} - to be implemented"}
