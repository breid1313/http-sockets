import sys
import argparse
import unittest
from unittest import mock
from myclient.main import main


@mock.patch(
    "argparse.ArgumentParser.parse_args",
    return_value=argparse.Namespace(
        host="www.cnn.com", port=80, method="GET", filename="index.html"
    ),
)
def test_external_get(mock_args):
    return main()


@mock.patch(
    "argparse.ArgumentParser.parse_args",
    return_value=argparse.Namespace(
        host="localhost", port=5678, method="GET", filename="index.html"
    ),
)
def test_internal_get(mock_args):
    return main()


@mock.patch(
    "argparse.ArgumentParser.parse_args",
    return_value=argparse.Namespace(
        host="localhost", port=5678, method="PUT", filename="test.txt"
    ),
)
def test_internal_put(mock_args):
    return main()


class TestClient(unittest.TestCase):
    # test that we get a 200 OK at the beginning of the response from the external server
    def test_get_external(self):
        self.assertEqual(test_external_get().find("HTTP/1.1 200 OK"), 0)

    # test that we get a 200 OK at the beginning of the response from the internal server
    # this will obviously fail if the server is not running on localhost
    def test_get_internal(self):
        self.assertEqual(test_internal_get().find("HTTP/1.1 200 OK"), 0)

    # test that we get a 2xx from the internal server for a PUT request
    # this will obviously fail if the server is not running on localhost
    def test_put_internal(self):
        self.assertIn(int(test_internal_put().split(" ")[1]), [200, 201, 204])


if __name__ == "__main__":
    unittest.main()
