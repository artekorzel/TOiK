# coding=utf-8
import random


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Vector(%d, %d)" % (self.x, self.y)

    def move(self, coordinates_change, max_coordinates):
        self.x = (self.x + coordinates_change.x) % max_coordinates.x
        self.y = (self.y + coordinates_change.y) % max_coordinates.y


def random_vector(max_dimensions):
    #return Vector(max_dimensions.x / 2, max_dimensions.y / 2)
    return Vector(random.randrange(0, max_dimensions.x), random.randrange(0, max_dimensions.y))