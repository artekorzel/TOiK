import Pyro4
from pyage.core.agent.agent import AGENT
from multiprocessing import Pool


def create_agent_async(type, agents, agents_in_line, lines_of_agents):
    print "creating agent in [", str(agents_in_line), ", ", str(lines_of_agents), "]"
    agent = type(agents_in_line, lines_of_agents)
    agents[agent.get_address()] = agent
    print "AGENTS", str(agents)

def net_agent(type, net_agents_per_host, net_agents_per_line, ns_hostname):
    def factory():
        print 'starting factory'
        ns = Pyro4.locateNS(ns_hostname())
        current_number_of_agents = len(ns.list(AGENT))
        agents_in_line = current_number_of_agents % net_agents_per_line()
        lines_of_agents = current_number_of_agents / net_agents_per_line() - 1

        agents = {}
        for i in range(net_agents_per_host()):
            if agents_in_line % net_agents_per_line() == 0:
                agents_in_line = 0
                lines_of_agents += 1
            # pool = Pool(processes=1)
            # pool.apply_async(create_agent_async, [type, agents, agents_in_line, lines_of_agents])
            print "creating agent in [", str(agents_in_line), ", ", str(lines_of_agents), "]"
            agent = type(agents_in_line, lines_of_agents)
            agent.name = agent.get_address()
            agents[agent.get_address()] = agent
            agents_in_line += 1
        print "returning agents ", str(agents)
        return agents

    return factory


