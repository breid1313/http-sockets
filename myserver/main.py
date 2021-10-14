# http server file

import argparse
import socket
import sys
from pathlib import Path
import time


# declare a constant with the HTTP version given in the assignment
HTTP_VERSION = 1.1

# constant buffer size
BUFF_SIZE = 1024


def parse_args():
    # instantiate an argument parser to gather the command line input
    parser = argparse.ArgumentParser(description="Initialize an HTTP server.")

    # add the expected argument
    parser.add_argument(
        "port", type=int, help="Port to bind the server to",
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

    # does the file already exist?
    created = True if not asset.is_file() else False

    # opening in w mode will delete the contents of the file before
    # writing, hence updating with the new asset
    with open(asset, "w") as f:
        f.write(content)

    # craft our response message, change the status code depending
    # on whether or not we created a new file or updated an existing one
    message = (
        f"HTTP/{HTTP_VERSION} 201 Content created\r\n"
        if created
        else f"HTTP/{HTTP_VERSION} 200 OK\r\n"
    )
    dt = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    message += f"Date: {dt}\r\n"
    message += "Server: Python HTTP Socket Server\r\n"
    message += "Connection: close\r\n\r\n"

    print("sending 2xx")
    connection.send(message.encode())
    connection.close()
    print("closed connection")

    return


def receive_data(connection):
    """Receive 'chunks' of data from the client into a buffer until the
    data stops coming in. Then join the chunks to obtain the original
    data string that was sent.
    """
    chunks = []
    chunks.append(connection.recv(BUFF_SIZE).decode("utf-8"))
    while True:
        try:
            data = connection.recv(BUFF_SIZE).decode("utf-8")
            if not data:
                break
            chunks.append(data)
        except:
            raise
    return "".join(chunks)


def main():
    args = parse_args()

    # assign args to more friendly variables
    port = args.port

    # get host name
    # we don't actually use this... if we call bind() with the host name that
    # we just gathered, its a little more tricky to connect to the socket in
    # that the HTTP request needs to have the hostname (brians-air.comcast....)
    # but if we pass bind() and empty string, we're also able to connect to the
    # socket by passing localhost as the hostname
    host = socket.gethostname()

    # instantiate a low-level networking client from the builtin socket library
    # the first argument defines the address family, and the second defines the socket type
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # allow us to reconnect if the process is killed
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("", port))

    # only allow 1 concurrent connection
    server.listen(1)
    print("server started at {}:{}".format(host, port))

    while True:
        try:
            # accept an incoming connection
            connection, address = server.accept()
            print(f"received incoming connection from {repr(address)}.")

            # receive all data from the client
            data = receive_data(connection, server)

            # parse the HTTP method and filename from the incoming message
            method = data.split(" ")[0].upper()
            filename = data.split(" ")[1]

            if method == "GET":
                # send a message back with the desired file or 404
                return_file(connection, filename)

            if method == "PUT":
                # get the file data from the request
                content = data.split("\r\n\r\n")[1]
                # try to write the file data and return a response message
                put_file(connection, filename, content)

        except Exception:
            # we had a problem... send a 500
            message = f"HTTP/{HTTP_VERSION} 500 Server Error\r\n"
            dt = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
            message += f"Date: {dt}\r\n"
            message += "Server: Python HTTP Socket Server\r\n"
            message += "Connection: close\r\n\r\n"

            connection.send(message.encode())
            connection.close()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
