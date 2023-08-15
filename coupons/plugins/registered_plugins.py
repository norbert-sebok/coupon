from typing import Optional

from pydantic import BaseModel

from coupons.plugins.plugins.discount import DiscountData, DiscountPlugin
from coupons.plugins.plugins.queue import QueueData, QueuePlugin
from coupons.plugins.plugins.user_verification import (
    UserVerificationData,
    UserVerificationPlugin,
    UserVerificationRequests,
)

registered_plugins = [
    UserVerificationPlugin(),
    DiscountPlugin(),
    QueuePlugin(),
]


class PluginRequests(BaseModel):
    user_verification: Optional[UserVerificationRequests] = None


class PluginParameters(BaseModel):
    user_verification: Optional[UserVerificationData] = None
    discount: Optional[DiscountData] = None
    queue: Optional[QueueData] = None
