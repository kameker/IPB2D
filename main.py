from json import load
from random import sample

import pygame as pg
import pymunk as pm
from pymunk import pygame_util
from objects_fun import ObjectsCreator
from world import World
from menu import PMenu


class Game():
    def __init__(self):
        self.WIDTH = 1920
        self.HEIGHT = 1000
        self.objects = []
        self.fps = 200
        self.caption = "IPB2D"

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
        world = World(self.WIDTH, self.HEIGHT, window)
        draw_options = pm.pygame_util.DrawOptions(window)
        menu = PMenu(self.WIDTH, self.HEIGHT, window)
        menu.start()
        self.name = menu.get_name()
        space = pm.Space()
        with open('StandartG.json', 'r') as f:
            data2 = load(f)
        g = int(data2['g'])
        print(g)
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
                        data = OCreator.openStandartS(type_o)

                        OCreator.add_obj(mouse_position, type_o, space, data[0], data[6], data[3], data[1], data[2],
                                         data[-1] * 3.1415926535 / 180, data[5])
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
                            menu.SettingsMenu.enable()
                            menu.show_settings(OCreator.get_info(space, mouse_position))
                            menu.SettingsMenu.mainloop(window)
                            menu.SettingsMenu.remove_widget(menu.SettingsMenu._widgets[-1])
                            OCreator.edit_object(space, mouse_position)
                            world.resume_object()
                            on = False
                        else:
                            menu.SaveMenu.mainloop(window)
                            name_file = menu.save_field()
                            if name_file == "":
                                for i in sample("0123456789", k=5):
                                    name_file += str(i)
                            OCreator.save_field(name_file)
                            run = False
                    if event.key == 122:
                        menu.showStandartS('квадрат')
                        menu.StandartObjectS.enable()
                        menu.StandartObjectS.mainloop(window)
                        menu.saveStandartS('StandartS.json')
                        menu.StandartObjectS.remove_widget(menu.StandartObjectS._widgets[-1])
                    if event.key == 120:
                        menu.showStandartS('круг')
                        menu.StandartObjectS.enable()
                        menu.StandartObjectS.mainloop(window)
                        menu.saveStandartS('StandartB.json')
                        menu.StandartObjectS.remove_widget(menu.StandartObjectS._widgets[-1])
                    if event.key == 118:
                        menu.StandartConnection.enable()
                        menu.showStandartJ()
                        menu.StandartConnection.mainloop(window)
                        menu.saveStandartConnection()
                    if event.key == 100 and on:
                        OCreator.set_90d_object((OCreator.searchf(space, mouse_position)))
                    elif event.key == pg.K_DELETE:
                        if on:
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


def run():
    game = Game()
    game.game_init()


run()
