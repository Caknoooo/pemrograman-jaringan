import sys
import unittest
from io import StringIO
from unittest import mock
import http.client
import json


def send_json_request():
    conn = http.client.HTTPConnection('httpbin.org')
    conn.request("POST", '/post', body=json.dumps({"name": "John Doe", "age": 30}), headers={
        "Content-Type": "application/json",
        "Content-Length": str(len(json.dumps({"name": "John Doe", "age": 30})))
    })
    response = conn.getresponse()
    body = response.read().decode()
    conn.close()
    return body


# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass


def assert_equal(parameter1, parameter2):
    if parameter1 == parameter2:
        print(f'test attribute passed: {parameter1} is equal to {parameter2}')
    else:
        print(f'test attribute failed: {parameter1} is not equal to {parameter2}')


class TestSendJsonRequest(unittest.TestCase):
    @mock.patch('http.client.HTTPConnection')
    def test_send_json_request(self, mock_http_connection):
        # Mock the HTTPConnection object
        mock_conn = mock_http_connection.return_value

        # Set up the expected data, headers, host, and path
        expected_data = json.dumps({"name": "John Doe", "age": 30})
        expected_content_length = len(expected_data)
        expected_headers = {
            "Content-Type": "application/json",
            "Content-Length": str(expected_content_length)
        }
        expected_host = 'httpbin.org'
        expected_path = '/post'

        # Set up the expected response
        expected_response_body = 'Mock response body'
        expected_response = mock.Mock()
        expected_response.read.return_value.decode.return_value = expected_response_body
        mock_conn.getresponse.return_value = expected_response

        # Call the function
        response_body = send_json_request()

        # Assert that the HTTPConnection was called with the expected arguments
        mock_http_connection.assert_called_once_with(expected_host)
        print(f"connection called with: {mock_http_connection.call_args}")

        # Assert that the request was sent with the expected arguments
        mock_conn.request.assert_called_once_with("POST", expected_path, body=expected_data, headers=expected_headers)
        print(f"request called with: {mock_conn.request.call_args}")

        # Assert that the response was read and decoded
        expected_response.read.assert_called_once()
        expected_response.read.return_value.decode.assert_called_once()
        print(f"read called: {expected_response.read.return_value.decode.return_value}")

        # Assert that the connection was closed
        mock_conn.close.assert_called_once()
        print(f"connection closed: {mock_conn.close.call_args}")

        # Assert that the response body is returned
        assert_equal(response_body, expected_response_body)

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        body = send_json_request()
        print(body)

    # run unit test to test locally
    # or for domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)