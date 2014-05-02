# coding=utf-8
import logging
from pyage.core.address import SequenceAddressProvider
from pyage.core.agent.agent import unnamed_agents
from pyage.core.locator import ParentLocator
from pyage.core.migration import NoMigration
from pyage.core.stop_condition import StepLimitStopCondition
from pyage.langtons_ant.agent import NetAgent, SubAgent
from pyage.langtons_ant.layer import ColorLayer
from pyage.langtons_ant.statistics import PositionStatistics
from pyage.langtons_ant.vector import Vector


logger = logging.getLogger(__name__)

net_dimensions = lambda: Vector(30, 30)

agents = unnamed_agents(1, NetAgent)
layers = lambda: [ColorLayer()]
sub_agents = unnamed_agents(1, SubAgent)

stop_condition = lambda: StepLimitStopCondition(1000)

address_provider = SequenceAddressProvider

migration = NoMigration
locator = ParentLocator
stats = lambda: PositionStatistics("positions/langtons_ant_positions_%d.txt")