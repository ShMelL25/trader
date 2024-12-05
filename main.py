import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from core.dash_plot.app import app
from core.telegram.core.handlers import router

async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    
    
    
if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)
    #logging.basicConfig(level=logging.INFO)
    #asyncio.run(main())