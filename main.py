from overland_server import OverlandServer
from overland_request_handler import OverlandRequestHandler
import argparse


def run_server():
    server = OverlandServer((args.host, args.port), OverlandRequestHandler,
                            args.token)
    if args.token:
        auth_msg = ", requiring authorization"
    else:
        auth_msg = " WITHOUT authorization"
    print("Server listening at http://%s:%s%s" %
          (args.host, args.port, auth_msg))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Overcloud, an Overland backend")
    parser.add_argument("--host",
                        nargs="?",
                        type=str,
                        default="localhost",
                        help="The host address the server will bind to.")
    parser.add_argument("--port",
                        nargs="?",
                        type=int,
                        default=4567,
                        help="The port the server will listen on.")
    parser.add_argument("--token",
                        nargs="?",
                        type=str,
                        help="The token used for authentication.")
    args = parser.parse_args()

    run_server()
