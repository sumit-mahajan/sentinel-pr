from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ReviewComment:
    """A single line-level comment to attach to a GitHub PR review."""

    file_path: str
    line: int
    body: str
    line_end: int | None = None


@dataclass(frozen=True)
class PostedReviewResult:
    """Outcome of posting a PR review to GitHub."""

    github_review_id: int
    comment_ids: tuple[int, ...]


class IGithubCommentPoster(ABC):
    @abstractmethod
    async def post_pull_request_review(
        self,
        *,
        installation_id: int,
        owner: str,
        repo: str,
        pr_number: int,
        commit_id: str,
        summary_body: str,
        comments: list[ReviewComment],
    ) -> PostedReviewResult:
        """Post a COMMENT-status PR review with optional inline comments."""
