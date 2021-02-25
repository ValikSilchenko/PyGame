import sys
from game_objects import *


pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
fon = pygame.transform.scale(load_image('data/Fon/sky.png'), (WIDTH, HEIGHT))
fon.blit(pygame.transform.scale(load_image('data/Fon/clouds.png'), (WIDTH, HEIGHT // 2)), (0, HEIGHT // 2))
pygame.display.set_caption('Warriori')
player = Warrior()


def render_level(level):
    level = list(reversed(level))
    y = HEIGHT - 100
    for i in range(len(level)):
        f = True
        x = 20
        for j in range(len(level[i])):
            if level[i][j] == '-' or level[i][j] == '@':
                if f:
                    f = False
                    im = load_image('data/Cliffs/leftb.png')
                else:
                    if j + 1 < len(level[i]):
                        if level[i][j + 1] == '-':
                            im = load_image('data/Cliffs/midb.png')
                        elif level[i][j + 1] == '.':
                            im = load_image('data/Cliffs/rightb.png')
                            f = True
                c = Cliff(x, y, im)
                if level[i][j] == '@':
                    player.rect.x = x + 20
                    h = player.image.get_height()
                    player.rect.y = y - h + 1
                x += c.rect.width
            else:
                x += 10
        y -= HEIGHT // len(level)


cam = Camera()
cam.set_cam(player)


def main():
    clock = pygame.time.Clock()
    running = True
    key = None
    render_level(load_level('data/Levels/level1.txt'))
    while running:
        for i, event in enumerate(pygame.event.get()):
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_a, pygame.K_LEFT]:
                    player.change_mode('Run', -1)
                    key = event.key
                elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                    player.change_mode('Run', 1)
                    key = event.key
                elif event.key == pygame.K_SPACE:
                    if player.cur_mode not in ['Jump', 'Fall']:
                        player.change_mode('Jump')
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_a, pygame.K_d, pygame.K_LEFT, pygame.K_RIGHT] and event.key == key:
                    if player.cur_mode != 'Attack':
                        player.change_mode('Idle')
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.change_mode('Attack')

        player.move()
        cam.set_cam(player)

        screen.blit(fon, (0, 0))
        for sprite in all_sprites:
            sprite.update()
            cam.apply(sprite)
        all_sprites.draw(screen)

        clock.tick(100)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    sys.exit(main())
