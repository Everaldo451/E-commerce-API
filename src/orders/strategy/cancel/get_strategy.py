from backend.core.enums import OrderStatus

from . import CancelOrderStrategy
from .pending_status import CancelOrderPendingStrategy
from .other_status import CancelOrderOtherStatusStrategy
from .cancel_status import CancelOrderCanceledStrategy

STRATEGIES: dict[str, CancelOrderStrategy] = {
    OrderStatus.PENDING.value: CancelOrderPendingStrategy,
    OrderStatus.CANCELED.value: CancelOrderCanceledStrategy
}

def get_strategy_based_in_order_status(request, status:str) -> CancelOrderStrategy:
    strategy_class = STRATEGIES.get(status, CancelOrderOtherStatusStrategy)
    return strategy_class(request)