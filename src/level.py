import pygame

from tiles import Tile
from player import Player
from settings import tile_size, screen_width


class Level:
    def __init__(self, level_data, surface):

        # level setup
        self.display_surface = surface
        self.level_data = level_data
        self.setup_level(level_data)

        self.world_shift = 0

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player1 = pygame.sprite.GroupSingle()
        self.player2 = pygame.sprite.GroupSingle()
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):

                x = col_index * tile_size
                y = row_index * tile_size

                if cell == 'X':
                    tile = Tile(pos=(x, y), size=tile_size)
                    self.tiles.add(tile)
                if cell == '1':
                    player_sprite1 = Player(pos=(x, y), color='red')
                    self.player1.add(player_sprite1)
                if cell == '2':
                    player_sprite2 = Player(pos=(x, y), color='green')
                    self.player2.add(player_sprite2)

    def scroll_x(self):
        player1 = self.player1.sprite
        player2 = self.player2.sprite
        player_x = player1.rect.centerx
        direction_x = player1.direction.x

        if player_x < screen_width/4 and direction_x < 0:
            self.world_shift = 8
            player1.speed = 0
            # player2.speed = 0
        elif player_x > screen_width - screen_width/4 and direction_x > 0:
            self.world_shift = -8
            player1.speed = 0
            # player2.speed = 0
        else:
            self.world_shift = 0
            player1.speed = 8
            # player2.speed = 8

    def horizontal_movement_collisions(self):
        for player in [self.player1.sprite, self.player2.sprite]:
            # player = self.player.sprite
            player.rect.x += player.direction.x * player.speed

            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(player.rect):
                    if player.direction.x < 0:
                        player.rect.left = sprite.rect.right
                    elif player.direction.x > 0:
                        player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        for player in [self.player1.sprite, self.player2.sprite]:
            # player = self.player.sprite
            player.apply_gravity()

            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(player.rect):
                    if player.direction.y > 0:
                        player.rect.bottom = sprite.rect.top
                        player.direction.y = 0
                        player.is_jump = False
                    elif player.direction.y < 0:
                        player.rect.top = sprite.rect.bottom
                        player.direction.y = 0

    def player_death(self):
        for player in [self.player1.sprite, self.player2.sprite]:
            # player = self.player.sprite
            if player.rect.bottom > 1500:
                self.setup_level(self.level_data)
                pygame.time.wait(500)


    def run(self, keys_pl):

        # level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        # player
        # self.player.update()
        self.player1.update(1, keys_pl, self.world_shift)
        self.player2.update(2, keys_pl, self.world_shift)
        # self.player1.update_player1(keys_pl1)
        # self.player2.update_player2(keys_pl2, self.world_shift)
        self.horizontal_movement_collisions()
        self.vertical_movement_collision()
        self.player_death()
        self.player1.draw(self.display_surface)
        self.player2.draw(self.display_surface)


