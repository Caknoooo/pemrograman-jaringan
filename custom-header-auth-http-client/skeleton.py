import sys
import unittest
from io import StringIO
from unittest import mock
import http.client


def send_get_request_with_custom_headers():
    conn = http.client.HTTPConnection("httpbin.org")
    conn.request("GET", "/headers", headers={
        'Authorization': 'Basic dXNlcjpwYXNz',
        'X-Custom-Header': 'Test123'
    })

    response = conn.getresponse()
    data = response.read()
    conn.close()

    # Parse the response
    data = data.decode()
    return data


# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass


def assert_equal(parameter1, parameter2):
    if parameter1 == parameter2:
        print(f'test attribute passed: {parameter1} is equal to {parameter2}')
    else:
        print(f'test attribute failed: {parameter1} is not equal to {parameter2}')


class TestSendGetRequestWithCustomHeaders(unittest.TestCase):
    @mock.patch('http.client.HTTPConnection')
    def test_send_get_request_with_custom_headers(self, mock_http_connection):
        # Create a mock HTTPConnection instance
        mock_conn = mock_http_connection.return_value

        # Create a mock HTTPResponse instance
        mock_response = mock.Mock()
        mock_response.read.return_value = b'Test Response'
        mock_conn.getresponse.return_value = mock_response

        # Call the function under test
        result = send_get_request_with_custom_headers()

        # Assert the expected behavior
        mock_http_connection.assert_called_once_with('httpbin.org')
        print(f"connection called with: {mock_http_connection.call_args}")

        mock_conn.request.assert_called_once_with("GET", "/headers", headers={
            'Authorization': 'Basic dXNlcjpwYXNz',
            'X-Custom-Header': 'Test123'
        })
        print(f"request called with: {mock_conn.request.call_args}")

        mock_response.read.assert_called_once()
        print(f"read called: {mock_response.read.return_value}")

        mock_conn.close.assert_called_once()
        print(f"connection closed: {mock_conn.close.call_args}")

        assert_equal(result, 'Test Response')

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        body = send_get_request_with_custom_headers()
        print(body)

    # run unit test to test locally
    # or for domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)