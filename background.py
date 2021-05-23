import pygame
from settings.BACKGROUND import *


class Background(pygame.sprite.Sprite):
    def __init__(self, game):
        """
        :type game: main.Game
        """
        super().__init__()
        self.game = game
        self.sky_image = pygame.image.load(SKY_IMAGE).convert_alpha()
        self.mountain_image = pygame.image.load(MOUNTAIN_IMAGE).convert_alpha()
        self.rect = self.sky_image.get_rect()
        self.sky_multiplier = SKY_MULTIPLIER
        self.mountain_multiplier = MOUNTAIN_MULTIPLIER

    def update(self):
        pass

    def draw(self):
        # SKY
        cam = self.game.camera * self.sky_multiplier
        x = int(cam.x / self.rect.width)
        y = int(cam.y / self.rect.height)
        for disp in ((0, 0), (0, 1), (1, 0), (1, 1), (0, -1), (1, -1), (-1, 0), (-1, -1), (-1, 1)):
            position = ((x+disp[0]) * self.rect.width, (y+disp[1]) * self.rect.height)
            self.game.screen.blit(self.sky_image, - cam + position)
        # MOUNTAINS
        cam = self.game.camera * self.mountain_multiplier
        x = int(cam.x / self.rect.width)
        y = 0
        for disp in ((0, 0), (1, 0), (-1, 0)):
            position = ((x + disp[0]) * self.rect.width, (y + disp[1]) * self.rect.height)
            self.game.screen.blit(self.mountain_image, - cam + position)
