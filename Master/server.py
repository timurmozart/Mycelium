#!/usr/bin/env python3
from http import server
import socketserver as SocketServer
from concurrent.futures import ThreadPoolExecutor
import socket
import json


class CustomHandler(server.SimpleHTTPRequestHandler):

    def client_tcp(self, msg, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.send(str.encode(msg))
        sock.close()

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
                    self.wfile.write(bytes(str(m), encoding='utf-8'))
            print('Data: ', server_data)

    def do_POST(self):
        global server_data
        global HOST_secondaty_1, HOST_secondaty_2
        global PORT_secondaty_1, PORT_secondaty_2
        if self.path == '/append':
            self.data_string = self.rfile.read(int(self.headers['Content-Length']))
            data = json.loads(self.data_string)
            print('JSON DATA:', data)
            new_message = data['msg']
            print('NEW', new_message)
            server_data.append(new_message)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes('Appended message:' + str(new_message), encoding='utf-8'))
            tasks = [lambda: self.client_tcp(new_message, HOST_secondaty_1, PORT_secondaty_1),
                     lambda: self.client_tcp(new_message, HOST_secondaty_2, PORT_secondaty_2)]
            with ThreadPoolExecutor() as executor:
                running_tasks = [executor.submit(task) for task in tasks]
                for running_task in running_tasks:
                    running_task.result()


if __name__ == '__main__':
    PORT = 8080
    server_data = []
    HOST_secondaty_1 = '127.0.0.1'
    PORT_secondaty_1 = 8000
    HOST_secondaty_2 = '127.0.0.2'
    PORT_secondaty_2 = 8001
    Handler = CustomHandler
    with SocketServer.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
