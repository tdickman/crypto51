import requests
import json
import time

class WTM:
    def __init__(self):
        self._wtm = {}

        print("Getting whattomine data")
        wtm = requests.get('https://whattomine.com/calculators.json').json()

        print("Filter out lagging coins from whattomine data")
        # print(json.dumps(wtm, indent=2))

        # Filter out 'lagging'
        for coin in wtm["coins"]:
            print("Grabbing more data for "+coin)
            if wtm["coins"][coin]['lagging'] == False and wtm["coins"][coin]['status'] == "Active":
                print("-> Coin isn't lagging and is active")

                # Grab *more* data from WTM
                wtmlink = 'https://whattomine.com/coins/'+str(wtm['coins'][coin]['id'])+'.json'
                wtmcoin = requests.get(wtmlink).json()

                if 'errors' in wtmcoin:
                    print(wtmcoin['errors'])
                    continue

                self._wtm[wtm["coins"][coin]['tag']] = {
                    "id":wtm["coins"][coin]['id'],
                    "name":wtmcoin["name"],
                    "symbol":wtm["coins"][coin]['tag'],
                    "algorithm":wtm["coins"][coin]['algorithm'],
                    "marketcap":float(wtmcoin["market_cap"].replace("$", '').replace(',','')),
                    "exchange_rate":wtmcoin["exchange_rate"],
                    "hashrate":wtmcoin["nethash"],
                    "block_time":float(wtmcoin['block_time'])
                }
                time.sleep(1.2)

    def get_coin_data(self):
        return self._wtm

    def get_coin_details(self, symbol):
        return self._wtm[symbol]

    def _get_h_hash_rate(self, text):
        """Convert the hash rate string to a h/s hash rate."""
        value, units = text.split(' ')
        value = float(value.replace(',', ''))
        if units == 'KH/s':
            return value * (1000.0 ** 1)
        elif units == 'MH/s':
            return value * (1000.0 ** 2)
        elif units == 'GH/s':
            return value * (1000.0 ** 3)
        elif units == 'TH/s':
            return value * (1000.0 ** 4)
        raise Exception('Unknown units: {}'.format(units))
