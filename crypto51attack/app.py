import json

from crypto51attack.libs.mtc import MTC
from crypto51attack.libs.nicehash import NiceHash
from crypto51attack.libs.cmc import CMC


if __name__ == '__main__':
    mtc = MTC()
    nh = NiceHash()
    cmc = CMC()
    listings = cmc.get_listings()
    results = []
    for coin in mtc.get_coins():
        details = mtc.get_details(coin['link'])
        cost = nh.get_cost_global(details['algorithm'], details['hash_rate'])
        nh_hash_percentage = nh.get_hash_percentage(details['algorithm'], details['hash_rate'])
        if cost:
            print(coin)
            print(details)
            print(cost)
            data: dict = {}
            data.update(coin)
            data.update(details)
            listing = listings.get(data['symbol'])
            del data['market_cap']
            # Skip anything not in cmc for now
            # Also skip bitgem since the hash rate appears to be incorrect
            if not listing or data['name'] == 'Bitgem':
                continue

            data['nicehash_capacity'] = nh.get_capacity(details['algorithm'])
            data['nicehash_algorithm_name'] = nh.get_algorithm_name(details['algorithm'])
            data['nicehash_units'] = nh.get_units(details['algorithm'])
            data['nicehash_price'] = nh.get_algorithm_price(details['algorithm'])
            data['hour_cost'] = '${:,.0f}'.format(cost * listings['BTC']['price'] / 24.0)
            data['nicehash_hash_percentage'] = '{:,.0f}%'.format(nh_hash_percentage * 100.0)
            data['market_cap'] = '${:,.0f}'.format(listing['market_cap']) if listing['market_cap'] else None
            data['rank'] = listing['rank']
            data['cmc_slug'] = listing['website_slug']
            results.append(data)

    # Sort by rank
    results = sorted(results, key=lambda k: k['rank'])

    with open('results.json', 'w') as f:
        json.dump(results, f)
