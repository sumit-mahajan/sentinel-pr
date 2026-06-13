import hashlib
import hmac

from domain.services.i_webhook_signature_validator import IWebhookSignatureValidator


class GithubWebhookSignatureValidator(IWebhookSignatureValidator):
    def __init__(self, webhook_secret: str) -> None:
        self._secret = webhook_secret.encode()

    def validate(self, body: bytes, signature_header: str | None) -> bool:
        if not signature_header or not signature_header.startswith("sha256="):
            return False

        expected = signature_header.removeprefix("sha256=")
        computed = hmac.new(self._secret, body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(computed, expected)
