from typing import List, Optional, Tuple

from nqs_sdk import MetricName, Metrics, RefSharedState, SealedParameters, SimulationClock, TxRequest
from nqs_sdk.bindings.env_builder import SimulatorEnvBuilder
from nqs_sdk.bindings.protocols.uniswap_v3.spots.historical_uniswap_pool import HistoricalSpotGenerator
from nqs_sdk.bindings.protocols.uniswap_v3.tx_generators.univ3_historical_tx_generator import Univ3HistoricalTxGenerator
from nqs_sdk.bindings.protocols.uniswap_v3.uniswap_v3_factory import UniswapV3Factory
from nqs_sdk.bindings.protocols.uniswap_v3.uniswap_v3_pool import UniswapV3Pool
from nqs_sdk.bindings.protocols.uniswap_v3.uniswap_v3_transactions import RawSwapTransaction
from nqs_sdk.bindings.tx_generators.abstract_transaction import Transaction
from nqs_sdk.interfaces.observable_consumer import ObservableConsumer
from nqs_sdk.interfaces.tx_generator import TxGenerator


class AgentTransaction(TxGenerator, ObservableConsumer):
    def __init__(self, agent_name: str, required_metrics: List[str]) -> None:
        super().__init__()
        self.txns: List[Tuple[Transaction, UniswapV3Pool]] = []
        self.agent_name = agent_name
        self.required_metrics = required_metrics

    @property
    def factory_id(self) -> str:
        return "uniswap_v3"

    def id(self) -> str:
        return self.agent_name

    def initialize(self, parameters: SealedParameters) -> None:
        return

    def consume(self, parameters: SealedParameters, clock: SimulationClock) -> Tuple[List[MetricName], Optional[int]]:
        metrics_names = []

        for metric_name in self.required_metrics:
            metrics_names.append(parameters.str_to_metric(metric_name))

        return metrics_names, None

    def append_tx(self, tx: Transaction, uniswap_pool: UniswapV3Pool) -> None:
        self.txns.append((tx, uniswap_pool))

    def next(
        self,
        clock: SimulationClock,
        state: RefSharedState,
        metrics: Metrics,
    ) -> Tuple[List[TxRequest], Optional[int]]:
        txns = []
        agent_addr = state.agent_name_to_addr(self.agent_name)

        for raw_tx, pool in self.txns:
            tx = raw_tx.to_tx_request(pool.name, self.agent_name, agent_addr)
            txns.append(tx)
        self.txns = []  # clear pending agent transactions

        return txns, None


def uniswap_v3_simulation_builder(uniswap_pools: List[UniswapV3Pool]) -> SimulatorEnvBuilder:
    env_builder = SimulatorEnvBuilder()
    uniswap_factory = UniswapV3Factory()
    env_builder.register_factory(uniswap_factory)

    for uniswap_pool in uniswap_pools:
        env_builder.register_protocol(uniswap_pool)  # maybe misleading function name
        tx_generator = Univ3HistoricalTxGenerator(uniswap_pool)
        env_builder.register_tx_generator(tx_generator)

    return env_builder


def register_agent(
    env_builder: SimulatorEnvBuilder, agent_name: str, agent_wallet: dict, required_metrics: List[str]
) -> AgentTransaction:
    env_builder.register_agent(agent_name, agent_wallet)
    tx_generator = AgentTransaction(agent_name, required_metrics)
    env_builder.register_tx_generator(tx_generator)
    return tx_generator


def main() -> None:
    # uniswap_pool = UniswapV3Pool.from_custom_params(token0="USDT", token1="USDC", fee_tier=0.01,
    #                                                 initial_amount=100000000, unit="token0")
    uniswap_pool = UniswapV3Pool.from_address("0x3416cf6c708da44db2624d63ea0aaef7113527c6", 18725000)

    env_builder = uniswap_v3_simulation_builder([uniswap_pool])

    spot_generator = HistoricalSpotGenerator([uniswap_pool])
    env_builder.register_spot_generator(spot_generator)

    env_builder.set_simulator_time(18725000, 18725010, 1)
    env_builder.set_numeraire("USDC")
    env_builder.set_gas_fee(10, "USDC")

    # Define metric keys you use
    agent_name = "swapper_agent"
    usdt_wallet_key = f'{agent_name}.all.wallet_holdings:{{token="USDT"}}'
    usdc_wallet_key = f'{agent_name}.all.wallet_holdings:{{token="USDC"}}'
    dex_spot_key = f"{uniswap_pool.name}.dex_spot"
    agent_handler = register_agent(
        env_builder, agent_name, {"USDT": 10000, "USDC": 10000}, [usdt_wallet_key, usdc_wallet_key, dex_spot_key]
    )

    simulation = env_builder.build()
    for out in simulation:
        print(out)

        usdt_wallet = out.observables.get(usdt_wallet_key)
        usdc_wallet = out.observables.get(usdc_wallet_key)
        dex_spot = out.observables.get(dex_spot_key)

        # ensure initial values
        if out.block == 18725000:
            # Store initial wallet holdings and dex spot
            initial_usdt_wallet = usdt_wallet
            initial_usdc_wallet = usdc_wallet
            initial_dex_spot = dex_spot

            # Verify initial holdings
            assert initial_usdt_wallet == 10000, f"Expected initial USDT wallet to be 10000, got {initial_usdt_wallet}"
            assert initial_usdc_wallet == 10000, f"Expected initial USDC wallet to be 10000, got {initial_usdc_wallet}"
            assert initial_dex_spot is not None, "DEX spot should be available"

        else:
            print(dex_spot)
            if dex_spot <= 1:
                raw_swap_tx = RawSwapTransaction(amount=100000000, zero_for_one=True, sqrt_price_limit_x96=None)
                agent_handler.append_tx(raw_swap_tx, uniswap_pool)


if __name__ == "__main__":
    main()
