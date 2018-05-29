import datetime
import json

from crypto51attack.apis.mtc import MTC
from crypto51attack.apis.nicehash import NiceHash
from crypto51attack.apis.cmc import CMC
from crypto51attack.libs import common
from crypto51attack import config


if __name__ == '__main__':
    mtc = MTC()
    nh = NiceHash()
    cmc = CMC()
    listings = cmc.get_listings()
    btc_price = listings['BTC']['price']
    coins = []
    for coin in mtc.get_coins():
        # Certain coins have invalid hash rates or other values, so we skip them
        if coin['symbol'] in config.coin_blacklist:
            continue

        mining_details = mtc.get_details(coin['link'])
        cost = nh.get_cost_global(mining_details['algorithm'], mining_details['hash_rate'])
        nh_hash_ratio = nh.get_hash_percentage(mining_details['algorithm'], mining_details['hash_rate'])

        # Skip coins that NiceHash doesn't support
        if not cost:
            continue

        # Skip anything not in cmc for now
        listing = listings.get(coin['symbol'])
        if not listing:
            continue

        # TODO: Add this to the coin blacklist.
        if coin['name'] == 'Bitgem':
            continue

        print(coin)
        print(mining_details)
        print(cost)

        rentable_capacity = nh.get_capacity(mining_details['algorithm'])
        rentable_price_btc = nh.get_algorithm_price(mining_details['algorithm'])
        coins.append({
            'symbol': coin['symbol'],
            'name': coin['name'],
            'minethecoin_link': coin['link'],
            'algorithm': mining_details['algorithm'],
            'market_cap': listing['market_cap'],
            'market_cap_pretty': common.get_pretty_money(listing['market_cap']),
            'coinmarketcap_rank': listing['rank'],
            'coinmarketcap_link': 'https://www.coinmarketcap.com/currencies/{}'.format(listing['website_slug']),
            'hash_rate': mining_details['hash_rate'],
            'hash_rate_pretty': common.get_pretty_hash_rate(mining_details['hash_rate']),
            'rentable_capacity': rentable_capacity,
            'rentable_capacity_pretty': common.get_pretty_hash_rate(rentable_capacity),
            'nicehash_market_link': 'https://www.nicehash.com/marketplace/{}'.format(nh.get_algorithm_name(mining_details['algorithm'])),
            'hour_cost': cost * btc_price / 24.0,
            'hour_cost_pretty': '${:,.0f}'.format(cost * btc_price / 24.0),
            'network_vs_rentable_ratio': nh_hash_ratio,
            'rentable_price_btc': rentable_price_btc,
            'rentable_price_btc_units': nh.get_units(mining_details['algorithm']),
            'rentable_price_usd_hour': '{:,.2f}'.format(rentable_price_btc * btc_price / 24.0)
        })

    # Sort by rank
    results = {
        'last_updated': datetime.datetime.utcnow(),
        'coins': sorted(coins, key=lambda k: k['coinmarketcap_rank'])
    }

    with open('dist/coins.json', 'w') as f:
        json.dump(results, f)
