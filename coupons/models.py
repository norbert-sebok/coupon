from typing import Optional

from pydantic import BaseModel
from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel

from coupons.plugins.registered_plugins import PluginParameters


class Coupon(SQLModel, table=True):
    uuid: str = Field(primary_key=True)
    taken: bool = False
    parameters: PluginParameters = Field(sa_column=Column(JSON), default={})


class CouponDetails(BaseModel):
    exists: bool
    coupon: Optional[Coupon] = None
