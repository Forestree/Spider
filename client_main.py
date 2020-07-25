import threading
import time
import requests
import sys
import json
import os
import jieba.analyse
from PyQt5 import QtCore, QtGui, QtWidgets
import pickle


from Spiders.bilibili.spider import Bilibili
from Spiders.zhihu.spider import Zhihu
from tools.helper import LoginHelper
from Chat import chat_client

pickle_file = 'pickle.pkl'
bilibili_history = []
bilibili_users = []


def bilibili_run():
    global bilibili_history
    global bilibili_users
    login_helper = LoginHelper()
    login_helper.login(Bilibili.login_url)
    bilibili = Bilibili(login_helper.get_cookies(), login_helper.get_driver())
    bilibili_history = bilibili.get_user_history(max_history_record=500)
    bilibili_users = bilibili.get_following_user()
    login_helper.driver.quit()

zhihu_following_topics = []
zhihu_related_questions = []
zhihu_following_questions = []

server_ip = '127.0.0.1:8899'
id_str = ''

def zhihu_run():
    global zhihu_following_questions
    global zhihu_following_topics
    global zhihu_related_questions

    zhihu_login_helper = LoginHelper()
    zhihu_login_helper.login(Zhihu.login_url)
    zhihu = Zhihu(zhihu_login_helper.get_cookies(), zhihu_login_helper.get_driver())

    zhihu_following_questions = zhihu.get_following_questions()
    zhihu_following_topics = zhihu.get_following_topics()
    zhihu_related_questions = zhihu.get_related_questions(100)

    zhihu_login_helper.driver.quit()


def heartbeat_run():
    assert id_str
    while True:
        requests.post('http://{}/heartbeat'.format(server_ip), id_str)
        time.sleep(3)


def is_yes(s):
    s = s.strip().upper()
    if s == 'YES' or s == 'Y':
        return  True
    return False


if __name__ == '__main__':
    port = int(sys.argv[1])
    chat_client.LISTEN_PORT = port
    app = QtWidgets.QApplication(sys.argv)
    window = chat_client.ExampleApp()
    window.listen_in_thread()
    window.show()

    # 如果3天内已经爬起过数据，直接读取pickle文件
    if os.path.exists(pickle_file) and time.time() - os.path.getmtime(pickle_file) < 60*60*25*3:
        pkl_file = open(pickle_file, 'rb')
        user_profile = pickle.load(pkl_file)
        pkl_file.close()
    # 否则重新爬取数据
    else:
        bilibili_thread = threading.Thread(target=bilibili_run)
        bilibili_thread.start()
        zhihu_thread = threading.Thread(target=zhihu_run)
        zhihu_thread.start()
        bilibili_thread.join()
        zhihu_thread.join()

        # 获取关键词
        corpus = ''
        for que in zhihu_related_questions + zhihu_following_questions:
            corpus += '。' + que
        question_keyword = jieba.analyse.textrank(corpus)
        corpus = ''
        for history in bilibili_history:
            corpus += '。' + history
        video_keyword = jieba.analyse.textrank(corpus)

        topics = zhihu_following_topics
        video_up = bilibili_users
        user_profile = {
            'question_keyword': question_keyword,
            'video_keyword': video_keyword,
            'topics': topics,
            'video_up': video_up
        }
        with open(pickle_file, 'wb') as f:
            pickle.dump(user_profile, f)

    # print('user_profile', user_profile)
    resp = requests.post('http://{}/signin?port={}'.format(server_ip, port), json.dumps(user_profile))
    id_str = resp.content.decode()

    # 向server发送心跳
    heartbeat_thread = threading.Thread(target=heartbeat_run)
    heartbeat_thread.setDaemon(True)
    heartbeat_thread.start()

    while True:
        s = input('Do you want to connect to a random user? [Y/N] (N to exit)')
        if is_yes(s):
            # 获取随机匹配/有相似兴趣的用户
            resp = requests.post('http://{}/hello'.format(server_ip), id_str)
            peer = json.loads(resp.content.decode())
            print(peer)
            if 'common' not in peer:
                print(peer[0])
                s = input('Do you want to exit? [Y/N]')
                if is_yes(s):
                    break
            else:
                chat_client.client_ip = peer['ip']
                chat_client.CONNECT_PORT = int(peer['port'])
                intro = ''
                for k in peer['common'].keys():
                    intro += k + ': '
                    for t in peer['common'][k]:
                        intro += t + ', '
                    intro += '\n\n'

                window.connect_to()
                # 告知用户共同兴趣信息
                shard_num = (len(intro.encode(encoding="utf-8"))+4096) // 4096
                shard_size = len(intro) // shard_num
                for i in range(shard_num):
                    window.send(intro[i*shard_size: (i+1)*shard_size])
                # window.send(intro)
                sys.exit(app.exec())
        else:
            break
    exit()

