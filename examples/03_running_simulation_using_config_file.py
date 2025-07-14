import nqs_sdk.preload  # noqa: F401
from nqs_sdk import Simulation
from nqs_sdk.protocols import UniswapV3Factory


uniswap_v3 = UniswapV3Factory()  # factory for all UniswapV3 instances
sim = Simulation([uniswap_v3], "./configs/basic_config.yml")

results = sim.run()  # dictionary with all requested timeseries results
