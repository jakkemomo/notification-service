"""Модуль с реализацией методов для авторизации пользователей"""

import logging
from datetime import datetime
from functools import lru_cache
from typing import Optional, Set

import aiohttp
from authlib.jose import jwt
from authlib.jose.errors import BadSignatureError, ExpiredTokenError, JoseError
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param

from websocket_service.src.settings import settings

AUTH_DEBUG = settings.auth.debug
DEBUG_USER_ID = settings.auth.debug_user_id
AUTH_URI = settings.auth.get_uri()

logger = logging.getLogger(__name__)

http_bearer = HTTPBearer(auto_error=False)


class AuthorizedUser:
    def __init__(self, token_claims: dict):
        self._id = token_claims["sub"]
        self._roles = token_claims["rls"].keys()
        self._permissions = self._get_permissions(token_claims["rls"])

    @property
    def id(self):
        return self._id

    def _get_permissions(self, roles: dict) -> Set[str]:
        user_permissions = set()
        for role_name in roles:
            user_permissions.update(roles[role_name])
        return user_permissions

    def has_permissions(self, *permissions) -> bool:
        return self._permissions.issuperset(permissions)

    def is_superuser(self) -> bool:
        return "superuser" in self._roles


def _decode_token(token: str, public_key: str):
    """Метод проверки подписи и актуальности токена"""
    try:
        claims = jwt.decode(token, public_key)
    except (BadSignatureError, JoseError):
        return None

    try:
        now = datetime.utcnow().timestamp()
        claims.validate_exp(now)
    except ExpiredTokenError:
        return None

    return claims


@lru_cache()
async def get_public_key() -> Optional[str]:
    async with aiohttp.ClientSession() as session:
        async with session.get(AUTH_URI) as resp:
            if resp.status != 200:
                # Обеспечиваем возможность работы сервиса без авторизации пользователя
                # В случае, если по какой-то причине не удалось получить `public key`
                # от сервера авторизации, просто возвращаем None.
                return None

            body = await resp.json()
            assert (
                body is not None
            ), "Something goes wrong, body must contain `public_key` value"

            return body["public_key"]


async def get_http_user(
    token: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer),
) -> Optional[AuthorizedUser]:
    if AUTH_DEBUG:
        debug_claims = {
            "sub": DEBUG_USER_ID,
            "rls": {},
        }
        return AuthorizedUser(debug_claims)

    if not token:
        return None

    public_key = await get_public_key()
    if not public_key:
        return None

    claims = _decode_token(token.credentials, public_key)
    if not claims:
        return None

    return AuthorizedUser(claims)


def get_token(authorization: str):
    if not authorization:
        return None

    scheme, credentials = get_authorization_scheme_param(authorization)
    if not (scheme and credentials):
        return None

    if scheme.lower() != "bearer":
        return None

    return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)


async def get_websocket_user(
    authorization: str,
) -> Optional[AuthorizedUser]:
    if AUTH_DEBUG:
        debug_claims = {
            "sub": DEBUG_USER_ID,
            "rls": {},
        }
        return AuthorizedUser(debug_claims)

    token = get_token(authorization)
    if not token:
        return None

    public_key = await get_public_key()
    if not public_key:
        return None

    claims = _decode_token(token.credentials, public_key)
    if not claims:
        return None

    return AuthorizedUser(claims)
