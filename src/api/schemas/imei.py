from typing import Optional

from pydantic import BaseModel, Field


class IMEICheckRequest(BaseModel):
    imei: str = Field(..., min_length=8, max_length=15)
    token: str


class IMEIDeviceInfo(BaseModel):
    id: str
    type: str
    status: str
    orderId: Optional[str] = None
    service: dict
    amount: str
    deviceId: str
    processedAt: int
    properties: dict
    imei: Optional[str] = None

    def __init__(self, **data):
        # Если imei нет, используйте deviceId
        if "imei" not in data:
            data["imei"] = data.get("deviceId")
        super().__init__(**data)


class IMEICheckResponse(BaseModel):
    status: str
    device_data: IMEIDeviceInfo


class IMEICheckError(BaseModel):
    message: str


class IMEIServiceItem(BaseModel):
    id: int
    title: str
    price: str


IMEIServicesSchema = list[IMEIServiceItem]


class IMEIAccountInfo(BaseModel):
    balance: str
    warning: Optional[str] = Field(None, alias="!!! WARNING !!!")
