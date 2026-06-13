from dataclasses import dataclass


@dataclass(frozen=True)
class ReviewFinding:
    """Structured finding produced by the agent pipeline."""

    severity: str
    category: str
    agent_source: str
    file_path: str
    line_start: int | None
    line_end: int | None
    title: str
    description: str
    fix_suggestion: str | None
