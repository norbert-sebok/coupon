from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from api.database import SQLAlchemyDB
from coupons.models import CouponDetails
from coupons.plugins.registered_plugins import PluginParameters, PluginRequests
from coupons.use_cases import create_coupon, get_coupon_details, mark_coupon_as_taken

app = FastAPI()
db = SQLAlchemyDB()


@app.post("/get_coupon")
async def api_get_coupon(
    coupon_uuid: str, requests: Optional[PluginRequests]
) -> CouponDetails:
    return get_coupon_details(db, coupon_uuid, requests)


class CreateCouponRequest(BaseModel):
    parameters: Optional[PluginParameters] = None


class CreateCouponResponse(BaseModel):
    uuid: str


@app.post("/coupon")
async def api_create_coupon(request: CreateCouponRequest) -> CreateCouponResponse:
    coupon = create_coupon(db, request.parameters)
    return CreateCouponResponse(uuid=coupon.uuid)


@app.put("/coupon/taken")
async def api_mark_coupon_as_taken(coupon_uuid: str):
    try:
        mark_coupon_as_taken(db, coupon_uuid)
    except KeyError:
        raise HTTPException(status_code=404)
