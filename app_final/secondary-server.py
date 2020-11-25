#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler
import socketserver as SocketServer
from concurrent.futures import ThreadPoolExecutor
from sys import argv
import socket
import config
import time


class CustomHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global server_data
        if self.path == '/list':
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()
            if not server_data:
                self.wfile.write(bytes(str('No data on server'), encoding='utf-8'))
            else:
                for m in server_data:
                    self.wfile.write(bytes(str(m) + ' ', encoding='utf-8'))
            print('Saved data on the server: ', server_data)


def run_server_tcp(host, port):
    global server_data
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    print('TCP server is up: {}:{}'.format(host, port))
    sock.listen(10)
    while True:
        try:
            client, addr = sock.accept()
        except KeyboardInterrupt:
            sock.close()
            break
        else:
            result = client.recv(1024)
            #time.sleep(10)
            client.send(b'OK')
            client.close()
            server_data.append(result.decode('utf-8'))
            print('Appended new message:', result.decode('utf-8'))


def run_http_server(host, http_port):
    httpd = SocketServer.TCPServer((host, http_port), CustomHandler)
    print('HTTP server is up: {}:{}'.format(host, http_port))
    httpd.serve_forever()


if __name__ == '__main__':
    server_data = []
    if int(argv[1]) == 1:
        HOST_secondary = config.Secondary_1[0]
        PORT_secondary_1 = config.Secondary_1[1]
        PORT_secondary_2 = config.Secondary_1[2]
    elif int(argv[1]) == 2:
        HOST_secondary = config.Secondary_2[0]
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
