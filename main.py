from http.server import HTTPServer
from ip_address import IpAddress
from overland_request_handler import OverlandRequestHandler
import os
import sys

HOSTNAME = IpAddress.local()
PORT = 4567


def run_server():
    server = HTTPServer((HOSTNAME, PORT), OverlandRequestHandler)
    print("Server started http://%s:%s" % (HOSTNAME, PORT))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()


if __name__ == '__main__':
    run_server()
