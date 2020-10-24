from __future__ import division

import PIL


def resize_keeping_aspect_ratio(pil_img, length):
    W, H = pil_img.size
    aspect = W / H
    if H > W:
        width = int(length * aspect)
        height = length
    else:
        height = int(length / aspect)
        width = length
    return pil_img.resize((width, height),
                          resample=PIL.Image.BILINEAR)
