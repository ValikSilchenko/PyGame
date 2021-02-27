import pygame
import os


class SpritesLoadError(Exception):
    def __init__(self, message):
        self.msg = message


class EmptyLevelFile(Exception):
    def __init__(self):
        self.msg = 'Выбранный файл пуст'


def load_image(fullname, colorkey=None):
    if not os.path.isfile(fullname):
        raise SpritesLoadError(f"Файл с изображением '{fullname}' не найден")
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))

    if not level_map:
        raise EmptyLevelFile
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def objects_in_dir(path, is_file=False):
    if not is_file:
        return [name for name in os.listdir(path)]
    return [name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]
