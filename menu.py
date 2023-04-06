import json
from os import listdir
from os.path import isfile, join
from random import sample
from json import load
import pygame_menu


class PMenu():

    def __init__(self, width, height, surface):
        self.WIDTH = width
        self.HEIGHT = height
        self.surface = surface

        self.StandartG = pygame_menu.Menu('', self.WIDTH, self.HEIGHT,
                                          theme=pygame_menu.themes.THEME_BLUE)
        self.StandartG.add.text_input('Ускорение свободного падения: ')
        self.StandartG.add.button('Сохранить', self.saveStandartG)
        self.StandartG.add.button('Выход', self.closeStandartG)

        self.MainMenu = pygame_menu.Menu('', self.WIDTH, self.HEIGHT,
                                         theme=pygame_menu.themes.THEME_BLUE)
        self.MainMenu.add.button('Новое поле', self.start_the_game)
        self.MainMenu.add.button('Загрузить поле', self.LoadMenu)
        self.MainMenu.add.button('Настройки', self.openStandartG)
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
        self.objects = 0

        self.StandartObjectS = pygame_menu.Menu('', self.WIDTH, self.HEIGHT,
                                                theme=pygame_menu.themes.THEME_BLUE)
        self.StandartObjectS.add.text_input('Масса: ', default=self.name_field)
        self.StandartObjectS.add.text_input('Коэффициент трения: ', default=0)
        self.StandartObjectS.add.text_input('Коэффициент упругости: ', default=0)
        self.StandartObjectS.add.text_input('Красный R: ', default=0)
        self.StandartObjectS.add.text_input('Зелёный G: ', default=0)
        self.StandartObjectS.add.text_input('Синий B: ', default=0)
        self.StandartObjectS.add.text_input('Прозрачность: ', default=0)
        self.StandartObjectS.add.text_input('Длина: ', default=0)
        self.StandartObjectS.add.text_input('Ширина: ', default=0)
        self.StandartObjectS.add.text_input('Угол: ', default=0)
        self.StandartObjectS.add.text_input('X: ', default=0)
        self.StandartObjectS.add.text_input('Y: ', default=0)
        self.StandartObjectS.add.button('Сохранить', self.closeStandartS)

        self.StandartConnection = pygame_menu.Menu('', self.WIDTH, self.HEIGHT,
                                                   theme=pygame_menu.themes.THEME_BLUE)
        self.StandartConnection.add.text_input('Коэфецент жёсткости: ', default=self.name_field)
        self.StandartConnection.add.button('Сохранить', self.closeStandartConnection)
        self.StandartConnection.add.button('Выход', self.closeStandartConnection)



    def saveStandartG(self):
        with open("StandartG.json", "w") as file:
            d = {
                "g": self.StandartG._widgets[0].get_value()
            }
            data = json.dumps(d)
            data = json.loads(str(data))
            json.dump(data, file, indent=4, ensure_ascii=False)
        self.closeStandartG()

    def closeStandartG(self):
        self.StandartG.disable()
        self.MainMenu.enable()
        self.MainMenu.mainloop(self.surface)

    def openStandartG(self):
        self.StandartG.enable()
        with open('StandartG.json', 'r') as f:
            data = load(f)
        self.StandartG._widgets[0].set_value(data['g'])
        self.StandartG.mainloop(self.surface)
        self.MainMenu.disable()

    def closeStandartConnection(self):
        self.StandartConnection.disable()

    def saveStandartConnection(self):
        d = {
            "k": float(self.StandartConnection._widgets[0].get_value())
        }
        data = json.dumps(d)
        data = json.loads(str(data))
        with open("StandartJ.json", "w") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def showStandartJ(self):
        with open('StandartJ.json', 'r') as f:
            data = load(f)
        self.StandartConnection._widgets[0].set_value(str(data['k']))

    def showStandartS(self, ob):
        if ob == "ball":
            with open('StandartB.json', 'r') as f:
                data = load(f)['0']
            size = data['args'][0]
            h = 0
            self.StandartObjectS._widgets[7].set_title("Радиус: ")
            self.StandartObjectS._widgets[8].hide()
        elif ob == "square":
            with open('StandartS.json', 'r') as f:
                data = load(f)['0']
            self.StandartObjectS._widgets[7].set_title("Длина: ")
            self.StandartObjectS._widgets[8].show()
            size = data['args'][0]
            h = data['args'][1]
        self.StandartObjectS._widgets[0].set_value(str(data['mass']))
        self.StandartObjectS._widgets[1].set_value(str(data['friction']))
        self.StandartObjectS._widgets[2].set_value(str(data['elasticity']))
        self.StandartObjectS._widgets[3].set_value(str(data['color'][0]))
        self.StandartObjectS._widgets[4].set_value(str(data['color'][1]))
        self.StandartObjectS._widgets[5].set_value(str(data['color'][2]))
        self.StandartObjectS._widgets[6].set_value(str(data['color'][3]))
        self.StandartObjectS._widgets[7].set_value(str(size))
        self.StandartObjectS._widgets[8].set_value(str(h))
        self.StandartObjectS._widgets[9].set_value(data['angle'])
        self.StandartObjectS._widgets[10].set_value(str(data['position'][0]))
        self.StandartObjectS._widgets[11].set_value(str(data['position'][1]))
        print(data['body_type'])
        if data['body_type'] == 0:
            self.StandartObjectS.add.selector('Состояние:', [("Динамическое", 0), ("Статичное", 1)])
        else:
            self.StandartObjectS.add.selector('Состояние:', [("Статичное", 0), ("Динамическое", 1)])

    def saveStandartS(self, f):
        color = [int(self.StandartObjectS._widgets[3].get_value()), int(self.StandartObjectS._widgets[4].get_value()),
                 int(self.StandartObjectS._widgets[5].get_value()), int(self.StandartObjectS._widgets[6].get_value())]
        t = "квадрат"
        size = [float(self.StandartObjectS._widgets[7].get_value()),
                float(self.StandartObjectS._widgets[8].get_value())]
        btype = self.StandartObjectS._widgets[-1].get_value()[0][0]
        if btype == "Динамическое":
            btype = 0
        else:
            btype = 1
        d = {0: {
            "mass": float(self.StandartObjectS._widgets[0].get_value()),
            "friction": float(self.StandartObjectS._widgets[1].get_value()),
            "elasticity": float(self.StandartObjectS._widgets[2].get_value()),
            "color": color,
            'position': [float(self.StandartObjectS._widgets[10].get_value()),
                         float(self.StandartObjectS._widgets[11].get_value())],
            'shape': t,
            'body_type': btype,
            'args': size,
            'angle': float(self.StandartObjectS._widgets[9].get_value())
        }}
        data = json.dumps(d)
        data = json.loads(str(data))
        with open(f, "w") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        self.StandartObjectS.disable()

    def closeStandartS(self):
        self.StandartObjectS.disable()

    def closeSettings(self):
        self.SettingsMenu.disable()

    def StandartS(self):
        self.StandartObjectS.mainloop(self.surface)

    def openMain(self):
        self.FieldsMenu.disable()
        self.MainMenu.enable()
        # self.MainMenu.mainloop(self.surface)

    def exits(self):
        self.SettingsMenu.disable()

    def save_settings(self):
        color = [int(self.SettingsMenu._widgets[3].get_value()), int(self.SettingsMenu._widgets[4].get_value()),
                 int(self.SettingsMenu._widgets[5].get_value()), int(self.SettingsMenu._widgets[6].get_value())]
        f = str(self.objects[0])[15:str(self.objects[0]).index(' ')]
        if f == "Circle":
            t = "ball"
            size = float(self.SettingsMenu._widgets[7].get_value())
        elif f == "Poly":
            t = "square"
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
