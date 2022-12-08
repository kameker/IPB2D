import pymunk as pm
import json
import os.path

from saveUI_ import sf


class ObjectsCreator:
    def __init__(self):
        self.height = 1000
        self.width = 1000
        self.objects = []
        self.bodyO = []
        self.shapeO = []
        self.id = 0
        self.d = {}
        self.window2 = 0

    def searchf(self, space, position):
        search = space.point_query_nearest(position, 0, pm.ShapeFilter())
        if search is not None:
            if search.shape.collision_type == 0:
                return search.shape

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
            shape.friction = 1
            shape.elasticity = 1
            space.add(body, shape)

    def delete_object(self, space, searchd):
        space.remove(searchd, self.bodyO[self.shapeO.index(searchd)])
        self.objects.remove((searchd, self.bodyO[self.shapeO.index(searchd)]))

    def rotate_object(self, searchd, arg):
        self.bodyO[self.shapeO.index(searchd)]._set_angle(
            float(str(self.bodyO[self.shapeO.index(searchd)]._get_angle())[0:6]) + (0.1 * arg))

    def rotate_object_45(self, searchd):
        self.bodyO[self.shapeO.index(searchd)]._set_angle(
            float(str(self.bodyO[self.shapeO.index(searchd)]._get_angle())[0:6]) + 0.785)

    def save_field(self):
        sf()
        with open("name.txt", "r") as namef:
            name_file = namef.read()
        k = 0
        for i in self.objects:
            f = str(i[0])[15:str(i[0]).index(' ')]
            if f == "Circle":
                t = 0
                size = i[0].radius
                h = 0
            elif f == "Poly":
                t = 4
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
        data = json.dumps(self.d)
        data = json.loads(str(data))
        with open(f'fields/{name_file}.json', "w") as file:
            json.dump(data, file, indent=4)

    def delete_all_objects(self, space):
        for i in self.objects:
            space.remove(i[0], i[1])
        self.objects = []

    def stop_all_objects(self):
        for i in self.objects:
            i[1].body_type = pm.Body.STATIC

    def resume_all_objects(self):
        for i in self.objects:
            i[1].body_type = pm.Body.DYNAMIC

    def add_obj(self, position, typeOb, space, mass, args):
        shape = None
        body = pm.Body()
        body.position = position
        if typeOb == 0:
            shape = pm.Circle(body, args)
            shape.elasticity = 0.1
        elif typeOb == 4:
            shape = pm.Poly.create_box(body, (args, args))
            shape.elasticity = 0
        shape.mass = mass
        shape.friction = 0
        shape.color = (0, 255, 0, 100)
        space.add(body, shape)
        self.bodyO.append(body)
        self.shapeO.append(shape)
        self.objects.append((shape, body))

    def load_field(self, space):
        if os.path.isfile("fields/13.json"):
            with open("fields/13.json", 'r') as field:
                field = json.load(field)
                for i in field:
                    data = field[i]
                    body = pm.Body()
                    body.position = data['position']
                    if data['shape'] == 0:
                        shape = pm.Circle(body, data['args'][0])
                        shape.elasticity = 0.5
                    elif data['shape'] == 4:

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
            if data['shape'] == 0:
                shape = pm.Circle(body, data['args'])
            elif data['shape'] == 4:
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
