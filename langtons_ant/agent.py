# coding=utf-8
import time

from pyage.core.address import Addressable
from pyage.core.inject import Inject
from pyage.core.agent.agent import AGENT
import Pyro4

from langtons_ant.overlap import Overlaps, Direction, OverlapAgent
from langtons_ant.vector import random_vector, Vector


class NetAgent(Addressable):
    @Inject("locator", "net_dimensions", "layers")
    @Inject("sub_agents:_NetAgent__agents")
    @Inject("migration")
    @Inject("iterations_per_update")
    @Inject("simulate_in_overlaps")
    @Inject("overlap_size")
    @Inject("ns_hostname")
    @Inject("global_number_of_net_agents")
    @Inject("waiting_interval")
    @Inject("number_of_iterations")
    def __init__(self, position_in_net_x, position_in_net_y, name=None):
        super(NetAgent, self).__init__()
        self.position_in_net_x = position_in_net_x
        self.position_in_net_y = position_in_net_y
        self.name = name
        self.agents_matrix = [[[] for _ in range(self.net_dimensions.x)] for _ in range(self.net_dimensions.y)]
        self.overlaps = Overlaps(self.net_dimensions.x, self.net_dimensions.y)
        for agent in self.__agents.values():
            self.__add_agent(agent)
        self.iter = 0
        self.start_step_agents = 0
        self.end_step_agents = 0
        self.big_iter = 0

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

    def increase_start_step_agents(self):
        self.start_step_agents += 1
        return self.start_step_agents

    def increase_end_step_agents(self):
        self.end_step_agents += 1
        return self.end_step_agents

    def __check_all_agents_present(self):
        ns = Pyro4.locateNS(self.ns_hostname)
        return len(ns.list(AGENT)) == self.global_number_of_net_agents

    def __get_all_agents(self):
        ns = Pyro4.locateNS(self.ns_hostname)
        return ns.list(AGENT)

    def __synchronize_start(self):
        while not self.__check_all_agents_present():
            time.sleep(self.waiting_interval)

        self.end_step_agents = 0

        agents = self.__get_all_agents()
        for agent in agents:
            proxy = Pyro4.Proxy(agents[agent])
            proxy.increase_start_step_agents()

        while self.start_step_agents != self.global_number_of_net_agents:
            time.sleep(1)

    def __synchronize_end(self):
        while not self.__check_all_agents_present():
            time.sleep(self.waiting_interval)

        self.start_step_agents = 0

        agents = self.__get_all_agents()
        for agent in agents:
            proxy = Pyro4.Proxy(agents[agent])
            proxy.increase_end_step_agents()

        while self.end_step_agents != self.global_number_of_net_agents:
            time.sleep(1)

    def step(self):

        if self.big_iter == 0:
            Pyro4.config.COMMTIMEOUT = 0  # overrides timeout set by pyage. It's ugly but works.
            self.__synchronize_start()

        self.big_iter += 1

        if self.iter % self.iterations_per_update == 0:
            # self.__synchronize_end()
            # self.__synchronize_start()
            self.migration.update_overlaps(self)
            self.iter = 1;
        else:
            self.iter += 1
            if self.simulate_in_overlaps:
                self.overlaps.simulate()

        for agent in self.__agents.values():
            agent.step()

        if self.big_iter == self.number_of_iterations:
            self.__synchronize_end()

    def __move_agent(self, agent, x, y):
        self.__remove_agent_from_matrix(agent)

        if y >= self.net_dimensions.y:
            self.migration.migrate_direction(agent, x, 0, Direction.S)
        elif y < 0:
            self.migration.migrate_direction(agent, x, self.net_dimensions.y - 1, Direction.N)
        else:
            agent.position.y = y

            if x < 0:
                self.migration.migrate_direction(agent, self.net_dimensions.x - 1, y, Direction.W)
            elif x >= self.net_dimensions.x:
                self.migration.migrate_direction(agent, 0, y, Direction.E)
            else:
                agent.position.x = x
                self.agents_matrix[agent.position.y][agent.position.x].append(agent)

    def move_agent(self, agent):
        vector = SubAgent.directions[agent.direction_index]
        x = agent.position.x + vector.x
        y = agent.position.y + vector.y
        neighbours = self.can_move(x, y)

        if neighbours:
            agent.turn_around()
        else:
            self.__move_agent(agent, x, y)

    def can_move(self, x, y):
        if 0 <= x < self.net_dimensions.x and 0 <= y < self.net_dimensions.y:
            return len(self.agents_matrix[y][x]) > 0
        elif x < 0:
            return self.overlaps.contains_agent(Direction.W, 0, y)
        elif x >= self.net_dimensions.x:
            return self.overlaps.contains_agent(Direction.E, 0, y)
        elif y < 0:
            return self.overlaps.contains_agent(Direction.N, x, 0)
        return self.overlaps.contains_agent(Direction.S, x, 0)

    def get_neighbours(self, x, y, direction):
        cnt = 0

        # Tu trzeba dużo bardziej skomplikowany algorytm...
        # if x < 0 or y < 0 or y == self.net_dimensions.y:
        # if self.overlaps.contains_agent(Direction.W, x, y):
        #         cnt += 1
        # else:
        #     if x != old_x + 1:
        #         cnt += len(self.agents_matrix[y][x - 1])
        #
        # if x + 1 >= self.net_dimensions.x or y < 0 or y == self.net_dimensions.y:
        #     if self.overlaps.contains_agent(Direction.E, x + 1, y):
        #         cnt += 1
        # else:
        #     if x + 1 != old_x:
        #         cnt += len(self.agents_matrix[y][x + 1])
        #
        # if y < 1 or x < 0 or x == self.net_dimensions.x:
        #     if self.overlaps.contains_agent(Direction.S, x, y - 1):
        #         cnt += 1
        # else:
        #     if y - 1 != old_y:
        #         cnt += len(self.agents_matrix[y - 1][x])
        #
        # if y + 1 >= self.net_dimensions.y or x < 0 or x == self.net_dimensions.x:
        #     if self.overlaps.contains_agent(Direction.N, x, y + 1):
        #         cnt += 1
        # else:
        #     if y + 1 != old_y:
        #         cnt += len(self.agents_matrix[y + 1][x])

        return cnt

    def get_position_in_net_x(self):
        return self.position_in_net_x

    def get_position_in_net_y(self):
        return self.position_in_net_y

    def __append_to_ret(self, direction, ret, tab, tab_i, ret_i):
        for agent in tab[tab_i]:
            if not not agent:
                if direction == Direction.N or direction == Direction.S:
                    position = Vector(ret_i, agent[0].position.x)
                else:
                    position = Vector(ret_i, agent[0].position.y)
                overlap_agent = OverlapAgent(position, agent[0].direction_index)
                ret[ret_i].append(overlap_agent)

    def get_overlaps(self):
        return self.overlaps

    def get_overlap(self, direction):
        ret = [[] for _ in range(self.overlap_size)]

        if direction == Direction.N:
            for i in range(self.overlap_size):
                self.__append_to_ret(direction, ret, self.agents_matrix, i, i)
        elif direction == Direction.S:
            for i in range(self.overlap_size):
                self.__append_to_ret(direction, ret, self.agents_matrix, self.net_dimensions.y - 1 - i, i)
        else:
            overlap = [[] for _ in range(self.overlap_size)]
            if direction == Direction.E:
                for i in range(len(self.agents_matrix)):
                    for j in range(self.overlap_size):
                        overlap[j].append(self.agents_matrix[i][self.net_dimensions.x - 1 - j])
            else:
                for i in range(len(self.agents_matrix)):
                    for j in range(self.overlap_size):
                        overlap[j].append(self.agents_matrix[i][j])
            for i in range(self.overlap_size):
                self.__append_to_ret(direction, ret, overlap, i, i)
        return ret

    def __print_matrix(self):
        for agents in self.agents_matrix:
            print agents


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