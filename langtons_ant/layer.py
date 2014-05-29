# coding=utf-8
from pyage.core.inject import Inject


class Layer(object):
    @Inject("net_dimensions")
    def __init__(self, cell_type, dim_x=-1, dim_y=-1):
        if dim_x == -1:
            self.dim_x = self.net_dimensions.x
        else:
            self.dim_x = dim_x
        if dim_y == -1:
            self.dim_y = self.net_dimensions.y
        else:
            self.dim_y = dim_y

        self.matrix = [[cell_type() for i in range(self.dim_x)] for j in range(self.dim_y)]

    def get_current_cell(self, agent):
        return self.matrix[agent.position.y][agent.position.x]

    def affect(self, agent):
        raise NotImplementedError()


class Color:
    white, black = range(2)


class ColorLayer(Layer):
    def __init__(self, dim_x=-1, dim_y=-1):
        super(ColorLayer, self).__init__(ColoredCell, dim_x, dim_y)

    def affect(self, agent):
        current_cell = self.get_current_cell(agent)
        if current_cell.color == Color.white:
            agent.turn_left()
            current_cell.color = Color.black
        else:
            agent.turn_right()
            current_cell.color = Color.white


class Cell(object):
    pass


class ColoredCell(Cell):
    def __init__(self):
        self.color = Color.white