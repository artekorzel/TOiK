import logging
import Pyro4
from pyage.core.agent.agent import AGENT
from pyage.core.inject import Inject
from pyage.core.migration import Migration
from langtons_ant.overlap import Direction

logger = logging.getLogger(__name__)


class CrossBorderMigration(Migration):
    @Inject("ns_hostname", "net_dimensions", "net_agents_per_line")
    def __init__(self):
        super(CrossBorderMigration, self).__init__()

    def migrate_direction(self, subAgent, posx, posy, direction):
        current_parent = subAgent.parent
        next_parent = self.get_neighbour(current_parent, direction)
        subAgent.position.x = posx
        subAgent.position.y = posy
        next_parent.add_existing_agent(current_parent.remove_agent(subAgent), posx, posy)

    def get_neighbour(self, netAgent, direction):
        ns = Pyro4.locateNS(self.ns_hostname)
        list_of_agents = ns.list(AGENT)
        number_of_agents = len(list_of_agents)
        agent_nr = netAgent.position_in_net_y * self.net_agents_per_line + netAgent.position_in_net_x + 1

        if direction == Direction.N:
            next_parent_x = netAgent.position_in_net_x
            next_parent_y = self.__next_north_neighbour(netAgent, number_of_agents, agent_nr)
        elif direction == Direction.S:
            next_parent_x = netAgent.position_in_net_x
            next_parent_y = self.__next_south_neighbour(netAgent, number_of_agents)
        elif direction == Direction.W:
            next_parent_x = self.__next_west_neighbour(netAgent, number_of_agents, agent_nr)
            next_parent_y = netAgent.position_in_net_y
        else:
            next_parent_x = self.__next_east_neighbour(netAgent, number_of_agents, agent_nr)
            next_parent_y = netAgent.position_in_net_y

        return self.__get_agent(list_of_agents, next_parent_x, next_parent_y)

    def update_overlaps(self, netAgent):
        overlaps = netAgent.get_overlaps()
        overlaps.clear()
        neighbour = self.get_neighbour(netAgent, Direction.N)
        overlaps.add_agents(Direction.N, neighbour.get_overlap(Direction.S))
        neighbour = self.get_neighbour(netAgent, Direction.S)
        overlaps.add_agents(Direction.S, neighbour.get_overlap(Direction.N))
        neighbour = self.get_neighbour(netAgent, Direction.E)
        overlaps.add_agents(Direction.E, neighbour.get_overlap(Direction.W))
        neighbour = self.get_neighbour(netAgent, Direction.W)
        overlaps.add_agents(Direction.W, neighbour.get_overlap(Direction.E))

    def __next_north_neighbour(self, netAgent, number_of_agents, current_agent_nr):
        neighbour = netAgent.position_in_net_y + 1
        if number_of_agents - current_agent_nr < self.net_agents_per_line:
            neighbour = 0
        return neighbour

    def __next_south_neighbour(self, netAgent, number_of_agents):
        next_parent = netAgent.position_in_net_y - 1
        if next_parent < 0:
            last_agent_position = (number_of_agents - 1) % self.net_agents_per_line
            if netAgent.position_in_net_x <= last_agent_position:
                next_parent = (number_of_agents - 1) / self.net_agents_per_line
            else:
                next_parent = (number_of_agents - 1) / self.net_agents_per_line - 1
        return next_parent

    def __next_west_neighbour(self, netAgent, number_of_agents, current_agent_nr):
        next_parent = netAgent.position_in_net_x - 1
        if next_parent == -1:
            if ((current_agent_nr - 1) / self.net_agents_per_line) == ((number_of_agents - 1) / self.net_agents_per_line):
                next_parent = (number_of_agents - 1) % self.net_agents_per_line
            else:
                next_parent = self.net_agents_per_line - 1
        return next_parent

    def __next_east_neighbour(self, netAgent, number_of_agents, current_agent_nr):
        next_parent = netAgent.position_in_net_x + 1
        if current_agent_nr == number_of_agents or next_parent == self.net_agents_per_line:
            next_parent = 0
        return next_parent

    def __get_agent(self, agents, agent_nr_x, agent_nr_y):
        for agent in agents:
            currAgent = Pyro4.Proxy(agents[agent])
            if currAgent.get_position_in_net_x() == agent_nr_x and currAgent.get_position_in_net_y() == agent_nr_y:
                return currAgent
        return None
