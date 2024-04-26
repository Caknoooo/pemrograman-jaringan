import sys
from unittest.mock import patch, MagicMock
from io import StringIO
import unittest
import json
import socket

def fetch_comments():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
        conn.connect(('jsonplaceholder.typicode.com', 80))
        conn.send(b"GET /comments?postId=1 HTTP/1.1\r\nHost: jsonplaceholder.typicode.com\r\nConnection: close\r\n\r\n")
        response = conn.recv(4096)
        conn.close()

        response = response.decode()
        response = response.split("\r\n\r\n")[1]
        
        # Extract the comments from the response
        # remove 5e3 and 0 from the response
        data = json.loads(response[3:-1])
        
        # get postId
        postId = data[0]["postId"]
        return postId
        

    


# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass


def assert_equal(parameter1, parameter2):
    if parameter1 == parameter2:
        print(f'test attribute passed: {parameter1} is equal to {parameter2}')
    else:
        print(f'test attribute failed: {parameter1} is not equal to {parameter2}')


class TestCommentsFetcher(unittest.TestCase):
    @patch('socket.socket')
    def test_fetch_comments(self, mock_socket):
        # Setup mock socket
        mock_socket_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_socket_instance

        # Define the fake response to be returned by socket.recv
        fake_response = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n5e3[{\"postId\": 1, \"id\": 1, \"name\": \"Test Comment\"}]0"
        mock_socket_instance.recv.return_value = fake_response.encode()

        # Call the function
        result = fetch_comments()

        # Assertions to verify behavior and results
        mock_socket_instance.connect.assert_called_with(('jsonplaceholder.typicode.com', 80))
        print(f"connect called with: {mock_socket_instance.connect.call_args}")

        mock_socket_instance.send.assert_called_once()
        print(f"send called with: {mock_socket_instance.send.call_args}")
        
        mock_socket_instance.recv.assert_called_once()
        print(f"recv called with: {mock_socket_instance.recv.call_args}")

        assert_equal(result, 1)

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        comment = fetch_comments()
        print(comment)

    # run unit test to test locally
    # or for domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)