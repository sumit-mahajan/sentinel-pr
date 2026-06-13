import json
from dataclasses import asdict
from uuid import uuid4

from domain.services.i_queue_client import IQueueClient, QueueMessage


class InMemoryQueueClient(IQueueClient):
    """In-memory queue for tests and local development without Redis."""

    def __init__(self) -> None:
        self.messages: list[QueueMessage] = []

    async def enqueue(self, message: QueueMessage) -> str:
        self.messages.append(message)
        return str(uuid4())

    def dump_messages(self) -> list[dict[str, object]]:
        return [asdict(message) for message in self.messages]

    @staticmethod
    def serialize(message: QueueMessage) -> str:
        payload = {
            "job_type": message.job_type.value,
            "job_id": str(message.job_id) if message.job_id else None,
            "repository_id": str(message.repository_id),
            "head_sha": message.head_sha,
            "pr_number": message.pr_number,
        }
        return json.dumps(payload)
