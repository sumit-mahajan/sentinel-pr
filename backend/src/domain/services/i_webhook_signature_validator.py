from abc import ABC, abstractmethod


class IWebhookSignatureValidator(ABC):
    @abstractmethod
    def validate(self, body: bytes, signature_header: str | None) -> bool:
        """Return True if X-Hub-Signature-256 matches body."""
