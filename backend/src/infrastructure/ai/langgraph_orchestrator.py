"""
LanggraphOrchestrator — implements IAgentOrchestrator using the LangGraph pipeline.

Replaces StubAgentOrchestrator when Gemini API key is configured.
"""
from __future__ import annotations

from uuid import UUID

import structlog

from domain.repositories.i_job_repository import IJobRepository
from domain.services.i_agent_orchestrator import IAgentOrchestrator, OrchestratorResult
from domain.value_objects.agent_type import AgentType
from infrastructure.ai.agents.arch_agent import ArchAgent
from infrastructure.ai.agents.perf_agent import PerfAgent
from infrastructure.ai.agents.security_agent import SecurityAgent
from infrastructure.ai.agents.supervisor_agent import SupervisorAgent
from infrastructure.ai.agents.synthesis_agent import SynthesisAgent
from infrastructure.ai.agents.test_agent import TestAgent
from infrastructure.ai.gemini_client import GeminiClient
from infrastructure.ai.graph.review_graph import build_review_graph
from infrastructure.ai.graph.state import ChangedFile, PRMetadata, ReviewState
from infrastructure.observability.langfuse_client import ILangfuseClient, NoOpLangfuseClient

logger = structlog.get_logger()


class LanggraphOrchestrator(IAgentOrchestrator):
    def __init__(
        self,
        gemini: GeminiClient,
        job_repo: IJobRepository,
        langfuse: ILangfuseClient | None = None,
    ) -> None:
        self._gemini = gemini
        self._job_repo = job_repo
        self._langfuse = langfuse or NoOpLangfuseClient()

        supervisor = SupervisorAgent(gemini)
        security = SecurityAgent(gemini)
        perf = PerfAgent(gemini)
        arch = ArchAgent(gemini)
        test = TestAgent(gemini)
        synthesis = SynthesisAgent(gemini)

        self._graph = build_review_graph(
            supervisor, security, perf, arch, test, synthesis
        ).compile()

    async def run(self, job_id: UUID) -> OrchestratorResult:
        job = await self._job_repo.get_by_id(job_id)
        if job is None:
            raise ValueError(f"Job {job_id} not found")

        log = logger.bind(job_id=str(job_id), pr_number=job.pr_number)
        trace_id = self._langfuse.start_trace("review_pipeline", job_id=job_id)
        await log.ainfo("pipeline_started", trace_id=trace_id)

        initial_state: ReviewState = {
            "job_id": job_id,
            "repository_id": job.repository_id,
            "trace_id": trace_id,
            "pr_metadata": PRMetadata(
                pr_number=job.pr_number,
                title=job.pr_title,
                author=job.pr_author,
                pr_url=job.pr_url,
                base_sha=job.base_sha,
                head_sha=job.head_sha,
                base_branch="main",    # enriched in F-03 from GitHub API
                head_branch="feature", # enriched in F-03 from GitHub API
                changed_files=[],      # enriched in F-03 from GitHub API
            ),
            "context_units": [],       # enriched in F-03 (tree-sitter)
            "raw_diff_chunks": [],     # enriched in F-03 (GitHub diff fetch)
            "rag_chunks": {},          # enriched in F-03 (pgvector)
            "active_agents": [],
            "findings": [],
            "summary": None,
            "synthesis_complete": False,
        }

        final_state: ReviewState = await self._graph.ainvoke(initial_state)  # type: ignore[assignment]

        findings = final_state.get("findings", [])
        agents_run = [
            AgentType(a.value) for a in final_state.get("active_agents", [])
        ]

        self._langfuse.end_trace(trace_id, output={"total_findings": len(findings)})
        await log.ainfo(
            "pipeline_complete",
            findings=len(findings),
            agents_run=[a.value for a in agents_run],
        )

        return OrchestratorResult(
            job_id=job_id,
            agents_run=agents_run,
            total_findings=len(findings),
            langfuse_trace_id=trace_id,
        )
