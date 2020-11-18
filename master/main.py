from flask import Flask
from flask import request


def Welcome_message(name):

    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def client_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(b'ebaaaaa', ('127.0.0.1', 8888))

def client_tcp(msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('myc-n', 8000))
    # print(msg)
    print(type(msg))
    sndmsg = str.encode(msg)
    sock.send(sndmsg)
    sock.close()

app = Flask(__name__)
@app.route('/post-example', methods=['POST'])
def json_example():
    print('**************** start **********************')
    # data = request.get_json()['data']
    data = request.get_data().decode("utf-8")
    # print(data)
    print(data)
    client_tcp(data)
    print('***************** end **********************')
    return "End"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) #run app in debug mode on port 5000


