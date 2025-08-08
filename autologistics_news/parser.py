"""Fetch news from sources and store them in the database."""

from __future__ import annotations

import logging
from typing import Dict, Iterable

import feedparser

from .database import get_connection, init_db, insert_news
from .sources import SOURCES

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")


def fetch_source(source: Dict[str, str]) -> Iterable[Dict[str, str]]:
    """Fetch entries from a single RSS source."""
    logger.info("Fetching %s", source["name"])
    feed = feedparser.parse(source["url"], request_headers={"User-Agent": "Mozilla/5.0"})
    for entry in feed.entries:
        yield {
            "source": source["name"],
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "summary": entry.get("summary", ""),
            "published": entry.get("published", ""),
            "category": entry.tags[0]["term"] if entry.get("tags") else None,
        }


def fetch_all() -> Iterable[Dict[str, str]]:
    """Fetch entries from all configured sources."""
    for source in SOURCES:
        try:
            yield from fetch_source(source)
        except Exception as exc:  # pragma: no cover - network errors
            logger.warning("Failed to fetch %s: %s", source["name"], exc)


def main() -> None:
    """Fetch news and store them into the database."""
    conn = get_connection()
    init_db(conn)
    count = 0
    for item in fetch_all():
        insert_news(conn, item)
        count += 1
    logger.info("Stored %d items", count)
    conn.close()


if __name__ == "__main__":  # pragma: no cover
    main()
