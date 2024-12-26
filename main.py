import logging
import threading
import asyncio
from multiprocessing import Process, Pool
from core.main_telegram import run_telegram_bot, telegrambot
from core.main_dash import run_dash  

        
def start_processes():
    """
    Запускает Telegram-бота и Dash-приложение параллельно.
    """
    # Логирование
    logging.basicConfig(level=logging.INFO)

    # Создаем два независимых процесса
    telegram_process = Process(target=run_telegram_bot, daemon=True)
    dash_process = Process(target=run_dash, daemon=True)

    # Запускаем процессы
    telegram_process.start()
    dash_process.start()

    # Логгирование информации о процессах
    logging.info(f"Telegram-bot process started with PID: {telegram_process.pid}")
    logging.info(f"Dash application process started with PID: {dash_process.pid}")

    # Ждем завершения процессов
    telegram_process.join()
    dash_process.join()

    

if __name__ == "__main__":
    start_processes()
    