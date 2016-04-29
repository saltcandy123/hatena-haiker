#!/usr/bin/env python3
# coding: utf-8

import argparse
import pprint
import readline
import time
import haiker

def display(title, res):
    time.sleep(5)
    print('[{0}]'.format(title))
    pprint.pprint(res)
    print()

def test_noauth(someone):
    print('=======')
    print('NO AUTH')
    print('=======')
    api = haiker.Haiku()
    display('statuses/public_timeline',
            api.statuses.public_timeline(count=3))
    display('statuses/keyword_timeline',
            api.statuses.keyword_timeline('BOT', count=1))
    display('statuses/user_timeline',
            api.statuses.user_timeline(someone, count=1))
    display('statuses/friends_timeline',
            api.statuses.friends_timeline(someone, count=1))
    display('statuses/album',
            api.statuses.album(count=1))
    display('friendship/show',
            api.friendships.show(someone))
    display('keywords/show',
            api.keywords.show('BOT', without_related_keywords=False))
    display('keywords/hot',
            api.keywords.hot(without_related_keywords=False)[:1])
    display('keywords/list',
            api.keywords.list(without_related_keywords=True)[:1])
    display('statuses/friends',
            api.statuses.friends(someone)[:1])
    display('statuses/followers',
            api.statuses.followers(someone)[:1])

def test_basic_auth(username, password):
    print('==========')
    print('BASIC AUTH')
    print('==========')
    auth = haiker.BasicAuth(username, password)
    api = haiker.Haiku(auth)
    display('statuses/user_timeline',
            api.statuses.user_timeline())

def test_oauth(someone, consumer_key, consumer_secret,
               oauth_token=None, token_secret=None):
    print('=====')
    print('OAUTH')
    print('=====')
    if oauth_token is None or token_secret is None:
        auth = haiker.OAuth(consumer_key, consumer_secret)
        auth.initiate(['read_public', 'write_public'])
        print('GOTO: {url}'.format(url=auth.auth_url()))
        verifier = input('verifier: ').strip()
        token, secret = auth.verify(verifier)
        print('oauth_toen: {0}'.format(token))
        print('oauth_secret: {0}'.format(secret))
        print()
    else:
        auth = haiker.OAuth(consumer_key, consumer_secret, oauth_token, token_secret)
    api = haiker.Haiku(auth)
    res = api.applications.my()
    display('applications/my', res)
    url_name = res['url_name']
    res = api.statuses.update('id:{0}'.format(url_name), 'Hello, world', source='bot')
    display('statuses/update', res)
    eid = res['id']
    display('statuses/show',
              api.statuses.show(eid))
    display('favosites/create',
              api.favorites.create(eid))
    display('favosites/destroy',
              api.favorites.destroy(eid))
    display('statuses/destroy',
              api.statuses.destroy(eid, url_name))
    display('keywords/create',
              api.keywords.create('bot'))
    display('keywords/destroy',
              api.keywords.destroy('bot'))
    display('statuses/keywords',
              api.statuses.keywords(someone)[:1])
    display('keywords/relation/create',
              api.keywords.relation.create('id:{0}'.format(url_name), 'BOT'))
    display('keywords/relation/destroy',
              api.keywords.relation.destroy('id:{0}'.format(url_name), 'BOT'))
    display('friendships/create',
              api.friendships.create(someone))
    display('friendships/destroy',
              api.friendships.destroy(someone))

def main():
    parser = argparse.ArgumentParser(description='test API calls')
    parser.add_argument('--noauth', action='store_const',
                        default=False, const=True,
                        help='test with no auth')
    parser.add_argument('--username', nargs='?', default=None,
                        help='Basic Auth username '
                             '(required for testing Basic Auth API calls)')
    parser.add_argument('--password', nargs='?', default=None,
                        help='Basic Auth password '
                             '(required for testing Basic Auth API calls)')
    parser.add_argument('--consumer_key', nargs='?', default=None,
                        help='OAuth consumer key '
                             '(required for testing OAuth API calls)')
    parser.add_argument('--consumer_secret', nargs='?', default=None,
                        help='OAuth consumer secret '
                             '(required for testing OAuth API calls)')
    parser.add_argument('--oauth_token', nargs='?', default=None,
                        help='OAuth access token (optional)')
    parser.add_argument('--oauth_secret', nargs='?', default=None,
                        help='OAuth access token secret (optional)')
    parser.add_argument('--someone', nargs='?', default='jkondo',
                        help='username of someone (default: jkondo)')
    args = parser.parse_args()
    if args.noauth:
        test_noauth(args.someone)
    if args.username is not None and args.password is not None:
        test_basic_auth(args.username, args.password)
    if args.consumer_key is not None and args.consumer_secret is not None:
        test_oauth(args.someone,
                   args.consumer_key, args.consumer_secret,
                   args.oauth_token, args.oauth_secret)


if __name__ == '__main__':
    main()
