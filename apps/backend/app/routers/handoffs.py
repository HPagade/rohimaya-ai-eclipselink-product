"""
Handoffs Router
CRUD operations for clinical handoffs with SBAR reports
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
import logging
from datetime import datetime

from app.database import get_db
from app.models import User, Handoff, Patient
from app.schemas import HandoffCreate, HandoffUpdate, HandoffResponse, HandoffList
from app.utils.auth import get_current_active_user

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=HandoffResponse, status_code=status.HTTP_201_CREATED)
async def create_handoff(
    handoff_data: HandoffCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new handoff
    """
    # Verify patient exists and belongs to user's facility
    patient = db.query(Patient).filter(
        Patient.id == handoff_data.patient_id,
        Patient.facility_id == current_user.facility_id,
        Patient.deleted_at.is_(None)
    ).first()

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    # Create handoff
    new_handoff = Handoff(
        facility_id=current_user.facility_id,
        created_by_id=current_user.id,
        **handoff_data.dict()
    )
    db.add(new_handoff)
    db.commit()
    db.refresh(new_handoff)

    logger.info(f"Handoff {new_handoff.id} created by user {current_user.id}")

    # Build response with related data
    response = HandoffResponse.from_orm(new_handoff)
    response.patient_name = f"{patient.first_name} {patient.last_name}"
    response.created_by_name = f"{current_user.first_name} {current_user.last_name}"

    if new_handoff.assigned_to_id:
        assigned_to = db.query(User).filter(User.id == new_handoff.assigned_to_id).first()
        if assigned_to:
            response.assigned_to_name = f"{assigned_to.first_name} {assigned_to.last_name}"

    return response


@router.get("/", response_model=HandoffList)
async def list_handoffs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    patient_id: int = Query(None),
    status_filter: str = Query(None),
    priority: str = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    List handoffs with pagination and filtering
    """
    query = db.query(Handoff).filter(
        Handoff.facility_id == current_user.facility_id,
        Handoff.deleted_at.is_(None)
    )

    # Patient filter
    if patient_id:
        query = query.filter(Handoff.patient_id == patient_id)

    # Status filter
    if status_filter:
        query = query.filter(Handoff.status == status_filter)

    # Priority filter
    if priority:
        query = query.filter(Handoff.priority == priority)

    # Get total count
    total = query.count()

    # Pagination
    handoffs = query.order_by(Handoff.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    # Build responses with related data
    handoff_responses = []
    for handoff in handoffs:
        response = HandoffResponse.from_orm(handoff)

        # Get patient name
        patient = db.query(Patient).filter(Patient.id == handoff.patient_id).first()
        if patient:
            response.patient_name = f"{patient.first_name} {patient.last_name}"

        # Get creator name
        creator = db.query(User).filter(User.id == handoff.created_by_id).first()
        if creator:
            response.created_by_name = f"{creator.first_name} {creator.last_name}"

        # Get assigned to name
        if handoff.assigned_to_id:
            assigned_to = db.query(User).filter(User.id == handoff.assigned_to_id).first()
            if assigned_to:
                response.assigned_to_name = f"{assigned_to.first_name} {assigned_to.last_name}"

        handoff_responses.append(response)

    return HandoffList(
        handoffs=handoff_responses,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{handoff_id}", response_model=HandoffResponse)
async def get_handoff(
    handoff_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a single handoff by ID
    """
    handoff = db.query(Handoff).filter(
        Handoff.id == handoff_id,
        Handoff.facility_id == current_user.facility_id,
        Handoff.deleted_at.is_(None)
    ).first()

    if not handoff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Handoff not found"
        )

    # Build response with related data
    response = HandoffResponse.from_orm(handoff)

    patient = db.query(Patient).filter(Patient.id == handoff.patient_id).first()
    if patient:
        response.patient_name = f"{patient.first_name} {patient.last_name}"

    creator = db.query(User).filter(User.id == handoff.created_by_id).first()
    if creator:
        response.created_by_name = f"{creator.first_name} {creator.last_name}"

    if handoff.assigned_to_id:
        assigned_to = db.query(User).filter(User.id == handoff.assigned_to_id).first()
        if assigned_to:
            response.assigned_to_name = f"{assigned_to.first_name} {assigned_to.last_name}"

    return response


@router.put("/{handoff_id}", response_model=HandoffResponse)
async def update_handoff(
    handoff_id: int,
    handoff_data: HandoffUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update a handoff
    """
    handoff = db.query(Handoff).filter(
        Handoff.id == handoff_id,
        Handoff.facility_id == current_user.facility_id,
        Handoff.deleted_at.is_(None)
    ).first()

    if not handoff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Handoff not found"
        )

    # Update fields
    update_data = handoff_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(handoff, field, value)

    # Update submitted_at if status changed to submitted
    if handoff_data.status == "submitted" and not handoff.submitted_at:
        handoff.submitted_at = datetime.utcnow()

    db.commit()
    db.refresh(handoff)

    logger.info(f"Handoff {handoff_id} updated by user {current_user.id}")

    # Build response with related data
    response = HandoffResponse.from_orm(handoff)

    patient = db.query(Patient).filter(Patient.id == handoff.patient_id).first()
    if patient:
        response.patient_name = f"{patient.first_name} {patient.last_name}"

    creator = db.query(User).filter(User.id == handoff.created_by_id).first()
    if creator:
        response.created_by_name = f"{creator.first_name} {creator.last_name}"

    if handoff.assigned_to_id:
        assigned_to = db.query(User).filter(User.id == handoff.assigned_to_id).first()
        if assigned_to:
            response.assigned_to_name = f"{assigned_to.first_name} {assigned_to.last_name}"

    return response


@router.delete("/{handoff_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_handoff(
    handoff_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Soft delete a handoff
    """
    handoff = db.query(Handoff).filter(
        Handoff.id == handoff_id,
        Handoff.facility_id == current_user.facility_id,
        Handoff.deleted_at.is_(None)
    ).first()

    if not handoff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Handoff not found"
        )

    # Soft delete
    handoff.deleted_at = datetime.utcnow()
    db.commit()

    logger.info(f"Handoff {handoff_id} deleted by user {current_user.id}")

    return None


@router.post("/{handoff_id}/submit", response_model=HandoffResponse)
async def submit_handoff(
    handoff_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Submit a handoff (change status from draft to submitted)
    """
    handoff = db.query(Handoff).filter(
        Handoff.id == handoff_id,
        Handoff.facility_id == current_user.facility_id,
        Handoff.deleted_at.is_(None)
    ).first()

    if not handoff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Handoff not found"
        )

    if handoff.status != "draft":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only draft handoffs can be submitted"
        )

    handoff.status = "submitted"
    handoff.submitted_at = datetime.utcnow()
    db.commit()
    db.refresh(handoff)

    logger.info(f"Handoff {handoff_id} submitted by user {current_user.id}")

    # Build response
    response = HandoffResponse.from_orm(handoff)

    patient = db.query(Patient).filter(Patient.id == handoff.patient_id).first()
    if patient:
        response.patient_name = f"{patient.first_name} {patient.last_name}"

    return response
