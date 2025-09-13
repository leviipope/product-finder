import pytest
import sqlite3
from datetime import datetime
from backend.scraper.scraper.pipelines import SQLitePipeline
from itemadapter import ItemAdapter

# Helper function to create in-memory DB
def create_test_db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE listings (
            id TEXT PRIMARY KEY,
            iced_status INTEGER,
            iced_at TEXT,
            description TEXT
        )
    """)
    conn.commit()
    return conn, cursor

@pytest.fixture
def pipeline():
    # Create pipeline but override its connection with in-memory DB
    pl = SQLitePipeline()
    conn, cursor = create_test_db()
    pl.conn = conn
    pl.cursor = cursor
    return pl

def test_full_item_insert(pipeline):
    item = {
        "id": "listing1",
        "iced_status": True,
        "description": "Full description"
    }
    pipeline.process_item(item, None)

    pipeline.cursor.execute("SELECT * FROM listings WHERE id = ?", ("listing1",))
    row = pipeline.cursor.fetchone()

    assert row["id"] == "listing1"
    assert row["iced_status"] == 1
    assert row["iced_at"] is None  # Full item does NOT set iced_at
    assert row["description"] == "Full description"

def test_iced_update_true(pipeline):
    # Insert initial listing
    pipeline.cursor.execute(
        "INSERT INTO listings (id, iced_status, iced_at) VALUES (?, ?, ?)",
        ("listing2", 0, None)
    )
    pipeline.conn.commit()

    # Partial item: iced status changed to True
    item = {
        "id": "listing2",
        "iced_status": True,
        "description": None
    }
    pipeline.process_item(item, None)

    pipeline.cursor.execute("SELECT * FROM listings WHERE id = ?", ("listing2",))
    row = pipeline.cursor.fetchone()

    assert row["iced_status"] == 1
    assert row["iced_at"] is not None  # iced_at set for partial update

def test_iced_update_false(pipeline):
    # Insert initial listing with iced_status = True
    pipeline.cursor.execute(
        "INSERT INTO listings (id, iced_status, iced_at) VALUES (?, ?, ?)",
        ("listing3", 1, "2025-09-13 21:00:00")
    )
    pipeline.conn.commit()

    # Partial item: iced status changed to False
    item = {
        "id": "listing3",
        "iced_status": False,
        "description": None
    }
    pipeline.process_item(item, None)

    pipeline.cursor.execute("SELECT * FROM listings WHERE id = ?", ("listing3",))
    row = pipeline.cursor.fetchone()

    assert row["iced_status"] == 0
    assert row["iced_at"] is None  # iced_at cleared for False
