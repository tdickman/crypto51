import datetime
import json
import pytz
from jinja2 import Template


def copy(name):
    """Copy the specified file from src to dist."""
    with open('src/{}'.format(name), 'r') as f:
        with open('dist/{}'.format(name), 'w') as g:
            g.write(f.read())


def render(api_data):
    copy('style.css')
    copy('about.html')
    copy('donate.html')

    with open('src/index.jinja', 'r') as f:
        template = Template(f.read())
        with open('dist/index.html', 'w') as g:
            tz = pytz.timezone('US/Eastern')
            now = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
            g.write(template.render(api_data=api_data, last_updated=now))

    with open('src/coin.jinja', 'r') as f:
        template = Template(f.read())
        for coin in api_data['coins']:
            with open('dist/coins/{}.html'.format(coin['symbol']), 'w') as g:
                g.write(template.render(coin=coin))


if __name__ == '__main__':
    with open('dist/coins.json', 'r') as f:
        render(json.load(f))
