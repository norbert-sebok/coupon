from typing import TYPE_CHECKING, Optional

from coupons.plugins.plugin_base import Plugin, PluginData

if TYPE_CHECKING:
    from coupons.models import Coupon


class DiscountData(PluginData):
    discount_percentage: Optional[float]
    discount_amount: Optional[float]


class DiscountPlugin(Plugin):
    name = 'discount'

    def verify_and_set(self, coupon: 'Coupon', parameters: DiscountData):
        coupon.parameters.discount = parameters
