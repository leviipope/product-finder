from db import get_connection

def main():
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # 1. Fetch new items added today
        cursor.execute("""
            SELECT product_type, COUNT(*) 
            FROM listings 
            WHERE DATE(scraped_at) = CURRENT_DATE 
              AND archived_at IS NULL 
              AND product_type IN ('Notebook', 'Hardver')
            GROUP BY product_type
        """)
        new_stats = {row[0]: row[1] for row in cursor.fetchall()}
        
        # 2. Fetch verified items archived today
        cursor.execute("""
            SELECT product_type, COUNT(*) 
            FROM listings 
            WHERE DATE(archived_at) = CURRENT_DATE 
              AND product_type IN ('Notebook', 'Hardver')
            GROUP BY product_type
        """)
        archived_stats = {row[0]: row[1] for row in cursor.fetchall()}

    CYAN = "\033[96m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

    print(f"{CYAN}{BOLD}=" * 45)
    print("            DAILY SCRAPE SUMMARY            ")
    print("=" * 45 + f"{RESET}")
    print(f"{GREEN}{BOLD} NEW LISTINGS ADDED:{RESET}")
    print(f"   Laptops (Notebook): {new_stats.get('Notebook', 0)}")
    print(f"   GPUs (Hardver):     {new_stats.get('Hardver', 0)}")
    print(f"{CYAN}-" * 45 + f"{RESET}")
    print(f"{RED}{BOLD} ITEMS ARCHIVED:{RESET}")
    print(f"   Laptops (Notebook): {archived_stats.get('Notebook', 0)}")
    print(f"   GPUs (Hardver):     {archived_stats.get('Hardver', 0)}")
    print(f"{CYAN}{BOLD}=" * 45 + f"{RESET}")

if __name__ == "__main__":
    main()