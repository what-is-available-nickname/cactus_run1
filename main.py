import pygame
import sys
import os

V = -3
GAME_RUNNING = True


class Background1(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__(all_sprites)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 0

    def update(self, *args):
        self.rect = self.rect.move(V, 0)
        if self.rect[0] <= -1200:
            self.rect.x = 1200


class Background2(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__(all_sprites)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 1200

    def update(self, *args):
        self.rect = self.rect.move(V, 0)
        if self.rect[0] <= -1200:
            self.rect[0] = 1200


class Running_cactus(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.v = -14
        self.g = 0.6
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
        print(self.rect.size)

    def get_y(self):
        return self.rect[1]

    def jump(self):
        self.v += self.g
        self.rect = self.rect.move(0, self.v)
        if self.rect[1] > 430:
            self.rect[1] = 430
            self.v = -14

    def update(self):
        global GAME_RUNNING
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.g += 0.0002
        if pygame.sprite.collide_mask(self, enemy):
            print(1)
            GAME_RUNNING = False


class Enemy(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(1200, 450)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
        print(self.rect.size)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(V, 0)
        if self.rect[0] <= -100:
            self.rect[0] = 1300


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Гугл динозавр наоборот')
    size = width, height = 1200, 600
    screen = pygame.display.set_mode(size)
    font = pygame.freetype.Font(None, 40)
    all_sprites = pygame.sprite.Group()
    record = open('record.txt', 'r')
    best_score = int(record.readline())
    record.close()

    background1 = Background1(load_image('background1.png'))
    background2 = Background2(load_image('background2.png'))
    cactus = Running_cactus(load_image("cactus_running.png"), 8, 1, 250, 430)
    enemy = Enemy(load_image('enemy.png'), 8, 2)

    running = True
    jumping = False
    score = 0
    clock = pygame.time.Clock()

    while running:

        if cactus.get_y() == 430:
            jumping = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                jumping = True

        all_sprites.draw(screen)

        pygame.draw.rect(screen, 'white', ((940, 110), (235, 100)), 100)
        font.render_to(screen, (1000, 170), f'Счёт: {str(round(score))}', (0, 0, 0))
        if round(score) < best_score:
            font.render_to(screen, (950, 120), f'Рекорд: {str(best_score)}', (0, 0, 0))
        else:
            font.render_to(screen, (950, 120), f'Рекорд: {str(round(score))}', (0, 0, 0))

        if GAME_RUNNING is True:
            enemy.update()
            background1.update()
            background2.update()

            score += -V / 100
            V -= 0.005

            if jumping is True:
                cactus.jump()
            else:
                cactus.update()
        else:
            pygame.draw.rect(screen, 'white', ((490, 190), (320, 55)), 100)
            font.render_to(screen, (500, 200), f'Игра окончена!', (0, 0, 0))
            if round(score) > best_score:
                record = open('record.txt', 'w')
                record.write(str(round(score)))
                record.close()
                pygame.draw.rect(screen, 'white', ((490, 240), (320, 55)), 100)
                font.render_to(screen, (500, 250), f'Новый рекорд!', (0, 0, 0))

        clock.tick(30)
        pygame.display.flip()
    pygame.quit()