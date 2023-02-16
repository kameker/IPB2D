import pymunk
import pymunk as pm
import json
import os.path
from random import sample
from math import degrees, radians
from saveUI_ import sf



class ObjectsCreator:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.objects = []
        self.bodyO = []
        self.shapeO = []
        self.id = 0
        self.d = {}
        self.window2 = 0
        self.cshapes = [None, None]
        self.flag = True
        self.sshapes = []
        self.objects_for_save = []

    def searchf(self, space, position):
        search = space.point_query_nearest(position, 0, pm.ShapeFilter())
        if search is not None:
            if search.shape.collision_type == 0:
                return search.shape

    def collect_shapes(self, space, position):
        search = space.point_query_nearest(position, 0, pm.ShapeFilter())
        if search is not None:
            if search.shape.collision_type == 0:
                if self.flag:
                    self.cshapes[0] = search.shape
                    self.flag = False
                else:
                    self.cshapes[1] = search.shape

    def ground(self, space):
        rects = [
            [(self.width / 2, self.height - 10), (self.width, 20)],
            [(self.width / 2, 10), (self.width, 20)],
            [(10, self.height / 2), (20, self.height)],
            [(self.width - 10, self.height / 2), (20, self.height)]
        ]
        for pos, size in rects:
            body = pm.Body(body_type=pm.Body.STATIC)
            body.position = pos

            shape = pm.Poly.create_box(body, size)
            shape.friction = 0.3
            shape.elasticity = 1
            space.add(body, shape)

    def set_90d_object(self, searchd):
        self.bodyO[self.shapeO.index(searchd)]._set_angle(0)

    def delete_object(self, space, searchd):
        space.remove(searchd, self.bodyO[self.shapeO.index(searchd)])
        self.objects.remove((searchd, self.bodyO[self.shapeO.index(searchd)]))
        self.objects_for_save = self.objects

    def rotate_object(self, searchd, arg):
        self.bodyO[self.shapeO.index(searchd)]._get_angle()
        self.bodyO[self.shapeO.index(searchd)]._set_angle(
            float(str(self.bodyO[self.shapeO.index(searchd)]._get_angle())[0:10]) + (0.01 * arg))

    def rotate_object_45(self, searchd):
        self.bodyO[self.shapeO.index(searchd)]._set_angle(
            float(str(self.bodyO[self.shapeO.index(searchd)]._get_angle())[0:10]) + 0.785)

    def connect_shapes(self, space, type_j):
        """for i in self.cshapes:
            if i != f:
                # joint = pymunk.PinJoint(self.bodyO[self.shapeO.index(f)], self.bodyO[self.shapeO.index(i)]) # нить
                joint = pymunk.DampedSpring(self.bodyO[self.shapeO.index(f)], self.bodyO[self.shapeO.index(i)],
                                            (0, 0),
                                            (0, 0), 10, 50, 1)  # пружина
                f = self.shapeO[self.shapeO.index(i)]
                space.add(joint)
                self.objects.append(joint)"""
        if self.cshapes[0] and self.cshapes[1]:
            if type_j == "нить":
                joint = pymunk.PinJoint(self.bodyO[self.shapeO.index(self.cshapes[0])],
                                        self.bodyO[self.shapeO.index(self.cshapes[1])])
            else:
                joint = pymunk.DampedSpring(self.bodyO[self.shapeO.index(self.cshapes[0])],
                                            self.bodyO[self.shapeO.index(self.cshapes[1])], (0, 0), (0, 0), 10, 50,
                                            1)  # пружина

            space.add(joint)
            self.objects.append(joint)
            self.sshapes.append(
                [joint, (self.cshapes[0], self.bodyO[self.shapeO.index(self.cshapes[0])]),
                 (self.cshapes[1], self.bodyO[self.shapeO.index(self.cshapes[1])]), type_j])
            self.flag = True

    def save_field(self,name_file):
        k = 0
        npsl = []
        list_of_objects_without_anco = []
        for j in self.sshapes:
            npsl.append(j[1])
            npsl.append(j[2])
        for i in self.objects_for_save:
            if i not in npsl:
                list_of_objects_without_anco.append(i)
        for i in list_of_objects_without_anco:
            f = str(i[0])[15:str(i[0]).index(' ')]
            if f == "Circle":
                t = "круг"
                size = i[0].radius
                h = 0
            elif f == "Poly":
                t = "квадрат"
                size = abs(i[0].get_vertices()[0][0])
                h = abs(i[0].get_vertices()[0][1])
            self.d[k] = {
                "mass": i[0].mass,
                "friction": i[0].friction,
                "elasticity": i[0].elasticity,
                "color": i[0].color,
                'position': i[1].position,
                'shape': t,
                'body_type': i[1].body_type,
                'args': [size, h],
                'angle': i[1]._get_angle()
            }
            k += 1
        ADDED_OBJECTS = []
        indexo = 0
        for j in self.sshapes:
            d2 = {}
            k2 = 0
            vl = [j[1], j[2]]
            if indexo != len(self.sshapes) - 1:
                print(self.sshapes[indexo + 1])
                vl2 = [self.sshapes[indexo + 1][1],self.sshapes[indexo + 1][2], self.sshapes[indexo + 1][3]]
            if vl2[0] in vl and indexo != len(self.sshapes) - 1:
                vl.append(vl2[1])
                self.sshapes.remove(self.sshapes[indexo + 1])
            if vl2[1] in vl and indexo != len(self.sshapes) - 1:
                self.sshapes.remove(self.sshapes[indexo + 1])
                vl.append(vl2[0])
            for i in vl:
                if i in ADDED_OBJECTS:
                    print(True)
                f = str(i[0])[15:str(i[0]).index(' ')]
                if f == "Circle":
                    t = "круг"
                    size = i[0].radius
                    h = 0
                elif f == "Poly":
                    t = "квадрат"
                    size = abs(i[0].get_vertices()[0][0])
                    h = abs(i[0].get_vertices()[0][1])
                d2[k2] = {
                    "mass": i[0].mass,
                    "friction": i[0].friction,
                    "elasticity": i[0].elasticity,
                    "color": i[0].color,
                    'position': i[1].position,
                    'shape': t,
                    'body_type': i[1].body_type,
                    'args': [size, h],
                    'angle': i[1]._get_angle()
                }
                k2 += 1
                ADDED_OBJECTS.append(i)
            self.d[k] = {
                f"{j[3]}": d2
            }
            indexo += 1
            k += 1
        data = json.dumps(self.d)
        data = json.loads(str(data))
        with open(f'fields/{name_file}.json', "w") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def load_field(self, space, name):
        if os.path.isfile(f"fields/{name}.json"):
            with open(f"fields/{name}.json", 'r') as field:
                field = json.load(field)
                for i in field:
                    data = field[i]
                    if 'пружина' in data:
                        data2 = data['пружина']
                        SBODY = []
                        SSHAPE = []
                        for j in range(0, 2):
                            data = data2[str(j)]
                            body = pm.Body()
                            body.position = data['position']
                            if data['shape'] == "круг":
                                shape = pm.Circle(body, data['args'][0])
                                shape.elasticity = 0.5
                            elif data['shape'] == 'квадрат':
                                shape = pm.Poly.create_box(body, (data['args'][0] * 2, data['args'][1] * 2))
                                shape.elasticity = 0
                            SSHAPE.append(shape)
                            body.body_type = data['body_type']
                            shape.color = data['color']
                            shape.friction = data['friction']
                            shape.mass = data['mass']
                            body._set_angle(data['angle'])
                            space.add(body, shape)
                            self.bodyO.append(body)
                            self.shapeO.append(shape)
                            self.objects.append((shape, body))
                            SBODY.append(body)
                        joint = pymunk.DampedSpring(SBODY[0], SBODY[1], (0, 0), (0, 0), 10, 50, 1)
                        self.sshapes.append(
                            [joint, (SSHAPE[0], self.bodyO[self.shapeO.index(SSHAPE[0])]),
                             (SSHAPE[1], self.bodyO[self.shapeO.index(SSHAPE[1])]), "пружина"])
                        space.add(joint)
                        self.objects.append(joint)
                    else:
                        body = pm.Body()
                        body.position = data['position']
                        if data['shape'] == "круг":
                            shape = pm.Circle(body, data['args'][0])
                            shape.elasticity = 0.5
                        elif data['shape'] == 'квадрат':
                            shape = pm.Poly.create_box(body, (data['args'][0] * 2, data['args'][1] * 2))
                            shape.elasticity = 0
                        body.body_type = data['body_type']
                        shape.color = data['color']
                        shape.friction = data['friction']
                        shape.mass = data['mass']
                        body._set_angle(data['angle'])
                        space.add(body, shape)
                        self.bodyO.append(body)
                        self.shapeO.append(shape)
                        self.objects.append((shape, body))
                        self.objects_for_save.append((shape, body))

    def delete_all_objects(self, space):
        for i in self.objects:
            try:
                space.remove(i[0], i[1])
            except:
                space.remove(i)
        self.objects = []
        self.objects_for_save = []
        self.cshapes = [None, None]
        self.flag = True

    def stop_all_objects(self):
        for i in self.objects:
            if i != 'нить' and i != "пружина":
                i[1].body_type = pm.Body.STATIC

    def resume_all_objects(self):
        for i in self.objects:
            if i != 'нить' and i != "пружина":
                i[1].body_type = pm.Body.DYNAMIC

    def create_ball(self, position, space, mass, radius):
        body = pm.Body()
        body.position = position
        shape = pm.Circle(body, radius)
        shape.elasticity = 0.4
        shape.mass = mass
        shape.friction = 0.4
        shape.color = (100, 200, 100, 100)
        space.add(body, shape)
        self.bodyO.append(body)
        self.shapeO.append(shape)
        self.objects.append((shape, body))
        self.objects_for_save.append((shape, body))

    def create_square(self, position, space, mass, size):
        body = pm.Body()
        body.position = position
        shape = pm.Poly.create_box(body, (size, size))
        shape.elasticity = 0.1
        shape.mass = mass
        shape.friction = 0.4
        shape.color = (180, 100, 100, 100)
        space.add(body, shape)
        self.bodyO.append(body)
        self.shapeO.append(shape)
        self.objects.append((shape, body))
        self.objects_for_save.append((shape, body))

    def add_obj(self, position, typeOb, space, mass, args):
        if typeOb == "круг":
            self.create_ball(position, space, mass, args)
        elif typeOb == "квадрат":
            self.create_square(position, space, mass, args)

    def get_info(self, space, position):
        search = space.point_query_nearest(position, 0, pm.ShapeFilter())
        if search is not None:
            if search.shape.collision_type == 0:
                return search.shape, self.bodyO[self.shapeO.index(search.shape)]

    def edit_object(self, space, position):
        with open("object.json", 'r') as field:
            search = space.point_query_nearest(position, 0, pm.ShapeFilter())
            if search is not None:
                if search.shape.collision_type == 0:
                    body = self.bodyO[self.shapeO.index(search.shape)]
            self.delete_object(space, search.shape)
            field = json.load(field)
            data = field['0']
            body.position = data['position']
            if data['shape'] == "круг":
                shape = pm.Circle(body, data['args'])
            elif data['shape'] == "квадрат":
                shape = pm.Poly.create_box(body, (data['args'][0] * 2, data['args'][1] * 2))
            shape.elasticity = data['elasticity']
            body.body_type = data['body_type']
            shape.color = data['color']
            shape.friction = data['friction']
            shape.mass = data['mass']
            body._set_angle(data['angle'])
            space.add(body, shape)
            self.bodyO.append(body)
            self.shapeO.append(shape)
            self.objects.append((shape, body))
            self.objects_for_save.append((shape, body))
