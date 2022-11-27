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
            if pos[1] < 900:
                self.shape_founded.body.position = pos
                self.shape_founded.body.velocity = 0, 0

    def draw_circle(self, position, space, r=12, width=1):
        search = space.point_query_nearest(position, 0, pm.ShapeFilter())
        if search is not None:
            if search.shape.collision_type == 0:
                doo_center = pm.pygame_util.to_pygame(search.shape.body.position, self)
                pg.draw.circle(self, [255, 0, 0], doo_center, r, width)

    def draw(self, space, window, draw_options):
        window.fill("gray")
        space.debug_draw(draw_options)
        pg.display.update()
