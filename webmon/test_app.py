from collections import namedtuple
from unittest import TestCase
from unittest.mock import patch

from .app import check_website


class TestApp(TestCase):
    '''
    TODO: add tests to check return value in cases when requests.get raises an exception (e.g. timeout)
    '''
    def test_check_website(self):
        url='fake url'
        Test = namedtuple('Test', ['regexp', 'status_code', 'text', 'regexp_matched'])
        tt = [
            Test(regexp='def', status_code=200, text='abc def', regexp_matched=True),
            Test(regexp=None,  status_code=200, text='abc def', regexp_matched=None),
            Test(regexp='def', status_code=404, text='abc def', regexp_matched=None),
        ]
        for n, t in enumerate(tt):
            with patch('requests.get') as mock_requests_get:
                mock_requests_get.return_value.status_code = t.status_code
                mock_requests_get.return_value.text = t.text
                expected = {
                    'url': url,
                    'http_status_code': t.status_code,
                    'regexp': t.regexp,
                    'regexp_matched': t.regexp_matched,
                }
                actual = check_website(url, t.regexp)
                self.assertTrue(
                    set(expected.items()) <= set(actual.items()),
                    msg=f'\ntest #{n}\n\twant: {expected}\n\tgot: {actual}'
                )

