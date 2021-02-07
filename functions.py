import pygame
import os
import sys


def load_image(fullname, colorkey=None):
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
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

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def objects_in_dir(path, is_file=False):
    if not is_file:
        return [name for name in os.listdir(path)]
    return [name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]


# def render_level(level):
#     screen.fill('black')
#     im = load_image('grass.png')
#     cell_width, cell_height = im.get_size()
#     for i in range(len(level)):
#         for j in range(len(level[0])):
#             field.blit(im, (j * cell_width, i * cell_height))
#             if level[i][j] == '#':
#                 Tile([j * cell_width, i * cell_height], (cell_width, cell_height), 'box')
#             elif level[i][j] == '.':
#                 Tile([j * cell_width, i * cell_height], (cell_width, cell_height), 'grass')
#             elif level[i][j] == '@':
#                 Tile([j * cell_width, i * cell_height], (cell_width, cell_height), 'grass')
#                 Player([j * cell_width, i * cell_height], (cell_width, cell_height))
