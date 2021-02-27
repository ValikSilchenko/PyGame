import sys
from game_objects import *


pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
fon = pygame.transform.scale(load_image('data/Fon/sky.png'), (WIDTH, HEIGHT))
fon.blit(pygame.transform.scale(load_image('data/Fon/clouds.png'), (WIDTH, HEIGHT // 2)), (0, HEIGHT // 2))
pygame.display.set_caption('Warriori')
player = Warrior()


def terminate():
    """End of program working"""
    pygame.quit()
    sys.exit()


def load_menu(intro_text, level_index):
    """Load start menu"""
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 60)
    text_coord = 100
    color = (130, 24, 160)
    for line in intro_text:
        if line == 'No levels have found':
            string_rendered = font.render(line, True, pygame.Color('red'))
        else:
            string_rendered = font.render(line, True, pygame.Color(color))
        x_coord = WIDTH // 2 - string_rendered.get_size()[0] // 2
        screen.blit(string_rendered, (x_coord, text_coord))
        if line not in ['Warriori', 'No levels have found', 'Levels:'] and intro_text.index(line) == level_index:
            pygame.draw.rect(screen, color, (
                x_coord - 4, text_coord - 4, string_rendered.get_size()[0] + 8, string_rendered.get_size()[1] + 8
            ), width=2, border_radius=7)
            level_index = 1
        if line == 'Warriori':
            text_coord += 100
        else:
            text_coord += 70


def start_screen():
    have_levels = True
    clock = pygame.time.Clock()  # переменная clock для уменьшения нагрузки на процессор
    tick = 10
    intro_text = ['Warriori', 'Levels:'] + list(map(lambda x: x.split('.')[0], objects_in_dir('data/Levels', True)))
    if len(intro_text) == 1:
        intro_text += ['No levels have found']
        have_levels = False

    level_index = 2

    load_menu(intro_text, level_index)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and have_levels:
                tick = 0
                if event.key == pygame.K_RETURN:
                    return intro_text[level_index]  # начало игры
                elif event.key in [pygame.K_w, pygame.K_UP]:
                    level_index -= 1
                    if level_index <= 1:
                        level_index = len(intro_text) - 1
                    load_menu(intro_text, level_index)
                elif event.key in [pygame.K_s, pygame.K_DOWN]:
                    level_index += 1
                    if level_index >= len(intro_text):
                        level_index = 2
                    load_menu(intro_text, level_index)

        pygame.display.flip()
        clock.tick(tick)
        tick = 10


def render_level(level):
    """

    Render function, put all objects on screen.
    Objects designation(description: "sign"):
        empty space: ".";
        cliffs(leftb, midb, rightb): "-";
        land: "~";
        miniland: "_";

    """
    cliff_sprites = {
        '-': ['leftb.png', 'midb.png', 'rightb.png'],
        '~': ['land.png'],
        '_': ['miniland.png']
    }
    screen.blit(fon, (0, 0))
    level = list(reversed(level))
    max_y = None
    y = HEIGHT - 100
    for i in range(len(level)):
        k = 0
        x = 20
        for j in range(len(level[i])):
            if level[i][j] in cliff_sprites.keys() or level[i][j] == '@':
                if level[i][j] == level[i][j + 1] or level[i][j] == '@' or level[i][j + 1] == '@':
                    if level[i][j] == '@':
                        if level[i][j - 1] != '.':
                            key = level[i][j - 1]
                        else:
                            key = level[i][j + 1]
                    else:
                        key = level[i][j]
                    im = load_image('data/Cliffs/' + cliff_sprites[key][k])
                    k = 1
                elif len(cliff_sprites[level[i][j]]) > 1:
                    im = load_image('data/Cliffs/' + cliff_sprites[level[i][j]][k + 1])
                    k = 0
                else:
                    im = load_image('data/Cliffs/' + cliff_sprites[level[i][j]][k])
                c = Cliff(x, y, im)
                if max_y is None:
                    max_y = c
                if level[i][j] == '@':
                    player.rect.x = x + 20
                    h = player.image.get_height()
                    player.rect.y = y - h + 1
                x += c.rect.width
            else:
                x += 10
        y -= HEIGHT // len(level)
    return max_y


cam = Camera()
cam.set_cam(player)


def main():
    running = True

    # True - если игра на паузе(для pause) или игрок проигал(для game_over), False в противном случае
    pause = game_over = False

    pause_color = [110, 150, 101]  # цвет текста при паузе
    clock = pygame.time.Clock()  # переменная для регулировки скорости изменения цвета текста при паузе
    k = -4  # коэффициент для регулировки скорости изменения цвета текста при паузе
    key = None  # переменная, хранящая значение нажатой клавиши
    level = start_screen()
    lowest_cliff = render_level(load_level(f'data/Levels/{level}.txt'))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN:
                if game_over:
                    running = False
                    break
                elif event.key in [pygame.K_a, pygame.K_LEFT] and not pause:
                    player.change_mode('Run', -1)
                    key = event.key
                elif event.key in [pygame.K_d, pygame.K_RIGHT] and not pause:
                    player.change_mode('Run', 1)
                    key = event.key
                elif event.key == pygame.K_SPACE and not pause:
                    if player.cur_mode not in ['Jump', 'Fall']:
                        player.change_mode('Jump')
                elif event.key == pygame.K_ESCAPE:
                    if pause:
                        pause = False
                    else:
                        pause = True

            if not game_over:
                if event.type == pygame.KEYUP and not pause:
                    if event.key in [pygame.K_a, pygame.K_d, pygame.K_LEFT, pygame.K_RIGHT] and event.key == key:
                        if player.cur_mode != 'Attack':
                            player.change_mode('Idle')
                if event.type == pygame.MOUSEBUTTONDOWN and not pause:
                    if event.button == 1:
                        player.change_mode('Attack')

        if not (pause or game_over):
            player.move()
            cam.set_cam(player)  # обновление положения игрока

            screen.blit(fon, (0, 0))
            for sprite in all_sprites:
                sprite.update()
                cam.apply(sprite)
            all_sprites.draw(screen)
            if player.rect.y > lowest_cliff.rect.y + HEIGHT:
                game_over = True
                all_sprites.empty()
                cliffs.empty()
                player.__init__()
        else:
            font = pygame.font.Font(None, 80)
            if pause:
                text = font.render('PAUSE', True, pause_color)
                coords = (WIDTH // 2 - text.get_size()[0] // 2, HEIGHT // 2 - 80)
            else:
                text = font.render('Game over', True, (87, 91, 99))
                coords = (WIDTH // 2 - text.get_size()[0] // 2, HEIGHT // 2 - text.get_size()[1] // 2)
            screen.blit(text, coords)
            for i in range(3):
                if pause_color[i] + k < 0 or pause_color[i] + k > 255:
                    k = -k
                pause_color[i] += k
            clock.tick(5)

        pygame.display.flip()

    main()


if __name__ == '__main__':
    main()
