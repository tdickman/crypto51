import requests


algorithms = [
    'scrypt',
    'sha256',
    'scryptnf',
    'x11',
    'x13',
    'keccak',
    'x15',
    'nist5',
    'neoscrypt',
    'lyra2re',
    'whirlpoolx',
    'qubit',
    'quark',
    'axiom',
    'lyra2rev2',
    'scryptjanenf16',
    'blake256r8',
    'blake256r14',
    'blake256r8vnl',
    'hodl',
    'daggerhashimoto',
    'decred',
    'cryptonight',
    'lbry',
    'equihash',
    'pascal',
    'x11gost',
    'sia',
    'blake2s',
    'skunk',
    'cryptonightv7'
]

remap_algorithms = {
    'ethash': 'daggerhashimoto'
}


class NiceHash:
    """Retrieve details from the NiceHash api.

    Responses are cached for the life of the class.
    """
    def __init__(self):
        self._session = requests.Session()
        # self._session.headers.update({'Cookie': os.env['NICEHASH_COOKIE']})
        self._buy_info = requests.get('https://api.nicehash.com/api?method=buy.info').json()
        self._global_stats = requests.get('https://api.nicehash.com/api?method=stats.global.current').json()

    def get_cost(self, algorithm, amount):
        """Calculate the cost / hr to obtain the required hash rate with fixed contracts.

        Args:
        * algorithm - the algorithm
        * amount - the hash rate in gh/s
        """
        index = self._get_algorithm_index(algorithm)
        if index is None:
            return None
        amount = self._get_in_nicehash_units(algorithm, amount)
        day_cost_btc = 0.0
        for country in ['eu', 'us']:
            resp = self._session.get('https://www.nicehash.com/siteapi/market/{}/{}/fixed?limit={}'.format(index, country, amount)).json()
            if resp['fixedPrice'] == 'Not enough hashing power available.':
                max_fixed_price = float(resp['fixedMax']) - 0.01
                resp = self._session.get('https://www.nicehash.com/siteapi/market/{}/{}/fixed?limit={}'.format(index, country, max_fixed_price)).json()
                if resp['fixedPrice'] == 'Not enough hashing power available.':
                    continue
                day_cost_btc += float(resp['fixedPrice']) * max_fixed_price
                amount -= max_fixed_price
            else:
                day_cost_btc += float(resp['fixedPrice']) * amount
                amount -= amount
            if amount <= 0.0:
                return day_cost_btc
        return None

    def _get_in_nicehash_units(self, algorithm, value):
        """Use the buy info endpoint to convert the given value from gh to the specified units in nicehash."""
        index = self._get_algorithm_index(algorithm)
        units = self._buy_info['result']['algorithms'][index]['speed_text']
        if units == 'PH':
            return value / 1000000.0
        elif units == 'TH':
            return value / 1000.0
        elif units == 'GH':
            return value
        elif units in ['MSol', 'MH']:
            return value * 1000.0
        elif units == 'KH':
            return value * 1000000.0
        raise Exception('Unknown units: {}'.format(units))

    def get_orders(self, algorithm):
        index = self._get_algorithm_index(algorithm)
        if index is None:
            return []
        resp = requests.get('https://api.nicehash.com/api?method=orders.get&location=1&algo={}'.format(index))
        return resp.json()['result']['orders']

    def _get_algorithm_index(self, algorithm):
        algorithm = algorithm.replace('-', '').replace('(', '').replace(')', '').replace(' ', '').lower()
        algorithm = remap_algorithms.get(algorithm, algorithm)
        try:
            index = algorithms.index(algorithm)
        except ValueError:
            return None
        return index

    def get_cost_global(self, algorithm, hash_rate_ghs):
        """Return the global pricing for the specified algorithm.

        Speed in gh/s, and price in btc per gh/s per day.
        """
        index = self._get_algorithm_index(algorithm)
        if index is None:
            return None
        # Convert hash rate to the units used by NiceHash.
        hash_rate = self._get_in_nicehash_units(algorithm, hash_rate_ghs)
        pricing = float(self._global_stats['result']['stats'][index]['price'])
        print(algorithm, hash_rate, pricing, pricing * hash_rate)
        return pricing * hash_rate

    def get_hash_percentage(self, algorithm, hash_rate_ghs):
        """Return the percent of the network hash rate the hash_rate_ghs represents."""
        index = self._get_algorithm_index(algorithm)
        if index is None:
            return None
        # Convert hash rate to the units used by NiceHash.
        hash_rate = self._get_in_nicehash_units(algorithm, hash_rate_ghs)
        nicehash_speed = float(self._global_stats['result']['stats'][index]['speed'])
        print(algorithm, nicehash_speed, hash_rate)
        return nicehash_speed / hash_rate_ghs
