import os.path
import sqlite3
from contextlib import contextmanager

from dotenv import load_dotenv

from ai_researcher.utils.paths import data_root

load_dotenv()


@contextmanager
def sqlite_connection():
    connection = sqlite3.connect(
        os.path.join(data_root, os.getenv("SQLITE_FILE")),
    )
    try:
        yield connection
    finally:
        connection.close()
