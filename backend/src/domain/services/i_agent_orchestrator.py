from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from domain.value_objects.agent_type import AgentType


@dataclass(frozen=True)
class OrchestratorResult:
    """Outcome produced by the agent pipeline for one review job."""

    job_id: UUID
    agents_run: list[AgentType]
    total_findings: int
    # Extended fields populated by F-02 (pipeline) and F-07 (observability)
    langfuse_trace_id: str | None = None
    error: str | None = None


class IAgentOrchestrator(ABC):
    @abstractmethod
    async def run(self, job_id: UUID) -> OrchestratorResult:
        """Execute the multi-agent review pipeline for the given job."""
