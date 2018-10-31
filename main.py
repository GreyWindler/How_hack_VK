import requests as rq
import json
from time import sleep

BASE_ADDR = 'https://api.vk.com/method/'
DEFAULT_PARAMS = {'v': '5.52'}


def get_user_id(user):
    url = BASE_ADDR + 'users.get'
    params = DEFAULT_PARAMS.copy()
    params['users_ids'] = user
    r = rq.get(url, params=params)
    return r.json()['response'][0]['id']


def get_groups(user_id):
    url = BASE_ADDR + 'groups.get'
    params = DEFAULT_PARAMS.copy()
    params['user_id'] = user_id
    r = rq.get(url, params=params)
    try:
        return (set(r.json()['response']['items']), 0)
    except Exception as ex:
        err_msg = r.json()['error']['error_msg']
        print('Exception while getting user: ', err_msg)
        if err_msg == 'Permission to perform this action is denied':
            print('user_id: ', user_id)
            return (None, 1)
        elif err_msg == 'User was deleted or banned':
            return (None, 2)
        elif err_msg == 'Too many requests per second':
            return (None, 3)


def get_friends(user_id):
    url = BASE_ADDR + 'friends.get'
    params = DEFAULT_PARAMS.copy()
    params['user_id'] = user_id
    r = rq.get(url, params=params)
    return r.json()['response']['items']


def get_members(group_ids):
    url = BASE_ADDR + 'groups.getById'
    params = DEFAULT_PARAMS.copy()
    params['group_ids'] = ','.join(map(str, group_ids))
    params['fields'] = 'members_count'
    r = rq.get(url, params=params)
    return r.json()['response']


def remove_keys(lst):
    keys = [
        'screen_name',
        'is_closed',
        'type',
        'photo_50',
        'photo_100',
        'photo_200',
    ]
    for d in lst:
        for k in keys:
            d.pop(k)


if __name__ == '__main__':
    DEFAULT_PARAMS['access_token'] = input('Введите токен: ')
    user = input('Введите пользователя: ')

    user_id = get_user_id(user)
    user_friends = get_friends(user_id)
    user_groups, err = get_groups(user_id)
    friends_groups = set()

    for friend in user_friends:
        print('-')
        got_groups_or_banned = False
        while not got_groups_or_banned:
            grps, err = get_groups(friend)
            if err == 0:
                friends_groups |= grps
                got_groups_or_banned = True
            elif err == 2 or err == 1:
                got_groups_or_banned = True
            elif err == 3:
                sleep(2)

    groups = user_groups - friends_groups
    members = get_members(groups)
    remove_keys(members)
    with open('groups.json', 'w') as f:
        json.dump(members, f)
