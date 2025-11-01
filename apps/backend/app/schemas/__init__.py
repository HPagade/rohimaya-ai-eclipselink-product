"""
Pydantic schemas for request/response validation
"""
from .auth import (
    UserRegister,
    UserLogin,
    Token,
    UserResponse,
    PasswordReset,
    PasswordResetConfirm
)
from .handoff import (
    HandoffCreate,
    HandoffUpdate,
    HandoffResponse,
    HandoffList
)
from .patient import (
    PatientCreate,
    PatientUpdate,
    PatientResponse,
    PatientList
)

__all__ = [
    "UserRegister",
    "UserLogin",
    "Token",
    "UserResponse",
    "PasswordReset",
    "PasswordResetConfirm",
    "HandoffCreate",
    "HandoffUpdate",
    "HandoffResponse",
    "HandoffList",
    "PatientCreate",
    "PatientUpdate",
    "PatientResponse",
    "PatientList",
]
