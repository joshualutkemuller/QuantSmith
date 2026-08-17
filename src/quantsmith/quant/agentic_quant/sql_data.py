"""SQL data integration layer for quant workflows.

Provides a lightweight abstraction over common database backends for
general quant data access.  Designed for Python + SQL environments.

Supported backends (add credentials via environment variables):
  - SQLite   (built-in, ideal for local dev/testing)
  - PostgreSQL via psycopg2
  - SQL Server via pyodbc (common in institutional environments)
"""

from __future__ import annotations

import abc
import contextlib
from typing import Any, Dict, Generator, List, Optional, Sequence

from .framework import Blackboard


# ---------------------------------------------------------------------------
# Abstract interface
# ---------------------------------------------------------------------------

class SQLDataSource(abc.ABC):
    """Abstract SQL connection interface.  Implement for any backend."""

    @abc.abstractmethod
    def query(self, sql: str, params: Sequence[Any] = ()) -> List[Dict[str, Any]]:
        """Execute a SELECT and return rows as a list of dicts."""

    @abc.abstractmethod
    def execute(self, sql: str, params: Sequence[Any] = ()) -> None:
        """Execute a non-SELECT statement."""

    @contextlib.contextmanager
    def transaction(self) -> Generator[None, None, None]:
        """Context manager for transactional operations."""
        yield


# ---------------------------------------------------------------------------
# Concrete implementations
# ---------------------------------------------------------------------------

class SQLiteDataSource(SQLDataSource):
    """SQLite-backed source for local development and testing."""

    def __init__(self, database: str = ":memory:") -> None:
        import sqlite3

        self._conn = sqlite3.connect(database, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row

    def query(self, sql: str, params: Sequence[Any] = ()) -> List[Dict[str, Any]]:
        cursor = self._conn.execute(sql, params)
        columns = [d[0] for d in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def execute(self, sql: str, params: Sequence[Any] = ()) -> None:
        self._conn.execute(sql, params)
        self._conn.commit()

    @contextlib.contextmanager
    def transaction(self) -> Generator[None, None, None]:
        with self._conn:
            yield

class PostgreSQLDataSource(SQLDataSource):
    """PostgreSQL backend via psycopg2.

    Usage::

        import os
        src = PostgreSQLDataSource(
            host=os.environ["PG_HOST"],
            dbname=os.environ["PG_DB"],
            user=os.environ["PG_USER"],
            password=os.environ["PG_PASS"],
        )
    """

    def __init__(self, **connect_kwargs: Any) -> None:
        try:
            import psycopg2
            import psycopg2.extras
        except ImportError as exc:
            raise RuntimeError("psycopg2 is required for PostgreSQLDataSource") from exc

        self._conn = psycopg2.connect(**connect_kwargs)
        self._extras = psycopg2.extras

    def query(self, sql: str, params: Sequence[Any] = ()) -> List[Dict[str, Any]]:
        with self._conn.cursor(cursor_factory=self._extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            return [dict(row) for row in cur.fetchall()]

    def execute(self, sql: str, params: Sequence[Any] = ()) -> None:
        with self._conn.cursor() as cur:
            cur.execute(sql, params)
        self._conn.commit()

    @contextlib.contextmanager
    def transaction(self) -> Generator[None, None, None]:
        try:
            yield
            self._conn.commit()
        except Exception:
            self._conn.rollback()
            raise


class SQLServerDataSource(SQLDataSource):
    """SQL Server backend via pyodbc (common in institutional environments).

    Usage::

        import os
        src = SQLServerDataSource(
            dsn="DRIVER={ODBC Driver 18 for SQL Server};"
                f"SERVER={os.environ['MSSQL_HOST']};"
                f"DATABASE={os.environ['MSSQL_DB']};"
                "Trusted_Connection=yes;"
        )
    """

    def __init__(self, dsn: str, **connect_kwargs: Any) -> None:
        try:
            import pyodbc
        except ImportError as exc:
            raise RuntimeError("pyodbc is required for SQLServerDataSource") from exc

        self._conn = pyodbc.connect(dsn, **connect_kwargs)

    def query(self, sql: str, params: Sequence[Any] = ()) -> List[Dict[str, Any]]:
        cursor = self._conn.execute(sql, params)
        columns = [d[0] for d in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def execute(self, sql: str, params: Sequence[Any] = ()) -> None:
        self._conn.execute(sql, params)
        self._conn.commit()


