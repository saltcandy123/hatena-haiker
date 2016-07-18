#!/usr/bin/env python3

import datetime
import inspect
import itertools
import re
import sys
import unittest
import requests
import responses
import haiker
from . import samples


def all_combinations(iterable):
    """Enumerate all subsequences of elements of iterable
    from the longest to the shortest (i.e. the empty).
    """
    iterable = list(iterable)
    n = len(iterable)
    for r in range(n + 1):
        for subseq in itertools.combinations(iterable, n - r):
            yield subseq


def _can_accept_legacy(func, kwargs):
    try:
        func(**kwargs)
    except haiker.HaikerError as e:
        if isinstance(e.causal_error, TypeError):
            return False
        raise
    return True


def _find_args_legacy(func, kwargs):
    required, optional = set(), set()
    for keys in all_combinations(kwargs):
        max_kwargs = {kw: kwargs[kw] for kw in keys}
        if _can_accept_legacy(func, max_kwargs):
            break
    else:  # func cannot accept any combination of kwargs
        raise AssertionError('another argument is required')
    for key in max_kwargs:
        removed = {kw: max_kwargs[kw] for kw in max_kwargs if kw != key}
        if _can_accept_legacy(func, removed):
            optional.add(key)
        else:
            required.add(key)
    return required, optional


def find_args(func, kwargs):
    """Find all acceptable arguments from kwargs
    and return a pair of sets: required arguments and optional ones.
    """
    if sys.version_info < (3, 3):
        return _find_args_legacy(func, kwargs)
    required, optional = set(), set()
    for p in inspect.signature(func).parameters.values():
        if p.kind in [p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY]:
            if p.default is p.empty:
                required.add(p.name)
            else:
                optional.add(p.name)
    return required, optional


class TestTestAPIFuncs(unittest.TestCase):
    def test_all_combinations(self):
        a = [''.join(x) for x in all_combinations('abc')]
        b = ['abc', 'ab', 'ac', 'bc', 'a', 'b', 'c', '']
        self.assertEqual(a, b)

    def test_find_args(self):
        f = haiker.error.HaikerError.replace(
                lambda a, b, c, d, e=1, f=2, *, g, h, i=3, j=4, k=5: 0
            )
        d = {kw: 1 for kw in 'abcdefghijkxyz'}
        required, optional = find_args(f, d)
        self.assertEqual(required, {'a', 'b', 'c', 'd', 'g', 'h'})
        self.assertEqual(optional, {'e', 'f', 'i', 'j', 'k'})


def change(json):
    """Change the response of responses mock to json."""
    responses.reset()
    url = re.compile('http://h\\.hatena\\.ne\\.jp/api/.+\\.json')
    responses.add(responses.GET, url, json=json)
    responses.add(responses.POST, url, json=json)


def check(func, kwargs=None):
    """Check that no exception is raised when func is called,
    for all combination of the arguments.
    """
    d = dict() if kwargs is None else dict(kwargs)
    kwargs = {
        'body_formats': ['text', 'haiku'],
        'count': 1,
        'eid': '123',
        'media': 'album',
        'page': 1,
        'since': datetime.datetime(2010, 1, 1, 0, 0, 0),
        'url_name': 'me',
        'sort': 'hot',
        'without_related_keywords': True,
        'word': 'BOT',
        'word1': 'BOT1',
        'word2': 'BOT2',
    }
    kwargs.update(d)
    required, optional = find_args(func, kwargs)
    for keys in all_combinations(optional):
        func(**{kw: kwargs[kw] for kw in required | set(keys)})


class TestBaseAPIHandler(unittest.TestCase):
    def setUp(self):
        auth = haiker.BasicAuth('MyUsername', 'MyPassword')
        root = 'http://h.hatena.ne.jp/api/'
        self.api = haiker.api.BaseAPIHandler(auth, root, 'TestUserAgent')

    @responses.activate
    def test_get(self):
        url = 'http://h.hatena.ne.jp/api/get/method.json'
        responses.add(responses.GET, url, json=samples.STATUS)
        self.api.get('/get/method.json')
        responses.reset()
        responses.add(responses.GET, url, status=403, json=samples.STATUS)
        with self.assertRaises(requests.HTTPError):
            self.api.get('/get/method.json')

    @responses.activate
    def test_post(self):
        url = 'http://h.hatena.ne.jp/api/post/method.json'
        responses.add(responses.POST, url, json=samples.STATUS)
        self.api.post('/post/method.json')
        responses.reset()
        responses.add(responses.POST, url, status=403, json=samples.STATUS)
        with self.assertRaises(requests.HTTPError):
            self.api.post('/post/method.json')

    @responses.activate
    def test_suspicious_url(self):
        url = re.compile('http://h\\.hatena\\.ne\\.jp/api/get/.+\\.json')
        responses.add(responses.GET, url, json=samples.STATUS)
        self.api.get('/get/Th1s-1S_s4F3.json')
        malicious_list = ['../../malicious', '////malicious', '\uff21', '# ']
        for s in malicious_list:
            with self.assertRaises(ValueError):
                self.api.get('/get/{0}.json'.format(s))


