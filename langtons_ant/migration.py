import logging
import Pyro4
from pyage.core.agent.agent import AGENT
from pyage.core.inject import Inject
from pyage.core.migration import Migration

logger = logging.getLogger(__name__)


class CrossBorderMigration(Migration):
    @Inject("ns_hostname", "net_dimensions")
    def __init__(self):
        super(CrossBorderMigration, self).__init__()

    def migrate_to_previous(self, agent, posy):
        ns = Pyro4.locateNS(self.ns_hostname)
        list_of_agents = ns.list(AGENT)
        next_parent_in_net = agent.parent.position_in_net - 1

        if next_parent_in_net == -1:
            next_parent_in_net = len(list_of_agents) - 1

        agent.position.x = self.net_dimensions.x - 1

        previous_parent = self.__get_agent(list_of_agents, next_parent_in_net)
        previous_parent.add_existing_agent(agent.parent.remove_agent(agent), self.net_dimensions.x - 1, posy)

    def migrate_to_next(self, agent, posy):
        ns = Pyro4.locateNS(self.ns_hostname)
        list_of_agents = ns.list(AGENT)
        number_of_agents = len(list_of_agents)
        next_parent_in_net = agent.parent.position_in_net + 1

        if next_parent_in_net == number_of_agents:
            next_parent_in_net = 0

        agent.position.y = 0

        next_parent = self.__get_agent(list_of_agents, next_parent_in_net)
        next_parent.add_existing_agent(agent.parent.remove_agent(agent), 0, posy)

    def __get_agent(self, agents, agent_nr):
        for agent in agents:
            currAgent = Pyro4.Proxy(agents[agent])
            if currAgent.get_position_in_net() == agent_nr:
                return currAgent
        return None
