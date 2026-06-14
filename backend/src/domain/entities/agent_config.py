from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class AgentConfig:
    id: UUID
    repository_id: UUID
    security_enabled: bool
    perf_enabled: bool
    arch_enabled: bool
    test_enabled: bool
    min_severity: str
    created_at: datetime
    updated_at: datetime
