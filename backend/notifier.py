import json
from typing import Callable, Any
from db import get_connection

def run_laptop_notifier():
    pass

def add_search():
    conn = get_connection()
    cursor = conn.cursor()

    while True:
        email = input("Please provide your email: ").strip().lower()
        if not email or '@' not in email:
            print("Either no email or no '@'.")
            continue

        confirm_email = input(f"Is '{email}' correct? (y/n): ").strip().lower()
        if confirm_email in ('y', 'yes'):
            break

        category = input("Please specify a category (laptops/gpus): ").strip().lower()
        filter_results = {}
        if category == "laptops":
             filter_results = get_laptop_filters()

        # try:


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
            return data

    
def remove_search():
    pass

def get_input(prompt: str, cast_type: Callable[[Any], Any] = str, default: Any = "Not specified") -> Any:
    user_val = input(prompt).strip()
    if not user_val:
        return default
    try:
        return cast_type(user_val)
    except (ValueError, TypeError):
        print(f"Invalid input. Using default: {default}")
        return default

if __name__=="__main__":
    action = input("Enter action (add/remove): ")

    if action == "add":
        add_search()
    elif action == "remove":
        remove_search()
    else:
        print("Please type either 'add' or 'remove'")