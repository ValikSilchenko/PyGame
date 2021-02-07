from functions import *


class SpritesLoadError(Exception):
    pass


all_sprites = pygame.sprite.Group()


class Warrior(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.frames = {}  # array with all sprites of character (idle sprites, running sprites etc.)
        self.load_frames()
        self.cur_frame = 0
        self.cur_mode = 'Idle'
        self.image = self.frames[self.cur_mode][self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.clock = pygame.time.Clock()  # clock to control sprites update
        self.tick = 20  # tick for clock
        self.vx = self.vy = 0
        self.direction = 1  # direction of moving: 1 - right, -1 - left
        self.flip = False

    def load_frames(self):
        for folder in objects_in_dir('data/Warrior'):
            self.frames[folder] = []
            for i in range(1, len(objects_in_dir(f'data/Warrior/{folder}', True)) + 1):
                self.frames[folder] += [load_image(f'data/Warrior/{folder}/Warrior_{folder}_{i}.png')]

    def change_mode(self, mode, direction=None):
        self.cur_mode = mode
        self.cur_frame = 0
        if mode == 'Run':
            if direction != self.direction and direction is not None:
                for sprite in self.frames['Run']:
                    self.frames['Run'][self.frames['Run'].index(sprite)] = pygame.transform.flip(sprite, True, False)
                for sprite in self.frames['Idle']:
                    self.frames['Idle'][self.frames['Idle'].index(sprite)] = pygame.transform.flip(sprite, True, False)
                self.direction = direction
            if self.direction > 0:
                self.vx = 10
            else:
                self.vx = -10
        else:
            self.vx = self.vy = 0
        self.image = self.frames[self.cur_mode][self.cur_frame]

    def move(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames[self.cur_mode])
        self.image = self.frames[self.cur_mode][self.cur_frame]
        self.clock.tick(self.tick)

    # def cut_sheet(self, sheet, columns, rows):
    #     self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
    #                             sheet.get_height() // rows)
    #     for j in range(rows):
    #         for i in range(columns):
    #             frame_location = (self.rect.w * i, self.rect.h * j)
    #             self.frames.append(sheet.subsurface(pygame.Rect(
    #                 frame_location, self.rect.size)))

# class Tile(pygame.sprite.Sprite):
#     def __init__(self, pos, size, tile):
#         super().__init__(all_sprites)
#         if tile == 'box':
#             self.image = pygame.transform.scale(load_image('box.png'), size)
#             borders.add(self)
#         elif tile == 'grass':
#             self.image = pygame.transform.scale(load_image('grass.png'), size)
#             grass.add(self)
#         self.rect = self.image.get_rect()
#         self.rect.x, self.rect.y = pos


# class Player(pygame.sprite.Sprite):
#     def __init__(self, pos, size):
#         super().__init__(all_sprites, player)
#         self.image = load_image('mar.png')
#         self.rect = self.image.get_rect()
#         self.rect.x, self.rect.y = pos[0] + 15, pos[1] + 5
#         self.step = size
#
#     def update(self, key):
#         move = ()
#         if key == pygame.K_LEFT or key == pygame.K_a:
#             move = (-self.step[0], 0)
#         elif key == pygame.K_RIGHT or key == pygame.K_d:
#             move = (self.step[0], 0)
#         elif key == pygame.K_UP or key == pygame.K_w:
#             move = (0, -self.step[1])
#         elif key == pygame.K_DOWN or key == pygame.K_s:
#             move = (0, self.step[1])
#         if move:
#             self.rect.x += move[0]
#             self.rect.y += move[1]
#             if pygame.sprite.spritecollideany(self, borders):
#                 self.rect.x -= move[0]
#                 self.rect.y -= move[1]
#

# class Camera:
#     def __init__(self):
#         self.x = self.y = 0
#
#     def apply(self, other):
#         other.rect.x += self.x
#         other.rect.y += self.y
#
#     def set_cam(self, target):
#         self.x = WIDTH // 2 - target.rect.x
#         self.y = HEIGHT // 2 - target.rect.y
