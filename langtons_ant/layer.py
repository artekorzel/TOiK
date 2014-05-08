# coding=utf-8
from pyage.core.inject import Inject


class Layer(object):
    @Inject("net_dimensions")
    def __init__(self, cell_type):
        self.matrix = [[cell_type() for i in range(self.net_dimensions.x)] for j in range(self.net_dimensions.y)]

    def get_current_cell(self, agent):
        return self.matrix[agent.position.y][agent.position.x]

    def affect(self, agent):
        raise NotImplementedError()


class Color:
    white, black = range(2)


class ColorLayer(Layer):
    def __init__(self):
        super(ColorLayer, self).__init__(ColoredCell)

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