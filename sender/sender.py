# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import time

def send_post():
    import requests
    url = 'http://0.0.0.0:5000/post-example'
    data_text = open("./data.txt", "r").read()
    data_json = {'data': data_text}
    x = requests.post(url, json=data_json)
    print(data_json)
    print(x.text)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        send_post()
        print('sssss')
        time.sleep(1)
        print('sssss')
        time.sleep(1)
        print('sssss')
        time.sleep(1)
        print('sssss')
        time.sleep(1)
        print('sssss')
        time.sleep(1)
        print('sssss')
        time.sleep(1)
