from functions import *


all_sprites = pygame.sprite.Group()
cliffs = pygame.sprite.Group()


class Warrior(pygame.sprite.Sprite):
    """

    Player class that providing his movement and interaction with around world
    self.frames - dict that contain all animations;
    self.clock - class pygame.time.Clock() that responsible for animation update and movement speed;
    self.direction - contain value about current direction: 1 - directed on right, -1 - directed on left;

    """

    def __init__(self):
        super().__init__(all_sprites)
        self.frames = {}
        self.load_frames()
        self.cur_frame = 0
        self.cur_mode = 'Idle'
        self.run_after_jump = self.jump_fall = False
        self.image = self.frames[self.cur_mode][self.cur_frame]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.clock = pygame.time.Clock()
        self.tick = 10
        self.vx = self.vy = 0
        self.direction = 1

    def load_frames(self):
        for folder in objects_in_dir('data/Warrior'):
            self.frames[folder] = []
            for i in range(1, len(objects_in_dir(f'data/Warrior/{folder}', True)) + 1):
                self.frames[folder] += [load_image(f'data/Warrior/{folder}/Warrior_{folder}_{i}.png')]

    def flip(self):
        """Function that get frames mirrored"""
        for folder in self.frames.keys():
            for sprite in self.frames[folder]:
                self.frames[folder][self.frames[folder].index(sprite)] = pygame.transform.flip(sprite, True, False)

    def check_collide_mask(self):
        for sprite in cliffs:
            if pygame.sprite.collide_mask(self, sprite):
                return sprite.rect.x, sprite.rect.y
        return False

    def terrain_movement(self):
        """Function that change character's position depending on terrain"""
        if pygame.sprite.spritecollideany(self, cliffs):
            if not self.check_collide_mask():
                k = 0
                while k < 5:
                    self.rect.y += 1
                    if self.check_collide_mask():
                        self.rect.y -= 1
                        break
                    k += 1
                if k == 5:
                    self.rect.y -= 5
                    if self.cur_mode not in ['Jump', 'Fall']:
                        self.change_mode('Fall')
            else:
                coords = self.check_collide_mask()
                if coords[1] + 5 < self.rect.y + self.rect.height:
                    self.rect.x -= self.vx

    def change_mode(self, mode, direction=None):
        if not (self.cur_mode == 'Attack' and self.cur_frame < 7):
            self.cur_frame = -1
        if (self.cur_mode == 'Run' and mode == 'Jump') or (self.cur_mode in ['Jump', 'Fall'] and mode == 'Run'):
            self.run_after_jump = True
        elif self.run_after_jump and mode == 'Idle':
            self.run_after_jump = False
        if not self.jump_fall or (self.cur_mode == 'Jump' and mode == 'Fall'):
            if not (self.cur_mode == 'Attack' and mode == 'Jump'):
                self.cur_mode = mode

        if direction != self.direction and direction is not None:
            self.flip()
            self.direction = direction

        if mode == 'Run':
            self.vx = 10 * self.direction
            if not self.jump_fall:
                self.vy = 0
            self.tick = 20
        elif mode == 'Idle' and not (mode == 'Attack' and self.jump_fall):
            self.vx = 0
            if not self.jump_fall:
                self.vy = 0
                self.tick = 10
        elif mode == 'Jump' and self.cur_mode != 'Attack':
            self.vy = -15
            self.tick = 20
            self.jump_fall = True
        elif mode == 'Fall':
            self.vy = 1
            self.tick = 20
            self.jump_fall = True

    def move(self):
        self.rect.x += self.vx
        self.terrain_movement()

        self.rect.y += self.vy
        coords = self.check_collide_mask()
        if pygame.sprite.spritecollideany(self, cliffs) and coords:
            if self.rect.y > coords[1] and self.vy < 0:
                self.rect.y -= self.vy
                self.vy = -self.vy
            elif self.rect.y < coords[1]:
                self.rect.y = coords[1] - self.rect.height + 1
                self.jump_fall = False
                if self.run_after_jump:
                    self.change_mode('Run')
                else:
                    self.change_mode('Idle')
                return

        if self.jump_fall:
            self.vy += 0.75

    def update(self):
        if self.cur_mode == 'Attack' and self.cur_frame == len(self.frames[self.cur_mode]) - 1:
            self.change_mode('Idle')
        elif self.cur_mode == 'Jump' and self.vy >= 0:
            self.change_mode('Fall')
        else:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames[self.cur_mode])
            self.image = self.frames[self.cur_mode][self.cur_frame]
            self.clock.tick(self.tick)


class Cliff(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        super().__init__(all_sprites, cliffs)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.mask = pygame.mask.from_surface(self.image)


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
