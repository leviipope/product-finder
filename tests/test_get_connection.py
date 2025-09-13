import os
import sqlite3
import pytest
from backend.db import get_connection, DATABASE_PATH

def test_get_connection_success(tmp_path):
    # Create a temporary valid DB file
    db_file = tmp_path / "test.db"
    conn = sqlite3.connect(db_file)
    conn.close()

    # Patch DATABASE_PATH
    global DATABASE_PATH
    DATABASE_PATH = str(db_file)

    result = get_connection()
    assert isinstance(result, sqlite3.Connection)
    result.close()

def test_get_connection_missing_file(monkeypatch, tmp_path):
    missing_db = tmp_path / "missing.db"
    monkeypatch.setattr("backend.db.DATABASE_PATH", str(missing_db))  # patch the variable

    import backend.db as db  # ensure the patch is active

    with pytest.raises(FileNotFoundError):
        db.get_connection()

def test_get_connection_sqlite_error(monkeypatch, tmp_path):
    # Create a valid DB file
    db_file = tmp_path / "test_invalid.db"
    open(db_file, "w").close() # empty file
    global DATABASE_PATH
    DATABASE_PATH = str(db_file)

    # Force sqlite3.connect to raise sqlite3.Error
    def bad_connect(*args, **kwargs):
        raise sqlite3.Error("boom")
    
    monkeypatch.setattr(sqlite3, "connect", bad_connect)

    with pytest.raises(RuntimeError) as excinfo:
        get_connection()
    assert "DB ERROR" in str(excinfo.value)

