import sqlite3

DATABASE_PATH = "/workspaces/product-finder/data/database.db"

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

def add_demo_listing():
    conn = get_connection()
    c = conn.cursor()

    c.execute("INSERT INTO listings (site, id) VALUES ('test site', 430)")

    conn.commit()
    conn.close()

def delete_all_listings():
    conn = get_connection()
    c = conn.cursor()

    c.execute("DELETE FROM listings")

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
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def main():
    list_tables()
    get_all_listings()

if __name__ == "__main__":
    main()
