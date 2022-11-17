import math

import pygame
import pymunk.pygame_util

pygame.init()
pymunk.pygame_util.positive_y_is_up = False

size = WIDTH, HEIGHT = 1000, 900

window = pygame.display.set_mode(size)
clock = pygame.time.Clock()
shape_founded = None
draw_options = pymunk.pygame_util.DrawOptions(window)
objects = []


def create_ball(space, radius, mass, pos):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.elasticity = 0.9
    shape.color = (0, 255, 0, 100)
    space.add(body, shape)
    return shape


def add_obj(position, type, space, mass, args):
    global shape
    body = pymunk.Body()
    body.position = position
    if type == 0:
        shape = pymunk.Circle(body, args)
        shape.elasticity = 0.9
    elif type == 4:
        shape = pymunk.Poly.create_box(body, (args * 2, args))
        shape.elasticity = 0
    shape.mass = 1000
    shape.friction = 0.5
    shape.color = (0, 255, 0, 100)
    space.add(body, shape)
    objects.append((shape, body))


def cal_dis(p1, p2):
    return math.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)


def cal_angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])


def ground(space, width, height):
    rects = [
        [(width / 2, height - 10), (width, 20)],
        [(width / 2, 10), (width, 20)],
        [(10, height / 2), (20, height)],
        [(width - 10, height / 2), (20, height)]
    ]
    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos

        shape = pymunk.Poly.create_box(body, size)
        shape.friction = 1
        shape.elasticity = 0.3
        space.add(body, shape)


def draw_line(space):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (1, 850)
    body._set_angle(-0.5)

    shape = pymunk.Segment(body, (-50, 0), (500, 0), radius=10)
    shape.friction = 0.9
    space.add(body, shape)


def draw(space, window, draw_options):
    window.fill("black")
    space.debug_draw(draw_options)
    pygame.display.update()


def delete_all_objects(space):
    global objects
    for i in objects:
        space.remove(i[0], i[1])
    objects = []


def stop_all_objects():
    for i in objects:
        i[1].body_type = pymunk.Body.STATIC


def resume_all_objects():
    for i in objects:
        i[1].body_type = pymunk.Body.DYNAMIC


def pick_object(space, position):
    global shape_founded
    search = space.point_query_nearest(position, 0, pymunk.ShapeFilter())
    if search is not None:
        if search.shape.collision_type == 0:
            shape_founded = search.shape
    print(shape_founded)


def resume_object():
    global shape_founded
    shape_founded = None


def move_founded_object(pos):
    if shape_founded is not None:
        if pos[1] < 900:
            shape_founded.body.position = pos
            shape_founded.body.velocity = 0, 0




def run(window, w, h):
    run = True
    fps = 60
    g = 981
    PAUSE = False
    flag = False
    clock = pygame.time.Clock()
    space = pymunk.Space()
    space.gravity = 0, g
    ground(space, WIDTH, HEIGHT)
    draw_line(space)
    while run:
        mouse_position = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    add_obj(mouse_position, 0, space, 10, 30)
                elif event.button == 1:
                    pick_object(space, mouse_position)
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    resume_object()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if PAUSE:
                        resume_all_objects()
                        PAUSE = False
                    else:
                        stop_all_objects()
                        PAUSE = True
                elif event.key == pygame.K_DELETE:
                    delete_all_objects(space)
        move_founded_object(mouse_position)
        draw(space, window, draw_options)
        space.step(1 / fps)
        clock.tick(fps)
    pygame.quit()


if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)
