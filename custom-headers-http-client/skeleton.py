import http.client
import json
import sys
import unittest
from io import StringIO
from unittest import mock


def send_get_request_with_custom_header():
    conn = http.client.HTTPSConnection("httpbin.org")
    conn.request("GET", "/headers", headers={'X-Test-Header': 'TestValue'})
    response = conn.getresponse()
    data = response.read()
    conn.close()

    # Parse the response
    data = data.decode()
    data = json.loads(data)
    headers = data["headers"]
    return headers["X-Test-Header"]


# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass


def assert_equal(parameter1, parameter2):
    if parameter1 == parameter2:
        print(f'test attribute passed: {parameter1} is equal to {parameter2}')
    else:
        print(f'test attribute failed: {parameter1} is not equal to {parameter2}')


class TestSendGetRequestWithCustomHeader(unittest.TestCase):
    @mock.patch('http.client.HTTPSConnection')
    def test_send_get_request_with_custom_header(self, mock_conn):
        # Mock the HTTP connection
        mock_response = mock.Mock()
        mock_response.read.return_value = b'{"headers": {"X-Test-Header": "TestValue"}}'
        mock_conn.return_value.getresponse.return_value = mock_response

        # Call the function
        result = send_get_request_with_custom_header()

        mock_conn.assert_called_once_with("httpbin.org")
        print(f"connection called with: {mock_conn.call_args}")

        # Assert request method was called with correct arguments
        mock_conn.return_value.request.assert_called_once_with('GET', '/headers', headers={'X-Test-Header': 'TestValue'})
        print(f"request called with: {mock_conn.return_value.request.call_args}")

        mock_response.read.assert_called_once()
        print(f"read called: {mock_response.read.return_value}")

        conn_close = mock_conn.return_value.close
        conn_close.assert_called_once()
        print(f"connection closed: {conn_close.call_args}")

        # Assert the result
        assert_equal(result, 'TestValue')


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        comments = send_get_request_with_custom_header()
        print(comments)

    # run unit test to test locally
    # or for domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)