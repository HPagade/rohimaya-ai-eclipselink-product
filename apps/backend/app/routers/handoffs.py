"""
Handoffs Router
Handles clinical handoff creation, retrieval, and the Update-Only Model™
"""
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import time
from datetime import datetime

from app.database import get_db
from app.models.models import Handoff, Patient, User, RewardPoints
from app.schemas.handoff_schemas import HandoffResponse, SBARResponse, CriticalAlertResponse
from app.services.ai_service import ai_service
from app.config import settings

router = APIRouter()


@router.post("/upload", response_model=HandoffResponse)
async def create_handoff(
    audio_file: UploadFile = File(...),
    patient_id: int = Form(...),
    is_baseline: bool = Form(True),
    user_id: int = Form(...),  # TODO: Get from JWT token
    db: Session = Depends(get_db)
):
    """
    Create handoff: Upload audio → Transcribe → Generate SBAR → Save
    """
    # Validate
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Save audio temporarily
    upload_dir = "/tmp/eclipselink_audio"
    os.makedirs(upload_dir, exist_ok=True)
    audio_path = os.path.join(upload_dir, f"{int(time.time())}_{audio_file.filename}")

    with open(audio_path, "wb") as f:
        content = await audio_file.read()
        f.write(content)

    audio_size_bytes = len(content)

    try:
        # Step 1: Transcribe
        transcription_result = await ai_service.transcribe_audio(audio_path)

        # Step 2: Find baseline if update
        baseline_handoff_id = None
        if not is_baseline:
            baseline = db.query(Handoff).filter(
                Handoff.patient_id == patient_id,
                Handoff.is_baseline == True
            ).order_by(Handoff.created_at.desc()).first()
            if baseline:
                baseline_handoff_id = baseline.id

        # Step 3: Generate SBAR
        patient_context = {
            "name": f"{patient.first_name} {patient.last_name}",
            "age": (datetime.now().date() - patient.date_of_birth).days // 365 if patient.date_of_birth else None,
            "diagnosis": patient.primary_diagnosis,
            "room": patient.room_number
        }

        sbar_result = await ai_service.generate_sbar(
            transcript=transcription_result["text"],
            patient_context=patient_context,
            user_role=user.role,
            is_baseline=is_baseline
        )

        # Step 4: Detect critical alerts
        critical_alert = await ai_service.detect_critical_alerts(
            transcript=transcription_result["text"],
            sbar=sbar_result
        )

        # Step 5: Save handoff
        handoff = Handoff(
            facility_id=user.facility_id,
            patient_id=patient_id,
            created_by_user_id=user_id,
            is_baseline=is_baseline,
            baseline_handoff_id=baseline_handoff_id,
            audio_file_url=audio_path,
            audio_duration_seconds=transcription_result.get("duration_seconds"),
            audio_file_size_bytes=audio_size_bytes,
            transcript_text=transcription_result["text"],
            transcript_confidence=transcription_result.get("confidence"),
            transcribed_at=datetime.now(),
            sbar_situation=sbar_result["situation"],
            sbar_background=sbar_result["background"],
            sbar_assessment=sbar_result["assessment"],
            sbar_recommendation=sbar_result["recommendation"],
            ai_processing_time_ms=sbar_result.get("processing_time_ms"),
            ai_processed_at=datetime.now(),
            has_critical_alert=bool(critical_alert),
            critical_alert_type=critical_alert["alert_type"] if critical_alert else None,
            critical_alert_confidence=critical_alert["confidence"] if critical_alert else None,
            status="completed"
        )

        db.add(handoff)
        db.flush()

        # Step 6: Award points
        points_earned = 0
        if is_baseline:
            points_earned = settings.POINTS_BASELINE_HANDOFF
            action_type = "baseline_handoff"
        else:
            points_earned = settings.POINTS_UPDATE_HANDOFF
            action_type = "update_handoff"

        if critical_alert:
            points_earned += settings.POINTS_CRITICAL_ALERT

        reward = RewardPoints(
            user_id=user_id,
            facility_id=user.facility_id,
            points_earned=points_earned,
            action_type=action_type,
            description=f"Created {'baseline' if is_baseline else 'update'} handoff",
            handoff_id=handoff.id
        )

        db.add(reward)
        db.commit()
        db.refresh(handoff)

        # Return response
        return HandoffResponse(
            id=handoff.id,
            patient_id=handoff.patient_id,
            created_by_user_id=handoff.created_by_user_id,
            is_baseline=handoff.is_baseline,
            baseline_handoff_id=handoff.baseline_handoff_id,
            audio_duration_seconds=handoff.audio_duration_seconds,
            transcript_text=handoff.transcript_text,
            transcript_confidence=float(handoff.transcript_confidence) if handoff.transcript_confidence else None,
            sbar=SBARResponse(
                situation=handoff.sbar_situation,
                background=handoff.sbar_background,
                assessment=handoff.sbar_assessment,
                recommendation=handoff.sbar_recommendation
            ),
            critical_alert=CriticalAlertResponse(**critical_alert) if critical_alert else None,
            status=handoff.status,
            points_earned=points_earned,
            created_at=handoff.created_at,
            ai_processed_at=handoff.ai_processed_at
        )

    finally:
        # Cleanup
        if os.path.exists(audio_path):
            os.remove(audio_path)


