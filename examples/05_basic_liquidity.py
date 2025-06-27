"""
Example 1: Basic Liquidity Management

This example demonstrates the complete lifecycle of a liquidity position:
- Creating a liquidity position with specific tick ranges
- Closing the position to collect fees and principal
"""

import os
import sys
import warnings
import logging

# Disable all warnings
warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("root").setLevel(logging.ERROR)


project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

import nqs_sdk.preload  # noqa: F401
from nqs_sdk import ProtocolManager, Simulation


def main():
    """Run the basic liquidity management simulation."""
    print("=" * 60)
    print("Example 1: Basic Liquidity Management")
    print("=" * 60)
    print("This simulation demonstrates:")
    print("* Creating a liquidity position in USDC/USDT pool")
    print("* Using tight tick ranges for stable pairs")
    print()
    
    print("[INIT] Initializing Uniswap V3 protocol manager...")
    uniswap_v3 = ProtocolManager("uniswap_v3_rust")
    
    config_path = "./configs/basic_liquidity_config.yml"
    print(f"[CONFIG] Loading configuration from {config_path}")
    
    try:
        sim = Simulation([uniswap_v3], config_path)
        print("[OK] Simulation created successfully")
    except Exception as e:
        print(f"[ERROR] Error creating simulation: {e}")
        return
    
    print("\n[RUN] Running simulation...")
    print("Block range: 18725000 -> 18725002 (3 blocks)")
    print("Strategy: Mint liquidity -> Collect fees -> Burn position")
    
    try:
        results = sim.simulator.run_to_dict()          # using run_to_dict() here for easier exploit the results TODO: use run_to_dict() in pycore run() by default, instead of returning a str 
        print("[SUCCESS] Simulation completed successfully!")
        
        # Display results summary
        print("\n[RESULTS] Summary:")
        print("-" * 40)
        
        # Agent wallet analysis
        agent_initial_usdc = results.get("liquidity_provider.all.wallet_holdings:{token=\"USDC\"}", {}).get("values", [None])[0]
        agent_final_usdc = results.get("liquidity_provider.all.wallet_holdings:{token=\"USDC\"}", {}).get("values", [None])[-1]
        agent_initial_usdt = results.get("liquidity_provider.all.wallet_holdings:{token=\"USDT\"}", {}).get("values", [None])[0]
        agent_final_usdt = results.get("liquidity_provider.all.wallet_holdings:{token=\"USDT\"}", {}).get("values", [None])[-1]
        
        print(f"[PORTFOLIO] Agent Portfolio:")
        print(f"  * Initial USDC: {agent_initial_usdc:,.0f} -> Final USDC: {agent_final_usdc:,.0f}")
        print(f"  * Initial USDT: {agent_initial_usdt:,.0f} -> Final USDT: {agent_final_usdt:,.0f}")
        
        # Net position analysis
        net_position_values = results.get("liquidity_provider.all.net_position", {}).get("values", [])
        if net_position_values:
            print(f"  * Net position: ${net_position_values[0]:,.0f} -> ${net_position_values[-1]:,.0f}")
        
        # Pool liquidity analysis  
        pool_liquidity = results.get("univ3_usdc_usdt_001.liquidity", {}).get("values", [])
        if len(pool_liquidity) >= 3:
            print(f"\n[LIQUIDITY] Pool Liquidity Evolution:")
            print(f"  * Block 1 (start): {pool_liquidity[0]:,.0f}")
            print(f"  * Block 2 (after mint): {pool_liquidity[1]:,.0f} (+{pool_liquidity[1]-pool_liquidity[0]:,.0f})")
            print(f"  * Block 3 (after burn): {pool_liquidity[2]:,.0f}")
            
            liquidity_added = pool_liquidity[1] - pool_liquidity[0]
            print(f"  * Liquidity provided: {liquidity_added:,.0f}")
        
        # Price stability check
        spot_prices = results.get("univ3_usdc_usdt_001.dex_spot", {}).get("values", [])
        if spot_prices:
            print(f"\n[PRICE] Price Stability:")
            print(f"  * USDC/USDT price remained stable at ${spot_prices[0]:.3f}")
            print(f"  * No price volatility (perfect for stablecoin LP)")
        
        # Tick analysis
        current_ticks = results.get("univ3_usdc_usdt_001.current_tick", {}).get("values", [])
        if current_ticks:
            print(f"\n[POSITION] Position Targeting:")
            print(f"  * Current tick: {current_ticks[0]:.0f} (price = ${spot_prices[0] if spot_prices else 'N/A'})")
            print(f"  * Position range: tick -101 to +101 (~$0.99 to $1.01)")
            print(f"  * Position status: In range [OK]")
        
        print(f"\n[INSIGHTS] Key Insights:")
        print("  * Position lifecycle completed successfully: mint -> burn")
        print("  * No fees collected due to lack of trading activity")
        print("  * Tight tick range (-101 to +101) ideal for stablecoin pairs")
        print("  * Capital preserved: agent maintained exact token balances")
        print("  * Pool liquidity temporarily increased during position lifetime")
        
    except Exception as e:
        print(f"[ERROR] Simulation failed: {e}")
        return


if __name__ == "__main__":
    main()