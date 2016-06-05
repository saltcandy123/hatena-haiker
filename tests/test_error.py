#!/usr/bin/env python3

import unittest
import haiker


class TestError(unittest.TestCase):
    def test_str(self):
        str(haiker.error.HaikerError(Exception()))

    def test_replace(self):
        exc = haiker.error.HaikerError
        f = exc.replace(lambda x, y, z='0': int(x) + int(y) + int(z))
        g = exc.replace(lambda x, y, z: f(x + y, z))
        self.assertEqual(f('12', '34', '56'), 12 + 34 + 56)
        self.assertEqual(g('12', '34', '56'), 1234 + 56)
        # ValueError -> HaikerError
        self.assertRaises(exc, f, '1', 'a')
        self.assertRaises(exc, g, '1', '2', 'a')
        # TypeError -> HaikerError
        self.assertRaises(exc, g, None, None, None)
        # f: ValueError -> HaikerError, g: HaikerError -> HaikerError
        with self.assertRaises(exc) as cm:
            f('a', 'b', '3')
        self.assertIsInstance(cm.exception.causal_error, ValueError)
