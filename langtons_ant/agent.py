# coding=utf-8
from pyage.core.address import Addressable
from pyage.core.inject import Inject
from langtons_ant.vector import random_vector, Vector

class NetAgent(Addressable):
    @Inject("locator", "net_dimensions", "layers")
    @Inject("sub_agents:_NetAgent__agents")
    @Inject("migration")
    def __init__(self, position_in_net, name=None):
        super(NetAgent, self).__init__()
        self.position_in_net = position_in_net
        self.name = name
        self.agents_matrix = [[[] for i in range(self.net_dimensions.x)] for j in range(self.net_dimensions.y)]
        for agent in self.__agents.values():
            self.__add_agent(agent)

    def __add_agent(self, agent):
        agent.parent = self
        position = random_vector(self.net_dimensions)
        self.agents_matrix[position.y][position.x].append(agent)
        agent.position = position

    def __add_existing_agent(self, agent, posx, posy):
        agent.parent = self
        position = Vector(posx, posy)
        self.agents_matrix[position.y][position.x].append(agent)
        agent.position = position

    def add_agent(self, agent):
        self.__add_agent(agent)
        self.__agents[agent.get_address()] = agent

    def add_existing_agent(self, agent, posx, posy):
        self.__add_existing_agent(agent, posx, posy)
        self.__agents[agent.get_address()] = agent

    def __remove_agent_from_matrix(self, agent):
        for matrix_line in self.agents_matrix:
            for matrix in matrix_line:
                if agent in matrix:
                    matrix.remove(agent)

    def remove_agent(self, agent):
        agent = self.__agents[agent.get_address()]
        self.__remove_agent_from_matrix(agent)
        return self.__agents.pop(agent.get_address())

    def get_agents(self):
        return self.__agents.values()

    def step(self):
        for agent in self.__agents.values():
            agent.step()

    def __move_agent(self, agent, vector):
        self.__remove_agent_from_matrix(agent)
        new_position_x = agent.position.x + vector.x
        new_position_y = agent.position.y + vector.y

        if self.net_dimensions.y > new_position_y >= 0:
            agent.position.y = new_position_y

        if new_position_x < 0:
            self.migration.migrate_to_previous(agent, agent.position.y)
            #pass

        elif new_position_x >= self.net_dimensions.x:
            self.migration.migrate_to_next(agent, agent.position.y)
            #pass

        else:
            agent.position.x = new_position_x
            self.agents_matrix[agent.position.y][agent.position.x].append(agent)

    def move_agent(self, agent):
        self.__move_agent(agent, SubAgent.directions[agent.direction_index])
        neighbours = self.get_neighbours(agent)
        if len(neighbours) > 0:
            agent.turn_around()
            self.__move_agent(agent, SubAgent.directions[agent.direction_index])

    def get_neighbours(self, agent):
        position = agent.position
        min_horizontal = (position.x - 1) % self.net_dimensions.x
        max_horizontal = (position.x + 1) % self.net_dimensions.x
        min_vertical = (position.y - 1) % self.net_dimensions.y
        max_vertical = (position.y + 1) % self.net_dimensions.y
        return self.agents_matrix[min_vertical][position.x] + self.agents_matrix[max_vertical][position.x] + \
            self.agents_matrix[position.y][min_horizontal] + self.agents_matrix[position.y][max_horizontal]

    def get_position_in_net(self):
        return self.position_in_net


class SubAgent(Addressable):
    directions = [Vector(-1, 0), Vector(0, -1), Vector(+1, 0), Vector(0, +1)]

    @Inject("locator", "migration")
    def __init__(self, name=None):
        super(SubAgent, self).__init__()
        self.name = name
        self.parent = None
        self.position = None
        self.direction_index = 0

    def __repr__(self):
        return self.get_address()

    def step(self):
        for layer in self.parent.layers:
            layer.affect(self)
        self.parent.move_agent(self)

    def turn_right(self):
        self.direction_index = (self.direction_index + 1) % len(SubAgent.directions)

    def turn_left(self):
        self.direction_index = (self.direction_index - 1) % len(SubAgent.directions)

    def turn_around(self):
        self.direction_index = (self.direction_index + 2) % len(SubAgent.directions)