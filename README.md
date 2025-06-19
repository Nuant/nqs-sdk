# Nuant Quantitative System SDK

The Nuant Quantitative System (NQS) SDK is a Python package that provides tools and utilities for quantitative analysis. 
This repository serves as a public endpoint for the `nqs-sdk` package, which is published on PyPI.

## Installation

You can install the NQS SDK using pip:

```bash
pip install nqs-sdk
```

NB: currently, we only support Python 3.12 for Linux x64, Windows x64 and macOS arm64 and x64.

## Usage

Here's a simple example of how to use the NQS SDK:

```python
import nqs_sdk

# Basic usage example
# For more detailed examples, see the examples directory
```

To run any simulation requiring onchain data, you need a config file referenced by the environment variable
`QUANTLIB_CONFIG`:

```toml
[proxy]
url = "https://data.app.nuant.com/graphql"
api-key = "<your-api-key>"
```

To speed up and minimize data queries, you can define the `QUANTLIB_CACHE_DIR` environment variable to reference an
existing directory that will be used for caching.

## Examples

Check out the [examples](./examples) directory for more detailed usage examples.

## Documentation

For detailed documentation, please refer to the [docs](./docs) directory:

- [Getting Started Guide](./docs/getting_started.md)
- [FAQ](./docs/faq.md)
- [Examples](./examples)

## Reporting Issues

If you encounter any issues or bugs, please report them by creating an issue in this repository. When reporting an
issue, please include:

1. A clear and descriptive title
2. Steps to reproduce the issue
3. Expected behavior
4. Actual behavior
5. Any error messages or logs
6. Your environment (OS, Python version, nqs-sdk version)

## License

This project is licensed under the License - see the [LICENSE](./LICENSE) file for details.

## Contact

For additional support or questions, please [contact us](mailto:thelab@nuant.ai).
