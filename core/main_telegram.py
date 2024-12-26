import asyncio
from aiogram import Bot, Dispatcher, exceptions
from aiogram.fsm.storage.memory import MemoryStorage
from .telegram.core.handlers import router
from config import config


async def telegrambot():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot, skip_updates=True) #, allowed_updates=dp.resolve_used_update_types()
    except exceptions.AiogramError as e:
        print(f"Telegram Bot Error: {e}")
    

def run_telegram_bot():
    """
    Функция запуска бота Telegram
    """
    asyncio.run(telegrambot())