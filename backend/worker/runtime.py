"""Periodic worker runtime — polls Postgres for pending jobs."""

from __future__ import annotations

import asyncio

import structlog

from infrastructure.config.settings import get_settings
from worker.poll import poll_and_process

logger = structlog.get_logger()


class WorkerRuntime:
    def __init__(self) -> None:
        self._running = False
        self._supervisor_task: asyncio.Task[None] | None = None

    async def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._supervisor_task = asyncio.create_task(self._supervisor_loop())
        await logger.ainfo("worker_runtime_started")

    async def stop(self) -> None:
        self._running = False
        if self._supervisor_task is not None:
            await self._supervisor_task
            self._supervisor_task = None
        await logger.ainfo("worker_runtime_stopped")

    async def _supervisor_loop(self) -> None:
        settings = get_settings()
        poll_interval = settings.worker_poll_interval_seconds

        while self._running:
            await logger.ainfo("worker_poll_triggered")
            try:
                processed = await poll_and_process(settings)
                if processed == 0:
                    await logger.ainfo("worker_poll_empty")
            except Exception as exc:  # noqa: BLE001
                await logger.aerror(
                    "worker_poll_error",
                    error=str(exc) or repr(exc),
                    exc_type=type(exc).__name__,
                )
                await asyncio.sleep(1)

            await asyncio.sleep(poll_interval)

        await logger.ainfo("worker_supervisor_exiting")
