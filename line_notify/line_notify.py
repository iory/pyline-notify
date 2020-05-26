import datetime
import io
import os
import requests

import numpy as np
from PIL import Image


class LineNotify(object):

    def __init__(self, token=None):
        if token is None:
            token = os.getenv('LINENOTIFY_TOKEN')
        self.token = token
        self.headers = {'Authorization': 'Bearer ' + self.token}
        if token is None \
           or len(token) == 0 \
           or self.status().status_code != 200:
            raise RuntimeError('Correct line notify token is not set.')

    def status(self):
        line_notify_api = 'https://notify-api.line.me/api/status'
        response = requests.get(line_notify_api, headers=self.headers)
        return response

    def _notify(self, data=None, files=None):
        line_notify_api = 'https://notify-api.line.me/api/notify'
        response = requests.post(line_notify_api,
                                 data=data,
                                 headers=self.headers,
                                 files=files)
        return response

    def notify(self, message=None, imgs=None):
        """Notify by using line notify api.

        Parameters
        ----------
        message : None or str
            text message.
        imgs : None, list[PIL.Image.Image], list[numpy.ndarray] or list[str]
            Images or paths of image file.

        Returns
        -------
        responses : list[requests.models.Response]
            list of responses.
        """
        if message is None and imgs is None:
            return

        # First, check imgs.
        if imgs is not None:
            if not isinstance(imgs, list):
                imgs = [imgs]

            pil_imgs = []
            for img in imgs:
                if isinstance(img, Image.Image):
                    pil_img = img
                elif isinstance(img, np.ndarray):
                    pil_img = Image.fromarray(img)
                elif isinstance(img, str):
                    if os.path.exists(img):
                        pil_img = Image.open(img)
                    else:
                        raise OSError('Image path of {} is not exist'
                                      .format(img))
                else:
                    raise ValueError
                pil_imgs.append(pil_img)

        responses = []
        if message is not None:
            message = "{}\n{}".format(
                datetime.datetime.now().strftime('%H:%M'), message)
            payload = {'message': message}
            res = self._notify(data=payload)
            responses.append(res)

        if imgs is not None:
            files = []
            for pil_img in pil_imgs:
                buf = io.BytesIO()
                pil_img.save(buf, format='png')
                buf.seek(0)
                files.append({"imageFile": buf})

            for f in files:
                message = "{}".format(
                    datetime.datetime.now().strftime('%H:%M'))
                payload = {'message': message}
                res = self._notify(files=f, data=payload)
                responses.append(res)
        return responses


def send_line_notify(message=None, imgs=None, token=None):
    """Notify by using line notify api.

    Parameters
    ----------
    message : None or str
        text message.
    imgs : None, list[PIL.Image.Image], list[numpy.ndarray] or list[str]
        Images or paths of image file.
    token : None or str
        access token. If this value is None, get access token from
        environment variable LINENOTIFY_TOKEN.

    Returns
    -------
    responses : list[requests.models.Response]
        list of responses.
    """
    ln = LineNotify(token=token)
    return ln.notify(message, imgs)
