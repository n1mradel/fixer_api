URLS = {
    'latest': '/latest',
    'incorrect': '/latest/test'
}

FIELDS_TYPES = {
    'base': str,
    'date': str,
    'rates': dict
}

BASE_PARAMS = ['base', 'date', 'rates']

LENGTH = 32

CURRENCY = ['AUD', 'BGN', 'BRL', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'GBP', 'HKD', 'HRK', 'HUF', 'IDR', 'ILS', 'INR',
            'ISK', 'JPY', 'KRW', 'MXN', 'MYR', 'NOK', 'NZD', 'PHP', 'PLN', 'RON', 'RUB', 'SEK', 'SGD', 'THB', 'TRY',
            'USD', 'ZAR']

# Errors:

NOT_FOUND = 'Not found'
INVALID_BASE = 'Invalid base'
