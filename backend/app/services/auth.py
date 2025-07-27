"""Authentication service."""

from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from jose import jwt
from jwt import ExpiredSignatureError
from passlib.context import CryptContext
from sqlmodel import Session, select

from app.core.logging import get_logger
from app.core.settings import settings
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logger = get_logger(__name__)


class AuthService:
    """Service for handling authentication-related operations."""

    def __init__(self, session: Session) -> None:
        """Initialize AuthService with a database session."""
        self.session = session

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash password."""
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_seconds: int | None = None) -> str:
        """Create JWT access token."""
        logger.debug("Creating access token with data: %s", data)
        to_encode = data.copy()
        if expires_seconds:
            expire = datetime.now(UTC) + timedelta(seconds=expires_seconds)
        else:
            expire = datetime.now(UTC) + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            )

        to_encode.update({"exp": expire})
        logger.debug("Token expiration time: %s", to_encode["exp"])
        logger.debug("to_encode: %s", to_encode)
        return jwt.encode(
            to_encode,
            settings.AUTH_SECRET.get_secret_value(),
            algorithm=settings.ALGORITHM,
        )

    @staticmethod
    def decode_jwt_token(token: str) -> dict:
        """Decode JWT token."""
        try:
            return jwt.decode(
                token,
                settings.AUTH_SECRET.get_secret_value(),
                algorithms=[settings.ALGORITHM],
            )
        except jwt.JWTError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            ) from exc
        except ExpiredSignatureError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
            ) from exc

    def authenticate_user(self, email: str, password: str) -> User | None:
        """Authenticate user by email."""
        statement = select(User).where(User.email == email)
        result = self.session.exec(statement)
        user = result.first()

        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None

        return user

    # async def create_user(self, user_data: UserCreate) -> User:
    #     """Create a new user."""
    #     # Check if email exists
    #     email_statement = select(User).where(User.email == user_data.email)
    #     email_result = await self.session.exec(email_statement)
    #     if email_result.first():
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail="Email already registered",
    #         )

    #     # Check if username exists
    #     username_statement = select(User).where(User.username == user_data.username)
    #     username_result = await self.session.exec(username_statement)
    #     if username_result.first():
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
    #         )

    #     # Create user
    #     db_user = User(
    #         email=user_data.email,
    #         username=user_data.username,
    #         hashed_password=self.get_password_hash(user_data.password),
    #         first_name=user_data.first_name,
    #         last_name=user_data.last_name,
    #         status=UserStatus.ACTIVE,
    #     )

    #     self.session.add(db_user)
    #     await self.session.commit()
    #     await self.session.refresh(db_user)
    #     return db_user
