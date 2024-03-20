from PIL import Image, ImageOps
import numpy as np

import os
_DIR = os.getcwd()

import goopylib as gp
os.chdir(_DIR)  # TODO fix bug with goopylib changing working directory


def _load_image(path, size=80):
    img = Image.open(path)
    img = ImageOps.grayscale(img)
    img = img.rotate(-90, expand=True)
    img = ImageOps.contain(img, (size, size))
    img.load()

    data = np.asarray(img, dtype="float32")
    return data / 255


def _to_dice(image, window):
    image = np.digitize(image, bins=np.linspace(0, 1, 12))

    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            rect = gp.Image(f"assets/dice/{image[x, y]}.png", (x, y), (x + 1, y + 1))
            rect.draw(window)


def _to_rect(image, window):
    image = np.digitize(1 - image, bins=np.linspace(0, 1, 12)).astype("float32")
    image /= 12

    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            rect = gp.Rectangle((x, y), (x + 1, y + 1))
            rect.set_color("#000")
            rect.transparency = image[x, y]
            rect.draw(window)


def _get_window_size(image):
    max_size = gp.get_screen_height() * 0.7
    aspect_ratio = image.shape[0] / image.shape[1]

    if aspect_ratio < 1:
        return int(max_size * aspect_ratio), int(max_size)  # vertical
    return int(max_size), int(max_size / aspect_ratio)  # horizontal


def _setup_window(image):
    size = _get_window_size(image)
    window = gp.Window(*size)

    camera = window.get_camera()
    camera.set_projection(0, image.shape[0], 0, image.shape[1])
    return window


def _image2mosaic(plotting_func, path, size):
    image = _load_image(path, size)

    window = _setup_window(image)
    plotting_func(image, window)

    while window.is_open():
        gp.update()
    gp.terminate()


def image2rect(path, size=80):
    _image2mosaic(_to_rect, path, size)


def image2dice(path, size=80):
    _image2mosaic(_to_dice, path, size)


image2dice("demo/img1.jpeg")
