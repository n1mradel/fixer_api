import pytest


from urllib.parse import urlencode
from helpers.constants import URLS
from faker import Faker

fake = Faker()


def get_date():
    return fake.date_this_month(after_today=True)


def generate_params(**kwargs):
    filters = urlencode({k: ','.join(v) if (isinstance(v, set) or isinstance(v, list)) else v
                         for k, v in kwargs.get('filters', {}).items()})

    if filters:
        get_params = '?' + filters
    else:
        get_params = ''
    return get_params


def get_url(app, url, expect_errors=False, **kwargs):
    pytest.allure.attach('url', app.app.uri + url)
    url += generate_params(**kwargs)
    return app.get(url, expect_errors=expect_errors)


def generate_url(name, **kwargs):
    get_params = generate_params(**kwargs)
    return URLS[name] + get_params if name in URLS else "/" + name + get_params


def get(app, url, **kwargs):
    pytest.allure.attach(
        'curl',
        "curl -X GET '%s'" % (app.app.uri + url)
    )
    return app.get(url, expect_errors=kwargs.get('expect_errors', False))