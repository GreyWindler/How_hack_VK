import requests as rq
from time import sleep

base_addr = 'https://api.vk.com/method/'
token = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'

default_params = {
    'v': '5.52',
    'access_token': token
}


def get_user_id(user):
    url = base_addr + 'users.get'
    params = default_params.copy()
    params['users_ids'] = user
    r = rq.get(url, params=params)
    return r.json()['response'][0]['id']


def get_groups(user_id):
    url = base_addr + 'groups.get'
    params = default_params.copy()
    params['user_id'] = user_id
    r = rq.get(url, params=params)
    try:
        return r.json()['response']['items']
    except Exception as ex:
        print('Exception while getting user: ', r.json()['error']['error_msg'])


def get_friends(user_id):
    url = base_addr + 'friends.get'
    params = default_params.copy()
    params['user_id'] = user_id
    r = rq.get(url, params=params)
    return r.json()['response']['items']


user = 'eshmargunov'
user_id = get_user_id(user)
sleep(0.334)
user_friends = get_friends(user_id)
sleep(0.334)
user_groups = set(get_groups(user_id))
sleep(0.334)
friends_groups = set()

for friend in user_friends:
    try:
        friends_groups |= set(get_groups(friend))
        sleep(1)
    except Exception:
        sleep(2)

# тут мы получаем список id групп, в которых состоят друзья, но не состоит сам юзер
print(friends_groups - user_groups)
