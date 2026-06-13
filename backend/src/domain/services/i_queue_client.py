from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from domain.value_objects.job_type import JobType


@dataclass(frozen=True)
class QueueMessage:
    job_type: JobType
    job_id: UUID | None
    repository_id: UUID
    head_sha: str
    pr_number: int | None = None


class IQueueClient(ABC):
    @abstractmethod
    async def enqueue(self, message: QueueMessage) -> str:
        """Push a job message to the queue. Returns stream/message ID."""
