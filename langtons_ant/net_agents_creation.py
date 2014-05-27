import Pyro4
from pyage.core.agent.agent import AGENT


def net_agent(type, count, net_agents_per_line, ns_hostname):
    def factory():
        ns = Pyro4.locateNS(ns_hostname())
        total_agents = len(ns.list(AGENT))
        agents_in_line = total_agents % net_agents_per_line()
        lines_of_agents = total_agents / net_agents_per_line() - 1

        agents = {}
        for i in range(count):
            if agents_in_line % net_agents_per_line() == 0:
                agents_in_line = 0
                lines_of_agents += 1
            print "creating agent in [", str(agents_in_line), ", ", str(lines_of_agents), "]"
            agent = type(agents_in_line, lines_of_agents)
            agents[agent.get_address()] = agent
            agents_in_line += 1
        return agents

    return factory