@router.get("/", response_model=List[HandoffResponse])
async def get_handoffs(
    limit: int = 50,
    patient_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Get all handoffs
    """
    query = db.query(Handoff)
    if patient_id:
        query = query.filter(Handoff.patient_id == patient_id)

    handoffs = query.order_by(Handoff.created_at.desc()).limit(limit).all()

    return [
        HandoffResponse(
            id=h.id,
            patient_id=h.patient_id,
            created_by_user_id=h.created_by_user_id,
            is_baseline=h.is_baseline,
            baseline_handoff_id=h.baseline_handoff_id,
            audio_duration_seconds=h.audio_duration_seconds,
            transcript_text=h.transcript_text,
            transcript_confidence=float(h.transcript_confidence) if h.transcript_confidence else None,
            sbar=SBARResponse(
                situation=h.sbar_situation or "",
                background=h.sbar_background or "",
                assessment=h.sbar_assessment or "",
                recommendation=h.sbar_recommendation or ""
            ) if h.sbar_situation else None,
            critical_alert=None,
            status=h.status,
            points_earned=0,
            created_at=h.created_at,
            ai_processed_at=h.ai_processed_at
        )
        for h in handoffs
    ]


@router.get("/{handoff_id}", response_model=HandoffResponse)
async def get_handoff(handoff_id: int, db: Session = Depends(get_db)):
    """
    Get specific handoff
    """
    handoff = db.query(Handoff).filter(Handoff.id == handoff_id).first()
    if not handoff:
        raise HTTPException(status_code=404, detail="Handoff not found")

    return HandoffResponse(
        id=handoff.id,
        patient_id=handoff.patient_id,
        created_by_user_id=handoff.created_by_user_id,
        is_baseline=handoff.is_baseline,
        baseline_handoff_id=handoff.baseline_handoff_id,
        audio_duration_seconds=handoff.audio_duration_seconds,
        transcript_text=handoff.transcript_text,
        transcript_confidence=float(handoff.transcript_confidence) if handoff.transcript_confidence else None,
        sbar=SBARResponse(
            situation=handoff.sbar_situation or "",
            background=handoff.sbar_background or "",
            assessment=handoff.sbar_assessment or "",
            recommendation=handoff.sbar_recommendation or ""
        ),
        critical_alert=None,
        status=handoff.status,
        points_earned=0,
        created_at=handoff.created_at,
        ai_processed_at=handoff.ai_processed_at
    )
