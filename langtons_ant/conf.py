# coding=utf-8
import os
import logging
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

ns_hostname = lambda: os.environ['NS_HOSTNAME']

net_dimensions = lambda: Vector(30, 30)

agents = net_agent(NetAgent, ns_hostname)
layers = lambda: [ColorLayer()]
sub_agents = unnamed_agents(1, SubAgent)

stop_condition = lambda: StepLimitStopCondition(1000)

address_provider = SequenceAddressProvider

migration = CrossBorderMigration
locator = ParentLocator
stats = lambda: PositionStatistics("../positions/langtons_ant_positions_%05d.txt")