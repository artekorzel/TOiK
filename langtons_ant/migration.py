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

    def migrate_to_previous(self, agent):
        if agent.parent.position_in_net == 0:
            pass
        agent.position.x = self.net_dimensions.x - 1
        ns = Pyro4.locateNS(self.ns_hostname)
        list_of_agents = ns.list(AGENT)
        next_parent = Pyro4.Proxy(list_of_agents[agent.parent.position_in_net - 1])
        next_parent.add_agent(agent.parent.remove_agent(agent))

    def migrate_to_next(self, agent):
        ns = Pyro4.locateNS(self.ns_hostname)
        list_of_agents = ns.list(AGENT)
        number_of_agents = len(list_of_agents)
        if agent.parent.position_in_net == number_of_agents - 1:
            pass
        agent.position.y = 0
        next_parent = Pyro4.Proxy(list_of_agents[agent.parent.position_in_net + 1])
        next_parent.add_agent(agent.parent.remove_agent(agent))


