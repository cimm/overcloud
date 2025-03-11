from geopackage import GeoPackage
from http.server import BaseHTTPRequestHandler
from shapely.geometry import Point
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
            json_data = json.loads(body.decode(self.encoding))
            self.store(json_data)
            #self.send_response(200)
            self.send_response(
                400)  # FIXME: don't want to loose the client data for now
            self.send_header('Content-type', self.content_type)
            self.end_headers()
            self.wfile.write(
                json.dumps({
                    "result": "OK"
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

        # FIXME: Add authentication

        return True

    def store(self, json_data):
        # FIXME: Can this move to main?
        path = "locdb.gpkg"
        geopackage = GeoPackage(path, 'locations')
        locations = {'geometry': [], 'timestamp': []}

        #if os.path.exists(path):
        #    print(f'File `{path}` already exists')
        #    sys.exit(1)

        for record in json_data['locations']:
            point = Point(record['geometry']['coordinates'])
            locations['geometry'].append(point)
            timestamp = record['properties']['timestamp']
            locations['timestamp'].append(timestamp)

        geopackage.add_locations_to_layer(locations)
