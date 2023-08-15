from typing import TYPE_CHECKING, Optional

from coupons.plugins.plugin_base import Plugin, PluginData

if TYPE_CHECKING:
    from coupons.models import Coupon


class UserVerificationRequests(PluginData):
    user_uuid: str


class UserVerificationData(PluginData):
    for_user_uuid: str


class UserVerificationPlugin(Plugin):
    name = 'user_verification'

    def verify_and_set(self, coupon: 'Coupon', parameters: UserVerificationData):
        coupon.parameters.user_verification = parameters

    def verify_request(
        self, coupon: 'Coupon', requests: Optional[UserVerificationRequests]
    ) -> bool:
        params = coupon.parameters.user_verification
        if not params:
            return True

        if requests:
            return requests.user_uuid == params.for_user_uuid
        else:
            return False
