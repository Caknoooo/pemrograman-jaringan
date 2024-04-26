import http.client
import json
import sys
import unittest
from io import StringIO
from unittest import mock



def get_title():
    conn = http.client.HTTPSConnection("jsonplaceholder.typicode.com")
    conn.request("GET", "/posts/1")
    response = conn.getresponse()
    data = response.read()
    conn.close()

    # Parse the response
    data = data.decode()
    data = json.loads(data)
    title = data["title"]
    return title

# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass


def assert_equal(parameter1, parameter2):
    if parameter1 == parameter2:
        print(f'test attribute passed: {parameter1} is equal to {parameter2}')
    else:
        print(f'test attribute failed: {parameter1} is not equal to {parameter2}')


class TestSolution(unittest.TestCase):
    @mock.patch('http.client.HTTPSConnection')
    def test_get_title(self, mock_conn):
        # Mock the response
        mock_response = mock.Mock()
        mock_response.read.return_value = b'{"title": "Sample Title"}'
        mock_conn.return_value.getresponse.return_value = mock_response

        # Call the function under test
        result = get_title()

        # Assert the HTTP connection is called with the correct arguments
        mock_conn.assert_called_once_with("jsonplaceholder.typicode.com")
        print(f"connection called with: {mock_conn.call_args}")

        mock_conn.return_value.request.assert_called_once_with("GET", "/posts/1")
        print(f"request called with: {mock_conn.return_value.request.call_args}")

        mock_response.read.assert_called_once()
        print(f"read called: {mock_response.read.return_value}")

        # Assert the expected result
        assert_equal(result, "Sample Title")


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        title = get_title()
        print(title)

    # run unit test to test locally
    # or for domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)