import configparser
import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties

from loguru import logger

from events import error_handler
from handlers import commands_handler, different_types


config = configparser.ConfigParser()
config.read("config.ini")

bot = Bot(config["SETTINGS"]["token"], default=DefaultBotProperties(parse_mode=ParseMode.HTML))
bot.config = config
bot.ADMINS_IDS = [872278858, 767922691]

dp = Dispatcher()


# --- Подгрузка модулей --- #
async def main():
    # Настройка конфигурации логгера
    logging.basicConfig(
        filename='logs/autoBot.log', 
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    logger.info("Loading modules...")
    dp.include_routers(
        error_handler.router,
        commands_handler.router,
        different_types.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    logger.success("Successfully launched")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
