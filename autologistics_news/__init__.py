"""Auto logistics news parser package."""

from .parser import fetch_all, main  # re-export
from .database import init_db, get_connection, query_news

__all__ = ["fetch_all", "main", "init_db", "get_connection", "query_news"]
