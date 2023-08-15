import uuid

from coupons.database import DB
from coupons.plugins.plugins.user_verification import (
    UserVerificationData,
    UserVerificationRequests,
)
from coupons.plugins.registered_plugins import PluginParameters, PluginRequests
from coupons.use_cases import create_coupon, get_coupon_details


def test_verify_user():
    db = DB()
    user_uuid = str(uuid.uuid4())

    coupon = create_coupon(
        db=db,
        parameters=PluginParameters(
            user_verification=UserVerificationData(for_user_uuid=user_uuid)
        ),
    )
    result = get_coupon_details(db, coupon.uuid)
    assert not result.exists

    result = get_coupon_details(
        db,
        coupon.uuid,
        PluginRequests(user_verification=UserVerificationRequests(user_uuid=user_uuid)),
    )
    assert result.exists
