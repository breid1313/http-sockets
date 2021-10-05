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
def test_external(mock_args):
    return main()


@mock.patch(
    "argparse.ArgumentParser.parse_args",
    return_value=argparse.Namespace(
        host="localhost", port=6131, method="GET", filename="index.html"
    ),
)
def test_internal(mock_args):
    return main()


class TestClient(unittest.TestCase):
    # test that we get a 200 OK at the beginning of the response from the external server
    def test_ok_external(self):
        self.assertEqual(test_external().find("HTTP/1.1 200 OK"), 0)

    # test that we get a 200 OK at the beginning of the response from the internal server
    def test_ok_internal(self):
        self.assertEqual(test_internal().find("HTTP/1.1 200 OK"), 0)


if __name__ == "__main__":
    unittest.main()
