from requests_html import HTMLSession


class MTC:
    def __init__(self):
        self._session = HTMLSession()

    def get_coins(self):
        resp = self._session.get('https://minethecoin.com')
        for match in resp.html.find('.mineable'):
            symbol = match.find('.coin-name', first=True).attrs['title'].split(' - ')[0]
            yield {
                'symbol': symbol,
                'name': match.find('.coin-name', first=True).attrs['title'].split(' - ')[1],
                'link': match.find('.coin-name', first=True).attrs['href']
            }

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

    def get_details(self, link):
        resp = self._session.get(link)
        html = resp.html
        hash_rate_pretty = html.find('.stats tr')[2].find('td', first=True).text
        hash_rate = self._get_h_hash_rate(hash_rate_pretty)
        return {
            'market_cap': html.find('.stats tr')[3].find('td', first=True).text,
            'hash_rate': hash_rate,
            'algorithm': html.find('.text-primary strong a', first=True).text
        }
