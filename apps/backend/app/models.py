"""
Domain Models (Pydantic Schemas)
Following SOLID Principles:
- Single Responsibility: Each model represents ONE domain concept
- Open/Closed: Use inheritance for extensibility
- Liskov Substitution: Child classes can replace parent classes
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime, date
from enum import Enum
from uuid import UUID


# ============================================================================
# ENUMS: Type-safe constants
# ============================================================================

class UserRole(str, Enum):
    """User roles in the system"""
    CLINICIAN = "clinician"
    ADMIN = "admin"


class Profession(str, Enum):
    """Healthcare professions"""
    RN = "RN"  # Registered Nurse
    LPN = "LPN"  # Licensed Practical Nurse
    CNA = "CNA"  # Certified Nursing Assistant
    MD = "MD"  # Medical Doctor
    DO = "DO"  # Doctor of Osteopathic Medicine
    NP = "NP"  # Nurse Practitioner
    PA = "PA"  # Physician Assistant
    RT = "RT"  # Respiratory Therapist
    PT = "PT"  # Physical Therapist
    OT = "OT"  # Occupational Therapist
    PHARMD = "PharmD"  # Pharmacist
    MSW = "MSW"  # Medical Social Worker
    MA = "MA"  # Medical Assistant
    EMT = "EMT"  # Emergency Medical Technician
    ADMIN = "Admin"  # System Administrator


class ShiftType(str, Enum):
    """Shift types"""
    DAY = "day"
    EVENING = "evening"
    NIGHT = "night"


class HandoffStatus(str, Enum):
    """Handoff workflow status"""
    DRAFT = "draft"
    COMPLETED = "completed"
    ARCHIVED = "archived"


# ============================================================================
# BASE MODELS: Common fields (Liskov Substitution Principle)
# ============================================================================

class TimestampMixin(BaseModel):
    """Single Responsibility: Timestamp tracking"""
    created_at: datetime
    updated_at: datetime


class UUIDMixin(BaseModel):
    """Single Responsibility: UUID identification"""
    id: UUID


# ============================================================================
# USER MODELS
# ============================================================================

class UserBase(BaseModel):
    """Single Responsibility: User core attributes"""
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    profession: Profession
    license_number: Optional[str] = Field(None, max_length=100)
    role: UserRole = UserRole.CLINICIAN


class UserCreate(UserBase):
    """Single Responsibility: User creation data"""
    password: str = Field(..., min_length=12, max_length=128)

    @validator('password')
    def validate_password(cls, v):
        """Validate password strength"""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v):
            raise ValueError('Password must contain at least one special character')
        return v


class UserUpdate(BaseModel):
    """Single Responsibility: User update data"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    profession: Optional[Profession] = None
    license_number: Optional[str] = Field(None, max_length=100)


class User(UUIDMixin, UserBase, TimestampMixin):
    """Single Responsibility: Complete user representation"""
    is_active: bool
    last_login_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    """Single Responsibility: Authentication request"""
    email: EmailStr
    password: str


class UserToken(BaseModel):
    """Single Responsibility: Authentication response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: User


# ============================================================================
# PATIENT MODELS
# ============================================================================

class PatientBase(BaseModel):
    """Single Responsibility: Patient core attributes"""
    mrn: str = Field(..., min_length=1, max_length=50)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date
    gender: Optional[str] = Field(None, max_length=20)
    room_number: Optional[str] = Field(None, max_length=20)
    primary_diagnosis: Optional[str] = None
    code_status: str = Field(default="Full Code", max_length=50)

    @validator('date_of_birth')
    def validate_dob(cls, v):
        """Ensure date of birth is not in the future"""
        if v > date.today():
            raise ValueError('Date of birth cannot be in the future')
        return v


class PatientCreate(PatientBase):
    """Single Responsibility: Patient creation data"""
    admission_date: Optional[datetime] = None


class PatientUpdate(BaseModel):
    """Single Responsibility: Patient update data"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    gender: Optional[str] = Field(None, max_length=20)
    room_number: Optional[str] = Field(None, max_length=20)
    primary_diagnosis: Optional[str] = None
    code_status: Optional[str] = Field(None, max_length=50)
    discharge_date: Optional[datetime] = None


class Patient(UUIDMixin, PatientBase, TimestampMixin):
    """Single Responsibility: Complete patient representation"""
    admission_date: Optional[datetime] = None
    discharge_date: Optional[datetime] = None
    is_active: bool
    created_by: UUID

    class Config:
        orm_mode = True


# ============================================================================
# SBAR MODELS (Open/Closed Principle - extend without modifying)
# ============================================================================

class SBARSituation(BaseModel):
    """Single Responsibility: SBAR Situation component"""
    patient_name: Optional[str] = None
    age: Optional[int] = None
    room: Optional[str] = None
    diagnosis: Optional[str] = None
    chief_complaint: Optional[str] = None


