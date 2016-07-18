#!/usr/bin/env python3

import datetime
import unittest
import haiker
from . import samples


class TestTypes(unittest.TestCase):
    def test_list_of(self):
        f = haiker.types.list_of
        self.assertEqual(f(str)([1, 2, 3]), ['1', '2', '3'])
        self.assertEqual(f(int)(['1', '2', '3']), [1, 2, 3])

    def test_none_or(self):
        f = haiker.types.none_or
        self.assertEqual(f(str)('a'), 'a')
        self.assertEqual(f(int)(1), 1)
        self.assertIsNone(f(str)(None))
        self.assertIsNone(f(int)(None))

    def test_to_datetime(self):
        f = haiker.types.to_datetime
        dt = datetime.datetime(2010, 1, 2, 3, 4, 5,
                               tzinfo=datetime.timezone.utc)
        self.assertEqual(f('2010-01-02T03:04:05Z'), dt)
        dt = dt.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
        self.assertEqual(f('2010-01-02T03:04:05+09:00'), dt)
        self.assertEqual(f('2010-01-02T03:04:05.000+09:00'), dt)

    def test_status(self):
        status = haiker.types.Status(samples.STATUS)
        eq = self.assertEqual
        eq(status.link, 'http://h.hatena.ne.jp/xxxx/XXXX')
        eq(status.created_at,
           datetime.datetime(2010, 1, 2, 3, 4, 5,
                             tzinfo=datetime.timezone.utc))
        eq(status.favorited, 12)
        eq(status.haiku_text, 'HaikuText')
        eq(status.html, 'HTML')
        eq(status.html_touch, 'HTMLTouch')
        eq(status.html_mobile, 'HTMLMobile')
        eq(status.id, 'XXXX')
        eq(status.in_reply_to_status_id, 'YYYY')
        eq(status.in_reply_to_user_id, 'yyyy')
        eq(status.keyword, 'Word')
        eq(status.source, 'API')
        eq(status.text, 'Text')
        for reply in status.replies:
            self.assertIsInstance(reply, haiker.types.Status)
        self.assertIsInstance(status.target, haiker.types.Target)
        self.assertIsInstance(status.user, haiker.types.User)
        repr(status)

    def test_user(self):
        user = haiker.types.User(samples.USER)
        eq = self.assertEqual
        eq(user.followers_count, 123)
        eq(user.name, 'Name')
        eq(user.id, 'ID')
        eq(user.profile_image_url, 'http://xxxx/')
        eq(user.screen_name, 'ScreenName')
        eq(user.url, 'http://h.hatena.ne.jp/ID')
        repr(user)

    def test_keyword(self):
        keyword = haiker.types.Keyword(samples.KEYWORD)
        eq = self.assertEqual
        eq(keyword.entry_count, 123)
        eq(keyword.followers_count, 456)
        eq(keyword.link, 'http://h.hatena.ne.jp/Word')
        eq(keyword.related_keywords[0], 'word1')
        eq(keyword.title, 'Title')
        eq(keyword.word, 'Word')
        eq(keyword.url_name, 'URLName')
        repr(keyword)

    def test_target(self):
        target = haiker.types.Target(samples.TARGET)
        eq = self.assertEqual
        eq(target.title, 'Title')
        eq(target.word, 'Word')
        eq(target.url_name, 'URLName')
        repr(target)
