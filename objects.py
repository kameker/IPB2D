import pymunk


def create_square(space, pos):
    square_mass, square_size = 1, (60, 60)
    square_moment = pymunk.moment_for_box(square_mass, square_size)
    square_body = pymunk.Body(square_mass, square_moment)
    square_body.position = pos
    square_shape = pymunk.Poly.create_box(square_body, square_size)
    square_shape.elasticity = 0.4
    square_shape.friction = 1.0
    square_shape.color = [100, 100, 100, 100]
    space.add(square_body, square_shape)