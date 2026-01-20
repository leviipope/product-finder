def match_listing_to_filters_gpus(listing, user_filter):
    """
    listing: joined row from listings and enriched_gpus
    user_filter: dict with filter criteria
    """

    def is_gpu_model_match(user_model, listing_model):
        import re
        def check_ti(s):
            return bool(re.search(r'(\d+ti|\bti\b|superti)', s.lower()))
        def check_super(s):
            return bool(re.search(r'(\d+super|\bsuper\b|tisuper)', s.lower()))

        user_searching_for_ti = check_ti(user_model)
        listing_is_ti = check_ti(listing_model)
        user_searching_for_super = check_super(user_model)
        listing_is_super = check_super(listing_model)

        if user_searching_for_ti != listing_is_ti:
            return False
        
        if user_searching_for_super != listing_is_super:
            return False

        user_model = user_model.replace(' ', '').strip().lower()
        listing_model = listing_model.replace(' ', '').strip().lower()
        return user_model in listing_model

    if user_filter['enriched_brand'] != "Any" and listing['enriched_brand'].lower() != user_filter['enriched_brand'].lower():
        return False

    user_model = user_filter['enriched_model']
    listing_model = (listing['enriched_model'] or "")

    if not listing_model:
        return False

    if isinstance(user_model, list):
        match_found = False
        for um in user_model:
            if is_gpu_model_match(um, listing_model):
                match_found = True
                break

        if not match_found:
            return False
    else:
        if user_filter['max_price'] < listing['price'] or (user_model != "Any" and not is_gpu_model_match(user_model, listing_model)):
            return False
        
    return True

def main():
    listing = {
        'enriched_brand': 'NVIDIA',
        'enriched_model': 'GeForce GTX 2060 super ti',
        'price': 50000
    }
    user_filter = {
        'enriched_brand': 'NVIDIA',
        'enriched_model': '2060ti',
        'max_price': 9_999_999
    }

    is_match = match_listing_to_filters_gpus(listing, user_filter)
    print(f"Is match: {is_match}")

if __name__ == "__main__":
    main()