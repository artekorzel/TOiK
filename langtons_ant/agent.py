# coding=utf-8
from pyage.core.address import Addressable
from pyage.core.inject import Inject
from langtons_ant.vector import random_vector, Vector


class NetAgent(Addressable):
    @Inject("locator", "net_dimensions", "layers")
    @Inject("sub_agents:_NetAgent__agents")
    def __init__(self, name=None):
        super(NetAgent, self).__init__()
        for agent in self.__agents.values():
            agent.parent = self
            agent.position = random_vector(self.net_dimensions)
        self.name = name

    def step(self):
        for agent in self.__agents.values():
            agent.step()

    def remove_agent(self, agent):
        agent = self.__agents[agent.get_address()]
        del self.__agents[agent.get_address()]
        agent.parent = None
        agent.position = None
        return agent

    def add_agent(self, agent):
        agent.parent = self
        agent.position = random_vector(self.net_dimensions)
        self.__agents[agent.get_address()] = agent

    def get_agents(self):
        return self.__agents.values()


class SubAgent(Addressable):
    directions = [Vector(-1, 0), Vector(0, -1), Vector(+1, 0), Vector(0, +1)]

    @Inject("locator")
    def __init__(self, name=None):
        super(SubAgent, self).__init__()
        self.name = name
        self.parent = None
        self.position = None
        self.direction_index = 0

    def step(self):
        for layer in self.parent.layers:
            layer.affect(self)
        direction = SubAgent.directions[self.direction_index]
        self.position.move(direction, self.parent.net_dimensions)

    def turn_right(self):
        self.direction_index = (self.direction_index + 1) % len(SubAgent.directions)

    def turn_left(self):
        self.direction_index = (self.direction_index - 1) % len(SubAgent.directions)