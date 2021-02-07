from game_objects import *

WIDTH, HEIGHT = 500, 660
FPS = 50

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
field = pygame.Surface([WIDTH, HEIGHT])
pygame.display.set_caption('Перемещение героя')


def start_screen():
    intro_text = ["ЗАСТАВКА"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def main():
    player = Warrior(50, 50)
    running = True
    change = False
    key = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_a, pygame.K_LEFT, pygame.K_d, pygame.K_RIGHT]:
                    change = True
                    key = event.key
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_a, pygame.K_d, pygame.K_LEFT, pygame.K_RIGHT]:
                    player.change_mode('Idle')

        if change:
            if key in [pygame.K_a, pygame.K_LEFT]:
                player.change_mode('Run', -1)
            elif key in [pygame.K_d, pygame.K_RIGHT]:
                player.change_mode('Run', 1)
            change = False

        player.move()

        screen.fill('black')
        for sprite in all_sprites:
            sprite.update()
        all_sprites.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    sys.exit(main())
