from typing import Any, List, Tuple

from nqs_sdk import MutBuilderSharedState, SimulationTime
from nqs_sdk.interfaces.protocol import Protocol
from nqs_sdk.interfaces.protocol_factory import ProtocolFactory
from nqs_sdk.interfaces.tx_generator import TxGenerator


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
