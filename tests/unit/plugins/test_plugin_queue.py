

from coupons.database import DB
from coupons.plugins.plugins.queue import QueueData
from coupons.plugins.registered_plugins import PluginParameters
from coupons.use_cases import create_coupon, get_coupon_details


def test_queue_coupons():
    db = DB()

    coupon = create_coupon(
        db=db,
        parameters=PluginParameters(queue=QueueData(queue_position=0)),
    )
    result = get_coupon_details(db, coupon.uuid)
    assert result.exists
    assert result.coupon.parameters.queue.queue_position == 0
