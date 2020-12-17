#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler
import socketserver as SocketServer
import socket
import threading
import json
import sys
import config


class CountDownLatch:
    def __init__(self, count=1):
        self.count = count
        self.lock = threading.Condition()

    def count_down(self):
        try:
            self.lock.acquire()
            self.count -= 1
            if self.count <= 0:
                self.lock.notifyAll()
        finally:
            self.lock.release()

    def wait(self):
        try:
            self.lock.acquire()
            while self.count > 0:
                self.lock.wait()
        finally:
            self.lock.release()


def send_to_secondary(msg, node_details, ack_dict):

    host = node_details[0]
    port = node_details[1]
    node_index = node_details[2]
    print('Sending to a secondary node {} ...'.format(node_index))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.sendall(msg.encode())
    response = sock.recv(1024)
    acknowledgement = response.decode('utf-8')
    print('ACK from the secondary node {}:'.format(node_index), acknowledgement)
    ack_dict[node_index] = acknowledgement
    sock.close()


def run_thread_with_count(params):
    print('Thread: ' + str(params[1]) + ':' + str(params[2]) + " is running")
    send_to_secondary(params[0], params[1:4], params[4])
    print('Thread: ' + str(params[1]) + ':' + str(params[2]) + " is finished")
    params[5].count_down()


class CustomHandler(BaseHTTPRequestHandler):

    # def send_to_secondary(self, msg, host, port, node_index):
    #     print('Sending to a secondary node {} ...'.format(node_index))
    #     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     sock.connect((host, port))
    #     sock.sendall(msg.encode())
    #     response = sock.recv(1024)
    #     acknowledgement = response.decode('utf-8')
    #     print('ACK from the secondary node {}:'.format(node_index), acknowledgement)
    #     sock.close()
    #     return acknowledgement

    def do_GET(self):
        global server_data
        if self.path == '/list':
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            if server_data == []:
                self.wfile.write(bytes(str('No data on server'), encoding='utf-8'))
            else:
                for m in server_data:
                    self.wfile.write(bytes(str(m) + ' ', encoding='utf-8'))
            print('Saved data on the server: ', server_data)

    def do_POST(self):
        global server_data
        global HOST_secondaty_1, HOST_secondaty_2
        global PORT_secondaty_12, PORT_secondaty_22
        if self.path == '/append':
            self.data_string = self.rfile.read(int(self.headers['Content-Length']))
            data = json.loads(self.data_string)
            new_message = data['msg']
            write_concern = data['write_concern']
            server_data.append(new_message)
            print('Appended new message:', new_message)
            print('Write concern', write_concern)
            replies_from_nodes = write_concern - 1
            acknolegment = {}
            countDownLatch = CountDownLatch(replies_from_nodes)
            if write_concern == 1:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(bytes('Appended new message:' + str(new_message), encoding='utf-8'))
                for tuple_params in [(new_message, HOST_secondaty_1, PORT_secondaty_12, 1, acknolegment, countDownLatch),
                         (new_message, HOST_secondaty_2, PORT_secondaty_22, 2, acknolegment, countDownLatch)]:
                    threading.Thread(target=run_thread_with_count, args=(tuple_params,)).start()
            else:
                for tuple_params in [(new_message, HOST_secondaty_1, PORT_secondaty_12, 1, acknolegment, countDownLatch),
                         (new_message, HOST_secondaty_2, PORT_secondaty_22, 2, acknolegment, countDownLatch)]:
                    threading.Thread(target=run_thread_with_count, args=(tuple_params,)).start()
                countDownLatch.wait()
                if len(acknolegment) == replies_from_nodes:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(bytes('Appended new message:' + str(new_message), encoding='utf-8'))
                else:
                    print('Error')
                    self.send_response(500)


if __name__ == '__main__':
    server_data = []
    HOST_master = config.Master[0]
    PORT_master = config.Master[1]
    HOST_secondaty_1 = config.Secondary_1[0]
    PORT_secondaty_11 = config.Secondary_1[1]
    PORT_secondaty_12 = config.Secondary_1[2]
    HOST_secondaty_2 = config.Secondary_2[0]
    PORT_secondaty_21 = config.Secondary_2[1]
    PORT_secondaty_22 = config.Secondary_2[2]
    Handler = CustomHandler
    with SocketServer.TCPServer((HOST_master, PORT_master), Handler) as httpd:
        print('Master: {}:{}'.format(HOST_master, PORT_master))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")
            httpd.socket.close()
            sys.exit(0)
