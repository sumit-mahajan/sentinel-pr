from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from domain.value_objects.agent_type import AgentType
from domain.value_objects.severity import Severity


@dataclass
class Finding:
    id: UUID
    review_id: UUID
    severity: Severity
    category: str  # security | perf | arch | test
    agent_source: str
    file_path: str
    line_start: int | None
    line_end: int | None
    title: str
    description: str
    fix_suggestion: str | None
    github_comment_id: int | None
    created_at: datetime


@dataclass
class Review:
    id: UUID
    job_id: UUID
    repository_id: UUID
    pr_number: int
    head_sha: str
    pr_url: str
    summary: str | None
    total_findings: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    info_count: int
    agents_run: list[AgentType]
    langfuse_trace_id: str | None
    posted_to_github: bool
    created_at: datetime
    updated_at: datetime
    findings: list[Finding] = field(default_factory=list)
