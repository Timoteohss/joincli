import http.server
import socketserver
import json
import logging
from joincliHandler import handleMessage
import joincliUtils as ju



logger = logging.getLogger(__name__)
logging.basicConfig()
devices = ju.open_local_devices()

Handler = http.server.SimpleHTTPRequestHandler
PORT = 1820


class webServer(Handler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()

    def do_POST(self):
        self._set_headers()
        data = self.rfile.read()
        data_str = ju.decode_UTF8(data).replace("'", '"') #Get data from POST
        data = json.loads(json.loads(data_str)['json'])['push'] #dict this bitch
        s = json.dumps(data, sort_keys=True, indent=4)
        print(s) #print shit to be done
        handleMessage(data)
            
    def do_GET(self):
        self.send_response(403)
        self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Credentials', 'false')
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:1820')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")


def run(server_class=Handler, handler_class=webServer, port=PORT):
    try:
        logging.info("Listening on port %d for clients..." % port)
        server_address = ('',port)
        httpd = socketserver.TCPServer(server_address,handler_class)
        httpd.serve_forever()
    except KeyboardInterrupt:
        handleMessage(False)
        httpd.server_close()
        logger.info("Server terminated.")
    except Exception as e:
        handleMessage(False)
        logger.error(str(e), exc_info=True)
        exit(1)

if __name__ == "__main__":
    import sys

    if devices is not None:
        run()
    else:
        print("Devices not found!")
        print("Setup your eviroment first")
        sys.exit(1)

