from abc import ABC, abstractmethod
from uuid import UUID


class ICodeEmbeddingStore(ABC):
    """Store and retrieve code chunk embeddings for RAG (F-03)."""

    @abstractmethod
    async def store_file_chunks(
        self,
        *,
        repository_id: UUID,
        commit_sha: str,
        file_path: str,
        chunks: list[dict[str, object]],
        language: str | None = None,
    ) -> int:
        """Upsert parsed code chunks for a file at a commit. Returns chunks stored."""

    @abstractmethod
    async def retrieve_similar(
        self,
        *,
        repository_id: UUID,
        commit_sha: str,
        query_text: str,
        k: int = 5,
        language: str | None = None,
    ) -> list[str]:
        """Return top-k chunk contents by cosine similarity for the given commit."""
