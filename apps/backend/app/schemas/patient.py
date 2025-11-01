"""
Patient Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime


class PatientCreate(BaseModel):
    mrn: str = Field(..., min_length=1, max_length=50)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date
    gender: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    room_number: Optional[str] = None
    admission_date: Optional[date] = None
    primary_diagnosis: Optional[str] = None
    allergies: Optional[str] = None
    code_status: Optional[str] = None


class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    room_number: Optional[str] = None
    admission_date: Optional[date] = None
    discharge_date: Optional[date] = None
    primary_diagnosis: Optional[str] = None
    allergies: Optional[str] = None
    code_status: Optional[str] = None
    status: Optional[str] = None


class PatientResponse(BaseModel):
    id: int
    facility_id: int
    mrn: str
    first_name: str
    last_name: str
    date_of_birth: date
    gender: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    room_number: Optional[str]
    admission_date: Optional[date]
    discharge_date: Optional[date]
    primary_diagnosis: Optional[str]
    allergies: Optional[str]
    code_status: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PatientList(BaseModel):
    patients: List[PatientResponse]
    total: int
    page: int
    page_size: int
