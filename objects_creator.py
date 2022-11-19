import pymunk as pm


class ObjectsCreator:
    def __init__(self):
        self.height = 900
        self.width = 1000
        self.objects = []
        self.bodyO = []
        self.shapeO = []

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
            shape.elasticity = 0.5
            space.add(body, shape)

    def deg_to_rad(self, degree):
        return degree / 180 * 3.14

    def delete_object(self, space, position):
        search = space.point_query_nearest(position, 0, pm.ShapeFilter())
        if search is not None:
            if search.shape.collision_type == 0:
                space.remove(search.shape, self.bodyO[self.shapeO.index(search.shape)])
        self.objects.remove((search.shape, self.bodyO[self.shapeO.index(search.shape)]))

    def rotate_object(self, space, position, arg):
        search = space.point_query_nearest(position, 0, pm.ShapeFilter())
        if search is not None:
            if search.shape.collision_type == 0:
                self.bodyO[self.shapeO.index(search.shape)]._set_angle(
                    float(str(self.bodyO[self.shapeO.index(search.shape)]._get_angle())[0:6]) + (0.1 * arg))

    def rotate_object_45(self, space, position, arg):
        search = space.point_query_nearest(position, 0, pm.ShapeFilter())
        if search is not None:
            if search.shape.collision_type == 0:
                self.bodyO[self.shapeO.index(search.shape)]._set_angle(
                    float(str(self.bodyO[self.shapeO.index(search.shape)]._get_angle())[0:6]) + 0.785)

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
            shape.elasticity = 0.5
        elif typeOb == 4:
            shape = pm.Poly.create_box(body, (args * 2, args))
            shape.elasticity = 0
        shape.mass = mass
        shape.friction = 0.5
        shape.color = (0, 255, 0, 100)
        space.add(body, shape)
        self.bodyO.append(body)
        self.shapeO.append(shape)
        self.objects.append((shape, body))
