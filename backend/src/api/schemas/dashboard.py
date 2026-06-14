from pydantic import BaseModel


class UserDTO(BaseModel):
    id: str
    github_id: int
    login: str
    avatar_url: str | None


class AuthTokenDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserDTO


class AgentConfigDTO(BaseModel):
    repository_id: str
    security_enabled: bool
    perf_enabled: bool
    arch_enabled: bool
    test_enabled: bool
    min_severity: str


class UpdateAgentConfigRequest(BaseModel):
    security_enabled: bool | None = None
    perf_enabled: bool | None = None
    arch_enabled: bool | None = None
    test_enabled: bool | None = None
    min_severity: str | None = None
    is_active: bool | None = None


class RepoDTO(BaseModel):
    id: str
    github_id: int
    full_name: str
    default_branch: str
    is_active: bool
    language: str | None
    agent_config: AgentConfigDTO


class FindingDTO(BaseModel):
    id: str
    severity: str
    category: str
    agent_source: str
    file_path: str
    line_start: int | None
    line_end: int | None
    title: str
    description: str
    fix_suggestion: str | None


class ReviewSummaryDTO(BaseModel):
    id: str
    pr_number: int
    pr_url: str
    head_sha: str
    total_findings: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    info_count: int
    agents_run: list[str]
    posted_to_github: bool
    created_at: str


class ReviewDetailDTO(ReviewSummaryDTO):
    summary: str | None
    langfuse_trace_id: str | None
    findings: list[FindingDTO]


class JobStatusDTO(BaseModel):
    id: str
    pr_number: int
    pr_url: str
    head_sha: str
    status: str
    attempt_count: int
    error_message: str | None
    enqueued_at: str
    started_at: str | None
    completed_at: str | None


class PaginatedResponse(BaseModel):
    items: list[ReviewSummaryDTO]
    total: int
    page: int
    limit: int
    has_next: bool
