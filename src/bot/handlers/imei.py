from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger

from src.api.controllers.imei import IMEIService
from src.core.config import settings

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Добро пожаловать в IMEI Checker Bot!\nВведите IMEI для проверки."
    )


@router.message(F.text)
async def check_imei(message: Message):
    imei = message.text.strip()
    try:
        imei_service = IMEIService()
        result = await imei_service.check_imei(
            message.text,
            api_key=settings.IMEI_CHECK_API_KEY_LIVE,
        )
        logger.info(f"IMEI check result: {result.model_dump()}")
        response_text = result.model_dump()
        await message.answer(str(response_text))

    except Exception as e:
        logger.error(f"Error checking IMEI {imei}^ ")
