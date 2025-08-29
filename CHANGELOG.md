# Changelog

All notable changes to the Python package (nqs_sdk) distributed from this repository are documented in this file.

Format: this file follows the principles of Keep a Changelog (https://keepachangelog.com/en/1.1.0/) and Semantic Versioning (https://semver.org/).

Only changes relevant to Python users are listed below (either changes in the Python bindings/package itself, or functional changes in the Rust core that are exposed to / affect Python usage).

## [0.6.8] - 2025-08-29

### Performance
- Transport-layer caching for JSON-RPC requests implemented in the Rust core, reducing repeated network calls and improving performance for Python workflows that perform many RPC queries.

### Changed
- Uniswap V3 Python and raw transaction amount handling updated to avoid floating-point approximations in computations (leveraging Decimal/integer math in the Rust core), improving numerical stability for Python users.

### Fixed
- Uniswap V3: corrected `total_holdings` aggregated observable in the Rust core; values exposed through Python metrics now accurately aggregate and report holdings.

## [0.6.7] - 2025-08-21

### Fixed
- Correct registration of transaction generators in the Coding Environment, ensuring generators are available as expected from Python.

## [0.6.6] - 2025-08-20

### Added
- Option to force observables to `float` (intended to simplify LLM-oriented workflows).
- Introduced initial "optimal allocation v0.1" capability.
- Exposed an agent protocol on the `PolicyCaller` interface.
- Uniswap V3 Python binding improvements: manual `JsonSchema` implementation for `PyUniswapV3SwapLimit` and support for a `None` variant, improving (de)serialization and type coverage.

### Changed
- Simulation time handling: removed the `set_simulation_time` call; pass simulation time during `run` instead. This may require updating existing scripts.
- Uniswap V3 interface alignment and liquidity calculation improvements; constructors adjusted for better consistency across languages.

## [0.6.5] - 2025-08-05

### Added
- Uniswap V3: `token_amounts_from_liquidity` helper to improve liquidity amount computations.

### Fixed
- Uniswap V3: refined minted amount computation and adjusted burn transaction values for correctness.

## [0.6.4] - 2025-07-29

### Added
- Python: support Decimal serialization via a custom JSON encoder.

### Changed
- Uniswap V3: fee tier handling now uses `Decimal`; accurate tick spacing computed from `fee_tier`.
- Consistent parameter naming: `block_number` replaces `blocknumber` across pools/tests and related APIs.
- Uniswap V3 transactions now use `new_with_order`; default transaction order changed to `-inf` to prioritize agent transactions.

### Removed
- Python preload mechanism for `nqs_sdk`.

### Fixed
- Uniswap V3: handle tick rounding in current price to ensure safe liquidity calculations.


Notes:
- Entries are limited to Python-facing or Python-impacting changes; internal refactors, CI, and documentation-only changes are omitted unless they alter user-visible behavior.
