from http.server import HTTPServer, BaseHTTPRequestHandler
# import urlparser

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        post_body = self.rfile.read1()
        print(post_body)

def run(server_class=HTTPServer, handler_class=RequestHandler):
    server_address = ('192.168.1.231', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


run()
