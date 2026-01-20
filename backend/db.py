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

def get_non_enriched_ids_by_product_type() -> dict[str, list[int]]:
    laptop_ids = get_non_enriched_laptop_ids()
    gpu_ids = get_non_enriched_gpu_ids()

    return laptop_ids | gpu_ids

def get_non_enriched_laptop_ids() -> dict[str, list[int]]:
    with get_connection() as conn:
        c = conn.cursor()
        
        c.execute("""
            SELECT id FROM listings 
            WHERE product_type = 'Notebook' 
            AND id NOT IN (SELECT listing_id FROM enriched_specs_laptops)
        """)
        results = c.fetchall()

        ids = [row['id'] for row in results]

        return {"laptop": ids}
    
def get_non_enriched_gpu_ids() -> dict[str, list[int]]:
    with get_connection() as conn:
        c = conn.cursor()
        
        c.execute("""
            SELECT id FROM listings 
            WHERE json_extract(category, '$[2]') = 'Videokártya'
            AND id NOT IN (SELECT listing_id FROM enriched_gpus)
        """)
        results = c.fetchall()

        ids = [row['id'] for row in results]

        return {"gpu": ids}

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

def get_prompt(id, product_type):
    conn = get_connection()
    c = conn.cursor()

    c.execute(f"SELECT title, category, site, description FROM listings WHERE id = {id}")

    row = c.fetchone()
    title, category, site, description = row

    if product_type == "gpu":
            prompt = f"""
Title = {title}
Here is the category hierarchy for the product (use this as a hint): {category}
"""
    else:
        prompt = f"""
Category = {category}
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
    with get_connection() as conn:
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

def create_enriched_gpus_table():
    with get_connection() as conn:
        c = conn.cursor()

        c.execute('''
            CREATE TABLE IF NOT EXISTS enriched_gpus (
                site TEXT NOT NULL,
                listing_id INT NOT NULL,
                enriched_brand TEXT,
                enriched_model TEXT,
                vram INTEGER,
                                
                PRIMARY KEY (site, listing_id),
                FOREIGN KEY (site, listing_id) 
                    REFERENCES listings(site, id)
                    ON DELETE CASCADE
            )
        ''')

def create_searches_table():
    with get_connection() as conn:
        c = conn.cursor()

        c.execute('''
            CREATE TABLE IF NOT EXISTS searches(
                search_id INTEGER PRIMARY KEY,  
                email TEXT NOT NULL,
                search_name TEXT NOT NULL,
                category TEXT NOT NULL,
                filters TEXT NOT NULL,
                is_active BOOLEAN
            )
        ''')

def create_laptop_view():
    with get_connection() as conn:
        c = conn.cursor()

        c.execute('''
            CREATE VIEW IF NOT EXISTS laptop_view AS
            SELECT 
                l.site,
                l.id AS listing_id,
                e.enriched_brand AS brand,
                e.enriched_model AS model,
                l.title,
                l.price,
                l.currency,
                l.iced_status,
                l.archived_at,
                e.cpu_brand,
                e.cpu_model,
                e.gpu_brand,
                e.gpu_model,
                e.gpu_type,
                e.ram,
                e.storage_size,
                e.resolution,
                e.screen_size,
                e.panel_type,
                e.refresh_rate,
                e.storage_type,
                l.listing_url,
                l.location,
                l.listed_at,
                l.scraped_at
            FROM listings l
            JOIN enriched_specs_laptops e
            ON l.site = e.site AND l.id = e.listing_id
            WHERE l.product_type = 'Notebook';
        ''')

def create_gpu_view():
    with get_connection() as conn:
        c = conn.cursor()

        c.execute('''
            CREATE VIEW IF NOT EXISTS gpu_view AS
            SELECT 
                l.site,
                l.id AS listing_id,
                e.enriched_brand AS brand,
                e.enriched_model AS model,
                e.vram,
                l.price,
                l.currency,
                l.iced_status,
                l.archived_at,
                l.listing_url,
                l.location,
                l.listed_at,
                l.scraped_at
            FROM listings l
            JOIN enriched_gpus e
            ON l.site = e.site AND l.id = e.listing_id
            WHERE json_extract(l.category, '$[2]') = 'Videokártya';
        ''')

def get_connection():
    try:
        if not os.path.exists(DATABASE_PATH):
            raise FileNotFoundError(f"\033[91mDatabase not found at {DATABASE_PATH}\033[0m")
        
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        raise RuntimeError(f"\033[91m[DB ERROR] Failed to connect to database: {e}\033[0m")

def main():
    pass

if __name__ == "__main__":
    main()
