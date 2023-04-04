import requests
import fake_useragent

import pickle

from const import Cfg

URL = f'https://{Cfg.site}'
session = requests.Session()

"""Для новой авторизации удали coockies_file"""


def login():
    user_agent = fake_useragent.UserAgent().random
    headers = {'User-agent': user_agent}
    data = {  # названия полей в форме авторизации
        'user[email]': Cfg.login,
        'user[password]': Cfg.psw,
        'user[remember_me]': 1
    }
    print('Авторизация..')
    session.post(f'{URL}/login', data=data, headers=headers)
    with open('cookies_file', 'wb') as f:
        pickle.dump(session.cookies, f)


def request(link):
    try:
        with open('cookies_file', 'rb') as f:
            session.cookies.update(pickle.load(f))
    except FileNotFoundError:
        login()
    # print(f'{URL}/{link}')
    return session.get(f'{URL}/{link}').text


# print(request('education_new'))
