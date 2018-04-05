import re
import webtest
import pytest

from allure.constants import Severity as AllureSeverity


class Severity(object):
    CRITICAL = AllureSeverity.CRITICAL
    MAJOR = AllureSeverity.NORMAL
    MINOR = AllureSeverity.MINOR


def pytest_addoption(parser):
    parser.addoption('--fixer_url', action='store', default='http://api.fixer.io', help='url for fixer api test')
    parser.addoption('--categories', action='store', metavar='NAME', help='only run tests matches with categories')


@pytest.fixture
def fixer_app():
    return webtest.TestApp(pytest.config.getoption("--fixer_url"))


def pytest_collection_modifyitems(session, config, items):
    """
    Skip tests, which  not satisfying categories param
    :param session: Current session
    :param config: pytest.ini
    :param items: all founded tests
    :return: tests, which satisfy 'categories' param
    """
    market_categories = config.option.categories
    if not market_categories or market_categories == 'all':
        return

    # Transform argument string, like 'known_bugs,component=debug'
    # to dict {'known_bugs': 'known_bugs, 'component':'debug'}
    categories_filter = [x.split('=') for x in market_categories.split(',')]
    categories_filter = [tuple(x.strip() for x in y) for y in categories_filter]
    categories_filter = dict([x * 2 if len(x) == 1 else x for x in categories_filter])

    if not categories_filter:
        return

    selected = []
    deselected = []
    for item in items:
        markers_on_tests = item.get_marker('categories')

        if not markers_on_tests:
            deselected.append(item)
            continue
        else:
            test_markers = markers_on_tests.kwargs
            test_markers_string = markers_on_tests.args or ()

        if len(markers_on_tests._arglist) == 2:
            # Merge test markers in class markers (rewrite)
            test_markers.update(markers_on_tests._arglist[0][1])

        found = False
        for category_filter in categories_filter:
            filtered_value = categories_filter[category_filter]

            if filtered_value == category_filter:
                if any([_ in filtered_value for _ in ('not ', 'not_')]):
                    if re.sub('not[\s_]', '', filtered_value) in test_markers_string:
                        # We dont want run these tests
                        deselected.append(item)
                        found = True
                        break
                else:
                    # We want run these tests
                    if filtered_value not in test_markers_string:
                        deselected.append(item)
                        found = True
                        break
            else:
                if not test_markers.get(category_filter):
                    deselected.append(item)
                    found = True
                    break

                if test_markers.get(category_filter) and filtered_value not in test_markers.get(category_filter):
                    deselected.append(item)
                    found = True
                    break

        if not found:
            selected.append(item)
    if deselected:
        config.hook.pytest_deselected(items=deselected)
        items[:] = selected
