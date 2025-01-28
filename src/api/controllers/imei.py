from typing import Union

from fastapi import APIRouter, Header

from src.api.services.imei import IMEIService
from src.api.schemas.imei import (
    IMEICheckRequest,
    IMEICheckResponse,
    IMEICheckError,
    IMEIServiceItem,
    IMEIDeviceInfo,
    IMEIAccountInfo,
)
from src.core.logger import logger
from src.core.config import settings


router = APIRouter(
    tags=["IMEI"],
)


@router.post(
    "/api/check-imei", response_model=Union[IMEICheckError, IMEICheckResponse, dict]
)
async def check_imei(
    request: IMEICheckRequest,
    api_key: str = Header(default=settings.IMEI_CHECK_API_KEY_SANDBOX),
):

    imei_service = IMEIService()
    result = await imei_service.check_imei(request.imei, api_key)

    # logger.info(f"IMEI check result: {result.model_dump()}")
    logger.info(f"IMEI check result: {result}")

    if isinstance(result, IMEICheckError):
        return result.model_dump()

    if isinstance(result, dict):
        try:
            result = IMEIDeviceInfo(**result)
        except Exception as e:
            logger.error(f"Error parsing IMEI check result: {result}")
            return IMEICheckError(message=str(e)).model_dump()

    return IMEICheckResponse(status=result.status, device_data=result).model_dump()


@router.get("/api/services", response_model=list[IMEIServiceItem])
async def get_services(
    api_key: str = Header(default=settings.IMEI_CHECK_API_KEY_SANDBOX),
):
    imei_service = IMEIService()
    imei_services = await imei_service.get_services(api_key)
    logger.info(f"List of IMEI services: {imei_services}")
    return imei_services


@router.get("/api/account", response_model=IMEIAccountInfo)
async def get_account_info(
    api_key: str = Header(default=settings.IMEI_CHECK_API_KEY_SANDBOX),
):
    imei_service = IMEIService()
    account_info = await imei_service.get_account_info(api_key)
    logger.info(f"Account info: {account_info}")
    return account_info
