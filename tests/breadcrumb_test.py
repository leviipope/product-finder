breadcrumb_text = '\n\t\t\n\t\tApróhirdetések\n\t\tNotebook\n\t'
if breadcrumb_text:
    breadcrumb_text = breadcrumb_text.replace("\t", " ").replace("\n", " ").strip()
    parts = breadcrumb_text.split()
    print(breadcrumb_text, parts)
    if len(parts) >= 2:
        product_type = parts[1]
        print(f"\033[92mDEBUG: Added category: {product_type}\033[0m") # Add this line