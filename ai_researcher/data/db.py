from datetime import datetime
from typing import Any, Dict, List

from dotenv import load_dotenv

from ai_researcher.utils.db import sqlite_connection

load_dotenv()


def _setup_tables():
    with sqlite_connection() as sql_connection:
        c = sql_connection.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS embeddings (
                id VARCHAR PRIMARY KEY,
                embedding_time TIMESTAMP,
                metadata BLOB
            )"""
        )
        sql_connection.commit()


def get_all_embedding_ids() -> List[str]:
    with sqlite_connection() as sql_connection:
        c = sql_connection.cursor()
        c.execute("SELECT id FROM embeddings")
        embedding_ids = [row[0] for row in c.fetchall()]
    return embedding_ids


def add_embedding(
    id: str, embedding_time: datetime, metadata: Dict[str, Any]
) -> None:
    with sqlite_connection() as sql_connection:
        c = sql_connection.cursor()
        c.execute(
            "INSERT OR REPLACE INTO embeddings VALUES (?, ?, ?)",
            (id, embedding_time, str(metadata)),
        )
        sql_connection.commit()


_setup_tables()
