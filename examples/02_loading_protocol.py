import nqs_sdk.preload  # noqa: F401
from nqs_sdk.core.protocol_manager import ProtocolManager
from nqs_sdk.core.protocol_registry.registry import ProtocolRegistry

# Load directly from registry
factory = ProtocolRegistry.get_factory("nqs_sdk::compound_v2")

# Or using ProtocolManager
protocol = ProtocolManager("nqs_sdk::compound_v2")
