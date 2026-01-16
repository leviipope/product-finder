import json
import sqlite3
import yagmail
import os
from typing import Callable, Any
from dotenv import load_dotenv
from db import get_connection
from collections import defaultdict

load_dotenv()
GOOGLE_APP_PASSWORD = os.getenv("GOOGLE_APP_PASSWORD")
GOOGLE_EMAIL = os.getenv("GOOGLE_EMAIL")

def send_laptop_notifications(matches_by_email):
    '''
    matches_by_email: dict where key=email, value=list of dicts with keys:
        - listing: joined row from listings and enriched_specs_laptops
        - is_partial_match: bool
        - search_name: str
    '''

    yag = yagmail.SMTP(GOOGLE_EMAIL, GOOGLE_APP_PASSWORD)

    for email, data in matches_by_email.items():
        subject = f"🔥 {len(data)} New Laptop Matches Found!"

        th_css = "padding: 12px 15px; text-align: left; color: #495057; font-weight: 600;"

        html_body = f'''
        <h3 style="font-family: 'Segoe UI', Helvetica, Arial, sans-serif; color: #333; margin-bottom: 20px;">
            Hello! We found {len(data)} laptops matching your searches.
        </h3>
        <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse; width: 100%; font-family: 'Segoe UI', Helvetica, Arial, sans-serif; background-color: #fff;">
            <tr style="background-color: #f8f9fa; border-bottom: 2px solid #dee2e6;">
                <th style="{th_css}">Match</th>
                <th style="{th_css}">Search</th>
                <th style="{th_css}">Brand</th>
                <th style="{th_css}">Model</th>
                <th style="{th_css}">Specs</th>
                <th style="{th_css}">Price</th>
                <th style="{th_css}">Location</th>
                <th style="padding: 12px 15px; text-align: center; color: #495057; font-weight: 600;">Action</th>
            </tr>
        '''

        td_css = "padding: 12px 15px; vertical-align: middle;"

        for match in data:
            listing = match['listing']
            is_partial_match = match['is_partial_match']

            match_type = "⚠️ Partial" if is_partial_match else "✅ Match"
            specs = f"{listing['cpu_brand']} {listing['cpu_model']} | {listing['gpu_brand']} {listing['gpu_model']} | {listing['ram']}GB | {listing['storage_size']}GB"

            html_body += f'''
            <tr style="border-bottom: 1px solid #dee2e6;">
                <td style="padding: 12px 15px; vertical-align: middle;">{match_type}</td>
                <td style="{td_css} color: #555;">{match['search_name']}</td>
                <td style="{td_css} color: #333;">{listing['enriched_brand']}</td>
                <td style="{td_css} font-weight: 600; color: #333;">{listing['enriched_model']}</td>
                <td style="{td_css} font-size: 0.9em; color: #666; line-height: 1.4;">{specs}</td>
                <td style="{td_css} color: #2e7d32; font-weight: 700; white-space: nowrap;">{listing['price']:,} {listing['currency']}</td>
                <td style="{td_css} color: #555;">{listing['location']}</td>
                <td style="{td_css} text-align: center;">
                    <a href="{listing['listing_url']}" target="_blank" style="background-color: #007bff; color: #ffffff; padding: 8px 16px; text-decoration: none; border-radius: 4px; font-weight: 500; font-size: 0.9em; display: inline-block;">View</a>
                </td>
            </tr>
            '''

        html_body += '</table><br><p style="font-family: \'Segoe UI\', Helvetica, Arial, sans-serif; color: #555;">Happy hunting!</p>'

        yag.send(
            to=email,
            subject=subject,
            contents=html_body
        )

    print(f"Sent notifications to {len(matches_by_email)} users.")

def run_laptop_notifier(new_laptop_ids):
    with get_connection() as conn:
        c = conn.cursor()

        placeholders = ', '.join(['?'] * len(new_laptop_ids))
        query = f"""
            SELECT 
                l.site,
                l.id,
                l.price,
                l.title,
                l.iced_status,
                l.price,
                l.currency,
                l.location,
                l.listed_at,
                l.listing_url,
                e.enriched_model,
                e.enriched_brand,
                e.screen_size,
                e.panel_type,
                e.refresh_rate,
                e.cpu_brand,
                e.cpu_model,
                e.gpu_brand,
                e.gpu_model,
                e.ram,
                e.storage_size,
                e.storage_type
            FROM listings l
            INNER JOIN enriched_specs_laptops e
                ON l.id = e.listing_id
                AND l.site = e.site
            WHERE l.id IN ({placeholders})
        """

        c.execute(query, new_laptop_ids)
        new_listings = c.fetchall()

        c.execute("SELECT * FROM searches WHERE category = 'laptops' and is_active = 1")
        searches = c.fetchall()

        laptop_matches_by_email = defaultdict(list)
        for listing in new_listings:
            for search in searches:
                user_filter = json.loads(search['filters'])
                is_match, is_partial_match = match_listings_to_filters_laptops(listing, user_filter)

                if is_match:
                    laptop_matches_by_email[search['email']].append({
                        "listing": listing,
                        "is_partial_match": is_partial_match,
                        "search_name": search['search_name']
                    })

        for email, matches in laptop_matches_by_email.items():
            print(f"Constructing email for {email}...")
            for item in matches:
                status = "PARTIAL" if item['is_partial_match'] else "FULL"
                print(f" - [{status}] {item['listing']['enriched_model']}")

        send_laptop_notifications(laptop_matches_by_email)

