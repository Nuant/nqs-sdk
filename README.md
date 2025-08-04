WARNING: original source file is docs/getting_started.rst

# Getting Started

**Nuant Quantitative System SDK** is a purpose-built SDK for decentralized finance. It enables a unified lifecycle that supports research, protocol-level simulation, backtesting, optimization, and live monitoring. Designed to empower quants, researchers, and developers, NQS makes it easy to experiment, iterate, and bring DeFi protocols and strategies from concept to execution.

This repository is the public endpoint for the nqs-sdk package, available on PyPI, providing all the tools needed to build, test, and run strategies within a single, integrated environment.

For additional examples and tests, please visit the companion repository at [https://github.com/Nuant/nqs-sdk-extension/](https://github.com/Nuant/nqs-sdk-extension/).

## Prerequisites

Before installing the NQS SDK, ensure you have:

- Python 3.12 or 3.13
- pip package manager

## Installation

Install the NQS SDK using pip:

```bash
pip install nqs-sdk
```

Note: This installation will also include several other packages provided by Nuant.

### Environment Configuration

Get your API key from

<a href="https://agents.nuant.ai/subscribe" target="_blank" rel="noopener noreferrer">https://agents.nuant.ai/subscribe</a>

The following command creates a `nuant-quantlib.toml` file with the required proxy configuration for accessing Nuant’s GraphQL API.
Make sure to replace `YOUR_API_KEY`.

```bash
(
echo "[proxy]"
echo 'url = "https://data.app.nuant.com/graphql"'
echo 'api-key = "YOUR_API_KEY" # <- the one, you got previously'
) > nuant-quantlib.toml
```

Then, export it as an environment variable:

```bash
export QUANTLIB_CONFIG=/path/to/nuant-quantlib.toml
```

### Verify Installation

First, verify that the installation was successful:

```python
import nqs_sdk
print(f"NQS SDK version: {nqs_sdk.__version__}")
```

## Quick Start

### Basic Use Case

Here’s a simple example to get you started with the NQS SDK:

```python
from nqs_sdk import Simulation
from nqs_sdk.protocols import UniswapV3Factory
import json

# Initialize simulation with protocols and configuration
uniswap_v3 = UniswapV3Factory() # factory for all UniswapV3 instances
sim = Simulation([uniswap_v3], "./examples/configs/basic_config.yml")

# Run the simulation
all_observables = sim.run()

# Access results
print(f"Simulation completed with {len(all_observables)} observables")
```

Tips:

- By default, the execution is quiet, and you can make it verbose to watch the execution flow.
- Data queries to feed the simulation can be expensive; consider setting the quantlib cache to make it faster.

for both, see [Useful environment variables]() section below.

### Getting Involved

- **Documentation**: [https://nuant.github.io/nqs-sdk/](https://nuant.github.io/nqs-sdk/)
  > - [Explore Core Concepts](https://nuant.github.io/nqs-sdk/core_concepts.html) - Learn about the fundamental architecture and components
  > - [Study How to Build](https://nuant.github.io/nqs-sdk/build.html) - Dive deeper into configuration and practical examples
  > - [Check the API Reference](https://nuant.github.io/nqs-sdk/api_reference.html) - Detailed documentation of all classes and methods
- **GitHub Issues**: [https://github.com/Nuant/nqs-sdk/issues](https://github.com/Nuant/nqs-sdk/issues)
- **Contact**: Contact us to [thelab@nuant.ai](mailto:thelab@nuant.ai) for joining us on private Telegram channel
- **Examples**: Explore practical implementations in the [examples](https://github.com/Nuant/nqs-sdk/tree/master/examples) directory. [JSON schemas](https://github.com/Nuant/nqs-sdk/tree/master/examples/configs/schemas) are provided to ensure proper format and validation.

Now that you have the NQS SDK installed and understand the basics, you might want to:

## Known issues and roadmap

Coming soon:

- API stabilisation
- API examples with arbitrageur or other multi-agent scenarios

And later:

- Compound V2 support, more protocols will follow
- Open Rust API to extend core interfaces directly in Rust
- API for external data provider

  (Currently, the NQS SDK uses quantlib and data.app.nuant.com for data handling.)
- EVM based *any* protocol executions

Known issues:

- Support of Python 3.11
- Support of Linux arm64

### Useful environment variables

| Variable name     | Example               | Description                                                                                          |
|-------------------|-----------------------|------------------------------------------------------------------------------------------------------|
| `QUANTLIB_CONFIG` | `nuant-quantlib.toml` | Path to a config file in TOML format                                                                 |
| `QUANTLIB_CACHE`  | `./your_dir/.cache`   | Cache directory to optimize quantlib calls<br/><br/><br/>(be sure to create the directory)<br/><br/> |
| `RUST_LOG`        | `debug`               | Configure the log level of core engine                                                               |

For more environment variables, see [Environment variables](https://nuant.github.io/nqs-sdk/environment_variables.html)
