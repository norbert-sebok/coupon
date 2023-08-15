import uuid

import pytest

from coupons.database import DB
from coupons.plugins.plugins.discount import DiscountData
from coupons.plugins.plugins.user_verification import (
    UserVerificationData,
    UserVerificationRequests,
)
from coupons.plugins.registered_plugins import PluginParameters, PluginRequests
from coupons.use_cases import create_coupon, get_coupon_details


def test_discount_coupons():
    db = DB()

    coupon = create_coupon(
        db=db,
        parameters=PluginParameters(discount=DiscountData(discount_percentage=50)),
    )
    result = get_coupon_details(db, coupon.uuid)
    assert result.exists
    assert result.coupon.parameters.discount.discount_percentage == 50.0

    coupon_amount = create_coupon(
        db=db,
        parameters=PluginParameters(discount=DiscountData(discount_amount=2000)),
    )
    result = get_coupon_details(db, coupon_amount.uuid)
    assert result.exists
    assert result.coupon.parameters.discount.discount_percentage is None
    assert result.coupon.parameters.discount.discount_amount == 2000.0


def test_extra_parameter():
    db = DB()

    with pytest.raises(ValueError) as exc_info:
        create_coupon(
            db=db,
            parameters=PluginParameters(
                discount={
                    'invalid_parameter': 50,
                }
            ),
        )
    assert 'invalid_parameter\n  extra fields not permitted' in str(exc_info.value)


def test_verify_user_with_discount():
    db = DB()
    user_uuid = str(uuid.uuid4())

    coupon = create_coupon(
        db=db,
        parameters=PluginParameters(
            discount=DiscountData(discount_percentage=50),
            user_verification=UserVerificationData(for_user_uuid=user_uuid),
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
    assert result.coupon.parameters.discount.discount_percentage == 50.0
