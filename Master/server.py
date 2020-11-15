#!/usr/bin/env python3
from http import server
import socketserver as SocketServer


class CustomHandler(server.SimpleHTTPRequestHandler):

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
                    
    def do_POST(self):
        global server_data
        if '/append' in self.path:
            print(self.path)
            new_message = self.path.split('msg=')[-1]
            print('NEW', new_message)
            server_data.append(new_message)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes('Appended message:' + str(new_message), encoding='utf-8'))


if __name__ == '__main__':
    PORT = 8080
    server_data = []
    Handler = CustomHandler
    with SocketServer.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
