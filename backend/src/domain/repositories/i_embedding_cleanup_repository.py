from abc import ABC, abstractmethod
from uuid import UUID


class IEmbeddingCleanupRepository(ABC):
    @abstractmethod
    async def delete_by_repo_and_sha(self, repository_id: UUID, commit_sha: str) -> int:
        """Delete all embeddings for a (repository_id, commit_sha) pair.

        Returns the number of rows deleted.
        """

    @abstractmethod
    async def delete_older_than_days(self, days: int) -> int:
        """Delete embeddings created more than ``days`` days ago.

        Used by the weekly background cleanup job. Returns rows deleted.
        """
