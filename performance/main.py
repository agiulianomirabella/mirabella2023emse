import pandas as pd

SERVICES = [
    "GitHub",
    "Amadeus_Hotels",
    "Stripe_Coupons",
    "Stripe_Products",
    "Yelp_Businesses",
    "YouTube_CommentsAndThreads",
    "YouTube_Videos",
    "YouTube_Search",
]

results = pd.DataFrame()

for service in SERVICES:
    for tech in ['rt', 'atlas']:
        time = sum(pd.read_csv(f'data/{service}_{tech}_time/time.csv')['Test suite generation'])
        results = results.append({
            'service': service,
            'tech': tech,
            'time': time,
        }, ignore_index = True)

results.to_csv('results.csv')

print(results.groupby('tech').mean()/(1000 * 60))