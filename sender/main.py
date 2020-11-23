import time

def send_post(file):
    import requests
    url = 'http://0.0.0.0:5000/post-example'
    data_json = open(file, "r").read()
    # data_json = {'data': data_text}
    x = requests.post(url, json=data_json)
    print(data_json)
    print(x.text)

list = [
    "sender/1.json",
    "sender/2.json",
    "sender/3.json"
]
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    for i in list:
        print(i)
        send_post(i)
