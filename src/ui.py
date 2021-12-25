import pygame


class UI:
    def __init__(self, surface):
        self.display_surface = surface

        # coins
        self.star = pygame.image.load('../graphics/stars/pink/pink_1.png').convert_alpha()
        self.star_rect = self.star.get_rect(topleft=(30, 30))
        self.font = pygame.font.SysFont('Comic Sans MS', 25)

    def show_coins(self, amount):
        self.display_surface.blit(self.star, self.star_rect)
        star_amount_surf = self.font.render(str(amount), False, '#C71585')
        star_amount_rect = star_amount_surf.get_rect(midleft=(self.star_rect.right + 3, self.star_rect.centery - 4))
        self.display_surface.blit(star_amount_surf, star_amount_rect)
