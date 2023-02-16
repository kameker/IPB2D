from random import sample

import pygame as pg
import pymunk as pm
from pymunk import pygame_util
from objects_fun import ObjectsCreator
from settingsPy_ import start
from saveUI_ import sf
from world import World


class Game():
    def __init__(self, name):
        self.WIDTH = 1920
        self.HEIGHT = 1080
        self.objects = []
        self.fps = 144
        self.caption = "IPB2D"
        self.name = name

    def game_init(self):
        pg.init()
        si = pg.display.Info()
        self.WIDTH = si.current_w
        self.HEIGHT = si.current_h
        window = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption(self.caption)
        clock = pg.time.Clock()
        pm.pygame_util.positive_y_is_up = False
        self.game_run(window, clock)

    def game_run(self, window, clock):
        OCreator = ObjectsCreator(self.HEIGHT, self.WIDTH)
        draw_options = pm.pygame_util.DrawOptions(window)
        world = World(self.WIDTH, self.HEIGHT, window)
        space = pm.Space()
        g = 981
        space.gravity = 0, g
        PAUSE = False
        run = True
        on = False

        OCreator.ground(space)
        OCreator.load_field(space, self.name)
        type_o = "квадрат"
        type_j = "пружина"
        while run:
            mouse_position = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    break
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        OCreator.add_obj(mouse_position, type_o, space, 1, 20)
                    elif event.button == 1:
                        if on:
                            world.resume_object()
                            on = False
                        elif on == False and world.is_shape(space, mouse_position):
                            world.pick_object(world.is_shape(space, mouse_position))
                            on = True
                    elif event.button == 4 and on:
                        OCreator.rotate_object(OCreator.searchf(space, mouse_position), 1)
                    elif event.button == 5 and on:
                        OCreator.rotate_object(OCreator.searchf(space, mouse_position), -1)
                    elif event.button == 4:
                        if type_o == "квадрат":
                            type_o = "круг"
                        else:
                            type_o = "квадрат"
                    elif event.button == 5:
                        if type_j == "пружина":
                            type_j = "нить"
                        else:
                            type_j = "пружина"
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        if PAUSE:
                            OCreator.resume_all_objects()
                            PAUSE = False
                        else:
                            OCreator.stop_all_objects()
                            PAUSE = True
                    if event.key == 115:
                        if on:
                            start(OCreator.get_info(space, mouse_position))
                            OCreator.edit_object(space, mouse_position)
                            world.resume_object()
                            on = False
                        else:
                            sf()
                            with open("name.txt", "r") as namef:
                                name_file = namef.read()
                            if name_file == "":
                                for i in sample("0123456789", k=5):
                                    name_file += str(i)
                            OCreator.save_field(name_file)
                            run = False
                    if event.key == 100 and on:
                        OCreator.set_90d_object((OCreator.searchf(space, mouse_position)))
                    elif event.key == pg.K_DELETE:
                        OCreator.delete_object(space, OCreator.searchf(space, mouse_position))
                        on = False
                    elif event.key == pg.K_TAB:
                        OCreator.delete_all_objects(space)
                        world.resume_object()
                        on = False
                    elif event.key == pg.K_LSHIFT and on:
                        OCreator.rotate_object_45(OCreator.searchf(space, mouse_position))
                    elif event.key == 99:
                        OCreator.collect_shapes(space, mouse_position)
                    elif event.key == 106:
                        OCreator.connect_shapes(space, type_j)
                    elif event.key == 113:
                        run = False
            world.move_founded_object(mouse_position)
            world.draw(space, window, draw_options, type_o, clock, type_j)
            space.step(1 / self.fps)
            clock.tick(self.fps)
        pg.quit()


def run(name):
    game = Game(name)
    game.game_init()

# run()
