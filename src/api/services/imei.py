from aiohttp import ClientSession, ClientError
from loguru import logger
from fastapi import HTTPException, status, Header

from src.api.schemas.imei import (
    IMEIDeviceInfo,
    IMEICheckError,
    IMEIServicesSchema,
    IMEIAccountInfo,
)
from src.core.config import settings


class APIRequestMixin:
    @staticmethod
    def _get_headers(api_key: str) -> dict:
        """Создает стандартные заголовки для запросов."""
        return {
            "Authorization": f"Bearer {api_key}",
            "Accept-Language": "en",
            "Content-Type": "application/json",
        }

    @classmethod
    async def _make_request(
        cls,
        method: str,
        endpoint: str,
        api_key: str,
        base_url: str = settings.IMEI_CHECK_API_URL,
        json_data: dict = None,
    ) -> dict:
        async with ClientSession() as session:
            headers = cls._get_headers(api_key)
            url = f"{base_url}/{endpoint}"

            # Логируем детали запроса
            logger.info(f"Making {method} request to: {url}")
            # logger.info(f"Headers: {headers}")
            if json_data:
                logger.info(f"Request body: {json_data}")

            try:
                async with session.request(
                    method=method, url=url, headers=headers, json=json_data
                ) as response:
                    if response.status != 200:
                        logger.error(
                            f"Request failed response.text(): {await response.text()}"
                        )

                    return await response.json()

            except ClientError as e:
                logger.error(f"Request failed: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Failed to fetch services: {str(e)}",
                )


class IMEIService(APIRequestMixin):

    @classmethod
    async def get_services(
        cls, api_key: str = Header(default=settings.IMEI_CHECK_API_KEY_SANDBOX)
    ) -> dict:
        result = await cls._make_request("GET", "services", api_key=api_key)
        logger.info(f"IMEI check result type: {type(result)}: {result}")
        return result

    @classmethod
    async def check_imei(
        cls,
        imei: str,
        api_key: str = Header(default=settings.IMEI_CHECK_API_KEY_SANDBOX),
    ) -> IMEIDeviceInfo | IMEICheckError | dict:

        try:
            services = await cls.get_services(api_key)
            logger.info(f"IMEI check services: {services}")

            # Выбираем первый сервис с успешными результатами
            service_id = next(
                (
                    service["id"]
                    for service in services
                    if "successful" in service["title"].lower()
                ),
                services[0]["id"],
            )
            # service_id = services[0]["id"]

            logger.info(f"Using service {service_id}")

            check_data = {
                "deviceId": imei,
                "serviceId": service_id,
            }

            result = await cls._make_request(
                "POST", "checks", api_key=api_key, json_data=check_data
            )

            # Если в ответе есть сообщение об ошибке
            if "message" in result:
                return IMEICheckError(**result)

            # Если получены данные об устройстве
            return IMEIDeviceInfo(**result)

        except Exception as e:
            # В случае любой ошибки возвращаем IMEICheckError
            return IMEICheckError(message=str(e))

    @classmethod
    async def get_account_info(
        cls, api_key: str = Header(default=settings.IMEI_CHECK_API_KEY_SANDBOX)
    ) -> IMEIAccountInfo:
        """Получает информацию об аккаунте."""
        try:
            result = await cls._make_request("GET", "account", api_key=api_key)
            return IMEIAccountInfo(**result)
        except Exception as e:
            logger.error(f"Failed to get account info: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Failed to get account info: {str(e)}",
            )
