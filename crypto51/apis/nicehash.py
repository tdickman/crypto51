import requests


# Nicehash name on left, wtm on right
remap_algorithms = {
    'daggerhashimoto': 'ethash',
}


class NiceHash:
    """Retrieve details from the NiceHash api.

    Responses are cached for the life of the class.
    """
    def __init__(self):
        self._session = requests.Session()
        # self._session.headers.update({'Cookie': os.env['NICEHASH_COOKIE']})
        _buy_info = requests.get('https://api2.nicehash.com/main/api/v2/public/buy/info').json()['miningAlgorithms']
        _global_stats = requests.get('https://api2.nicehash.com/main/api/v2/public/stats/global/current').json()['algos']
        self._algorithms = {a['order']: a for a in requests.get('https://api2.nicehash.com/main/api/v2/mining/algorithms/').json()['miningAlgorithms']}
        """Set up global stats"""
        self._global_stats = {}
        for stats in _global_stats:
            self._global_stats[stats['a']] = stats
        """Set up buy info"""
        self._buy_info = {}
        for info in _buy_info:
            self._buy_info[info['algo']] = info
        """Set up algo ids"""
        self._algo_ids = self._get_algo_ids()

    def _get_algo_ids(self):
        algorithms = requests.get('https://api2.nicehash.com/main/api/v2/mining/algorithms/').json()['miningAlgorithms']
        algo_ids = {}
        for a in algorithms:
            name = a['algorithm'].lower()
            name = remap_algorithms.get(name, name)
            algo_ids[name] = a['order']
        return algo_ids

    def get_cost(self, algorithm, amount):
        """Calculate the cost / hr to obtain the required hash rate with fixed contracts.

        Args:
        * algorithm - the algorithm
        * amount - the hash rate in gh/s
        """
        index = self._get_algorithm_index(algorithm)
        if index is None:
            return None
        amount = self.get_in_nicehash_units(algorithm, amount)
        day_cost_btc = 0.0
        for country in ['eu', 'us']:
            resp = self._session.post('https://api2.nicehash.com/main/api/v2/hashpower/orders/fixedPrice/', {'limit': amount, 'market': country, 'algorithm': algorithm}).json()
            if resp['fixedPrice'] == 'Not enough hashing power available.':
                max_fixed_price = float(resp['fixedMax']) - 0.01
                resp = self._session.post('https://api2.nicehash.com/main/api/v2/hashpower/orders/fixedPrice/', {'limit': max_fixed_price, 'market': country, 'algorithm': algorithm}).json()
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

    def get_units(self, algorithm):
        index = self._get_algorithm_index(algorithm)
        units = self._buy_info[index]['speed_text']
        return units

    def get_in_nicehash_units(self, algorithm, value):
        """Use the buy info endpoint to convert the given value from h/s to the specified units in nicehash."""
        return value / self.get_nicehash_unit_scale(algorithm)

    def get_nicehash_unit_scale(self, algorithm):
        units = self.get_units(algorithm)
        if units == 'PH':
            return 1000.0 ** 5
        elif units == 'TH':
            return 1000.0 ** 4
        elif units == 'GH':
            return 1000.0 ** 3
        elif units in ['MSol', 'MH']:
            return 1000.0 ** 2
        elif units in ['KH', 'kG', 'kSol']:
            return 1000.0
        raise Exception('Unknown units: {}'.format(units))

    def get_orders(self, algorithm):
        index = self._get_algorithm_index(algorithm)
        if index is None:
            return []
        """
        I have no idea what does location=1 mean:
        https://api.nicehash.com/api?method=orders.get&location=1&algo={}
        """
        resp = requests.get('https://api2.nicehash.com/main/api/v2/public/orders/?algorithm={}'.format(index))
        return resp.json()['result']['orders']

    def get_algorithm_name(self, algorithm):
        """Get the cleaned up algorithm name that nicehash uses."""
        algorithm = algorithm.replace('-', '').replace('(', '').replace(')', '').replace(' ', '').lower()
        return algorithm

    def _get_algorithm_index(self, algorithm):
        algorithm = self.get_algorithm_name(algorithm)
        return self._algo_ids.get(algorithm)

    def get_algorithm_price(self, algorithm):
        """Get the hashing cost (BTC) + units.

        Value is returned in BTC/H/DAY.
        """
        index = self._get_algorithm_index(algorithm)
        if index is None:
            return None
        # I have no clue where this constant comes from, but using it produces
        # the numbers presented on Nicehash's website.
        pricing = float(self._global_stats[index]['p']) / (10 ** 8)
        return pricing

    def get_cost_global(self, algorithm, hash_rate):
        """Return the daily cost of the given hashrate in btc."""
        pricing = self.get_algorithm_price(algorithm)
        if pricing is None:
            return
        return pricing * hash_rate

    def get_capacity(self, algorithm):
        index = self._get_algorithm_index(algorithm)
        if index is None:
            return None
        # Speed is in H/s
        nicehash_speed = float(self._global_stats[index]['s'])
        return nicehash_speed

    def get_hash_percentage(self, algorithm, hash_rate):
        """Return the percent of the network hash rate the hash_rate_ghs represents."""
        index = self._get_algorithm_index(algorithm)
        if index is None:
            return None
        # Speed is in H/s
        nicehash_speed = float(self._global_stats[index]['s'])
        return nicehash_speed / hash_rate
