# flake8: noqa

from __future__ import absolute_import

import pkg_resources


__version__ = pkg_resources.get_distribution("pyline-notify").version


from line_notify.line_notify import LineNotify
from line_notify.line_notify import send_line_notify
