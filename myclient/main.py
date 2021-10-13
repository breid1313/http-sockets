# http client file

import argparse
import socket

# declare a constant with the HTTP version given in the assignment
HTTP_VERSION = 1.1

# constant buffer size
BUFF_SIZE = 1024


def parse_args():
    # instantiate an argument parser to gather the command line input
    parser = argparse.ArgumentParser(description="Make an HTTP request to a server.")

    # add the expected arguments
    parser.add_argument(
        "host",
        type=str,
        help="Host to which you would like to make a request",
    )
    parser.add_argument(
        "port",
        type=int,
        help="Port over which to make the request",
    )
    parser.add_argument("method", type=str, help="HTTP method to use")
    parser.add_argument(
        "filename",
        type=str,
        help="File to request from the server",
    )

    # parse the args from the command line
    return parser.parse_args()


def prepare_request(method: str, filename: str, host: str) -> str:
    return f"{method.upper()} {filename} HTTP/{HTTP_VERSION}\r\nHost: {host}\r\n\r\n"


def main():
    args = parse_args()

    # assign args to more friendly variables
    host = args.host
    port = args.port
    method = args.method
    filename = args.filename

    # instantiate a low-level networking client from the builtin socket library
    # the first argument defines the address family, and the second defines the socket type
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to the host over the desired port
    client.connect((host, port))

    # build the HTTP request message
    request = prepare_request(method, filename, host)
    print("Ready to send the following HTTP request:")
    print(request)

    # send the request to the server
    client.send(request.encode())
    print("Request sent!")

    if method.upper() == "PUT":
        # send the file to the server
        with open(filename, "r") as f:
            print(f"about to send {filename}...")

            # read in enough data to fill the buffer
            l = f.read(buff_size)

            # until the file has been entirely read...
            while l:
                print("sending...")
                # send the buffered data to the server
                client.send(l)
                # read more data into the buffer
                l = f.read(BUFF_SIZE)
        print("Done sending")
        # notify the server that we're done sending data
        s.shutdown(socket.SHUT_WR)

    # receive the response from the server
    response = client.recv(BUFF_SIZE)
    print("Response received!")
    print(response.decode("utf-8"))

    # close the socket once finished
    client.close()

    return response.decode()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
