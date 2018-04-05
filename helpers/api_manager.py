from helpers.common import generate_url, get, get_url
from helpers.constants import URLS


class ApiManager(object):
    def get_latest(self, fixer_app, url, error=False, **kwargs):

        body = {**kwargs}

        if not error:
            response = get(fixer_app, generate_url(url, filters=body))
            status_code = response.status_code
            assert status_code == 200, "Incorrect status code. Expected: 200, actual: %s" % status_code
        else:
            response = get_url(fixer_app, '{g}'.format(g=URLS[url] if url in URLS else "/" + url), expect_errors=True,
                               filters=body)
        return response


api_manager = ApiManager()
