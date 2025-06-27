# Getting Started

**Nuant Quantitative System SDK** is a purpose-built SDK for decentralized finance. It enables a unified lifecycle that supports research, protocol-level simulation, backtesting, optimization, and live monitoring. Designed to empower quants, researchers, and developers, NQS makes it easy to experiment, iterate, and bring DeFi protocols and strategies from concept to execution.

This repository is the public endpoint for the nqs-sdk package, available on PyPI, providing all the tools needed to build, test, and run strategies within a single, integrated environment.

## Prerequisites

Before installing the NQS SDK, ensure you have:

- Python 3.12 (currently supported version; more versions coming soon)
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

This following command creates a `nuant-quantlib.toml` file with the required proxy configuration for accessing Nuant’s GraphQL API.
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
import nqs_sdk.preload  # noqa: F401 # should be always on top
from nqs_sdk import Simulation, ProtocolManager
import json

# Create protocol managers
uniswap = ProtocolManager("uniswap_v3_rust")

# Initialize simulation with protocols and configuration
# You can use the example config or create your own with create_config.py
sim = Simulation([uniswap], "./examples/configs/basic_config.yml")

# Run the simulation
all_observables_str = sim.run() # this intermediate step will be fixed soon
all_observables = json.loads(all_observables_str)

# Access results
print(f"Simulation completed with {len(all_observables)} observables")
```

### Getting Involved

- **Documentation**: [https://nuant.github.io/nqs-sdk/](https://nuant.github.io/nqs-sdk/)
- **GitHub Issues**: [https://github.com/Nuant/nqs-sdk/issues](https://github.com/Nuant/nqs-sdk/issues)
- **Contact**: Contact us to [thelab@nuant.ai](mailto:thelab@nuant.ai) for joining us on private Telegram channel
- **Examples**: Explore practical implementations in the [examples](https://github.com/Nuant/nqs-sdk/tree/master/examples) directory. [JSON schemas](https://github.com/Nuant/nqs-sdk/tree/master/examples/configs/schemas) are provided to ensure proper format and validation.

## Next Steps

Now that you have the NQS SDK installed and understand the basics, you might want to:

1. **Explore Core Concepts** - Learn about the fundamental architecture and components ([Core Concepts](core_concepts.md))
2. **Study How to Build** - Dive deeper into configuration and practical examples ([Build](build.md))
3. **Check the API Reference** - Detailed documentation of all classes and methods ([API Reference](api_reference.md))
4. **Join the Community** - Connect with other users and contributors
5. **Contribute** - Help improve the NQS SDK by reporting issues or submitting pull requests

## Known issues and roadmap

Coming soon:

- Programmatic API to manage simulation and backtest directly in Python
- API stabilisation

And later:

- Compound V2 support, more protocols will follow
- EVM based *any* protocol executions

Known issues:

- Support of Python 3.13
- Improve protocol naming to reflect implementation variants (e.g. uniswap_v3_rust)
- Replace default String sim.run() output by a native Python dict
