from typing import TYPE_CHECKING

from coupons.plugins.plugin_base import Plugin, PluginData

if TYPE_CHECKING:
    from coupons.models import Coupon


class QueueData(PluginData):
    queue_position: int


class QueuePlugin(Plugin):
    name = 'queue'

    def verify_and_set(self, coupon: 'Coupon', parameters: QueueData):
        coupon.parameters.queue = parameters
