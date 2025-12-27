from __future__ import annotations

from functools import lru_cache

# local imports
from src.services.auth_service import AuthService
from src.services.chat_service import ChatService
from src.repository.user_repository import UserRepository
from src.settings import setting


@lru_cache(maxsize=1)
def _auth_service_singleton() -> AuthService:
    return AuthService(repo=UserRepository())

def get_auth_service() -> AuthService:
    return _auth_service_singleton()


@lru_cache(maxsize=1)
def _chat_service_singleton() -> ChatService:
    return ChatService(data_dir=setting.data_dir)

def get_chat_service() -> ChatService:
    return _chat_service_singleton()
