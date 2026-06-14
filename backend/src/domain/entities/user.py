from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class User:
    id: UUID
    github_id: int
    login: str
    email: str | None
    avatar_url: str | None
    created_at: datetime
    updated_at: datetime
