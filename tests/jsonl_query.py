#!/usr/bin/env python3

import json
import sys
from pathlib import Path

def main():
    jsonl_file = sys.argv[1] if len(sys.argv) > 1 else "/workspaces/product-finder/backend/scraper/test.jsonl"
    
    if not Path(jsonl_file).is_file():
        print(f"Error: File '{jsonl_file}' not found.")
        return 1
    
    try:
        with open(jsonl_file, 'r', encoding='utf-8') as file:
            print(f"{'Title':<33} | {'Seller Rating'}")
            print(f"{'-' * 33} | {'-' * 20}")
            
            for line in file:
                if line.strip().startswith("//") or not line.strip():
                    continue
                
                try:
                    item = json.loads(line)
                    
                    title = item.get('title', 'N/A')
                    seller_rating = item.get('seller_rating', 'N/A')
                    
                    if len(title) > 30:
                        title = title[:30] + '...'
                        
                    print(f"{title:<33} | {seller_rating}")
                    
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON line: {e}")
                    continue
                    
        return 0
                
    except Exception as e:
        print(f"Error processing file: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())