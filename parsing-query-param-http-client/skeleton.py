import http.client
import json
import sys
import unittest
from io import StringIO
from unittest import mock

def get_comments():
    conn = http.client.HTTPSConnection("jsonplaceholder.typicode.com")
    conn.request("GET", "/comments?postId=1")
    response = conn.getresponse()
    data = response.read()
    conn.close()

    # Parse the response
    data = data.decode()
    data = json.loads(data)
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


class TestSolution(unittest.TestCase):
    @mock.patch('http.client.HTTPSConnection')
    def test_get_comments(self, mock_conn):
        # Mock the response
        mock_response = mock.Mock()
        mock_response.status = 200
        mock_response.read.return_value = b'[{"postId": 1, "id": 1, "name": "John Doe", "email": "johndoe@example.com", "body": "Great post!"}]'
        mock_conn.return_value.getresponse.return_value = mock_response

        # Call the function to be tested
        comments = get_comments()

        # Assertions
        assert_equal(len(comments), 1)
        assert_equal(comments[0]['postId'], 1)
        assert_equal(comments[0]['id'], 1)
        assert_equal(comments[0]['name'], "John Doe")
        assert_equal(comments[0]['email'], "johndoe@example.com")
        assert_equal(comments[0]['body'], "Great post!")

        # Assert the HTTP connection is called with the correct arguments
        mock_conn.assert_called_once_with("jsonplaceholder.typicode.com")
        print(f"connection called with: {mock_conn.call_args}")

        mock_conn.return_value.request.assert_called_once_with("GET", "/comments?postId=1")
        print(f"request called with: {mock_conn.return_value.request.call_args}")

        mock_response.read.assert_called_once()
        print(f"read called: {mock_response.read.return_value}")

        conn_close = mock_conn.return_value.close
        conn_close.assert_called_once()
        print(f"connection closed: {conn_close.call_args}")


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        comments = get_comments()
        print(comments)

    # run unit test to test locally
    # or for domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)