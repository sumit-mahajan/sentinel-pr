from datetime import UTC, datetime, timedelta
from uuid import UUID

from jose import JWTError, jwt

from domain.errors import DomainError
from domain.services.i_jwt_service import IJwtService, JwtPayload


class JwtService(IJwtService):
    def __init__(
        self,
        *,
        secret: str,
        algorithm: str = "HS256",
        expire_days: int = 7,
    ) -> None:
        self._secret = secret
        self._algorithm = algorithm
        self._expire_days = expire_days

    def create_token(self, *, user_id: UUID, github_id: int, login: str) -> str:
        now = datetime.now(UTC)
        payload = {
            "sub": str(user_id),
            "github_id": github_id,
            "login": login,
            "iat": now,
            "exp": now + timedelta(days=self._expire_days),
        }
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)

    def decode_token(self, token: str) -> JwtPayload:
        try:
            data = jwt.decode(token, self._secret, algorithms=[self._algorithm])
            return JwtPayload(
                sub=UUID(str(data["sub"])),
                github_id=int(data["github_id"]),
                login=str(data["login"]),
            )
        except (JWTError, KeyError, ValueError) as exc:
            raise DomainError("Invalid or expired session token") from exc
