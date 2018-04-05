import pytest
import random

from helpers.api_manager import api_manager
from helpers.common import get_date
from helpers.constants import LENGTH, NOT_FOUND, CURRENCY, INVALID_BASE
from helpers.verification import check_result, check_error, check_not_in_rates, check_in_rates


@pytest.allure.feature('Money value')
@pytest.mark.categories(component='currency')
class TestFixerCurrency:

    _DATE = get_date()

    @pytest.mark.parametrize('url', ('latest', str(_DATE)))
    def test_fixer_without_params(self, fixer_app, url):
        with pytest.allure.step('Get data'):
            response = api_manager.get_latest(fixer_app, url)
        with pytest.allure.step('Check response'):
            check_result(response, length=LENGTH)

    @pytest.mark.parametrize('url', ('latest', str(_DATE)))
    def test_fixer_with_base_param(self, fixer_app, url):
        with pytest.allure.step('Get data'):
            base = random.choice(CURRENCY)
            response = api_manager.get_latest(fixer_app, url, base=base)
        with pytest.allure.step('Check response'):
            check_result(response, length=LENGTH)
        with pytest.allure.step('Check %s not in rates' % base):
            check_not_in_rates(response, params=base)

    @pytest.mark.parametrize('url', ('latest', str(_DATE)))
    def test_fixer_with_symbols_param(self, fixer_app, url):
        with pytest.allure.step('Get data'):
            symbols = [random.choice(CURRENCY)]
            response = api_manager.get_latest(fixer_app, url, symbols=symbols)
        with pytest.allure.step('Check response'):
            check_in_rates(response, symbols=symbols)

    @pytest.mark.parametrize('url', ('latest', str(_DATE)))
    def test_fixer_all_params(self, fixer_app, url):
        with pytest.allure.step('Get data'):
            base = random.choice(CURRENCY)
            symbols = [random.choice(CURRENCY)]
            response = api_manager.get_latest(fixer_app, url, base=base, symbols=symbols)
        with pytest.allure.step('Check response'):
            check_in_rates(response, base=base, symbols=symbols)

    @pytest.mark.parametrize('url', ('latest', str(_DATE)))
    def test_fixer_many_symbols(self, fixer_app, url):
        with pytest.allure.step('Get data'):
            base = random.choice(CURRENCY)
            symbols = random.sample(set(CURRENCY), 3)
            response = api_manager.get_latest(fixer_app, url, base=base, symbols=symbols)
        with pytest.allure.step('Check response'):
            check_in_rates(response, base=base, symbols=symbols)

    def test_fixer_incorrect_url(self, fixer_app):
        with pytest.allure.step('Get test cart'):
            url = 'incorrect'
            response = api_manager.get_latest(fixer_app, error=True, url=url)
        with pytest.allure.step('Check response'):
            check_error(response, NOT_FOUND)

    @pytest.mark.parametrize('url', ('latest', str(_DATE)))
    def test_fixer_incorrect_base(self, fixer_app, url):
        with pytest.allure.step('Get test cart'):
            base = 'test'
            response = api_manager.get_latest(fixer_app, url, error=True, base=base)
        with pytest.allure.step('Check response'):
            check_error(response, INVALID_BASE)

    def test_fixer_incorrect_symbols(self):
        pytest.skip('Not implemented.')

    def test_fixer_default_base(self):
        pytest.skip('Not implemented.')

    def test_fixer_random_params(self):
        pytest.skip('Not implemented.')

    def test_fixer_same_base_and_symbols_value(self):
        pytest.skip('Not implemented.')






