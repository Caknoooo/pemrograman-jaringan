import sys
import unittest
import json
import socket
from io import StringIO
from unittest.mock import patch, MagicMock

def request_invalid_url():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('jsonplaceholder.typicode.com', 80))
        s.send(b"GET /invalidurl HTTP/1.1\r\nHost: jsonplaceholder.typicode.com\r\nConnection: close\r\n\r\n")
        response = s.recv(4096)
        if b"404 Not Found" in response:
            return "Request Failed"
        else:
            return "Request Succeeded"
        


# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass


def assert_equal(parameter1, parameter2):
    if parameter1 == parameter2:
        print(f'test attribute passed: {parameter1} is equal to {parameter2}')
    else:
        print(f'test attribute failed: {parameter1} is not equal to {parameter2}')


class TestInvalidUrlRequest(unittest.TestCase):
    @patch('socket.socket')
    def test_request_invalid_url(self, mock_socket):
        # Setup the mock socket
        mock_socket_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_socket_instance
        
        # Define a fake response to be returned by socket.recv
        fake_response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<html><body>404 Not Found</body></html>"
        mock_socket_instance.recv.return_value = fake_response.encode()

        # Call the function
        result = request_invalid_url()

        # Verify that the socket methods were called correctly
        mock_socket_instance.connect.assert_called_with(('jsonplaceholder.typicode.com', 80))
        print(f"connect called with: {mock_socket_instance.connect.call_args}")

        mock_socket_instance.send.assert_called_once()
        print(f"send called with: {mock_socket_instance.send.call_args}")

        mock_socket_instance.recv.assert_called_once()
        print(f"recv called with: {mock_socket_instance.recv.call_args}")
        
        assert_equal(result, "Request Failed")

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        status = request_invalid_url()
        print(status)

    # run unit test to test locally
    # or for domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)