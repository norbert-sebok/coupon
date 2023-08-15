import pytest

from coupons.database import DB
from coupons.use_cases import create_coupon, get_coupon_details, mark_coupon_as_taken


def test_missing_coupon():
    db = DB()
    result = get_coupon_details(db, 'missing-uuid')
    assert not result.exists


def test_mark_coupon_as_taken():
    db = DB()

    coupon = create_coupon(db=db)
    result = get_coupon_details(db, coupon.uuid)
    assert not result.coupon.taken

    mark_coupon_as_taken(db, coupon.uuid)

    result = get_coupon_details(db, coupon.uuid)
    assert result.coupon.taken

    with pytest.raises(KeyError):
        mark_coupon_as_taken(db, coupon.uuid)
