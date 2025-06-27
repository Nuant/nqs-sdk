import nqs_sdk.preload  # noqa: F401
from nqs_sdk.core.protocol_registry.discovery import print_protocol_info

# List all protocols
print_protocol_info()

# Get details for a specific protocol
print_protocol_info("uniswap_v3_rust")
