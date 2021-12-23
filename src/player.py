import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()
        self.image = pygame.Surface((32, 64))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
        self.is_jump = False

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            self.jump()

    def get_input_player1(self, keys):
        # keys = pygame.key.get_pressed()
        #
        # if keys[pygame.K_RIGHT]:
        #     self.direction.x = 1
        # elif keys[pygame.K_LEFT]:
        #     self.direction.x = -1
        # else:
        #     self.direction.x = 0
        #
        # if keys[pygame.K_UP]:
        #     self.jump()
        if keys['right']:
            self.direction.x = 1
        elif keys['left']:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys['jump']:
            self.jump()

    def get_input_player2(self, keys, x_shift):
        # keys = pygame.key.get_pressed()
        #
        # if keys[pygame.K_d]:
        #     self.direction.x = 1
        # elif keys[pygame.K_a]:
        #     self.direction.x = -1
        # else:
        #     self.direction.x = 0
        #
        # if keys[pygame.K_w]:
        #     self.jump()
        #
        # self.rect.x += x_shift

        if keys['right2']:
            self.direction.x = 1
        elif keys['left2']:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys['jump2']:
            self.jump()

        self.rect.x += x_shift

    def set_directions(self, player_no, keys, x_shift):
        if keys['right']:
            self.direction.x = 1
        elif keys['left']:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys['jump']:
            self.jump()

        if player_no == 2:
            self.rect.x += x_shift

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        if not self.is_jump:
            self.direction.y = self.jump_speed
            self.is_jump = True

    def update_old(self):
        self.get_input()

    def update_player1(self, keys):
        self.get_input_player1(keys)

    def update_player2(self, keys, x_shift):
        self.get_input_player2(keys, x_shift)

    def update(self, player_no, keys, x_shift):
        if player_no == 1:
            self.get_input_player1(keys)
        else:
            self.get_input_player2(keys, x_shift)
        # self.set_directions(player_no, keys, x_shift)



