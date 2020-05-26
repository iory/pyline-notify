# flake8: noqa

import pkg_resources


__version__ = pkg_resources.get_distribution("pyline-notify").version


from .line_notify import LineNotify
from .line_notify import send_line_notify
