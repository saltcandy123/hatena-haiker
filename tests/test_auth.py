#!/usr/bin/env python3

import re
import unittest
import requests
import responses
import haiker
from . import samples


URL_INITIATE = 'https://www.hatena.com/oauth/initiate'
URL_VERIFY = 'https://www.hatena.com/oauth/token'
BODY_INITIATE = 'oauth_token=OAuthToken&oauth_token_secret=OAuthTokenSecret'
BODY_VERIFY = 'oauth_token=AccessToken&oauth_token_secret=AccessTokenSecret'


def check(auth):
    """Check that no exception is raised when calling Haiker methods
    using auth.
    """
    url = re.compile('http://h\\.hatena\\.ne\\.jp/api/statuses/.+')
    responses.add(responses.GET, url, json=samples.STATUS)
    responses.add(responses.POST, url, json=samples.STATUS)
    api = haiker.Haiker(auth)
    api.show_status('xyz')
    api.update_status('BOT', 'Hello world')


class TestBasicAuth(unittest.TestCase):
    @responses.activate
    def test_basic_auth(self):
        auth = haiker.BasicAuth('MyUsername', 'MyPassword')
        check(auth)


class TestOAuth(unittest.TestCase):
    @responses.activate
    def test_oauth_case1(self):
        auth = haiker.OAuth('MyConsumerKey', 'MyConsumerSecret',
                            'MyAccessToken', 'MyAccessTokenSecret')
        check(auth)

    @responses.activate
    def test_oauth_case2(self):
        responses.add(responses.POST, URL_INITIATE, body=BODY_INITIATE)
        responses.add(responses.POST, URL_VERIFY, body=BODY_VERIFY)
        auth = haiker.OAuth('MyConsumerKey', 'MyConsumerSecret')
        auth.initiate(['read_public', 'write_public'])
        auth.auth_url()
        auth.verify('verifier')
        check(auth)

    def _check_403(self, func, *args, **kwargs):
        with self.assertRaises(haiker.HaikerError) as cm:
            func(*args, **kwargs)
        exc = cm.exception.causal_error
        self.assertIsInstance(exc, requests.HTTPError)
        self.assertEqual(exc.response.status_code, 403)

    @responses.activate
    def test_oauth_error(self):
        responses.add(responses.POST, URL_INITIATE,
                      body=BODY_INITIATE, status=403)
        responses.add(responses.POST, URL_VERIFY,
                      body=BODY_VERIFY, status=403)
        auth = haiker.OAuth('MyConsumerKey', 'MyConsumerSecret')
        self._check_403(auth.initiate, ['read_public', 'write_public'])
        with self.assertRaises(haiker.HaikerError) as cm:
            auth.auth_url()
        self.assertIsInstance(cm.exception.causal_error, RuntimeError)
        self._check_403(auth.verify, 'verifier')
