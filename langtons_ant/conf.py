# coding=utf-8
import os
import logging
import Pyro4
from pyage.core.address import SequenceAddressProvider
from pyage.core.agent.agent import unnamed_agents
from pyage.core.locator import ParentLocator
from pyage.core.stop_condition import StepLimitStopCondition
from langtons_ant.agent import NetAgent, SubAgent
from langtons_ant.layer import ColorLayer
from langtons_ant.statistics import PositionStatistics
from langtons_ant.vector import Vector
from langtons_ant.migration import CrossBorderMigration
from langtons_ant.net_agents_creation import net_agent

logger = logging.getLogger(__name__)

stop_condition = lambda: StepLimitStopCondition(12000)
net_dimensions = lambda: Vector(100, 100)
net_agents_per_line = lambda: 1
net_agents_count = lambda: 2
agents_per_net = 6
layers = lambda: [ColorLayer()]

iterations_per_update = lambda: 100
overlap_size = lambda: 5
simulate_in_overlaps = lambda: True
overlap_simulation_agent_turnaround = lambda: True

ns_hostname = lambda: os.environ['NS_HOSTNAME']

agents = net_agent(NetAgent, net_agents_count, net_agents_per_line, ns_hostname)
sub_agents = unnamed_agents(agents_per_net, SubAgent)

address_provider = SequenceAddressProvider
migration = CrossBorderMigration

locator = ParentLocator
pyro_daemon = Pyro4.Daemon()
daemon = lambda: pyro_daemon

stats = lambda: PositionStatistics("../positions/langtons_ant_positions_%05d.txt")