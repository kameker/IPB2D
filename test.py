import pymunk
b = pymunk.Body()
b.position = 1,2
b.angle = 0.5
shape = pymunk.Poly(b, [(0,0), (10,0), (10,10)])
for v in shape.get_vertices():
    x,y = v.rotated(shape.body.angle) + shape.body.position
    (int(x), int(y))