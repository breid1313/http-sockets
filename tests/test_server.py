import argparse
import unittest
import os
from unittest import mock
from pathlib import Path

from myclient.main import main as client_main


@mock.patch(
    "argparse.ArgumentParser.parse_args",
    return_value=argparse.Namespace(
        host="localhost", port=5678, method="GET", filename="index.html"  # client
    ),
)
def test_get_success(mock_args):
    response = client_main()
    return response


@mock.patch(
    "argparse.ArgumentParser.parse_args",
    return_value=argparse.Namespace(
        host="localhost", port=5678, method="GET", filename="foo.html"  # client
    ),
)
def test_get_404(mock_args):
    response = client_main()
    return response


@mock.patch(
    "argparse.ArgumentParser.parse_args",
    return_value=argparse.Namespace(
        host="localhost", port=5678, method="PUT", filename="test.txt"  # client
    ),
)
def test_put_success(mock_args):
    response = client_main()
    return response


class TestServer(unittest.TestCase):
    def test_success_get(self):
        success_result = test_get_success()
        status_code = int(success_result.split(" ")[1])
        self.assertEqual(status_code, 200)

    def test_fail_get(self):
        fail_result = test_get_404()
        status_code = int(fail_result.split(" ")[1])
        self.assertEqual(status_code, 404)

    def test_success_put(self):
        put_result = test_put_success()
        status_code = int(put_result.split(" ")[1])
        self.assertEqual(status_code, 201)

        new_path = Path(__file__).parent.parent / "myserver" / "static" / "test.txt"
        orig_path = Path(__file__).parent.parent / "myclient" / "static" / "test.txt"
        self.assertTrue(new_path.is_file())

        with open(new_path, "r") as f:
            new_data = f.read()
        with open(orig_path, "r") as f:
            orig_data = f.read()
        self.assertEqual(new_data, orig_data)

        # cleanup
        os.remove(new_path)


if __name__ == "__main__":
    unittest.main()

