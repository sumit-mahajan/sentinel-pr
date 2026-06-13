from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Repository:
    id: UUID
    github_id: int
    installation_id: UUID
    owner: str
    name: str
    full_name: str
    default_branch: str
    is_active: bool
    language: str | None
    created_at: datetime
    updated_at: datetime
