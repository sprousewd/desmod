from __future__ import division

import json

from desmod.simulation import SimEnvironment, SimStopEvent
from desmod.timescale import parse_time, scale_time


class Environment(SimEnvironment):
    """Simulation environment with Snowbird-specific global state."""

    def __init__(self, config):
        super(Environment, self).__init__(config)

