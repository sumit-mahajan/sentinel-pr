from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.value_objects.job_status import JobStatus


@dataclass
class ReviewJob:
    id: UUID
    repository_id: UUID
    pr_number: int
    pr_title: str
    pr_author: str
    pr_url: str
    base_sha: str
    head_sha: str
    status: JobStatus
    attempt_count: int
    error_message: str | None
    enqueued_at: datetime
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime
