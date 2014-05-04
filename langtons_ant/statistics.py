# coding=utf-8
from pyage.core.statistics import Statistics


class PositionStatistics(Statistics):
    def __init__(self, output_file_name="positions_%d.txt"):
        self.output_file_name = output_file_name

    def update(self, step_count, net_agents):
        with open(self.output_file_name % step_count, "w") as out:
            for net_agent in net_agents:
                for agent in net_agent.get_agents():
                    out.write("%s: %d %d %d %d\n" %
                              (agent.get_address(), agent.position.x, agent.position.y,
                               net_agent.layers[0].get_current_cell(agent).color, agent.direction_index))

    def summarize(self, agents):
        pass