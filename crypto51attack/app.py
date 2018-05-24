from crypto51attack.libs.mtc import MTC
from crypto51attack.libs.nicehash import NiceHash


if __name__ == '__main__':
    mtc = MTC()
    nh = NiceHash()
    for coin in mtc.get_coins():
        details = mtc.get_details(coin['link'])
        cost = nh.get_cost(details['algorithm'], details['hash_rate'])
        if cost:
            print(coin)
            print(details)
            print(cost)
