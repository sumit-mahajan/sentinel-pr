"""
LangfuseClient — thin wrapper around the Langfuse Python SDK.

Provides trace/span lifecycle management used by @trace_agent.
Falls back to a no-op implementation when LANGFUSE_PUBLIC_KEY is not set
so the app works in development without a Langfuse account.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any
from uuid import UUID


@dataclass
class SpanContext:
    trace_id: str
    span_id: str
    name: str
    metadata: dict[str, Any] = field(default_factory=dict)


class ILangfuseClient(ABC):
    @abstractmethod
    def start_trace(self, name: str, job_id: UUID, metadata: dict[str, Any] | None = None) -> str:
        """Open a new top-level trace. Returns the trace ID."""

    @abstractmethod
    def start_span(
        self, trace_id: str, name: str, metadata: dict[str, Any] | None = None
    ) -> SpanContext:
        """Open a child span inside an existing trace."""

    @abstractmethod
    def end_span(
        self,
        ctx: SpanContext,
        *,
        output: dict[str, Any] | None = None,
        error: str | None = None,
    ) -> None:
        """Close a span, optionally recording output or error."""

    @abstractmethod
    def end_trace(self, trace_id: str, *, output: dict[str, Any] | None = None) -> None:
        """Close the top-level trace."""


class NoOpLangfuseClient(ILangfuseClient):
    """Used when Langfuse is not configured (local dev / CI)."""

    def start_trace(self, name: str, job_id: UUID, metadata: dict[str, Any] | None = None) -> str:
        return f"noop-{job_id}"

    def start_span(
        self, trace_id: str, name: str, metadata: dict[str, Any] | None = None
    ) -> SpanContext:
        return SpanContext(trace_id=trace_id, span_id=f"span-{name}", name=name)

    def end_span(
        self,
        ctx: SpanContext,
        *,
        output: dict[str, Any] | None = None,
        error: str | None = None,
    ) -> None:
        pass

    def end_trace(self, trace_id: str, *, output: dict[str, Any] | None = None) -> None:
        pass


class LangfuseClient(ILangfuseClient):
    """Real Langfuse client backed by the langfuse Python SDK."""

    def __init__(self, public_key: str, secret_key: str, host: str) -> None:
        from langfuse import Langfuse  # lazy import — optional dependency

        self._lf = Langfuse(public_key=public_key, secret_key=secret_key, host=host)
        self._traces: dict[str, Any] = {}
        self._spans: dict[str, Any] = {}

    def start_trace(self, name: str, job_id: UUID, metadata: dict[str, Any] | None = None) -> str:
        trace = self._lf.trace(name=name, metadata={"job_id": str(job_id), **(metadata or {})})
        trace_id = trace.id
        self._traces[trace_id] = trace
        return trace_id

    def start_span(
        self, trace_id: str, name: str, metadata: dict[str, Any] | None = None
    ) -> SpanContext:
        trace = self._traces.get(trace_id)
        span = (trace or self._lf).span(name=name, metadata=metadata or {})
        ctx = SpanContext(trace_id=trace_id, span_id=span.id, name=name)
        self._spans[span.id] = span
        return ctx

    def end_span(
        self,
        ctx: SpanContext,
        *,
        output: dict[str, Any] | None = None,
        error: str | None = None,
    ) -> None:
        span = self._spans.pop(ctx.span_id, None)
        if span is not None:
            span.end(output=output, level="ERROR" if error else "DEFAULT", status_message=error)

    def end_trace(self, trace_id: str, *, output: dict[str, Any] | None = None) -> None:
        trace = self._traces.pop(trace_id, None)
        if trace is not None:
            trace.update(output=output)
        self._lf.flush()


def build_langfuse_client(
    public_key: str | None,
    secret_key: str | None,
    host: str = "https://cloud.langfuse.com",
) -> ILangfuseClient:
    """Return a real client when credentials are present, NoOp otherwise."""
    if public_key and secret_key:
        return LangfuseClient(public_key=public_key, secret_key=secret_key, host=host)
    return NoOpLangfuseClient()
