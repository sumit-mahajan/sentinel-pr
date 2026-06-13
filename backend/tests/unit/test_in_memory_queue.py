from uuid import uuid4

import pytest

from domain.services.i_queue_client import QueueMessage
from domain.value_objects.job_type import JobType
from infrastructure.queue.in_memory_queue_client import InMemoryQueueClient


@pytest.mark.asyncio
async def test_in_memory_queue_enqueue_and_serialize() -> None:
    queue = InMemoryQueueClient()
    message = QueueMessage(
        job_type=JobType.REVIEW,
        job_id=uuid4(),
        repository_id=uuid4(),
        head_sha="d" * 40,
        pr_number=7,
    )

    message_id = await queue.enqueue(message)
    assert message_id
    assert len(queue.messages) == 1

    serialized = InMemoryQueueClient.serialize(message)
    assert '"job_type": "review"' in serialized