def run_gpu_notifier(new_gpu_ids):
    with get_connection() as conn:
        c = conn.cursor()

        placeholders = ', '.join(['?'] * len(new_gpu_ids))
        query = f"""
            SELECT
                l.site,
                l.id,
                l.price,
                l.title,
                l.iced_status,
                l.price,
                l.currency,
                l.location,
                l.listed_at,
                l.listing_url,
                e.enriched_brand,
                e.enriched_model,
            FROM listings l
            INNER JOIN enriched_gpus e
                ON l.id = e.listing_id
                AND l.site = e.site
            WHERE l.id IN ({placeholders})
        """

        c.execute(query, new_gpu_ids)
        new_listings = c.fetchall()

        c.execute("SELECT * FROM searches WHERE category = 'gpus' and is_active = 1")
        searches = c.fetchall()

        gpu_matches_by_email = defaultdict(list)
        for listing in new_listings:
            for search in searches:
                user_filter = json.loads(search['filters'])
                is_match = match_listings_to_filters_gpus(listing, user_filter)

                if is_match:
                    gpu_matches_by_email[search['email']].append({
                        "listing": listing,
                        "search_name": search['search_name']
                    })


def match_listings_to_filters_laptops(listing, user_filter):
    """
    listing: joined row from listings and enriched_specs_laptops
    user_filter: dict with filter criteria
    """

    partial_match = False

    if not (user_filter['min_price'] <= listing['price'] <= user_filter['max_price']):
        return False, False

    if user_filter['enriched_brand'] != "Any" and listing['enriched_brand'].lower() != user_filter['enriched_brand'].lower():
        return False, False

    if listing['screen_size'] is None:
        partial_match = True
    elif not (user_filter['min_screen_size'] <= float(listing['screen_size']) <= user_filter['max_screen_size']):
        return False, partial_match
    
    if user_filter['panel_type'] != "Any":
        if listing['panel_type'] is None:
            partial_match = True
        elif user_filter['panel_type'].lower().strip() != listing['panel_type'].lower().strip():
            return False, partial_match
        
    if listing['refresh_rate'] is None:
        partial_match = True
    elif not (int(listing['refresh_rate']) >= user_filter['refresh_rate']):
        return False, partial_match
    
    user_gpu = user_filter['gpu_model'].strip()
    listing_gpu = (listing['gpu_model'] or "").lower().strip()
    if user_gpu == 'Any':
        pass
    elif not listing_gpu:
        partial_match = True
    elif user_gpu not in listing_gpu:
        return False, partial_match
        
    if listing['ram'] is None:
        partial_match = True
    elif not (int(listing['ram']) >= user_filter['ram']):
        return False, partial_match
    
    if listing['storage_size'] is None:
        partial_match = True
    elif not (int(listing['storage_size']) >= user_filter['storage_size']):
        return False, partial_match

    return True, partial_match

def match_listings_to_filters_gpus(listing, user_filter):
    """
    listing: joined row from listings and enriched_gpus
    user_filter: dict with filter criteria
    """

    def is_gpu_model_match(user_model, listing_model):
        user_model = user_model.replace(' ', '').strip().lower()
        listing_model = listing_model.replace(' ', '').strip().lower()
        if user_model in listing_model:
            return True

    if user_filter['enriched_brand'] != "Any" and listing['enriched_brand'].lower() != user_filter['enriched_brand'].lower():
        return False

    user_model = user_filter['enriched_model']
    listing_model = (listing['enriched_model'] or "")
    if not listing_model:
        return False

    if isinstance(user_model, list):
        for um in user_model:
            if not is_gpu_model_match(um, listing_model):
                return False
    else:
        if user_model != "Any" and not is_gpu_model_match(user_model, listing_model):
            return False
        
    return True

