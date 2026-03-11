"""
src/db.py

Database connectivity utilities for the DE lab.

Security/enterprise notes:
- Credentials are read from environment variables (never hardcoded).
- Supports local dev by optionally loading a .env file (python-dotenv).
- Uses SQLAlchemy URL builder to safely escape credentials.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, URL


@dataclass(frozen=True)
class PostgresConnectionConfig:
    host: str
    port: int
    database: str
    username: str
    password: str


def _load_dotenv_if_available() -> None:
    """
    Optional: load .env for local runs.
    In Docker Compose, env_file already injects variables, so this is harmless.
    """
    try:
        from dotenv import load_dotenv  # type: ignore

        load_dotenv(override=False)
    except Exception:
        # If python-dotenv isn't present or fails, we continue with OS env vars.
        return


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        raise RuntimeError(
            f"Missing required environment variable: {name}. "
            "Set it in your .env file (for local) or via Docker Compose env_file."
        )
    return value.strip()


def get_postgres_config_from_env() -> PostgresConnectionConfig:
    """
    Reads Postgres connection settings from environment variables.
    Expected:
      - DATABASE_HOST (service name in Docker network, e.g., 'postgres')
      - DATABASE_PORT (e.g., '5432')
      - POSTGRES_DB
      - POSTGRES_USER
      - POSTGRES_PASSWORD
    """
    _load_dotenv_if_available()

    host = os.getenv("DATABASE_HOST", "localhost").strip()
    port_raw = os.getenv("DATABASE_PORT", "5432").strip()

    try:
        port = int(port_raw)
    except ValueError as exc:
        raise RuntimeError(f"Invalid DATABASE_PORT (must be int): {port_raw}") from exc

    database = _require_env("POSTGRES_DB")
    username = _require_env("POSTGRES_USER")
    password = _require_env("POSTGRES_PASSWORD")

    return PostgresConnectionConfig(
        host=host,
        port=port,
        database=database,
        username=username,
        password=password,
    )


def create_postgres_engine() -> Engine:
    """
    Creates a SQLAlchemy Engine for Postgres.

    Enterprise notes:
    - pool_pre_ping avoids stale connections in long-running processes.
    - future=True uses modern SQLAlchemy behavior.
    """
    cfg = get_postgres_config_from_env()

    url = URL.create(
        drivername="postgresql+psycopg2",
        username=cfg.username,
        password=cfg.password,
        host=cfg.host,
        port=cfg.port,
        database=cfg.database,
    )

    return create_engine(url, pool_pre_ping=True, future=True)