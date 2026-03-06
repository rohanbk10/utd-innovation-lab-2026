"""
Database module for JKYog WhatsApp Bot
Chakradhar's database schema and state tracking
"""

from .models import Base, engine, SessionLocal, get_db, init_db
from .schema import User, Conversation, Message, SessionState
from .state_tracking import (
    get_or_create_user,
    get_or_create_active_conversation,
    log_message,
    create_session,
    get_session_by_token,
    merge_session_state,
)

__all__ = [
    "Base",
    "engine",
    "SessionLocal",
    "get_db",
    "init_db",
    "User",
    "Conversation",
    "Message",
    "SessionState",
    "get_or_create_user",
    "get_or_create_active_conversation",
    "log_message",
    "create_session",
    "get_session_by_token",
    "merge_session_state",
]
