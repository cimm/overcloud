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
    #if len(sys.argv) != 2:
    #    print('Usage: python main.py <path_to_geopackage>')
    #    sys.exit(1)
    #geopackage_path = sys.argv[1]
    run_server()
