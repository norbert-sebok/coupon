from typing import Dict, Optional

from coupons.models import Coupon


class DB:
    coupons: Dict[str, Coupon]

    def __init__(self):
        self.coupons = {}

    def insert_coupon(self, coupon: Coupon):
        self.coupons[coupon.uuid] = coupon

    def find_coupon_by_uuid(self, uuid: str) -> Optional[Coupon]:
        return self.coupons.get(uuid)

    @classmethod
    def mark_coupon_as_taken(cls, coupon: Coupon):
        coupon.taken = True
