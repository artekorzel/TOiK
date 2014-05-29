from pyage.core.inject import Inject
from langtons_ant.layer import ColorLayer
from langtons_ant.vector import Vector


class Direction:
    N = 1
    S = 2
    E = 3
    W = 4


class Overlaps:
    @Inject("overlap_size")
    def __init__(self, x_size, y_size):
        self.x_size = x_size
        self.y_size = y_size
        self.clear()

    def __is_inside_overlap(self, overlap, x, y):
        return -1 < x < self.overlap_size and -1 < y < len(overlap)

    def __check_for_agent(self, overlap, x, y):
        if self.__is_inside_overlap(overlap, x, y):
            return not not overlap[x][y]
        return False

    def __add_agents_to_overlap(self, overlap, layers, agents, row, overlap_direction):
        for agent in agents:
            agent.layers = layers
            agent.overlap = overlap
            overlap[agent.position.x][agent.position.y].append(agent)
            self.agents.append(agent)

    def __get_printable_overlap(self, overlap):
        val = ""
        for i in range(self.overlap_size):
            val += "\t" + str(overlap[i]) + "\n"
        return val

    def __get_overlap(self, overlap_direction):
        if overlap_direction == Direction.N:
            return self.overlap_n
        if overlap_direction == Direction.S:
            return self.overlap_s
        if overlap_direction == Direction.W:
            return self.overlap_w
        return self.overlap_e

    def __get_layers(self, overlap_direction):
        if overlap_direction == Direction.N:
            return [self.layer_n]
        if overlap_direction == Direction.S:
            return [self.layer_s]
        if overlap_direction == Direction.W:
            return [self.layer_w]
        return [self.layer_e]

    def __remove_agent(self, overlap, agent):
        overlap[agent.position.x][agent.position.y].remove(agent)
        self.agents.remove(agent)

    def __move_(self, agent, x, y):
        agent.overlap[x][y].append(agent)

    def __move_agent(self, agent):
        agent.step()
        vector = OverlapAgent.directions[agent.direction_index]
        x = agent.position.x + vector.x
        y = agent.position.y + vector.y

        if self.__check_for_agent(agent.overlap, x, y):
            agent.turn_around()
        else:
            self.__remove_agent(agent.overlap, agent)
            if self.__is_inside_overlap(agent.overlap, x, y):
                agent.position.x = x
                agent.position.y = y
                self.__move_(agent, x, y)

    def simulate(self):
        for agent in self.agents:
            self.__move_agent(agent)


    def clear(self):
        self.overlap_n = [[[] for _ in range(self.x_size)] for _ in range(self.overlap_size)]
        self.overlap_s = [[[] for _ in range(self.x_size)] for _ in range(self.overlap_size)]
        self.overlap_e = [[[] for _ in range(self.y_size)] for _ in range(self.overlap_size)]
        self.overlap_w = [[[] for _ in range(self.y_size)] for _ in range(self.overlap_size)]
        self.layer_n = ColorLayer(self.overlap_size, self.x_size)
        self.layer_s = ColorLayer(self.overlap_size, self.x_size)
        self.layer_e = ColorLayer(self.overlap_size, self.y_size)
        self.layer_w = ColorLayer(self.overlap_size, self.y_size)
        self.agents = []

    def contains_agent(self, overlap_direction, x, y):
        overlap = self.__get_overlap(overlap_direction)
        return self.__check_for_agent(overlap, x, y)

    def add_agents(self, overlap_direction, agents):
        overlap = self.__get_overlap(overlap_direction)
        layers = self.__get_layers(overlap_direction)
        for i in range(self.overlap_size):
            self.__add_agents_to_overlap(overlap, layers, agents[i], i, overlap_direction)

    def print_overlaps(self):
        print "N:\n" + self.__get_printable_overlap(self.overlap_n)
        print "S:" + self.__get_printable_overlap(self.overlap_s)
        print "E:" + self.__get_printable_overlap(self.overlap_e)
        print "W:" + self.__get_printable_overlap(self.overlap_w)
        print


class OverlapAgent:
    directions = [Vector(-1, 0), Vector(0, -1), Vector(+1, 0), Vector(0, +1)]

    def __init__(self, position, direction_index):
        self.position = position
        self.direction_index = direction_index
        self.layers = None
        self.overlap = None

    def __repr__(self):
        return "(" + str(self.position.x) + "," + str(self.position.y) + ")"

    def step(self):
        for layer in self.layers:
            layer.affect(self)

    def turn_right(self):
        self.direction_index = (self.direction_index + 1) % len(OverlapAgent.directions)

    def turn_left(self):
        self.direction_index = (self.direction_index - 1) % len(OverlapAgent.directions)

    def turn_around(self):
        self.direction_index = (self.direction_index + 2) % len(OverlapAgent.directions)