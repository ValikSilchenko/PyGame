from functions import *
from time import time

WIDTH, HEIGHT = 800, 800

all_sprites = pygame.sprite.Group()
cliffs = pygame.sprite.Group()
enemies = pygame.sprite.Group()


class Camera:
    """Class that changes objects position depend of player coords"""

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
    self.health - health of object;

    """

    def __init__(self, path_to_sprites, *groups):
        super().__init__(all_sprites, *groups)
        self.frames = {}
        self.load_frames(path_to_sprites)
        self.cur_frame = 0
        self.cur_mode = 'Idle'
        self.clock = pygame.time.Clock()
        self.tick = 10
        self.vx = self.vy = 0
        self.direction = 1
        self.health = 5

    def check_collide_mask(self):
        for sprite in cliffs:
            if pygame.sprite.collide_mask(self, sprite):
                return sprite.rect.x, sprite.rect.y
        return False

    def load_frames(self, path):
        files = objects_in_dir(path, True)
        if not files:  # загрузка спрайтов, если каждый спрайт является отдельным файлом
            for folder in objects_in_dir(path):
                self.frames[folder] = []
                for i in range(1, len(objects_in_dir(path + f'/{folder}', True)) + 1):
                    self.frames[folder] += [
                        load_image(path + f'/{folder}' + f'/{path.split("/")[1]}_{folder}_{i}.png')]
        else:  # загрузка спрайтов, если несколько спрайтов находятся в одном файле
            for file in files:
                self.frames[file.split('.')[0]] = load_image(path + f'/{file}')

    def flip(self):
        """Function that get frames mirrored"""
        for folder in self.frames.keys():
            for sprite in self.frames[folder]:
                self.frames[folder][self.frames[folder].index(sprite)] = pygame.transform.flip(sprite, True, False)


class Warrior(NPC):
    """Player class that providing his movement and interaction with around world"""

    def __init__(self):
        super().__init__('data/Warrior')
        self.run_after_fall = self.jump_fall = False
        self.image = self.frames[self.cur_mode][self.cur_frame]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

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
        if not (self.cur_mode == 'Attack' and self.cur_frame < 7) and self.cur_mode != 'Death':
            self.cur_frame = -1

        if (self.cur_mode == 'Run' and mode in ['Jump', 'Fall']) \
                or (self.cur_mode in ['Jump', 'Fall'] and mode == 'Run'):
            self.run_after_fall = True
        elif self.run_after_fall and mode == 'Idle':
            self.run_after_fall = False

        if not self.jump_fall or (self.cur_mode == 'Jump' and mode == 'Fall'):
            if not (self.cur_mode == 'Attack' and mode == 'Jump') and self.cur_mode != 'Death':
                self.cur_mode = mode

        if direction != self.direction and direction is not None:  # проверка смены направления
            self.flip()
            self.direction = direction

        if mode == 'Run' and self.cur_mode != 'Death':
            self.vx = 10 * self.direction
            if not self.jump_fall:
                self.vy = 0
            self.tick = 25
        elif mode == 'Idle' or (mode == 'Attack' and self.cur_mode != 'Jump'):
            self.vx = 0
            if not self.jump_fall:
                self.vy = 0
                self.tick = 10
        elif mode == 'Jump' and self.cur_mode != 'Attack' and self.cur_mode != 'Death':
            self.vy = -15
            self.tick = 30
            self.jump_fall = True
        elif mode == 'Fall':
            self.vy = 1
            self.tick = 30
            self.jump_fall = True
        elif mode == 'Hurt':
            self.vx = 0
            self.health -= 1

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
        if self.health == 0:
            if self.cur_mode != 'Death':
                self.change_mode('Death')
            if self.cur_frame == len(self.frames['Death']) - 1:
                return

        # переключение в режим 'Idle' после завершения атаки или после нанесения удара
        if self.cur_mode in ['Attack', 'Hurt'] and self.cur_frame == len(self.frames[self.cur_mode]) - 1:
            self.change_mode('Idle')
        # переключение в режим падения после достижения пиковой высоты прыжка, индикатором чего является self.vy >= 0
        elif self.cur_mode == 'Jump' and self.vy >= 0:
            self.change_mode('Fall')
        else:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames[self.cur_mode])  # обновление спрайта
            self.image = self.frames[self.cur_mode][self.cur_frame]
            self.clock.tick(self.tick)


class Cliff(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        super().__init__(all_sprites, cliffs)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.mask = pygame.mask.from_surface(self.image)


class Goblin(NPC):
    """

    Class of enemy 'Goblin'
    self.coords - cortege with border cliffs;
    self.death_time - time after death;

    """
    def __init__(self):
        super().__init__('data/Goblin', enemies)
        self.cut_sheets()
        self.tick = 30
        self.image = self.frames[self.cur_mode][self.cur_frame]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.coords = (None, None)
        self.death_time = None

    def cut_sheets(self):
        for mode in self.frames.keys():
            if mode in ['Attack', 'Run']:
                columns = 8
            else:
                columns = 4
            frames = []
            for i in range(columns):
                frames.append(self.frames[mode].subsurface(
                    (
                        (self.frames[mode].get_width() // columns) * i, 0,
                        self.frames[mode].get_width() // columns, self.frames[mode].get_height())))
            self.frames[mode] = frames

    def change_mode(self, mode, enemy_x=None):
        if enemy_x is not None:
            if (enemy_x < self.rect.x and self.direction == 1) or (enemy_x > self.rect.x and self.direction == -1):
                self.direction = -self.direction
                self.flip()
        if self.cur_mode != 'Death' and not (self.cur_mode == 'Run' and mode == 'Run'):
            self.cur_mode = mode
            self.cur_frame = -1

        if mode == 'Run':
            self.vx = 11 * self.direction
        elif mode in ['Attack', 'Idle', 'Hurt', 'Death']:
            self.vx = 0
            if mode == 'Hurt':
                self.health -= 1

    def move(self):
        self.rect.x += self.vx
        if pygame.sprite.spritecollideany(self, cliffs) and not self.check_collide_mask():
            while not self.check_collide_mask():
                self.rect.y += 1
            self.rect.y -= 1
        elif self.check_collide_mask():
            k = 0
            while k < 6:
                k += 1
                self.rect.y -= 1
                if not self.check_collide_mask():
                    self.rect.y += 1
                    break
            if k == 5:
                self.rect.x -= self.vx

        # обработка выхода за край острова
        if not (self.coords[1].rect.x - 50 <= self.rect.x <= self.coords[0].rect.x - 20):
            self.flip()
            self.direction = -self.direction
            self.change_mode('Run')

    def update(self):
        if self.cur_mode == 'Hurt' and self.cur_frame == len(self.frames['Hurt']) - 1:
            self.change_mode('Idle')

        if self.health <= 0 and self.cur_mode != 'Death':
            self.change_mode('Death')
            return

        # удаление объекта после смерти
        if self.death_time is not None:
            if time() - self.death_time > 10:
                self.kill()

        if self.cur_mode == 'Death' and self.cur_frame == len(self.frames[self.cur_mode]) - 1:
            if self.death_time is None:
                self.death_time = time()
            return

        for sprite in all_sprites.sprites():
            if len(sprite.groups()) == 1 and self.cur_mode != 'Hurt' and sprite.cur_mode != 'Hurt':
                if self.coords[1].rect.x <= sprite.rect.x <= self.coords[0].rect.x + self.coords[0].rect.width \
                        and abs(sprite.rect.y - self.rect.y) < 30:

                    if sprite.cur_mode == 'Death':
                        if self.cur_mode != 'Idle':
                            self.change_mode('Idle')
                        return

                    if (self.rect.x - 55 > sprite.rect.x - sprite.rect.width
                        or self.rect.x + self.rect.width - 65 < sprite.rect.x) \
                            and self.cur_mode != 'Run':
                        self.change_mode('Run', sprite.rect.x)

                    if not (self.rect.x - 55 > sprite.rect.x - sprite.rect.width
                            or self.rect.x + self.rect.width - 65 < sprite.rect.x) \
                            and self.cur_mode != 'Attack' and sprite.cur_mode != 'Death':
                        self.change_mode('Attack')

                    if sprite.cur_mode == 'Attack' and sprite.cur_frame > 5 \
                            and pygame.sprite.spritecollideany(sprite, enemies):
                        self.change_mode('Hurt')

                    if self.cur_mode == 'Attack' and self.cur_frame >= 6 \
                            and pygame.sprite.spritecollideany(sprite, enemies):
                        sprite.change_mode('Hurt')

                elif len(sprite.groups()) == 1 and self.cur_mode != 'Idle':
                    self.change_mode('Idle')

        self.cur_frame = (self.cur_frame + 1) % len(self.frames[self.cur_mode])  # обновление спрайта
        self.image = self.frames[self.cur_mode][self.cur_frame]
        self.clock.tick(self.tick)
