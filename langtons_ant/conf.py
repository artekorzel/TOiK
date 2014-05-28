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

net_dimensions = lambda: Vector(100, 100)

ns_hostname = lambda: os.environ['NS_HOSTNAME']

net_agents_per_line = lambda: 1
net_agents_count = lambda: 1
agents_per_net = 1
agents = net_agent(NetAgent, net_agents_count, net_agents_per_line, ns_hostname)
layers = lambda: [ColorLayer()]
sub_agents = unnamed_agents(agents_per_net, SubAgent)
iterations_per_update = lambda: 20

overlap_size = lambda: 1
overlap_simulation = lambda: True

stop_condition = lambda: StepLimitStopCondition(15000)

address_provider = SequenceAddressProvider
migration = CrossBorderMigration

locator = ParentLocator
pyro_daemon = Pyro4.Daemon()
daemon = lambda: pyro_daemon

stats = lambda: PositionStatistics("../positions/langtons_ant_positions_%05d.txt")