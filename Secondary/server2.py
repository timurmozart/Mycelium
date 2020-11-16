import socket


def server_tcp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.2', 8001))
    sock.listen(10)
    msgs = []
    while True:
        try:
            client, addr = sock.accept()
        except KeyboardInterrupt:
            sock.close()
            break
        else:
            result = client.recv(1024)
            client.close()
            print('msg: ', result.decode('utf-8'))
            msgs.append(result.decode('utf-8'))
            print(msgs)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    server_tcp()