# mypy: disable-error-code="list-item"
from typing import Any

from nqs_sdk.bindings.protocols.uniswap_v3.spots.historical_uniswap_pool import HistoricalSpotGenerator
from nqs_sdk.bindings.protocols.uniswap_v3.uniswap_v3_pool import UniswapV3Pool
from nqs_sdk.coding_envs.coding_env import CodingEnv
from nqs_sdk.coding_envs.policy_caller import PolicyCaller
from nqs_sdk.coding_envs.protocols.coding_protocol import CodingProtocol
from nqs_sdk.coding_envs.protocols.uniswap_v3.uniswap_v3_coding_env import UniswapV3CodingProtocol
from nqs_sdk.utils.logging import local_logger


logger = local_logger(__name__)


class SpotTrackingStrategy(PolicyCaller):
    def __init__(self) -> None:
        self.position_id = "tracking_position"
        self.has_position = False
        self.target_range_pct = 0.001  # +/- 0.1%

        # Store previous values to compare for logging
        self.prev_values = {
            "current_spot": None,
            "liquidity": None,
            "usdc_holdings": None,
            "usdt_holdings": None,
            "usdc_token_amount": None,
            "usdt_token_amount": None,
            "fees_collected": None,
            "fees_not_collected": None,
        }

    def log_if_changed(self, key: str, message: str, value: Any = None) -> None:
        """Log message only if the value has changed since the last log."""
        if value is None:
            value = message
        if self.prev_values[key] != value:
            logger.info(message)
            self.prev_values[key] = value

    def policy(self, block: int, protocols: dict[str, CodingProtocol]) -> None:
        # This strategy requires protocols to be instances of UniswapV3CodingProtocol
        for protocol in protocols.values():
            if not isinstance(protocol, UniswapV3CodingProtocol):
                raise TypeError("This strategy requires UniswapV3CodingProtocol instances")

            # Log progression
            current_spot = protocol.dex_spot()[-1]  # Get the latest spot price
            self.log_if_changed("current_spot", f"Current spot at block {block}: {current_spot}", current_spot)
            self.log_if_changed("liquidity", f"Pool liquidity: {protocol.liquidity()[-1]}")
            self.log_if_changed("usdc_holdings", f"{protocol.get_wallet_holdings("USDC")=}")
            self.log_if_changed("usdt_holdings", f"{protocol.get_wallet_holdings("USDT")=}")
            if self.has_position:
                self.log_if_changed("usdc_token_amount", f"{protocol.token_amount("USDC", self.position_id)=}")
                self.log_if_changed("usdt_token_amount", f"{protocol.token_amount("USDT", self.position_id)=}")
                self.log_if_changed("fees_collected", f"{protocol.fees_collected()=}")
                self.log_if_changed("fees_not_collected", f"{protocol.fees_not_collected()=}")

            # print(f"{protocol.observables=}") # all available observables

            if not self.has_position:
                lower_bound = float(current_spot) * (1 - self.target_range_pct)
                upper_bound = float(current_spot) * (1 + self.target_range_pct)

                if protocol.get_wallet_holdings("USDC") == 0 or protocol.get_wallet_holdings("USDT") == 0:
                    return

                protocol.mint(
                    lower_bound,
                    upper_bound,
                    # FIXME -1 hack to avoid overflow in Mint (due to raw conversion)
                    protocol.get_wallet_holdings("USDC") - 1,
                    protocol.get_wallet_holdings("USDT") - 1,
                    self.position_id,
                )
                self.has_position = True
                logger.info(f"Initial position to {lower_bound}:{upper_bound}")

            else:
                position_lower, position_upper = protocol.position_bounds(self.position_id)

                if current_spot <= position_lower or current_spot >= position_upper:
                    # Burn and collect current position
                    protocol.burn(1.0, self.position_id)

                    # Mint new position around current spot
                    lower_bound = float(current_spot) * (1 - self.target_range_pct)
                    upper_bound = float(current_spot) * (1 + self.target_range_pct)

                    protocol.mint(
                        lower_bound,
                        upper_bound,
                        # FIXME -1 hack to avoid overflow in Mint (due to raw conversion)
                        protocol.get_wallet_holdings("USDC") + protocol.token_amount("USDC", self.position_id) - 1,
                        protocol.get_wallet_holdings("USDT") + protocol.token_amount("USDT", self.position_id) - 1,
                        self.position_id,
                    )
                    logger.info(f"Update position to {lower_bound}:{upper_bound}")


def main() -> None:
    uniswap_pool = UniswapV3Pool.from_params(token0="USDT", token1="USDC", fee_tier=0.01, blocknumber=18725000)
    uniswap_v3_coding_env = UniswapV3CodingProtocol(uniswap_pool)
    spot_generator = HistoricalSpotGenerator([uniswap_v3_coding_env.protocol])

    env = CodingEnv(do_backtest=True)
    env.register_protocol(uniswap_v3_coding_env)
    env.register_spot_generator(spot_generator)
    env.set_simulation_time(18725000, 18726010, 1)  # FIXME NOT TIME; THESE ARE BLOCK NUMBERS
    env.set_numeraire("USDC")
    env.set_gas_fee(10000000, "USDC")

    env.register_agent("agent_1", {"USDC": 1500, "USDT": 1000}, SpotTrackingStrategy())
    out = env.run()
    logger.info(f"Run outputs {len(out)} observables")


if __name__ == "__main__":
    main()
