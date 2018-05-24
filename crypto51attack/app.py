import json

from crypto51attack.libs.mtc import MTC
from crypto51attack.libs.nicehash import NiceHash


if __name__ == '__main__':
    mtc = MTC()
    nh = NiceHash()
    results = []
    for coin in mtc.get_coins():
        details = mtc.get_details(coin['link'])
        cost = nh.get_cost(details['algorithm'], details['hash_rate'])
        if cost:
            print(coin)
            print(details)
            print(cost)
            data: dict = {}
            data.update(coin)
            data.update(details)
            data['24h_cost'] = cost
            results.append(data)

    with open('results.json', 'w') as f:
        json.dump(results, f)
