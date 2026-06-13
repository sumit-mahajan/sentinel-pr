"""Tests for GithubCommentPoster payload formatting."""
from domain.services.i_github_comment_poster import ReviewComment
from infrastructure.github.comment_poster import _to_github_comment


def test_single_line_comment_payload() -> None:
    payload = _to_github_comment(
        ReviewComment(file_path="a.py", line=10, body="issue")
    )
    assert payload == {
        "path": "a.py",
        "body": "issue",
        "side": "RIGHT",
        "line": 10,
    }


def test_multiline_comment_payload() -> None:
    payload = _to_github_comment(
        ReviewComment(file_path="a.py", line=10, line_end=15, body="issue")
    )
    assert payload["start_line"] == 10
    assert payload["line"] == 15
    assert payload["start_side"] == "RIGHT"
