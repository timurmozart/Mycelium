# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import socket
import time

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def client_tcp1(msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('myc-n1', 8000))
    # print(msg)
    print(type(msg))
    sndmsg = str.encode(msg)
    sock.send(sndmsg)
    sock.close()

def client_tcp2(msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('myc-n2', 8000))
    # print(msg)
    print(type(msg))
    sndmsg = str.encode(msg)
    sock.send(sndmsg)
    sock.close()

from flask import Flask, request #import main Flask class and request object
app = Flask(__name__) #create the Flask app
@app.route('/post-example', methods=['POST']) #GET requests will be blocked
def json_example():
    print('**************** start **********************')
    data = request.get_json()['data']
    # data = request.get_data().decode("utf-8")
    print(type(data))
    # print(data)
    
    # client_tcp1(data)
    # client_tcp2(data)
    print('***************** end **********************')
    return "got it"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) #run app in debug mode on port 5000


