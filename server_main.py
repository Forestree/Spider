from flask import Flask
from flask import request
import random
import string
import json
import datetime

app = Flask(__name__)
online_users = {}

chars = string.ascii_letters + string.punctuation


def random_string_generator(str_size):
    return ''.join(random.choice(chars) for x in range(str_size))


@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    id_str = request.get_data().decode()
    online_users[id_str][-1] = datetime.datetime.now()
    return 'OK'


@app.route('/signin', methods=['POST'])
def signin():
    ip = request.remote_addr
    listen_port = request.args.get("port")
    user_profile = request.get_data().decode()
    id_str = random_string_generator(50)
    online_users[id_str] = [ip, listen_port, json.loads(user_profile), datetime.datetime.now()]
    print('signin', id_str)
    return id_str


def find_common(u1, u2):
    common = {}
    for idx in u1.keys():
        l1 = u1[idx]
        l2 = u2[idx]
        common[idx] = list(set(l1).intersection(l2))
    return common


def clear_offline_user():
    for id_str in list(online_users.keys()):
        if (datetime.datetime.now() - online_users[id_str][-1]).seconds > 15:
            online_users.pop(id_str)


@app.route('/hello', methods=['POST'])
def hello():
    clear_offline_user()
    id_str = request.get_data().decode()
    print('hello', list(online_users.keys()))
    print('id_str', id_str)
    if id_str not in online_users:
        return json.dumps(['Try to signin again!'])
    while True:
        if len(online_users) <= 1:
            return json.dumps(['Not enough users'])
        id = random.sample(online_users.keys(), 1)[0]
        if id != id_str:
            common = find_common(online_users[id][-2], online_users[id_str][-2])
            return json.dumps({'ip': online_users[id][0],
                               'port': online_users[id][1],
                               'common': common})


if __name__ == '__main__':
    app.run('0.0.0.0', port=8899)