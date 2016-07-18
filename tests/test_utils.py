#!/usr/bin/env python3

import datetime
import sys
import time
import unittest
import haiker


class TestUtils(unittest.TestCase):
    def test_user_agent(self):
        haiker.utils.user_agent()

    def test_removed_dict(self):
        f = haiker.utils.removed_dict
        d = {'a': 123, 'b': 456}
        self.assertEqual(f(d, set()), d)
        self.assertEqual(f(d, {'a', 'c'}), {'b': 456})

    def test_strftime(self):
        utc = datetime.datetime(2000, 1, 1, tzinfo=datetime.timezone.utc)
        jst = utc.astimezone(datetime.timezone(datetime.timedelta(hours=9)))
        if sys.version_info < (3, 3):
            delta = datetime.timedelta(seconds=-time.mktime(time.gmtime(0)))
            naive = (utc + delta).replace(tzinfo=None)
        else:
            naive = utc.astimezone().replace(tzinfo=None)
        f = haiker.utils.strftime
        s = '%Y-%m-%d %H:%M:%S'
        expr = '2000-01-01 00:00:00'
        self.assertEqual(f(utc, s), expr)
        self.assertEqual(f(jst, s), expr)
        self.assertEqual(f(naive, s), expr)

    def test_serialize(self):
        f = haiker.utils.serialize
        eq = self.assertEqual
        self.assertIsNone(f(None))
        eq(f(123), b'123')
        eq(f(True), b'1')
        eq(f(False), b'0')
        eq(f('abc'), b'abc')
        eq(f(b'abc'), b'abc')
        eq(f(datetime.datetime(2000, 1, 1, tzinfo=datetime.timezone.utc)),
           b'Sat, 01 January 2000 00:00:00 GMT')
        eq(f([123, 'abc', None, True]), b'123,abc,,1')
        self.assertRaises(TypeError, f, 1 + 2j)

    def test_build_params(self):
        f = haiker.utils.build_params
        self.assertIsNone(f(None))
        self.assertEqual(dict(f({'a': 9, 'b': True})), {'a': b'9', 'b': b'1'})
        self.assertEqual(f([('a', 'xyz')]), [('a', b'xyz')])
