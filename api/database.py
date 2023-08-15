import json
from typing import Optional

from sqlmodel import Session, SQLModel, create_engine, select

from api.config import SQLALCHEMY_ENGINE_URL
from coupons.database import DB
from coupons.models import Coupon
from coupons.plugins.registered_plugins import PluginParameters


def custom_serializer(d):
    return json.dumps(d, default=lambda v: v.json())


engine = create_engine(SQLALCHEMY_ENGINE_URL, json_serializer=custom_serializer)
SQLModel.metadata.create_all(engine)


class SQLAlchemyDB(DB):
    def insert_coupon(self, coupon: Coupon):
        save_coupon(coupon)

    def find_coupon_by_uuid(self, uuid: str) -> Optional[Coupon]:
        with Session(engine) as session:
            statement = select(Coupon).where(Coupon.uuid == uuid)
            coupon = session.exec(statement).first()

            if coupon:
                # Why SQLModel doesn't convert it automatically?
                # It should be a PluginParameters type, not str
                text: str = coupon.parameters  # type: ignore [assignment]
                coupon.parameters = PluginParameters(**json.loads(text))

            return coupon

    @classmethod
    def mark_coupon_as_taken(cls, coupon: Coupon):
        coupon.taken = True
        save_coupon(coupon)


def save_coupon(coupon: Coupon):
    with Session(engine) as session:
        session.add(coupon)
        session.commit()
        session.refresh(coupon)
