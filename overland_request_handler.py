from geopackage import GeoPackage
from http.server import BaseHTTPRequestHandler
import json


class OverlandRequestHandler(BaseHTTPRequestHandler):
    content_type = 'application/json'
    encoding = 'utf-8'

    def do_GET(self):
        self.send_error(405, 'Method Not Allowed')

    def do_POST(self):
        if not self.valid_request():
            return

        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        try:
            overland_json = json.loads(body.decode(self.encoding))
            self.store(overland_json)
            self.send_response(200)
            self.send_header('Content-type', self.content_type)
            self.end_headers()
            self.wfile.write(
                json.dumps({
                    "result": "ok"
                }).encode(self.encoding))
        except json.JSONDecodeError:
            self.send_error(400, 'Invalid JSON')

    def valid_request(self):
        if self.headers.get('Content-Type') != self.content_type:
            self.send_error(415, 'Content-Type Not Allowed')
            return False

        if self.headers.get('User-Agent').lower() in 'overland':
            self.send_error(403, 'User-Agent Not Allowed')
            return False

        auth_header = self.headers.get('Authorization')
        if auth_header and auth_header.startswith(
                'Bearer ') and self.server.token:
            token = auth_header.split(' ')[1]
            return token == self.server.token

        return True

    # FIXME: Can this method move to main?
    def store(self, overland_json):
        geopackage = GeoPackage('locdb.gpkg', 'locations')
        frames = []
        for location in overland_json['locations']:
            frame = geopackage.json_to_frame(location)
            frames.append(frame)
        geopackage.save_frames_to_file(frames)
