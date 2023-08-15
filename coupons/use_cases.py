from typing import Optional
from uuid import uuid4

from .database import DB
from .models import Coupon, CouponDetails
from .plugins.registered_plugins import (
    PluginParameters,
    PluginRequests,
    registered_plugins,
)


def create_coupon(db: DB, parameters: Optional[PluginParameters] = None) -> Coupon:
    coupon = Coupon(
        uuid=str(uuid4()),
        parameters=PluginParameters(),
    )

    if parameters:
        for plugin in registered_plugins:
            attr = getattr(parameters, plugin.name)
            if attr:
                plugin.verify_and_set(coupon, attr)

    db.insert_coupon(coupon)
    return coupon


def get_coupon_details(
    db: DB, uuid: str, requests: Optional[PluginRequests] = None
) -> CouponDetails:
    coupon = db.find_coupon_by_uuid(uuid)
    if not coupon:
        return CouponDetails(exists=False)

    for plugin in registered_plugins:
        plugin_request = getattr(requests, plugin.name, None)
        if not plugin.verify_request(coupon, plugin_request):
            return CouponDetails(exists=False)

    return CouponDetails(exists=True, coupon=coupon)


def mark_coupon_as_taken(db: DB, uuid: str):
    coupon = db.find_coupon_by_uuid(uuid)
    if coupon and not coupon.taken:
        db.mark_coupon_as_taken(coupon)
    else:
        raise KeyError
