from http.server import HTTPServer


class OverlandServer(HTTPServer):

    def __init__(self, server_address, RequestHandlerClass, token):
        super().__init__(server_address, RequestHandlerClass)
        self.token = token
