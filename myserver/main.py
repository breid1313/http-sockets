# http server file

import argparse
import socket
import os
import sys
from pathlib import Path
import time
import traceback

# declare a constant with the HTTP version given in the assignment
HTTP_VERSION = 1.1

# constant buffer size
BUFF_SIZE = 1024


def parse_args():
    # instantiate an argument parser to gather the command line input
    parser = argparse.ArgumentParser(description="Initialize an HTTP server.")

    # add the expected argument
    parser.add_argument(
        "port",
        type=int,
        help="Port to bind the server to",
    )

    # parse the args from the command line
    return parser.parse_args()


def return_file(connection, filename):
    asset = Path(__file__).parent / "static" / filename
    if not asset.is_file():
        message = f"HTTP/{HTTP_VERSION} 404 Not Found\r\n"
        dt = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        message += f"Date: {dt}\r\n"
        message += "Server: Python HTTP Socket Server\r\n"
        message += "Connection: close\r\n\r\n"

        print("sending 404")
        connection.send(message.encode())
        connection.close()
        print("closed connection")

        return

    message = f"HTTP/{HTTP_VERSION} 200 OK\r\n"
    dt = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    message += f"Date: {dt}\r\n"
    message += "Server: Python HTTP Socket Server\r\n"
    message += "Connection: close\r\n\r\n"

    with open(asset, "r") as f:
        lines = f.read()
    message += lines

    print("sending 200")
    connection.send(message.encode())
    connection.close()
    print("closed connection")

    return


def put_file(connection, filename, content):
    asset = Path(__file__).parent / "static" / filename
    
    created = True if not asset.is_file() else False

    # opening in w mode will delete the contents of the file before
    # writing, hence updating withe the new asset
    with open(asset, 'w') as f:
        f.write(content)

    message = f"HTTP/{HTTP_VERSION} 201 Content created\r\n" if created else message = f"HTTP/{HTTP_VERSION} 200 OK\r\n"
    dt = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    message += f"Date: {dt}\r\n"
    message += "Server: Python HTTP Socket Server\r\n"
    message += "Connection: close\r\n\r\n"

    print("sending 2xx")
    connection.send(message.encode())
    connection.close()
    print("closed connection")


def main():
    args = parse_args()

    # assign args to more friendly variables
    port = args.port

    # get host name
    host = socket.gethostname()

    # initialize the server socket, bind to the local machine on the desired port
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", port))

    # only allow 1 concurrent connection
    server.listen(1)
    print("server started at {}:{}".format(host, port))

    # TODO read until the data buffer is empty
    try:
        while True:
            connection, address = server.accept()
            print(f"received incoming connection from {repr(address)}.")

            data = connection.recv(BUFF_SIZE).decode("utf-8")
            method = data.split(" ")[0].upper()
            print("HTTP method: " + method)
            filename = data.split(" ")[1]
            print("file name: " + filename)

            if method == "GET":
                return_file(connection, filename)
    except Exception as e:
        # debug
        traceback.format_exc(e)
        
        # we had a problem... send a 500
        message = f"HTTP/{HTTP_VERSION} 500 Server Error\r\n"
        dt = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        message += f"Date: {dt}\r\n"
        message += "Server: Python HTTP Socket Server\r\n"
        message += "Connection: close\r\n\r\n"

        server.send(message.encode())
        server.close()

        # TODO write file for PUT
        # TODO send response for PUT


if __name__ == "__main__":
    sys.exit(main(sys.argv))
