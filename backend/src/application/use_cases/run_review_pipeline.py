"""
RunReviewPipelineUseCase — orchestrates a single review job end-to-end.

Execution order:
  1. Mark job RUNNING
  2. Call IAgentOrchestrator (F-02 implements the real pipeline)
  3. Persist results in DB (F-07 adds Langfuse trace fields)
  4. Mark job COMPLETED
  On any exception: increment attempt_count, mark FAILED with error_message.
"""
from uuid import UUID

import structlog

from domain.errors import ApplicationError
from domain.repositories.i_job_repository import IJobRepository
from domain.services.i_agent_orchestrator import IAgentOrchestrator
from domain.value_objects.job_status import JobStatus

logger = structlog.get_logger()

MAX_ATTEMPTS = 3


class RunReviewPipelineUseCase:
    def __init__(
        self,
        job_repo: IJobRepository,
        orchestrator: IAgentOrchestrator,
    ) -> None:
        self._job_repo = job_repo
        self._orchestrator = orchestrator

    async def execute(self, job_id: UUID) -> bool:
        """Run the pipeline for the given job.

        Returns True if the job completed, False if it should be retried later.
        Raises ApplicationError if the job has exceeded MAX_ATTEMPTS.
        """
        job = await self._job_repo.get_by_id(job_id)
        if job is None:
            await logger.awarning("worker_job_not_found", job_id=str(job_id))
            return True  # Nothing to do; ack the message.

        log = logger.bind(
            job_id=str(job_id),
            pr_number=job.pr_number,
            attempt=job.attempt_count + 1,
        )

        if job.attempt_count >= MAX_ATTEMPTS:
            raise ApplicationError(
                f"Job {job_id} has already reached the maximum of {MAX_ATTEMPTS} attempts"
            )

        # Bump attempt count and mark running.
        await self._job_repo.update_attempt_count(job_id, job.attempt_count + 1)
        await self._job_repo.update_status(job_id, JobStatus.RUNNING)
        await log.ainfo("worker_job_started")

        try:
            result = await self._orchestrator.run(job_id)
            await self._job_repo.update_status(job_id, JobStatus.COMPLETED)
            await log.ainfo(
                "worker_job_completed",
                agents_run=[a.value for a in result.agents_run],
                total_findings=result.total_findings,
            )
            return True

        except Exception as exc:  # noqa: BLE001
            error_msg = f"{type(exc).__name__}: {exc}"
            await self._job_repo.update_status(
                job_id, JobStatus.FAILED, error_message=error_msg
            )
            await log.aerror("worker_job_failed", error=error_msg)
            return False