def add_search():
    with get_connection() as conn:
        c = conn.cursor()
        email = get_email()

        while True:
            search_name = input("Please name your search: ")
            if search_name != "":
                break

        while True:
            category = input("Please specify a category (laptops/gpus): ").strip().lower()
            if category == "laptops":
                filter_results = get_laptop_filters()
                break
            elif category == "gpus":
                filter_results = get_gpu_filters()
                break

        query = 'INSERT INTO searches (email, search_name, category, filters, is_active) VALUES (?, ?, ?, ?, ?)'
        values = (email, search_name, category, filter_results, 1)

        try:
            c.execute(query, values)
            row_id = c.lastrowid
            print(f"\nSearch {search_name} added for {email}! Your Search ID is: {row_id}")
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
        data = {"enriched_brand": "Any", "min_screen_size": 0.0, "max_screen_size": 99.0,
                "panel_type": "Any", "refresh_rate": 0, "gpu_model": "Any", "ram": 0, "storage_size": 0,
                "min_price": 0, "max_price": 9999999}

        only_price = input("Do you wish to only add a price filter (y/n)? ").lower()
        if only_price != "y":
            data["enriched_brand"] = get_input("Brand: ", str, "Any")
            data["min_screen_size"] = get_input("Minimum screen size (float): ", float, 0.0)
            data["max_screen_size"] = get_input("Maximum screen size (float): ", float, 99.0)
            data["panel_type"] = get_input("Panel type: ", str, "Any")
            data["refresh_rate"] = get_input("Minimum refresh rate (int): ", int, 0)
            data["gpu_model"] = get_input("GPU model (ex.: 3080, 4060) : ", str, "Any")
            data["ram"] = get_input("Minimum ram (GB): ", int, 0)
            data["storage_size"] = get_input("Minimum storage (GB): ", int, 0)
                
        data["min_price"] = get_input("Minimum price (int): ", int, 0)
        data["max_price"] = get_input("Maximum price (int): ", int, 9999999)

        print("\n--- Review Your Filter ---")
        for key, value in data.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        
        if input("\nDoes this look correct? (y/n): ").lower() in ('y', 'yes'):
            return json.dumps(data, indent=2)
        
def get_gpu_filters():
    while True:
        data: dict[str, Any] = {"enriched_brand": "Any", "enriched_model": "Any",}

        data['enriched_brand'] = get_input("Brand ('NVIDIA', 'AMD' or 'Intel'): ", str, "Any")
        
        only_one_model = input("How many models do you wish to search for? (one/more) ").lower()
        if only_one_model == 'more':
            data["enriched_model"] = []
            print("Please type a model (ex. 3080/3070ti) and hit enter.")
            print("If you are finished, type 'done' or ''.")
            while model not in ("done", ""):
                model = input("Model: ").lower().strip()
                data["enriched_model"].append(model)

        elif only_one_model == 'one':
            model = get_input("Model: ", str, "Any")
            data["enriched_model"] = model

        print("\n--- Review Your Filter ---")
        for key, value in data.items():
            print(f"{key.replace('_', ' ').title()}: {value}")

        if input("\nDoes this look correct? (y/n): ").lower() in ('y', 'yes'):
            return json.dumps(data, indent=2)
        
def toggle_active_serch():
    email = get_email()
    search_id = int(input("Please provide the id of the search you'd like to toggle: "))

    with get_connection() as conn:
        c = conn.cursor()

        c.execute('SELECT * FROM searches WHERE search_id = ?', (search_id,))
        search = c.fetchone()

        if not search:
            print("Error.")
            return
        
        search_name = search['search_name']
        search_email = search['email']
        is_active = search['is_active']

        if search_email != email:
            print("Error.")
            return
        
        new_status = 0 if is_active else 1
        c.execute('UPDATE searches SET is_active = ? WHERE search_id = ?', (new_status, search_id))
        status_str = "activated" if new_status else "deactivated"
        print(f"Search '{search_name}' (ID: {search_id}) has been {status_str}.")

def get_input(prompt: str, cast_type: Callable[[Any], Any] = str, default: Any = None) -> Any:
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

def run_notifiers(non_enriched_dict):
    run_laptop_notifier(non_enriched_dict['laptop'])
    run_laptop_notifier(non_enriched_dict['gpu'])

if __name__=="__main__":
    action = input("Enter action (add/remove/toggle): ")

    if action == "add":
        add_search()
    elif action == "remove":
        remove_search()
    elif action == "toggle":
        toggle_active_serch()
    elif action == 'dev':
        pass
    else:
        print("Please type either 'add', 'remove' or 'toggle'")