# coding=utf-8
from pyage.core.inject import Inject
from pyage.core.statistics import Statistics


class PositionStatistics(Statistics):
    @Inject("net_agents_per_line")
    @Inject("net_agents_count")
    def __init__(self, output_file_name="positions_%d.txt"):
        self.output_file_name = output_file_name
        self.config = True

    def update(self, step_count, net_agents):
        with open(self.output_file_name % step_count, "w") as out:
            for net_agent in net_agents:
                net_agent_position_x = net_agent.get_position_in_net_x() * net_agent.net_dimensions.x
                net_agent_position_y = net_agent.get_position_in_net_y() * net_agent.net_dimensions.y
                for agent in net_agent.get_agents():
                    out.write("%s: %d %d %d %d\n" %
                              (agent.get_address(), agent.position.x + net_agent_position_x,
                               agent.position.y + net_agent_position_y,
                               net_agent.layers[0].get_current_cell(agent).color, agent.direction_index))

    def summarize(self, agents):
        pass