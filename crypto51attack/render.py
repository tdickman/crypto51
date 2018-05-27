import json
from jinja2 import Template


def render(results):
    with open('src/index.html', 'r') as f:
        template = Template(f.read())
        with open('dist/index.html', 'w') as g:
            g.write(template.render(results={'coins': results}))

    with open('src/coin.html', 'r') as f:
        template = Template(f.read())
        for details in results:
            with open('dist/coins/{}.html'.format(details['symbol']), 'w') as g:
                g.write(template.render(coin=details))


if __name__ == '__main__':
    with open('results.json', 'r') as f:
        render(json.load(f))
