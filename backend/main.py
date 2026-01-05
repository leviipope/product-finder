from fastapi import FastAPI
from .db import get_connection

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "OK"}

@app.get("/listings")
def get_listings():
    conn = get_connection()

    listings = conn.execute(
        'SELECT * FROM listings'
    ).fetchall()

    conn.close()

    return [dict(row) for row in listings]