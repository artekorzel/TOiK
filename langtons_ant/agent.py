# coding=utf-8
from pyage.core.address import Addressable
from pyage.core.inject import Inject
from langtons_ant.border import Border, BorderType
from langtons_ant.vector import random_vector, Vector

class NetAgent(Addressable):
    @Inject("locator", "net_dimensions", "layers")
    @Inject("sub_agents:_NetAgent__agents")
    @Inject("migration")
    @Inject("iterations_per_update")
    def __init__(self, position_in_net, name=None):
        super(NetAgent, self).__init__()
        self.position_in_net = position_in_net
        self.name = name
        self.agents_matrix = [[[] for i in range(self.net_dimensions.x)] for j in range(self.net_dimensions.y)]
        self.border = Border(self.net_dimensions.x, self.net_dimensions.y)
        for agent in self.__agents.values():
            self.__add_agent(agent)
        self.iter = 0

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
        if self.iter % self.iterations_per_update == 0:
            self.migration.update_border(self)
            self.iter = 1;
        else:
            self.iter += 1
        for agent in self.__agents.values():
            agent.step()

    def __move_agent(self, agent, vector):
        self.__remove_agent_from_matrix(agent)
        new_position_x = agent.position.x + vector.x
        new_position_y = agent.position.y + vector.y

        if new_position_y >= self.net_dimensions.y:
            agent.position.y = 0
        elif new_position_y < 0:
            agent.position.y = self.net_dimensions.y - 1
        else:
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
        v = SubAgent.directions[agent.direction_index]
        x = agent.position.x + v.x
        y = agent.position.y + v.y
        neighbours = self.get_neighbours(x, y, agent.position.x, agent.position.y)
        if neighbours > 0:
            agent.turn_around()
        else:
            self.__move_agent(agent, SubAgent.directions[agent.direction_index])

    def get_neighbours(self, x, y, old_x, old_y):
        cnt = 0
        if x < 1 or y < 0 or y == self.net_dimensions.y:
            if self.border.containsAgent(BorderType.W, x - 1, y):
                cnt += 1
        else:
            if x != old_x + 1:
                cnt += len(self.agents_matrix[y][x - 1])

        if x + 1 >= self.net_dimensions.x or y < 0 or y == self.net_dimensions.y:
            if self.border.containsAgent(BorderType.E, x + 1, y):
                cnt += 1
        else:
            if x + 1 != old_x:
                cnt += len(self.agents_matrix[y][x + 1])

        if y < 1 or x < 0 or x == self.net_dimensions.x:
            if self.border.containsAgent(BorderType.S, x, y - 1):
                cnt += 1
        else:
            if y - 1 != old_y:
                cnt += len(self.agents_matrix[y - 1][x])

        if y + 1 >= self.net_dimensions.y or x < 0 or x == self.net_dimensions.x:
            if self.border.containsAgent(BorderType.N, x, y + 1):
                cnt += 1
        else:
            if y + 1 != old_y:
                cnt += len(self.agents_matrix[y + 1][x])

        return cnt

    def get_position_in_net(self):
        return self.position_in_net

    def get_border(self):
        return self.border

    def __append_to_ret(self, ret, tab, tab_i, ret_i):
        for agent in tab[tab_i]:
            if not not agent:
                ret[ret_i].append(agent[0].position.x)

    def get_border_n(self):
        ret = [[] for _ in range(2)]
        self.__append_to_ret(ret, self.agents_matrix, 0, 0)
        self.__append_to_ret(ret, self.agents_matrix, 1, 1)
        return ret

    def get_border_s(self):
        ret = [[] for _ in range(2)]
        self.__append_to_ret(ret, self.agents_matrix, self.net_dimensions.y - 1, 0)
        self.__append_to_ret(ret, self.agents_matrix, self.net_dimensions.y - 2, 1)
        return ret

    def get_border_w(self):
        border = [[] for _ in range(2)]
        ret = [[] for _ in range(2)]
        for i in range(len(self.agents_matrix)):
            border[0].append(self.agents_matrix[i][self.net_dimensions.x - 1])
            border[1].append(self.agents_matrix[i][self.net_dimensions.x - 2])
        self.__append_to_ret(ret, border, 0, 0)
        self.__append_to_ret(ret, border, 1, 1)
        return ret

    def get_border_e(self):
        border = [[] for _ in range(2)]
        ret = [[] for _ in range(2)]
        for i in range(len(self.agents_matrix)):
            border[0].append(self.agents_matrix[i][0])
            border[1].append(self.agents_matrix[i][1])
        self.__append_to_ret(ret, border, 0, 0)
        self.__append_to_ret(ret, border, 1, 1)
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