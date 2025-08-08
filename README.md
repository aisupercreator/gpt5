# Auto Logistics News Parser

This repository provides a basic parser that collects auto/logistics news from several popular Russian sources and stores them into a SQLite database for further processing and display. The parser currently targets ten feeds including Autonews, Kommersant, RBC, TASS, Gazeta, RG, as well as logistics focused portals such as Logirus, RZD‑Partner (logistics) and Lognews.

## Setup

```bash
pip install -r requirements.txt
```

## Fetch news

```bash
python -m autologistics_news.parser
```

The script will create `autologistics_news/news.db` and populate it with parsed articles. The database can be queried using helpers from `autologistics_news.database` for filtering by source, category and date.
