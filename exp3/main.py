import os
import pandas as pd

from root.data.dataset import read_dataset

MODES = ['rt', 'atlas']
SERVICES = [
    "GitHub",
    'Amadeus_Hotels', 
    "Stripe_Coupons",
    "Stripe_Products",
    "Yelp_Businesses",
    "YouTube_CommentsAndThreads",
    "YouTube_Videos",
    "YouTube_Search",
]

out = pd.DataFrame(columns=['service', 'tech', 'dirname', 'size', 'n_valid', 'valid_ratio', 'n_remainings'])

for service in SERVICES:
    for mode in MODES:
        for i in range(10):

            dirname = f'{service}_{mode}_{i}'

            exp_folder = f'data/{service}/{mode}/{dirname}'
            properties_path = f'../RESTest/src/test/resources/{service}/props.properties'

            data = read_dataset(exp_folder, properties_path)

            out = out.append({
                'service': service,
                'tech': mode,
                'dirname': dirname,
                'size': data.size,
                'OAS': data.get_oas(),
                '5XX': data.get_5XX(),
                'n_valid': data.n_obt_valid,
                'valid_ratio': data.obt_valid_ratio,
            }, ignore_index=True)
            
for service in out['service']:
    tmp = out[out['service']==service]
    tmp[['tech', 'valid_ratio', 'OAS']].set_index('tech').sort_index().to_csv(f'results/{service}.csv')

out = out[['service', 'tech', 'valid_ratio', 'OAS', '5XX']].groupby(['service', 'tech']).mean()

out = pd.pivot_table(out, index='service', columns='tech', values=['valid_ratio', 'OAS', '5XX'])
out.columns = [f'{col}_{tech}' for col, tech in out.columns]
out = out[out.columns[::-1]]
out.loc['Mean'] = out.mean()

print(out)
