import requests


class CryptoCompare:
    """NOTE: This interface is a WIP and is currently not used by this project."""
    def get_all_coins(self):
        resp = requests.get('https://min-api.cryptocompare.com/data/all/coinlist')
        return resp.json()

    def get_coin_details(self, coin_symbol):
        resp = requests.get('https://min-api.cryptocompare.com/data/top/exchanges/full?fsym={}&tsym=USD'.format(coin_symbol))
        return resp.json()['Data']

    def get_all_coins_detailed(self):
        """Retrieve details for all PoW coins that meet the following requirements:

        * PoW
        * nethashes > 0
        """
        for coin_symbol, short_details in self.get_all_coins()['Data'].items():
            if short_details['ProofType'] != 'PoW':
                continue
            if not short_details['IsTrading']:
                continue
            if int(short_details['SortOrder']) > 10:
                continue
            details = self.get_coin_details(coin_symbol)
            if details['CoinInfo']['NetHashesPerSecond'] <= 0:
                continue
            print('{}: {} {} {}'.format(
                coin_symbol,
                details['AggregatedData']['MKTCAP'],
                details['CoinInfo']['NetHashesPerSecond'],
                short_details['SortOrder']
            ))
            yield {

            }
