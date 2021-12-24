import pygame


class UI:
    def __init__(self, surface):
        self.display_surface = surface

        # coins
        self.coin = pygame.image.load('../graphics/stars/star_tiles.png')

    def show_coins(self):
        pass