class TestHaiker(unittest.TestCase):
    def setUp(self):
        self.api = haiker.Haiker()

    def test_auth_property(self):
        auth = haiker.BasicAuth('MyUsername', 'MyPassword')
        api = haiker.Haiker(auth)
        self.assertIs(api.auth, auth)
        auth2 = haiker.BasicAuth('MyUsername2', 'MyPassword2')
        api.auth = auth2
        self.assertIs(api.auth, auth2)

    # Timeline APIs
    @responses.activate
    def test_public_timeline(self):
        change([samples.STATUS])
        check(self.api.public_timeline)

    @responses.activate
    def test_keyword_timeline(self):
        change([samples.STATUS])
        check(self.api.keyword_timeline)

    @responses.activate
    def test_user_timeline(self):
        change([samples.STATUS])
        check(self.api.user_timeline)

    @responses.activate
    def test_friends_timeline(self):
        change([samples.STATUS])
        check(self.api.friends_timeline)

    @responses.activate
    def test_album(self):
        change([samples.STATUS])
        check(self.api.album)

    # Entry and star APIs
    @responses.activate
    def test_update_status(self):
        change(samples.STATUS)
        kwargs = {
            'keyword': 'BOT',
            'status': 'hello world',
            'in_reply_to_status_id': '123',
            'source': 'API',
            'files': [b'A', b'B', b'C'],
        }
        check(self.api.update_status, kwargs=kwargs)
        files = [open(__file__, 'br')]
        self.api.update_status('BOT', 'hello world', files=files)
        files[0].close()

    @responses.activate
    def test_show_status(self):
        change(samples.STATUS)
        check(self.api.show_status)

    @responses.activate
    def test_delete_status(self):
        change(samples.STATUS)
        check(self.api.delete_status, kwargs={'author_url_name': 'me'})

    @responses.activate
    def test_add_star(self):
        change(samples.STATUS)
        check(self.api.add_star)

    @responses.activate
    def test_remove_star(self):
        change(samples.STATUS)
        check(self.api.remove_star)

    # User and keyword APIs
    @responses.activate
    def test_show_user(self):
        change(samples.USER)
        check(self.api.show_user)

    @responses.activate
    def test_show_keyword(self):
        change(samples.KEYWORD)
        check(self.api.show_keyword)

    @responses.activate
    def test_hot_keywords(self):
        change([samples.KEYWORD])
        check(self.api.hot_keywords)

    @responses.activate
    def test_keywords_list(self):
        change([samples.KEYWORD])
        check(self.api.keyword_list)

    @responses.activate
    def test_associate_keywords(self):
        change(samples.KEYWORD)
        check(self.api.associate_keywords)

    @responses.activate
    def test_dissociate_keywords(self):
        change(samples.KEYWORD)
        check(self.api.dissociate_keywords)

    # Favorite APIs
    @responses.activate
    def test_friends(self):
        change([samples.USER])
        check(self.api.friends)

    @responses.activate
    def test_followers(self):
        change([samples.USER])
        check(self.api.followers)

    @responses.activate
    def test_follow_user(self):
        change(samples.USER)
        check(self.api.follow_user)

    @responses.activate
    def test_unfollow_user(self):
        change(samples.USER)
        check(self.api.unfollow_user)

    @responses.activate
    def test_favorite_keywords(self):
        change([samples.KEYWORD])
        check(self.api.favorite_keywords)

    @responses.activate
    def test_follow_keyword(self):
        change(samples.KEYWORD)
        check(self.api.follow_keyword)

    @responses.activate
    def test_unfollow_keyword(self):
        change(samples.KEYWORD)
        check(self.api.unfollow_keyword)
