def get_pretty_hash_rate(hash_rate):
    """Convert the given hash rate to a pretty value."""
    if hash_rate > (1000.0 ** 5):
        return '{:,.0f} PH/s'.format(hash_rate / (1000.0 ** 5))
    elif hash_rate > (1000.0 ** 4):
        return '{:,.0f} TH/s'.format(hash_rate / (1000.0 ** 4))
    elif hash_rate > (1000.0 ** 3):
        return '{:,.0f} GH/s'.format(hash_rate / (1000.0 ** 3))
    elif hash_rate > (1000.0 ** 2):
        return '{:,.0f} MH/s'.format(hash_rate / (1000.0 ** 2))
    elif hash_rate > (1000.0 ** 1):
        return '{:,.0f} KH/s'.format(hash_rate / (1000.0 ** 1))
    else:
        return '{:,.0f} H/s'.format(hash_rate / (1000.0 ** 0))


def get_pretty_money(value):
    """Conver the number to a pretty dollar value with units."""
    if value is None:
        return '-'
    elif value > (1000.0 ** 4):
        return '${:,.2f} T'.format(value / (1000.0 ** 4))
    elif value > (1000.0 ** 3):
        return '${:,.2f} B'.format(value / (1000.0 ** 3))
    elif value > (1000.0 ** 2):
        return '${:,.2f} M'.format(value / (1000.0 ** 2))
    elif value > (1000.0 ** 0):
        return '${:,.0f}'.format(value)
