from pyage.core.inject import Inject
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

    def __check_for_agent(self, overlap, x, y):
        if x < self.overlap_size and y < len(overlap):
            return not not overlap[x][y]
        return False

    def __get_agent_position_param(self, agent, overlap_direction):
        if overlap_direction == Direction.N or overlap_direction == Direction.S:
            return agent.position.x
        return agent.position.y

    def __add_agents_to_overlap(self, overlap, agents, row, overlap_direction):
        for agent in agents:
            agent_position_param = self.__get_agent_position_param(agent, overlap_direction)
            overlap[row][agent_position_param].append(agent)

    def __get_printable_overlap(self, overlap):
        val = ""
        for i in range(self.overlap_size):
            val += str(overlap[i]) + "\t"
        return val

    def __get_overlap(self, overlap_direction):
        if overlap_direction == Direction.N:
            return self.overlap_n
        if overlap_direction == Direction.S:
            return self.overlap_s
        if overlap_direction == Direction.W:
            return self.overlap_w
        return self.overlap_e

    def clear(self):
        self.overlap_n = [[[] for _ in range(self.x_size)] for _ in range(self.overlap_size)]
        self.overlap_s = [[[] for _ in range(self.x_size)] for _ in range(self.overlap_size)]
        self.overlap_e = [[[] for _ in range(self.y_size)] for _ in range(self.overlap_size)]
        self.overlap_w = [[[] for _ in range(self.y_size)] for _ in range(self.overlap_size)]

    def contains_agent(self, overlap_direction, x, y):
        overlap = self.__get_overlap(overlap_direction)
        return self.__check_for_agent(overlap, x, y)

    def add_agents(self, overlap_direction, agents):
        overlap = self.__get_overlap(overlap_direction)
        for i in range(self.overlap_size):
            self.__add_agents_to_overlap(overlap, agents[i], i, overlap_direction)

    def print_overlaps(self):
        print "N:" + self.__get_printable_overlap(self.overlap_n)
        print "S:" + self.__get_printable_overlap(self.overlap_s)
        print "E:" + self.__get_printable_overlap(self.overlap_e)
        print "W:" + self.__get_printable_overlap(self.overlap_w)
        print


class OverlapAgent:
    directions = [Vector(-1, 0), Vector(0, -1), Vector(+1, 0), Vector(0, +1)]

    def __init__(self, position, direction_index):
        self.position = position
        self.direction_index = direction_index

    def __repr__(self):
        return "(" + str(self.position.x) + "," + str(self.position.y) + ")"

    def turn_right(self):
        self.direction_index = (self.direction_index + 1) % len(OverlapAgent.directions)

    def turn_left(self):
        self.direction_index = (self.direction_index - 1) % len(OverlapAgent.directions)

    def turn_around(self):
        self.direction_index = (self.direction_index + 2) % len(OverlapAgent.directions)