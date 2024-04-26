import http.client
import json
import sys
import unittest
from io import StringIO
from unittest import mock
from urllib.parse import urlencode

def post_comment():
    conn = http.client.HTTPSConnection("jsonplaceholder.typicode.com")
    conn.request("POST", "/comments", body=urlencode({
        'postId': 1,
        'name': 'Test Name',
        'email': 'test@example.com',
        'body': 'This is a test comment.'
    }), headers={'Content-Type': 'application/x-www-form-urlencoded'})
    response = conn.getresponse()
    data = response.read()
    conn.close()

    # Parse the response
    data = data.decode()
    data = json.loads(data)
    comment_id = data["id"]
    return comment_id

# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass


def assert_equal(parameter1, parameter2):
    if parameter1 == parameter2:
        print(f'test attribute passed: {parameter1} is equal to {parameter2}')
    else:
        print(f'test attribute failed: {parameter1} is not equal to {parameter2}')


class TestPostComment(unittest.TestCase):
    @mock.patch('http.client.HTTPSConnection')
    def test_post_comment(self, mock_connection):
        # Mock the HTTP connection
        mock_conn = mock.Mock()
        mock_connection.return_value = mock_conn

        # Mock the response
        mock_response = mock.Mock()
        mock_response.read.return_value = b'{"id": 1}'
        mock_conn.getresponse.return_value = mock_response

        # Call the function
        comment_id = post_comment()

        # Assertions
        assert_equal(comment_id, 1)

        mock_connection.assert_called_once_with("jsonplaceholder.typicode.com")
        print(f"connection called with: {mock_connection.call_args}")

        mock_conn.request.assert_called_once_with(
            "POST",
            "/comments",
            body=urlencode({
                'postId': 1,
                'name': 'Test Name',
                'email': 'test@example.com',
                'body': 'This is a test comment.'
            }),
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        print(f"request called with: {mock_conn.request.call_args}")

        mock_response.read.assert_called_once()
        print(f"read called: {mock_response.read.return_value}")

        mock_conn.close.assert_called_once()
        print(f"connection closed: {mock_conn.close.call_args}")


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        comments = post_comment()
        print(comments)

    # run unit test to test locally
    # or for domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)