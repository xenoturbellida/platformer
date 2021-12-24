import pygame

from tiles import Tile, StaticTile, AnimatedTile, Star
from player import Player
from settings import tile_size, screen_width
from particles import ParticleEffect
from support import import_csv_layout, import_cut_graphics


class Level:
    def __init__(self, level_data, surface):
        # general setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = 0
        self.level_data = level_data

        # player
        player_layout = import_csv_layout((level_data['player']))
        player_layout2 = import_csv_layout((level_data['player2']))
        self.player1 = pygame.sprite.GroupSingle()
        self.player2 = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout, player_layout2)

        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # stars
        star_layout = import_csv_layout(level_data['stars'])
        self.star_sprites = self.create_tile_group(star_layout, 'stars')

        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    sprite = None
                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('../graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        # sprite_group.add(sprite)

                    if type == 'stars':
                        if val == '0':
                            sprite = AnimatedTile(tile_size, x, y, '../graphics/stars/blue')
                            # sprite = Star(tile_size, x, y, '../graphics/stars/blue')
                        if val == '1':
                            sprite = AnimatedTile(tile_size, x, y, '../graphics/stars/pink')
                            # sprite = Star(tile_size, x, y, '../graphics/stars/pink')
                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout, layout2):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles)
                    self.player1.add(sprite)
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles)
                    self.player2.add(sprite)
                if val == '1':
                    hat_surface = pygame.image.load('../graphics/character/hat.png')
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)

        for row_index, row in enumerate(layout2):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles)
                    self.player2.add(sprite)

    def create_jump_particles(self, pos):
        if self.player1.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def get_player_on_ground(self, player):
        if player.on_ground:
            player.player_on_ground = True
        else:
            player.player_on_ground = False

    def create_landing_dust(self, player):
        if not player.player_on_ground and player.on_ground and not self.dust_sprite.sprites():
            if player.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particle = ParticleEffect(player.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)

    # old method
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
                    player_sprite = Player((x, y), self.display_surface, self.create_jump_particles)
                    self.player1.add(player_sprite)
                if cell == '2':
                    player_sprite = Player((x, y), self.display_surface, self.create_jump_particles)
                    self.player2.add(player_sprite)

    def scroll_x(self):
        player1 = self.player1.sprite
        player2 = self.player2.sprite
        player_x = player1.rect.centerx
        direction_x = player1.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player1.speed = 0
        elif player_x > screen_width - screen_width / 4 and direction_x > 0:
            self.world_shift = -8
            player1.speed = 0
        else:
            self.world_shift = 0
            player1.speed = 8

    def horizontal_movement_collisions(self):
        for player in [self.player1.sprite, self.player2.sprite]:
            player.rect.x += player.direction.x * player.speed

            for sprite in self.terrain_sprites.sprites():
                if sprite.rect.colliderect(player.rect):
                    if player.direction.x < 0:
                        player.rect.left = sprite.rect.right
                        player.on_left = True
                        self.current_x = player.rect.left
                    elif player.direction.x > 0:
                        player.rect.right = sprite.rect.left
                        player.on_right = True
                        self.current_x = player.rect.right

            if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
                player.on_left = False
            if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
                player.on_right = False

    def vertical_movement_collision(self):
        for player in [self.player1.sprite, self.player2.sprite]:
            player.apply_gravity()

            for sprite in self.terrain_sprites.sprites():
                if sprite.rect.colliderect(player.rect):
                    if player.direction.y > 0:
                        player.rect.bottom = sprite.rect.top
                        player.direction.y = 0
                        player.on_ground = True
                        player.is_jump = False
                    elif player.direction.y < 0:
                        player.rect.top = sprite.rect.bottom
                        player.direction.y = 0
                        player.on_ceiling = True

            # if a player is jumping or falling, then the player are not on ground anymore
            if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
                player.on_ground = False
            # if a player is falling, then the player are not on ceiling anymore
            if player.on_ceiling and player.direction.y > 0:
                player.on_ceiling = False

    def player_fall(self):
        for player in [self.player1.sprite, self.player2.sprite]:
            if player.rect.bottom > 1500:
                self.setup_level(self.level_data)
                pygame.time.wait(500)

    def run(self, keys_pl):
        # run the entire game / level

        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # stars
        self.star_sprites.update(self.world_shift)
        self.star_sprites.draw(self.display_surface)

        # dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # player sprites
        self.player1.update(1, keys_pl, self.world_shift)
        self.player2.update(2, keys_pl, self.world_shift)
        self.player_fall()
        self.horizontal_movement_collisions()
        self.vertical_movement_collision()
        for player in [self.player1.sprite, self.player2.sprite]:
            self.get_player_on_ground(player)
            self.create_landing_dust(player)
        self.scroll_x()
        self.player1.draw(self.display_surface)
        self.player2.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
