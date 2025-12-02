import sqlite3
import os
from pathlib import Path

base_dir = Path(__file__).parent.parent
db_path = base_dir / "data" / "database.db"
db_path = os.path.abspath(db_path)
DATABASE_PATH = db_path

def get_active_listing_ids():
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT id, iced_status FROM listings WHERE archived_at IS NULL")
    results = c.fetchall()

    conn.close()
    return {str(row['id']): bool(row['iced_status']) for row in results}

def get_non_enriched_listings():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        SELECT id FROM listings 
        WHERE id NOT IN (SELECT listing_id FROM enriched_specs_laptops)
    """)
    results = c.fetchall()

    conn.close()

    ids = [row['id'] for row in results]

    return ids

def get_latest_price(id):
    conn = get_connection()
    c = conn.cursor()

    c.execute(f"SELECT price FROM listings WHERE id = {id}")
    row = c.fetchone()

    conn.close()

    if row is None:
        return None

    return int(row[0])

def get_iced_status(id):
    conn = get_connection()
    c = conn.cursor()

    c.execute(f"SELECT iced_status FROM listings WHERE id = {id}")
    row = c.fetchone()

    conn.close()

    if row is None:
        return None

    return bool(row[0])

def get_prompt(id):
    conn = get_connection()
    c = conn.cursor()

    c.execute(f"SELECT title, site, description FROM listings WHERE id = {id}")

    row = c.fetchone()
    title, site, description = row

    prompt = f"""
Title = {title}
Description = {description}
"""

    conn.close()

    return prompt, site

def get_all_listings():
    """Prints all listings in the table, but only prints attributes that have value"""
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM listings")
    results = c.fetchall()

    if not results:
        print("Table is empty")
        return None

    number_of_listings = 0

    for row in results:
        row_dict = dict(row)
        filtered = {k: v for k, v in row_dict.items() if v is not None}
        number_of_listings += 1
        print(filtered)
    print(f"\n{'-'*33}\nNumber of listings in total: {number_of_listings}")

    conn.close()

def execute_sql(sql):
    conn = get_connection()
    c = conn.cursor()

    if isinstance(sql, str):
        c.execute(sql)
    else:
        print("SQL code has to be string")

    conn.commit()
    conn.close()

def list_tables():
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in c.fetchall()]

    conn.close()
    print(tables)

def create_listings_table():
    conn = get_connection()
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS listings (
            site TEXT,
            id INT UNIQUE NOT NULL,
            title TEXT,
            category TEXT,
            product_type TEXT,
            iced_status BOOLEAN,
            iced_at DATE,
            archived_at DATE,
            price INT,
            price_history TEXT,
            currency TEXT,
            img TEXT,
            seller TEXT,
            seller_rating TEXT,
            seller_profile_url TEXT,
            location TEXT,
            delivery_options TEXT,
            listed_at DATE,
            listing_url TEXT,
            description TEXT,
            scraped_at DATE,
              
            PRIMARY KEY (site, id)
        )
    ''')

    conn.commit()
    conn.close()

def create_enriched_specs_laptops_table():
    conn = get_connection()
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS enriched_specs_laptops (
            site TEXT NOT NULL,
            listing_id INT NOT NULL,
            enriched_model TEXT,
            enriched_brand TEXT,
            resolution TEXT,
            screen_size TEXT,
            panel_type TEXT,
            refresh_rate TEXT,
            cpu_brand TEXT,
            cpu_model TEXT,
            gpu_brand TEXT,
            gpu_model TEXT,
            gpu_type TEXT,
            ram TEXT,
            storage_size TEXT,
            storage_type TEXT,
            
            PRIMARY KEY (site, listing_id),
            FOREIGN KEY (site, listing_id) 
                REFERENCES listings(site, id)
                ON DELETE CASCADE
        )
    ''')

def get_connection():
    try:
        if not os.path.exists(DATABASE_PATH):
            raise FileNotFoundError(f"\033[91mDatabase not found at {DATABASE_PATH}\033[0m")
        
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        raise RuntimeError("\033[91m[DB ERROR] Failed to connect to database: {e}\033[0m")

def main():
    execute_sql("DELETE FROM enriched_specs_laptops")

if __name__ == "__main__":
    main()
