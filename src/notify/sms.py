from typing import Dict, Union

import os
import time

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from twilio.rest import Client

from .model import Message

router = APIRouter(
    prefix="/notify/sms",
    tags=["Notify: SMS"],
    responses={404: {"description": "Not found"}},
)

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
phone_number = os.environ['TWILIO_NUMBER']



def err_response(error: Union[Dict, str]) -> JSONResponse:
    if isinstance(error, str):
        error = {'err': error}
    json_compatible_item_data = jsonable_encoder(error)
    return JSONResponse(content=json_compatible_item_data, status_code=500)


@router.post("/")
async def send(msg: Message) -> JSONResponse:
    try:
        client = Client(account_sid, auth_token)
        wait = False
        recips = msg.to if isinstance(msg.to, list) else [msg.to]

        for r in recips:
            if wait:
                time.sleep(1)
            m = client.messages.create(
                body=msg.text,
                from_=phone_number,
                to=r
            )
            wait = True

        return {"success": True}
    except Exception as error:
        return err_response(vars(error))
