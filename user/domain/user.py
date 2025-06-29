from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


@dataclass
class User:
    id: str
    name: str
    email: str
    password: str
    role: UserRole
    memo: str | None
    created_at: datetime
    updated_at: datetime
