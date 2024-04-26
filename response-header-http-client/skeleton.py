import sys
import unittest
from io import StringIO
from unittest.mock import patch, MagicMock
import http.client

def get_headers(response):
    return response.getheaders()

def get_server_header():
    conn = http.client.HTTPConnection('httpbin.org')
    conn.request("GET", '/response-headers?Content-Type=text/html&Server=Domjudge')
    response = conn.getresponse()
    headers = response.getheaders()
    conn.close()
    
    for header in headers:
        if header[0].lower() == 'server':
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


class TestGetServerHeader(unittest.TestCase):
    @patch('http.client.HTTPConnection')
    def test_get_server_header(self, mock_connection):
        # Mock the HTTPConnection object
        mock_conn = mock_connection.return_value
        
        # Mock the request method
        mock_request = mock_conn.request
        
        # Mock the getresponse method
        mock_response = mock_conn.getresponse.return_value
        
        # Set the headers of the mock response
        mock_response.getheaders.return_value = [('Server', 'MockServer')]
        
        # Call the function under test
        server_header = get_server_header()
        
        # Assert the connection was made with the correct arguments
        mock_connection.assert_called_once_with('httpbin.org')
        print(f"connection called with: {mock_connection.call_args}")
        
        # Assert the request was made with the correct arguments
        mock_request.assert_called_once_with("GET", '/response-headers?Content-Type=text/html&Server=Domjudge')
        print(f"request called with: {mock_connection.return_value.request.call_args}")
        
        # Assert the getresponse method was called
        mock_response.getheaders.assert_called_once()
        print(f"response headers: {mock_response.getheaders.return_value}")

        mock_connection.return_value.close.assert_called_once()
        print(f"connection closed: {mock_connection.return_value.close.call_args}")

        # Assert the result
        assert_equal(server_header, 'MockServer')

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        header = get_server_header()
        print(header)

    # run unit test to test locally
    # or for domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)