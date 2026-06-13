import hashlib
import hmac

from infrastructure.github.webhook_signature import GithubWebhookSignatureValidator


def test_validate_accepts_valid_signature() -> None:
    secret = "test-webhook-secret"
    body = b'{"action":"opened"}'
    digest = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    header = f"sha256={digest}"

    validator = GithubWebhookSignatureValidator(webhook_secret=secret)
    assert validator.validate(body, header) is True


def test_validate_rejects_invalid_signature() -> None:
    validator = GithubWebhookSignatureValidator(webhook_secret="secret")
    assert validator.validate(b"{}", "sha256=deadbeef") is False


def test_validate_rejects_missing_header() -> None:
    validator = GithubWebhookSignatureValidator(webhook_secret="secret")
    assert validator.validate(b"{}", None) is False
