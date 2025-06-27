import os

import nqs_sdk.preload  # noqa: F401
from nqs_sdk import ProtocolManager, Simulation
from nqs_sdk.spot import DataLoader  # noqa: E402


uniswap_v3 = ProtocolManager("uniswap_v3_rust")
sim = Simulation([uniswap_v3], "./configs/basic_config.yml")

results = sim.run()
