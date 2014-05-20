import logging
import Pyro4
from pyage.core.agent.agent import AGENT
from pyage.core.inject import Inject
from pyage.core.migration import Migration
from langtons_ant import agent
from langtons_ant.border import BorderType

logger = logging.getLogger(__name__)


class CrossBorderMigration(Migration):
    @Inject("ns_hostname", "net_dimensions")
    def __init__(self):
        super(CrossBorderMigration, self).__init__()

    def get_north_neighbour(self, agent):
        return agent

    def get_south_neighbour(self, agent):
        return agent

    def get_west_neighbour(self, netAgent):
        ns = Pyro4.locateNS(self.ns_hostname)
        list_of_agents = ns.list(AGENT)
        previous_parent_in_net = netAgent.position_in_net - 1

        if previous_parent_in_net == -1:
            previous_parent_in_net = len(list_of_agents) - 1

        return self.__get_agent(list_of_agents, previous_parent_in_net)

    def get_east_neighbour(self, netAgent):
        ns = Pyro4.locateNS(self.ns_hostname)
        list_of_agents = ns.list(AGENT)
        number_of_agents = len(list_of_agents)
        next_parent_in_net = netAgent.position_in_net + 1

        if next_parent_in_net == number_of_agents:
            next_parent_in_net = 0

        return self.__get_agent(list_of_agents, next_parent_in_net)

    def migrate_to_previous(self, subAgent, posy):
        previous_parent = self.get_west_neighbour(subAgent.parent)
        subAgent.position.x = self.net_dimensions.x - 1
        previous_parent.add_existing_agent(subAgent.parent.remove_agent(subAgent), self.net_dimensions.x - 1, posy)

    def migrate_to_next(self, subAgent, posy):
        current_parent = subAgent.parent
        next_parent = self.get_east_neighbour(subAgent.parent)
        subAgent.position.y = 0
        next_parent.add_existing_agent(current_parent.remove_agent(subAgent), 0, posy)

    def __get_agent(self, agents, agent_nr):
        for agent in agents:
            currAgent = Pyro4.Proxy(agents[agent])
            if currAgent.get_position_in_net() == agent_nr:
                return currAgent
        return None

    def update_border(self, netAgent):
        border = netAgent.get_border()
        border.clear()
        neighbour = self.get_north_neighbour(netAgent)
        border.addAgents(BorderType.N, neighbour.get_border_s())
        neighbour = self.get_south_neighbour(netAgent)
        border.addAgents(BorderType.S, neighbour.get_border_n())
        neighbour = self.get_west_neighbour(netAgent)
        border.addAgents(BorderType.E, neighbour.get_border_w())
        neighbour = self.get_east_neighbour(netAgent)
        border.addAgents(BorderType.W, neighbour.get_border_e())