"""
Authentication Service (SOLID Principles)
Single Responsibility: User authentication and authorization
Dependency Inversion: Abstract token management
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from uuid import UUID

from app.config import settings
from app.database import get_db
from app.models import User, UserLogin, UserCreate, UserToken


# ============================================================================
# PASSWORD HASHING (Single Responsibility)
# ============================================================================

class PasswordHasher:
    """Single Responsibility: Password hashing and verification"""

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        """Hash a plain password"""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hash"""
        return self.pwd_context.verify(plain_password, hashed_password)


# ============================================================================
# TOKEN MANAGEMENT (Single Responsibility)
# ============================================================================

class TokenManager:
    """Single Responsibility: JWT token creation and validation"""

    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_access_token(
        self,
        data: dict,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token"""
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def create_refresh_token(
        self,
        data: dict,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT refresh token"""
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_token(self, token: str) -> dict:
        """Decode and validate JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )


# ============================================================================
# AUTHENTICATION SERVICE (Orchestration)
# ============================================================================

class AuthService:
    """
    Single Responsibility: Authentication orchestration
    Dependency Inversion: Uses abstract components
    """

    def __init__(self):
        self.password_hasher = PasswordHasher()
        self.token_manager = TokenManager(
            secret_key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )

    async def register_user(self, user_data: UserCreate, db: Session) -> User:
        """
        Register new user
        Single Responsibility: User creation workflow
        """
        # Check if user exists
        from sqlalchemy import text
        result = db.execute(
            text("SELECT * FROM users WHERE email = :email"),
            {"email": user_data.email}
        )
        if result.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash password
        hashed_password = self.password_hasher.hash_password(user_data.password)

        # Create user
        user_dict = user_data.dict(exclude={"password"})
        user_dict["password_hash"] = hashed_password

        result = db.execute(
            text("""
                INSERT INTO users (
                    email, password_hash, first_name, last_name,
                    profession, license_number, role, is_active
                )
                VALUES (
                    :email, :password_hash, :first_name, :last_name,
                    :profession, :license_number, :role, true
                )
                RETURNING *
            """),
            {
                "email": user_dict["email"],
                "password_hash": user_dict["password_hash"],
                "first_name": user_dict["first_name"],
                "last_name": user_dict["last_name"],
                "profession": user_dict["profession"].value,
                "license_number": user_dict.get("license_number"),
                "role": user_dict["role"].value
            }
        )
        db.commit()

        user_row = result.fetchone()
        return User(
            id=user_row.id,
            email=user_row.email,
            first_name=user_row.first_name,
            last_name=user_row.last_name,
            profession=user_row.profession,
            license_number=user_row.license_number,
            role=user_row.role,
            is_active=user_row.is_active,
            created_at=user_row.created_at,
            updated_at=user_row.updated_at,
            last_login_at=user_row.last_login_at
        )

    async def authenticate_user(self, credentials: UserLogin, db: Session) -> UserToken:
        """
        Authenticate user and generate tokens
        Single Responsibility: Login workflow
        """
        from sqlalchemy import text

        # Get user
        result = db.execute(
            text("SELECT * FROM users WHERE email = :email AND is_active = true"),
            {"email": credentials.email}
        )
        user_row = result.fetchone()

        if not user_row:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        # Verify password
        if not self.password_hasher.verify_password(
            credentials.password,
            user_row.password_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        # Update last login
        db.execute(
            text("UPDATE users SET last_login_at = NOW() WHERE id = :id"),
            {"id": user_row.id}
        )
        db.commit()

        # Create tokens
        token_data = {"sub": str(user_row.id), "email": user_row.email}
        access_token = self.token_manager.create_access_token(token_data)
        refresh_token = self.token_manager.create_refresh_token(token_data)

        # Build user object
        user = User(
            id=user_row.id,
            email=user_row.email,
            first_name=user_row.first_name,
            last_name=user_row.last_name,
            profession=user_row.profession,
            license_number=user_row.license_number,
            role=user_row.role,
            is_active=user_row.is_active,
            created_at=user_row.created_at,
            updated_at=user_row.updated_at,
            last_login_at=datetime.utcnow()
        )

        return UserToken(
            access_token=access_token,
            refresh_token=refresh_token,
            user=user
        )

    async def get_current_user(self, token: str, db: Session) -> User:
        """
        Get current authenticated user from token
        Single Responsibility: Token validation and user retrieval
        """
        from sqlalchemy import text

        payload = self.token_manager.decode_token(token)
        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

        result = db.execute(
            text("SELECT * FROM users WHERE id = :id AND is_active = true"),
            {"id": user_id}
        )
        user_row = result.fetchone()

        if user_row is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        return User(
            id=user_row.id,
            email=user_row.email,
            first_name=user_row.first_name,
            last_name=user_row.last_name,
            profession=user_row.profession,
            license_number=user_row.license_number,
            role=user_row.role,
            is_active=user_row.is_active,
            created_at=user_row.created_at,
            updated_at=user_row.updated_at,
            last_login_at=user_row.last_login_at
        )


# ============================================================================
# DEPENDENCY INJECTION
# ============================================================================

# HTTP Bearer token security
security = HTTPBearer()

# Global auth service instance
auth_service = AuthService()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    FastAPI dependency for getting current user
    Usage: current_user: User = Depends(get_current_user)
    """
    token = credentials.credentials
    return await auth_service.get_current_user(token, db)


async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    FastAPI dependency for admin-only routes
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
