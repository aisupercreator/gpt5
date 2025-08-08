"""SQLite helpers for storing news items."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional, Sequence

DB_PATH = Path(__file__).resolve().parent / "news.db"


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    """Return a SQLite connection."""
    return sqlite3.connect(str(db_path))


def init_db(conn: sqlite3.Connection) -> None:
    """Initialise DB tables."""
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            title TEXT NOT NULL,
            link TEXT NOT NULL UNIQUE,
            published TEXT,
            summary TEXT,
            category TEXT
        );
        """
    )
    conn.commit()


def insert_news(conn: sqlite3.Connection, item: dict) -> None:
    """Insert a news item if it's not already present."""
    conn.execute(
        """
        INSERT OR IGNORE INTO news (source, title, link, published, summary, category)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            item.get("source"),
            item.get("title"),
            item.get("link"),
            item.get("published"),
            item.get("summary"),
            item.get("category"),
        ),
    )
    conn.commit()


def query_news(
    conn: sqlite3.Connection,
    *,
    source: Optional[str] = None,
    category: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> Sequence[sqlite3.Row]:
    """Query news with simple filtering options."""
    conn.row_factory = sqlite3.Row
    query = "SELECT * FROM news WHERE 1=1"
    params: list = []
    if source:
        query += " AND source = ?"
        params.append(source)
    if category:
        query += " AND category = ?"
        params.append(category)
    if start_date:
        query += " AND published >= ?"
        params.append(start_date)
    if end_date:
        query += " AND published <= ?"
        params.append(end_date)
    query += " ORDER BY published DESC"
    cur = conn.execute(query, params)
    return cur.fetchall()
