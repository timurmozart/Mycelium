# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import socket


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def client_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(b'ebaaaaa', ('127.0.0.1', 8888))

def client_tcp():
    for i in range(11):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('127.0.0.1', 8000))
        msg = 'msg #'+str(i+1)
        print(msg)
        sndmsg = str.encode(msg)
        sock.send(sndmsg)
        sock.close()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    # client_udp()
    client_tcp()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
