
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 1234)
result = s.recv(1024)
print('msg: ', result.decode('utf-8'))
s.close()