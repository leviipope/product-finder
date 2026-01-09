import json
import sqlite3
from typing import Callable, Any
from db import get_connection

def run_laptop_notifier():
    pass

def add_search():
    with get_connection() as conn:
        c = conn.cursor()
        email = get_email()

        while True:
            category = input("Please specify a category (laptops/gpus): ").strip().lower()
            if category == "laptops":
                filter_results = get_laptop_filters()
                break
            elif category == "gpus":
                print("gpu alerting not yet integrated")
                return

        query = 'INSERT INTO searches (email, category, filters, is_active) VALUES (?, ?, ?, ?)'
        values = (email, category, filter_results, 1)

        try:
            c.execute(query, values)
            row_id = c.lastrowid
            print(f"\nSearch added for {email}! Your Search ID is: {row_id}")
            print(f"Keep this ID if you wish to delete this search later.")
        except Exception as e:
            print(f"Error saving to database: {e}")

def remove_search():
    with get_connection() as conn:
        c = conn.cursor()

        while True:
            val = input("Please provide your row_id: ")
            if val.isdigit():
                row_id = int(val)
                break
            print("Please enter a valid numeric ID")

        c.execute('SELECT email, category FROM searches WHERE search_id = ?', (row_id,))
        row = c.fetchone()

        if not row:
            print(f"Search not found with id: {row_id}")

        email_in_db, category = row

        print(f"Found search in category: {category}")
        if input("Please verify yourself by providing your email: ").strip().lower() == email_in_db:
            print(f"Deleting row {row_id}...")
            try:
                c.execute('DELETE FROM searches WHERE search_id = ?', (row_id,))
                conn.commit()
                print("Success!")
            except sqlite3.OperationalError as e:
                print(f"Database error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        else:
            print("Email verification failed. Deletion aborted.") 

def get_laptop_filters():
    while True:
        data = {
            "brand": "Not specified", "min_screen": "Not specified",
            "max_screen": "Not specified", "panel": "Not specified",
            "refresh": "Not specified", "ram": "Not specified", "storage": "Not specified"
        }

        only_price = input("Do you wish to only add a price filter (y/n)? ").lower()

        if only_price != "y":
            data["brand"] = get_input("Brand: ")
            data["min_screen"] = get_input("Minimum screen size (float): ", float)
            data["max_screen"] = get_input("Maximum screen size (float): ", float)
            data["panel"] = get_input("Panel type: ")
            data["refresh"] = get_input("Minimum refresh rate (int): ", int)
            data["ram"] = get_input("Minimum ram (GB): ", int)
            data["storage"] = get_input("Minimum storage (GB): ", int)
                
        data["min_price"] = get_input("Minimum price (int): ", int)
        data["max_price"] = get_input("Maximum price (int): ", int)

        print("\n--- Review Your Filter ---")
        for key, value in data.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        
        if input("\nDoes this look correct? (y/n): ").lower() in ('y', 'yes'):
            return json.dumps(data, indent=2)

def get_input(prompt: str, cast_type: Callable[[Any], Any] = str, default: Any = "Not specified") -> Any:
    user_val = input(prompt).strip()
    if not user_val:
        return default
    try:
        return cast_type(user_val)
    except (ValueError, TypeError):
        print(f"Invalid input. Using default: {default}")
        return default
    
def get_email():
    while True:
        email = input("Please provide your email: ").strip().lower()
        if not email or '@' not in email or '.' not in email:
            print("Please check if you provided the correct email.")
            continue

        confirm_email = input(f"Is '{email}' correct? (y/n): ").strip().lower()
        if confirm_email not in ('y', 'yes'):
            continue

        return email

if __name__=="__main__":
    action = input("Enter action (add/remove): ")

    if action == "add":
        add_search()
    elif action == "remove":
        remove_search()
    else:
        print("Please type either 'add' or 'remove'")