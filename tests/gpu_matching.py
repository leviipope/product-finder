def match_listing_to_filters_gpus(listing, user_filter):
    """
    listing: joined row from listings and enriched_gpus
    user_filter: dict with filter criteria
    """

    def is_gpu_model_match(user_model, listing_model):
        user_model = user_model.replace(' ', '').strip().lower()
        listing_model = listing_model.replace(' ', '').strip().lower()
        if user_model in listing_model:
            return True
        return False

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
        if user_model != "Any" and not is_gpu_model_match(user_model, listing_model):
            return False
        
    return True

def main():
    listing = {
        'enriched_brand': 'NVIDIA',
        'enriched_model': 'NVIDIA GeForce GT1030'
    }
    user_filter = {
        'enriched_brand': 'NVIDIA',
        'enriched_model': ['4060ti', '1080ti']
    }

    is_match = match_listing_to_filters_gpus(listing, user_filter)
    print(f"Is match: {is_match}")

if __name__ == "__main__":
    main()