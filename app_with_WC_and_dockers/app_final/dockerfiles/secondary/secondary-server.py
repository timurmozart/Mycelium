#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler
import socketserver as SocketServer
from concurrent.futures import ThreadPoolExecutor
from sys import argv
import socket
import config
import time
import random


class CustomHandler(BaseHTTPRequestHandler):

    def do_GET(self): # якщо немає меседжа 3, але є 4, то ми не показуємо меседж 4 поки 3 не прийде
        global server_data
        if self.path == '/list':
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            messages2print = []
            if not server_data:
                self.wfile.write(bytes(str('No data on server'), encoding='utf-8'))
            else:
                id_prev = 1
                for id in sorted(server_data.keys()):
                    if len(server_data.keys()) == 1:
                        if id == id_prev:
                            self.wfile.write(bytes(str(server_data[id]) + ' ', encoding='utf-8'))
                            messages2print.append(server_data[id])
                        else:
                            break
                    else:
                        if abs(id - id_prev) <= 1:
                            self.wfile.write(bytes(str(server_data[id]) + ' ', encoding='utf-8'))
                            messages2print.append(server_data[id])
                            id_prev = id
                        else:
                            break
            print('Saved data on the server: ', messages2print)


def run_server_tcp(host, port):
    global server_data
    global HOST_secondary
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    print('TCP server is up: {}:{}'.format(host, port))
    sock.listen(10)
    while True:
        try:
            client, addr = sock.accept()  # це блокуюча точка, тут повинен відкриватися новий потік
        except KeyboardInterrupt:
            sock.close()
            break
        else:
            result = client.recv(1024)
            sleep_time = random.randint(1, 10)
            print('Sleep time: ', sleep_time)
            time.sleep(sleep_time)
            sent_error = random.randint(0, 1) # randomly generate error indicator
            if sent_error == 1:
                client.send(b'InternalServerError')
                print('Send an error to the master node')
            else:
                client.send(b'OK')
                messageID = int(result.decode('utf-8').split(':')[0])
                message = ''.join(result.decode('utf-8').split(':')[1:])
                if messageID not in server_data.keys():
                    server_data[messageID] = message  # result.decode('utf-8') == 'check'
                    print('Appended new message:', message)
            client.close()


def run_http_server(host, http_port):
    httpd = SocketServer.TCPServer((host, http_port), CustomHandler)
    print('HTTP server is up: {}:{}'.format(host, http_port))
    httpd.serve_forever()


if __name__ == '__main__':
    print("**************")
    print(socket.gethostname())
    print("**************")
    server_data = {}
    HOST_secondary = socket.gethostname()
    if HOST_secondary == 'myc-n1':
        PORT_secondary_1 = config.Secondary_1[1]
        PORT_secondary_2 = config.Secondary_1[2]
    elif HOST_secondary == 'myc-n2':
        PORT_secondary_1 = config.Secondary_2[1]
        PORT_secondary_2 = config.Secondary_2[2]
    else:
        print('No secondary node with index {}'.format(argv[1]))

    tasks = [lambda: run_server_tcp(HOST_secondary, PORT_secondary_2),
             lambda: run_http_server(HOST_secondary, PORT_secondary_1)]
    with ThreadPoolExecutor() as executor:
        running_tasks = [executor.submit(task) for task in tasks]
        try:
            for running_task in running_tasks:
                running_task.result()
        except KeyboardInterrupt:
            for running_task in running_tasks:
                if not running_task.done():
                    print('\nShutting down...: ', )
                    running_task.cancel()
            executor.shutdown(wait=False)
