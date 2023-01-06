import pygame as pg
import pymunk as pm
from pymunk import pygame_util


class World(pg.Surface):

    def __init__(self, width, height, window, color=None):
        super().__init__([width, height])
        if color is None:
            color = [250, 250, 250]
        self.width = width
        self.height = height
        self.color = color
        self.window = window
        self.shape_founded = None
        self.ground_y = self.height - 10

    def is_shape(self, space, position):
        search = space.point_query_nearest(position, 0, pm.ShapeFilter())
        if search is not None:
            if search.shape.collision_type == 0:
                return search

    def pick_object(self, search):
        self.shape_founded = search.shape

    def resume_object(self):
        self.shape_founded = None

    def move_founded_object(self, pos):
        if self.shape_founded is not None:
            if pos[1] < 1000:
                self.shape_founded.body.position = pos
                self.shape_founded.body.velocity = 0, 0


    def draw(self, space, window, draw_options, type_o,clock, type_j):
        window.fill("gray")
        font1 = pg.font.SysFont('standart.ttf', 25)
        fps = font1.render('{0:.0f}'.format(clock.get_fps()) + " fps", True, [50, 50, 50])
        text1 = font1.render(f'{type_o}', True, (100, 100, 100))
        text2 = font1.render(f'{type_j}', True, (100, 100, 100))

        textRect1 = text1.get_rect()
        textRect1.center = (100, 50)

        textRect2 = text2.get_rect()
        textRect2.center = (1800, 50)

        tfps = fps.get_rect()
        tfps.center = (900, 50)

        window.blit(text1, textRect1)
        window.blit(fps, tfps)
        window.blit(text2, textRect2)
        space.debug_draw(draw_options)
        pg.display.update()
