from functions import *


WIDTH, HEIGHT = 800, 800

all_sprites = pygame.sprite.Group()
cliffs = pygame.sprite.Group()


class Camera:
    def __init__(self):
        self.x = self.y = 0

    def apply(self, other):
        other.rect.x += self.x
        other.rect.y += self.y

    def set_cam(self, target):
        self.x = WIDTH // 2 - target.rect.x
        self.y = HEIGHT // 2 - target.rect.y


class NPC(pygame.sprite.Sprite):
    """

    The body class of Player's and Enemy's classes
    self.frames - dict that contain all animations;
    self.clock - class pygame.time.Clock() that responsible for animation update and movement speed;
    self.direction - contain value about current direction: 1 - directed on right, -1 - directed on left;

    """
    def __init__(self, path_to_sprites):
        super().__init__(all_sprites)
        self.frames = {}
        self.load_frames(path_to_sprites)
        self.cur_frame = 0
        self.cur_mode = 'Idle'
        self.image = self.frames[self.cur_mode][self.cur_frame]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.clock = pygame.time.Clock()
        self.tick = 10
        self.vx = self.vy = 0
        self.direction = 1

    def load_frames(self, path):
        for folder in objects_in_dir(path):
            self.frames[folder] = []
            for i in range(1, len(objects_in_dir(path + f'/{folder}', True)) + 1):
                self.frames[folder] += [load_image(path + f'/{folder}' + f'/{path.split("/")[1]}_{folder}_{i}.png')]

    def flip(self):
        """Function that get frames mirrored"""
        for folder in self.frames.keys():
            for sprite in self.frames[folder]:
                self.frames[folder][self.frames[folder].index(sprite)] = pygame.transform.flip(sprite, True, False)


class Warrior(NPC):
    """

    Player class that providing his movement and interaction with around world

    """

    def __init__(self):
        super().__init__('data/Warrior')
        self.run_after_fall = self.jump_fall = False

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
                k = 0
                while k < 5:
                    self.rect.y -= 1
                    if not self.check_collide_mask():
                        break
                    k += 1
                if k == 5:
                    self.rect.x -= self.vx

    def change_mode(self, mode, direction=None):
        if not (self.cur_mode == 'Attack' and self.cur_frame < 7):
            self.cur_frame = -1

        if (self.cur_mode == 'Run' and mode in ['Jump', 'Fall']) \
                or (self.cur_mode in ['Jump', 'Fall'] and mode == 'Run'):
            self.run_after_fall = True
        elif self.run_after_fall and mode == 'Idle':
            self.run_after_fall = False

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
            self.tick = 25
        elif mode == 'Idle' or (mode == 'Attack' and self.cur_mode != 'Jump'):
            self.vx = 0
            if not self.jump_fall:
                self.vy = 0
                self.tick = 10
        elif mode == 'Jump' and self.cur_mode != 'Attack':
            self.vy = -15
            self.tick = 30
            self.jump_fall = True
        elif mode == 'Fall':
            self.vy = 1
            self.tick = 30
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
                if self.run_after_fall:
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



