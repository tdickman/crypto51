import json
from jinja2 import Template


def render(api_data):
    with open('src/style.css', 'r') as f:
        with open('dist/style.css', 'w') as g:
            g.write(f.read())

    with open('src/about.jinja', 'r') as f:
        with open('dist/about.html', 'w') as g:
            g.write(f.read())

    with open('src/index.jinja', 'r') as f:
        template = Template(f.read())
        with open('dist/index.html', 'w') as g:
            g.write(template.render(api_data=api_data))

    with open('src/coin.jinja', 'r') as f:
        template = Template(f.read())
        for coin in api_data['coins']:
            with open('dist/coins/{}.html'.format(coin['symbol']), 'w') as g:
                g.write(template.render(coin=coin))


if __name__ == '__main__':
    with open('dist/coins.json', 'r') as f:
        render(json.load(f))
