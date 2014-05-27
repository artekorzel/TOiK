

class Direction:
    N = 1
    S = 2
    E = 3
    W = 4


class Overlaps:
    def __init__(self, x_size, y_size):
        self.overlap_n = [[[] for _ in range(x_size)] for _ in range(2)]
        self.overlap_s = [[[] for _ in range(x_size)] for _ in range(2)]
        self.overlap_e = [[[] for _ in range(y_size)] for _ in range(2)]
        self.overlap_w = [[[] for _ in range(y_size)] for _ in range(2)]
        self.x_size = x_size
        self.y_size = y_size

    def __check_for_agent(self, overlap, x, y):
        if x < 2 and y < len(overlap):
            return not overlap[y][x]
        return False

    def __add_agents_to_overlap(self, overlap, agents, row):
        for agent in agents:
            if agent < len(overlap):
                overlap[row][agent].append(agent)

    def clear(self):
        self.overlap_n = [[[] for _ in range(self.x_size)] for _ in range(2)]
        self.overlap_s = [[[] for _ in range(self.x_size)] for _ in range(2)]
        self.overlap_e = [[[] for _ in range(self.y_size)] for _ in range(2)]
        self.overlap_w = [[[] for _ in range(self.y_size)] for _ in range(2)]

    def contains_agent(self, direction, x, y):
        if direction == Direction.N:
            return self.__check_for_agent(self.overlap_n, x, y)
        if direction == Direction.S:
            return self.__check_for_agent(self.overlap_s, x, y)
        if direction == Direction.E:
            return self.__check_for_agent(self.overlap_e, x, y)
        if direction == Direction.W:
            return self.__check_for_agent(self.overlap_w, x, y)

    def add_agents(self, overlap_direction, agents):
        if overlap_direction == Direction.N:
            self.__add_agents_to_overlap(self.overlap_n, agents[0], 0)
            self.__add_agents_to_overlap(self.overlap_n, agents[1], 1)
        if overlap_direction == Direction.S:
            self.__add_agents_to_overlap(self.overlap_s, agents[0], 0)
            self.__add_agents_to_overlap(self.overlap_s, agents[1], 1)
        if overlap_direction == Direction.E:
            self.__add_agents_to_overlap(self.overlap_w, agents[0], 0)
            self.__add_agents_to_overlap(self.overlap_w, agents[1], 1)
        if overlap_direction == Direction.W:
            self.__add_agents_to_overlap(self.overlap_e, agents[0], 0)
            self.__add_agents_to_overlap(self.overlap_e, agents[1], 1)

    def print_overlaps(self):
        print "N:" + str(self.overlap_n[0]) + "\t" + str(self.overlap_n[1])
        print "S:" + str(self.overlap_s[0]) + "\t" + str(self.overlap_s[1])
        print "E:" + str(self.overlap_e[0]) + "\t" + str(self.overlap_e[1])
        print "W:" + str(self.overlap_w[0]) + "\t" + str(self.overlap_w[1])