from typing import Any, List, Tuple

from nqs_pycore import MutBuilderSharedState, SimulationTime

from nqs_sdk.core.protocol_registry.decorators import protocol_factory
from nqs_sdk.interfaces.protocol import Protocol
from nqs_sdk.interfaces.protocol_factory import ProtocolFactory
from nqs_sdk.interfaces.tx_generator import TxGenerator


@protocol_factory(description="My custom AMM protocol", version="0.1.0", author="Developer Name")
class MyProtocolFactory(ProtocolFactory):
    def id(self) -> str:
        return "my_custom_protocol"

    def build(
        self,
        time: SimulationTime,
        builder_state: MutBuilderSharedState,
        common_config: Any,
        backtest: bool,
        config: Any,
    ) -> Tuple[List[Protocol], List[TxGenerator]]:
        return ([], [])
