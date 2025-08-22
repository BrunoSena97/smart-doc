from __future__ import annotations
from pathlib import Path
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

_engine = None
_SessionLocal: Optional[sessionmaker] = None

def _resolve_sqlite_url(app, url: str) -> str:
    # Only touch sqlite URLs
    if not url.startswith("sqlite:///"):
        return url
    # Remove "sqlite:///" and resolve against the app's instance_path
    rel = url.replace("sqlite:///", "", 1)
    # If rel is absolute already, keep it
    p = Path(rel)
    if p.is_absolute():
        p.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite:///{p}"

    # Otherwise resolve into instance folder
    inst = Path(app.instance_path)
    inst.mkdir(parents=True, exist_ok=True)
    target = (inst / rel).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{target}"

def init_app(app):
    global _engine, _SessionLocal
    db_cfg = app.config.get("DATABASE", {})
    url = db_cfg.get("url", "sqlite:///:memory:")
    url = _resolve_sqlite_url(app, url)
    echo = db_cfg.get("echo", False)

    _engine = create_engine(url, echo=echo, future=True, pool_pre_ping=True)
    _SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False, future=True)

    # Enable WAL/sane sync only for on-disk SQLite
    if url.startswith("sqlite:///") and ":memory:" not in url:
        with _engine.connect() as conn:
            conn.exec_driver_sql("PRAGMA journal_mode=WAL;")
            conn.exec_driver_sql("PRAGMA synchronous=NORMAL;")

def get_engine():
    return _engine

def get_session():
    if _SessionLocal is None:
        raise RuntimeError("DB not initialized; call db.init_app(app) first.")
    return _SessionLocal()
