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
from math import sqrt

logger = logging.getLogger(__name__)

stop_condition = lambda: StepLimitStopCondition(20)
net_dimensions = lambda: Vector(15, 15)


# Distributed environment settings
number_of_hosts = lambda: 2
global_number_of_net_agents = lambda: 2  # square root must be an integer
net_agents_per_host = lambda: global_number_of_net_agents() / number_of_hosts()
net_agents_per_line = lambda: int(sqrt(global_number_of_net_agents()))
waiting_interval = lambda: 3  # frequency of checking presence of all net_agents (in seconds)
# ================================

agents_per_net = 6
layers = lambda: [ColorLayer()]

iterations_per_update = lambda: 5
overlap_size = lambda: 5
simulate_in_overlaps = lambda: True
overlap_simulation_agent_turnaround = lambda: True

ns_hostname = lambda: os.environ['NS_HOSTNAME']

agents = net_agent(NetAgent, net_agents_per_host, net_agents_per_line, ns_hostname)
sub_agents = unnamed_agents(agents_per_net, SubAgent)

address_provider = SequenceAddressProvider
migration = CrossBorderMigration

locator = ParentLocator
pyro_daemon = Pyro4.Daemon()
daemon = lambda: pyro_daemon

stats = lambda: PositionStatistics("../positions/langtons_ant_positions_%05d.txt")