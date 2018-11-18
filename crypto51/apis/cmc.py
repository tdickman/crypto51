import requests


class CMC:
    def get_listings(self):
        results = {}
        page_size = 100
        start = 1
        while True:
            resp = requests.get('https://api.coinmarketcap.com/v2/ticker/?sort=id&start={}'.format(start))
            data = resp.json()

            # Stop when we hit the end
            if data['metadata'].get('error') == 'id not found':
                break

            for _id, coin in data['data'].items():
                results[coin['symbol']] = {
                    'rank': coin['rank'],
                    'market_cap': coin['quotes']['USD']['market_cap'],
                    'price': coin['quotes']['USD']['price'],
                    'website_slug': coin['website_slug']
                }
            start += page_size
        return results
