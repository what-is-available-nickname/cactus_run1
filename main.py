import pygame
import sys
import os
import random


class Running_cactus(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.v = -25
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
        self.v += 2.5
        self.rect = self.rect.move(0, self.v)
        if self.rect[1] > 350:
            self.rect[1] = 350
            self.v = -25

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


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

    all_sprites = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()

    cactus = Running_cactus(load_image("cactus_running.png"), 8, 1, 250, 350)

    running = True
    jumping = False
    clock = pygame.time.Clock()

    while running:

        if cactus.get_y() == 350:
            jumping = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                jumping = True

        if jumping is True:
            cactus.jump()
        else:
            cactus.update()

        screen.fill(pygame.Color('black'))
        all_sprites.draw(screen)
        clock.tick(10)
        pygame.display.flip()
    pygame.quit()