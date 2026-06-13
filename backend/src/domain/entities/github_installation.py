from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class GithubInstallation:
    id: UUID
    installation_id: int
    account_login: str
    account_type: str
    account_avatar_url: str | None
    access_token_encrypted: str | None
    access_token_expires_at: datetime | None
    created_at: datetime
    updated_at: datetime
