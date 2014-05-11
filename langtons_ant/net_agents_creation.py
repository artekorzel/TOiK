import Pyro4
from pyage.core.agent.agent import AGENT


def net_agent(type, count, ns_hostname):
    def factory():
        ns = Pyro4.locateNS(ns_hostname())
        number_of_agents = len(ns.list(AGENT))

        agents = {}
        for i in range(count):
            agent = type(number_of_agents)
            agents[agent.get_address()] = agent
            number_of_agents += 1
        return agents

    return factory