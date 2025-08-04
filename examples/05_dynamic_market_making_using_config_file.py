"""
Example 2: Dynamic Market Making (based on simulation_with_blocknumber.yml)

This example demonstrates market making with volatile price action:
- High volatility ETH price simulation (40% annual volatility)
- Single liquidity position in volatile market
- Shows impact of price movements on LP positions
"""

import logging
import warnings


warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("root").setLevel(logging.ERROR)

from nqs_sdk import Simulation  # noqa: E402
from nqs_sdk.protocols import UniswapV3Factory  # noqa: E402


def main() -> None:
    """Run the dynamic market making simulation."""
    print("=" * 60)
    print("Example 2: Dynamic Market Making")
    print("=" * 60)
    print("This simulation demonstrates:")
    print("* Market making in high volatility environment (40% annual vol)")
    print("* ETH price simulation with Geometric Brownian Motion")
    print("* Impact of price movements on liquidity positions")
    print("* Based on simulation_with_blocknumber.yml test")
    print()

    print("[INIT] Initializing Uniswap V3 protocol factory...")
    uniswap_v3 = UniswapV3Factory()

    config_path = "./configs/dynamic_market_making_config.yml"
    print(f"[CONFIG] Loading configuration from {config_path}")

    try:
        sim = Simulation([uniswap_v3], config_path)
        print("[OK] Simulation created successfully")
    except Exception as e:
        print(f"[ERROR] Error creating simulation: {e}")
        return

    print("\n[RUN] Running simulation...")
    print("Block range: 18725000 -> 18726000 (1000 blocks)")
    print("Strategy: Single liquidity position in volatile market")
    print("Price model: GBM with 40% volatility, starting at $2000")

    try:
        if sim.simulator is None:
            print("[ERROR] Simulator is not initialized")
            return
        results = sim.simulator.run_to_dict()
        print("[SUCCESS] Simulation completed successfully!")

        # Display results summary
        print("\n[RESULTS] Summary:")
        print("-" * 40)

        # Portfolio analysis
        agent_initial_usdc = results.get('market_maker.all.wallet_holdings:{token="USDC"}', {}).get("values", [None])[0]
        agent_final_usdc = results.get('market_maker.all.wallet_holdings:{token="USDC"}', {}).get("values", [None])[-1]
        agent_initial_eth = results.get('market_maker.all.wallet_holdings:{token="ETH"}', {}).get("values", [None])[0]
        agent_final_eth = results.get('market_maker.all.wallet_holdings:{token="ETH"}', {}).get("values", [None])[-1]

        print("[PORTFOLIO] Market Maker Portfolio:")
        if agent_initial_usdc is not None and agent_final_usdc is not None:
            print(f"  * USDC: {agent_initial_usdc:,.0f} -> {agent_final_usdc:,.0f}")
        if agent_initial_eth is not None and agent_final_eth is not None:
            print(f"  * ETH: {agent_initial_eth:.2f} -> {agent_final_eth:.2f}")

        # Net position tracking
        net_position_values = results.get("market_maker.all.net_position", {}).get("values", [])
        if net_position_values:
            print(f"  * Net Position: ${net_position_values[0]:,.0f} -> ${net_position_values[-1]:,.0f}")
            pnl = net_position_values[-1] - net_position_values[0]
            pnl_pct = (pnl / net_position_values[0]) * 100 if net_position_values[0] > 0 else 0
            print(f"  * P&L: ${pnl:,.0f} ({pnl_pct:+.2f}%)")

    except Exception as e:
        print(f"[ERROR] Simulation failed: {e}")
        return


if __name__ == "__main__":
    main()
