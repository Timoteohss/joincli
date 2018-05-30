import http.server
import socketserver
import json
import logging
from joincliHandler import handleMessage


logger = logging.getLogger(__name__)
logging.basicConfig()

Handler = http.server.SimpleHTTPRequestHandler
PORT = 1820

def try_decode_UTF8(data):
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        return False
    except Exception as e:
        raise(e)

class S(Handler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()

    def do_POST(self):
        self._set_headers()
        data = self.rfile.read()
        data_str = try_decode_UTF8(data).replace("'", '"') #Get data from POST
        data = json.loads(json.loads(data_str)['json'])['push'] #dict this bitch
        s = json.dumps(data, sort_keys=True, indent=4)
        print(s) #print shit to be done
        handleMessage(data)
            
    def do_GET(self):
        self.send_response(403)
        self.end_headers()
    
    def do_OPTIONS(self):
        self._set_headers()

def run(server_class=Handler, handler_class=S, port=PORT):
    try:
        logging.info("Listening on port %d for clients..." % port)
        server_address = ('',port)
        httpd = socketserver.TCPServer(server_address,handler_class)
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        logger.info("Server terminated.")
    except Exception as e:
        logger.error(str(e), exc_info=True)
        exit(1)



if __name__ == "__main__":
    from sys import argv

    run()