class SBARBackground(BaseModel):
    """Single Responsibility: SBAR Background component"""
    medical_history: Optional[list[str]] = []
    surgical_history: Optional[list[str]] = []
    allergies: Optional[list[str]] = []
    medications: Optional[list[Dict[str, Any]]] = []
    code_status: Optional[str] = None


class SBARAssessment(BaseModel):
    """Single Responsibility: SBAR Assessment component"""
    vital_signs: Optional[Dict[str, Any]] = {}
    labs: Optional[Dict[str, Any]] = {}
    current_condition: Optional[str] = None
    progress: Optional[str] = None
    concerns: Optional[list[str]] = []


class SBARRecommendation(BaseModel):
    """Single Responsibility: SBAR Recommendation component"""
    pending_orders: Optional[list[str]] = []
    follow_up_needed: Optional[list[str]] = []
    escalation_required: bool = False
    next_steps: Optional[str] = None


# ============================================================================
# HANDOFF MODELS
# ============================================================================

class HandoffBase(BaseModel):
    """Single Responsibility: Handoff core attributes"""
    patient_id: UUID
    shift_type: Optional[ShiftType] = None


class HandoffCreate(HandoffBase):
    """Single Responsibility: Handoff creation data"""
    audio_url: Optional[str] = None
    audio_duration_seconds: Optional[int] = Field(None, gt=0)
    audio_file_size_bytes: Optional[int] = Field(None, gt=0)


class HandoffUpdate(BaseModel):
    """Single Responsibility: Handoff update data"""
    transcription: Optional[str] = None
    sbar_situation: Optional[SBARSituation] = None
    sbar_background: Optional[SBARBackground] = None
    sbar_assessment: Optional[SBARAssessment] = None
    sbar_recommendation: Optional[SBARRecommendation] = None
    status: Optional[HandoffStatus] = None


class Handoff(UUIDMixin, HandoffBase, TimestampMixin):
    """Single Responsibility: Complete handoff representation"""
    created_by: UUID
    audio_url: Optional[str] = None
    audio_duration_seconds: Optional[int] = None
    audio_file_size_bytes: Optional[int] = None
    transcription: Optional[str] = None
    transcription_confidence: Optional[float] = None
    sbar_situation: Optional[Dict[str, Any]] = None
    sbar_background: Optional[Dict[str, Any]] = None
    sbar_assessment: Optional[Dict[str, Any]] = None
    sbar_recommendation: Optional[Dict[str, Any]] = None
    status: HandoffStatus
    completed_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class HandoffWithPatient(Handoff):
    """Single Responsibility: Handoff with patient details (Interface Segregation)"""
    patient: Patient


class HandoffWithUser(Handoff):
    """Single Responsibility: Handoff with creator details (Interface Segregation)"""
    creator: User


class HandoffDetailed(Handoff):
    """Single Responsibility: Handoff with all related data"""
    patient: Patient
    creator: User


# ============================================================================
# AI PROCESSING MODELS
# ============================================================================

class TranscriptionRequest(BaseModel):
    """Single Responsibility: Audio transcription request"""
    audio_url: str
    language: str = "en"


class TranscriptionResponse(BaseModel):
    """Single Responsibility: Audio transcription result"""
    text: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    duration_seconds: Optional[int] = None


class SBARGenerationRequest(BaseModel):
    """Single Responsibility: SBAR generation request"""
    transcription: str
    patient_context: Optional[Dict[str, Any]] = None


class SBARGenerationResponse(BaseModel):
    """Single Responsibility: SBAR generation result"""
    situation: SBARSituation
    background: SBARBackground
    assessment: SBARAssessment
    recommendation: SBARRecommendation
    quality_score: Optional[float] = Field(None, ge=0.0, le=1.0)


# ============================================================================
# AUDIT LOG MODELS
# ============================================================================

class AuditLogCreate(BaseModel):
    """Single Responsibility: Audit log creation"""
    user_id: Optional[UUID] = None
    user_email: str
    user_ip_address: Optional[str] = None
    action: str
    resource_type: str
    resource_id: Optional[UUID] = None
    changes: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class AuditLog(UUIDMixin, AuditLogCreate):
    """Single Responsibility: Complete audit log"""
    created_at: datetime

    class Config:
        orm_mode = True


# ============================================================================
# PAGINATION MODELS (Interface Segregation Principle)
# ============================================================================

class PaginationParams(BaseModel):
    """Single Responsibility: Pagination parameters"""
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class PaginatedResponse(BaseModel):
    """Single Responsibility: Paginated response wrapper"""
    items: list[Any]
    total: int
    page: int
    page_size: int
    total_pages: int


# ============================================================================
# API RESPONSE MODELS
# ============================================================================

class SuccessResponse(BaseModel):
    """Single Responsibility: Success response"""
    success: bool = True
    message: str
    data: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Single Responsibility: Error response"""
    success: bool = False
    error: str
    details: Optional[Dict[str, Any]] = None
