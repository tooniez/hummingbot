from __future__ import annotations

from decimal import Decimal
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict

from hummingbot.core.data_type.common import OrderType, TradeType
from hummingbot.strategy_v2.executors.data_types import ExecutorConfigBase


class TrailingStop(BaseModel):
    activation_price: Decimal
    trailing_delta: Decimal


class TripleBarrierConfig(BaseModel):
    stop_loss: Optional[Decimal] = None
    take_profit: Optional[Decimal] = None
    time_limit: Optional[int] = None
    trailing_stop: Optional[TrailingStop] = None
    open_order_type: OrderType = OrderType.LIMIT
    take_profit_order_type: OrderType = OrderType.MARKET
    stop_loss_order_type: OrderType = OrderType.MARKET
    time_limit_order_type: OrderType = OrderType.MARKET
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def new_instance_with_adjusted_volatility(self, volatility_factor: float) -> TripleBarrierConfig:
        new_trailing_stop = None
        if self.trailing_stop is not None:
            new_trailing_stop = TrailingStop(
                activation_price=self.trailing_stop.activation_price * Decimal(volatility_factor),
                trailing_delta=self.trailing_stop.trailing_delta * Decimal(volatility_factor)
            )

        return TripleBarrierConfig(
            stop_loss=self.stop_loss * Decimal(volatility_factor) if self.stop_loss is not None else None,
            take_profit=self.take_profit * Decimal(volatility_factor) if self.take_profit is not None else None,
            time_limit=self.time_limit,
            trailing_stop=new_trailing_stop,
            open_order_type=self.open_order_type,
            take_profit_order_type=self.take_profit_order_type,
            stop_loss_order_type=self.stop_loss_order_type,
            time_limit_order_type=self.time_limit_order_type
        )


class PositionExecutorConfig(ExecutorConfigBase):
    type: Literal["position_executor"] = "position_executor"
    trading_pair: str
    connector_name: str
    side: TradeType
    entry_price: Optional[Decimal] = None
    amount: Decimal
    triple_barrier_config: TripleBarrierConfig = TripleBarrierConfig()
    leverage: int = 1
    activation_bounds: Optional[List[Decimal]] = None
    level_id: Optional[str] = None
    model_config = ConfigDict(arbitrary_types_allowed=True)
