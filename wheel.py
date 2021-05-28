import pygame
import pymunk
from pymunk import Vec2d as Vec
from settings.WHEEL import *
from functions import blitrotate, scale, rad_to_degrees
import random
# from functions import load_svg


class Wheel(pygame.sprite.Sprite):
    def __init__(self, game, identity):
        """
        :type game: main.Game
        :type identity: str
        :param identity Frontwheel or Backwheel
        """
        super().__init__()
        self.game = game
        self.id = identity
        assert self.id == 'backwheel' or self.id == 'frontwheel', \
            f'INVALID ID, expected frontwheel or backwheel, got {identity}'
        self.color = COLOR
        self.radius = RADIUS
        self.width = WIDTH
        self.thetaacc = THETAACC
        # self.image = load_svg(IMAGE, size=DIMENSIONS).convert_alpha()
        self.image = pygame.image.load(IMAGE).convert_alpha()
        if self.id == 'backwheel':
            self.initial_position = Vec(*BACKWHEEL_INITIAL_POSITION)
        elif self.id == 'frontwheel':
            self.initial_position = Vec(*BACKWHEEL_INITIAL_POSITION) + Vec(DISTANCE, 0)
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.body.position = self.initial_position
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.density = DENSITY
        self.shape.friction = FRICTION
        self.shape.color = self.color
        self.shape.elasticity = ELASTICITY
        self.shape.collision_type = 1
        self.game.space.add(self.body, self.shape)
        self.shape.filter = pymunk.ShapeFilter(group=1)
        if self.id == 'backwheel':
            self.handler = self.game.space.add_collision_handler(1, 3)
            self.handler.separate = self.check_ground_separate
            self.handler.begin = self.check_ground_begin
            self.handler.pre_solve = self.check_ground_presolve

    def update(self):
        if self.id == 'backwheel':
            self.body.angular_velocity *= AIR_DRAG_MULTIPLIER
        if self.game.crushed:
            self.body.angular_velocity = random.randint(-300, 300)/100
            self.shape.sensor = True

    def reset(self):
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.body.position = self.initial_position
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.density = DENSITY
        self.shape.friction = FRICTION
        self.shape.color = self.color
        self.shape.elasticity = ELASTICITY
        self.shape.collision_type = 1
        self.game.space.add(self.body, self.shape)
        self.shape.filter = pymunk.ShapeFilter(group=1)
        if self.id == 'backwheel':
            self.handler = self.game.space.add_collision_handler(1, 3)
            self.handler.separate = self.check_ground_separate
            self.handler.begin = self.check_ground_begin
            self.handler.pre_solve = self.check_ground_presolve

    def draw(self):
        # if not self.game.crushed:
        im = scale(self.image, DIMENSIONS, self.game.zoom)
        rect = im.get_rect()
        # print(rect.size)
        rect.center = self.body.position*self.game.zoom - self.game.camera + self.game.displacement
        self.game.screen.blit(*blitrotate(im, Vec(*rect.center), Vec(rect.width/2, rect.height/2),
                                          rad_to_degrees(-self.body.angle)))
        # pygame.draw.circle(self.game.screen, self.color, self.body.position-self.game.camera, self.radius, self.width)

    def check_ground_presolve(self, arbiter, space, data):
        if self.game.airtime:
            # print('begin', self.game.board.checkground)
            self.game.airtime = 0
        return True

    def check_ground_begin(self, arbiter, space, data):
        self.game.board.checkground = 0
        if self.game.airtime:
            # print('begin', self.game.board.checkground)
            self.game.airtime = 0
        if not self.game.camera_shake and self.body.velocity.y > 15:
            # print('shake')
            self.game.camera_shake = 8
        return True

    def check_ground_separate(self, arbiter, space, data):
        self.game.board.checkground = 1
        if not self.game.airtime:
            # print('separate', self.game.board.checkground)
            self.game.airtime = 1
        return True
