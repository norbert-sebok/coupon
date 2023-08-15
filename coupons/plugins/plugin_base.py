from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from coupons.models import Coupon


class PluginData(BaseModel, extra='forbid'):
    pass


class Plugin:
    name = 'plugin'

    def verify_and_set(self, coupon: 'Coupon', parameters):
        raise NotImplementedError

    def verify_request(self, coupon: 'Coupon', requests) -> bool:
        return True
