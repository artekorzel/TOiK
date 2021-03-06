import Pyro4
from pyage.core.agent.agent import AGENT
from multiprocessing import Pool


def create_agent_async(type, agents, agents_in_line, lines_of_agents):
    print "creating agent in [", str(agents_in_line), ", ", str(lines_of_agents), "]"
    agent = type(agents_in_line, lines_of_agents)
    agents[agent.get_address()] = agent


def net_agent(type, net_agents_per_host, net_agents_per_line, ns_hostname):
    def factory():
        ns = Pyro4.locateNS(ns_hostname())
        current_number_of_agents = len(ns.list(AGENT))
        agents_in_line = current_number_of_agents % net_agents_per_line()
        lines_of_agents = current_number_of_agents / net_agents_per_line() - 1

        agents = {}
        for i in range(net_agents_per_host()):
            if agents_in_line % net_agents_per_line() == 0:
                agents_in_line = 0
                lines_of_agents += 1
            elif len(agents) == 0:
                agents_in_line = current_number_of_agents % net_agents_per_line()
                lines_of_agents += 1
            print "creating agent in [", str(agents_in_line), ", ", str(lines_of_agents), "]"
            agent = type(agents_in_line, lines_of_agents)
            agent.name = agent.get_address()
            agents[agent.get_address()] = agent
            agents_in_line += 1
        return agents

    return factory


