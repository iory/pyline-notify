import unittest

import numpy as np

from line_notify import LineNotify
from line_notify import send_line_notify


class TestLineNotify(unittest.TestCase):

    client = None

    @classmethod
    def setUpClass(cls):
        # from environment variable LINENOTIFY_TOKEN
        cls.client = LineNotify(token=None)

    def test___init__(self):
        # invalid token
        with self.assertRaises(RuntimeError):
            LineNotify(token='')

    def test_notify(self):
        for time_format in [None, '%H:%M']:
            # do nothing
            self.client.notify()

            # notify message
            self.client.notify(message='[unittest] test_notify')

            # notify imgs
            self.client.notify(imgs=np.ones((64, 64), dtype=np.uint8))

    def test_send_line_notify(self):
        for time_format in [None, '%H:%M']:
            send_line_notify(
                '[unittest] send_line_notify',
                np.ones((64, 64), dtype=np.uint8),
                time_format=time_format)
