#!/usr/bin/env python3

import argparse
import datetime
import functools
import pprint
import readline
import time
import haiker


def _request(func):
    @functools.wraps(func)
    def req(self, path, *args, **kwargs):
        time.sleep(5)
        print('[{0}]'.format(path))
        retval = data = func(self, path, *args, **kwargs)
        if isinstance(data, list):
            print('Number of Elements: {0}'.format(len(retval)))
            if len(data) > 0:
                print('First Element:')
                data = data[0]
        pprint.pprint(data)
        print()
        return retval
    return req


haiker.api.BaseAPIHandler.get = _request(haiker.api.BaseAPIHandler.get)
haiker.api.BaseAPIHandler.post = _request(haiker.api.BaseAPIHandler.post)


class APIChecker(object):
    def __init__(self, keyword, someone):
        super().__init__()
        self.keyword = keyword
        self.someone = someone

    @staticmethod
    def _print_title(text):
        n = len(text) + 4
        print('=' * n)
        print('* {0} *'.format(text))
        print('=' * n)

    def check_without_auth(self):
        self._print_title('Checking APIs available without auth')
        api = haiker.Haiker()
        # Timeline APIs
        api.public_timeline()
        api.keyword_timeline(self.keyword)
        api.user_timeline(self.someone)
        api.friends_timeline(self.someone)
        api.album(word=self.keyword)
        # User and keyword APIs
        api.show_user(self.someone)
        api.show_keyword(self.keyword)
        api.hot_keywords()
        api.keyword_list(word=self.keyword)
        # Favorite APIs
        api.friends(self.someone)
        api.followers(self.someone)

    def _check_with_auth(self, auth):
        api = haiker.Haiker(auth)
        url_name = api.show_user().screen_name
        user_keyword = 'id:{0}'.format(url_name)
        # Timeline APIs
        api.user_timeline(count=1)
        api.friends_timeline(count=1)
        # Entry and star APIs
        text = 'Hello world'
        eid = api.update_status(user_keyword, text, source=self.keyword).id
        api.show_status(eid)
        api.add_star(eid)
        api.remove_star(eid)
        api.delete_status(eid, url_name)
        # User and keyword APIs
        api.associate_keywords(user_keyword, self.keyword)
        api.dissociate_keywords(user_keyword, self.keyword)
        # Favorite APIs
        api.friends()
        api.followers()
        api.follow_user(self.someone)
        api.unfollow_user(self.someone)
        api.favorite_keywords(self.someone)
        api.follow_keyword(self.keyword)
        api.unfollow_keyword(self.keyword)

    def check_with_basic_auth(self, username, password):
        self._print_title('Checking APIs with Basic Authentication')
        auth = haiker.BasicAuth(username, password)
        self._check_with_auth(auth)

    def check_with_oauth(self, consumer_key, consumer_secret,
                         oauth_token=None, token_secret=None):
        self._print_title('Checking APIs with OAuth')
        if oauth_token is None or token_secret is None:
            auth = haiker.OAuth(consumer_key, consumer_secret)
            auth.initiate(['read_public', 'write_public'])
            print('GOTO: {url}'.format(url=auth.auth_url()))
            verifier = input('verifier: ').strip()
            token, secret = auth.verify(verifier)
            print('oauth_token: {0}'.format(token))
            print('oauth_secret: {0}'.format(secret))
            print()
        else:
            auth = haiker.OAuth(consumer_key, consumer_secret,
                                oauth_token, token_secret)
        api = haiker.Haiker(auth)
        self._check_with_auth(auth)

    @classmethod
    def main(cls):
        parser = argparse.ArgumentParser(description='test API calls')
        add_arg = parser.add_argument
        add_arg('--without_auth', action='store_true',
                help='call APIs which do not require auth')
        add_arg('--username', nargs='?',
                help='required for calling APIs with Basic Auth')
        add_arg('--password', nargs='?',
                help='required for calling APIs with Basic Auth')
        add_arg('--consumer_key', nargs='?',
                help='required for calling APIs with OAuth')
        add_arg('--consumer_secret', nargs='?',
                help='required for calling APIs with OAuth')
        add_arg('--oauth_token', nargs='?',
                help='OAuth access token (optional)')
        add_arg('--oauth_secret', nargs='?',
                help='OAuth access token secret (optional)')
        add_arg('--keyword', nargs='?', default='BOT',
                help='keyword required for some APIs (default: BOT)')
        add_arg('--someone', nargs='?', default='jkondo',
                help='url_name required for some APIs (default: jkondo)')
        args = parser.parse_args()
        checker = cls(args.keyword, args.someone)
        if args.without_auth:
            checker.check_without_auth()
        if args.username is not None and args.password is not None:
            checker.check_with_basic_auth(args.username, args.password)
        if args.consumer_key is not None and args.consumer_secret is not None:
            checker.check_with_oauth(args.consumer_key, args.consumer_secret,
                                     args.oauth_token, args.oauth_secret)


if __name__ == '__main__':
    APIChecker.main()
