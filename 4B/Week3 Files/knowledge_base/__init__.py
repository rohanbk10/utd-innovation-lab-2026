"""
Knowledge Base module for JKYog WhatsApp Bot
Leena's FAQ and event data with search functionality
"""

from .ingestion import search_kb, load_faqs, load_events, build_documents

__all__ = [
    "search_kb",
    "load_faqs",
    "load_events",
    "build_documents",
]
