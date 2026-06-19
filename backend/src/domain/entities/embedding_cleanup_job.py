from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.value_objects.job_status import JobStatus


@dataclass
class EmbeddingCleanupJob:
    id: UUID
    repository_id: UUID
    head_sha: str
    pr_number: int
    status: JobStatus
    attempt_count: int
    retry_after: datetime | None
    error_message: str | None
    enqueued_at: datetime
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime
