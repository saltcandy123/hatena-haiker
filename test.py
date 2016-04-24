#!/usr/bin/env python3
# coding: utf-8

import argparse
from pprint import pprint
import readline
import haiker

def test_noauth_methods():
    print('======================================')
    print('TEST SUITE OF METHODS WITHOUT ANY AUTH')
    print('======================================')
    api = haiker.Haiku()
    print('[statuses/public_timeline]')
    pprint(api.statuses.public_timeline(count=3))
    print()
    print('[statuses/keyword_timeline]')
    pprint(api.statuses.keyword_timeline('おはよう', count=1))
    print()
    print('[statuses/user_timeline]')
    pprint(api.statuses.user_timeline('jkondo', count=1))
    print()
    print('[statuses/friends_timeline]')
    pprint(api.statuses.friends_timeline('jkondo', count=1))
    print()
    print('[statuses/album]')
    pprint(api.statuses.album(count=1))
    print()
    print('[friendship/show]')
    pprint(api.friendships.show('jkondo'))
    print()
    print('[keywords/show]')
    pprint(api.keywords.show('BOT', without_related_keywords=False))
    print()
    print('[keywords/hot]')
    pprint(api.keywords.hot(without_related_keywords=False)[:1])
    print()
    print('[keywords/list]')
    pprint(api.keywords.list(without_related_keywords=True)[:1])
    print()
    print('[statuses/friends]')
    pprint(api.statuses.friends('jkondo')[:1])
    print()
    print('[statuses/followers]')
    pprint(api.statuses.followers('jkondo')[:1])
    print()

def test_basic_auth(username, password):
    print('=====================================')
    print('TEST SUITE OF METHODS WITH BASIC AUTH')
    print('=====================================')
    auth = haiker.BasicAuth(username, password)
    api = haiker.Haiku(auth)
    pprint(api.statuses.user_timeline())
    print()

def test_oauth(consumer_key, consumer_secret, oauth_token=None, token_secret=None):
    print('================================')
    print('TEST SUITE OF METHODS WITH OAUTH')
    print('================================')
    if oauth_token is None or token_secret is None:
        auth = haiker.OAuth(consumer_key, consumer_secret)
        auth.initiate(['read_public', 'write_public'])
        print('GOTO: {url}'.format(url=auth.auth_url()))
        verifier = input('verifier: ')
        print('oauth_toen: {0}\toauth_secret: {1}'.format(*auth.verify(verifier)))
        print()
    else:
        auth = haiker.OAuth(consumer_key, consumer_secret, oauth_token, token_secret)
    appapi = haiker.Applications(auth)
    api = haiker.Haiku(auth)
    print('[applications/my]')
    res = appapi.my()
    pprint(res)
    url_name = res['url_name']
    print()
    print('[statuses/update]')
    res = api.statuses.update('id:{0}'.format(url_name), 'Hello, world', source='bot')
    pprint(res)
    eid = res['id']
    print()
    print('[statuses/show]')
    pprint(api.statuses.show(eid))
    print()
    print('[favosites/create]')
    pprint(api.favorites.create(eid))
    print()
    print('[favosites/destroy]')
    pprint(api.favorites.destroy(eid))
    print()
    print('[statuses/destroy]')
    pprint(api.statuses.destroy(eid, url_name))
    print()
    print('[keywords/create]')
    pprint(api.keywords.create('bot'))
    print()
    print('[keywords/destroy]')
    pprint(api.keywords.destroy('bot'))
    print('[statuses/keywords]')
    pprint(api.statuses.keywords('jkondo')[:1])
    print()
    print('[keywords/relation/create]')
    pprint(api.keywords.relation.create('id:{0}'.format(url_name), 'BOT'))
    print()
    print('[keywords/relation/destroy]')
    pprint(api.keywords.relation.destroy('id:{0}'.format(url_name), 'BOT'))
    print()
    print('[friendships/create]')
    pprint(api.friendships.create('kaminagi'))
    print('[friendships/destroy]')
    pprint(api.friendships.destroy('kaminagi'))
    print()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--noauth', action='store_const',
                        default=lambda:None, const=test_noauth_methods)
    parser.add_argument('--username', nargs='?', default=None)
    parser.add_argument('--password', nargs='?', default=None)
    parser.add_argument('--consumer_key', nargs='?', default=None)
    parser.add_argument('--consumer_secret', nargs='?', default=None)
    parser.add_argument('--oauth_token', nargs='?', default=None)
    parser.add_argument('--oauth_secret', nargs='?', default=None)
    args = parser.parse_args()
    args.noauth()
    if args.username is not None and args.password is not None:
        test_basic_auth(args.username, args.password)
    if args.consumer_key is not None and args.consumer_secret is not None:
        test_oauth( args.consumer_key, args.consumer_secret,
                    args.oauth_token, args.oauth_secret)


if __name__ == '__main__':
    main()
