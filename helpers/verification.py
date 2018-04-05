import pytest

from helpers.constants import FIELDS_TYPES, BASE_PARAMS, LENGTH, NOT_FOUND


def check_result(response, params=BASE_PARAMS, **kwargs):
    """Check response object with specified params"""
    status_code = response.status_code
    assert status_code == 200, "Incorrect status code. Expected: 200, actual: %s" % status_code
    for param in params:
        with pytest.allure.step('Check %s' % param):
            assert response.json[param], "Incorrect %s" % param
            assert type(response.json[param]) is FIELDS_TYPES[param], "Incorrect %s" % param
    for kwarg in kwargs:
        with pytest.allure.step('Check %s' % kwarg):
            if kwarg == 'length':
                assert len(response.json['rates']) == kwargs.get('length'), "Incorrect length"
            else:
                assert response.json[kwarg] == kwargs.get(kwarg), "Incorrect %s" % kwarg
                assert type(response.json[kwarg]) is FIELDS_TYPES[kwarg], "Incorrect %s" % kwarg


def check_in_rates(response, **kwargs):
    status_code = response.status_code
    assert status_code == 200, "Incorrect status code. Expected: 200, actual: %s" % status_code
    if len(kwargs.get('symbols')) > 1:
        for kwarg in kwargs.get('symbols'):
            with pytest.allure.step('Check %s' % kwarg):
                assert kwarg in response.json['rates'], "Incorrect %s" % kwarg
    elif len(kwargs.get('symbols')) == 1:
        assert kwargs.get('symbols')[0] in response.json['rates'], "Incorrect %s" % kwargs.get('symbols')[0]
    else:
        assert len(response.json['rates']) == LENGTH, "Incorrect length"


def check_not_in_rates(response, **kwargs):
    status_code = response.status_code
    assert status_code == 200, "Incorrect status code. Expected: 200, actual: %s" % status_code
    for kwarg in kwargs:
        with pytest.allure.step('Check %s' % kwarg):
            assert kwarg not in response.json['rates'], "Incorrect %s" % kwarg


def check_error(response, error):
        with pytest.allure.step('Check error %s' % error):
            assert error in response, "Incorrect %s" % error
            if error == NOT_FOUND:
                status_code = response.status_code
                assert status_code == 404, "Incorrect status code. Expected: 404, actual: %s" % status_code
            else:
                status_code = response.status_code
                assert status_code == 422, "Incorrect status code. Expected: 404, actual: %s" % status_code
