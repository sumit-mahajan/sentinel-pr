"""
RunReviewPipelineUseCase — orchestrates a single review job end-to-end.

Execution order:
  1. Mark job RUNNING
  2. Skip if review already persisted and posted (idempotent retry)
  3. Call IAgentOrchestrator (F-02 implements the real pipeline)
  4. Persist results in DB (F-04)
  5. Post review to GitHub (F-04)
  6. Mark job COMPLETED
  On any exception: increment attempt_count, mark FAILED with error_message.
"""
from uuid import UUID

import structlog

from application.use_cases.persist_review import PersistReviewUseCase
from application.use_cases.post_review_to_github import PostReviewToGithubUseCase
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
        persist_review: PersistReviewUseCase | None = None,
        post_to_github: PostReviewToGithubUseCase | None = None,
    ) -> None:
        self._job_repo = job_repo
        self._orchestrator = orchestrator
        self._persist_review = persist_review
        self._post_to_github = post_to_github

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
            existing_review = None
            if self._persist_review is not None:
                existing_review = await self._persist_review.get_existing(job_id)

            if (
                existing_review is not None
                and existing_review.posted_to_github
            ):
                await self._job_repo.update_status(job_id, JobStatus.COMPLETED)
                await log.ainfo("worker_job_idempotent_complete")
                return True

            if existing_review is None:
                result = await self._orchestrator.run(job_id)
                if self._persist_review is not None:
                    existing_review = await self._persist_review.execute(job, result)
                await log.ainfo(
                    "worker_pipeline_finished",
                    agents_run=[a.value for a in result.agents_run],
                    total_findings=result.total_findings,
                )

            if (
                existing_review is not None
                and self._post_to_github is not None
                and not existing_review.posted_to_github
            ):
                await self._post_to_github.execute(existing_review)

            await self._job_repo.update_status(job_id, JobStatus.COMPLETED)
            await log.ainfo("worker_job_completed")
            return True

        except Exception as exc:  # noqa: BLE001
            error_msg = f"{type(exc).__name__}: {exc}"
            await self._job_repo.update_status(
                job_id, JobStatus.FAILED, error_message=error_msg
            )
            await log.aerror("worker_job_failed", error=error_msg)
            return False
