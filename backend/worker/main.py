"""
Worker process — polls Postgres for pending jobs.

Run:
    python -m worker.main
"""
from __future__ import annotations

import asyncio
import signal

from worker.runtime import WorkerRuntime


async def _main() -> None:
    runtime = WorkerRuntime()
    stop = asyncio.Event()

    async def _shutdown() -> None:
        stop.set()
        await runtime.stop()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, lambda: asyncio.create_task(_shutdown()))
        except NotImplementedError:
            pass

    await runtime.start()
    await stop.wait()


def main() -> None:
    asyncio.run(_main())


if __name__ == "__main__":
    main()
