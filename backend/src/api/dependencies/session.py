from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from domain.services.i_github_oauth_client import IGithubOAuthClient
from domain.services.i_jwt_service import IJwtService
from infrastructure.auth.jwt_service import JwtService
from infrastructure.config.settings import Settings, get_settings
from infrastructure.db.session import create_session_factory
from infrastructure.github.oauth_client import GithubOAuthClient


@lru_cache
def get_session_factory() -> async_sessionmaker[AsyncSession]:
    return create_session_factory(get_settings())


@lru_cache
def get_jwt_service() -> IJwtService:
    settings = get_settings()
    return JwtService(
        secret=settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
        expire_days=settings.jwt_expire_days,
    )


@lru_cache
def get_github_oauth_client() -> IGithubOAuthClient:
    settings = get_settings()
    redirect_uri = f"{settings.frontend_url.rstrip('/')}/callback"
    return GithubOAuthClient(
        client_id=settings.github_client_id,
        client_secret=settings.github_client_secret,
        redirect_uri=redirect_uri,
    )


def get_settings_cached() -> Settings:
    return get_settings()
