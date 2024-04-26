import sys
import unittest
import json
import socket
from io import StringIO
from unittest.mock import patch, MagicMock



def get_custom_header():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
        conn.connect(('httpbin.org', 80))
        conn.send(b"GET /headers HTTP/1.1\r\nHost: httpbin.org\r\nX-Test-Header: TestValue\r\nConnection: close\r\n\r\n")
        response = conn.recv(4096)
        conn.close()

        response = response.decode()
        response = response.split("\r\n\r\n")[1]
        data = json.loads(response)
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


class TestHeaderRequester(unittest.TestCase):
    @patch('socket.socket')
    def test_get_custom_header(self, mock_socket):
        # Setup the mock socket
        mock_socket_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_socket_instance
        
        # Define a fake response to be returned by socket.recv
        fake_response = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{\"headers\": {\"X-Test-Header\": \"TestValue\"}}"
        mock_socket_instance.recv.return_value = fake_response.encode()

        # Call the function
        test_header_value = get_custom_header()

        # Verify that the socket methods were called correctly
        mock_socket_instance.connect.assert_called_with(('httpbin.org', 80))
        print(f"connect called with: {mock_socket_instance.connect.call_args}")

        mock_socket_instance.send.assert_called_once()
        print(f"send called with: {mock_socket_instance.send.call_args}")

        mock_socket_instance.recv.assert_called_once()
        print(f"recv called with: {mock_socket_instance.recv.call_args}")

        assert_equal(test_header_value, "TestValue")


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        header_field = get_custom_header()
        print(header_field)

    # run unit test to test locally
    # or for domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)