import json
from os import listdir
from os.path import isfile, join
from random import sample

import pygame_menu


class PMenu():

    def __init__(self, width, height, surface):
        self.WIDTH = width
        self.HEIGHT = height
        self.surface = surface
        self.MainMenu = pygame_menu.Menu('', self.WIDTH, self.HEIGHT,
                                         theme=pygame_menu.themes.THEME_BLUE)
        self.MainMenu.add.button('Новое поле', self.start_the_game)
        self.MainMenu.add.button('Загрузить поле', self.LoadMenu)
        self.MainMenu.add.button('Выход', pygame_menu.events.EXIT)

        self.fields = [f[0:-5] for f in listdir('fields') if isfile(join('fields', f))]
        for i in range(0, len(self.fields)):
            self.fields[i] = (self.fields[i], i + 1)
        self.FieldsMenu = pygame_menu.Menu('', self.WIDTH, self.HEIGHT,
                                           theme=pygame_menu.themes.THEME_BLUE)
        self.FieldsMenu.add.selector('Поле :', self.fields)
        self.FieldsMenu.add.button('Загрузить', self.load_field)
        self.FieldsMenu.add.button('Выход', self.openMain)
        self.name = ""

        self.SaveMenu = pygame_menu.Menu('', self.WIDTH, self.HEIGHT,
                                         theme=pygame_menu.themes.THEME_BLUE)
        self.name_field = ""
        for i in sample("0123456789", k=5):
            self.name_field += str(i)
        self.SaveMenu.add.text_input('Название :', default=self.name_field)
        self.SaveMenu.add.button('Сохранить', self.save_field)
        self.SaveMenu.add.button('Выход', pygame_menu.events.EXIT)

        self.SettingsMenu = pygame_menu.Menu('', self.WIDTH, self.HEIGHT,
                                             theme=pygame_menu.themes.THEME_BLUE)
        self.SettingsMenu.add.text_input('Масса: ', default=self.name_field)
        self.SettingsMenu.add.text_input('Коэффициент трения: ', default=0)
        self.SettingsMenu.add.text_input('Коэффициент упругости: ', default=0)
        self.SettingsMenu.add.text_input('Красный R: ', default=0)
        self.SettingsMenu.add.text_input('Зелёный G: ', default=0)
        self.SettingsMenu.add.text_input('Синий B: ', default=0)
        self.SettingsMenu.add.text_input('Прозрачность: ', default=0)
        self.SettingsMenu.add.text_input('Длина: ', default=0)
        self.SettingsMenu.add.text_input('Ширина: ', default=0)
        self.SettingsMenu.add.text_input('Угол: ', default=0)
        self.SettingsMenu.add.text_input('X: ', default=0)
        self.SettingsMenu.add.text_input('Y: ', default=0)
        self.SettingsMenu.add.button('Сохранить', self.save_settings)
        self.SettingsMenu.add.button('Выход', self.exits())
        self.objects = 0

    def openMain(self):
        self.FieldsMenu.disable()
        self.MainMenu.enable()
        #self.MainMenu.mainloop(self.surface)

    def exits(self):
        self.SettingsMenu.disable()

    def save_settings(self):
        color = [int(self.SettingsMenu._widgets[3].get_value()), int(self.SettingsMenu._widgets[4].get_value()),
                 int(self.SettingsMenu._widgets[5].get_value()), int(self.SettingsMenu._widgets[6].get_value())]
        f = str(self.objects[0])[15:str(self.objects[0]).index(' ')]
        if f == "Circle":
            t = "круг"
            size = float(self.SettingsMenu._widgets[7].get_value())
        elif f == "Poly":
            t = "квадрат"
            size = [float(self.SettingsMenu._widgets[7].get_value()), float(self.SettingsMenu._widgets[8].get_value())]
        btype = self.SettingsMenu._widgets[-1].get_value()[1]
        d = {0: {
            "mass": float(self.SettingsMenu._widgets[0].get_value()),
            "friction": float(self.SettingsMenu._widgets[1].get_value()),
            "elasticity": float(self.SettingsMenu._widgets[2].get_value()),
            "color": color,
            'position': [float(self.SettingsMenu._widgets[10].get_value()),
                         float(self.SettingsMenu._widgets[11].get_value())],
            'shape': t,
            'body_type': btype,
            'args': size,
            'angle': float(self.SettingsMenu._widgets[9].get_value()) * 3.1415926535 / 180
        }}
        data = json.dumps(d)
        data = json.loads(str(data))
        with open('object.json', "w") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        self.SettingsMenu.disable()

    def show_settings(self, objects):
        self.objects = objects
        f = str(objects[0])[15:str(objects[0]).index(' ')]
        if f == "Circle":
            size = objects[0].radius
            h = 0
            self.SettingsMenu._widgets[7].set_title("Радиус: ")
            self.SettingsMenu._widgets[8].hide()
        elif f == "Poly":
            self.SettingsMenu._widgets[7].set_title("Длина: ")
            self.SettingsMenu._widgets[8].show()
            size = abs(objects[0].get_vertices()[0][0])
            h = abs(objects[0].get_vertices()[0][1])
        self.SettingsMenu._widgets[0].set_value(str(objects[0].mass))
        self.SettingsMenu._widgets[1].set_value(str(objects[0].friction))
        self.SettingsMenu._widgets[2].set_value(str(objects[0].elasticity))
        self.SettingsMenu._widgets[3].set_value(str(objects[0].color[0]))
        self.SettingsMenu._widgets[4].set_value(str(objects[0].color[1]))
        self.SettingsMenu._widgets[5].set_value(str(objects[0].color[2]))
        self.SettingsMenu._widgets[6].set_value(str(objects[0].color[3]))
        self.SettingsMenu._widgets[7].set_value(str(size))
        self.SettingsMenu._widgets[8].set_value(str(h))
        self.SettingsMenu._widgets[9].set_value(
            str(float(str(objects[1]._get_angle())[0:10]) * 180 / 3.1415926535)[0:7])
        self.SettingsMenu._widgets[10].set_value(str(objects[1].position[0])[0:6])
        self.SettingsMenu._widgets[11].set_value(str(objects[1].position[1])[0:6])

        if objects[1].body_type == 0:
            self.SettingsMenu.add.selector('Состояние:', [("Динамическое", 0), ("Статичное", 1)])
        else:
            self.SettingsMenu.add.selector('Состояние:', [("Статичное", 0), ("Динамическое", 1)])

    def save_field(self):
        self.SaveMenu.disable()
        return self.SaveMenu._widgets[0].get_value()

    def get_name(self):
        return self.name

    def load_field(self):
        self.name = self.FieldsMenu._widgets[0].get_value()[0][0]
        self.FieldsMenu.disable()

    def start(self):
        self.MainMenu.mainloop(self.surface)

    def LoadMenu(self):
        self.MainMenu.disable()
        self.FieldsMenu.enable()
        self.FieldsMenu.mainloop(self.surface)

    def start_the_game(self):
        self.MainMenu.disable()
