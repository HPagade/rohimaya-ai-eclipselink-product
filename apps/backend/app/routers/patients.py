"""
Patients Router
CRUD operations for patient records
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
import logging

from app.database import get_db
from app.models import User, Patient
from app.schemas import PatientCreate, PatientUpdate, PatientResponse, PatientList
from app.utils.auth import get_current_active_user

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient(
    patient_data: PatientCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new patient
    """
    # Check if patient with same MRN exists in facility
    existing_patient = db.query(Patient).filter(
        Patient.facility_id == current_user.facility_id,
        Patient.mrn == patient_data.mrn,
        Patient.deleted_at.is_(None)
    ).first()

    if existing_patient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Patient with MRN {patient_data.mrn} already exists"
        )

    # Create patient
    new_patient = Patient(
        facility_id=current_user.facility_id,
        **patient_data.dict()
    )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    logger.info(f"Patient {new_patient.id} created by user {current_user.id}")

    return new_patient


@router.get("/", response_model=PatientList)
async def list_patients(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str = Query(None),
    status_filter: str = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    List patients with pagination and filtering
    """
    query = db.query(Patient).filter(
        Patient.facility_id == current_user.facility_id,
        Patient.deleted_at.is_(None)
    )

    # Search filter
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Patient.first_name.ilike(search_term)) |
            (Patient.last_name.ilike(search_term)) |
            (Patient.mrn.ilike(search_term))
        )

    # Status filter
    if status_filter:
        query = query.filter(Patient.status == status_filter)

    # Get total count
    total = query.count()

    # Pagination
    patients = query.order_by(Patient.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return PatientList(
        patients=patients,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(
    patient_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a single patient by ID
    """
    patient = db.query(Patient).filter(
        Patient.id == patient_id,
        Patient.facility_id == current_user.facility_id,
        Patient.deleted_at.is_(None)
    ).first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    return patient


@router.put("/{patient_id}", response_model=PatientResponse)
async def update_patient(
    patient_id: int,
    patient_data: PatientUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update a patient
    """
    patient = db.query(Patient).filter(
        Patient.id == patient_id,
        Patient.facility_id == current_user.facility_id,
        Patient.deleted_at.is_(None)
    ).first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    # Update fields
    update_data = patient_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)

    logger.info(f"Patient {patient_id} updated by user {current_user.id}")

    return patient


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(
    patient_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Soft delete a patient
    """
    patient = db.query(Patient).filter(
        Patient.id == patient_id,
        Patient.facility_id == current_user.facility_id,
        Patient.deleted_at.is_(None)
    ).first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    # Soft delete
    from datetime import datetime
    patient.deleted_at = datetime.utcnow()
    db.commit()

    logger.info(f"Patient {patient_id} deleted by user {current_user.id}")

    return None
