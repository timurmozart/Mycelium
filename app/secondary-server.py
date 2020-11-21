#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler
import socketserver as SocketServer
import json

import sys
import config


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
            print('Data: ', server_data)

    def do_POST(self):
        global server_data
        print(self.headers)
        if self.headers['User-Agent'] == 'Master-node':
            if self.path == '/append':
                self.data_string = self.rfile.read(int(self.headers['Content-Length']))
                data = json.loads(self.data_string)
                new_message = data['msg']
                server_data.append(new_message)
                print('Appended new message', new_message)
                self.send_response(200, message='ACK:OK')
                self.end_headers()
        else:
            self.send_response(400, message='POST requests are not available')


if __name__ == '__main__':
    from sys import argv
    server_data = []
    if int(argv[1]) == 1:
        HOST_secondary = config.Secondary_1[0]
        PORT_secondary = config.Secondary_1[1]
    elif int(argv[1]) == 2:
        HOST_secondary = config.Secondary_2[0]
        PORT_secondary = config.Secondary_2[1]
    else:
        print('No secondary node with index {}'.format(argv[1]))
    Handler = CustomHandler
    with SocketServer.TCPServer((HOST_secondary, PORT_secondary), Handler) as httpd:
        print('Secondary {}: {}:{}'.format(argv[1], HOST_secondary, PORT_secondary))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")
            httpd.socket.close()
            sys.exit(0)
