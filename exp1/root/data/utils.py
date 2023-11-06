SERVICES = [
    "GitHub", 
    'Amadeus_Hotels', 
    'Stripe_Coupons', 
    "Stripe_Products", 
    "Yelp_Businesses", 
    "YouTube_CommentsAndThreads", 
    "YouTube_Search", 
    "YouTube_Videos", 
]

def key_value_preprocessing(key, value, types):
    if not types[key]=='number' and not value.lower() in ['true', 'false']:
        value = "'" + value + "'"

    return key, value

def is_api_key(key, api_keys):
    if key in api_keys:
        return True
    return False
