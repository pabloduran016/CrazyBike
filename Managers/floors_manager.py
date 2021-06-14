import pygame.draw
import pymunk
from Floors import *
from settings.FLOORS import *
from random import randint
# from game import Physics
vec = pymunk.Vec2d


class FloorsManager(pygame.sprite.Sprite):
    def __init__(self, game, physics):
        """
        :type game: game.Game
        """
        pygame.sprite.Sprite.__init__(self)
        self.all = []
        self.game = game
        self.physics = physics

    def reset(self):
        self.all = []

    def start(self):
        # self.all.append(Line(self.game, position=Vec(x, y), final_pos=Vec(x, y) + Vec(512, -256), width=WIDTH))
        self.all.append(HorizontalLine(game=self.game, physics=self.physics, position=vec(*INITIALPOS), length=800,
                                       width=WIDTH))
        # self.all.append(ParabolaDown(game=self.game, position=Vec(x, y), length=500, height=800, width=WIDTH))
        # lastfloor: Floor = self.all[-1]
        # self.all.append(ParabolaUp(game=self.game, position=Vec(x, y), length=600, height=-800,
        #                          width=WIDTH))
        # self.game.coin_manager.generate(self.all[-1])

    def update(self):
        try:
            lastfloor: Floor = self.all[-1]
        except IndexError:
            print(self.all)
            raise
        distance = (lastfloor.body.position*self.game.zoom - self.game.camera.position).length
        while distance < 3000*self.game.zoom:
            # self.all.append(HorizontalLine(game=self.game, position=lastfloor.lastpoint,
            #                                length=800, width=WIDTH))
            selection = randint(1, 2)
            le = randint(500, 1400)
            # selection = 2
            if selection == 1:
                if len(self.all) > 2:  # LINE
                    h = randint(-60 * le, 80 * le) / 100
                    if h + self.all[-2].lastpoint.y > INITIALPOS[1]:  # If you go down, do you reach de bottom?
                        h = randint(-60 * le, 0) / 100
                else:
                    h = randint(-60 * le, 0) / 100
                self.all.append(Line(game=self.game, physics=self.physics, position=lastfloor.lastpoint,
                                     final_pos=lastfloor.lastpoint + vec(le, h), width=WIDTH))
            elif selection == 2:  # PARABOLA
                if len(self.all) > 2:
                    h = randint(-400, 800)
                    if h + self.all[-2].lastpoint.y > INITIALPOS[1]:  # If you go down, do you reach de bottom?
                        h = randint(-400, 0)
                        self.all.append(Parabola(game=self.game, physics=self.physics, position=lastfloor.lastpoint,
                                                 length=le, height=h, width=WIDTH, up=True))
                    else:
                        if h >= 0:
                            self.all.append(Parabola(game=self.game, physics=self.physics, position=lastfloor.lastpoint,
                                                     length=le, height=h, width=WIDTH, up=False))
                        else:
                            self.all.append(Parabola(game=self.game, physics=self.physics, position=lastfloor.lastpoint,
                                                     length=le, height=h, width=WIDTH, up=True))

                else:
                    # print('h')
                    h = randint(-400, 0)
                    self.all.append(Parabola(game=self.game, physics=self.physics, position=lastfloor.lastpoint,
                                             length=le, height=h, width=WIDTH, up=True))
            lastfloor: Floor = self.all[-1]
            self.game.coin_manager.generate(self.all[-1])
            self.all.append(HorizontalLine(game=self.game, physics=self.physics, position=lastfloor.lastpoint, length=500,
                                           width=WIDTH))
            self.game.coin_manager.generate(self.all[-1])
            lastfloor: Floor = self.all[-1]
            distance = (lastfloor.body.position - self.game.backwheel.body.position).length

        while len(self.all) > 30:
            self.all.pop(0)

    def draw(self):
        for floor in self.all:
            floor.draw()

        # pygame.draw.circle(self.game.screen, (0, 0, 0, 255), INITIALPOS, 10)