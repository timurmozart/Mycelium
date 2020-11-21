#!/usr/bin/env python3
from http import server
import socketserver as SocketServer
from concurrent.futures import ThreadPoolExecutor
import socket
import json
import sys
import config


class CustomHandler(server.SimpleHTTPRequestHandler):

    def client_tcp(self, msg, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        body = '{"msg":' + '"' + msg + '"' + '}'
        length = len(body)
        serverHost = str(host) + ":" + str(port)
        request = "POST /append HTTP/1.1\r\nHost:{0}\r\nUser-Agent: Master-node\r\nContent-Type: application/json\r\nContent-Length: {1}\r\n\r\n{2}\r\n".format(
            serverHost, length, body)
        payload = request.encode()
        sock.sendall(payload)
        response = sock.recv(1024)
        acknowledgement = response.decode('utf-8').split('\r\n')[0].split('ACK:')[-1]
        sock.close()
        return acknowledgement

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
            print('Data: ', server_data)

    def do_POST(self):
        global server_data
        global HOST_secondaty_1, HOST_secondaty_2
        global PORT_secondaty_1, PORT_secondaty_2
        if self.path == '/append':
            self.data_string = self.rfile.read(int(self.headers['Content-Length']))
            data = json.loads(self.data_string)
            #print('JSON DATA:', data)
            new_message = data['msg']
            #print('NEW', new_message)
            server_data.append(new_message)
            print('Appended new message', new_message)
            ack_list = []
            tasks = [lambda: self.client_tcp(new_message, HOST_secondaty_1, PORT_secondaty_1),
                     lambda: self.client_tcp(new_message, HOST_secondaty_2, PORT_secondaty_2)]
            with ThreadPoolExecutor() as executor:
                running_tasks = [executor.submit(task) for task in tasks]
                for running_task in running_tasks:
                    node_ack = running_task.result()
                    ack_list.append(node_ack)
            #print(set(ack_list))
            if set(ack_list) == {'OK'}:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(bytes('Appended new message:' + str(new_message), encoding='utf-8'))
            else:
                self.send_response(500)


if __name__ == '__main__':
    server_data = []
    HOST_master = config.Master[0]
    PORT_master = config.Master[1]
    HOST_secondaty_1 = config.Secondary_1[0]
    PORT_secondaty_1 = config.Secondary_1[1]
    HOST_secondaty_2 = config.Secondary_2[0]
    PORT_secondaty_2 = config.Secondary_2[1]
    Handler = CustomHandler
    with SocketServer.TCPServer((HOST_master, PORT_master), Handler) as httpd:
        print('Master: {}:{}'.format(HOST_master, PORT_master))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")
            httpd.socket.close()
            sys.exit(0)
