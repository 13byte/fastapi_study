from dataclasses import dataclass
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from config import get_settings
from user.domain.user import UserRole

settings = get_settings()

SECRET_KEY = settings.jwt_secret
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


@dataclass
class CurrentUser:
    id: str
    role: UserRole


def create_access_token(
    payload: dict,
    role: UserRole,
    expires_delta: timedelta = timedelta(hours=6),
):
    expire = datetime.now(timezone.utc) + expires_delta
    payload.update({"role": role, "exp": expire})
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> CurrentUser:
    payload = decode_access_token(token)

    user_id = payload.get("user_id")
    role = payload.get("role")

    if not user_id or not role or role != UserRole.USER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return CurrentUser(user_id, UserRole(role))


def get_admin_user(token: Annotated[str, Depends(oauth2_scheme)]) -> CurrentUser:
    payload = decode_access_token(token)

    user_id = payload.get("user_id")
    role = payload.get("role")

    if not role or role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return CurrentUser(user_id, UserRole(role))
