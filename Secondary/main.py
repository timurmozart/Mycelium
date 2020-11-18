def print_hi(name):

    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def server_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', 8888))
    while True:
        try:
            result = sock.recv(1024)
        except KeyboardInterrupt:
            sock.close()
            break
        else:
            print('msg: ', result.decode('utf-8'))

def server_tcp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('myc-n', 8000))
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



if __name__ == '__main__':
    print_hi('PyCharm')
    # server_udp()
    server_tcp()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
