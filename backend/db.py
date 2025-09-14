import sqlite3
import os

DATABASE_PATH = "/workspaces/product-finder/data/database.db"

def get_active_listing_ids():
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT id, iced_status FROM listings WHERE archived_at IS NULL")
    results = c.fetchall()

    conn.close()
    return {str(row['id']): bool(row['iced_status']) for row in results}


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

def excecute_sql(sql):
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
            enriched_model TEXT,
            enriched_brand TEXT,
            enriched_specs TEXT,
            iced_status BOOLEAN,
            iced_at DATE,
            archived_at DATE,
            price INT,
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
    excecute_sql("INSERT INTO listings (id) VALUES (0)")


if __name__ == "__main__":
    main()
