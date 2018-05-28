import json

from crypto51attack.libs.mtc import MTC
from crypto51attack.libs.nicehash import NiceHash
from crypto51attack.libs.cmc import CMC


def get_pretty_hash_rate(hash_rate):
    """Convert the given hash rate to a pretty value."""
    if hash_rate > (1000.0 ** 5):
        return '{:,.0f} PH/s'.format(hash_rate / (1000.0 ** 5))
    elif hash_rate > (1000.0 ** 4):
        return '{:,.0f} TH/s'.format(hash_rate / (1000.0 ** 4))
    elif hash_rate > (1000.0 ** 3):
        return '{:,.0f} GH/s'.format(hash_rate / (1000.0 ** 3))
    elif hash_rate > (1000.0 ** 2):
        return '{:,.0f} MH/s'.format(hash_rate / (1000.0 ** 2))
    elif hash_rate > (1000.0 ** 1):
        return '{:,.0f} KH/s'.format(hash_rate / (1000.0 ** 1))
    else:
        return '{:,.0f} H/s'.format(hash_rate / (1000.0 ** 0))


def get_pretty_money(value):
    """Conver the number to a pretty dollar value with units."""
    if value > (1000.0 ** 4):
        return '${:,.2f} T'.format(value / (1000.0 ** 4))
    elif value > (1000.0 ** 3):
        return '${:,.2f} B'.format(value / (1000.0 ** 3))
    elif value > (1000.0 ** 2):
        return '${:,.2f} M'.format(value / (1000.0 ** 2))
    elif value > (1000.0 ** 0):
        return '${:,.0f}'.format(value)


if __name__ == '__main__':
    mtc = MTC()
    nh = NiceHash()
    cmc = CMC()
    listings = cmc.get_listings()
    btc_price = listings['BTC']['price']
    results = []
    for coin in mtc.get_coins():
        details = mtc.get_details(coin['link'])
        cost = nh.get_cost_global(details['algorithm'], details['hash_rate'])
        nh_hash_percentage = nh.get_hash_percentage(details['algorithm'], details['hash_rate'])
        nh_hash_percentage = int(nh_hash_percentage * 100.0) / 100.0 if nh_hash_percentage and nh_hash_percentage > 100 else nh_hash_percentage
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

            data['nicehash_capacity'] = get_pretty_hash_rate(nh.get_capacity(details['algorithm']))
            data['nicehash_algorithm_name'] = nh.get_algorithm_name(details['algorithm'])
            data['nicehash_units'] = nh.get_units(details['algorithm'])
            data['nicehash_price_btc'] = nh.get_algorithm_price(details['algorithm'])
            data['nicehash_price_usd_hour'] = '{:,.2f}'.format(data['nicehash_price_btc'] * btc_price / 24.0)
            data['hour_cost'] = '${:,.0f}'.format(cost * btc_price / 24.0)
            data['nicehash_hash_percentage'] = nh_hash_percentage
            data['market_cap'] = get_pretty_money(listing['market_cap']) if listing['market_cap'] else '-'
            data['rank'] = listing['rank']
            data['cmc_slug'] = listing['website_slug']
            data['hash_rate_pretty'] = get_pretty_hash_rate(details['hash_rate'])
            results.append(data)

    # Sort by rank
    results = sorted(results, key=lambda k: k['rank'])

    with open('results.json', 'w') as f:
        json.dump(results, f)
