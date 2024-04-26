import sys
import unittest
from io import StringIO
from unittest import mock
import http.client


def get_redirect_location():
    conn = http.client.HTTPConnection('httpbin.org')
    conn.request("GET", '/redirect-to?url=http://example.com')
    response = conn.getresponse()
    headers = response.getheaders()
    conn.close()
    
    for header in headers:
        if header[0].lower() == 'location':
            return header[1]
    return None

# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass


def assert_equal(parameter1, parameter2):
    if parameter1 == parameter2:
        print(f'test attribute passed: {parameter1} is equal to {parameter2}')
    else:
        print(f'test attribute failed: {parameter1} is not equal to {parameter2}')


class TestGetRedirectLocation(unittest.TestCase):
    @mock.patch('http.client.HTTPConnection')
    def test_get_redirect_location(self, mock_http_connection):
        # Mock the HTTPConnection object
        mock_conn = mock_http_connection.return_value

        # Mock the response object
        mock_response = mock.Mock()
        mock_response.getheaders.return_value = [('Location', 'http://example.com')]
        mock_conn.getresponse.return_value = mock_response

        # Call the function
        result = get_redirect_location()

        # Assert that the HTTPConnection was called with the correct arguments
        mock_http_connection.assert_called_once_with('httpbin.org')
        print(f"connection called with: {mock_http_connection.call_args}")

        # Assert that the request was made with the correct arguments
        mock_conn.request.assert_called_once_with("GET", '/redirect-to?url=http://example.com')
        print(f"request called with: {mock_conn.request.call_args}")

        # Assert that the response headers were read
        mock_response.getheaders.assert_called_once()
        print(f"response headers: {mock_response.getheaders.return_value}")

        # Assert that the connection was closed
        mock_conn.close.assert_called_once()
        print(f"connection closed: {mock_conn.close.call_args}")

        # Assert the result
        assert_equal(result, 'http://example.com')

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        location = get_redirect_location()
        print(location)

    # run unit test to test locally
    # or for domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)