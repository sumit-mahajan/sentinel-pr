"""Domain and application error hierarchy."""


class DomainError(Exception):
    """Base for domain rule violations."""


class EntityNotFoundError(DomainError):
    """Requested entity does not exist."""


class BusinessRuleViolationError(DomainError):
    """Operation violates a business rule."""


class ForbiddenError(DomainError):
    """Authenticated user lacks permission for this resource."""


class ApplicationError(Exception):
    """Base for use-case / orchestration failures."""


class UseCaseError(ApplicationError):
    """Generic use-case failure."""


class InfrastructureError(Exception):
    """Base for wrapped external system errors."""


class DatabaseError(InfrastructureError):
    """Database operation failed."""


class ExternalServiceError(InfrastructureError):
    """External API or service call failed."""
